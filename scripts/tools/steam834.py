#!/usr/bin/env python3
"""STEAM 839->834 leftovers (longest-first)."""
import io
jobs = [
    ("README.md", [("(1,143 nodes · 839 links, no cross-links)", "(1,143 nodes · 834 links, no cross-links)"),
                   ("1,143 nodes · 839 links", "1,143 nodes · 834 links")]),
    ("docs/SSOT-web.md", [("1143 nodes / 839 intra-discipline links", "1143 nodes / 834 intra-discipline links")]),
]
for p, pairs in jobs:
    t = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(p, repr(old[:34]), "x%d" % c)
        t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(t)
print("done")
