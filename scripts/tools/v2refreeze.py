#!/usr/bin/env python3
"""Portal v2 re-freeze 517/233/0.933 (replace-all, min-count asserts)."""
import io

jobs = {
    "cognitive-space/portal/_v2dict.js": [
        ("(0.934 / 0.938)", "(0.933 / 0.938)"),
        ("Frozen: 0.519 / 0.934 / 0.938", "Frozen: 0.519 / 0.933 / 0.938"),
        ("（0.934/0.938）", "（0.933/0.938）"),
        ("0.519/0.934/0.938", "0.519/0.933/0.938"),
        ("(of 525)", "(of 517)"),
        ("(von 525)", "(von 517)"),
        ("（共 525）", "（共 517）"),
        ("(238 rendered)", "(233 rendered)"),
        ("(238 gerendert)", "(233 gerendert)"),
        ("（渲染 238）", "（渲染 233）"),
        ("238 渲染边", "233 渲染边"),
    ],
    "cognitive-space/portal/_v2body.html": [
        ("(0.934 / 0.938)", "(0.933 / 0.938)"),
        ("0.519 / 0.934 / 0.938", "0.519 / 0.933 / 0.938"),
        ("556·525·219", "556·517·219"),
        ("(of 525)", "(of 517)"),
        ("(238 rendered)", "(233 rendered)"),
    ],
}
for p, pairs in jobs.items():
    t = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        assert c >= 1, "%s: missing %r" % (p, old[:30])
        t = t.replace(old, new)
        print("%s: %r x%d" % (p.split("/")[-1], old[:24], c))
    io.open(p, "w", encoding="utf-8").write(t)
print("v2 refreeze done")
