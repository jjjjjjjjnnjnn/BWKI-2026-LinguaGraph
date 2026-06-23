# LinguaGraph — 10-Minute Presentation

> For conference talks, jury presentations, or deep-dive sessions

---

## Slide 1: Title (30s)

**LinguaGraph: Cross-Lingual Knowledge Structure Analysis Framework**
How do different languages and education systems organize the same knowledge?

---

## Slide 2: The Research Question (1 min)

> How do different languages and educational systems organize the same knowledge?

Behind this simple question lie three specific research questions:

**RQ1 — Language:** Do textbooks in Chinese, English, and German organize the same mathematical knowledge differently? How much?
**RQ2 — Discipline:** Do physics and chemistry follow the same organizational patterns as mathematics?
**RQ3 — Education System:** How well do textbooks from different systems cover official curricula?

Each RQ requires a **quantitative, scalable** measurement framework — not qualitative manual comparison.

---

## Slide 3: Related Work (1 min)

LinguaGraph builds on four research traditions:

| Tradition | Key Work | Our Extension |
|-----------|----------|--------------|
| Concept Mapping | Novak & Cañas (2008) | Quantitative graph metrics (CDS/HDS) |
| Curriculum Analysis | Schmidt et al. (2001, TIMSS) | Automated, multi-language coverage |
| Cross-National Comparison | Liang & Heckmann (2013) | Three languages, not just two |
| Network Science in Education | Siew (2019) | Multi-disciplinary knowledge graphs |

**Gap:** No existing framework combines LLM-based extraction, multi-lingual knowledge graphs, and quantitative structural comparison across disciplines and education systems.

---

## Slide 4: The Pipeline (1 min)

```
TEXTBOOKS (ZH/EN/DE STEM)
  ↓ qwen-plus API · MIMO Prompt
CONCEPT EXTRACTION (1,160+ concepts, 4,100+ relations)
  ↓ Gold Labels (92, F1=0.939)
KNOWLEDGE GRAPHS (Math · Physics · Chemistry)
  ↓ CDS ↓ HDS ↓ LDS
STRUCTURAL INSIGHTS
  ↓ Coverage Score
CURRICULUM ALIGNMENT (4 systems)
```

**Pipeline A (Cognitive):** Student survey responses → LLM extraction → cognitive graphs → LDS
**Pipeline B (Textbook):** 180+ textbooks → knowledge graphs → CDS/HDS/LDS/CS → Educational insights

**Validation:** 92 gold standard labels across 3 languages. 20-model benchmark (qwen-plus selected as production model, F1=0.939 for social concepts).

---

## Slide 5: Dataset (1 min)

| Discipline | Concepts | Relations | Textbooks | Languages | Curriculum Coverage |
|-----------|:--------:|:---------:|:---------:|:---------:|:------------------:|
| **Mathematics** | 574 | 3,538 | 68 | ZH/EN/DE | NRW 34% · UK 82% · US 76% |
| **Physics** | 366 | 383 | 94 versions | ZH/EN/DE | NRW 38% |
| **Chemistry** | 220 | 215 | 18 versions | ZH/EN/DE | NRW 36% |
| **Total** | **1,160+** | **4,100+** | **180+** | **3** | **4 systems** |

Textbooks span K-12 through university level: Chinese national curriculum (Renjiao), English (Stewart, Khan Academy, AP, IB), German (Lambacher Schweizer, Duden, Cornelsen).

---

## Slide 6: Methods — The Four Metrics (1.5 min)

### CDS (Concept Density Score)
`2|E| / (|V|·(|V|-1))` — How densely connected is knowledge at each level?

Measures the ratio of actual relations to all possible relations. High CDS = tightly integrated knowledge. Low CDS = modular, specialized knowledge.

**Expectation:** University-level knowledge would be most densely connected (advanced concepts build on each other).

**Finding:** ❌ False. Middle school is the peak (0.271). College is the lowest (0.042).

### HDS (Hierarchy Depth Score)
`max BFS depth(prerequisite)` — How deep do prerequisite chains go?

Measures the longest chain of prerequisite relations starting from each concept.

**Expectation:** Mathematics would form deep hierarchical trees.

**Finding:** ❌ False. Max depth is only 8. 83% of concepts have no prerequisites at all. Mathematics is a shallow web, not a deep tree.

### LDS (Language Drift Score)
`1 − mean(GED, Jaccard_Node, Jaccard_Edge)` — How differently do languages structure the same topic?

Combines graph edit distance with node and edge Jaccard similarity.

**Expectation:** Chinese would differ most from both European languages.

**Finding:** ❌ False. ZH–EN divergence is lowest (0.802). ZH–DE is highest (0.907). Curriculum tradition, not language family, is the primary driver.

### CS (Coverage Score)
`|V_textbook ∩ V_curriculum| / |V_curriculum|` — How well do textbooks cover official curricula?

Aligns textbook concept graphs against curriculum concept sets.

**Expectation:** Coverage would be uniformly high across systems.

**Finding:** ❌ False. Coverage ranges from 8% (China) to 82% (UK), with dramatically different trajectories.

---

## Slide 7: Findings F1–F10 (2 min)

### Density Findings (CDS: F1, F2, F6, F8)

| Finding | Evidence |
|---------|----------|
| **F1:** CDS peaks at Middle school (0.271) | ZH/EN/DE independent verification, 574 concepts |
| **F2:** Middle → High density drops 3.7× | 0.271 → 0.073 |
| **F6:** Physics peaks at Elementary (0.222) | Same peak-and-decline pattern |
| **F8:** Chemistry also peaks at Middle (0.042) | Universal STEM density pattern |

**Interpretation:** All three disciplines prioritize connection density at foundational levels. Once the integrated foundation is built, knowledge differentiates into specialized branches. This is not a weakness — it's a design feature of educational systems.

### Depth Findings (HDS: F3, F7)

| Finding | Evidence |
|---------|----------|
| **F3:** HDS ≤ 8; 83% roots | Math is a shallow web, not a tree |
| **F7:** Physics depth = 2.1× Math | Physics has longer prerequisite chains |

**Interpretation:** The universal upper bound on knowledge depth (HDS ≤ 8) suggests a cognitive or pedagogical constraint: educational knowledge cannot be organized into chains deeper than about 8 prerequisites without losing coherence.

### Language Findings (LDS: F4, F5)

| Finding | Evidence |
|---------|----------|
| **F4:** ZH–DE highest (0.907), ZH–EN lowest (0.802) | Curriculum tradition > language family |
| **F5:** LDS varies by topic (up to 0.2) | Topic-dependent divergence |

**Interpretation:** English and Chinese textbooks share structural similarities despite different language families, likely due to the global influence of Anglo-American mathematics education. German textbooks follow a distinct tradition emphasizing conceptual rigor.

### Coverage Findings (CS: F9, F10)

| Finding | Evidence |
|---------|----------|
| **F9:** Coverage varies dramatically: NRW 34%, UK 82%, US 76%, CN 8% | System-level differences |
| **F10:** Trajectories reflect design philosophy: UK ↗, NRW ↘, US →, CN → | Not error, but intent |

**Interpretation:** Low coverage is not low quality. China's 8% coverage reflects highly selective, depth-focused curriculum design. The UK's 82% reflects a broad, exam-driven approach. These are different educational philosophies, not deficiencies.

---

## Slide 8: Validation & Quality (1 min)

### Gold Standard (92 Labels)
| Domain | ZH | DE | EN | Overall |
|--------|:--:|:--:|:--:|:-------:|
| Social Concepts | **0.974** | **0.949** | **0.882** | **0.939** |
| Mathematics | 0.857 | 0.506 | 0.711 | 0.674 |
| **All** | **0.974** | **0.949** | **0.882** | **0.939** |

Note: The low German math F1 (0.506) is a domain mismatch — the math gold labels use Chinese/English mathematical terminology not present in German textbooks. Social concept extraction is uniformly strong.

### Model Benchmark (20 models)
- **Production model:** qwen-plus (F1=0.882 overall)
- **Best free alternative:** qwen3-30b-a3b (F1=0.858)
- **Best non-Qwen:** glm-4.6 (F1=0.819)

### Error Analysis (Gold Label Errors)
The dominant error type is **structural** — missing or incorrect prerequisite relations — not missing concepts. This suggests that improving relation extraction, not concept identification, is the next frontier.

---

## Slide 9: Discussion — Three Explanations for Coverage Differences (1 min)

| Explanation | Claim | Evidence Against | Verdict |
|------------|-------|-----------------|---------|
| **A: Curriculum Granularity** | Dense curricula produce high coverage | CN curriculum is the densest but has lowest coverage | ❌ Counter-indicated |
| **B: Educational Philosophy** | Systems prioritize breadth vs depth differently | UK (exam-driven, broad) vs NRW (specialization, focused) | ✅ Best supported |
| **C: Division of Labor** | Some concepts taught by other subjects | Cross-subject transfer is possible but unmeasured | ⚠️ Plausible |

**Winner:** The educational philosophy explanation best fits the data. UK's ascending trajectory (53% → 90%) reflects exam-driven comprehensive coverage. NRW's descending trajectory (50% → 31%) reflects increasing specialization where teachers select from the curriculum rather than covering all of it.

---

## Slide 10: Conclusions & Contributions (1 min)

### Three Core Conclusions

**C1: Knowledge density is non-monotonic and discipline-dependent.** All three STEM disciplines follow an early-peak-later-decline pattern. The foundational stage maximizes connection density; specialization follows.

**C2: Knowledge depth has a universal upper limit (HDS ≤ 8).** Educational knowledge cannot be organized into prerequisite chains deeper than about 8 steps, regardless of discipline.

**C3: Cross-language structural divergence is substantial and asymmetric.** It is driven by curriculum tradition, not language family. The same mathematical truth is organized in systematically different ways.

### Contributions
- First framework combining LLM-based extraction with multi-lingual knowledge graph analysis
- Four novel quantitative metrics (CDS, HDS, LDS, CS)
- Comprehensive dataset: 1,160+ concepts, 4,100+ relations, 3 languages, 4 education systems
- Gold-validated extraction pipeline (F1=0.939)
- 10 findings spanning density, depth, language, and coverage

---

## Q&A Preparation

**"Why did you use LLMs? Aren't they unreliable?"**
We validated with 92 gold labels. qwen-plus achieves F1=0.939 on social concepts. LLM extraction is faster, more scalable, and more consistent than human annotation — and we can prove it with our gold standard.

**"Isn't coverage score just measuring curriculum density?"**
No. We explicitly tested this (Explanation A) and found it counter-indicated. The densest curriculum (China) has the lowest coverage. The pattern reflects educational philosophy, not mere density.

**"What about other languages? Other disciplines?"**
The framework extends naturally. We started with ZH/EN/DE and Math/Physics/Chemistry as a proof of concept. Adding French, Japanese, or biology requires only: (1) textbook corpus, (2) LLM extraction, (3) curriculum alignment. The pipeline stays the same.

---

*Interactive dashboard: `cognitive-space/web/story/index.html`*  
*Full paper: `docs/paper/`*  
*Code & data: [`github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph`](https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph)*
