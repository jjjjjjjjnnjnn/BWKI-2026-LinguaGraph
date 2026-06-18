"""
LinguaGraph Pilot Study — Textbook Comparison Experiment
========================================================

Compares cognitive graphs extracted from textbook passages across
three languages (zh/de/en) on 5 topics.

Usage:
    python experiments/textbook_comparison.py

Output:
    - data/output/textbook_lds_results.json
    - data/output/textbook_graphs.json
    - Console summary with LDS values
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.graph import build_graph
from src.extract import extract_concepts as fallback_extract
from src.scoring import calculate_lds_score

TEXTBOOK_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "textbook")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "output")

TOPICS = ["freedom", "knowledge", "time", "identity", "society"]
LANGS = ["zh", "de", "en"]


def load_textbook(topic, lang):
    path = os.path.join(TEXTBOOK_DIR, f"{lang}_{topic}.txt")
    if not os.path.exists(path):
        print(f"  [WARN] Missing: {path}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def extract_and_build_graph(text, lang):
    result = fallback_extract(text, lang)
    concepts = result["concepts"]
    relations = [(r["from"], r["type"], r["to"]) for r in result.get("relations", [])]
    G = build_graph(concepts, relations)
    return G, result


def run_experiment():
    print("=" * 60)
    print("LinguaGraph Pilot Study: Textbook Comparison")
    print("=" * 60)

    all_results = {}
    all_graphs = {}

    for topic in TOPICS:
        print(f"\n--- Topic: {topic} ---")
        graphs = {}

        for lang in LANGS:
            text = load_textbook(topic, lang)
            if text is None:
                continue

            print(f"  [{lang}] Text length: {len(text)} chars")
            G, extraction = extract_and_build_graph(text, lang)
            graphs[lang] = G
            print(f"  [{lang}] Extracted: {len(extraction['concepts'])} concepts, {len(extraction['relations'])} relations")
            print(f"  [{lang}] Concepts: {extraction['concepts'][:8]}...")

        if len(graphs) >= 2:
            result = compare_three_languages(graphs)
            all_results[topic] = result
            all_graphs[topic] = {lang: list(G.nodes()) for lang, G in graphs.items()}

            print(f"\n  LDS Results:")
            for key, val in result["pairwise"].items():
                print(f"    {key}: LDS={val['language_drift_score']}, "
                      f"GED={val['graph_edit_distance']}, "
                      f"Jaccard={val['node_jaccard']}")
            print(f"  Average LDS: {result['average_lds']}")
        else:
            print(f"  [SKIP] Not enough languages for comparison")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    results_path = os.path.join(OUTPUT_DIR, "textbook_lds_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    graphs_path = os.path.join(OUTPUT_DIR, "textbook_graphs.json")
    with open(graphs_path, "w", encoding="utf-8") as f:
        json.dump(all_graphs, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("Summary: LDS across all topics")
    print("=" * 60)
    for topic, result in all_results.items():
        avg = result["average_lds"]
        print(f"  {topic:12s}: LDS = {avg:.4f}")

    all_lds = [r["average_lds"] for r in all_results.values()]
    overall = sum(all_lds) / len(all_lds) if all_lds else 0
    print(f"\n  Overall average LDS: {overall:.4f}")
    print(f"\nResults saved to: {results_path}")
    print(f"Graphs saved to: {graphs_path}")

    return all_results


if __name__ == "__main__":
    run_experiment()
