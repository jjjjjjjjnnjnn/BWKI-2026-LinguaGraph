"""
MCL Analysis Scripts

Batch analysis tools for evaluating LLM extraction vs human annotation.
Run after collecting student data to produce research evidence.
"""

import json
import sys
from pathlib import Path
from collections import Counter

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def load_gold_dataset(path=None):
    """Load the gold dataset (human annotations)."""
    if path is None:
        path = Path(__file__).parent.parent / "data" / "gold" / "gold_dataset.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_extraction_results(path=None):
    """Load LLM extraction results."""
    if path is None:
        path = Path(__file__).parent.parent / "output" / "extraction_results.json"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def calculate_concept_metrics(gold, extracted):
    """
    Calculate concept-level Precision, Recall, F1.

    Args:
        gold: set of human-annotated concepts
        extracted: set of LLM-extracted concepts

    Returns:
        dict with precision, recall, f1
    """
    tp = len(gold & extracted)
    fp = len(extracted - gold)
    fn = len(gold - extracted)

    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-6)

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "tp": tp, "fp": fp, "fn": fn
    }


def calculate_relation_metrics(gold_relations, extracted_relations):
    """
    Calculate relation-level Precision, Recall, F1.

    Relations are compared by (from, to) pairs.
    Handles both {from, to} and {source, target} formats.
    """
    def normalize_rel(r):
        src = r.get("from") or r.get("source", "")
        tgt = r.get("to") or r.get("target", "")
        return (src, tgt)

    gold_pairs = {normalize_rel(r) for r in gold_relations}
    extracted_pairs = {normalize_rel(r) for r in extracted_relations}

    tp = len(gold_pairs & extracted_pairs)
    fp = len(extracted_pairs - gold_pairs)
    fn = len(gold_pairs - extracted_pairs)

    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-6)

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "tp": tp, "fp": fp, "fn": fn
    }


def calculate_mcl_metrics(gold_mcl, detected_mcl):
    """
    Calculate MCL detection Precision, Recall, F1.

    MCL is compared by (from, to) pairs.
    """
    def normalize_mcl(m):
        src = m.get("from") or m.get("source", "")
        tgt = m.get("to") or m.get("target", "")
        return (src, tgt)

    gold_pairs = {normalize_mcl(m) for m in gold_mcl}
    detected_pairs = {normalize_mcl(m) for m in detected_mcl}

    tp = len(gold_pairs & detected_pairs)
    fp = len(detected_pairs - gold_pairs)
    fn = len(gold_pairs - detected_pairs)

    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-6)

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "tp": tp, "fp": fp, "fn": fn
    }


def analyze_by_language(gold_data, results_map):
    """Analyze metrics broken down by language."""
    by_lang = {}

    for sample in gold_data:
        lang = sample["language"]
        if lang not in by_lang:
            by_lang[lang] = {"concepts": [], "relations": [], "mcl": []}

        sid = sample["sample_id"]
        if sid in results_map:
            result = results_map[sid]

            # Concept metrics
            gold_concepts = set(sample["human_labels"]["concepts"])
            extracted_concepts = set(result.get("concepts", []))
            by_lang[lang]["concepts"].append(
                calculate_concept_metrics(gold_concepts, extracted_concepts)
            )

            # Relation metrics
            gold_relations = sample["human_labels"].get("relations", [])
            extracted_relations = result.get("relations", [])
            by_lang[lang]["relations"].append(
                calculate_relation_metrics(gold_relations, extracted_relations)
            )

    # Average by language
    summary = {}
    for lang, metrics in by_lang.items():
        summary[lang] = {}
        for metric_type in ["concepts", "relations"]:
            if metrics[metric_type]:
                avg = {
                    k: round(sum(m[k] for m in metrics[metric_type]) / len(metrics[metric_type]), 4)
                    for k in ["precision", "recall", "f1"]
                }
                summary[lang][metric_type] = avg

    return summary


def print_report(gold_data, results_map):
    """Print a comprehensive analysis report."""
    print("=" * 60)
    print("CognitiveSpace — MCL Analysis Report")
    print("=" * 60)

    # Overall metrics
    all_concept_metrics = []
    all_relation_metrics = []

    for sample in gold_data:
        sid = sample["sample_id"]
        if sid not in results_map:
            continue

        result = results_map[sid]
        gold_concepts = set(sample["human_labels"]["concepts"])
        extracted_concepts = set(result.get("concepts", []))
        all_concept_metrics.append(calculate_concept_metrics(gold_concepts, extracted_concepts))

        gold_relations = sample["human_labels"].get("relations", [])
        extracted_relations = result.get("relations", [])
        all_relation_metrics.append(calculate_relation_metrics(gold_relations, extracted_relations))

    # Average overall
    if all_concept_metrics:
        avg_concept = {
            k: round(sum(m[k] for m in all_concept_metrics) / len(all_concept_metrics), 4)
            for k in ["precision", "recall", "f1"]
        }
        print(f"\nOverall Concept Extraction:")
        print(f"  Precision: {avg_concept['precision']:.2%}")
        print(f"  Recall:    {avg_concept['recall']:.2%}")
        print(f"  F1:        {avg_concept['f1']:.2%}")
        print(f"  Samples:   {len(all_concept_metrics)}")

    if all_relation_metrics:
        avg_relation = {
            k: round(sum(m[k] for m in all_relation_metrics) / len(all_relation_metrics), 4)
            for k in ["precision", "recall", "f1"]
        }
        print(f"\nOverall Relation Extraction:")
        print(f"  Precision: {avg_relation['precision']:.2%}")
        print(f"  Recall:    {avg_relation['recall']:.2%}")
        print(f"  F1:        {avg_relation['f1']:.2%}")
        print(f"  Samples:   {len(all_relation_metrics)}")

    # By language
    by_lang = analyze_by_language(gold_data, results_map)
    print(f"\nBy Language:")
    for lang in ["zh", "de", "en"]:
        if lang in by_lang:
            lang_name = {"zh": "Chinese", "de": "German", "en": "English"}[lang]
            c = by_lang[lang].get("concepts", {})
            r = by_lang[lang].get("relations", {})
            print(f"\n  {lang_name}:")
            if c:
                print(f"    Concept F1: {c['f1']:.2%}")
            if r:
                print(f"    Relation F1: {r['f1']:.2%}")

    print("\n" + "=" * 60)


# --- Main ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MCL Analysis")
    parser.add_argument("--gold", type=str, help="Path to gold dataset")
    parser.add_argument("--results", type=str, help="Path to extraction results")
    args = parser.parse_args()

    gold = load_gold_dataset(args.gold)
    print(f"Loaded {len(gold)} gold samples")

    # For demo, run extraction on gold samples
    from extract import extract_concepts
    results_map = {}
    for sample in gold:
        try:
            result = extract_concepts(sample["text"], language=sample["language"])
            results_map[sample["sample_id"]] = result
        except Exception as e:
            print(f"Error on {sample['sample_id']}: {e}")

    print(f"Extracted {len(results_map)} samples")
    print_report(gold, results_map)
