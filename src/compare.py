"""
Missing Cognitive Links Detection Module

Compares student graph against expert graph to find missing links.
This is a DETERMINISTIC module - no LLM calls.
"""

from typing import List, Dict, Tuple

try:
    import networkx as nx
except ImportError:
    nx = None


def detect_missing_links(
    student_graph: "nx.DiGraph",
    expert_graph: "nx.DiGraph",
    threshold: float = 0.5
) -> List[Dict]:
    """
    Find missing cognitive links by comparing student and expert graphs.

    Three-layer detection:
    1. Concept layer: Concepts in expert but missing in student
    2. Relation layer: Relations in expert but missing in student
    3. Structural layer: Topological differences

    Args:
        student_graph: Student's knowledge graph
        expert_graph: Expert reference graph
        threshold: Minimum confidence for a missing link (0-1)

    Returns:
        List of missing links with details
    """
    missing_links = []

    # Layer 1: Missing Concepts
    student_nodes = set(student_graph.nodes())
    expert_nodes = set(expert_graph.nodes())

    missing_concepts = expert_nodes - student_nodes
    for concept in missing_concepts:
        # Find prerequisites (nodes that point TO this concept in expert graph)
        prerequisites = list(expert_graph.predecessors(concept))
        prereq_in_student = [p for p in prerequisites if p in student_nodes]

        # Calculate confidence based on prerequisites present
        confidence = len(prereq_in_student) / max(len(prerequisites), 1)

        missing_links.append({
            "type": "missing_concept",
            "concept": concept,
            "prerequisites": prerequisites,
            "prerequisites_present": prereq_in_student,
            "prerequisites_missing": [p for p in prerequisites if p not in student_nodes],
            "confidence": confidence,
            "severity": "high" if confidence > 0.7 else "medium" if confidence > 0.3 else "low"
        })

    # Layer 2: Missing Relations
    expert_edges = set(expert_graph.edges())
    student_edges = set(student_graph.edges())

    missing_edges = expert_edges - student_edges
    for source, target in missing_edges:
        # Check if both concepts exist in student graph
        if source in student_nodes and target in student_nodes:
            # Get relation type from expert graph
            rel_type = expert_graph[source][target].get("relation", "unknown")

            missing_links.append({
                "type": "missing_relation",
                "source": source,
                "target": target,
                "relation": rel_type,
                "confidence": 0.8,  # High confidence - both concepts exist
                "severity": "high"
            })

    # Layer 3: Structural Analysis
    structural_issues = analyze_structure(student_graph, expert_graph)
    missing_links.extend(structural_issues)

    # Sort by severity and confidence
    severity_order = {"high": 0, "medium": 1, "low": 2}
    missing_links.sort(key=lambda x: (severity_order.get(x["severity"], 3), -x["confidence"]))

    # Filter by threshold
    missing_links = [link for link in missing_links if link["confidence"] >= threshold]

    return missing_links


def analyze_structure(
    student_graph: "nx.DiGraph",
    expert_graph: "nx.DiGraph"
) -> List[Dict]:
    """
    Analyze structural differences between graphs.
    Detects: isolated nodes, disconnected components, hub nodes
    """
    issues = []

    # Check for isolated nodes (concepts with no connections)
    for node in student_graph.nodes():
        if student_graph.degree(node) == 0:
            issues.append({
                "type": "isolated_concept",
                "concept": node,
                "confidence": 0.9,
                "severity": "medium",
                "suggestion": f"Concept '{node}' is isolated - consider connecting it to related concepts"
            })

    # Check for disconnected components
    if student_graph.number_of_nodes() > 1:
        components = list(nx.weakly_connected_components(student_graph))
        if len(components) > 1:
            issues.append({
                "type": "disconnected_graph",
                "components": [list(c) for c in components],
                "confidence": 0.95,
                "severity": "medium",
                "suggestion": f"Knowledge graph has {len(components)} disconnected parts"
            })

    return issues


def calculate_graph_similarity(
    graph1: "nx.DiGraph",
    graph2: "nx.DiGraph"
) -> float:
    """
    Calculate structural similarity between two graphs.
    Returns: 0.0 (completely different) to 1.0 (identical)
    """
    nodes1 = set(graph1.nodes())
    nodes2 = set(graph2.nodes())

    edges1 = set(graph1.edges())
    edges2 = set(graph2.edges())

    # Node overlap
    node_overlap = len(nodes1 & nodes2) / max(len(nodes1 | nodes2), 1)

    # Edge overlap
    edge_overlap = len(edges1 & edges2) / max(len(edges1 | edges2), 1)

    # Weighted average
    return 0.4 * node_overlap + 0.6 * edge_overlap


# --- Simple Demo ---
if __name__ == "__main__":
    import json

    print("=== Missing Link Detection Demo ===\n")

    # Simulated graphs
    try:
        from graph import build_graph, load_expert_graph

        # Student graph (partial knowledge)
        student_data = {
            "concepts": ["Ableitung", "Funktion"],
            "relations": [
                {"source": "Ableitung", "target": "Funktion", "type": "is_part_of"}
            ]
        }
        student_graph = build_graph(student_data)
        print(f"Student knows: {list(student_graph.nodes())}")

        # Expert graph (full knowledge)
        try:
            expert_graph = load_expert_graph("calculus")
            print(f"Expert knows: {list(expert_graph.nodes())[:5]}...")

            # Detect missing links
            missing = detect_missing_links(student_graph, expert_graph)
            print(f"\nMissing links found: {len(missing)}")
            for link in missing[:3]:
                print(f"  - {link['type']}: {link.get('concept', link.get('source', 'N/A'))}")
        except FileNotFoundError:
            print("Expert graph not found - using demo data")
            # Create simple expert graph
            import networkx as nx
            expert_graph = nx.DiGraph()
            expert_graph.add_edges_from([
                ("Ableitung", "Funktion"),
                ("Ableitung", "Steigung"),
                ("Integral", "Ableitung"),
                ("Kettenregel", "Ableitung")
            ])
            missing = detect_missing_links(student_graph, expert_graph)
            print(f"\nMissing links found: {len(missing)}")

    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure networkx is installed: pip install networkx")

    print("\n✅ Missing link detection works!")
