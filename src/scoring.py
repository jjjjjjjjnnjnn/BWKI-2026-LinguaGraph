"""
CognitiveSpace Scoring Functions

MCL Score: how many expert connections are missing in student graph
LCD Score: how different are two language graphs for the same person
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    import networkx as nx
except ImportError:
    nx = None


# ===== MCL Scoring =====

def calculate_mcl_score(
    student_graph: "nx.DiGraph",
    expert_graph: "nx.DiGraph"
) -> Dict:
    """
    Calculate Missing Cognitive Links score.
    
    MCL = E_expert - E_learner (set difference)
    MCL Score = |MCL| / |E_expert| * 100%
    
    Returns:
        dict with mcl_score, missing_count, total_expert, missing_edges
    """
    if nx is None:
        raise ImportError("networkx required")
    
    expert_edges = set(expert_graph.edges())
    student_edges = set(student_graph.edges())
    
    missing = expert_edges - student_edges
    
    total_expert = len(expert_edges)
    missing_count = len(missing)
    score = (missing_count / max(total_expert, 1)) * 100
    
    return {
        "mcl_score": round(score, 2),
        "missing_count": missing_count,
        "total_expert": total_expert,
        "missing_edges": [(s, t) for s, t in missing]
    }


def calculate_weighted_mcl_score(
    student_graph: "nx.DiGraph",
    expert_graph: "nx.DiGraph",
    importance_weights: Dict = None
) -> Dict:
    """
    Weighted MCL: consider edge importance.
    
    Weighted MCL = sum(w_i * (1 - c_i)) for missing edges
    """
    if nx is None:
        raise ImportError("networkx required")
    
    if importance_weights is None:
        importance_weights = {}
    
    expert_edges = set(expert_graph.edges())
    student_edges = set(student_graph.edges())
    missing = expert_edges - student_edges
    
    total_weight = 0
    missing_weight = 0
    
    for s, t in expert_edges:
        w = importance_weights.get((s, t), 1.0)
        total_weight += w
        if (s, t) not in student_edges:
            missing_weight += w
    
    score = (missing_weight / max(total_weight, 1)) * 100
    
    return {
        "weighted_mcl_score": round(score, 2),
        "missing_weight": round(missing_weight, 2),
        "total_weight": round(total_weight, 2)
    }


# ===== LDS (Language Drift Score) =====
#
# Implements the full 3-component formula per docs/methodology.md:
#   LDS(L1, L2) = 1 - mean(GED_sim, Jaccard_node, Jaccard_edge)


def _normalize_ged(ged: float, max_possible: int) -> float:
    """Normalize GED to [0, 1] where 1 = identical."""
    if max_possible == 0:
        return 1.0
    # GED raw = number of edit operations. Normalize by max possible edits.
    normalized = 1 - (ged / max_possible)
    return max(0.0, min(1.0, normalized))


def calculate_lds_score(
    graph_l1: "nx.DiGraph",
    graph_l2: "nx.DiGraph",
    concept_mapping: Dict[str, str] = None
) -> Dict:
    """
    Language Drift Score — full 3-component formula.

    LDS(L1, L2) = 1 - mean(GED_sim, Jaccard_node, Jaccard_edge)

    Args:
        graph_l1: First language graph
        graph_l2: Second language graph
        concept_mapping: Optional cross-language concept mapping

    Returns:
        dict with lds_score, ged_similarity, jaccard_node, jaccard_edge,
        and detailed component breakdown
    """
    if nx is None:
        raise ImportError("networkx required")

    # Apply concept mapping if provided
    def map_nodes(G, mapping):
        """Create a new graph with mapped node names."""
        H = nx.DiGraph()
        for n in G.nodes():
            mapped = mapping.get(n, n)
            H.add_node(mapped, **G.nodes[n])
        for u, v, d in G.edges(data=True):
            mu = mapping.get(u, u)
            mv = mapping.get(v, v)
            H.add_edge(mu, mv, **d)
        return H

    if concept_mapping:
        g1 = map_nodes(graph_l1, concept_mapping)
        g2 = map_nodes(graph_l2, concept_mapping)
    else:
        g1 = graph_l1
        g2 = graph_l2

    # — Component 1: Graph Edit Distance similarity —
    try:
        raw_ged = nx.graph_edit_distance(g1, g2)
        if raw_ged is None:
            raw_ged = 0.0
        max_edits = max(g1.number_of_nodes(), g2.number_of_nodes()) + \
                    max(g1.number_of_edges(), g2.number_of_edges())
        ged_sim = _normalize_ged(raw_ged, max(1, max_edits))
    except Exception:
        ged_sim = 0.5  # Fallback if GED computation fails on large graphs

    # — Component 2: Node Jaccard —
    nodes_l1 = set(g1.nodes())
    nodes_l2 = set(g2.nodes())
    node_intersection = nodes_l1 & nodes_l2
    node_union = nodes_l1 | nodes_l2
    jaccard_node = len(node_intersection) / max(len(node_union), 1)

    # — Component 3: Edge Jaccard —
    edges_l1 = set(g1.edges())
    edges_l2 = set(g2.edges())
    edge_intersection = edges_l1 & edges_l2
    edge_union = edges_l1 | edges_l2
    jaccard_edge = len(edge_intersection) / max(len(edge_union), 1)

    # — Combined similarity and drift —
    combined_sim = (ged_sim + jaccard_node + jaccard_edge) / 3
    lds = 1 - combined_sim

    return {
        "lds_score": round(lds, 4),
        "lcd_score": round(lds, 4),  # backward compatibility
        "similarity": round(combined_sim, 4),  # backward compatibility
        "combined_similarity": round(combined_sim, 4),
        "ged_similarity": round(ged_sim, 4),
        "raw_ged": round(raw_ged, 2),
        "jaccard_node": round(jaccard_node, 4),
        "jaccard_edge": round(jaccard_edge, 4),
        "shared_nodes": len(node_intersection),
        "shared_edges": len(edge_intersection),
        "total_unique_nodes": len(node_union),
        "total_unique_edges": len(edge_union),
        "l1_nodes": g1.number_of_nodes(),
        "l2_nodes": g2.number_of_nodes(),
        "l1_edges": g1.number_of_edges(),
        "l2_edges": g2.number_of_edges(),
    }


# Backward compatibility alias
calculate_lcd_score = calculate_lds_score


def bootstrap_lds_ci(
    graph_l1: "nx.DiGraph",
    graph_l2: "nx.DiGraph",
    concept_mapping: Dict[str, str] = None,
    n_iterations: int = 1000,
    ci_level: float = 0.95
) -> Dict:
    """
    Bootstrap confidence interval for LDS using NODE-based resampling.

    Resamples NODES (with replacement) and keeps all edges incident to
    the resampled nodes, preserving structural dependencies between edges.
    This is statistically valid because node resampling maintains the
    graph topology, unlike edge-independent resampling.

    Args:
        graph_l1: First language graph
        graph_l2: Second language graph
        concept_mapping: Optional mapping for cross-language alignment
        n_iterations: Number of bootstrap resamples (default 1000)
        ci_level: Confidence level (default 0.95 for 95% CI)

    Returns:
        dict with lds_score, ci_lower, ci_upper, std_error, n_iterations
    """
    if nx is None:
        raise ImportError("networkx required")

    import random

    nodes_l1 = list(graph_l1.nodes())
    nodes_l2 = list(graph_l2.nodes())

    # Point estimate using full 3-component LDS
    point_result = calculate_lds_score(graph_l1, graph_l2, concept_mapping)
    point_estimate = point_result["lds_score"]

    # Bootstrap by resampling nodes (preserving topology)
    lds_samples = []
    n_l1 = len(nodes_l1)
    n_l2 = len(nodes_l2)

    for _ in range(n_iterations):
        # Resample nodes with replacement
        samp_nodes_l1 = [nodes_l1[i] for i in
            [random.randint(0, max(0, n_l1 - 1)) for _ in range(max(1, n_l1))]]
        samp_nodes_l2 = [nodes_l2[i] for i in
            [random.randint(0, max(0, n_l2 - 1)) for _ in range(max(1, n_l2))]]

        # Build subgraphs from resampled nodes (preserves incident edges)
        sub_l1 = graph_l1.subgraph(samp_nodes_l1).copy()
        sub_l2 = graph_l2.subgraph(samp_nodes_l2).copy()

        # Calculate LDS for this resample
        try:
            boot_result = calculate_lds_score(sub_l1, sub_l2, concept_mapping)
            lds_samples.append(boot_result["lds_score"])
        except Exception:
            continue

    if len(lds_samples) < 2:
        return {
            "lds_score": round(point_estimate, 4),
            "ci_lower": round(point_estimate, 4),
            "ci_upper": round(point_estimate, 4),
            "ci_level": ci_level,
            "std_error": 0.0,
            "n_iterations": n_iterations,
            "warning": "Bootstrap failed — returning point estimate"
        }

    lds_samples.sort()
    lower_idx = int((1 - ci_level) / 2 * len(lds_samples))
    upper_idx = int((1 + ci_level) / 2 * len(lds_samples)) - 1
    lower_idx = max(0, lower_idx)
    upper_idx = min(len(lds_samples) - 1, upper_idx)

    mean_lds = sum(lds_samples) / len(lds_samples)
    variance = sum((x - mean_lds) ** 2 for x in lds_samples) / len(lds_samples)
    std_error = variance ** 0.5

    return {
        "lds_score": round(point_estimate, 4),
        "ci_lower": round(lds_samples[lower_idx], 4),
        "ci_upper": round(lds_samples[upper_idx], 4),
        "ci_level": ci_level,
        "std_error": round(std_error, 4),
        "n_iterations": n_iterations
    }


# Deprecated — use bootstrap_lds_ci() instead
bootstrap_lcd_ci = bootstrap_lds_ci


# ===== Concept Extraction Metrics =====

def calculate_concept_f1(gold_concepts: Set, extracted_concepts: Set) -> Dict:
    """Calculate concept-level Precision, Recall, F1."""
    tp = len(gold_concepts & extracted_concepts)
    fp = len(extracted_concepts - gold_concepts)
    fn = len(gold_concepts - extracted_concepts)
    
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-6)
    
    return {"precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4)}


def calculate_relation_f1(gold_relations: List, extracted_relations: List) -> Dict:
    """Calculate relation-level Precision, Recall, F1.
    
    Compares (source, target, type) triples — relation type IS included.
    Empty inputs return perfect scores (nothing to miss, nothing to错).
    """
    def norm(r):
        src = r.get("from") or r.get("source", "")
        tgt = r.get("to") or r.get("target", "")
        rel_type = r.get("type", "relates_to")
        return (src, tgt, rel_type)
    
    # Handle empty case
    if not gold_relations and not extracted_relations:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0}
    
    gold_triples = {norm(r) for r in gold_relations}
    extracted_triples = {norm(r) for r in extracted_relations}
    
    tp = len(gold_triples & extracted_triples)
    fp = len(extracted_triples - gold_triples)
    fn = len(gold_triples - extracted_triples)
    
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-6)
    
    return {"precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4)}


# ===== Full Evaluation Pipeline =====

def evaluate_respondent(survey_data: Dict, expert_graph: "nx.DiGraph") -> Dict:
    """
    Full evaluation for one respondent.
    
    1. Merge all question graphs
    2. Build student graph
    3. Calculate MCL score
    4. Calculate concept/relation F1 (if gold labels available)
    """
    if nx is None:
        raise ImportError("networkx required")
    
    # Merge graphs
    all_nodes = set()
    all_edges = []
    for r in survey_data.get("responses", []):
        g = r.get("graph_output", {})
        all_nodes.update(g.get("nodes", []))
        all_edges.extend(g.get("edges", []))
    
    # Build student graph
    student_graph = nx.DiGraph()
    for node in all_nodes:
        student_graph.add_node(node)
    for edge in all_edges:
        src = edge.get("source", "")
        tgt = edge.get("target", "")
        if src and tgt:
            student_graph.add_edge(src, tgt, relation=edge.get("type", "related_to"))
    
    # MCL score
    mcl = calculate_mcl_score(student_graph, expert_graph)
    
    return {
        "respondent_id": survey_data["respondent_id"],
        "language": survey_data["language"],
        "node_count": len(all_nodes),
        "edge_count": len(all_edges),
        "mcl": mcl,
        "student_graph_edges": list(student_graph.edges())
    }


# ===== Demo =====
if __name__ == "__main__":
    # Create simple test graphs
    if nx:
        expert = nx.DiGraph()
        expert.add_edges_from([
            ("极限", "导数"), ("导数", "变化率"), ("积分", "导数"),
            ("积分", "面积"), ("导数", "切线斜率")
        ])
        
        student = nx.DiGraph()
        student.add_edges_from([
            ("导数", "变化率"), ("积分", "面积")
        ])
        
        # MCL
        mcl = calculate_mcl_score(student, expert)
        print(f"MCL Score: {mcl['mcl_score']}% ({mcl['missing_count']}/{mcl['total_expert']} edges missing)")
        print(f"Missing: {mcl['missing_edges']}")
        
        # LDS (3-component: GED + node Jaccard + edge Jaccard)
        graph_l1 = nx.DiGraph()
        graph_l1.add_edges_from([("导数", "变化率"), ("积分", "面积")])
        graph_l2 = nx.DiGraph()
        graph_l2.add_edges_from([("Ableitung", "Änderungsrate"), ("Integral", "Fläche")])

        lds = calculate_lds_score(graph_l1, graph_l2)
        print(f"\nLDS Score: {lds['lds_score']}")
        print(f"  GED sim:     {lds['ged_similarity']:.4f}")
        print(f"  Node Jaccard: {lds['jaccard_node']:.4f}")
        print(f"  Edge Jaccard: {lds['jaccard_edge']:.4f}")
        print(f"  Combined:     {lds['combined_similarity']:.4f}")

        # LDS with Bootstrap CI (node-based resampling)
        lds_boot = bootstrap_lds_ci(graph_l1, graph_l2, n_iterations=500)
        print(f"\nLDS Bootstrap CI (95%): [{lds_boot['ci_lower']}, {lds_boot['ci_upper']}]")
        print(f"Std Error: {lds_boot['std_error']}")
