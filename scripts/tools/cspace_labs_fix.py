#!/usr/bin/env python3
"""cspace dict: labs relabel (en/de/zh) + stale 839/525/238 fixes."""
import io
p = "cognitive-space/portal/cspace.html"
L = io.open(p, encoding="utf-8").read().split("\n")
assert "cds-terrain" not in "\n".join(L)[15000:30000] or True
jobs = [
 ("cds_t: \"CDS terrain\", cds_s: \"3 disciplines \u00d7 4 levels \u00b7 Finding A\", cds_d: \"Concept-density bars (2D). Peaks \u2605, values on hover, click through to the finding.\"",
  "cds_t: \"Reproduce lab\", cds_s: \"5 steps \u00b7 run it yourself\", cds_d: \"Each methodology step hands-on: align a word, move the LDS threshold, run 50 permutations, light up the 59-run roster.\""),
 ("gal_t: \"Margin proof\", gal_s: \"59 runs \u00b7 sorted desc \u00b7 59/59 positive\", gal_d: \"Every full ZH-DE margin as a sorted bar. Length = margin; red outline = western runs (scattered = no origin clustering).\"",
  "gal_t: \"Counterexample hunter\", gal_s: \"8 tough cases \u00b7 verdict included\", gal_d: \"The concepts that look most like counterexamples, side by side in three languages \u2014 with the ruling why they don't overturn claim C.\""),
 ("tow_t: \"Coverage towers\", tow_s: \"4 systems \u00b7 per-stage bars\", tow_d: \"Textbook\u2013curriculum coverage as towers. Bright bars = overall. Matched/total counts on hover.\"",
  "tow_t: \"Limit switchboard\", tow_s: \"6 limits \u00b7 switch them off\", tow_d: \"Turn off any limitation and watch which findings go dim \u2014 plus the misreading you'd fall for without it.\""),
 ("steam_s: \"1,143 nodes \u00b7 839 links \u00b7 no cross-links\"", "steam_s: \"1,143 nodes \u00b7 834 links \u00b7 no cross-links\""),
 ("math_s: \"556 nodes \u00b7 525 relations (238 shown) \u00b7 219 groups\"", "math_s: \"556 nodes \u00b7 517 relations (233 shown) \u00b7 219 groups\""),
 ("cds_t: \"CDS-Terrain\", cds_s: \"3 F\u00e4cher \u00d7 4 Stufen \u00b7 Finding A\", cds_d: \"Konzeptdichte-Balken (2D). Spitzen \u2605, Werte beim Hovern, Klick zum Finding.\"",
  "cds_t: \"Reproduktions-Labor\", cds_s: \"5 Schritte \u00b7 selbst ausf\u00fchren\", cds_d: \"Jeder Methodenschritt zum Anfassen: Wort alignieren, LDS-Schwelle ziehen, 50 Permutationen laufen lassen, 59er-Roster aufleuchten.\""),
 ("gal_t: \"Margin-Beleg\", gal_s: \"59 Runs \u00b7 absteigend \u00b7 59/59 positiv\", gal_d: \"Jede vollst\u00e4ndige ZH-DE-Marge als sortierter Balken. L\u00e4nge = Marge; rote Kontur = West-Runs (verstreut = kein Herkunfts-Cluster). Klick zum Roster.\"",
  "gal_t: \"Gegenbeispiel-Jagd\", gal_s: \"8 harte F\u00e4lle \u00b7 mit Urteil\", gal_d: \"Die Konzepte, die am meisten wie Gegenbeispiele aussehen, dreisprachig nebeneinander \u2014 mit Urteil, warum sie Claim C nicht kippen.\""),
 ("tow_t: \"Coverage-T\u00fcrme\", tow_s: \"4 Systeme \u00b7 Stufen-Balken\", tow_d: \"Lehrbuch-Curriculum-Abdeckung als T\u00fcrme. Helle Balken = gesamt. Treffer/Gesamt beim Hovern.\"",
  "tow_t: \"Limit-Schalttafel\", tow_s: \"6 Limits \u00b7 abschaltbar\", tow_d: \"Ein Limit abschalten und zusehen, welche Findings verblassen \u2014 plus die Fehldeutung, der man ohne es erl\u00e4ge.\""),
 ("steam_s: \"1.143 Knoten \u00b7 839 Kanten \u00b7 keine Querbr\u00fccken\"", "steam_s: \"1.143 Knoten \u00b7 834 Kanten \u00b7 keine Querbr\u00fccken\""),
 ("math_s: \"556 Knoten \u00b7 525 Relationen (238 gezeigt) \u00b7 219 Gruppen\"", "math_s: \"556 Knoten \u00b7 517 Relationen (233 gezeigt) \u00b7 219 Gruppen\""),
]
t = "\n".join(L)
SCOPE2 = [
 ("(556 nodes \u00b7 525 relations \u00b7 219 groups), 238 links rendered", "(556 nodes \u00b7 517 relations \u00b7 219 groups), 233 links rendered"),
 ("(556 Knoten \u00b7 525 Relationen \u00b7 219 Gruppen), 238 Links dargestellt", "(556 Knoten \u00b7 517 Relationen \u00b7 219 Gruppen), 233 Links dargestellt"),
]
for old, new in SCOPE2:
    c = t.count(old)
    print("scope x%d" % c)
    assert c >= 1, old[:60]
    t = t.replace(old, new)
for old, new in jobs:
    c = t.count(old)
    print("x%d %s..." % (c, old[:40]))
    assert c == 1, old[:60]
    t = t.replace(old, new)
import re
zh_new = {
 "cds_t": "\u590d\u7b97\u5b9e\u9a8c\u5ba4", "cds_s": "5 \u6b65 \u00b7 \u4eb2\u624b\u8dd1\u4e00\u904d",
 "cds_d": "\u6bcf\u4e2a\u65b9\u6cd5\u6b65\u9aa4\u90fd\u53ef\u52a8\u624b\uff1a\u5bf9\u9f50\u4e00\u4e2a\u8bcd\u3001\u62d6\u52a8 LDS \u9608\u503c\u3001\u8dd1 50 \u6b21\u7f6e\u6362\u3001\u70b9\u4eae 59 \u6b21\u590d\u7b97\u540d\u5f55\u3002",
 "gal_t": "\u53cd\u4f8b\u730e\u4eba", "gal_s": "8 \u4e2a\u786c\u832c \u00b7 \u9644\u88c1\u51b3",
 "gal_d": "\u6700\u50cf\u53cd\u4f8b\u7684\u6982\u5ff5\u4e09\u8bed\u5e76\u6392\u2014\u2014\u9644\u88c1\u51b3\uff1a\u4e3a\u4ec0\u4e48\u5b83\u4eec\u63a8\u4e0d\u7ffb\u7ed3\u8bba C\u3002",
 "tow_t": "\u9650\u5236\u5f00\u5173\u677f", "tow_s": "6 \u6761\u9650\u5236 \u00b7 \u5173\u6389\u8bd5\u8bd5",
 "tow_d": "\u5173\u6389\u4efb\u4e00\u6761\u9650\u5236\uff0c\u770b\u54ea\u4e9b\u53d1\u73b0\u53d8\u6697\u2014\u2014\u4ee5\u53ca\u6ca1\u6709\u5b83\u4f60\u4f1a\u8bef\u8bfb\u51fa\u4ec0\u4e48\u3002",
 "steam_s": "1,143 \u8282\u70b9 \u00b7 834 \u8fb9 \u00b7 \u65e0\u8de8\u5b66\u79d1\u6865",
 "math_s": "556 \u8282\u70b9 \u00b7 517 \u5173\u7cfb\uff08\u5c55\u793a 233\uff09\u00b7 219 \u5206\u7ec4",
}
for k, v in zh_new.items():
    pat = re.compile(r"(%s: \")[^\"]*(\")" % k)
    line = [l for l in t.split("\n") if l.startswith("zh: ")][0]
    newline, n = pat.subn(r"\g<1>" + v + r"\g<2>", line)
    print("zh %s x%d" % (k, n))
    assert n == 1, k
    t = t.replace(line, newline)
m = re.search(r"(scope: \".*?556.*?\")", t)
print("zh-scope-before:", m.group(1)[:80] if m else None)
t = re.sub(r"525 \u5173\u7cfb", "517 \u5173\u7cfb", t)
t = re.sub(r"\u6e32\u67d3 238 \u6761", "\u6e32\u67d3 233 \u6761", t)
io.open(p, "w", encoding="utf-8").write(t)
print("done")
