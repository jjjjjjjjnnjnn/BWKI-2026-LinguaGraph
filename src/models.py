"""
LinguaGraph Data Models

Standardized data models for the entire pipeline.
All modules should import from this file.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Language(str, Enum):
    CHINESE = "zh"
    GERMAN = "de"
    ENGLISH = "en"


class TaskType(str, Enum):
    """任务类型 — Router 根据任务类型分发到不同 Provider"""
    CONCEPT_EXTRACTION = "concept_extraction"
    RELATION_EXTRACTION = "relation_extraction"
    TRANSLATION = "translation"
    NPC_DIALOGUE = "npc_dialogue"
    BIOGRAPHY = "biography"
    ANNOTATION_ASSIST = "annotation_assist"


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


# ============================================================
# Provider Abstraction Layer — 模型无关的统一接口
# ============================================================

@dataclass
class TaskRequest:
    """
    模型输入的标准格式。
    所有 Provider 接受统一的 TaskRequest，返回统一的 TaskResponse。
    """
    task: TaskType                           # 任务类型
    text: str                                # 输入文本
    language: Language = Language.CHINESE    # 文本语言
    system_prompt: Optional[str] = None      # 可选系统提示词
    max_tokens: int = 512                    # 最大生成长度
    temperature: float = 0.1                 # 生成温度
    metadata: dict = field(default_factory=dict)  # 附加元数据


@dataclass
class TaskResponse:
    """
    模型输出的标准格式。
    无论底层是 OpenAI / Ollama / GGUF / WebLLM，格式统一。
    """
    task: TaskType                            # 任务类型
    raw_text: str = ""                        # 原始生成文本
    structured: Optional[dict] = None         # 结构化输出 (JSON parsed)
    confidence: float = 1.0                   # 置信度
    tokens_in: int = 0                        # 输入 token 数
    tokens_out: int = 0                       # 输出 token 数
    latency_ms: float = 0.0                   # 推理延迟 (ms)
    error: Optional[str] = None               # 错误信息 (失败时非空)
    metadata: dict = field(default_factory=dict)  # 附加元数据

    @property
    def success(self) -> bool:
        """是否成功"""
        return self.error is None
