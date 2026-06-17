"""
Ingest Student Data
====================
Import student survey responses and demographic info into the linguaGraph database.

Supports:
    - Single student JSON files (data/student_*.json)
    - Batch import from data/students/*.json
    - Auto-creates student records if they don't exist
    - Calculates word counts for quality flags

Usage:
    python ingest_student_data.py                          # Import all student data
    python ingest_student_data.py --file data/student_001.json  # Import single file
    python ingest_student_data.py --fresh                   # Re-import (delete existing)
    python ingest_student_data.py --dry-run                 # Preview without importing
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from db_utils import get_connection, query, query_one, insert, upsert

DATA_DIR = Path(__file__).parent / "data"
QUESTIONNAIRE_PREFIX = "social_issues_v1"


def get_questionnaire_id(language: str) -> str:
    """Get the questionnaire_id for a given language."""
    return f"{QUESTIONNAIRE_PREFIX}_{language}"


def calculate_word_count(text: str, language: str) -> int:
    """Calculate word count appropriate for the language."""
    text = text.strip()
    if not text:
        return 0
    if language == "zh":
        # Chinese: count characters (each character ≈ 1 word)
        return len(re.findall(r'[一-鿿㐀-䶿]', text))
    else:
        # German/English: count space-separated tokens
        return len(text.split())


def get_student_from_response(data: dict) -> dict:
    """Extract or create a student record from response data."""
    return {
        "student_id": data.get("student_id", f"S{datetime.now().strftime('%j%H%M')}"),
        "age_group": data.get("age_group"),
        "native_lang": data.get("native_lang", "zh"),
        "school_lang": data.get("school_lang", "de"),
        "other_langs": data.get("other_langs", "en"),
        "years_in_germany": data.get("years_in_germany"),
        "consent": 1 if data.get("consent", False) else 0,
        "notes": data.get("notes", ""),
    }


def import_student_file(conn, filepath: Path, dry_run: bool = False) -> Dict[str, int]:
    """Import a single student JSON file. Returns counts of imported objects."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    counts = {"students": 0, "responses": 0}

    # --- Extract student info ---
    student = get_student_from_response(data)
    sid = student["student_id"]

    if dry_run:
        print(f"  [DRY-RUN] Would import student: {sid}")
    else:
        upsert(conn, "students", student, "student_id")
        counts["students"] = 1

    # --- Extract responses ---
    responses_raw = data.get("responses", {})
    language = data.get("language", "zh")

    if isinstance(responses_raw, dict):
        # Format: {"q1": "answer text", "q2": "answer text", ...}
        # Map question IDs to topics based on the data
        for qid, answer in responses_raw.items():
            if not answer or not answer.strip():
                continue

            response_id = f"R{sid}_{language}_{qid}"
            wc = calculate_word_count(answer, language)
            quality = "ok"
            if wc < 2:
                quality = "empty"
            elif wc < 5:
                quality = "short"

            if dry_run:
                print(f"  [DRY-RUN] Would import response: {response_id} ({wc} words, flag={quality})")
                continue

            try:
                insert(conn, "responses", {
                    "response_id": response_id,
                    "student_id": sid,
                    "questionnaire_id": get_questionnaire_id(language),
                    "language": language,
                    "question_id": qid,
                    "answer_text": answer,
                    "word_count": wc,
                    "source": data.get("source", "survey"),
                    "quality_flag": quality,
                })
                counts["responses"] += 1
            except Exception as e:
                print(f"  [WARN] Skipping {response_id}: {e}")

    elif isinstance(responses_raw, list):
        # Format: [{"question_id": "q1", "answer": "..."}, ...]
        for resp in responses_raw:
            qid = resp.get("question_id") or resp.get("id", "")
            answer = resp.get("answer_text") or resp.get("text") or resp.get("answer", "")
            response_id = f"R{sid}_{language}_{qid}"
            wc = calculate_word_count(answer, language)

            if dry_run:
                print(f"  [DRY-RUN] Would import response: {response_id}")
                continue

            try:
                insert(conn, "responses", {
                    "response_id": response_id,
                    "student_id": sid,
                    "questionnaire_id": get_questionnaire_id(language),
                    "language": language,
                    "question_id": qid,
                    "answer_text": answer,
                    "word_count": wc,
                    "source": data.get("source", "survey"),
                    "quality_flag": "ok",
                })
                counts["responses"] += 1
            except Exception as e:
                print(f"  [WARN] Skipping {response_id}: {e}")

    return counts


def import_all_student_files(conn, fresh: bool = False, dry_run: bool = False) -> Dict[str, int]:
    """Import all student data files."""
    if fresh and not dry_run:
        conn.execute("DELETE FROM responses")
        conn.execute("DELETE FROM students")
        conn.commit()
        print("  [FRESH] Cleared existing student/responses data")

    # Look for files: data/student_*.json or data/students/*.json
    patterns = [
        DATA_DIR.glob("student_*.json"),
        (DATA_DIR / "students").glob("*.json") if (DATA_DIR / "students").exists() else [],
    ]

    total = {"students": 0, "responses": 0}
    files_imported = 0

    for pattern in patterns:
        for filepath in sorted(pattern):
            if filepath.name == "student_template.json":
                continue
            print(f"\n  File: {filepath.name}")
            counts = import_student_file(conn, filepath, dry_run=dry_run)
            total["students"] += counts["students"]
            total["responses"] += counts["responses"]
            files_imported += 1

    return total, files_imported


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Import student data into linguaGraph DB")
    parser.add_argument("--file", type=str, help="Import a single student JSON file")
    parser.add_argument("--fresh", action="store_true", help="Re-import all data")
    parser.add_argument("--dry-run", action="store_true", help="Preview without importing")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  Importing Student Data")
    print(f"{'='*50}")

    conn = get_connection()

    if args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"  [ERROR] File not found: {filepath}")
            return
        counts = import_student_file(conn, filepath, dry_run=args.dry_run)
        print(f"\n  [DONE] {counts['students']} student, {counts['responses']} responses imported")
    else:
        total, files = import_all_student_files(conn, fresh=args.fresh, dry_run=args.dry_run)
        print(f"\n  [DONE] {files} files: {total['students']} students, {total['responses']} responses")

    if not args.dry_run:
        conn.close()

    # Show summary
    if not args.dry_run:
        conn = get_connection()
        from db_utils import query
        students = query(conn, "SELECT student_id, native_lang FROM students")
        resp_count = query(conn, "SELECT COUNT(*) as c FROM responses")[0]["c"]
        print(f"\n  Summary: {len(students)} students, {resp_count} total responses in DB")
        for s in students:
            print(f"    - {s['student_id']} (native: {s['native_lang']})")
        conn.close()


if __name__ == "__main__":
    main()
