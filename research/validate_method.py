"""
LinguaGraph Method Validation — Concept Mapping + LDS Re-computation
=====================================================================

Re-runs the analysis with concept mapping to verify:
1. Jaccard is no longer 0
2. LDS rankings are stable
3. Success still shows highest drift

Usage:
    python research/validate_method.py
"""

import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from src.compare import build_graph, compare_graphs, compare_three_languages
from src.extract_v2 import fallback_extract
from concept_mapping import map_concepts, CONCEPT_MAP

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "pilot_dataset", "education")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "findings")

TOPICS = ["freedom", "responsibility", "success", "home"]
LANGS = ["zh", "en", "de"]


def load_texts(topic, lang):
    topic_dir = os.path.join(DATASET_DIR, topic)
    if not os.path.isdir(topic_dir):
        return []
    texts = []
    for f in os.listdir(topic_dir):
        if f.endswith(".json") and f.startswith(f"{lang}_"):
            try:
                with open(os.path.join(topic_dir, f), "r", encoding="utf-8") as fh:
                    entry = json.load(fh)
                if entry.get("content") and len(entry["content"]) > 50:
                    texts.append(entry)
            except Exception:
                continue
    return texts


def extract_and_map(texts, lang, use_mapping=True):
    combined = "\n".join(t["content"][:500] for t in texts[:20])
    extraction = fallback_extract(combined, lang)
    raw_concepts = extraction["concepts"]

    if use_mapping:
        mapped_concepts = map_concepts(raw_concepts)
    else:
        mapped_concepts = raw_concepts

    return raw_concepts, mapped_concepts


def run_validation():
    print("=" * 60)
    print("Method Validation: Concept Mapping + LDS")
    print("=" * 60)

    results = {}

    for topic in TOPICS:
        print(f"\n--- {topic} ---")

        graphs_raw = {}
        graphs_mapped = {}
        raw_concepts_all = {}
        mapped_concepts_all = {}

        for lang in LANGS:
            texts = load_texts(topic, lang)
            if len(texts) < 3:
                print(f"  [{lang}] SKIP ({len(texts)} texts)")
                continue

            raw, mapped = extract_and_map(texts, lang)
            raw_concepts_all[lang] = raw
            mapped_concepts_all[lang] = mapped

            G_raw = build_graph(raw, [])
            G_mapped = build_graph(mapped, [])
            graphs_raw[lang] = G_raw
            graphs_mapped[lang] = G_mapped

            print(f"  [{lang}] raw={len(raw)} mapped={len(mapped)}: {mapped[:6]}")

        if len(graphs_mapped) < 2:
            continue

        result_raw = compare_three_languages(graphs_raw)
        result_mapped = compare_three_languages(graphs_mapped)

        print(f"\n  WITHOUT mapping:")
        for key, val in result_raw["pairwise"].items():
            print(f"    {key}: LDS={val['language_drift_score']}, Jaccard={val['node_jaccard']}")
        print(f"  Average LDS: {result_raw['average_lds']}")

        print(f"\n  WITH mapping:")
        for key, val in result_mapped["pairwise"].items():
            print(f"    {key}: LDS={val['language_drift_score']}, Jaccard={val['node_jaccard']}")
        print(f"  Average LDS: {result_mapped['average_lds']}")

        results[topic] = {
            "raw": result_raw,
            "mapped": result_mapped,
            "concepts": {
                lang: {"raw": raw_concepts_all.get(lang, []), "mapped": mapped_concepts_all.get(lang, [])}
                for lang in LANGS
            },
        }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "method_validation.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")
    print(f"{'Topic':15s} {'LDS_raw':>10s} {'LDS_mapped':>12s} {'Jac_raw':>10s} {'Jac_mapped':>12s}")
    print("-" * 60)
    for topic, r in results.items():
        lds_raw = r["raw"]["average_lds"]
        lds_mapped = r["mapped"]["average_lds"]
        jac_raw = 0
        jac_mapped = 0
        for key, val in r["raw"]["pairwise"].items():
            jac_raw += val["node_jaccard"]
        for key, val in r["mapped"]["pairwise"].items():
            jac_mapped += val["node_jaccard"]
        n = len(r["raw"]["pairwise"])
        jac_raw /= n if n else 1
        jac_mapped /= n if n else 1
        print(f"{topic:15s} {lds_raw:10.4f} {lds_mapped:12.4f} {jac_raw:10.4f} {jac_mapped:12.4f}")

    print(f"\nResults saved: {out_path}")
    return results


if __name__ == "__main__":
    run_validation()
