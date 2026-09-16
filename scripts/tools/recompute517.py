#!/usr/bin/env python3
"""Recompute LDS-K + Konnektivität + HDS on rebuilt merged data (read-only)."""
import io
import json
import sys

sys.path.insert(0, "scripts/figures")
from _lds_utils import lds_pair, load_aligned, get_lang_graphs

al = load_aligned()
ln, le = get_lang_graphs(al)
o = io.open("C:\\Users\\rongj\\AppData\\Local\\Temp\\opencode\\recompute.txt", "w", encoding="utf-8")
for (a, b) in (("zh", "en"), ("de", "en"), ("zh", "de")):
    v = lds_pair(ln[a], ln[b], le[a], le[b])
    o.write("LDS-K %s-%s = %.4f (frozen: %s)\n" % (a, b, v,
            {"zh-en": 0.934, "de-en": 0.938, "zh-de": 0.519}["%s-%s" % (a, b)]))
    o.write("  edges %s=%d %s=%d\n" % (a, len(le[a]), b, len(le[b])))
# Konnektivität on visualization graph
v = json.load(io.open("data/math_extractions/merged/visualization_data.json", encoding="utf-8"))
nodes = [n["id"] if isinstance(n, dict) else n for n in v["nodes"]]
adj = {n: set() for n in nodes}
for e in v["links"]:
    s = e["source"] if isinstance(e["source"], str) else e["source"].get("id")
    t = e["target"] if isinstance(e["target"], str) else e["target"].get("id")
    if s in adj and t in adj:
        adj[s].add(t)
        adj[t].add(s)
n = len(nodes)
m = sum(len(x) for x in adj.values()) // 2
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
o.write("Konnektivität: links=%d nodes=%d density=%.4f comps=%d degree_zero=%d (%.1f%%) largest=%d\n"
        % (m, n, dens, comps, dz, 100.0 * dz / n, largest))
o.write("frozen was: 238 links, 0.0015, 388 comps, 381 (68.5%%), largest 121\n")
o.close()
print("ok")
