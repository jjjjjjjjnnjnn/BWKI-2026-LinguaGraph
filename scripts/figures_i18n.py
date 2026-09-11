#!/usr/bin/env python3
"""LinguaGraph — Figure i18n renderer (DE/ZH variants).

Renders portal figures with translated UI labels. DATA SOURCES ARE ARCHIVED
SNAPSHOTS (same numbers as the published EN figures + portal text):
  fig3/fig7 ← outputs/physics_comparison.json + outputs/chemistry_comparison.json
  fig4      ← deterministic recompute (seeded) + assert ZH-DE 0.519
  fig5      ← SKIPPED: source graph superseded (recompute gives 442/270/6/0.72
              vs published 556/459/8/0.40); re-rendering would falsify bars.

Usage:
    python scripts/figures_i18n.py --lang de [--fig 3]
    python scripts/figures_i18n.py --lang zh [--fig all]

Outputs: outputs/figures/fig{3,7}_*_cds_{de,zh}.png, fig4_null_model_{de,zh}.png
(mirrored to cognitive-space/web/figures/ by the caller, not here)
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR / "scripts" / "figures"))
OUTPUT_DIR = PROJECT_DIR / "outputs" / "figures"

import fig4_null_model as F4  # noqa: E402

LV = {
    "de": {"elementary": "Grundschule", "middle": "Mittelstufe", "high": "Oberstufe", "college": "Hochschule"},
    "zh": {"elementary": "小学", "middle": "初中", "high": "高中", "college": "大学"},
}
SUBJ = {
    "de": {"Math": "Mathematik", "Physics": "Physik", "Chemistry": "Chemie"},
    "zh": {"Math": "数学", "Physics": "物理", "Chemistry": "化学"},
}
T = {
    "de": {
        "fig3_title": "Konzeptdichte nach Bildungsstufe",
        "fig3_ylabel": "CDS (Konzeptdichte)",
        "fig3_sum0": "CDS sinkt mit\nder Bildungsstufe:",
        "fig3_concepts": "Konzepte",
        "fig7_title": "CDS nach Bildungsstufe: Drei-Fächer-Vergleich",
        "fig7_ylabel": "CDS (Konzeptdichte)",
        "fig4_title": "LDS-Nullmodell-Suite: Standard- und Adversarial-Bedingungen",
        "fig4_xlabel": "Sprachpaar",
        "fig4_note": ("Standard (Balken): Struktur-Test\n"
                      "Adversarial (Linien): Falsifikations-Test"),
    },
    "zh": {
        "fig3_title": "各教育阶段概念密度",
        "fig3_ylabel": "CDS（概念密度）",
        "fig3_sum0": "CDS 随教育阶段\n下降：",
        "fig3_concepts": "个概念",
        "fig7_title": "各教育阶段 CDS：三学科对比",
        "fig7_ylabel": "CDS（概念密度）",
        "fig4_title": "LDS 零模型套件：标准 ＋ 对抗条件",
        "fig4_xlabel": "语言对",
        "fig4_note": ("标准（柱）：结构检验\n"
                      "对抗（线）：证伪检验"),
    },
}

FONT = {"de": ["DejaVu Sans"], "zh": ["Microsoft YaHei", "SimSun", "DejaVu Sans"]}
LV_COLORS = {"elementary": "#4ade80", "middle": "#22d3ee", "high": "#60a5fa", "college": "#c084fc"}
ORDER = ["elementary", "middle", "high", "college"]


def setup(lang):
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": FONT[lang],
        "font.size": 11, "axes.titlesize": 14, "axes.labelsize": 12,
        "figure.dpi": 150, "savefig.dpi": 300,
        "savefig.bbox": "tight", "savefig.pad_inches": 0.15,
        "axes.unicode_minus": False,
    })


def load_comp():
    pc = json.loads((OUTPUT_DIR / ".." / "physics_comparison.json").read_text(encoding="utf-8"))
    cc = json.loads((OUTPUT_DIR / ".." / "chemistry_comparison.json").read_text(encoding="utf-8"))
    return pc, cc


def fig3(pc, lang):
    t, lv = T[lang], LV[lang]
    math = pc["math"]["cds"]
    labels = [lv[l] for l in ORDER]
    values = [math[l]["cds"] for l in ORDER]
    counts = [math[l]["nodes"] for l in ORDER]
    assert abs(values[1] - 0.2705) < 1e-4 and abs(math["high"]["cds"] - 0.0731) < 1e-4, values
    colors = [LV_COLORS[l] for l in ORDER]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), gridspec_kw={"width_ratios": [1.5, 1]})
    bars = ax1.bar(labels, values, color=colors, width=0.55, edgecolor="white", linewidth=0.5)
    ax1.set_ylabel(t["fig3_ylabel"])
    ax1.set_title(t["fig3_title"], fontweight="bold")
    for bar, v in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.003, f"{v:.3f}",
                 ha="center", va="bottom", fontsize=10)
    ax1.set_ylim(0, max(values) * 1.25)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax2.axis("off")
    summary = (t["fig3_sum0"] + "\n\n" + f"{labels[0]}: {values[0]:.3f}\n    ({counts[0]} {t['fig3_concepts']})\n\n"
               f"{labels[-1]}: {values[-1]:.3f}\n    ({counts[-1]} {t['fig3_concepts']})\n\n"
               f"Ratio: {values[0]/values[-1]:.1f}×")
    ax2.text(0.1, 0.5, summary, fontsize=11, va="center",
             bbox=dict(boxstyle="round,pad=0.6", facecolor="#f0f0f0", edgecolor="#ccc"))
    plt.tight_layout()
    path = OUTPUT_DIR / f"fig3_cds_by_level_{lang}.png"
    plt.savefig(path)
    plt.close()
    print(f"  [OK] {path.name} ({path.stat().st_size // 1024} KB)")
    return path


def fig7(pc, cc, lang):
    t, lv, sj = T[lang], LV[lang], SUBJ[lang]
    labels = [lv[l] for l in ORDER]
    mv = [pc["math"]["cds"][l]["cds"] for l in ORDER]
    pv = [pc["physics"]["cds"][l]["cds"] for l in ORDER]
    cv = [cc["chemistry"]["cds"][l]["cds"] for l in ORDER]
    assert abs(mv[1] - 0.2705) < 1e-4 and abs(pv[0] - 0.2222) < 1e-4 and abs(cv[1] - 0.0415) < 1e-4
    x = np.arange(len(ORDER))
    width = 0.25
    fig, ax = plt.subplots(figsize=(10, 5))
    b1 = ax.bar(x - width, mv, width, label=sj["Math"], color="#60a5fa", edgecolor="white", linewidth=0.5)
    b2 = ax.bar(x, pv, width, label=sj["Physics"], color="#f97316", edgecolor="white", linewidth=0.5)
    b3 = ax.bar(x + width, cv, width, label=sj["Chemistry"], color="#22c55e", edgecolor="white", linewidth=0.5)
    ax.set_ylabel(t["fig7_ylabel"])
    ax.set_title(t["fig7_title"], fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for bars in [b1, b2, b3]:
        for bar in bars:
            v = bar.get_height()
            if v > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, v + 0.003, f"{v:.3f}",
                        ha="center", va="bottom", fontsize=8)
    plt.tight_layout()
    path = OUTPUT_DIR / f"fig7_three_subject_cds_{lang}.png"
    plt.savefig(path)
    plt.close()
    print(f"  [OK] {path.name} ({path.stat().st_size // 1024} KB)")
    return path


def fig4(lang):
    t = T[lang]
    from fig4_null_model import (load_aligned, get_lang_graphs, CONDITION_CONFIG, PAIRS,
                                 condition_full, condition_structure_null, condition_node_permuted,
                                 condition_random_graph, condition_within_language,
                                 condition_language_label_permutation, condition_monolingual_control)
    aligned = load_aligned()
    lang_nodes, lang_edges = get_lang_graphs(aligned)
    funcs = [("Full (baseline)", condition_full),
             ("Structure Null\n(deg.-preserving)", condition_structure_null),
             ("Node-Permuted Null", condition_node_permuted),
             ("Complete Random", condition_random_graph)]
    results = {name: func(lang_nodes, lang_edges) for name, func in funcs}
    full = results["Full (baseline)"]
    assert abs(full.get("ZH-DE", 0) - 0.5188) < 0.005, full
    adv_funcs = [("Within-Lang\n(same split)", condition_within_language, None),
                 ("Label Permute\n(group-level)",
                  lambda ln, le: condition_language_label_permutation(ln, le, aligned), None),
                 ("Mono Control\n(same lang)", condition_monolingual_control, None)]
    adversarial = {}
    for name, func, _ in adv_funcs:
        try:
            adversarial[name] = func(lang_nodes, lang_edges)
        except Exception as e:
            print(f"    [SKIP] {e}")
            adversarial[name] = {}
    x = np.arange(len(PAIRS))
    width = 0.12
    fig, ax = plt.subplots(figsize=(12, 5.5))
    std_names = [c[0] for c in CONDITION_CONFIG[:4]]
    for i, (name, color, desc) in enumerate(CONDITION_CONFIG[:4]):
        vals = [results.get(name, {}).get(p, 0) for p in PAIRS]
        offset = (i - 1.5) * width
        bars = ax.bar(x + offset, vals, width, label=f"{name}", color=color, alpha=0.85,
                      edgecolor="white", linewidth=0.5)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.015,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=6, rotation=45)
    adv_colors = ["#7c3aed", "#db2777", "#0891b2"]
    for j, (name, _, _) in enumerate([c for c in CONDITION_CONFIG if c[0] not in std_names]):
        vals = [adversarial.get(name, {}).get(p, 0) for p in PAIRS]
        if not any(vals):
            if name == "Within-Lang\n(same split)":
                vals = [adversarial.get("ZH", adversarial.get("Within-Lang", {})).get("ZH", 0)
                        if adversarial else 0 for _ in PAIRS]
            all_vals = list(adversarial.get(name, {}).values()) if adversarial else []
            if all_vals:
                avg = sum(all_vals) / len(all_vals)
                ax.axhline(y=avg, color=adv_colors[j], linestyle="--", linewidth=1.5, alpha=0.7,
                           xmin=0.05, xmax=0.95)
                ax.text(x[-1] + 0.4, avg + 0.01, f"{name}\n{avg:.3f}", fontsize=7,
                        color=adv_colors[j], va="bottom")
    ax.set_xlabel(t["fig4_xlabel"], fontsize=11)
    ax.set_ylabel("LDS", fontsize=11)
    ax.set_title(t["fig4_title"], fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(PAIRS, fontsize=10)
    ax.legend(fontsize=7, loc="upper right", ncol=2)
    ax.set_ylim(0, 1.15)
    ax.text(1.5, 0.30, t["fig4_note"], ha="center", va="center",
            fontsize=6.5, color="#555",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f8f9fa", edgecolor="#ddd"))
    plt.tight_layout()
    path = OUTPUT_DIR / f"fig4_null_model_{lang}.png"
    fig.savefig(path, dpi=300)
    print(f"  [OK] {path.name} ({path.stat().st_size // 1024} KB)")
    plt.close(fig)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=["de", "zh"], required=True)
    ap.add_argument("--fig", type=int, choices=[3, 4, 7], default=None)
    args = ap.parse_args()
    setup(args.lang)
    print(f"Figure i18n renderer — lang={args.lang} (fig5 skipped: source superseded)")
    pc, cc = load_comp()
    want = [args.fig] if args.fig else [3, 4, 7]
    if 3 in want:
        fig3(pc, args.lang)
    if 7 in want:
        fig7(pc, cc, args.lang)
    if 4 in want:
        fig4(args.lang)


if __name__ == "__main__":
    main()
