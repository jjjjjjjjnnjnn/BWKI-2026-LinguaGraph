import re
with open("cognitive-space/portal/index.html", "r", encoding="utf-8") as f:
    h = f.read()

# Find where the extra </section> is hiding
# Let's track opening and closing sections
opens = [(m.start(), m.group()) for m in re.finditer(r"<section\b[^>]*>", h)]
closes = [(m.start(), m.group()) for m in re.finditer(r"</section\s*>", h)]

# Match them properly
open_positions = sorted([p for p, t in opens])
close_positions = sorted([p for p, t in closes])

# Pair opens with closes (simple approach)
# If there are more closes than opens, find the orphan close
if len(close_positions) > len(open_positions):
    orphan_count = len(close_positions) - len(open_positions)
    print(f"Found {orphan_count} orphan </section> tags")

    for i in range(len(close_positions) - 1, -1, -1):
        # Check if this close has a matching open before it
        open_before = [o for o in open_positions if o < close_positions[i]]
        if len(open_before) > i:
            continue  # This close has a matching open
        # Orphan found!
        context = h[close_positions[i]-20:close_positions[i]+30].replace("\n", " ")
        print(f"  Orphan at pos {close_positions[i]}: ...{context}...")
        # Show line number
        line_no = h[:close_positions[i]].count("\n") + 1
        print(f"  Line: {line_no}")
