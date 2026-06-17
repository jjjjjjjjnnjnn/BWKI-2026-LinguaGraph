"""
Survey Entry — CLI tool for data collection
=============================================
Allows the partner (language & cognition expert) to enter student data
into the LinguaGraph database directly from the command line.

Usage:
    python survey_entry.py add-student --id S002 --native zh --school de
    python survey_entry.py add-response --student S002 --lang zh --question q1 --answer "..."
    python survey_entry.py add-batch --student S002 --lang zh
    python survey_entry.py batch-import data/students/new/
    python survey_entry.py status
    python survey_entry.py list-students
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from db_utils import get_connection, query, query_one, insert, upsert

QUESTIONNAIRE_PREFIX = "social_issues_v1"


def get_qid(lang: str) -> str:
    """Get questionnaire ID per language."""
    return f"{QUESTIONNAIRE_PREFIX}_{lang}"


def cmd_add_student(args):
    """Add a new student participant."""
    conn = get_connection()

    student = {
        "student_id": args.id,
        "age_group": args.age_group or "",
        "native_lang": args.native,
        "school_lang": args.school,
        "other_langs": args.other_langs or "",
        "years_in_germany": args.years or 0,
        "consent": 1 if args.consent else 0,
        "notes": args.notes or "",
    }

    upsert(conn, "students", student, "student_id")
    print(f"  [OK] Student {args.id} added/updated ({args.native}→native, {args.school}→school)")

    # Print questionnaire prompts
    quest = query_one(conn, "SELECT questions FROM questionnaires WHERE questionnaire_id=?", (get_qid(args.native),))
    if quest:
        questions = json.loads(quest["questions"])
        print(f"\n  Questions for {args.id} ({args.native}):")
        for q in questions:
            print(f"    {q['id']}: {q['text']}")

    conn.close()


def cmd_add_response(args):
    """Add a student response."""
    conn = get_connection()

    # Verify student exists
    student = query_one(conn, "SELECT student_id FROM students WHERE student_id=?", (args.student,))
    if not student:
        print(f"  [ERROR] Student '{args.student}' not found. Add them first: survey_entry.py add-student --id {args.student} ...")
        return

    response_id = f"R{args.student}_{args.lang}_{args.question}"
    word_count = len(args.answer.strip().split())
    if args.lang == "zh":
        import re
        word_count = len(re.findall(r'[一-鿿㐀-䶿]', args.answer))

    try:
        insert(conn, "responses", {
            "response_id": response_id,
            "student_id": args.student,
            "questionnaire_id": get_qid(args.lang),
            "language": args.lang,
            "question_id": args.question,
            "answer_text": args.answer,
            "word_count": word_count,
            "source": args.source or "manual",
            "quality_flag": "ok" if word_count >= 5 else "short",
        })
        print(f"  [OK] Response saved: {response_id} ({word_count} words)")
    except Exception as e:
        print(f"  [ERROR] {e}")

    conn.close()


def cmd_add_batch(args):
    """Interactive batch entry for one student in one language."""
    conn = get_connection()

    student = query_one(conn, "SELECT student_id FROM students WHERE student_id=?", (args.student,))
    if not student:
        print(f"  [ERROR] Student '{args.student}' not found.")
        return

    quest = query_one(conn, "SELECT questions FROM questionnaires WHERE questionnaire_id=?",
                     (get_qid(args.lang),))
    if not quest:
        print(f"  [ERROR] Questionnaire not found for language: {args.lang}")
        return

    questions = json.loads(quest["questions"])
    print(f"\n  Batch entry for {args.student} ({args.lang})")
    print(f"  {'─'*50}")

    for q in questions:
        print(f"\n  Q: {q['text']}")
        answer = input(f"  A: ").strip()
        if not answer:
            print(f"  [SKIP] Empty answer")
            continue

        response_id = f"R{args.student}_{args.lang}_{q['id']}"
        try:
            insert(conn, "responses", {
                "response_id": response_id,
                "student_id": args.student,
                "questionnaire_id": get_qid(args.lang),
                "language": args.lang,
                "question_id": q["id"],
                "answer_text": answer,
                "word_count": len(answer.split()),
                "source": "manual",
                "quality_flag": "ok",
            })
            print(f"  [OK] Saved: {response_id}")
        except Exception as e:
            print(f"  [ERROR] {e}")

    conn.close()


def cmd_batch_import(args):
    """Batch import all JSON files from a directory."""
    import ingest_student_data
    conn = get_connection()
    path = Path(args.path)

    if not path.exists() or not path.is_dir():
        print(f"  [ERROR] Invalid directory: {path}")
        return

    files = sorted(path.glob("*.json"))
    if not files:
        print(f"  [ERROR] No JSON files found in {path}")
        return

    print(f"  Importing {len(files)} files from {path}")
    total = {"students": 0, "responses": 0}

    for filepath in files:
        print(f"\n  ── {filepath.name}")
        try:
            counts = ingest_student_data.import_student_file(conn, filepath)
            total["students"] += counts["students"]
            total["responses"] += counts["responses"]
        except Exception as e:
            print(f"  [ERROR] Failed to import {filepath.name}: {e}")

    print(f"\n  [DONE] {total['students']} students, {total['responses']} responses imported")
    conn.close()


def cmd_status(args):
    """Show data collection status."""
    conn = get_connection()

    students = query(conn, "SELECT * FROM students ORDER BY student_id")
    print(f"\n{'='*50}")
    print(f"  LinguaGraph Data Collection Status")
    print(f"{'='*50}")

    print(f"\n  Total students: {len(students)}")
    for s in students:
        lang_resp = query(conn,
            "SELECT language, COUNT(*) as c FROM responses WHERE student_id=? GROUP BY language",
            (s["student_id"],))
        languages = {r["language"]: r["c"] for r in lang_resp}

        print(f"\n    {s['student_id']} ({s['native_lang']}→{s['school_lang']})")
        for lang_code in ["zh", "de", "en"]:
            count = languages.get(lang_code, 0)
            icon = "✅" if count >= 4 else "⚠️" if count > 0 else "❌"
            print(f"      {icon} {lang_code}: {count} responses")
        if args.detail:
            responses = query(conn,
                "SELECT language, question_id, answer_text, word_count FROM responses WHERE student_id=? ORDER BY language, question_id",
                (s["student_id"],))
            for r in responses:
                preview = r["answer_text"][:60].replace("\n", " ")
                print(f"        {r['language']} {r['question_id']}: {preview}...")

    conn.close()


def cmd_list_students(args):
    """List all students with basic info."""
    conn = get_connection()
    students = query(conn, "SELECT * FROM students ORDER BY student_id")

    print(f"\n{'='*50}")
    print(f"  Registered Students ({len(students)})")
    print(f"{'='*50}")
    for s in students:
        print(f"  {s['student_id']:<8s} | native: {s['native_lang']:<4s} | school: {s['school_lang']:<4s} | consent: {s['consent']}")
    print()

    conn.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph Survey Entry Tool (for partners)")
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # add-student
    p_student = sub.add_parser("add-student", help="Register a new student")
    p_student.add_argument("--id", required=True, help="Student ID, e.g. S002")
    p_student.add_argument("--native", default="zh", help="Native language (zh/de/en)")
    p_student.add_argument("--school", default="de", help="School language (zh/de/en)")
    p_student.add_argument("--age-group", help="Age group (e.g. 13-15, 16-18)")
    p_student.add_argument("--other-langs", help="Other languages, comma-separated")
    p_student.add_argument("--years", type=int, help="Years in Germany")
    p_student.add_argument("--consent", action="store_true", help="Consent obtained")
    p_student.add_argument("--notes", help="Free-form notes")

    # add-response
    p_resp = sub.add_parser("add-response", help="Add a student response")
    p_resp.add_argument("--student", required=True, help="Student ID")
    p_resp.add_argument("--lang", required=True, help="Language (zh/de/en)")
    p_resp.add_argument("--question", required=True, help="Question ID (q1/q2/q3/q4)")
    p_resp.add_argument("--answer", required=True, help="Answer text")
    p_resp.add_argument("--source", default="manual", help="Data source")

    # add-batch
    p_batch = sub.add_parser("add-batch", help="Interactive batch entry for one student/language")
    p_batch.add_argument("--student", required=True, help="Student ID")
    p_batch.add_argument("--lang", required=True, help="Language (zh/de/en)")

    # batch-import
    p_bi = sub.add_parser("batch-import", help="Import all JSON files from a directory")
    p_bi.add_argument("path", help="Directory containing student JSON files")

    # status
    p_status = sub.add_parser("status", help="Show data collection status")
    p_status.add_argument("--detail", action="store_true", help="Show full response details")

    # list-students
    sub.add_parser("list-students", help="List all registered students")

    args = parser.parse_args()

    if args.command == "add-student":
        cmd_add_student(args)
    elif args.command == "add-response":
        cmd_add_response(args)
    elif args.command == "add-batch":
        cmd_add_batch(args)
    elif args.command == "batch-import":
        cmd_batch_import(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "list-students":
        cmd_list_students(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
