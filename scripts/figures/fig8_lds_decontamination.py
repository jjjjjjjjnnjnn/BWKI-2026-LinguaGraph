#!/usr/bin/env python3
"""Fig 8 — LDS-K decontamination (T1 verdict chart).

Deterministic data snapshot (no recompute):
  Full           ← paper/03_results.md §3.7 (0.934 / 0.938 / 0.519)
  Structure Null ← degree-preserving rewiring, same table (0.957 / 0.957 / 0.717)
  Decontaminated ← T1 FilterA: drop groups whose de-label contains CJK
                   (167/219 removed, 52 retained), recompute via
                   scripts/figures/_lds_utils.py (0.985 / 0.985 / 0.990).
                   Full provenance: t123 T1 (2026-09-12).

Outputs (300 DPI):
  outputs/figures/fig8_lds_decontamination{,_de,_zh}.png
  outputs/figures/fig8_lds_decontamination_data.csv
Mirror to cognitive-space/web/figures/ by the caller.

Usage: python scripts/figures/fig8_lds_decontamination.py
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAIRS = ["ZH-EN", "DE-EN", "ZH-DE"]
FULL = [0.934, 0.938, 0.519]
STRUCT_NULL = [0.957, 0.957, 0.717]
DECONTAM = [0.985, 0.985, 0.990]

T = {
    "en": {"title": "LDS-K: Full vs Structure Null vs Decontaminated (T1)",
           "ylabel": "LDS-K (0 = identical, 1 = divergent)",
           "cap": "Dropping de-labels with CJK text (167/219) collapses\nZH-DE convergence 0.52 → 0.99: label artifact.",
           "s_full": "Full", "s_null": "Structure Null", "s_dec": "Decontaminated (T1)"},
    "de": {"title": "LDS-K: Voll vs. Struktur-Null vs. Dekontaminiert (T1)",
           "ylabel": "LDS-K (0 = identisch, 1 = divergent)",
           "cap": "Entfernen von de-Labels mit CJK-Text (167/219) lässt\nZH-DE-Konvergenz kollabieren 0,52 → 0,99: Label-Artefakt.",
           "s_full": "Voll", "s_null": "Struktur-Null", "s_dec": "Dekontaminiert (T1)"},
    "zh": {"title": "LDS-K：原值 vs 结构零模型 vs 去污染（T1）",
           "ylabel": "LDS-K（0＝相同，1＝分歧）",
           "cap": "去掉含中文的德语标签（167/219）后\nZH-DE 趋同 0.52→0.99 坍塌：标签伪影。",
           "s_full": "原值", "s_null": "结构零模型", "s_dec": "去污染（T1）"},
}
FONT = {"en": ["DejaVu Sans"], "de": ["DejaVu Sans"],
        "zh": ["Microsoft YaHei", "SimSun", "DejaVu Sans"]}
COLORS = ["#1e3a8a", "#0e7490", "#b45309"]


def render(lang):
    plt.rcParams.update({"font.family": "sans-serif",
                         "font.sans-serif": FONT[lang],
                         "font.size": 11, "axes.titlesize": 14,
                         "axes.labelsize": 12})
    t = T[lang]
    x = np.arange(len(PAIRS))
    w = 0.24
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    series = [(FULL, t["s_full"]), (STRUCT_NULL, t["s_null"]),
              (DECONTAM, t["s_dec"])]
    for i, (vals, label) in enumerate(series):
        bars = ax.bar(x + (i - 1) * w, vals, w, label=label,
                      color=COLORS[i], edgecolor="white")
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.012,
                    f"{v:.3f}" if lang == "en" else f"{v:.3f}".replace(".", ","),
                    ha="center", va="bottom", fontsize=9)
    # gap arrows for ZH-DE
    ax.annotate("", xy=(2 + w, 0.990), xytext=(2 + w, 0.519),
                arrowprops={"arrowstyle": "<->", "color": "#b45309", "lw": 1.5})
    ax.text(2 + w - 0.44, 0.60, "+0.47", color="#b45309",
            fontweight="bold", fontsize=10,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1})
    ax.set_xticks(x)
    ax.set_xticklabels(PAIRS)
    ax.set_ylabel(t["ylabel"])
    ax.set_title(t["title"], fontweight="bold")
    ax.set_ylim(0, 1.12)
    ax.legend(frameon=True, loc="center left", bbox_to_anchor=(1.0, 0.5))
    ax.text(0.02, 0.02, t["cap"], transform=ax.transAxes, fontsize=9,
            color="#334155", va="bottom", ha="left",
            bbox={"facecolor": "#f1f5f9", "edgecolor": "#cbd5e1",
                  "boxstyle": "round,pad=0.4"})
    fig.tight_layout()
    fig.subplots_adjust(right=0.80)
    suf = "" if lang == "en" else "_" + lang
    fig.savefig(OUTPUT_DIR / f"fig8_lds_decontamination{suf}.png", dpi=300)
    plt.close(fig)
    print("saved fig8" + suf)


def main():
    for lang in ("en", "de", "zh"):
        render(lang)
    with open(OUTPUT_DIR / "fig8_lds_decontamination_data.csv", "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pair", "full", "structure_null", "decontaminated_T1"])
        for p, a, b, c in zip(PAIRS, FULL, STRUCT_NULL, DECONTAM):
            w.writerow([p, a, b, c])
    print("saved csv")


if __name__ == "__main__":
    main()
