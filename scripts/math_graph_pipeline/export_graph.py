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
def infer_implicit_relations(aligned_groups: list[dict],
                              existing_relations: list[dict],
                              aligned_data: dict | None = None) -> list[dict]:
    """
    Infer implicit prerequisite/related_to relations from co-occurrence in
    the same textbook. This connects isolated nodes by looking at
    which concepts share source references, including unmatched concepts.

    Returns additional relations to merge into the existing list.
    """
    # Build a map: textbook → list of entries (aligned groups + unmatched)
    textbook_entries: dict[str, list[dict]] = {}
    group_by_id: dict[str, dict] = {}

    for g in aligned_groups:
        gid = g["id"]
        group_by_id[gid] = g
        for ref in g.get("cross_references", []):
            if isinstance(ref, dict):
                tname = ref.get("textbook", "")
                if tname:
                    textbook_entries.setdefault(tname, []).append({
                        "id": gid, "type": "aligned", "chapter": ref.get("chapter", ""),
                        "level": g.get("domain", g.get("level", ""))
                    })

    # Also index unmatched concepts
    for c in (aligned_data or {}).get("unmatched_concepts", []):
        cid = f"math_unmatched_{c['canonical_name']}"
        for ref in c.get("source", {}).get("cross_references", []):
            if isinstance(ref, dict):
                tname = ref.get("textbook", "")
                if tname:
                    # Infer level from concept metadata or from textbook name
                    cl = c.get("level", "")
                    textbook_entries.setdefault(tname, []).append({
                        "id": cid, "type": "unmatched", "chapter": ref.get("chapter", ""),
                        "level": cl
                    })

    # Build existing relation set for dedup
    existing_pairs: set[tuple[str, str]] = set()
    for r in existing_relations:
        sg = r.get("source_group") or r.get("source", "")
        tg = r.get("target_group") or r.get("target", "")
        if sg and tg:
            existing_pairs.add((sg, tg))

    # Per-node cap to prevent excessive connections
    MAX_INFERRED_PER_NODE = 15
    inferred_count: dict[str, int] = {}

    new_relations: list[dict] = []
    seen: set[tuple[str, str]] = set()

    for textbook, entries in textbook_entries.items():
        if len(entries) < 2:
            continue

        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                a = entries[i]
                b = entries[j]
                a_id, b_id = a["id"], b["id"]
                if a_id == b_id:
                    continue

                pair = (a_id, b_id)
                reverse = (b_id, a_id)

                if pair in existing_pairs or reverse in existing_pairs:
                    continue
                if pair in seen or reverse in seen:
                    continue

                # Same-level filter: only connect concepts from the same education level
                a_level = a.get("level", "")
                b_level = b.get("level", "")
                if a_level and b_level and a_level != b_level:
                    continue

                seen.add(pair)

                # Determine if same chapter (high cohesion) or cross-chapter (moderate)
                same_chapter = a.get("chapter") == b.get("chapter") and a.get("chapter", "")
                
                # Try to determine direction from chapter ordering:
                # Earlier chapter → later chapter = prerequisite
                # Extract numeric chapter for comparison
                import re as _cr
                def _ch_num(ch):
                    m = _cr.search(r'(\d+)', ch or '')
                    return int(m.group(1)) if m else 0
                
                a_ch = _ch_num(a.get("chapter", ""))
                b_ch = _ch_num(b.get("chapter", ""))
                
                if a_ch > 0 and b_ch > 0 and a_ch != b_ch:
                    # Directional: lower chapter → higher chapter = prerequisite
                    if a_ch < b_ch:
                        src_id, tgt_id = a_id, b_id
                        rel_type = "prerequisite"
                    else:
                        src_id, tgt_id = b_id, a_id
                        rel_type = "prerequisite"
                    importance = 0.35  # Cross-chapter prerequisite
                elif same_chapter:
                    # Same chapter: undirected strong related_to
                    src_id, tgt_id = a_id, b_id
                    rel_type = "related_to"
                    importance = 0.6  # High cohesion: same chapter
                else:
                    # Same textbook but can't determine order
                    src_id, tgt_id = a_id, b_id
                    rel_type = "related"
                    importance = 0.2  # Weak: same textbook only

                # Per-node cap check
                if inferred_count.get(src_id, 0) >= MAX_INFERRED_PER_NODE:
                    continue
                if inferred_count.get(tgt_id, 0) >= MAX_INFERRED_PER_NODE:
                    continue

                new_relations.append({
                    "source": src_id,
                    "target": tgt_id,
                    "source_group": src_id,
                    "target_group": tgt_id,
                    "type": rel_type,
                    "importance": importance,
                    "evidence": f"Co-occur in {textbook}",
                    "known": True,
                    "inferred": True,
                })
                inferred_count[src_id] = inferred_count.get(src_id, 0) + 1
                inferred_count[tgt_id] = inferred_count.get(tgt_id, 0) + 1

    return new_relations


def export_visualization_data(aligned_groups: list[dict], relations: list[dict],
                              output_path: Path, aligned_data: dict | None = None):
    """
    Export data in the format expected by 3d-force-graph (demo.html).

    The visualization needs:
    - nodes: [{id, name, group, importance, labels, source, level, level_order}]
    - links: [{source, target, type, importance, evidence}]
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

    # --- Step 0: Infer implicit relations to connect isolated nodes ---
    implicit = infer_implicit_relations(aligned_groups, relations, aligned_data)
    all_relations = relations + implicit

    # Build lookup for relation count per node
    rel_counts: dict[str, int] = {}
    for r in all_relations:
        sg = r.get("source_group") or r.get("source", "")
        tg = r.get("target_group") or r.get("target", "")
        if sg: rel_counts[sg] = rel_counts.get(sg, 0) + 1
        if tg: rel_counts[tg] = rel_counts.get(tg, 0) + 1

    # --- Step 1: Build nodes from aligned groups with data ---
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

    # --- Step 1.5: Backfill EN/DE translations for unmatched ZH-only concepts ---
    # Primary lookup: aligned group labels
    label_lookup: dict[str, dict] = {}
    def _norm(n):
        import re
        return re.sub(r'[\s\-_()（）\[\]]+', '', n.lower()).strip()

    for g in aligned_groups:
        for lang, label in g["labels"].items():
            if label:
                label_lookup[_norm(label)] = g["labels"]
        dn = g.get("display_name", "")
        if dn:
            label_lookup[_norm(dn)] = g["labels"]

    # Fallback: known translations for elementary/middle school concepts not in CROSS_LANG_MAP
    KNOWN_ZH_EN: dict[str, dict[str, str]] = {
        "自然数": {"en": "Natural Number", "de": "Natürliche Zahl"},
        "整数": {"en": "Integer", "de": "Ganze Zahl"},
        "加法": {"en": "Addition", "de": "Addition"},
        "减法": {"en": "Subtraction", "de": "Subtraktion"},
        "乘法": {"en": "Multiplication", "de": "Multiplikation"},
        "除法": {"en": "Division", "de": "Division"},
        "分数": {"en": "Fraction", "de": "Bruch"},
        "小数": {"en": "Decimal", "de": "Dezimalzahl"},
        "百分数": {"en": "Percentage", "de": "Prozent"},
        "面积": {"en": "Area", "de": "Fläche"},
        "体积": {"en": "Volume", "de": "Volumen"},
        "棱长": {"en": "Edge Length", "de": "Kantenlänge"},
        "周长": {"en": "Perimeter", "de": "Umfang"},
        "运算律": {"en": "Operation Laws", "de": "Rechengesetze"},
        "四则运算": {"en": "Arithmetic", "de": "Grundrechenarten"},
        "交换律": {"en": "Commutative Law", "de": "Kommutativgesetz"},
        "结合律": {"en": "Associative Law", "de": "Assoziativgesetz"},
        "分配律": {"en": "Distributive Law", "de": "Distributivgesetz"},
        "估算": {"en": "Estimation", "de": "Schätzung"},
        "近似数": {"en": "Approximate Number", "de": "Näherungswert"},
        "位值": {"en": "Place Value", "de": "Stellenwert"},
        "因数": {"en": "Factor", "de": "Teiler"},
        "倍数": {"en": "Multiple", "de": "Vielfaches"},
        "素数": {"en": "Prime Number", "de": "Primzahl"},
        "公因数": {"en": "Common Factor", "de": "Gemeinsamer Teiler"},
        "公倍数": {"en": "Common Multiple", "de": "Gemeinsames Vielfaches"},
        "奇数": {"en": "Odd Number", "de": "Ungerade Zahl"},
        "偶数": {"en": "Even Number", "de": "Gerade Zahl"},
        "质数": {"en": "Prime", "de": "Primzahl"},
        "合数": {"en": "Composite Number", "de": "Zusammengesetzte Zahl"},
        "代数": {"en": "Algebra", "de": "Algebra"},
        "方程": {"en": "Equation", "de": "Gleichung"},
        "不等式": {"en": "Inequality", "de": "Ungleichung"},
        "有理数": {"en": "Rational Number", "de": "Rationale Zahl"},
        "无理数": {"en": "Irrational Number", "de": "Irrationale Zahl"},
        "实数": {"en": "Real Number", "de": "Reelle Zahl"},
        "复数": {"en": "Complex Number", "de": "Komplexe Zahl"},
        "坐标": {"en": "Coordinate", "de": "Koordinate"},
        "变量": {"en": "Variable", "de": "Variable"},
        "单项式": {"en": "Monomial", "de": "Monom"},
        "多项式": {"en": "Polynomial", "de": "Polynom"},
        "恒等式": {"en": "Identity", "de": "Identität"},
        "比例": {"en": "Proportion", "de": "Proportion"},
        "平均值": {"en": "Average", "de": "Durchschnitt"},
        "统计": {"en": "Statistics", "de": "Statistik"},
        "概率": {"en": "Probability", "de": "Wahrscheinlichkeit"},
        "命题": {"en": "Proposition", "de": "Aussage"},
        "对数": {"en": "Logarithm", "de": "Logarithmus"},
        "指数": {"en": "Exponent", "de": "Exponent"},
        "正弦": {"en": "Sine", "de": "Sinus"},
        "余弦": {"en": "Cosine", "de": "Kosinus"},
        "正切": {"en": "Tangent", "de": "Tangens"},
        "弧度": {"en": "Radian", "de": "Bogenmaß"},
    }

    backfilled = 0
    for c in aligned_data.get("unmatched_concepts", []):
        if c.get("language") != "zh":
            continue
        name = c.get("canonical_name", "")
        if not name:
            continue

        # Try 1: aligned group labels by normalized name
        norm = _norm(name)
        if norm in label_lookup:
            fl = label_lookup[norm]
            if fl.get("en") and fl.get("de"):
                c["_translations"] = {"en": fl["en"], "de": fl["de"]}
                backfilled += 1
                continue

        # Try 2: alias match
        for alias in c.get("aliases", []):
            na = _norm(alias)
            if na in label_lookup:
                fl = label_lookup[na]
                if fl.get("en") and fl.get("de"):
                    c["_translations"] = {"en": fl["en"], "de": fl["de"]}
                    backfilled += 1
                    break
        if "_translations" in c:
            continue

        # Try 3: KNOWN_ZH_EN lookup
        if name in KNOWN_ZH_EN:
            trans = KNOWN_ZH_EN[name]
            c["_translations"] = {"en": trans["en"], "de": trans["de"]}
            backfilled += 1
            continue

        # Try 4: fuzzy match (if normalized name contains a known key)
        for zh_key, trans in KNOWN_ZH_EN.items():
            if zh_key in name or name in zh_key:
                c["_translations"] = {"en": trans["en"], "de": trans["de"]}
                backfilled += 1
                break

    if backfilled > 0:
        print(f"  [A2] Backfilled EN/DE translations for {backfilled} ZH-only concepts")

    # Add one node for each unmatched concept from aligned_data
    for c in aligned_data.get("unmatched_concepts", []):
        cid = f"math_unmatched_{c['canonical_name']}"
        if cid not in node_ids:
            # Infer level from the concept's source references
            level = c.get("level", "college")
            level_order = c.get("level_order", 4)
            # Use backfilled translations if available
            translations = c.get("_translations", {})
            labels = {c["language"]: c["canonical_name"]}
            if translations.get("en"):
                labels["en"] = translations["en"]
            if translations.get("de"):
                labels["de"] = translations["de"]
            node = {
                "id": cid,
                "name": c["canonical_name"],
                "labels": labels,
                "group": "general",
                "level": level,
                "level_order": level_order,
                "importance": 5,
                "source_count": 1,
                "cross_references": c.get("source", {}).get("cross_references", [])[:3],
            }
            nodes.append(node)
            node_ids.add(cid)

    # Build links (existing + inferred)
    for r in all_relations:
        src_group = r.get("source_group")
        tgt_group = r.get("target_group")
        if src_group and tgt_group:
            link = {
                "source": src_group,
                "target": tgt_group,
                "type": r.get("type", "related_to"),
                "importance": r.get("importance", 0.5),
                "known": r.get("known", True),
                "inferred": r.get("inferred", False),
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
