"""
LinguaGraph Pilot Study — Corpus Analysis from BWKI Knowledge Base
==================================================================

Analyzes existing BWKI research texts to extract cognitive patterns
across languages and topics.

Usage:
    python experiments/pilot_corpus_analysis.py

Output:
    - data/output/pilot_corpus_lds.json
    - data/output/pilot_corpus_concepts.json
    - Console analysis summary
"""

import json
import os
import sys
import re
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.compare import build_graph, compare_graphs, compare_three_languages
from src.cross_language import build_concept_translations, compute_conceptual_stability

BWKI_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "本地知识库", "知识库内容", "BWKI")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "output")

TOPIC_KEYWORDS = {
    "freedom": {
        "zh": ["自由", "权利", "责任", "民主", "法治"],
        "en": ["freedom", "liberty", "right", "autonomy", "democracy"],
        "de": ["Freiheit", "Recht", "Autonomie", "Demokratie", "Verantwortung"],
    },
    "knowledge": {
        "zh": ["知识", "权力", "学习", "教育", "认知"],
        "en": ["knowledge", "power", "learning", "education", "cognition"],
        "de": ["Wissen", "Macht", "Lernen", "Bildung", "Kognition"],
    },
    "language_thought": {
        "zh": ["语言", "思维", "认知", "概念", "理解"],
        "en": ["language", "thought", "cognition", "concept", "understanding"],
        "de": ["Sprache", "Gedanke", "Kognition", "Konzept", "Verständnis"],
    },
    "bilingualism": {
        "zh": ["双语", "多语", "认知", "语言能力", "迁移"],
        "en": ["bilingual", "multilingual", "cognitive", "transfer", "advantage"],
        "de": ["bilingual", "mehrsprachig", "kognitiv", "Transfer", "Vorteil"],
    },
    "emotion": {
        "zh": ["情感", "情绪", "文化", "表达", "跨文化"],
        "en": ["emotion", "feeling", "culture", "expression", "cross-cultural"],
        "de": ["Emotion", "Gefühl", "Kultur", "Ausdruck", "interkulturell"],
    },
}

EXCLUDE_PATTERNS = [
    r"dark energy", r"cosmolog", r"gravitational", r"quantum",
    r"starr? formation", r"black hole", r"riemann", r"theorem",
    r"scheduling", r"GPU", r"convolver", r"beamforming",
]


def read_kb_entry(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content.strip()


def classify_topic(text, lang):
    text_lower = text.lower() if lang == "en" else text
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        kw_list = keywords.get(lang, keywords.get("en", []))
        score = sum(1 for kw in kw_list if kw.lower() in text_lower)
        scores[topic] = score
    if max(scores.values()) == 0:
        return None
    return max(scores, key=scores.get)


def is_relevant(text):
    text_lower = text.lower()
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, text_lower):
            return False
    return True


def analyze_corpus():
    print("=" * 60)
    print("LinguaGraph Pilot Study: BWKI Corpus Analysis")
    print("=" * 60)

    topic_texts = defaultdict(lambda: {"zh": [], "en": [], "de": []})
    file_count = 0

    for domain in os.listdir(BWKI_DIR):
        domain_path = os.path.join(BWKI_DIR, domain)
        if not os.path.isdir(domain_path) or domain.startswith("."):
            continue
        for filename in os.listdir(domain_path):
            if not filename.endswith(".md"):
                continue
            filepath = os.path.join(domain_path, filename)
            try:
                text = read_kb_entry(filepath)
                if not text or len(text) < 100:
                    continue
                if not is_relevant(text):
                    continue

                lang = "en"
                if any(c > '\u4e00' for c in text[:500]):
                    lang = "zh"
                elif any(c in text[:500] for c in "äöüßÄÖÜ"):
                    lang = "de"

                topic = classify_topic(text, lang)
                if topic and len(topic_texts[topic][lang]) < 25:
                    topic_texts[topic][lang].append({
                        "file": filename,
                        "text": text[:2000],
                        "topic": topic,
                        "lang": lang,
                    })
                    file_count += 1
            except Exception:
                continue

    print(f"\nScanned {file_count} relevant texts across all domains\n")

    print("Text distribution by topic and language:")
    for topic in TOPIC_KEYWORDS:
        counts = {lang: len(topic_texts[topic][lang]) for lang in ["zh", "en", "de"]}
        total = sum(counts.values())
        if total > 0:
            print(f"  {topic:20s}: zh={counts['zh']:3d}, en={counts['en']:3d}, de={counts['de']:3d} (total={total})")

    print("\n" + "=" * 60)
    print("Running concept extraction and LDS computation")
    print("=" * 60)

    from src.extract_v2 import fallback_extract

    results = {}
    concept_stats = defaultdict(Counter)

    for topic in TOPIC_KEYWORDS:
        topic_data = topic_texts[topic]
        if sum(len(v) for v in topic_data.values()) < 6:
            print(f"\n  [{topic}] SKIP — not enough texts")
            continue

        print(f"\n--- Topic: {topic} ---")

        all_concepts = {"zh": Counter(), "en": Counter(), "de": Counter()}
        graphs = {}

        for lang in ["zh", "en", "de"]:
            texts = topic_data[lang]
            if len(texts) < 3:
                continue

            combined_text = "\n".join(t["text"] for t in texts[:15])
            extraction = fallback_extract(combined_text, lang)
            concepts = extraction["concepts"]
            if not concepts:
                print(f"  [{lang}] {len(texts)} texts → 0 concepts (SKIP)")
                continue
            relations = [(r["from"], r["type"], r["to"]) for r in extraction.get("relations", [])]

            G = build_graph(concepts, relations)
            graphs[lang] = G

            for c in concepts:
                all_concepts[lang][c] += 1

            print(f"  [{lang}] {len(texts)} texts → {len(concepts)} concepts: {concepts[:8]}")

        if len(graphs) >= 2:
            result = compare_three_languages(graphs)
            results[topic] = result

            print(f"\n  LDS Results:")
            for key, val in result["pairwise"].items():
                print(f"    {key}: LDS={val['language_drift_score']}, "
                      f"GED={val['graph_edit_distance']}, "
                      f"Jaccard={val['node_jaccard']}")
            print(f"  Average LDS: {result['average_lds']}")

            for lang in ["zh", "en", "de"]:
                if all_concepts[lang]:
                    top5 = all_concepts[lang].most_common(5)
                    concept_stats[topic][lang] = top5

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    lds_path = os.path.join(OUTPUT_DIR, "pilot_corpus_lds.json")
    with open(lds_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    concepts_path = os.path.join(OUTPUT_DIR, "pilot_corpus_concepts.json")
    concepts_output = {}
    for topic in concept_stats:
        concepts_output[topic] = {}
        for lang in ["zh", "en", "de"]:
            if concept_stats[topic][lang]:
                concepts_output[topic][lang] = [
                    {"concept": c, "count": n} for c, n in concept_stats[topic][lang]
                ]
    with open(concepts_path, "w", encoding="utf-8") as f:
        json.dump(concepts_output, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("SUMMARY: LDS across all topics (from real research corpus)")
    print("=" * 60)
    for topic, result in results.items():
        avg = result["average_lds"]
        print(f"  {topic:20s}: LDS = {avg:.4f}")

    all_lds = [r["average_lds"] for r in results.values()]
    if all_lds:
        overall = sum(all_lds) / len(all_lds)
        print(f"\n  Overall average LDS: {overall:.4f}")

    print(f"\nResults saved to: {lds_path}")
    print(f"Concepts saved to: {concepts_path}")

    return results, concepts_output


if __name__ == "__main__":
    analyze_corpus()
