"""
Graph Builder Module

Converts extracted concepts/relations into a NetworkX graph.
This is a DETERMINISTIC module - no LLM calls.
"""

import json
from pathlib import Path
from typing import Optional

try:
    import networkx as nx
except ImportError:
    import logging
    logging.getLogger(__name__).warning("networkx not installed. Run: pip install networkx")
    nx = None


def build_graph(extracted_data: dict) -> "nx.DiGraph":
    """
    Build a directed graph from extracted concepts and relations.

    Args:
        extracted_data: Output from extract_concepts()

    Returns:
        NetworkX DiGraph
    """
    if nx is None:
        raise ImportError("networkx is required. Run: pip install networkx")

    G = nx.DiGraph()

    # Add concept nodes
    for concept in extracted_data.get("concepts", []):
        G.add_node(concept, type="concept")

    # Add relation edges
    for relation in extracted_data.get("relations", []):
        if isinstance(relation, dict):
            source = relation.get("source")
            target = relation.get("target")
            rel_type = relation.get("type", "relates_to")
        elif isinstance(relation, list) and len(relation) >= 2:
            source, target = relation[0], relation[1]
            rel_type = relation[2] if len(relation) > 2 else "relates_to"
        else:
            continue

        if source and target:
            G.add_edge(source, target, relation=rel_type)

    return G


def load_expert_graph(domain: str = "calculus") -> "nx.DiGraph":
    """
    Load the expert reference graph for a domain.

    Args:
        domain: Domain name (e.g., "calculus", "algebra")

    Returns:
        NetworkX DiGraph
    """
    if nx is None:
        raise ImportError("networkx is required. Run: pip install networkx")

    graph_file = Path(__file__).parent.parent / "config" / "expert_graphs" / f"{domain}.json"

    if not graph_file.exists():
        raise FileNotFoundError(f"Expert graph not found: {graph_file}")

    data = json.loads(graph_file.read_text(encoding="utf-8"))

    G = nx.DiGraph()

    # Add concepts
    for concept in data.get("concepts", []):
        if isinstance(concept, str):
            G.add_node(concept, type="expert")
        elif isinstance(concept, dict):
            name = concept.get("name", concept.get("concept"))
            G.add_node(name, type="expert", **{k: v for k, v in concept.items() if k not in ["name", "concept"]})

    # Add relations
    for rel in data.get("relations", []):
        if isinstance(rel, dict):
            source = rel.get("source")
            target = rel.get("target")
            rel_type = rel.get("type", "relates_to")
        elif isinstance(rel, list) and len(rel) >= 2:
            source, target = rel[0], rel[1]
            rel_type = rel[2] if len(rel) > 2 else "relates_to"
        else:
            continue

        if source and target:
            G.add_edge(source, target, relation=rel_type)

    return G


def graph_to_dict(G: "nx.DiGraph") -> dict:
    """
    Convert NetworkX graph to dict for JSON serialization.

    Returns:
        dict with "nodes" and "edges" keys
    """
    nodes = []
    for node in G.nodes():
        node_data = G.nodes[node].copy()
        node_data["id"] = node
        nodes.append(node_data)

    edges = []
    for u, v, data in G.edges(data=True):
        edges.append({
            "source": u,
            "target": v,
            **data
        })

    return {
        "nodes": nodes,
        "edges": edges,
        "node_count": len(nodes),
        "edge_count": len(edges)
    }


def graph_stats(G: "nx.DiGraph") -> dict:
    """Get basic statistics of a graph"""
    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "density": nx.density(G) if nx else 0,
        "is_connected": nx.is_weakly_connected(G) if G.number_of_nodes() > 0 else False
    }


# --- Simple Demo ---
if __name__ == "__main__":
    print("=== Graph Builder Demo ===\n")

    # Simulated extracted data
    extracted = {
        "concepts": ["Ableitung", "Funktion", "Steigung", "Integral"],
        "relations": [
            {"source": "Ableitung", "target": "Funktion", "type": "is_part_of"},
            {"source": "Ableitung", "target": "Steigung", "type": "measures"},
            {"source": "Integral", "target": "Ableitung", "type": "inverse_of"}
        ]
    }

    # Build graph
    student_graph = build_graph(extracted)
    print(f"Student graph: {graph_stats(student_graph)}")

    # Load expert graph
    try:
        expert_graph = load_expert_graph("calculus")
        print(f"Expert graph: {graph_stats(expert_graph)}")
    except FileNotFoundError:
        print("Expert graph not found (expected in demo)")

    print("\n✅ Graph builder works!")
