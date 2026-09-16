#!/usr/bin/env python3
"""Check whether the 8 ring-deleted edges exist in merged relations (read-only)."""
import io
import json

RING = [
    ("counting", "place value", "requires"),
    ("Erwartungswert", "Varianz", "requires"),
    ("variable", "equation", "requires"),
    ("克", "千克", "representation"),
    ("相似三角形", "全等三角形", "generalization"),
    ("方向导数", "梯度", "representation"),
    ("长方形", "正方形", "generalization"),
    ("area", "perimeter", "analogy"),
]
d = json.load(io.open("data/math_extractions/merged/aligned_data.json", encoding="utf-8"))
rels = d.get("relations", [])
o = io.open("C:\\Users\\rongj\\AppData\\Local\\Temp\\opencode\\ringmerged.txt", "w", encoding="utf-8")
o.write("merged relations N=%d\n" % len(rels))
s = io.open("C:\\Users\\rongj\\AppData\\Local\\Temp\\opencode\\relkeys.txt", "w", encoding="utf-8")
for r in rels[:3]:
    s.write(repr(list(r.keys())) + "\n")
s.close()
for (src, tgt, typ) in RING:
    hits = [i for i, r in enumerate(rels)
            if r.get("source") == src and r.get("target") == tgt and r.get("type") == typ]
    o.write("%s -> %s (%s): merged_idx=%s\n" % (src, tgt, typ, hits))
o.close()
print("ok")
