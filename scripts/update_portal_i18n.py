#!/usr/bin/env python3
"""Replace TRANSLATIONS and update setLanguage in portal"""
with open('cognitive-space/portal/index.html', encoding='utf-8') as f:
    html = f.read()

start = html.find('const TRANSLATIONS = {')
# Find the closing }; by matching braces
depth = 0
end = start
for i in range(start, len(html)):
    if html[i] == '{': depth += 1
    elif html[i] == '}': depth -= 1
    if depth == 0 and html[i] == ';':
        end = i + 1
        break

print(f'Found TRANSLATIONS at {start}-{end}')

# Read new translations from external file
with open('scripts/portal_translations.js', encoding='utf-8') as f:
    new_trans = f.read()

html = html[:start] + new_trans + html[end:]

# Update setLanguage
old_fn_start = html.find('function setLanguage')
fn_end = html.find('function initLang', old_fn_start)

new_setlang = """function setLanguage(lang) {
  const t = TRANSLATIONS[lang] || TRANSLATIONS.en;
  document.title = t.page_title;
  const navMap = { research: 'nav_research', contributions: 'nav_contributions', methodology: 'nav_methodology', 'finding-a': 'nav_findings', cognitivespace: 'nav_cognitivespace', limitations: 'nav_curriculum', validation: 'nav_validation', paper: 'nav_paper', 'open-science': 'nav_open' };
  document.querySelectorAll('nav a').forEach(a => {
    const id = a.getAttribute('href')?.replace('#', '');
    if (id && navMap[id]) a.textContent = t[navMap[id]];
  });
  // Hero
  const h1 = document.querySelector('.hero h1');
  if (h1) h1.innerHTML = t.hero_title;
  const hSub = document.querySelector('.hero .subtitle');
  if (hSub) hSub.textContent = t.hero_sub;
  const cta = document.querySelector('.hero .ctas a:first-child');
  if (cta) cta.innerHTML = t.cta_findings;
  const btn3d = document.querySelector('.hero .ctas a:nth-child(2)');
  if (btn3d) btn3d.innerHTML = t.cta_3d;
  // All data-i18n elements
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key]) el.textContent = t[key];
  });
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.textContent.toLowerCase() === lang));
  localStorage.setItem('portal_lang', lang);
  document.documentElement.lang = lang;
}"""

html = html[:old_fn_start] + new_setlang + html[fn_end:]

with open('cognitive-space/portal/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

count = html.count('data-i18n=')
print(f'setLanguage updated, data-i18n count: {count}')
