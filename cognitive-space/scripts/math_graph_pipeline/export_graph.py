#!/usr/bin/env python3
"""
CognitiveSpace — Export Graphs

Takes aligned data from align_languages.py and produces:
1. config/expert_graphs/{domain}.json — loadable by src/graph.py::load_expert_graph()
2. config/expert_graphs/math_full.json — combined graph (all domains merged)
3. data/math_extractions/merged/visualization_data.json — for 3D force-graph

Usage:
    python scripts/math_graph_pipeline/export_graph.py [--input-dir data/math_extractions]
"""

import json
import sys
from pathlib import Path
from collections import defaultdict


# ── Domain classification ────────────────────────────────────────────

def classify_domain(group: dict) -> str:
    """Determine domain from alignment group."""
    domain = group.get("domain", "general")
    return domain


def export_expert_graphs(aligned_groups: list[dict], relations: list[dict],
                         output_dir: Path) -> dict[str, list[dict]]:
    """
    Export per-domain expert graphs — ONLY concepts with actual extraction data.

    Also writes a suggested_expansions.json with placeholder concepts
    that have no extraction data yet, for future expansion planning.

    Returns:
        dict mapping domain → list of group IDs that have data (for relation filtering)
    """
    domain_map = {
        "calculus": "微积分专家知识图谱",
        "linear_algebra": "线性代数专家知识图谱",
        "geometry": "几何专家知识图谱",
        "general": "通用数学概念专家知识图谱",
    }

    # Separate groups with data vs placeholders
    groups_with_data: dict[str, list[dict]] = defaultdict(list)
    placeholders: dict[str, list[dict]] = defaultdict(list)
    for g in aligned_groups:
        domain = classify_domain(g)
        if len(g.get("cross_references", [])) > 0:
            groups_with_data[domain].append(g)
        else:
            placeholders[domain].append(g)

    domain_data_ids: dict[str, set[str]] = {}

    for domain, groups_in_domain in groups_with_data.items():
        concepts_out = []
        group_ids = set()
        for g in groups_in_domain:
            primary_name = (
                g["labels"].get("zh") or
                g["labels"].get("en") or
                g["labels"].get("de") or
                g["display_name"]
            )
            concepts_out.append({
                "name": g["id"],
                "display_name": primary_name,
                "category": "concept",
                "labels": g["labels"],
                "source_references": g.get("cross_references", []),
            })
            group_ids.add(g["id"])

        domain_data_ids[domain] = group_ids

        relations_out = []
        for r in relations:
            src_group = r.get("source_group")
            tgt_group = r.get("target_group")
            if src_group in group_ids and tgt_group in group_ids:
                relations_out.append({
                    "source": src_group,
                    "target": tgt_group,
                    "type": r.get("type", "related_to"),
                    "importance": r.get("importance", 0.5),
                    "evidence": r.get("evidence", ""),
                })

        expert_graph = {
            "version": "2.0",
            "domain": domain,
            "description": domain_map.get(domain, f"{domain} 专家知识图谱"),
            "languages": ["zh", "de", "en"],
            "created": __import__('datetime').datetime.now().isoformat(),
            "pipeline": "scripts/math_graph_pipeline/export_graph.py",
            "concepts": concepts_out,
            "relations": relations_out,
            "metadata": {
                "total_concepts": len(concepts_out),
                "total_relations": len(relations_out),
                "data_sources": sum(len(g.get("cross_references", [])) for g in groups_in_domain),
            },
        }

        out_path = output_dir / f"{domain}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(expert_graph, f, ensure_ascii=False, indent=2)
        print(f"[OK] {domain}: {len(concepts_out)} concepts, {len(relations_out)} relations -> {out_path}")

    # Write suggested expansions (placeholder concepts without data)
    all_placeholders = []
    for domain, groups in placeholders.items():
        for g in groups:
            primary_name = (
                g["labels"].get("zh") or
                g["labels"].get("en") or
                g["labels"].get("de") or
                g["display_name"]
            )
            all_placeholders.append({
                "id": g["id"],
                "display_name": primary_name,
                "domain": domain,
                "labels": g["labels"],
            })

    if all_placeholders:
        expansions_path = output_dir / "suggested_expansions.json"
        with open(expansions_path, "w", encoding="utf-8") as f:
            json.dump({
                "version": "2.0",
                "description": "Concepts without extraction data — candidates for future textbook processing",
                "total": len(all_placeholders),
                "concepts": all_placeholders,
            }, f, ensure_ascii=False, indent=2)
        print(f"[OK] Suggested expansions: {len(all_placeholders)} placeholder concepts -> {expansions_path}")

    return domain_data_ids


def export_visualization_data(aligned_groups: list[dict], relations: list[dict],
                              output_path: Path, aligned_data: dict | None = None):
    """
    Export data in the format expected by 3d-force-graph (demo.html).

    The visualization needs:
    - nodes: [{id, name, group, importance, labels, source, level, level_order}]
    - links: [{source, target, type, importance, evidence}]

    Plus a cross_language mapping for the color-coding.
    """
    # Simplified level inference from textbook references
    LEVEL_KEYWORDS = [
        ("elementary", ["小学"]),
        ("middle", ["初中", "七年", "八年", "九年"]),
        ("high", ["高中", "选修", "必修"]),
    ]

    def infer_level_from_refs(refs: list) -> tuple[str, int]:
        texts = []
        for r in refs:
            if isinstance(r, dict):
                texts.append(r.get("textbook", ""))
            elif isinstance(r, str):
                texts.append(r)
        combined = " ".join(texts)
        for level, keywords in LEVEL_KEYWORDS:
            for kw in keywords:
                if kw in combined:
                    order = {"elementary": 1, "middle": 2, "high": 3, "college": 4}.get(level, 4)
                    return level, order
        return "college", 4  # default

    nodes = []
    links = []
    node_ids: set[str] = set()

    # Build nodes — only include groups with actual source data
    for g in aligned_groups:
        has_data = len(g.get("cross_references", [])) > 0
        if not has_data:
            continue  # Skip placeholder groups with no textbook data yet

        primary_name = (
            g["labels"].get("zh") or
            g["labels"].get("en") or
            g["labels"].get("de") or
            g["display_name"]
        )
        domain = classify_domain(g)
        level, level_order = infer_level_from_refs(g.get("cross_references", []))

        node = {
            "id": g["id"],
            "name": primary_name,
            "labels": g["labels"],
            "group": domain,
            "level": level,
            "level_order": level_order,
            "importance": 8,
            "source_count": len(g.get("cross_references", [])),
            "cross_references": g.get("cross_references", [])[:5],
        }
        nodes.append(node)
        node_ids.add(g["id"])

    # Add one node for each unmatched concept from aligned_data
    for c in aligned_data.get("unmatched_concepts", []):
        cid = f"math_unmatched_{c['canonical_name']}"
        if cid not in node_ids:
            # Infer level from the concept's source references
            level = c.get("level", "college")
            level_order = c.get("level_order", 4)
            node = {
                "id": cid,
                "name": c["canonical_name"],
                "labels": {c["language"]: c["canonical_name"]},
                "group": "general",
                "level": level,
                "level_order": level_order,
                "importance": 5,
                "source_count": 1,
                "cross_references": c.get("source", {}).get("cross_references", [])[:3],
            }
            nodes.append(node)
            node_ids.add(cid)

    # Build links
    for r in relations:
        src_group = r.get("source_group")
        tgt_group = r.get("target_group")
        if src_group and tgt_group:
            link = {
                "source": src_group,
                "target": tgt_group,
                "type": r.get("type", "related_to"),
                "importance": r.get("importance", 0.5),
                "known": True,  # all expert relations are "known"
                "evidence": r.get("evidence", ""),
            }
            links.append(link)

    vis_data = {
        "version": "2.0",
        "generated_at": __import__('datetime').datetime.now().isoformat(),
        "nodes": nodes,
        "links": links,
        "metadata": {
            "total_nodes": len(nodes),
            "total_links": len(links),
            "domains": list(set(n["group"] for n in nodes)),
            "languages": ["zh", "en", "de"],
        },
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(vis_data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Visualization data: {len(nodes)} nodes, {len(links)} links -> {output_path}")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Export expert graphs and visualization data")
    parser.add_argument("--input-dir", type=str, default="data/math_extractions")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent.parent
    input_dir = (project_root / args.input_dir).resolve()
    aligned_file = input_dir / "merged" / "aligned_data.json"

    if not aligned_file.exists():
        print(f"ERROR: Run align_languages.py first — {aligned_file} not found")
        sys.exit(1)

    with open(aligned_file, encoding="utf-8") as f:
        aligned_data = json.load(f)

    aligned_groups = aligned_data.get("aligned_groups", [])
    relations = aligned_data.get("relations", [])

    print(f"Loaded {len(aligned_groups)} aligned groups, {len(relations)} relations\n")

    # 1. Export expert graphs to config/expert_graphs/
    expert_output_dir = project_root / "config" / "expert_graphs"
    expert_output_dir.mkdir(parents=True, exist_ok=True)
    print("Exporting expert graphs...")
    domain_data_ids = export_expert_graphs(aligned_groups, relations, expert_output_dir)

    # 1b. Export combined math_full graph (all domains merged)
    all_concepts = []
    all_relations = []
    for domain_file in sorted(expert_output_dir.glob("*.json")):
        if domain_file.stem in ("social_issues", "suggested_expansions"):
            continue
        try:
            domain_data = json.loads(domain_file.read_text(encoding="utf-8"))
            all_concepts.extend(domain_data.get("concepts", []))
            all_relations.extend(domain_data.get("relations", []))
        except (json.JSONDecodeError, KeyError):
            pass

    # Deduplicate by concept name
    seen_concepts = set()
    deduped_concepts = []
    for c in all_concepts:
        if c["name"] not in seen_concepts:
            seen_concepts.add(c["name"])
            deduped_concepts.append(c)

    seen_rels = set()
    deduped_rels = []
    for r in all_relations:
        key = (r["source"], r["target"], r["type"])
        if key not in seen_rels:
            seen_rels.add(key)
            deduped_rels.append(r)

    math_full = {
        "version": "2.0",
        "domain": "math_full",
        "description": "全流程数学知识图谱 — 从小学到高数的完整概念网络",
        "languages": ["zh", "de", "en"],
        "created": __import__('datetime').datetime.now().isoformat(),
        "pipeline": "scripts/math_graph_pipeline/export_graph.py",
        "concepts": deduped_concepts,
        "relations": deduped_rels,
        "metadata": {
            "total_concepts": len(deduped_concepts),
            "total_relations": len(deduped_rels),
        },
    }
    math_full_path = expert_output_dir / "math_full.json"
    with open(math_full_path, "w", encoding="utf-8") as f:
        json.dump(math_full, f, ensure_ascii=False, indent=2)
    print(f"[OK] math_full: {len(deduped_concepts)} concepts, {len(deduped_rels)} relations -> {math_full_path}")

    # 2. Export visualization data
    vis_output_path = input_dir / "merged" / "visualization_data.json"
    print("\nExporting visualization data...")
    export_visualization_data(aligned_groups, relations, vis_output_path, aligned_data)

    print("\nExport complete.")
    print(f"\nFiles produced:")
    for fpath in sorted(expert_output_dir.glob("*.json")):
        size = fpath.stat().st_size
        print(f"  {fpath.relative_to(project_root)} ({size:,} bytes)")
    print(f"  {vis_output_path.relative_to(project_root)} ({vis_output_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
