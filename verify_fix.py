import re
with open("cognitive-space/portal/index.html", "r", encoding="utf-8") as f:
    h = f.read()
d_open = h.count("<div")
d_close = h.count("</div>")
print("Divs: %d open, %d close (diff=%d)" % (d_open, d_close, d_open - d_close))
s_open = h.count("<section")
s_close = h.count("</section>")
print("Sections: %d open, %d close" % (s_open, s_close))
if s_open == s_close and d_open == d_close:
    print("PERFECT!")
else:
    print("STILL NEEDS WORK")
