import re
with open("cognitive-space/portal/index.html", "r", encoding="utf-8") as f:
    h = f.read()

# Simple character-level stack tracking for ALL divs
stack = []
line_starts = {}
for i, ch in enumerate(h):
    if h[i:i+4] == '<div':
        end = h.find('>', i)
        if end < 0:
            break
        tag = h[i:end+1]
        line = h[:i].count('\n') + 1
        stack.append(('OPEN', line, tag[:70]))
        i = end
    elif h[i:i+6] == '</div>':
        if stack:
            stack.pop()
        else:
            print(f"ORPHAN </div> at line {h[:i].count(chr(10))+1}")
        i += 5
    elif h[i:i+8] == '<section' and 'id=' not in h[i:i+30]:
        # Skip non-id sections
        pass

if stack:
    print("UNCLOSED DIVS (%d):" % len(stack))
    for typ, line, tag in stack:
        print(f"  Line {line}: {tag}...")
else:
    print("ALL DIVS BALANCED!")
