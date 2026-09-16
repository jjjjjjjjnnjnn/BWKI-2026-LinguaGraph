#!/usr/bin/env python3
"""Portal number unification (SSOT batch 1). Run from repo root."""
import io

p = "cognitive-space/portal/index.html"
t = io.open(p, encoding="utf-8").read()
edits = [
    ("(that is the 58-run replication below).",
     "(that is the 59-run replication below)."),
    ("8 \u4e2a\u542b EN \u6d4b\u8bd5\u4e0d\u663e\u8457\u3002",
     "177 \u4e2d 9 \u4e2a EN n.s.\u3002"),
    ("glos_7: '\u6807\u7b7e shuffling\uff0c\u5982\u4e2d\u5fb7 59/59\u3001p\uff1c0.004\uff08500 perm.\uff09\u3002'",
     "glos_7: '\u6807\u7b7e shuffling\uff0c\u5982\u4e2d\u5fb7 59/59\u3001p\uff1c0.004\uff08500 perm.\uff0cfile-truth 62/62\uff09\u3002'"),
    ("multi_model_replication_20260913.json 55 \u4e2a\u5b8c\u6574\u8fd0\u884c",
     "multi_model_replication_20260913.json 59 \u4e2a\u5b8c\u6574\u8fd0\u884c"),
]
for old, new in edits:
    assert t.count(old) == 1, "match!=1: " + old[:30]
    t = t.replace(old, new)
io.open(p, "w", encoding="utf-8").write(t)
print("portal 4 fixes applied")
