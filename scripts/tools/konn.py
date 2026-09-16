#!/usr/bin/env python3
"""Konnektivität with raw methodology + endpoint format audit (read-only)."""
import io
import json

v = json.load(io.open("data/math_extractions/merged/visualization_data.json", encoding="utf-8"))
nodes = v["nodes"]
n0 = nodes[0]
o = io.open("C:\\Users\\rongj\\AppData\\Local\\Temp\\opencode\\konn.txt", "w", encoding="utf-8")
o.write("node0=%r\n" % (n0,))
o.write("link0=%r\n" % (v["links"][0],))
nids = {n["id"] if isinstance(n, dict) else n for n in nodes}
miss = 0
for e in v["links"]:
    s = e["source"] if isinstance(e["source"], str) else e["source"].get("id")
    t = e["target"] if isinstance(e["target"], str) else e["target"].get("id")
    if s not in nids or t not in nids:
        miss += 1
o.write("links=%d endpoints-missing-node=%d\n" % (len(v["links"]), miss))
o.close()
print("ok")
