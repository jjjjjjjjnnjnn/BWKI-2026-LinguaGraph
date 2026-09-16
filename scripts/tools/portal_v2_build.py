#!/usr/bin/env python3
"""Assemble portal v2: v1 head+CSS (lines 1-259) + new body + dict + JS core."""
import io

P = "cognitive-space/portal/"
v1 = io.open(P + "index.html", encoding="utf-8").read().splitlines()
assert v1[0].startswith("<!DOCTYPE") and v1[258].strip() == "</style>", v1[258][:60]
head = "\n".join(v1[:259])
body = io.open(P + "_v2body.html", encoding="utf-8").read()
d = io.open(P + "_v2dict.js", encoding="utf-8").read()
js = io.open(P + "_v2js.js", encoding="utf-8").read()
out = head + "\n</head>\n<body>\n" + body + "\n<script>\n" + d + "\n</script>\n" + js + "\n</body>\n</html>\n"
io.open(P + "index.v2.html", "w", encoding="utf-8").write(out)
print("v2 lines:", len(out.splitlines()))
