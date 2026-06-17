"""
CognitiveSpace Scoring Functions

MCL Score: how many expert connections are missing in student graph
LCD Score: how different are two language graphs for the same person
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

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


# ===== LCD Scoring =====

def calculate_lcd_score(
    graph_l1: "nx.DiGraph",
    graph_l2: "nx.DiGraph",
    concept_mapping: Dict[str, str] = None
) -> Dict:
    """
    Language Cognitive Drift score.
    
    LCD = 1 - Graph_Similarity(G_l1, G_l2)
    
    Where similarity considers node overlap and edge overlap.
    """
    if nx is None:
        raise ImportError("networkx required")
    
    # Get edges as sets
    edges_l1 = set(graph_l1.edges())
    edges_l2 = set(graph_l2.edges())
    
    # If mapping provided, translate L1 edges to L2 language
    if concept_mapping:
        mapped_edges_l1 = set()
        for s, t in edges_l1:
            ms = concept_mapping.get(s, s)
            mt = concept_mapping.get(t, t)
            mapped_edges_l1.add((ms, mt))
        edges_l1 = mapped_edges_l1
    
    # Calculate overlap
    intersection = edges_l1 & edges_l2
    union = edges_l1 | edges_l2
    
    similarity = len(intersection) / max(len(union), 1)
    lcd = 1 - similarity
    
    return {
        "lcd_score": round(lcd, 4),
        "similarity": round(similarity, 4),
        "shared_edges": len(intersection),
        "total_unique_edges": len(union),
        "l1_only": len(edges_l1 - edges_l2),
        "l2_only": len(edges_l2 - edges_l1)
    }


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
        
        # LCD
        graph_l1 = nx.DiGraph()
        graph_l1.add_edges_from([("导数", "变化率"), ("积分", "面积")])
        graph_l2 = nx.DiGraph()
        graph_l2.add_edges_from([("Ableitung", "Änderungsrate"), ("Integral", "Fläche")])
        
        lcd = calculate_lcd_score(graph_l1, graph_l2)
        print(f"\nLCD Score: {lcd['lcd_score']}")
        print(f"Similarity: {lcd['similarity']}")
