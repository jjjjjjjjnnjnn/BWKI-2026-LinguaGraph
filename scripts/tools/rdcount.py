#!/usr/bin/env python3
"""README number unification batch (SSOT 59/54/177, 556/525/219)."""
import glob
import io
import os

counts = {}
for fp in glob.glob(os.path.join("data", "math_extractions", "*.json")):
    b = os.path.basename(fp)
    if b.startswith("zh_"):
        counts["zh"] = counts.get("zh", 0) + 1
    elif b.startswith("en_"):
        counts["en"] = counts.get("en", 0) + 1
    elif b.startswith("de_"):
        counts["de"] = counts.get("de", 0) + 1
print("math_extractions:", counts)

o = io.open("C:\\Users\\rongj\\AppData\\Local\\Temp\\opencode\\final18.txt", "w", encoding="utf-8")
ls = io.open("submission/final/README.md", encoding="utf-8").read().splitlines()
o.write("L17: " + ls[16] + "\nL18: " + ls[17] + "\n")
o.close()
