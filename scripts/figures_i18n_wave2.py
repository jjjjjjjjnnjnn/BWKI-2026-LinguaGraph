#!/usr/bin/env python3
"""LinguaGraph -- Figure i18n renderer WAVE 2 (DE/ZH variants for 15 EN-only figs).

Covers the 15 figures that are EN-only after wave 1 (fig3/fig7/fig4_null_model):
  fig1_lds_k_heatmap, fig4_lds_heatmap, fig4_ablation, fig5_falsification,
  fig5_hds_distribution, fig6_coverage, fig6_cds_comparison, fig_wikipedia_lds,
  figure1_lds_distribution, figure3_topic_comparison, fig_a7_1..5.

DESIGN (same pattern as scripts/figures_i18n.py: T={de,zh} dict + frozen asserts):
  * Every numeric value below is FROZEN from the published EN artefact
    (EN PNG companion CSV, archived JSON snapshot, or tracked history file).
    The renderer NEVER recomputes frozen numbers from live sources that have
    drifted since publication. Runtime asserts guard each frozen value; the
    EN re-render is pixel-compared against the existing EN PNG (gate).
  * Red lines:
    - fig5_hds_distribution: chrome-overlay translation ONLY (title/xlabel/
      ylabel). The June-2026 generation was order-dependent (set-iteration in
      compute_hds) and is not reproducible; bars/annotations stay pixel-
      identical. No fig5 CSV is written (counts unrecoverable by design).
    - fig6_cds_comparison: chrome-overlay translation ONLY (title/ylabel/
      xtick level names; legend+finding box stay EN). Pixel forensics shows
      the math-college blue bar (~0.27 implied) and physics-middle orange
      bar (~0.028 implied) match NO committed physics_comparison.json
      snapshot (8ad379a/897f04e/current); re-rendering would falsify bars.
      No fig6_cds CSV is written.
    - fig6_coverage: data frozen from 7d31a32 coverage_scores.json (4 systems,
      S1 = overall quirk replicated); current
      config/expert_graphs/coverage_scores.json is NRW-only and would
      falsify the figure if recomputed.
    - fig5_falsification panel B: means frozen from CSV (hash-order unstable
      across processes); stds are cosmetic-only (<0.01 asserted). Panel C:
      frozen 19-model fallback rows (live dir must NOT be rescanned).
    - fig_wikipedia_lds: frozen all-1.0 artefact values (see
      docs/BASELINE_LEDGER.md S7 Latin-only alignment artefact); empty/unknown
      gloss topics excluded (matches archived 20260912 CSV, 5 topics).
    - fig_a7_5 strict-gloss values frozen from CSV (0.6992/...); live JSON was
      revised afterwards (M13 fix 0.699->0.709) and would falsify bars.
  * If any frozen assert or the EN pixel gate fails for a figure, that figure
    is SKIPPED (no output) and reported -- differing => stop & report, the
    remaining figures still render. Exit code 1 when anything was skipped.

Usage:
    python scripts/figures_i18n_wave2.py --lang de
    python scripts/figures_i18n_wave2.py --lang all --fig fig_a7_1
    python scripts/figures_i18n_wave2.py --lang all --check   # gates only

Outputs (new files only; existing EN PNGs/CSVs are never overwritten):
    outputs/figures/<stem>_de.png, <stem>_zh.png (dpi 300, Agg)
    + missing data CSVs (wiki/heatmap/cds_comparison/figure1/figure3)
    mirrored to cognitive-space/web/figures/ (new files only).
"""

import argparse
import csv
import shutil
import sys
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs" / "figures"
WEBFIG_DIR = PROJECT_DIR / "cognitive-space" / "web" / "figures"
MPL_FONTS = Path(matplotlib.matplotlib_fname()).parent / "fonts" / "ttf"
DEJA = str(MPL_FONTS / "DejaVuSans.ttf")
DEJA_B = str(MPL_FONTS / "DejaVuSans-Bold.ttf")
YAHEI = r"C:\Windows\Fonts\msyh.ttc"

PAIRS = ["ZH-EN", "DE-EN", "ZH-DE"]

T = {
    "de": {
        "f1_title": "LDS-K: Sprachübergreifende Divergenz der Wissensstruktur",
        "f1_xlabel": "Sprachpaar", "f1_ylabel": "Wissensdomäne",
        "f1_cbar": "LDS-K (0 = identisch, 1 = völlig divergent)",
        "f1_domains": ["Analysis", "Lineare Algebra", "Statistik",
                       "Grundschule", "Mittelstufe", "Geometrie"],
        "h4_title": "LDS nach Thema × Sprachpaar",
        "h4_avg": "Mittlere LDS",
        "h4_cbar": "LDS (höher = divergenter)",
        "h4_topics": ["Freiheit", "Gerechtigkeit", "Verantwortung", "Erfolg"],
        "ab_title": "LDS-Ablation: Was geschieht, wenn wir die Struktur aufbrechen?",
        "ab_xlabel": "Sprachpaar",
        "ab_conds": ["Vollständig (Baseline)", "Ohne Sprachlabels", "Zufallsgraph"],
        "f5_a": "A: Zufälliger Sprachentausch",
        "f5_b": "B: Graph-Permutation",
        "f5_c": "C: Modell-F1",
        "f5_base": "Basislinie", "f5_swap": "Zufallstausch", "f5_perm": "Permutiert",
        "f5_f1": "F1-Wert",
        "h5_title": "Verteilung der Voraussetzungskettentiefe",
        "h5_xlabel": "Kettentiefe (HDS)",
        "h5_ylabel": "Anzahl der Konzepte",
        "cov_title": "Gesamt-Curriculum-Abdeckung",
        "cov_ylabel": "Vom Lehrbuch abgedeckte Curriculum-Konzepte",
        "cov_stage": "Abdeckung pro Stufe (Detail)",
        "cov_cov": "Abdeckung",
        "cov_systems": ["China", "UK", "USA", "NRW\n(Deutschland)"],
        "cov_note": ("Höher = Curriculum-\nKonzepte im Lehrbuch-\n"
                     "Wissensgraphen gefunden\n\n"
                     "China: zentralisiertes Curriculum\n"
                     "NRW: detaillierte Vorgaben je Zweig\n"
                     "USA: breite Richtlinien, geringe Treffer"),
        "c6_title": "CDS nach Bildungsstufe: Mathematik vs. Physik",
        "c6_ylabel": "CDS (Konzeptdichte)",
        "c6_levels": ["Grundschule", "Mittelstufe", "Oberstufe", "Hochschule"],
        "c6_legend": ["Mathematik", "Physik"],
        "c6_find": ("Fächerübergreifender Befund:\n\n"
                    "Mathe-CDS-Spitze:    Mittelstufe\n"
                    "  (CDS = 0.270)\n\n"
                    "Physik-CDS-Spitze: Hochschule\n"
                    "  (CDS = 0.065)\n\n"
                    "Disziplinen zeigen\n"
                    "unterschiedliche Dichtemuster:\n"
                    "  Mathe am dichtesten im Fundament,\n"
                    "  Physik am dichtesten in der\n"
                    "  fortgeschrittenen Spezialisierung."),
        "wiki_left": "Wikipedia-Konzept-LDS pro Thema",
        "wiki_x": "Soziales Thema", "wiki_y": "LDS (Wikipedia)",
        "wiki_right": "Wikipedia Sozial vs Lehrbuchwissen",
        "wiki_pair": "Sprachpaar",
        "wiki_text": "Lehrbuch (LDS-K)", "wiki_soc": "Wikipedia (Sozial)",
        "wiki_topics": ["Freiheit", "Gerechtigkeit", "Verantwortung",
                        "Heimat", "Erfolg"],
        "g1_title": "Sprachdrift-Wert nach Thema und Sprachpaar",
        "g1_x": "Thema",
        "g1_topics": ["Freiheit", "Gerechtigkeit", "Gesamt",
                      "Verantwortung", "Erfolg"],
        "g3_title": "Konzeptdrift nach Thema",
        "g3_x": "Mittlere LDS (± SD)",
        "g3_hi": "Hohe Drift-Schwelle", "g3_mid": "Mittlere Drift-Schwelle",
        "a1_title": "Dreifacher Strukturvergleich: Mensch / LLM / sozial / Lehrbuch",
        "a1_y": "LDS (höher = divergenter)",
        "a1_series": ["Mensch N=15 (zwischen)", "LLM innersubjekt",
                      "Soziale Wikipedia", "Mathe-Lehrbuch (LDS-K)"],
        "a2_title": "LLM-innersubjekte LDS-C nach Thema",
        "a2_x": "Sprachpaar",
        "a2_topics": ["Freiheit", "Gerechtigkeit", "Verantwortung",
                      "Heimat", "Erfolg"],
        "a3_title": "LDS-K gegen Nullmodelle",
        "a3_labels": ["LDS-K (beobachtet)", "Struktur-Null", "Innersprach-Boden"],
        "a3_rand": "komplett zufällig = 1.0",
        "a4_a": "(A) Sprachsignal > Rauschboden",
        "a4_b": "(B) LMM: Code dominiert, Frame ~0",
        "a4_leg": ["LDS-C beobachtet", "Split-Half-Boden", "Label-Perm"],
        "a4_y2": "Marginaler Effekt auf Jaccard-Ähnlichkeit",
        "a4_x2": ["gleiche\nSprache", "gleicher\nFrame"],
        "a5_a": "(A) Mathe-LDS-K: Richtungs- & Kanten-Sensitivität",
        "a5_b": "(B) Soziale Wikipedia: Alignment-Strenge",
        "a5_leg1": ["direkt", "ungerichtet", "nur-Knoten"],
        "a5_leg2": ["locker (kanonisch)", "strikt (Gloss)"],
        "a5_floor": "Rauschboden 0.97",
    },
    "zh": {
        "f1_title": "LDS-K：跨语言知识结构差异",
        "f1_xlabel": "语言对", "f1_ylabel": "知识领域",
        "f1_cbar": "LDS-K（0 = 完全相同，1 = 完全分歧）",
        "f1_domains": ["微积分", "线性代数", "统计", "小学", "初中", "几何"],
        "h4_title": "各主题 × 语言对 LDS",
        "h4_avg": "平均 LDS",
        "h4_cbar": "LDS（越高分歧越大）",
        "h4_topics": ["自由", "正义", "责任", "成功"],
        "ab_title": "LDS 消融：当结构被破坏时会发生什么？",
        "ab_xlabel": "语言对",
        "ab_conds": ["完整（基线）", "无语言标签", "随机图"],
        "f5_a": "A：随机语言交换",
        "f5_b": "B：图置换",
        "f5_c": "C：模型 F1",
        "f5_base": "基线", "f5_swap": "随机交换", "f5_perm": "置换",
        "f5_f1": "F1 分数",
        "h5_title": "前提链深度分布",
        "h5_xlabel": "链深度（HDS）",
        "h5_ylabel": "概念数量",
        "cov_title": "课程总体覆盖率",
        "cov_ylabel": "教材覆盖的课程概念",
        "cov_stage": "分阶段覆盖率（明细）",
        "cov_cov": "覆盖率",
        "cov_systems": ["中国", "英国", "美国", "北威州\n（德国）"],
        "cov_note": ("越高 = 课程概念\n在教材知识图谱\n中的命中越多\n\n"
                     "中国：集中统一课程\n"
                     "北威州：分轨道详细大纲\n"
                     "美国：宽泛指南，命中低"),
        "c6_title": "各教育阶段 CDS：数学 vs 物理",
        "c6_ylabel": "CDS（概念密度）",
        "c6_levels": ["小学", "初中", "高中", "大学"],
        "c6_legend": ["数学", "物理"],
        "c6_find": ("跨学科发现：\n\n"
                    "数学 CDS 峰值：初中\n"
                    "  （CDS = 0.270）\n\n"
                    "物理 CDS 峰值：大学\n"
                    "  （CDS = 0.065）\n\n"
                    "不同学科密度模式不同：\n"
                    "  数学在基础阶段最密，\n"
                    "  物理在高级专业阶段最密。"),
        "wiki_left": "各主题维基概念 LDS",
        "wiki_x": "社会主题", "wiki_y": "LDS（维基）",
        "wiki_right": "维基社会 vs 教材知识",
        "wiki_pair": "语言对",
        "wiki_text": "教材（LDS-K）", "wiki_soc": "维基（社会）",
        "wiki_topics": ["自由", "正义", "责任", "家园", "成功"],
        "g1_title": "各主题与语言对的语言漂移得分",
        "g1_x": "主题",
        "g1_topics": ["自由", "正义", "总体", "责任", "成功"],
        "g3_title": "各主题概念漂移",
        "g3_x": "平均 LDS（± 标准差）",
        "g3_hi": "高漂移阈值", "g3_mid": "中漂移阈值",
        "a1_title": "三方结构分歧：人类 / LLM / 社会 / 教材",
        "a1_y": "LDS（越高分歧越大）",
        "a1_series": ["人类 N=15（组间）", "LLM 被试内",
                      "社会维基", "数学教材（LDS-K）"],
        "a2_title": "LLM 被试内 LDS-C（分主题）",
        "a2_x": "语言对",
        "a2_topics": ["自由", "正义", "责任", "家园", "成功"],
        "a3_title": "LDS-K 与零模型对照",
        "a3_labels": ["LDS-K（观测）", "结构零模型", "语言内基线"],
        "a3_rand": "完全随机 = 1.0",
        "a4_a": "(A) 语言信号 > 噪声基线",
        "a4_b": "(B) LMM：语言编码主导，框架 ~0",
        "a4_leg": ["LDS-C 观测", "折半基线", "标签置换"],
        "a4_y2": "对 Jaccard 相似度的边际效应",
        "a4_x2": ["相同\n语言", "相同\n框架"],
        "a5_a": "(A) 数学 LDS-K：方向与边敏感性",
        "a5_b": "(B) 社会维基：对齐严格度",
        "a5_leg1": ["有向", "无向", "仅节点"],
        "a5_leg2": ["宽松（规范）", "严格（注释）"],
        "a5_floor": "噪声基线 0.97",
    },
}

# ── FROZEN values (provenance in module docstring) ──────────────────────
FROZEN = {
    # fig1_lds_k_heatmap ← outputs/figures/fig1_lds_k_data.csv
    # (recompute from config/expert_graphs/*.json verified identical)
    "fig1": {
        "domains": ["Calculus", "Linear Algebra", "Statistics",
                    "Elementary", "Middle School", "Geometry"],
        "ZH-EN": [0.8662, 0.9556, 0.95, 0.9681, 1.0, 1.0],
        "DE-EN": [0.9061, 0.9501, 0.95, 0.9681, 1.0, 1.0],
        "ZH-DE": [0.5748, 0.6127, 0.1624, 0.2946, 0.8417, 0.1429],
    },
    # fig4_lds_heatmap ← linguaGraph.db WIKIPEDIA_CORPUS rows, last-wins per
    # topic×pair (matches published averages ZH-DE 0.907 / DE-EN 0.901 /
    # ZH-EN 0.802 from commit 2ffd963 message)
    "h4": {
        "topics": ["freedom", "justice", "responsibility", "success"],
        "zh-de": [0.8551, 0.8913, 0.881, 1.0],
        "zh-en": [0.8205, 0.6989, 0.7727, 0.9167],
        "de-en": [0.8889, 0.8765, 0.8378, 1.0],
        "avg": {"zh-de": 0.9069, "zh-en": 0.8022, "de-en": 0.9008},
    },
    # fig4_ablation ← outputs/figures/fig4_ablation_data.csv
    # (recompute via _archive/.../fig4_ablation.py on live aligned_data.json
    # verified identical: 219 groups / 525 relations)
    "ab": {
        "conds": ["Full (baseline)", "No Language Labels", "Random Graph"],
        "ZH-EN": [0.9336, 0.9141274238227147, 1.0],
        "DE-EN": [0.9382, 0.9136490250696379, 1.0],
        "ZH-DE": [0.5188, 0.4444444444444444, 1.0],
    },
    # fig5_falsification ← outputs/figures/fig5_falsification_data.csv
    # (baseline + swap stable across processes; perm means frozen, stds
    # cosmetic only; panel C frozen 19-model fallback rows -- live
    # data/model_comparison grew to 19 files and must NOT be rescanned)
    "f5": {
        "base": {"ZH-EN": 0.9336, "DE-EN": 0.9382, "ZH-DE": 0.5188},
        "swap": {"ZH-EN": 0.9141, "DE-EN": 0.9136, "ZH-DE": 0.4444},
        "perm": {"ZH-EN": 0.9562, "DE-EN": 0.9561, "ZH-DE": 0.7159},
        "models": {
            "deepseek-chat": 0.5465, "deepseek-v4-flash": 0.6078,
            "deepseek-v4-pro": 0.5934, "glm-5.1": 0.5897,
            "glm-5.2": 0.5909, "glm-5": 0.5921, "hy3-preview": 0.6741,
            "kimi-k2.5": 0.5884, "kimi-k2.6": 0.6261,
            "mimo-v2.5-pro": 0.6735, "mimo-v2.5": 0.6275,
            "minimax-m2.5": 0.5759, "minimax-m2.7": 0.5662,
            "minimax-m3": 0.5797, "qwen3.5-plus": 0.6130,
            "qwen3.6-plus": 0.5766, "qwen3.7-max": 0.6143,
            "qwen-max": 0.6610, "qwen-plus": 0.6659,
        },
    },
    # fig6_coverage ← 7d31a32:config/expert_graphs/coverage_scores.json
    "cov": {
        "order": ["China", "UK", "US", "NRW"],
        "overall": {"China": 0.954, "UK": 0.3728, "US": 0.1723, "NRW": 0.1271},
        "matched": {"China": 83, "UK": 148, "US": 366, "NRW": 38},
        "total": {"China": 87, "UK": 397, "US": 2124, "NRW": 299},
        "stages": {
            "China": [1.0, 0.9474, 0.9615, 0.9167],
            "UK": [0.3333, 0.4, 0.4167, 0.4048, 0.4808, 0.4386, 0.3, 0.2833],
            "US": [0.1794, 0.1794, 0.1794],
            "NRW": [0.2069, 0.1875, 0.1525, 0.1667, 0.0256, 0.0755],
        },
    },
    # fig6_cds_comparison ← 8ad379a:outputs/physics_comparison.json
    "c6": {
        "levels": ["elementary", "middle", "high", "college"],
        "math": [0.2162, 0.2705, 0.0731, 0.0415],
        "phys": [0.0, 0.0468, 0.0359, 0.0654],
    },
    # fig_wikipedia_lds ← _archive/.../20260912_superseded CSV (all-1.0
    # artefact, BASELINE_LEDGER S7); 5 topics only
    "wiki": {
        "topics": ["freedom", "home", "justice", "responsibility", "success"],
        "per": [1.0, 1.0, 1.0],
        "pooled": {"ZH-EN": 1.0, "DE-EN": 1.0, "ZH-DE": 1.0},
        "textbook": {"ZH-EN": 0.9336, "DE-EN": 0.9382, "ZH-DE": 0.5188},
    },
    # figure1 ← June-2026 DB: 15 WIKIPEDIA_CORPUS rows + 2 overall/en-de
    # rows (S002+S008, still present in linguaGraph.db; 15+2 = the "17
    # analyses" of the June-18 lds_report). topics sorted => 5 groups;
    # the overall group shows zh=0 + en-de=1.0 (green bar only).
    "g1": {
        "topics": ["freedom", "justice", "overall", "responsibility",
                   "success"],
        "pairs": ["zh-de", "zh-en", "en-de"],
        "rows": [
            ("freedom", "de-en", 0.8718), ("freedom", "de-en", 0.8889),
            ("freedom", "zh-de", 0.8209), ("freedom", "zh-de", 0.8551),
            ("freedom", "zh-en", 0.614), ("freedom", "zh-en", 0.8205),
            ("justice", "de-en", 0.8765), ("justice", "zh-de", 0.8913),
            ("justice", "zh-en", 0.6989),
            ("overall", "en-de", 1.0), ("overall", "en-de", 1.0),
            ("responsibility", "de-en", 0.8378),
            ("responsibility", "zh-de", 0.881),
            ("responsibility", "zh-en", 0.7727),
            ("success", "de-en", 1.0), ("success", "zh-de", 1.0),
            ("success", "zh-en", 0.9167),
        ],
    },
    # figure3 ← same 17 rows, pooled per topic (population std)
    "g3": {
        "freedom": (0.8118667, 0.091926),
        "justice": (0.8222333, 0.087419),
        "overall": (1.0, 0.0),
        "responsibility": (0.8305, 0.044514),
        "success": (0.9722333, 0.039268),
    },
    # fig_a7_* ← outputs/figures/fig_a7_*.csv (+ data/lds_c JSONs, Aug-08)
    "a1": {
        "Human": {"ZH-EN": 0.9634, "DE-EN": 0.9324, "ZH-DE": 0.9364},
        "LLM": {"ZH-EN": 0.9552, "DE-EN": 0.93, "ZH-DE": 0.9446},
        "Wiki": {"ZH-EN": 0.6976, "DE-EN": 0.7234, "ZH-DE": 0.8191},
        "Math": {"ZH-EN": 0.9336, "DE-EN": 0.9382, "ZH-DE": 0.5188},
    },
    "a2": {
        "topics": ["Freiheit", "Gerechtigkeit", "Verantwortung",
                   "Heimat", "Erfolg"],
        "ZH-EN": [0.9286, 0.9524, 0.9529, 0.9444, 0.9775],
        "DE-EN": [0.9012, 0.973, 0.9333, 0.8689, 0.9474],
        "ZH-DE": [0.939, 0.9512, 0.9178, 0.9571, 0.9651],
    },
    "a3": {
        "full": {"ZH-EN": 0.9336, "DE-EN": 0.9382, "ZH-DE": 0.5188},
        "structure": {"ZH-EN": 0.9571, "DE-EN": 0.9568, "ZH-DE": 0.7154},
        "floor": {"ZH-EN": 0.9582, "DE-EN": 0.9233, "ZH-DE": 0.9219},
    },
    "a4": {
        "obs": {"ZH-EN": 0.9552, "DE-EN": 0.93, "ZH-DE": 0.9446},
        "floor": {"ZH-EN": 0.8745, "DE-EN": 0.8456, "ZH-DE": 0.8618},
        "perm": {"ZH-EN": 0.8786, "DE-EN": 0.8797, "ZH-DE": 0.8787},
        "same_lang": (0.03788250985966519, 0.008848532756617261,
                      9.08855067669982e-05),
        "same_frame": (0.001131265105925696, 0.008848532756316127,
                       0.8988149174561388),
    },
    "a5": {
        "directed": {"ZH-EN": 0.9336, "DE-EN": 0.9382, "ZH-DE": 0.5188},
        "undirected": {"ZH-EN": 0.9329, "DE-EN": 0.9377, "ZH-DE": 0.5154},
        "node_only": {"ZH-EN": 0.9141, "DE-EN": 0.9136, "ZH-DE": 0.4444},
        "loose": {"ZH-EN": 0.6976, "DE-EN": 0.7234, "ZH-DE": 0.8191},
        "strict": {"ZH-EN": 0.6992, "DE-EN": 0.7705, "ZH-DE": 0.8511},
    },
}

FONT = {"de": ["DejaVu Sans"], "zh": ["Microsoft YaHei", "SimSun", "DejaVu Sans"]}
EN_RC = {"font.size": 11, "axes.titlesize": 14, "axes.labelsize": 12}


def setup(lang, base_size=11, title_size=14, label_size=12, tight=True):
    plt.rcdefaults()
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": FONT[lang],
        "font.size": base_size, "axes.titlesize": title_size,
        "axes.labelsize": label_size,
        "figure.dpi": 150, "savefig.dpi": 300,
        "savefig.bbox": "tight" if tight else "standard",
        "savefig.pad_inches": 0.15,
        "axes.unicode_minus": False,
    })


def setup_en_plain():
    """Original scripts without rcParams (fig1/falsification/coverage/wiki/
    ablation): pure matplotlib defaults, full-frame save."""
    plt.rcdefaults()


def setup_en_legacy():
    """rcParams of scripts/generate_paper_figures.py (June 2026) for EN gate."""
    plt.rcdefaults()
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
        "font.size": 11, "axes.titlesize": 14, "axes.labelsize": 12,
        "figure.dpi": 150, "savefig.dpi": 300,
        "savefig.bbox": "tight", "savefig.pad_inches": 0.15,
    })


def png_mae(a_path, b_path):
    a = np.array(Image.open(a_path).convert("RGB")).astype(float)
    b = np.array(Image.open(b_path).convert("RGB")).astype(float)
    if a.shape != b.shape:
        return None, f"shape {a.shape} vs {b.shape}"
    d = np.abs(a - b)
    return float(d.mean()), None


GATE_TOL = 1.5  # mean abs pixel error; calibrated: exact re-render gives 0.0


def verify_en(stem, render_en, check_only=False):
    """Render EN variant to temp file, pixel-compare with committed EN PNG."""
    ref = OUTPUT_DIR / f"{stem}.png"
    if not ref.exists():
        return False, f"EN reference missing: {ref.name}"
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
        tmp = tf.name
    try:
        with _warnings.catch_warnings():
            _warnings.simplefilter("error", UserWarning)
            try:
                render_en(tmp)
            except UserWarning as e:
                if "Glyph" in str(e):
                    return False, f"tofu glyph in EN render: {e}"
                raise
        mae, err = png_mae(ref, tmp)
    finally:
        try:
            Path(tmp).unlink()
        except OSError:
            pass
    if err is not None:
        return False, err
    if mae > GATE_TOL:
        return False, f"EN pixel gate MAE={mae:.2f} > {GATE_TOL}"
    return True, f"EN gate MAE={mae:.3f}"


def save_and_mirror(fig, stem, lang, bbox=None):
    out = OUTPUT_DIR / f"{stem}_{lang}.png"
    with _warnings.catch_warnings():
        _warnings.simplefilter("error", UserWarning)
        try:
            if bbox:
                fig.savefig(out, dpi=300, bbox_inches=bbox)
            else:
                fig.savefig(out, dpi=300)
        except UserWarning as e:
            if "Glyph" in str(e):
                raise RuntimeError(f"tofu glyph at savefig: {e}")
            raise
    plt.close(fig)
    dst = WEBFIG_DIR / out.name
    if not dst.exists():
        shutil.copy2(out, dst)
        mir = "mirrored"
    else:
        mir = "mirror-exists"
    print(f"  [OK] {out.name} ({out.stat().st_size // 1024} KB, {mir})")
    return out


def read_en_csv(name):
    rows = list(csv.DictReader((OUTPUT_DIR / name).open(encoding="utf-8")))
    return rows


def fail(msg):
    print(f"  [SKIP] {msg}")
    return False


def audit_T():
    """No CJK codepoints may appear in DE strings (tofu guard)."""
    import re
    bad = []
    for k, v in T["de"].items():
        vals = v if isinstance(v, list) else [v]
        for s in vals:
            if re.search(r"[\u4e00-\u9fff\u3040-\u30ff]", s):
                bad.append(k)
    if bad:
        raise SystemExit(f"T-dict audit failed (CJK in DE): {sorted(set(bad))}")
    print("  [OK] T-dict audit: no CJK in DE strings")


import warnings as _warnings


def render_clean(fn, *args, **kwargs):
    """Run a renderer; any missing-glyph warning becomes an exception."""
    with _warnings.catch_warnings():
        _warnings.simplefilter("error", UserWarning)
        try:
            return fn(*args, **kwargs)
        except UserWarning as e:
            if "Glyph" in str(e) and "missing from font" in str(e):
                raise RuntimeError(f"tofu glyph: {e}")
            raise


# ── fig1_lds_k_heatmap ────────────────────────────────────────────────
def check_fig1():
    fr = FROZEN["fig1"]
    rows = {r["domain"]: r for r in read_en_csv("fig1_lds_k_data.csv")}
    assert len(rows) == 6, rows.keys()
    for i, d in enumerate(fr["domains"]):
        for p in PAIRS:
            assert abs(float(rows[d][p]) - fr[p][i]) < 1e-9, (d, p)
    assert abs(fr["ZH-EN"][0] - 0.8662) < 1e-9 and abs(fr["ZH-DE"][5] - 0.1429) < 1e-9


def render_fig1(lang, path=None):
    fr = FROZEN["fig1"]
    t = T[lang] if lang in T else None
    domains = (t["f1_domains"] if t else fr["domains"])
    pairs = PAIRS
    data = np.array([[fr[p][i] for p in pairs] for i in range(len(domains))])
    fig, ax = plt.subplots(figsize=(6, 4))
    im = ax.imshow(data, cmap="YlOrRd", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(pairs)))
    ax.set_xticklabels(pairs, fontsize=10)
    ax.set_yticks(range(len(domains)))
    ax.set_yticklabels(domains, fontsize=9)
    if t:
        ax.set_xlabel(t["f1_xlabel"], fontsize=11)
        ax.set_ylabel(t["f1_ylabel"], fontsize=11)
        ax.set_title(t["f1_title"], fontsize=12)
    else:
        ax.set_xlabel("Language Pair", fontsize=11)
        ax.set_ylabel("Knowledge Domain", fontsize=11)
        ax.set_title("LDS-K: Cross-Language Knowledge Structure Divergence",
                     fontsize=12)
    for i in range(len(domains)):
        for j in range(len(pairs)):
            val = data[i, j]
            color = "white" if val > 0.6 else "black"
            ax.text(j, i, f"{val:.3f}", ha="center", va="center",
                    fontsize=8, color=color)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(t["f1_cbar"] if t else
                   "LDS-K (0 = identical, 1 = fully divergent)", fontsize=9)
    plt.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
        plt.close(fig)
        return None
    return fig


# ── fig4_lds_heatmap (legacy June-22; superseded, kept for reference) ──
def check_h4():
    fr = FROZEN["h4"]
    for k in ("zh-de", "zh-en", "de-en"):
        assert len(fr[k]) == 4
    assert abs(sum(fr["zh-de"]) / 4 - fr["avg"]["zh-de"]) < 1e-4
    assert abs(sum(fr["zh-en"]) / 4 - fr["avg"]["zh-en"]) < 1e-4
    assert abs(sum(fr["de-en"]) / 4 - fr["avg"]["de-en"]) < 1e-4
    # published averages, commit 2ffd963 message (3-dec)
    assert round(fr["avg"]["zh-de"], 3) == 0.907
    assert round(fr["avg"]["de-en"], 3) == 0.901
    assert round(fr["avg"]["zh-en"], 3) == 0.802


def render_h4(lang, path=None):
    fr = FROZEN["h4"]
    t = T[lang] if lang in T else None
    topics = fr["topics"]
    tlabels = [x.capitalize() for x in topics] if not t else t["h4_topics"]
    pair_keys = ["zh-de", "zh-en", "de-en"]
    pair_labels = ["ZH–DE", "ZH–EN", "DE–EN"]
    matrix = np.array([[fr[pk][i] for pk in pair_keys] for i in range(4)])
    avg = [fr["avg"][pk] for pk in pair_keys]
    fig, (ax_heat, ax_avg) = plt.subplots(1, 2, figsize=(9, 5),
                                          gridspec_kw={"width_ratios": [2, 1]})
    im = ax_heat.imshow(matrix, aspect="auto", cmap=plt.cm.YlOrRd,
                        vmin=0, vmax=1)
    ax_heat.set_xticks(range(len(pair_labels)))
    ax_heat.set_xticklabels(pair_labels, fontsize=10)
    ax_heat.set_yticks(range(len(topics)))
    ax_heat.set_yticklabels(tlabels, fontsize=10)
    ax_heat.set_title(t["h4_title"] if t else "LDS by Topic × Language Pair",
                      fontweight="bold", pad=10)
    for i in range(len(topics)):
        for j in range(len(pair_keys)):
            v = matrix[i, j]
            color = "white" if v > 0.6 else "black"
            ax_heat.text(j, i, f"{v:.2f}", ha="center", va="center",
                         fontsize=9, color=color)
    cbar = plt.colorbar(im, ax=ax_heat, shrink=0.7, pad=0.04)
    cbar.set_label(t["h4_cbar"] if t else "LDS (higher = more divergent)",
                   fontsize=9)
    bars = ax_avg.barh(pair_labels, avg, color=["#e74c3c", "#3498db", "#f39c12"],
                       height=0.5)
    ax_avg.set_title(t["h4_avg"] if t else "Average LDS", fontweight="bold")
    ax_avg.set_xlim(0, 1)
    ax_avg.spines["top"].set_visible(False)
    ax_avg.spines["right"].set_visible(False)
    for bar, v in zip(bars, avg):
        ax_avg.text(v + 0.02, bar.get_y() + bar.get_height() / 2,
                    f"{v:.2f}", ha="left", va="center", fontsize=10)
    plt.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
        plt.close(fig)
        return None
    return fig


# ── fig4_ablation (archived script geometry) ──────────────────────────
def check_ab():
    fr = FROZEN["ab"]
    rows = {r["condition"]: r for r in read_en_csv("fig4_ablation_data.csv")}
    for i, c in enumerate(fr["conds"]):
        for p in PAIRS:
            assert abs(float(rows[c][p]) - fr[p][i]) < 1e-9, (c, p)
    assert abs(fr["ZH-EN"][1] - 0.9141274238227147) < 1e-9
    assert abs(fr["ZH-DE"][1] - 0.4444444444444444) < 1e-9


def render_ab(lang, path=None):
    fr = FROZEN["ab"]
    t = T[lang] if lang in T else None
    conds = t["ab_conds"] if t else fr["conds"]
    pairs = PAIRS
    x = np.arange(len(pairs))
    width = 0.25
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#2563eb", "#ea580c", "#6b7280"]
    for i, (cn, key) in enumerate(zip(conds, fr["conds"])):
        vals = [fr[p][fr["conds"].index(key)] for p in pairs]
        bars = ax.bar(x + i * width, vals, width, label=cn, color=colors[i])
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=7)
    ax.set_xlabel(t["ab_xlabel"] if t else "Language Pair", fontsize=11)
    ax.set_ylabel("LDS", fontsize=11)
    ax.set_title(t["ab_title"] if t else
                 "LDS Ablation: What Happens When We Break the Structure?",
                 fontsize=12)
    ax.set_xticks(x + width)
    ax.set_xticklabels(pairs, fontsize=10)
    ax.legend(fontsize=9)
    ax.set_ylim(0, 1.15)
    plt.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
        plt.close(fig)
        return None
    return fig


# ── fig5_falsification ────────────────────────────────────────────────
def check_f5():
    fr = FROZEN["f5"]
    rows = list(read_en_csv("fig5_falsification_data.csv"))
    got = {(r["panel"], r["condition"]): r for r in rows}
    for p in PAIRS:
        assert abs(float(got[("A", "Baseline")][p]) - fr["base"][p]) < 1e-9
        assert abs(float(got[("A", "Random Swap")][p]) - fr["swap"][p]) < 1e-9
        assert abs(float(got[("B", "Permuted")][p]) - fr["perm"][p]) < 1e-9
    # panel C: 19-model fallback (no benchmark file); CSV has an extra n col
    mods = {r["condition"]: r for r in rows
            if r["panel"] == "C" and r["condition"] != "model"}
    assert set(mods) == set(fr["models"]), set(mods) ^ set(fr["models"])
    for n, v in fr["models"].items():
        assert abs(float(mods[n]["ZH-EN"]) - v) < 1e-9, (n, mods[n])


def f5_panel_stats():
    """Seeded recompute for cosmetic stds; means asserted frozen (hash-order
    unstable for panel B, so frozen CSV means are authoritative)."""
    sys.path.insert(0, str(PROJECT_DIR / "scripts" / "figures"))
    import fig5_falsification as F5
    from _lds_utils import load_aligned, get_lang_graphs
    aligned = load_aligned()
    assert len(aligned.get("aligned_groups", [])) == 219
    assert len(aligned.get("relations", [])) == 525
    lang_nodes, lang_edges = get_lang_graphs(aligned)
    base = F5.baseline_lds(lang_nodes, lang_edges)
    swap = F5.panel_a_random_swap(lang_nodes, lang_edges)
    perm = F5.panel_b_graph_permutation(lang_nodes, lang_edges)
    fr = FROZEN["f5"]
    for p in PAIRS:
        assert abs(base[p] - fr["base"][p]) < 1e-9, (p, base[p])
        assert abs(swap[p][0] - fr["swap"][p]) < 5e-5, (p, swap[p])
        assert abs(perm[p][0] - fr["perm"][p]) < 5e-3, (p, perm[p])
        assert perm[p][1] < 0.01, (p, perm[p])
    return swap, perm


def render_f5(lang, path=None, swap=None, perm=None):
    fr = FROZEN["f5"]
    t = T[lang] if lang in T else None
    pairs = PAIRS
    x = np.arange(len(pairs))
    width = 0.2
    f5a = t["f5_a"] if t else "A: Random Language Swap"
    f5b = t["f5_b"] if t else "B: Graph Permutation"
    f5c = t["f5_c"] if t else "C: Model F1"
    base_l = t["f5_base"] if t else "Baseline"
    swap_l = t["f5_swap"] if t else "Random Swap"
    perm_l = t["f5_perm"] if t else "Permuted"
    if swap is None:
        swap = {p: (fr["swap"][p], 0.0) for p in pairs}
    if perm is None:
        perm = {p: (fr["perm"][p], 0.001) for p in pairs}
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.5), sharey=False)
    ax = axes[0]
    for i, (label, vals, color, err) in enumerate([
            (base_l, [fr["base"][p] for p in pairs], "#2563eb", None),
            (swap_l, [swap[p][0] for p in pairs], "#ea580c",
             [swap[p][1] for p in pairs])]):
        offset = (i - 0.5) * width
        bars = ax.bar(x + offset, vals, width, label=label, color=color,
                      alpha=0.85)
        if err and any(err):
            ax.errorbar(x + offset, vals, yerr=err, fmt="none", capsize=3,
                        color="black", alpha=0.5)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=7)
    ax.set_title(f5a, fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(pairs, fontsize=9)
    ax.set_ylabel("LDS", fontsize=11)
    ax.set_ylim(0, 1.15)
    ax.legend(fontsize=8)
    ax = axes[1]
    for i, (label, vals, color, err) in enumerate([
            (base_l, [fr["base"][p] for p in pairs], "#2563eb", None),
            (perm_l, [perm[p][0] for p in pairs], "#6b7280",
             [perm[p][1] for p in pairs])]):
        offset = (i - 0.5) * width
        bars = ax.bar(x + offset, vals, width, label=label, color=color,
                      alpha=0.85)
        if err and any(err):
            ax.errorbar(x + offset, vals, yerr=err, fmt="none", capsize=3,
                        color="black", alpha=0.5)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=7)
    ax.set_title(f5b, fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(pairs, fontsize=9)
    ax.set_ylim(0, 1.15)
    ax.legend(fontsize=8)
    ax = axes[2]
    # frozen 19-model fallback branch (sorted names; 2-colour list cycles,
    # exactly like the original script)
    names = sorted(fr["models"].keys())
    f1s = [fr["models"][n] for n in names]
    bp = np.arange(len(names))
    bars = ax.bar(bp, f1s, 0.5, color=["#2563eb", "#16a34a"][:len(names)])
    for bar, val in zip(bars, f1s):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"{val:.3f}", ha="center", va="bottom", fontsize=8)
    ax.set_title(f5c, fontsize=10)
    ax.set_xticks(bp)
    ax.set_xticklabels(names, fontsize=7, rotation=15)
    ax.set_ylabel(t["f5_f1"] if t else "F1 Score", fontsize=11)
    ax.set_ylim(0, 1.15)
    plt.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
        plt.close(fig)
        return None
    return fig


# ── fig6_coverage (data: 7d31a32 coverage_scores.json, 4 systems) ──────
SYS_COLORS = {"NRW": "#2563eb", "UK": "#ea580c", "US": "#16a34a",
              "China": "#9333ea"}
SYS_LABELS_EN = {"NRW": "NRW\n(Germany)", "UK": "UK", "US": "USA",
                 "China": "China"}


def check_cov():
    fr = FROZEN["cov"]
    rows = {r["system"]: r for r in read_en_csv("fig6_coverage_data.csv")}
    for s in fr["order"]:
        assert abs(float(rows[s]["overall_coverage"]) - fr["overall"][s]) < 1e-9
        assert int(rows[s]["matched"]) == fr["matched"][s]
        assert int(rows[s]["total"]) == fr["total"][s]
    assert len(fr["stages"]["UK"]) == 8 and len(fr["stages"]["NRW"]) == 6
    assert len(fr["stages"]["US"]) == 3 and len(fr["stages"]["China"]) == 4


def render_cov(lang, path=None):
    fr = FROZEN["cov"]
    t = T[lang] if lang in T else None
    sys_labels = (t["cov_systems"] if t
                  else [SYS_LABELS_EN[s] for s in fr["order"]])
    overall = fr["overall"]
    systems = sorted(overall.keys(), key=lambda s: -overall[s])
    assert systems == fr["order"], systems
    vals = [overall[s] for s in systems]
    colors = [SYS_COLORS[s] for s in systems]
    labels = [sys_labels[fr["order"].index(s)] for s in systems]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    ax = axes[0]
    bars = ax.bar(range(len(systems)), vals, 0.5, color=colors, alpha=0.85)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{val * 100:.1f}%", ha="center", va="bottom", fontsize=9)
    ax.set_xticks(range(len(systems)))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel(t["cov_ylabel"] if t else
                  "Curriculum Concepts Covered by Textbook", fontsize=10)
    ax.set_title(t["cov_title"] if t else "Overall Curriculum Coverage",
                 fontsize=11)
    ax.set_ylim(0, 1.1)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))
    ax.text(0.98, 0.97, t["cov_note"] if t else
            "Higher = curriculum\nconcepts found in\ntextbook knowledge graph"
            "\n\nChina: centralized curriculum\nNRW: detailed per-track specs\n"
            "US: broad guidelines, low match",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=6.5, color="#555",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f8f9fa",
                      edgecolor="#ddd"))
    ax = axes[1]
    # NOTE: replicates the original grouping quirk -- the "overall" entry
    # also carries "coverage", so it becomes the FIRST per-stage bar of
    # every system (S1 = overall). Frozen values include it via overall.
    systems_data = {s: [fr["overall"][s]] + list(fr["stages"][s])
                    for s in systems}
    stage_systems = [s for s in systems if len(systems_data[s]) >= 3]
    max_stages = max(len(systems_data[s]) for s in stage_systems)
    x = np.arange(max_stages)
    width = 0.8 / max(len(stage_systems), 1)
    for i, sname in enumerate(stage_systems):
        v = list(systems_data[sname])
        padded = v + [0] * (max_stages - len(v))
        offset = (i - (len(stage_systems) - 1) / 2) * width
        bars = ax.bar(x + offset, padded, width,
                      label=sys_labels[fr["order"].index(sname)],
                      color=SYS_COLORS[sname], alpha=0.85)
        for bar, val in zip(bars, padded):
            if val > 0.05:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.005, f"{val:.0%}", ha="center",
                        va="bottom", fontsize=5.5, rotation=45)
    ax.set_xticks(x)
    ax.set_xticklabels([f"S{i + 1}" for i in range(max_stages)], fontsize=7,
                       rotation=20)
    ax.legend(fontsize=8)
    ax.set_title(t["cov_stage"] if t else "Per-Stage Coverage (Detailed)",
                 fontsize=10)
    ax.set_ylabel(t["cov_cov"] if t else "Coverage", fontsize=10)
    ax.set_ylim(0, 1.0)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))
    plt.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
        plt.close(fig)
        return None
    return fig


# ── fig6_cds_comparison (data: 8ad379a physics_comparison.json) ─────────
def check_c6():
    fr = FROZEN["c6"]
    assert abs(fr["math"][1] - 0.2705) < 1e-9  # fig3 forensic anchor
    assert abs(fr["math"][0] - 0.2162) < 1e-9
    assert abs(fr["math"][2] - 0.0731) < 1e-9
    assert abs(fr["phys"][3] - 0.0654) < 1e-9  # F6: physics peaks college
    assert abs(fr["phys"][1] - 0.0468) < 1e-9
    assert max(range(4), key=lambda i: fr["math"][i]) == 1
    assert max(range(4), key=lambda i: fr["phys"][i]) == 3


def render_c6(lang, path=None):
    fr = FROZEN["c6"]
    t = T[lang] if lang in T else None
    levels = fr["levels"]
    labels = (t["c6_levels"] if t else
              ["Elementary", "Middle", "High", "College"])
    mv, pv = fr["math"], fr["phys"]
    legend = t["c6_legend"] if t else ["Math", "Physics"]
    x = np.arange(len(levels))
    width = 0.35
    fig, (ax_bar, ax_info) = plt.subplots(1, 2, figsize=(10, 4.5),
                                          gridspec_kw={"width_ratios": [1.5, 1]})
    b1 = ax_bar.bar(x - width / 2, mv, width, label=legend[0], color="#60a5fa",
                    edgecolor="white", linewidth=0.5)
    b2 = ax_bar.bar(x + width / 2, pv, width, label=legend[1], color="#f97316",
                    edgecolor="white", linewidth=0.5)
    ax_bar.set_ylabel(t["c6_ylabel"] if t else "CDS (Concept Density Score)")
    ax_bar.set_title(t["c6_title"] if t else
                     "CDS by Education Level: Math vs Physics",
                     fontweight="bold")
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(labels)
    ax_bar.legend()
    ax_bar.spines["top"].set_visible(False)
    ax_bar.spines["right"].set_visible(False)
    for bar, v in zip(b1, mv):
        if v > 0:
            ax_bar.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.003, f"{v:.3f}", ha="center",
                        va="bottom", fontsize=8)
    for bar, v in zip(b2, pv):
        if v > 0:
            ax_bar.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.003, f"{v:.3f}", ha="center",
                        va="bottom", fontsize=8)
    math_peak = levels[max(range(4), key=lambda i: mv[i])]
    phys_peak = levels[max(range(4), key=lambda i: pv[i])]
    if t:
        finding = t["c6_find"]
    else:
        finding = (
            "Cross-Disciplinary Finding:\n\n"
            f"Math CDS peak:    {math_peak}\n"
            f"  (CDS = {mv[levels.index(math_peak)]:.3f})\n\n"
            f"Physics CDS peak: {phys_peak}\n"
            f"  (CDS = {pv[levels.index(phys_peak)]:.3f})\n\n"
            "Different disciplines show\n"
            "different density patterns:\n"
            "  Math densest at foundation,\n"
            "  Physics densest at advanced\n"
            "  specialization."
        )
    ax_info.axis("off")
    ax_info.text(0.05, 0.5, finding, fontsize=10, va="center",
                 bbox=dict(boxstyle="round,pad=0.6", facecolor="#fff7ed",
                           edgecolor="#fed7aa"))
    plt.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
        plt.close(fig)
        return None
    return fig


# ── fig_wikipedia_lds ─────────────────────────────────────────────────
def check_wiki():
    fr = FROZEN["wiki"]
    assert fr["pooled"] == {"ZH-EN": 1.0, "DE-EN": 1.0, "ZH-DE": 1.0}
    assert fr["textbook"] == {"ZH-EN": 0.9336, "DE-EN": 0.9382,
                              "ZH-DE": 0.5188}
    assert len(fr["topics"]) == 5


def render_wiki(lang, path=None):
    fr = FROZEN["wiki"]
    t = T[lang] if lang in T else None
    pairs = PAIRS
    topics = fr["topics"]
    tlabels = ([x.capitalize() for x in topics] if not t else t["wiki_topics"])
    pooled = fr["pooled"]
    textv = fr["textbook"]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    ax = axes[0]
    x = np.arange(len(topics))
    width = 0.22
    colors = {"ZH-EN": "#2563eb", "DE-EN": "#ea580c", "ZH-DE": "#16a34a"}
    for i, p in enumerate(pairs):
        vals = [1.0 for _ in topics]
        offset = (i - 1) * width
        bars = ax.bar(x + offset, vals, width, label=p, color=colors[p],
                      alpha=0.85)
        for bar, val in zip(bars, vals):
            if val > 0.01:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.01, f"{val:.3f}", ha="center",
                        va="bottom", fontsize=6, rotation=45)
    ax.set_xlabel(t["wiki_x"] if t else "Social Topic", fontsize=11)
    ax.set_ylabel(t["wiki_y"] if t else "LDS (Wikipedia)", fontsize=11)
    ax.set_title(t["wiki_left"] if t else "Per-Topic Wikipedia Concept LDS",
                 fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(tlabels, fontsize=8)
    ax.legend(fontsize=8)
    ax.set_ylim(0, 1.15)
    ax = axes[1]
    x2 = np.arange(len(pairs))
    w2 = 0.3
    tv = [textv[p] for p in pairs]
    wv = [pooled[p] for p in pairs]
    ax.bar(x2 - w2 / 2, tv, w2, label=t["wiki_text"] if t else
           "Textbook (LDS-K)", color="#6b7280", alpha=0.7)
    ax.bar(x2 + w2 / 2, wv, w2, label=t["wiki_soc"] if t else
           "Wikipedia (Social)", color="#f59e0b", alpha=0.7)
    for i, (a, b) in enumerate(zip(tv, wv)):
        ax.text(i - w2 / 2, a + 0.02, f"{a:.3f}", ha="center", va="bottom",
                fontsize=7)
        ax.text(i + w2 / 2, b + 0.02, f"{b:.3f}", ha="center", va="bottom",
                fontsize=7)
    ax.set_xlabel(t["wiki_pair"] if t else "Language Pair", fontsize=11)
    ax.set_ylabel("LDS", fontsize=11)
    ax.set_title(t["wiki_right"] if t else
                 "Wikipedia Social vs Textbook Knowledge", fontsize=10)
    ax.set_xticks(x2)
    ax.set_xticklabels(pairs, fontsize=9)
    ax.legend(fontsize=8)
    ax.set_ylim(0, 1.15)
    plt.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
        plt.close(fig)
        return None
    return fig


# ── figure1_lds_distribution (pilot June-18; dpi150/bbox-tight EN) ─────
def check_g1():
    fr = FROZEN["g1"]
    assert len(fr["rows"]) == 17
    means = {}
    for p in fr["pairs"]:
        for tp in fr["topics"]:
            vals = [v for (tt, pp, v) in fr["rows"] if tt == tp and pp == p]
            means[(tp, p)] = (sum(vals) / len(vals), len(vals)) if vals else (0, 0)
    assert abs(means[("freedom", "zh-de")][0] - 0.8380) < 1e-4
    assert abs(means[("freedom", "zh-en")][0] - 0.71725) < 1e-4
    assert abs(means[("justice", "zh-de")][0] - 0.8913) < 1e-9
    assert abs(means[("success", "zh-de")][0] - 1.0) < 1e-9
    assert means[("freedom", "en-de")] == (0, 0)
    # overall group: zh pairs absent, en-de pooled 1.0 (S002+S008 rows)
    assert means[("overall", "en-de")] == (1.0, 2)
    assert means[("overall", "zh-de")] == (0, 0)


def g1_means():
    fr = FROZEN["g1"]
    out = {}
    for p in fr["pairs"]:
        col = []
        for tp in fr["topics"]:
            vals = [v for (tt, pp, v) in fr["rows"] if tt == tp and pp == p]
            col.append(sum(vals) / len(vals) if vals else 0)
        out[p] = col
    return out


def render_g1(lang, path=None, dpi=300):
    fr = FROZEN["g1"]
    t = T[lang] if lang in T else None
    topics = fr["topics"]
    tlabels = ([x.capitalize() for x in topics] if not t else t["g1_topics"])
    pairs = fr["pairs"]
    plabels = [p.upper() for p in pairs]
    means = g1_means()
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(topics))
    width = 0.25
    colors = ["#e74c3c", "#3498db", "#2ecc71"]
    for i, p in enumerate(pairs):
        ax.bar(x + i * width, means[p], width, label=plabels[i],
               color=colors[i], alpha=0.8)
    ax.set_xlabel(t["g1_x"] if t else "Topic", fontsize=12)
    ax.set_ylabel("LDS", fontsize=12)
    ax.set_title(t["g1_title"] if t else
                 "Language Drift Score by Topic and Language Pair",
                 fontsize=14)
    ax.set_xticks(x + width)
    ax.set_xticklabels(tlabels, fontsize=10)
    ax.legend(fontsize=10)
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    if path:
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)
        return None
    return fig


# ── figure3_topic_comparison ──────────────────────────────────────────
def check_g3():
    fr = FROZEN["g1"]
    g3 = FROZEN["g3"]
    for tp in fr["topics"]:
        vals = [v for (tt, pp, v) in fr["rows"] if tt == tp]
        m = sum(vals) / len(vals)
        s = float(np.std(vals))
        assert abs(m - g3[tp][0]) < 1e-6, (tp, m)
        assert abs(s - g3[tp][1]) < 1e-6, (tp, s)


def render_g3(lang, path=None, dpi=300):
    fr = FROZEN["g1"]
    t = T[lang] if lang in T else None
    topics = fr["topics"]
    tlabels = ([x.capitalize() for x in topics] if not t else t["g1_topics"])
    g3 = FROZEN["g3"]
    means = [g3[tp][0] for tp in topics]
    stds = [g3[tp][1] for tp in topics]
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#e74c3c" if m > 0.7 else "#f39c12" if m > 0.4 else "#2ecc71"
              for m in means]
    y_pos = np.arange(len(topics))
    ax.barh(y_pos, means, xerr=stds, color=colors, alpha=0.8, capsize=5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tlabels, fontsize=11)
    ax.set_xlabel(t["g3_x"] if t else "Mean LDS (± SD)", fontsize=12)
    ax.set_title(t["g3_title"] if t else "Concept Drift by Topic", fontsize=14)
    ax.set_xlim(0, 1.0)
    ax.axvline(x=0.7, color="red", linestyle="--", alpha=0.5,
               label=t["g3_hi"] if t else "High drift threshold")
    ax.axvline(x=0.4, color="orange", linestyle="--", alpha=0.5,
               label=t["g3_mid"] if t else "Moderate drift threshold")
    ax.legend(fontsize=9)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    if path:
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)
        return None
    return fig


# ── fig_a7_1..5 (data: fig_a7_*.csv + Aug-08 JSONs) ────────────────────
def setup_a7(lang):
    plt.rcdefaults()
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": FONT[lang],
        "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
        "legend.fontsize": 8, "figure.dpi": 300,
        "savefig.dpi": 300, "axes.unicode_minus": False,
    })


def setup_a7_en():
    plt.rcdefaults()
    plt.rcParams.update({
        "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
        "legend.fontsize": 8, "figure.dpi": 300, "savefig.dpi": 300,
    })


def check_a1():
    fr = FROZEN["a1"]
    rows = {r["pair"]: r for r in read_en_csv("fig_a7_1_delta_lds.csv")}
    assert abs(float(rows["ZH-EN"]["Human N=15 (between)"]) - 0.9634) < 1e-9
    assert abs(float(rows["ZH-DE"]["Math textbook (LDS-K)"]) - 0.5188) < 1e-9
    assert abs(float(rows["DE-EN"]["LLM within-subject"]) - 0.93) < 1e-9
    assert abs(fr["LLM"]["ZH-EN"] - 0.9552) < 1e-9


def render_a1(lang, path=None):
    fr = FROZEN["a1"]
    t = T[lang] if lang in T else None
    series_en = ["Human N=15 (between)", "LLM within-subject",
                 "Social Wikipedia", "Math textbook (LDS-K)"]
    series = t["a1_series"] if t else series_en
    vals = [fr["Human"], fr["LLM"], fr["Wiki"], fr["Math"]]
    colors = ["#d62728", "#1f77b4", "#2ca02c", "#7f7f7f"]
    hatches = ["//", "", "..", "xx"]
    x = np.arange(len(PAIRS))
    w = 0.19
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    for i, (label, d, c, h) in enumerate(zip(series, vals, colors, hatches)):
        ys = [d[p] for p in PAIRS]
        ax.bar(x + (i - 1.5) * w, ys, w, label=label, color=c, hatch=h,
               edgecolor="black", linewidth=0.5)
        for xi, yi in zip(x + (i - 1.5) * w, ys):
            ax.text(xi, yi + 0.01, f"{yi:.2f}", ha="center", va="bottom",
                    fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels(PAIRS)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel(t["a1_y"] if t else "LDS (higher = more divergent)")
    ax.set_title(t["a1_title"] if t else
                 "Three-way structural divergence: human / LLM / social / "
                 "textbook")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
        plt.close(fig)
        return None
    return fig


def check_a2():
    fr = FROZEN["a2"]
    rows = {r["topic"]: r for r in read_en_csv("fig_a7_2_thematic_heatmap.csv")}
    assert abs(float(rows["Freiheit"]["ZH-EN"]) - 0.9286) < 1e-9
    assert abs(float(rows["Erfolg"]["ZH-DE"]) - 0.9651) < 1e-9
    assert fr["topics"][0] == "Freiheit"


def render_a2(lang, path=None):
    fr = FROZEN["a2"]
    t = T[lang] if lang in T else None
    topics = (["Freiheit", "Gerechtigkeit", "Verantwortung", "Heimat",
               "Erfolg"] if not t else t["a2_topics"])
    mat = np.array([[fr[p][i] for p in PAIRS] for i in range(5)])
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    im = ax.imshow(mat, cmap="YlOrRd", aspect="auto", vmin=0.5, vmax=1.0)
    ax.set_xticks(range(3))
    ax.set_xticklabels(PAIRS)
    ax.set_yticks(range(len(topics)))
    ax.set_yticklabels(topics)
    for i in range(len(topics)):
        for j in range(3):
            v = mat[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8,
                    color="white" if v > 0.85 else "black")
    ax.set_title(t["a2_title"] if t else "LLM within-subject LDS-C by topic")
    ax.set_xlabel(t["a2_x"] if t else "Language pair")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label("LDS-C")
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
        plt.close(fig)
        return None
    return fig


def check_a3():
    fr = FROZEN["a3"]
    rows = {r["pair"]: r for r in read_en_csv("fig_a7_3_null_models.csv")}
    assert abs(float(rows["ZH-DE"]["Structure Null"]) - 0.7154) < 1e-9
    assert abs(float(rows["ZH-EN"]["Within-lang floor"]) - 0.9582) < 1e-9
    assert abs(fr["full"]["ZH-DE"] - 0.5188) < 1e-9


def render_a3(lang, path=None):
    fr = FROZEN["a3"]
    t = T[lang] if lang in T else None
    labels = (["LDS-K (observed)", "Structure Null", "Within-lang floor"]
              if not t else t["a3_labels"])
    keys = ["full", "structure", "floor"]
    colors = ["#1f77b4", "#ff7f0e", "#d62728"]
    x = np.arange(len(PAIRS))
    w = 0.22
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    for i, (lab, key) in enumerate(zip(labels, keys)):
        ys = [fr[key][p] for p in PAIRS]
        ax.bar(x + (i - 1) * w, ys, w, label=lab, color=colors[i],
               edgecolor="black", linewidth=0.5)
        for xi, yi in zip(x + (i - 1) * w, ys):
            ax.text(xi, yi + 0.005, f"{yi:.2f}", ha="center", va="bottom",
                    fontsize=7)
    ax.axhline(1.0, color="black", lw=0.8, ls=":")
    ax.text(2.5, 1.01, t["a3_rand"] if t else "complete random = 1.0",
            fontsize=7, ha="right")
    ax.set_xticks(x)
    ax.set_xticklabels(PAIRS)
    ax.set_ylim(0.3, 1.1)
    ax.set_ylabel("LDS")
    ax.set_title(t["a3_title"] if t else "LDS-K against null models")
    ax.legend(framealpha=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
        plt.close(fig)
        return None
    return fig


def check_a4():
    fr = FROZEN["a4"]
    rows = {r["effect"]: r for r in read_en_csv("fig_a7_4_mechanism.csv")}
    assert abs(float(rows["same_lang"]["coef"]) - fr["same_lang"][0]) < 1e-12
    assert abs(float(rows["same_frame"]["p"]) - fr["same_frame"][2]) < 1e-12
    assert abs(fr["obs"]["ZH-EN"] - 0.9552) < 1e-9


def render_a4(lang, path=None):
    fr = FROZEN["a4"]
    t = T[lang] if lang in T else None
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(7.4, 3.6))
    x = np.arange(len(PAIRS))
    obs = [fr["obs"][p] for p in PAIRS]
    floor = [fr["floor"][p] for p in PAIRS]
    perm = [fr["perm"][p] for p in PAIRS]
    leg = t["a4_leg"] if t else ["LDS-C observed", "Split-half floor",
                                 "Label perm"]
    axA.bar(x - 0.25, obs, 0.22, label=leg[0], color="#1f77b4",
            edgecolor="black", lw=0.5)
    axA.bar(x, floor, 0.22, label=leg[1], color="#d62728", edgecolor="black",
            lw=0.5)
    axA.bar(x + 0.25, perm, 0.22, label=leg[2], color="#7f7f7f",
            edgecolor="black", lw=0.5)
    for i, o in enumerate(obs):
        axA.text(i - 0.25, o + 0.01, f"{o:.2f}", ha="center", fontsize=7)
    axA.set_xticks(x)
    axA.set_xticklabels(PAIRS)
    axA.set_ylim(0.7, 1.05)
    axA.set_ylabel("LDS-C")
    axA.set_title(t["a4_a"] if t else "(A) Language signal > noise floor")
    axA.legend(fontsize=7, framealpha=0.9)
    axA.spines["top"].set_visible(False)
    axA.spines["right"].set_visible(False)
    names = ["same_lang", "same_frame"]
    xlabels = t["a4_x2"] if t else ["same\nlanguage", "same\nframe"]
    coefs = [fr[n][0] for n in names]
    ses = [fr[n][1] for n in names]
    ps = [fr[n][2] for n in names]
    xb = np.arange(2)
    axB.bar(xb, coefs, 0.4, color=["#1f77b4", "#d62728"], edgecolor="black",
            lw=0.5, yerr=ses, capsize=3)
    for xi, c, p in zip(xb, coefs, ps):
        axB.text(xi, c + 0.006, f"{c:+.3f}\np={p:.3f}", ha="center",
                 va="bottom", fontsize=7)
    axB.axhline(0, color="black", lw=0.8)
    axB.set_xticks(xb)
    axB.set_xticklabels(xlabels)
    axB.set_ylabel(t["a4_y2"] if t else
                   "Marginal effect on Jaccard similarity")
    axB.set_title(t["a4_b"] if t else "(B) LMM: code dominates, frame ~0")
    axB.spines["top"].set_visible(False)
    axB.spines["right"].set_visible(False)
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
        plt.close(fig)
        return None
    return fig


def check_a5():
    fr = FROZEN["a5"]
    rows = {r["pair"]: r for r in
            read_en_csv("fig_a7_5_ldsk_sensitivity.csv")}
    # CSV predates the M13 strict-gloss revision: frozen displayed values win
    assert abs(float(rows["ZH-EN"]["wiki_strict_gloss"]) - 0.6992) < 1e-9
    assert abs(float(rows["ZH-DE"]["wiki_strict_gloss"]) - 0.8511) < 1e-9
    assert abs(float(rows["ZH-EN"]["math_directed"]) - 0.9336) < 1e-9
    assert abs(fr["strict"]["ZH-EN"] - 0.6992) < 1e-9


def render_a5(lang, path=None):
    fr = FROZEN["a5"]
    t = T[lang] if lang in T else None
    x = np.arange(len(PAIRS))
    w = 0.17
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.4, 3.6))
    leg1 = (["directed", "undirected", "node-only"] if not t else t["a5_leg1"])
    series = [(leg1[0], fr["directed"], "#1f77b4"),
              (leg1[1], fr["undirected"], "#2ca02c"),
              (leg1[2], fr["node_only"], "#ff7f0e")]
    for i, (lab, d, c) in enumerate(series):
        ys = [d[p] for p in PAIRS]
        axL.bar(x + (i - 1) * w, ys, w, label=lab, color=c, edgecolor="black",
                lw=0.5)
    axL.axhline(0.97, color="red", lw=0.8, ls="--")
    axL.text(2.5, 0.975, t["a5_floor"] if t else "noise floor 0.97",
             fontsize=6.5, ha="right")
    axL.set_xticks(x)
    axL.set_xticklabels(PAIRS)
    axL.set_ylim(0.3, 1.05)
    axL.set_ylabel("LDS")
    axL.set_title(t["a5_a"] if t else
                  "(A) Math LDS-K: direction & edge sensitivity")
    axL.legend(fontsize=7)
    axL.spines["top"].set_visible(False)
    axL.spines["right"].set_visible(False)
    leg2 = (["loose (canonical)", "strict (gloss)"] if not t else t["a5_leg2"])
    series2 = [(leg2[0], fr["loose"], "#1f77b4"),
               (leg2[1], fr["strict"], "#d62728")]
    for i, (lab, d, c) in enumerate(series2):
        ys = [d[p] for p in PAIRS]
        axR.bar(x + (i - 0.5) * w, ys, w, label=lab, color=c, edgecolor="black",
                lw=0.5)
    axR.set_xticks(x)
    axR.set_xticklabels(PAIRS)
    axR.set_ylim(0.3, 1.05)
    axR.set_ylabel("LDS")
    axR.set_title(t["a5_b"] if t else
                  "(B) Social Wikipedia: alignment tightness")
    axR.legend(fontsize=7)
    axR.spines["top"].set_visible(False)
    axR.spines["right"].set_visible(False)
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=300)
        plt.close(fig)
        return None
    return fig


# ── chrome-overlay translation (fig5_hds + fig6_cds) ───────────────────
# Red line: data pixels stay identical; only number-free chrome
# (titles/axis labels/tick level names) is replaced via white-fill +
# redraw. Numeric annotations, value labels, finding boxes and legends
# stay in EN pixels. No CSV is written for overlay figures.
H5_STRIPS = {
    "title": (290, 1720, 15, 135),
    "xlabel": (290, 1720, 1022, 1085),
    "ylabel": (140, 290, 140, 1010),
}
C6_STRIPS = {
    "title": (100, 1720, 15, 125),
    "ylabel": (140, 290, 150, 1150),
    "xticks": (100, 1720, 1210, 1300),
}
H5_BLUE = np.array([96, 165, 250])
H5_GRAY = np.array([240, 240, 240])
C6_BLUE = np.array([96, 165, 250])
C6_ORANGE = np.array([249, 115, 22])
C6_BOX = np.array([255, 247, 237])


def _dilate(mask, r=3):
    out = mask.copy()
    h, w = mask.shape
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if not dy and not dx:
                continue
            y0, y1 = max(0, dy), min(h, h + dy)
            x0, x1 = max(0, dx), min(w, w + dx)
            sy0, sy1 = max(0, -dy), min(h, h - dy)
            sx0, sx1 = max(0, -dx), min(w, w - dx)
            out[y0:y1, x0:x1] |= mask[sy0:sy1, sx0:sx1]
    return out


def _has_box(region):
    """True gray fill box present? Text antialias ramps also pass near-white
    shades, so glyph-adjacent pixels (3px dilation) are excluded first."""
    gray = (np.abs(region - H5_GRAY).max(axis=2) <= 8) | \
           (np.abs(region - C6_BOX).max(axis=2) <= 8)
    dark = region.max(axis=2) < 100
    clean = gray & ~_dilate(dark, 3)
    return clean.sum() > 300


def _fit_font(path, text, max_w, max_h, index=0):
    size = 64
    while size > 8:
        try:
            f = ImageFont.truetype(path, size, index=index)
        except OSError:
            return ImageFont.load_default()
        b = f.getbbox(text)
        if b[2] - b[0] <= max_w and b[3] - b[1] <= max_h:
            return f
        size -= 2
    return ImageFont.truetype(path, 8, index=index)


def overlay_h5(lang):
    t = T[lang]
    jobs = [
        ("title", t["h5_title"], True, False),
        ("xlabel", t["h5_xlabel"], False, False),
        ("ylabel", t["h5_ylabel"], False, True),
    ]
    return _overlay("fig5_hds_distribution", jobs, lang,
                    avoid=[H5_BLUE], avoid_box=[H5_GRAY])


def overlay_c6(lang):
    # xtick level names: split the strip into one rect per label, left->right
    t = T[lang]
    jobs = [
        ("title", t["c6_title"], True, False),
        ("ylabel", t["c6_ylabel"], False, True),
    ]
    ok = _overlay("fig6_cds_comparison", jobs, lang,
                  avoid=[C6_BLUE, C6_ORANGE], avoid_box=[C6_BOX],
                  extra_texts=t["c6_levels"], extra_strip=C6_STRIPS["xticks"])
    return ok


def _overlay(stem, jobs, lang, avoid, avoid_box, extra_texts=None,
             extra_strip=None):
    strips = H5_STRIPS if stem.startswith("fig5") else C6_STRIPS
    src = OUTPUT_DIR / f"{stem}.png"
    if not src.exists():
        return fail(f"EN reference missing: {stem}.png")
    im = Image.open(src).convert("RGB")
    arr = np.array(im)
    draw_zones = []  # (key, text, bold, is_ylabel, zx0,zx1,zy0,zy1)
    for key, text, bold, is_ylabel in jobs:
        x0, x1, y0, y1 = strips[key]
        strip = arr[y0:y1, x0:x1]
        dark = strip.max(axis=2) < 100
        if is_ylabel:
            # drop the vertical axis spine (full-bleed cols), then keep the
            # leftmost text cluster (rotated label), never tick numerals
            full = np.where(dark.sum(axis=0) > (y1 - y0) * 0.7)[0]
            if len(full):
                dark = dark.copy()
                dark[:, max(0, full.min() - 8):] = False
            colsum = dark.sum(axis=0)
            cols = np.where(colsum > 2)[0]
            if len(cols) == 0:
                return fail(f"{stem} ylabel text not found")
            gaps = np.where(np.diff(cols) > 6)[0]
            cut = cols[gaps[0]] if len(gaps) else cols[-1]
            dark = dark.copy()
            dark[:, cut - x0 + 1:] = False
            # zone: full strip height, left of the tick numerals
            zx0, zx1, zy0, zy1 = x0, x0 + cut + 6, y0, y1
        else:
            # drop horizontal spines (full-bleed rows): text lives below them
            full = np.where(dark.sum(axis=1) > (x1 - x0) * 0.7)[0]
            if len(full):
                dark = dark.copy()
                dark[:full.max() + 8, :] = False
            # zone: the whole strip (asserted below to hold only this text)
            zx0, zx1, zy0, zy1 = x0, x1, y0, y1
        rows = np.where(dark.sum(axis=1) > 1)[0]
        cols = np.where(dark.sum(axis=0) > 1)[0]
        if len(rows) == 0 or len(cols) == 0:
            return fail(f"{stem} {key} text not found")
        zone = arr[zy0:zy1, zx0:zx1].astype(int)
        for bg in avoid:
            if (np.abs(zone - bg).max(axis=2) <= 60).sum() > 50:
                return fail(f"{stem} {key} zone overlaps data bars")
        if _has_box(zone):
            return fail(f"{stem} {key} zone overlaps annotation box")
        inner = dark[zy0 - y0:zy1 - y0, zx0 - x0:zx1 - x0]
        textpix = dark[rows.min():rows.max() + 1,
                       cols.min():cols.max() + 1].sum()
        if inner.sum() - textpix > 300:
            return fail(f"{stem} {key} zone holds foreign marks")
        tw0 = cols.max() - cols.min() + 1
        th0 = rows.max() - rows.min() + 1
        draw_zones.append((key, text, bold, is_ylabel, zx0, zx1, zy0, zy1,
                           tw0, th0))
    if extra_texts and extra_strip:
        x0, x1, y0, y1 = extra_strip
        strip = arr[y0:y1, x0:x1]
        dark = strip.max(axis=2) < 100
        full = np.where(dark.sum(axis=1) > (x1 - x0) * 0.7)[0]
        if len(full) == 0:
            return fail(f"{stem} xtick spine not found")
        dark = dark.copy()
        dark[:full.max() + 8, :] = False
        colsum = dark.sum(axis=0)
        cols = np.where(colsum > 1)[0]
        if len(cols) == 0:
            return fail(f"{stem} xtick texts not found")
        gaps = np.where(np.diff(cols) > 25)[0]
        bounds = []
        prev = cols[0]
        for g in gaps:
            bounds.append((prev, cols[g]))
            prev = cols[g + 1]
        bounds.append((prev, cols[-1]))
        # drop stray marks (axis corners): labels are tall
        kept = []
        for a, b in bounds:
            sub = dark[:, a:b + 1]
            rows = np.where(sub.sum(axis=1) > 1)[0]
            if len(rows) and rows.max() - rows.min() + 1 > 20:
                kept.append((a, b))
        bounds = kept
        if len(bounds) != len(extra_texts):
            return fail(f"{stem} xtick groups {len(bounds)} != "
                        f"{len(extra_texts)}")
        for (a, b), text in zip(bounds, extra_texts):
            sub = dark[:, a:b + 1]
            rows = np.where(sub.sum(axis=1) > 1)[0]
            rx0, rx1 = x0 + a - 4, x0 + b + 4
            ry0, ry1 = y0 + rows.min() - 4, y0 + rows.max() + 4
            region = arr[ry0:ry1, rx0:rx1].astype(int)
            for bg in avoid:
                if (np.abs(region - bg).max(axis=2) <= 60).sum() > 50:
                    return fail(f"{stem} xtick rect overlaps data")
            if _has_box(region):
                return fail(f"{stem} xtick rect overlaps annotation box")
            tw0 = b - a + 1
            th0 = rows.max() - rows.min() + 1
            draw_zones.append(("xtick", text, False, False,
                               rx0, rx1, ry0, ry1, tw0, th0))
    before = arr.copy()
    canvas = im.copy()
    dr = ImageDraw.Draw(canvas)
    for _, _, _, _, rx0, rx1, ry0, ry1, _, _ in draw_zones:
        dr.rectangle([rx0, ry0, rx1, ry1], fill="white")
    check = np.array(canvas)
    for _, _, _, _, rx0, rx1, ry0, ry1, _, _ in draw_zones:
        if (check[ry0:ry1, rx0:rx1].max(axis=2) < 250).any():
            return fail(f"{stem} fill rect not pure white")
    font_path = DEJA if lang == "de" else YAHEI
    for key, text, bold, is_ylabel, rx0, rx1, ry0, ry1, tw0, th0 in draw_zones:
        fp = (DEJA_B if bold and lang == "de" else font_path)
        if is_ylabel:
            # unrotated frame: detected rotated extent (tw0,th0) swaps
            f = _fit_font(fp, text, min(ry1 - ry0, th0 * 1.15),
                          min(rx1 - rx0, tw0 * 1.15))
            b = f.getbbox(text)
            if (b[2] - b[0]) > ry1 - ry0 or (b[3] - b[1]) > rx1 - rx0:
                f = _fit_font(fp, text, ry1 - ry0, rx1 - rx0)
                b = f.getbbox(text)
            tmp = Image.new("RGB", (ry1 - ry0, rx1 - rx0), "white")
            dt = ImageDraw.Draw(tmp)
            dt.text((((ry1 - ry0) - (b[2] - b[0])) / 2 - b[0],
                     ((rx1 - rx0) - (b[3] - b[1])) / 2 - b[1]),
                    text, font=f, fill="black")
            tmp = tmp.transpose(Image.Transpose.ROTATE_90)
            tw, th = tmp.size
            # by construction tmp is exactly zone-sized; paste at origin
            if (tw, th) != (rx1 - rx0, ry1 - ry0):
                return fail(f"{stem} ylabel canvas size mismatch")
            canvas.paste(tmp, (rx0, ry0))
        else:
            f = _fit_font(fp, text, min(rx1 - rx0, tw0 * 1.15),
                          min(ry1 - ry0, th0 * 1.15))
            b = f.getbbox(text)
            if (b[2] - b[0]) > rx1 - rx0 or (b[3] - b[1]) > ry1 - ry0:
                f = _fit_font(fp, text, rx1 - rx0, ry1 - ry0)
                b = f.getbbox(text)
            dr.text((rx0 + (rx1 - rx0 - (b[2] - b[0])) / 2 - b[0],
                     ry0 + (ry1 - ry0 - (b[3] - b[1])) / 2 - b[1]),
                    text, font=f, fill="black")
    after = np.array(canvas)
    mask = np.ones(after.shape[:2], dtype=bool)
    for _, _, _, _, rx0, rx1, ry0, ry1, _, _ in draw_zones:
        # PIL rectangle is end-inclusive; mask must cover the painted px
        mask[ry0:ry1 + 1, rx0:rx1 + 1] = False
    if not (before[mask] == after[mask]).all():
        return fail(f"{stem} data region changed")
    out = OUTPUT_DIR / f"{stem}_{lang}.png"
    canvas.save(out, dpi=(300, 300))
    dst = WEBFIG_DIR / out.name
    if not dst.exists():
        shutil.copy2(out, dst)
        mir = "mirrored"
    else:
        mir = "mirror-exists"
    print(f"  [OK] {out.name} ({out.stat().st_size // 1024} KB, {mir}, "
          f"overlay chrome only)")
    return True


# ── missing data CSVs (new files only) ────────────────────────────────
def write_missing_csvs():
    def _w(name, header, rows):
        p = OUTPUT_DIR / name
        if p.exists():
            print(f"  [CSV] {name} exists, kept")
            return
        with p.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)
        print(f"  [OK] {name} written")
    fr = FROZEN["wiki"]
    _w("fig_wikipedia_lds_data.csv", ["topic", "language_pair", "lds"],
       [[tp, p, fr["per"][PAIRS.index(p)]] for tp in fr["topics"]
        for p in PAIRS]
       + [["pooled", p, fr["pooled"][p]] for p in PAIRS]
       + [["textbook", p, fr["textbook"][p]] for p in PAIRS])
    h4 = FROZEN["h4"]
    _w("fig4_lds_heatmap_data.csv", ["topic", "ZH-DE", "ZH-EN", "DE-EN"],
       [[tp, h4["zh-de"][i], h4["zh-en"][i], h4["de-en"][i]]
        for i, tp in enumerate(h4["topics"])]
       + [["AVERAGE", h4["avg"]["zh-de"], h4["avg"]["zh-en"],
           h4["avg"]["de-en"]]])
    # NOTE: no fig6_cds_comparison_data.csv and no fig5_hds CSV are
    # written (see module docstring red lines): overlay figures keep EN
    # pixels, and snapshotting unrecoverable numbers would falsify data.
    g1 = FROZEN["g1"]
    means = g1_means()
    _w("figure1_lds_distribution_data.csv", ["topic", "ZH-DE", "ZH-EN",
                                             "EN-DE"],
       [[tp, round(means["zh-de"][i], 4), round(means["zh-en"][i], 4),
         round(means["en-de"][i], 4)] for i, tp in enumerate(g1["topics"])])
    g3 = FROZEN["g3"]
    _w("figure3_topic_comparison_data.csv", ["topic", "mean_lds", "std_lds",
                                             "n"],
       [[tp, g3[tp][0], g3[tp][1],
         len([1 for (tt, pp, v) in g1["rows"] if tt == tp])]
        for tp in g1["topics"]])


# ── registry ──────────────────────────────────────────────────────────
FIGS = {
    "fig1_lds_k_heatmap": ("fig1", check_fig1, render_fig1, "std"),
    "fig4_lds_heatmap": ("h4", check_h4, render_h4, "legacy"),
    "fig4_ablation": ("ab", check_ab, render_ab, "std"),
    "fig5_falsification": ("f5", check_f5, None, "f5"),
    "fig5_hds_distribution": ("h5", None, None, "overlay"),
    "fig6_coverage": ("cov", check_cov, render_cov, "std"),
    "fig6_cds_comparison": ("c6", check_c6, render_c6, "overlay-c6"),
    "fig_wikipedia_lds": ("wiki", check_wiki, render_wiki, "std"),
    "figure1_lds_distribution": ("g1", check_g1, render_g1, "pilot"),
    "figure3_topic_comparison": ("g3", check_g3, render_g3, "pilot"),
    "fig_a7_1": ("a1", check_a1, render_a1, "a7"),
    "fig_a7_2": ("a2", check_a2, render_a2, "a7"),
    "fig_a7_3": ("a3", check_a3, render_a3, "a7"),
    "fig_a7_4": ("a4", check_a4, render_a4, "a7"),
    "fig_a7_5": ("a5", check_a5, render_a5, "a7"),
}
STEMS = {
    "fig1_lds_k_heatmap": "fig1_lds_k_heatmap",
    "fig4_lds_heatmap": "fig4_lds_heatmap",
    "fig4_ablation": "fig4_ablation",
    "fig5_falsification": "fig5_falsification",
    "fig5_hds_distribution": "fig5_hds_distribution",
    "fig6_coverage": "fig6_coverage",
    "fig6_cds_comparison": "fig6_cds_comparison",
    "fig_wikipedia_lds": "fig_wikipedia_lds",
    "figure1_lds_distribution": "figure1_lds_distribution",
    "figure3_topic_comparison": "figure3_topic_comparison",
    "fig_a7_1": "fig_a7_1_delta_lds",
    "fig_a7_2": "fig_a7_2_thematic_heatmap",
    "fig_a7_3": "fig_a7_3_null_models",
    "fig_a7_4": "fig_a7_4_mechanism",
    "fig_a7_5": "fig_a7_5_ldsk_sensitivity",
}


def run_fig(key, lang, check_only=False, f5stats=None):
    stem = STEMS[key]
    _, check, render, kind = FIGS[key]
    print(f"[{key}] lang={lang}")
    try:
        if kind in ("overlay", "overlay-c6"):
            if check_only:
                print("  [OK] overlay fig: gates apply at render time")
                return True
            if kind == "overlay":
                return overlay_h5(lang)
            return overlay_c6(lang)
        if check:
            check()
        if kind == "f5":
            swapd, permd = f5stats
            swap = {p: (FROZEN["f5"]["swap"][p], swapd[p][1]) for p in PAIRS}
            perm = {p: (FROZEN["f5"]["perm"][p], permd[p][1]) for p in PAIRS}

            def ref(p, _r=render_f5):
                setup_en_plain()
                return _r("en", p, swap=swap, perm=perm)
        elif kind == "pilot":
            def ref(p, _r=render):
                plt.rcdefaults()
                return _r("en", p, dpi=150)
        elif kind == "a7":
            def ref(p, _r=render):
                setup_a7_en()
                return _r("en", p)
        elif kind == "legacy":
            def ref(p, _r=render):
                setup_en_legacy()
                return _r("en", p)
        else:
            def ref(p, _r=render):
                setup_en_plain()
                return _r("en", p)
        ok, msg = verify_en(stem, ref)
        print(f"  {msg}")
        if not ok:
            return fail(f"{stem}: {msg}")
        if check_only:
            return True
        if kind == "pilot":
            plt.rcdefaults()
            plt.rcParams.update({
                "font.family": "sans-serif",
                "font.sans-serif": FONT[lang],
                "axes.unicode_minus": False,
            })
            save_and_mirror(render_clean(render, lang, dpi=300), stem, lang,
                            bbox="tight")
        elif kind == "a7":
            setup_a7(lang)
            save_and_mirror(render_clean(render, lang), stem, lang)
        elif kind == "f5":
            setup(lang, tight=False)
            save_and_mirror(render_clean(render_f5, lang, swap=swap,
                                         perm=perm), stem, lang)
        elif kind == "legacy":
            setup(lang, tight=True)
            save_and_mirror(render_clean(render, lang), stem, lang)
        else:
            setup(lang, tight=False)
            save_and_mirror(render_clean(render, lang), stem, lang)
        return True
    except AssertionError as e:
        return fail(f"{stem}: frozen assert failed: {e}")
    except Exception as e:  # noqa: BLE001
        return fail(f"{stem}: {type(e).__name__}: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=["de", "zh", "all"], default="all")
    ap.add_argument("--fig", choices=["all"] + sorted(FIGS.keys()),
                    default="all")
    ap.add_argument("--check", action="store_true",
                    help="gates only, no output")
    ap.add_argument("--no-csv", action="store_true")
    args = ap.parse_args()
    langs = ["de", "zh"] if args.lang == "all" else [args.lang]
    keys = sorted(FIGS.keys()) if args.fig == "all" else [args.fig]
    print(f"Figure i18n wave2 renderer -- langs={langs} figs={len(keys)}")
    audit_T()
    f5stats = None
    if any(FIGS[k][3] == "f5" for k in keys):
        print("[fig5_falsification] seeded panel recompute (cosmetic stds)..")
        try:
            setup("de")
            f5stats = f5_panel_stats()
            print("  panel means asserted frozen; "
                  f"perm stds={[round(f5stats[1][p][1], 4) for p in PAIRS]}")
        except AssertionError as e:
            print(f"  [SKIP] fig5_falsification frozen assert failed: {e}")
            keys = [k for k in keys if FIGS[k][3] != "f5"]
        plt.close("all")
    ok_all = True
    for key in keys:
        for lang in langs:
            plt.close("all")
            if not run_fig(key, lang, args.check, f5stats):
                ok_all = False
    if not args.check and not args.no_csv:
        write_missing_csvs()
    print("WAVE2 " + ("ALL OK" if ok_all else "DONE WITH SKIPS (see above)"))
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
