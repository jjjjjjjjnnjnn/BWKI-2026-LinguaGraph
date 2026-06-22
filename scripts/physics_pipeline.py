#!/usr/bin/env python3
"""
Physics Pipeline — converts physics_full.json into data.js format,
runs CDS/HDS metrics, and generates comparison figures.
"""

import json, sys, re
from pathlib import Path
from collections import defaultdict

PROJECT_DIR = Path(__file__).resolve().parent.parent
PHYSICS_JSON = PROJECT_DIR / "config" / "expert_graphs" / "physics_full.json"
DATA_JS = PROJECT_DIR / "cognitive-space" / "web" / "data.js"
OUTPUT_JSON = PROJECT_DIR / "outputs" / "physics_comparison.json"

LV_ORDER = ["elementary", "middle", "high", "college"]


def load_graph(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def graph_to_cognitivespace(graph):
    """Convert physics_full.json format to data.js compatible format."""
    nodes = []
    for c in graph["concepts"]:
        level = c.get("level", "college")
        nodes.append({
            "id": c["name"],
            "name": c["display_name"],
            "labels": c.get("labels", {}),
            "group": "physics",
            "level": level,
            "level_order": LV_ORDER.index(level) if level in LV_ORDER else 3,
            "importance": 5,
            "source_count": len(c.get("source_references", [])),
            "cross_references": c.get("source_references", [])
        })

    links = []
    for r in graph["relations"]:
        links.append({
            "source": r["source"],
            "target": r["target"],
            "type": r.get("type", "relates_to"),
            "relation": r.get("relation", r.get("type", "relates_to"))
        })

    return {"nodes": nodes, "links": links}


def load_data_js():
    """Load nodes and links from data.js (the visualization file, which has correct levels)."""
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
    """CDS = 2|E| / (|V| * (|V|-1)) per level."""
    lv_nodes = defaultdict(set)
    lv_edges = defaultdict(set)

    for n in nodes:
        lv_nodes[n["level"]].add(n["id"])

    node_lookup = {n["id"]: n["level"] for n in nodes}

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
    """HDS = longest prerequisite chain depth."""
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
        if node in depths:
            return depths[node]
        if not children[node]:
            return 0
        max_d = 0
        for child in children[node]:
            if child in visited:
                continue
            visited.add(child)
            d = 1 + dfs(child, visited)
            visited.discard(child)
            max_d = max(max_d, d)
        depths[node] = max_d
        return max_d

    for r in roots:
        dfs(r, {r})

    for c in all_ids:
        if c not in depths:
            depths[c] = 0

    return depths


def main():
    print("=== Physics Pipeline ===\n")

    # Load physics graph
    physics = load_graph(PHYSICS_JSON)
    print(f"Physics: {len(physics['concepts'])} concepts, {len(physics['relations'])} relations")

    # Load math from data.js (has correct levels)
    math_nodes, math_links_raw = load_data_js()
    # Only keep math nodes (not physics if any)
    math_node_ids = set(n["id"] for n in math_nodes if n.get("group") != "physics")
    math_nodes = [n for n in math_nodes if n["id"] in math_node_ids]
    math_links = [{"source": l["source"], "target": l["target"],
                    "type": l.get("type", "relates_to"), "relation": l.get("relation", l.get("type", "relates_to"))}
                   for l in math_links_raw if l["source"] in math_node_ids and l["target"] in math_node_ids]
    print(f"Math (from data.js): {len(math_nodes)} nodes, {len(math_links)} links")

    # Convert to data.js format
    cs_data = graph_to_cognitivespace(physics)
    nodes = cs_data["nodes"]
    links = cs_data["links"]

    print(f"\nConverted: {len(nodes)} nodes, {len(links)} links")

    # CDS comparison
    physics_cds = compute_cds_by_level(nodes, links)
    math_cds = compute_cds_by_level(math_nodes, math_links)

    print("\n=== CDS Comparison ===")
    print(f"{'Level':<12} {'Physics CDS':>12} {'Math CDS':>12} {'Ratio':>8}")
    print("-" * 48)
    for lv in LV_ORDER:
        p = physics_cds[lv]["cds"]
        m = math_cds[lv]["cds"]
        ratio = p / m if m > 0 else float('inf')
        print(f"{lv:<12} {p:>12.4f} {m:>12.4f} {ratio:>8.2f}")

    # HDS comparison
    physics_hds = compute_hds(nodes, links)
    math_hds = compute_hds(
        [{"id": n["id"], "level": n["level"]} for n in math_nodes],
        math_links
    )

    max_depth_p = max(physics_hds.values()) if physics_hds else 0
    mean_depth_p = sum(physics_hds.values()) / max(len(physics_hds), 1)
    max_depth_m = max(math_hds.values()) if math_hds else 0
    mean_depth_m = sum(math_hds.values()) / max(len(math_hds), 1)

    roots_p = sum(1 for d in physics_hds.values() if d == 0)
    roots_m = sum(1 for d in math_hds.values() if d == 0)

    print(f"\n=== HDS Comparison ===")
    print(f"{'Metric':<25} {'Physics':>10} {'Math':>10}")
    print("-" * 48)
    print(f"{'Max depth':<25} {max_depth_p:>10} {max_depth_m:>10}")
    print(f"{'Mean depth':<25} {mean_depth_p:>10.2f} {mean_depth_m:>10.2f}")
    print(f"{'Root concepts':<25} {roots_p:>10} {roots_m:>10}")
    print(f"{'Total concepts':<25} {len(physics_hds):>10} {len(math_hds):>10}")

    # Save comparison
    comparison = {
        "physics": {
            "concepts": len(physics["concepts"]),
            "relations": len(physics["relations"]),
            "cds": physics_cds,
            "hds": {
                "max_depth": max_depth_p,
                "mean_depth": round(mean_depth_p, 4),
                "root_count": roots_p
            }
        },
        "math": {
            "concepts": len(math_nodes),
            "relations": len(math_links),
            "cds": math_cds,
            "hds": {
                "max_depth": max_depth_m,
                "mean_depth": round(mean_depth_m, 4),
                "root_count": roots_m
            }
        }
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] Comparison saved: {OUTPUT_JSON}")

    # Export physics data.js nodes for visualization
    physics_cs_json = PROJECT_DIR / "outputs" / "physics_cognitivespace.json"
    with open(physics_cs_json, "w", encoding="utf-8") as f:
        json.dump(cs_data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Physics CS data: {physics_cs_json}")

    print("\n=== Key Findings ===")
    print(f"Physics CDS peak: {max(physics_cds.values(), key=lambda x: x['cds'])}")
    peak_lv = max(physics_cds, key=lambda k: physics_cds[k]["cds"])
    print(f"Physics CDS peak at: {peak_lv} (CDS={physics_cds[peak_lv]['cds']})")
    math_peak_lv = max(math_cds, key=lambda k: math_cds[k]["cds"])
    print(f"Math CDS peak at:    {math_peak_lv} (CDS={math_cds[math_peak_lv]['cds']})")

    if peak_lv != math_peak_lv:
        print(f"\n>>> CROSS-DISCIPLINARY FINDING: Physics peaks at {peak_lv}, Math peaks at {math_peak_lv}")
    else:
        print(f"\n   Both peak at {peak_lv} -- same pattern")


if __name__ == "__main__":
    main()
