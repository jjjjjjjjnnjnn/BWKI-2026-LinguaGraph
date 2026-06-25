#!/usr/bin/env python3
"""
analyze_human_between.py — Between-Subject Group LDS Analysis
==============================================================
Aggregates concepts by language group (ZH-native vs DE-native vs EN-native)
for each social topic, then computes LDS between group-level graphs.

Usage:
    python scripts/analyze_human_between.py
    python scripts/analyze_human_between.py --verbose
    python scripts/analyze_human_between.py --output results_between.json

Output:
    - Writes summary JSON to outputs/human_pilot_between_lds.json
    - Prints per-topic cross-language LDS summary
"""

import json, sys, time, sqlite3
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
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "human_pilot_between_lds.json"
MAPPING_FILE = PROJECT_ROOT / "config" / "cross_language_mapping.json"

QUESTION_TOPIC_MAP = {
    "q_freedom_boundary": "freedom", "q_freedom_words": "freedom", "q_freedom_scenario": "freedom",
    "q_justice_def": "justice", "q_justice_words": "justice",
    "q_success_def": "success", "q_success_words": "success", "q_success_scenario": "success",
    "q_resp_relation": "responsibility", "q_resp_words": "responsibility",
    "q_home_diff": "home", "q_home_words": "home", "q_home_scenario": "home",
}

TOPIC_LABELS = {
    "freedom": "Freedom", "justice": "Justice", "success": "Success",
    "responsibility": "Responsibility", "home": "Home",
}

# Participant → language group mapping
# ZH-native: only ZH responses
# DE-native: only DE responses (native language)
# EN-native: only EN responses (native language)
LANG_GROUPS = {
    "S001": "zh", "S004": "zh", "S007": "zh",  # ZH-native → ZH
    "S002": "de", "S005": "de", "S008": "de",  # DE-native → DE
    "S003": "en", "S006": "en",                 # EN-native → EN
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

def load_native_responses():
    """Load extractions grouped by native language group + topic."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT r.student_id, r.language, r.question_id, e.concepts
        FROM responses r
        JOIN extractions e ON r.response_id = e.response_id
        WHERE r.student_id LIKE 'S%'
        ORDER BY r.student_id, r.question_id
    """).fetchall()
    conn.close()

    # Group by (native_lang_group, topic)
    groups = defaultdict(lambda: {"concepts": [], "participants": set()})

    for row in rows:
        sid = row["student_id"]
        native_group = LANG_GROUPS.get(sid)
        qid = row["question_id"]
        topic = QUESTION_TOPIC_MAP.get(qid)

        if native_group is None or topic is None:
            continue

        # Only use responses in the participant's native language
        resp_lang = row["language"]
        if resp_lang != native_group:
            continue

        concepts = []
        if row["concepts"]:
            try:
                concepts = json.loads(row["concepts"])
            except:
                concepts = []

        key = (native_group, topic)
        groups[key]["concepts"].extend(concepts)
        groups[key]["participants"].add(sid)

    # Deduplicate and build graphs
    graphs = {}
    group_stats = []

    for (lang, topic), gdata in sorted(groups.items()):
        concepts = list(dict.fromkeys(gdata["concepts"]))  # dedup, preserve order
        extracted = {"concepts": concepts, "relations": []}
        G = build_graph(extracted)
        graphs[(lang, topic)] = G
        group_stats.append({
            "language": lang, "topic": topic,
            "n_participants": len(gdata["participants"]),
            "participants": sorted(gdata["participants"]),
            "n_concepts": len(concepts),
            "n_nodes": G.number_of_nodes(),
            "n_edges": G.number_of_edges(),
        })

    return graphs, group_stats

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Between-subject group LDS analysis")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--output", type=str, default=str(OUTPUT_FILE))
    args = parser.parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 60)
    print("  BETWEEN-SUBJECT GROUP LDS ANALYSIS")
    print("=" * 60)

    graphs, group_stats = load_native_responses()
    mapping = load_concept_mapping()

    print(f"\n  Groups: {len(graphs)} (language × topic)")
    if args.verbose:
        for gs in sorted(group_stats, key=lambda x: (x["language"], x["topic"])):
            print(f"  {gs['language']} | {gs['topic']:<15s}: {gs['n_participants']} participants, {gs['n_concepts']} concepts")

    # Compute LDS for each topic across language pairs
    topics = set(k[1] for k in graphs)
    comparisons = []

    for topic in sorted(topics):
        # Get graphs for each language that has this topic
        available = {}
        for (lang, t), G in graphs.items():
            if t == topic:
                available[lang] = G

        langs = sorted(available.keys())
        if len(langs) < 2:
            print(f"\n  [SKIP] {topic}: only {langs} available")
            continue

        print(f"\n  --- {TOPIC_LABELS.get(topic, topic)} ---")
        print(f"      Languages: {langs}")
        for gs in group_stats:
            if gs["topic"] == topic:
                print(f"      {gs['language']}: {gs['n_participants']} participants, {gs['n_concepts']} unique concepts")

        for i in range(len(langs)):
            for j in range(i + 1, len(langs)):
                l1, l2 = langs[i], langs[j]
                pair = f"{l1}-{l2}"

                result = calculate_lds_score(available[l1], available[l2], concept_mapping=mapping if mapping else None)
                try:
                    boot = bootstrap_lds_ci(available[l1], available[l2], concept_mapping=mapping if mapping else None, n_iterations=500)
                except:
                    boot = {"ci_lower": None, "ci_upper": None, "std_error": None}

                print(f"      {pair}: LDS={result['lds_score']:.4f} "
                      f"(GED={result['ged_similarity']:.4f} "
                      f"NodeJac={result['jaccard_node']:.4f} "
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
        print(f"\n  {'='*50}")
        print(f"  SUMMARY")
        print(f"  {'='*50}")
        print(f"  Total comparisons: {len(comparisons)}")
        print(f"  Mean LDS: {sum(lds_vals)/len(lds_vals):.4f}")
        print(f"  Range: [{min(lds_vals):.4f}, {max(lds_vals):.4f}]")

        # Per pair
        from collections import Counter
        pc = Counter(c["lang_pair"] for c in comparisons)
        for pair in sorted(pc):
            vals = [c["lds_score"] for c in comparisons if c["lang_pair"] == pair]
            print(f"  {pair}: {sum(vals)/len(vals):.4f} (n={pc[pair]})")

    # Write output
    result = {
        "metadata": {
            "pipeline": "analyze_human_between.py",
            "timestamp": datetime.now().isoformat(),
            "n_comparisons": len(comparisons),
        },
        "group_stats": group_stats,
        "comparisons": comparisons,
        "summary": {
            "mean_lds": round(sum(c["lds_score"] for c in comparisons) / max(len(comparisons), 1), 4),
            "n_comparisons": len(comparisons),
        } if comparisons else {"mean_lds": None, "n_comparisons": 0},
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n  [OK] Written to {output_path}")
    print(f"  {'='*60}\n")

if __name__ == "__main__":
    main()
