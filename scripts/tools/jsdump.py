#!/usr/bin/env python3
"""Dump v1 JS core (read-only)."""
import io
ls = io.open("cognitive-space/portal/index.html", encoding="utf-8").read().splitlines()
o = io.open("C:\\Users\\rongj\\AppData\\Local\\Temp\\opencode\\jscore.txt", "w", encoding="utf-8")
for n in range(2453, 2628):
    o.write("%d: %s\n" % (n + 1, ls[n]))
o.close()
print("ok")
