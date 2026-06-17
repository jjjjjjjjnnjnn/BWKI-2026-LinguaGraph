"""
LinguaGraph Inter-Annotator Agreement Analysis
================================================
Compute Cohen's Kappa, Jaccard similarity, and conflict reports
between two independent annotators.

Usage:
    python scripts/annotator_agreement.py \
        --annotator_a data/labels/annotator_A.json \
        --annotator_b data/labels/annotator_B.json
    python scripts/annotator_agreement.py \
        --annotator_a data/labels/annotator_A.json \
        --annotator_b data/labels/annotator_B.json \
        --report

Output:
    research/findings/annotator_agreement.json
    research/findings/annotator_conflicts.md
"""

import json
import sys
import math
from pathlib import Path
from datetime import datetime
from collections import Counter

PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR))


def load_annotations(filepath):
    """Load annotation JSON file (list of annotation objects)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict):
        return [data]
    return data


def jaccard_similarity(set_a, set_b):
    """Jaccard similarity between two sets."""
    if not set_a and not set_b:
        return 1.0  # both empty → perfect agreement
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union) if union else 0.0


def cohen_kappa(annotator_a, annotator_b, all_categories):
    """
    Compute Cohen's Kappa for categorical agreement.

    κ = (p_o - p_e) / (1 - p_e)

    where p_o = observed agreement, p_e = expected agreement by chance.
    """
    n = len(annotator_a)
    # Observed agreement
    observed = sum(1 for a, b in zip(annotator_a, annotator_b) if a == b) / n if n > 0 else 0

    # Expected agreement by chance
    count_a = Counter(annotator_a)
    count_b = Counter(annotator_b)
    expected = sum((count_a.get(cat, 0) / n) * (count_b.get(cat, 0) / n) for cat in all_categories) if n > 0 else 0

    # Kappa
    if 1 - expected == 0:
        return 0.0
    kappa = (observed - expected) / (1 - expected)
    return round(kappa, 4)


def compare_annotations(ann_a, ann_b):
    """
    Compare two annotation sets. Returns detailed comparison per item.
    """
    # Index by response_id
    idx_a = {a["response_id"]: a for a in ann_a}
    idx_b = {b["response_id"]: b for b in ann_b}

    common_ids = set(idx_a.keys()) & set(idx_b.keys())
    comparisons = []

    if not common_ids:
        print("[ERROR] No common response_ids found between annotators")
        return comparisons

    for rid in sorted(common_ids):
        a = idx_a[rid]
        b = idx_b[rid]

        # Concept comparison
        concepts_a = set(a.get("concepts", []))
        concepts_b = set(b.get("concepts", []))
        concept_jaccard = jaccard_similarity(concepts_a, concepts_b)

        # Relation comparison
        rels_a = set((r["source"], r["target"], r["type"]) for r in a.get("relations", []))
        rels_b = set((r["source"], r["target"], r["type"]) for r in b.get("relations", []))
        relation_jaccard = jaccard_similarity(rels_a, rels_b)

        # Quality rating
        quality_a = a.get("quality_rating", "unknown")
        quality_b = b.get("quality_rating", "unknown")
        quality_agree = quality_a == quality_b

        comparisons.append({
            "response_id": rid,
            "concepts_a": list(concepts_a),
            "concepts_b": list(concepts_b),
            "concepts_shared": list(concepts_a & concepts_b),
            "concepts_only_a": list(concepts_a - concepts_b),
            "concepts_only_b": list(concepts_b - concepts_a),
            "concept_jaccard": round(concept_jaccard, 4),
            "relation_jaccard": round(relation_jaccard, 4),
            "quality_a": quality_a,
            "quality_b": quality_b,
            "quality_agreement": quality_agree,
        })

    return comparisons


def compute_overall_agreement(comparisons):
    """Compute overall agreement metrics from pairwise comparisons."""
    if not comparisons:
        return {}

    concept_jaccards = [c["concept_jaccard"] for c in comparisons]
    relation_jaccards = [c["relation_jaccard"] for c in comparisons]
    quality_agreements = sum(1 for c in comparisons if c["quality_agreement"])

    # Cohen's Kappa for quality ratings
    quality_a = [c["quality_a"] for c in comparisons]
    quality_b = [c["quality_b"] for c in comparisons]
    all_ratings = list(set(quality_a + quality_b))
    quality_kappa = cohen_kappa(quality_a, quality_b, all_ratings)

    return {
        "num_compared": len(comparisons),
        "mean_concept_jaccard": round(sum(concept_jaccards) / len(concept_jaccards), 4),
        "min_concept_jaccard": round(min(concept_jaccards), 4),
        "max_concept_jaccard": round(max(concept_jaccards), 4),
        "mean_relation_jaccard": round(sum(relation_jaccards) / len(relation_jaccards), 4),
        "quality_agreement_pct": round(quality_agreements / len(comparisons) * 100, 1),
        "quality_cohens_kappa": quality_kappa,
    }


def generate_conflict_report(comparisons, overall):
    """Generate markdown report of annotator conflicts."""
    md = []
    md.append("# LinguaGraph Inter-Annotator Agreement Report\n")
    md.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    md.append("---\n")

    # Overall metrics
    md.append("## Overall Agreement\n")
    md.append(f"| Metric | Value | Target | Status |\n")
    md.append(f"|--------|-------|--------|--------|\n")

    status = lambda v, t: "✅ PASS" if v >= t else "❌ FAIL"

    sj = overall.get("mean_concept_jaccard", 0)
    md.append(f"| Mean Concept Jaccard | {sj:.4f} | ≥ 0.70 | {status(sj, 0.70)} |\n")

    rj = overall.get("mean_relation_jaccard", 0)
    md.append(f"| Mean Relation Jaccard | {rj:.4f} | ≥ 0.65 | {status(rj, 0.65)} |\n")

    qk = overall.get("quality_cohens_kappa", 0)
    md.append(f"| Quality Cohen's Kappa | {qk:.4f} | ≥ 0.70 | {status(qk, 0.70)} |\n")

    md.append(f"| Samples compared | {overall.get('num_compared', 0)} | ≥ 20 | {'✅' if overall.get('num_compared', 0) >= 20 else '⚠️'} |\n")

    # Per-item breakdown
    md.append("\n## Per-Item Breakdown\n")
    md.append("| Response | Concept Jaccard | Relation Jaccard | Quality | Conflicts |\n")
    md.append("|----------|----------------|-----------------|---------|-----------|\n")

    for c in comparisons:
        conflicts = []
        if c["concepts_only_a"]:
            conflicts.append(f"A-only: {', '.join(c['concepts_only_a'][:3])}")
        if c["concepts_only_b"]:
            conflicts.append(f"B-only: {', '.join(c['concepts_only_b'][:3])}")
        conflict_str = "; ".join(conflicts) if conflicts else "-"
        quality_str = "✅" if c["quality_agreement"] else f"❌ A={c['quality_a']} B={c['quality_b']}"
        md.append(f"| {c['response_id']} | {c['concept_jaccard']:.4f} | {c['relation_jaccard']:.4f} | {quality_str} | {conflict_str} |\n")

    # Recommendations
    md.append("\n## Recommendations\n")
    if sj < 0.70:
        md.append("- ❌ Concept agreement below target (0.70). Review concept extraction rules.\n")
    if rj < 0.65:
        md.append("- ❌ Relation agreement below target (0.65). Review relation type definitions.\n")
    if qk < 0.70:
        md.append("- ❌ Quality rating agreement below target. Clarify rich/moderate/thin/empty criteria.\n")

    if sj >= 0.70 and rj >= 0.65 and qk >= 0.70:
        md.append("- ✅ All targets met. Annotations are reliable.\n")

    # Save
    outdir = PROJECT_DIR / "research" / "findings"
    outdir.mkdir(parents=True, exist_ok=True)

    report_path = outdir / "annotator_conflicts.md"
    report_path.write_text("\n".join(md), encoding="utf-8")
    print(f"[OK] Report saved to {report_path}")

    return md


def main():
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph Inter-Annotator Agreement Analysis")
    parser.add_argument("--annotator_a", type=str, required=True, help="Annotator A JSON file")
    parser.add_argument("--annotator_b", type=str, required=True, help="Annotator B JSON file")
    parser.add_argument("--report", action="store_true", help="Generate conflict report")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  Inter-Annotator Agreement Analysis")
    print(f"{'='*50}")

    # Load
    ann_a = load_annotations(args.annotator_a)
    ann_b = load_annotations(args.annotator_b)
    print(f"\n  Annotator A: {len(ann_a)} annotations")
    print(f"  Annotator B: {len(ann_b)} annotations")

    # Compare
    comparisons = compare_annotations(ann_a, ann_b)
    if not comparisons:
        print("[ERROR] No matching annotations to compare")
        return

    print(f"  Common responses: {len(comparisons)}")

    # Compute
    overall = compute_overall_agreement(comparisons)
    print(f"\n  Concept Jaccard:  {overall['mean_concept_jaccard']:.4f}  (target ≥ 0.70)")
    print(f"  Relation Jaccard: {overall['mean_relation_jaccard']:.4f}  (target ≥ 0.65)")
    print(f"  Quality Kappa:    {overall['quality_cohens_kappa']:.4f}  (target ≥ 0.70)")

    # Save results
    outdir = PROJECT_DIR / "research" / "findings"
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / "annotator_agreement.json"
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump({"overall": overall, "comparisons": comparisons}, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] Saved to {outpath}")

    # Report
    if args.report:
        generate_conflict_report(comparisons, overall)

    print(f"\n[DONE]\n")


if __name__ == "__main__":
    main()
