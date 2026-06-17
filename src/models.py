"""
LinguaGraph Data Models

Standardized data models for the entire pipeline.
All modules should import from this file.
"""

from dataclasses import dataclass, field
from enum import Enum


class Language(str, Enum):
    CHINESE = "zh"
    GERMAN = "de"
    ENGLISH = "en"


class GapType(str, Enum):
    CONCEPT_ABSENT = "concept_absent"
    RELATION_BROKEN = "relation_broken"
    MAPPING_MISSING = "mapping_missing"
    STRUCTURAL_SHIFT = "structural_shift"


class Severity(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Concept:
    id: str
    name: str
    name_zh: str = ""
    name_en: str = ""
    name_de: str = ""
    domain: str = ""
    confidence: float = 1.0
    importance: float = 0.5


@dataclass
class Relation:
    source: str
    target: str
    rel_type: str
    weight: float = 1.0
    evidence: str = ""


@dataclass
class ConceptGraph:
    concepts: dict[str, Concept] = field(default_factory=dict)
    relations: list[Relation] = field(default_factory=list)
    source: str = "unknown"
    lang: str = "zh"

    @property
    def node_count(self) -> int:
        return len(self.concepts)

    @property
    def edge_count(self) -> int:
        return len(self.relations)


@dataclass
class MissingLink:
    type: str
    concept: str = ""
    source: str = ""
    target: str = ""
    rel_type: str = ""
    confidence: float = 0.0
    severity: str = "low"
    explanation: str = ""


@dataclass
class AnalysisResult:
    student_graph: ConceptGraph
    expert_graph: ConceptGraph
    missing_links: list[MissingLink]
    lds: float = 0.0
    explanation: str = ""
    metadata: dict = field(default_factory=dict)
