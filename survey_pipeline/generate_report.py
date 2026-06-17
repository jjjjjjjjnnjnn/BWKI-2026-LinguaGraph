"""
Survey Pipeline — Report Generation
=====================================
Generate comprehensive analysis report from survey data.

Usage:
    python generate_report.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from db_utils import get_connection, query, query_one

from config import REPORT_DIR


def get_data_summary(conn) -> dict:
    """Get high-level data summary."""
    summary = {}

    # Students
    students = query(conn, """
        SELECT student_id, native_lang FROM students
        WHERE student_id LIKE 'S%'
        ORDER BY student_id
    """)
    summary["students"] = students
    summary["student_count"] = len(students)

    # Responses by source
    sources = query(conn, """
        SELECT source, COUNT(*) as c FROM responses GROUP BY source
    """)
    summary["by_source"] = {r["source"]: r["c"] for r in sources}

    # Survey responses
    survey_count = query_one(conn, """
        SELECT COUNT(*) as c FROM responses WHERE source='survey'
    """)
    summary["survey_responses"] = survey_count["c"] if survey_count else 0

    # By language
    by_lang = query(conn, """
        SELECT language, COUNT(*) as c FROM responses
        WHERE source='survey' GROUP BY language
    """)
    summary["by_language"] = {r["language"]: r["c"] for r in by_lang}

    # Quality
    quality = query(conn, """
        SELECT quality_flag, COUNT(*) as c FROM responses
        WHERE source='survey' GROUP BY quality_flag
    """)
    summary["by_quality"] = {r["quality_flag"]: r["c"] for r in quality}

    # Extractions
    ext_count = query_one(conn, """
        SELECT COUNT(*) as c FROM extractions WHERE extraction_type='survey'
    """)
    summary["extractions"] = ext_count["c"] if ext_count else 0

    # LDS results
    lds_count = query_one(conn, """
        SELECT COUNT(*) as c FROM cross_language_analysis
    """)
    summary["lds_results"] = lds_count["c"] if lds_count else 0

    return summary


def get_concept_frequency(conn) -> dict:
    """Get most frequent concepts across all extractions."""
    extractions = query(conn, """
        SELECT e.concepts, r.language
        FROM extractions e
        JOIN responses r ON e.response_id = r.response_id
        WHERE r.source = 'survey' AND e.extraction_type = 'survey'
    """)

    by_lang = defaultdict(Counter)
    for ext in extractions:
        concepts = json.loads(ext["concepts"]) if isinstance(ext["concepts"], str) else ext["concepts"]
        lang = ext["language"]
        for c in concepts:
            if isinstance(c, str):
                by_lang[lang][c] += 1

    return dict(by_lang)


def get_lds_results(conn) -> dict:
    """Get LDS results from database."""
    results = query(conn, """
        SELECT student_id, topic, lang_pair, lcd_score, similarity
        FROM cross_language_analysis
        ORDER BY student_id, topic, lang_pair
    """)
    return results


def generate_report():
    """Generate the full analysis report."""
    print(f"\n{'='*60}")
    print(f"  Generating Survey Analysis Report")
    print(f"{'='*60}\n")

    conn = get_connection()
    summary = get_data_summary(conn)
    concepts = get_concept_frequency(conn)
    lds = get_lds_results(conn)
    conn.close()

    md = []
    md.append("# LinguaGraph — Survey Analysis Report\n")
    md.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    md.append("---\n")

    # === Section 1: Data Overview ===
    md.append("## 1. Data Overview\n")
    md.append(f"| Metric | Value |\n")
    md.append(f"|--------|-------|\n")
    md.append(f"| Students | {summary['student_count']} |\n")
    md.append(f"| Survey responses | {summary['survey_responses']} |\n")
    md.append(f"| Extractions | {summary['extractions']} |\n")
    md.append(f"| LDS results | {summary['lds_results']} |\n")

    md.append("\n### Language Distribution\n")
    for lang, count in summary.get("by_language", {}).items():
        md.append(f"- **{lang}**: {count} responses\n")

    md.append("\n### Quality Flags\n")
    for flag, count in summary.get("by_quality", {}).items():
        md.append(f"- **{flag}**: {count}\n")

    # === Section 2: Student Profiles ===
    md.append("\n## 2. Student Profiles\n")
    md.append("| ID | Native Language | Responses |\n")
    md.append("|----|----------------|-----------|\n")
    for s in summary["students"]:
        md.append(f"| {s['student_id']} | {s['native_lang']} | — |\n")

    # === Section 3: Concept Frequency ===
    md.append("\n## 3. Concept Frequency by Language\n")

    for lang in ["zh", "en", "de"]:
        if lang in concepts:
            md.append(f"### {lang.upper()}\n")
            top = concepts[lang].most_common(15)
            md.append("| Concept | Frequency |\n")
            md.append("|---------|----------|\n")
            for c, count in top:
                md.append(f"| {c} | {count} |\n")

    # === Section 4: LDS Results ===
    md.append("\n## 4. Language Drift Score (LDS)\n")

    if lds:
        md.append("| Student | Topic | Pair | LCD | Similarity |\n")
        md.append("|---------|-------|------|-----|------------|\n")
        for r in lds[:30]:
            lcd = f"{r['lcd_score']:.4f}" if r['lcd_score'] else "N/A"
            sim = f"{r['similarity']:.4f}" if r['similarity'] else "N/A"
            md.append(f"| {r['student_id']} | {r['topic']} | {r['lang_pair']} | {lcd} | {sim} |\n")
        if len(lds) > 30:
            md.append(f"\n*... and {len(lds) - 30} more results*\n")
    else:
        md.append("No LDS results computed yet. Run `run_lds.py` first.\n")

    # === Section 5: Next Steps ===
    md.append("\n## 5. Next Steps\n")
    md.append("- [ ] Complete pilot data collection (N=9)\n")
    md.append("- [ ] Run LLM annotation on all responses\n")
    md.append("- [ ] Compute LDS and compare with simulation baseline\n")
    md.append("- [ ] Generate comparison figures\n")

    # Save
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "survey_analysis_report.md"
    report_path.write_text("\n".join(md), encoding="utf-8")
    print(f"  Report saved: {report_path}")

    print(f"\n{'='*60}")
    print(f"  Report generation complete")
    print(f"{'='*60}\n")


def main():
    generate_report()


if __name__ == "__main__":
    main()
