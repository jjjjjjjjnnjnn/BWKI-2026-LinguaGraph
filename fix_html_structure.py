import re

with open("cognitive-space/portal/index.html", "r", encoding="utf-8") as f:
    h = f.read()

# The findings sections have cascading unclosed tags.
# Structure should be: each finding is one <section> with one <div class="finding-card">
# We need to close all finding sections properly before the next one starts.

# Strategy: find the COMMENT before each finding-b/c/d/e section
# and insert </div></section> before each comment.

fixes = [
    # Before Finding B comment, close finding-a-content
    ("<!-- ==================== FINDING B: HDS ==================== -->",
     "</div></section>\n\n<!-- ==================== FINDING B: HDS ==================== -->"),
    # Before Finding C comment, close finding-b
    ("<!-- ==================== FINDING C: LDS ==================== -->",
     "</div></section>\n\n<!-- ==================== FINDING C: LDS ==================== -->"),
    # Before Finding D comment, close finding-c
    ("<!-- ==================== FINDING D: COVERAGE ==================== -->",
     "</div></section>\n\n<!-- ==================== FINDING D: COVERAGE ==================== -->"),
    # Before Finding E, close finding-d
    ("<!-- ==================== FINDING E: HUMAN VALIDATION ==================== -->",
     "</div></section>\n\n<!-- ==================== FINDING E: HUMAN VALIDATION ==================== -->"),
    # Before CognitiveSpace, close finding-e
    ("<!-- ==================== COGNITIVESPACE ==================== -->",
     "</div></section>\n\n<!-- ==================== COGNITIVESPACE ==================== -->"),
]

for search, replace in fixes:
    if search in h:
        h = h.replace(search, replace, 1)
        print(f"Fixed: ...^{search[4:30]}... -> added </div></section>")
    else:
        print(f"NOT FOUND: {search[:60]}")

with open("cognitive-space/portal/index.html", "w", encoding="utf-8") as f:
    f.write(h)

# Verify
print("\nVerifying...")
with open("cognitive-space/portal/index.html", "r", encoding="utf-8") as f:
    h = f.read()

s_open = h.count("<section")
s_close = h.count("</section>")
d_open = h.count("<div")
d_close = h.count("</div>")
print("Sections: %d open, %d close" % (s_open, s_close))
print("Divs: %d open, %d close" % (d_open, d_close))

# Verify specific sections
for sname in ["finding-a", "finding-a-content", "finding-b", "finding-c", "finding-d", "finding-e"]:
    opens = h.count('id="' + sname + '"')
    closes = h.count('id="' + sname + '"')  # section close uses </section>
    print(f"  section#{sname}: {h.count('id=\"' + sname + '\"')} opens")
