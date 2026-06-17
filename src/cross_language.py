"""
Cross-Language Cognitive Gap Detection Module

Compares student's knowledge graphs across languages to find
gaps caused by language switching, not knowledge deficiency.

Core insight: "Why does a student understand a concept in Chinese
but fail to use it in German?"
"""

from typing import List, Dict, Optional
from enum import Enum

try:
    import networkx as nx
except ImportError:
    nx = None


class GapType(str, Enum):
    """Types of cross-language cognitive gaps"""
    CONCEPT_ABSENT = "concept_absent"           # Concept exists in L1 but not L2
    RELATION_BROKEN = "relation_broken"         # Relation exists in L1 but not L2
    MAPPING_MISSING = "mapping_missing"         # No L1-L2 concept mapping exists
    STRUCTURAL_SHIFT = "structural_shift"       # Graph structure differs significantly
    TERMINOLOGY_CONFUSION = "terminology_confusion"  # Similar terms, different meanings


class CrossLanguageGap:
    """Represents a cognitive gap caused by language switching"""

    def __init__(
        self,
        gap_type: GapType,
        concept_l1: str,
        concept_l2: Optional[str],
        language_l1: str,
        language_l2: str,
        confidence: float,
        severity: str,
        explanation: str
    ):
        self.gap_type = gap_type
        self.concept_l1 = concept_l1
        self.concept_l2 = concept_l2
        self.language_l1 = language_l1
        self.language_l2 = language_l2
        self.confidence = confidence
        self.severity = severity
        self.explanation = explanation

    def to_dict(self) -> dict:
        return {
            "type": self.gap_type.value,
            "concept_l1": self.concept_l1,
            "concept_l2": self.concept_l2,
            "language_l1": self.language_l1,
            "language_l2": self.language_l2,
            "confidence": self.confidence,
            "severity": self.severity,
            "explanation": self.explanation
        }


def detect_cross_language_gaps(
    graph_l1: "nx.DiGraph",
    graph_l2: "nx.DiGraph",
    concept_mapping: Dict[str, str],
    language_l1: str = "zh",
    language_l2: str = "de",
    expert_graph: Optional["nx.DiGraph"] = None
) -> List[CrossLanguageGap]:
    """
    Detect cognitive gaps caused by language switching.

    Args:
        graph_l1: Student's knowledge graph in language 1 (e.g., Chinese)
        graph_l2: Student's knowledge graph in language 2 (e.g., German)
        concept_mapping: Mapping from L1 concepts to L2 concepts
                         e.g., {"导数": "Ableitung", "极限": "Grenzwert"}
        language_l1: Language 1 code
        language_l2: Language 2 code
        expert_graph: Optional expert graph for severity assessment

    Returns:
        List of CrossLanguageGap objects
    """
    gaps = []

    # Layer 1: Concept Absence
    # Find concepts in L1 that don't appear in L2
    l1_concepts = set(graph_l1.nodes())
    l2_concepts = set(graph_l2.nodes())

    for concept_l1 in l1_concepts:
        concept_l2 = concept_mapping.get(concept_l1)

        if concept_l2 is None:
            # No mapping exists
            gaps.append(CrossLanguageGap(
                gap_type=GapType.MAPPING_MISSING,
                concept_l1=concept_l1,
                concept_l2=None,
                language_l1=language_l1,
                language_l2=language_l2,
                confidence=1.0,
                severity="high",
                explanation=f"概念 '{concept_l1}' 没有对应的{language_l2}翻译"
            ))
        elif concept_l2 not in l2_concepts:
            # Mapping exists but concept not used in L2
            gaps.append(CrossLanguageGap(
                gap_type=GapType.CONCEPT_ABSENT,
                concept_l1=concept_l1,
                concept_l2=concept_l2,
                language_l1=language_l1,
                language_l2=language_l2,
                confidence=0.9,
                severity="high",
                explanation=f"学生知道 '{concept_l1}' ({language_l1})，但在{language_l2}回答中没有使用 '{concept_l2}'"
            ))

    # Layer 2: Relation Broken
    # Find relations in L1 that don't exist in L2
    l1_edges = set(graph_l1.edges())
    l2_edges = set(graph_l2.edges())

    for source_l1, target_l1 in l1_edges:
        source_l2 = concept_mapping.get(source_l1)
        target_l2 = concept_mapping.get(target_l1)

        if source_l2 and target_l2:
            if (source_l2, target_l2) not in l2_edges:
                # Relation exists in L1 but not in L2
                gaps.append(CrossLanguageGap(
                    gap_type=GapType.RELATION_BROKEN,
                    concept_l1=f"{source_l1} → {target_l1}",
                    concept_l2=f"{source_l2} → {target_l2}",
                    language_l1=language_l1,
                    language_l2=language_l2,
                    confidence=0.85,
                    severity="medium",
                    explanation=f"关系 '{source_l1}→{target_l1}' 在{language_l1}中存在，但在{language_l2}中缺失"
                ))

    # Layer 3: Structural Shift
    # Compare graph density and connectivity
    density_l1 = nx.density(graph_l1) if graph_l1.number_of_nodes() > 0 else 0
    density_l2 = nx.density(graph_l2) if graph_l2.number_of_nodes() > 0 else 0

    if abs(density_l1 - density_l2) > 0.2:
        severity = "high" if abs(density_l1 - density_l2) > 0.4 else "medium"
        gaps.append(CrossLanguageGap(
            gap_type=GapType.STRUCTURAL_SHIFT,
            concept_l1=f"密度: {density_l1:.2f}",
            concept_l2=f"密度: {density_l2:.2f}",
            language_l1=language_l1,
            language_l2=language_l2,
            confidence=0.7,
            severity=severity,
            explanation=f"{language_l1}图密度({density_l1:.2f})与{language_l2}图密度({density_l2:.2f})差异显著"
        ))

    # Sort by severity
    severity_order = {"high": 0, "medium": 1, "low": 2}
    gaps.sort(key=lambda x: severity_order.get(x.severity, 3))

    return gaps


def generate_bilingual_report(
    gaps: List[CrossLanguageGap],
    language_l1: str = "zh",
    language_l2: str = "de"
) -> str:
    """
    Generate a human-readable report of cross-language gaps.

    Args:
        gaps: List of CrossLanguageGap objects
        language_l1: Language 1 name
        language_l2: Language 2 name

    Returns:
        Formatted report string
    """
    if not gaps:
        return f"[OK] No significant cognitive gaps found between {language_l1} and {language_l2}."

    lines = []
    lines.append(f"[Brain] Cross-Language Cognitive Gap Report")
    lines.append(f"Languages: {language_l1} -> {language_l2}")
    lines.append("=" * 50)

    # Group by gap type
    concept_gaps = [g for g in gaps if g.gap_type == GapType.CONCEPT_ABSENT]
    relation_gaps = [g for g in gaps if g.gap_type == GapType.RELATION_BROKEN]
    mapping_gaps = [g for g in gaps if g.gap_type == GapType.MAPPING_MISSING]
    structural_gaps = [g for g in gaps if g.gap_type == GapType.STRUCTURAL_SHIFT]

    if concept_gaps:
        lines.append("")
        lines.append("[X] Concepts known in {0} but missing in {1}:".format(language_l1, language_l2))
        for gap in concept_gaps:
            lines.append(f"  * {gap.concept_l1} ({gap.concept_l2})")

    if relation_gaps:
        lines.append("")
        lines.append("[~] Relations broken across languages:")
        for gap in relation_gaps:
            lines.append(f"  * {gap.concept_l1} -> {gap.concept_l2}")

    if mapping_gaps:
        lines.append("")
        lines.append("[!] Concepts without translation:")
        for gap in mapping_gaps:
            lines.append(f"  * {gap.concept_l1}")

    if structural_gaps:
        lines.append("")
        lines.append("[i] Structural differences:")
        for gap in structural_gaps:
            lines.append(f"  * {gap.explanation}")

    lines.append("")
    lines.append("=" * 50)
    lines.append(f"Total gaps: {len(gaps)}")
    lines.append(f"High severity: {len([g for g in gaps if g.severity == 'high'])}")
    lines.append(f"Medium severity: {len([g for g in gaps if g.severity == 'medium'])}")

    return "\n".join(lines)


# --- Demo ---
if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 60)
    print("Cross-Language Cognitive Gap Detection Demo")
    print("=" * 60)

    # Create sample graphs
    graph_zh = nx.DiGraph()
    graph_zh.add_edges_from([
        ("导数", "函数"),
        ("积分", "导数"),
    ])

    graph_de = nx.DiGraph()
    graph_de.add_edges_from([
        ("Ableitung", "Funktion"),
        # Missing: Integral -> Ableitung relation
    ])

    # Concept mapping
    mapping = {
        "导数": "Ableitung",
        "函数": "Funktion",
        "积分": "Integral",
        "极限": "Grenzwert",
        "连续性": "Stetigkeit"
    }

    # Detect gaps
    gaps = detect_cross_language_gaps(
        graph_zh,
        graph_de,
        mapping,
        language_l1="zh",
        language_l2="de"
    )

    # Generate report
    report = generate_bilingual_report(gaps, "Chinese", "German")
    print(report)

    print("\n" + "=" * 60)
    print("Demo complete!")
