#!/usr/bin/env python3
"""STEAM leftovers by bare tokens (verified STEAM-only contexts)."""
import io
jobs = [
    ("README_ZH.md", [("839\u8fb9", "834\u8fb9")]),
    ("README_DE.md", [("839 Kanten", "834 Kanten")]),
]
for p, pairs in jobs:
    t = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(p, "x%d" % c)
        assert c >= 1
        t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(t)
print("done")
