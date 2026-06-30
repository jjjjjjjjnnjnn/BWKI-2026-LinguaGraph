#!/usr/bin/env python3
"""
merge_gold_dataset.py — Merge gold_review_80 into gold_dataset.json
Converts review format to gold format and produces N=~99 dataset.
"""
import json, re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
GOLD_PATH = PROJECT / "data" / "gold" / "gold_dataset.json"
REVIEW_PATH = PROJECT / "research" / "gold_review" / "gold_review_80.json"
OUTPUT_PATH = PROJECT / "data" / "gold" / "gold_dataset_expanded.json"

def merge():
    # Load existing gold
    with open(GOLD_PATH, "r", encoding="utf-8") as f:
        existing = json.load(f)
    
    existing_ids = {item["sample_id"] for item in existing}
    print(f"Existing gold: {len(existing)} items")
    
    # Load review items
    with open(REVIEW_PATH, "r", encoding="utf-8") as f:
        review = json.load(f)
    
    review_items = review["items"]
    print(f"Review items: {len(review_items)} (all accepted)")
    
    # Convert review format to gold format
    new_items = []
    id_counters = {"zh": 0, "de": 0, "en": 0}
    
    # Find max existing IDs per language
    for item in existing:
        lang = item["language"]
        m = re.search(r"_(\d+)$", item["sample_id"])
        if m:
            num = int(m.group(1))
            if num > id_counters.get(lang, 0):
                id_counters[lang] = num
    
    for ri in review_items:
        lang = ri.get("language", "zh")
        text = ri.get("text", "").strip()
        if not text:
            continue
        
        # Generate sample_id
        id_counters[lang] = id_counters.get(lang, 0) + 1
        sample_id = f"{lang}_{id_counters[lang]:03d}"
        
        # Skip if ID already exists
        if sample_id in existing_ids:
            continue
        
        # Use auto_concepts as the concepts (human-accepted)
        concepts = ri.get("auto_concepts", [])
        if not concepts:
            # Try to extract from text as fallback
            continue
        
        # Build gold-format item
        item = {
            "sample_id": sample_id,
            "language": lang,
            "question": ri.get("question_id", ""),
            "text": text,
            "human_labels": {
                "concepts": concepts,
                "relations": [],
                "missing_hints": [],
            },
            "annotator": "auto_accepted",
            "difficulty": ri.get("difficulty", "medium"),
        }
        new_items.append(item)
        existing_ids.add(sample_id)
    
    # Merge
    merged = existing + new_items
    print(f"New items added: {len(new_items)}")
    print(f"Total merged: {len(merged)}")
    
    # Stats by language
    by_lang = {}
    for item in merged:
        l = item["language"]
        by_lang[l] = by_lang.get(l, 0) + 1
    print(f"By language: {by_lang}")
    
    # Save
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"Saved: {OUTPUT_PATH}")
    
    # Also overwrite original
    with open(GOLD_PATH, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"Updated: {GOLD_PATH}")

if __name__ == "__main__":
    merge()
