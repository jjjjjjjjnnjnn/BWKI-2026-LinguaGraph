#!/usr/bin/env python3
"""REAUDIT 2026-09-19 (D-V11): concept-level T1 agreement.

Read-only inputs: research/ensemble_v2/<ns>/<base>.r1.json + data/math_extractions/<base>.json
Outputs (NEW, frozen originals untouched):
  research/mimo_spark_replication/T1_AGREEMENT_reaudit_20260919.json/.md
Method fix vs score_t1_agreement.py: each CONCEPT counts once (name-or-alias
cross-match), instead of expanding every alias into an independent key
(which inflates inter/n_new/n_ref by alias count).
Zero API. Deterministic.
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REP = os.path.join(BASE, "research", "mimo_spark_replication")
ENS = os.path.join(BASE, "research", "ensemble_v2")
MEX = os.path.join(BASE, "data", "math_extractions")
ARMS = ["muse-spark-1.3-contributor-free", "muse-spark-1.2-contributor-free",
        "mm-minimax-m3", "r4-deepseek-v4.1-flash",
        "sn-sensenova-6.7-flash-lite", "sn-deepseek-v4-flash", "sn-glm-5.2",
        "sn-sensenova-6.8-flash-lite",
        "sn-deepseek-v4-pro", "sn-kimi-k3", "sn-sensenova-u1.5-fast"]
TAG = "reaudit_20260919"


def norm(s):
    return "".join(str(s).lower().split()).replace("-", "").replace("_", "").replace("\u00df", "ss")


def ckeys(c):
    if not isinstance(c, dict):
        return set()
    ks = {norm(c.get("name", ""))}
    for a in c.get("aliases", []) or []:
        if a:
            ks.add(norm(a))
    ks.discard("")
    return ks


def agree_concept(new_cs, ref_cs):
    nk = [ckeys(c) for c in new_cs if isinstance(c, dict)]
    rk = [ckeys(c) for c in ref_cs if isinstance(c, dict)]
    ref_union, new_union = set().union(*rk) if rk else set(), set().union(*nk) if nk else set()
    nm = sum(1 for k in nk if k & ref_union)
    rm = sum(1 for k in rk if k & new_union)
    return (nm / max(len(nk), 1), rm / max(len(rk), 1),
            nm, rm, len(nk), len(rk))


def main():
    table = {}
    for arm in ARMS:
        ddir = os.path.join(ENS, arm)
        if not os.path.isdir(ddir):
            table[arm] = {"n": 0, "status": "missing (not run or archived)"}
            continue
        files = sorted(f for f in os.listdir(ddir) if f.endswith(".r1.json"))
        rows = []
        for f in files:
            b = f[:-8]
            try:
                new = json.load(open(os.path.join(ddir, f), encoding="utf-8"))
                ref = json.load(open(os.path.join(MEX, b + ".json"), encoding="utf-8"))
            except Exception as e:
                rows.append({"base": b, "error": "%s" % type(e).__name__})
                continue
            nc = (new.get("parsed") or new).get("extracted_concepts", [])
            rc = ref.get("extracted_concepts", [])
            p, r, nm, rm, nn, rn = agree_concept(nc, rc)
            rows.append({"base": b, "p": round(p, 4), "r": round(r, 4),
                         "n_matched_new": nm, "n_matched_ref": rm,
                         "n_new": nn, "n_ref": rn})
        ok = [x for x in rows if "error" not in x]
        table[arm] = {
            "n": len(ok),
            "micro_p": round(sum(x["n_matched_new"] for x in ok) / max(sum(x["n_new"] for x in ok), 1), 4),
            "micro_r": round(sum(x["n_matched_ref"] for x in ok) / max(sum(x["n_ref"] for x in ok), 1), 4),
            "rows": rows,
        }
    json.dump(table, open(os.path.join(REP, "T1_AGREEMENT_%s.json" % TAG), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    L = ["# T1 Agreement REAUDIT 2026-09-19 (concept-level; frozen T1_AGREEMENT.json untouched)", "",
         "Method: each concept counts once (name-or-alias cross-match). "
         "Original expanded every alias into an independent key (alias-count inflation).",
         "",
         "| arm | files | micro-P | micro-R |",
         "|---|---|---|---|"]
    for arm, t in table.items():
        if t.get("status", "").startswith("missing") or t.get("n", -1) == 0:
            L.append("| %s | %d | missing/partial | |" % (arm, t.get("n", 0)))
            continue
        L.append("| %s | %d | %.4f | %.4f |" % (arm, t["n"], t["micro_p"], t["micro_r"]))
    open(os.path.join(REP, "T1_AGREEMENT_%s.md" % TAG), "w",
         encoding="utf-8").write("\n".join(L) + "\n")
    for arm, t in table.items():
        if t.get("status", "").startswith("missing") or t.get("n", -1) == 0:
            print("%s MISSING/EMPTY" % arm)
            continue
        print("%s micro-P/R=%.3f/%.3f" % (arm, t["micro_p"], t["micro_r"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
