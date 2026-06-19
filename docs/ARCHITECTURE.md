# LinguaGraph System Architecture

> **Model-Agnostic Provider Layer**
>
> LinguaGraph's LLM infrastructure is designed as a **pluggable, task-routed provider system**.
> The research pipeline never knows which model is running — it only speaks `TaskRequest` / `TaskResponse`.

---

## Architecture Overview

```
                  ┌──────────────────────┐
                  │     TaskRequest       │
                  │  (task, text, lang)   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     Task Router       │
                  │  (routes by task type)│
                  └──────────┬───────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  OpenAIProvider  │ │  OllamaProvider  │ │  LocalProvider   │
│  (Research)      │ │  (Development)   │ │  (Runtime/MML)   │
│  concept_extract │ │  translation     │ │  npc_dialogue    │
│  relation_extract│ │                  │ │  annotation_assist│
└─────────────────┘ └─────────────────┘ └─────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     TaskResponse      │
                  │ (raw_text, structured)│
                  └──────────────────────┘
```

---

## Core Components

### 1. TaskRequest / TaskResponse (src/models.py)

Unified data contract. Every provider speaks the same protocol.

```python
@dataclass
class TaskRequest:
    task: TaskType        # concept_extraction, npc_dialogue, ...
    text: str             # input text
    language: Language    # zh / de / en
    system_prompt: str    # optional system prompt
    max_tokens: int       # generation budget
    temperature: float    # 0.0-1.0

@dataclass  
class TaskResponse:
    task: TaskType
    raw_text: str         # generated text
    confidence: float     # 0.0-1.0
    latency_ms: float     # inference time
    error: str            # None if successful
```

### 2. Provider Base Class (src/providers/base.py)

```python
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, request: TaskRequest) -> TaskResponse: ...
    @abstractmethod
    def is_available(self) -> bool: ...
```

Four implementations:

| Provider | Backend | Use Case | Status |
|----------|---------|----------|--------|
| `OpenAIProvider` | GPT-4.1-mini API | Research extraction | ✅ Stable |
| `OllamaProvider` | Local LLM via Ollama | Development / offline | ✅ Stable |
| `LocalProvider` | llama.cpp GGUF subprocess | MML Runtime / game | ✅ New |
| `MockProvider` | Deterministic stub | Testing / CI | ✅ New |

### 3. Task Router (src/providers/router.py)

Routes by task type with automatic fallback:

```yaml
# config.yaml
llm:
  routing:
    concept_extraction: research      # → OpenAI
    npc_dialogue: runtime             # → Local GGUF
    annotation_assist: runtime        # → Local GGUF
  defaults:
    - research                        # try first
    - runtime                         # then local
    - mock                            # never fail
```

### 4. Provider Independence

The pipeline **never imports a specific provider**. It only calls:

```python
from src.providers import create_router
router = create_router()
response = router.route(TaskRequest(task="concept_extraction", text="..."))
```

---

## Research Integrity

The Provider Abstraction Layer guarantees:

1. **Reproducibility** — All published results use a pinned provider/config
2. **Auditability** — Every TaskResponse records latency, tokens, and confidence
3. **Isolation** — Model changes don't affect LDS computation (models.py, scoring.py unchanged)
4. **Fallback safety** — Automatic mock fallback prevents silent failures

---

## Cross-Project Reuse

This architecture serves three independent projects from the same code:

| Project | Provider | Adapter |
|---------|----------|---------|
| LinguaGraph (BWKI) | OpenAI / Ollama | Concept Extraction LoRA |
| MML Runtime | Local GGUF | NPC Dialogue LoRA |
| Game (Aftermask) | Local GGUF (GDExtension) | Character / Narrative LoRA |

All share: `TaskRequest` / `TaskResponse`, `Router`, fallback chain.
Only differ: `Provider` backend, `LoRA` adapter.

---

## How to Use

```python
# 1. Create router (auto-configures from config.yaml)
from src.providers import create_router
router = create_router()

# 2. Route a request
from src.models import TaskRequest, TaskType
response = router.route(
    TaskRequest(task=TaskType.CONCEPT_EXTRACTION, text="Freedom means...")
)

# 3. Use the response
if response.success:
    concepts = response.structured or response.raw_text
else:
    print(f"Error: {response.error}")
    # Fallback logic here
```

---

*Document: ARCHITECTURE.md v1.0 · 2026-06-19*
