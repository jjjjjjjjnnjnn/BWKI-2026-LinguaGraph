"""
Survey Evaluator

Processes survey responses through the pipeline:
  Raw survey → LLM extraction → Knowledge Graph → MCL detection

Usage:
  python tests/evaluate_survey.py --input data/survey/example_response_zh.json
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from extract import extract_concepts
from graph import build_graph
from compare import detect_missing_links


# ===== Per-Question Extraction Prompts =====

PROMPTS = {
    "Q01": "Extract 5 concept nodes from this vocabulary association. Output JSON: {\"nodes\": [...]}",
    
    "Q02": "Extract concepts and relations from this concept explanation. Output JSON: {\"nodes\": [...], \"edges\": [{\"source\": \"\", \"target\": \"\", \"type\": \"represents|requires|contrasts_with|is_part_of|causes|prerequisite\"}]}",
    
    "Q03": "Extract the untranslatable concept, its components, and whether it's missing in other languages. Output JSON: {\"concept_l1\": \"\", \"concept_l2\": \"\", \"components\": [...], \"missing_in_other\": true/false}",
    
    "Q04": "Extract key concepts from this translation. Output JSON: {\"nodes\": [...], \"edges\": [{\"source\": \"\", \"target\": \"\", \"type\": \"temporal_future|agent|object\"}]}",
    
    "Q05": "Extract key concepts from this translation. Output JSON: {\"nodes\": [...], \"edges\": [{\"source\": \"\", \"target\": \"\", \"type\": \"temporal_change|agent|object\"}]}",
    
    "Q06": "Extract key concepts from this translation. Output JSON: {\"nodes\": [...], \"edges\": [{\"source\": \"\", \"target\": \"\", \"type\": \"agent|spatial_from|spatial_to\"}]}",
    
    "Q07": "Extract key concepts from this translation. Output JSON: {\"nodes\": [...], \"edges\": [{\"source\": \"\", \"target\": \"\", \"type\": \"emotional|object\"}]}",
    
    "Q09": "Extract objects and spatial relations from this description. Output JSON: {\"nodes\": [...], \"edges\": [{\"source\": \"\", \"target\": \"\", \"type\": \"spatial_left_of|spatial_right_of\"}]}",
    
    "Q10": "Determine if this concept is hard to express and represents a missing cognitive link. Output JSON: {\"missing_concept\": \"\", \"mcl_candidate\": true/false}",
}


def extract_question(response):
    """Extract graph output from a single survey question using LLM."""
    qid = response["question_id"]
    raw = response["raw_input"]
    
    if qid == "Q08":
        # Q08 is structured (relation judgment), no LLM needed
        return {
            "nodes": [],
            "edges": []
        }
    
    prompt = PROMPTS.get(qid)
    if not prompt:
        return {"nodes": [], "edges": []}
    
    try:
        result = extract_concepts(
            f"{prompt}\n\nInput: {raw}",
            language="zh"  # Default to Chinese, will be overridden by survey language
        )
        # extract_concepts returns {"concepts": [...], "relations": [...]}
        nodes = result.get("concepts", [])
        edges = []
        for r in result.get("relations", []):
            if isinstance(r, dict):
                edges.append({
                    "source": r.get("source", ""),
                    "target": r.get("target", ""),
                    "type": r.get("type", "relates_to")
                })
        return {"nodes": nodes, "edges": edges}
    except Exception as e:
        print(f"  [WARN] Failed to extract {qid}: {e}")
        return {"nodes": [], "edges": []}


def merge_graphs(responses):
    """Merge all question outputs into a single knowledge graph."""
    all_nodes = set()
    all_edges = []
    
    for r in responses:
        graph = r.get("graph_output", {})
        all_nodes.update(graph.get("nodes", []))
        all_edges.extend(graph.get("edges", []))
    
    return {
        "nodes": list(all_nodes),
        "edges": all_edges
    }


def evaluate_survey(survey_path):
    """Process a complete survey response."""
    with open(survey_path, encoding="utf-8") as f:
        survey = json.load(f)
    
    print(f"Respondent: {survey['respondent_id']}")
    print(f"Language: {survey['language']}")
    print(f"Questions: {len(survey['responses'])}")
    print()
    
    # Step 1: Extract graph from each question
    print("Step 1: Extracting concepts per question...")
    for response in survey["responses"]:
        qid = response["question_id"]
        graph = extract_question(response)
        response["graph_output"] = graph
        print(f"  {qid}: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")
    
    # Step 2: Merge into single graph
    print("\nStep 2: Merging graphs...")
    merged = merge_graphs(survey["responses"])
    print(f"  Total: {len(merged['nodes'])} nodes, {len(merged['edges'])} edges")
    
    # Step 3: Build NetworkX graph
    print("\nStep 3: Building NetworkX graph...")
    student_graph = build_graph({
        "concepts": merged["nodes"],
        "relations": merged["edges"]
    })
    
    # Step 4: Load expert graph
    print("\nStep 4: Loading expert graph...")
    try:
        from graph import load_expert_graph
        expert_graph = load_expert_graph("calculus")
        print(f"  Expert: {len(expert_graph.nodes())} nodes, {len(expert_graph.edges())} edges")
    except FileNotFoundError:
        print("  [WARN] No expert graph found, skipping MCL detection")
        expert_graph = None
    
    # Step 5: Detect MCL
    if expert_graph:
        print("\nStep 5: Detecting Missing Cognitive Links...")
        missing = detect_missing_links(student_graph, expert_graph)
        print(f"  Found {len(missing)} missing links")
        for m in missing[:5]:
            print(f"    - {m.get('type')}: {m.get('concept', m.get('source', 'N/A'))}")
    
    # Return results
    return {
        "respondent_id": survey["respondent_id"],
        "language": survey["language"],
        "merged_graph": merged,
        "student_graph": student_graph,
        "missing_links": missing if expert_graph else [],
        "responses": survey["responses"]
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    args = parser.parse_args()
    
    result = evaluate_survey(args.input)
    print(f"\n{'='*50}")
    print(f"Evaluation complete for {result['respondent_id']}")
