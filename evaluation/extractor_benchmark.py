"""
LinguaGraph — Extractor Benchmark Framework

Compares concept extraction methods on the gold standard dataset.

Baselines:
  - keyword: Simple keyword matching (lower bound)
  - llm:     LLM-based extraction (LinguaGraph current)
  - cocoex:  CoCo-Ex traditional NLP extraction (external, English only)

Usage:
    python evaluation/extractor_benchmark.py
    python evaluation/extractor_benchmark.py --extractor llm
    python evaluation/extractor_benchmark.py --extractor cocoex --verbose

Output:
    Prints F1 scores and generates evaluation/reports/extractor_comparison.json
"""
import json
import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.scoring import calculate_concept_f1, calculate_relation_f1


def load_gold_data():
    """Load gold standard annotation dataset."""
    gold_file = PROJECT_ROOT / "data" / "gold" / "gold_dataset.json"
    if not gold_file.exists():
        print(f"[ERROR] Gold data not found: {gold_file}")
        print("Run `python scripts/ingest_gold_labels.py` first.")
        return []
    with open(gold_file, encoding="utf-8") as f:
        return json.load(f)


def extract_keyword(text: str, language: str) -> dict:
    """
    Baseline A: Simple keyword-based concept extraction.

    Matches against cross_language_mapping.json keyword lists.
    This is the LOWEST baseline — any reasonable extractor should beat it.
    """
    mapping_file = PROJECT_ROOT / "config" / "cross_language_mapping.json"
    with open(mapping_file, encoding="utf-8") as f:
        mapping = json.load(f)

    text_lower = text.lower()
    lang_key = {"zh": "zh", "de": "de", "en": "en"}.get(language, "en")
    concepts = set()
    relations = []

    for entry in mapping["mappings"]:
        keywords = entry.get(lang_key, [])
        for kw in keywords:
            if kw.lower() in text_lower:
                concepts.add(kw)

    # For keyword baseline, generate simple co-occurrence relations
    concept_list = sorted(concepts)
    for i in range(len(concept_list)):
        for j in range(i + 1, len(concept_list)):
            relations.append({
                "source": concept_list[i],
                "target": concept_list[j],
                "type": "relates_to"
            })

    return {"concepts": list(concepts), "relations": relations}


def extract_llm(text: str, language: str) -> dict:
    """Baseline B: LLM-based extraction (LinguaGraph current)."""
    from src.extract import extract_concepts
    return extract_concepts(text, language, use_mock=False)


def extract_mock(text: str, language: str) -> dict:
    """Mock extraction (for testing, no API key needed)."""
    from src.extract import extract_concepts
    return extract_concepts(text, language, use_mock=True)


def extract_cocoex(text: str, language: str) -> dict:
    """
    Baseline C: CoCo-Ex extraction (English only, traditional NLP).

    Requires CoCo-Ex dependencies (spaCy, gensim, nltk, stanford parser).
    Falls back to keyword if CoCo-Ex not available.
    """
    if language != "en":
        print(f"  [WARN] CoCo-Ex only supports English. Skipping {language}.")
        return {"concepts": [], "relations": []}

    try:
        sys.path.insert(0, str(PROJECT_ROOT / "external" / "CoCo-Ex"))
        # CoCo-Ex requires specific dependency setup — check availability
        import importlib.util
        if importlib.util.find_spec("spacy") is None:
            print("  [WARN] CoCo-Ex dependencies not installed. Falling back to keyword.")
            return extract_keyword(text, language)

        # CoCo-Ex file has a hyphen in the name — use importlib
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "coco_ex",
            PROJECT_ROOT / "external" / "CoCo-Ex" / "CoCo-Ex_entity_extraction.py"
        )
        print("  [WARN] CoCo-Ex integration requires manual setup (see external/CoCo-Ex/README.md)")
        return {"concepts": [], "relations": []}
    except ImportError:
        print("  [WARN] CoCo-Ex not available. Run: pip install spacy gensim nltk")
        return extract_keyword(text, language)


EXTRACTORS = {
    "keyword": extract_keyword,
    "llm": extract_llm,
    "mock": extract_mock,
    "cocoex": extract_cocoex,
}


def run_benchmark(extractor_name: str = "all", verbose: bool = False):
    """Run benchmark for specified extractor(s)."""
    gold_data = load_gold_data()
    if not gold_data:
        return

    if extractor_name == "all":
        extractors_to_run = list(EXTRACTORS.keys())
    else:
        extractors_to_run = [extractor_name]

    results = {}

    for name in extractors_to_run:
        extractor = EXTRACTORS.get(name)
        if not extractor:
            print(f"[ERROR] Unknown extractor: {name}. Options: {list(EXTRACTORS.keys())}")
            continue

        print(f"\n{'='*60}")
        print(f"Extractor: {name}")
        print(f"{'='*60}")

        total_cp = 0
        total_cr = 0
        total_cf = 0
        total_rp = 0
        total_rr = 0
        total_rf = 0
        n_samples = 0

        for sample in gold_data:
            if not isinstance(sample, dict):
                continue

            text = sample.get("text", "")
            language = sample.get("language", sample.get("lang", "zh"))

            # Handle gold labels format
            human_labels = sample.get("human_labels", sample.get("labels", {}))
            if isinstance(human_labels, dict):
                gold_concepts = set(human_labels.get("concepts", sample.get("concepts", [])))
                gold_relations = human_labels.get("relations", sample.get("relations", []))
            else:
                gold_concepts = set(sample.get("concepts", []))
                gold_relations = sample.get("relations", [])

            if not text:
                continue

            try:
                result = extractor(text, language)
            except Exception as e:
                print(f"  [ERROR] {sample_key}: {e}")
                continue

            extracted_concepts = set(result.get("concepts", []))
            extracted_relations = result.get("relations", [])

            # Calculate concept F1
            cf = calculate_concept_f1(gold_concepts, extracted_concepts)
            # Calculate relation F1
            rf = calculate_relation_f1(gold_relations, extracted_relations)

            sample_id = sample.get("sample_id", sample.get("id", f"sample_{n_samples}"))
            if verbose:
                print(f"  [{sample_id}] ({language})")
                print(f"    Concepts F1: {cf['f1']:.3f}  P={cf['precision']:.3f} R={cf['recall']:.3f}")
                print(f"    Relations F1: {rf['f1']:.3f}  P={rf['precision']:.3f} R={rf['recall']:.3f}")

            total_cp += cf["precision"]
            total_cr += cf["recall"]
            total_cf += cf["f1"]
            total_rp += rf["precision"]
            total_rr += rf["recall"]
            total_rf += rf["f1"]
            n_samples += 1

        if n_samples > 0:
            avg_cf = total_cf / n_samples
            avg_rf = total_rf / n_samples
            results[name] = {
                "concept_f1": round(avg_cf, 4),
                "concept_precision": round(total_cp / n_samples, 4),
                "concept_recall": round(total_cr / n_samples, 4),
                "relation_f1": round(avg_rf, 4),
                "relation_precision": round(total_rp / n_samples, 4),
                "relation_recall": round(total_rr / n_samples, 4),
                "samples": n_samples,
            }
            print(f"\n  RESULTS [{name}]:")
            print(f"    Concept F1: {avg_cf:.3f}")
            print(f"    Relation F1: {avg_rf:.3f}")
            print(f"    Samples: {n_samples}")

    # Print comparison table
    if len(results) > 1:
        print(f"\n{'='*60}")
        print("COMPARISON TABLE")
        print(f"{'='*60}")
        print(f"{'Extractor':<12} {'Concept F1':<12} {'Relation F1':<12} {'Samples':<8}")
        print("-" * 44)
        for name, r in results.items():
            print(f"{name:<12} {r['concept_f1']:<12.3f} {r['relation_f1']:<12.3f} {r['samples']:<8}")

    # Save report
    report_dir = PROJECT_ROOT / "evaluation" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "extractor_comparison.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nReport saved: {report_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LinguaGraph Extractor Benchmark")
    parser.add_argument("--extractor", default="all",
                        help=f"Extractor to benchmark: {list(EXTRACTORS.keys())} or 'all'")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show per-sample results")
    args = parser.parse_args()

    print("=" * 60)
    print("LinguaGraph — Extractor Benchmark")
    print("=" * 60)
    run_benchmark(args.extractor, verbose=args.verbose)
