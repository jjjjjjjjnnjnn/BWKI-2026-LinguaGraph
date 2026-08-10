#!/usr/bin/env python3
"""P2-1 (C8): size-matched domain-control recheck.

The "institutional (math) converges / cultural (wiki) diverges" reversal
(node-only 0.444 vs 0.800) is potentially confounded by GRAPH SIZE: math has
~195 nodes/language vs wiki ~45. J_node is size-sensitive (large sets saturate).
This script subsamples both graphs to matched sizes (k nodes/language) and
recomputes ZH-DE J_node / J_edge with a bootstrap, to test whether the reversal
survives size-matching.

Zero API — uses committed data. Outputs a console table + JSON.
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_node_edge_decomp import math_pooled, wiki_pooled  # noqa: E402


def jaccard(a, b):
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return float("nan")
    return len(sa & sb) / len(sa | sb)


def subsample_graph(nodes, edges, k, rng):
    """Subsample k nodes (preserving edges whose BOTH endpoints survive)."""
    nodes = list(nodes)
    if len(nodes) <= k:
        return set(nodes), set(edges)
    sampled = set(rng.sample(nodes, k))
    new_edges = {(s, t) for (s, t) in edges if s in sampled and t in sampled}
    return sampled, new_edges


def size_match(graph, la, lb, ks, n_iter=200, seed=20260810):
    """For each k, subsample each language's graph to k nodes, compute
    J_node/J_edge for (la,lb), bootstrap mean/SD."""
    rng = random.Random(seed)
    out = {}
    ga, gb = graph.get(la, {}), graph.get(lb, {})
    maxk = min(len(ga.get("nodes", [])), len(gb.get("nodes", [])), max(ks))
    for k in ks:
        if k > maxk:
            continue
        jn, je = [], []
        for _ in range(n_iter):
            sa, ea = subsample_graph(ga.get("nodes", []), ga.get("edges", []), k, rng)
            sb, eb = subsample_graph(gb.get("nodes", []), gb.get("edges", []), k, rng)
            jn.append(jaccard(sa, sb))
            je.append(jaccard(ea, eb))
        out[k] = {
            "j_node_mean": round(sum(x for x in jn if x == x) / max(1, len([x for x in jn if x == x])), 3),
            "j_edge_mean": round(sum(x for x in je if x == x) / max(1, len([x for x in je if x == x])), 3),
            "n_sim": len([x for x in jn if x == x]),
        }
    return out


def main() -> None:
    # load wiki gloss (ZH/DE -> English) needed by wiki_graphs
    from lds_c_node_edge_decomp import load_wiki_gloss
    gloss = load_wiki_gloss()

    math = math_pooled()  # lang -> {nodes, edges} (aligned labels)
    wiki = wiki_pooled(gloss)  # lang -> {nodes, edges} (independent extraction)

    print("=== Node counts per language ===")
    for name, g in [("math (aligned)", math), ("wiki (independent)", wiki)]:
        for lang in ("zh", "de", "en"):
            n = len(g.get(lang, {}).get("nodes", []))
            e = len(g.get(lang, {}).get("edges", []))
            print(f"  {name:<20} {lang}: {n} nodes, {e} edges")

    KS = [15, 25, 35, 45, 60, 100]
    print("\n=== ZH-DE J_node vs sample size k (bootstrap mean) ===")
    print(f"{'k':>5} | {'math aligned':>18} | {'wiki independent':>18} | gap (math-wiki)")
    for k in KS:
        m = size_match(math, "zh", "de", [k], n_iter=200).get(k)
        w = size_match(wiki, "zh", "de", [k], n_iter=200).get(k)
        if not m or not w:
            continue
        gap = m["j_node_mean"] - w["j_node_mean"]
        print(f"{k:>5} | {m['j_node_mean']:>12} | {w['j_node_mean']:>12}   | {gap:+.3f}")

    print("\n=== Full-size ZH-DE (reference, from committed data) ===")
    # math J_node full-size
    jn_full_m = jaccard(math["zh"]["nodes"], math["de"]["nodes"])
    jn_full_w = jaccard(wiki["zh"]["nodes"], wiki["de"]["nodes"])
    print(f"  math full J_node = {jn_full_m:.3f}, wiki full J_node = {jn_full_w:.3f}")


if __name__ == "__main__":
    main()
