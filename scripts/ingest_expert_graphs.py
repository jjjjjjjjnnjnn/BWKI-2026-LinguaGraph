"""
Ingest Expert Graphs
======================
Import expert knowledge graphs into the linguaGraph database.

Currently supports:
    - social_issues_graph.json (primary - social issues domain)
    - expert_graph_9th.json (backup - calculus domain)

Usage:
    python ingest_expert_graphs.py                # Import all expert graphs
    python ingest_expert_graphs.py --fresh         # Re-import
"""

import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from db_utils import get_connection, query, insert

DATA_DIR = Path(__file__).parent / "data"
EXPERT_DIR = Path(__file__).parent / "expert_graph"
CONFIG_DIR = Path(__file__).parent / "config" / "expert_graphs"


def import_expert_graph(conn, filepath: Path, domain: str = None, fresh: bool = False) -> dict:
    """Import an expert graph into the database."""
    if not filepath.exists():
        print(f"  [SKIP] File not found: {filepath}")
        return {"nodes": 0, "edges": 0}

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if domain is None:
        domain = data.get("domain", filepath.stem)

    # Create expert_graphs table if not exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expert_graphs (
            graph_id        TEXT PRIMARY KEY,
            domain          TEXT NOT NULL,
            description     TEXT,
            concepts        TEXT NOT NULL,
            relations       TEXT NOT NULL,
            metadata        TEXT,
            created_at      TEXT DEFAULT (datetime('now'))
        )
    """)

    concepts = data.get("concepts", [])
    relations = data.get("relations", [])
    metadata = data.get("metadata", {})

    graph_id = f"expert_{domain}"

    if fresh:
        conn.execute("DELETE FROM expert_graphs WHERE graph_id=?", (graph_id,))

    existing = query(conn, "SELECT graph_id FROM expert_graphs WHERE graph_id=?", (graph_id,))
    if existing and not fresh:
        print(f"  [SKIP] {graph_id} already exists")
        return {"nodes": len(concepts), "edges": len(relations)}

    insert(conn, "expert_graphs", {
        "graph_id": graph_id,
        "domain": domain,
        "description": data.get("description", ""),
        "concepts": json.dumps(concepts, ensure_ascii=False) if isinstance(concepts, list) else json.dumps(list(concepts), ensure_ascii=False),
        "relations": json.dumps(relations, ensure_ascii=False),
        "metadata": json.dumps(metadata, ensure_ascii=False),
    })

    node_count = len(concepts)
    edge_count = len(relations)
    print(f"  [OK] {graph_id}: {node_count} concepts, {edge_count} relations")

    return {"nodes": node_count, "edges": edge_count}


def import_all_expert_graphs(conn, fresh: bool = False) -> list:
    """Import all available expert graphs."""
    results = []

    # Primary: social_issues_graph.json
    results.append(import_expert_graph(
        conn, EXPERT_DIR / "social_issues_graph.json", "social_issues", fresh
    ))

    # Backup: expert_graph_9th.json (calculus)
    results.append(import_expert_graph(
        conn, EXPERT_DIR / "expert_graph_9th.json", "calculus_9th", fresh
    ))

    # Also look in config/expert_graphs/ for standardized versions
    if CONFIG_DIR.exists():
        for cfg_file in sorted(CONFIG_DIR.glob("*.json")):
            results.append(import_expert_graph(conn, cfg_file, fresh=fresh))

    conn.commit()
    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Import expert graphs into linguaGraph DB")
    parser.add_argument("--fresh", action="store_true", help="Re-import all graphs")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  Importing Expert Graphs")
    print(f"{'='*50}")

    conn = get_connection()
    results = import_all_expert_graphs(conn, fresh=args.fresh)

    total_nodes = sum(r.get("nodes", 0) for r in results)
    total_edges = sum(r.get("edges", 0) for r in results)
    print(f"\n  [DONE] {len(results)} graphs imported ({total_nodes} nodes, {total_edges} edges)\n")

    conn.close()


if __name__ == "__main__":
    main()
