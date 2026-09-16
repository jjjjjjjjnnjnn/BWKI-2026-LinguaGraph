#!/usr/bin/env python3
"""LEDGER re-freeze edits (exact)."""
import io
p = "docs/BASELINE_LEDGER.md"
t = io.open(p, encoding="utf-8").read()
e1 = "Full 0.934/0.938/0.519 vs Structure Null 0.957/0.957/0.717"
assert t.count(e1) == 1
t = t.replace(e1, "Full 0.933/0.938/0.519 (re-freeze 2026-09-16) vs Structure Null 0.957/0.957/0.717")
e2 = "wiki 0.698/0.723/0.819 vs math 0.934/0.938/0.519"
assert t.count(e2) == 1
t = t.replace(e2, "wiki 0.698/0.723/0.819 vs math 0.933/0.938/0.519")
anchor = "portal W \u6307\u9488\uff08paper \u00a79 \u7ed3\u8bba\u7ae0\uff0c\u8bc4\u5ba1\u8bc1\u636e\u5916\uff09\u3002"
assert t.count(anchor) == 1
t = t.replace(anchor, anchor + "\n- \u518d\u51bb\u7ed3 2026-09-16\uff08ring/prune \u4fee\u590d\u540e pipeline \u91cd\u7b97\uff09\uff1a"
              "merged relations 525\u2192517\uff0cvis links 238\u2192233\uff08\u5bc6\u5ea60.0015/\u5206\u91cf388/"
              "\u96f6\u5ea6381/\u6700\u5927\u5206\u91cf121 \u4e0d\u53d8\uff09\uff0c"
              "Full LDS-K 0.9336/0.9382/0.5188\u21920.9330/0.9378/0.5190"
              "(\u53d1\u88680.933/0.938/0.519\uff0c\u03b4\u22640.001\u820d\u5165\u5bb9\u9650\u5185)\uff0c"
              "STEAM 839\u2192834\uff1bCI guard \u4e0e SSOT \u540c\u6b65\uff1b10 \u6761\u51cf\u886812 \u6761\u589e"
              "\u5747\u53ef\u8ffd\u6eaf\u81f3\u5ba1\u8ba1\u4fee\u590d\u3002")
io.open(p, "w", encoding="utf-8").write(t)
print("ledger done")
