#!/usr/bin/env python3
"""
LinguaGraph Pilot Results Pipeline
====================================
Single-command pipeline: DB → Summary → Quality Report → LDS-ready Templates.

When DE/EN data arrives:
    python scripts/pilot_pipeline.py
    → All tables, figures, and reports regenerated automatically.

Usage:
    python scripts/pilot_pipeline.py                  # Full pipeline (default)
    python scripts/pilot_pipeline.py --summary         # Participant summary only
    python scripts/pilot_pipeline.py --quality         # Quality report only
    python scripts/pilot_pipeline.py --lds-template    # LDS report template
    python scripts/pilot_pipeline.py --all             # Same as default
    python scripts/pilot_pipeline.py --watch           # Re-run every 60s (for live data)
"""

import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from db_utils import get_connection, query

# === Paths ===
OUTPUT_DIR = Path(__file__).parent.parent / "results"
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"


def ensure_dirs():
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 1. Participant Summary
# ============================================================

def export_participant_summary() -> Path:
    """Generate participant_summary.csv — demographics overview."""
    conn = get_connection()
    students = query(conn, """
        SELECT s.student_id, s.native_lang, s.age_group, s.school_lang,
               s.other_langs, s.years_in_germany, s.consent,
               COUNT(r.response_id) as response_count
        FROM students s
        LEFT JOIN responses r ON s.student_id = r.student_id
        GROUP BY s.student_id
        ORDER BY s.student_id
    """)
    conn.close()

    output_path = TABLES_DIR / "participant_summary.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "student_id", "native_lang", "age_group", "school_lang",
            "other_langs", "years_in_germany", "consent", "response_count",
        ])
        for s in students:
            writer.writerow([
                s["student_id"], s["native_lang"], s["age_group"],
                s["school_lang"], s["other_langs"], s["years_in_germany"],
                s["consent"], s["response_count"],
            ])

    print(f"  [OK] Participant summary: {output_path}")
    return output_path


def export_participant_summary_md() -> str:
    """Generate participant_summary.md — human-readable."""
    conn = get_connection()
    students = query(conn, """
        SELECT s.student_id, s.native_lang, s.age_group, s.consent,
               COUNT(r.response_id) as response_count
        FROM students s
        LEFT JOIN responses r ON s.student_id = r.student_id
        GROUP BY s.student_id
        ORDER BY s.student_id
    """)
    conn.close()

    lines = ["## Participant Summary\n"]
    lines.append("| ID | Lang | Age | Consent | Responses |")
    lines.append("|----|:----:|:---:|:-------:|:---------:|")
    for s in students:
        consent_str = "✅" if s["consent"] == 1 else "❌"
        lines.append(f"| {s['student_id']} | {s['native_lang']} | {s['age_group'] or '—'} | {consent_str} | {s['response_count']} |")

    # Aggregate
    by_lang = Counter(s["native_lang"] for s in students)
    lines.append(f"\n**Total participants:** {len(students)}")
    for lang, count in sorted(by_lang.items()):
        lines.append(f"- {lang}: {count}")

    report = "\n".join(lines)
    output_path = TABLES_DIR / "participant_summary.md"
    output_path.write_text(report, encoding="utf-8")
    print(f"  [OK] Participant summary (MD): {output_path}")
    return report


# ============================================================
# 2. Quality Report
# ============================================================

def export_quality_report() -> str:
    """Generate quality_report.md — data quality assessment."""
    conn = get_connection()
    pilot_responses = query(conn, """
        SELECT r.student_id, r.language, r.question_id,
               r.answer_text, r.word_count
        FROM responses r
        WHERE r.source = 'pilot'
        ORDER BY r.student_id, r.language, r.question_id
    """)
    students = query(conn, "SELECT * FROM students WHERE student_id LIKE 'P%' ORDER BY student_id")
    conn.close()

    if not pilot_responses:
        return "No pilot data found."

    # Basic stats
    n_participants = len(students)
    n_responses = len(pilot_responses)
    expected_total = n_participants * 10  # 10 questions per participant

    by_lang = Counter(r["language"] for r in pilot_responses)
    by_student = Counter(r["student_id"] for r in pilot_responses)

    completion_rate = n_responses / max(expected_total, 1)

    # Word count stats
    word_counts = [r["word_count"] for r in pilot_responses]
    avg_words = sum(word_counts) / max(len(word_counts), 1)
    min_words = min(word_counts) if word_counts else 0
    max_words = max(word_counts) if word_counts else 0

    # Missing data
    missing = max(0, expected_total - n_responses)

    # Short answers (< 5 chars)
    short_answers = [r for r in pilot_responses if len(r["answer_text"].strip()) < 5]
    short_rate = len(short_answers) / max(n_responses, 1)

    # Language mixing detection
    import re
    mixed = []
    for r in pilot_responses:
        has_cn = bool(re.search(r'[一-鿿]', r["answer_text"]))
        has_en = bool(re.search(r'[a-zA-Z]{2,}', r["answer_text"]))
        if has_cn and has_en:
            mixed.append(r)

    lines = ["# LinguaGraph — Pilot Quality Report\n"]
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    lines.append(f"**Snapshot:** pilot_v1 (frozen)\n")

    lines.append("## 1. Completion\n")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|:-----:|")
    lines.append(f"| Participants | {n_participants} |")
    lines.append(f"| Expected responses | {expected_total} |")
    lines.append(f"| Actual responses | {n_responses} |")
    lines.append(f"| Completion rate | {completion_rate:.1%} |")
    lines.append(f"| Missing answers | {missing} |")

    lines.append("\n## 2. Per-Participant\n")
    lines.append("| ID | Lang | Got | Expected | Complete |")
    lines.append("|----|:----:|:---:|:--------:|:--------:|")
    for s in students:
        sid = s["student_id"]
        got = by_student.get(sid, 0)
        exp = 10
        status = "✅" if got == exp else "⚠️"
        lines.append(f"| {sid} | {s['native_lang']} | {got} | {exp} | {status} |")

    lines.append("\n## 3. Language Distribution\n")
    lines.append(f"| Language | Responses |")
    lines.append(f"|:--------:|:---------:|")
    for lang, count in sorted(by_lang.items()):
        pct = count / n_responses * 100
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        lines.append(f"| {lang} | {count} ({pct:.0f}%) {bar} |")

    lines.append("\n## 4. Response Quality\n")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|:-----:|")
    lines.append(f"| Average word count | {avg_words:.1f} |")
    lines.append(f"| Min word count | {min_words} |")
    lines.append(f"| Max word count | {max_words} |")
    lines.append(f"| Short answers (<5 chars) | {len(short_answers)} ({short_rate:.1%}) |")
    lines.append(f"| Language-mixed answers | {len(mixed)} ({len(mixed)/n_responses:.1%}) |")

    if short_answers:
        lines.append("\n### Short Answers:\n")
        for r in short_answers[:5]:
            lines.append(f"- {r['student_id']} {r['question_id']}: \"{r['answer_text'][:50]}\"")

    # Known issues
    lines.append("\n## 5. Known Issues\n")
    issues = [
        "P006 q12: Residual characters from previous question ('杯子zai')",
        "P003 q12: Incomplete translation (missing 'through living room')",
        "P003 q16: Metaphorical interpretation deviating from source",
        "q14: 'brought forward' systematically misunderstood by 4/8 participants",
    ]
    for issue in issues:
        lines.append(f"- {issue}")

    lines.append("\n## 6. Lessons Learned\n")
    lessons = [
        "Question order matters: P006 q12 contamination suggests spacing/attention issues",
        "Translation difficulty varies: 'brought forward' widely misinterpreted",
        "Age range matters: 10-55 spanning 4 decades enables generational analysis",
        "Instruction clarity: q3 (12_year_old) translation was uniquely creative",
    ]
    for lesson in lessons:
        lines.append(f"- {lesson}")

    lines.append("\n## 7. Planned Improvements\n")
    improvements = [
        "Separate screens per question (prevent carryover contamination)",
        "Add example translations for tricky phrases (e.g., 'brought forward')",
        "Standardize age format before collection",
        "Collect response time metadata if platform allows",
    ]
    for imp in improvements:
        lines.append(f"- {imp}")

    report = "\n".join(lines)

    output_path = Path(__file__).parent.parent / "docs" / "pilot_quality_report.md"
    output_path.write_text(report, encoding="utf-8")
    print(f"  [OK] Quality report: {output_path}")
    return report


# ============================================================
# 3. LDS Report Template (pre-filled when DE/EN data arrives)
# ============================================================

def export_lds_template() -> str:
    """Generate lds_report_template.md — ready-to-fill when DE/EN data arrives."""
    conn = get_connection()
    students = query(conn, "SELECT student_id, native_lang FROM students WHERE student_id LIKE 'P%' ORDER BY student_id")
    existing_analyses = query(conn, "SELECT COUNT(*) as c FROM cross_language_analysis")
    conn.close()

    n_analyses = existing_analyses[0]["c"] if existing_analyses else 0

    zh_only = [s for s in students if s["native_lang"] == "zh"]
    de_count = len([s for s in students if s["native_lang"] == "de"])
    en_count = len([s for s in students if s["native_lang"] == "en"])

    lines = ["# LinguaGraph — Cross-Language LDS Results\n"]
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    lines.append("## Data Availability\n")
    lines.append(f"| Language | Participants | Status |")
    lines.append(f"|:--------:|:------------:|:------:|")
    lines.append(f"| ZH | {len(zh_only)} | ✅ Collected |")
    lines.append(f"| DE | {de_count} | {'⏳ Pending' if de_count == 0 else '✅ Collected'} |")
    lines.append(f"| EN | {en_count} | {'⏳ Pending' if en_count == 0 else '✅ Collected'} |")
    lines.append(f"\n**Cross-language analyses in DB:** {n_analyses}\n")

    lines.append("## LDS Results Per Language Pair\n")
    lines.append("| Language Pair | Mean LDS | Std | N | 95% CI |")
    lines.append("|:------------:|:--------:|:---:|:-:|:------:|")
    if n_analyses > 0:
        conn = get_connection()
        for pair in ["zh-de", "zh-en", "de-en"]:
            rows = query(conn, """
                SELECT lcd_score FROM cross_language_analysis WHERE lang_pair = ?
            """, (pair,))
            if rows:
                scores = [r["lcd_score"] for r in rows]
                mean = sum(scores) / len(scores)
                std = (sum((s - mean) ** 2 for s in scores) / len(scores)) ** 0.5
                ci_95 = 1.96 * std / (len(scores) ** 0.5)
                lines.append(f"| {pair} | {mean:.4f} | {std:.4f} | {len(scores)} | [{mean-ci_95:.4f}, {mean+ci_95:.4f}] |")
            else:
                lines.append(f"| {pair} | — | — | 0 | — |")
        conn.close()
    else:
        for pair in ["zh-de", "zh-en", "de-en"]:
            lines.append(f"| {pair} | *Awaiting DE/EN data* | — | 0 | — |")

    lines.append("\n## LDS By Topic\n")
    lines.append("| Topic | ZH-DE | ZH-EN | DE-EN |")
    lines.append("|-------|:-----:|:-----:|:-----:|")
    topics = ["freedom", "justice", "responsibility", "success", "home"]
    for t in topics:
        lines.append(f"| {t.capitalize()} | — | — | — |")

    lines.append("\n## Figures\n")
    lines.append("```")
    lines.append("Figure 1: LDS distribution by language pair → results/figures/figure1_lds_distribution.png")
    lines.append("Figure 2: LDS by topic heatmap → results/figures/figure2_lds_heatmap.png")
    lines.append("Figure 3: Topic comparison → results/figures/figure3_topic_comparison.png")
    lines.append("```")

    lines.append("\n---\n")
    lines.append("*Template auto-generated. Fill when DE/EN data arrives.*\n")

    report = "\n".join(lines)
    output_path = TABLES_DIR / "lds_report_template.md"
    output_path.write_text(report, encoding="utf-8")
    print(f"  [OK] LDS report template: {output_path}")
    return report


# ============================================================
# 4. Full Pipeline Report
# ============================================================

def export_results_summary():
    """Generate a single-page results summary linking all outputs."""
    lines = []
    lines.append("# LinguaGraph — Results Summary\n")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    lines.append("## Outputs\n")
    lines.append("| File | Description |")
    lines.append("|------|-------------|")
    lines.append("| `tables/participant_summary.csv` | Participant demographics (CSV) |")
    lines.append("| `tables/participant_summary.md` | Participant demographics (MD) |")
    lines.append("| `docs/pilot_quality_report.md` | Data quality assessment |")
    lines.append("| `tables/lds_report_template.md` | LDS results (ready when DE/EN arrives) |")
    lines.append("| `tables/table1_demographics.md` | Table 1: Full demographics |")
    lines.append("| `tables/table2_lds_by_topic.md` | Table 2: LDS by topic |")
    lines.append("| `figures/figure1_lds_distribution.png` | Figure 1: LDS distribution |")
    lines.append("| `figures/figure3_topic_comparison.png` | Figure 3: Topic comparison |")

    report = "\n".join(lines)
    output_path = OUTPUT_DIR / "RESULTS_SUMMARY.md"
    output_path.write_text(report, encoding="utf-8")
    print(f"  [OK] Results summary: {output_path}")


# ============================================================
# Main
# ============================================================

def run_all():
    """Run the complete pipeline."""
    print(f"\n{'='*60}")
    print(f"  LinguaGraph — Pilot Results Pipeline")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    ensure_dirs()

    print("1. Participant Summary...")
    export_participant_summary()
    export_participant_summary_md()

    print("\n2. Quality Report...")
    export_quality_report()

    print("\n3. LDS Report Template...")
    export_lds_template()

    print("\n4. Results Summary...")
    export_results_summary()

    print(f"\n{'='*60}")
    print(f"  Pipeline complete. All outputs in results/ and docs/")
    print(f"{'='*60}\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph Pilot Results Pipeline")
    parser.add_argument("--summary", action="store_true", help="Participant summary only")
    parser.add_argument("--quality", action="store_true", help="Quality report only")
    parser.add_argument("--lds-template", action="store_true", help="LDS report template only")
    parser.add_argument("--all", action="store_true", help="Run all (default)")
    args = parser.parse_args()

    ensure_dirs()

    if args.summary:
        export_participant_summary()
        export_participant_summary_md()
    elif args.quality:
        export_quality_report()
    elif args.lds_template:
        export_lds_template()
    else:
        run_all()


if __name__ == "__main__":
    main()
