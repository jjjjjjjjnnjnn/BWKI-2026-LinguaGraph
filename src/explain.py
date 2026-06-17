"""
Explanation Generation Module

Converts missing links into natural language explanations.
This module uses LLM for generating explanations, but the missing links
themselves are computed deterministically.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional

PROMPTS_DIR = Path(__file__).parent.parent / "config" / "prompts"


def generate_explanation(
    missing_links: List[Dict],
    language: str = "zh",
    student_context: Optional[str] = None,
    model: str = "gpt-4.1-mini",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
) -> str:
    """
    Generate a natural language explanation for missing cognitive links.

    Args:
        missing_links: Output from detect_missing_links()
        language: Output language (zh/en/de)
        student_context: Optional student background info
        model: LLM model name
        api_key: API key
        base_url: Custom API base URL

    Returns:
        Human-readable explanation string
    """
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from providers import get_provider

    # Build context for LLM
    context = format_missing_links(missing_links)

    if student_context:
        context = f"Student Background:\n{student_context}\n\n{context}"

    # Load prompt template
    try:
        system_prompt = load_prompt("explain")
    except FileNotFoundError:
        # Fallback prompt
        system_prompt = """You are an educational AI assistant that explains
        why a student cannot learn certain concepts. Be encouraging and specific."""

    user_prompt = f"""Language: {language}

Missing Cognitive Links:
{context}

Please explain:
1. Why these gaps exist
2. How they connect
3. What the student should learn first to bridge them
4. A practical next step

Be concise and encouraging."""

    # Use provider system instead of direct OpenAI import
    provider = get_provider()
    return provider.extract(prompt=user_prompt, system=system_prompt)


def generate_simple_explanation(missing_links: List[Dict], language: str = "zh") -> str:
    """
    Generate a simple explanation WITHOUT LLM.
    Used for demo or when API is unavailable.
    """
    if not missing_links:
        return get_encouragement(language)

    lines = []
    lines.append(get_header(language))
    lines.append("")

    # Group by type
    missing_concepts = [l for l in missing_links if l["type"] == "missing_concept"]
    missing_relations = [l for l in missing_links if l["type"] == "missing_relation"]

    if missing_concepts:
        lines.append(get_concepts_header(language))
        for link in missing_concepts:
            concept = link["concept"]
            prereqs = link.get("prerequisites_missing", [])
            if prereqs:
                lines.append(get_prereq_message(language, concept, prereqs))
            else:
                lines.append(get_concept_missing_message(language, concept))

    if missing_relations:
        lines.append("")
        lines.append(get_relations_header(language))
        for link in missing_relations:
            source = link["source"]
            target = link["target"]
            lines.append(get_relation_message(language, source, target))

    lines.append("")
    lines.append(get_next_step(language, missing_links))

    return "\n".join(lines)


def format_missing_links(missing_links: List[Dict]) -> str:
    """Format missing links for LLM prompt"""
    lines = []

    for i, link in enumerate(missing_links, 1):
        lines.append(f"--- Missing Link #{i} ---")
        lines.append(f"Type: {link['type']}")
        lines.append(f"Severity: {link['severity']}")
        lines.append(f"Confidence: {link['confidence']:.0%}")

        if link["type"] == "missing_concept":
            lines.append(f"Missing Concept: {link['concept']}")
            if link.get("prerequisites"):
                lines.append(f"Prerequisites: {', '.join(link['prerequisites'])}")
            if link.get("prerequisites_present"):
                lines.append(f"Prerequisites Already Known: {', '.join(link['prerequisites_present'])}")

        elif link["type"] == "missing_relation":
            lines.append(f"Missing Connection: {link['source']} → {link['target']}")
            lines.append(f"Relation Type: {link['relation']}")

        lines.append("")

    return "\n".join(lines)


def load_prompt(template_name: str) -> str:
    """Load a prompt template"""
    prompt_file = PROMPTS_DIR / f"{template_name}.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Prompt template not found: {prompt_file}")


# --- Language-specific templates ---
def get_header(lang: str) -> str:
    headers = {
        "zh": "[Brain] 认知空间分析报告",
        "en": "[Brain] Cognitive Space Analysis Report",
        "de": "[Brain] Kognitionsraum-Analysebericht"
    }
    return headers.get(lang, headers["zh"])


def get_concepts_header(lang: str) -> str:
    headers = {
        "zh": "[X] 缺失的概念：",
        "en": "[X] Missing Concepts:",
        "de": "[X] Fehlende Konzepte:"
    }
    return headers.get(lang, headers["zh"])


def get_relations_header(lang: str) -> str:
    headers = {
        "zh": "[~] 缺失的连接：",
        "en": "[~] Missing Connections:",
        "de": "[~] Fehlende Verbindungen:"
    }
    return headers.get(lang, headers["zh"])


def get_concept_missing_message(lang: str, concept: str) -> str:
    messages = {
        "zh": f"  • 概念「{concept}」在你的知识中缺失",
        "en": f"  • Concept '{concept}' is missing from your knowledge",
        "de": f"  • Konzept '{concept}' fehlt in Ihrem Wissen"
    }
    return messages.get(lang, messages["zh"])


def get_prereq_message(lang: str, concept: str, prereqs: list) -> str:
    prereq_str = "、".join(prereqs)
    messages = {
        "zh": f"  • 要理解「{concept}」，你需要先掌握：{prereq_str}",
        "en": f"  • To understand '{concept}', you first need: {prereq_str}",
        "de": f"  • Um '{concept}' zu verstehen, benötigen Sie zuerst: {prereq_str}"
    }
    return messages.get(lang, messages["zh"])


def get_relation_message(lang: str, source: str, target: str) -> str:
    messages = {
        "zh": f"  • 「{source}」和「{target}」之间缺少关联",
        "en": f"  • Missing link between '{source}' and '{target}'",
        "de": f"  • Fehlende Verbindung zwischen '{source}' und '{target}'"
    }
    return messages.get(lang, messages["zh"])


def get_next_step(lang: str, missing_links: list) -> str:
    # Find highest priority missing link
    high_severity = [l for l in missing_links if l["severity"] == "high"]
    if high_severity:
        focus = high_severity[0].get("concept", high_severity[0].get("source", ""))
    else:
        focus = missing_links[0].get("concept", missing_links[0].get("source", ""))

    messages = {
        "zh": f"[Next] 建议：从「{focus}」开始学习，这是你当前最大的知识缺口。",
        "en": f"[Next] Suggestion: Start with '{focus}' - this is your biggest knowledge gap.",
        "de": f"[Next] Empfehlung: Beginnen Sie mit '{focus}' - das ist Ihre größte Wissenslücke."
    }
    return messages.get(lang, messages["zh"])


def get_encouragement(lang: str) -> str:
    messages = {
        "zh": "[OK] 很棒！你对这个领域的概念理解得非常全面。没有发现明显的认知缺口。",
        "en": "[OK] Great! Your understanding of this domain is comprehensive. No significant cognitive gaps found.",
        "de": "[OK] Grossartig! Ihr Verstaendnis dieses Bereichs ist umfassend. Keine signifikanten kognitiven Luecken gefunden."
    }
    return messages.get(lang, messages["zh"])


# --- Simple Demo ---
if __name__ == "__main__":
    print("=== Explanation Generation Demo ===\n")

    # Simulated missing links
    demo_links = [
        {
            "type": "missing_concept",
            "concept": "Kettenregel",
            "prerequisites": ["Ableitung", "Funktion"],
            "prerequisites_present": ["Ableitung"],
            "prerequisites_missing": ["Funktion"],
            "confidence": 0.6,
            "severity": "medium"
        },
        {
            "type": "missing_relation",
            "source": "Integral",
            "target": "Ableitung",
            "relation": "inverse_of",
            "confidence": 0.8,
            "severity": "high"
        }
    ]

    # Generate explanation without LLM
    for lang in ["zh", "en", "de"]:
        print(f"\n--- {lang.upper()} ---")
        explanation = generate_simple_explanation(demo_links, lang)
        print(explanation)

    print("\n✅ Explanation generation works!")
    print("💡 Connect to LLM API for more natural explanations.")
