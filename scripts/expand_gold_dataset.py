#!/usr/bin/env python3
"""
Gold Dataset Expansion Pipeline (20 → 100)
============================================
Design: select 80 survey responses, run qwen-plus extraction,
        create human-reviewable format, import reviewed results.

Target: 40 ZH + 30 DE + 30 EN = 100 total gold labels
Strategy: keep existing 20 calculus gold + add 80 social-domain gold

Usage:
    python scripts/expand_gold_dataset.py --generate    # Generate review files
    python scripts/expand_gold_dataset.py --status      # Current gold status
    python scripts/expand_gold_dataset.py --import      # Import reviewed results
"""

import json, os, sqlite3, sys, time, re
from collections import defaultdict
from datetime import datetime
from openai import OpenAI
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / "scripts"))
from db_utils import insert, query, get_connection

API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
API_KEY = os.environ.get("BAILIAN_API_KEY", "")
if not API_KEY:
    print("ERROR: Set BAILIAN_API_KEY environment variable")
    sys.exit(1)
MODEL = "qwen-plus"

REVIEW_DIR = PROJECT_DIR / "research" / "gold_review"
REVIEW_DIR.mkdir(parents=True, exist_ok=True)

EXAMPLES = {
    "zh": '{"concepts": ["自由", "责任", "权利"]}',
    "en": '{"concepts": ["freedom", "responsibility", "choice"]}',
    "de": '{"concepts": ["Freiheit", "Verantwortung", "Selbstbestimmung"]}',
}


def call_api(text, lang):
    """Extract concepts using qwen-plus."""
    client = OpenAI(base_url=API_URL, api_key=API_KEY)
    example = EXAMPLES.get(lang, EXAMPLES["en"])
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "你是概念提取助手。只输出JSON。"},
            {"role": "user", "content": f"{example}\n\nText: {text}\n\n提取概念为JSON格式。"},
        ],
        temperature=0.3, max_tokens=256, timeout=30,
    )
    raw = resp.choices[0].message.content.strip()
    cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    return json.loads(match.group()).get("concepts", []) if match else []


def print_status():
    """Print current gold dataset status."""
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM gold_labels").fetchone()[0]
    by_lang = conn.execute("SELECT language, COUNT(*) FROM responses WHERE student_id='GOLD_LABEL' GROUP BY language").fetchall()
    by_domain = conn.execute("SELECT gl.difficulty, COUNT(*) FROM gold_labels gl GROUP BY gl.difficulty").fetchall()

    print(f"\n{'='*60}")
    print(f"  Gold Dataset Status")
    print(f"{'='*60}")
    print(f"  Total gold labels: {total}")
    print(f"\n  By language:")
    for lang, cnt in by_lang:
        print(f"    {lang}: {cnt}")
    print(f"\n  By difficulty:")
    for diff, cnt in by_domain:
        print(f"    {diff}: {cnt}")

    # Current domain (from response content)
    sample = conn.execute("SELECT r.answer_text FROM gold_labels gl JOIN responses r ON gl.response_id=r.response_id LIMIT 1").fetchone()
    if sample:
        text = str(sample[0])[:60] if sample[0] else ""
        print(f"\n  Sample gold text: {text}")

    conn.close()
    print(f"\n  Target: 100 total (40 ZH + 30 DE + 30 EN)")
    need = max(0, 40 - 7) + max(0, 30 - 7) + max(0, 30 - 6)
    print(f"  New gold labels needed: {need}")


def generate_review_files():
    """
    Select 80 survey responses and generate review files.
    Strategy: stratified by language, topic, and student.
    """
    conn = get_connection()

    # Target per language
    targets = {"zh": 33, "de": 23, "en": 24}  # 33 + 23 + 24 = 80

    candidates = {}
    for lang, target_n in targets.items():
        # Select responses: 1 per (student × topic) when possible
        items = conn.execute(f"""
            SELECT response_id, student_id, question_id, answer_text, language
            FROM responses
            WHERE source='survey' AND language=?
            ORDER BY student_id, question_id
        """, (lang,)).fetchall()

        # Stratified selection
        selected = []
        seen_pairs = set()
        for item in items:
            resp_id = item[0]
            key = (item[2], item[1])  # (question, student)
            if key not in seen_pairs and len(selected) < target_n:
                selected.append({"response_id": resp_id, "student_id": item[1],
                                  "question_id": item[2], "text": str(item[3]) if item[3] else "",
                                  "language": lang})
                seen_pairs.add(key)

        # Fill remaining with any
        if len(selected) < target_n:
            for item in items:
                if len(selected) >= target_n:
                    break
                resp_id = item[0]
                if not any(s["response_id"] == resp_id for s in selected):
                    selected.append({"response_id": resp_id, "student_id": item[1],
                                      "question_id": item[2], "text": str(item[3]) if item[3] else "",
                                      "language": lang})

        candidates[lang] = selected[:target_n]

    total = sum(len(v) for v in candidates.values())
    print(f"\n  Selected {total} responses for gold expansion:")
    for lang, items in candidates.items():
        print(f"    {lang}: {len(items)} (students: {len(set(i['student_id'] for i in items))})")

    # Run qwen-plus extraction on each
    print(f"\n  Running qwen-plus extraction...\n")
    all_items = []
    for lang in ["zh", "de", "en"]:
        for item in candidates[lang]:
            text = item["text"]
            if not text.strip():
                item["auto_concepts"] = []
                continue
            print(f"    {item['response_id']}...", end=" ", flush=True)
            concepts = call_api(text, lang)
            item["auto_concepts"] = concepts
            print(f"OK ({len(concepts)} concepts)")
            time.sleep(0.1)
            all_items.append(item)

    # Create review file
    review = {
        "generated": datetime.now().isoformat(),
        "model": MODEL,
        "instructions": (
            "For each response below:\n"
            "  1. Review the auto-extracted concepts (from qwen-plus)\n"
            "  2. If correct, leave 'accepted': true\n"
            "  3. If incorrect, set 'accepted': false and fill 'corrected_concepts' with the correct list\n"
            "  4. Set 'difficulty' to 'easy', 'medium', or 'hard'\n"
            "  5. Delete the 'corrected_concepts' field if accepted is true\n"
            "\nThis should take ~30 seconds per item. Total ~40 minutes.\n"
        ),
        "target_total": 100,
        "existing_gold": 20,
        "new_gold_needed": 80,
        "items": all_items,
    }

    review_path = REVIEW_DIR / "gold_review_80.json"
    with open(review_path, "w", encoding="utf-8") as f:
        json.dump(review, f, ensure_ascii=False, indent=2)

    print(f"\n  Review file: {review_path}")
    print(f"  To review: edit the JSON file and set 'accepted' or 'corrected_concepts'")
    print(f"  Then run: python scripts/expand_gold_dataset.py --import")

    conn.close()


def import_reviewed():
    """Import reviewed gold labels from the review file."""
    review_path = REVIEW_DIR / "gold_review_80.json"
    if not review_path.exists():
        print(f"  Review file not found: {review_path}")
        return

    data = json.loads(review_path.read_text(encoding="utf-8"))
    conn = get_connection()

    count = 0
    for item in data["items"]:
        accepted = item.get("accepted", False)
        if not accepted:
            continue

        # Get corrected concepts
        concepts = item.get("corrected_concepts", item.get("auto_concepts", []))
        if not concepts:
            continue

        resp_id = item["response_id"]
        difficulty = item.get("difficulty", "medium")

        # Check if gold label already exists
        existing = conn.execute("SELECT label_id FROM gold_labels WHERE response_id=?", (resp_id,)).fetchone()
        if existing:
            print(f"  [SKIP] {resp_id} — gold label already exists")
            continue

        # Create gold label
        label_id = f"L_social_{resp_id[:15]}"
        insert(conn, "gold_labels", {
            "label_id": label_id,
            "response_id": resp_id,
            "annotator": "human_review",
            "concepts": json.dumps(concepts, ensure_ascii=False),
            "relations": json.dumps([]),
            "missing_hints": json.dumps([]),
            "difficulty": difficulty,
        })
        count += 1
        print(f"  [OK] {resp_id}: {concepts}")

    conn.commit()
    conn.close()

    print(f"\n  Imported {count} new gold labels")
    print(f"  Run evaluation: python scripts/evaluate_gold.py")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Gold Dataset Expansion 20→100")
    parser.add_argument("--status", action="store_true", help="Print gold status")
    parser.add_argument("--generate", action="store_true", help="Generate review files")
    parser.add_argument("--import", dest="import_mode", action="store_true", help="Import reviewed results")
    args = parser.parse_args()

    if args.status:
        print_status()
    elif args.generate:
        generate_review_files()
    elif args.import_mode:
        import_reviewed()
    else:
        print_status()
        print("\n  Usage:")
        print("    python scripts/expand_gold_dataset.py --status   # Check status")
        print("    python scripts/expand_gold_dataset.py --generate # Generate review files")
        print("    python scripts/expand_gold_dataset.py --import   # Import reviewed")


if __name__ == "__main__":
    main()
