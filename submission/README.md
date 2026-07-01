# LinguaGraph — BWKI 2026 Submission Package

> **Project**: Cross-Lingual Cognitive Structure Analysis  
> **Student**: [Name], [School], [Grade]  
> **Languages**: ZH (native) · DE (school) · EN (academic)

---

## 1. Research Question

> Do ZH/EN/DE languages systematically differ in how they organize knowledge — and can LLM-extracted knowledge graphs quantify these differences?

## 2. Core Contributions

| # | Contribution | Type |
|---|-------------|------|
| 1 | **LDS (Linguistic Divergence Score)** — graph-theoretic metric for cross-language structural divergence | Research |
| 2 | **Cross-lingual analysis framework** — textbook extraction → KG → LDS → comparison pipeline | Method |
| 3 | **CognitiveSpace** — interactive 3D visualization of cross-lingual knowledge structures | Demo |
| 4 | **Lightweight local inference** — runs on Qwen2.5-0.5B GGUF (CPU, no cloud API) | Engineering |

## 3. Key Results

| Metric | Value |
|--------|-------|
| Textbook corpus | 68 (45 ZH + 20 EN + 10 DE) |
| Knowledge graph | 574 concepts · 3538 relations |
| Trilingual alignment | 247 concepts (43%) |
| Education levels | 4 (elementary → university) |
| Structural conflicts | 0 |
| Human validation | In preparation (N=30) |

## 4. Deliverables

| Item | Location | How to open |
|------|----------|-------------|
| CognitiveSpace 3D | `cognitive-space/web/index.html` | Double-click |
| Research Workbench | `workbench/index.html` | Double-click |
| Paper drafts | `docs/paper/` | Any text editor |
| Project log | `docs/PROJECT_LOG.md` | Any text editor |
| Gold Dataset schema | `docs/gold_dataset_schema_v1.md` | Any text editor |
| All docs | `docs/` | — |

## 5. Technical Stack

| Component | Technology |
|-----------|-----------|
| Concept extraction | LLM (Qwen2.5-0.5B / OpenAI) |
| Knowledge graph | NetworkX |
| 3D viz | 3d-force-graph (Three.js) |
| Cross-language alignment | 30 shared concept IDs, deterministic hashing |
| Inference | llama.cpp GGUF / Ollama |
| Frontend (Workbench) | Flask / standalone HTML |

## 6. Ethics

- ✅ GDPR consent forms (ZH/DE/EN)
- ✅ No PII in repository
- ✅ Textbook sources CC-BY-SA / fair use
- ✅ Provenance tracked per concept

## 7. GitHub

`github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph`

```
submission/
├── idea/                    ← Ideenanmeldung (bis 28.06.)
│   ├── idee_anmeldung.md    ← Vollständiger Anmeldungstext
│   └── assets/              ← Optional: Screenshots, Diagramme
├── final/                   ← Projekteinreichung (bis 20.09.)
└── pitch/                   ← Video Pitch (für Finale)
```

## Ideenanmeldung — Prüfliste

- [ ] Projektname: **LinguaGraph — Wie Sprache das Denken formt** (44/60 Zeichen)
- [ ] Beschreibung: ~970/1000 Zeichen ✅
- [ ] Datenquellen: ~970/1000 Zeichen ✅
- [ ] Dateianhang (optional): Cognitive City Screenshot
- [ ] Team: Jiajun Rong (Einzelteilnahme)
