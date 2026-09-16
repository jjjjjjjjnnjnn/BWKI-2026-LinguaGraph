#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多源共识投票 v2（离线计算，不调 API）。

只读输入：
  data/math_extractions/<base>.json                    (mimo: extracted_concepts/extracted_relations)
  research/mimo_spark_audit/<base>.audit.json          (spark: spark_concepts/spark_relations，12 个)
  research/ensemble_v2/<model>/<base>.rN.json          (7 模型 ensemble；有多少算多少，缺席=missing 不计分)
  research/bailian_audit/<base>.bailian.json           (bailian parsed；0 个则该源缺席)
  research/ensemble_v2/depth24.json                    (深度 24 名单)
只写输出（research/ 下）：
  research/consensus_v2_20260914.json
  research/consensus_v2_20260914.md
不改 data/，不写其他目录。

计算（概念归一化一律：小写 + 去全部空白）：
  1) intra-model 自一致性：每模型有 >=2 runs 的文件，全部两两 run 概念 Jaccard 均值；分模型聚合=文件均值的均值。
  2) inter-model：深度 24 文件上两两模型概念 Jaccard 矩阵（各模型代表 run 取 r1，缺则 r2/r3）；
     每对模型=两模型共存文件的 Jaccard 均值；矩阵均值=全部非对角对的均值。
  3) vs mimo：各模型代表 run vs mimo 概念 Jaccard（深度 24 上共存文件：分文件 + 聚合均值）。
  4) 多数表决 v2（深度 24 文件）：每文件可用源 = mimo + spark(如有 audit) + bailian(如有)
     + 7 模型代表 run(如有)；概念 support>=阈值=收录，关系有序端点对(忽略 type)support>=阈值=Solid，
     support==1=Hypothetical，其余=Weak(2..阈值-1)，sources=={mimo}=mimo 独有候选删。
     阈值=“≥半数”按严格多数实现：thr = n//2 + 1（与 v1 一致：2 源需 2，3 源需 2）。

用法: python -B scripts/tools/consensus_vote_v2.py [--out-json research/consensus_v2_20260914.json --out-md research/consensus_v2_20260914.md]
"""
import argparse
import itertools
import json
import re
from pathlib import Path

DATE_TAG = "20260914"
OUT_JSON_DEFAULT = f"research/consensus_v2_{DATE_TAG}.json"
OUT_MD_DEFAULT = f"research/consensus_v2_{DATE_TAG}.md"

MODELS = [
    "deepseek-v4-pro-0813",
    "deepseek-v4.1-flash",
    "kimi-k3",
    "qwen3.7-flash",
    "qwen3.8-27b",
    "qwen3.8-max",
    "qwen3.8-max-0902",
]


def norm(s) -> str:
    return re.sub(r"\s+", "", str(s if s is not None else "").lower())


def concept_name(item) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        for k in ("name", "concept", "entity", "label", "text"):
            v = item.get(k)
            if isinstance(v, str) and v.strip():
                return v
        return ""
    return str(item)


def endpoint_name(v) -> str:
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        for k in ("name", "concept", "entity", "label", "text"):
            x = v.get(k)
            if isinstance(x, str) and x.strip():
                return x
        return ""
    return str(v) if v is not None else ""


def concept_set(raw_list) -> set:
    out = set()
    for item in raw_list or []:
        n = norm(concept_name(item))
        if n:
            out.add(n)
    return out


def rel_pairs(raw_list) -> set:
    out = set()
    for r in raw_list or []:
        if not isinstance(r, dict):
            continue
        ns, nt = norm(endpoint_name(r.get("source", ""))), norm(endpoint_name(r.get("target", "")))
        if ns and nt:
            out.add((ns, nt))
    return out


def jaccard(a: set, b: set):
    if not a and not b:
        return 1.0
    u = a | b
    if not u:
        return 1.0
    return len(a & b) / len(u)


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else None


def r4(x):
    return None if x is None else round(float(x), 4)


def load_concepts_relations_standard(d: dict):
    """mimo/ensemble 通用：优先 parsed，其次顶层；缺键=解析失败 -> None。"""
    if not isinstance(d, dict):
        return None, None
    parsed = d.get("parsed", None)
    holder = parsed if isinstance(parsed, dict) else d
    c = holder.get("extracted_concepts", None)
    r = holder.get("extracted_relations", None)
    if c is None:
        for k in ("concepts", "concepts_list"):
            if isinstance(holder.get(k), list):
                c = holder[k]
                break
    if r is None:
        for k in ("relations", "relations_list"):
            if isinstance(holder.get(k), list):
                r = holder[k]
                break
    if c is None and r is None:
        return None, None
    return (c or []), (r or [])


def load_mimo(fp: Path):
    try:
        d = json.loads(fp.read_text(encoding="utf-8"))
    except Exception:
        return None, None
    c = d.get("extracted_concepts", None)
    r = d.get("extracted_relations", None)
    if c is None and r is None:
        return None, None
    return (c or []), (r or [])


def load_spark_audit(fp: Path):
    try:
        d = json.loads(fp.read_text(encoding="utf-8"))
    except Exception:
        return None, None
    c = d.get("spark_concepts", None)
    r = d.get("spark_relations", None)
    if c is None and r is None:
        return None, None
    return (c or []), (r or [])


def load_bailian(fp: Path):
    try:
        d = json.loads(fp.read_text(encoding="utf-8"))
    except Exception:
        return None, None
    return load_concepts_relations_standard(d)


def load_ensemble_run(fp: Path):
    try:
        d = json.loads(fp.read_text(encoding="utf-8"))
    except Exception:
        return None, None
    return load_concepts_relations_standard(d)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-json", default=OUT_JSON_DEFAULT)
    ap.add_argument("--out-md", default=OUT_MD_DEFAULT)
    a = ap.parse_args()

    root = Path(__file__).resolve().parent.parent.parent
    mimo_dir = root / "data" / "math_extractions"
    spark_dir = root / "research" / "mimo_spark_audit"
    bailian_dir = root / "research" / "bailian_audit"
    ens_dir = root / "research" / "ensemble_v2"

    out_json = (root / a.out_json).resolve()
    out_md = (root / a.out_md).resolve()
    for p in (out_json, out_md):
        if p.parent != root / "research":
            raise SystemExit(f"refuse to write outside research/: {p}")

    depth24 = json.loads((ens_dir / "depth24.json").read_text(encoding="utf-8"))["depth24"]

    # ---- 载入 mimo / spark / bailian（概念集 + 关系对）----
    mimo_c, mimo_r = {}, {}
    for b in depth24:
        fp = mimo_dir / f"{b}.json"
        if fp.is_file():
            c_raw, r_raw = load_mimo(fp)
            if c_raw is not None:
                mimo_c[b] = concept_set(c_raw)
                mimo_r[b] = rel_pairs(r_raw)

    spark_c, spark_r, spark_bases = {}, {}, set()
    for p in spark_dir.glob("*.audit.json"):
        b = p.name[: -len(".audit.json")]
        c_raw, r_raw = load_spark_audit(p)
        if c_raw is not None:
            spark_c[b] = concept_set(c_raw)
            spark_r[b] = rel_pairs(r_raw)
            spark_bases.add(b)

    bailian_c, bailian_bases = {}, set()
    bailian_r = {}
    for p in bailian_dir.glob("*.bailian.json"):
        b = p.name[: -len(".bailian.json")]
        c_raw, r_raw = load_bailian(p)
        if c_raw is not None:
            bailian_c[b] = concept_set(c_raw)
            bailian_r[b] = rel_pairs(r_raw)
            bailian_bases.add(b)

    # ---- 载入 ensemble：model -> base -> {run: (cset, rset)} ----
    ens_runs = {m: {} for m in MODELS}  # m -> b -> {"1": (cs, rs), ...}
    run_pat = re.compile(r"^(.*)\.r([123])\.json$")
    for m in MODELS:
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
            c_raw, r_raw = load_ensemble_run(f)
            if c_raw is None:
                continue  # 解析失败=missing，不计分
            ens_runs[m].setdefault(b, {})[rn] = (concept_set(c_raw), rel_pairs(r_raw))

    # 代表 run：r1 优先，缺用 r2/r3
    rep_c, rep_r = {m: {} for m in MODELS}, {m: {} for m in MODELS}
    rep_which = {m: {} for m in MODELS}
    for m in MODELS:
        for b, runs in ens_runs[m].items():
            for rn in ("1", "2", "3"):
                if rn in runs:
                    rep_c[m][b] = runs[rn][0]
                    rep_r[m][b] = runs[rn][1]
                    rep_which[m][b] = rn
                    break

    # ============ 1) intra-model 自一致性 ============
    intra = {}
    for m in MODELS:
        per_file = {}
        for b, runs in ens_runs[m].items():
            if len(runs) >= 2:
                sets = [runs[rn][0] for rn in sorted(runs)]
                js = [jaccard(x, y) for x, y in itertools.combinations(sets, 2)]
                per_file[b] = mean(js)
        intra[m] = {"n_files": len(per_file), "mean": mean(per_file.values()), "files": per_file}

    # ============ 2) inter-model（深度24，代表 run） ============
    inter_pairs = {}
    for ma, mb in itertools.combinations(MODELS, 2):
        common = [b for b in depth24 if b in rep_c[ma] and b in rep_c[mb]]
        js = [jaccard(rep_c[ma][b], rep_c[mb][b]) for b in common]
        inter_pairs[f"{ma}||{mb}"] = {"n": len(common), "mean": mean(js),
                                      "files": {b: jaccard(rep_c[ma][b], rep_c[mb][b]) for b in common}}
    inter_global = mean([v["mean"] for v in inter_pairs.values() if v["mean"] is not None])
    inter_per_model = {}
    for m in MODELS:
        vals = [v["mean"] for k, v in inter_pairs.items() if m in k.split("||") and v["mean"] is not None]
        inter_per_model[m] = mean(vals)

    # ============ 3) vs mimo（深度24） ============
    vs_mimo = {}
    for m in MODELS:
        per_file = {}
        for b in depth24:
            if b in rep_c[m] and b in mimo_c:
                per_file[b] = jaccard(rep_c[m][b], mimo_c[b])
        vs_mimo[m] = {"n": len(per_file), "mean": mean(per_file.values()), "files": per_file}

    # ============ 4) 多数表决 v2（深度24） ============
    vote_files = []
    tot_accepted = tot_solid = tot_hypo = tot_weak = tot_mimo_only = 0
    for b in depth24:
        # 可用源（有序，mimo 先）
        src_csets, src_rsets, disp_c, disp_r = {}, {}, {}, {}
        order = []
        if b in mimo_c:
            order.append("mimo")
            src_csets["mimo"] = mimo_c[b]
            src_rsets["mimo"] = mimo_r.get(b, set())
        if b in spark_c:
            order.append("spark")
            src_csets["spark"] = spark_c[b]
            src_rsets["spark"] = spark_r.get(b, set())
        if b in bailian_c:
            order.append("bailian")
            src_csets["bailian"] = bailian_c[b]
            src_rsets["bailian"] = bailian_r.get(b, set())
        for m in MODELS:
            if b in rep_c[m]:
                order.append(m)
                src_csets[m] = rep_c[m][b]
                src_rsets[m] = rep_r[m].get(b, set())
        n_src = len(order)
        thr = n_src // 2 + 1 if n_src else 0
        # display 名（首见原文）
        cmap: dict = {}
        for s in order:
            raw_lists = {"mimo": None, "spark": None, "bailian": None}
            # 为 display 回读原文名：仅 mimo/spark/bailian/ensemble 代表 run 文件
            cands = []
            if s == "mimo":
                d = json.loads((mimo_dir / f"{b}.json").read_text(encoding="utf-8"))
                cands = d.get("extracted_concepts", []) or []
            elif s == "spark":
                d = json.loads((spark_dir / f"{b}.audit.json").read_text(encoding="utf-8"))
                cands = d.get("spark_concepts", []) or []
            elif s == "bailian":
                d = json.loads((bailian_dir / f"{b}.bailian.json").read_text(encoding="utf-8"))
                p = d.get("parsed", d) if isinstance(d, dict) else {}
                cands = (p.get("extracted_concepts", []) or []) if isinstance(p, dict) else []
            else:
                rn = rep_which[s][b]
                d = json.loads((ens_dir / s / f"{b}.r{rn}.json").read_text(encoding="utf-8"))
                holder = d.get("parsed", d) if isinstance(d, dict) else {}
                cands = (holder.get("extracted_concepts", []) or []) if isinstance(holder, dict) else []
            for item in cands:
                nm = concept_name(item)
                nn = norm(nm)
                if nn and nn in src_csets[s] and nn not in disp_c:
                    disp_c[nn] = nm.strip()
        # 概念 support
        csup: dict = {}
        for s, cs in src_csets.items():
            for nn in cs:
                csup.setdefault(nn, set()).add(s)
        accepted = sorted([nn for nn, ss in csup.items() if len(ss) >= thr]) if thr else []
        mimo_only = sorted([nn for nn, ss in csup.items() if ss == {"mimo"}])
        # 关系 support（有序端点对，忽略 type）
        rsup: dict = {}
        for s, rs in src_rsets.items():
            for pr in rs:
                rsup.setdefault(pr, set()).add(s)
        solid = sorted([list(k) for k, ss in rsup.items() if len(ss) >= thr]) if thr else []
        hypo = sorted([list(k) for k, ss in rsup.items() if len(ss) == 1])
        weak = sorted([list(k) for k, ss in rsup.items() if 1 < len(ss) < thr])
        tot_accepted += len(accepted)
        tot_solid += len(solid)
        tot_hypo += len(hypo)
        tot_weak += len(weak)
        tot_mimo_only += len(mimo_only)
        vote_files.append({
            "basename": b,
            "n_sources": n_src,
            "sources": order,
            "threshold": thr,
            "counts": {
                "mimo_concepts": len(src_csets.get("mimo", set())),
                "spark_concepts": len(src_csets.get("spark", set())),
                "bailian_concepts": len(src_csets.get("bailian", set())),
                "accepted_concepts": len(accepted),
                "mimo_only_review": len(mimo_only),
                "solid": len(solid),
                "weak": len(weak),
                "hypothetical": len(hypo),
                **{f"{m}_concepts": len(src_csets[m]) if m in src_csets else None for m in MODELS},
            },
            "accepted_concepts": [
                {"norm": nn, "display": disp_c.get(nn, nn), "sources": sorted(csup[nn]), "support": len(csup[nn])}
                for nn in accepted
            ],
            "mimo_only_review": [{"norm": nn, "display": disp_c.get(nn, nn)} for nn in mimo_only],
            "solid_relations": [
                {"source_norm": p[0], "target_norm": p[1], "sources": sorted(rsup[(p[0], p[1])]),
                 "support": len(rsup[(p[0], p[1])])} for p in solid
            ],
        })

    coverage = {}
    for m in MODELS:
        depth_done = sum(1 for b in depth24 if b in rep_c[m])
        coverage[m] = {
            "depth_done": depth_done,
            "depth_missing": len(depth24) - depth_done,
            "rep_r1": sum(1 for b in depth24 if rep_which[m].get(b) == "1"),
            "rep_fallback_r2_r3": sum(1 for b in depth24 if b in rep_which[m] and rep_which[m][b] in ("2", "3")),
            "total_bases": len(ens_runs[m]),
            "total_runs": sum(len(v) for v in ens_runs[m].values()),
        }

    payload = {
        "meta": {
            "date": DATE_TAG,
            "offline": True,
            "method": "归一化=小写+去全部空白；Jaccard=|交|/|并(空空=1.0)；"
                      "intra=每模型>=2runs文件的两两run概念Jaccard均值再按文件平均；"
                      "inter=深度24上代表run(r1缺则r2/r3)两两模型共存文件Jaccard均值；"
                      "vs_mimo=代表run vs mimo概念Jaccard；"
                      "vote v2=深度24每文件可用源严格多数thr=n//2+1：概念support>=thr收录，"
                      "关系有序端点对support>=thr=Solid，==1=Hypothetical，中间=Weak，sources=={mimo}=候选删",
            "inputs": ["data/math_extractions/<base>.json",
                       "research/mimo_spark_audit/<base>.audit.json",
                       "research/ensemble_v2/<model>/<base>.rN.json",
                       "research/bailian_audit/<base>.bailian.json",
                       "research/ensemble_v2/depth24.json"],
            "models": MODELS,
            "depth24": depth24,
            "n_depth": len(depth24),
            "n_spark_audit_total": len(spark_bases),
            "n_spark_audit_in_depth": sum(1 for b in depth24 if b in spark_bases),
            "n_bailian_files": len(bailian_bases),
            "mimo_in_depth": sum(1 for b in depth24 if b in mimo_c),
        },
        "coverage": coverage,
        "intra": {m: {"n_files": v["n_files"], "mean": r4(v["mean"]),
                      "files": {b: r4(x) for b, x in v["files"].items()}} for m, v in intra.items()},
        "inter": {"pairs": {k: {"n": v["n"], "mean": r4(v["mean"]),
                                "files": {b: r4(x) for b, x in v["files"].items()}}
                            for k, v in inter_pairs.items()},
                  "global_mean": r4(inter_global),
                  "per_model_mean": {m: r4(x) for m, x in inter_per_model.items()}},
        "vs_mimo": {m: {"n": v["n"], "mean": r4(v["mean"]),
                        "files": {b: r4(x) for b, x in v["files"].items()}} for m, v in vs_mimo.items()},
        "vote": {
            "threshold_rule": "thr = n_sources//2 + 1",
            "totals": {"accepted_concepts": tot_accepted, "solid_relations": tot_solid,
                       "weak_relations": tot_weak, "hypothetical_relations": tot_hypo,
                       "mimo_only_review": tot_mimo_only},
            "files": vote_files,
        },
    }

    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- MD ----
    L = [f"# 多源共识投票 v2 {DATE_TAG}", "",
         "离线计算，不调 API。归一化=小写+去全部空白；Jaccard=|交|/|并|（空空=1.0）。"
         "intra=每模型≥2 runs 文件的两两 run 概念 Jaccard 均值再按文件平均；"
         "inter=深度 24 上代表 run（r1，缺则 r2/r3）两两模型共存文件均值；"
         "vs mimo=代表 run vs mimo 概念 Jaccard；"
         "表决 v2=深度 24 每文件可用源严格多数（thr=n//2+1）：概念≥thr 收录，关系≥thr=Solid，==1=Hypothetical，中间=Weak，mimo 独有=候选删。", "",
         f"输入：mimo `{len(mimo_c)}/24`（深度内）+ spark audit `{len(spark_bases)}` 个（深度内 `{sum(1 for b in depth24 if b in spark_bases)}`）"
         f"+ ensemble 7 模型 + bailian `*.bailian.json` `{len(bailian_bases)}` 个（缺席，missing 不计分）"
         "；缺席一律不计分。", ""]
    L += ["## 覆盖表（深度 24）", "",
          "| 模型 | done | 缺席 | 代表run r1 | 回退r2/r3 | intra_n | intra 均值 | vs_mimo_n | vs_mimo 均值 | inter 行均值 |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for m in MODELS:
        c = coverage[m]
        L.append(f"| {m} | {c['depth_done']} | {c['depth_missing']} | {c['rep_r1']} | {c['rep_fallback_r2_r3']} | "
                 f"{intra[m]['n_files']} | {r4(intra[m]['mean'])} | {vs_mimo[m]['n']} | {r4(vs_mimo[m]['mean'])} | "
                 f"{r4(inter_per_model[m])} |")
    L += ["", f"mimo 深度覆盖：{sum(1 for b in depth24 if b in mimo_c)}/24；"
              f"spark audit 深度覆盖：{sum(1 for b in depth24 if b in spark_bases)}/24；"
              f"bailian：{len(bailian_bases)}（无 `*.bailian.json`，全部缺席）。", ""]
    L += ["## 1) intra-model 自一致性（概念 Jaccard）", "",
          "| 模型 | 文件数(≥2runs) | 均值 |",
          "|---|---:|---:|"]
    for m in MODELS:
        L.append(f"| {m} | {intra[m]['n_files']} | {r4(intra[m]['mean'])} |")
    L += ["", "## 2) inter-model 矩阵（深度 24，代表 run，概念 Jaccard；括号=n 共存文件）", "",
          "|  | " + " | ".join(MODELS) + " |",
          "|---|" + "---|" * len(MODELS)]
    for ma in MODELS:
        row = [ma]
        for mb in MODELS:
            if ma == mb:
                row.append("1.0000")
            else:
                k = f"{ma}||{mb}" if f"{ma}||{mb}" in inter_pairs else f"{mb}||{ma}"
                v = inter_pairs[k]
                row.append(f"{r4(v['mean'])} ({v['n']})" if v["mean"] is not None else "missing (0)")
        L.append("| " + " | ".join(row) + " |")
    L += ["", f"矩阵均值（非对角 21 对的均值）：**{r4(inter_global)}**。", ""]
    L += ["## 3) vs mimo（概念 Jaccard，深度 24 共存文件）", "",
          "| 模型 | n | 均值 |",
          "|---|---:|---:|"]
    for m in MODELS:
        L.append(f"| {m} | {vs_mimo[m]['n']} | {r4(vs_mimo[m]['mean'])} |")
    L += ["",
          "## 4) 多数表决 v2（深度 24，thr=n//2+1）", "",
          f"- 收录概念：**{tot_accepted}**；Solid 关系：**{tot_solid}**；"
          f"Weak 关系（2..thr-1）：**{tot_weak}**；Hypothetical（1 源）：**{tot_hypo}**；"
          f"候选删（mimo 独有）：**{tot_mimo_only}**。", "",
          "| basename | 源数 | 阈值 | 收录概念 | 候选删 | Solid | Weak | Hypo | 源列表 |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    for f in vote_files:
        cc = f["counts"]
        L.append(f"| {f['basename']} | {f['n_sources']} | {f['threshold']} | {cc['accepted_concepts']} | "
                 f"{cc['mimo_only_review']} | {cc['solid']} | {cc['weak']} | {cc['hypothetical']} | "
                 f"{'+'.join(f['sources'])} |")
    L += ["", f"明细见 `{OUT_JSON_DEFAULT}`。", ""]
    out_md.write_text("\n".join(L), encoding="utf-8")

    print(f"intra: " + "; ".join(f"{m}={r4(intra[m]['mean'])} (n={intra[m]['n_files']})" for m in MODELS))
    print(f"inter_global={r4(inter_global)}")
    print("vs_mimo: " + "; ".join(f"{m}={r4(vs_mimo[m]['mean'])} (n={vs_mimo[m]['n']})" for m in MODELS))
    print(f"vote: accepted={tot_accepted} solid={tot_solid} weak={tot_weak} hypo={tot_hypo} mimo_only={tot_mimo_only}")
    print(f"wrote {out_json.name} + {out_md.name}")


if __name__ == "__main__":
    main()
