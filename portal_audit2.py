import re

with open("cognitive-space/portal/index.html", "r", encoding="utf-8") as f:
    h = f.read()

# Find all section tags with positions
tags = []
for m in re.finditer(r"</?(section|div)[^>]*>", h):
    tags.append((m.start(), m.group()))

# Track open/close
stack = []
for pos, tag in tags:
    if tag.startswith("</"):
        # Closing tag - find matching open
        tag_name = re.search(r"</(\w+)", tag).group(1)
        if stack and stack[-1][1].startswith("<" + tag_name):
            stack.pop()
        elif any(t for t in stack if t[1].startswith("<" + tag_name)):
            # Mismatch
            pass
    else:
        stack.append((pos, tag))

print("UNMATCHED OPEN TAGS (%d):" % len(stack))
for pos, tag in stack:
    # Show context around the unmatched tag
    context_start = max(0, pos - 30)
    context_end = min(len(h), pos + 40)
    context = h[context_start:context_end].replace("\n", " ").strip()
    print("  Line ~%d: ...%s..." % (h[:pos].count("\n") + 1, context))
