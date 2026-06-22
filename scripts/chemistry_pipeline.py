#!/usr/bin/env python3
"""
Chemistry Pipeline — computes CDS/HDS for chemistry vs math, generates comparison.
"""

import json, re
from pathlib import Path
from collections import defaultdict

PROJECT_DIR = Path(__file__).resolve().parent.parent
CHEM_JSON = PROJECT_DIR / "config" / "expert_graphs" / "chemistry_full.json"
DATA_JS = PROJECT_DIR / "cognitive-space" / "web" / "data.js"
OUTPUT_JSON = PROJECT_DIR / "outputs" / "chemistry_comparison.json"

LV_ORDER = ["elementary", "middle", "high", "college"]
LV_LABELS = {"elementary": "Elementary", "middle": "Middle", "high": "High", "college": "College"}


def load_graph(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_data_js():
    with open(DATA_JS, "r", encoding="utf-8") as f:
        content = f.read()
    start = content.index("{")
    depth, end = 0, start
    for i in range(start, len(content)):
        if content[i] == "{": depth += 1
        elif content[i] == "}": depth -= 1
        if depth == 0: end = i + 1; break
    raw = content[start:end].strip()
    if raw.endswith(";"): raw = raw[:-1]
    raw = re.sub(r",\s*([}\]])", r"\1", raw)
    data = json.loads(raw)
    return data["nodes"], data["links"]


def compute_cds_by_level(nodes, links):
    lv_nodes = defaultdict(set)
    node_lookup = {n["id"]: n["level"] for n in nodes}
    for n in nodes:
        lv_nodes[n["level"]].add(n["id"])
    lv_edges = defaultdict(set)
    for l in links:
        src_lv = node_lookup.get(l["source"])
        tgt_lv = node_lookup.get(l["target"])
        if src_lv and tgt_lv and src_lv == tgt_lv:
            lv_edges[src_lv].add((l["source"], l["target"]))
    results = {}
    for lv in LV_ORDER:
        n = len(lv_nodes.get(lv, []))
        e = len(lv_edges.get(lv, []))
        cds = (2 * e) / (n * (n - 1)) if n > 1 else 0.0
        results[lv] = {"nodes": n, "edges": e, "cds": round(cds, 4)}
    return results


def compute_hds(nodes, links):
    prereq_kw = ["prerequisite", "requires", "depends_on", "part_of"]
    children = defaultdict(list)
    has_parents = defaultdict(list)
    for l in links:
        rel = (l.get("type") or l.get("relation") or "").lower()
        if any(k in rel for k in prereq_kw):
            children[l["source"]].append(l["target"])
            has_parents[l["target"]].append(l["source"])
    all_ids = set(n["id"] for n in nodes)
    roots = all_ids - set(has_parents.keys())
    depths = {}
    def dfs(node, visited):
        if node in depths: return depths[node]
        if not children[node]: return 0
        max_d = 0
        for child in children[node]:
            if child in visited: continue
            visited.add(child)
            d = 1 + dfs(child, visited)
            visited.discard(child)
            max_d = max(max_d, d)
        depths[node] = max_d
        return max_d
    for r in roots: dfs(r, {r})
    for c in all_ids:
        if c not in depths: depths[c] = 0
    return depths


def main():
    print("=== Chemistry Pipeline ===\n")

    # Load chemistry
    chem = load_graph(CHEM_JSON)
    chem_nodes = [{"id": c["name"], "level": c.get("level", "college")} for c in chem["concepts"]]
    chem_links = [{"source": r["source"], "target": r["target"],
                    "type": r.get("type", "relates_to"), "relation": r.get("relation", r.get("type", "relates_to"))}
                   for r in chem["relations"]]

    # Load math from data.js
    math_nodes_raw, math_links_raw = load_data_js()
    math_node_ids = set(n["id"] for n in math_nodes_raw if n.get("group") != "chemistry")
    math_nodes = [n for n in math_nodes_raw if n["id"] in math_node_ids]
    math_links = [{"source": l["source"], "target": l["target"],
                    "type": l.get("type", "relates_to"), "relation": l.get("relation", l.get("type", "relates_to"))}
                   for l in math_links_raw if l["source"] in math_node_ids and l["target"] in math_node_ids]

    print(f"Chemistry: {len(chem_nodes)} concepts, {len(chem_links)} relations")
    print(f"Math:      {len(math_nodes)} nodes, {len(math_links)} links")

    # CDS
    chem_cds = compute_cds_by_level(chem_nodes, chem_links)
    math_cds = compute_cds_by_level(math_nodes, math_links)

    print("\n=== CDS Comparison ===")
    print(f"{'Level':<12} {'Chemistry':>12} {'Math':>12}")
    print("-" * 38)
    for lv in LV_ORDER:
        c = chem_cds[lv]["cds"]
        m = math_cds[lv]["cds"]
        print(f"{lv:<12} {c:>12.4f} {m:>12.4f}")

    # HDS
    chem_hds = compute_hds(chem_nodes, chem_links)
    math_hds = compute_hds(
        [{"id": n["id"], "level": n["level"]} for n in math_nodes],
        math_links
    )
    max_d_c = max(chem_hds.values()) if chem_hds else 0
    mean_d_c = sum(chem_hds.values()) / max(len(chem_hds), 1)
    max_d_m = max(math_hds.values()) if math_hds else 0
    mean_d_m = sum(math_hds.values()) / max(len(math_hds), 1)
    roots_c = sum(1 for d in chem_hds.values() if d == 0)
    roots_m = sum(1 for d in math_hds.values() if d == 0)

    print(f"\n=== HDS Comparison ===")
    print(f"{'Metric':<25} {'Chemistry':>10} {'Math':>10}")
    print("-" * 48)
    print(f"{'Max depth':<25} {max_d_c:>10} {max_d_m:>10}")
    print(f"{'Mean depth':<25} {mean_d_c:>10.2f} {mean_d_m:>10.2f}")
    print(f"{'Root concepts':<25} {roots_c:>10} {roots_m:>10}")

    # Save
    comparison = {
        "chemistry": {
            "concepts": len(chem_nodes), "relations": len(chem_links),
            "cds": chem_cds,
            "hds": {"max_depth": max_d_c, "mean_depth": round(mean_d_c, 4), "root_count": roots_c}
        },
        "math": {
            "concepts": len(math_nodes), "relations": len(math_links),
            "cds": math_cds,
            "hds": {"max_depth": max_d_m, "mean_depth": round(mean_d_m, 4), "root_count": roots_m}
        }
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False)

    chem_peak = max(chem_cds, key=lambda k: chem_cds[k]["cds"])
    math_peak = max(math_cds, key=lambda k: math_cds[k]["cds"])
    print(f"\n=== Key Findings ===")
    print(f"Chemistry CDS peak: {chem_peak} (CDS={chem_cds[chem_peak]['cds']})")
    print(f"Math CDS peak:      {math_peak} (CDS={math_cds[math_peak]['cds']})")
    if chem_peak != math_peak:
        print(f">>> CROSS-DISCIPLINARY: Chemistry peaks at {chem_peak}, Math peaks at {math_peak}")
    else:
        print(f"   Both peak at {chem_peak}")

    print(f"\n[OK] Saved: {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
