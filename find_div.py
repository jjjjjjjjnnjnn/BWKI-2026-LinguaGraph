import re
with open("cognitive-space/portal/index.html", "r", encoding="utf-8") as f:
    h = f.read()

# Track div opens/closes to find the unclosed one
stack = []
for i, ch in enumerate(h):
    if ch != '<':
        continue
    tag_end = h.find('>', i)
    if tag_end < 0:
        break
    tag = h[i:tag_end+1]

    if tag.startswith('</div'):
        if stack:
            if stack[-1].startswith('<div'):
                stack.pop()
            else:
                # Mismatch - check if there's any <div in stack
                for j in range(len(stack)-1, -1, -1):
                    if stack[j].startswith('<div'):
                        # Found matching div
                        stack.pop(j)
                        break
    elif tag.startswith('<div'):
        stack.append(tag)

    i = tag_end + 1

if stack:
    print("REMAINING UNMATCHED DIVS (%d):" % len(stack))
    for tag in stack:
        line_no = h[:h.find(tag)].count('\n') + 1
        # Show context
        pos = h.find(tag)
        ctx_start = max(0, pos - 20)
        ctx_end = min(len(h), pos + len(tag) + 40)
        ctx = h[ctx_start:ctx_end].replace('\n', ' ').strip()
        print(f"  Line ~{line_no}: ...{ctx}...")
else:
    print("All divs balanced!")
