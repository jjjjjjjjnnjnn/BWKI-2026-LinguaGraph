"""
Ingest Gold Labels
====================
Import human-annotated gold standard data into the linguaGraph database.

The gold labels are used to evaluate LLM extraction accuracy.
Each label contains human-annotated concepts, relations, and missing hints
for a given student response.

Usage:
    python ingest_gold_labels.py                # Import all gold labels
    python ingest_gold_labels.py --fresh         # Re-import (delete existing)
    python ingest_gold_labels.py --file <path>   # Import from custom file
"""

import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from db_utils import get_connection, query, insert

DATA_DIR = Path(__file__).parent / "data"


def map_question_to_id(question_text: str) -> str:
    """Map question text to a standard question ID."""
    q = question_text.lower()
    if "导数" in q or "ableitung" in q or "derivative" in q:
        return "q1"
    if "积分" in q or "integral" in q or "integration" in q:
        return "q2"
    if "极限" in q or "grenzwert" in q or "limit" in q:
        return "q3"
    if "函数" in q or "funktion" in q or "function" in q:
        return "q4"
    return "q_unknown"


def import_gold_labels(conn, filepath: Path, fresh: bool = False, prefix: str = "L") -> int:
    """Import gold labels from a JSON file."""
    if fresh:
        conn.execute("DELETE FROM gold_labels")
        conn.commit()
        print("  [FRESH] Cleared existing gold labels")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]

    count = 0
    label_counter = 0

    # Ensure a "GOLD_LABEL" student exists for gold-label responses
    try:
        insert(conn, "students", {
            "student_id": "GOLD_LABEL",
            "native_lang": "zh",
            "school_lang": "de",
            "consent": 1,
            "notes": "System account for gold label responses",
        })
    except Exception:
        pass  # Already exists

    for entry in data:
        label_counter += 1
        sample_id = entry.get("sample_id", f"sample_{label_counter:03d}")
        lang_code = entry.get("language", "zh")
        answer_text = entry.get("text", "")

        label_id = f"{prefix}_{datetime.now().strftime('%Y%m%d')}_{label_counter:03d}"

        # Extract labels
        labels = entry.get("human_labels", entry)
        concepts = labels.get("concepts", [])
        relations = labels.get("relations", [])

        # Try to match an existing response by exact text
        existing_response = None
        if answer_text.strip():
            all_responses = query(conn,
                "SELECT response_id, answer_text FROM responses WHERE language=?",
                (lang_code,))
            for r in all_responses:
                if r["answer_text"].strip() == answer_text.strip():
                    existing_response = r
                    break

        if existing_response:
            response_id = existing_response["response_id"]
        else:
            response_id = f"Rgold_{sample_id}"
            qid = f"q_{sample_id}"
            try:
                insert(conn, "responses", {
                    "response_id": response_id,
                    "student_id": "GOLD_LABEL",
                    "questionnaire_id": f"social_issues_v1_{lang_code}",
                    "language": lang_code,
                    "question_id": qid,
                    "answer_text": answer_text,
                    "word_count": len(answer_text.split()),
                    "source": "gold_import",
                    "quality_flag": "ok",
                })
            except Exception as e:
                print(f"  [SKIP] Cannot create response for {sample_id}: {e}")
                continue

        # Insert gold label
        missing_hints = labels.get("missing_hints", [])
        difficulty = entry.get("difficulty", "medium")

        try:
            insert(conn, "gold_labels", {
                "label_id": label_id,
                "response_id": response_id,
                "annotator": entry.get("annotator", "import"),
                "concepts": json.dumps(concepts, ensure_ascii=False),
                "relations": json.dumps(relations, ensure_ascii=False),
                "missing_hints": json.dumps(missing_hints, ensure_ascii=False) if missing_hints else None,
                "difficulty": difficulty,
            })
            count += 1
            print(f"  [OK] {label_id} -> {response_id} ({len(concepts)} concepts, {len(relations)} relations)")
        except Exception as e:
            print(f"  [WARN] Skipping {label_id}: {e}")

    return count


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Import gold labels into linguaGraph DB")
    parser.add_argument("--fresh", action="store_true", help="Re-import all labels")
    parser.add_argument("--file", type=str, help="Import from custom JSON file")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  Importing Gold Labels")
    print(f"{'='*50}")

    conn = get_connection()

    if args.file:
        filepath = Path(args.file)
    else:
        filepath = DATA_DIR / "gold" / "gold_dataset.json"

    if not filepath.exists():
        print(f"  [ERROR] File not found: {filepath}")
        print(f"  Expected at: data/gold/gold_dataset.json")
        return

    count = import_gold_labels(conn, filepath, fresh=args.fresh)
    print(f"\n  [DONE] {count} gold labels imported\n")

    conn.close()


if __name__ == "__main__":
    main()
