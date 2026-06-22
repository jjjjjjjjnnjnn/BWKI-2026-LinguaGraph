#!/usr/bin/env python3
"""
LinguaGraph — LDS from Pre-computed Extractions
=================================================
Computes LDS for multi-language students using existing extractions
from the extractions table (no re-extraction needed).

Usage:
    python scripts/compute_lds_from_db.py
    python scripts/compute_lds_from_db.py --report
"""

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / "scripts"))
sys.path.insert(0, str(PROJECT_DIR / "src"))

from db_utils import get_connection, query, query_one, insert


def load_student_extractions(conn, student_id: str) -> Dict[str, Tuple[List[str], List[str]]]:
    """Load pre-computed extractions for a student, grouped by language."""
    rows = query(conn, """
        SELECT r.language, e.concepts, e.relations
        FROM responses r
        JOIN extractions e ON r.response_id = e.response_id
        WHERE r.student_id = ?
        AND e.model_used NOT IN ('mock')
        AND r.source = 'survey'
        ORDER BY r.language
    """, (student_id,))

    result = {}
    for r in rows:
        lang = r["language"]
        concepts = _safe_json_parse(r["concepts"], [])
        relations = _safe_json_parse(r["relations"], [])
        if lang not in result:
            result[lang] = ([], [])
        result[lang][0].extend(concepts)
        result[lang][1].extend(relations)

    # Deduplicate
    for lang in result:
        result[lang] = (list(set(result[lang][0])), list(set(str(r) for r in result[lang][1])))

    return result


def _safe_json_parse(val, default=None):
    if default is None:
        default = []
    if not val:
        return default
    try:
        return json.loads(val) if isinstance(val, str) else val
    except (json.JSONDecodeError, TypeError):
        return default


def compute_lds_from_graphs(concepts_a: List[str], concepts_b: List[str]) -> float:
    """
    Simplified LDS: 1 - Jaccard similarity of concept sets.
    This is a lightweight approximation when NetworkX is not available.
    """
    set_a = set(concepts_a)
    set_b = set(concepts_b)

    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 1.0

    intersection = set_a & set_b
    union = set_a | set_b

    if not union:
        return 1.0

    jaccard = len(intersection) / len(union)
    lds = 1.0 - jaccard
    return round(lds, 4)


def compute_lds_for_student(conn, student_id: str) -> List[Dict]:
    """Compute LDS between all language pairs for one student."""
    extractions = load_student_extractions(conn, student_id)
    languages = sorted(extractions.keys())

    if len(languages) < 2:
        return []

    results = []
    for i in range(len(languages)):
        for j in range(i + 1, len(languages)):
            lang_a = languages[i]
            lang_b = languages[j]
            concepts_a, _ = extractions[lang_a]
            concepts_b, _ = extractions[lang_b]
            pair_key = f"{lang_a}-{lang_b}"

            lds = compute_lds_from_graphs(concepts_a, concepts_b)

            # Save to cross_language_analysis table
            try:
                insert(conn, "cross_language_analysis", {
                    "analysis_id": f"LDS_{student_id}_{pair_key}_{datetime.now().strftime('%Y%m%d')}",
                    "student_id": student_id,
                    "lang_pair": pair_key,
                    "topic": "social_issues",
                    "lcd_score": lds,
                    "graph_a_json": json.dumps({"concepts": concepts_a}, ensure_ascii=False),
                    "graph_b_json": json.dumps({"concepts": concepts_b}, ensure_ascii=False),
                    "jaccard_score": round(1.0 - lds, 4),
                })
            except Exception as e:
                pass  # Duplicate key

            results.append({
                "student_id": student_id,
                "lang_pair": pair_key,
                "lds": lds,
                "concepts_a": len(set(concepts_a)),
                "concepts_b": len(set(concepts_b)),
                "concepts_overlap": len(set(concepts_a) & set(concepts_b)),
            })

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compute LDS from existing extractions")
    parser.add_argument("--report", action="store_true", help="Print report only")
    parser.add_argument("--student", type=str, default=None, help="Specific student only")
    args = parser.parse_args()

    conn = get_connection()

    # Find all students with multi-language extractions
    students = query(conn, """
        SELECT r.student_id
        FROM responses r
        JOIN extractions e ON r.response_id = e.response_id
        WHERE e.model_used NOT IN ('mock')
        AND r.source = 'survey'
        GROUP BY r.student_id
        HAVING COUNT(DISTINCT r.language) >= 2
    """)

    if not students:
        print("  No students with multi-language extractions found.")
        conn.close()
        return

    print(f"\n{'='*60}")
    print(f"  LDS from Extractions")
    print(f"{'='*60}")

    all_results = []
    for s in students:
        sid = s["student_id"]
        if args.student and sid != args.student:
            continue

        results = compute_lds_for_student(conn, sid)
        all_results.extend(results)

        if results:
            print(f"\n  {sid}:")
            for r in results:
                print(f"    {r['lang_pair']}: LDS={r['lds']:.4f} "
                      f"({r['concepts_a']} vs {r['concepts_b']} concepts, "
                      f"{r['concepts_overlap']} overlap)")
        else:
            print(f"\n  {sid}: < 2 languages")

    # Summary
    if all_results:
        print(f"\n  Summary:")
        lds_by_pair = defaultdict(list)
        for r in all_results:
            lds_by_pair[r["lang_pair"]].append(r["lds"])

        for pair, scores in sorted(lds_by_pair.items()):
            mean_lds = sum(scores) / len(scores)
            print(f"    {pair}: mean LDS={mean_lds:.4f} (n={len(scores)})")

        overall = sum(r["lds"] for r in all_results) / len(all_results)
        print(f"    OVERALL: mean LDS={overall:.4f} (n={len(all_results)})")

    conn.commit()
    conn.close()

    print()


if __name__ == "__main__":
    main()
