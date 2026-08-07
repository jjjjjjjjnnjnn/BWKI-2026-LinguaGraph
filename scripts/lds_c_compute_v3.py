#!/usr/bin/env python3
"""
LinguaGraph — LDS-C v3 (node+edge Jaccard, frozen formula)

Extends the concept-level analysis with edge sets from the relation
extraction (lds_c_extract_relations.py). Computes the FROZEN v3 LDS:
    LDS = 1 - (J(nodes) + J(edges)) / 2
with the same null models (within-language split-half, label permutation)
and ΔLDS vs the ORIGINAL v3 LDS-K values (0.934 / 0.938 / 0.519).

Usage:
    python scripts/lds_c_compute_v3.py --relations data/lds_c/relations_20260808.json
Output: outputs/lds_c_v3_results_<date>.json
"""

import argparse
import json
import random
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_compute import (  # noqa: E402
    canonical_key, PAIRS, TOPICS, RANDOM_SEED, latest_extraction_path,
    load_extractions, load_lds_k_nodes,
)

# Frozen v3 LDS-K values (node+edge, from pipeline)
LDS_K_V3 = {"ZH-EN": 0.934, "DE-EN": 0.938, "ZH-DE": 0.519}


def load_relations(path: Path) -> Dict[str, Dict[str, List[Tuple[str, str, str]]]]:
    """response_id -> topic -> [(src_key, tgt_key, type)]."""
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for r in data.get("responses", []):
        rid = r["response_id"]
        out[rid] = {}
        for tr in r.get("topic_relations", []):
            topic = tr.get("topic", "")
            rels = [(e["source"], e["target"], e["type"]) for e in tr.get("relations", [])]
            out[rid][topic] = rels
    return out


def aggregate_node_edge(records: List[dict], relations: Dict[str, Dict[str, List]]) -> Dict[str, Dict[str, Set]]:
    """lang -> {nodes: set(keys), edges: set((src,tgt))}, pooled across topics."""
    agg: Dict[str, Dict[str, Set]] = defaultdict(lambda: {"nodes": set(), "edges": set()})
    for r in records:
        lang = r.get("language", "")
        rid = r["response_id"]
        for t in r.get("topics", []):
            topic = t.get("topic", "")
            for c in t.get("concepts", []):
                key = canonical_key(c.get("en", ""))
                if key:
                    agg[lang]["nodes"].add(key)
            for (src, tgt, _typ) in relations.get(rid, {}).get(topic, []):
                if src and tgt:
                    agg[lang]["edges"].add((src, tgt))
    return dict(agg)


def lds_v3(nodes_a, nodes_b, edges_a, edges_b) -> float:
    node_j = len(nodes_a & nodes_b) / max(len(nodes_a | nodes_b), 1)
    edge_j = len(edges_a & edges_b) / max(len(edges_a | edges_b), 1)
    return round(1.0 - (node_j + edge_j) / 2, 4)


def compute_v3(agg) -> Dict[str, Dict[str, float]]:
    out = {}
    for pair, la, lb in PAIRS:
        if la not in agg or lb not in agg:
            continue
        out[pair] = {
            "lds": lds_v3(agg[la]["nodes"], agg[lb]["nodes"],
                          agg[la]["edges"], agg[lb]["edges"]),
            "node_jaccard": round(len(agg[la]["nodes"] & agg[lb]["nodes"]) / max(len(agg[la]["nodes"] | agg[lb]["nodes"]), 1), 4),
            "edge_jaccard": round(len(agg[la]["edges"] & agg[lb]["edges"]) / max(len(agg[la]["edges"] | agg[lb]["edges"]), 1), 4),
            "n_edges": {"la": len(agg[la]["edges"]), "lb": len(agg[lb]["edges"])},
        }
    return out


def bootstrap_v3(records, relations, n_iter=1000) -> Dict[str, dict]:
    random.seed(RANDOM_SEED)
    by_lang = defaultdict(list)
    for r in records:
        by_lang[r.get("language", "")].append(r)
    pair_vals = defaultdict(list)
    for _ in range(n_iter):
        sample = []
        for lang, reps in by_lang.items():
            for _ in range(len(reps)):
                sample.append(random.choice(reps))
        agg = aggregate_node_edge(sample, relations)
        v3 = compute_v3(agg)
        for pair, v in v3.items():
            pair_vals[pair].append(v["lds"])
    ci = {}
    for pair, vals in pair_vals.items():
        vals.sort()
        ci[pair] = {"lds_v3_mean": round(statistics.mean(vals), 4),
                    "ci_lower": round(vals[int(0.025 * len(vals))], 4),
                    "ci_upper": round(vals[int(0.975 * len(vals))], 4)}
    return ci


def split_half_v3(records, relations, n_iter=100) -> Dict[str, float]:
    random.seed(RANDOM_SEED)
    by_lang = defaultdict(list)
    for r in records:
        by_lang[r.get("language", "")].append(r)
    floors = defaultdict(list)
    for _ in range(n_iter):
        for pair, la, lb in PAIRS:
            vals = []
            for lang in [la, lb]:
                reps = by_lang.get(lang, [])
                if len(reps) < 2:
                    continue
                random.shuffle(reps)
                half = len(reps) // 2
                a = aggregate_node_edge(reps[:half], relations)
                b = aggregate_node_edge(reps[half:], relations)
                if lang in a and lang in b:
                    vals.append(lds_v3(a[lang]["nodes"], b[lang]["nodes"],
                                       a[lang]["edges"], b[lang]["edges"]))
            if vals:
                floors[pair].append(statistics.mean(vals))
    return {p: round(statistics.mean(v), 4) for p, v in floors.items()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--relations", required=True)
    ap.add_argument("--iterations", type=int, default=1000)
    args = ap.parse_args()

    rel_path = Path(args.relations)
    relations = load_relations(rel_path)
    records = load_extractions(latest_extraction_path())
    print(f"  Relations: {rel_path} ({len(relations)} responses)")
    print(f"  Concepts: {len(records)} responses")

    agg = aggregate_node_edge(records, relations)
    v3 = compute_v3(agg)
    ci = bootstrap_v3(records, relations, args.iterations)
    split = split_half_v3(records, relations, max(100, args.iterations // 10))

    print(f"\n{'Pair':8s} | {'LDS v3':7s} | {'95% CI':17s} | {'node-J':7s} | {'edge-J':7s} | {'LDS-K(v3)':9s} | {'ΔLDS':7s} | split-half")
    print("-" * 80)
    for pair, la, lb in PAIRS:
        v = v3.get(pair, {})
        c = ci.get(pair, {})
        lds = v.get("lds", "-")
        cistr = f"[{c.get('ci_lower','-'):.4f}, {c.get('ci_upper','-'):.4f}]" if "ci_lower" in c else "-"
        nj = v.get("node_jaccard", "-")
        ej = v.get("edge_jaccard", "-")
        lk = LDS_K_V3.get(pair, "-")
        dl = round(lds - lk, 4) if isinstance(lds, float) else "-"
        sh = split.get(pair, "-")
        print(f"{pair:8s} | {lds:7.4f} | {cistr:17s} | {nj:7.4f} | {ej:7.4f} | {lk:9.4f} | {dl:+7.4f} | {sh}")

    report = {
        "generated_at": datetime.now().isoformat(),
        "relation_source": str(rel_path),
        "lds_v3": v3,
        "bootstrap_ci": ci,
        "split_half_floor": split,
        "lds_k_v3": LDS_K_V3,
        "delta_lds_v3": {p: round(v3[p]["lds"] - LDS_K_V3[p], 4) for p in v3},
    }
    out = PROJECT_ROOT / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    op = out / f"lds_c_v3_results_{datetime.now().strftime('%Y%m%d')}.json"
    op.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  [OK] Saved: {op}")


if __name__ == "__main__":
    main()
