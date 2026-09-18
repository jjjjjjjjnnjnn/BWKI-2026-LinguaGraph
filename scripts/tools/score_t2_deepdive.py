#!/usr/bin/env python3
"""Deterministic T2 deep-dive (zero API, zero human).

Extends T2_MATRIX with rigor analyses, all exploratory unless noted:
  1. cell6: bootstrap 95% CI for every language x domain cell (6 cells/arm).
  2. gold_n stratification: F1 for gold_n==1 (n=37) vs >=2 (n=55), A2 rule.
  3. paired dF1: per-item F1 differences on common IDs + bootstrap CI.
     Primary pairs (pre-declared): spark1.3-qwen-plus, spark1.3-spark1.2,
     minimax-glm. Exploratory: all pairs among 6 new arms (Bonferroni noted).
  4. pred_n-F1 mechanism: Pearson r per arm + pooled + binned means.
  5. difficulty: medium+hard (n=9, all math) — expected underpowered, reported
     as negative result with DO-NOT-USE warning.
Inputs: research/mimo_spark_replication/t2_*.json + data/gold + qwen history.
Outputs: research/mimo_spark_replication/T2_DEEPDIVE.json + T2_DEEPDIVE.md
Methods: bootstrap B=1000, seed 20260918 (same as score_t2_matrix.py).
"""
import json
import math
import os
import random

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REP = os.path.join(BASE, "research", "mimo_spark_replication")
SEED = 20260918
B = 1000

T2_FILES = {
    "muse-spark-1.3-free": "t2_muse-spark-1.3-contributor-free.json",
    "muse-spark-1.2-free": "t2_muse-spark-1.2-contributor-free.json",
    "minimax-m3": "t2_mm-minimax-m3.json",
    "deepseek-v4.1-flash-r4": "t2_r4-deepseek-v4.1-flash.json",
    "sensenova-6.8-flash-lite": "t2_sn-sensenova-6.8-flash-lite.json",
    "glm-5.2-r4": "t2_sn-glm-5.2.json",
}
HIST = {
    "qwen-plus (Bailian hist)": os.path.join(BASE, "data", "model_comparison", "qwen-plus_results.json"),
    "qwen-max (Bailian hist)": os.path.join(BASE, "data", "model_comparison", "qwen-max_results.json"),
}
PRIMARY_PAIRS = [
    ("muse-spark-1.3-free", "qwen-plus (Bailian hist)"),
    ("muse-spark-1.3-free", "muse-spark-1.2-free"),
    ("minimax-m3", "glm-5.2-r4"),
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


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return round(sxy / math.sqrt(sxx * syy), 4) if sxx and syy else 0.0


def load_arms():
    gold = json.load(open(os.path.join(BASE, "data", "gold", "gold_dataset.json"), encoding="utf-8"))
    gmap = {g.get("sample_id"): g for g in gold}
    arms = {}
    for label, fn in T2_FILES.items():
        d = json.load(open(os.path.join(REP, fn), encoding="utf-8"))
        recs = []
        for r in d["items"]:
            g = gmap.get(r.get("sample_id"), {})
            recs.append({
                "sid": r.get("sample_id"), "f1": r["f1"] if r.get("valid") else 0.0,
                "valid": bool(r.get("valid")),
                "lang": r.get("language", g.get("language", "")),
                "ann": r.get("annotator", g.get("annotator", "")),
                "gold_n": r.get("gold_n", len(g.get("human_labels", {}).get("concepts", []))),
                "pred_n": len(r.get("predicted", [])),
                "diff": g.get("difficulty", ""),
            })
        arms[label] = recs
    for label, fp in HIST.items():
        d = json.load(open(fp, encoding="utf-8"))
        recs = []
        for r in d.get("results", d.get("items", [])):
            g = gmap.get(r.get("sample_id"), {})
            recs.append({
                "sid": r.get("sample_id"), "f1": r.get("f1", 0),
                "valid": True,
                "lang": r.get("language", g.get("language", "")),
                "ann": g.get("annotator", ""),
                "gold_n": len(r.get("gold_concepts", [])) or len(g.get("human_labels", {}).get("concepts", [])),
                "pred_n": len(r.get("predicted_concepts", r.get("predicted", []))),
                "diff": g.get("difficulty", ""),
            })
        arms[label] = recs
    ids = {label: [r["sid"] for r in recs] for label, recs in arms.items()}
    base = set(ids["muse-spark-1.3-free"])
    assert all(set(v) == base and len(v) == 92 for v in ids.values()), "ID universe mismatch: %s" % {k: len(v) for k, v in ids.items()}
    return arms


def main():
    arms = load_arms()
    out = {"seed": SEED, "B": B, "rule": "A2 (invalid=0 over 92 IDs)", "cells": {}, "goldn": {}, "paired": {}, "predn_corr": {}, "difficulty": {}}
    # 1. cell6 CIs
    for label, recs in arms.items():
        out["cells"][label] = {}
        for lang in ("zh", "de", "en"):
            for ann, tag in (("annotator_1", "math"), ("auto_accepted", "social")):
                cell = [r for r in recs if r["lang"] == lang and r["ann"] == ann]
                vals = [r["f1"] for r in cell]
                out["cells"][label]["%s_%s" % (lang, tag)] = {
                    "n": len(vals),
                    "n_valid": sum(1 for r in cell if r["valid"]),
                    "mean": round(sum(vals) / len(vals), 4) if vals else 0.0,
                    "ci95": bootstrap_ci(vals),
                }
    # 2. gold_n stratification
    for label, recs in arms.items():
        s1 = [r["f1"] for r in recs if r["gold_n"] == 1]
        s2 = [r["f1"] for r in recs if r["gold_n"] >= 2]
        out["goldn"][label] = {
            "n1": len(s1), "mean1": round(sum(s1) / len(s1), 4),
            "n2": len(s2), "mean2": round(sum(s2) / len(s2), 4),
            "ci1": bootstrap_ci(s1), "ci2": bootstrap_ci(s2),
        }
    # 3. paired differences
    fmap = {label: {r["sid"]: r["f1"] for r in recs} for label, recs in arms.items()}
    pairs = list(PRIMARY_PAIRS)
    new6 = list(T2_FILES.keys())
    for i in range(len(new6)):
        for j in range(i + 1, len(new6)):
            if (new6[i], new6[j]) not in pairs and (new6[j], new6[i]) not in pairs:
                pairs.append((new6[i], new6[j]))
    for a, c in pairs:
        d = [fmap[a][s] - fmap[c][s] for s in fmap[a]]
        out["paired"]["%s vs %s" % (a, c)] = {
            "primary": (a, c) in PRIMARY_PAIRS or (c, a) in PRIMARY_PAIRS,
            "mean_d": round(sum(d) / len(d), 4), "ci95": bootstrap_ci(d),
            "n": len(d),
        }
    # 4. pred_n-F1 correlation
    pool_x, pool_y = [], []
    for label, recs in arms.items():
        xs = [r["pred_n"] for r in recs]
        ys = [r["f1"] for r in recs]
        out["predn_corr"][label] = {"pearson_r": pearson(xs, ys), "mean_pred_n": round(sum(xs) / len(xs), 2)}
        pool_x += xs
        pool_y += ys
    out["predn_corr"]["_pooled_new6"] = {"pearson_r": pearson(
        [r["pred_n"] for l in new6 for r in arms[l]],
        [r["f1"] for l in new6 for r in arms[l]])}
    bins = {}
    for l in new6:
        for r in arms[l]:
            bins.setdefault(r["pred_n"], []).append(r["f1"])
    out["predn_corr"]["_binned_new6"] = {str(k): {"n": len(v), "mean_f1": round(sum(v) / len(v), 4)}
                                         for k, v in sorted(bins.items()) if len(v) >= 5}
    # 5. difficulty (negative result expected)
    for label, recs in arms.items():
        hard = [r["f1"] for r in recs if r.get("diff") in ("medium", "hard")]
        out["difficulty"][label] = {"n": len(hard),
                                    "mean": round(sum(hard) / len(hard), 4) if hard else 0.0,
                                    "warning": "DO-NOT-USE: n<=9, all math; underpowered by design"}
    json.dump(out, open(os.path.join(REP, "T2_DEEPDIVE.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # markdown
    L = ["# T2 Deep-Dive (deterministic, zero API — exploratory unless noted)", "",
         "Seed/B = 20260918/1000 (same as T2_MATRIX). A2 rule (invalid=0/92).",
         "Cell n = A2 denominator (incl. fails); n_valid per cell in JSON.",
         "Primary paired comparisons pre-declared; all other pairs exploratory (Bonferroni over 15 pairs: α≈0.003).",
         "", "## 1. Cell CIs (language x domain)", "",
         "| arm | zh_math n/mean/CI | zh_soc | de_math | de_soc | en_math | en_soc |",
         "|---|---|---|---|---|---|---|"]
    for label in list(T2_FILES.keys()) + list(HIST.keys()):
        c = out["cells"][label]
        parts = []
        for k in ("zh_math", "zh_social", "de_math", "de_social", "en_math", "en_social"):
            parts += [c[k]["n"], c[k]["mean"], c[k]["ci95"]]
        L.append("| %s | %d %.3f %s | %d %.3f %s | %d %.3f %s | %d %.3f %s | %d %.3f %s | %d %.3f %s |" % tuple([label] + parts))
    L += ["", "## 2. gold_n stratification (1 vs >=2)", "",
          "| arm | n1/mean/CI | n2/mean/CI |", "|---|---|---|"]
    for label in list(T2_FILES.keys()) + list(HIST.keys()):
        g = out["goldn"][label]
        L.append("| %s | %d %.3f %s | %d %.3f %s |" % (label, g["n1"], g["mean1"], g["ci1"], g["n2"], g["mean2"], g["ci2"]))
    L += ["", "## 3. Paired dF1 (primary first)", "",
          "| pair | primary | mean_d | 95%CI | 0 in CI? |", "|---|---|---|---|---|"]
    for k, v in out["paired"].items():
        inside = v["ci95"][0] <= 0 <= v["ci95"][1]
        L.append("| %s | %s | %.4f | %s | %s |" % (k, v["primary"], v["mean_d"], v["ci95"], inside))
    L += ["", "## 4. pred_n-F1 mechanism", "",
          "| arm | Pearson r | mean pred_n |", "|---|---|---|"]
    for label in list(T2_FILES.keys()) + list(HIST.keys()):
        L.append("| %s | %.4f | %.1f |" % (label, out["predn_corr"][label]["pearson_r"], out["predn_corr"][label]["mean_pred_n"]))
    L.append("| pooled-new6 | %.4f | — |" % out["predn_corr"]["_pooled_new6"]["pearson_r"])
    L += ["", "Binned (new6, bins n>=5): " + "; ".join(
        "pred=%s: n=%d F1=%.3f" % (k, v["n"], v["mean_f1"]) for k, v in out["predn_corr"]["_binned_new6"].items())]
    L += ["", "## 5. Difficulty (negative result — DO NOT USE)", "",
          "| arm | n(med+hard) | mean |", "|---|---|---|"]
    for label in list(T2_FILES.keys()) + list(HIST.keys()):
        L.append("| %s | %d | %.3f |" % (label, out["difficulty"][label]["n"], out["difficulty"][label]["mean"]))
    L += ["", "Power note (normal approx, ΔF1=0.1, 80% power): paired same-item design needs n≈32–71 "
               "(σ_diff 0.20–0.30); existing per-language cells n=6–7 detect only Δ≈0.4+; n=72/92 pools approach Δ≈0.1–0.16."]
    open(os.path.join(REP, "T2_DEEPDIVE.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    for k, v in out["paired"].items():
        if v["primary"]:
            print("PRIMARY %s d=%.4f CI=%s" % (k, v["mean_d"], v["ci95"]))
    print("pooled-new6 pred_n-F1 r =", out["predn_corr"]["_pooled_new6"]["pearson_r"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
