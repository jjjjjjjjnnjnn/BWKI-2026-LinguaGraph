"""
CognitiveSpace - Missing Cognitive Links Detection System
Main Entry Point

This is the simplest working version - just the pipeline.
"""

import json
from pathlib import Path

from extract import extract_concepts
from graph import build_graph, load_expert_graph, graph_to_dict, graph_stats
from compare import detect_missing_links
from explain import generate_simple_explanation


def run_pipeline(
    student_answer: str,
    language: str = "zh",
    domain: str = "calculus",
    use_mock: bool = False
) -> dict:
    """
    Run the complete CognitiveSpace pipeline.

    Args:
        student_answer: Student's response text
        language: Language of the answer
        domain: Knowledge domain
        use_mock: Use mock extraction (no API key needed)

    Returns:
        dict with all results
    """
    print("[Brain] CognitiveSpace Pipeline Starting...\n")

    # Step 1: Extract concepts
    print("Step 1: Extracting concepts...")
    extracted = extract_concepts(student_answer, language, use_mock=use_mock)
    print(f"  Found {len(extracted['concepts'])} concepts, {len(extracted['relations'])} relations")

    # Step 2: Build student graph
    print("\nStep 2: Building knowledge graph...")
    student_graph = build_graph(extracted)
    stats = graph_stats(student_graph)
    print(f"  Graph: {stats['nodes']} nodes, {stats['edges']} edges")

    # Step 3: Load expert graph
    print(f"\nStep 3: Loading expert graph ({domain})...")
    try:
        expert_graph = load_expert_graph(domain)
        print(f"  Expert: {graph_stats(expert_graph)['nodes']} nodes, {graph_stats(expert_graph)['edges']} edges")
    except FileNotFoundError:
        print(f"  [!] Expert graph not found for '{domain}'")
        print("  Using empty expert graph for demo")
        import networkx as nx
        expert_graph = nx.DiGraph()

    # Step 4: Detect missing links
    print("\nStep 4: Detecting missing cognitive links...")
    missing = detect_missing_links(student_graph, expert_graph)
    high_severity = [m for m in missing if m["severity"] == "high"]
    print(f"  Found {len(missing)} missing links ({len(high_severity)} high severity)")

    # Step 5: Generate explanation
    print("\nStep 5: Generating explanation...")
    explanation = generate_simple_explanation(missing, language)

    print("\n[OK] Pipeline complete!\n")

    return {
        "extracted": extracted,
        "student_graph": graph_to_dict(student_graph),
        "missing_links": missing,
        "explanation": explanation,
        "stats": {
            "concepts_extracted": len(extracted["concepts"]),
            "relations_extracted": len(extracted["relations"]),
            "missing_links_count": len(missing),
            "high_severity_count": len(high_severity)
        }
    }


def save_result(result: dict, output_path: str):
    """Save pipeline result to JSON file"""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"💾 Result saved to: {output_file}")


# --- Demo ---
if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 50)
    print("CognitiveSpace v0.1.0 - Demo")
    print("=" * 50)

    # Test with sample data
    SAMPLE_STUDENTS = [
        {"id": "zh_001", "language": "zh", "answer": "我知道导数表示变化率，但不知道为什么需要极限。"},
        {"id": "de_001", "language": "de", "answer": "Ableitung ist die Änderungsrate einer Funktion an einem Punkt."},
        {"id": "en_001", "language": "en", "answer": "The derivative represents the rate of change of a function."},
    ]

    for student in SAMPLE_STUDENTS[:1]:  # Just first one for demo
        print(f"\nStudent ID: {student['id']}")
        print(f"Language: {student['language']}")
        print(f"Answer preview: {student['answer'][:100]}...")

        result = run_pipeline(
            student_answer=student["answer"],
            language=student["language"],
            domain="social_issues",
            use_mock=True
        )

        print("\nExplanation:")
        print(result["explanation"])

        # Save result
        save_result(result, f"output/{student['id']}.json")

    print("\n" + "=" * 50)
    print("Demo complete!")
    print("=" * 50)
