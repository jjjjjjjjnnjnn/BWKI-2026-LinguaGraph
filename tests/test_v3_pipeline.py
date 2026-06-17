import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'src')
from scoring import calculate_mcl_score
import networkx as nx

with open('data/survey/v3/example_zh.json', encoding='utf-8') as f:
    survey = json.load(f)

all_nodes = set()
all_edges = []
all_mcl = []
for r in survey['responses']:
    g = r.get('graph_output', {})
    all_nodes.update(g.get('nodes', []))
    all_edges.extend(g.get('edges', []))
    all_mcl.extend(g.get('mcl_candidates', []))

G = nx.DiGraph()
for n in all_nodes:
    G.add_node(n)
for e in all_edges:
    if e.get('source') and e.get('target'):
        G.add_edge(e['source'], e['target'], relation=e.get('type',''))

expert = nx.DiGraph()
expert.add_edges_from([('极限','导数'),('导数','变化率'),('积分','导数'),('积分','面积'),('导数','切线斜率')])

mcl = calculate_mcl_score(G, expert)

print('=== v3 Survey Evaluation ===')
print('Respondent:', survey['respondent_id'])
print('Language:', survey['language'])
print('Nodes:', len(all_nodes))
print('Edges:', len(all_edges))
print('MCL Score:', str(mcl['mcl_score']) + '%', '(' + str(mcl['missing_count']) + '/' + str(mcl['total_expert']) + ' missing)')
print('Missing:', mcl['missing_edges'])
print('MCL Candidates:', [m['concept'] for m in all_mcl])
