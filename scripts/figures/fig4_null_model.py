#!/usr/bin/env python3
"""
Fig 4 — LDS Null Model Suite (Ablation)

Replaces the old ablation study with a proper null hypothesis framework:

  1. Full (baseline)        — Real LDS from aligned data
  2. Structure Null         — Degree-preserving random graphs
                             (tests: is LDS driven by degree structure alone?)
  3. Node-Permuted Null     — Randomly permute node labels within each language
                             (tests: do specific concept-label assignments carry signal?)
  4. Complete Random        — Erdős–Rényi random graph with same N, E
                             (tests: is LDS > 0 at all?)

Outputs:
  outputs/figures/fig4_null_model.png (300 DPI)
  outputs/figures/fig4_null_model_data.csv

Usage:
    python scripts/figures/fig4_null_model.py
"""

import csv, json, random, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
N_REWIRINGS = 1000  # double-edge swaps for structure null


# ── Inline LDS (Jaccard-only, no GED dependency) ──

def lds_jaccard(nodes_a: list, nodes_b: list, edges_a: list, edges_b: list) -> dict:
    set_a, set_b = set(nodes_a), set(nodes_b)
    node_jac = len(set_a & set_b) / max(len(set_a | set_b), 1)
    set_ea, set_eb = set(edges_a), set(edges_b)
    edge_jac = len(set_ea & set_eb) / max(len(set_ea | set_eb), 1)
    return {
        "lds_score": round(1.0 - (node_jac + edge_jac) / 2, 4),
        "jaccard_node": round(node_jac, 4),
        "jaccard_edge": round(edge_jac, 4),
    }


# ── Graph loading ──

def load_aligned() -> dict:
    path = PROJECT_ROOT / "data" / "math_extractions" / "merged" / "aligned_data.json"
    return json.loads(path.read_text(encoding="utf-8"))


def get_lang_graphs(aligned: dict) -> tuple[dict, dict]:
    """Return (lang→[node_labels], lang→set_of_edges) with labels from aligned groups."""
    groups = aligned.get("aligned_groups", [])
    gid_to_labels: dict[str, dict] = {g["id"]: g.get("labels", {}) for g in groups}

    lang_nodes: dict[str, list[str]] = {"zh": [], "en": [], "de": []}
    for g in groups:
        labels = g.get("labels", {})
        for lang in ["zh", "en", "de"]:
            if labels.get(lang):
                lang_nodes[lang].append(labels[lang])

    lang_edges: dict[str, set[tuple[str, str]]] = {"zh": set(), "en": set(), "de": set()}
    for r in aligned.get("relations", []):
        sg = r.get("source_group") or r.get("source", "")
        tg = r.get("target_group") or r.get("target", "")
        if sg in gid_to_labels and tg in gid_to_labels:
            for lang in ["zh", "en", "de"]:
                s_label = gid_to_labels[sg].get(lang)
                t_label = gid_to_labels[tg].get(lang)
                if s_label and t_label:
                    lang_edges[lang].add((s_label, t_label))
    return lang_nodes, lang_edges


# ── Null model generators ──

def degree_preserving_rewire(edges: list[tuple], n_swaps: int = N_REWIRINGS) -> list[tuple]:
    """Double-edge swap: preserves degree sequence of each node."""
    if len(edges) < 2:
        return edges
    edge_list = list(edges)
    random.seed(RANDOM_SEED)
    for _ in range(n_swaps):
        i, j = random.randrange(len(edge_list)), random.randrange(len(edge_list))
        if i == j:
            continue
        a, b = edge_list[i]
        c, d = edge_list[j]
        # Check all four nodes are distinct
        if len({a, b, c, d}) < 4:
            continue
        # Avoid self-loops and parallel edges
        if a == d or b == c:
            continue
        if (a, d) in edge_list or (c, b) in edge_list:
            continue
        edge_list[i] = (a, d)
        edge_list[j] = (c, b)
    return edge_list


def condition_full(lang_nodes, lang_edges) -> dict:
    """Baseline: real LDS from aligned data."""
    results = {}
    for pair_name, (la, lb) in [("ZH-EN", ("zh", "en")), ("DE-EN", ("de", "en")), ("ZH-DE", ("zh", "de"))]:
        lds = lds_jaccard(lang_nodes[la], lang_nodes[lb], list(lang_edges[la]), list(lang_edges[lb]))
        results[pair_name] = lds["lds_score"]
    return results


def condition_structure_null(lang_nodes, lang_edges) -> dict:
    """Structure null: degree-preserving rewiring.

    H0: LDS is entirely explained by degree distribution.
    If true, rewired graphs should have the same LDS as real graphs.
    """
    rewired: dict[str, list] = {}
    for lang in ["zh", "en", "de"]:
        rewired[lang] = degree_preserving_rewire(list(lang_edges[lang]))

    results = {}
    for pair_name, (la, lb) in [("ZH-EN", ("zh", "en")), ("DE-EN", ("de", "en")), ("ZH-DE", ("zh", "de"))]:
        lds = lds_jaccard(lang_nodes[la], lang_nodes[lb], rewired[la], rewired[lb])
        results[pair_name] = lds["lds_score"]
    return results


def condition_node_permuted(lang_nodes, lang_edges) -> dict:
    """Node-permuted null: shuffle node labels within each language.

    H0: specific label-to-concept assignments carry no language signal.
    If true, permuted labels yield same LDS as real labels.
    """
    random.seed(RANDOM_SEED)
    permuted: dict[str, list] = {}
    for lang in ["zh", "en", "de"]:
        nodes = list(lang_nodes[lang])
        random.shuffle(nodes)
        permuted[lang] = nodes

    results = {}
    for pair_name, (la, lb) in [("ZH-EN", ("zh", "en")), ("DE-EN", ("de", "en")), ("ZH-DE", ("zh", "de"))]:
        lds = lds_jaccard(permuted[la], permuted[lb], list(lang_edges[la]), list(lang_edges[lb]))
        results[pair_name] = lds["lds_score"]
    return results


def condition_random_graph(lang_nodes, lang_edges) -> dict:
    """Complete random: Erdős–Rényi with same N, E per language.

    H0: any graph with these node/edge counts produces same LDS.
    If true, real LDS is meaningless.
    """
    random.seed(RANDOM_SEED)
    results = {}
    for pair_name, (la, lb) in [("ZH-EN", ("zh", "en")), ("DE-EN", ("de", "en")), ("ZH-DE", ("zh", "de"))]:
        n_a, n_b = len(lang_nodes[la]), len(lang_nodes[lb])
        e_a, e_b = len(lang_edges[la]), len(lang_edges[lb])
        nodes_a = [f"RND_{la}_{i}" for i in range(n_a)]
        nodes_b = [f"RND_{lb}_{i}" for i in range(n_b)]
        edges_a = set()
        edges_b = set()
        for _ in range(min(e_a, n_a * (n_a - 1) // 2)):
            a, b = random.sample(range(n_a), 2)
            edges_a.add((nodes_a[a], nodes_a[b]))
        for _ in range(min(e_b, n_b * (n_b - 1) // 2)):
            a, b = random.sample(range(n_b), 2)
            edges_b.add((nodes_b[a], nodes_b[b]))
        lds = lds_jaccard(nodes_a, nodes_b, list(edges_a), list(edges_b))
        results[pair_name] = lds["lds_score"]
    return results


# ── Plotting ──

PAIRS = ["ZH-EN", "DE-EN", "ZH-DE"]
CONDITION_CONFIG = [
    ("Full (baseline)", "#2563eb", "Real aligned data"),
    ("Structure Null\n(deg.-preserving)", "#ea580c", "Degree-preserving rewired"),
    ("Node-Permuted Null", "#16a34a", "Shuffled node labels"),
    ("Complete Random", "#6b7280", "Erdos–Renyi"),
]


def plot_results(conditions: dict[str, dict]):
    x = np.arange(len(PAIRS))
    width = 0.18

    fig, ax = plt.subplots(figsize=(9, 5))

    for i, (name, color, desc) in enumerate(CONDITION_CONFIG):
        vals = [conditions[name].get(p, 0) for p in PAIRS]
        offset = (i - (len(CONDITION_CONFIG) - 1) / 2) * width
        bars = ax.bar(x + offset, vals, width, label=f"{name}", color=color, alpha=0.85)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.015,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=6.5, rotation=45)

    ax.set_xlabel("Language Pair", fontsize=11)
    ax.set_ylabel("LDS", fontsize=11)
    ax.set_title("LDS Null Model Suite: What Explains the Observed Divergence?", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(PAIRS, fontsize=10)
    ax.legend(fontsize=8, loc="upper right")
    ax.set_ylim(0, 1.15)

    # Annotation box
    ax.text(0.98, 0.98,
            "If Full ≈ Null → metric dominated by null factors\n"
            "If Full > Null → evidence for language-driven structure",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=7, color="#555",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f8f9fa", edgecolor="#ddd"))

    plt.tight_layout()
    path = OUTPUT_DIR / "fig4_null_model.png"
    fig.savefig(path, dpi=300)
    print(f"  [OK] {path}")
    plt.close(fig)


# ── Main ──

def main():
    print("Fig 4: Null Model Suite")
    print("  Loading aligned data...")
    aligned = load_aligned()
    lang_nodes, lang_edges = get_lang_graphs(aligned)

    groups = aligned.get("aligned_groups", [])
    print(f"  Groups: {len(groups)}, Relations: {len(aligned.get('relations', []))}")

    funcs = [
        ("Full (baseline)", condition_full),
        ("Structure Null\n(deg.-preserving)", condition_structure_null),
        ("Node-Permuted Null", condition_node_permuted),
        ("Complete Random", condition_random_graph),
    ]

    results: dict[str, dict] = {}
    for name, func in funcs:
        print(f"  {name}...")
        results[name] = func(lang_nodes, lang_edges)

    plot_results(results)

    # CSV
    csv_path = OUTPUT_DIR / "fig4_null_model_data.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["condition", "ZH-EN", "DE-EN", "ZH-DE"])
        for name, _ in funcs:
            w.writerow([name.replace("\n", " "),
                       results[name].get("ZH-EN", ""),
                       results[name].get("DE-EN", ""),
                       results[name].get("ZH-DE", "")])
    print(f"  [OK] {csv_path}")

    print("\n  Results:")
    for name, _ in funcs:
        vals = " | ".join(f"{results[name].get(p, 0):.4f}" for p in PAIRS)
        print(f"    {name:30s}: {vals}")

    # Scientific interpretation
    full = results.get("Full (baseline)", {})
    struct_null = results.get("Structure Null\n(deg.-preserving)", {})
    print("\n  Interpretation:")
    for p in PAIRS:
        delta = full.get(p, 0) - struct_null.get(p, 0)
        tag = "LDS > null → language signal" if delta > 0.02 else (
              "LDS ≈ null → structure dominates" if abs(delta) <= 0.02 else
              "LDS < null (unexpected)")
        print(f"    {p}: full={full.get(p, 0):.4f} - null={struct_null.get(p, 0):.4f} = {delta:+.4f}  [{tag}]")


if __name__ == "__main__":
    main()
