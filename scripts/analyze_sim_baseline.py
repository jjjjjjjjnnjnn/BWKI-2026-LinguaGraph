#!/usr/bin/env python3
"""
analyze_sim_baseline.py — Simulation Baseline: Computational LDS Distribution
============================================================================
Runs mock extraction on 300 SIM responses, builds per-(topic, language) graphs,
computes LDS between language pairs, and produces a statistical baseline.

Purpose:
    The simulation baseline serves as a "null model" for human LDS comparison.
    If human LDS > simulation LDS, then cross-language structural divergence
    exceeds random expectation, validating that human LDS reflects genuine
    cognitive differences rather than measurement noise.

Usage:
    python scripts/analyze_sim_baseline.py                    # Full analysis
    python scripts/analyze_sim_baseline.py --verbose          # Detailed output
    python scripts/analyze_sim_baseline.py --output results.json  # Custom output
    python scripts/analyze_sim_baseline.py --by-response      # Per-response LDS distribution

Output:
    - Summary JSON to outputs/sim_baseline_lds.json
    - Print comparison with human LDS
"""

import json, sys, time, sqlite3, random
from collections import defaultdict
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

import networkx as nx
from graph import build_graph, graph_stats
from scoring import calculate_lds_score, bootstrap_lds_ci

# Config
DB_PATH = PROJECT_ROOT / "linguaGraph.db"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "sim_baseline_lds.json"
MAPPING_FILE = PROJECT_ROOT / "config" / "cross_language_mapping.json"
SEED = 42

# Topic mapping (SIM uses q1-q5)
QUESTION_TOPIC_MAP = {
    "q1": "freedom", "q2": "justice", "q3": "success",
    "q4": "responsibility", "q5": "home",
}
TOPIC_LABELS = {
    "freedom": "Freedom", "justice": "Justice", "success": "Success",
    "responsibility": "Responsibility", "home": "Home",
}


def load_concept_mapping():
    mapping = {}
    if MAPPING_FILE.exists():
        with open(MAPPING_FILE, encoding="utf-8") as f:
            data = json.load(f)
        for entry in data.get("mappings", []):
            cid = entry["id"]
            for lang_key in ("zh", "de", "en"):
                for kw in entry.get(lang_key, []):
                    mapping[kw.strip()] = cid
                    mapping[kw.strip().lower()] = cid
    return mapping


def mock_extract(text: str, lang: str) -> dict:
    """Mock extraction: extract concepts by simple keyword matching.

    This mimics the qwen-plus extraction behavior without API calls.
    Uses language-specific keyword lists and simple text matching.
    """
    # Language-specific concept keywords (from extraction patterns)
    KEYWORDS = {
        "zh": {
            "freedom": ["自由", "权利", "选择", "独立", "平等", "责任", "自律", "民主", "人权", "解放"],
            "justice": ["公平", "正义", "平等", "法律", "权利", "社会", "分配", "教育", "机会", "和谐"],
            "success": ["成功", "努力", "成就", "家庭", "目标", "幸福", "财富", "社会", "事业", "教育"],
            "responsibility": ["责任", "义务", "道德", "家庭", "社会", "选择", "担当", "法律", "良心", "承诺"],
            "home": ["家", "家庭", "归属", "温暖", "安全", "亲人", "爱", "回忆", "传统", "根"],
        },
        "de": {
            "freedom": ["Freiheit", "Recht", "Selbstbestimmung", "Unabhängigkeit", "Gleichheit", "Verantwortung", "Demokratie", "Menschenwürde", "Autonomie", "Grenze"],
            "justice": ["Gerechtigkeit", "Gleichheit", "Recht", "Gesetz", "Menschenwürde", "Freiheit", "Solidarität", "Ordnung", "Verfahren", "Urteil"],
            "success": ["Erfolg", "Leistung", "Karriere", "Ziel", "Glück", "Wohlstand", "Bildung", "Arbeit", "Familie", "Zufriedenheit"],
            "responsibility": ["Verantwortung", "Pflicht", "Freiheit", "Gewissen", "Gesellschaft", "Familie", "Recht", "moralisch", "Sorge", "Gemeinschaft"],
            "home": ["Heimat", "Familie", "Zuhause", "Geborgenheit", "Sicherheit", "Herkunft", "Tradition", "Identität", "Nest", "Wohnort"],
        },
        "en": {
            "freedom": ["freedom", "rights", "choice", "liberty", "equality", "responsibility", "democracy", "individual", "autonomy", "independence"],
            "justice": ["justice", "equality", "fairness", "rights", "law", "society", "opportunity", "education", "freedom", "democracy"],
            "success": ["success", "achievement", "goal", "happiness", "wealth", "education", "career", "family", "effort", "opportunity"],
            "responsibility": ["responsibility", "duty", "accountability", "choice", "society", "family", "moral", "obligation", "commitment", "trust"],
            "home": ["home", "family", "love", "safety", "comfort", "belonging", "memory", "warmth", "childhood", "community"],
        }
    }

    concepts = []
    text_lower = text.lower()

    # Determine topic from text content (fallback heuristic)
    for lang_key, topics in KEYWORDS.items():
        if lang_key == lang:
            for topic, keywords in topics.items():
                for kw in keywords:
                    if kw.lower() in text_lower:
                        concepts.append(kw)
                    elif kw in text:  # case-sensitive check for capitalized German
                        concepts.append(kw)

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for c in concepts:
        if c not in seen:
            seen.add(c)
            deduped.append(c)

    return {"concepts": deduped[:8], "relations": []}  # cap at 8 concepts


def load_sim_responses():
    """Load all SIM responses from DB, grouped by (topic, language)."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT student_id, language, question_id, answer_text
        FROM responses
        WHERE student_id LIKE 'SIM_%'
        ORDER BY student_id
    """).fetchall()
    conn.close()

    # Group by (topic, language)
    groups = defaultdict(lambda: {"texts": [], "n": 0, "student_ids": []})
    lang_counts = defaultdict(int)

    for row in rows:
        sid = row["student_id"]
        lang = row["language"]
        qid = row["question_id"]
        text = row["answer_text"]

        topic = QUESTION_TOPIC_MAP.get(qid)
        if topic is None:
            continue

        key = (topic, lang)
        groups[key]["texts"].append(text)
        groups[key]["n"] += 1
        groups[key]["student_ids"].append(sid)
        lang_counts[lang] += 1

    return dict(groups), dict(lang_counts)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Simulation baseline LDS analysis")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--output", type=str, default=str(OUTPUT_FILE))
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    random.seed(args.seed)

    print("\n" + "=" * 60)
    print("  SIMULATION BASELINE — LDS DISTRIBUTION")
    print("=" * 60)

    # Load data
    groups, lang_counts = load_sim_responses()
    print(f"\n  Loaded {sum(g['n'] for g in groups.values())} SIM responses")
    print(f"  Languages: {dict(lang_counts)}")
    topics = sorted(set(k[0] for k in groups))
    print(f"  Topics: {len(topics)}")
    for t in topics:
        for l in ['zh', 'de', 'en']:
            key = (t, l)
            if key in groups:
                print(f"    {t:<15s} | {l}: {groups[key]['n']} responses")

    # Mock extraction + graph building
    mapping = load_concept_mapping()
    graph_index = {}

    for key, gdata in sorted(groups.items()):
        topic, lang = key

        # Run mock extraction on each text
        all_concepts = []
        for text in gdata["texts"]:
            extracted = mock_extract(text, lang)
            all_concepts.extend(extracted["concepts"])

        # Deduplicate
        seen = set()
        deduped = []
        for c in all_concepts:
            if c not in seen:
                seen.add(c)
                deduped.append(c)

        extracted = {"concepts": deduped, "relations": []}
        G = build_graph(extracted)
        graph_index[key] = G

        if args.verbose:
            print(f"\n  [GRAPH] {topic:<15s} | {lang}: {G.number_of_nodes()} concepts from {gdata['n']} responses")

    # Compute LDS for each topic across language pairs
    comparisons = []

    for topic in topics:
        available = {}
        for lang in ['zh', 'de', 'en']:
            key = (topic, lang)
            if key in graph_index:
                available[lang] = graph_index[key]

        langs = sorted(available.keys())
        if len(langs) < 2:
            continue

        print(f"\n  --- {TOPIC_LABELS.get(topic, topic)} ---")
        for lang in langs:
            print(f"      {lang}: {available[lang].number_of_nodes()} concepts")

        for i in range(len(langs)):
            for j in range(i + 1, len(langs)):
                l1, l2 = langs[i], langs[j]
                pair = f"{l1}-{l2}"

                result = calculate_lds_score(available[l1], available[l2],
                                              concept_mapping=mapping if mapping else None)

                print(f"      {pair}: LDS={result['lds_score']:.4f} "
                      f"(NodeJac={result['jaccard_node']:.4f} "
                      f"EdgeJac={result['jaccard_edge']:.4f})")

                comparisons.append({
                    "topic": topic,
                    "lang_pair": pair,
                    "lds_score": result["lds_score"],
                    "ged_similarity": result["ged_similarity"],
                    "jaccard_node": result["jaccard_node"],
                    "jaccard_edge": result["jaccard_edge"],
                    "shared_nodes": result["shared_nodes"],
                    "total_unique_nodes": result["total_unique_nodes"],
                    "l1_nodes": result["l1_nodes"],
                    "l2_nodes": result["l2_nodes"],
                })

    # Summary
    if comparisons:
        lds_vals = [c["lds_score"] for c in comparisons]

        # Per pair
        from collections import Counter
        pc = Counter(c["lang_pair"] for c in comparisons)

        print(f"\n  {'='*50}")
        print(f"  SIMULATION BASELINE SUMMARY")
        print(f"  {'='*50}")
        print(f"  Total comparisons: {len(comparisons)}")
        print(f"  Mean LDS: {sum(lds_vals)/len(lds_vals):.4f}")
        print(f"  Range: [{min(lds_vals):.4f}, {max(lds_vals):.4f}]")
        print(f"  SD: {__import__('statistics').stdev(lds_vals):.4f}")
        print(f"")
        for pair in sorted(pc):
            vals = [c["lds_score"] for c in comparisons if c["lang_pair"] == pair]
            print(f"  {pair}: mean LDS={sum(vals)/len(vals):.4f} (n={pc[pair]})")

        # Comparison with human between-subject LDS
        print(f"\n  {'='*50}")
        print(f"  COMPARISON: SIMULATION vs HUMAN")
        print(f"  {'='*50}")
        print(f"  {'Pair':<10s} {'Sim LDS':<10s} {'Human LDS':<12s} {'Diff':<10s}")
        print(f"  {'-'*42}")
        sim_mean = sum(lds_vals)/len(lds_vals)

        # Load human between-subject LDS for comparison
        human_file = PROJECT_ROOT / "outputs" / "human_pilot_between_lds.json"
        human_data = {}
        if human_file.exists():
            with open(human_file) as f:
                hd = json.load(f)
            for c in hd.get("comparisons", []):
                pair = c["lang_pair"]
                if pair not in human_data:
                    human_data[pair] = []
                human_data[pair].append(c["lds_score"])

        for pair in sorted(pc):
            sim_v = sum(c["lds_score"] for c in comparisons if c["lang_pair"] == pair) / pc[pair]
            human_v = sum(human_data.get(pair, [0])) / max(len(human_data.get(pair, [1])), 1) if pair in human_data else None
            diff = sim_v - human_v if human_v else None
            diff_str = f"{diff:+.4f}" if diff else "N/A"
            human_str = f"{human_v:.4f}" if human_v else "N/A"
            print(f"  {pair:<10s} {sim_v:<10.4f} {human_str:<12s} {diff_str:<10s}")

        sim_mean = sum(lds_vals)/len(lds_vals)
        human_mean = sum(sum(human_data.get(p, [])) for p in human_data) / max(sum(len(human_data.get(p, [])) for p in human_data), 1) if human_data else None
        if human_mean:
            print(f"  {'-'*42}")
            print(f"  {'Overall':<10s} {sim_mean:<10.4f} {human_mean:<12.4f} {sim_mean-human_mean:+.4f}")

    else:
        print(f"\n  [WARN] No comparisons possible")

    # Save output
    result = {
        "metadata": {
            "pipeline": "analyze_sim_baseline.py",
            "timestamp": datetime.now().isoformat(),
            "n_responses": sum(groups[k]["n"] for k in groups),
            "n_comparisons": len(comparisons),
            "extraction_method": "mock (keyword-based, no API calls)",
            "seed": args.seed,
        },
        "comparisons": comparisons,
        "summary": {
            "mean_lds": round(sum(c["lds_score"] for c in comparisons) / max(len(comparisons), 1), 4),
            "n_comparisons": len(comparisons),
        } if comparisons else {"mean_lds": None},
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n  [OK] Output written to {output_path}")
    print(f"  {'='*60}\n")


if __name__ == "__main__":
    main()
