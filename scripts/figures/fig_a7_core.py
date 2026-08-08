#!/usr/bin/env python3
"""LinguaGraph — A7: Core figures for the paper.

Produces the key figures integrating all analysis layers:
  fig_a7_1_delta_lds.png        : ΔLDS across human (N=15) / LLM within-subject /
                                   social-wiki / textbook — the three-way comparison
  fig_a7_2_thematic_heatmap.png : topic-level LDS-C (LLM) + human thematic directionality
  fig_a7_3_null_models.png      : LDS-K vs structure null / split-half floor / label perm
  fig_a7_4_mechanism.png        : D1 mechanism decomposition (P1-P5 + LMM marginal)
  fig_a7_5_ldsk_sensitivity.png : A4 sensitivity (directed/undirected, alignment,
                                   threshold, levels)

Output dir: outputs/figures/ (gitignored) + CSV data next to each PNG.
Reproducible from the committed JSON results (data/lds_c/...).

Usage:
    python scripts/figures/fig_a7_core.py
"""

from __future__ import annotations

import json
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT = PROJECT_ROOT / "outputs" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

SEED = 42
np.random.seed(SEED)
plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
    "legend.fontsize": 8, "figure.dpi": 300,
})

PAIRS = ["ZH-EN", "DE-EN", "ZH-DE"]
PAIR_ORDER = {"ZH-EN": 0, "DE-EN": 1, "ZH-DE": 2}


def load(rel: str) -> dict:
    p = PROJECT_ROOT / rel
    return json.loads(p.read_text(encoding="utf-8"))


def save_csv(name: str, rows: list, fieldnames: list) -> None:
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


# ── 1. ΔLDS three-way comparison ────────────────────────────────────
def fig_delta_lds() -> None:
    human = load("data/lds_c/lds_c_results_20260807.json")
    llm = load("data/lds_c/llm_subject/analysis_20260808.json")
    a4 = load("data/lds_c/lds_k_deep/lds_k_deepen_20260808.json")

    # human concept-level LDS-C (pooled per pair)
    human_lds = {}
    for pair in PAIRS:
        row = human.get("pooled_lds_c", {})
        human_lds[pair] = row.get(pair, None)
    # LLM within-subject P1
    llm_lds = {p: llm["P1_language_main_effect"][p]["lds_c_pooled"] for p in PAIRS}
    # social wiki (aligned) + textbook math
    wiki_lds = {p: a4["wiki_pooled_lds"][p]["lds"] for p in PAIRS}
    math_lds = {p: a4["math_pooled_lds"][p]["lds"] for p in PAIRS}

    x = np.arange(len(PAIRS))
    w = 0.19
    series = [
        ("Human N=15 (between)", human_lds, "#d62728", "//"),
        ("LLM within-subject", llm_lds, "#1f77b4", ""),
        ("Social Wikipedia", wiki_lds, "#2ca02c", ".."),
        ("Math textbook (LDS-K)", math_lds, "#7f7f7f", "xx"),
    ]
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    for i, (label, vals, color, hatch) in enumerate(series):
        ys = [vals[p] for p in PAIRS]
        ax.bar(x + (i - 1.5) * w, ys, w, label=label, color=color, hatch=hatch, edgecolor="black", linewidth=0.5)
        for xi, yi in zip(x + (i - 1.5) * w, ys):
            ax.text(xi, yi + 0.01, f"{yi:.2f}", ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels(PAIRS)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("LDS (higher = more divergent)")
    ax.set_title("Three-way structural divergence: human / LLM / social / textbook")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "fig_a7_1_delta_lds.png", dpi=300)
    plt.close(fig)

    rows = [{"pair": p, **{f"{name}": vals[p] for name, vals, _, _ in series}} for p in PAIRS]
    save_csv("fig_a7_1_delta_lds.csv", rows, ["pair"] + [s[0] for s in series])
    print("  [OK] fig_a7_1_delta_lds.png")


# ── 2. Thematic heatmap (topic-level LDS-C, LLM) ────────────────────
def fig_thematic() -> None:
    pt = load("data/lds_c/llm_subject/per_topic_20260808.json")
    topics = pt["topics"]
    # topic -> pair -> LDS-C
    mat = np.zeros((len(topics), 3))
    for i, t in enumerate(topics):
        for j, p in enumerate(PAIRS):
            mat[i, j] = pt["p1_lds_per_topic"].get(t, {}).get(p, np.nan)
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    im = ax.imshow(mat, cmap="YlOrRd", aspect="auto", vmin=0.5, vmax=1.0)
    ax.set_xticks(range(3)); ax.set_xticklabels(PAIRS)
    ax.set_yticks(range(len(topics))); ax.set_yticklabels(topics)
    for i in range(len(topics)):
        for j in range(3):
            v = mat[i, j]
            if v == v:
                ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8,
                        color="white" if v > 0.85 else "black")
    ax.set_title("LLM within-subject LDS-C by topic")
    ax.set_xlabel("Language pair")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label("LDS-C")
    fig.tight_layout()
    fig.savefig(OUT / "fig_a7_2_thematic_heatmap.png", dpi=300)
    plt.close(fig)

    rows = [{"topic": t, **{p: (round(float(mat[i, j]), 4) if mat[i, j] == mat[i, j] else None)
                            for j, p in enumerate(PAIRS)}} for i, t in enumerate(topics)]
    save_csv("fig_a7_2_thematic_heatmap.csv", rows, ["topic"] + PAIRS)
    print("  [OK] fig_a7_2_thematic_heatmap.png")


# ── 3. Null models (LDS-K vs floors) ────────────────────────────────
def fig_null_models() -> None:
    a4 = load("data/lds_c/lds_k_deep/lds_k_deepen_20260808.json")
    human = load("data/lds_c/lds_c_results_20260807.json")
    fig4_csv = PROJECT_ROOT / "outputs" / "figures" / "fig4_null_model_data.csv"

    # read structure null + full from fig4 CSV (committed, reproducible)
    null = {"ZH-EN": {}, "DE-EN": {}, "ZH-DE": {}}
    if fig4_csv.exists():
        with fig4_csv.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                cond = row.get("condition", "")
                for p in PAIRS:
                    if "Structure" in cond and p in row:
                        null[p]["structure"] = float(row[p])
                    elif "Full" in cond and p in row:
                        null[p]["full"] = float(row[p])
    # fall back to deep-dive math pooled if fig4 CSV missing
    for p in PAIRS:
        null[p].setdefault("full", a4["math_pooled_lds"][p]["lds"])
        null[p].setdefault("structure", None)
    # within-language floor from human null_models (split-half)
    nh = human.get("null_models", {}).get("within_language_split_half", {})
    for p in PAIRS:
        null[p]["floor"] = nh.get(p, 0.97)

    x = np.arange(len(PAIRS))
    w = 0.22
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    labels = ["LDS-K (observed)", "Structure Null", "Within-lang floor"]
    colors = ["#1f77b4", "#ff7f0e", "#d62728"]
    for i, (lab, key) in enumerate(zip(labels, ["full", "structure", "floor"])):
        ys = [null[p][key] if null[p][key] is not None else np.nan for p in PAIRS]
        ax.bar(x + (i - 1) * w, ys, w, label=lab, color=colors[i], edgecolor="black", linewidth=0.5)
        for xi, yi in zip(x + (i - 1) * w, ys):
            if yi == yi:
                ax.text(xi, yi + 0.005, f"{yi:.2f}", ha="center", va="bottom", fontsize=7)
    ax.axhline(1.0, color="black", lw=0.8, ls=":")
    ax.text(2.5, 1.01, "complete random = 1.0", fontsize=7, ha="right")
    ax.set_xticks(x); ax.set_xticklabels(PAIRS)
    ax.set_ylim(0.3, 1.1)
    ax.set_ylabel("LDS")
    ax.set_title("LDS-K against null models")
    ax.legend(framealpha=0.9)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "fig_a7_3_null_models.png", dpi=300)
    plt.close(fig)
    rows = [{"pair": p, **{lab: null[p][key] for lab, key in zip(labels, ["full", "structure", "floor"])}}
            for p in PAIRS]
    save_csv("fig_a7_3_null_models.csv", rows, ["pair"] + labels)
    print("  [OK] fig_a7_3_null_models.png")


# ── 4. D1 mechanism decomposition ───────────────────────────────────
def fig_mechanism() -> None:
    llm = load("data/lds_c/llm_subject/analysis_20260808.json")
    lmm = load("data/lds_c/llm_subject/lmm_20260808.json")

    # Panel A: P1 language effect vs floors
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(7.4, 3.6))

    p1 = llm["P1_language_main_effect"]
    x = np.arange(len(PAIRS))
    obs = [p1[p]["lds_c_pooled"] for p in PAIRS]
    floor = [p1[p]["split_half_floor"] for p in PAIRS]
    perm = [p1[p]["label_perm_mean"] for p in PAIRS]
    axA.bar(x - 0.25, obs, 0.22, label="LDS-C observed", color="#1f77b4", edgecolor="black", lw=0.5)
    axA.bar(x, floor, 0.22, label="Split-half floor", color="#d62728", edgecolor="black", lw=0.5)
    axA.bar(x + 0.25, perm, 0.22, label="Label perm", color="#7f7f7f", edgecolor="black", lw=0.5)
    for i, (o, f) in enumerate(zip(obs, floor)):
        axA.text(i - 0.25, o + 0.01, f"{o:.2f}", ha="center", fontsize=7)
    axA.set_xticks(x); axA.set_xticklabels(PAIRS)
    axA.set_ylim(0.7, 1.05); axA.set_ylabel("LDS-C")
    axA.set_title("(A) Language signal > noise floor")
    axA.legend(fontsize=7, framealpha=0.9)
    axA.spines["top"].set_visible(False); axA.spines["right"].set_visible(False)

    # Panel B: LMM marginal contributions (code vs frame)
    params = lmm["params"]
    names = ["same_lang", "same_frame"]
    labels = ["same\nlanguage", "same\nframe"]
    coefs = [params[n]["coef"] for n in names]
    ses = [params[n]["se"] for n in names]
    ps = [params[n]["p"] for n in names]
    xb = np.arange(2)
    axB.bar(xb, coefs, 0.4, color=["#1f77b4", "#d62728"], edgecolor="black", lw=0.5, yerr=ses, capsize=3)
    for xi, c, p in zip(xb, coefs, ps):
        axB.text(xi, c + 0.006, f"{c:+.3f}\np={p:.3f}", ha="center", va="bottom", fontsize=7)
    axB.axhline(0, color="black", lw=0.8)
    axB.set_xticks(xb); axB.set_xticklabels(labels)
    axB.set_ylabel("Marginal effect on Jaccard similarity")
    axB.set_title("(B) LMM: code dominates, frame ~0")
    axB.spines["top"].set_visible(False); axB.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUT / "fig_a7_4_mechanism.png", dpi=300)
    plt.close(fig)
    rows = [{"effect": n, "coef": params[n]["coef"], "se": params[n]["se"],
             "p": params[n]["p"]} for n in names]
    save_csv("fig_a7_4_mechanism.csv", rows, ["effect", "coef", "se", "p"])
    print("  [OK] fig_a7_4_mechanism.png")


# ── 5. A4 sensitivity ───────────────────────────────────────────────
def fig_ldsk_sensitivity() -> None:
    a4 = load("data/lds_c/lds_k_deep/lds_k_deepen_20260808.json")
    sens = a4["sensitivity"]
    align = a4["sensitivity_alignment"]
    x = np.arange(len(PAIRS))
    w = 0.17
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.4, 3.6))

    # left: directed/undirected/node_only on math
    series = [("directed", sens["directed"], "#1f77b4"),
              ("undirected", sens["undirected"], "#2ca02c"),
              ("node-only", sens["node_only"], "#ff7f0e")]
    for i, (lab, d, c) in enumerate(series):
        ys = [d[p]["lds"] for p in PAIRS]
        axL.bar(x + (i - 1) * w, ys, w, label=lab, color=c, edgecolor="black", lw=0.5)
    axL.axhline(0.97, color="red", lw=0.8, ls="--")
    axL.text(2.5, 0.975, "noise floor 0.97", fontsize=6.5, ha="right")
    axL.set_xticks(x); axL.set_xticklabels(PAIRS)
    axL.set_ylim(0.3, 1.05); axL.set_ylabel("LDS")
    axL.set_title("(A) Math LDS-K: direction & edge sensitivity")
    axL.legend(fontsize=7)
    axL.spines["top"].set_visible(False); axL.spines["right"].set_visible(False)

    # right: alignment tightness on Wikipedia
    series = [("loose (canonical)", align["loose_canonical"], "#1f77b4"),
              ("strict (gloss)", align["strict_gloss"], "#d62728")]
    for i, (lab, d, c) in enumerate(series):
        ys = [d[p]["lds"] for p in PAIRS]
        axR.bar(x + (i - 0.5) * w, ys, w, label=lab, color=c, edgecolor="black", lw=0.5)
    axR.set_xticks(x); axR.set_xticklabels(PAIRS)
    axR.set_ylim(0.3, 1.05); axR.set_ylabel("LDS")
    axR.set_title("(B) Social Wikipedia: alignment tightness")
    axR.legend(fontsize=7)
    axR.spines["top"].set_visible(False); axR.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUT / "fig_a7_5_ldsk_sensitivity.png", dpi=300)
    plt.close(fig)
    rows = [{"pair": p, **{f"math_{k}": sens[k][p]["lds"] for k in ["directed", "undirected", "node_only"]},
             **{f"wiki_{k}": align[k][p]["lds"] for k in ["loose_canonical", "strict_gloss"]}}
            for p in PAIRS]
    save_csv("fig_a7_5_ldsk_sensitivity.csv", rows,
             ["pair", "math_directed", "math_undirected", "math_node_only",
              "wiki_loose_canonical", "wiki_strict_gloss"])
    print("  [OK] fig_a7_5_ldsk_sensitivity.png")


def main() -> None:
    print("A7: generating core figures")
    fig_delta_lds()
    fig_thematic()
    fig_null_models()
    fig_mechanism()
    fig_ldsk_sensitivity()
    print(f"\n  Output dir: {OUT}")


if __name__ == "__main__":
    main()
