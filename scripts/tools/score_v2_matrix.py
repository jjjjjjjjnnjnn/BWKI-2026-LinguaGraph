#!/usr/bin/env python3
"""Deterministic Harness-v2 scoring (zero API).

Pairs each v2 cell file against its archival v1 (P0) control, same 92 IDs.
Inputs: research/mimo_spark_replication/t2_*.json (v1) + t2_v2-*.json (v2).
Outputs: research/mimo_spark_replication/V2_MATRIX.json + V2_MATRIX.md
Methods: A2 fails-as-0/92, bootstrap B=1000 seed 20260918 (same as v1).
"""
import json
import os
import random
import re

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REP = os.path.join(BASE, "research", "mimo_spark_replication")
SEED = 20260918
B = 1000
# (v1label, v1file, v2ns-prefix, model)
ARMS = [
    ("glm-5.2-r4", "t2_sn-glm-5.2.json", "v2-glm52r4"),
    ("deepseek-v4.1-flash-r4", "t2_r4-deepseek-v4.1-flash.json", "v2-ds41f"),
    ("sensenova-6.8-flash-lite", "t2_sn-sensenova-6.8-flash-lite.json", "v2-sn68"),
    ("big-pickle-free", "t2_v2-bigpickle-P0.json", "v2-bigpickle"),
]
CELLS = ["P1", "P2", "P3"]
# P0 drift calibration files (P0 cell, stratified subsets; paired vs v1 same IDs)
P0CAL = [
    ("glm-5.2-r4", "t2_sn-glm-5.2.json", "t2_v2-glm52r4-P0cal.json"),
    ("deepseek-v4.1-flash-r4", "t2_r4-deepseek-v4.1-flash.json", "t2_v2-ds41f-P0cal.json"),
    ("sensenova-6.8-flash-lite", "t2_sn-sensenova-6.8-flash-lite.json", "t2_v2-sn68-P0cal.json"),
]


def bootstrap_ci(vals, seed=SEED, b=B):
    rng = random.Random(seed)
    n = len(vals)
    if n == 0:
        return [0.0, 0.0]
    means = []
    for _ in range(b):
        means.append(sum(rng.choice(vals) for _ in range(n)) / n)
    means.sort()
    return [round(means[int(0.025 * b)], 4), round(means[int(0.975 * b) - 1], 4)]


def is_cjk(s):
    return bool(re.search(r"[\u4e00-\u9fff]", s or ""))


def summarize(items):
    f1 = [r["f1"] if r.get("valid") else 0.0 for r in items]
    soc = [r["f1"] if (r.get("valid") and r.get("annotator") == "auto_accepted") else 0.0
           for r in items if r.get("annotator") == "auto_accepted"]
    pred = [len(r.get("predicted", [])) for r in items if r.get("valid")]
    en = [r for r in items if r.get("valid") and r.get("language") == "en"]
    en_tot = sum(len(r.get("predicted", [])) for r in en)
    langs = {}
    for lang in ("zh", "de", "en"):
        v = [r["f1"] if r.get("valid") else 0.0 for r in items if r.get("language") == lang]
        langs[lang] = {"n": len(v), "mean": round(sum(v) / len(v), 4) if v else 0.0,
                       "ci": bootstrap_ci(v)}
    return {"n": len(items), "valid": sum(1 for r in items if r.get("valid")),
            "f1": round(sum(f1) / len(f1), 4), "ci": bootstrap_ci(f1),
            "social": round(sum(soc) / len(soc), 4) if soc else 0.0,
            "pred_n": round(sum(pred) / len(pred), 2) if pred else 0.0,
            "en_cjk": round(sum(1 for r in en for c in r.get("predicted", []) if is_cjk(c)) / max(en_tot, 1), 4),
            "langs": langs}


def main():
    rows, pairs, drift = {}, {}, {}
    for label, v1fn, prefix in ARMS:
        v1 = json.load(open(os.path.join(REP, v1fn), encoding="utf-8"))
        v1map = {r["sample_id"]: (r["f1"] if r.get("valid") else 0.0) for r in v1["items"]}
        rows[label + "-P0"] = summarize(v1["items"])
        for cell in CELLS:
            fp = os.path.join(REP, "t2_%s-%s.json" % (prefix, cell))
            if not os.path.exists(fp):
                continue
            d = json.load(open(fp, encoding="utf-8"))
            assert d.get("cell", cell) == cell, "cell mismatch %s" % fp
            rows[label + "-" + cell] = summarize(d["items"])
            common = [r["sample_id"] for r in d["items"] if r["sample_id"] in v1map]
            dd = [(r["f1"] if r.get("valid") else 0.0) - v1map[r["sample_id"]]
                  for r in d["items"] if r["sample_id"] in v1map]
            pairs["%s %s-P0" % (label, cell)] = {
                "mean_d": round(sum(dd) / len(dd), 4), "ci": bootstrap_ci(dd), "n": len(dd)}
    L = ["# Harness v2 Matrix (deterministic, zero API)", "",
         "A2 fails-as-0/92. CI = bootstrap 95% (B=1000, seed 20260918).",
         "Drift = P0-cal rerun vs v1 same IDs (~0 = no transport drift).",
         "", "## Cells", "",
         "| arm-cell | n/valid | F1 | CI | social | pred_n | EN-CJK | zh/de/en |",
         "|---|---|---|---|---|---|---|---|"]
    for k, r in rows.items():
        L.append("| %s | %d/%d | %.4f | %s | %.4f | %.1f | %.4f | %.3f/%.3f/%.3f |" % (
            k, r["n"], r["valid"], r["f1"], r["ci"], r["social"], r["pred_n"],
            r["en_cjk"], r["langs"]["zh"]["mean"], r["langs"]["de"]["mean"], r["langs"]["en"]["mean"]))
    L += ["", "## Paired vs archival P0", "",
          "| contrast | mean_d | 95%CI | 0 in CI? |", "|---|---|---|---|"]
    for k, v in pairs.items():
        L.append("| %s | %.4f | %s | %s |" % (k, v["mean_d"], v["ci"], v["ci"][0] <= 0 <= v["ci"][1]))
    L += ["", "## P0 drift calibration (same IDs, P0 cell rerun; ~0 = no transport drift)", "",
          "| arm | n | mean_d | 95%CI |", "|---|---|---|---|"]
    for label, v1fn, calfn in P0CAL:
        v1 = json.load(open(os.path.join(REP, v1fn), encoding="utf-8"))
        v1map = {r["sample_id"]: (r["f1"] if r.get("valid") else 0.0) for r in v1["items"]}
        cal = json.load(open(os.path.join(REP, calfn), encoding="utf-8"))
        dd = [(r["f1"] if r.get("valid") else 0.0) - v1map[r["sample_id"]]
              for r in cal["items"] if r["sample_id"] in v1map]
        drift[label] = {"mean_d": round(sum(dd) / len(dd), 4),
                        "ci": bootstrap_ci(dd), "n": len(dd)}
        L.append("| %s | %d | %.4f | %s |" % (label, len(dd), drift[label]["mean_d"], drift[label]["ci"]))
    json.dump({"seed": SEED, "B": B, "rows": rows, "paired": pairs, "drift": drift},
              open(os.path.join(REP, "V2_MATRIX.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    open(os.path.join(REP, "V2_MATRIX.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    for k, v in pairs.items():
        print("%s d=%.4f CI=%s" % (k, v["mean_d"], v["ci"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
