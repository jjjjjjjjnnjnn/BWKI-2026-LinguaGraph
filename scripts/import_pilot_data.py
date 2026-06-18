#!/usr/bin/env python3
"""
Import Pilot Data: Cognitive-Linguistic Battery
===============================================
Imports the first batch of real human pilot data (8 ZH participants).
Reads from participant_data/pilot_raw/participants.csv and responses.csv.

Usage:
    python scripts/import_pilot_data.py
    python scripts/import_pilot_data.py --status   # Preview only
"""

import csv
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from db_utils import get_connection, query, query_one, insert, upsert


PILOT_DIR = Path(__file__).parent.parent / "participant_data" / "pilot_raw"
QUESTIONNAIRE_ID = "cognitive_linguistic_v1"


# === Questionnaire Definition ===

COGNITIVE_LINGUISTIC_QUESTIONS = {
    "zh": {
        "title": "认知语言学测试（中文版）",
        "questions": [
            {"id": "q8_time_assoc", "text": "看到「时间」这个词，你最先联想到哪5个词？"},
            {"id": "q9_xiao_explain", "text": "什么是「孝」？请用中英文分别解释。"},
            {"id": "q10_emotion_reaction", "text": "如果你在公共场合犯了一个明显错误，你会有什么情感反应？"},
            {"id": "q11_picture_vase", "text": "请描述图中发生了什么。（花瓶被打碎的情景）"},
            {"id": "q12_translate_mike", "text": "请翻译：Mike entered the house, walked through the living room, and went into the garden."},
            {"id": "q13_picture_spatial", "text": "请描述图中物体的位置关系。（书、笔、杯子的空间位置）"},
            {"id": "q14_translate_test", "text": "请翻译：The test is in six days. The exam was brought forward two days."},
            {"id": "q15_picture_exchange", "text": "请描述图中发生了什么。（A把书递给B）"},
            {"id": "q16_translate_umbrella", "text": "请翻译：Because it was raining, the mother lent her umbrella to the girl yesterday afternoon."},
            {"id": "q17_robot_description", "text": "请描述你眼中的医护机器人应该是什么样的。"},
        ],
    },
    "de": {
        "title": "Kognitiv-linguistischer Test (Deutsch)",
        "questions": [
            {"id": "q8_time_assoc", "text": "Welche 5 Wörter fallen Ihnen als erstes zum Thema «Zeit» ein?"},
            {"id": "q9_xiao_explain", "text": "Was ist «孝» (kindliche Pietät)? Erklären Sie auf Deutsch und Englisch."},
            {"id": "q10_emotion_reaction", "text": "Wenn Sie in der Öffentlichkeit einen offensichtlichen Fehler machen, wie reagieren Sie emotional?"},
            {"id": "q11_picture_vase", "text": "Beschreiben Sie, was auf dem Bild passiert. (Eine Vase wird zerbrochen)"},
            {"id": "q12_translate_mike", "text": "Übersetzen Sie: Mike entered the house, walked through the living room, and went into the garden."},
            {"id": "q13_picture_spatial", "text": "Beschreiben Sie die räumliche Position der Objekte. (Buch, Stift, Tasse)"},
            {"id": "q14_translate_test", "text": "Übersetzen Sie: The test is in six days. The exam was brought forward two days."},
            {"id": "q15_picture_exchange", "text": "Beschreiben Sie, was auf dem Bild passiert. (A gibt B ein Buch)"},
            {"id": "q16_translate_umbrella", "text": "Übersetzen Sie: Because it was raining, the mother lent her umbrella to the girl yesterday afternoon."},
            {"id": "q17_robot_description", "text": "Beschreiben Sie, wie ein medizinischer Pflegeroboter Ihrer Meinung nach sein sollte."},
        ],
    },
    "en": {
        "title": "Cognitive-Linguistic Test (English)",
        "questions": [
            {"id": "q8_time_assoc", "text": "What 5 words do you first associate with 'time'?"},
            {"id": "q9_xiao_explain", "text": "What is '孝' (filial piety)? Explain in English."},
            {"id": "q10_emotion_reaction", "text": "If you make an obvious mistake in public, what is your emotional reaction?"},
            {"id": "q11_picture_vase", "text": "Describe what is happening in the picture. (A vase being broken)"},
            {"id": "q12_translate_mike", "text": "Translate: Mike entered the house, walked through the living room, and went into the garden."},
            {"id": "q13_picture_spatial", "text": "Describe the spatial relationship of the objects. (book, pen, cup)"},
            {"id": "q14_translate_test", "text": "Translate: The test is in six days. The exam was brought forward two days."},
            {"id": "q15_picture_exchange", "text": "Describe what is happening in the picture. (A gives B a book)"},
            {"id": "q16_translate_umbrella", "text": "Translate: Because it was raining, the mother lent her umbrella to the girl yesterday afternoon."},
            {"id": "q17_robot_description", "text": "Describe what you think a medical care robot should be like."},
        ],
    },
}


# === Import Functions ===


def register_questionnaire(conn):
    """Register the cognitive-linguistic battery questionnaire in the DB."""
    for lang, data in COGNITIVE_LINGUISTIC_QUESTIONS.items():
        qid = f"{QUESTIONNAIRE_ID}_{lang}"
        existing = query_one(conn, "SELECT questionnaire_id FROM questionnaires WHERE questionnaire_id = ?", (qid,))
        if existing:
            print(f"  [SKIP] Questionnaire {qid} already exists")
            continue
        insert(conn, "questionnaires", {
            "questionnaire_id": qid,
            "title": data["title"],
            "language": lang,
            "questions": json.dumps(data["questions"], ensure_ascii=False),
            "version": "1.0",
        })
        print(f"  [OK] Registered questionnaire: {qid}")


def import_participants(conn, dry_run: bool = False):
    """Import pilot participants from CSV."""
    csv_path = PILOT_DIR / "participants.csv"
    if not csv_path.exists():
        print(f"  [ERROR] participants.csv not found at {csv_path}")
        return [], 0

    imported = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["student_id"].strip()
            existing = query_one(conn, "SELECT student_id FROM students WHERE student_id = ?", (sid,))
            if existing:
                print(f"  [SKIP] Participant {sid} already exists in DB")
                continue

            if not dry_run:
                upsert(conn, "students", {
                    "student_id": sid,
                    "age_group": row.get("age_group", "").strip(),
                    "native_lang": row.get("native_lang", "zh").strip(),
                    "school_lang": row.get("school_lang", "zh").strip(),
                    "other_langs": row.get("other_langs", "").strip(),
                    "years_in_germany": float(row.get("years_in_germany", 0) or 0),
                    "consent": 1 if str(row.get("consent", "0")).strip() == "1" else 0,
                }, "student_id")
            imported.append(sid)
            print(f"  [OK] Imported participant: {sid} ({row.get('native_lang', '?')})")

    return imported, len(imported)


def import_responses(conn, participants: list, dry_run: bool = False):
    """Import pilot responses from CSV."""
    csv_path = PILOT_DIR / "responses.csv"
    if not csv_path.exists():
        print(f"  [ERROR] responses.csv not found at {csv_path}")
        return 0

    count = 0
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["student_id"].strip()
            lang = row["language"].strip()
            qid = row["question_id"].strip()
            answer = row["answer_text"].strip()

            if sid not in participants:
                continue

            response_id = f"R{sid}_{lang}_{qid}"
            existing = query_one(conn, "SELECT response_id FROM responses WHERE response_id = ?", (response_id,))
            if existing:
                print(f"  [SKIP] Response {response_id} already exists")
                continue

            questionnaire_id = f"{QUESTIONNAIRE_ID}_{lang}"

            if not dry_run:
                insert(conn, "responses", {
                    "response_id": response_id,
                    "student_id": sid,
                    "questionnaire_id": questionnaire_id,
                    "language": lang,
                    "question_id": qid,
                    "answer_text": answer,
                    "word_count": len(answer),
                    "source": "pilot",
                })
            count += 1

    print(f"  [OK] Imported {count} responses")
    return count


def import_all(dry_run: bool = False):
    """Run the full pilot data import."""
    conn = get_connection()

    print(f"\n{'='*60}")
    print(f"  LinguaGraph — Pilot Data Import")
    print(f"  {'(DRY RUN)' if dry_run else '(LIVE)'}")
    print(f"{'='*60}\n")

    # Step 1: Register questionnaire
    print("Step 1: Registering questionnaire...")
    register_questionnaire(conn)

    # Step 2: Import participants
    print("\nStep 2: Importing participants...")
    participants, n_p = import_participants(conn, dry_run=dry_run)
    print(f"  Total: {n_p} participants imported")

    # Step 3: Import responses
    print("\nStep 3: Importing responses...")
    n_r = import_responses(conn, participants, dry_run=dry_run)
    print(f"  Total: {n_r} responses imported")

    # Summary
    print(f"\n{'='*60}")
    print(f"  Import Summary")
    print(f"{'='*60}")
    print(f"  Participants: {n_p}")
    print(f"  Responses:    {n_r}")

    if not dry_run:
        # Verify
        from db_utils import query_value
        total_p = query_value(conn, "SELECT COUNT(*) FROM students")
        total_r = query_value(conn, "SELECT COUNT(*) FROM responses")
        zh_count = query_value(conn, "SELECT COUNT(*) FROM responses WHERE language='zh'")
        print(f"\n  DB state after import:")
        print(f"    Total students:  {total_p}")
        print(f"    Total responses: {total_r}")
        print(f"    ZH responses:    {zh_count}")
        print(f"\n  [OK] Import complete!\n")

    conn.close()
    return n_p, n_r


def show_status():
    """Preview what would be imported without making changes."""
    conn = get_connection()

    # Count existing pilot data in DB
    existing_p = query(conn, "SELECT student_id FROM students WHERE student_id LIKE 'P%'")
    existing_r = query(conn, "SELECT COUNT(*) as c FROM responses WHERE response_id LIKE 'RP%'")

    print(f"\n=== Pilot Data Import Status ===")
    print(f"Existing pilot students in DB: {len(existing_p)}")
    print(f"Existing pilot responses in DB: {existing_r[0]['c']}")
    print(f"\nCSV files:")
    print(f"  participants.csv: {'✅' if (PILOT_DIR/'participants.csv').exists() else '❌'}")
    print(f"  responses.csv:    {'✅' if (PILOT_DIR/'responses.csv').exists() else '❌'}")

    # Preview participants
    csv_path = PILOT_DIR / "participants.csv"
    if csv_path.exists():
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            print(f"\nParticipants to import:")
            for row in reader:
                print(f"  {row['student_id']}: {row['native_lang']}, age={row.get('age_group','?')}, consent={row.get('consent','?')}")

    # Preview responses
    csv_path = PILOT_DIR / "responses.csv"
    if csv_path.exists():
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            langs = set(r["language"] for r in rows)
            students = set(r["student_id"] for r in rows)
            questions = set(r["question_id"] for r in rows)
            print(f"\nResponses to import: {len(rows)}")
            print(f"  Students: {', '.join(sorted(students))}")
            print(f"  Languages: {', '.join(sorted(langs))}")
            print(f"  Questions: {len(questions)}")

    conn.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--import", action="store_true", dest="do_import", help="Run import (live)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without importing")
    parser.add_argument("--status", action="store_true", help="Show status")
    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.dry_run:
        import_all(dry_run=True)
    elif args.do_import:
        import_all(dry_run=False)
    else:
        # Default: show status
        show_status()
        print(f"\nTo import: python scripts/import_pilot_data.py --import")
        print(f"To preview: python scripts/import_pilot_data.py --dry-run")
