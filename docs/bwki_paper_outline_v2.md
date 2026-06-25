# LinguaGraph — BWKI 2026 Paper (Updated Structure)

> **Version**: 2.0 | **Date**: 2026-06-21
> **Target**: 25-30 pages, German, PDF
> **Status**: ~55% complete → target 80% before DE/EN data arrival

---

## Core Narrative (Updated)

The paper now has **two complementary evidence threads**, both serving the same research question:

```
Research Question:
Do ZH/EN/DE languages systematically differ in knowledge organization?
```

| Thread | Evidence | Method | Status |
|--------|----------|--------|--------|
| **A. Cognitive Graph Pipeline** | Student-generated concept graphs | LLM extraction → LDS | ⏳ Waiting for DE/EN data |
| **B. Textbook Knowledge Graph** | Curriculum knowledge structures | MIMO extraction → 574 concepts | ✅ Complete |

Thread B (CognitiveSpace) provides **engineering validation** — it proves the extraction and graph construction pipeline works at scale, independent of the human study timeline.

---

## 1. Introduction (3-4 pages)

### 1.1 Personal Motivation
A bilingual student (ZH native, DE schooling, EN academic) observes that the same concepts feel different across languages. This personal experience becomes a research question.

### 1.2 Research Question
- **Primary**: Do ZH/EN/DE speakers organize knowledge differently?
- **Secondary**: Can LLM-extracted cognitive graphs capture these differences?
- **Secondary**: Is the Language Drift Score stable and interpretable?

### 1.3 Contributions
1. **Language Drift Score (LDS)**: A graph-theoretic metric quantifying cross-language cognitive divergence
2. **First cross-linguistic comparison** of mathematical knowledge structures across ZH/EN/DE textbooks
3. **CognitiveSpace**: A scalable 3D knowledge graph visualization (574 concepts, 3538 relations, 68 textbooks)
4. **Pipeline**: End-to-end system from textbook extraction → concept alignment → graph analysis → visualization

### 1.4 Paper Structure
Brief roadmap of sections.

---

## 2. Related Work (3-4 pages)

### 2.1 Linguistic Relativity Hypothesis
How language shapes thought. From Sapir-Whorf to modern empirical evidence.

### 2.2 Cross-Linguistic Knowledge Representation
Knowledge graphs, concept maps, and how structure differs across languages.

### 2.3 LLMs for Cognitive Science
Using LLMs as cognitive models (not just NLP tools). RISE (ICLR 2026), Separating Tongue from Thought (ACL 2025).

### 2.4 Educational Knowledge Graphs
Knowledge organization in curricula. How textbooks structure concepts across languages.

### 2.5 Research Gap
No existing work compares ZH/EN/DE mathematical knowledge structures at this scale.

---

## 3. Methodology (6-7 pages)

### 3.1 Overview

Two parallel pipelines:

```
Pipeline A (LinguaGraph):
Student Response → LLM Extraction → Cognitive Graph → LDS → Cross-Language Comparison

Pipeline B (CognitiveSpace):
Textbook Corpus → MIMO Extraction → Concept Graph → Alignment → 3D Visualization
```

### 3.2 Textbook Corpus (Pipeline B) [NEW]

| Language | Textbooks | Coverage |
|----------|-----------|----------|
| Chinese | 45 (Renjiao K-12, Tongji Calculus, Probability, Linear Algebra) | Elementary → University |
| English | 20 (Stewart Calculus, MIT OCW, Khan Academy, IGCSE, IB) | K-12 → University |
| German | 10 (Forster Analysis, Fischer LA, Lambacher Schweizer, Papula) | Secondary → University |
| **Total** | **68** | **574 concepts, 3538 relations** |

### 3.3 Concept Extraction
LLM-based extraction from textbook text. MIMO prompt engineering for structured output.

### 3.4 Graph Construction & Cross-Language Alignment
- Pipeline B: Merge → Deduplicate → Align (30 shared concept IDs across languages)
- Pipeline A: Co-occurrence graphs from student responses → LDS

### 3.5 The Language Drift Score (LDS)
Mathematical definition. Graph edit distance. Stability analysis.

### 3.6 CognitiveSpace Visualization
3D concentric shell layout using 3d-force-graph. ZH/EN/DE interactive filtering.
574 concepts arranged by education level with deterministic hash-based positioning.

---

## 4. Results (5-6 pages)

### 4.1 Pipeline B: CognitiveSpace Knowledge Graph

| Metric | Value |
|--------|-------|
| Total concepts | 574 |
| Total relations | 3538 |
| Cross-language alignment | 247 trilingual concepts (43%) |
| Education levels | 4 (elementary: 37, middle: 46, high: 193, university: 298) |
| Structural consistency | 0 conflicts, <0.5% isolated nodes |

**Key finding**: The cross-language alignment methodology successfully maps concepts across three languages with high structural consistency, demonstrating that the extraction and alignment pipeline works at scale.

### 4.2 Pipeline A: LDS Results (Pilot)
[Waiting for DE/EN data — methodology ready]

### 4.3 Stability Analysis
LDS metric stability across extraction methods and parameters.

---

## 5. Human Study Protocol (2-3 pages)

### 5.1 Design
- N=30 (10 ZH, 10 DE, 10 EN)
- Mixed within-subject + between-subject
- 5 topics, 3 languages

### 5.2 Materials & Procedure
Questionnaires, ethics, randomization.

### 5.3 Analysis Plan
Statistical tests, hypotheses, power analysis.

---

## 6. Discussion (2 pages)

### 6.1 Interpretation
What the results mean for linguistic relativity.

### 6.2 Limitations
Sample size, corpus coverage, language families.

### 6.3 Broader Impact
Implications for bilingual education, AI system design.

---

## 7. Conclusion (1 page)

---

## Figures & Tables (Updated)

| # | Figure | Content | Source |
|---|--------|---------|--------|
| F1 | Pipeline diagram | Two-thread architecture | New |
| F2 | CognitiveSpace screenshot | 574-node concentric shell | `cognitive-space/web/screenshot.png` |
| F3 | Education level distribution | 4-level bar chart | Graph data |
| F4 | Cross-language alignment matrix | 247/574 trilingual | Alignment data |
| F5 | LDS bar chart | Topic comparison | Pipeline A results |
| F6 | Case study concept graphs | ZH/EN/DE side-by-side | Pipeline A |
| T1 | Corpus statistics | 68 textbooks breakdown | Section 3.2 |
| T2 | Graph statistics | Nodes/edges/levels | Section 4.1 |
| T3 | Alignment coverage | Per-language statistics | Section 4.1 |
| T4 | LDS per topic | ZH-EN/DE-EN/ZH-DE | Pipeline A |

---

## Writing Roadmap

| Phase | Sections | Timeline | Status |
|-------|----------|----------|--------|
| 1 | Introduction (1.1-1.4) + Related Work (2.1-2.3) | Now | 📝 Start |
| 2 | Methodology (3.1-3.6) | This week | ⏳ |
| 3 | Results (4.1) — CognitiveSpace data available now | This week | ✅ Data ready |
| 4 | Results (4.2-4.3) — LDS requires DE/EN data | After data collection | ❌ Blocked |
| 5 | Discussion + Conclusion | After results | ⏳ |
| 6 | Figures + References | Throughout | ⏳ |
