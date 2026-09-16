#!/usr/bin/env python3
"""STEAM 839->834 DE/ZH READMEs."""
import io
jobs = [
    ("README_ZH.md", [("1,143\u8282\u70b9 \u00b7 839\u8fb9", "1,143\u8282\u70b9 \u00b7 834\u8fb9"),
                    ("1,143 \u8282\u70b9 \u00b7 839\u8fb9", "1,143 \u8282\u70b9 \u00b7 834\u8fb9")]),
    ("README_DE.md", [("1.143 Knoten \u00b7 839 Kanten", "1.143 Knoten \u00b7 834 Kanten")]),
]
for p, pairs in jobs:
    t = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(p, "x%d" % c)
        assert c >= 1, c
        t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(t)
print("done")
