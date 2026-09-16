#!/usr/bin/env python3
"""Dump README fix contexts (read-only)."""
import io
o = io.open("C:\\Users\\rongj\\AppData\\Local\\Temp\\opencode\\rdctx.txt", "w", encoding="utf-8")
for p, keys in [
    ("submission/final/README.md", ["F12", "177er", "Phase-3b"]),
    ("cognitive-space/README.md", ["574", "557", "219", "37/46", "45ZH", "45", "20EN", "10DE"]),
    ("submission/pitch/README.md", ["55 Messungen", "87"]),
]:
    ls = io.open(p, encoding="utf-8").read().splitlines()
    o.write("===== " + p + " (" + str(len(ls)) + " lines)\n")
    for n, l in enumerate(ls):
        if any(k in l for k in keys):
            o.write("%d: %s\n" % (n + 1, l[:200]))
o.close()
print("ok")
