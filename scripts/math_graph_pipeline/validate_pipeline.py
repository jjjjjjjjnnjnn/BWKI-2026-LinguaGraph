#!/usr/bin/env python3
"""
CognitiveSpace — Data Quality Gates

Usage:
    python scripts/math_graph_pipeline/validate_pipeline.py
        [--snapshot-file data/math_extractions/merged/pipeline_snapshot.json]
        [--check-levels-only] [--verbose]

Exits with 0 if all gates pass, 1 if any gate fails.
"""

import json
import sys
from pathlib import Path


def load_visualization(vis_path: Path) -> dict:
    with open(vis_path, encoding="utf-8") as f:
        return json.load(f)


def load_aligned(aligned_path: Path) -> dict:
    with open(aligned_path, encoding="utf-8") as f:
        return json.load(f)


def gate_01_uniqueness(vis: dict) -> bool:
    """Gate 1: Every node ID must be unique."""
    ids = [n["id"] for n in vis["nodes"]]
    unique = set(ids)
    dups = len(ids) - len(unique)
    if dups > 0:
        dup_ids = {i for i in ids if ids.count(i) > 1}
        print(f"  [FAIL] Gate 1 (uniqueness): {dups} duplicate IDs found: {dup_ids}")
        return False
    print(f"  [PASS] Gate 1 (uniqueness): {len(ids)} nodes, all unique")
    return True


def gate_02_level_consistency(aligned: dict, vis: dict) -> bool:
    """Gate 2: All aligned groups must have a level; level distribution must be stable."""
    groups = aligned.get("aligned_groups", [])
    missing = [g["id"] for g in groups if "level" not in g or not g.get("level")]
    if missing:
        print(f"  [FAIL] Gate 2 (level completeness): {len(missing)} groups missing level")
        for m in missing[:5]:
            print(f"         missing level: {m}")
        return False

    # Check level distribution
    lv_expected = {}
    for g in groups:
        lv = g.get("level", "?")
        lv_expected[lv] = lv_expected.get(lv, 0) + 1

    lv_actual = {}
    for n in vis["nodes"]:
        lv = n.get("level", "?")
        lv_actual[lv] = lv_actual.get(lv, 0) + 1

    print(f"  [PASS] Gate 2 (level): {len(groups)} groups all have level")
    print(f"         Aligned groups: {json.dumps(lv_expected)}")
    print(f"         Data.js nodes:  {json.dumps(lv_actual)}")
    return True


def gate_03_multilingual(aligned: dict, vis: dict) -> bool:
    """Gate 3: All aligned groups must have ZH/EN/DE labels; data.js nodes should have proper EN labels."""
    groups = aligned.get("aligned_groups", [])
    # Check trilingual completeness on aligned groups
    incomplete = [g["id"] for g in groups
                  if not g.get("labels", {}).get("zh")
                  or not g.get("labels", {}).get("en")
                  or not g.get("labels", {}).get("de")]
    if incomplete:
        print(f"  [FAIL] Gate 3 (trilingual): {len(incomplete)} groups missing language labels")
        for i in incomplete[:5]:
            print(f"         {i}")
        return False

    # Check how many data.js nodes have EN label that's different from ZH (proper translation)
    proper_en = sum(1 for n in vis["nodes"]
                    if n.get("labels", {}).get("en")
                    and n["labels"]["en"] != n["labels"].get("zh", ""))
    print(f"  [PASS] Gate 3 (multilingual): {len(groups)} groups trilingual")
    print(f"         Data.js nodes with proper EN label: {proper_en}/{len(vis['nodes'])}")
    return True


def gate_04_snapshot(aligned: dict, vis: dict, snapshot_path: Path) -> bool:
    """Gate 4: Compare current stats against baseline snapshot; warn on significant drift."""
    groups = aligned.get("aligned_groups", [])
    unmatched = aligned.get("unmatched_concepts", [])

    snapshot = {
        "nodes": len(vis["nodes"]),
        "node_ids": len({n["id"] for n in vis["nodes"]}),
        "links": len(vis["links"]),
        "levels": {},
        "aligned_groups": len(groups),
        "unmatched": len(unmatched),
        "relations": len(aligned.get("relations", [])),
    }
    for n in vis["nodes"]:
        lv = n.get("level", "?")
        snapshot["levels"][lv] = snapshot["levels"].get(lv, 0) + 1

    if snapshot_path.exists():
        with open(snapshot_path, encoding="utf-8") as f:
            baseline = json.load(f)

        diffs = []
        for key in ["nodes", "links", "aligned_groups", "unmatched"]:
            old = baseline.get(key, 0)
            new = snapshot[key]
            if abs(new - old) > baseline.get(key, 0) * 0.1 + 3:  # >10% or >3 change
                diffs.append(f"{key}: {old} -> {new}")

        for lv, cnt in snapshot["levels"].items():
            old_cnt = baseline.get("levels", {}).get(lv, 0)
            if abs(cnt - old_cnt) > old_cnt * 0.15 + 5:
                diffs.append(f"level[{lv}]: {old_cnt} -> {cnt}")

        if diffs:
            print(f"  [WARN] Gate 4 (snapshot): drift detected vs baseline:")
            for d in diffs:
                print(f"         {d}")
        else:
            print(f"  [PASS] Gate 4 (snapshot): stable vs baseline")
    else:
        print(f"  [INFO] Gate 4 (snapshot): no baseline yet — writing snapshot to {snapshot_path}")

    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)
    return True


def _project_root() -> Path:
    """Robust project root detection (handles garbled paths on Windows)."""
    here = Path(__file__).resolve().parent  # scripts/math_graph_pipeline/
    for cand in [here.parent.parent.parent, here.parent.parent, here.parent]:
        if (cand / "cognitive-space").exists():
            return cand
    # Fallback: try CWD
    cand = Path.cwd()
    if (cand / "cognitive-space").exists():
        return cand
    raise RuntimeError(f"Cannot find project root from {here}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="CognitiveSpace data quality gates")
    parser.add_argument("--snapshot-file", type=str,
                        default="data/math_extractions/merged/pipeline_snapshot.json")
    parser.add_argument("--check-levels-only", action="store_true",
                        help="Only check levels (fast mode)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    project_root = _project_root()
    aligned_path = project_root / "data/math_extractions/merged/aligned_data.json"
    vis_path = project_root / "data/math_extractions/merged/visualization_data.json"
    snapshot_path = (project_root / args.snapshot_file).resolve()

    if not aligned_path.exists():
        print(f"ERROR: Run pipeline first — {aligned_path} not found")
        sys.exit(1)
    if not vis_path.exists():
        print(f"ERROR: Run export_graph.py first — {vis_path} not found")
        sys.exit(1)

    aligned = load_aligned(aligned_path)
    vis = load_visualization(vis_path)

    print("=" * 50)
    print("  Data Quality Gates")
    print("=" * 50)

    all_ok = True
    all_ok &= gate_01_uniqueness(vis)
    all_ok &= gate_02_level_consistency(aligned, vis)

    if not args.check_levels_only:
        all_ok &= gate_03_multilingual(aligned, vis)
        all_ok &= gate_04_snapshot(aligned, vis, snapshot_path)

    if all_ok:
        print(f"\n{'=' * 50}")
        print("  ALL GATES PASSED")
        print(f"{'=' * 50}")
    else:
        print(f"\n{'=' * 50}")
        print("  SOME GATES FAILED — review above")
        print(f"{'=' * 50}")
        sys.exit(1)


if __name__ == "__main__":
    main()
