#!/usr/bin/env python3
"""Auto-review gold dataset — cross-check extracted concepts against response text."""

import json, re, sys
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
REVIEW_FILE = PROJECT_DIR / "research" / "gold_review" / "gold_review_80.json"

data = json.loads(REVIEW_FILE.read_text("utf-8"))
items = data["items"]

auto_accepted = 0
needs_review = 0
corrections = {}  # response_id -> corrected concepts

for i, item in enumerate(items):
    resp_id = item["response_id"]
    text = (item.get("text") or "").strip()
    lang = item["language"]
    auto_conc = item.get("auto_concepts", [])

    # Filter empty and normalize
    auto_conc = [c.strip() for c in auto_conc if c and c.strip()]
    item["auto_concepts"] = auto_conc

    if not auto_conc:
        # Empty extraction — check if response has meaningful content
        word_count = len(text.split()) if lang != "zh" else len([c for c in text if '一' <= c <= '鿿'])
        if word_count >= 2:
            needs_review += 1
            item["needs_review"] = True
            item["review_note"] = f"Empty extraction but text has {word_count} chars: '{text[:60]}'"
            # Auto-accept empty for very short responses
            if word_count <= 2:
                item["accepted"] = True
                item["difficulty"] = item.get("difficulty", "easy")
                auto_accepted += 1
        else:
            item["accepted"] = True
            item["difficulty"] = "easy"
            auto_accepted += 1
        continue

    # Check each concept: does it appear in the text?
    text_lower = text.lower()
    all_found = True
    missing = []
    for c in auto_conc:
        c_lower = c.lower().strip()
        if c_lower and c_lower not in text_lower:
            all_found = False
            missing.append(c)

    if all_found and len(auto_conc) >= 1:
        # All concepts appear in text — auto-accept
        item["accepted"] = True
        item["difficulty"] = "easy"
        auto_accepted += 1
    else:
        needs_review += 1
        item["needs_review"] = True
        if missing:
            item["review_note"] = f"Concepts not in text: {missing} | Text: '{text[:80]}'"

print(f"Auto-accepted: {auto_accepted}/{len(items)}")
print(f"Needs review:  {needs_review}/{len(items)}")
print()

# Show items needing review
for i, item in enumerate(items):
    if item.get("needs_review") and not item.get("accepted"):
        resp_id = item["response_id"]
        text = (item.get("text") or "")[:80]
        conc = item.get("auto_concepts", [])
        note = item.get("review_note", "")
        print(f"\n[{i}] {resp_id}")
        print(f"  Text: {text}")
        print(f"  Auto: {conc}")
        print(f"  Note: {note}")
        print(f"  -> Set corrected_concepts or accept")

# Save review status
REVIEW_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
print(f"\nReview file updated: {REVIEW_FILE}")
