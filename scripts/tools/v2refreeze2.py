#!/usr/bin/env python3
"""Portal v2 cs_sub links phrases (exact-count)."""
import io
for p in ("cognitive-space/portal/_v2dict.js", "cognitive-space/portal/_v2body.html"):
    t = io.open(p, encoding="utf-8").read()
    for old, new in (("238 rendered links", "233 rendered links"),
                     ("238 gerenderte Links", "233 gerenderte Links")):
        c = t.count(old)
        print(p.split("/")[-1], repr(old), "x%d" % c)
        t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(t)
print("done")
