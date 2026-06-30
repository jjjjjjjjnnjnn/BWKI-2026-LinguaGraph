#!/usr/bin/env python3
"""
CognitiveSpace — Quality Report Generator

Generates a structured quality report with:
  - Complete graph metrics (nodes, edges, degree, components)
  - Cross-language completeness
  - Level distribution
  - Historical diff against previous report (drift detection)

Usage:
    python scripts/quality_report.py [--history-dir data/quality_history]
                                     [--check-quality-gates]
                                     [--verbose]

Output: quality_report.json (latest) + history archive
"""

import hashlib
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def compute_graph_metrics(vis: dict) -> dict:
    """Compute all graph-theoretic metrics from visualization data."""
    nodes = vis["nodes"]
    links = vis["links"]

    node_ids = [n["id"] for n in nodes]
    unique_ids = set(node_ids)
    dup_count = len(node_ids) - len(unique_ids)
    dup_ids = sorted(set(i for i in node_ids if node_ids.count(i) > 1)) if dup_count else []

    # Degree distribution
    degree: Counter[str] = Counter()
    for n in nodes:
        degree[n["id"]] = 0
    for link in links:
        src = link.get("source", link.get("source_group", ""))
        tgt = link.get("target", link.get("target_group", ""))
        if isinstance(src, dict):
            src = src.get("id", "")
        if isinstance(tgt, dict):
            tgt = tgt.get("id", "")
        if src in degree:
            degree[src] += 1
        if tgt in degree:
            degree[tgt] += 1

    degrees = list(degree.values()) if degree else [0]
    avg_degree = sum(degrees) / len(degrees) if degrees else 0.0
    sorted_deg = sorted(degrees)

    # Graph density: 2E / (N(N-1))
    n_nodes = len(nodes)
    density = (2 * len(links)) / (n_nodes * (n_nodes - 1)) if n_nodes > 1 else 0.0

    # Extended percentiles
    deg_p95_idx = min(int(len(sorted_deg) * 0.95), len(sorted_deg) - 1)
    deg_p99_idx = min(int(len(sorted_deg) * 0.99), len(sorted_deg) - 1)

    # Degree 0 count
    deg_zero = sum(1 for d in degrees if d == 0)

    # Connected components (undirected BFS)
    adj: dict[str, set[str]] = {n["id"]: set() for n in nodes}
    for link in links:
        src = link.get("source", link.get("source_group", ""))
        tgt = link.get("target", link.get("target_group", ""))
        if isinstance(src, dict):
            src = src.get("id", "")
        if isinstance(tgt, dict):
            tgt = tgt.get("id", "")
        if src in adj and tgt in adj:
            adj[src].add(tgt)
            adj[tgt].add(src)

    visited: set[str] = set()
    components: list[set[str]] = []
    for nid in adj:
        if nid not in visited:
            stack = [nid]
            comp: set[str] = set()
            while stack:
                cur = stack.pop()
                if cur not in visited:
                    visited.add(cur)
                    comp.add(cur)
                    stack.extend(adj[cur] - visited)
            components.append(comp)

    component_sizes = sorted((len(c) for c in components), reverse=True)

    return {
        "nodes": len(nodes),
        "unique_ids": len(unique_ids),
        "duplicate_ids": dup_count,
        "duplicate_id_list": dup_ids,
        "links": len(links),
        "avg_degree": round(avg_degree, 4),
        "degree_min": min(degrees),
        "degree_max": max(degrees),
        "degree_median": sorted_deg[len(sorted_deg) // 2] if sorted_deg else 0,
        "connected_components": len(components),
        "largest_component_size": component_sizes[0] if component_sizes else 0,
        "isolated_nodes": sum(1 for s in component_sizes if s == 1),
        "component_size_distribution": component_sizes[:10],
        "graph_density": round(density, 6),
        "degree_zeros": deg_zero,
        "degree_p95": sorted_deg[deg_p95_idx] if sorted_deg else 0,
        "degree_p99": sorted_deg[deg_p99_idx] if sorted_deg else 0,
    }


def compute_alignment_metrics(aligned: dict) -> dict:
    """Compute metrics from aligned data."""
    groups = aligned.get("aligned_groups", [])
    unmatched = aligned.get("unmatched_concepts", [])
    relations = aligned.get("relations", [])

    level_order_dist: Counter[int] = Counter()
    level_name_dist: Counter[str] = Counter()
    domain_dist: Counter[str] = Counter()
    trilingual = 0
    bilingual = 0
    monolingual = 0

    for g in groups:
        lo = g.get("level_order", 4)
        level_order_dist[lo] += 1
        level_name_dist[g.get("level", "?")] += 1
        domain_dist[g.get("domain", "?")] += 1

        labels = g.get("labels", {})
        has_zh = bool(labels.get("zh"))
        has_en = bool(labels.get("en"))
        has_de = bool(labels.get("de"))
        lang_count = sum([has_zh, has_en, has_de])
        if lang_count == 3:
            trilingual += 1
        elif lang_count == 2:
            bilingual += 1
        else:
            monolingual += 1

    unmatched_lang: Counter[str] = Counter()
    for c in unmatched:
        unmatched_lang[c.get("language", "?")] += 1

    unmatched_level: Counter[str] = Counter()
    for c in unmatched:
        unmatched_level[c.get("level", "?")] += 1

    return {
        "aligned_groups": len(groups),
        "unmatched_concepts": len(unmatched),
        "total_relations": len(relations),
        "level_order_distribution": {str(k): v for k, v in sorted(level_order_dist.items())},
        "level_name_distribution": dict(level_name_dist),
        "domain_distribution": dict(domain_dist),
        "trilingual_groups": trilingual,
        "bilingual_groups": bilingual,
        "monolingual_groups": monolingual,
        "unmatched_by_language": dict(unmatched_lang),
        "unmatched_by_level": dict(unmatched_level),
    }


def compute_file_checksums(project_root: Path) -> dict:
    """MD5 checksums of key files for integrity tracking."""
    files = {
        "data.js": project_root / "cognitive-space" / "web" / "data.js",
        "visualization_data.json": project_root / "data" / "math_extractions" / "merged" / "visualization_data.json",
        "aligned_data.json": project_root / "data" / "math_extractions" / "merged" / "aligned_data.json",
    }
    result = {}
    for name, path in files.items():
        if path.exists():
            result[name] = hashlib.md5(path.read_bytes()).hexdigest()
        else:
            result[name] = None
    return result


def compute_diff(current: dict, previous: dict | None):
    """Compare current report against previous, flag meaningful changes."""
    if previous is None:
        return None

    diffs = []
    sensitive_keys = [
        "nodes", "links", "aligned_groups", "unmatched_concepts",
        "unique_ids", "duplicate_ids", "trilingual_groups",
        "largest_component_size", "connected_components",
        "isolated_nodes", "total_relations", "graph_density",
        "degree_zeros", "degree_p95",
    ]

    THRESHOLD_PCT = 0.10
    THRESHOLD_ABS = 3

    for key in sensitive_keys:
        old_val = previous.get(key, 0)
        new_val = current.get(key, 0)
        delta = new_val - old_val
        if abs(delta) > max(old_val * THRESHOLD_PCT, THRESHOLD_ABS):
            diffs.append({
                "metric": key,
                "old": old_val,
                "new": new_val,
                "delta": delta,
                "delta_pct": round(delta / old_val * 100, 1) if old_val else None,
                "severity": "WARN",
            })
        elif delta != 0:
            diffs.append({
                "metric": key,
                "old": old_val,
                "new": new_val,
                "delta": delta,
                "delta_pct": round(delta / old_val * 100, 1) if old_val else None,
                "severity": "INFO",
            })

    # Level distribution diff
    old_levels = previous.get("level_order_distribution", {})
    new_levels = current.get("level_order_distribution", {})
    for lv in set(list(old_levels.keys()) + list(new_levels.keys())):
        old_cnt = old_levels.get(lv, 0)
        new_cnt = new_levels.get(lv, 0)
        delta = new_cnt - old_cnt
        if abs(delta) > max(old_cnt * 0.15, 5):
            diffs.append({
                "metric": f"level[{lv}]",
                "old": old_cnt,
                "new": new_cnt,
                "delta": delta,
                "delta_pct": round(delta / old_cnt * 100, 1) if old_cnt else None,
                "severity": "WARN",
            })

    return diffs if diffs else None


def main():
    import argparse
    parser = argparse.ArgumentParser(description="CognitiveSpace quality report")
    parser.add_argument("--history-dir", type=str, default="data/quality_history",
                        help="Directory for historical quality reports")
    parser.add_argument("--check-quality-gates", action="store_true",
                        help="Also run validate_pipeline.py gates (slower)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    aligned_path = project_root / "data" / "math_extractions" / "merged" / "aligned_data.json"
    vis_path = project_root / "data" / "math_extractions" / "merged" / "visualization_data.json"
    history_dir = (project_root / args.history_dir).resolve()
    history_dir.mkdir(parents=True, exist_ok=True)

    if not aligned_path.exists() or not vis_path.exists():
        print("ERROR: Run pipeline first -- data files not found")
        print(f"  aligned: {aligned_path}")
        print(f"  vis:     {vis_path}")
        sys.exit(1)

    aligned = load_json(aligned_path)
    vis = load_json(vis_path)

    print("=" * 50)
    print("  CognitiveSpace - Quality Report")
    print("=" * 50)

    print("\n  Computing graph metrics...")
    graph_metrics = compute_graph_metrics(vis)

    print("  Computing alignment metrics...")
    alignment_metrics = compute_alignment_metrics(aligned)

    print("  Computing file checksums...")
    checksums = compute_file_checksums(project_root)

    # Compile report
    timestamp = datetime.now().isoformat()
    report = {
        "report_version": "1.0",
        "generated_at": timestamp,
        "pipeline_version": vis.get("version", "unknown"),
        "graph_metrics": graph_metrics,
        "alignment_metrics": alignment_metrics,
        "file_checksums": checksums,
    }

    # Historical diff
    previous_report_path = history_dir / "quality_report_latest.json"
    previous_report = None
    if previous_report_path.exists():
        try:
            previous_report = json.loads(previous_report_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, Exception):
            pass

    diff = None
    if previous_report:
        combined_current = {**graph_metrics, **alignment_metrics}
        combined_previous = {**previous_report.get("graph_metrics", {}),
                             **previous_report.get("alignment_metrics", {})}
        diff = compute_diff(combined_current, combined_previous)

    if diff:
        warnings = [d for d in diff if d["severity"] == "WARN"]
        infos = [d for d in diff if d["severity"] == "INFO"]
        if warnings:
            print(f"\n  [WARN] {len(warnings)} change(s) above threshold:")
            for d in warnings:
                print(f"     {d['metric']}: {d['old']} -> {d['new']} ({d.get('delta_pct', '?')}%)")
        if infos:
            print(f"\n  [INFO] {len(infos)} minor change(s):")
            for d in infos:
                print(f"     {d['metric']}: {d['old']} -> {d['new']}")
    else:
        print("\n  [OK] No significant drift from previous report")

    report["diff"] = diff

    # Optional: run quality gates
    if args.check_quality_gates:
        print("\n  Running quality gates...")
        import subprocess
        gate_path = project_root / "scripts" / "math_graph_pipeline" / "validate_pipeline.py"
        if gate_path.exists():
            result = subprocess.run(
                [sys.executable, str(gate_path), "--check-levels-only"],
                cwd=str(project_root), capture_output=True, text=True
            )
            report["quality_gates"] = {
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
            if result.returncode == 0:
                print("  [PASS] Quality gates")
            else:
                print("  [FAIL] Quality gates - see output above")
        else:
            print("  [SKIP] validate_pipeline.py not found")

    # Write report
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = history_dir / f"quality_report_{ts}.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Report written: {report_path.relative_to(project_root)}")

    # Update latest
    latest_path = history_dir / "quality_report_latest.json"
    latest_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    # Summary
    print(f"\n{'=' * 50}")
    print(f"  SUMMARY")
    print(f"{'=' * 50}")
    gm = graph_metrics
    am = alignment_metrics
    print(f"  Nodes:           {gm['nodes']} (unique: {gm['unique_ids']})")
    print(f"  Links:           {gm['links']}")
    print(f"  Graph density:   {gm['graph_density']}")
    print(f"  Avg degree:      {gm['avg_degree']}  (median: {gm['degree_median']}, P95: {gm['degree_p95']}, max: {gm['degree_max']})")
    print(f"  Degree=0:        {gm['degree_zeros']} ({gm['degree_zeros']/max(gm['nodes'],1)*100:.1f}%)")
    print(f"  Components:      {gm['connected_components']} (largest: {gm['largest_component_size']})")
    print(f"  Aligned groups:  {am['aligned_groups']} (trilingual: {am['trilingual_groups']})")
    print(f"  Unmatched:       {am['unmatched_concepts']}")
    print(f"  Levels:          {am['level_name_distribution']}")
    print(f"  data.js MD5:     {checksums.get('data.js', 'N/A')}")
    if diff:
        warn_count = len([d for d in diff if d["severity"] == "WARN"])
        print(f"  Drift:           {warn_count} warning(s)")
    else:
        print(f"  Drift:           none")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
