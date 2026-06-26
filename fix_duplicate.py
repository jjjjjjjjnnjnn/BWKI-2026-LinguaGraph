import re
with open("cognitive-space/portal/index.html", "r", encoding="utf-8") as f:
    h = f.read()

# Remove duplicate closing tags before "FINDING E"
h = h.replace("</div></section>\n\n<!-- ==================== FINDING E: HUMAN VALIDATION ==================== -->",
              "<!-- ==================== FINDING E: HUMAN VALIDATION ==================== -->", 1)

with open("cognitive-space/portal/index.html", "w", encoding="utf-8") as f:
    f.write(h)

# Verify
with open("cognitive-space/portal/index.html", "r", encoding="utf-8") as f:
    h = f.read()
s_open = h.count("<section")
s_close = h.count("</section>")
d_open = h.count("<div")
d_close = h.count("</div>")
print("Sections: %d open, %d close" % (s_open, s_close))
print("Divs: %d open, %d close (diff=%d)" % (d_open, d_close, d_open - d_close))
print("PERFECT!" if s_open == s_close and d_open == d_close else "STILL BROKEN")
