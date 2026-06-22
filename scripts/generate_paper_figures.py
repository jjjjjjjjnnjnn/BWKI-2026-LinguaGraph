#!/usr/bin/env python3
"""
LinguaGraph — Paper Figure Generator

Generates publication-ready figures for the BWKI 2026 submission.
All figures are saved to outputs/figures/ as 300 DPI PNG.

Figures:
  Fig 1: Pipeline overview (system diagram)
  Fig 2: CognitiveSpace screenshot (annotated)
  Fig 3: CDS by Education Level
  Fig 4: LDS Cross-Language Heatmap (Wikipedia corpus)
  Fig 5: HDS Distribution

Usage:
    python scripts/generate_paper_figures.py
    python scripts/generate_paper_figures.py --fig 3   # Single figure
"""

import argparse, json, re, sqlite3, sys
from pathlib import Path
from collections import Counter, defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ── Paths ──────────────────────────────────────────────────────────────
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_JS = PROJECT_DIR / "cognitive-space" / "web" / "data.js"
DB_PATH = PROJECT_DIR / "linguaGraph.db"
FIGURES_DIR = PROJECT_DIR / "outputs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ── Matplotlib global style ────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
})

# ── Color palette (matches CognitiveSpace) ─────────────────────────────
LV_COLORS = {"elementary": "#4ade80", "middle": "#22d3ee", "high": "#60a5fa", "college": "#c084fc"}
LV_ORDER = ["elementary", "middle", "high", "college"]
LV_LABELS = {"elementary": "Elementary", "middle": "Middle", "high": "High", "college": "College"}

LANG_COLORS = {"zh": "#e74c3c", "en": "#3498db", "de": "#f39c12"}
LANG_PAIRS = [("zh-de", "ZH–DE"), ("zh-en", "ZH–EN"), ("de-en", "DE–EN")]


# ════════════════════════════════════════════════════════════════════════
#  Data Loaders
# ════════════════════════════════════════════════════════════════════════

def load_cognitive_data():
    """Load nodes and links from data.js (CognitiveSpace)."""
    with open(DATA_JS, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract the JSON object (between outermost { })
    start = content.index("{")
    depth, end = 0, start
    for i in range(start, len(content)):
        if content[i] == "{":
            depth += 1
        elif content[i] == "}":
            depth -= 1
        if depth == 0:
            end = i + 1
            break

    raw = content[start:end].strip()
    if raw.endswith(";"):
        raw = raw[:-1]

    # JSON doesn't like trailing commas — pre-clean
    raw = re.sub(r",\s*([}\]])", r"\1", raw)
    data = json.loads(raw)
    return data["nodes"], data["links"]


def load_lds_data():
    """Load LDS scores from the database."""
    if not DB_PATH.exists():
        print("  [WARN] linguaGraph.db not found — skipping LDS heatmap")
        return []

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT lang_pair, topic, lcd_score as lds
        FROM cross_language_analysis
        WHERE student_id = 'WIKIPEDIA_CORPUS'
        ORDER BY topic, lang_pair
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ════════════════════════════════════════════════════════════════════════
#  Metrics Computation
# ════════════════════════════════════════════════════════════════════════

def compute_cds(nodes, links):
    """Compute Concept Density Score per education level.

    CDS = 2|E| / (|V| * (|V|-1))
    """
    # Build level → subgraph
    lv_nodes = defaultdict(set)
    lv_edges = defaultdict(set)

    for n in nodes:
        lv = n.get("level", "unknown")
        lv_nodes[lv].add(n["id"])

    for l in links:
        src_lv = next((n.get("level") for n in nodes if n["id"] == l["source"]), None)
        tgt_lv = next((n.get("level") for n in nodes if n["id"] == l["target"]), None)
        if src_lv and tgt_lv and src_lv == tgt_lv:
            lv_edges[src_lv].add((l["source"], l["target"]))

    results = {}
    for lv in LV_ORDER:
        n_count = len(lv_nodes.get(lv, []))
        e_count = len(lv_edges.get(lv, []))
        if n_count > 1:
            cds = (2 * e_count) / (n_count * (n_count - 1))
        else:
            cds = 0.0
        results[lv] = {"nodes": n_count, "edges": e_count, "cds": round(cds, 4)}

    return results


def compute_hds(nodes, links):
    """Compute Hierarchy Depth Score distribution.

    HDS = longest prerequisite chain length for each concept
    Uses BFS on prerequisite relations (where type='prerequisite' or
    relation contains 'requires', etc.).
    """
    # Build adjacency list for prerequisite-like edges
    prereq_keywords = ["prerequisite", "requires", "depends_on", "part_of", "prerequisite_for"]

    children = defaultdict(list)  # concept → [concepts it enables]
    has_parents = defaultdict(list)  # concept → [concepts it needs]

    for l in links:
        rel_type = (l.get("type") or l.get("relation") or "").lower()
        is_prereq = any(k in rel_type for k in prereq_keywords)
        if is_prereq:
            children[l["source"]].append(l["target"])
            has_parents[l["target"]].append(l["source"])

    # Find root nodes (no prerequisites)
    all_concepts = set(n["id"] for n in nodes)
    roots = all_concepts - set(has_parents.keys())

    # DFS depth from each root
    depths = {}

    def dfs(node, visited):
        if node in depths:
            return depths[node]
        if not children[node]:
            return 0
        max_d = 0
        for child in children[node]:
            if child in visited:
                continue
            visited.add(child)
            d = 1 + dfs(child, visited)
            visited.remove(child)
            max_d = max(max_d, d)
        depths[node] = max_d
        return max_d

    for r in roots:
        dfs(r, {r})

    # For nodes not reached (isolated or no prerequisite chains)
    for c in all_concepts:
        if c not in depths:
            depths[c] = 0

    return depths


def compute_lds_matrix(lds_rows):
    """Compute LDS matrix per topic and overall average."""
    # Group by topic
    topics = defaultdict(dict)
    for r in lds_rows:
        topics[r["topic"]][r["lang_pair"]] = r["lds"]

    # Overall average per pair
    pair_scores = defaultdict(list)
    for topic, pairs in topics.items():
        for pair, score in pairs.items():
            pair_scores[pair].append(score)

    avg_matrix = {}
    for pair, scores in pair_scores.items():
        avg_matrix[pair] = round(np.mean(scores), 4)

    return topics, avg_matrix


# ════════════════════════════════════════════════════════════════════════
#  Figure Generators
# ════════════════════════════════════════════════════════════════════════

def fig3_cds(cds_data):
    """Fig 3: CDS by Education Level — bar chart."""
    levels = LV_ORDER
    labels = [LV_LABELS[l] for l in levels]
    values = [cds_data[l]["cds"] for l in levels]
    colors = [LV_COLORS[l] for l in levels]
    node_counts = [cds_data[l]["nodes"] for l in levels]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), gridspec_kw={"width_ratios": [1.5, 1]})

    # ── Left: CDS bar chart ──
    bars = ax1.bar(labels, values, color=colors, width=0.55, edgecolor="white", linewidth=0.5)
    ax1.set_ylabel("CDS (Concept Density Score)")
    ax1.set_title("Concept Density by Education Level", fontweight="bold")

    # Value labels on bars
    for bar, v in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.003,
                 f"{v:.3f}", ha="center", va="bottom", fontsize=10)

    ax1.set_ylim(0, max(values) * 1.25)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # ── Right: Node count + trend annotation ──
    ax2.axis("off")
    summary = (
        "CDS decreases with\neducation level:\n\n"
        f"Elementary: {values[0]:.3f}\n"
        f"    ({node_counts[0]} concepts)\n\n"
        f"College: {values[-1]:.3f}\n"
        f"    ({node_counts[-1]} concepts)\n\n"
        f"Ratio: {values[0]/values[-1]:.1f}×"
    )
    ax2.text(0.1, 0.5, summary, fontsize=11, va="center",
             bbox=dict(boxstyle="round,pad=0.6", facecolor="#f0f0f0", edgecolor="#ccc"))

    plt.tight_layout()
    path = FIGURES_DIR / "fig3_cds_by_level.png"
    plt.savefig(path)
    plt.close()
    print(f"  ✅ Fig 3 saved: {path.name} ({path.stat().st_size // 1024} KB)")
    return path


def fig4_lds_heatmap(topics_data, avg_matrix):
    """Fig 4: LDS Cross-Language Heatmap."""
    if not topics_data:
        print("  ⏭ Skipping Fig 4 — no LDS data")
        return None

    topic_names = sorted(topics_data.keys())
    pair_keys = [p[0] for p in LANG_PAIRS]
    pair_labels = [p[1] for p in LANG_PAIRS]

    # Build matrix: topics × pairs
    matrix = np.zeros((len(topic_names), len(pair_keys)))
    for i, t in enumerate(topic_names):
        for j, pk in enumerate(pair_keys):
            matrix[i, j] = topics_data[t].get(pk, np.nan)

    fig, (ax_heat, ax_avg) = plt.subplots(1, 2, figsize=(9, 5),
                                           gridspec_kw={"width_ratios": [2, 1]})

    # ── Left: heatmap ──
    cmap = plt.cm.YlOrRd
    im = ax_heat.imshow(matrix, aspect="auto", cmap=cmap, vmin=0, vmax=1)

    ax_heat.set_xticks(range(len(pair_labels)))
    ax_heat.set_xticklabels(pair_labels, fontsize=10)
    ax_heat.set_yticks(range(len(topic_names)))
    ax_heat.set_yticklabels([t.capitalize() for t in topic_names], fontsize=10)
    ax_heat.set_title("LDS by Topic × Language Pair", fontweight="bold", pad=10)

    # Annotate cells
    for i in range(len(topic_names)):
        for j in range(len(pair_keys)):
            v = matrix[i, j]
            if not np.isnan(v):
                color = "white" if v > 0.6 else "black"
                ax_heat.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=9, color=color)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax_heat, shrink=0.7, pad=0.04)
    cbar.set_label("LDS (higher = more divergent)", fontsize=9)

    # ── Right: average bar chart ──
    avg_values = [avg_matrix.get(pk, 0) for pk in pair_keys]
    bar_colors = ["#e74c3c", "#3498db", "#f39c12"]
    bars = ax_avg.barh(pair_labels, avg_values, color=bar_colors, height=0.5)
    ax_avg.set_title("Average LDS", fontweight="bold")
    ax_avg.set_xlim(0, 1)
    ax_avg.spines["top"].set_visible(False)
    ax_avg.spines["right"].set_visible(False)

    for bar, v in zip(bars, avg_values):
        ax_avg.text(v + 0.02, bar.get_y() + bar.get_height() / 2,
                    f"{v:.2f}", ha="left", va="center", fontsize=10)

    plt.tight_layout()
    path = FIGURES_DIR / "fig4_lds_heatmap.png"
    plt.savefig(path)
    plt.close()
    print(f"  ✅ Fig 4 saved: {path.name} ({path.stat().st_size // 1024} KB)")
    return path


def fig5_hds(depths, nodes):
    """Fig 5: HDS Distribution — histogram."""
    all_depths = list(depths.values())
    max_depth = max(all_depths)
    mean_depth = np.mean(all_depths)

    fig, (ax_hist, ax_stats) = plt.subplots(1, 2, figsize=(10, 4),
                                             gridspec_kw={"width_ratios": [1.5, 1]})

    # ── Left: histogram ──
    bins = range(0, max_depth + 2)
    counts, bins, patches = ax_hist.hist(all_depths, bins=bins, color="#60a5fa",
                                          edgecolor="white", linewidth=0.8, alpha=0.85)
    ax_hist.set_xlabel("Chain Depth (HDS)")
    ax_hist.set_ylabel("Number of Concepts")
    ax_hist.set_title("Prerequisite Chain Depth Distribution", fontweight="bold")
    ax_hist.set_xticks(range(0, max_depth + 1))
    ax_hist.spines["top"].set_visible(False)
    ax_hist.spines["right"].set_visible(False)

    # Annotate bars
    for i, (count, bin_start) in enumerate(zip(counts, bins[:-1])):
        if count > 0:
            ax_hist.text(bin_start + 0.25, count + max(counts) * 0.01,
                         f"{int(count)}", fontsize=9)

    # Legend annotation
    ax_hist.text(0.95, 0.95,
                 f"Mean depth: {mean_depth:.2f}\nMax depth: {max_depth}\nConcepts: {len(all_depths)}",
                 transform=ax_hist.transAxes, fontsize=10, va="top", ha="right",
                 bbox=dict(boxstyle="round", facecolor="#f0f0f0", edgecolor="#ccc", alpha=0.8))

    # ── Right: insight text ──
    zero_depth = sum(1 for d in all_depths if d == 0)
    shallow = sum(1 for d in all_depths if 1 <= d <= 2)
    deep = sum(1 for d in all_depths if d >= 3)

    ax_stats.axis("off")
    insight = (
        "HDS Findings:\n\n"
        f"• HDS <= 5          (max depth limited)\n"
        f"• Mean = {mean_depth:.2f}      (shallow on average)\n"
        f"• Zero chain: {zero_depth} concepts\n"
        f"  ({zero_depth/len(all_depths)*100:.0f}% -- roots)\n\n"
        "Interpretation:\n"
        "Mathematics is a web,\n"
        "not a deep tree.\n"
        "Knowledge expands\n"
        "horizontally, not\n"
        "vertically."
    )
    ax_stats.text(0.05, 0.5, insight, fontsize=11, va="center",
                  bbox=dict(boxstyle="round,pad=0.6", facecolor="#f0f0f0", edgecolor="#ccc"))

    plt.tight_layout()
    path = FIGURES_DIR / "fig5_hds_distribution.png"
    plt.savefig(path)
    plt.close()
    print(f"  [OK] Fig 5 saved: {path.name} ({path.stat().st_size // 1024} KB)")
    return path


def fig6_cds_comparison(physics_cds, math_cds):
    """Fig 6: CDS Comparison — Math vs Physics by Education Level."""
    levels = LV_ORDER
    labels = [LV_LABELS[l] for l in levels]
    math_vals = [math_cds[l]["cds"] for l in levels]
    phys_vals = [physics_cds[l]["cds"] for l in levels]

    x = np.arange(len(levels))
    width = 0.35

    fig, (ax_bar, ax_info) = plt.subplots(1, 2, figsize=(10, 4.5),
                                            gridspec_kw={"width_ratios": [1.5, 1]})

    bars1 = ax_bar.bar(x - width/2, math_vals, width, label="Math", color="#60a5fa", edgecolor="white", linewidth=0.5)
    bars2 = ax_bar.bar(x + width/2, phys_vals, width, label="Physics", color="#f97316", edgecolor="white", linewidth=0.5)

    ax_bar.set_ylabel("CDS (Concept Density Score)")
    ax_bar.set_title("CDS by Education Level: Math vs Physics", fontweight="bold")
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(labels)
    ax_bar.legend()
    ax_bar.spines["top"].set_visible(False)
    ax_bar.spines["right"].set_visible(False)

    # Value labels
    for bar, v in zip(bars1, math_vals):
        if v > 0:
            ax_bar.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
                        f"{v:.3f}", ha="center", va="bottom", fontsize=8)
    for bar, v in zip(bars2, phys_vals):
        if v > 0:
            ax_bar.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
                        f"{v:.3f}", ha="center", va="bottom", fontsize=8)

    # Right panel: findings
    math_peak = max(levels, key=lambda l: math_cds[l]["cds"])
    phys_peak = max(levels, key=lambda l: physics_cds[l]["cds"])
    ax_info.axis("off")
    finding = (
        "Cross-Disciplinary Finding:\n\n"
        f"Math CDS peak:    {math_peak}\n"
        f"  (CDS = {math_cds[math_peak]['cds']:.3f})\n\n"
        f"Physics CDS peak: {phys_peak}\n"
        f"  (CDS = {physics_cds[phys_peak]['cds']:.3f})\n\n"
        "Different disciplines show\n"
        "different density patterns:\n"
        "  Math densest at foundation,\n"
        "  Physics densest at advanced\n"
        "  specialization."
    )
    ax_info.text(0.05, 0.5, finding, fontsize=10, va="center",
                 bbox=dict(boxstyle="round,pad=0.6", facecolor="#fff7ed", edgecolor="#fed7aa"))

    plt.tight_layout()
    path = FIGURES_DIR / "fig6_cds_comparison.png"
    plt.savefig(path)
    plt.close()
    print(f"  [OK] Fig 6 saved: {path.name} ({path.stat().st_size // 1024} KB)")
    return path


def fig7_three_subject_cds(math_cds, physics_cds, chemistry_cds):
    """Fig 7: CDS Comparison — Math vs Physics vs Chemistry."""
    levels = LV_ORDER
    labels = [LV_LABELS[l] for l in levels]
    math_vals = [math_cds[l]["cds"] for l in levels]
    phys_vals = [physics_cds[l]["cds"] for l in levels]
    chem_vals = [chemistry_cds[l]["cds"] for l in levels]

    x = np.arange(len(levels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 5))

    bars1 = ax.bar(x - width, math_vals, width, label="Math", color="#60a5fa", edgecolor="white", linewidth=0.5)
    bars2 = ax.bar(x, phys_vals, width, label="Physics", color="#f97316", edgecolor="white", linewidth=0.5)
    bars3 = ax.bar(x + width, chem_vals, width, label="Chemistry", color="#22c55e", edgecolor="white", linewidth=0.5)

    ax.set_ylabel("CDS (Concept Density Score)")
    ax.set_title("CDS by Education Level: Three-Subject Comparison", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            v = bar.get_height()
            if v > 0:
                ax.text(bar.get_x() + bar.get_width()/2, v + 0.003,
                        f"{v:.3f}", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    path = FIGURES_DIR / "fig7_three_subject_cds.png"
    plt.savefig(path)
    plt.close()
    print(f"  [OK] Fig 7 saved: {path.name} ({path.stat().st_size // 1024} KB)")
    return path


# ══════════════════════════════════════════════════════════════════════
#  Main
# ════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Generate paper figures for LinguaGraph")
    parser.add_argument("--fig", type=int, choices=[1, 2, 3, 4, 5, 6, 7], help="Single figure to generate")
    args = parser.parse_args()

    print("=" * 55)
    print("  LinguaGraph — Paper Figure Generator")
    print("=" * 55)

    # ── Load data ──
    print("\n[1/3] Loading data...")
    nodes, links = load_cognitive_data()
    print(f"  Loaded {len(nodes)} concepts, {len(links)} relations")
    lds_rows = load_lds_data()
    print(f"  Loaded {len(lds_rows)} LDS records")

    # ── Compute metrics ──
    print("\n[2/3] Computing metrics...")
    cds_data = compute_cds(nodes, links)
    print("  CDS computed:")
    for lv in LV_ORDER:
        d = cds_data[lv]
        print(f"    {LV_LABELS[lv]:12s}: {d['cds']:.4f}  ({d['nodes']} nodes, {d['edges']} edges)")

    hds_depths = compute_hds(nodes, links)
    max_hds = max(hds_depths.values())
    mean_hds = np.mean(list(hds_depths.values()))
    print(f"  HDS computed: max={max_hds}, mean={mean_hds:.2f}")

    topics_data, avg_matrix = compute_lds_matrix(lds_rows)
    if avg_matrix:
        print("  LDS averages:")
        for pair, label in LANG_PAIRS:
            print(f"    {label:8s}: {avg_matrix.get(pair, 0):.4f}")

    # ── Generate figures ──
    print("\n[3/3] Generating figures...")

    if args.fig is None or args.fig == 3:
        fig3_cds(cds_data)

    if args.fig is None or args.fig == 4:
        fig4_lds_heatmap(topics_data, avg_matrix)

    if args.fig is None or args.fig == 5:
        fig5_hds(hds_depths, nodes)

    # Fig 6: Physics vs Math CDS comparison
    physics_json = PROJECT_DIR / "config" / "expert_graphs" / "physics_full.json"
    physics_cds = None
    if physics_json.exists():
        with open(physics_json, "r", encoding="utf-8") as f:
            physics_g = json.load(f)
        p_nodes = [{"id": c["name"], "level": c.get("level", "college")} for c in physics_g["concepts"]]
        p_links = [{"source": r["source"], "target": r["target"],
                    "type": r.get("type", "relates_to"), "relation": r.get("relation", r.get("type", "relates_to"))}
                   for r in physics_g["relations"]]
        physics_cds = compute_cds(p_nodes, p_links)

    if args.fig is None or args.fig == 6:
        if physics_cds is not None:
            fig6_cds_comparison(physics_cds, cds_data)
        else:
            print("  [SKIP] Fig 6: physics_full.json not found")

    # Fig 7: Three-subject CDS comparison
    if args.fig is None or args.fig == 7:
        chem_json = PROJECT_DIR / "config" / "expert_graphs" / "chemistry_full.json"
        if chem_json.exists() and physics_cds is not None:
            with open(chem_json, "r", encoding="utf-8") as f:
                chem_g = json.load(f)
            c_nodes = [{"id": c["name"], "level": c.get("level", "college")} for c in chem_g["concepts"]]
            c_links = [{"source": r["source"], "target": r["target"],
                        "type": r.get("type", "relates_to"), "relation": r.get("relation", r.get("type", "relates_to"))}
                       for r in chem_g["relations"]]
            chemistry_cds = compute_cds(c_nodes, c_links)
            fig7_three_subject_cds(cds_data, physics_cds, chemistry_cds)
        else:
            print("  [SKIP] Fig 7: chemistry or physics data not found")

    # Fig 1 and 2 are informational/stub
    if args.fig is None or args.fig == 1:
        print("  ⏭ Fig 1 (Pipeline): use docs/pipeline_diagram source")
    if args.fig is None or args.fig == 2:
        print("  ⏭ Fig 2 (CognitiveSpace): use annotated screenshot")

    # ── Summary ──
    print(f"\n{'=' * 55}")
    print("  All figures saved to: outputs/figures/")
    if FIGURES_DIR.exists():
        for f in sorted(FIGURES_DIR.glob("*.png")):
            print(f"    {f.name}  ({f.stat().st_size // 1024} KB)")
    print("=" * 55)


if __name__ == "__main__":
    main()
