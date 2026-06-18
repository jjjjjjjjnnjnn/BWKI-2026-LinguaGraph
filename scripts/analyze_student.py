"""
Analyze Student — Full Cross-Language Analysis
==================================================
Reads a student's trilingual responses from the database,
runs the full analysis pipeline, and writes results back.

Usage:
    python analyze_student.py --student S001          # Analyze one student
    python analyze_student.py --student S001 --mock   # Use mock extraction (no LLM)
    python analyze_student.py --student S001 --verbose # Show detailed output
    python analyze_student.py --all                   # Analyze all students
    python analyze_student.py --list                  # List available students
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))  # project root for db_utils
from db_utils import get_connection, query, query_one, insert, upsert

# Import existing pipeline modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from extract import extract_concepts
from graph import build_graph, graph_to_dict, graph_stats
from cross_language import detect_cross_language_gaps, GapType
from scoring import calculate_lds_score, bootstrap_lds_ci, calculate_concept_f1, calculate_relation_f1

try:
    import networkx as nx
except ImportError:
    nx = None


def load_concept_mapping() -> Dict[str, str]:
    """
    Load cross-language concept mapping from config.
    Returns a dict mapping each language-specific keyword to its shared concept ID.
    Used to align concepts across languages before LDS comparison.
    """
    mapping_file = Path(__file__).parent.parent / "config" / "cross_language_mapping.json"
    if not mapping_file.exists():
        print("  [WARN] Concept mapping file not found — LDS will use raw string matching")
        return {}

    with open(mapping_file, encoding="utf-8") as f:
        data = json.load(f)

    mapping = {}
    for entry in data.get("mappings", []):
        cid = entry["id"]
        for lang_key in ("zh", "de", "en"):
            for kw in entry.get(lang_key, []):
                mapping[kw] = cid
    return mapping


def get_student_responses(conn, student_id: str) -> Dict[str, List]:
    """Get all responses for a student, grouped by language."""
    rows = query(conn, """
        SELECT r.response_id, r.language, r.question_id, r.answer_text,
               q.questions as questionnaire_json
        FROM responses r
        LEFT JOIN questionnaires q ON r.questionnaire_id = q.questionnaire_id
        WHERE r.student_id = ?
        ORDER BY r.language, r.question_id
    """, (student_id,))

    grouped = {}
    for r in rows:
        lang = r["language"]
        if lang not in grouped:
            grouped[lang] = []
        grouped[lang].append(r)

    return grouped


def get_expert_graph_for_topic(conn, topic: str) -> "nx.DiGraph":
    """Get expert graph for a given topic from the database."""
    expert = query_one(conn,
        "SELECT concepts, relations FROM expert_graphs WHERE domain='social_issues'")
    if not expert or nx is None:
        return nx.DiGraph()

    concepts = json.loads(expert["concepts"])
    relations = json.loads(expert["relations"])

    G = nx.DiGraph()
    for c in concepts:
        G.add_node(c.get("zh", c.get("name", "")),
                   de=c.get("de", ""), en=c.get("en", ""),
                   category=c.get("category", "concept"))

    topic_node = None
    topic_map = {"q1": "自由", "q2": "公平", "q3": "成功", "q4": "家庭"}
    zh_topic = topic_map.get(topic, topic)

    for r in relations:
        from_id = r.get("from", "")
        to_id = r.get("to", "")
        # Resolve IDs to concept names
        from_name = None
        to_name = None
        for c in concepts:
            cid = c.get("id", "")
            if cid == from_id:
                from_name = c.get("zh", "")
            if cid == to_id:
                to_name = c.get("zh", "")

        if from_name and to_name and from_name in G and to_name in G:
            G.add_edge(from_name, to_name, relation=r.get("type", "relates_to"),
                       importance=r.get("importance", 0.5))

    return G


def analyze_student_responses(
    conn,
    student_id: str,
    use_mock: bool = True,
    verbose: bool = False
) -> Dict:
    """Run the full cross-language analysis for a student."""
    print(f"\n{'='*50}")
    print(f"  Analyzing Student: {student_id}")
    print(f"{'='*50}")

    # Step 1: Get all responses
    responses = get_student_responses(conn, student_id)
    if not responses:
        print(f"  [ERROR] No responses found for student {student_id}")
        return {"error": "no_responses"}

    print(f"  Languages: {', '.join(responses.keys())}")
    for lang, resp_list in responses.items():
        print(f"    {lang}: {len(resp_list)} responses")

    # Step 2: Extract concepts and build graphs per language
    lang_results = {}
    for lang, resp_list in responses.items():
        if verbose:
            print(f"\n  --- Processing {lang} ---")

        # Combine all answers for this language
        combined_text = " ".join(r["answer_text"] for r in resp_list)
        if verbose:
            print(f"  Combined text ({len(combined_text)} chars)")

        # Extract concepts
        try:
            extracted = extract_concepts(combined_text, language=lang, use_mock=use_mock)
        except Exception as e:
            print(f"  [ERROR] Extraction failed for {lang}: {e}")
            continue

        # Build graph
        try:
            student_graph = build_graph(extracted)
            stats = graph_stats(student_graph)
        except Exception as e:
            print(f"  [ERROR] Graph building failed for {lang}: {e}")
            continue

        # Save extraction to DB
        eid = f"E_{datetime.now().strftime('%Y%m%d')}_{student_id}_{lang}"
        try:
            insert(conn, "extractions", {
                "extraction_id": eid,
                "response_id": resp_list[0]["response_id"],
                "model_used": extracted.get("model", "mock"),
                "concepts": json.dumps(extracted.get("concepts", []), ensure_ascii=False),
                "relations": json.dumps(extracted.get("relations", []), ensure_ascii=False),
                "raw_response": extracted.get("raw_response", ""),
            })
        except Exception as e:
            if verbose:
                print(f"  [WARN] DB insert failed for {eid}: {e}")

        # Save graph to DB
        gid = f"G_{datetime.now().strftime('%Y%m%d')}_{student_id}_{lang}"
        try:
            insert(conn, "graphs", {
                "graph_id": gid,
                "extraction_id": eid,
                "language": lang,
                "domain": "social_issues",
                "node_count": stats["nodes"],
                "edge_count": stats["edges"],
                "density": stats["density"],
                "graph_json": json.dumps(graph_to_dict(student_graph), ensure_ascii=False),
            })
        except Exception as e:
            if verbose:
                print(f"  [WARN] DB insert failed for {gid}: {e}")

        lang_results[lang] = {
            "extracted": extracted,
            "graph": student_graph,
            "stats": stats,
            "extraction_id": eid,
            "graph_id": gid,
        }

        if verbose:
            print(f"  Concepts: {extracted.get('concepts', [])}")
            print(f"  Relations: {len(extracted.get('relations', []))}")
            print(f"  Graph: {stats['nodes']} nodes, {stats['edges']} edges")

    # Step 3: Cross-language comparison with concept mapping
    mapping = load_concept_mapping()
    if verbose and mapping:
        print(f"  Loaded concept mapping: {len(mapping)} entries")

    langs = list(lang_results.keys())
    comparisons = []

    for i in range(len(langs)):
        for j in range(i + 1, len(langs)):
            l1 = langs[i]
            l2 = langs[j]
            lang_pair = f"{l1}-{l2}"

            if l1 not in lang_results or l2 not in lang_results:
                continue

            if verbose:
                print(f"\n  --- Comparing {lang_pair} ---")

            g1 = lang_results[l1]["graph"]
            g2 = lang_results[l2]["graph"]

            # Calculate LDS score (3-component: GED + node Jaccard + edge Jaccard)
            lds_result = calculate_lds_score(g1, g2, concept_mapping=mapping if mapping else None)
            # Bootstrap CI (node-based resampling)
            lds_boot = bootstrap_lds_ci(g1, g2, concept_mapping=mapping if mapping else None, n_iterations=500)

            if verbose:
                print(f"  LDS: {lds_result['lds_score']:.4f}")
                print(f"    GED sim:   {lds_result['ged_similarity']:.4f}")
                print(f"    Node Jac:  {lds_result['jaccard_node']:.4f}")
                print(f"    Edge Jac:  {lds_result['jaccard_edge']:.4f}")
                print(f"    95% CI:    [{lds_boot['ci_lower']}, {lds_boot['ci_upper']}]")
                print(f"    Std Err:   {lds_boot['std_error']}")
                print(f"  Shared edges: {lds_result.get('shared_edges', 0)}")
                print(f"  L1 only: {lds_result.get('l1_only', 0)}, L2 only: {lds_result.get('l2_only', 0)}")

            # Detect cross-language gaps
            gaps = detect_cross_language_gaps(g1, g2, {})

            # Group gaps by type
            concept_gaps = [g for g in gaps if g.gap_type == GapType.CONCEPT_ABSENT]
            relation_gaps = [g for g in gaps if g.gap_type == GapType.RELATION_BROKEN]
            struct_gaps = [g for g in gaps if g.gap_type == GapType.STRUCTURAL_SHIFT]

            # Save to DB
            aid = f"A_{datetime.now().strftime('%Y%m%d')}_{student_id}_{lang_pair}"
            try:
                insert(conn, "cross_language_analysis", {
                    "analysis_id": aid,
                    "student_id": student_id,
                    "lang_pair": lang_pair,
                    "topic": "all",
                    "lcd_score": lds_result.get("lds_score"),
                    "graph_similarity": lds_result.get("combined_similarity"),
                    "concept_shift_count": len(concept_gaps),
                    "relation_shift_count": len(relation_gaps),
                    "shared_concepts": lds_result.get("shared_nodes"),
                    "unique_l1_concepts": lds_result.get("l1_only"),
                    "unique_l2_concepts": lds_result.get("l2_only"),
                    "details_json": json.dumps({
                        "lds": lds_result,
                        "bootstrap_ci": {
                            "ci_lower": lds_boot.get("ci_lower"),
                            "ci_upper": lds_boot.get("ci_upper"),
                            "std_error": lds_boot.get("std_error"),
                        },
                        "gaps": [g.to_dict() for g in gaps],
                    }, ensure_ascii=False),
                })
            except Exception as e:
                if verbose:
                    print(f"  [WARN] DB insert failed for {aid}: {e}")

            comparisons.append({
                "lang_pair": lang_pair,
                "lds": lds_result,
                "bootstrap_ci": lds_boot,
                "gaps": gaps,
            })

    print(f"\n  [OK] Analysis complete for {student_id}")
    return {
        "student_id": student_id,
        "languages": list(responses.keys()),
        "lang_results": {k: {"stats": v["stats"]} for k, v in lang_results.items()},
        "comparisons": comparisons,
    }


def analyze_all_students(conn, use_mock: bool = True, verbose: bool = False):
    """Run analysis for all students in the database."""
    students = query(conn, "SELECT student_id FROM students WHERE student_id != 'GOLD_LABEL'")
    print(f"\n  Found {len(students)} students to analyze")

    results = []
    for s in students:
        sid = s["student_id"]
        result = analyze_student_responses(conn, sid, use_mock=use_mock, verbose=verbose)
        results.append(result)

    return results


def list_students(conn):
    """List available students with their response counts."""
    students = query(conn, """
        SELECT s.student_id, s.native_lang, s.school_lang,
               COUNT(r.response_id) as response_count
        FROM students s
        LEFT JOIN responses r ON s.student_id = r.student_id
        WHERE s.student_id != 'GOLD_LABEL'
        GROUP BY s.student_id
        ORDER BY s.student_id
    """)

    print(f"\n{'='*50}")
    print(f"  Available Students")
    print(f"{'='*50}")
    for s in students:
        print(f"  {s['student_id']:<12s} | {s['native_lang']}->{s['school_lang']} | {s['response_count']} responses")
    print()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyze student cross-language data")
    parser.add_argument("--student", type=str, help="Student ID to analyze")
    parser.add_argument("--all", action="store_true", help="Analyze all students")
    parser.add_argument("--list", action="store_true", help="List available students")
    parser.add_argument("--mock", action="store_true", default=True, help="Use mock extraction (no LLM)")
    parser.add_argument("--no-mock", action="store_true", help="Use real LLM extraction")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    conn = get_connection()
    use_mock = not args.no_mock

    if args.list:
        list_students(conn)
        conn.close()
        return

    if args.all:
        analyze_all_students(conn, use_mock=use_mock, verbose=args.verbose)
    elif args.student:
        analyze_student_responses(conn, args.student, use_mock=use_mock, verbose=args.verbose)
    else:
        parser.print_help()

    conn.close()


if __name__ == "__main__":
    main()
