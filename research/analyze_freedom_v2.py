"""
Freedom Cross-Language Analysis v2
=====================================
Corrected: Uses cross-language concept mapping layer to normalize
concepts across languages before computing LCD scores.

Key improvement: Maps "权利", "Recht", "right" → shared ID "rights"
so we measure COGNITIVE differences, not TRANSLATION differences.
"""

import json, os, sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_DIR, 'src'))

from graph import build_graph, graph_stats
from scoring import calculate_lcd_score
import networkx as nx

# Load mapping
MAPPING_PATH = os.path.join(PROJECT_DIR, 'config', 'cross_language_mapping.json')
with open(MAPPING_PATH, 'r', encoding='utf-8') as f:
    MAPPING = json.load(f)["mappings"]

# Build lookup: language word -> shared concept ID
# Also build per-language keyword dicts
zh_to_id = {}
de_to_id = {}
en_to_id = {}
concept_labels = {}  # shared_id -> human label in each language

for m in MAPPING:
    cid = m["id"]
    concept_labels[cid] = {"zh": m["zh"][0], "de": m["de"][0], "en": m["en"][0]}
    for w in m["zh"]:
        zh_to_id[w] = cid
    for w in m["de"]:
        de_to_id[w] = cid
    for w in m["en"]:
        en_to_id[w] = cid

# Build keyword-to-ID dict for extraction
LANG_KEYWORD_MAP = {
    "zh": zh_to_id,
    "de": de_to_id,
    "en": en_to_id,
}

# Text files
TEXT_FILES = {
    "zh": ("zh_自由_wikipedia.txt", "自由 / Freedom"),
    "de": ("de_freiheit_wikipedia.txt", "Freiheit / Freedom"),
    "en": ("en_freedom_wikipedia.txt", "Freedom"),
}

BASE_DIR = os.path.join(PROJECT_DIR, 'data', 'pilot_corpus', 'freedom')


def extract_mapped(text, lang):
    """Extract concepts, mapping to shared IDs immediately."""
    word_map = LANG_KEYWORD_MAP[lang]
    found_ids = set()
    for word, cid in word_map.items():
        if word in text:
            found_ids.add(cid)
    return sorted(found_ids)


def main():
    # Read and process each language
    results = {}
    for lang, (filename, label) in TEXT_FILES.items():
        path = os.path.join(BASE_DIR, filename)
        if not os.path.exists(path):
            print(f"[SKIP] {filename} not found")
            continue

        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Extract to shared concept IDs
        concept_ids = extract_mapped(text, lang)
        concept_names = [concept_labels[cid][lang] for cid in concept_ids]

        # Build all-pairs relations for cognitive graph
        relations = []
        for i, c1 in enumerate(concept_ids):
            for j, c2 in enumerate(concept_ids):
                if i != j:
                    relations.append({"source": c1, "target": c2, "type": "relates_to"})

        # Build graph (using shared IDs so comparison works!)
        G = build_graph({"concepts": concept_ids, "relations": relations})
        stats = graph_stats(G)
        results[lang] = {
            "concept_ids": concept_ids,
            "concept_names": concept_names,
            "graph": G,
            "stats": stats,
        }

        print(f"\n=== {lang.upper()} ({label}) ===")
        print(f"Shared concept IDs ({len(concept_ids)}): {concept_ids}")
        print(f"Display names: {concept_names}")
        print(f"Graph: {stats['nodes']} nodes, {stats['edges']} edges")

    # Cross-language comparison (now using same ID space!)
    print("\n\n========== CROSS-LANGUAGE COMPARISON (MAPPED) ==========")

    lang_pairs = [("zh", "de"), ("zh", "en"), ("de", "en")]
    lang_names = {"zh": "Chinese", "de": "German", "en": "English"}
    comparisons = []

    for l1, l2 in lang_pairs:
        g1 = results[l1]["graph"]
        g2 = results[l2]["graph"]

        s1 = set(g1.nodes())
        s2 = set(g2.nodes())
        shared = s1 & s2
        only_l1 = s1 - s2
        only_l2 = s2 - s1

        lcd = calculate_lcd_score(g1, g2)
        # Since we use shared IDs, edges with identical IDs are "same"
        # LCD from scoring module compares edge sets
        # But edges are all-pairs, so density matters

        # Better: concept Jaccard similarity
        jaccard = len(shared) / len(s1 | s2) if (s1 | s2) else 0

        print(f"\n--- {lang_names[l1]} vs {lang_names[l2]} ---")
        print(f"LCD Score (edge-based): {lcd['lcd_score']:.4f}")
        print(f"Graph Similarity: {lcd['similarity']:.4f}")
        print(f"Concept Jaccard: {jaccard:.4f}")
        print(f"Shared concepts ({len(shared)}): {[concept_labels[c]['zh'] for c in shared]}")
        print(f"{lang_names[l1]} only: {[concept_labels[c][l1] for c in only_l1]}")
        print(f"{lang_names[l2]} only: {[concept_labels[c][l2] for c in only_l2]}")

        comparisons.append({
            "pair": f"{l1}-{l2}",
            "lcd": lcd["lcd_score"],
            "similarity": lcd["similarity"],
            "concept_jaccard": round(jaccard, 4),
            "shared_ids": list(shared),
            "shared_labels": [concept_labels[c]["zh"] for c in shared],
            "unique_l1": list(only_l1),
            "unique_l1_labels": [concept_labels[c][l1] for c in only_l1],
            "unique_l2": list(only_l2),
            "unique_l2_labels": [concept_labels[c][l2] for c in only_l2],
        })

    # Build output
    output = {
        "topic": "freedom",
        "topic_labels": {"zh": "自由", "de": "Freiheit", "en": "Freedom"},
        "method": "v2 - cross-language concept mapping applied",
        "source": "Wikipedia",
        "pre_mapping_lcd_note": "PREVIOUS analysis (v1) gave LCD=1.00 due to missing concept mapping. This is the CORRECTED analysis.",
        "concept_ids_per_language": {
            lang: {
                "count": len(results[lang]["concept_ids"]),
                "ids": results[lang]["concept_ids"],
                "labels": results[lang]["concept_names"],
            }
            for lang in ["zh", "de", "en"]
        },
        "cross_language": comparisons,
    }

    # Findings
    print("\n\n============================================")
    print("CORRECTED FINDINGS (with concept mapping)")
    print("============================================")

    # Which concepts are shared across all 3?
    all_shared = set(results["zh"]["concept_ids"]) & set(results["de"]["concept_ids"]) & set(results["en"]["concept_ids"])
    print(f"\nConcepts shared by ALL three languages ({len(all_shared)}):")
    for cid in sorted(all_shared):
        labels = {l: concept_labels[cid][l] for l in ["zh", "de", "en"]}
        print(f"  {cid}: zh={labels['zh']}, de={labels['de']}, en={labels['en']}")

    # Which are unique to each?
    for lang in ["zh", "de", "en"]:
        other1, other2 = [l for l in ["zh", "de", "en"] if l != lang]
        unique = set(results[lang]["concept_ids"]) - set(results[other1]["concept_ids"]) - set(results[other2]["concept_ids"])
        if unique:
            print(f"\nUnique to {lang_names[lang]}:")
            for cid in sorted(unique):
                print(f"  {cid}: {concept_labels[cid][lang]}")

    output["findings"] = {
        "shared_across_all": list(all_shared),
        "shared_labels": [concept_labels[c]["zh"] for c in all_shared],
        "unique_per_language": {
            lang: {
                "ids": list(set(results[lang]["concept_ids"]) -
                           set(sum([results[l2]["concept_ids"] for l2 in ["zh", "de", "en"] if l2 != lang], []))),
            }
            for lang in ["zh", "de", "en"]
        },
    }

    # Save
    os.makedirs(os.path.join(PROJECT_DIR, "research", "findings"), exist_ok=True)
    outpath = os.path.join(PROJECT_DIR, "research", "findings", "freedom_cross_language_v2.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n[SAVED] {outpath}")

    # Questionnaire suggestions
    print("\n\nQUESTIONNAIRE SUGGESTIONS:")
    if "responsibility" in all_shared and "individual" in all_shared:
        print('  - "Is freedom more about individual rights or social responsibility?"')
    if "security" in all_shared:
        print('  - "Can freedom conflict with security? How would you resolve this?"')
    if "economy" in all_shared or "liberalism" in all_shared:
        print('  - "Does economic freedom contradict social equality?"')

    # For uniqueness-based questions
    for lang in ["zh", "de", "en"]:
        unique = output["findings"]["unique_per_language"][lang]["ids"]
        if unique:
            labels = [concept_labels[c][lang] for c in unique]
            print(f'  [{lang_names[lang]}] How important is {" / ".join(labels)} to your understanding of freedom?')


if __name__ == "__main__":
    main()
