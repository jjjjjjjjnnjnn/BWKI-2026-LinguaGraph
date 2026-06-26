import re
with open("cognitive-space/portal/index.html", "r", encoding="utf-8") as f:
    h = f.read()
sec_open = h.count("<section")
sec_close = h.count("</section>")
div_open = h.count("<div")
div_close = h.count("</div>")
print("Sections: %d open, %d close" % (sec_open, sec_close))
print("Divs: %d open, %d close (diff=%d)" % (div_open, div_close, div_open - div_close))

# Check setLanguage for crashes
sl_start = h.index("function setLanguage")
sl_end = h.index("function initLang")
body = h[sl_start:sl_end]
print("setLanguage braces: %d = %d -> %s" % (body.count("{"), body.count("}"), "OK" if body.count("{") == body.count("}") else "BROKEN"))

# Check for any _q or _a calls that might reference bad selectors
bad = re.findall(r"(?:document\.querySelector\(['\"][^'\"]+['\"]\))", h[sl_start:sl_end])
print("Query selectors in setLanguage: %d" % len(bad))

# Check mermaid config
mermaid_init = re.search(r"mermaid\.initialize\(\{([^}]*)\}", h)
if mermaid_init:
    print("Mermaid init: %s..." % mermaid_init.group(0)[:80])
