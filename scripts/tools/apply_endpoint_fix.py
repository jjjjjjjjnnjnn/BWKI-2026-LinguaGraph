#!/usr/bin/env python3
"""Apply endpoint fixes from a JSON plan (R3 policy A, phased).

Plan format: [{"file": ..., "edge_index": N, "side": "source|target", "new": "..."}, ...]
Default dry-run (lists edits + pre-checks). --apply executes:
  backup whole files to research/prune_backup_20260916_endpoint/ (new dir),
  rewrite endpoint strings, save data JSON.
Guards: skips merged/, asserts edge_index in range, asserts old endpoint still
dangling (concept set built from file), refuses if new value duplicates an
existing edge (would create dup).
Usage: python scripts/tools/apply_endpoint_fix.py --plan <json> [--apply] [--help]
Writes data/*.json ONLY under --apply; backups under research/.
"""
import json
import os
import shutil
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(BASE_DIR, "data", "math_extractions")
BACKUP = os.path.join(BASE_DIR, "research", "prune_backup_20260916_endpoint")


def concepts_of(d):
    return {c.get("name", "") for c in d.get("extracted_concepts", []) if isinstance(c, dict)}


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: apply_endpoint_fix.py --plan <json> [--apply] [--help]")
        return 0
    if "--plan" not in sys.argv:
        print("usage: apply_endpoint_fix.py --plan <json> [--apply]")
        return 1
    plan = json.load(open(sys.argv[sys.argv.index("--plan") + 1], encoding="utf-8"))
    apply = "--apply" in sys.argv
    print("PLAN_N=%d" % len(plan))
    staged = []
    for e in plan:
        f, i, side, new = e["file"], e["edge_index"], e["side"], e["new"]
        assert "merged" not in f, "unsafe " + f
        d = json.load(open(os.path.join(DATA, f), encoding="utf-8"))
        rels = d.get("extracted_relations", [])
        assert isinstance(i, int) and 0 <= i < len(rels), "bad index %s %s" % (f, i)
        r = rels[i]
        old = r.get(side, "")
        assert old not in concepts_of(d), "no longer dangling: %s %s" % (f, old)
        assert new in concepts_of(d), "new value not a concept: %s %s" % (f, new)
        r2 = dict(r)
        r2[side] = new
        key = (r2.get("source"), r2.get("target"))
        others = [(x.get("source"), x.get("target")) for j, x in enumerate(rels) if j != i]
        assert key not in others, "would create dup: %s %s" % (f, key)
        staged.append((f, i, side, old, new))
        print("  %s [%d] %s: %s -> %s" % (f, i, side, old, new))
    if not apply:
        print("DRY_RUN (add --apply to execute)")
        return 0
    os.makedirs(BACKUP, exist_ok=True)
    by_file = {}
    for f, i, side, old, new in staged:
        by_file.setdefault(f, []).append((i, side, new))
    for f, edits in sorted(by_file.items()):
        shutil.copyfile(os.path.join(DATA, f), os.path.join(BACKUP, f))
        d = json.load(open(os.path.join(DATA, f), encoding="utf-8"))
        for i, side, new in edits:
            d["extracted_relations"][i][side] = new
        json.dump(d, open(os.path.join(DATA, f), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("APPLIED %s (%d endpoints)" % (f, len(edits)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
