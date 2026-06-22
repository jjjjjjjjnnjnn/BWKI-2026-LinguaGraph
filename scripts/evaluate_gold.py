#!/usr/bin/env python3
"""
LinguaGraph — Gold Label Evaluation
======================================
Evaluates concept extraction quality by comparing extracted concepts
against human-annotated gold labels.

Two modes:
  1) LLM mode: Evaluate LLM extractions from the extractions table
     (requires LLM extractions to exist — run batch_process_responses.py first)

  2) Keyword baseline: Simple text-matching extractor to establish
     a lower-bound F1 score without any LLM

Usage:
    python scripts/evaluate_gold.py                          # Auto-detect mode
    python scripts/evaluate_gold.py --keyword-baseline       # Force keyword baseline
    python scripts/evaluate_gold.py --report                 # Report only
    python scripts/evaluate_gold.py --export-json            # Export evaluation JSON

Authors: BWKI 2026 — LinguaGraph Team
"""

import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / "scripts"))
sys.path.insert(0, str(PROJECT_DIR / "src"))

from db_utils import get_connection, insert, query, query_one

OUTPUT_DIR = PROJECT_DIR / "research" / "findings"


# ===== CORE EVALUATION =====

def load_gold_data(conn) -> List[Dict]:
    """Load all gold labels with their response texts."""
    rows = query(conn, """
        SELECT gl.label_id, gl.response_id, gl.concepts as gold_concepts,
               gl.relations as gold_relations, r.answer_text, r.language
        FROM gold_labels gl
        JOIN responses r ON gl.response_id = r.response_id
        ORDER BY gl.response_id
    """)
    return rows


def load_llm_extractions(conn) -> Dict[str, Dict]:
    """Load LLM extractions grouped by response_id."""
    rows = query(conn, """
        SELECT response_id, extraction_id, concepts, relations, model_used
        FROM extractions
        ORDER BY created_at
    """)
    result = {}
    for r in rows:
        result[r["response_id"]] = {
            "extraction_id": r["extraction_id"],
            "concepts": _parse_json_list(r["concepts"]),
            "relations": r.get("relations", "[]"),
            "model": r.get("model_used", "unknown"),
        }
    return result


def _parse_json_list(val) -> List:
    """Parse a JSON string to list, with error handling."""
    if not val:
        return []
    try:
        if isinstance(val, str):
            return json.loads(val)
        return val if isinstance(val, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def _normalize_concept(c: str) -> str:
    """Normalize a concept for comparison."""
    c = c.strip().lower()
    c = re.sub(r'[^\w一-鿿-]', '', c)  # keep alphanumeric + CJK + hyphens
    return c


# ===== KEYWORD BASELINE EXTRACTOR =====

def keyword_extract(text: str, gold_concepts: List[str]) -> List[str]:
    """
    Simple keyword-based concept extractor.
    Finds gold concepts that appear in the text.
    This is the weakest possible extractor — a lower bound.
    """
    text_lower = text.lower()
    found = []
    for c in gold_concepts:
        c_norm = _normalize_concept(c)
        if c_norm and c_norm in text_lower:
            found.append(c)
    return found


def compute_f1(gold: set, predicted: set) -> Dict:
    """Compute precision, recall, F1."""
    if not gold:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    if not predicted:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    true_positives = len(gold & predicted)
    if true_positives == 0:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    precision = true_positives / len(predicted)
    recall = true_positives / len(gold)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


def evaluate_gold_labels(conn, mode: str = "auto") -> List[Dict]:
    """Run evaluation on all gold labels."""
    gold_items = load_gold_data(conn)
    llm_extractions = load_llm_extractions(conn) if mode in ("auto", "llm") else {}

    if not gold_items:
        print("  [WARN] No gold labels found in database.")
        return []

    results = []
    matched_extractions = 0
    gold_with_extractions = 0

    for item in gold_items:
        response_id = item["response_id"]
        gold_concepts = _parse_json_list(item["gold_concepts"])
        gold_relations = item.get("gold_relations", "[]")
        answer_text = item.get("answer_text", "")
        language = item.get("language", "zh")

        # Normalize gold concepts set
        gold_set = set(_normalize_concept(c) for c in gold_concepts if c.strip())

        # Determine predicted concepts
        if mode == "keyword" or (mode == "auto" and response_id not in llm_extractions):
            # Use keyword baseline
            predicted = keyword_extract(answer_text, gold_concepts)
            source = "keyword_baseline"
        else:
            # Use LLM extraction
            ext = llm_extractions.get(response_id)
            if ext and ext["concepts"]:
                predicted = ext["concepts"]
                source = ext["model"]
                matched_extractions += 1
            else:
                predicted = []
                source = "no_extraction"
            gold_with_extractions += 1

        predicted_set = set(_normalize_concept(c) for c in predicted if c.strip())

        metrics = compute_f1(gold_set, predicted_set)
        metrics["gold_count"] = len(gold_set)
        metrics["predicted_count"] = len(predicted_set)
        metrics["response_id"] = response_id
        metrics["language"] = language
        metrics["source"] = source
        metrics["gold_concepts"] = gold_concepts
        metrics["predicted_concepts"] = predicted
        metrics["text_preview"] = answer_text[:80] if answer_text else ""

        # Save to evaluation_results table
        _save_evaluation(conn, response_id, metrics, source)

        results.append(metrics)

    return results


def _save_evaluation(conn, response_id: str, metrics: Dict, source: str):
    """Save evaluation result to evaluation_results table."""
    eval_id = f"GE_{datetime.now().strftime('%Y%m%d')}_{response_id[:15]}"
    try:
        insert(conn, "evaluation_results", {
            "eval_id": eval_id,
            "extraction_id": f"eval_{response_id}",
            "label_id": f"L_{response_id}",
            "concept_precision": metrics["precision"],
            "concept_recall": metrics["recall"],
            "concept_f1": metrics["f1"],
            "relation_precision": 0.0,
            "relation_recall": 0.0,
            "relation_f1": 0.0,
            "coverage": metrics["predicted_count"] / max(metrics["gold_count"], 1),
            "details_json": json.dumps({
                "gold": metrics["gold_concepts"],
                "predicted": metrics["predicted_concepts"],
                "source": source,
            }, ensure_ascii=False),
        })
    except Exception as e:
        print(f"    [WARN] DB save: {e}")


# ===== REPORTING =====

def print_report(results: List[Dict], title: str = "Gold Label Evaluation"):
    """Print structured evaluation report."""
    if not results:
        print("  No results to report.")
        return

    f1_scores = [r["f1"] for r in results]
    precisions = [r["precision"] for r in results]
    recalls = [r["recall"] for r in results]

    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"\n  Summary:")
    print(f"    Items evaluated:  {len(results)}")
    print(f"    Mean F1:         {sum(f1_scores)/len(f1_scores):.4f}")
    print(f"    Mean Precision:  {sum(precisions)/len(precisions):.4f}")
    print(f"    Mean Recall:     {sum(recalls)/len(recalls):.4f}")
    print(f"    Median F1:       {sorted(f1_scores)[len(f1_scores)//2]:.4f}")

    # Per-language breakdown
    by_lang = defaultdict(list)
    for r in results:
        by_lang[r["language"]].append(r)

    print(f"\n  By Language:")
    for lang in ["zh", "de", "en"]:
        items = by_lang.get(lang, [])
        if items:
            lang_f1 = [i["f1"] for i in items]
            lang_p = [i["precision"] for i in items]
            lang_r = [i["recall"] for i in items]
            sources = set(i["source"] for i in items)
            print(f"    {lang}: F1={sum(lang_f1)/len(lang_f1):.4f} "
                  f"P={sum(lang_p)/len(lang_p):.4f} R={sum(lang_r)/len(lang_r):.4f} "
                  f"(n={len(items)}, source={', '.join(sources)})")

    # Source breakdown
    by_source = defaultdict(list)
    for r in results:
        by_source[r["source"]].append(r)
    print(f"\n  By Source:")
    for src, items in sorted(by_source.items()):
        src_f1 = [i["f1"] for i in items]
        print(f"    {src}: F1={sum(src_f1)/len(src_f1):.4f} (n={len(items)})")

    # Detail per item
    print(f"\n  Per-Item Details:")
    for i, r in enumerate(results):
        status = "✅" if r["f1"] >= 0.7 else "⚠️" if r["f1"] >= 0.5 else "❌"
        print(f"    {i+1:>2d}. {status} {r['response_id']:<20s} "
              f"F1={r['f1']:.3f} P={r['precision']:.3f} R={r['recall']:.3f} "
              f"({r['gold_count']}g/{r['predicted_count']}p) [{r['language']}]")

    print()


def export_results(results: List[Dict], filename: str = "gold_evaluation.json"):
    """Export evaluation results to JSON."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename

    # Aggregate
    f1_scores = [r["f1"] for r in results]
    by_lang = defaultdict(list)
    for r in results:
        by_lang[r["language"]].append(r)

    export = {
        "evaluation_date": datetime.now().isoformat(),
        "total_items": len(results),
        "summary": {
            "mean_f1": round(sum(f1_scores) / len(f1_scores), 4) if f1_scores else 0,
            "mean_precision": round(sum(r["precision"] for r in results) / len(results), 4) if results else 0,
            "mean_recall": round(sum(r["recall"] for r in results) / len(results), 4) if results else 0,
        },
        "by_language": {
            lang: {
                "count": len(items),
                "mean_f1": round(sum(i["f1"] for i in items) / len(items), 4),
            }
            for lang, items in sorted(by_lang.items())
        },
        "results": results,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=2)

    print(f"  Exported: {path}")
    return path


def check_status(conn):
    """Print current evaluation status."""
    gold = query_one(conn, "SELECT COUNT(*) as c FROM gold_labels")["c"]
    extractions = query_one(conn, "SELECT COUNT(*) as c FROM extractions")["c"]
    evaluated = query_one(conn, "SELECT COUNT(*) as c FROM evaluation_results")["c"]
    llm_gold = query(conn, """
        SELECT COUNT(*) as c FROM extractions e
        JOIN gold_labels gl ON e.response_id = gl.response_id
    """)
    llm_count = llm_gold[0]["c"] if llm_gold else 0 if not isinstance(llm_gold, int) else llm_gold

    print(f"\n  Evaluation Status:")
    print(f"    Gold labels:       {gold}")
    print(f"    Total extractions: {extractions}")
    print(f"    Gold LLM extractions: {llm_count}")
    print(f"    Evaluation rows:   {evaluated}")

    if llm_count == 0 and evaluated == 0:
        print(f"\n  ⚠️  No LLM extractions for gold labels yet.")
        print(f"  To generate, run an LLM (LM Studio, OpenAI) then:")
        print(f"    python scripts/batch_process_responses.py --gold-only")
        print(f"  Then run this evaluation:")
        print(f"    python scripts/evaluate_gold.py")
        print(f"\n  For now, keyword baseline available:")
        print(f"    python scripts/evaluate_gold.py --keyword-baseline")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph Gold Label Evaluation")
    parser.add_argument("--keyword-baseline", action="store_true", help="Force keyword baseline evaluation")
    parser.add_argument("--report", action="store_true", help="Print report from existing results only")
    parser.add_argument("--export-json", action="store_true", help="Export results as JSON")
    parser.add_argument("--status", action="store_true", help="Show evaluation status only")
    args = parser.parse_args()

    conn = get_connection()

    if args.status:
        check_status(conn)
        conn.close()
        return

    if args.report:
        results = query(conn, """
            SELECT concept_f1, concept_recall, concept_precision,
                   details_json, created_at
            FROM evaluation_results
            ORDER BY created_at
        """)
        if not results:
            print("  No evaluation results in DB.")
            conn.close()
            return

        # Reconstruct from stored details
        reconstructed = []
        for r in results:
            try:
                details = json.loads(r["details_json"])
            except (json.JSONDecodeError, TypeError):
                details = {}
            reconstructed.append({
                "f1": r["concept_f1"],
                "precision": r["concept_precision"],
                "recall": r["concept_recall"],
                "gold_concepts": details.get("gold", []),
                "predicted_concepts": details.get("predicted", []),
                "source": details.get("source", "unknown"),
                "response_id": "unknown",
                "language": "unknown",
                "gold_count": len(details.get("gold", [])),
                "predicted_count": len(details.get("predicted", [])),
            })

        print_report(reconstructed, "Stored Evaluation Results")
        conn.close()
        return

    # Determine mode
    mode = "keyword" if args.keyword_baseline else "auto"

    print(f"\n{'='*60}")
    print(f"  LinguaGraph — Gold Label Evaluation")
    print(f"  Mode: {mode}")
    print(f"{'='*60}")

    results = evaluate_gold_labels(conn, mode=mode)

    if results:
        print_report(results)
        if args.export_json or mode == "keyword":
            export_results(results)
    else:
        print("\n  Nothing to evaluate.")

    # Summary
    total_gold = len(results)
    passed = sum(1 for r in results if r["f1"] >= 0.7)
    borderline = sum(1 for r in results if 0.5 <= r["f1"] < 0.7)
    failed = sum(1 for r in results if r["f1"] < 0.5)

    print(f"\n  Quality Gates:")
    print(f"    F1 ≥ 0.70: {passed}/{total_gold} ({passed/total_gold*100:.0f}%)" if total_gold else "")
    print(f"    0.50 ≤ F1 < 0.70: {borderline} items")
    print(f"    F1 < 0.50: {failed} items")
    print()

    conn.close()


if __name__ == "__main__":
    main()
