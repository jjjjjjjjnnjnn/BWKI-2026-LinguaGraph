import re

# Read EN README
with open('README.md', 'r', encoding='utf-8') as f:
    en = f.read()

# Use regex to find ALL section headings (## ...) regardless of emoji
headings = re.findall(r'^## .+$', en, re.MULTILINE)

# Generate DE and ZH by replacing headings first, then body phrases
for lang_code, output_file, heading_map, body_map in [
    ('DE', 'README_DE.md', {
        '## ': '## ',
    }, {
        # These must match exact substrings in the EN text
        'How do different languages and educational systems organize the same knowledge?': 'Wie organisieren verschiedene Sprachen und Bildungssysteme das gleiche Wissen?',
        'A cross-lingual analysis of mathematics, physics and chemistry': 'Eine sprachubergreifende Analyse von Mathematik-, Physik- und Chemie-Lehrbuchern',
        'across China, Germany, the United Kingdom and the United States': 'aus China, Deutschland, Grovbritannien und den USA',
        'measured through structural graph metrics and curriculum alignment': 'gemessen anhand struktureller Graphmetriken und Lehrplanabgleich',
        'Story Dashboard': 'Dashboard',
        'Research Portal': 'Forschungsportal',
        'Explore Findings': 'Erkenntnisse entdecken',
        '3D Knowledge Graph': '3D-Wissensgraph',
        'Research Questions': 'Forschungsfragen',
        'Interactive 3D': 'Interaktives 3D',
        'ZH F1': 'ZH F1',
        'DE F1': 'DE F1',
        'EN F1': 'EN F1',
        'Overall': 'Gesamt',
        'Concepts': 'Konzepte',
        'Relations': 'Beziehungen',
        'Languages': 'Sprachen',
        'Disciplines': 'Disziplinen',
        'Education Systems': 'Bildungssysteme',
        'Gold Labels': 'Gold-Standard',
        'Overall F1': 'Gesamt-F1',
        'Social concepts': 'Soziale Konzepte',
        'Mathematics': 'Mathematik',
        'Total': 'Gesamt',
        'Domain': 'Bereich',
        'Model': 'Modell',
        'Speed': 'Geschwindigkeit',
        'Full results': 'Vollstandige Ergebnisse',
        'Error analysis': 'Fehleranalyse',
        'Subject': 'Fach',
        'Textbooks': 'Lehrbucher',
        'Curriculum Coverage': 'Lehrplanabdeckung',
        'Metric': 'Metrik',
        'Full Name': 'Bezeichnung',
        'Formula': 'Formel',
        'What It Reveals': 'Bedeutung',
        'Finding': 'Erkenntnis',
        'Evidence': 'Beleg',
        'Impact': 'Auswirkung',
        'Production model': 'Produktionsmodell',
        'Best free': 'Bestes kostenloses',
        'Best non-Qwen': 'Bestes nicht-Qwen',
        'pip install openai numpy': 'pip install openai numpy',
        'export BAILIAN_API_KEY': 'export BAILIAN_API_KEY',
        'Test any model': 'Beliebiges Modell testen',
        'Citation': 'Zitationshinweis',
        'Quick Start': 'Schnellstart',
        'Self hosten': 'Selbst hosten',
        'Project Structure': 'Projektstruktur',
        'Model Benchmark': 'Modellvergleich',
        'Table of Contents': 'Inhaltsverzeichnis',
        'Why LinguaGraph': 'Warum LinguaGraph',
        'Metrics at a Glance': 'Metriken im Uberblick',
        'Dataset': 'Datensatz',
        'Extraction Validation': 'Validierung der Extraktion',
        'References': 'Literaturverzeichnis',
        'License': 'Lizenz',
        'Compliance': 'Compliance',
        'Contact': 'Kontakt',
        'Deploy Your Own': 'Selbst hosten',
        '10 Findings': '10 Erkenntnisse',
        'All Rights Reserved': 'Alle Rechte vorbehalten',
        'BWKI 2026': 'BWKI 2026',
    }),
    ('ZH', 'README_ZH.md', {
        '## ': '## ',
    }, {
        'How do different languages and educational systems organize the same knowledge?': '不同语言和教育体系是如何组织同一种知识的？',
        'A cross-lingual analysis of mathematics, physics and chemistry': '跨语言数学、物理和化学教材分析',
        'across China, Germany, the United Kingdom and the United States': '跨越中国、德国、英国和美国',
        'measured through structural graph metrics and curriculum alignment': '通过结构性图指标和课程对齐来量化',
        'Story Dashboard': '故事面板',
        'Research Portal': '研究门户',
        'Explore Findings': '探索发现',
        '3D Knowledge Graph': '3D 知识图谱',
        'Research Questions': '研究问题',
        'Interactive 3D': '交互式 3D',
        'ZH F1': '中文 F1',
        'DE F1': '德文 F1',
        'EN F1': '英文 F1',
        'Overall': '总体',
        'Concepts': '概念',
        'Relations': '关系',
        'Languages': '语言',
        'Disciplines': '学科',
        'Education Systems': '教育体系',
        'Gold Labels': '黄金标注',
        'Overall F1': '总体 F1',
        'Social concepts': '社会概念',
        'Mathematics': '数学',
        'Total': '总计',
        'Domain': '领域',
        'Model': '模型',
        'Speed': '速度',
        'Full results': '完整结果',
        'Error analysis': '误差分析',
        'Subject': '学科',
        'Textbooks': '教材',
        'Curriculum Coverage': '课程覆盖率',
        'Metric': '指标',
        'Full Name': '全称',
        'Formula': '公式',
        'What It Reveals': '含义',
        'Finding': '发现',
        'Evidence': '证据',
        'Impact': '影响',
        'Production model': '生产模型',
        'Best free': '最佳免费',
        'Best non-Qwen': '最佳非 Qwen',
        'pip install openai numpy': 'pip install openai numpy',
        'export BAILIAN_API_KEY': 'export BAILIAN_API_KEY',
        'Test any model': '测试任意模型',
        'Citation': '引用说明',
        'Quick Start': '快速开始',
        'Self hosten': '自行部署',
        'Project Structure': '项目结构',
        'Model Benchmark': '模型基准测试',
        'Table of Contents': '目录',
        'Why LinguaGraph': '为什么需要 LinguaGraph',
        'Metrics at a Glance': '核心指标一览',
        'Dataset': '数据集',
        'Extraction Validation': '提取质量验证',
        'References': '参考文献',
        'License': '许可',
        'Compliance': '合规',
        'Contact': '联系方式',
        'Deploy Your Own': '自行部署',
        '10 Findings': '10 项发现',
        'All Rights Reserved': '保留所有权利',
        'BWKI 2026': 'BWKI 2026',
        'How do different languages organize the same knowledge?': '不同语言如何组织相同的知识？',
        'How do different STEM subjects organize knowledge?': '不同 STEM 学科如何组织知识？',
        'How do different curricula organize the same subject?': '不同课程体系如何组织同一学科？',
    }),
]:
    text = en
    # Apply body translations (longest first to avoid partial matches)
    for old in sorted(body_map.keys(), key=len, reverse=True):
        text = text.replace(old, body_map[old])

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

    # Verify
    with open(output_file, 'r', encoding='utf-8') as f:
        t = f.read()

    # Check remaining English words
    remaining = []
    check_words = ['Concepts', 'Relations', 'Disciplines', 'Gold Labels', 'Overall F1',
                   'Research Questions', 'Interactive 3D', 'Research Portal',
                   'Social concepts', 'Mathematics', 'Model Benchmark',
                   'Project Structure', 'Quick Start', 'Extraction Validation',
                   'Table of Contents', 'Why LinguaGraph', 'Dataset',
                   'References', 'License', 'Compliance', 'Contact']
    for w in check_words:
        if w in t:
            remaining.append(w)

    sections = [l.strip() for l in t.split('\n') if l.strip().startswith('## ') and not l.strip().startswith('### ')]
    print(f'{output_file}: {len(t)} chars, {len(sections)} sections')
    if remaining:
        print(f'  Remaining English ({len(remaining)}): {remaining}')
    else:
        print(f'  All text translated!')

# Also fix portal footer links to use GitHub URLs
with open('cognitive-space/portal/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace(
    'href="../README.md"',
    'href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph"'
)
html = html.replace(
    'href="../README_DE.md"',
    'href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/blob/master/README_DE.md"'
)
html = html.replace(
    'href="../README_ZH.md"',
    'href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/blob/master/README_ZH.md"'
)

with open('cognitive-space/portal/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('\nPortal footer links fixed to GitHub URLs')
print('Done!')
