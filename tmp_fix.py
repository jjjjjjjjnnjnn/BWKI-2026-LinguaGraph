import re, sys

with open('cognitive-space/portal/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find all Chart.new calls
for m in re.finditer(r"new Chart\(document\.getElementById\('(\w+)'\)", c):
    name = m.group(1)
    start = m.end()
    opts_start = c.find('options: {', start)
    if opts_start > 0:
        snippet = c[opts_start:opts_start+300]
        print(f'--- {name} ---')
        print(snippet[:250])
        print()
