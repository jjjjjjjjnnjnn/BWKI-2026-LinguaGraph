#!/usr/bin/env python3
"""Fig 2 — LDS calculation flow (binary formula, as-published).

Published formula (LDS-K):
  LDS = 1 - mean(J_node, J_edge)
Verified on three pairs (0.9336 / 0.9382 / 0.5188 exact hits).
The ternary as-implemented variant does NOT produce published values.

Flow: Graph_G_ZH + Graph_G_DE (same topic) -> concept mapping
  (cross-language alignment) -> two similarity components
  (Jaccard_node / Jaccard_edge) -> mean -> LDS.

Outputs (300 DPI):
  outputs/figures/fig2_lds_flow{,_de,_zh}.png
Mirror to cognitive-space/web/figures/, _deploy/figures/,
_deploy/web/figures/ by the script.
No CSV (flow diagram, no data).

Usage: python scripts/figures/fig2_lds_flow.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MIRROR_DIRS = [
    PROJECT_ROOT / "cognitive-space" / "web" / "figures",
    PROJECT_ROOT / "_deploy" / "figures",
    PROJECT_ROOT / "_deploy" / "web" / "figures",
]

BG = "#f1f3f5"
NAVY = "#0a1f3d"
INDIGO = "#1e3a8a"
LIGHT = "#dbeafe"
GRAY = "#334155"

T = {
    "en": {
        "title": "LDS Calculation Flow (binary formula, as-published)",
        "in_zh": "Graph G_ZH\n(same topic)",
        "in_de": "Graph G_DE\n(same topic)",
        "mapping": "Concept mapping\n(cross-language alignment)",
        "c_node": "Node Jaccard\n(J_node)",
        "c_edge": "Edge Jaccard\n(J_edge)",
        "mean": "Mean similarity\n(J_node + J_edge) / 2",
        "lds": "LDS = 1 \u2212 mean(J_node, J_edge)",
        "foot": "Exact-GED variant not used for published values (intractable); see BASELINE_LEDGER",
    },
    "de": {
        "title": "LDS-Berechnungsfluss (bin\u00e4re Formel, publiziert)",
        "in_zh": "Graph G_ZH\n(gleiches Thema)",
        "in_de": "Graph G_DE\n(gleiches Thema)",
        "mapping": "Konzept-Mapping\n(sprach\u00fcbergreifender Abgleich)",
        "c_node": "Knoten-Jaccard\n(J_node)",
        "c_edge": "Kanten-Jaccard\n(J_edge)",
        "mean": "Mittlere \u00c4hnlichkeit\n(J_Knoten + J_Kante) / 2",
        "lds": "LDS = 1 \u2212 Mittelwert(J_node, J_edge)",
        "foot": "Exakte GED-Variante f\u00fcr publizierte Werte nicht verwendet (nicht berechenbar); siehe BASELINE_LEDGER",
    },
    "zh": {
        "title": "LDS \u8ba1\u7b97\u6d41\u7a0b\uff08\u4e8c\u5143\u516c\u5f0f\uff0c\u53d1\u8868\u503c\uff09",
        "in_zh": "\u56fe G_\u4e2d\u6587\n\uff08\u540c\u4e00\u4e3b\u9898\uff09",
        "in_de": "\u56fe G_\u5fb7\u6587\n\uff08\u540c\u4e00\u4e3b\u9898\uff09",
        "mapping": "\u6982\u5ff5\u6620\u5c04\n\uff08\u8de8\u8bed\u8a00\u5bf9\u9f50\uff09",
        "c_node": "\u8282\u70b9 Jaccard\n(J_node)",
        "c_edge": "\u8fb9 Jaccard\n(J_edge)",
        "mean": "\u5e73\u5747\u76f8\u4f3c\u5ea6\n(J_\u8282\u70b9 + J_\u8fb9) / 2",
        "lds": "LDS = 1 \u2212 mean(J_node, J_edge)",
        "foot": "\u7cbe\u786eGED\u53d8\u4f53\u56e0\u4e0d\u53ef\u8ba1\u7b97\u672a\u7528\u4e8e\u53d1\u8868\u503c\uff0c\u89c1BASELINE_LEDGER",
    },
}
FONT = {"en": ["DejaVu Sans"], "de": ["DejaVu Sans"],
        "zh": ["Microsoft YaHei", "SimSun", "DejaVu Sans"]}


def _box(ax, x0, y0, w, h, text, *, facecolor="white", edgecolor=INDIGO,
         textcolor=NAVY, fontsize=10, bold=False, lw=1.8):
    box = FancyBboxPatch((x0, y0), w, h,
                         boxstyle="round,pad=0.015,rounding_size=0.02",
                         facecolor=facecolor, edgecolor=edgecolor, lw=lw)
    ax.add_patch(box)
    ax.text(x0 + w / 2, y0 + h / 2, text, ha="center", va="center",
            fontsize=fontsize, color=textcolor,
            fontweight="bold" if bold else "normal", linespacing=1.45)


def _arrow(ax, x0, y0, x1, y1):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1),
                                 arrowstyle="-|>", mutation_scale=16,
                                 color=INDIGO, lw=1.8, shrinkA=0, shrinkB=2))


def render(lang):
    plt.rcParams.update({"font.family": "sans-serif",
                         "font.sans-serif": FONT[lang],
                         "font.size": 10, "axes.titlesize": 14})
    t = T[lang]
    fig, ax = plt.subplots(figsize=(11, 6.8))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.set_title(t["title"], color=NAVY, fontweight="bold", pad=12)

    # Row 1: two input graphs
    _box(ax, 5, 71, 42, 17, t["in_zh"], fontsize=10, bold=True)
    _box(ax, 53, 71, 42, 17, t["in_de"], fontsize=10, bold=True)
    # Row 2: concept mapping
    _box(ax, 24, 51, 52, 14, t["mapping"], facecolor=LIGHT, fontsize=10,
         bold=True)
    # Row 3: two components (binary, as-published; no GED_sim main box)
    _box(ax, 8, 30, 40, 15, t["c_node"], fontsize=9.5, bold=True)
    _box(ax, 52, 30, 40, 15, t["c_edge"], fontsize=9.5, bold=True)
    # Row 4: mean
    _box(ax, 26, 14.5, 48, 11, t["mean"], facecolor=LIGHT, fontsize=9.5,
         bold=True)
    # Row 5: LDS output (emphasis)
    _box(ax, 24, 1.5, 52, 9, t["lds"], facecolor=INDIGO, edgecolor=NAVY,
         textcolor="white", fontsize=11, bold=True, lw=2.0)

    # Arrows: inputs -> mapping
    _arrow(ax, 26, 71, 40, 65)
    _arrow(ax, 74, 71, 60, 65)
    # mapping -> components (binary)
    _arrow(ax, 40, 51, 28, 45)
    _arrow(ax, 60, 51, 72, 45)
    # components -> mean (binary)
    _arrow(ax, 28, 30, 40, 25.5)
    _arrow(ax, 72, 30, 60, 25.5)
    # mean -> LDS
    _arrow(ax, 50, 14.5, 50, 10.5)

    fig.text(0.5, 0.015, t["foot"], ha="center", va="bottom", fontsize=7.5,
             color=GRAY, style="italic", wrap=True)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.90, bottom=0.08)
    suf = "" if lang == "en" else "_" + lang
    out = OUTPUT_DIR / f"fig2_lds_flow{suf}.png"
    # No bbox_inches="tight": keeps foot text uncropped; fonts raster-embedded in PNG.
    fig.savefig(out, dpi=300, facecolor=BG)
    plt.close(fig)
    print("saved fig2" + (suf or ""))

    # mirror to all publish targets
    try:
        import shutil
        for md in MIRROR_DIRS:
            md.mkdir(parents=True, exist_ok=True)
            shutil.copy2(out, md / out.name)
            print("mirrored " + str(md / out.name))
    except Exception as exc:
        print("mirror skipped: " + str(exc))


def main():
    for lang in ("en", "de", "zh"):
        render(lang)


if __name__ == "__main__":
    main()
