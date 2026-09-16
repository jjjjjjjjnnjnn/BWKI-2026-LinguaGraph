#!/usr/bin/env python3
"""Live-number re-freeze 517/233/834/0.933 across live docs (replace-all + counts).

Historical files (CHANGELOG, quality_history, forensic, workbench, _archive,
data/corpus, config, LINGUAGRAPH_*, v1 archive, DOI strings) are EXCLUDED.
"""
import io

jobs = [
    ("README.md", [("525 direct", "517 direct"), ("556 concepts, 525 relations", "556 concepts, 517 relations"),
                   ("(556/525/219)", "(556/517/219)"), ("525 relations (+~3000 transitive)", "517 relations (+~3000 transitive)")]),
    ("README_ZH.md", [("525", "517")]),
    ("README_DE.md", [("525", "517")]),
    ("research/numbers_ssot_20260916.json", [("525 relations", "517 relations")]),
    ("docs/SSOT-web.md", [("525", "517"), ("238 rendered", "233 rendered"), ("238 gerendert", "233 gerendert"),
                           ("839 links", "834 links"), ("238+386+215 = 839", "233+386+215 = 834"),
                           ("238+386+215", "233+386+215")]),
    ("docs/submission/plattform_antworten.md", [("525 Relationen", "517 Relationen")]),
    ("submission/final/plattform_antworten.md", [("525 Relationen", "517 Relationen")]),
    ("submission/final/README.md", [("525", "517")]),
    ("docs/submission/README.md", [("525", "517")]),
    ("submission/pitch/README.md", [("525", "517")]),
    ("docs/submission/einreichung_checkliste.md", [("556/525/219", "556/517/219")]),
    ("docs/paper/01_abstract_introduction.md", [("525", "517")]),
    ("docs/paper/02_methodology.md", [("525", "517")]),
    ("docs/paper/03_results.md", [("525", "517"), ("238 Links", "233 Links")]),
    ("cognitive-space/web/i18n.js", [("525", "517"), ("238 shown", "233 shown"), ("238 gezeigt", "233 gezeigt")]),
    ("cognitive-space/web/index.html", [("839", "834"), ("238 links (visual subset of 525 relations", "233 links (visual subset of 517 relations")]),
    ("cognitive-space/web/story/index.html", [("525 relations", "517 relations")]),
]
for p, pairs in jobs:
    t = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print("%s: %r x%d" % (p.split("/")[-1], old[:36], c))
        t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(t)
print("refreeze done")
