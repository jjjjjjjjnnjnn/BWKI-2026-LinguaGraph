"""Validate LLM extraction accuracy against human labels."""
import json
import sys
import io
from pathlib import Path

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.extract import extract_concepts

DATA_DIR = Path(__file__).parent.parent / "data"
TEST_FILE = DATA_DIR / "extraction_test.json"


def load_test_data():
    with open(TEST_FILE, encoding="utf-8") as f:
        return json.load(f)


def evaluate_extraction(use_mock=False):
    """Evaluate extraction accuracy on 10 test samples."""
    test_data = load_test_data()

    concept_tp = 0
    concept_fp = 0
    concept_fn = 0
    relation_tp = 0
    relation_fp = 0
    relation_fn = 0
    json_errors = 0
    total = len(test_data)

    print("=" * 60)
    print("Extraction Validation - Detailed Results")
    print("=" * 60)

    for sample in test_data:
        try:
            result = extract_concepts(
                sample["input"],
                language=sample["language"],
                use_mock=use_mock
            )
        except Exception as e:
            json_errors += 1
            print(f"[ERROR] {sample['id']}: {e}")
            continue

        # Concept comparison
        extracted_concepts = set(result["concepts"])
        human_concepts = set(sample["human_labels"]["concepts"])

        tp = len(extracted_concepts & human_concepts)
        fp = len(extracted_concepts - human_concepts)
        fn = len(human_concepts - extracted_concepts)

        concept_tp += tp
        concept_fp += fp
        concept_fn += fn

        # Relation comparison (simplified: source-target pairs)
        extracted_relations = {(r["source"], r["target"]) for r in result["relations"]}
        human_relations = {(r["from"], r["to"]) for r in sample["human_labels"]["relations"]}

        r_tp = len(extracted_relations & human_relations)
        r_fp = len(extracted_relations - human_relations)
        r_fn = len(human_relations - extracted_relations)

        relation_tp += r_tp
        relation_fp += r_fp
        relation_fn += r_fn

        # Print per-sample results
        status = "OK" if fp == 0 and fn == 0 else "PARTIAL"
        print(f"\n[{status}] {sample['id']} ({sample['language']})")
        print(f"  Input: {sample['input'][:60]}...")
        print(f"  Extracted: {result['concepts']}")
        print(f"  Expected:  {list(human_concepts)}")
        print(f"  Concept P={tp/(tp+fp):.0%} R={tp/(tp+fn):.0%}" if (tp+fp) > 0 and (tp+fn) > 0 else "  Concept: N/A")

    # Calculate metrics
    concept_precision = concept_tp / max(concept_tp + concept_fp, 1)
    concept_recall = concept_tp / max(concept_tp + concept_fn, 1)
    concept_f1 = 2 * concept_precision * concept_recall / max(concept_precision + concept_recall, 1e-6)

    relation_precision = relation_tp / max(relation_tp + relation_fp, 1)
    relation_recall = relation_tp / max(relation_tp + relation_fn, 1)
    relation_f1 = 2 * relation_precision * relation_recall / max(relation_precision + relation_recall, 1e-6)

    json_success_rate = (total - json_errors) / total

    print("\n" + "=" * 60)
    print("EXTRACTION VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Samples: {total}")
    print(f"JSON Success Rate: {json_success_rate:.0%}")
    print()
    print("Concept Extraction:")
    print(f"  Precision: {concept_precision:.2%}")
    print(f"  Recall:    {concept_recall:.2%}")
    print(f"  F1:        {concept_f1:.2%}")
    print()
    print("Relation Extraction:")
    print(f"  Precision: {relation_precision:.2%}")
    print(f"  Recall:    {relation_recall:.2%}")
    print(f"  F1:        {relation_f1:.2%}")
    print("=" * 60)

    # Pass criteria
    passed = (
        json_success_rate >= 0.9 and
        concept_f1 >= 0.5 and
        relation_f1 >= 0.4
    )

    if passed:
        print("[PASS] Extraction is reliable enough for MCL validation.")
    else:
        print("[FAIL] Extraction needs improvement before proceeding.")
        print("  -> Review failed samples above")
        print("  -> Consider adjusting prompt or adding few-shot examples")

    return {
        "json_success_rate": json_success_rate,
        "concept_precision": concept_precision,
        "concept_recall": concept_recall,
        "concept_f1": concept_f1,
        "relation_precision": relation_precision,
        "relation_recall": relation_recall,
        "relation_f1": relation_f1,
        "passed": passed
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Use mock extraction")
    args = parser.parse_args()

    results = evaluate_extraction(use_mock=args.mock)
