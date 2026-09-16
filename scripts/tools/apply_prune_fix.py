#!/usr/bin/env python3
"""Apply deterministic prune deletions (dup/self-loop/noise-edge only).

Default dry-run (lists exact edits). --apply executes:
  backup changed files to research/prune_backup_20260915/ (new dir),
  delete by edge_index (descending per file), rewrite data JSON.
NEVER touches: 纠目标/补充概念/人工定 kinds, merged/ dir, forbidden zones.
Usage: python scripts/tools/apply_prune_fix.py [--apply]
"""
import json
import os
import shutil
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAND = os.path.join(BASE_DIR, "research", "prune_candidates_20260914.json")
DATA = os.path.join(BASE_DIR, "data", "math_extractions")
BACKUP = os.path.join(BASE_DIR, "research", "prune_backup_20260915")

ALLOW_KINDS = {"dup_relation", "self_loop", "dangling"}


def load_cands():
    items = json.load(open(CAND, encoding="utf-8"))
    dels, other = [], []
    for c in items:
        det = c.get("detail", {})
        if c.get("kind") == "dup_relation":
            dels.append(c)
        elif c.get("kind") == "self_loop":
            dels.append(c)
        elif c.get("kind") == "dangling" and det.get("suggest") is None \
                and det.get("freq_global", 0) <= 1 and "噪声" in str(det.get("reason", "")):
            dels.append(c)  # noise-edge delete (Trennung der Variablen)
        else:
            other.append(c)
    return dels, other


def plan(dels):
    by_file = {}
    for c in dels:
        det = c.get("detail", {})
        if c.get("kind") == "dup_relation":
            idxs = det.get("edge_indices", [])[1:]  # keep first occurrence
        else:
            idxs = [det.get("edge_index")]
        by_file.setdefault(c["file"], []).extend(idxs)
    return by_file


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: apply_prune_fix.py [--apply] [--help]")
        print("  Dry-run lists deterministic deletions (dup/self-loop/noise-edge).")
        print("  --apply backs up to research/prune_backup_20260915/ then deletes by edge_index.")
        return 0
    apply = "--apply" in sys.argv
    dels, other = load_cands()
    by_file = plan(dels)
    print("DELETE_PLAN files=%d edges=%d kinds=%s" % (
        len(by_file), sum(len(v) for v in by_file.values()),
        sorted({c.get("kind") for c in dels})))
    for f, idxs in sorted(by_file.items()):
        print("  %s delete_index=%s" % (f, sorted(idxs, reverse=True)))
    print("HELD kinds=%d (manual review only)" % len(other))
    if not apply:
        print("DRY_RUN (add --apply to execute)")
        return 0
    os.makedirs(BACKUP, exist_ok=True)
    for f, idxs in sorted(by_file.items()):
        p = os.path.join(DATA, f)
        assert os.path.exists(p) and "merged" not in f, "unsafe target " + f
        d = json.load(open(p, encoding="utf-8"))
        rels = d.get("extracted_relations", [])
        for i in sorted(idxs, reverse=True):
            assert isinstance(i, int) and 0 <= i < len(rels), "bad index %s in %s" % (i, f)
        shutil.copyfile(p, os.path.join(BACKUP, f))
        for i in sorted(idxs, reverse=True):
            rels.pop(i)
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("APPLIED %s (-%d edges)" % (f, len(idxs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
