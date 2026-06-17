"""LinguaGraph Cross-Language Research Pipeline v2 — Batch Analyzer

Analyzes a concept across Chinese, German, and English Wikipedia texts
using the cross-language concept mapping layer for correct LCD computation.

Usage: python research/analyze_concept.py <concept_name>
  concept_name: directory name under data/pilot_corpus/
"""

import json, os, sys, glob, re
from pathlib import Path

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_DIR, 'src'))

from graph import build_graph, graph_stats
from scoring import calculate_lcd_score
import networkx as nx

# Load cross-language mapping
MAPPING_PATH = os.path.join(PROJECT_DIR, 'config', 'cross_language_mapping.json')
with open(MAPPING_PATH, 'r', encoding='utf-8') as f:
    MAPPING = json.load(f)["mappings"]

# Build lookup dicts
zh_to_id, de_to_id, en_to_id = {}, {}, {}
concept_labels = {}
for m in MAPPING:
    cid = m["id"]
    concept_labels[cid] = {"zh": m["zh"][0], "de": m["de"][0], "en": m["en"][0]}
    for w in m["zh"]: zh_to_id[w] = cid
    for w in m["de"]: de_to_id[w] = cid
    for w in m["en"]: en_to_id[w] = cid

LANG_KEY_MAP = {"zh": zh_to_id, "de": de_to_id, "en": en_to_id}
LANG_NAMES = {"zh": "Chinese", "de": "German", "en": "English"}


def extract_mapped(text, lang):
    found = set()
    word_map = LANG_KEY_MAP[lang]
    for word, cid in word_map.items():
        if lang in ("de", "en"):
            # Use word boundaries for European languages
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                found.add(cid)
        else:
            # Chinese: direct substring (Chinese chars are self-delimiting)
            if word in text:
                found.add(cid)
    return sorted(found)


def load_article(lang, concept_dir):
    """Load text from corpus directory. Only matches {lang}_*.txt"""
    pattern = os.path.join(concept_dir, f"{lang}_*.txt")
    files = sorted(glob.glob(pattern))
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if len(content) > 50:
            return content
    return None


def analyze_concept(concept_name):
    concept_dir = os.path.join(PROJECT_DIR, 'data', 'pilot_corpus', concept_name)

    if not os.path.exists(concept_dir):
        print(f"[ERROR] No corpus directory: {concept_dir}")
        return None

    print(f"\n{'='*60}")
    print(f"  Analyzing: {concept_name}")
    print(f"{'='*60}")

    # Load articles per language
    texts = {}
    for lang in ["zh", "de", "en"]:
        text = load_article(lang, concept_dir)
        if text:
            texts[lang] = text
            print(f"  [OK] {lang.upper()}: {len(text)} chars")
        else:
            print(f"  [WARN] {lang.upper()}: No article found")

    if len(texts) < 2:
        print("[ERROR] Need at least 2 languages to compare")
        return None

    # Process each language
    results = {}
    for lang, text in texts.items():
        concept_ids = extract_mapped(text, lang)
        if lang in concept_labels and concept_ids:
            display_names = [concept_labels[c][lang] for c in concept_ids]
        else:
            display_names = concept_ids

        # Build co-occurrence-based graph (NOT all-pairs!)
        # Split text into paragraphs; concepts co-occurring in the same
        # paragraph get an edge. This creates STRUCTURAL graph differences.
        paragraphs = [p.strip() for p in re.split(r'[\n\r]+', text) if len(p.strip()) > 20]
        cooccur = {}
        for para in paragraphs:
            para_concepts = set()
            for word, cid in LANG_KEY_MAP[lang].items():
                if lang in ("de", "en"):
                    if re.search(r'\b' + re.escape(word) + r'\b', para, re.IGNORECASE):
                        para_concepts.add(cid)
                else:
                    if word in para:
                        para_concepts.add(cid)
            # For every pair of concepts in same paragraph, increment co-occurrence
            clist = sorted(para_concepts)
            for i, c1 in enumerate(clist):
                for c2 in clist[i+1:]:
                    key = (c1, c2)
                    cooccur[key] = cooccur.get(key, 0) + 1

        relations = []
        for (c1, c2), weight in cooccur.items():
            relations.append({"source": c1, "target": c2, "type": "co_occurs"})
            relations.append({"source": c2, "target": c1, "type": "co_occurs"})

        G = build_graph({"concepts": concept_ids, "relations": relations})
        stats = graph_stats(G)
        results[lang] = {"ids": concept_ids, "names": display_names, "graph": G, "stats": stats}

        print(f"\n  {lang.upper()}: {len(concept_ids)} concepts, {stats['nodes']} nodes")
        print(f"  Top: {display_names[:8]}")

    # Cross-language comparisons
    print(f"\n\n  {'='*50}")
    print(f"  CROSS-LANGUAGE COMPARISON (with concept mapping)")
    print(f"  {'='*50}")

    comparisons = []
    lang_list = list(results.keys())
    for i in range(len(lang_list)):
        for j in range(i+1, len(lang_list)):
            l1, l2 = lang_list[i], lang_list[j]
            g1, g2 = results[l1]["graph"], results[l2]["graph"]
            s1, s2 = set(results[l1]["ids"]), set(results[l2]["ids"])
            shared = s1 & s2
            only_l1 = s1 - s2
            only_l2 = s2 - s1
            jaccard = len(shared) / len(s1 | s2) if (s1 | s2) else 0
            lcd = calculate_lcd_score(g1, g2)

            shared_names = []
            for c in sorted(shared):
                lbl = concept_labels.get(c, {})
                shared_names.append(lbl.get("zh", c))

            comp = {
                "pair": f"{l1}-{l2}",
                "lcd": round(lcd["lcd_score"], 4),
                "similarity": round(lcd["similarity"], 4),
                "concept_jaccard": round(jaccard, 4),
                "concept_shift": len(only_l1) + len(only_l2),
                "shared_count": len(shared),
                "shared": [concept_labels.get(c, {}).get("zh", c) for c in sorted(shared)],
                "unique_l1": [concept_labels.get(c, {}).get(l1, c) for c in sorted(only_l1)],
                "unique_l2": [concept_labels.get(c, {}).get(l2, c) for c in sorted(only_l2)],
            }

            comparisons.append(comp)
            print(f"\n  {LANG_NAMES[l1]} vs {LANG_NAMES[l2]}:")
            print(f"    LCD: {comp['lcd']:.4f} | Jaccard: {comp['concept_jaccard']:.4f}")
            print(f"    Shared: {comp['shared']}")
            if comp['unique_l1']: print(f"    Unique {LANG_NAMES[l1]}: {comp['unique_l1']}")
            if comp['unique_l2']: print(f"    Unique {LANG_NAMES[l2]}: {comp['unique_l2']}")

    # Build full output
    shared_by_all = set.intersection(*[set(results[l]["ids"]) for l in results]) if len(results) >= 3 else set()
    all_unique = {}
    for lang in results:
        others = [l for l in results if l != lang]
        unique = set(results[lang]["ids"]) - set.union(*[set(results[l]["ids"]) for l in others])
        all_unique[lang] = [concept_labels.get(c, {}).get(lang, c) for c in sorted(unique)]

    output = {
        "topic": concept_name,
        "source": "Wikipedia",
        "method": "v2 - cross-language concept mapping applied",
        "languages": list(results.keys()),
        "concepts_per_language": {
            lang: {"count": len(r["ids"]), "ids": r["ids"], "names": r["names"]}
            for lang, r in results.items()
        },
        "shared_across_all_languages": {
            "count": len(shared_by_all),
            "ids": sorted(shared_by_all),
            "labels": [concept_labels.get(c, {}).get("zh", c) for c in sorted(shared_by_all)],
        },
        "unique_per_language": all_unique,
        "cross_language": comparisons,
    }

    # Questionnaire suggestions
    questions = []
    shared_ids = output["shared_across_all_languages"]["ids"]
    for comp in comparisons:
        if comp["unique_l1"]:
            questions.append(f"[{LANG_NAMES[comp['pair'].split('-')[0]]}] How important is {'/'.join(comp['unique_l1'][:3])} to your understanding of {concept_name}?")
        if comp["unique_l2"]:
            questions.append(f"[{LANG_NAMES[comp['pair'].split('-')[1]]}] How important is {'/'.join(comp['unique_l2'][:3])} to your understanding of {concept_name}?")

    if "individual" in shared_ids and "society" in shared_ids:
        questions.append(f"Is {concept_name} more about individual rights or social harmony?")
    if "equality" in shared_ids:
        questions.append(f"Is true {concept_name} about equality of opportunity or equality of outcome?")

    output["questionnaire_suggestions"] = questions[:6]

    # Save
    findings_dir = os.path.join(PROJECT_DIR, "research", "findings")
    os.makedirs(findings_dir, exist_ok=True)
    outpath = os.path.join(findings_dir, f"{concept_name}_cross_language.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n\n  [SAVED] {outpath}")
    print(f"  [QUESTIONS] {len(questions)} suggested for survey")

    return output


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Analyze a concept across languages")
    parser.add_argument("concept", nargs="?", default="justice", help="Concept name (directory in data/pilot_corpus/)")
    args = parser.parse_args()
    analyze_concept(args.concept)
