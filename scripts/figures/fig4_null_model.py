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

import argparse
import csv, json, random, statistics, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

from _lds_utils import (
    lds_jaccard,
    load_aligned,
    get_lang_graphs,
    degree_preserving_rewire,
    RANDOM_SEED,
)
import _lds_utils as _lds_utils_mod

DEFAULT_SEEDS = "42,999,2026,7,1234"


def parse_seeds(s: str) -> list[int]:
    return [int(x.strip()) for x in s.split(",") if x.strip()]


# ── Null model conditions ──

def condition_full(lang_nodes, lang_edges) -> dict:
    """Baseline: real LDS from aligned data."""
    results = {}
    for pair_name, (la, lb) in [("ZH-EN", ("zh", "en")), ("DE-EN", ("de", "en")), ("ZH-DE", ("zh", "de"))]:
        lds = lds_jaccard(lang_nodes[la], lang_nodes[lb], list(lang_edges[la]), list(lang_edges[lb]))
        results[pair_name] = lds["lds_score"]
    return results


def condition_structure_null(lang_nodes, lang_edges, seed: int = RANDOM_SEED) -> dict:
    """Structure null: degree-preserving rewiring.

    H0: LDS is entirely explained by degree distribution.
    If true, rewired graphs should have the same LDS as real graphs.
    seed: degree_preserving_rewire() pins random.seed(RANDOM_SEED) internally,
    so we temporarily override _lds_utils.RANDOM_SEED per multi-seed iteration.
    B6-class fix: edge lists are sorted by repr before rewiring because
    list(set) order is PYTHONHASHSEED-dependent and the double-edge-swap
    outcome is order-sensitive (same seed=42 gave ZH-DE 0.7177 vs 0.7166
    under PYTHONHASHSEED=1 vs 2). sorted() makes the point value hash-stable;
    residual seed-to-seed spread is reported via --seeds mean±SD rows.
    """
    prev = _lds_utils_mod.RANDOM_SEED
    _lds_utils_mod.RANDOM_SEED = seed
    try:
        rewired: dict[str, list] = {}
        for lang in ["zh", "en", "de"]:
            rewired[lang] = degree_preserving_rewire(sorted(list(lang_edges[lang]), key=repr))
    finally:
        _lds_utils_mod.RANDOM_SEED = prev

    results = {}
    for pair_name, (la, lb) in [("ZH-EN", ("zh", "en")), ("DE-EN", ("de", "en")), ("ZH-DE", ("zh", "de"))]:
        lds = lds_jaccard(lang_nodes[la], lang_nodes[lb], rewired[la], rewired[lb])
        results[pair_name] = lds["lds_score"]
    return results


def condition_node_permuted(lang_nodes, lang_edges, seed: int = RANDOM_SEED) -> dict:
    """Node-permuted null: shuffle node labels within each language.

    H0: specific label-to-concept assignments carry no language signal.
    If true, permuted labels yield same LDS as real labels.
    """
    random.seed(seed)
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


def condition_random_graph(lang_nodes, lang_edges, seed: int = RANDOM_SEED) -> dict:
    """Complete random: Erdős–Rényi with same N, E per language.

    H0: any graph with these node/edge counts produces same LDS.
    If true, real LDS is meaningless.
    """
    random.seed(seed)
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


# ═══════════════════════════════════════════════════════════
# ADVERSARIAL NULL MODELS (added per reviewer feedback)
# ═══════════════════════════════════════════════════════════

def condition_within_language(lang_nodes, lang_edges, seed: int = RANDOM_SEED) -> dict:
    """ADVERSARIAL: Within-language baseline.

    Split ONE language's graph into two random halves and compute LDS
    between them. If cross-language LDS ≈ within-language LDS, then
    LDS measures sampling variability, not language divergence.

    H0 (threatening): cross-language LDS <= within-language LDS
    → language effect indistinguishable from same-language noise.

    Report: LDS(ZH_splitA, ZH_splitB), LDS(EN_splitA, EN_splitB),
    LDS(DE_splitA, DE_splitB) — then show cross-language vs within
    in the interpretation.

    NOTE (B5): single deterministic split-half per seed; multi-seed
    distribution is obtained by looping this function over --seeds
    (see main()); do NOT treat one split as a CI.
    """
    random.seed(seed)
    results = {}
    for lang in ["zh", "en", "de"]:
        nodes = list(lang_nodes[lang])
        edges = list(lang_edges[lang])
        random.shuffle(nodes)
        random.shuffle(edges)
        # Split into halves
        mid_n = max(1, len(nodes) // 2)
        mid_e = max(1, len(edges) // 2)
        a_nodes, b_nodes = nodes[:mid_n], nodes[mid_n:]
        a_edges, b_edges = edges[:mid_e], edges[mid_e:]
        lds = lds_jaccard(a_nodes, b_nodes, a_edges, b_edges)
        results[lang.upper()] = lds["lds_score"]
    return results


def condition_cross_discipline(lang_nodes: dict, lang_edges: dict,
                               discipline_nodes: dict | None = None,
                               discipline_edges: dict | None = None,
                               seed: int = RANDOM_SEED) -> dict:
    """ADVERSARIAL: Cross-discipline LDS within the same language.

    Compute LDS between Math and Physics FOR THE SAME LANGUAGE.
    If LDS(math_zh, physics_zh) ≈ LDS(math_zh, math_en), then
    LDS measures domain differences, not language differences.

    This is genuinely threatening: if within-language-cross-discipline LDS
    is as high as cross-language-same-discipline LDS, then language
    contributes little to structural divergence.

    H0 (threatening): LDS(same_lang, diff_discipline) ≥ LDS(diff_lang, same_discipline)
    """
    results = {}
    # If no discipline data provided, use the textbook graphs as pseudo cross-discipline
    # (same language, different subject matter within mathematics)
    for lang_code, lang_name in [("zh", "ZH"), ("en", "EN"), ("de", "DE")]:
        nodes = list(lang_nodes[lang_code])
        edges = list(lang_edges[lang_code])
        # Split nodes into two random subsets to simulate different "disciplines"
        # within the same language
        random.seed(seed)
        shuffled_nodes = list(nodes)
        random.shuffle(shuffled_nodes)
        mid = max(1, len(shuffled_nodes) // 2)
        disc_a_nodes = shuffled_nodes[:mid]
        disc_b_nodes = shuffled_nodes[mid:]

        # Split edges by which nodes they connect
        disc_a_nodes_set = set(disc_a_nodes)
        disc_a_edges = [e for e in edges if e[0] in disc_a_nodes_set or e[1] in disc_a_nodes_set]
        disc_b_edges = [e for e in edges if e[0] not in disc_a_nodes_set or e[1] not in disc_a_nodes_set]
        if not disc_b_edges:
            disc_b_edges = disc_a_edges[:max(1, len(disc_a_edges)//2)]
            disc_a_edges = disc_a_edges[:max(1, len(disc_a_edges)//2)]

        lds = lds_jaccard(disc_a_nodes, disc_b_nodes, disc_a_edges, disc_b_edges)
        results[f"Within-{lang_name}"] = lds["lds_score"]
    return results


def condition_language_label_permutation(lang_nodes, lang_edges, aligned, seed: int = RANDOM_SEED + 999) -> dict:
    """ADVERSARIAL: Language-label permutation at group level.

    For each aligned concept group, randomly reassign which label
    counts as "ZH", "EN", or "DE". This preserves:
    - The graph topology (same edges)
    - The set of all labels (same vocabulary)
    - But destroys: which SPECIFIC language each label belongs to

    H0 (threatening): Permuted labels produce the same LDS as real labels.
    → LDS measures structural properties of the GROUPS, not language.
    """
    random.seed(seed)
    groups = aligned.get("aligned_groups", [])
    gid_to_labels: dict[str, dict] = {g["id"]: g.get("labels", {}) for g in groups}

    # Collect all label triples
    triples = []
    for g in groups:
        labels = g.get("labels", {})
        zh = labels.get("zh", "")
        en = labels.get("en", "")
        de = labels.get("de", "")
        if zh or en or de:
            triples.append({"zh": zh, "en": en, "de": de})

    # Permute: within each triple, randomly reassign languages
    permuted_nodes: dict[str, list] = {"zh": [], "en": [], "de": []}
    for t in triples:
        langs = ["zh", "en", "de"]
        random.shuffle(langs)
        permuted_nodes[langs[0]].append(t.get("zh", "") or t.get("en", "") or t.get("de", ""))
        permuted_nodes[langs[1]].append(t.get("en", "") or t.get("zh", "") or t.get("de", ""))
        permuted_nodes[langs[2]].append(t.get("de", "") or t.get("zh", "") or t.get("en", ""))

    # Keep edges the same (they reference group IDs, not labels)
    lang_edges_permuted = lang_edges

    results = {}
    for pair_name, (la, lb) in [("ZH-EN", ("zh", "en")), ("DE-EN", ("de", "en")), ("ZH-DE", ("zh", "de"))]:
        lds = lds_jaccard(permuted_nodes[la], permuted_nodes[lb],
                          list(lang_edges_permuted[la]), list(lang_edges_permuted[lb]))
        results[pair_name] = lds["lds_score"]
    return results


def condition_monolingual_control(lang_nodes, lang_edges, seed: int = RANDOM_SEED) -> dict:
    """ADVERSARIAL: Monolingual textbook-pair control.

    LDS(ZH_textbook_1, ZH_textbook_2) — two different textbooks
    in the same language covering the same domain. This measures
    the "same language, same knowledge" baseline.

    If cross-language LDS ≈ monolingual LDS, then cross-language
    differences are no larger than within-language-publisher variation.
    This would be genuinely damaging to the language-divergence claim.

    Since we only have one combined graph per language, we simulate:
    random split → treat each half as a separate "textbook".
    """
    random.seed(seed)
    results = {}
    for lang in ["zh", "en", "de"]:
        nodes = list(lang_nodes[lang])
        edges = list(lang_edges[lang])
        random.shuffle(nodes)
        random.shuffle(edges)
        mid_n = max(1, len(nodes) // 2)
        mid_e = max(1, len(edges) // 2)
        t1_nodes, t2_nodes = nodes[:mid_n], nodes[mid_n:]
        t1_edges, t2_edges = edges[:mid_e], edges[mid_e:]
        lds = lds_jaccard(t1_nodes, t2_nodes, t1_edges, t2_edges)
        pair_label = f"{lang.upper()}-{lang.upper()}"
        results[pair_label] = lds["lds_score"]
    return results


# ── Plotting ──

PAIRS = ["ZH-EN", "DE-EN", "ZH-DE"]
CONDITION_CONFIG = [
    ("Full (baseline)", "#2563eb", "Real aligned data"),
    ("Structure Null\n(deg.-preserving)", "#ea580c", "Degree-preserving rewired"),
    ("Node-Permuted Null", "#16a34a", "Shuffled node labels"),
    ("Complete Random", "#6b7280", "Erdos–Renyi"),
    # ═══ Adversarial conditions (new) ═══
    ("Within-Lang\n(same split)", "#7c3aed", "Within-language split-half"),
    ("Label Permute\n(group-level)", "#db2777", "Permuted language labels"),
    ("Mono Control\n(same lang)", "#0891b2", "Within-language baseline"),
]


def plot_results(conditions: dict[str, dict], adversarial: dict[str, dict] | None = None):
    x = np.arange(len(PAIRS))
    width = 0.12

    fig, ax = plt.subplots(figsize=(12, 5.5))

    # Standard conditions
    std_names = [c[0] for c in CONDITION_CONFIG[:4]]
    for i, (name, color, desc) in enumerate(CONDITION_CONFIG[:4]):
        vals = [conditions.get(name, {}).get(p, 0) for p in PAIRS]
        offset = (i - 1.5) * width
        bars = ax.bar(x + offset, vals, width, label=f"{name}", color=color, alpha=0.85, edgecolor="white", linewidth=0.5)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.015,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=6, rotation=45)

    # Adversarial conditions
    adv_start = 0.5  # offset to the right
    adv_colors = ["#7c3aed", "#db2777", "#0891b2"]
    for j, (name, _, _) in enumerate([c for c in CONDITION_CONFIG if c[0] not in std_names]):
        vals = [adversarial.get(name, {}).get(p, 0) if adversarial else 0 for p in PAIRS]
        # For conditions that don't have ZH-EN/DE-EN/ZH-DE keys, use next-best mapping
        if not any(vals):
            if name == "Within-Lang\n(same split)":
                vals = [adversarial.get("ZH", adversarial.get("Within-Lang", {})).get("ZH", 0) if adversarial else 0 for _ in PAIRS]
            # Try to display as single value across all pairs
            all_vals = list(adversarial.get(name, {}).values()) if adversarial else []
            if all_vals:
                avg = sum(all_vals) / len(all_vals)
                ax.axhline(y=avg, color=adv_colors[j], linestyle="--", linewidth=1.5, alpha=0.7, xmin=0.05, xmax=0.95)
                ax.text(x[-1] + 0.4, avg + 0.01, f"{name}\n{avg:.3f}", fontsize=7, color=adv_colors[j], va="bottom")

    ax.set_xlabel("Language Pair", fontsize=11)
    ax.set_ylabel("LDS", fontsize=11)
    ax.set_title("LDS Null Model Suite: Standard + Adversarial Conditions", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(PAIRS, fontsize=10)
    ax.legend(fontsize=7, loc="upper right", ncol=2)
    ax.set_ylim(0, 1.15)

    # Annotation box
    ax.text(0.98, 0.98,
            "Standard (bars): test specific structural explanations\n"
            "Adversarial (lines): could falsify language claim\n"
            "If cross-lang LDS ≈ within-lang LDS → language effect is noise",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=7, color="#555",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f8f9fa", edgecolor="#ddd"))

    plt.tight_layout()
    path = OUTPUT_DIR / "fig4_null_model.png"
    fig.savefig(path, dpi=300)
    print(f"  [OK] {path}")
    plt.close(fig)


# ── Main ──

def _mean_sd_rows(runs: list[dict], keys: list[str]) -> tuple[dict, dict]:
    """Per-key mean and SD across multi-seed runs (B1/B2/B5)."""
    mean: dict = {}
    sd: dict = {}
    for k in keys:
        vals = [r[k] for r in runs if k in r and r[k] == r[k]]
        if vals:
            mean[k] = round(statistics.mean(vals), 4)
            sd[k] = round(statistics.stdev(vals), 4) if len(vals) > 1 else 0.0
    return mean, sd


def _adv_cell(row: dict, pair: str, cond_name: str) -> object:
    """B5 fix: key mapping for adversarial rows.

    Within-Lang keys are ZH/EN/DE (legacy mapping kept for compat:
    ZH-EN<-ZH, DE-EN<-DE, ZH-DE<-EN).
    Mono Control keys are ZH-ZH/EN-EN/DE-DE (previously unmapped → empty
    columns); fixed mapping is positional: ZH-EN<-ZH-ZH, DE-EN<-EN-EN,
    ZH-DE<-DE-DE.
    """
    if "Mono Control" in cond_name:
        mono_map = {"ZH-EN": "ZH-ZH", "DE-EN": "EN-EN", "ZH-DE": "DE-DE"}
        v = row.get(mono_map[pair], "")
        if v == "":
            # fallback: positional zh/en/de order
            fall = {"ZH-EN": "ZH", "DE-EN": "EN", "ZH-DE": "DE"}
            v = row.get(fall[pair], "")
        return v
    return row.get(pair, row.get({"ZH-EN": "ZH", "DE-EN": "DE", "ZH-DE": "EN"}[pair], ""))


def main(argv: list[str] | None = None):
    ap = argparse.ArgumentParser(description="Fig 4 null-model suite (B1/B2/B5: --seeds multi-seed)")
    ap.add_argument("--seeds", type=str, default=DEFAULT_SEEDS,
                    help=f"comma-separated seeds for null distributions (default {DEFAULT_SEEDS})")
    args = ap.parse_args(argv)
    seeds = parse_seeds(args.seeds)
    print("Fig 4: Null Model Suite")
    print(f"  seeds: {seeds}")
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

    # ═══ Adversarial conditions ═══
    adv_funcs: list[tuple[str, callable, dict | None]] = [
        ("Within-Lang\n(same split)", condition_within_language, None),
        ("Label Permute\n(group-level)", lambda ln, le, seed=RANDOM_SEED + 999: condition_language_label_permutation(ln, le, aligned, seed=seed), None),
        ("Mono Control\n(same lang)", condition_monolingual_control, None),
    ]

    results: dict[str, dict] = {}
    for name, func in funcs:
        print(f"  {name}...")
        if "Structure Null" in name:
            results[name] = func(lang_nodes, lang_edges, seed=RANDOM_SEED)
        else:
            results[name] = func(lang_nodes, lang_edges)

    adversarial: dict[str, dict] = {}
    for name, func, _ in adv_funcs:
        print(f"  [ADV] {name}...")
        try:
            adversarial[name] = func(lang_nodes, lang_edges)
        except Exception as e:
            print(f"    [SKIP] {e}")
            adversarial[name] = {}

    # ═══ B1/B2/B5: multi-seed distributions (legacy single-seed rows above untouched) ═══
    print(f"  [MULTI-SEED] structure-null × {len(seeds)} seeds ...")
    struct_runs = [condition_structure_null(lang_nodes, lang_edges, seed=s) for s in seeds]
    struct_mean, struct_sd = _mean_sd_rows(struct_runs, PAIRS)
    print(f"  [MULTI-SEED] label-permute × {len(seeds)} seeds ...")
    perm_runs = [condition_language_label_permutation(lang_nodes, lang_edges, aligned, seed=s) for s in seeds]
    perm_mean, perm_sd = _mean_sd_rows(perm_runs, PAIRS)
    # B5: within-lang split-half is one deterministic split per seed → same --seeds loop
    print(f"  [MULTI-SEED] within-lang split-half × {len(seeds)} seeds ...")
    within_runs = [condition_within_language(lang_nodes, lang_edges, seed=s) for s in seeds]
    within_mean, within_sd = _mean_sd_rows(within_runs, ["ZH", "EN", "DE"])
    print(f"  [MULTI-SEED] mono control × {len(seeds)} seeds ...")
    mono_runs = [condition_monolingual_control(lang_nodes, lang_edges, seed=s) for s in seeds]
    mono_mean, mono_sd = _mean_sd_rows(mono_runs, ["ZH-ZH", "EN-EN", "DE-DE"])
    print(f"    struct mean={struct_mean} sd={struct_sd}")
    print(f"    perm   mean={perm_mean} sd={perm_sd}")
    print(f"    within mean={within_mean} sd={within_sd}")
    print(f"    mono   mean={mono_mean} sd={mono_sd}")

    plot_results(results, adversarial)

    # CSV — standard conditions (legacy single-seed rows first, untouched for old asserts)
    csv_path = OUTPUT_DIR / "fig4_null_model_data.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["condition", "type", "ZH-EN", "DE-EN", "ZH-DE", "notes"])
        for name, _ in funcs:
            w.writerow([name.replace("\n", " "), "standard",
                       results[name].get("ZH-EN", ""),
                       results[name].get("DE-EN", ""),
                       results[name].get("ZH-DE", ""), ""])
        for name, _, _ in adv_funcs:
            row = adversarial.get(name, {})
            disp = name.replace("\n", " ")
            w.writerow([disp, "adversarial",
                       _adv_cell(row, "ZH-EN", disp),
                       _adv_cell(row, "DE-EN", disp),
                       _adv_cell(row, "ZH-DE", disp),
                       "adversarial null — tests threaten language claim"])
        # B1/B2/B5: appended multi-seed mean±SD rows (new; legacy rows above unchanged)
        seed_tag = f"n={len(seeds)}, seeds={','.join(map(str, seeds))}"
        w.writerow(["Structure Null (5-seed mean±SD)", "standard-multiseed",
                    struct_mean.get("ZH-EN", ""), struct_mean.get("DE-EN", ""),
                    struct_mean.get("ZH-DE", ""),
                    f"mean±SD over {seed_tag}; SD ZH-EN={struct_sd.get('ZH-EN','')} "
                    f"DE-EN={struct_sd.get('DE-EN','')} ZH-DE={struct_sd.get('ZH-DE','')}"])
        w.writerow(["Label Permute (5-seed mean±SD)", "adversarial-multiseed",
                    perm_mean.get("ZH-EN", ""), perm_mean.get("DE-EN", ""),
                    perm_mean.get("ZH-DE", ""),
                    f"mean±SD over {seed_tag}; SD ZH-EN={perm_sd.get('ZH-EN','')} "
                    f"DE-EN={perm_sd.get('DE-EN','')} ZH-DE={perm_sd.get('ZH-DE','')}"])
        w.writerow(["Within-Lang (5-seed mean±SD)", "adversarial-multiseed",
                    within_mean.get("ZH", ""), within_mean.get("DE", ""),
                    within_mean.get("EN", ""),
                    f"mean±SD over {seed_tag} (cols map ZH-EN<-ZH, DE-EN<-DE, ZH-DE<-EN); "
                    f"SD ZH={within_sd.get('ZH','')} DE={within_sd.get('DE','')} EN={within_sd.get('EN','')}"])
        w.writerow(["Mono Control (5-seed mean±SD)", "adversarial-multiseed",
                    mono_mean.get("ZH-ZH", ""), mono_mean.get("EN-EN", ""),
                    mono_mean.get("DE-DE", ""),
                    f"mean±SD over {seed_tag} (cols map ZH-EN<-ZH-ZH, DE-EN<-EN-EN, ZH-DE<-DE-DE; B5 fix); "
                    f"SD ZH-ZH={mono_sd.get('ZH-ZH','')} EN-EN={mono_sd.get('EN-EN','')} DE-DE={mono_sd.get('DE-DE','')}"])
    print(f"  [OK] {csv_path}")

    print("\n  Standard Results:")
    for name, _ in funcs:
        vals = " | ".join(f"{results[name].get(p, 0):.4f}" for p in PAIRS)
        print(f"    {name:30s}: {vals}")

    print("\n  Adversarial Results:")
    for name, _, _ in adv_funcs:
        row = adversarial.get(name, {})
        vals = " | ".join(f"{k}: {v:.4f}" for k, v in row.items())
        print(f"    {name:30s}: {vals}")

    # Scientific interpretation
    full = results.get("Full (baseline)", {})
    struct_null = results.get("Structure Null\n(deg.-preserving)", {})
    print("\n  Interpretation (Standard):")
    for p in PAIRS:
        delta = full.get(p, 0) - struct_null.get(p, 0)
        tag = "LDS > null → language signal" if delta > 0.02 else (
              "LDS ≈ null → structure dominates" if abs(delta) <= 0.02 else
              "LDS < null (convergence)")
        print(f"    {p}: full={full.get(p, 0):.4f} - null={struct_null.get(p, 0):.4f} = {delta:+.4f}  [{tag}]")

    print("\n  Interpretation (Adversarial):")
    for name, _, _ in adv_funcs:
        row = adversarial.get(name, {})
        for k, v in row.items():
            print(f"    {name} [{k}]: LDS = {v:.4f}")


if __name__ == "__main__":
    main()
