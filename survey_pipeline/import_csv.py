"""
Survey Pipeline — CSV Import
==============================
Import Google Forms CSV export into linguaGraph database.

Usage:
    python import_csv.py <csv_file>
    python import_csv.py <csv_file> --dry-run
"""

import csv
import json
import sys
import re
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from db_utils import get_connection, insert, query_one

from config import (
    QUESTION_TOPIC_MAP, QUESTION_ID_MAP, WORD_QUESTIONS,
    NATIVE_LANG_MAP, MIN_WORD_COUNT, MIN_ANSWER_LENGTH
)


def parse_timestamp(ts_str: str) -> str:
    """Parse Google Forms timestamp to ISO format."""
    try:
        dt = datetime.strptime(ts_str, "%m/%d/%Y %H:%M:%S")
        return dt.isoformat()
    except (ValueError, TypeError):
        return datetime.now().isoformat()


def detect_language(answer: str, native_lang: str) -> str:
    """
    Detect the language of an answer.
    Simple heuristic based on character ranges.
    """
    if not answer:
        return native_lang

    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', answer))
    total_chars = len(answer.strip())

    if total_chars == 0:
        return native_lang

    chinese_ratio = chinese_chars / total_chars

    if chinese_ratio > 0.3:
        return "zh"
    elif any(c in answer for c in "äöüßÄÖÜ"):
        return "de"
    else:
        return native_lang


def count_words(answer: str, language: str) -> int:
    """Count words in answer, handling Chinese differently."""
    if not answer:
        return 0
    if language == "zh":
        # Count characters (excluding spaces/punctuation)
        return len(re.findall(r'[\u4e00-\u9fff]', answer))
    else:
        return len(answer.split())


def import_csv(csv_path: str, dry_run: bool = False) -> dict:
    """
    Import a Google Forms CSV export into the database.

    Returns dict with import statistics.
    """
    csv_file = Path(csv_path)
    if not csv_file.exists():
        print(f"  [ERROR] File not found: {csv_path}")
        return {"error": "file not found"}

    print(f"\n{'='*60}")
    print(f"  Importing: {csv_file.name}")
    print(f"{'='*60}\n")

    # Read CSV
    with open(csv_file, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)

    print(f"  Headers: {len(headers)} columns")
    print(f"  Rows: {len(rows)} responses")

    # Parse headers to find question columns by content keywords
    # IMPORTANT: Process demographics FIRST, then questions.
    # Prevent question headers (which may contain keywords like "native language")
    # from overwriting demographics column mapping.
    question_cols = {}
    demographics_found = {}

    for i, h in enumerate(headers):
        h_lower = h.lower().strip()
        # Demographics (processed first — matches cannot be overwritten)
        if h_lower in ("what is your native language?", "muttersprache", "native language"):
            demographics_found["native_lang"] = i
        elif h_lower in ("your age", "alter", "age"):
            demographics_found["age"] = i
        elif h_lower in ("your highest education level", "education", "bildung"):
            demographics_found["education"] = i

    # Copy demographics to question_cols (locked, won't be overwritten)
    question_cols.update(demographics_found)

    # Now process question headers
    for i, h in enumerate(headers):
        h_lower = h.lower().strip()
        # Skip demographics columns (already mapped)
        if i in demographics_found.values():
            continue
        # Success questions
        elif "erfolg" in h_lower or "success" in h_lower:
            if "worter" in h_lower or "words" in h_lower or "5 worter" in h_lower:
                question_cols[5] = i  # word association
            elif "schuler" in h_lower or "student" in h_lower or "perfekte" in h_lower:
                question_cols[6] = i  # scenario
            elif 4 not in question_cols:
                question_cols[4] = i  # definition
        # Responsibility questions
        elif "verantwortung" in h_lower or "responsibility" in h_lower:
            if "beziehung" in h_lower or "relationship" in h_lower:
                question_cols[7] = i
            elif "worter" in h_lower or "words" in h_lower:
                question_cols[8] = i
            elif "person" in h_lower and ("hilfe" in h_lower or "help" in h_lower):
                question_cols[9] = i
        # Freedom questions
        elif "freiheit" in h_lower or "freedom" in h_lower:
            if "grenzen" in h_lower or "boundaries" in h_lower or "boundary" in h_lower:
                question_cols[10] = i
            elif "worter" in h_lower or "words" in h_lower:
                question_cols[11] = i
            elif "schadet" in h_lower or "harms" in h_lower or "harm" in h_lower:
                question_cols[12] = i
        # Home questions
        elif "zuhause" in h_lower or "home" in h_lower:
            if "unterschied" in h_lower or "difference" in h_lower:
                question_cols[13] = i
            elif "worter" in h_lower or "words" in h_lower:
                question_cols[14] = i
            elif "villa" in h_lower or "mansion" in h_lower or "gefuhl" in h_lower or "warmth" in h_lower:
                question_cols[15] = i
        # Justice questions
        elif "gerechtigkeit" in h_lower or "justice" in h_lower:
            if "bedeutet" in h_lower or "means" in h_lower or "beschreiben" in h_lower or "describe" in h_lower:
                question_cols[16] = i
            elif "worter" in h_lower or "words" in h_lower:
                question_cols[17] = i
            elif "opfern" in h_lower or "sacrific" in h_lower:
                question_cols[18] = i
        # Meta questions
        elif "muttersprache" in h_lower and "beeinflus" in h_lower:
            question_cols[19] = i
        elif "mehrsprach" in h_lower or "multiple language" in h_lower or "sprachwechsel" in h_lower:
            question_cols[20] = i

    print(f"  Mapped columns: {question_cols}")

    if dry_run:
        print("\n  [DRY RUN] Would import the following:")
        for i, row in enumerate(rows[:3]):
            print(f"    Row {i+1}: {row[:5]}...")
        return {"dry_run": True, "rows": len(rows)}

    # Import into database
    conn = get_connection()
    conn.execute("PRAGMA foreign_keys=OFF")  # Disable FK for bulk import
    stats = {
        "total_rows": len(rows),
        "imported_students": 0,
        "imported_responses": 0,
        "skipped_short": 0,
        "errors": 0,
    }

    for row_idx, row in enumerate(rows):
        try:
            # Parse timestamp
            timestamp = parse_timestamp(row[0]) if len(row) > 0 else datetime.now().isoformat()

            # Find native language
            native_lang = "unknown"
            if "native_lang" in question_cols:
                col_idx = question_cols["native_lang"]
                if col_idx < len(row):
                    raw_lang = row[col_idx].strip()
                    native_lang = NATIVE_LANG_MAP.get(raw_lang, raw_lang.lower()[:2])

            # Generate student ID
            student_num = row_idx + 1
            student_id = f"S{student_num:03d}"

            # Insert student
            try:
                insert(conn, "students", {
                    "student_id": student_id,
                    "native_lang": native_lang,
                    "school_lang": native_lang,
                    "consent": 1,
                    "notes": f"Imported from CSV: {csv_file.name}",
                })
                stats["imported_students"] += 1
            except Exception:
                pass  # Student already exists

            # Process each question
            for q_num, col_idx in question_cols.items():
                if not isinstance(q_num, int) or q_num not in QUESTION_TOPIC_MAP:
                    continue
                if col_idx >= len(row):
                    continue

                answer = row[col_idx].strip()
                if not answer:
                    continue

                topic = QUESTION_TOPIC_MAP[q_num]
                q_id = QUESTION_ID_MAP.get(q_num, f"q{q_num}")
                language = detect_language(answer, native_lang)
                word_count = count_words(answer, language)

                # Quality check
                quality_flag = "ok"
                if word_count < MIN_WORD_COUNT:
                    quality_flag = "short"
                    stats["skipped_short"] += 1

                if topic == "meta":
                    # Store meta questions differently
                    continue

                # Insert response
                response_id = f"R{student_id}_{language}_{q_id}"
                try:
                    insert(conn, "responses", {
                        "response_id": response_id,
                        "student_id": student_id,
                        "questionnaire_id": f"survey_{language}",
                        "language": language,
                        "question_id": q_id,
                        "answer_text": answer,
                        "word_count": word_count,
                        "source": "survey",
                        "quality_flag": quality_flag,
                    })
                    stats["imported_responses"] += 1
                except Exception as e:
                    stats["errors"] += 1
                    print(f"  [WARN] Row {row_idx+1}, Q{q_num}: {e}")

        except Exception as e:
            stats["errors"] += 1
            print(f"  [ERROR] Row {row_idx+1}: {e}")

    conn.commit()
    conn.close()

    # Print summary
    print(f"\n{'='*60}")
    print(f"  Import Summary")
    print(f"{'='*60}")
    print(f"  Students created:  {stats['imported_students']}")
    print(f"  Responses created: {stats['imported_responses']}")
    print(f"  Skipped (short):   {stats['skipped_short']}")
    print(f"  Errors:            {stats['errors']}")
    print(f"{'='*60}\n")

    return stats


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Import Google Forms CSV")
    parser.add_argument("csv_file", help="Path to CSV file")
    parser.add_argument("--dry-run", action="store_true", help="Preview without importing")
    args = parser.parse_args()

    import_csv(args.csv_file, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
