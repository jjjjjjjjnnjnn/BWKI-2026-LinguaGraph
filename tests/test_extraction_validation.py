"""
Validate LLM extraction accuracy against human labels.

This test uses inline test data to verify the extraction module works.
No external data files required.
"""
import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.extract import extract_concepts


def evaluate_extraction(use_mock=False):
    """Evaluate extraction accuracy on inline test samples."""
    test_data = {
        "samples": [
            {
                "id": "zh_001",
                "language": "zh",
                "text": "自由是每个人都应该拥有的权利，但同时也伴随着责任。",
                "gold_concepts": ["自由", "权利", "责任"]
            },
            {
                "id": "de_001",
                "language": "de",
                "text": "Freiheit ist ein grundlegendes Recht, das mit Verantwortung einhergeht.",
                "gold_concepts": ["Freiheit", "Recht", "Verantwortung"]
            },
            {
                "id": "en_001",
                "language": "en",
                "text": "Freedom is a fundamental right that comes with responsibility.",
                "gold_concepts": ["freedom", "right", "responsibility"]
            }
        ]
    }

    concept_tp = 0
    concept_fp = 0
    concept_fn = 0

    for sample in test_data["samples"]:
        result = extract_concepts(sample["text"], sample["language"], use_mock=use_mock)
        extracted = set(result.get("concepts", []))
        gold = set(sample["gold_concepts"])

        concept_tp += len(extracted & gold)
        concept_fp += len(extracted - gold)
        concept_fn += len(gold - extracted)

        print(f"  [{sample['id']}] Extracted: {extracted}")

    precision = concept_tp / max(concept_tp + concept_fp, 1)
    recall = concept_tp / max(concept_tp + concept_fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-6)

    print(f"\nResults (mock={use_mock}):")
    print(f"  Precision: {precision:.3f}")
    print(f"  Recall:    {recall:.3f}")
    print(f"  F1:        {f1:.3f}")

    return {"precision": precision, "recall": recall, "f1": f1}


if __name__ == "__main__":
    print("=== Extraction Validation ===\n")

    # Test with mock mode (no LLM calls)
    print("Testing mock extraction...")
    result = evaluate_extraction(use_mock=True)
    print(f"\n  → F1 = {result['f1']:.3f}")

    # Test with real LLM (only if API key is set)
    import os
    if os.environ.get("OPENAI_API_KEY"):
        print("\nTesting live LLM extraction...")
        result = evaluate_extraction(use_mock=False)
        print(f"\n  → F1 = {result['f1']:.3f}")
    else:
        print("\n[Skipped] No OPENAI_API_KEY set — live extraction test requires API key.")
        print("Set OPENAI_API_KEY environment variable to run live tests.")

    print("\nDone.")
