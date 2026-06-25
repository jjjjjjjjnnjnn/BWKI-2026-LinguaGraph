#!/usr/bin/env python3
"""
analyze_human_pilot.py — Human Pilot Data Analysis Pipeline
=============================================================
Reads existing qwen-plus extractions from DB, builds per-(subject, topic, language)
concept graphs, computes Language Drift Score (LDS) between language pairs,
and writes results back to DB + summary JSON.

Uses MOCK mode (no LLM calls) — works entirely from pre-computed extractions.

Usage:
    python scripts/analyze_human_pilot.py                     # Full analysis
    python scripts/analyze_human_pilot.py --verbose           # Detailed output
    python scripts/analyze_human_pilot.py --json-only         # JSON output only, no DB
    python scripts/analyze_human_pilot.py --output results.json # Custom output path

Output:
    - Writes to cross_language_analysis table in linguaGraph.db
    - Writes summary JSON to outputs/human_pilot_lds_results.json
    - Prints per-subject, per-topic LDS summary to stdout
"""

import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Ensure project root is on path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import networkx as nx
from graph import build_graph, graph_to_dict, graph_stats
from scoring import calculate_lds_score, bootstrap_lds_ci

# ============================================================
# CONFIG
# ============================================================

OUTPUT_FILE = PROJECT_ROOT / "outputs" / "human_pilot_lds_results.json"
DB_PATH = PROJECT_ROOT / "linguaGraph.db"
MAPPING_FILE = PROJECT_ROOT / "config" / "cross_language_mapping.json"

# Question ID → Topic mapping
# Each S* participant answered questions covering these 5 social topics
QUESTION_TOPIC_MAP = {
    "q_freedom_boundary": "freedom",
    "q_freedom_words": "freedom",
    "q_freedom_scenario": "freedom",
    "q_justice_def": "justice",
    "q_justice_words": "justice",
    "q_success_def": "success",
    "q_success_words": "success",
    "q_success_scenario": "success",
    "q_resp_relation": "responsibility",
    "q_resp_words": "responsibility",
    "q_home_diff": "home",
    "q_home_words": "home",
    "q_home_scenario": "home",
}

TOPIC_LABELS = {
    "freedom": "Freiheit / 自由 / Freedom",
    "justice": "Gerechtigkeit / 公平 / Justice",
    "success": "Erfolg / 成功 / Success",
    "responsibility": "Verantwortung / 责任 / Responsibility",
    "home": "Heimat / 家 / Home",
}


# ============================================================
# HELPER: load concept mapping
# ============================================================

def load_concept_mapping() -> dict:
    """Load cross-language concept mapping.

    Returns a flat dict: keyword -> shared concept ID.
    Used to align concepts across languages before LDS comparison.
    """
    if not MAPPING_FILE.exists():
        print("  [WARN] concept mapping file not found — using raw string matching")
        return {}

    try:
        with open(MAPPING_FILE, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        print(f"  [WARN] failed to load concept mapping: {exc}")
        return {}

    mapping = {}
    for entry in data.get("mappings", []):
        cid = entry["id"]
        for lang_key in ("zh", "de", "en"):
            for kw in entry.get(lang_key, []):
                mapping[kw.strip()] = cid
                # Also add lowercase version for case-insensitive matching
                mapping[kw.strip().lower()] = cid
    print(f"  [INFO] loaded {len(mapping)} concept mapping entries ({len(data.get('mappings',[]))} shared IDs)")
    return mapping


# ============================================================
# HELPER: DB access (minimal, no external db_utils dependency)
# ============================================================

def get_db():
    """Get database connection with dict-like row access."""
    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def load_extractions(conn, student_ids: list = None) -> list:
    """Load extractions for specified student IDs (or all if None)."""
    if student_ids:
        placeholders = ",".join("?" for _ in student_ids)
        query = f"""
            SELECT e.extraction_id, e.response_id, e.concepts, e.relations,
                   r.student_id, r.language, r.question_id
            FROM extractions e
            JOIN responses r ON e.response_id = r.response_id
            WHERE r.student_id IN ({placeholders})
            ORDER BY r.student_id, r.language, r.question_id
        """
        rows = conn.execute(query, student_ids).fetchall()
    else:
        query = """
            SELECT e.extraction_id, e.response_id, e.concepts, e.relations,
                   r.student_id, r.language, r.question_id
            FROM extractions e
            JOIN responses r ON e.response_id = r.response_id
            WHERE r.student_id LIKE 'S%'
            ORDER BY r.student_id, r.language, r.question_id
        """
        rows = conn.execute(query).fetchall()
    return rows


def parse_concepts(concepts_json: str) -> list:
    """Safely parse concepts JSON field."""
    if not concepts_json:
        return []
    try:
        return json.loads(concepts_json)
    except (json.JSONDecodeError, TypeError):
        return []


def parse_relations(relations_json: str) -> list:
    """Safely parse relations JSON field."""
    if not relations_json:
        return []
    try:
        return json.loads(relations_json)
    except (json.JSONDecodeError, TypeError):
        return []


# ============================================================
# CORE: group extractions → build graphs → compute LDS
# ============================================================

def group_by_student_topic_lang(rows: list) -> dict:
    """Group extractions by (student_id, topic, language).

    Returns:
        dict: {
            (student_id, topic, language): {
                "response_ids": [...],
                "concepts": [concept_str, ...],
                "relations": [...],
            }
        }
    """
    groups = defaultdict(lambda: {"response_ids": [], "concepts": [], "relations": []})

    for row in rows:
        rid = row["response_id"]
        sid = row["student_id"]
        lang = row["language"]
        qid = row["question_id"]

        # Map question_id to topic
        topic = QUESTION_TOPIC_MAP.get(qid)
        if topic is None:
            continue  # skip unmapped questions (control questions, etc.)

        concepts = parse_concepts(row["concepts"])
        relations = parse_relations(row["relations"])

        key = (sid, topic, lang)
        groups[key]["response_ids"].append(rid)
        groups[key]["concepts"].extend(concepts)
        groups[key]["relations"].extend(relations)

    return dict(groups)


def deduplicate_concepts(concept_list: list) -> list:
    """Deduplicate while preserving order."""
    seen = set()
    result = []
    for c in concept_list:
        if c not in seen:
            seen.add(c)
            result.append(c)
    return result


def build_group_graph(group_data: dict) -> nx.DiGraph:
    """Build a directed graph from a group's extracted concepts and relations.

    Uses the same build_graph() function as the textbook pipeline.
    Deduplicates concepts first.
    """
    concepts = deduplicate_concepts(group_data["concepts"])
    relations = group_data["relations"]

    extracted_data = {
        "concepts": concepts,
        "relations": relations,
    }

    return build_graph(extracted_data)


def compute_lds_for_pair(g1: nx.DiGraph, g2: nx.DiGraph,
                         mapping: dict, pair_label: str) -> dict:
    """Compute LDS between two language graphs with bootstrap CI."""
    # Prepare concept mapping for this pair if available
    concept_mapping = mapping if mapping else None

    # Compute LDS (3-component: GED + node Jaccard + edge Jaccard)
    lds_result = calculate_lds_score(g1, g2, concept_mapping=concept_mapping)

    # Bootstrap confidence interval (node-based resampling)
    try:
        lds_boot = bootstrap_lds_ci(g1, g2, concept_mapping=concept_mapping, n_iterations=500)
    except Exception as exc:
        print(f"    [WARN] bootstrap failed for {pair_label}: {exc}")
        lds_boot = {"ci_lower": None, "ci_upper": None, "std_error": None}

    return {
        "lds": lds_result,
        "bootstrap": lds_boot,
    }


# ============================================================
# MAIN ANALYSIS
# ============================================================

def analyze_human_pilot(student_ids: list = None, verbose: bool = False) -> dict:
    """Run the full human pilot analysis.

    Args:
        student_ids: List of student IDs to analyze (None = all S*)
        verbose: Print detailed per-step output

    Returns:
        dict with complete analysis results
    """
    print("\n" + "=" * 60)
    print("  LINGUAGRAPH — HUMAN PILOT LDS ANALYSIS")
    print("=" * 60)

    # --- Load data ---
    conn = get_db()
    try:
        rows = load_extractions(conn, student_ids)
    finally:
        conn.close()

    if not rows:
        print("  [ERROR] No extractions found for human participants")
        return {"error": "no_data"}

    print(f"\n  Loaded {len(rows)} extractions from {len(set(r['student_id'] for r in rows))} participants")
    if verbose:
        for r in rows:
            print(f"    {r['response_id']}: {r['student_id']} | {r['language']} | {r['question_id']}")

    # --- Group by (student, topic, language) ---
    groups = group_by_student_topic_lang(rows)
    n_groups = len(groups)
    n_students = len(set(k[0] for k in groups))
    n_topics = len(set(k[1] for k in groups))

    print(f"  Grouped into {n_groups} (student, topic, language) groups")
    print(f"  Students: {n_students}, Topics: {n_topics}")
    print(f"  Languages in data: {sorted(set(k[2] for k in groups))}")

    # --- Build concept mapping ---
    mapping = load_concept_mapping()

    # --- Build graphs for each group ---
    graphs = {}
    group_stats_list = []

    for key, gdata in sorted(groups.items()):
        sid, topic, lang = key
        G = build_group_graph(gdata)
        graphs[key] = G
        stats = graph_stats(G)

        group_stats_list.append({
            "student_id": sid,
            "topic": topic,
            "language": lang,
            "node_count": stats["nodes"],
            "edge_count": stats["edges"],
            "density": stats["density"],
            "response_count": len(gdata["response_ids"]),
            "concept_count": len(deduplicate_concepts(gdata["concepts"])),
        })

        if verbose:
            print(f"\n  [GRAPH] {sid} | {topic} | {lang}")
            print(f"          nodes={stats['nodes']} edges={stats['edges']} concepts={len(deduplicate_concepts(gdata['concepts']))}")

    # --- Compute LDS for each (student, topic) with 2+ languages ---
    comparisons = []
    lds_matrix = defaultdict(dict)  # {(sid, topic): {lang_pair: lds}}

    # Group by (student, topic)
    st_groups = defaultdict(dict)
    for key, G in graphs.items():
        sid, topic, lang = key
        st_groups[(sid, topic)][lang] = G

    for (sid, topic), lang_graphs in sorted(st_groups.items()):
        langs = sorted(lang_graphs.keys())
        if len(langs) < 2:
            if verbose:
                print(f"\n  [SKIP] {sid} | {topic}: only {langs[0]} available (need 2+ languages)")
            continue

        if verbose:
            print(f"\n  --- {sid} | {TOPIC_LABELS.get(topic, topic)} ---")

        for i in range(len(langs)):
            for j in range(i + 1, len(langs)):
                l1 = langs[i]
                l2 = langs[j]
                pair = f"{l1}-{l2}"
                pair_label = f"{sid} | {topic} | {pair}"

                g1 = lang_graphs[l1]
                g2 = lang_graphs[l2]

                # Compute LDS
                result = compute_lds_for_pair(g1, g2, mapping, pair_label)
                lds_val = result["lds"]["lds_score"]

                if verbose:
                    print(f"    {pair}: LDS={lds_val:.4f} "
                          f"(GED={result['lds']['ged_similarity']:.4f} "
                          f"NodeJac={result['lds']['jaccard_node']:.4f} "
                          f"EdgeJac={result['lds']['jaccard_edge']:.4f})")

                # Store
                comparisons.append({
                    "student_id": sid,
                    "topic": topic,
                    "lang_pair": pair,
                    "lang_1": l1,
                    "lang_2": l2,
                    "lds_score": lds_val,
                    "combined_similarity": result["lds"]["combined_similarity"],
                    "ged_similarity": result["lds"]["ged_similarity"],
                    "jaccard_node": result["lds"]["jaccard_node"],
                    "jaccard_edge": result["lds"]["jaccard_edge"],
                    "shared_nodes": result["lds"]["shared_nodes"],
                    "shared_edges": result["lds"]["shared_edges"],
                    "total_unique_nodes": result["lds"]["total_unique_nodes"],
                    "l1_nodes": result["lds"]["l1_nodes"],
                    "l2_nodes": result["lds"]["l2_nodes"],
                    "l1_edges": result["lds"]["l1_edges"],
                    "l2_edges": result["lds"]["l2_edges"],
                    "ci_lower": result["bootstrap"]["ci_lower"],
                    "ci_upper": result["bootstrap"]["ci_upper"],
                    "std_error": result["bootstrap"]["std_error"],
                    "details": result["lds"],
                })
                lds_matrix[(sid, topic)][pair] = lds_val

    # --- Summary statistics ---
    if comparisons:
        lds_values = [c["lds_score"] for c in comparisons]
        mean_lds = sum(lds_values) / len(lds_values)
        min_lds = min(lds_values)
        max_lds = max(lds_values)

        # Per language pair
        from collections import Counter
        pair_counts = Counter(c["lang_pair"] for c in comparisons)
        pair_means = {}
        for pair in pair_counts:
            vals = [c["lds_score"] for c in comparisons if c["lang_pair"] == pair]
            pair_means[pair] = sum(vals) / len(vals)

        print(f"\n  {'='*50}")
        print(f"  SUMMARY")
        print(f"  {'='*50}")
        print(f"  Total LDS comparisons: {len(comparisons)}")
        print(f"  Mean LDS: {mean_lds:.4f}")
        print(f"  Min LDS: {min_lds:.4f}")
        print(f"  Max LDS: {max_lds:.4f}")
        print(f"")
        for pair in sorted(pair_means):
            print(f"  {pair}: mean LDS={pair_means[pair]:.4f} (n={pair_counts[pair]})")

        # Per topic
        topic_counts = Counter(c["topic"] for c in comparisons)
        topic_means = {}
        for topic in topic_counts:
            vals = [c["lds_score"] for c in comparisons if c["topic"] == topic]
            topic_means[topic] = sum(vals) / len(vals)

        print(f"")
        for topic in sorted(topic_means):
            print(f"  {TOPIC_LABELS.get(topic, topic)}: mean LDS={topic_means[topic]:.4f} (n={topic_counts[topic]})")
    else:
        print(f"\n  [WARN] No cross-language comparisons possible")
        mean_lds = None

    # --- Build result object ---
    result = {
        "metadata": {
            "pipeline": "analyze_human_pilot.py",
            "timestamp": datetime.now().isoformat(),
            "n_extractions": len(rows),
            "n_groups": n_groups,
            "n_students": n_students,
            "n_topics": n_topics,
            "n_comparisons": len(comparisons),
            "model_used": "qwen-plus (batch) — pre-existing extractions",
            "lds_formula": "LDS = 1 - mean(GED_sim, Node_Jaccard, Edge_Jaccard)",
        },
        "group_stats": group_stats_list,
        "comparisons": comparisons,
        "summary": {
            "mean_lds": round(mean_lds, 4) if mean_lds else None,
            "min_lds": round(min_lds, 4) if comparisons else None,
            "max_lds": round(max_lds, 4) if comparisons else None,
            "n_comparisons": len(comparisons),
            "pair_means": {k: round(v, 4) for k, v in pair_means.items()},
            "topic_means": {k: round(v, 4) for k, v in topic_means.items()},
        },
    }

    return result


# ============================================================
# DB WRITE
# ============================================================

def write_to_db(conn, comparisons: list):
    """Write LDS results to cross_language_analysis table."""
    from db_utils import insert

    written = 0
    errors = 0

    for c in comparisons:
        aid = f"A_HUMAN_{c['student_id']}_{c['topic']}_{c['lang_pair']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            insert(conn, "cross_language_analysis", {
                "analysis_id": aid,
                "student_id": c["student_id"],
                "lang_pair": c["lang_pair"],
                "topic": c["topic"],
                "lcd_score": c["lds_score"],
                "graph_similarity": c["combined_similarity"],
                "concept_shift_count": c.get("concept_shift_count", c["total_unique_nodes"] - c["shared_nodes"]),
                "relation_shift_count": 0,
                "shared_concepts": c["shared_nodes"],
                "unique_l1_concepts": c["l1_nodes"] - c["shared_nodes"],
                "unique_l2_concepts": c["l2_nodes"] - c["shared_nodes"],
                "details_json": json.dumps(c["details"], ensure_ascii=False),
            })
            written += 1
        except Exception as exc:
            print(f"  [ERROR] DB write failed for {aid}: {exc}")
            errors += 1

    return written, errors


# ============================================================
# MAIN
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze human pilot data — build graphs and compute LDS from existing extractions"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Detailed per-step output")
    parser.add_argument("--json-only", action="store_true", help="JSON output only, skip DB write")
    parser.add_argument("--output", type=str, default=str(OUTPUT_FILE),
                        help=f"Output JSON path (default: {OUTPUT_FILE})")
    parser.add_argument("--students", type=str, nargs="*", default=None,
                        help="Specific students to analyze (default: all S*)")
    args = parser.parse_args()

    # Ensure output dir exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Run analysis
    t_start = time.time()
    result = analyze_human_pilot(student_ids=args.students, verbose=args.verbose)
    elapsed = time.time() - t_start

    # Write JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n  [OK] Results written to {output_path}")

    # Write to DB (unless --json-only)
    if not args.json_only and not result.get("error"):
        import sqlite3
        conn = sqlite3.connect(str(DB_PATH))
        try:
            written, errors = write_to_db(conn, result["comparisons"])
            conn.commit()
            print(f"  [OK] DB: {written} written, {errors} errors")
        finally:
            conn.close()

    print(f"\n  Elapsed: {elapsed:.1f}s")
    print(f"  {'='*60}\n")


if __name__ == "__main__":
    main()
