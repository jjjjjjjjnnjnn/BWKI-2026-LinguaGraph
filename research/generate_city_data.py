"""
Cognitive City Data Generator v2
Uses structured edge patterns for meaningful city-like layouts.
"""

import json, os, sys, re, glob
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_DIR, 'src'))
sys.path.insert(0, PROJECT_DIR)

from graph import build_graph, graph_stats
import networkx as nx

# Load mapping
MAPPING_PATH = os.path.join(PROJECT_DIR, 'config', 'cross_language_mapping.json')
with open(MAPPING_PATH, 'r', encoding='utf-8') as f:
    MAPPING = json.load(f)["mappings"]

# Build lookup
zh_to_id, de_to_id, en_to_id = {}, {}, {}
id_labels = {}
for m in MAPPING:
    cid = m["id"]
    id_labels[cid] = {"zh": m["zh"][0], "de": m["de"][0], "en": m["en"][0]}
    for w in m["zh"]: zh_to_id[w] = cid
    for w in m["de"]: de_to_id[w] = cid
    for w in m["en"]: en_to_id[w] = cid

LANG_MAP = {"zh": zh_to_id, "de": de_to_id, "en": en_to_id}
LANG_NAMES = {"zh": "Chinese", "de": "German", "en": "English"}

# Semantic groups for meaningful edge connections
# Concepts in the same group are connected; cross-group edges only for strong links
SEMANTIC_GROUPS = {
    "social_individual": ["individual", "society", "family", "community"],
    "rights_freedoms": ["freedom", "rights", "choice", "speech", "autonomy"],
    "governance": ["democracy", "law", "power", "justice"],
    "philosophy": ["philosophy", "reason", "free_will", "history"],
    "economy": ["economy", "progress", "success"],
    "values": ["equality", "responsibility", "security", "liberation"],
    "culture": ["religion", "education", "identity", "tradition"],
}

# Strong cross-group connections
CROSS_EDGES = [
    ("freedom", "responsibility"), ("freedom", "justice"),
    ("rights", "equality"), ("rights", "law"),
    ("individual", "autonomy"), ("society", "justice"),
    ("democracy", "freedom"), ("democracy", "equality"),
    ("economy", "freedom"), ("success", "individual"),
    ("education", "individual"), ("education", "progress"),
    ("responsibility", "family"), ("responsibility", "society"),
    ("philosophy", "freedom"), ("philosophy", "justice"),
]

CONCEPTS = [
    ("freedom", "自由", "Freiheit", "Freedom"),
    ("justice", "公平", "Gerechtigkeit", "Justice"),
    ("responsibility", "责任", "Verantwortung", "Responsibility"),
    ("success", "成功", "Erfolg", "Success"),
]

from db_utils import get_connection, query
conn = get_connection()
db_results = query(conn, """
    SELECT topic, lang_pair, lcd_score
    FROM cross_language_analysis
    WHERE student_id = 'WIKIPEDIA_CORPUS'
    ORDER BY topic, lang_pair
""")
topic_lcd = {}
for r in db_results:
    t = r['topic']
    topic_lcd.setdefault(t, []).append(r['lcd_score'] if r['lcd_score'] else 0)
conn.close()


def extract_concepts(text, lang):
    found = set()
    wmap = LANG_MAP[lang]
    for word, cid in wmap.items():
        if lang in ("de", "en"):
            if re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE):
                found.add(cid)
        else:
            if word in text:
                found.add(cid)
    return sorted(found)


def build_city_v2(concept_ids, lang):
    """Build city with meaningful edge structure."""
    G = nx.Graph()
    for cid in concept_ids:
        G.add_node(cid)

    # Add edges from semantic groups
    for group_name, members in SEMANTIC_GROUPS.items():
        group_ids = [m for m in members if m in concept_ids]
        for i, c1 in enumerate(group_ids):
            for c2 in group_ids[i+1:]:
                if not G.has_edge(c1, c2):
                    G.add_edge(c1, c2, weight=0.8, connection="semantic")

    # Add cross-group edges
    for c1, c2 in CROSS_EDGES:
        if c1 in concept_ids and c2 in concept_ids and not G.has_edge(c1, c2):
            G.add_edge(c1, c2, weight=0.5, connection="cross")

    # Centrality
    if G.number_of_nodes() > 0:
        try:
            cent = nx.degree_centrality(G)
            betweenness = nx.betweenness_centrality(G)
            closeness = nx.closeness_centrality(G)
        except:
            cent = {n: 0.5 for n in G.nodes()}
            betweenness = {n: 0 for n in G.nodes()}
            closeness = {n: 0 for n in G.nodes()}
    else:
        cent = betweenness = closeness = {}

    nodes_out = []
    for node in G.nodes():
        label = id_labels.get(node, {}).get(lang, node)
        nodes_out.append({
            "id": node,
            "label": label,
            "language": lang,
            "centrality": round(cent.get(node, 0), 4),
            "betweenness": round(betweenness.get(node, 0), 4),
            "closeness": round(closeness.get(node, 0), 4),
            "group": "core" if cent.get(node, 0) > 0.3 else "peripheral",
        })

    edges_out = []
    for u, v, d in G.edges(data=True):
        edges_out.append({
            "source": u,
            "target": v,
            "weight": d.get("weight", 0.5),
            "connection": d.get("connection", "default"),
        })

    return {
        "nodes": nodes_out,
        "edges": edges_out,
        "centrality": {n: round(c, 4) for n, c in cent.items()},
        "stats": {"nodes": len(nodes_out), "edges": len(edges_out)},
    }


def main():
    cities = {}
    base = os.path.join(PROJECT_DIR, 'data', 'pilot_corpus')

    for concept_key, zh_label, de_label, en_label in CONCEPTS:
        concept_dir = os.path.join(base, concept_key)
        if not os.path.exists(concept_dir):
            continue

        cities[concept_key] = {
            "labels": {"zh": zh_label, "de": de_label, "en": en_label},
            "languages": {},
        }

        for lang in ["zh", "de", "en"]:
            files = sorted(glob.glob(os.path.join(concept_dir, f"{lang}_*.txt")))
            if not files:
                continue
            with open(files[0], 'r', encoding='utf-8') as f:
                text = f.read()
            ids = extract_concepts(text, lang)
            if not ids:
                continue

            city = build_city_v2(ids, lang)
            avg_lcd = 0
            if concept_key in topic_lcd and topic_lcd[concept_key]:
                avg_lcd = sum(topic_lcd[concept_key]) / len(topic_lcd[concept_key])
            city["avg_lcd"] = round(avg_lcd, 4)
            cities[concept_key]["languages"][lang] = city

            print(f"  [OK] {concept_key}/{lang}: {city['stats']['nodes']} nodes, {city['stats']['edges']} edges, LCD={city['avg_lcd']}")

    outdir = os.path.join(PROJECT_DIR, 'research', 'visualization')
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, 'cognitive_cities_v2.json')
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(cities, f, ensure_ascii=False, indent=2)

    print(f"\n[SAVED] {outpath}")
    print(f"  {len(cities)} concepts, 4 languages")
    print(f"  Edge types: semantic (group-internal), cross (inter-group)")
    print(f"  Ready for Three.js import")


if __name__ == "__main__":
    main()
