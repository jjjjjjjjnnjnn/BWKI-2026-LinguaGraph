"""
Freedom Cross-Language Analysis
=================================
Processes Wikipedia articles on "Freedom" in Chinese, German, and English,
extracts concepts and relations, builds cognitive graphs, and compares them.
"""

import json, os, sys
# Add project src to path
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_DIR, 'src'))

from graph import build_graph, graph_to_dict, graph_stats
from scoring import calculate_lcd_score
import networkx as nx

# === CONCEPT DICTIONARIES ===
freedom_concepts = {
    'zh': [
        ('自由', ['自由', '自主', '支配']),
        ('个体', ['个人', '个体', '自己', '私人']),
        ('权利', ['权利', '权力', '人权']),
        ('选择', ['选择', '决定']),
        ('社会', ['社会', '群体', '集体', '社群']),
        ('责任', ['责任', '义务']),
        ('平等', ['平等', '公平']),
        ('法律', ['法律', '宪法', '法治', '法']),
        ('民主', ['民主', '共和']),
        ('言论', ['言论', '表达']),
        ('解放', ['解放']),
        ('自律', ['自律', '康德', '理性', '道德']),
        ('安全', ['安全', '秩序']),
        ('经济', ['经济', '市场', '财产', '贸易', '资本']),
        ('革命', ['革命', '法国大革命']),
        ('宗教', ['宗教', '信仰']),
        ('自由意志', ['自由意志']),
    ],
    'de': [
        ('Freiheit', ['Freiheit', 'frei']),
        ('Autonomie', ['Autonomie', 'Selbstbestimmung', 'Selbstverwirklichung']),
        ('Individuum', ['Individuum', 'Einzelperson']),
        ('Recht', ['Recht', 'Rechte', 'Grundrechte', 'Menschenrechte']),
        ('negative Freiheit', ['negative Freiheit', 'Freiheit von']),
        ('positive Freiheit', ['positive Freiheit', 'Freiheit zu']),
        ('Gesellschaft', ['Gesellschaft', 'sozial', 'gemeinschaftlich']),
        ('Verantwortung', ['Verantwortung']),
        ('Gleichheit', ['Gleichheit']),
        ('Gesetz', ['Gesetz', 'Verfassung', 'Grundgesetz']),
        ('Demokratie', ['Demokratie']),
        ('Meinungsfreiheit', ['Meinungsfreiheit', 'Redefreiheit']),
        ('Vernunft', ['Vernunft', 'Kant', 'rational']),
        ('Sicherheit', ['Sicherheit']),
        ('Wirtschaft', ['Wirtschaft', 'Markt', 'Eigentum', 'Marktwirtschaft']),
        ('Revolution', ['Revolution']),
        ('Liberalismus', ['Liberalismus']),
        ('Sozialismus', ['Sozialismus', 'Arbeiterklasse', 'Marx']),
        ('Willensfreiheit', ['Willensfreiheit', 'Determinismus']),
    ],
    'en': [
        ('freedom', ['freedom', 'free']),
        ('liberty', ['liberty']),
        ('autonomy', ['autonomy', 'autonomous', 'self-governance']),
        ('individual', ['individual', 'personal']),
        ('right', ['right', 'rights']),
        ('choice', ['choice', 'choose']),
        ('society', ['society', 'social', 'community']),
        ('responsibility', ['responsibility']),
        ('equality', ['equality']),
        ('law', ['law', 'constitution', 'constitutional']),
        ('democracy', ['democracy', 'democratic']),
        ('speech', ['speech', 'expression']),
        ('free will', ['free will', 'determinism']),
        ('security', ['security']),
        ('economy', ['economy', 'market', 'property', 'trade', 'capital']),
        ('civil rights', ['civil rights', 'assembly', 'association']),
        ('domination', ['domination', 'slavery', 'oppression']),
        ('liberalism', ['liberalism']),
        ('philosophy', ['philosophy', 'philosophical']),
    ],
}

# === RELATION PATTERNS PER LANGUAGE ===
relations_map = {
    'zh': [
        ('自由', '个体'), ('自由', '权利'), ('自由', '选择'), ('自由', '责任'),
        ('自由', '社会'), ('自由', '法律'), ('自由', '平等'), ('自由', '言论'),
        ('自由', '解放'), ('自由', '自律'), ('自由', '经济'), ('自由', '民主'),
        ('自由', '革命'), ('自由', '安全'), ('革命', '平等'), ('革命', '民主'),
        ('自由', '宗教'), ('自由', '自由意志'),
    ],
    'de': [
        ('Freiheit', 'Autonomie'), ('Freiheit', 'Individuum'), ('Freiheit', 'Recht'),
        ('Freiheit', 'negative Freiheit'), ('Freiheit', 'positive Freiheit'),
        ('Freiheit', 'Gesellschaft'), ('Freiheit', 'Verantwortung'),
        ('Freiheit', 'Gleichheit'), ('Freiheit', 'Gesetz'),
        ('Freiheit', 'Meinungsfreiheit'), ('Freiheit', 'Vernunft'),
        ('Freiheit', 'Sicherheit'), ('Freiheit', 'Wirtschaft'),
        ('Freiheit', 'Liberalismus'), ('Freiheit', 'Sozialismus'),
        ('Freiheit', 'Demokratie'), ('Freiheit', 'Willensfreiheit'),
        ('Freiheit', 'Revolution'),
    ],
    'en': [
        ('freedom', 'liberty'), ('freedom', 'autonomy'), ('freedom', 'individual'),
        ('freedom', 'right'), ('freedom', 'choice'), ('freedom', 'society'),
        ('freedom', 'responsibility'), ('freedom', 'equality'),
        ('freedom', 'law'), ('freedom', 'democracy'), ('freedom', 'speech'),
        ('freedom', 'free will'), ('freedom', 'security'),
        ('freedom', 'civil rights'), ('freedom', 'domination'),
        ('freedom', 'economy'), ('freedom', 'liberalism'),
        ('freedom', 'philosophy'),
    ],
}


def extract(text, lang):
    """Extract concepts from text using keyword matching."""
    concepts_dict = {c[0]: c[1] for c in freedom_concepts[lang]}
    found = []
    for concept, keywords in concepts_dict.items():
        for kw in keywords:
            if kw in text:
                found.append(concept)
                break
    return found


def build_relations(concepts, lang):
    """Build relations from co-occurring concepts."""
    rels = []
    pairs = relations_map.get(lang, [])
    for src, tgt in pairs:
        if src in concepts and tgt in concepts:
            rels.append({'source': src, 'target': tgt, 'type': 'relates_to'})
    return rels


def main():
    base = os.path.join(PROJECT_DIR, 'data', 'pilot_corpus', 'freedom')

    # Read texts
    texts = {}
    for lang, filename in [('zh', 'zh_自由_wikipedia.txt'), ('de', 'de_freiheit_wikipedia.txt'), ('en', 'en_freedom_wikipedia.txt')]:
        path = os.path.join(base, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                texts[lang] = f.read()
        else:
            print(f'[ERROR] File not found: {path}')
            return

    # Process each language
    results = {}
    for lang, text in texts.items():
        concepts = extract(text, lang)
        relations = build_relations(concepts, lang)
        G = build_graph({'concepts': concepts, 'relations': relations})
        stats = graph_stats(G)
        results[lang] = {'concepts': concepts, 'relations': relations, 'graph': G, 'stats': stats}

        print(f'\n=== {lang.upper()} ===')
        print(f'Concepts ({len(concepts)}): {concepts}')
        print(f'Relations: {len(relations)}')
        print(f'Graph: {stats["nodes"]} nodes, {stats["edges"]} edges, density={stats["density"]:.3f}')
        for r in relations:
            print(f'  {r["source"]} -- {r["target"]}')

    # Cross-language comparison
    print('\n\n========== CROSS-LANGUAGE COMPARISON ==========')
    lang_pairs = [('zh', 'de'), ('zh', 'en'), ('de', 'en')]
    comparisons = []

    for l1, l2 in lang_pairs:
        g1 = results[l1]['graph']
        g2 = results[l2]['graph']
        s1 = set(g1.nodes())
        s2 = set(g2.nodes())
        shared = s1 & s2
        only_l1 = s1 - s2
        only_l2 = s2 - s1

        lcd = calculate_lcd_score(g1, g2)

        print(f'\n--- {l1} vs {l2} ---')
        print(f'LCD Score: {lcd["lcd_score"]:.4f}')
        print(f'Graph Similarity: {lcd["similarity"]:.4f}')
        print(f'Shared edges: {lcd["shared_edges"]}')
        print(f'Unique to {l1}: {list(only_l1)[:8]}')
        print(f'Unique to {l2}: {list(only_l2)[:8]}')

        comparisons.append({
            'pair': f'{l1}-{l2}',
            'lcd': lcd['lcd_score'],
            'similarity': lcd['similarity'],
            'shared_edges': lcd['shared_edges'],
            'l1_unique': list(only_l1)[:10],
            'l2_unique': list(only_l2)[:10],
        })

    # Build output
    output = {
        'topic': 'freedom',
        'topic_zh': '自由',
        'topic_de': 'Freiheit',
        'topic_en': 'Freedom',
        'source': 'Wikipedia',
        'concepts_per_language': {
            lang: {'count': len(results[lang]['concepts']), 'list': results[lang]['concepts']}
            for lang in ['zh', 'de', 'en']
        },
        'cross_language_comparisons': comparisons,
    }

    # Interpret results
    most_diff = max(comparisons, key=lambda c: c['lcd'])
    most_sim = min(comparisons, key=lambda c: c['lcd'])

    # Calculate concept overlap matrix
    zh_set = set(results['zh']['concepts'])
    de_set = set(results['de']['concepts'])
    en_set = set(results['en']['concepts'])

    output['interpretation'] = {
        'most_different_pair': most_diff['pair'],
        'most_different_lcd': most_diff['lcd'],
        'most_similar_pair': most_sim['pair'],
        'most_similar_similarity': most_sim['similarity'],
        'zh_de_concept_overlap': len(zh_set & de_set),
        'zh_en_concept_overlap': len(zh_set & en_set),
        'de_en_concept_overlap': len(de_set & en_set),
        'concepts_only_in_zh': list(zh_set - de_set - en_set)[:8],
        'concepts_only_in_de': list(de_set - zh_set - en_set)[:8],
        'concepts_only_in_en': list(en_set - zh_set - de_set)[:8],
    }

    # Save
    os.makedirs(os.path.join(PROJECT_DIR, 'research', 'findings'), exist_ok=True)
    outpath = os.path.join(PROJECT_DIR, 'research', 'findings', 'freedom_cross_language.json')
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f'\n\n[SAVED] {outpath}')

    # Print summary
    print('\n' + '='*50)
    print('FINDINGS SUMMARY')
    print('='*50)
    print(f'Topic: Freedom / 自由 / Freiheit')
    print(f'Source: Wikipedia articles')
    print(f'\nMost different pair: {most_diff["pair"]} (LCD={most_diff["lcd"]:.4f})')
    print(f'Most similar pair: {most_sim["pair"]} (LCD={most_sim["lcd"]:.4f})')
    print(f'\nUnique concepts by language:')
    only_zh = output['interpretation']['concepts_only_in_zh']
    only_de = output['interpretation']['concepts_only_in_de']
    only_en = output['interpretation']['concepts_only_in_en']
    if only_zh: print(f'  Chinese only: {only_zh}')
    if only_de: print(f'  German only: {only_de}')
    if only_en: print(f'  English only: {only_en}')
    print(f'\nQuestion suggestions for survey:')
    print(f'  - "What does freedom mean to you personally?"')
    print(f'  - "Is freedom more about individual rights or social responsibility?"')
    print(f'  - "Can freedom conflict with security? How would you resolve this?"')
    print(f'  - "Does freedom require economic independence?"')

if __name__ == '__main__':
    main()
