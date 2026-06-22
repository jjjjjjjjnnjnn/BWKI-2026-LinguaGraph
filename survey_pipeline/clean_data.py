"""
Survey Pipeline — Data Cleaning
================================
Clean and validate imported survey responses.

Usage:
    python clean_data.py
    python clean_data.py --verbose
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from db_utils import get_connection, query, query_one

from config import MIN_WORD_COUNT, MIN_ANSWER_LENGTH


def detect_answer_language(text: str) -> str:
    """Detect language of a text response."""
    if not text:
        return "unknown"
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total = len(text.strip())
    if total == 0:
        return "unknown"
    if chinese_chars / total > 0.3:
        return "zh"
    if any(c in text for c in "äöüßÄÖÜ"):
        return "de"
    return "en"


def check_duplicates(conn) -> list:
    """Find duplicate responses."""
    dupes = query(conn, """
        SELECT response_id, student_id, question_id, language,
               COUNT(*) as cnt
        FROM responses
        WHERE source = 'survey'
        GROUP BY student_id, question_id, language
        HAVING cnt > 1
    """)
    return dupes


def check_quality(conn) -> dict:
    """Assess response quality."""
    stats = {}

    # Total responses
    total = query_one(conn, """
        SELECT COUNT(*) as c FROM responses WHERE source='survey'
    """)
    stats["total"] = total["c"] if total else 0

    # By quality flag
    for flag in ["ok", "short", "empty"]:
        count = query_one(conn, """
            SELECT COUNT(*) as c FROM responses
            WHERE source='survey' AND quality_flag=?
        """, (flag,))
        stats[f"flag_{flag}"] = count["c"] if count else 0

    # Word count distribution
    wc_stats = query(conn, """
        SELECT word_count, language FROM responses
        WHERE source='survey'
    """)
    if wc_stats:
        for lang in ["zh", "en", "de"]:
            lang_words = [r["word_count"] for r in wc_stats if r["language"] == lang]
            if lang_words:
                stats[f"avg_words_{lang}"] = round(sum(lang_words) / len(lang_words), 1)
                stats[f"min_words_{lang}"] = min(lang_words)
                stats[f"max_words_{lang}"] = max(lang_words)

    # Language distribution
    lang_dist = query(conn, """
        SELECT language, COUNT(*) as c FROM responses
        WHERE source='survey' GROUP BY language
    """)
    stats["by_language"] = {r["language"]: r["c"] for r in lang_dist}

    # Student coverage
    students = query(conn, """
        SELECT student_id, COUNT(DISTINCT language) as lang_count,
               COUNT(*) as resp_count
        FROM responses WHERE source='survey'
        GROUP BY student_id
    """)
    stats["students"] = len(students)
    stats["complete_students"] = sum(1 for s in students if s["lang_count"] >= 2)

    return stats


def fix_language_tags(conn, verbose: bool = False) -> int:
    """
    Re-check and fix language tags based on actual content.
    Returns number of fixes.
    """
    responses = query(conn, """
        SELECT response_id, answer_text, language FROM responses
        WHERE source='survey'
    """)

    fixes = 0
    for r in responses:
        detected = detect_answer_language(r["answer_text"])
        if detected != r["language"] and detected != "unknown":
            if verbose:
                print(f"  Fix: {r['response_id']} {r['language']} -> {detected}")
            conn.execute(
                "UPDATE responses SET language=? WHERE response_id=?",
                (detected, r["response_id"])
            )
            fixes += 1

    conn.commit()
    return fixes


def mark_short_responses(conn, min_words: int = MIN_WORD_COUNT) -> int:
    """Mark responses that are too short."""
    responses = query(conn, """
        SELECT response_id, word_count FROM responses
        WHERE source='survey' AND quality_flag='ok'
    """)

    count = 0
    for r in responses:
        if r["word_count"] < min_words:
            conn.execute(
                "UPDATE responses SET quality_flag='short' WHERE response_id=?",
                (r["response_id"],)
            )
            count += 1

    conn.commit()
    return count


def generate_cleaning_report(stats: dict, dupes: list, fixes: int, short_marked: int) -> str:
    """Generate a markdown cleaning report."""
    md = []
    md.append("# Survey Data Cleaning Report\n")
    md.append(f"Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    md.append("## Overview\n")
    md.append(f"| Metric | Value |\n")
    md.append(f"|--------|-------|\n")
    md.append(f"| Total responses | {stats.get('total', 0)} |\n")
    md.append(f"| Students | {stats.get('students', 0)} |\n")
    md.append(f"| Complete (≥2 languages) | {stats.get('complete_students', 0)} |\n")

    md.append("\n## Quality Flags\n")
    md.append(f"| Flag | Count |\n")
    md.append(f"|------|-------|\n")
    md.append(f"| ok | {stats.get('flag_ok', 0)} |\n")
    md.append(f"| short | {stats.get('flag_short', 0)} |\n")
    md.append(f"| empty | {stats.get('flag_empty', 0)} |\n")

    md.append("\n## Language Distribution\n")
    for lang, count in stats.get("by_language", {}).items():
        md.append(f"- **{lang}**: {count} responses\n")

    md.append("\n## Word Count Statistics\n")
    for lang in ["zh", "en", "de"]:
        avg = stats.get(f"avg_words_{lang}", "N/A")
        mn = stats.get(f"min_words_{lang}", "N/A")
        mx = stats.get(f"max_words_{lang}", "N/A")
        md.append(f"- **{lang}**: avg={avg}, min={mn}, max={mx}\n")

    if dupes:
        md.append(f"\n## Duplicates Found: {len(dupes)}\n")
        for d in dupes[:10]:
            md.append(f"- {d['student_id']} Q{d['question_id']} ({d['language']}): {d['cnt']}x\n")

    md.append(f"\n## Cleaning Actions\n")
    md.append(f"- Language tags fixed: {fixes}\n")
    md.append(f"- Short responses marked: {short_marked}\n")

    return "\n".join(md)


def run_cleaning(verbose: bool = False):
    """Run the full cleaning pipeline."""
    print(f"\n{'='*60}")
    print(f"  Survey Data Cleaning")
    print(f"{'='*60}\n")

    conn = get_connection()

    # Step 1: Check quality
    print("  Step 1: Checking quality...")
    stats = check_quality(conn)
    print(f"    Total: {stats.get('total', 0)} responses")
    print(f"    Students: {stats.get('students', 0)}")

    # Step 2: Fix language tags
    print("\n  Step 2: Fixing language tags...")
    fixes = fix_language_tags(conn, verbose=verbose)
    print(f"    Fixed: {fixes}")

    # Step 3: Mark short responses
    print("\n  Step 3: Marking short responses...")
    short_marked = mark_short_responses(conn)
    print(f"    Marked: {short_marked}")

    # Step 4: Check duplicates
    print("\n  Step 4: Checking duplicates...")
    dupes = check_duplicates(conn)
    print(f"    Found: {len(dupes)}")

    # Re-check quality after cleaning
    stats_after = check_quality(conn)

    # Generate report
    report = generate_cleaning_report(stats_after, dupes, fixes, short_marked)
    from config import REPORT_DIR
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "cleaning_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\n  Report saved: {report_path}")

    conn.close()
    print(f"\n{'='*60}")
    print(f"  Cleaning complete")
    print(f"{'='*60}\n")

    return stats_after


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Clean survey data")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()
    run_cleaning(verbose=args.verbose)


if __name__ == "__main__":
    main()
