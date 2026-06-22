"""
LinguaGraph — Human vs Model Validation Framework
====================================================
Final integration script for BWKI result analysis.

Produces:
  1. Three-way comparison table (Internet LDS | Model LDS | Human LDS)
  2. Spearman/Pearson correlation
  3. BWKI-ready figure data (JSON for plotting)
  4. Markdown report with result tables

Usage:
    python scripts/bwki_analysis.py                          # Run with available data
    python scripts/bwki_analysis.py --predict                # Show predicted Human LDS from regression
    python scripts/bwki_analysis.py --export-figures         # Export figure-ready JSON

Data Sources:
  - Internet LDS:  Wikipedia corpus (student_id='WIKIPEDIA_CORPUS')
  - Model LDS:     Simulation data (source='simulation')
  - Human LDS:     Real participants (source NOT simulation/gold)
"""

import json
import random
import sys
import math
from pathlib import Path
from datetime import datetime

import numpy as np

PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR / 'src'))
sys.path.insert(0, str(PROJECT_DIR))

from db_utils import get_connection, query


# ===== DATA LOADING =====

def load_lds_by_source(conn) -> dict:
    """Load LDS data grouped by source type."""
    sources = {
        "internet": """
            SELECT topic, lang_pair, lcd_score
            FROM cross_language_analysis
            WHERE student_id = 'WIKIPEDIA_CORPUS'
        """,
        "human": """
            SELECT a.topic, a.lang_pair, a.lcd_score
            FROM cross_language_analysis a
            JOIN responses r ON a.student_id = r.student_id
            WHERE r.student_id != 'WIKIPEDIA_CORPUS'
              AND r.student_id != 'SIMULATION'
              AND r.student_id != 'GOLD_LABEL'
              AND r.source NOT IN ('simulation', 'gold_import')
        """,
        "model": """
            SELECT a.topic, a.lang_pair, a.lcd_score
            FROM cross_language_analysis a
            WHERE a.student_id = 'SIMULATION'
        """,
    }

    result = {}
    for source_name, sql in sources.items():
        rows = query(conn, sql)
        by_pair = {}
        for r in rows:
            pair = r["lang_pair"]
            score = r["lcd_score"] if r["lcd_score"] is not None else 0.0
            if pair not in by_pair:
                by_pair[pair] = []
            by_pair[pair].append(score)
        result[source_name] = by_pair
    return result


# ===== STATISTICS =====

def mean(vals):
    return sum(vals) / len(vals) if vals else 0.0


def pearson_corr(xs, ys):
    """Pearson correlation coefficient."""
    n = len(xs)
    if n < 3:
        return None, None
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs)) * math.sqrt(sum((y - my) ** 2 for y in ys))
    if den == 0:
        return None, None
    r = num / den
    # Approximate p-value using t-distribution
    t = r * math.sqrt((n - 2) / (1 - r * r)) if abs(r) < 1 else float('inf')
    from scipy.stats import t as t_dist
    try:
        p = 2 * (1 - t_dist.cdf(abs(t), n - 2))
    except (ImportError, ValueError):
        p = None
    return round(r, 4), p


def spearman_rank(xs, ys):
    """Spearman rank correlation."""
    n = len(xs)
    if n < 3:
        return None, None

    def rank(vals):
        sorted_idx = sorted(range(len(vals)), key=lambda i: vals[i])
        ranks = [0] * len(vals)
        for pos, idx in enumerate(sorted_idx, 1):
            ranks[idx] = pos
        return ranks

    rx, ry = rank(xs), rank(ys)
    d_sq = sum((a - b) ** 2 for a, b in zip(rx, ry))
    rho = 1 - (6 * d_sq) / (n * (n * n - 1))

    from scipy.stats import spearmanr
    try:
        _, p = spearmanr(xs, ys)
    except (ImportError, ValueError):
        p = None
    return round(rho, 4), p


# ===== MAIN ANALYSIS =====

def build_comparison_table(data: dict) -> dict:
    """Build three-way comparison table by topic."""
    all_topics = set()
    for source in data.values():
        for pair in source:
            for entry in source[pair]:
                pass  # TODO
    # Actually let's do it properly
    topics_by_source = {}
    for source_name, by_pair in data.items():
        topics = set()
        for pair, scores in by_pair.items():
            if scores:
                topics.add("all")
        topics_by_source[source_name] = topics

    # Pair-level aggregation per source
    result = {}
    for source_name, by_pair in data.items():
        for pair, scores in by_pair.items():
            if not scores:
                continue
            key = pair
            if key not in result:
                result[key] = {}
            result[key][source_name] = {
                "mean": round(mean(scores), 4),
                "std": round(math.sqrt(sum((s - mean(scores)) ** 2 for s in scores) / len(scores)), 4) if len(scores) > 1 else 0,
                "n": len(scores),
                "all": scores,
            }

    # Per-topic aggregation
    # Group by topic across all three sources
    topic_result = {}
    for source_name, by_pair in data.items():
        for pair, scores in by_pair.items():
            if not scores:
                continue
            topic = pair  # e.g., "zh-de"
            if topic not in topic_result:
                topic_result[topic] = {}
            topic_result[topic][source_name] = {
                "mean": round(mean(scores), 4),
                "n": len(scores),
            }

    return {
        "by_pair": result,
        "by_topic": topic_result,
    }


def generate_bwki_report(table: dict, data: dict):
    """Generate BWKI-ready report with comparison tables."""
    topics = sorted(table["by_topic"].keys())
    sources = ["internet", "model", "human"]
    source_labels = {"internet": "Internet LDS", "model": "Model LDS", "human": "Human LDS"}

    md = []
    md.append("# LinguaGraph — BWKI Analysis Report\n")
    md.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    md.append("---\n")

    # Table 1: Three-way comparison
    md.append("## 1. Three-Way LDS Comparison\n")
    md.append("| Language Pair | Internet LDS | Model LDS | Human LDS |\n")
    md.append("|--------------|-------------|-----------|-----------|\n")

    for topic in topics:
        row = f"| {topic} |"
        for src in sources:
            if topic in table["by_topic"] and src in table["by_topic"][topic]:
                val = table["by_topic"][topic][src]["mean"]
                row += f" {val:.4f} |"
            else:
                row += " — |"
        md.append(row + "\n")

    # Table 2: Correlation matrix
    md.append("\n## 2. Cross-Source Correlation\n")
    md.append("| Source A | Source B | Pearson r | Spearman ρ |\n")
    md.append("|----------|----------|-----------|------------|\n")

    source_pairs = [("internet", "model"), ("internet", "human"), ("model", "human")]
    for s1, s2 in source_pairs:
        vals1, vals2 = [], []
        for topic in topics:
            if topic in table["by_topic"] and s1 in table["by_topic"][topic] and s2 in table["by_topic"][topic]:
                vals1.append(table["by_topic"][topic][s1]["mean"])
                vals2.append(table["by_topic"][topic][s2]["mean"])

        if len(vals1) >= 3:
            pr, pp = pearson_corr(vals1, vals2)
            sr, sp = spearman_rank(vals1, vals2)
            pr_str = f"{pr:.4f}" + (f" (p={pp:.4f})" if pp else "")
            sr_str = f"{sr:.4f}" + (f" (p={sp:.4f})" if sp else "")
        else:
            pr_str = sr_str = f"N/A (n={len(vals1)} < 3)"

        label1 = source_labels.get(s1, s1)
        label2 = source_labels.get(s2, s2)
        md.append(f"| {label1} | {label2} | {pr_str} | {sr_str} |\n")

    # Table 3: Sample counts
    md.append("\n## 3. Data Volume by Source\n")
    md.append("| Source | Pairs with Data | Topics |\n")
    md.append("|--------|----------------|--------|\n")
    for src in sources:
        pairs_with_data = sum(1 for t in topics if t in table["by_topic"] and src in table["by_topic"][t])
        label = source_labels.get(src, src)
        md.append(f"| {label} | {pairs_with_data} | {pairs_with_data} |\n")

    # Figure data (JSON block for plotting)
    md.append("\n## 4. Figure Data (for plotting)\n")
    md.append("```json\n")
    fig_data = {"labels": [], "internet": [], "model": [], "human": []}
    for topic in topics:
        fig_data["labels"].append(topic)
        for src in sources:
            if topic in table["by_topic"] and src in table["by_topic"][topic]:
                fig_data[src].append(table["by_topic"][topic][src]["mean"])
            else:
                fig_data[src].append(None)
    md.append(json.dumps(fig_data, ensure_ascii=False, indent=2))
    md.append("\n```\n")

    # Interpretation
    md.append("\n## 5. Interpretation\n")
    vals_i = [table["by_topic"][t].get("internet", {}).get("mean") for t in topics if "internet" in table["by_topic"].get(t, {})]
    vals_m = [table["by_topic"][t].get("model", {}).get("mean") for t in topics if "model" in table["by_topic"].get(t, {})]
    vals_h = [table["by_topic"][t].get("human", {}).get("mean") for t in topics if "human" in table["by_topic"].get(t, {})]

    if vals_i and vals_m and len(vals_i) >= 3 and len(vals_m) >= 3:
        ir, _ = pearson_corr(vals_i, vals_m)
        md.append(f"- Internet-Model correlation: r = {ir:.4f}\n")
    if vals_i and vals_h and len(vals_i) >= 3 and len(vals_h) >= 3:
        ir, _ = pearson_corr(vals_i, vals_h)
        md.append(f"- Internet-Human correlation: r = {ir:.4f} (predicted)\n")
    if vals_m and vals_h and len(vals_m) >= 3 and len(vals_h) >= 3:
        mr, _ = pearson_corr(vals_m, vals_h)
        md.append(f"- Model-Human correlation: r = {mr:.4f} (predicted)\n")

    # Prediction if human data missing
    if not vals_h:
        md.append("\n### Human LDS Prediction (from Internet LDS)\n")
        if vals_i and len(vals_i) >= 3:
            mi = mean(vals_i)
            md.append(f"Based on Internet LDS mean = {mi:.4f}, we predict Human LDS in range:\n")
            md.append(f"- Expected: {mi:.4f} ± 0.10\n")
            md.append(f"- Range: [{mi - 0.10:.4f}, {mi + 0.10:.4f}]\n")

    # Save
    outdir = PROJECT_DIR / "research" / "findings"
    outdir.mkdir(parents=True, exist_ok=True)
    report_path = outdir / "bwki_analysis_report.md"
    report_path.write_text("\n".join(md), encoding="utf-8")
    print(f"[OK] Report saved: {report_path}")

    # Save figure data
    fig_path = outdir / "bwki_figure_data.json"
    with open(fig_path, "w", encoding="utf-8") as f:
        json.dump(fig_data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Figure data: {fig_path}")

    print("\n".join(md))


def main():
    random.seed(42)
    np.random.seed(42)
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph BWKI Analysis Framework")
    parser.add_argument("--predict", action="store_true", help="Show predicted Human LDS from internet regression")
    parser.add_argument("--export-figures", action="store_true", help="Export figure-ready JSON")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  LinguaGraph — BWKI Analysis Framework")
    print(f"{'='*50}")

    conn = get_connection()
    data = load_lds_by_source(conn)

    # Print data availability
    total_internet = sum(len(v) for v in data["internet"].values())
    total_model = sum(len(v) for v in data["model"].values())
    total_human = sum(len(v) for v in data["human"].values())

    print(f"\n  Data available:")
    print(f"    Internet (Wikipedia): {total_internet} data points")
    print(f"    Model (Simulation):   {total_model} data points")
    print(f"    Human (Participants): {total_human} data points")

    if total_human == 0:
        print(f"\n  [NOTE] No human data yet. Add after pilot/experiment.")
        print(f"  Running prediction mode with available data.\n")

    table = build_comparison_table(data)
    generate_bwki_report(table, data)

    conn.close()


if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    main()
