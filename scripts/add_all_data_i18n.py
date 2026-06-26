#!/usr/bin/env python3
"""
Comprehensively add data-i18n attributes to ALL translatable elements in the portal.
"""
import re

FPATH = 'cognitive-space/portal/index.html'
with open(FPATH, encoding='utf-8') as f:
    html = f.read()

# ─── Add data-i18n to section titles (h2.section-title) ───────────
# Pattern: <h2 class="section-title">TEXT</h2>
pairs = [
    (r'(<h2 class="section-title">)Research Questions(</h2>)', r'\1 data-i18n="section_rq">Research Questions\2'),
    (r'(<h2 class="section-title">)Research Contributions(</h2>)', r'\1 data-i18n="section_contrib">Research Contributions\2'),
    (r'(<h2 class="section-title">)Methodology(</h2>)', r'\1 data-i18n="section_method">Methodology\2'),
    (r'(<h2 class="section-title">)Findings(</h2>)', r'\1 data-i18n="section_findings">Findings\2'),
    (r'(<h2 class="section-title">)Curriculum Analysis(</h2>)', r'\1 data-i18n="section_curriculum">Curriculum Analysis\2'),
    (r'(<h2 class="section-title">)Validation(</h2>)', r'\1 data-i18n="section_validation">Validation\2'),
    (r'(<h2 class="section-title">)Limitations(</h2>)', r'\1 data-i18n="section_limitations">Limitations\2'),
    (r'(<h2 class="section-title">)Paper(</h2>)', r'\1 data-i18n="section_paper">Paper\2'),
    (r'(<h2 class="section-title">)Open Science(</h2>)', r'\1 data-i18n="section_openscience">Open Science\2'),
    (r'(<h2 class="section-title">)Interactive CognitiveSpace(</h2>)', r'\1 data-i18n="section_cognitivespace">Interactive CognitiveSpace\2'),
]
for pattern, replacement in pairs:
    html = re.sub(pattern, replacement, html)

# ─── Section subtitles (p.section-sub) ─────────────────────────────
sub_pairs = [
    ('Three complementary lenses', 'rq_sub'),
    ('What this project delivers', 'contrib_sub'),
    ('From textbook text to structural', 'method_sub'),
    ('Five structural discoveries', 'section_findings'),
    ('How four education systems align', 'curriculum_sub'),
    ('Gold standard annotations and model', 'validation_sub'),
    ('Transparent assessment of methodological', 'limitations_sub'),
    ('Preprint manuscript available', 'paper_sub'),
    ('All data, code and results are publicly', 'openscience_sub'),
    ('Explore 1,160+ concepts', 'cognitivespace_sub'),
]
for text, key in sub_pairs:
    pattern = re.escape(f'>{text}')
    html = re.sub(pattern, f' data-i18n="{key}">{text}', html, count=1)

# ─── Card titles (h3 elements) ─────────────────────────────────────
card_pairs = [
    ('RQ1: Language', 'rq1_title'),
    ('How do different languages organize the same knowledge?', 'rq1_question'),
    ('RQ2: Discipline', 'rq2_title'),
    ('How do different STEM subjects organize knowledge?', 'rq2_question'),
    ('RQ3: Education System', 'rq3_title'),
    ('How do different curricula organize the same subject?', 'rq3_question'),
    ('A multilingual STEM knowledge', 'contrib1_title'),
    ('Three structural metrics for', 'contrib2_title'),
    ('Curriculum coverage analysis', 'contrib3_title'),
    ('Empirical findings across 4', 'contrib4_title'),
    ('Knowledge density peaks early', 'finding_a_title'),
    ('Knowledge structures stay shallow', 'finding_b_title'),
    ('Languages organize knowledge differently', 'finding_c_title'),
    ('Education systems emphasize different curriculum', 'finding_d_title'),
    ('Fig 3: CDS by Education Level', 'fig3_caption'),
    ('Fig 7: Three Subject CDS', 'fig7_caption'),
    ('Fig 5: HDS Distribution', 'fig5_caption'),
    ('Fig 4: LDS Heatmap', 'fig4_caption'),
    ('NRW (Germany) — Specialization', 'curr_nrw_title'),
    ('UK — Exam-Driven Model', 'curr_uk_title'),
    ('US — Broad Standards Model', 'curr_us_title'),
    ('China — Selective Depth', 'curr_cn_title'),
    ('Three competing explanations', 'curr_explanations_title'),
]
for text, key in card_pairs:
    # Find this text inside an h3 or p element and add data-i18n
    pattern = re.escape(f'>{text}')
    replacement = f' data-i18n="{key}">{text}'
    html = re.sub(pattern, replacement, html, count=1)

# ─── Stat labels ──────────────────────────────────────────────────
stat_pairs = [
    ('Concepts', 'stat_concepts'),
    ('Relations', 'stat_relations'),
    ('Languages', 'stat_languages'),
    ('Disciplines', 'stat_disciplines'),
    ('Education Systems', 'stat_edu_systems'),
    ('Gold Labels', 'stat_gold_labels'),
    ('Overall F1', 'stat_overall_f1'),
]
for text, key in stat_pairs:
    pattern = re.escape(f'>{text}<')
    html = re.sub(pattern, f' data-i18n="{key}">{text}<', html, count=1)

# ─── Open Science cards ───────────────────────────────────────────
osc_pairs = [
    ('Full Dataset', 'openscience_dataset'),
    ('Knowledge graphs, gold labels', 'openscience_dataset_desc'),
    ('Source Code', 'openscience_code'),
    ('Complete analysis pipeline', 'openscience_code_desc'),
    ('Research Paper', 'openscience_paper'),
    ('Full manuscript with methodology', 'openscience_paper_desc'),
    ('Figures & Visualizations', 'openscience_figures'),
    ('Publication-ready charts', 'openscience_figures_desc'),
    ('Benchmark Results', 'openscience_bench'),
    ('20-model comparison', 'openscience_bench_desc'),
    ('Get in Touch', 'openscience_contact'),
    ('Questions, feedback, collaborations', 'openscience_contact_desc'),
]
for text, key in osc_pairs:
    pattern = re.escape(f'>{text}<')
    html = re.sub(pattern, f' data-i18n="{key}">{text}<', html, count=1)

# ─── Finding descriptions (p content) ──────────────────────────────
find_pairs = [
    ('Finding A — All three STEM disciplines follow', 'finding_a_sub'),
    ('Finding B — Maximum prerequisite depth', 'finding_b_sub'),
    ('Finding C — ZH–DE textbooks diverge', 'finding_c_sub'),
    ('Finding D — Coverage scores range', 'finding_d_sub'),
]
for text, key in find_pairs:
    pattern = re.escape(f'>{text}')
    replacement = f' data-i18n="{key}">{text}'
    html = re.sub(pattern, replacement, html, count=1)

# ─── Validation and Benchmark card descriptions ────────────────────
val_pairs = [
    ('Human-annotated gold standard', 'validation_gold_desc'),
    ('All free-quota Bailian API models', 'validation_bench_desc'),
]
for text, key in val_pairs:
    pattern = re.escape(f'>{text}')
    html = re.sub(pattern, f' data-i18n="{key}">{text}', html, count=1)

# ─── Curriculum card descriptions (long text blocks) ──────────────
curr_desc_pairs = [
    ('Coverage decreases with stage', 'curr_nrw_desc'),
    ('Coverage increases with stage', 'curr_uk_desc'),
    ('Stable high coverage across stages', 'curr_us_desc'),
    ('Very low but deliberate coverage', 'curr_cn_desc'),
]
for text, key in curr_desc_pairs:
    pattern = re.escape(f'>{text}')
    html = re.sub(pattern, f' data-i18n="{key}">{text}', html, count=1)

# ─── RQ answer texts ──────────────────────────────────────────────
rq_ans_pairs = [
    ('Chinese and German textbooks show the highest', 'rq1_answer'),
    ('All three disciplines follow an early-peak-later', 'rq2_answer'),
    ('Coverage scores range from 8', 'rq3_answer'),
]
for text, key in rq_ans_pairs:
    pattern = re.escape(f'>{text}')
    html = re.sub(pattern, f' data-i18n="{key}">{text}', html, count=1)

# ─── Metric labels (small text tags) ──────────────────────────────
metric_pairs = [
    ('LDS: 0.802–0.907', 'rq1_metric'),
    ('CDS: 0.042–0.271', 'rq2_cds'),
    ('HDS: max 8', 'rq2_hds'),
    ('CS: 8%–82%', 'rq3_cs'),
]
for text, key in metric_pairs:
    pattern = re.escape(f'>{text}<')
    html = re.sub(pattern, f' data-i18n="{key}">{text}<', html, count=1)

# ─── Footer links ────────────────────────────────────────────────
footer_pairs = [
    ('>GitHub<', 'footer_github', '>GitHub<'),
]
for text, key, _ in footer_pairs:
    pattern = re.escape(text)
    html = re.sub(pattern, f' data-i18n="{key}"{text[1:]}', html, count=1)

# ─── Nav CSS fix for desktop overflow ─────────────────────────────
# The existing nav CSS should handle desktop too. Let me check.
# Actually, on desktop with ~10 nav links + brand + 3 lang buttons,
# we need about 700px+ just for the nav items.
# Let me add a more aggressive overflow fix.

old_nav_end = """nav a.active { color: var(--accent); background: rgba(96,165,250,.12); }
.lang-btn { padding: 3px 7px; font-size: .65rem; }
@media (max-width: 900px) {
  nav { gap: 1px; padding: 0 8px; }
  nav .brand { font-size: .85rem; margin-right: 6px; }
  nav a { font-size: .65rem; padding: 3px 4px; }
  .lang-btn { padding: 2px 5px; font-size: .6rem; }
}"""

new_nav_end = """nav a.active { color: var(--accent); background: rgba(96,165,250,.12); }
.lang-btn { padding: 3px 7px; font-size: .65rem; flex-shrink: 0; }
@media (max-width: 1100px) {
  nav { gap: 1px; padding: 0 6px; }
  nav .brand { font-size: .8rem; margin-right: 4px; }
  nav a { font-size: .6rem; padding: 3px 4px; }
  .lang-btn { padding: 2px 5px; font-size: .55rem; }
}
@media (max-width: 900px) {
  nav .brand { font-size: .75rem; margin-right: 3px; }
  nav a { font-size: .55rem; padding: 2px 3px; }
  .lang-btn { padding: 1px 4px; font-size: .5rem; }
}"""
html = html.replace(old_nav_end, new_nav_end)

# ─── Save ──────────────────────────────────────────────────────────
with open(FPATH, 'w', encoding='utf-8') as f:
    f.write(html)

count = html.count('data-i18n=')
print(f'data-i18n count: {count}')
print('Done!')
