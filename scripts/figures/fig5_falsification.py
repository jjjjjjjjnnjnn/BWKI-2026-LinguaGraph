#!/usr/bin/env python3
"""
Fig 5 — Falsification Tests

Tests whether LDS survives adversarial attacks:
  Panel A: Random language label swap — LDS should collapse
  Panel B: Graph permutation (random edge rewiring) — LDS should drop
  Panel C: Model replacement — F1 comparison across 4 LLMs

Outputs:
  outputs/figures/fig5_falsification.png (300 DPI)
  outputs/figures/fig5_falsification_data.csv

Usage:
    python scripts/figures/fig5_falsification.py
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

MODEL_COMP_DIR = PROJECT_ROOT / "data" / "model_comparison"

from _lds_utils import lds_jaccard, load_aligned, get_lang_graphs, RANDOM_SEED

N_TRIALS = 10

def compute_lds_for_pair(nodes_a, nodes_b, edges_a, edges_b) -> float:
    if len(nodes_a) < 2 or len(nodes_b) < 2:
        return 0.5
    return lds_jaccard(nodes_a, nodes_b, edges_a, edges_b)["lds_score"]

def baseline_lds(lang_nodes, lang_edges) -> dict:
    results = {}
    for pair_name, (la, lb) in [("ZH-EN", ("zh", "en")), ("DE-EN", ("de", "en")), ("ZH-DE", ("zh", "de"))]:
        results[pair_name] = compute_lds_for_pair(
            lang_nodes[la], lang_nodes[lb],
            list(lang_edges[la]), list(lang_edges[lb]),
        )
    return results

def panel_a_random_swap(lang_nodes, lang_edges) -> dict:
    random.seed(RANDOM_SEED)
    all_labels = []
    for groups in load_aligned().get("aligned_groups", []):
        labels = groups.get("labels", {})
        row = [labels.get("zh", ""), labels.get("en", ""), labels.get("de", "")]
        if any(row):
            all_labels.append(row)
    results = {"ZH-EN": [], "DE-EN": [], "ZH-DE": []}
    for trial in range(N_TRIALS):
        shuffled = list(all_labels)
        random.shuffle(shuffled)
        swapped: dict[str, list[str]] = {"zh": [], "en": [], "de": []}
        for orig, shuf in zip(all_labels, shuffled):
            if orig[0]: swapped["zh"].append(shuf[0] or "")
            if orig[1]: swapped["en"].append(shuf[1] or "")
            if orig[2]: swapped["de"].append(shuf[2] or "")
        for pair_name, (la, lb) in [("ZH-EN", ("zh", "en")), ("DE-EN", ("de", "en")), ("ZH-DE", ("zh", "de"))]:
            na = [n for n in swapped[la] if n]
            nb = [n for n in swapped[lb] if n]
            if not na or not nb:
                results[pair_name].append(0.5)
                continue
            intersection = len(set(na) & set(nb))
            union = len(set(na) | set(nb))
            jaccard = intersection / max(union, 1)
            results[pair_name].append(1.0 - jaccard)
    return {k: (np.mean(v), np.std(v)) for k, v in results.items()}

def panel_b_graph_permutation(lang_nodes, lang_edges) -> dict:
    random.seed(RANDOM_SEED)
    results = {"ZH-EN": [], "DE-EN": [], "ZH-DE": []}
    for trial in range(N_TRIALS):
        perm_edges: dict[str, list[tuple[str, str]]] = {"zh": [], "en": [], "de": []}
        for lang in ["zh", "en", "de"]:
            edges = list(lang_edges[lang])
            nodes = list(lang_nodes[lang])
            if not edges:
                continue
            new_edges = []
            for s, t in edges:
                if random.random() < 0.8:
                    s_new = random.choice(nodes)
                    t_new = random.choice(nodes)
                    while s_new == t_new:
                        t_new = random.choice(nodes)
                    new_edges.append((s_new, t_new))
                else:
                    new_edges.append((s, t))
            perm_edges[lang] = new_edges
        for pair_name, (la, lb) in [("ZH-EN", ("zh", "en")), ("DE-EN", ("de", "en")), ("ZH-DE", ("zh", "de"))]:
            lds = compute_lds_for_pair(
                lang_nodes[la], lang_nodes[lb],
                perm_edges[la], perm_edges[lb],
            )
            results[pair_name].append(lds)
    return {k: (np.mean(v), np.std(v)) for k, v in results.items()}

def panel_c_model_comparison() -> dict:
    """Load model comparison results. Returns individual models and benchmark summary."""
    models = {}
    benchmark = {"total": 0, "mean_f1": 0, "std_f1": 0}
    if not MODEL_COMP_DIR.exists():
        return models, benchmark

    # Check for aggregated benchmark first
    agg_path = PROJECT_ROOT / "outputs" / "figures" / "model_benchmark_full.json"
    if agg_path.exists():
        agg = json.loads(agg_path.read_text(encoding="utf-8"))
        if len(agg) > 5:
            f1s = [m["f1"] for m in agg if m["f1"] > 0]
            benchmark = {
                "total": len(f1s),
                "mean_f1": round(sum(f1s) / max(len(f1s), 1), 4),
                "std_f1": round(float(np.std(f1s)), 4),
                "max_f1": max(f1s),
                "min_f1": min(f1s),
            }

    # Load individual model results
    for fpath in sorted(MODEL_COMP_DIR.glob("*_results.json")):
        d = json.loads(fpath.read_text(encoding="utf-8"))
        model_name = d.get("model", fpath.stem)
        summary = d.get("summary", {})
        f1 = summary.get("mean_f1", 0)
        n_valid = d.get("valid", d.get("total_items", 0))
        # Filter: valid extraction with meaningful F1 (>=0.5)
        if n_valid >= 5 and f1 >= 0.5:
            models[model_name] = {
                "f1": f1,
                "precision": summary.get("mean_precision", 0),
                "recall": summary.get("mean_recall", 0),
                "n": n_valid,
            }
    return models, benchmark


def main():
    print("Fig 5: Falsification Tests")
    print("  Loading aligned data...")
    aligned = load_aligned()
    lang_nodes, lang_edges = get_lang_graphs(aligned)

    print("  Baseline LDS...")
    base = baseline_lds(lang_nodes, lang_edges)

    print(f"  Panel A: Random language swap ({N_TRIALS} trials)...")
    swap = panel_a_random_swap(lang_nodes, lang_edges)

    print(f"  Panel B: Graph permutation ({N_TRIALS} trials)...")
    perm = panel_b_graph_permutation(lang_nodes, lang_edges)

    print("  Panel C: Model comparison...")
    models, benchmark = panel_c_model_comparison()
    if benchmark["total"] > 0:
        print(f"    Benchmark: {benchmark['total']} models, mean F1={benchmark['mean_f1']:.4f}+-{benchmark['std_f1']:.4f}")
    for m, s in sorted(models.items()):
        print(f"    {m}: F1={s['f1']:.4f}, n={s['n']}")
    if not models:
        print("    No model comparison data found")

    pairs = ["ZH-EN", "DE-EN", "ZH-DE"]
    x = np.arange(len(pairs))
    width = 0.2

    fig, axes = plt.subplots(1, 3, figsize=(12, 4.5), sharey=False)

    # ── Panel A: Random Language Swap ──
    ax = axes[0]
    labels_a = ["Baseline", "Random Swap"]
    vals_a = [
        [base[p] for p in pairs],
        [swap[p][0] for p in pairs],
    ]
    colors_a = ["#2563eb", "#ea580c"]
    err_a = [None, [swap[p][1] for p in pairs]]

    for i, (label, vals, color) in enumerate(zip(labels_a, vals_a, colors_a)):
        offset = (i - 0.5) * width
        bars = ax.bar(x + offset, vals, width, label=label, color=color, alpha=0.85)
        if err_a[i]:
            ax.errorbar(x + offset, vals, yerr=err_a[i], fmt="none", capsize=3, color="black", alpha=0.5)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=7)
    ax.set_title("A: Random Language Swap", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(pairs, fontsize=9)
    ax.set_ylabel("LDS", fontsize=11)
    ax.set_ylim(0, 1.15)
    ax.legend(fontsize=8)

    # ── Panel B: Graph Permutation ──
    ax = axes[1]
    labels_b = ["Baseline", "Permuted"]
    vals_b = [
        [base[p] for p in pairs],
        [perm[p][0] for p in pairs],
    ]
    colors_b = ["#2563eb", "#6b7280"]
    err_b = [None, [perm[p][1] for p in pairs]]

    for i, (label, vals, color) in enumerate(zip(labels_b, vals_b, colors_b)):
        offset = (i - 0.5) * width
        bars = ax.bar(x + offset, vals, width, label=label, color=color, alpha=0.85)
        if err_b[i]:
            ax.errorbar(x + offset, vals, yerr=err_b[i], fmt="none", capsize=3, color="black", alpha=0.5)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=7)
    ax.set_title("B: Graph Permutation", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(pairs, fontsize=9)
    ax.set_ylim(0, 1.15)
    ax.legend(fontsize=8)

    # ── Panel C: Model Robustness ──
    ax = axes[2]
    has_benchmark = benchmark["total"] > 5

    if models and has_benchmark:
        # Show benchmark distribution with key model annotations
        ax.text(0.5, 0.75,
                f"Benchmark: {benchmark['total']} models\n"
                f"Mean F1 = {benchmark['mean_f1']:.3f}  ({benchmark['std_f1']:.3f})\n"
                f"Range: {benchmark['min_f1']:.2f} - {benchmark['max_f1']:.2f}",
                ha="center", va="center", transform=ax.transAxes,
                fontsize=10, color="#333",
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#eef2ff", edgecolor="#c7d2fe"))

        # Show key models as mini bars
        key_models = {k: v for k, v in sorted(models.items())
                     if "qwen" in k.lower() or "claude" in k.lower() or "deepseek" in k.lower()}
        if key_models:
            names = list(key_models.keys())[:3]
            f1s = [key_models[n]["f1"] for n in names]
            y_pos = [0.35, 0.25, 0.15]
            for name, f1_val, y in zip(names, f1s, y_pos):
                color = "#2563eb" if "qwen" in name.lower() else "#16a34a"
                ax.barh(y, f1_val, 0.08, color=color, alpha=0.85)
                ax.text(f1_val + 0.02, y, f"{name}: {f1_val:.4f}",
                        va="center", fontsize=7)

        ax.set_title(f"C: Model Robustness\n({benchmark['total']} models)", fontsize=10)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

    elif models:
        # Fallback: show individual bars when < 5 models
        model_names = sorted(models.keys())
        f1_vals = [models[m]["f1"] for m in model_names]
        bar_positions = np.arange(len(model_names))
        bars = ax.bar(bar_positions, f1_vals, 0.5, color=["#2563eb", "#16a34a"][:len(model_names)])
        for bar, val, name in zip(bars, f1_vals, model_names):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=8)
        ax.set_title("C: Model F1", fontsize=10)
        ax.set_xticks(bar_positions)
        ax.set_xticklabels(model_names, fontsize=7, rotation=15)
        ax.set_ylabel("F1 Score", fontsize=11)
        ax.set_ylim(0, 1.15)
    else:
        ax.text(0.5, 0.5, "No model comparison\ndata available", ha="center",
                va="center", transform=ax.transAxes, fontsize=10, color="#9ca3af")
        ax.set_title("C: Model Replacement", fontsize=10)
        ax.set_ylim(0, 1)

    plt.tight_layout()
    path = OUTPUT_DIR / "fig5_falsification.png"
    fig.savefig(path, dpi=300)
    print(f"  [OK] {path}")
    plt.close(fig)

    # Save CSV
    csv_path = OUTPUT_DIR / "fig5_falsification_data.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["panel", "condition", "ZH-EN", "DE-EN", "ZH-DE"])

        w.writerow(["A", "Baseline", f"{base['ZH-EN']:.4f}", f"{base['DE-EN']:.4f}", f"{base['ZH-DE']:.4f}"])
        w.writerow(["A", "Random Swap", f"{swap['ZH-EN'][0]:.4f}", f"{swap['DE-EN'][0]:.4f}", f"{swap['ZH-DE'][0]:.4f}"])
        w.writerow(["B", "Baseline", f"{base['ZH-EN']:.4f}", f"{base['DE-EN']:.4f}", f"{base['ZH-DE']:.4f}"])
        w.writerow(["B", "Permuted", f"{perm['ZH-EN'][0]:.4f}", f"{perm['DE-EN'][0]:.4f}", f"{perm['ZH-DE'][0]:.4f}"])

        if models:
            w.writerow(["C", "model", "F1", "precision", "recall", "n"])
            for m, s in models.items():
                w.writerow(["C", m, f"{s['f1']:.4f}", f"{s['precision']:.4f}", f"{s['recall']:.4f}", s["n"]])

    print(f"  [OK] {csv_path}")

    print("\n  Results:")
    print(f"    Baseline:        ZH-EN={base['ZH-EN']:.4f}, DE-EN={base['DE-EN']:.4f}, ZH-DE={base['ZH-DE']:.4f}")
    print(f"    Random swap:     ZH-EN={swap['ZH-EN'][0]:.4f}+-{swap['ZH-EN'][1]:.4f}, ...")
    print(f"    Graph perm:      ZH-EN={perm['ZH-EN'][0]:.4f}+-{perm['ZH-EN'][1]:.4f}, ...")
    if models:
        for m, s in models.items():
            print(f"    Model {m}: F1={s['f1']:.4f}")

if __name__ == "__main__":
    main()
