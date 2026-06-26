import re
with open("cognitive-space/portal/index.html", "r", encoding="utf-8") as f:
    h = f.read()

# Find all finding-card divs and see if they have matching closes
stack = []
for i, ch in enumerate(h):
    if ch != '<':
        continue
    end = h.find('>', i)
    if end < 0:
        break
    tag = h[i:end+1]

    if tag.startswith('</div'):
        if stack:
            stack.pop()
    elif tag.startswith('<div class="finding-card"'):
        stack.append(('DIV', i, tag[:60]))

if stack:
    print("UNCLOSED DIVS:", len(stack))
    for typ, pos, tag in stack:
        line = h[:pos].count('\n') + 1
        print(f"  Line {line}: {tag}...")
else:
    print("All finding-cards closed properly")

# Also check </section> before each <section id="finding-"
for find_id in ['finding-b', 'finding-c', 'finding-d', 'finding-e']:
    sec_idx = h.find('id="' + find_id + '"')
    if sec_idx > 0:
        # Find the preceding </section>
        before = h[:sec_idx]
        last_close = before.rfind('</section>')
        last_div_close = before.rfind('</div>')
        ctx = before[last_close:last_close+30].replace('\n', ' ')
        ctx_div = before[last_div_close:last_div_close+30].replace('\n', ' ')
        line_num = before[:last_close].count('\n') + 1
        print(f"  Before #{find_id}: </section> at ~line {line_num}: ...{ctx}...")
        line_div = before[:last_div_close].count('\n') + 1
        print(f"             </div> at ~line {line_div}: ...{ctx_div}...")
