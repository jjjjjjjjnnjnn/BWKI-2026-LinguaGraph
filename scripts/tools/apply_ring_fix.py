#!/usr/bin/env python3
"""Apply ring-breaking verdict fixes (research/ring_verdict_20260916.md, 9 actions).

Ops: delete-by-index (break weakest edge of a cycle) and reverse-by-index
(swap source/target for wrong-direction edges).
Default dry-run (lists edits + pre-checks). --apply executes:
  backup whole files to research/prune_backup_20260916_ring/ (new dir),
  apply deletes (descending index per file) then reverses, rewrite data JSON.
Guards: skips merged/, asserts edge_index in range, asserts the edge at index
still matches expected (source,target,type) from the verdict table (refuses on
drift), refuses reverse if swapped edge would duplicate an existing edge.
Usage: python scripts/tools/apply_ring_fix.py [--apply] [--help]
Writes data/*.json ONLY under --apply; backups under research/.
"""
import json
import os
import shutil
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(BASE_DIR, "data", "math_extractions")
BACKUP = os.path.join(BASE_DIR, "research", "prune_backup_20260916_ring")

# (ring, file, edge_index, op, expected source, expected target, expected type)
RING_PLAN = [
    ("#2", "en_khan_academy_k-2.json", 5, "delete", "counting", "place value", "requires"),
    ("#3", "de_westermann_9-10.json", 13, "delete", "Erwartungswert", "Varianz", "requires"),
    ("#4+#10", "en_khan_academy_5-6.json", 11, "delete", "variable", "equation", "requires"),
    ("#5", "zh_小学数学_二年级上.json", 7, "delete", "克", "千克", "representation"),
    ("#6", "zh_初中数学_九年级.json", 7, "delete", "相似三角形", "全等三角形", "generalization"),
    ("#7", "zh_选修2-2_ch9_sec9.1-9.2.json", 7, "delete", "方向导数", "梯度", "representation"),
    ("#8", "zh_小学数学_二年级上.json", 8, "delete", "长方形", "正方形", "generalization"),
    ("#9", "en_khan_academy_3-4.json", 9, "delete", "area", "perimeter", "analogy"),
    ("#11", "zh_选修2-2_ch9_sec9.5.json", 0, "reverse", "偏微分方程", "常微分方程", "generalization"),
]


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: apply_ring_fix.py [--apply] [--help]")
        print("  Dry-run lists 9 ring-verdict deletes/reverse with drift checks.")
        print("  --apply backs up to research/prune_backup_20260916_ring/ then applies.")
        return 0
    apply = "--apply" in sys.argv
    staged = []
    for ring, f, i, op, src, tgt, typ in RING_PLAN:
        assert "merged" not in f, "unsafe " + f
        d = json.load(open(os.path.join(DATA, f), encoding="utf-8"))
        rels = d.get("extracted_relations", [])
        assert isinstance(i, int) and 0 <= i < len(rels), "bad index %s %s" % (f, i)
        r = rels[i]
        assert (r.get("source"), r.get("target"), r.get("type")) == (src, tgt, typ), \
            "drift at %s [%d]: got %s->%s %s" % (f, i, r.get("source"), r.get("target"), r.get("type"))
        if op == "reverse":
            key = (tgt, src)
            others = [(x.get("source"), x.get("target")) for j, x in enumerate(rels) if j != i]
            assert key not in others, "reverse would create dup: %s" % f
        staged.append((ring, f, i, op, src, tgt, typ))
        print("  %s %s [%d] %s: %s -> %s (%s)" % (ring, f, i, op, src, tgt, typ))
    print("RING_PLAN_N=%d (delete=%d reverse=%d)" % (
        len(staged), sum(1 for s in staged if s[3] == "delete"),
        sum(1 for s in staged if s[3] == "reverse")))
    if not apply:
        print("DRY_RUN (add --apply to execute)")
        return 0
    os.makedirs(BACKUP, exist_ok=True)
    by_file = {}
    for ring, f, i, op, src, tgt, typ in staged:
        by_file.setdefault(f, []).append((i, op))
    for f, edits in sorted(by_file.items()):
        shutil.copyfile(os.path.join(DATA, f), os.path.join(BACKUP, f))
        d = json.load(open(os.path.join(DATA, f), encoding="utf-8"))
        rels = d["extracted_relations"]
        for i, op in sorted(edits, reverse=True):
            if op == "delete":
                rels.pop(i)
            else:
                r = rels[i]
                r["source"], r["target"] = r["target"], r["source"]
        json.dump(d, open(os.path.join(DATA, f), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("APPLIED %s (%s)" % (f, ",".join("%s[%d]" % (op, i) for i, op in edits)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
