#!/usr/bin/env python3
"""
Fig 1 — LDS-K: Knowledge Structure Divergence Across Languages

Computes LDS (GED + Node Jaccard + Edge Jaccard) per domain per language pair
from the expert knowledge graphs.

Outputs:
  outputs/figures/fig1_lds_k_heatmap.png (300 DPI)
  outputs/figures/fig1_lds_k_data.csv

Usage:
    python scripts/figures/fig1_lds_k_heatmap.py
"""

import csv, json, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# Inline LDS (Jaccard-only, no GED — GED requires networkx)
def lds_jaccard(nodes_a: list, nodes_b: list, edges_a: list, edges_b: list) -> dict:
    set_a, set_b = set(nodes_a), set(nodes_b)
    node_jac = len(set_a & set_b) / max(len(set_a | set_b), 1)
    set_ea, set_eb = set(edges_a), set(edges_b)
    edge_jac = len(set_ea & set_eb) / max(len(set_ea | set_eb), 1)
    combined = (node_jac + edge_jac) / 2
    return {
        "lds_score": round(1.0 - combined, 4),
        "jaccard_node": round(node_jac, 4),
        "jaccard_edge": round(edge_jac, 4),
    }

EXPERT_DIR = PROJECT_ROOT / "config" / "expert_graphs"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Domains with trilingual data
DOMAINS = [
    ("calculus", "Calculus"),
    ("linear_algebra", "Linear Algebra"),
    ("statistics", "Statistics"),
    ("elementary", "Elementary"),
    ("middle", "Middle School"),
    ("geometry", "Geometry"),
]

LANG_PAIRS = [("zh", "en"), ("de", "en"), ("zh", "de")]
LANG_LABELS = {"zh": "ZH", "en": "EN", "de": "DE"}


def load_graph_data(domain_file: str) -> dict[str, set]:
    """Load concepts grouped by language from an expert graph file."""
    path = EXPERT_DIR / domain_file
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))

    langs: dict[str, set] = {"zh": set(), "en": set(), "de": set()}
    for c in data.get("concepts", []):
        labels = c.get("labels", {})
        for lang in ["zh", "en", "de"]:
            name = labels.get(lang) or (lang + ":" + c.get("name", ""))
            langs[lang].add(name)

    # Build edge sets per language
    edges: dict[str, set[tuple[str, str]]] = {"zh": set(), "en": set(), "de": set()}
    for r in data.get("relations", []):
        src = r.get("source", "")
        tgt = r.get("target", "")
        for lang in ["zh", "en", "de"]:
            # Map source/target IDs to labels if possible
            src_labels = _find_labels(data["concepts"], src)
            tgt_labels = _find_labels(data["concepts"], tgt)
            s = src_labels.get(lang, src)
            t = tgt_labels.get(lang, tgt)
            edges[lang].add((s, t))

    return {"concepts": langs, "edges": edges}


def _find_labels(concepts: list[dict], concept_id: str) -> dict:
    for c in concepts:
        if c.get("name") == concept_id:
            return c.get("labels", {})
    return {}


def compute_lds_k() -> list[dict]:
    """Compute LDS-K for each domain × language pair."""
    results = []
    for domain_key, domain_label in DOMAINS:
        g = load_graph_data(f"{domain_key}.json")
        if not g or not any(g["concepts"].values()):
            print(f"  [SKIP] {domain_label}: no data")
            continue

        row = {"domain": domain_label}
        for la, lb in LANG_PAIRS:
            nodes_a = g["concepts"][la]
            nodes_b = g["concepts"][lb]
            edges_a = g["edges"][la]
            edges_b = g["edges"][lb]

            if len(nodes_a) < 2 or len(nodes_b) < 2:
                row[f"{LANG_LABELS[la]}-{LANG_LABELS[lb]}"] = None
                continue

            lds = lds_jaccard(
                list(nodes_a), list(nodes_b),
                list(edges_a), list(edges_b),
            )
            row[f"{LANG_LABELS[la]}-{LANG_LABELS[lb]}"] = lds["lds_score"]
            row[f"ged_{la}_{lb}"] = round(lds.get("ged_similarity", 0), 4)
            row[f"jaccard_node_{la}_{lb}"] = round(lds.get("jaccard_node", 0), 4)
            row[f"jaccard_edge_{la}_{lb}"] = round(lds.get("jaccard_edge", 0), 4)

        results.append(row)

    return results


def plot_heatmap(results: list[dict]):
    """Generate heatmap: domains × language pairs."""
    if not results:
        print("  [FAIL] No LDS-K data to plot")
        return

    domains = [r["domain"] for r in results]
    pairs = [k for k in results[0].keys() if k.startswith("ZH") or k.startswith("DE")]
    data = np.array([[r.get(p, 0) or 0 for p in pairs] for r in results])

    fig, ax = plt.subplots(figsize=(6, 4))
    im = ax.imshow(data, cmap="YlOrRd", vmin=0, vmax=1, aspect="auto")

    ax.set_xticks(range(len(pairs)))
    ax.set_xticklabels(pairs, fontsize=10)
    ax.set_yticks(range(len(domains)))
    ax.set_yticklabels(domains, fontsize=9)
    ax.set_xlabel("Language Pair", fontsize=11)
    ax.set_ylabel("Knowledge Domain", fontsize=11)
    ax.set_title("LDS-K: Cross-Language Knowledge Structure Divergence", fontsize=12)

    # Annotate cells
    for i in range(len(domains)):
        for j in range(len(pairs)):
            val = data[i, j]
            color = "white" if val > 0.6 else "black"
            ax.text(j, i, f"{val:.3f}", ha="center", va="center", fontsize=8, color=color)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("LDS-K (0 = identical, 1 = fully divergent)", fontsize=9)

    plt.tight_layout()
    path = OUTPUT_DIR / "fig1_lds_k_heatmap.png"
    fig.savefig(path, dpi=300)
    print(f"  [OK] {path}")
    plt.close(fig)


def save_csv(results: list[dict]):
    path = OUTPUT_DIR / "fig1_lds_k_data.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=results[0].keys())
        w.writeheader()
        w.writerows(results)
    print(f"  [OK] {path}")


def main():
    print("Fig 1: LDS-K Heatmap")
    print("  Computing LDS per domain × language pair...")
    results = compute_lds_k()
    if not results:
        print("  [FAIL] No results computed")
        return

    print(f"  {len(results)} domains computed")
    for r in results:
        parts = [f"{k}={v}" for k, v in r.items() if v is not None and k != "domain"]
        print(f"    {r['domain']}: {', '.join(parts[:3])}")

    plot_heatmap(results)
    save_csv(results)
    print("  Done.")


if __name__ == "__main__":
    main()
