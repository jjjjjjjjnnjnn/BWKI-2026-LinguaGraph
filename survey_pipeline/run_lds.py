"""
Survey Pipeline — LDS Computation
===================================
Compute Language Drift Score for each student and across all students.

Usage:
    python run_lds.py                    # Compute LDS for all students
    python run_lds.py --student S001     # Compute for one student
    python run_lds.py --verbose          # Show detailed output
"""

import json
import sys
import time
from pathlib import Path
from collections import defaultdict
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from db_utils import get_connection, query, query_one, insert

try:
    import networkx as nx
except ImportError:
    nx = None

from config import REPORT_DIR


def build_graph_from_extraction(extraction: dict) -> "nx.DiGraph":
    """Build a NetworkX graph from an extraction result."""
    if nx is None:
        return None

    G = nx.DiGraph()
    concepts = extraction.get("concepts", [])
    relations = extraction.get("relations", [])

    for c in concepts:
        if isinstance(c, str):
            G.add_node(c)
        elif isinstance(c, dict):
            G.add_node(c.get("name", str(c)))

    for r in relations:
        src = r.get("source", "")
        tgt = r.get("target", "")
        rel_type = r.get("type", "co_occurs")
        if src and tgt and src in G and tgt in G:
            G.add_edge(src, tgt, relation=rel_type)

    return G


def compute_lcd(graph_a: "nx.DiGraph", graph_b: "nx.DiGraph") -> dict:
    """
    Compute Language Cognitive Drift between two graphs.
    LCD = 1 - Jaccard(edge_sets)
    """
    if nx is None:
        return {"lcd_score": 0, "similarity": 0}

    edges_a = set(graph_a.edges())
    edges_b = set(graph_b.edges())

    if not edges_a and not edges_b:
        return {"lcd_score": 0, "similarity": 1.0}

    intersection = edges_a & edges_b
    union = edges_a | edges_b

    similarity = len(intersection) / max(len(union), 1)
    lcd = 1 - similarity

    return {
        "lcd_score": round(lcd, 4),
        "similarity": round(similarity, 4),
        "shared_edges": len(intersection),
        "total_unique_edges": len(union),
        "l1_only": len(edges_a - edges_b),
        "l2_only": len(edges_b - edges_a),
    }


def merge_student_graphs(conn, student_id: str) -> dict:
    """
    Merge all extractions for a student into per-language graphs.
    Returns {language: nx.DiGraph}
    """
    extractions = query(conn, """
        SELECT r.language, e.concepts, e.relations, r.question_id
        FROM extractions e
        JOIN responses r ON e.response_id = r.response_id
        WHERE r.student_id = ?
        ORDER BY r.language, r.question_id
    """, (student_id,))

    lang_graphs = defaultdict(list)

    for ext in extractions:
        concepts = json.loads(ext["concepts"]) if isinstance(ext["concepts"], str) else ext["concepts"]
        relations = json.loads(ext["relations"]) if isinstance(ext["relations"], str) else ext["relations"]
        lang_graphs[ext["language"]].append({
            "concepts": concepts,
            "relations": relations,
            "question_id": ext["question_id"],
        })

    # Build merged graph per language
    merged = {}
    for lang, extractions_list in lang_graphs.items():
        G = nx.DiGraph() if nx else None
        if G is None:
            continue

        all_concepts = set()
        all_relations = []

        for ext in extractions_list:
            for c in ext["concepts"]:
                if isinstance(c, str):
                    all_concepts.add(c)
            all_relations.extend(ext["relations"])

        for c in all_concepts:
            G.add_node(c)

        for r in all_relations:
            src = r.get("source", "")
            tgt = r.get("target", "")
            if src and tgt and src in G and tgt in G:
                G.add_edge(src, tgt, relation=r.get("type", "co_occurs"))

        merged[lang] = G

    return merged


def compute_student_lds(conn, student_id: str) -> dict:
    """Compute LDS for all language pairs of a student."""
    lang_graphs = merge_student_graphs(conn, student_id)

    pairs = [("zh", "en"), ("zh", "de"), ("en", "de")]
    results = {}

    for lang_a, lang_b in pairs:
        if lang_a in lang_graphs and lang_b in lang_graphs:
            lcd = compute_lcd(lang_graphs[lang_a], lang_graphs[lang_b])
            pair_key = f"{lang_a}-{lang_b}"
            results[pair_key] = lcd

            # Store in database
            try:
                from datetime import datetime
                analysis_id = f"A_{student_id}_{pair_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                insert(conn, "cross_language_analysis", {
                    "analysis_id": analysis_id,
                    "student_id": student_id,
                    "topic": "overall",
                    "lang_pair": pair_key,
                    "lcd_score": lcd["lcd_score"],
                    "graph_similarity": lcd["similarity"],
                    "shared_concepts": lcd["shared_edges"],
                    "unique_l1_concepts": lcd["l1_only"],
                    "unique_l2_concepts": lcd["l2_only"],
                })
            except Exception:
                pass  # May already exist

    conn.commit()
    return results


def compute_group_lds(conn) -> dict:
    """
    Compute group-level LDS by merging all students' extractions.
    Returns per-topic, per-pair LDS.
    """
    # Get all extractions
    extractions = query(conn, """
        SELECT r.student_id, e.concepts, e.relations,
               r.language, r.question_id, r.source
        FROM extractions e
        JOIN responses r ON e.response_id = r.response_id
        WHERE r.source = 'survey'
    """)

    # Group by language and question
    groups = defaultdict(list)
    for ext in extractions:
        lang = ext["language"]
        qid = ext["question_id"]
        concepts = json.loads(ext["concepts"]) if isinstance(ext["concepts"], str) else ext["concepts"]
        relations = json.loads(ext["relations"]) if isinstance(ext["relations"], str) else ext["relations"]
        groups[(lang, qid)].append({"concepts": concepts, "relations": relations})

    # Build merged graph per language
    lang_graphs = {}
    for (lang, qid), exts in groups.items():
        if lang not in lang_graphs:
            lang_graphs[lang] = nx.DiGraph() if nx else None
        if lang_graphs[lang] is None:
            continue

        for ext in exts:
            for c in ext["concepts"]:
                if isinstance(c, str):
                    lang_graphs[lang].add_node(c)
            for r in ext["relations"]:
                src = r.get("source", "")
                tgt = r.get("target", "")
                if src and tgt:
                    lang_graphs[lang].add_edge(src, tgt, relation=r.get("type", "co_occurs"))

    # Compute pairwise LCD
    pairs = [("zh", "en"), ("zh", "de"), ("en", "de")]
    results = {}
    for lang_a, lang_b in pairs:
        if lang_a in lang_graphs and lang_b in lang_graphs:
            lcd = compute_lcd(lang_graphs[lang_a], lang_graphs[lang_b])
            results[f"{lang_a}-{lang_b}"] = lcd

    return results


def run_lds(verbose: bool = False):
    """Run LDS computation for all students."""
    print(f"\n{'='*60}")
    print(f"  LDS Computation")
    print(f"{'='*60}\n")

    conn = get_connection()

    # Get all students
    students = query(conn, """
        SELECT DISTINCT student_id FROM responses
        WHERE source = 'survey'
        ORDER BY student_id
    """)

    print(f"  Students: {len(students)}")

    all_results = {}

    for s in students:
        sid = s["student_id"]
        print(f"\n  Computing LDS for {sid}...")

        lds = compute_student_lds(conn, sid)
        all_results[sid] = lds

        if verbose:
            for pair, data in lds.items():
                print(f"    {pair}: LCD={data['lcd_score']:.4f}")

    # Compute group-level
    print("\n  Computing group-level LDS...")
    group_lds = compute_group_lds(conn)
    all_results["group"] = group_lds

    for pair, data in group_lds.items():
        print(f"    {pair}: LCD={data['lcd_score']:.4f}")

    conn.close()

    # Save results
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORT_DIR / "lds_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n  Results saved: {output_path}")

    # Generate markdown report
    report = generate_lds_report(all_results)
    report_path = REPORT_DIR / "lds_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"  Report saved: {report_path}")

    print(f"\n{'='*60}")
    print(f"  LDS computation complete")
    print(f"{'='*60}\n")


def generate_lds_report(results: dict) -> str:
    """Generate markdown LDS report."""
    md = []
    md.append("# Survey LDS Report\n")
    md.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    # Group results
    if "group" in results:
        md.append("## Group-Level LDS\n")
        md.append("| Pair | LCD | Similarity | Shared Edges |\n")
        md.append("|------|-----|------------|--------------|\n")
        for pair, data in results["group"].items():
            md.append(f"| {pair} | {data['lcd_score']:.4f} | {data['similarity']:.4f} | {data['shared_edges']} |\n")

    # Per-student results
    md.append("\n## Per-Student LDS\n")
    for sid, lds in results.items():
        if sid == "group":
            continue
        md.append(f"### {sid}\n")
        if lds:
            md.append("| Pair | LCD | Similarity |\n")
            md.append("|------|-----|------------|\n")
            for pair, data in lds.items():
                md.append(f"| {pair} | {data['lcd_score']:.4f} | {data['similarity']:.4f} |\n")
        else:
            md.append("No LDS computed (missing language pairs).\n")

    return "\n".join(md)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compute LDS for survey data")
    parser.add_argument("--student", help="Compute for specific student")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    if args.student:
        conn = get_connection()
        lds = compute_student_lds(conn, args.student)
        print(json.dumps(lds, indent=2))
        conn.close()
    else:
        run_lds(verbose=args.verbose)


if __name__ == "__main__":
    main()
