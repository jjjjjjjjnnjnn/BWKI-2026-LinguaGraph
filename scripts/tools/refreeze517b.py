#!/usr/bin/env python3
"""Round-2 refreeze: LDS-K 0.934->0.933 + leftover 238 (live files only)."""
import io

jobs = [
    ("research/numbers_ssot_20260916.json",
     [("(238 rendered links)", "(233 rendered links)"),
      ('"zh_en": 0.934', '"zh_en": 0.933'),
      ('"status": "frozen"}', '"status": "re-frozen 2026-09-16 (517/233/0.933; ring+prune fixes; deltas within rounding)"}')]),
    ("cognitive-space/web/i18n.js", [("展示 238", "展示 233")]),
    ("README.md", [("ZH-EN (0.934)", "ZH-EN (0.933)"),
                   ("(freeze: 0.9336/0.9382/0.5188,", "(freeze: 0.9330/0.9378/0.5190 (re-freeze 2026-09-16, Δ≤0.001),")]),
    ("README_ZH.md", [("(0.934)", "(0.933)"),
                      ("冻结值：0.9336/0.9382/0.5188，", "冻结值：0.9330/0.9378/0.5190（2026-09-16 重冻，Δ≤0.001），")]),
    ("docs/paper/03_results.md", [("| ZH-EN | 0.934 |", "| ZH-EN | 0.933 |"),
                                  ("| Full (LDS-K baseline) | 0.934 | 0.938 | 0.519 |",
                                   "| Full (LDS-K baseline) | 0.933 | 0.938 | 0.519 |"),
                                  ("| Node-Permuted Null | 0.934 | 0.938 | 0.519 |",
                                   "| Node-Permuted Null | 0.933 | 0.938 | 0.519 |"),
                                  ("| Mathematik-Lehrbücher | 0.934 | 0.938 | **0.519** |",
                                   "| Mathematik-Lehrbücher | 0.933 | 0.938 | **0.519** |")]),
    ("docs/paper/04_discussion.md", [("(0.934/0.938", "(0.933/0.938")]),
]
for p, pairs in jobs:
    t = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print("%s: %r x%d" % (p.split("/")[-1], old[:40], c))
        assert c >= 1, "missing " + old[:40]
        t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(t)
print("round2 done")
