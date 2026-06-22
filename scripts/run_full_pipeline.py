#!/usr/bin/env python3
"""
LinguaGraph — Full Pipeline A Runner
======================================
After batch extraction completes, this script computes LDS for all
students with valid extractions and runs the human-vs-model comparison.

Usage:
    python scripts/run_full_pipeline.py                    # Run all steps
    python scripts/run_full_pipeline.py --lds-only         # LDS computation only
    python scripts/run_full_pipeline.py --compare-only     # Comparison only
    python scripts/run_full_pipeline.py --status           # Check readiness
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / "scripts"))
sys.path.insert(0, str(PROJECT_DIR / "src"))

from db_utils import get_connection, query, query_one, insert


def check_status(conn):
    """Check if we have enough data to run the full pipeline."""
    # Students with at least 2 languages extracted
    students = query(conn, """
        SELECT r.student_id,
               COUNT(DISTINCT r.language) as lang_count,
               COUNT(e.extraction_id) as ext_count
        FROM responses r
        JOIN extractions e ON r.response_id = e.response_id
        WHERE e.model_used NOT IN ('mock')
        AND r.source = 'survey'
        GROUP BY r.student_id
        ORDER BY lang_count DESC
    """)

    print(f"\n{'='*60}")
    print(f"  Pipeline A Readiness Check")
    print(f"{'='*60}")

    total_extractions = query_one(conn, "SELECT COUNT(*) as c FROM extractions")["c"]
    total_real = query_one(conn, "SELECT COUNT(*) as c FROM responses WHERE source='survey'")["c"]
    print(f"  Real responses: {total_real}")
    print(f"  Total extractions: {total_extractions}")

    print(f"\n  Students with LLM extractions:")
    multi_lang = 0
    for s in students:
        langs = query(conn, "SELECT DISTINCT language FROM responses WHERE student_id=?", (s["student_id"],))
        lang_list = [l["language"] for l in langs]
        print(f"    {s['student_id']}: {s['ext_count']} ext / {s['lang_count']} languages ({', '.join(lang_list)})")
        if s["lang_count"] >= 2:
            multi_lang += 1

    print(f"\n  Multi-language students (can compute LDS): {multi_lang}")
    print(f"  Current LDS rows: {query_one(conn, 'SELECT COUNT(*) as c FROM cross_language_analysis')['c']}")
    print(f"  Evaluation rows: {query_one(conn, 'SELECT COUNT(*) as c FROM evaluation_results')['c']}")

    return multi_lang > 0


def compute_lds_for_students(conn) -> int:
    """Compute LDS for each student that has multi-language extractions."""
    sys.path.insert(0, str(PROJECT_DIR))
    from analyze_student import analyze_student_responses

    students = query(conn, """
        SELECT r.student_id
        FROM responses r
        JOIN extractions e ON r.response_id = e.response_id
        WHERE e.model_used NOT IN ('mock')
        AND r.source = 'survey'
        GROUP BY r.student_id
    """)

    print(f"\n{'='*60}")
    print(f"  Computing LDS for {len(students)} students")
    print(f"{'='*60}")

    count = 0
    for s in students:
        sid = s["student_id"]
        print(f"\n  [{sid}] analyzing...")
        result = analyze_student_responses(conn, sid, use_mock=False, verbose=True)
        if result and "error" not in result:
            comparisons = result.get("comparisons", [])
            for comp in comparisons:
                lds = comp.get("lcd", {}).get("lcd_score", "N/A")
                print(f"    {comp['lang_pair']}: LDS={lds}")
            count += 1
        else:
            error = result.get("error", "unknown") if result else "no result"
            print(f"    [SKIP] {error}")

    print(f"\n  Done: LDS computed for {count} students")
    return count


def run_comparison(conn) -> None:
    """Run human vs model comparison."""
    print(f"\n{'='*60}")
    print(f"  Human vs Model Comparison")
    print(f"{'='*60}")

    try:
        sys.path.insert(0, str(PROJECT_DIR / "scripts"))
        from compare_human_vs_model import main as compare_main

        # The script's main() expects sys.argv
        import argparse
        sys.argv = ["compare_human_vs_model.py", "--report"]
        compare_main()
        print(f"  Comparison complete.")
    except Exception as e:
        print(f"  [ERROR] Comparison failed: {e}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph Full Pipeline A Runner")
    parser.add_argument("--lds-only", action="store_true", help="LDS computation only")
    parser.add_argument("--compare-only", action="store_true", help="Comparison only")
    parser.add_argument("--status", action="store_true", help="Check readiness only")
    args = parser.parse_args()

    conn = get_connection()

    if args.status:
        check_status(conn)
        conn.close()
        return

    ready = check_status(conn)

    if not ready:
        print(f"\n  Pipeline not ready. Need more extractions.")
        conn.close()
        return

    if args.compare_only:
        run_comparison(conn)
    elif args.lds_only:
        compute_lds_for_students(conn)
    else:
        # Full pipeline
        n = compute_lds_for_students(conn)
        if n > 0:
            run_comparison(conn)

    conn.close()


if __name__ == "__main__":
    main()
