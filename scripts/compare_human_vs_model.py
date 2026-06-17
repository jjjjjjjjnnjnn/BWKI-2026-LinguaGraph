"""
LinguaGraph Human vs Model Comparison
========================================
Compares LDS from human data vs simulation data.
Critical for the Computational Control Model analysis.

Usage:
    python scripts/compare_human_vs_model.py
    python scripts/compare_human_vs_model.py --report
    python scripts/compare_human_vs_model.py --export-json

Output:
    research/findings/human_vs_model_comparison.md
    research/findings/human_vs_model_comparison.json
"""

import json
import sys
import math
from pathlib import Path
from datetime import datetime
from collections import defaultdict

PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / 'src'))


def load_lcd_data(conn):
    """Load LDS data from DB, split by source."""
    from db_utils import query

    # Human data: from surveys
    human = query(conn, """
        SELECT topic, lang_pair, lcd_score
        FROM cross_language_analysis a
        JOIN responses r ON a.student_id = r.student_id
        WHERE r.source NOT IN ('simulation', 'gold_import')
        AND r.student_id != 'GOLD_LABEL'
        AND r.student_id != 'WIKIPEDIA_CORPUS'
        GROUP BY a.topic, a.lang_pair
    """)

    # Simulation data
    simulation = query(conn, """
        SELECT topic, lang_pair, lcd_score
        FROM cross_language_analysis a
        WHERE a.student_id = 'SIMULATION'
    """)

    # Wikipedia corpus data (pilot reference)
    wiki = query(conn, """
        SELECT topic, lang_pair, lcd_score
        FROM cross_language_analysis a
        WHERE a.student_id = 'WIKIPEDIA_CORPUS'
    """)

    return human, simulation, wiki


def structure_by_topic(rows, topic_key='topic', pair_key='lang_pair', score_key='lcd_score'):
    """Transform DB rows to {topic: {pair: score}} dict."""
    data = defaultdict(dict)
    for r in rows:
        topic = r[topic_key]
        pair = r[pair_key]
        score = r[score_key] if r[score_key] else 0.0
        data[topic][pair] = round(score, 4)
    return dict(data)


def spearman_rank(xs, ys):
    """
    Compute Spearman rank correlation between two paired lists.
    If n < 3, returns None (too few points).
    """
    n = len(xs)
    if n < 3:
        return None

    # Rank xs
    x_sorted = sorted(range(n), key=lambda i: xs[i])
    x_ranks = [0] * n
    for rank, idx in enumerate(x_sorted, 1):
        x_ranks[idx] = rank

    # Rank ys
    y_sorted = sorted(range(n), key=lambda i: ys[i])
    y_ranks = [0] * n
    for rank, idx in enumerate(y_sorted, 1):
        y_ranks[idx] = rank

    # Spearman
    d_sq = sum((xr - yr) ** 2 for xr, yr in zip(x_ranks, y_ranks))
    rho = 1 - (6 * d_sq) / (n * (n * n - 1))
    return round(rho, 4)


def compare_datasets(human_data, sim_data, ref_data=None):
    """Compare human vs simulation LDS across topics and pairs."""
    topics = sorted(set(list(human_data.keys()) + list(sim_data.keys())))
    pairs = ["zh-de", "zh-en", "de-en"]

    # Per-topic comparison
    topic_comparison = []
    human_lcds, sim_lcds = [], []

    for topic in topics:
        h = human_data.get(topic, {})
        s = sim_data.get(topic, {})
        r = ref_data.get(topic, {}) if ref_data else {}

        topic_row = {"topic": topic}
        for pair in pairs:
            topic_row[f"human_{pair}"] = h.get(pair)
            topic_row[f"sim_{pair}"] = s.get(pair)
            topic_row[f"ref_{pair}"] = r.get(pair)
            if h.get(pair) is not None and s.get(pair) is not None:
                human_lcds.append(h[pair])
                sim_lcds.append(s[pair])

        topic_comparison.append(topic_row)

    # Spearman correlation (across all topic-pair points)
    spearman = spearman_rank(human_lcds, sim_lcds) if len(human_lcds) >= 3 else None

    # Per-pair correlation
    pair_rhos = {}
    for pair in pairs:
        h_vals = [human_data.get(t, {}).get(pair) for t in topics]
        s_vals = [sim_data.get(t, {}).get(pair) for t in topics]
        h_clean = [h for h in h_vals if h is not None]
        s_clean = [s for s, h in zip(s_vals, h_vals) if h is not None]
        if len(h_clean) >= 3:
            pair_rhos[pair] = spearman_rank(h_clean, s_clean)
        else:
            pair_rhos[pair] = None

    # Bias analysis: is simulation systematically higher or lower?
    bias = None
    if len(human_lcds) >= 3 and len(sim_lcds) >= 3:
        h_mean = sum(human_lcds) / len(human_lcds)
        s_mean = sum(sim_lcds) / len(sim_lcds)
        bias = {
            "human_mean": round(h_mean, 4),
            "sim_mean": round(s_mean, 4),
            "difference": round(s_mean - h_mean, 4),
            "direction": "model_overestimates" if s_mean > h_mean else "model_underestimates",
        }

    return {
        "num_topics": len(topic_comparison),
        "num_comparable_points": len(human_lcds),
        "spearman_rho_all": spearman,
        "spearman_by_pair": pair_rhos,
        "bias": bias,
        "topics": topic_comparison,
    }


def generate_report(comparison, human_data, sim_data):
    """Generate markdown comparison report."""
    topics = comparison["topics"]
    pairs = ["zh-de", "zh-en", "de-en"]

    md = []
    md.append("# LinguaGraph Human vs Model Comparison\n")
    md.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    md.append("---\n")

    # Summary
    md.append("## Summary\n")
    md.append(f"| Metric | Value | Interpretation |\n")
    md.append(f"|--------|-------|----------------|\n")

    rho = comparison.get("spearman_rho_all")
    if rho is not None:
        strength = "strong" if abs(rho) > 0.7 else ("moderate" if abs(rho) > 0.4 else "weak")
        md.append(f"| Spearman ρ (all) | {rho:.4f} | {strength} correlation |\n")
    else:
        md.append(f"| Spearman ρ (all) | N/A | Need more data points |\n")

    bias = comparison.get("bias")
    if bias:
        direction = "overestimates" if bias["difference"] > 0 else "underestimates"
        md.append(f"| Model bias | {bias['difference']:+.4f} | Model {direction} LDS by {abs(bias['difference']):.4f} |\n")

    md.append(f"| Comparable data points | {comparison['num_comparable_points']} | ≥ 9 for reliable Spearman |\n")
    md.append(f"| Topics analyzed | {comparison['num_topics']} | \n")

    # Per-pair Spearman
    md.append("\n## Per-Pair Spearman Correlation\n")
    md.append("| Pair | ρ | Interpretation |\n")
    md.append("|------|---|----------------|\n")
    for pair in pairs:
        rho_p = comparison["spearman_by_pair"].get(pair)
        if rho_p is not None:
            strength = "strong" if abs(rho_p) > 0.7 else ("moderate" if abs(rho_p) > 0.4 else "weak")
            md.append(f"| {pair} | {rho_p:.4f} | {strength} |\n")
        else:
            md.append(f"| {pair} | N/A | Insufficient data |\n")

    # Per-topic detail
    md.append("\n## Per-Topic LDS Comparison\n")
    md.append("| Topic | Human LDS | Simulation LDS | Difference |\n")
    md.append("|-------|-----------|----------------|------------|\n")

    for t in topics:
        h_vals = [t[f"human_{p}"] for p in pairs if t.get(f"human_{p}") is not None]
        s_vals = [t[f"sim_{p}"] for p in pairs if t.get(f"sim_{p}") is not None]
        if h_vals and s_vals:
            h_mean = sum(h_vals) / len(h_vals)
            s_mean = sum(s_vals) / len(s_vals)
            diff = s_mean - h_mean
            md.append(f"| {t['topic']} | {h_mean:.4f} | {s_mean:.4f} | {diff:+.4f} |\n")
        else:
            md.append(f"| {t['topic']} | — | — | — |\n")

    # Ranking comparison
    md.append("\n## LDS Ranking Comparison\n")
    md.append("| Rank | Human | Simulation |\n")
    md.append("|------|-------|------------|\n")

    # Create ranking tables
    human_ranking = []
    for t in topics:
        h_vals = [t[f"human_{p}"] for p in pairs if t.get(f"human_{p}") is not None]
        if h_vals:
            human_ranking.append((t["topic"], sum(h_vals) / len(h_vals)))

    sim_ranking = []
    for t in topics:
        s_vals = [t[f"sim_{p}"] for p in pairs if t.get(f"sim_{p}") is not None]
        if s_vals:
            sim_ranking.append((t["topic"], sum(s_vals) / len(s_vals)))

    human_ranking.sort(key=lambda x: x[1], reverse=True)
    sim_ranking.sort(key=lambda x: x[1], reverse=True)

    max_rank = max(len(human_ranking), len(sim_ranking))
    for i in range(max_rank):
        h_entry = f"{human_ranking[i][0]} ({human_ranking[i][1]:.4f})" if i < len(human_ranking) else "—"
        s_entry = f"{sim_ranking[i][0]} ({sim_ranking[i][1]:.4f})" if i < len(sim_ranking) else "—"
        md.append(f"| {i+1} | {h_entry} | {s_entry} |\n")

    # Key finding
    md.append("\n## Key Finding\n")
    if rho is not None and rho > 0.7:
        md.append("**Human LDS and simulation LDS are strongly correlated.**\n")
        md.append("This suggests that LLM persona simulation captures some of the\n")
        md.append("same cross-language cognitive patterns observed in humans.\n")
        md.append("However, systematic biases exist (see Bias section).\n")
    elif rho is not None and rho > 0:
        md.append("**Human LDS and simulation LDS show moderate/weak correlation.**\n")
        md.append("The model does not fully reproduce human cross-language cognitive patterns.\n")
        md.append("This suggests that linguistic cognition has human-specific components\n")
        md.append("not captured by current LLMs with persona prompting.\n")
    else:
        md.append("**Insufficient data to determine correlation.**\n")

    md.append("\n## Interpretation\n")
    md.append("The simulation serves as a **zero-shot cognitive baseline**.\n")
    md.append("If human LDS differs systematically from simulation LDS,\n")
    md.append("this indicates that linguistic cognitive structures are not fully reproducible\n")
    md.append("by current language models — pointing to human-specific cognitive processing.\n")

    # Save
    outdir = PROJECT_DIR / "research" / "findings"
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / "human_vs_model_comparison.md"
    outpath.write_text("\n".join(md), encoding="utf-8")
    print(f"[OK] Report saved to {outpath}")

    return "\n".join(md)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compare Human vs Model LDS")
    parser.add_argument("--report", action="store_true", help="Generate markdown report")
    parser.add_argument("--export-json", type=str, help="Export to JSON file")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  Human vs Model LDS Comparison")
    print(f"{'='*50}")

    from db_utils import get_connection
    conn = get_connection()

    human, simulation, wiki = load_lcd_data(conn)
    conn.close()

    print(f"\n  Human rows:       {len(human)}")
    print(f"  Simulation rows:  {len(simulation)}")
    print(f"  Wikipedia rows:   {len(wiki)}")

    if not human:
        print("\n[ERROR] No human data yet. Collect pilot data first.")
        return

    if not simulation:
        print("\n[INFO] No simulation data. Run simulate_baseline.py first.")
        print("  Use: python scripts/simulate_baseline.py --all --n 30")
        return

    human_data = structure_by_topic(human)
    sim_data = structure_by_topic(simulation)
    ref_data = structure_by_topic(wiki) if wiki else None

    comparison = compare_datasets(human_data, sim_data, ref_data)

    print(f"\n  Topics compared:   {comparison['num_topics']}")
    print(f"  Comparable points: {comparison['num_comparable_points']}")
    if comparison["spearman_rho_all"] is not None:
        print(f"  Spearman ρ:        {comparison['spearman_rho_all']:.4f}")

    # Save JSON
    if args.export_json:
        outpath = Path(args.export_json)
    else:
        outpath = PROJECT_DIR / "research" / "findings" / "human_vs_model_comparison.json"
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(comparison, f, ensure_ascii=False, indent=2)
    print(f"[OK] Data saved to {outpath}")

    # Report
    if args.report or True:
        generate_report(comparison, human_data, sim_data)

    print(f"\n[DONE]\n")


if __name__ == "__main__":
    main()
