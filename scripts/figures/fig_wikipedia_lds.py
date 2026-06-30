#!/usr/bin/env python3
"""
Bonus: Wikipedia Concept LDS Analysis

Computes LDS across 5 social topics (Freedom, Justice, Responsibility, Home, Success)
extracted from ZH/EN/DE Wikipedia. This serves as a "cultural concept" middle ground
between LDS-K (textbook knowledge) and LDS-C (human cognitive expression).

Outputs:
  outputs/figures/fig_wikipedia_lds.png (300 DPI)
  outputs/figures/fig_wikipedia_lds_data.csv

Usage:
    python scripts/figures/fig_wikipedia_lds.py
"""

import csv, json, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
WIKI_DIR = PROJECT_ROOT / "data" / "wikipedia_extractions"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def lds_jaccard(nodes_a: list, nodes_b: list, edges_a: list, edges_b: list) -> float:
    set_a, set_b = set(nodes_a), set(nodes_b)
    node_jac = len(set_a & set_b) / max(len(set_a | set_b), 1)
    set_ea, set_eb = set(edges_a), set(edges_b)
    edge_jac = len(set_ea & set_eb) / max(len(set_ea | set_eb), 1)
    return round(1.0 - (node_jac + edge_jac) / 2, 4)


def load_wiki_data() -> dict:
    """Load all Wikipedia extractions, return {topic: {lang: data}}."""
    topics = {}
    for fpath in sorted(WIKI_DIR.glob("*.json")):
        d = json.loads(fpath.read_text(encoding="utf-8"))
        topic = d.get("topic", "unknown")
        lang = d.get("language", "unknown")
        if topic not in topics:
            topics[topic] = {}
        topics[topic][lang] = {
            "concepts": [c["name"] for c in d.get("concepts", [])],
            "edges": [(r["source"], r["target"]) for r in d.get("relations", [])],
        }
    return topics


def compute_lds_for_topic(topic_data: dict) -> dict:
    """Compute LDS for all 3 language pairs within a topic."""
    langs = ["zh", "en", "de"]
    pairs = [("ZH-EN", "zh", "en"), ("DE-EN", "de", "en"), ("ZH-DE", "zh", "de")]

    results = {}
    for pair_name, la, lb in pairs:
        if la not in topic_data or lb not in topic_data:
            results[pair_name] = None
            continue
        nodes_a = topic_data[la]["concepts"]
        nodes_b = topic_data[lb]["concepts"]
        edges_a = topic_data[la]["edges"]
        edges_b = topic_data[lb]["edges"]
        if not nodes_a or not nodes_b:
            results[pair_name] = None
            continue
        results[pair_name] = lds_jaccard(nodes_a, nodes_b, edges_a, edges_b)

    return results


def compute_pooled_lds(topics: dict) -> dict:
    """Compute LDS across ALL topics combined (pooled)."""
    pooled: dict[str, dict] = {"zh": {"concepts": [], "edges": []},
                                "en": {"concepts": [], "edges": []},
                                "de": {"concepts": [], "edges": []}}
    for tname, tdata in topics.items():
        for lang in ["zh", "en", "de"]:
            if lang in tdata:
                pooled[lang]["concepts"].extend(tdata[lang]["concepts"])
                pooled[lang]["edges"].extend(tdata[lang]["edges"])

    # Deduplicate
    for lang in ["zh", "en", "de"]:
        pooled[lang]["concepts"] = list(set(pooled[lang]["concepts"]))
        pooled[lang]["edges"] = list(set(pooled[lang]["edges"]))

    pairs = [("ZH-EN", "zh", "en"), ("DE-EN", "de", "en"), ("ZH-DE", "zh", "de")]
    results = {}
    for pair_name, la, lb in pairs:
        results[pair_name] = lds_jaccard(
            pooled[la]["concepts"], pooled[lb]["concepts"],
            pooled[la]["edges"], pooled[lb]["edges"],
        )
    return results


def main():
    print("Bonus: Wikipedia Concept LDS Analysis")
    print("  Loading Wikipedia extractions...")
    topics = load_wiki_data()
    print(f"  Found {len(topics)} topics")

    for tname, tdata in topics.items():
        langs = list(tdata.keys())
        sizes = {lang: len(tdata[lang].get("concepts", [])) for lang in langs}
        print(f"    {tname}: {sizes}")

    # Per-topic LDS
    topic_lds = {}
    for tname in sorted(topics.keys()):
        topic_lds[tname] = compute_lds_for_topic(topics[tname])

    # Pooled LDS
    pooled = compute_pooled_lds(topics)

    print("\n  Per-topic LDS:")
    for tname in sorted(topic_lds.keys()):
        vals = topic_lds[tname]
        fmt = " | ".join(f"{k}={v:.4f}" if v else f"{k}=N/A" for k, v in vals.items())
        print(f"    {tname:20s}: {fmt}")

    print("\n  Pooled LDS (all topics combined):")
    for pair, val in pooled.items():
        print(f"    {pair}: {val:.4f}")

    # Compare with textbook LDS-K
    print("\n  Comparison with Textbook LDS-K:")
    textbook_lds = {"ZH-EN": 0.9336, "DE-EN": 0.9382, "ZH-DE": 0.5188}
    for pair in ["ZH-EN", "DE-EN", "ZH-DE"]:
        wiki_val = pooled.get(pair, 0)
        text_val = textbook_lds.get(pair, 0)
        delta = wiki_val - text_val
        print(f"    {pair}: Wiki={wiki_val:.4f} vs Text={text_val:.4f}  (delta={delta:+.4f})")

    # ── Plot ──
    pairs_display = ["ZH-EN", "DE-EN", "ZH-DE"]
    topic_names = sorted(topic_lds.keys())
    n_topics = len(topic_names)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    # Left: Per-topic grouped bar chart
    ax = axes[0]
    x = np.arange(n_topics)
    width = 0.22

    colors = {"ZH-EN": "#2563eb", "DE-EN": "#ea580c", "ZH-DE": "#16a34a"}
    for i, pair in enumerate(pairs_display):
        vals = [topic_lds[t].get(pair, 0) or 0 for t in topic_names]
        offset = (i - 1) * width
        bars = ax.bar(x + offset, vals, width, label=pair, color=colors[pair], alpha=0.85)
        for bar, val in zip(bars, vals):
            if val > 0.01:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                        f"{val:.3f}", ha="center", va="bottom", fontsize=6, rotation=45)

    ax.set_xlabel("Social Topic", fontsize=11)
    ax.set_ylabel("LDS (Wikipedia)", fontsize=11)
    ax.set_title("Per-Topic Wikipedia Concept LDS", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels([t.capitalize() for t in topic_names], fontsize=8)
    ax.legend(fontsize=8)
    ax.set_ylim(0, 1.15)

    # Right: Pooled vs Textbook comparison
    ax = axes[1]
    x2 = np.arange(len(pairs_display))
    width2 = 0.3

    text_vals = [textbook_lds[p] for p in pairs_display]
    wiki_vals = [pooled.get(p, 0) for p in pairs_display]

    ax.bar(x2 - width2/2, text_vals, width2, label="Textbook (LDS-K)", color="#6b7280", alpha=0.7)
    ax.bar(x2 + width2/2, wiki_vals, width2, label="Wikipedia (Social)", color="#f59e0b", alpha=0.7)

    for i, (tv, wv) in enumerate(zip(text_vals, wiki_vals)):
        ax.text(i - width2/2, tv + 0.02, f"{tv:.3f}", ha="center", va="bottom", fontsize=7)
        ax.text(i + width2/2, wv + 0.02, f"{wv:.3f}", ha="center", va="bottom", fontsize=7)

    ax.set_xlabel("Language Pair", fontsize=11)
    ax.set_ylabel("LDS", fontsize=11)
    ax.set_title("Wikipedia Social vs Textbook Knowledge", fontsize=10)
    ax.set_xticks(x2)
    ax.set_xticklabels(pairs_display, fontsize=9)
    ax.legend(fontsize=8)
    ax.set_ylim(0, 1.15)

    plt.tight_layout()
    path = OUTPUT_DIR / "fig_wikipedia_lds.png"
    fig.savefig(path, dpi=300)
    print(f"\n  [OK] {path}")
    plt.close(fig)

    # CSV
    csv_path = OUTPUT_DIR / "fig_wikipedia_lds_data.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["topic", "language_pair", "lds"])
        for tname in topic_names:
            for pair in pairs_display:
                val = topic_lds[tname].get(pair)
                if val is not None:
                    w.writerow([tname, pair, val])
        w.writerow(["pooled", "ZH-EN", pooled.get("ZH-EN", "")])
        w.writerow(["pooled", "DE-EN", pooled.get("DE-EN", "")])
        w.writerow(["pooled", "ZH-DE", pooled.get("ZH-DE", "")])
        w.writerow(["textbook", "ZH-EN", textbook_lds.get("ZH-EN", "")])
        w.writerow(["textbook", "DE-EN", textbook_lds.get("DE-EN", "")])
        w.writerow(["textbook", "ZH-DE", textbook_lds.get("ZH-DE", "")])
    print(f"  [OK] {csv_path}")


if __name__ == "__main__":
    main()
