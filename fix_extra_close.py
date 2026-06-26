import re
with open("cognitive-space/portal/index.html", "r", encoding="utf-8") as f:
    h = f.read()

# Remove the extra closing tags before CognitiveSpace
old = '</div></section>\n\n<!-- ==================== COGNITIVESPACE ==================== -->'
new = '<!-- ==================== COGNITIVESPACE ==================== -->'
if old in h:
    h = h.replace(old, new, 1)
    print("Removed extra closing tags")
else:
    print("Pattern not found")

with open("cognitive-space/portal/index.html", "w", encoding="utf-8") as f:
    f.write(h)

with open("cognitive-space/portal/index.html", "r", encoding="utf-8") as f:
    h = f.read()
s_open = h.count("<section")
s_close = h.count("</section>")
d_open = h.count("<div")
d_close = h.count("</div>")
print("Sections: %d open, %d close" % (s_open, s_close))
print("Divs: %d open, %d close (diff=%d)" % (d_open, d_close, d_open - d_close))
print("OK" if s_open == s_close and d_open == d_close else "STILL BROKEN")
