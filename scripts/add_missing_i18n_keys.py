#!/usr/bin/env python3
"""Add missing translation keys to portal TRANSLATIONS"""
FPATH = 'cognitive-space/portal/index.html'
with open(FPATH, encoding='utf-8') as f:
    html = f.read()

DE_OLD = "contrib1_desc: '1.160+ Konzepte und 4.100+ Beziehungen in Mathematik, Physik und Chemie auf Chinesisch, Englisch und Deutsch — extrahiert aus 180+ Lehrbuechern und validiert mit 92 Goldstandard-Annotationen (F1 = 0,939).'"
DE_NEW = DE_OLD + ",\n    contrib2_title: 'Drei strukturelle Metriken zur Wissensorganisation',\n    contrib3_title: 'Curriculum-Coverage-Analyse-Framework',\n    contrib4_title: 'Empirische Ergebnisse aus 4 Bildungssystemen'"
# Use unicode escapes for special chars
DE_OLD_ESC = DE_OLD.replace('—', '—').replace('ü', 'ü')
html = html.replace(DE_OLD_ESC, DE_NEW)

ZH_OLD = "contrib1_desc: '1,160+ 个概念和 4,100+ 条关系，涵盖数学、物理和化学三种语言——从 180+ 本教材中提取，经 92 个黄金标准标注验证（F1 = 0.939）.'"
ZH_NEW = ZH_OLD + ",\n    contrib2_title: '知识组织的三个结构化指标',\n    contrib3_title: '课程覆盖率分析框架',\n    contrib4_title: '跨4个教育体系的实证发现'"
html = html.replace(ZH_OLD, ZH_NEW)

# DE finding_e
DE_F_OLD = "finding_d_sub: 'Erkenntnis D — Abdeckungswerte reichen von 8% (China) bis 82% (GB). Großbritannien folgt einem prüfungsgetriebenen aufsteigenden Modell; NRW spiegelt spezialisierungsbedingten Rückgang wider.'"
if 'finding_e_title' not in html[html.find('de:'):html.find('zh:')]:
    DE_F_NEW = DE_F_OLD + ",\n    finding_e_title: 'Humanvalidierung bestätigt sprachbedingte kognitive Divergenz',\n    finding_e_sub: 'Erkenntnis E — Echte Probanden zeigen dasselbe sprachübergreifende Muster wie aggregierte Korpora, jedoch mit geringerer Magnitude.'"
    html = html.replace(DE_F_OLD, DE_F_NEW)

# ZH finding_e
ZH_F_OLD = "finding_d_sub: '发现 D — 覆盖率从 8%（中国）到 82%（英国）。英国采用考试驱动的上升模式；德国北威州体现专业化驱动的下降模式。'"
if 'finding_e_title' not in html[html.find('zh:'):]:
    ZH_F_NEW = ZH_F_OLD + ",\n    finding_e_title: '人类验证证实语言驱动的认知差异',\n    finding_e_sub: '发现 E — 真实参与者展现出与聚合语料库相同的跨语言模式，但幅度更小。'"
    html = html.replace(ZH_F_OLD, ZH_F_NEW)

# EN finding_e
EN_F_OLD = "finding_d_sub: 'Finding D — Coverage scores range from 8% (China) to 82% (UK). The UK follows an exam-driven ascending model; Germany NRW reflects specialization-driven decline.'"
if 'finding_e_title' not in html[html.find('en:'):html.find('de:')]:
    EN_F_NEW = EN_F_OLD + ",\n    finding_e_title: 'Human validation confirms language-driven cognitive divergence',\n    finding_e_sub: 'Finding E — Real participants show the same cross-language pattern as aggregated corpora — but with smaller magnitude, confirming education amplifies language-specific organization.'"
    html = html.replace(EN_F_OLD, EN_F_NEW)

with open(FPATH, 'w', encoding='utf-8') as f:
    f.write(html)

print('Missing keys added')
