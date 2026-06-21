"""
LinguaGraph — Main Entry Point

Zero-config pipeline runner. Auto-detects available LLM (local GGUF
preferred, mock fallback). No API keys required.

Usage:
    python -m src.main                         # Demo with mock
    python -m src.main --answer "..." --lang zh  # Real analysis
"""

import json
import logging
from pathlib import Path

from extract import extract_concepts
from graph import build_graph, load_expert_graph, graph_to_dict, graph_stats
from compare import detect_missing_links
from explain import generate_simple_explanation
from logging_config import setup_logging

logger = logging.getLogger(__name__)


def run_pipeline(
    student_answer: str,
    language: str = "zh",
    domain: str = "calculus",
    use_mock: bool = False
) -> dict:
    """
    Run the complete LinguaGraph pipeline.

    Args:
        student_answer: Student's response text
        language: Language of the answer
        domain: Knowledge domain
        use_mock: Use mock extraction (no model needed)

    Returns:
        dict with all results
    """
    logger.info("=" * 50)
    logger.info("LinguaGraph Pipeline Starting...")
    logger.info(f"Language: {language} | Domain: {domain} | Mock: {use_mock}")

    # Step 1: Extract concepts
    logger.info("Step 1: Extracting concepts...")
    extracted = extract_concepts(student_answer, language, use_mock=use_mock)
    logger.info(f"  Found %d concepts, %d relations",
                len(extracted["concepts"]), len(extracted["relations"]))

    # Step 2: Build student graph
    logger.info("Step 2: Building knowledge graph...")
    student_graph = build_graph(extracted)
    stats = graph_stats(student_graph)
    logger.info(f"  Graph: %d nodes, %d edges", stats["nodes"], stats["edges"])

    # Step 3: Load expert graph
    logger.info("Step 3: Loading expert graph (%s)...", domain)
    try:
        expert_graph = load_expert_graph(domain)
        logger.info("  Expert: %d nodes, %d edges",
                     graph_stats(expert_graph)["nodes"],
                     graph_stats(expert_graph)["edges"])
    except FileNotFoundError:
        logger.warning("Expert graph not found for '%s' — using empty graph", domain)
        import networkx as nx
        expert_graph = nx.DiGraph()

    # Step 4: Detect missing links
    logger.info("Step 4: Detecting missing cognitive links...")
    missing = detect_missing_links(student_graph, expert_graph)
    high_severity = [m for m in missing if m["severity"] == "high"]
    logger.info("  Found %d missing links (%d high severity)",
                len(missing), len(high_severity))

    # Step 5: Generate explanation
    logger.info("Step 5: Generating explanation...")
    explanation = generate_simple_explanation(missing, language)

    logger.info("Pipeline complete!")
    if not use_mock:
        logger.info("  Model: %s", extracted.get("model", "unknown"))
    logger.info("=" * 50)

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
        save_result(result, f"outputs/{student['id']}.json")

    print("\n" + "=" * 50)
    print("Demo complete!")
    print("=" * 50)
