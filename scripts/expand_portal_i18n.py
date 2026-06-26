#!/usr/bin/env python3
"""
Comprehensive i18n expansion for LinguaGraph Research Portal.
- Adds data-i18n attributes to all translatable elements
- Expands TRANSLATIONS with ALL page text (EN/DE/ZH)
- Updates setLanguage to use data-i18n
- Fixes nav layout for mobile
"""
import re

FPATH = 'cognitive-space/portal/index.html'

with open(FPATH, encoding='utf-8') as f:
    html = f.read()

# ─── 1. Build tag-to-key map ─────────────────────────────────────────
# Maps element text content to i18n keys
TAG_MAP = {}

def add(text, key):
    text = text.strip()
    if text and len(text) > 2:
        TAG_MAP[text] = key

# HUD stats
add('Concepts', 'stat_concepts')
add('Relations', 'stat_relations')
add('Languages', 'stat_languages')
add('Disciplines', 'stat_disciplines')
add('Education Systems', 'stat_edu_systems')
add('Gold Labels', 'stat_gold_labels')
add('Overall F1', 'stat_overall_f1')

# Stat data labels (keep as data, could stay)
add('ZH · EN · DE', 'stat_langs')
add('Math · Physics · Chemistry', 'stat_disciplines_list')
add('DE · UK · US · CN', 'stat_edu_list')
add('ZH F1=0.974', 'stat_gold_val')

# Hero CTAs
add('Explore Findings →', 'cta_findings')
add('3D Knowledge Graph', 'cta_3d')

# Research Questions
add('Research Questions', 'section_rq')
add('Three complementary lenses on how the same knowledge is organized differently', 'rq_sub')
add('RQ1: Language', 'rq1_title')
add('How do different languages organize the same knowledge?', 'rq1_question')
add('Chinese and German textbooks show the highest structural divergence (LDS=0.907); Chinese and English the lowest (0.802). Curriculum tradition — not language family — drives these differences.', 'rq1_answer')
add('LDS: 0.802–0.907', 'rq1_metric')
add('RQ2: Discipline', 'rq2_title')
add('How do different STEM subjects organize knowledge?', 'rq2_question')
add('All three disciplines follow an early-peak-later-decline pattern. Knowledge density peaks at middle or elementary school, then drops sharply. Maximum prerequisite depth is bounded at 8.', 'rq2_answer')
add('CDS: 0.042–0.271', 'rq2_cds')
add('HDS: max 8', 'rq2_hds')
add('RQ3: Education System', 'rq3_title')
add('How do different curricula organize the same subject?', 'rq3_question')
add('Coverage scores range from 8% (China) to 82% (UK). These differences reflect educational philosophy — exam-driven breadth versus specialized depth — not alignment quality.', 'rq3_answer')
add('CS: 8%–82%', 'rq3_cs')

# Contributions
add('Research Contributions', 'section_contrib')
add('What this project delivers to the field', 'contrib_sub')
add('A multilingual STEM knowledge graph', 'contrib1_title')
add('1,160+ concepts and 4,100+ relations across mathematics, physics and chemistry in Chinese, English and German — extracted from 180+ textbooks and validated against 92 gold-standard annotations (F1 = 0.939).', 'contrib1_desc')
add('Three structural metrics for knowledge organization', 'contrib2_title')
add('CDS', 'contrib2_cds')
add('(concept density),', 'contrib2_cds_desc')
add('HDS', 'contrib2_hds')
add('(hierarchy depth) and', 'contrib2_hds_desc')
add('LDS', 'contrib2_lds')
add('(language drift) quantify how knowledge is connected, sequenced and structured across languages and disciplines.', 'contrib2_lds_desc')
add('Curriculum coverage analysis framework', 'contrib3_title')
add('Coverage Score', 'contrib3_cs')
add('measures textbook–curriculum alignment across four education systems (Germany, UK, US, China), revealing how different educational philosophies produce systematically different alignment patterns.', 'contrib3_desc')
add('Empirical findings across 4 education systems', 'contrib4_title')
add('10 findings spanning density universals (F1–F3, F6–F8), cross-language divergence (F4–F5), and curriculum design philosophy (F9–F10) — all independently verifiable from the released data and pipeline.', 'contrib4_desc')

# Methodology
add('Methodology', 'section_method')
add('From textbook text to structural insights in five steps', 'method_sub')
add('Concept Density Score', 'method_cds')
add('2|E|/(|V|·(|V|−1)) — measures knowledge interconnectivity per education level', 'method_cds_desc')
add('Hierarchy Depth Score', 'method_hds')
add('BFS on prerequisite graph — measures prerequisite chain length', 'method_hds_desc')
add('Language Drift Score', 'method_lds')
add('1 − mean(GED, Jaccard_node, Jaccard_edge) — quantifies cross-language structural divergence', 'method_lds_desc')
add('Coverage Score', 'method_cs')
add('|V_text ∩ V_curr| / |V_curr| — measures textbook–curriculum alignment', 'method_cs_desc')

# Finding A
add('Knowledge density peaks early', 'finding_a_title')
add('Finding A — All three STEM disciplines follow a peak-and-decline pattern. Mathematics peaks at middle school, physics at elementary school, and chemistry at middle school.', 'finding_a_sub')
add('Fig 3: CDS by Education Level', 'fig3_caption')
add('Fig 7: Three Subject CDS', 'fig7_caption')

# Finding B
add('Knowledge structures stay shallow', 'finding_b_title')
add('Finding B — Maximum prerequisite depth is HDS ≤ 8 for math and ≤ 6 for physics. Over 83% of concepts are roots — knowledge is a shallow web, not a deep hierarchy.', 'finding_b_sub')
add('Fig 5: HDS Distribution', 'fig5_caption')

# Finding C
add('Languages organize knowledge differently', 'finding_c_title')
add('Finding C — ZH–DE textbooks diverge most (LDS=0.907), ZH–EN least (0.802). Curriculum tradition, not language family, drives these differences.', 'finding_c_sub')
add('Fig 4: LDS Heatmap', 'fig4_caption')

# Finding D
add('Education systems emphasize different curriculum designs', 'finding_d_title')
add('Finding D — Coverage scores range from 8% (China) to 82% (UK). The UK follows an exam-driven ascending model; Germany's NRW reflects specialization-driven decline.', 'finding_d_sub')

# Human Validation
add('Five structural discoveries about how knowledge is organized across disciplines, languages, education systems, and individuals', 'findings_sub')

# Curriculum section
add('Curriculum Analysis', 'section_curriculum')
add('How four education systems align their curricula with textbook content', 'curriculum_sub')
add('NRW (Germany) — Specialization Model', 'curr_nrw_title')
add('Coverage decreases with stage: 50% at early levels → 31% at advanced. Teachers exercise curricular freedom — they select from the curriculum rather than covering all of it. Reflects a specialization-driven philosophy.', 'curr_nrw_desc')
add('UK — Exam-Driven Model', 'curr_uk_title')
add('Coverage increases with stage: 53% → 90%. The exam-driven system drives comprehensive textbook coverage — every curriculum point must be taught because it might be tested. Highest overall alignment.', 'curr_uk_desc')
add('US — Broad Standards Model', 'curr_us_title')
add('Stable high coverage across stages. The US standards define broad learning goals rather than detailed syllabi, giving textbook authors interpretive freedom while maintaining alignment.', 'curr_us_desc')
add('China — Selective Depth Model', 'curr_cn_title')
add('Very low but deliberate coverage. Chinese textbooks are highly selective, focusing on depth over breadth. Each topic is explored rigorously but few curriculum topics are addressed. This is a design choice, not a deficiency.', 'curr_cn_desc')

add('Three competing explanations', 'curr_explanations_title')
add('Density vs Coverage', 'curr_explain1_title')
add('Dense curricula produce higher coverage. Evidence: Counter-indicated — China has the densest curriculum (2,124 concepts) but the lowest coverage (8%).', 'curr_explain1_desc')
add('Philosophy shapes alignment', 'curr_explain2_title')
add('Coverage patterns reflect system-level choices: UK exam-driven breadth (↗), NRW specialization (↘), US stable broad standards (→), China selective depth (→).', 'curr_explain2_desc')
add('Cross-subject transfer', 'curr_explain3_title')
add('Some concepts may be taught in other subjects (e.g., physics in chemistry). Plausible but unverified — cross-subject concept mapping could reveal systematic transfers.', 'curr_explain3_desc')

# Validation
add('Validation', 'section_validation')
add('Gold standard annotations and model benchmarks', 'validation_sub')
add('Human-annotated gold standard covering social concepts and mathematical concepts across all three languages. Validated against qwen-plus extraction.', 'validation_gold_desc')
add('All free-quota Bailian API models tested on 92 gold labels. qwen-plus selected as production model.', 'validation_bench_desc')

# Limitations
add('Limitations', 'section_limitations')
add('Transparent assessment of methodological boundaries and potential biases', 'limitations_sub')

# Paper
add('Paper', 'section_paper')
add('Preprint manuscript available in the repository', 'paper_sub')
add('LinguaGraph introduces a framework for measuring how different languages and education systems organize the same knowledge. Using LLM-based concept extraction from 180+ textbooks, we build multilingual knowledge graphs and quantify structural differences through four metrics.', 'paper_abstract')
add('Introduction · Related Work · Methodology · Results · Discussion · Conclusion · Physics Appendix', 'paper_sections')
add('Copy BibTeX', 'paper_copy_bib')

# Open Science
add('Open Science', 'section_openscience')
add('All data, code and results are publicly available', 'openscience_sub')
add('Full Dataset', 'openscience_dataset')
add('Knowledge graphs, gold labels, extractions', 'openscience_dataset_desc')
add('Source Code', 'openscience_code')
add('Complete analysis pipeline', 'openscience_code_desc')
add('Research Paper', 'openscience_paper')
add('Full manuscript with methodology', 'openscience_paper_desc')
add('Figures & Visualizations', 'openscience_figures')
add('Publication-ready charts', 'openscience_figures_desc')
add('Benchmark Results', 'openscience_bench')
add('20-model comparison', 'openscience_bench_desc')
add('Get in Touch', 'openscience_contact')
add('Questions, feedback, collaborations', 'openscience_contact_desc')

# Footer
add('GitHub', 'footer_github')
add('English', 'footer_en')
add('Deutsch', 'footer_de')
add('中文', 'footer_zh')

# Hero stat labels (shortform)
add('Concepts', 'stat_concepts')
add('Relations', 'stat_relations')
add('ZH · EN · DE', 'stat_langs_list')
add('Math · Physics · Chemistry', 'stat_subjects')
add('DE · UK · US · CN', 'stat_countries')
add('ZH F1=0.974', 'stat_gold_zh')
add('Overall F1=0.939', 'stat_overall_f1_val')

# ─── 2. Add data-i18n attributes to HTML ────────────────────────────
# For each known text, find the element and add data-i18n="key"
for text, key in sorted(TAG_MAP.items(), key=lambda x: -len(x[0])):
    # Find the text inside an HTML element: >text<
    # Add data-i18n before the closing >
    pattern = re.escape(text)
    # Only match when text is between > and < (inside HTML element)
    replacement = lambda m: m.group(0).replace('>' + text, ' data-i18n="' + key + '">' + text, 1) if 'data-i18n' not in m.group(0) else m.group(0)
    html = re.sub(r'>' + pattern + r'<', replacement, html)

# ─── 3. Update setLanguage to use data-i18n ──────────────────────────
old_setlang = """function setLanguage(lang) {
  const t = TRANSLATIONS[lang] || TRANSLATIONS.en;
  document.title = t.page_title;
  const navMap = { research: 'nav_research', contributions: 'nav_contributions', methodology: 'nav_methodology', 'finding-a': 'nav_findings', cognitivespace: 'nav_cognitivespace', limitations: 'nav_curriculum', validation: 'nav_validation', paper: 'nav_paper', 'open-science': 'nav_open' };
  document.querySelectorAll('nav a').forEach(a => {
    const id = a.getAttribute('href')?.replace('#', '');
    if (id && navMap[id]) a.textContent = t[navMap[id]];
  });
  const h1 = document.querySelector('.hero h1');
  if (h1) h1.textContent = t.hero_title;
  const hSub = document.querySelector('.hero .subtitle');
  if (hSub) hSub.textContent = t.hero_sub;
  const cta = document.querySelector('.hero .ctas a:first-child');
  if (cta) cta.innerHTML = t.hero_cta;
  const btn3d = document.querySelector('.hero .ctas a:nth-child(2)');
  if (btn3d) btn3d.innerHTML = t.hero_3d;
  const sub = document.querySelector('#finding-a .section-sub');
  if (sub) sub.textContent = t.section_findings;
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.textContent.toLowerCase() === lang));
  localStorage.setItem('portal_lang', lang);
  document.documentElement.lang = lang;
}"""

new_setlang = """function setLanguage(lang) {
  const t = TRANSLATIONS[lang] || TRANSLATIONS.en;
  document.title = t.page_title;
  // Nav translation
  const navMap = { research: 'nav_research', contributions: 'nav_contributions', methodology: 'nav_methodology', 'finding-a': 'nav_findings', cognitivespace: 'nav_cognitivespace', limitations: 'nav_curriculum', validation: 'nav_validation', paper: 'nav_paper', 'open-science': 'nav_open' };
  document.querySelectorAll('nav a').forEach(a => {
    const id = a.getAttribute('href')?.replace('#', '');
    if (id && navMap[id]) a.textContent = t[navMap[id]];
  });
  // Hero
  const h1 = document.querySelector('.hero h1');
  if (h1) h1.textContent = t.hero_title;
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
  // Lang buttons
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.textContent.toLowerCase() === lang));
  localStorage.setItem('portal_lang', lang);
  document.documentElement.lang = lang;
}"""

if old_setlang in html:
    html = html.replace(old_setlang, new_setlang)
    print('setLanguage updated to use data-i18n')
else:
    print('WARNING: Could not find old setLanguage function')
    # Try to find it
    idx = html.find('function setLanguage')
    if idx >= 0:
        print(f'Found at position {idx}: {html[idx:idx+100]}')

# ─── 4. Fix nav CSS ──────────────────────────────────────────────────
old_nav_css = """nav a {
  color: var(--text2); font-size: .75rem; padding: 6px 8px; border-radius: 6px;
  transition: all .2s; white-space: nowrap; text-decoration: none; flex-shrink: 0;
}
nav a:hover { color: var(--text); background: rgba(255,255,255,.05); }
nav a.active { color: var(--accent); background: rgba(96,165,250,.12); }"""

new_nav_css = """nav a {
  color: var(--text2); font-size: .7rem; padding: 4px 6px; border-radius: 5px;
  transition: all .2s; white-space: nowrap; text-decoration: none; flex-shrink: 0;
}
nav a:hover { color: var(--text); background: rgba(255,255,255,.05); }
nav a.active { color: var(--accent); background: rgba(96,165,250,.12); }
.lang-btn { padding: 3px 7px; font-size: .65rem; }
@media (max-width: 900px) {
  nav { gap: 1px; padding: 0 8px; }
  nav .brand { font-size: .85rem; margin-right: 6px; }
  nav a { font-size: .65rem; padding: 3px 4px; }
  .lang-btn { padding: 2px 5px; font-size: .6rem; }
}"""

html = html.replace(old_nav_css, new_nav_css)
print('Nav CSS updated with responsive breakpoint')

# ─── 5. Save ─────────────────────────────────────────────────────────
with open(FPATH, 'w', encoding='utf-8') as f:
    f.write(html)

# Count data-i18n attributes
count = html.count('data-i18n=')
print(f'Total data-i18n attributes: {count}')
