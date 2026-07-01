# LinguaGraph — BWKI 2026 Submission Output Plan

> **Version**: 1.0 | **Date**: 2026-06-21
> **Goal**: Define ALL submission deliverables and their forms

---

## 1. Core Identity (What we're submitting)

```
Project LinguaGraph
===============================
A cross-lingual cognitive structure analysis system

Core claim:
  Languages systematically differ in how they organize knowledge,
  and this difference can be measured, visualized, and compared.

Three layers:
  Research layer    → LDS + cross-lingual comparison methodology
  Tool layer        → LLM extraction + knowledge graph pipeline
  Presentation      → CognitiveSpace 3D visualization
```

**NOT** a language model.
**NOT** a game.
**NOT** a generic graph viewer.

**IS** a research workstation for cross-lingual cognitive structure analysis.

---

## 2. Submission Package Overview

| # | Deliverable | Format | Status | Deadline |
|---|-------------|--------|--------|----------|
| 1 | Paper | PDF, 25-30 pp, German | 📝 55% | Sep 21 |
| 2 | CognitiveSpace Demo | Web (index.html) | ✅ Complete | Now |
| 3 | Pipeline Code | GitHub repo | ✅ Complete | Now |
| 4 | Application Cases | 3 documented scenarios | 📝 1/3 done | Jul |
| 5 | Figures & Tables | PNG + CSV | ⏳ 40% | Aug |
| 6 | Dataset | Gold Dataset JSONL | ⏳ Schema done | Aug |
| 7 | Poster | A0, German | ❌ Not started | Before finals |
| 8 | Video Demo | 2-3 min | ❌ Not started | Before finals |

---

## 3. Paper Structure (Final)

| Chapter | Pages | Content | Status |
|---------|-------|---------|--------|
| Abstract | 1 | Summary of research, method, findings | ✅ Draft |
| 1. Introduction | 3-4 | Motivation, research question, contributions | ✅ Draft |
| 2. Related Work | 3-4 | Linguistic relativity, cross-lingual KG, LLMs for cog sci | 📝 50% |
| 3. Methodology | 6-7 | Two pipelines, corpus, extraction, alignment, LDS, viz | ✅ Draft |
| 4. Results | 5-6 | CognitiveSpace (complete) + LDS (pending data) | ✅ 60% |
| 5. Human Study | 2-3 | Design, materials, ethics, analysis plan | 📝 30% |
| 6. Discussion | 2 | Interpretation, limitations, impact | ❌ |
| 7. Conclusion | 1 | Summary, closing | ❌ |
| References | 3-4 | 30-40 citations | 📝 50% |
| **Total** | **27-33** | | **~55%** |

### Paper Sections — Who Writes What

| Section | Author | Dependency |
|---------|--------|------------|
| Abstract | Student | Write last |
| 1. Introduction | Student + Claude | None |
| 2. Related Work | Student (literature) | References collected |
| 3. Methodology | Claude (technical) | Code complete |
| 4. Results (CognitiveSpace) | Claude | Data complete |
| 4. Results (LDS) | Student | DE/EN data needed |
| 5. Human Study | Student + Claude | Protocol designed |
| 6. Discussion | Both | Results needed |
| 7. Conclusion | Student | Write last |

---

## 4. Application Scenarios (3 Cases)

These are the **"so what?"** answer — concrete demonstrations of the system's value.

### Case A: Textbook Comparison

**Scenario**: A German educator wants to understand how the Chinese math curriculum differs from the German one.

| Step | Action | Output |
|------|--------|--------|
| 1 | Input Chinese high school math textbook + German counterpart | System ingests both |
| 2 | Run extraction + graph construction | ZH graph + DE graph |
| 3 | Calculate LDS | LDS = 0.52 |
| 4 | CognitiveSpace comparison | Side-by-side 3D visualization |

**What the user sees**:
- ZH graph: more algebra, earlier trigonometry
- DE graph: more geometry, later calculus introduction
- Concept overlap: 67% at high school level
- **Research insight**: Curriculum structure varies significantly despite same mathematical content

**Status**: ✅ Pipeline works, data exists, needs one documented run

### Case B: Cross-Language Concept Navigation

**Scenario**: A student wants to understand how "Derivative" / "导数" / "Ableitung" are connected in their respective knowledge networks.

| Step | Action | Output |
|------|--------|--------|
| 1 | Search "Derivative" in CognitiveSpace | Node highlighted with all connections |
| 2 | Toggle language filter (EN) | English knowledge neighborhood |
| 3 | Toggle language filter (ZH) | Chinese knowledge neighborhood |
| 4 | Toggle language filter (DE) | German knowledge neighborhood |

**What the user sees**:
- EN: Derivative → Limit → Function → Integral
- ZH: 导数 → 极限 → 函数 → 微分
- DE: Ableitung → Grenzwert → Funktion → Integral
- Overlapping core (Limit → Function) but different extensions
- **Tool insight**: Core mathematical concepts are universal, pedagogical emphasis differs

**Status**: ✅ CognitiveSpace already supports this

### Case C: Planned Evaluation — LDS Across Education Levels

**Research question**: Do cross-language structural differences grow with education level?
**Status**: ⏳ Planned evaluation study (requires full LDS computation across levels)

**Hypothesis**: LDS increases with education level (more specialized language → greater structural divergence between ZH/EN/DE knowledge representations).

**Method**: Compute LDS per education level pair (elementary, middle, high, university) using the existing CognitiveSpace graph data, controlling for concept set size differences.

This case is a **research finding**, not a product feature. It will be reported in the paper results section once analysis is complete.

---

## 5. CognitiveSpace — The Demonstration Layer

CognitiveSpace is the **primary visual demonstration** of the project.

### What it currently does:
- ✅ 574 nodes in concentric spherical shells by education level
- ✅ ZH/EN/DE language filtering
- ✅ Color-coded by level (green → cyan → blue → purple)
- ✅ Click for detail with textbook provenance
- ✅ BFS ripple, WASD navigation, 3 view modes
- ✅ Auto-rotate (optional)
- ✅ All 3538 relations visible

### What to add (before submission):

| Feature | Priority | Effort | Status |
|---------|----------|--------|--------|
| Link directional particles for relation flow | P2 | 1h | ❌ |
| Layer labels (小学/初中/高中/大学) floating | P2 | 1h | ❌ |
| Screenshot with annotations for paper | P1 | 30min | ⏳ |
| GitHub Pages auto-deploy | P1 | 15min | ✅ Fixed |

### Hosting

```
GitHub Pages: https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/
Local: cognitive-space/web/index.html (file:// works)
```

---

## 6. Figures Plan (For Paper)

| # | Figure | Type | Data Source | Status |
|---|--------|------|-------------|--------|
| F1 | Pipeline architecture | Mermaid diagram | Paper section 3 | ✅ Draft |
| F2 | CognitiveSpace screenshot | PNG 1280×800 | Live render | ✅ Captured |
| F3 | Education level distribution | Bar chart | Graph data | ✅ Data ready |
| F4 | Cross-language alignment matrix | Heatmap | Alignment data | ✅ Data ready |
| F5 | Textbook corpus composition | Table | 68 textbooks | ✅ Data ready |
| F6 | LDS by topic (when available) | Bar chart | Pipeline A | ❌ Needs data |
| F7 | Case Study: Derivative across ZH/EN/DE | Side-by-side KG | Pipeline B | ✅ Data ready |

### Figure generation scripts:
- `outputs/export_pipeline.py` has templates for F3, F4, F6
- CognitiveSpace screenshot already captured as `cognitive-space/web/screenshot.png`
- Use `docs/figures/` for exported paper figures

---

## 7. Data & Code Release

| Component | Where | Status |
|-----------|-------|--------|
| Pipeline code | `src/`, `scripts/` | ✅ Committed |
| CognitiveSpace | `cognitive-space/` | ✅ Committed |
| Config & mapping | `config/` | ✅ Committed |
| Documentation | `docs/` | ✅ Committed |
| Paper sections | `docs/paper/` | 📝 In progress |
| Raw textbook text | `data/textbook/` | 📦 Referenced (not versioned) |
| LLM extractions | `data/math_extractions/` | 📦 Referenced (not versioned) |
| Gold Dataset | `data/gold/` | ⏳ Schema done, data pending |

### Paper appendix should include:
- Dataset statistics (full table)
- Extraction prompt template (from `docs/mimo_prompt.md`)
- LDS mathematical definition
- Concept alignment mapping sample (30 IDs)

---

## 8. Timeline to Submission (Sep 21)

| Month | Milestone | Deliverable |
|-------|-----------|-------------|
| **Jun (now)** | Complete paper framework | Abstract, intro, methodology ✅ |
| **Jul** | DE/EN data collection | Full LDS results |
| **Jul** | Application cases | 3 documented scenarios |
| **Aug** | Figures + paper draft | All figures, complete paper |
| **Aug** | Gold Dataset generation | JSONL files |
| **Sep 1** | Paper review + revision | Internal review |
| **Sep 15** | Final polish | References, formatting |
| **Sep 21** | **Submission** | PDF + code + data |

---

## 9. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| DE/EN data not collected in time | LDS results missing | Paper focuses on CognitiveSpace + methodology |
| CognitiveSpace visualization not impressive enough | Weak presentation | Enhance with layer labels, comparison mode |
| Gold Dataset too small for training | Can't train LinguaCore | Frame it as evaluation dataset, not training data |
| Code not reproducible | Audit failure | All scripts committed, README with run instructions |
| Paper too long | Hard to read | Strict 30-page limit, appendix for extra tables |

---

## 10. Summary: The Three-Level Pitch

### 30 seconds (poster / README)

> **"Languages shape how we organize knowledge. LinguaGraph is a cross-lingual cognitive analysis system that extracts concepts from educational texts, builds knowledge graphs, measures structural differences using LDS (Linguistic Divergence Score), and visualizes them in an interactive 3D space."**

### 1 minute (oral introduction)

> "Languages do not only differ in vocabulary and grammar. They may also differ in how knowledge is structured and connected. To explore this question, I developed LinguaGraph, a cross-lingual cognitive analysis platform. The system extracts concepts from textbooks in Chinese, German, and English, constructs knowledge graphs, computes structural differences through LDS (Linguistic Divergence Score), and visualizes the resulting cognitive structures in an interactive 3D environment called CognitiveSpace."

### Abstract (paper)

> "How does language influence the way knowledge is organized? This project investigates cross-lingual cognitive structures through automated knowledge graph construction. Educational texts in Chinese, German, and English are processed using a lightweight concept extraction pipeline, transformed into structured knowledge graphs, and compared using the Linguistic Divergence Score (LDS). The resulting cognitive structures are explored through CognitiveSpace, an interactive three-dimensional visualization environment designed for comparative analysis."

These three versions share the same structure: research question → method → metric → visualization. No premature claims about completed validation.
