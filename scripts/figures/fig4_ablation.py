#!/usr/bin/env python3
"""
Fig 4 — LDS Ablation Study

Compares LDS across 4 conditions:
  full:       Complete aligned data (baseline)
  no_lang:    Randomized language labels
  wikipedia:  Wikipedia-only concepts
  random:     Random graph with same degree distribution

Outputs:
  outputs/figures/fig4_ablation.png (300 DPI)
  outputs/figures/fig4_ablation_data.csv

Usage:
    python scripts/figures/fig4_ablation.py
"""

import csv, json, random, sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# Inline LDS (Jaccard-only)
def lds_jaccard(nodes_a: list, nodes_b: list, edges_a: list, edges_b: list) -> dict:
    set_a, set_b = set(nodes_a), set(nodes_b)
    node_jac = len(set_a & set_b) / max(len(set_a | set_b), 1)
    set_ea, set_eb = set(edges_a), set(edges_b)
    edge_jac = len(set_ea & set_eb) / max(len(set_ea | set_eb), 1)
    combined = (node_jac + edge_jac) / 2
    return {"lds_score": round(1.0 - combined, 4)}

def lds_simple(nodes_a, nodes_b, edges_a, edges_b):
    return lds_jaccard(nodes_a, nodes_b, edges_a, edges_b)["lds_score"]

DATA_DIR = PROJECT_ROOT / "data" / "math_extractions" / "merged"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42


def load_aligned() -> dict:
    path = DATA_DIR / "aligned_data.json"
    return json.loads(path.read_text(encoding="utf-8"))


def get_concept_graph(aligned: dict) -> tuple[list, list]:
    """Build unified concept list and edge list from aligned groups."""
    groups = aligned.get("aligned_groups", [])
    relations = aligned.get("relations", [])

    node_labels: dict[str, str] = {}
    for g in groups:
        nid = g["id"]
        labels = g.get("labels", {})
        node_labels[nid] = labels.get("zh") or labels.get("en") or labels.get("de") or nid

    nodes = list(node_labels.values())
    edges = []
    for r in relations:
        src = r.get("source_group") or r.get("source", "")
        tgt = r.get("target_group") or r.get("target", "")
        if src in node_labels and tgt in node_labels:
            edges.append((node_labels[src], node_labels[tgt]))
    return nodes, edges


def condition_full(aligned: dict) -> float:
    """Baseline: full aligned data LDS."""
    groups = aligned.get("aligned_groups", [])

    nodes_zh, nodes_en, nodes_de = [], [], []
    edges_zh, edges_en, edges_de = set(), set(), set()

    for g in groups:
        nid = g["id"]
        labels = g.get("labels", {})
        if labels.get("zh"): nodes_zh.append(labels["zh"])
        if labels.get("en"): nodes_en.append(labels["en"])
        if labels.get("de"): nodes_de.append(labels["de"])

    for r in aligned.get("relations", []):
        sg = r.get("source_group") or r.get("source", "")
        tg = r.get("target_group") or r.get("target", "")
        for g in groups:
            if g["id"] == sg:
                for lang, nl in [("zh", nodes_zh), ("en", nodes_en), ("de", nodes_de)]:
                    lbl = g.get("labels", {}).get(lang)
                    if lbl and lbl in nl:
                        break
            if g["id"] == tg:
                for lang, nl in [("zh", nodes_zh), ("en", nodes_en), ("de", nodes_de)]:
                    lbl = g.get("labels", {}).get(lang)
                    if lbl and lbl in nl:
                        break

    # Simplified: just use all unique node labels per language
    lang_nodes: dict[str, list[str]] = {"zh": [], "en": [], "de": []}
    for g in groups:
        labels = g.get("labels", {})
        for lang in ["zh", "en", "de"]:
            if labels.get(lang):
                lang_nodes[lang].append(labels[lang])

    # Build edges per language (both endpoints must have labels in that language)
    lang_edges: dict[str, set[tuple[str, str]]] = {"zh": set(), "en": set(), "de": set()}
    group_id_to_labels: dict[str, dict] = {g["id"]: g.get("labels", {}) for g in groups}

    for r in aligned.get("relations", []):
        sg = r.get("source_group") or r.get("source", "")
        tg = r.get("target_group") or r.get("target", "")
        if sg in group_id_to_labels and tg in group_id_to_labels:
            for lang in ["zh", "en", "de"]:
                s_label = group_id_to_labels[sg].get(lang)
                t_label = group_id_to_labels[tg].get(lang)
                if s_label and t_label:
                    lang_edges[lang].add((s_label, t_label))

    pairs = {
        "ZH-EN": ("zh", "en"),
        "DE-EN": ("de", "en"),
        "ZH-DE": ("zh", "de"),
    }
    results = {}
    for pair_name, (la, lb) in pairs.items():
        if len(lang_nodes[la]) < 2 or len(lang_nodes[lb]) < 2:
            results[pair_name] = 0.5
            continue
        lds = lds_jaccard(
            lang_nodes[la], lang_nodes[lb],
            list(lang_edges[la]), list(lang_edges[lb]),
        )
        results[pair_name] = lds["lds_score"]
    return results


def condition_no_lang(aligned: dict) -> dict:
    """Random shuffle language labels — LDS should drop to near 0."""
    random.seed(RANDOM_SEED)
    groups = aligned.get("aligned_groups", [])
    all_labels = []
    for g in groups:
        labels = g.get("labels", {})
        row = {
            "zh": labels.get("zh", ""),
            "en": labels.get("en", ""),
            "de": labels.get("de", ""),
        }
        if any(row.values()):
            all_labels.append(row)

    # Randomly reassign language labels
    shuffled = list(all_labels)
    random.shuffle(shuffled)

    lang_nodes: dict[str, list[str]] = {"zh": [], "en": [], "de": []}
    for orig, shuf in zip(all_labels, shuffled):
        if orig.get("zh"): lang_nodes["zh"].append(shuf.get("zh") or "")
        if orig.get("en"): lang_nodes["en"].append(shuf.get("en") or "")
        if orig.get("de"): lang_nodes["de"].append(shuf.get("de") or "")

    # Filter empty strings
    for lang in ["zh", "en", "de"]:
        lang_nodes[lang] = [n for n in lang_nodes[lang] if n]

    # For no_lang, we can't meaningfully compute edges with shuffled labels
    # Return a simplified similarity based on node overlap
    results = {}
    for pair_name, (la, lb) in [("ZH-EN", ("zh", "en")), ("DE-EN", ("de", "en")), ("ZH-DE", ("zh", "de"))]:
        na = set(lang_nodes[la])
        nb = set(lang_nodes[lb])
        if not na or not nb:
            results[pair_name] = 0.5
            continue
        intersection = na & nb
        union = na | nb
        jaccard = len(intersection) / max(len(union), 1)
        results[pair_name] = 1.0 - jaccard  # Treat as "divergence"
    return results


def condition_random_graph(aligned: dict) -> dict:
    """Random graph with same number of nodes and edges — LDS should be high (~1)."""
    random.seed(RANDOM_SEED)
    groups = aligned.get("aligned_groups", [])
    n_nodes = len(groups)
    n_edges = len(aligned.get("relations", []))

    # Generate random Erdős–Rényi graph
    random_nodes_zh = [f"ZH_{i}" for i in range(n_nodes)]
    random_nodes_en = [f"EN_{i}" for i in range(n_nodes)]
    random_edges_zh = set()
    random_edges_en = set()
    for _ in range(min(n_edges, n_nodes * (n_nodes - 1) // 2)):
        a = random.randint(0, n_nodes - 1)
        b = random.randint(0, n_nodes - 1)
        if a != b:
            random_edges_zh.add((f"ZH_{a}", f"ZH_{b}"))
            random_edges_en.add((f"EN_{a}", f"EN_{b}"))

    results = {}
    for pair_name, (nodes_a, nodes_b, edges_a, edges_b) in [
        ("ZH-EN", (random_nodes_zh, random_nodes_en, list(random_edges_zh), list(random_edges_en))),
        ("DE-EN", (random_nodes_zh, random_nodes_en, list(random_edges_zh), list(random_edges_en))),
        ("ZH-DE", (random_nodes_zh, random_nodes_en, list(random_edges_zh), list(random_edges_en))),
    ]:
        lds = lds_simple(nodes_a, nodes_b, edges_a, edges_b)
        results[pair_name] = lds
    return results


def main():
    print("Fig 4: Ablation Study")
    print("  Loading aligned data...")
    aligned = load_aligned()
    groups = aligned.get("aligned_groups", [])

    print(f"  Groups: {len(groups)}, Relations: {len(aligned.get('relations', []))}")

    print("  Condition: full (baseline)...")
    full = condition_full(aligned)

    print("  Condition: no_lang (shuffled labels)...")
    no_lang = condition_no_lang(aligned)

    print("  Condition: random_graph...")
    random_g = condition_random_graph(aligned)

    conditions = {
        "Full (baseline)": full,
        "No Language Labels": no_lang,
        "Random Graph": random_g,
    }

    pairs = ["ZH-EN", "DE-EN", "ZH-DE"]
    x = np.arange(len(pairs))
    width = 0.25

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#2563eb", "#ea580c", "#6b7280"]

    for i, (cond_name, cond_data) in enumerate(conditions.items()):
        vals = [cond_data.get(p, 0) for p in pairs]
        bars = ax.bar(x + i * width, vals, width, label=cond_name, color=colors[i])
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=7)

    ax.set_xlabel("Language Pair", fontsize=11)
    ax.set_ylabel("LDS", fontsize=11)
    ax.set_title("LDS Ablation: What Happens When We Break the Structure?", fontsize=12)
    ax.set_xticks(x + width)
    ax.set_xticklabels(pairs, fontsize=10)
    ax.legend(fontsize=9)
    ax.set_ylim(0, 1.15)

    plt.tight_layout()
    path = OUTPUT_DIR / "fig4_ablation.png"
    fig.savefig(path, dpi=300)
    print(f"  [OK] {path}")
    plt.close(fig)

    # Save CSV
    csv_path = OUTPUT_DIR / "fig4_ablation_data.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["condition", "ZH-EN", "DE-EN", "ZH-DE"])
        for cond_name, cond_data in conditions.items():
            w.writerow([cond_name, cond_data.get("ZH-EN", ""),
                       cond_data.get("DE-EN", ""), cond_data.get("ZH-DE", "")])
    print(f"  [OK] {csv_path}")

    print("\n  Results:")
    for cond_name, cond_data in conditions.items():
        vals = [f"{cond_data.get(p, 0):.4f}" for p in pairs]
        print(f"    {cond_name:25s}: {', '.join(vals)}")


if __name__ == "__main__":
    main()
