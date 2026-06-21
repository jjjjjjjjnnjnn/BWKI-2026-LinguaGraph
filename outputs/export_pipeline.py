"""
Results Export Pipeline
========================
Generate publication-ready tables and figures from LinguaGraph LDS results.

Usage:
    python results/export_pipeline.py                    # Export all
    python results/export_pipeline.py --table demographics   # Table 1 only
    python results/export_pipeline.py --figure lds_distribution  # Figure 1 only
    python results/export_pipeline.py --format csv   # CSV instead of LaTeX
"""

import csv
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from db_utils import get_connection, query, query_value


OUTPUT_DIR = Path(__file__).parent
FIGURES_DIR = OUTPUT_DIR / "figures"
TABLES_DIR = OUTPUT_DIR / "tables"


def ensure_dirs():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)


# ===== Table 1: Participant Demographics =====

def export_demographics(format: str = "markdown") -> str:
    """Generate Table 1: Participant Demographics."""
    conn = get_connection()

    students = query(conn, "SELECT * FROM students ORDER BY student_id")
    conn.close()

    by_lang = defaultdict(list)
    for s in students:
        by_lang[s["native_lang"]].append(s)

    lines = []
    lines.append("## Table 1: Participant Demographics\n")
    lines.append("| Characteristic | Chinese (n={}) | German (n={}) | English (n={}) | Total (n={}) |".format(
        len(by_lang.get("zh", [])),
        len(by_lang.get("de", [])),
        len(by_lang.get("en", [])),
        len(students),
    ))
    lines.append("|------|:---:|:---:|:---:|:---:|")

    # Age groups
    for lang in ["zh", "de", "en"]:
        group = by_lang.get(lang, [])
        ages = [s.get("age_group", "") for s in group if s.get("age_group")]
    lines.append("| Age Group | {} | {} | {} | {} |".format(
        ", ".join(sorted(set(s.get("age_group", "") for s in by_lang.get("zh", []) if s.get("age_group")))) or "—",
        ", ".join(sorted(set(s.get("age_group", "") for s in by_lang.get("de", []) if s.get("age_group")))) or "—",
        ", ".join(sorted(set(s.get("age_group", "") for s in by_lang.get("en", []) if s.get("age_group")))) or "—",
        ", ".join(sorted(set(s.get("age_group", "") for s in students if s.get("age_group")))) or "—",
    ))

    # Consent
    consented = sum(1 for s in students if s.get("consent") == 1)
    lines.append("| Consent granted | {}/{} | {}/{} | {}/{} | {}/{} |".format(
        sum(1 for s in by_lang.get("zh", []) if s.get("consent") == 1), len(by_lang.get("zh", [])),
        sum(1 for s in by_lang.get("de", []) if s.get("consent") == 1), len(by_lang.get("de", [])),
        sum(1 for s in by_lang.get("en", []) if s.get("consent") == 1), len(by_lang.get("en", [])),
        consented, len(students),
    ))

    # Years in Germany
    years_zh = [s.get("years_in_germany", 0) for s in by_lang.get("zh", []) if s.get("years_in_germany")]
    years_de = [s.get("years_in_germany", 0) for s in by_lang.get("de", []) if s.get("years_in_germany")]
    years_en = [s.get("years_in_germany", 0) for s in by_lang.get("en", []) if s.get("years_in_germany")]
    years_all = [s.get("years_in_germany", 0) for s in students if s.get("years_in_germany")]

    def mean_fmt(lst):
        if not lst:
            return "—"
        m = sum(lst) / len(lst)
        return f"{m:.1f}"

    lines.append("| Years in Germany (M) | {} | {} | {} | {} |".format(
        mean_fmt(years_zh), mean_fmt(years_de), mean_fmt(years_en), mean_fmt(years_all),
    ))

    report = "\n".join(lines)

    # Save
    output_path = TABLES_DIR / "table1_demographics.md"
    output_path.write_text(report, encoding="utf-8")
    print(f"  [OK] Table 1 saved: {output_path}")

    if format == "csv":
        _export_demographics_csv(by_lang, students)

    return report


def _export_demographics_csv(by_lang, students):
    """Export demographics as CSV."""
    csv_path = TABLES_DIR / "table1_demographics.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["student_id", "native_lang", "age_group", "consent", "years_in_germany"])
        for s in students:
            writer.writerow([
                s["student_id"],
                s["native_lang"],
                s.get("age_group", ""),
                s.get("consent", 0),
                s.get("years_in_germany", 0),
            ])
    print(f"  [OK] CSV saved: {csv_path}")


# ===== Table 2: LDS by Language Pair =====

def export_lds_table(format: str = "markdown") -> str:
    """Generate Table 2: LDS by language pair and topic."""
    conn = get_connection()

    analyses = query(conn, """
        SELECT topic, lang_pair, lcd_score, graph_similarity,
               shared_concepts, unique_l1_concepts, unique_l2_concepts
        FROM cross_language_analysis
        ORDER BY topic, lang_pair
    """)
    conn.close()

    # Group by topic and pair
    data = defaultdict(lambda: defaultdict(list))
    for a in analyses:
        data[a["topic"]][a["lang_pair"]].append(a["lcd_score"])

    lines = []
    lines.append("## Table 2: Language Drift Score (LDS) by Topic and Language Pair\n")
    lines.append("| Topic | ZH-DE | ZH-EN | DE-EN |")
    lines.append("|-------|:-----:|:-----:|:-----:|")

    topics = ["freedom", "justice", "responsibility", "success", "home", "overall"]
    pairs = ["zh-de", "zh-en", "en-de"]

    for topic in topics:
        if topic not in data and topic != "overall":
            continue
        row = [topic.capitalize()]
        for pair in pairs:
            scores = data.get(topic, {}).get(pair, [])
            if scores:
                mean = sum(scores) / len(scores)
                row.append(f"{mean:.4f}")
            else:
                row.append("—")
        lines.append("| " + " | ".join(row) + " |")

    # Overall
    all_scores = defaultdict(list)
    for topic in data:
        for pair in data[topic]:
            all_scores[pair].extend(data[topic][pair])

    row = ["**Overall**"]
    for pair in pairs:
        scores = all_scores.get(pair, [])
        if scores:
            mean = sum(scores) / len(scores)
            row.append(f"{mean:.4f}")
        else:
            row.append("—")
    lines.append("| " + " | ".join(row) + " |")

    lines.append("")
    lines.append("> LDS = 1 − mean(GED_sim, Jaccard_node, Jaccard_edge). Higher = more drift.")

    report = "\n".join(lines)

    output_path = TABLES_DIR / "table2_lds_by_topic.md"
    output_path.write_text(report, encoding="utf-8")
    print(f"  [OK] Table 2 saved: {output_path}")

    if format == "csv":
        _export_lds_csv(analyses)

    return report


def _export_lds_csv(analyses):
    """Export LDS results as CSV."""
    csv_path = TABLES_DIR / "table2_lds_by_topic.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["topic", "lang_pair", "lcd_score", "graph_similarity", "shared_concepts"])
        for a in analyses:
            writer.writerow([
                a["topic"], a["lang_pair"], a["lcd_score"],
                a["graph_similarity"], a["shared_concepts"],
            ])
    print(f"  [OK] CSV saved: {csv_path}")


# ===== Figure Generation (matplotlib) =====

def generate_figures():
    """Generate all publication-ready figures."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("  [WARN] matplotlib not installed. Skipping figure generation.")
        print("  Install with: pip install matplotlib")
        return

    conn = get_connection()
    analyses = query(conn, """
        SELECT topic, lang_pair, lcd_score
        FROM cross_language_analysis
        ORDER BY topic, lang_pair
    """)
    conn.close()

    if not analyses:
        print("  [WARN] No LDS data available. Skipping figure generation.")
        return

    _figure1_lds_distribution(analyses, plt, np)
    _figure3_topic_comparison(analyses, plt, np)

    plt.close("all")
    print(f"  [OK] Figures saved to {FIGURES_DIR}")


def _figure1_lds_distribution(analyses, plt, np):
    """Figure 1: LDS distribution by language pair."""
    data = defaultdict(lambda: defaultdict(list))
    for a in analyses:
        data[a["lang_pair"]][a["topic"]].append(a["lcd_score"])

    pairs = ["zh-de", "zh-en", "en-de"]
    topics = sorted(set(a["topic"] for a in analyses))

    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(topics))
    width = 0.25
    colors = ["#e74c3c", "#3498db", "#2ecc71"]

    for i, pair in enumerate(pairs):
        means = [np.mean(data[pair].get(t, [0])) for t in topics]
        ax.bar(x + i * width, means, width, label=pair.upper(), color=colors[i], alpha=0.8)

    ax.set_xlabel("Topic", fontsize=12)
    ax.set_ylabel("LDS", fontsize=12)
    ax.set_title("Language Drift Score by Topic and Language Pair", fontsize=14)
    ax.set_xticks(x + width)
    ax.set_xticklabels([t.capitalize() for t in topics], fontsize=10)
    ax.legend(fontsize=10)
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    output_path = FIGURES_DIR / "figure1_lds_distribution.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"  [OK] Figure 1 saved: {output_path}")


def _figure3_topic_comparison(analyses, plt, np):
    """Figure 3: Mean LDS per topic (horizontal bar chart)."""
    topic_scores = defaultdict(list)
    for a in analyses:
        topic_scores[a["topic"]].append(a["lcd_score"])

    topics = sorted(topic_scores.keys())
    means = [np.mean(topic_scores[t]) for t in topics]
    stds = [np.std(topic_scores[t]) for t in topics]

    fig, ax = plt.subplots(figsize=(8, 5))

    colors = ["#e74c3c" if m > 0.7 else "#f39c12" if m > 0.4 else "#2ecc71" for m in means]
    y_pos = np.arange(len(topics))

    ax.barh(y_pos, means, xerr=stds, color=colors, alpha=0.8, capsize=5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([t.capitalize() for t in topics], fontsize=11)
    ax.set_xlabel("Mean LDS (± SD)", fontsize=12)
    ax.set_title("Concept Drift by Topic", fontsize=14)
    ax.set_xlim(0, 1.0)
    ax.axvline(x=0.7, color="red", linestyle="--", alpha=0.5, label="High drift threshold")
    ax.axvline(x=0.4, color="orange", linestyle="--", alpha=0.5, label="Moderate drift threshold")
    ax.legend(fontsize=9)
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    output_path = FIGURES_DIR / "figure3_topic_comparison.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"  [OK] Figure 3 saved: {output_path}")


# ===== Summary Report =====

def export_summary() -> str:
    """Generate a combined summary report."""
    lines = []
    lines.append("# LinguaGraph Results Summary\n")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    conn = get_connection()
    summary_query = query_value(conn, "SELECT COUNT(*) FROM cross_language_analysis")
    student_count = query_value(conn, "SELECT COUNT(DISTINCT student_id) FROM responses")
    conn.close()

    lines.append(f"- Students: {student_count}")
    lines.append(f"- LDS analyses: {summary_query}")
    lines.append(f"- Tables: {TABLES_DIR}")
    lines.append(f"- Figures: {FIGURES_DIR}")

    report = "\n".join(lines)
    output_path = OUTPUT_DIR / "RESULTS_SUMMARY.md"
    output_path.write_text(report, encoding="utf-8")
    print(f"  [OK] Summary saved: {output_path}")
    return report


# ===== CLI =====

def main():
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph Results Export Pipeline")
    parser.add_argument("--table", choices=["demographics", "lds", "all"], default="all",
                        help="Which table(s) to export")
    parser.add_argument("--figure", action="store_true", help="Generate figures")
    parser.add_argument("--all", action="store_true", help="Export everything (tables + figures)")
    parser.add_argument("--format", choices=["markdown", "csv"], default="markdown",
                        help="Output format")
    args = parser.parse_args()

    ensure_dirs()

    print(f"\n{'='*60}")
    print(f"  LinguaGraph Results Export Pipeline")
    print(f"{'='*60}\n")

    if args.all or args.table == "all":
        export_demographics(format=args.format)
        export_lds_table(format=args.format)
    elif args.table == "demographics":
        export_demographics(format=args.format)
    elif args.table == "lds":
        export_lds_table(format=args.format)

    if args.all or args.figure:
        generate_figures()

    export_summary()

    print(f"\n{'='*60}")
    print(f"  Export complete!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
