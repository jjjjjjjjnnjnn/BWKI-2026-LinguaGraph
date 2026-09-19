#!/usr/bin/env python3
"""Fig v2-cells: Harness-v2 P0/P1/P2/P3 social-F1 + EN-F1 grouped bars. Zero API.

Values are a HARDCODED snapshot transcribed from
research/mimo_spark_replication/V2_MATRIX.json (commit-pinned; reaudit 2026-09-19:
no json.load — V2_MATRIX.json updates do NOT propagate to this figure; re-transcribe + rerun manually).
Writes outputs/figures/fig_v2_cells{,_de,_zh}.png.
A2 denominator (fails-as-0); glm P3 carries serving-drift caveat (REPORT §7).
Encoding: color = cell (grey P0 / blue P1 / amber P2 / green P3),
hatch = anchor (plain glm-5.2 / slashed deepseek-flash / dotted sensenova-6.8),
cross-hatched pink = big-pickle P3 descriptive.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import matplotlib.patches as mpatches

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(BASE, "outputs", "figures")
os.makedirs(OUT, exist_ok=True)

# (anchor, P0, P1, P2, P3) social-F1 — TRANSCRIBED from V2_MATRIX.json rows, not read (see docstring)
SOC = {
    "glm-5.2":       (0.1382, 0.4612, 0.1292, 0.5441),
    "deepseek-flash": (0.1116, 0.5348, 0.1779, 0.5439),
    "sensenova-6.8": (0.1019, 0.3675, 0.1203, 0.3954),
}
EN = {
    "glm-5.2":       (0.0000, 0.3095, 0.0185, 0.3148),
    "deepseek-flash": (0.0046, 0.2333, 0.1357, 0.2148),
    "sensenova-6.8": (0.0000, 0.0370, 0.0000, 0.0370),
}
BP_SOC, BP_EN = 0.5804, 0.3765  # big-pickle P3 descriptive (partial-46 P0 control)
CELLS = ["P0 (v1)", "P1 CARD", "P2 LANG", "P3 BOTH"]
CELL_COL = ["#94a3b8", "#38bdf8", "#fbbf24", "#34d399"]  # color = cell
ANCHORS = ["glm-5.2", "deepseek-flash", "sensenova-6.8"]
HATCH = ["", "///", "..."]  # hatch = anchor
BP_COL, BP_HATCH = "#f472b6", "xx"

CAPTIONS = {
    "": ("Harness v2: cardinality fix lifts social F1 (P1/P3), language fix alone does not (P2); "
         "EN recovers only via cardinality. A2 denominator; glm P3 with serving-drift caveat. "
         "Source: V2_MATRIX.json, REPORT §7."),
    "_de": ("Harness v2: Kardinalitäts-Fix hebt Social-F1 (P1/P3), Sprach-Fix allein nicht (P2); "
            "EN erholt sich nur via Kardinalität. A2-Nenner; glm-P3 mit Serving-Drift-Caveat. "
            "Quelle: V2_MATRIX.json, REPORT §7."),
    "_zh": ("Harness v2：基数修复提升社会 F1（P1/P3），纯语言修复无效（P2）；英文仅随基数回升。"
            "A2 分母；glm P3 带有服务漂移 caveat。来源：V2_MATRIX.json，REPORT §7。"),
}
TITLES = {"": ("(a) Social F1 by cell", "(b) EN F1 by cell"),
          "_de": ("(a) Social-F1 je Zelle", "(b) EN-F1 je Zelle"),
          "_zh": ("（a）各 cell 社会 F1", "（b）各 cell 英文 F1")}

for suf in ("", "_de", "_zh"):
    plt.rcParams.update({"font.family": "sans-serif",
                         "font.sans-serif": (["Microsoft YaHei", "SimSun", "DejaVu Sans"]
                                             if suf == "_zh" else ["DejaVu Sans"])})
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.4))
    x = range(4)
    for i, a in enumerate(ANCHORS):
        v = SOC[a]
        ax[0].bar([p + (i - 1) * 0.22 for p in x], v, width=0.2,
                  color=CELL_COL, hatch=HATCH[i], edgecolor="white")
    ax[0].bar([3 + 2 * 0.22], [BP_SOC], width=0.2, color=BP_COL, hatch=BP_HATCH, edgecolor="white")
    ax[0].set_xticks(list(x));
    ax[0].set_xticklabels(CELLS, fontsize=8)
    ax[0].set_ylim(0, 0.65);
    ax[0].set_title(TITLES[suf][0]);
    ax[0].set_ylabel("Social F1 (A2)")
    for i, a in enumerate(ANCHORS):
        v = EN[a]
        ax[1].bar([p + (i - 1) * 0.22 for p in x], v, width=0.2,
                  color=CELL_COL, hatch=HATCH[i], edgecolor="white")
    ax[1].bar([3 + 2 * 0.22], [BP_EN], width=0.2, color=BP_COL, hatch=BP_HATCH, edgecolor="white")
    ax[1].set_xticks(list(x));
    ax[1].set_xticklabels(CELLS, fontsize=8)
    ax[1].set_ylim(0, 0.45);
    ax[1].set_title(TITLES[suf][1]);
    ax[1].set_ylabel("EN F1 (A2)")
    for a_ in ax:
        cell_handles = [mpatches.Patch(facecolor=c, edgecolor="white", label=l)
                        for c, l in zip(CELL_COL, CELLS)]
        anchor_handles = [mpatches.Patch(facecolor="white", hatch=h, edgecolor="black", label=l)
                          for h, l in zip(HATCH + [BP_HATCH],
                                          ANCHORS + ["big-pickle P3*"])]
        leg1 = a_.legend(handles=cell_handles, fontsize=6.5, loc="upper left", title="cell")
        a_.add_artist(leg1)
        a_.legend(handles=anchor_handles, fontsize=6.5, loc="upper right", title="anchor")
    fig.suptitle("Fig v2-cells — Harness v2 factor test (seed-foreign replication)", fontsize=11)
    fig.text(0.01, 0.01, CAPTIONS[suf] + " *descriptive (P0 partial-46).", fontsize=7, wrap=True,
             ha="left", va="bottom")
    fig.tight_layout(rect=[0, 0.06, 1, 0.94])
    fp = os.path.join(OUT, "fig_v2_cells%s.png" % suf)
    fig.savefig(fp, dpi=150)
    plt.close(fig)
    print("wrote", fp)
