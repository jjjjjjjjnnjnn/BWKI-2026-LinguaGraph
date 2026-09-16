#!/usr/bin/env python3
"""Probe v1 portal JS structure (read-only)."""
import io
ls = io.open("cognitive-space/portal/index.html", encoding="utf-8").read().splitlines()
print("total", len(ls))
for n, l in enumerate(ls):
    if "function setLanguage" in l or "function browserLang" in l or "localStorage" in l:
        print(n + 1, l[:90])
o = io.open("C:\\Users\\rongj\\AppData\\Local\\Temp\\opencode\\jsprobe.txt", "w", encoding="utf-8")
for n in (2448, 2449, 2450, 2451, 2452, 2453, 2454, 2625, 2626, 2627, 2628, 2629, 2630, 2631, 2632, 2633, 2634, 2635):
    if n - 1 < len(ls):
        o.write("%d: %s\n" % (n, ls[n - 1][:120]))
o.close()
