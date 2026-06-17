"""
Concept Mapping Layer — Cross-Lingual Concept Alignment
========================================================

Maps extracted concepts across languages to enable meaningful
Jaccard similarity computation.

Without this mapping:
  工作, work, Arbeit → Jaccard = 0 (three different strings)

With this mapping:
  工作→work, work→work, Arbeit→work → Jaccard = 1.0 (same concept)

Usage:
    python research/concept_mapping.py
"""

import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# =============================================================================
# CORE CONCEPT MAP: zh ↔ en ↔ de
# =============================================================================

CONCEPT_MAP = {
    # Freedom cluster
    "自由": "freedom", "Freiheit": "freedom",
    "liberty": "freedom", "自治": "autonomy", "Autonomie": "autonomy",
    "权利": "rights", "Recht": "rights", "Rechte": "rights",

    # Justice cluster
    "正义": "justice", "Gerechtigkeit": "justice", "公平": "fairness",
    "Fairness": "fairness", "公正": "impartiality",

    # Responsibility cluster
    "责任": "responsibility", "Verantwortung": "responsibility",
    "义务": "duty", "Pflicht": "duty", "职责": "obligation",

    # Knowledge cluster
    "知识": "knowledge", "Wissen": "knowledge",
    "学习": "learning", "Lernen": "learning",
    "教育": "education", "Bildung": "education",
    "智慧": "wisdom", "Weisheit": "wisdom",

    # Power cluster
    "权力": "power", "Macht": "power",
    "力量": "strength", "Kraft": "strength",

    # Success cluster
    "成功": "success", "Erfolg": "success",
    "成就": "achievement", "Leistung": "achievement",
    "目标": "goal", "Ziel": "goal",
    "事业": "career", "Karriere": "career",

    # Home cluster
    "家": "home", "Zuhause": "home", "Heimat": "homeland",
    "家庭": "family", "Familie": "family",
    "归属": "belonging", "Zugehoerigkeit": "belonging",

    # Time cluster
    "时间": "time", "Zeit": "time",
    "历史": "history", "Geschichte": "history",
    "未来": "future", "Zukunft": "future",
    "过去": "past", "Vergangenheit": "past",

    # Thought cluster
    "思维": "thought", "Gedanke": "thought", "Denken": "thinking",
    "认知": "cognition", "Kognition": "cognition",
    "理解": "understanding", "Verstaendnis": "understanding",
    "思考": "thinking",

    # Language cluster
    "语言": "language", "Sprache": "language",
    "表达": "expression", "Ausdruck": "expression",
    "沟通": "communication", "Kommunikation": "communication",

    # Culture cluster
    "文化": "culture", "Kultur": "culture",
    "传统": "tradition", "Tradition": "tradition",
    "价值观": "values", "Werte": "values",

    # Society cluster
    "社会": "society", "Gesellschaft": "society",
    "集体": "collective", "Kollektiv": "collective",
    "社区": "community", "Gemeinschaft": "community",

    # Individual cluster
    "个人": "individual", "Individuum": "individual",
    "自我": "self", "Selbst": "self",
    "身份": "identity", "Identitaet": "identity",

    # Emotion cluster
    "情感": "emotion", "Emotion": "emotion",
    "情绪": "feeling", "Gefuehl": "feeling",
    "幸福": "happiness", "Glueck": "happiness",
    "快乐": "joy", "Freude": "joy",

    # Moral cluster
    "道德": "morality", "Moral": "morality",
    "伦理": "ethics", "Ethik": "ethics",
    "善": "goodness", "Gut": "goodness",
    "恶": "evil", "Boese": "evil",

    # Truth cluster
    "真理": "truth", "Wahrheit": "truth",
    "真相": "reality", "Realitaet": "reality",

    # Nature cluster
    "自然": "nature", "Natur": "nature",
    "环境": "environment", "Umwelt": "environment",

    # Change cluster
    "变化": "change", "Veranderung": "change",
    "发展": "development", "Entwicklung": "development",
    "进步": "progress", "Fortschritt": "progress",

    # Work cluster
    "工作": "work", "Arbeit": "work",
    "劳动": "labor", "Arbeitskraft": "labor",
    "职业": "profession", "Beruf": "profession",
}


def map_concept(concept):
    """Map a concept to its English canonical form."""
    return CONCEPT_MAP.get(concept, CONCEPT_MAP.get(concept.lower(), concept))


def map_concepts(concepts):
    """Map a list of concepts to canonical English forms."""
    mapped = []
    for c in concepts:
        canonical = map_concept(c)
        if canonical not in mapped:
            mapped.append(canonical)
    return mapped


def map_graph(concepts, relations):
    """Map graph concepts and relations to canonical forms."""
    concept_mapping = {}
    for c in concepts:
        concept_mapping[c] = map_concept(c)

    mapped_concepts = list(set(concept_mapping.values()))

    mapped_relations = []
    for src, rel, tgt in relations:
        new_src = concept_mapping.get(src, src)
        new_tgt = concept_mapping.get(tgt, tgt)
        if new_src != new_tgt:
            mapped_relations.append((new_src, rel, new_tgt))

    return mapped_concepts, mapped_relations


if __name__ == "__main__":
    print("Concept Mapping Layer")
    print(f"Total mappings: {len(CONCEPT_MAP)}")

    test_cases = [
        (["成功", "努力", "家庭"], "zh"),
        (["success", "achievement", "goal"], "en"),
        (["Erfolg", "Leistung", "Ziel"], "de"),
    ]

    for concepts, lang in test_cases:
        mapped = map_concepts(concepts)
        print(f"  {lang}: {concepts} -> {mapped}")
