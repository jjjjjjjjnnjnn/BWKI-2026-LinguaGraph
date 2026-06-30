#!/usr/bin/env python3
"""
Cross-Source Null Model: Discipline-Language Interaction

Tests whether LDS is driven by discipline or language:
  - LDS(math_ZH, math_EN) — cross-language, same discipline (reference)
  - LDS(math_ZH, physics_ZH) — same language, cross-discipline
  - LDS(math_ZH, physics_EN) — cross-language, cross-discipline

If same-language cross-discipline LDS ≈ cross-language same-discipline LDS,
then LDS measures domain structure, not language divergence.
This would be a genuine falsification of the language-divergence claim.

Usage:
    python scripts/figures/fig_cross_source_null.py
"""

import json, sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "figures"))
from fig4_null_model import lds_jaccard


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def get_concept_ids(data):
    """Extract concept labels from aligned data."""
    groups = data.get("aligned_groups", [])
    langs = {"zh": [], "en": [], "de": []}
    for g in groups:
        labels = g.get("labels", {})
        for lang in langs:
            if labels.get(lang):
                langs[lang].append(labels[lang])
    return langs


def get_edges(data):
    """Extract edge lists per language."""
    groups = data.get("aligned_groups", [])
    gid_to_labels = {g["id"]: g.get("labels", {}) for g in groups}
    edges = {"zh": set(), "en": set(), "de": set()}
    for r in data.get("relations", []):
        sg = r.get("source_group") or r.get("source", "")
        tg = r.get("target_group") or r.get("target", "")
        if sg in gid_to_labels and tg in gid_to_labels:
            for lang in ["zh", "en", "de"]:
                s = gid_to_labels[sg].get(lang)
                t = gid_to_labels[tg].get(lang)
                if s and t:
                    edges[lang].add((s, t))
    return edges


def main():
    print("=" * 60)
    print("Cross-Source Null Model: Discipline × Language Interaction")
    print("=" * 60)

    # Load math data
    math_path = PROJECT_ROOT / "data" / "math_extractions" / "merged" / "aligned_data.json"
    math_data = load_json(math_path)
    math_nodes = get_concept_ids(math_data)
    math_edges = get_edges(math_data)

    # Load physics data
    physics_path = PROJECT_ROOT / "config" / "expert_graphs" / "physics_full.json"
    if not physics_path.exists():
        print("[WARN] physics_full.json not found. Checking alternative paths...")
        alt = PROJECT_ROOT / "config" / "expert_graphs"
        for f in sorted(alt.glob("physics*.json")):
            print(f"  Found: {f.name}")
        sys.exit(0)

    physics_raw = load_json(physics_path)
    # Physics data format: concepts[] with labels dict
    physics_nodes = {"zh": set(), "en": set(), "de": set()}
    physics_edges = {"zh": set(), "en": set(), "de": set()}

    # Concepts from physics_full.json
    for item in physics_raw.get("concepts", []):
        labels = item.get("labels", {})
        for lang in ["zh", "en", "de"]:
            if labels.get(lang):
                physics_nodes[lang].add(labels[lang])

    # Relations from physics_full.json
    # Build group ID to label mapping for physics
    phy_id_to_labels = {}
    for item in physics_raw.get("concepts", []):
        name = item.get("name", "")
        labels = item.get("labels", {})
        if name:
            phy_id_to_labels[name] = labels

    for rel in physics_raw.get("relations", []):
        src = rel.get("source", "")
        tgt = rel.get("target", "")
        if src in phy_id_to_labels and tgt in phy_id_to_labels:
            for lang in ["zh", "en", "de"]:
                s = phy_id_to_labels[src].get(lang)
                t = phy_id_to_labels[tgt].get(lang)
                if s and t:
                    physics_edges[lang].add((s, t))

    # Print sizes
    print("\n  Dataset sizes:")
    for lang in ["zh", "en", "de"]:
        print(f"    {lang}: Math({len(math_nodes[lang])} nodes, {len(math_edges[lang])} edges) "
              f"Physics({len(physics_nodes[lang])} nodes, {len(physics_edges[lang])} edges)")

    # ═══════════════════════════════════════════════
    # Condition 1: Cross-language, same discipline (reference)
    # ═══════════════════════════════════════════════
    print("\n\n  ── Cross-Language, Same Discipline (Reference) ──")
    ref_results = {}
    for pair_name, (la, lb) in [("ZH-EN Math", ("zh", "en")), ("DE-EN Math", ("de", "en")), ("ZH-DE Math", ("zh", "de"))]:
        if len(math_nodes[la]) > 5 and len(math_nodes[lb]) > 5:
            lds = lds_jaccard(list(math_nodes[la]), list(math_nodes[lb]),
                              list(math_edges[la]), list(math_edges[lb]))
            ref_results[pair_name] = lds["lds_score"]
            print(f"    {pair_name:20s}: LDS = {lds['lds_score']:.4f}")

    # ═══════════════════════════════════════════════
    # Condition 2: Same language, cross-discipline
    # ═══════════════════════════════════════════════
    print("\n\n  ── Same Language, Cross-Discipline (ADVERSARIAL) ──")
    cross_disc_results = {}
    for lang_name, lang_code in [("ZH", "zh"), ("EN", "en"), ("DE", "de")]:
        mn = list(math_nodes[lang_code])
        pn = list(physics_nodes[lang_code])
        me = list(math_edges[lang_code])
        pe = list(physics_edges[lang_code])
        if len(mn) > 5 and len(pn) > 5:
            lds = lds_jaccard(mn, pn, me, pe)
            cross_disc_results[f"Math-{lang_name} vs Physics-{lang_name}"] = lds["lds_score"]
            print(f"    Math-{lang_name} vs Physics-{lang_name}: LDS = {lds['lds_score']:.4f}")

    # ═══════════════════════════════════════════════
    # Interpretation
    # ═══════════════════════════════════════════════
    print("\n\n  ── Interpretation ──")
    print("""
    If same-language cross-discipline LDS ≈ cross-language same-discipline LDS,
    → LDS measures domain structure, not language divergence
    → LANGUAGE DIVERGENCE CLAIM FALSIFIED

    If same-language cross-discipline LDS << cross-language same-discipline LDS,
    → Language contributes more to structural divergence than discipline
    → Language divergence claim supported
    """)

    for pair, val in cross_disc_results.items():
        for ref_pair, ref_val in ref_results.items():
            ratio = val / max(ref_val, 0.001)
            print(f"    {pair:40s} LDS={val:.4f} vs {ref_pair:20s} LDS={ref_val:.4f}  (ratio={ratio:.2f})")
            if ratio >= 0.9:
                print(f"      → WARNING: Domain effect ≈ Language effect. Divergence claim challenged.")
            elif ratio >= 0.7:
                print(f"      → Domain effect is substantial. Interpret with caution.")
            else:
                print(f"      → Language effect dominates domain effect. Good.")


if __name__ == "__main__":
    main()
