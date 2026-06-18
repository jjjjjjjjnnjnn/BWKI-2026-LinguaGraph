"""Check and fix dirty data in students table."""
import sys
sys.path.insert(0, "scripts")
from db_utils import get_connection, query

conn = get_connection()

# Check dirty data
dirty = query(conn, "SELECT student_id, native_lang, consent FROM students WHERE native_lang NOT IN ('zh','de','en')")
print(f"Dirty rows: {len(dirty)}")
for r in dirty:
    print(f"  {r['student_id']}: native_lang={r['native_lang']!r}, consent={r['consent']}")

# Map known bad values to correct languages
# These came from CSV import where column mapping was wrong
FIX_MAP = {
    # Chinese concept words that leaked into native_lang
    "自由": "zh", "公平": "zh", "成功": "zh", "家庭": "zh",
    "du": "de", "fo": "de", "th": "de", "fr": "en",
    "pf": "de",  # Pflicht = duty (German)
    # N/A entries
    "N/A": "en",  # WIKIPEDIA_CORPUS default
}

fixed = 0
for r in dirty:
    sid = r["student_id"]
    old_lang = r["native_lang"]
    new_lang = FIX_MAP.get(old_lang)
    if new_lang:
        conn.execute("UPDATE students SET native_lang = ? WHERE student_id = ?", (new_lang, sid))
        fixed += 1
        print(f"  FIXED: {sid}: {old_lang!r} -> {new_lang!r}")
    else:
        print(f"  SKIP: {sid}: {old_lang!r} (no mapping)")

conn.commit()

# Verify
remaining = query(conn, "SELECT student_id, native_lang FROM students WHERE native_lang NOT IN ('zh','de','en')")
print(f"\nRemaining dirty rows: {len(remaining)}")
for r in remaining:
    print(f"  {r['student_id']}: {r['native_lang']!r}")

# Summary
all_students = query(conn, "SELECT student_id, native_lang FROM students ORDER BY student_id")
print(f"\nAll students ({len(all_students)}):")
for s in all_students:
    print(f"  {s['student_id']}: {s['native_lang']}")

conn.close()
print(f"\nFixed {fixed} rows.")
