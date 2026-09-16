#!/usr/bin/env python3
"""Portal v2 number re-freeze 517/233/0.933 ( herpes: exact-count asserts)."""
import io

p = "cognitive-space/portal/_v2dict.js"
t = io.open(p, encoding="utf-8").read()
pairs = [
    ("0.519 / 0.934 / 0.938", "0.519 / 0.933 / 0.938"),
    ("(0.934 / 0.938)", "(0.933 / 0.938)"),
    ("556\u00b7525\u00b7219", "556\u00b7517\u00b7219"),
    ("(of 525)", "(of 517)"),
    ("(von 525)", "(von 517)"),
    ("238 rendered", "233 rendered"),
    ("238 gerendert", "233 gerendert"),
]
for old, new in pairs:
    n = t.count(old)
    print("%r x%d" % (old[:24], n))
    assert n >= 1, "missing: " + old[:30]
    t = t.replace(old, new)
# CJK cs_sub 525/238 (count first, replace all)
for old_frag in ["\uff08525\uff09", "525\uff09", "\u6e32\u67d3 238", "238 \u6e32\u67d3"]:
    print("CJK %r x%d" % (old_frag, t.count(old_frag)))
io.open(p, "w", encoding="utf-8").write(t)
print("dict done")
