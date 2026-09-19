#!/usr/bin/env python3
"""Deterministic T2 matrix scoring (zero API).

Inputs: research/mimo_spark_replication/t2_*.json (6 complete, parked/incomplete excluded) +
  data/model_comparison/qwen-plus_results.json / qwen-max_results.json.
Outputs: research/mimo_spark_replication/T2_MATRIX.json + T2_MATRIX.md
Methods: subset means (frozen), bootstrap 95% CI (B=1000, seed 20260918),
  cardinality stats, script-mismatch rate (exploratory).
"""
import json
import os
import random

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REP = os.path.join(BASE, "research", "mimo_spark_replication")
T2_FILES = {
    "muse-spark-1.3-free": "t2_muse-spark-1.3-contributor-free.json",
    "muse-spark-1.2-free": "t2_muse-spark-1.2-contributor-free.json",
    "minimax-m3": "t2_mm-minimax-m3.json",
    "deepseek-v4.1-flash-r4": "t2_r4-deepseek-v4.1-flash.json",
    "sensenova-6.8-flash-lite": "t2_sn-sensenova-6.8-flash-lite.json",
    "glm-5.2-r4": "t2_sn-glm-5.2.json",
}
# NOTE 2026-09-18: sn-6.7 parked/incomplete (excluded); mimo archived (excluded).
HIST = {
    "qwen-plus (Bailian hist)": os.path.join(BASE, "data", "model_comparison", "qwen-plus_results.json"),
    "qwen-max (Bailian hist)": os.path.join(BASE, "data", "model_comparison", "qwen-max_results.json"),
}
SEED = 20260918
B = 1000


def is_cjk(s):
    return any("\u4e00" <= ch <= "\u9fff" for ch in s)


def load_t2(fn):
    d = json.load(open(os.path.join(REP, fn), encoding="utf-8"))
    return d


def summarize(items):
    valid = [r for r in items if r.get("valid") or r.get("f1", 0) > 0 or True]
    return valid


def subset_mean(items, fn):
    s = [r["f1"] for r in items if fn(r)]
    return {"n": len(s), "mean_f1": round(sum(s) / len(s), 4)} if s else {"n": 0}


def bootstrap_ci(vals, seed=SEED, b=B):
    # REAUDIT 2026-09-19 known limitation (frozen; do NOT "fix" without full refreeze):
    # fresh Random(seed) per call → all arms/cells share identical resample indices (CIs correlated);
    # upper index int(0.975*B)-1 = 974 (0-based should be 975) → systematically slightly narrow.
    rng = random.Random(seed)
    n = len(vals)
    if n == 0:
        return [0.0, 0.0]
    means = []
    for _ in range(b):
        means.append(sum(rng.choice(vals) for _ in range(n)) / n)
    means.sort()
    return [round(means[int(0.025 * b)], 4), round(means[int(0.975 * b) - 1], 4)]


def main():
    rows = {}
    # new arms
    for label, fn in T2_FILES.items():
        d = load_t2(fn)
        items = [r for r in d["items"] if r.get("valid")]
        f1s = [r["f1"] for r in items]
        # A2-compliant (D-S6): fails count in denominator — F1 over all 92 gold IDs, invalid=0
        f1_n92 = [r["f1"] if r.get("valid") else 0.0 for r in d["items"]]
        # REAUDIT 2026-09-19 (D-V11, verified): denominator below is the 72 social gold IDs
        # (every arm file carries 92/92 items WITH annotator; soc_n=72) with invalid→0,
        # i.e. this IS true A2-social. The name "soc_n92" is misleading (not /92);
        # T2_MATRIX.md social column shows valid-only "social_f1" — see Nenner-Hinweis there.
        soc_n92 = [r["f1"] if (r.get("valid") and r.get("annotator") == "auto_accepted") else 0.0
                   for r in d["items"] if r.get("annotator") == "auto_accepted"]
        soc = [r["f1"] for r in items if r.get("annotator") == "auto_accepted"]
        math = [r["f1"] for r in items if r.get("annotator") == "annotator_1"]
        pred_n = [len(r.get("predicted", [])) for r in items]
        gold_n = [r.get("gold_n", 0) for r in items]
        en_items = [r for r in items if r.get("language") == "en"]
        de_items = [r for r in items if r.get("language") == "de"]
        en_cjk = sum(1 for r in en_items for c in r.get("predicted", []) if is_cjk(c))
        en_tot = sum(len(r.get("predicted", [])) for r in en_items)
        de_cjk = sum(1 for r in de_items for c in r.get("predicted", []) if is_cjk(c))
        de_tot = sum(len(r.get("predicted", [])) for r in de_items)
        rows[label] = {
            "endpoint": d.get("transport", ""), "model": d.get("model", ""),
            "n": len(items),
            "mean_p": round(sum(r["p"] for r in items) / len(items), 4),
            "mean_r": round(sum(r["r"] for r in items) / len(items), 4),
            "mean_f1": round(sum(f1s) / len(f1s), 4),
            "ci95_overall": bootstrap_ci(f1s),
            "mean_f1_n92": round(sum(f1_n92) / len(f1_n92), 4),
            "ci95_n92": bootstrap_ci(f1_n92),
            "social_f1_n92": round(sum(soc_n92) / len(soc_n92), 4) if soc_n92 else 0.0,
            "social_f1": round(sum(soc) / len(soc), 4) if soc else 0.0,
            "ci95_social": bootstrap_ci(soc),
            "math_f1": round(sum(math) / len(math), 4) if math else 0.0,
            "ci95_math": bootstrap_ci(math),
            "pred_n_mean": round(sum(pred_n) / len(pred_n), 2),
            "gold_n_mean": round(sum(gold_n) / len(gold_n), 2),
            "en_cjk_frac": round(en_cjk / max(en_tot, 1), 4),
            "de_cjk_frac": round(de_cjk / max(de_tot, 1), 4),
            "rung": d.get("rung_counts", {}),
            "failed": d.get("failed_items", []),
            "subsets": d.get("subsets", {}),
        }
    # history arms (per-item P/R/F1 present; annotator/language absent -> join via gold file)
    gold = json.load(open(os.path.join(BASE, "data", "gold", "gold_dataset.json"), encoding="utf-8"))
    gmap = {g.get("sample_id"): g for g in gold}
    for label, fp in HIST.items():
        d = json.load(open(fp, encoding="utf-8"))
        items = d.get("results", d.get("items", []))
        recs = []
        for r in items:
            g = gmap.get(r.get("sample_id"), {})
            recs.append({"f1": r.get("f1", 0), "p": r.get("precision", 0), "r": r.get("recall", 0),
                         "annotator": g.get("annotator", ""),
                         "language": g.get("language", r.get("language", "")),
                         "pred_n": len(r.get("predicted_concepts", [])),
                         "gold_n": len(r.get("gold_concepts", []))})
        f1s = [r["f1"] for r in recs]
        soc = [r["f1"] for r in recs if r["annotator"] == "auto_accepted"]
        math = [r["f1"] for r in recs if r["annotator"] == "annotator_1"]
        rows[label] = {
            "endpoint": "Bailian history (see G3 note for path details)",
            "n": len(recs),
            "mean_p": round(sum(r["p"] for r in recs) / len(recs), 4),
            "mean_r": round(sum(r["r"] for r in recs) / len(recs), 4),
            "mean_f1": round(sum(f1s) / len(f1s), 4),
            "ci95_overall": bootstrap_ci(f1s),
            "social_f1": round(sum(soc) / len(soc), 4) if soc else 0.0,
            "ci95_social": bootstrap_ci(soc),
            "math_f1": round(sum(math) / len(math), 4) if math else 0.0,
            "ci95_math": bootstrap_ci(math),
            "pred_n_mean": round(sum(r["pred_n"] for r in recs) / len(recs), 2),
            "gold_n_mean": round(sum(r["gold_n"] for r in recs) / len(recs), 2),
            "en_cjk_frac": None, "de_cjk_frac": None,
        }
    json.dump({"seed": SEED, "B": B, "rows": rows},
              open(os.path.join(REP, "T2_MATRIX.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    L = ["# T2 Matrix (deterministic, zero API)", "",
         "CI = bootstrap 95% (B=1000, seed 20260918). "
         "en/de_cjk_frac = fraction of predicted names containing CJK (exploratory).",
         "F1_n92 = A2-compliant primary (fails as 0 over all 92 gold IDs, D-S6); "
         "F1 = valid-only secondary.",
         "",
         "| model | n | P | R | F1 | 95%CI | F1_n92 | 95%CI_n92 | social | math | pred_n/gold_n |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for label, r in rows.items():
        L.append("| %s | %d | %.4f | %.4f | %.4f | %s | %.4f | %s | %.4f | %.4f | %.1f/%.1f |" % (
            label, r["n"], r["mean_p"], r["mean_r"], r["mean_f1"],
            r["ci95_overall"], r.get("mean_f1_n92", r["mean_f1"]),
            r.get("ci95_n92", r["ci95_overall"]), r["social_f1"], r["math_f1"],
            r["pred_n_mean"], r["gold_n_mean"]))
    L += ["",
          "## Script-mismatch (exploratory)",
          "| model | EN predicted CJK-frac | DE predicted CJK-frac |",
          "|---|---|---|"]
    for label, r in rows.items():
        if r["en_cjk_frac"] is not None:
            L.append("| %s | %.4f | %.4f |" % (label, r["en_cjk_frac"], r["de_cjk_frac"]))
    open(os.path.join(REP, "T2_MATRIX.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    for label, r in rows.items():
        print("%s F1=%.4f CI=%s F1_n92=%.4f CI_n92=%s social=%.4f math=%.4f P/R=%.3f/%.3f pred_n=%.1f" % (
            label, r["mean_f1"], r["ci95_overall"], r.get("mean_f1_n92", r["mean_f1"]),
            r.get("ci95_n92", r["ci95_overall"]), r["social_f1"], r["math_f1"],
            r["mean_p"], r["mean_r"], r["pred_n_mean"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
