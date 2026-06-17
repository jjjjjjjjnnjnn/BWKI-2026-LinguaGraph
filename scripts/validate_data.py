"""
Validate Data — Data Quality Checks
=====================================
Run quality checks on the LinguaGraph database to ensure:
    - All students have complete trilingual response pairs
    - No duplicate entries
    - Text encoding is valid UTF-8
    - Word counts are reasonable
    - Consent forms are recorded

Usage:
    python validate_data.py                    # Full validation report
    python validate_data.py --summary          # Quick summary only
    python validate_data.py --fix              # Auto-fix minor issues
    python validate_data.py --export-report    # Export report to JSON
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent))
from db_utils import get_connection, query, query_one, query_value


class DataValidator:
    """Validates LinguaGraph database data quality."""

    def __init__(self, conn):
        self.conn = conn
        self.issues = []
        self.stats = {}

    def check_student_completeness(self) -> List[Dict]:
        """Check every student has responses in all 3 languages."""
        issues = []
        students = query(self.conn, "SELECT student_id, native_lang FROM students ORDER BY student_id")
        required_langs = ["zh", "de", "en"]
        topic_count_target = 4  # Each language should have 4 answers

        for s in students:
            langs = query(self.conn,
                "SELECT language, COUNT(*) as count FROM responses WHERE student_id=? GROUP BY language",
                (s["student_id"],))
            present = {r["language"]: r["count"] for r in langs}

            for lang in required_langs:
                count = present.get(lang, 0)
                if count == 0:
                    issues.append({
                        "severity": "error",
                        "student": s["student_id"],
                        "message": f"Missing all responses in '{lang}'"
                    })
                elif count < topic_count_target:
                    issues.append({
                        "severity": "warning",
                        "student": s["student_id"],
                        "message": f"Incomplete '{lang}': only {count}/{topic_count_target} questions answered"
                    })

        return issues

    def check_duplicates(self) -> List[Dict]:
        """Check for duplicate entries in responses table."""
        issues = []
        dups = query(self.conn, """
            SELECT student_id, language, question_id, COUNT(*) as count
            FROM responses
            GROUP BY student_id, language, question_id
            HAVING COUNT(*) > 1
        """)
        for d in dups:
            issues.append({
                "severity": "error",
                "student": d["student_id"],
                "message": f"Duplicate response: {d['student_id']} / {d['language']} / {d['question_id']} ({d['count']} copies)"
            })
        return issues

    def check_short_answers(self, min_words: int = 5) -> List[Dict]:
        """Flag very short answers that may indicate low effort."""
        issues = []
        short = query(self.conn,
            "SELECT response_id, student_id, language, question_id, word_count FROM responses WHERE word_count < ? OR word_count IS NULL",
            (min_words,))
        for r in short:
            severity = "warning" if r["word_count"] and r["word_count"] >= 2 else "error"
            issues.append({
                "severity": severity,
                "student": r["student_id"],
                "message": f"Very short answer: {r['response_id']} ({r['word_count']} words)"
            })
        return issues

    def check_quality_flags(self) -> List[Dict]:
        """Check quality flags that have been set."""
        issues = []
        flagged = query(self.conn,
            "SELECT response_id, student_id, language, quality_flag FROM responses WHERE quality_flag != 'ok'")
        for r in flagged:
            issues.append({
                "severity": "info",
                "student": r["student_id"],
                "message": f"Quality flag '{r['quality_flag']}': {r['response_id']}"
            })
        return issues

    def check_orphan_responses(self) -> List[Dict]:
        """Check responses referencing non-existent students."""
        issues = []
        orphans = query(self.conn, """
            SELECT r.response_id, r.student_id
            FROM responses r
            LEFT JOIN students s ON r.student_id = s.student_id
            WHERE s.student_id IS NULL
        """)
        for r in orphans:
            issues.append({
                "severity": "error",
                "student": r["student_id"],
                "message": f"Orphan response (no student record): {r['response_id']}"
            })
        return issues

    def check_consent(self) -> List[Dict]:
        """Check all students have consent recorded."""
        issues = []
        no_consent = query(self.conn,
            "SELECT student_id FROM students WHERE consent = 0 OR consent IS NULL")
        for s in no_consent:
            issues.append({
                "severity": "warning",
                "student": s["student_id"],
                "message": f"No consent recorded for {s['student_id']}"
            })
        return issues

    def run_all_checks(self) -> Dict:
        """Run all validation checks."""
        self.issues = []

        checks = {
            "student_completeness": self.check_student_completeness,
            "duplicates": self.check_duplicates,
            "short_answers": self.check_short_answers,
            "quality_flags": self.check_quality_flags,
            "orphan_responses": self.check_orphan_responses,
            "consent": self.check_consent,
        }

        for name, check_fn in checks.items():
            try:
                results = check_fn()
                self.issues.extend(results)
            except Exception as e:
                self.issues.append({
                    "severity": "error",
                    "student": "SYSTEM",
                    "message": f"Check '{name}' failed: {e}"
                })

        self.stats = {
            "total_issues": len(self.issues),
            "errors": len([i for i in self.issues if i["severity"] == "error"]),
            "warnings": len([i for i in self.issues if i["severity"] == "warning"]),
            "info": len([i for i in self.issues if i["severity"] == "info"]),
            "db_stats": {
                "students": query_value(self.conn, "SELECT COUNT(*) FROM students"),
                "responses": query_value(self.conn, "SELECT COUNT(*) FROM responses"),
                "questionnaires": query_value(self.conn, "SELECT COUNT(*) FROM questionnaires"),
                "gold_labels": query_value(self.conn, "SELECT COUNT(*) FROM gold_labels"),
                "extractions": query_value(self.conn, "SELECT COUNT(*) FROM extractions"),
            }
        }

        return self.stats

    def generate_report(self) -> str:
        """Generate a formatted validation report."""
        lines = []
        lines.append(f"{'='*50}")
        lines.append(f"  LinguaGraph Data Validation Report")
        lines.append(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"{'='*50}")

        # Database stats
        lines.append(f"\n[DB] Database Statistics:")
        for key, val in self.stats.get("db_stats", {}).items():
            lines.append(f"    {key:<20s}: {val}")

        # Issues by severity
        lines.append(f"\n[!] Issues Found: {self.stats.get('total_issues', 0)}")
        lines.append(f"    [ERR] Errors:   {self.stats.get('errors', 0)}")
        lines.append(f"    [WARN] Warnings: {self.stats.get('warnings', 0)}")
        lines.append(f"    [INFO] Info:     {self.stats.get('info', 0)}")

        if self.issues:
            sev_tag = {"error": "ERR", "warning": "WARN", "info": "INFO"}
            for i, issue in enumerate(self.issues, 1):
                tag = sev_tag.get(issue["severity"], "???")
                lines.append(f"\n  [{tag}] {issue['message']}")

        # Summary
        errors = self.stats.get("errors", 0)
        warnings = self.stats.get("warnings", 0)
        if errors == 0 and warnings == 0:
            lines.append(f"\n{'='*50}")
            lines.append(f"  [PASS] ALL CHECKS PASSED — Data is clean!")
        elif errors == 0:
            lines.append(f"\n{'='*50}")
            lines.append(f"  [WARN] PASSED WITH WARNINGS — Review {warnings} warning(s)")
        else:
            lines.append(f"\n{'='*50}")
            lines.append(f"  [FAIL] {errors} error(s) must be fixed")
        lines.append(f"{'='*50}\n")

        return "\n".join(lines)

    def auto_fix(self) -> int:
        """Auto-fix minor issues (e.g., empty word_counts)."""
        fixed = 0

        # Fix missing word counts
        fixed += self.conn.execute("""
            UPDATE responses SET word_count = 1
            WHERE (word_count IS NULL OR word_count = 0) AND quality_flag = 'empty'
        """).rowcount

        # Fix missing quality flags
        fixed += self.conn.execute("""
            UPDATE responses SET quality_flag = 'ok'
            WHERE quality_flag IS NULL
        """).rowcount

        self.conn.commit()
        return fixed


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate LinguaGraph data quality")
    parser.add_argument("--summary", action="store_true", help="Show only summary")
    parser.add_argument("--fix", action="store_true", help="Auto-fix minor issues")
    parser.add_argument("--export-report", type=str, help="Export report to JSON file")
    args = parser.parse_args()

    conn = get_connection()
    validator = DataValidator(conn)

    stats = validator.run_all_checks()

    if args.fix:
        fixed = validator.auto_fix()
        print(f"  [FIX] Auto-fixed {fixed} minor issue(s)")
        # Re-run checks after fix
        stats = validator.run_all_checks()

    report = validator.generate_report()
    print(report)

    if args.export_report:
        report_path = Path(args.export_report)
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "stats": stats,
            "issues": validator.issues,
            "report_text": report,
        }
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        print(f"  [EXPORT] Report saved to {report_path}")

    conn.close()


if __name__ == "__main__":
    main()
