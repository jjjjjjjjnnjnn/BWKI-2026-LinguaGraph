# LinguaGraph Processing Workbench — Architecture

> **Goal**: Upload textbook → LLM processing → auto-generate 3D knowledge graph
> **Principle**: All processing uses existing pipeline code. No new research.

---

## 1. User Flow

```
User opens workbench
    ↓
Uploads PDF or pastes text (ZH/EN/DE)
    ↓
Selects language (auto-detect or manual)
    ↓
Clicks "Analyze"
    ↓
[Progress: Extracting concepts... → Building graph... → Rendering 3D...]
    ↓
Sees: Interactive 3D knowledge graph + Analysis report
```

## 2. Architecture

```
┌─────────────────────────────────────────────────────┐
│  Web UI (workbench/index.html)                      │
│  Upload → Progress → CognitiveSpace iframe + Report │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP / Fetch
┌──────────────────────┴──────────────────────────────┐
│  Backend (workbench/server.py)                      │
│                                                     │
│  POST /upload → receives file/text                   │
│      ↓                                              │
│  PDF extractor (PyMuPDF) → plain text                │
│      ↓                                              │
│  LLM extractor (Qwen/Ollama/OpenAI) → concepts+rels  │
│      ↓                                              │
│  Graph builder (existing code) → JSON                │
│      ↓                                              │
│  Data exporter → CognitiveSpace-compatible data.js   │
│      ↓                                              │
│  Returns: results.json + redirect to visualization   │
└─────────────────────────────────────────────────────┘
```

## 3. Components

### A. Frontend
Single HTML page with:
- Upload zone (drag & drop file or paste text)
- Language selector (ZH/EN/DE)
- Processing progress indicator
- Results display (graph stats + embedded CognitiveSpace)
- Report section

### B. Backend (workbench/server.py)

| Endpoint | Method | Input | Output |
|----------|--------|-------|--------|
| `/upload` | POST | File + language | Job ID |
| `/status/<job_id>` | GET | — | Progress JSON |
| `/result/<job_id>` | GET | — | Graph data |
| `/viz/<job_id>/index.html` | GET | — | Standalone 3D viz |

### C. Processing pipeline (reuses existing code)

```python
from src.extract import extract_from_text  # existing
from src.graph import build_graph          # existing
from src.models import Concept, Relation   # existing
```

Processing order:
1. PDF→text: PyMuPDF (if PDF uploaded)
2. Concept extraction: LLM call via existing provider
3. Graph construction: co-occurrence + relation extraction
4. Data export: Generate CognitiveSpace-compatible JSON

## 4. LLM Strategy

Three backends supported (choosable by user):

| Backend | Setup | Quality | Speed |
|---------|-------|---------|-------|
| **Qwen2.5-0.5B** (local GGUF) | Already downloaded | Low–Medium | Fast |
| **Ollama** (local) | Needs running | Medium | Medium |
| **OpenAI API** (cloud) | Needs API key | High | Fast |

Default: Try local Qwen first, fallback to prompt template.

## 5. File Structure

```
workbench/
├── index.html          # Upload UI (standalone)
├── demo.html           # Or combined SPA
├── server.py           # Flask/FastAPI backend
├── processor.py        # Pipeline orchestration
├── templates/          # (if using Flask templates)
└── output/             # Generated visualizations
    └── <job_id>/
        ├── data.js
        ├── index.html  # Self-contained 3D viz
        └── report.json
```

## 6. Existing Code Reuse

| Component | Existing Location | Reuse? |
|-----------|------------------|--------|
| Concept extraction prompt | `config/prompts/extract.md` | ✅ Direct |
| LLM provider abstraction | `src/providers/` | ✅ Direct |
| Graph construction | `src/graph.py` | ✅ Direct |
| Data export | `cognitive-space/scripts/export_graph.py` | ✅ Adapt |
| 3D visualization | `cognitive-space/web/index.html` | ✅ Template |
| Education level detection | `config/concept_taxonomy.json` | ✅ Direct |

## 7. Deliverable

After building:

1. **User uploads** a textbook chapter (PDF or text)
2. **System processes** it via local LLM
3. **Generates** a customized 3D knowledge graph
4. **User explores** the interactive visualization
5. **Comparison**: Upload another language's version to see differences

This directly answers the reviewer question: "What can someone DO with this system?"
