#!/usr/bin/env python3
"""Konnektivität correct methodology (read-only)."""
import io
import json

v = json.load(io.open("data/math_extractions/merged/visualization_data.json", encoding="utf-8"))
nodes = [n["id"] for n in v["nodes"]]
adj = {n: set() for n in nodes}
m = 0
for e in v["links"]:
    s, t = e["source"], e["target"]
    if s in adj and t in adj:
        m += 1
        if s != t:
            adj[s].add(t)
            adj[t].add(s)
        else:
            adj[s].add(t)
n = len(nodes)
dens = 2 * m / (n * (n - 1))
seen, comps, largest = set(), 0, 0
for s in nodes:
    if s not in seen:
        comps += 1
        stack, sz = [s], 0
        seen.add(s)
        while stack:
            u = stack.pop()
            sz += 1
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        largest = max(largest, sz)
dz = sum(1 for s in nodes if not adj[s])
o = io.open("C:\\Users\\rongj\\AppData\\Local\\Temp\\opencode\\konn2.txt", "w", encoding="utf-8")
o.write("links=%d nodes=%d density=%.4f comps=%d degree_zero=%d (%.1f%%) largest=%d\n"
        % (m, n, dens, comps, dz, 100.0 * dz / n, largest))
o.write("frozen was: 238 / 0.0015 / 388 / 381 (68.5%%) / 121\n")
o.close()
print("ok")
