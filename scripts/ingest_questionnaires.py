"""
Ingest Questionnaires
======================
Import trilingual questionnaires into the linguaGraph database.

Usage:
    python ingest_questionnaires.py         # Import all questionnaires
    python ingest_questionnaires.py --fresh  # Re-import (delete existing)
"""

import json
import sys
from pathlib import Path

# Ensure db_utils is importable
sys.path.insert(0, str(Path(__file__).parent))
from db_utils import get_connection, insert, query

DATA_DIR = Path(__file__).parent / "data" / "questionnaires"


def load_questionnaire(filepath: Path) -> dict:
    """Load a questionnaire JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def import_questionnaires(conn, fresh: bool = False) -> int:
    """Import all questionnaire files into the database."""
    if fresh:
        conn.execute("DELETE FROM questionnaires")
        conn.commit()
        print("  [FRESH] Cleared existing questionnaires")

    count = 0
    lang_map = {
        "questionnaire_zh.json": "zh",
        "questionnaire_de.json": "de",
        "questionnaire_en.json": "en",
    }

    for filename, lang in lang_map.items():
        filepath = DATA_DIR / filename
        if not filepath.exists():
            print(f"  [SKIP] {filename} not found")
            continue

        data = load_questionnaire(filepath)
        questionnaire_id = f"social_issues_v1_{lang}"

        # Check if already imported
        existing = query(conn, "SELECT questionnaire_id FROM questionnaires WHERE questionnaire_id=?",
                        (questionnaire_id,))
        if existing and not fresh:
            print(f"  [SKIP] {questionnaire_id} already exists")
            continue

        insert(conn, "questionnaires", {
            "questionnaire_id": questionnaire_id,
            "title": data.get("title", f"Social Issues ({lang})"),
            "language": lang,
            "questions": json.dumps(data.get("questions", []), ensure_ascii=False),
            "version": data.get("metadata", {}).get("version", "1.0"),
        })
        count += 1
        topic_count = len(data.get("questions", []))
        print(f"  [OK] {lang.upper()} questionnaire: {topic_count} questions")

    return count


def import_expected_differences(conn) -> int:
    """Import the expected cross-language differences reference data."""
    filepath = DATA_DIR / "expected_differences.json"
    if not filepath.exists():
        print("  [SKIP] expected_differences.json not found")
        return 0

    # Store as a reference JSON in a simple metadata table-like structure
    # We use a custom table for research expectations
    conn.execute("""
        CREATE TABLE IF NOT EXISTS research_expectations (
            topic       TEXT PRIMARY KEY,
            hypotheses  TEXT NOT NULL,
            zh_concepts TEXT NOT NULL,
            de_concepts TEXT NOT NULL,
            en_concepts TEXT NOT NULL,
            created_at  TEXT DEFAULT (datetime('now'))
        )
    """)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    import datetime
    for topic_key, topic_data in data.items():
        conn.execute("""
            INSERT OR REPLACE INTO research_expectations
            (topic, hypotheses, zh_concepts, de_concepts, en_concepts, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            topic_key,
            topic_data.get("hypothesis", ""),
            json.dumps(topic_data.get("zh", []), ensure_ascii=False),
            json.dumps(topic_data.get("de", []), ensure_ascii=False),
            json.dumps(topic_data.get("en", []), ensure_ascii=False),
            datetime.datetime.now().isoformat()
        ))
        count += 1
        print(f"  [OK] Research expectation: {topic_key}")

    conn.commit()
    return count


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Import questionnaires into linguaGraph DB")
    parser.add_argument("--fresh", action="store_true", help="Re-import all questionnaires")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  Importing Questionnaires")
    print(f"{'='*50}")

    conn = get_connection()
    q_count = import_questionnaires(conn, fresh=args.fresh)
    e_count = import_expected_differences(conn)

    print(f"\n  [DONE] {q_count} questionnaires + {e_count} expectations imported\n")
    conn.close()


if __name__ == "__main__":
    main()
