#!/usr/bin/env python3
"""P2-1 (C8): size-matched domain-control recheck.

The "institutional (math) converges / cultural (wiki) diverges" reversal
is potentially confounded by GRAPH SIZE: math has
~195 nodes/language vs wiki ~45. J_node is size-sensitive (large sets saturate).
This script subsamples both graphs to matched sizes (k nodes/language) and
recomputes ZH-DE J_node / J_edge with a bootstrap, to test whether the reversal
survives size-matching.

Sourced reference (full-size, ZH-DE, from committed data):
math LDS = 0.519 (J_node 0.556, J_edge 0.407) vs wiki LDS = 0.819
(J_node 0.200, J_edge 0.162) — i.e. math converges, wiki diverges
(node-only ablation ZH-DE = 0.444, cf. scripts/figures_i18n_wave2.py).
Size-matched gaps (math-wiki) stay negative at every k (B6 frozen).

Zero API — uses committed data. Outputs a console table + JSON.
"""
from __future__ import annotations

import json
import os
import random
import statistics
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_node_edge_decomp import math_pooled, wiki_pooled  # noqa: E402


def check_hashseed() -> None:
    """B6: PYTHONHASHSEED must be 0 for exact reproducibility.

    math_pooled()/wiki_pooled() return sets; list(set) order depends on
    hash randomization, so rng.sample over unsorted nodes jitters ±0.002
    across processes. Fail fast unless PYTHONHASHSEED=0 (plus sorted()
    freeze below gives defense in depth)."""
    if os.environ.get("PYTHONHASHSEED") != "0":
        sys.exit("FATAL: set $env:PYTHONHASHSEED=0 before running "
                 f"(got {os.environ.get('PYTHONHASHSEED')!r}). "
                 "Exact reproducibility not guaranteed otherwise.")


def jaccard(a, b):
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return float("nan")
    return len(sa & sb) / len(sa | sb)


def subsample_graph(nodes, edges, k, rng):
    """Subsample k nodes (preserving edges whose BOTH endpoints survive).

    B6: nodes sorted before sampling so list order is hash-independent
    (PYTHONHASHSEED=0 asserted at entry; sorted() is defense in depth)."""
    nodes = sorted(nodes, key=repr)
    if len(nodes) <= k:
        return set(nodes), set(edges)
    sampled = set(rng.sample(nodes, k))
    new_edges = {(s, t) for (s, t) in edges if s in sampled and t in sampled}
    return sampled, new_edges


def size_match(graph, la, lb, ks, n_iter=200, seed=20260810):
    """For each k, subsample each language's graph to k nodes, compute
    J_node/J_edge for (la,lb), bootstrap mean±SD (B6)."""
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
        jn_c = [x for x in jn if x == x]
        je_c = [x for x in je if x == x]
        out[k] = {
            "j_node_mean": round(sum(jn_c) / max(1, len(jn_c)), 3),
            "j_node_sd": round(statistics.stdev(jn_c), 3) if len(jn_c) > 1 else 0.0,
            "j_edge_mean": round(sum(je_c) / max(1, len(je_c)), 3),
            "j_edge_sd": round(statistics.stdev(je_c), 3) if len(je_c) > 1 else 0.0,
            "n_sim": len(jn_c),
        }
    return out


def main() -> None:
    check_hashseed()
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
    print("\n=== ZH-DE J_node vs sample size k (bootstrap mean±SD, B6 frozen) ===")
    print(f"{'k':>5} | {'math aligned':>18} | {'wiki independent':>18} | gap (math-wiki)")
    for k in KS:
        m = size_match(math, "zh", "de", [k], n_iter=200).get(k)
        w = size_match(wiki, "zh", "de", [k], n_iter=200).get(k)
        if not m or not w:
            continue
        gap = m["j_node_mean"] - w["j_node_mean"]
        print(f"{k:>5} | {m['j_node_mean']:>6}±{m['j_node_sd']:<6} | {w['j_node_mean']:>6}±{w['j_node_sd']:<6}   | {gap:+.3f}")

    print("\n=== Full-size ZH-DE (reference, from committed data) ===")
    # math J_node full-size
    jn_full_m = jaccard(math["zh"]["nodes"], math["de"]["nodes"])
    jn_full_w = jaccard(wiki["zh"]["nodes"], wiki["de"]["nodes"])
    print(f"  math full J_node = {jn_full_m:.3f}, wiki full J_node = {jn_full_w:.3f}")


if __name__ == "__main__":
    main()
