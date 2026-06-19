"""
LLM Concept Extraction Module

This module handles:
1. Sending student answers to LLM via pluggable Provider
2. Parsing structured JSON responses
3. Normalizing concepts (e.g., "微分"/"求导"/"导数" → "导数")

LLM Boundary: This is the ONLY module that calls LLM.
All other modules use deterministic algorithms.
"""

import json
import os
import re
from pathlib import Path
from typing import Optional

# Load prompts from config
PROMPTS_DIR = Path(__file__).parent.parent / "config" / "prompts"


def load_prompt(template_name: str) -> str:
    """Load a prompt template from config/prompts/"""
    prompt_file = PROMPTS_DIR / f"{template_name}.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Prompt template not found: {prompt_file}")


def extract_concepts(
    student_answer: str,
    language: str = "zh",
    use_mock: bool = False
) -> dict:
    """
    Extract concepts and relations from student answer using LLM.

    Args:
        student_answer: The student's response text
        language: Language code (zh/en/de)
        use_mock: Use mock response for demo (no API needed)

    Returns:
        dict with keys: concepts, relations, raw_response, language, model
    """
    if use_mock:
        return _mock_extract(student_answer, language)

    # Get provider from config
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).parent))
    from providers import get_provider
    from src.models import TaskRequest, TaskType, Language
    provider = get_provider()

    # Load and format prompt
    system_prompt = load_prompt("extract")
    user_prompt = f"Language: {language}\n\nStudent Answer:\n{student_answer}"

    # Build and route TaskRequest
    task_lang = Language.CHINESE
    if language == "de":
        task_lang = Language.GERMAN
    elif language == "en":
        task_lang = Language.ENGLISH

    request = TaskRequest(
        task=TaskType.CONCEPT_EXTRACTION,
        text=user_prompt,
        system_prompt=system_prompt,
        language=task_lang,
    )
    response = provider.generate(request)

    if not response.success:
        raise RuntimeError(f"LLM extraction failed: {response.error}")

    raw_response = response.raw_text

    # Parse JSON
    try:
        result = json.loads(raw_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}\nRaw: {raw_response}")

    # Validate structure
    if "concepts" not in result:
        raise ValueError("Missing 'concepts' key in response")
    if "relations" not in result:
        result["relations"] = []

    # Normalize concepts (handle synonyms)
    result["concepts"] = normalize_concepts(result["concepts"])
    result["relations"] = normalize_relations(result["relations"])

    return {
        "concepts": result["concepts"],
        "relations": result["relations"],
        "raw_response": raw_response,
        "language": language,
        "model": repr(provider)
    }


def _mock_extract(student_answer: str, language: str) -> dict:
    """
    Keyword-based mock extraction for testing.
    Extracts concepts that appear in the input text.
    """
    concept_dict = {
        "zh": {
            "导数": ["导数", "微分", "求导"],
            "变化率": ["变化率", "变化", "速率"],
            "极限": ["极限", "趋于", "趋近"],
            "函数": ["函数", "f(x)"],
            "积分": ["积分", "求积"],
            "面积": ["面积"],
            "斜率": ["斜率"],
            "链式法则": ["链式法则", "chain rule"],
            "复合函数": ["复合函数"],
            "微积分": ["微积分"],
        },
        "de": {
            "Ableitung": ["Ableitung", "ableiten", "Derivat"],
            "Änderungsrate": ["Änderungsrate", "Änderung"],
            "Grenzwert": ["Grenzwert", "Grenzwerte"],
            "Funktion": ["Funktion"],
            "Integral": ["Integral", "Integrieren"],
            "Fläche": ["Fläche"],
            "Analysis": ["Analysis"],
        },
        "en": {
            "derivative": ["derivative", "differentiation"],
            "rate of change": ["rate of change", "rate"],
            "limits": ["limits", "limit"],
            "function": ["function"],
            "integration": ["integration", "integral"],
            "area": ["area"],
            "calculus": ["calculus"],
            "differentiation": ["differentiation"],
        }
    }

    relation_patterns = [
        (["导数", "变化率"], ["变化率"], "represents"),
        (["积分", "导数"], ["导数"], "inverse_of"),
        (["极限", "导数"], ["导数"], "requires"),
        (["链式法则", "复合函数"], ["复合函数"], "is_part_of"),
        (["Ableitung", "Änderungsrate"], ["Änderungsrate"], "represents"),
        (["Integral", "Ableitung"], ["Ableitung"], "inverse_of"),
        (["Grenzwert", "Ableitung"], ["Ableitung"], "requires"),
        (["derivative", "rate of change"], ["rate of change"], "represents"),
        (["integration", "differentiation"], ["differentiation"], "inverse_of"),
        (["derivative", "limits"], ["limits"], "requires"),
    ]

    text = student_answer
    lang_dict = concept_dict.get(language, concept_dict["zh"])
    found_concepts = []

    for concept, keywords in lang_dict.items():
        for kw in keywords:
            if kw in text:
                found_concepts.append(concept)
                break

    found_relations = []
    for source_kws, target_kws, rel_type in relation_patterns:
        if all(any(kw in text for kw in kws) for kws in source_kws):
            source = source_kws[0]
            target = target_kws[0]
            if source in found_concepts and target in found_concepts:
                found_relations.append({"source": source, "target": target, "type": rel_type})

    return {
        "concepts": found_concepts,
        "relations": found_relations,
        "raw_response": json.dumps({"concepts": found_concepts, "relations": found_relations}, ensure_ascii=False),
        "language": language,
        "model": "mock"
    }


def normalize_concepts(concepts: list) -> list:
    """
    Normalize concept names to handle synonyms and case.

    Examples:
        "微分", "求导", "导数" → "导数"
        "Derivative", "derivative" → "derivative"
        "Flächen", "Fläche" → "Fläche"
    """
    norm_map = _load_normalization_map()

    # English lowercase mapping
    en_lower_map = {
        "Derivative": "derivative",
        "Differentiation": "differentiation",
        "Integration": "integration",
        "Calculus": "calculus",
        "Limits": "limits",
        "Function": "function",
        "Area": "area",
    }

    normalized = []
    for concept in concepts:
        if isinstance(concept, str):
            name = concept
        elif isinstance(concept, dict):
            name = concept.get("name", concept.get("concept", ""))
        else:
            continue

        # Apply normalization map
        if name in norm_map:
            name = norm_map[name]

        # Apply English lowercase
        if name in en_lower_map:
            name = en_lower_map[name]

        normalized.append(name)

    return list(set(normalized))


def normalize_relations(relations: list) -> list:
    """Normalize relation targets"""
    norm_map = _load_normalization_map()

    normalized = []
    for rel in relations:
        if isinstance(rel, dict):
            if "source" in rel and "target" in rel:
                source = norm_map.get(rel["source"], rel["source"])
                target = norm_map.get(rel["target"], rel["target"])
                normalized.append({
                    "source": source,
                    "target": target,
                    "type": rel.get("type", "relates_to")
                })
        elif isinstance(rel, list) and len(rel) >= 2:
            source = norm_map.get(rel[0], rel[0])
            target = norm_map.get(rel[1], rel[1])
            normalized.append({
                "source": source,
                "target": target,
                "type": rel[2] if len(rel) > 2 else "relates_to"
            })

    return normalized


def _load_normalization_map() -> dict:
    """Load concept normalization map from config"""
    norm_file = Path(__file__).parent.parent / "config" / "normalization_map.json"
    if norm_file.exists():
        return json.loads(norm_file.read_text(encoding="utf-8"))
    return {}


# --- Simple Demo ---
if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    sample = "导数表示变化率，积分是导数的逆运算。"

    print("=== CognitiveSpace Concept Extraction Demo ===\n")
    print(f"Input: {sample}\n")

    result = extract_concepts(sample, language="zh")
    print(f"Model: {result['model']}")
    print(f"Concepts: {result['concepts']}")
    print(f"Relations: {result['relations']}")
    print("\n[OK] Demo complete!")
