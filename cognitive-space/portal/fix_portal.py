import re, sys

with open('cognitive-space/portal/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

fixes = []

# Fix 1: ../../docs/ paths
html = html.replace('"../../docs/paper/', '"docs/paper/')
html = html.replace('"../../README.md"', '"README.md"')
html = html.replace('"../../README_DE.md"', '"README_DE.md"')
html = html.replace('"../../README_ZH.md"', '"README_ZH.md"')
fixes.append('Fixed ../../docs/ paths')

# Fix 2: Contributions mobile margin
html = html.replace(
    'style="background:var(--surface);border-radius:24px;margin:0 24px;padding:80px 48px;max-width:1120px"',
    'style="background:var(--surface);border-radius:24px;padding:80px 24px"'
)
fixes.append('Fixed contributions mobile margin')

# Fix 3: Placeholder email
html = html.replace(
    'href="mailto:your-email@example.com"',
    'href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/issues" target="_blank"'
)
html = html.replace(
    'Questions, collaboration, or feedback? Reach out via GitHub or email.',
    'Questions, collaboration, or feedback? Open an issue on GitHub.'
)
html = html.replace(
    '<div class="meta">\U0001f426 BWKI 2026</div>',
    '<div class="meta">GitHub Issues</div>'
)
fixes.append('Fixed placeholder email')

# Fix 4: Split findings into individual sections with proper IDs
# Pattern: close section after finding-a intro, then wrap each finding card in its own section
old = (
    '<!-- FINDING A: CDS -->\n'
    '<section id="finding-a" class="fade-in">\n'
    '  <h2 class="section-title">Findings</h2>\n'
    '  <p class="section-sub">Four structural discoveries</p>\n'
    '\n'
    '  <div class="finding-card" style="border-left:4px solid var(--accent)">'
)
new = (
    '<!-- FINDINGS OVERVIEW -->\n'
    '<section id="finding-a" class="fade-in">\n'
    '  <h2 class="section-title">Findings</h2>\n'
    '  <p class="section-sub">Four structural discoveries</p>\n'
    '</section>\n'
    '\n'
    '<!-- FINDING A: CDS -->\n'
    '<section id="finding-a-content" class="fade-in">\n'
    '  <div class="finding-card" style="border-left:4px solid var(--accent)">'
)

# This is tricky with the emoji characters. Let me use a simpler approach.
# Find the closing tag of the findings section before "FINDING B" marker

# Find the exact boundary markers
fb_marker = 'FINDING B: HDS'
fc_marker = 'FINDING C: LDS'
fd_marker = 'FINDING D: COVERAGE'
end_marker = '</section><!-- COGNITIVESPACE'

# Replace section boundaries: close after finding-a intro header
# Open new section for each finding

# Split the findings block
idx_a_end = html.find('  <div class="finding-card" style="border-left:4px solid var(--accent)">')
idx_b = html.find(fb_marker)
idx_c = html.find(fc_marker)
idx_d = html.find(fd_marker)
idx_end = html.find('<section id="cognitivespace"')

if idx_a_end > 0 and idx_b > 0 and idx_c > 0 and idx_d > 0 and idx_end > 0:
    # After finding-a intro (the h2 + p), close the section
    # Find the </p> after the section-sub
    section_sub_end = html.rfind('</p>', 0, idx_a_end)
    # Close the section after the intro
    before_intro = html[:section_sub_end+4]
    after_intro = html[section_sub_end+4:]

    # Add section close + new section open after intro
    after_intro = '</section>\n\n' + after_intro

    # For each finding card div, wrap it in a section
    # Find the <div class="finding-card" for finding A — add section open
    div_a = after_intro.find('<div class="finding-card" style="border-left:4px solid var(--accent)">')
    if div_a >= 0:
        after_intro = after_intro[:div_a] + '<section id="finding-a-content" class="fade-in">\n' + after_intro[div_a:]
        # Find closing div of finding A and add section close
        close_a = after_intro.find('</div>', div_a)
        # Find the next </div> that ends finding A card (look for 3rd </div> after close_a)
        close_a2 = after_intro.find('</div>', close_a + 6)
        close_a3 = after_intro.find('</div>', close_a2 + 6)
        # The meta div closing is the end of the card
        after_intro = after_intro[:close_a3+6] + '\n</section>\n' + after_intro[close_a3+6:]

    # Wrap finding B in section
    div_b = after_intro.find('<div class="finding-card" style="border-left:4px solid var(--green)">')
    if div_b >= 0:
        after_intro = after_intro[:div_b] + '<section id="finding-b" class="fade-in">\n' + after_intro[div_b:]
        close_b = after_intro.find('</div>', after_intro.find('</div>', after_intro.find('</div>', div_b) + 6) + 6)
        after_intro = after_intro[:close_b+6] + '\n</section>\n' + after_intro[close_b+6:]

    # Wrap finding C in section
    div_c = after_intro.find('<div class="finding-card" style="border-left:4px solid #22d3ee">')
    if div_c >= 0:
        after_intro = after_intro[:div_c] + '<section id="finding-c" class="fade-in">\n' + after_intro[div_c:]
        close_c = after_intro.find('</div>', after_intro.find('</div>', after_intro.find('</div>', div_c) + 6) + 6)
        after_intro = after_intro[:close_c+6] + '\n</section>\n' + after_intro[close_c+6:]

    # Wrap finding D in section
    div_d = after_intro.find('<div class="finding-card" style="border-left:4px solid var(--yellow)">')
    if div_d >= 0:
        after_intro = after_intro[:div_d] + '<section id="finding-d" class="fade-in">\n' + after_intro[div_d:]
        close_d = after_intro.find('</div>', after_intro.find('</div>', after_intro.find('</div>', div_d) + 6) + 6)
        after_intro = after_intro[:close_d+6] + '\n</section>\n' + after_intro[close_d+6:]

    html = before_intro + after_intro
    fixes.append('Split findings into individual sections')
else:
    fixes.append('SKIPPED findings split (pattern not matched)')

# Verify
with open('cognitive-space/portal/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Applied {len(fixes)} fixes:')
for f in fixes:
    print(f'  - {f}')
print(f'File size: {len(html)} bytes')
