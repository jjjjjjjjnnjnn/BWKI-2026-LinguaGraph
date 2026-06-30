#!/usr/bin/env python3
"""
LinguaGraph — Manifest & Provenance Generator

Produces manifest.json — the single source of truth for all project-wide
numbers (nodes, edges, groups, checksums, schema versions, provenance).

manifest.json is consumed by:
  - release.py (bundled into release)
  - Portal (for displaying current stats)
  - Paper (for ensuring numbers match across sources)

Usage:
    python scripts/generate_manifest.py [--output-dir .]
"""

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_VERSION = "1.0.0"       # manifest.json schema
DATA_SCHEMA_VERSION = "2.1.0"   # data output schema


def git_commit() -> str | None:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT), timeout=5,
        )
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def git_branch() -> str | None:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT), timeout=5,
        )
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def git_commit_date() -> str | None:
    try:
        r = subprocess.run(
            ["git", "log", "-1", "--format=%ci"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT), timeout=5,
        )
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def md5(path: Path) -> str | None:
    if path.exists():
        return hashlib.md5(path.read_bytes()).hexdigest()
    return None


def load_json_safe(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def build_manifest() -> dict:
    """Build the complete manifest from all data sources."""

    # Load pipeline outputs
    vis_path = PROJECT_ROOT / "data" / "math_extractions" / "merged" / "visualization_data.json"
    aligned_path = PROJECT_ROOT / "data" / "math_extractions" / "merged" / "aligned_data.json"

    vis = load_json_safe(vis_path)
    aligned = load_json_safe(aligned_path)

    # Graph metrics
    nodes = len((vis or {}).get("nodes", []))
    links = len((vis or {}).get("links", []))
    density = (2 * links) / (nodes * (nodes - 1)) if nodes > 1 else 0.0

    # Degree metrics
    degree: dict[str, int] = {}
    if vis:
        for n in vis["nodes"]:
            degree[n["id"]] = 0
        for link in vis["links"]:
            src = link.get("source", link.get("source_group", ""))
            tgt = link.get("target", link.get("target_group", ""))
            if isinstance(src, dict): src = src.get("id", "")
            if isinstance(tgt, dict): tgt = tgt.get("id", "")
            if src in degree: degree[src] += 1
            if tgt in degree: degree[tgt] += 1
    deg_vals = sorted(degree.values()) if degree else [0]

    # Alignment metrics
    groups = (aligned or {}).get("aligned_groups", [])
    unmatched = (aligned or {}).get("unmatched_concepts", [])
    relations = (aligned or {}).get("relations", [])

    trilingual = sum(
        1 for g in groups
        if g.get("labels", {}).get("zh")
        and g.get("labels", {}).get("en")
        and g.get("labels", {}).get("de")
    )

    level_dist: dict[str, int] = {}
    for g in groups:
        lv = g.get("level", "?")
        level_dist[lv] = level_dist.get(lv, 0) + 1

    # Build manifest
    now = datetime.now().isoformat(timespec="seconds")

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "data_schema_version": DATA_SCHEMA_VERSION,
        "project": "LinguaGraph",
        "build_time": now,
        "provenance": {
            "git_commit": git_commit(),
            "git_branch": git_branch(),
            "git_commit_date": git_commit_date(),
            "pipeline_version": (vis or {}).get("version", "unknown"),
            "pipeline_scripts": "scripts/math_graph_pipeline/",
            "generated_by": "scripts/generate_manifest.py",
        },
        "graph": {
            "total_nodes": nodes,
            "total_links": links,
            "unique_ids": len(set(n["id"] for n in (vis or {}).get("nodes", []))),
            "graph_density": round(density, 6),
            "avg_degree": round(sum(deg_vals) / len(deg_vals), 4) if deg_vals else 0.0,
            "median_degree": deg_vals[len(deg_vals) // 2] if deg_vals else 0,
            "p95_degree": deg_vals[min(int(len(deg_vals) * 0.95), len(deg_vals) - 1)] if deg_vals else 0,
            "max_degree": max(deg_vals) if deg_vals else 0,
            "degree_zero": sum(1 for d in deg_vals if d == 0),
            "connected_components": None,  # computed in quality_report, not re-derived here
        },
        "alignment": {
            "aligned_groups": len(groups),
            "trilingual_groups": trilingual,
            "unmatched_concepts": len(unmatched),
            "total_relations": len(relations),
            "level_distribution": level_dist,
        },
        "checksums": {
            "visualization_data.json": md5(vis_path),
            "aligned_data.json": md5(aligned_path),
            "data.js": md5(PROJECT_ROOT / "cognitive-space" / "web" / "data.js"),
            "manifest.json": None,  # filled after writing
        },
    }

    return manifest


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate LinguaGraph manifest.json")
    parser.add_argument("--output-dir", type=str, default=".",
                        help="Output directory for manifest.json")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    output_dir = (PROJECT_ROOT / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = build_manifest()

    # Compute self-checksum after serialization
    manifest_path = output_dir / "manifest.json"
    manifest_str = json.dumps(manifest, indent=2, ensure_ascii=False)
    manifest_path.write_text(manifest_str, encoding="utf-8")
    manifest["checksums"]["manifest.json"] = hashlib.md5(manifest_str.encode("utf-8")).hexdigest()

    # Re-write with self-checksum included
    manifest_str = json.dumps(manifest, indent=2, ensure_ascii=False)
    manifest_path.write_text(manifest_str, encoding="utf-8")

    print(f"  [OK] manifest.json -> {manifest_path.relative_to(PROJECT_ROOT)}")
    print(f"       Commit: {manifest['provenance']['git_commit'] or 'N/A'}")
    print(f"       Nodes: {manifest['graph']['total_nodes']}")
    print(f"       Groups: {manifest['alignment']['aligned_groups']}")
    print(f"       Trilingual: {manifest['alignment']['trilingual_groups']}")

    # Also write a copy in the data directory for pipeline consumers
    data_manifest = PROJECT_ROOT / "data" / "math_extractions" / "merged" / "manifest.json"
    data_manifest.write_text(manifest_str, encoding="utf-8")
    print(f"  [OK] manifest.json -> {data_manifest.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
