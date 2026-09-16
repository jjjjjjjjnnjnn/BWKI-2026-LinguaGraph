#!/usr/bin/env python3
"""R5-B: thr sensitivity recomputation for consensus v4 (offline, no API).

Reuses loaders/normalization from consensus_vote_v2 (import only, no side
effects), rebuilds per-file source sets identically, then recomputes the vote
at thr shifts -1/0/+1 (thr = n//2+1+shift, floor 1).

Outputs:
  research/thr_sensitivity_v4_20260916.json  (per-shift totals + per-file rows)
  research/thr_sensitivity_v4_20260916.md    (thr-group table + Solid<=1 list)

Self-check gate: shift=0 MUST reproduce consensus_v4 totals
  (accepted 546 / solid 203 / weak 884 / hypo 1905 / mimo_only 70),
  else exit 3 and write nothing.
Usage: python scripts/tools/thr_sensitivity_v4.py [--help]
Writes ONLY under research/.
"""
import argparse
import itertools
import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts" / "tools"))
import consensus_vote_v2 as cv2  # noqa: E402  (helpers only; main() not called)

EXPECTED = {"accepted": 546, "solid": 203, "weak": 884, "hypo": 1905, "mimo_only": 70}


def load_all(root):
    mimo_dir = root / "data" / "math_extractions"
    spark_dir = root / "research" / "mimo_spark_audit"
    bailian_dir = root / "research" / "bailian_audit"
    ens_dir = root / "research" / "ensemble_v2"
    depth24 = json.loads((ens_dir / "depth24.json").read_text(encoding="utf-8"))["depth24"]
    mimo_c, mimo_r = {}, {}
    for b in depth24:
        fp = mimo_dir / f"{b}.json"
        if fp.is_file():
            c_raw, r_raw = cv2.load_mimo(fp)
            if c_raw is not None:
                mimo_c[b] = cv2.concept_set(c_raw)
                mimo_r[b] = cv2.rel_pairs(r_raw)
    spark_c, spark_r = {}, {}
    for p in spark_dir.glob("*.audit.json"):
        b = p.name[: -len(".audit.json")]
        c_raw, r_raw = cv2.load_spark_audit(p)
        if c_raw is not None:
            spark_c[b] = cv2.concept_set(c_raw)
            spark_r[b] = cv2.rel_pairs(r_raw)
    bailian_c, bailian_r = {}, {}
    for p in bailian_dir.glob("*.bailian.json"):
        b = p.name[: -len(".bailian.json")]
        c_raw, r_raw = cv2.load_bailian(p)
        if c_raw is not None:
            bailian_c[b] = cv2.concept_set(c_raw)
            bailian_r[b] = cv2.rel_pairs(r_raw)
    run_pat = re.compile(r"^(.*)\.r([123])\.json$")
    ens_runs = {m: {} for m in cv2.MODELS}
    for m in cv2.MODELS:
        d = ens_dir / m
        if not d.is_dir():
            continue
        for f in d.glob("*.json"):
            if f.name.startswith("_"):
                continue
            mm = run_pat.match(f.name)
            if not mm:
                continue
            b, rn = mm.group(1), mm.group(2)
            c_raw, r_raw = cv2.load_ensemble_run(f)
            if c_raw is None:
                continue
            ens_runs[m].setdefault(b, {})[rn] = (cv2.concept_set(c_raw), cv2.rel_pairs(r_raw))
    rep_c, rep_r = {m: {} for m in cv2.MODELS}, {m: {} for m in cv2.MODELS}
    for m in cv2.MODELS:
        for b, runs in ens_runs[m].items():
            for rn in ("1", "2", "3"):
                if rn in runs:
                    rep_c[m][b] = runs[rn][0]
                    rep_r[m][b] = runs[rn][1]
                    break
    return depth24, mimo_c, mimo_r, spark_c, spark_r, bailian_c, bailian_r, rep_c, rep_r


def vote_at(depth24, mimo_c, mimo_r, spark_c, spark_r, bailian_c, bailian_r,
            rep_c, rep_r, shift):
    files, totals = [], {"accepted": 0, "solid": 0, "weak": 0, "hypo": 0, "mimo_only": 0}
    for b in depth24:
        order, src_c, src_r = [], {}, {}
        if b in mimo_c:
            order.append("mimo")
            src_c["mimo"], src_r["mimo"] = mimo_c[b], mimo_r.get(b, set())
        if b in spark_c:
            order.append("spark")
            src_c["spark"], src_r["spark"] = spark_c[b], spark_r.get(b, set())
        if b in bailian_c:
            order.append("bailian")
            src_c["bailian"], src_r["bailian"] = bailian_c[b], bailian_r.get(b, set())
        for m in cv2.MODELS:
            if b in rep_c[m]:
                order.append(m)
                src_c[m], src_r[m] = rep_c[m][b], rep_r[m].get(b, set())
        n = len(order)
        thr = max(1, n // 2 + 1 + shift) if n else 0
        csup, rsup = {}, {}
        for s, cs in src_c.items():
            for nn in cs:
                csup.setdefault(nn, set()).add(s)
        for s, rs in src_r.items():
            for pr in rs:
                rsup.setdefault(pr, set()).add(s)
        acc = sum(1 for ss in csup.values() if len(ss) >= thr) if thr else 0
        mo = sum(1 for ss in csup.values() if ss == {"mimo"})
        so = sum(1 for ss in rsup.values() if len(ss) >= thr) if thr else 0
        hy = sum(1 for ss in rsup.values() if len(ss) == 1)
        we = sum(1 for ss in rsup.values() if 1 < len(ss) < thr)
        totals["accepted"] += acc
        totals["solid"] += so
        totals["weak"] += we
        totals["hypo"] += hy
        totals["mimo_only"] += mo
        files.append({"basename": b, "n_sources": n, "threshold": thr,
                      "accepted": acc, "solid": so, "weak": we, "hypo": hy,
                      "mimo_only": mo, "sources": order})
    return files, totals


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: thr_sensitivity_v4.py [--help]")
        print("  Offline thr±1 vote recomputation. Writes research/thr_sensitivity_v4_20260916.json/.md.")
        return 0
    root = BASE_DIR
    out_j = root / "research" / "thr_sensitivity_v4_20260916.json"
    out_m = root / "research" / "thr_sensitivity_v4_20260916.md"
    data = load_all(root)
    shifts = {}
    for sh in (-1, 0, 1):
        files, totals = vote_at(*data, sh)
        shifts[str(sh)] = {"totals": totals, "files": files}
    got = shifts["0"]["totals"]
    if any(got[k] != v for k, v in EXPECTED.items()):
        print("SELF_CHECK_FAIL: shift=0 gives %s, expected %s" % (got, EXPECTED))
        return 3
    print("SELF_CHECK_OK shift=0 reproduces v4 totals")
    # thr-group aggregation at shift 0 (actual thresholds, no forcing)
    groups = {}
    for f in shifts["0"]["files"]:
        g = groups.setdefault(f["threshold"], {"n_files": 0, "accepted": 0, "solid": 0,
                                               "weak": 0, "hypo": 0, "files": []})
        g["n_files"] += 1
        for k in ("accepted", "solid", "weak", "hypo"):
            g[k] += f[k]
        g["files"].append(f["basename"])
    thin = sorted([f for f in shifts["0"]["files"] if f["solid"] <= 1],
                  key=lambda f: (f["solid"], f["basename"]))
    json.dump({"meta": {"shifts": [-1, 0, 1], "rule": "thr = n//2+1+shift (floor 1)",
                        "self_check": "shift=0 reproduces consensus_v4 totals"},
               "shifts": {k: {"totals": v["totals"]} for k, v in shifts.items()},
               "shift0_files": shifts["0"]["files"],
               "thr_groups_shift0": {str(t): {k: v for k, v in g.items()}
                                     for t, g in sorted(groups.items())},
               "solid_le1_files": thin},
              open(out_j, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    L = ["# R5-B thr 敏感性（v4，2026-09-16，离线重算）",
         "",
         "> 方法：复用 `consensus_vote_v2` 载入/归一化，原样重建源集，thr=n//2+1+shift（下限 1）重投。",
         "> 自检门：shift=0 精确复现 v4 总数（540→**546**/194→**203**/736→**884**/1710→**1905**/73→**70**），否则拒写。",
         "",
         "## thr±1 漂移",
         "",
         "| shift | 收录 | Solid | Weak | Hypo | mimo独有 |",
         "|---|---|---|---|---|---|"]
    for sh in ("-1", "0", "1"):
        t = shifts[sh]["totals"]
        L.append("| %+d | %d | %d | %d | %d | %d |" % (
            int(sh), t["accepted"], t["solid"], t["weak"], t["hypo"], t["mimo_only"]))
    L += ["",
          "## shift=0 的实际 thr 分组（v4 无 thr=4，实为 thr 5/6；R5 旧定义已修正）",
          "",
          "| thr | 文件数 | 收录 | Solid | Weak | Hypo |",
          "|---|---|---|---|---|---|"]
    for t in sorted(groups):
        g = groups[t]
        L.append("| %d | %d | %d | %d | %d | %d |" % (
            t, g["n_files"], g["accepted"], g["solid"], g["weak"], g["hypo"]))
    L += ["", "## Solid≤1 文件单列（R5 要求）", "",
          "| basename | n源 | thr | 收录 | Solid | Weak | Hypo |",
          "|---|---|---|---|---|---|---|"]
    for f in thin:
        L.append("| %s | %d | %d | %d | %d | %d | %d |" % (
            f["basename"], f["n_sources"], f["threshold"], f["accepted"],
            f["solid"], f["weak"], f["hypo"]))
    L += ["",
          "## 解读（只许快照口径）",
          "- thr+1：收录/Solid 收缩、Hypo 膨胀（门槛提高挡出低 support）；thr−1 反之。",
          "- 分组与单列证明总数为混合刻度加总：在 L1（thr 敏感性表入库）前，总数禁报 headline。",
          ""]
    open(out_m, "w", encoding="utf-8").write("\n".join(L))
    print("wrote thr_sensitivity_v4_20260916.json/.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
