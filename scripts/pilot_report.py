"""Generate pilot data ingestion report."""
import csv
from pathlib import Path

base = Path(r"C:\Users\rongj\Desktop\学校\BWKI-2026-备战\participant_data\pilot_raw")

with open(base / "participants.csv", encoding="utf-8") as f:
    participants = list(csv.DictReader(f))

with open(base / "responses.csv", encoding="utf-8") as f:
    responses = list(csv.DictReader(f))

sources = list((base / "sources").glob("*"))

print("=" * 60)
print("  Pilot Data Ingestion Report")
print("=" * 60)
print(f"  Participants: {len(participants)}")
print(f"  Responses: {len(responses)}")
print(f"  Languages: zh (all responses)")
print(f"  Source files archived: {len(sources)}")
print()
print("  Questions covered:")
qids = sorted(set(r["question_id"] for r in responses))
for q in qids:
    count = sum(1 for r in responses if r["question_id"] == q)
    print(f"    {q}: {count} responses")
print()
print("=" * 60)
print("  Sample Data (first response per participant)")
print("=" * 60)

seen = set()
for r in responses:
    if r["student_id"] not in seen:
        seen.add(r["student_id"])
        sid = r["student_id"]
        lang = r["language"]
        qid = r["question_id"]
        ans = r["answer_text"][:80]
        print(f"  {sid} ({lang}):")
        print(f"    {qid}: {ans}")
        print()

print("=" * 60)
print("  Note: All responses are in Chinese (zh) only.")
print("  German (de) and English (en) versions not yet collected.")
print("  PDF questionnaires archived in sources/ for reference.")
print("=" * 60)
