"""
Schema utilities for CognitiveSpace

Provides consistent relation key handling across all modules.
Gold data uses 'from/to', LLM output uses 'source/target'.
This module normalizes both formats.
"""

from typing import Dict, List


def normalize_relation(rel: Dict) -> Dict:
    """
    Normalize a relation dict to standard format: {source, target, type}.
    
    Handles both:
    - {"from": "A", "to": "B", "type": "prerequisite"}
    - {"source": "A", "target": "B", "type": "prerequisite"}
    """
    return {
        "source": rel.get("from") or rel.get("source", ""),
        "target": rel.get("to") or rel.get("target", ""),
        "type": rel.get("type", "relates_to")
    }


def normalize_relation_pair(rel: Dict) -> tuple:
    """Extract (source, target) pair from relation dict."""
    n = normalize_relation(rel)
    return (n["source"], n["target"])


def normalize_relation_triple(rel: Dict) -> tuple:
    """Extract (source, target, type) triple from relation dict."""
    n = normalize_relation(rel)
    return (n["source"], n["target"], n["type"])


def relations_match(r1: Dict, r2: Dict) -> bool:
    """Check if two relations are equivalent (ignoring key naming)."""
    return normalize_relation_triple(r1) == normalize_relation_triple(r2)


# === Concept Normalization ===

# German plural → singular
DE_PLURALS = {
    "Flächen": "Fläche",
    "Grenzwerte": "Grenzwert",
    "Funktionen": "Funktion",
    "Konzepte": "Konzept",
}

# German verb → noun
DE_VERB_TO_NOUN = {
    "ableiten": "Ableitung",
    "integrieren": "Integration",
    "differenzieren": "Differentiation",
}

# English lowercase
EN_LOWERCASE = {
    "Derivative": "derivative",
    "Differentiation": "differentiation",
    "Integration": "integration",
    "Calculus": "calculus",
    "Limits": "limits",
    "Function": "function",
    "Area": "area",
    "Continuity": "continuity",
}


def normalize_concept(concept: str, language: str = "auto") -> str:
    """
    Normalize a concept name.
    
    Handles:
    - German plurals → singular
    - German verbs → nouns
    - English case normalization
    """
    # Apply language-specific normalization
    if language in ("de", "auto"):
        if concept in DE_PLURALS:
            return DE_PLURALS[concept]
        if concept in DE_VERB_TO_NOUN:
            return DE_VERB_TO_NOUN[concept]
    
    if language in ("en", "auto"):
        if concept in EN_LOWERCASE:
            return EN_LOWERCASE[concept]
    
    return concept
