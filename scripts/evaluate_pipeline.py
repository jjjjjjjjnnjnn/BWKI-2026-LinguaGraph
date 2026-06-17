"""
Evaluate Pipeline — LLM Extraction Quality Evaluation
========================================================
Compares LLM extractions against gold labels (ground truth)
and calculates Precision/Recall/F1 metrics.

Usage:
    python evaluate_pipeline.py                        # Evaluate all
    python evaluate_pipeline.py --fresh                 # Re-evaluate (clear existing)
    python evaluate_pipeline.py --summary               # Summary only
    python evaluate_pipeline.py --export-report         # Export report to JSON
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent))  # project root
from db_utils import get_connection, query, query_one, insert

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))  # src/


def evaluate_all(conn, fresh: bool = False) -> List[Dict]:
    """Evaluate all extractions against gold labels."""
    if fresh:
        conn.execute("DELETE FROM evaluation_results")
        conn.commit()
        print("  [FRESH] Cleared existing evaluation results")

    # Get all extractions that have corresponding gold labels
    evaluations = query(conn, """
        SELECT e.extraction_id, e.response_id, e.concepts as e_concepts,
               e.relations as e_relations, e.model_used,
               gl.label_id, gl.concepts as gl_concepts,
               gl.relations as gl_relations
        FROM extractions e
        JOIN gold_labels gl ON e.response_id = gl.response_id
        ORDER BY e.created_at
    """)

    if not evaluations:
        print("  [INFO] No evaluations to run (need both extractions and gold labels)")
        return []

    results = []
    for ev in evaluations:
        eval_id = f"EV_{datetime.now().strftime('%Y%m%d')}_{ev['extraction_id']}"

        # Parse JSON fields
        try:
            e_concepts = set(json.loads(ev["e_concepts"])) if ev["e_concepts"] else set()
        except (json.JSONDecodeError, TypeError):
            e_concepts = set()

        try:
            gl_concepts = set(json.loads(ev["gl_concepts"])) if ev["gl_concepts"] else set()
        except (json.JSONDecodeError, TypeError):
            gl_concepts = set()

        try:
            e_relations = json.loads(ev["e_relations"]) if ev["e_relations"] else []
        except (json.JSONDecodeError, TypeError):
            e_relations = []

        try:
            gl_relations = json.loads(ev["gl_relations"]) if ev["gl_relations"] else []
        except (json.JSONDecodeError, TypeError):
            gl_relations = []

        # Calculate metrics
        concept_metrics = calculate_concept_f1(gl_concepts, e_concepts)
        relation_metrics = calculate_relation_f1(gl_relations, e_relations)

        # Coverage
        coverage = len(e_concepts) / max(len(gl_concepts), 1) if gl_concepts else 0

        # Save to DB
        try:
            insert(conn, "evaluation_results", {
                "eval_id": eval_id,
                "extraction_id": ev["extraction_id"],
                "label_id": ev["label_id"],
                "concept_precision": concept_metrics["precision"],
                "concept_recall": concept_metrics["recall"],
                "concept_f1": concept_metrics["f1"],
                "relation_precision": relation_metrics["precision"],
                "relation_recall": relation_metrics["recall"],
                "relation_f1": relation_metrics["f1"],
                "coverage": coverage,
                "details_json": json.dumps({
                    "model": ev["model_used"],
                    "ai_concepts": list(e_concepts),
                    "gold_concepts": list(gl_concepts),
                    "ai_relations": e_relations,
                    "gold_relations": gl_relations,
                }, ensure_ascii=False),
            })
            results.append({
                "eval_id": eval_id,
                "extraction_id": ev["extraction_id"],
                "label_id": ev["label_id"],
                "concept_f1": concept_metrics["f1"],
                "relation_f1": relation_metrics["f1"],
                "coverage": coverage,
            })
            status = "OK"
        except Exception as e:
            status = f"WARN: {e}"

        print(f"  [{status}] {eval_id[:30]:<30s} | C-F1: {concept_metrics['f1']:.3f} | R-F1: {relation_metrics['f1']:.3f}")

    return results


def print_summary(conn):
    """Print summary of evaluation results."""
    results = query(conn, """
        SELECT
            COUNT(*) as total,
            AVG(concept_f1) as avg_concept_f1,
            AVG(relation_f1) as avg_relation_f1,
            AVG(concept_precision) as avg_precision,
            AVG(concept_recall) as avg_recall,
            AVG(coverage) as avg_coverage
        FROM evaluation_results
    """)

    if not results or results[0]["total"] == 0:
        print("  [INFO] No evaluation results yet. Run without --summary first.")
        return

    r = results[0]
    print(f"\n{'='*50}")
    print(f"  LLM Extraction Quality Summary")
    print(f"{'='*50}")
    print(f"  Total evaluations:   {r['total']}")
    print(f"  Avg Concept F1:      {r['avg_concept_f1']:.4f}")
    print(f"  Avg Relation F1:     {r['avg_relation_f1']:.4f}")
    print(f"  Avg Precision:       {r['avg_precision']:.4f}")
    print(f"  Avg Recall:          {r['avg_recall']:.4f}")
    print(f"  Avg Coverage:        {r['avg_coverage']:.4f}")
    print(f"{'='*50}\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate LLM extraction quality")
    parser.add_argument("--fresh", action="store_true", help="Re-evaluate all")
    parser.add_argument("--summary", action="store_true", help="Show summary only")
    parser.add_argument("--export-report", type=str, help="Export report to JSON file")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  Pipeline Evaluation")
    print(f"{'='*50}")

    conn = get_connection()

    if args.summary:
        print_summary(conn)
    else:
        results = evaluate_all(conn, fresh=args.fresh)
        print(f"\n  [DONE] {len(results)} evaluations completed")

        if args.export_report:
            report_path = Path(args.export_report)
            report_data = {
                "timestamp": datetime.now().isoformat(),
                "total": len(results),
                "results": results,
            }
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            print(f"  [EXPORT] Report saved to {report_path}")

        print_summary(conn)

    conn.close()


if __name__ == "__main__":
    main()
