#!/usr/bin/env python3
"""LinguaGraph — D: node/edge decomposition symmetry across sources.

Extends A4's edge-contribution finding into a cross-domain symmetry test.

A4 finding: in MATH (institutional knowledge), ZH-DE convergence is carried
largely by the EDGE component (edge adds +0.075 LDS beyond node-only, ~3-4x
ZH-EN/DE-EN). Question for this script:

  Does the "social/institutional reversal" (ZH-DE most convergent in math,
  most divergent in social Wikipedia) hold at the EDGE level too, or is it a
  node-level (concept-choice) artifact?

For each source x pair, decompose the frozen v3 LDS = 1 - mean(J_node, J_edge)
into node-only vs edge contribution:
    node_only_lds = 1 - J_node
    edge_contribution = (J_node - J_edge) / 2   (divergence added by edges)

Sources (reusing lds_k_deepen parsing for exact A4 consistency):
  - math textbooks (institutional): math_by_level() pooled
  - Wikipedia social (cultural):   wiki_graphs() pooled
  - human v3 (cognitive):          data/lds_c/relations_20260808.json

Deliverable: is the reversal present in BOTH node and edge components? If yes,
the reversal is a genuine structural (relational) difference, not a lexical
surface artifact. Also reports which component carries more divergence per
source (complements A4 §5.2).

Output: data/lds_c/lds_k_deep/node_edge_decomp_<date>.json + console table.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_compute import canonical_key, PAIRS  # noqa: E402
from lds_k_deepen import (  # noqa: E402
    TOPIC_SLUG,
    LANG_CODES,
    TOPICS,
    load_json,
    math_by_level,
    wiki_graphs,
)

OUT_DIR = PROJECT_ROOT / "data" / "lds_c" / "lds_k_deep"


def load_wiki_gloss() -> Dict[str, str]:
    files = sorted((PROJECT_ROOT / "data" / "wikipedia_extractions").glob("wiki_gloss_*.json"))
    if not files:
        return {}
    data = load_json(files[-1])
    # wiki_gloss JSON: top-level {"glosses": {src_lang_word: en, ...}}
    glosses = data.get("glosses", {})
    # tolerance for older cell-based layout
    if not glosses:
        for c in data.get("cells", []):
            for src, en in c.get("glosses", {}).items():
                glosses[src] = en
    return glosses


def math_pooled() -> Dict[str, dict]:
    """lang -> {nodes, edges} pooled across levels (raw labels, as A4)."""
    levels, _ = math_by_level()
    out: Dict[str, dict] = {}
    for lang in LANG_CODES:
        nodes, edges = set(), set()
        for lv in levels.values():
            nodes |= lv[lang]["nodes"]
            edges |= lv[lang]["edges"]
        out[lang] = {"nodes": nodes, "edges": edges}
    return out


def wiki_pooled(gloss: Dict[str, str]) -> Dict[str, dict]:
    """lang -> {nodes, edges} pooled across 5 social topics."""
    w = wiki_graphs(gloss)
    out: Dict[str, dict] = {}
    for lang in LANG_CODES:
        nodes, edges = set(), set()
        for t in TOPICS:
            if lang in w.get(t, {}):
                nodes |= w[t][lang]["nodes"]
                edges |= w[t][lang]["edges"]
        out[lang] = {"nodes": nodes, "edges": edges}
    return out


def human_pooled() -> Dict[str, dict]:
    """lang -> {nodes, edges} from 15 human responses' relation extractions.

    Edges use (src, tgt) BINARY tuples — matching scripts/lds_c_compute_v3.py and
    the wiki/math graphs — so the edge component is comparable across sources
    (audit M7)."""
    files = sorted((PROJECT_ROOT / "data" / "lds_c").glob("relations_*.json"))
    data = load_json(files[-1])
    out: Dict[str, dict] = {}
    nodes: Dict[str, set] = defaultdict(set)
    edges: Dict[str, set] = defaultdict(set)
    for resp in data.get("responses", []):
        lang = resp.get("language", "")
        for t in resp.get("topic_relations", []) or []:
            for rel in t.get("relations", []) or []:
                s = canonical_key(rel.get("source", ""))
                tg = canonical_key(rel.get("target", ""))
                if s:
                    nodes[lang].add(s)
                if tg:
                    nodes[lang].add(tg)
                if s and tg:
                    edges[lang].add((s, tg))  # binary tuple, type dropped (audit M7)
    for lang in LANG_CODES:
        out[lang] = {"nodes": nodes.get(lang, set()), "edges": edges.get(lang, set())}
    return out


def decompose(graphs: Dict[str, dict]) -> Dict[str, dict]:
    """Per-pair node/edge decomposition of frozen v3 LDS."""
    out: Dict[str, dict] = {}
    for pair, la, lb in PAIRS:
        if la not in graphs or lb not in graphs:
            continue
        a, b = graphs[la], graphs[lb]
        sa, sb = a["nodes"], b["nodes"]
        jn = len(sa & sb) / max(len(sa | sb), 1)
        ea, eb = a["edges"], b["edges"]
        je = len(ea & eb) / max(len(ea | eb), 1)
        lds = 1.0 - (jn + je) / 2
        node_only = 1.0 - jn
        edge_contrib = (jn - je) / 2
        out[pair] = {
            "lds_v3": round(lds, 4),
            "j_node": round(jn, 4),
            "j_edge": round(je, 4),
            "node_only_lds": round(node_only, 4),
            "edge_contribution": round(edge_contrib, 4),
            "n_nodes": {"a": len(sa), "b": len(sb)},
            "n_edges": {"a": len(ea), "b": len(eb)},
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Node/edge decomposition symmetry (D)")
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    gloss = load_wiki_gloss()
    print(f"  wiki gloss: {len(gloss)} entries")

    print("Loading math (institutional)...")
    math = math_pooled()
    print("Loading Wikipedia (social)...")
    wiki = wiki_pooled(gloss)
    print("Loading human (cognitive)...")
    human = human_pooled()

    result = {
        "design": "node_edge_decomposition",
        "generated_at": datetime.now().isoformat(),
        "formula": "LDS v3 = 1 - mean(J_node, J_edge); edge_contribution = (J_node - J_edge)/2",
        "lineage": {
            "math": "data/math_extractions/merged/aligned_data.json",
            "wiki": "data/wikipedia_extractions/*_{zh,en,de}.json + latest wiki_gloss_*.json",
            "human": "latest data/lds_c/relations_*.json",
            "note": "sources recorded for reproducibility (audit M9/M12)",
        },
        "edge_tuple_dimension": (
            "ALL sources use BINARY (src, tgt) edge tuples (audit M7): human edges "
            "match scripts/lds_c_compute_v3.py; wiki/math match lds_k_deepen.py. "
            "J_edge values are therefore comparable across sources."),
        "math_institutional": decompose(math),
        "wiki_social": decompose(wiki),
        "human_cognitive": decompose(human),
        "interpretation": (
            "If the social/institutional ZH-DE reversal appears in BOTH the "
            "node component (1-J_node) and the edge contribution ((J_node-J_edge)/2), "
            "it is a genuine structural difference, not a lexical surface artifact."
        ),
    }

    out_path = OUT_DIR / (args.out or f"node_edge_decomp_{datetime.now().strftime('%Y%m%d')}.json")
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  Saved: {out_path}")

    print("\n=== Node/edge decomposition across sources ===")
    hdr = f"{'Source':20s} | {'Pair':8s} | {'LDS':6s} | {'J_node':7s} | {'J_edge':7s} | {'node-only':9s} | {'edge+':7s}"
    print(hdr)
    print("-" * len(hdr))
    for src_key, label in [("math_institutional", "math (institutional)"),
                           ("wiki_social", "wiki (social/cultural)"),
                           ("human_cognitive", "human (cognitive)")]:
        for pair, _, _ in PAIRS:
            row = result[src_key].get(pair)
            if not row:
                continue
            print(f"{label:20s} | {pair:8s} | {row['lds_v3']:6} | {row['j_node']:7} | "
                  f"{row['j_edge']:7} | {row['node_only_lds']:9} | {row['edge_contribution']:7}")

    # Reversal check
    print("\n=== ZH-DE reversal check (node vs edge component) ===")
    m = result["math_institutional"].get("ZH-DE", {})
    w = result["wiki_social"].get("ZH-DE", {})
    if m and w:
        node_reversal = m["node_only_lds"] < w["node_only_lds"]
        edge_reversal = m["edge_contribution"] < w["edge_contribution"]
        print(f"  node-only:    math {m['node_only_lds']}  vs  wiki {w['node_only_lds']}  "
              f"-> reversal at node level? {node_reversal}")
        print(f"  edge contrib: math {m['edge_contribution']}  vs  wiki {w['edge_contribution']}  "
              f"-> reversal at edge level? {edge_reversal}")
        print(f"  => {'REVERSAL HOLDS IN BOTH COMPONENTS (structural, not lexical)' if node_reversal and edge_reversal else 'component-dependent'}")


if __name__ == "__main__":
    main()
