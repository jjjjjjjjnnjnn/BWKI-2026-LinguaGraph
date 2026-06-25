#!/usr/bin/env python3
"""Generate Error Analysis section for the paper."""

import sys, json
sys.path.insert(0, '.'); sys.path.insert(0, 'scripts')
from evaluate_gold import *
from collections import defaultdict

conn = get_connection()
results = evaluate_gold_labels(conn, mode='keyword')
errors = [r for r in results if r['f1'] < 1.0]

# Categorize errors
categories = {"empty_extraction": 0, "partial_extraction": 0, "over_extraction": 0, "mixed_language": 0}
by_lang = defaultdict(lambda: defaultdict(int))
case_studies = {"de": [], "en": []}

for e in errors:
    lang = e['language']
    gold = e['gold_concepts']
    pred = e['predicted_concepts']
    text = e.get('text_preview', '')
    f1 = e['f1']

    if not pred:
        # Check if text is very short
        if text and len(text.split()) <= 2:
            categories["empty_extraction"] += 1
            by_lang[lang]["short_response"] += 1
        else:
            categories["empty_extraction"] += 1
            by_lang[lang]["missed_concepts"] += 1
    elif len(pred) < len(gold) and all(p in gold for p in pred):
        categories["partial_extraction"] += 1
        by_lang[lang]["partial"] += 1
    else:
        categories["over_extraction"] += 1
        by_lang[lang]["over_extraction"] += 1

    # Collect case studies
    if lang in ("de", "en") and f1 < 0.7 and len(case_studies[lang]) < 4:
        case_studies[lang].append({"response_id": e['response_id'], "f1": f1,
                                    "gold": gold, "pred": pred, "text": text[:80]})

# Generate table
print("=" * 70)
print("ERROR ANALYSIS")
print("=" * 70)
print()
print("Table: Error Type Distribution")
print(f"{'Error Type':<30s} {'ZH':>6s} {'DE':>6s} {'EN':>6s} {'Total':>6s}")
print("-" * 55)

all_types = ["short_response", "missed_concepts", "partial", "over_extraction"]
type_labels = {"short_response": "Very short response", "missed_concepts": "Empty extraction (longer text)",
               "partial": "Partial extraction", "over_extraction": "Over-extraction"}

for t in all_types:
    zh_n = by_lang.get("zh", {}).get(t, 0)
    de_n = by_lang.get("de", {}).get(t, 0)
    en_n = by_lang.get("en", {}).get(t, 0)
    total = zh_n + de_n + en_n
    label = type_labels.get(t, t)
    print(f"{label:<30s} {zh_n:>6d} {de_n:>6d} {en_n:>6d} {total:>6d}")

print()
print(f"Case Study: German Extraction Errors")
print("-" * 40)
for cs in case_studies["de"]:
    print(f"  {cs['response_id']} (F1={cs['f1']:.3f})")
    print(f"  Gold: {cs['gold']}")
    print(f"  Pred: {cs['pred']}")
    print(f"  Text: \"{cs['text']}\"")
    print()

print(f"Case Study: English Extraction Errors")
print("-" * 40)
for cs in case_studies["en"]:
    print(f"  {cs['response_id']} (F1={cs['f1']:.3f})")
    print(f"  Gold: {cs['gold']}")
    print(f"  Pred: {cs['pred']}")
    print(f"  Text: \"{cs['text']}\"")
    print()

conn.close()
