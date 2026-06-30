> ⚠️ OBSOLETE — Use 03_results.md instead
> 
> This file contains results from the old Wikipedia-based pipeline. The current
> pipeline produces different LDS values. See 03_results.md for accurate results.

## 3. Results

### 3.1 Concept Density Structure (CDS)

We computed the Concept Density Score (CDS = 2|E|/(|V|·(|V|-1))) for each education level's subgraph. Figure 3 shows a clear non-monotonic pattern:

| Level | Concepts (|V|) | Edges (|E|) | CDS |
|-------|:----------:|:-------:|:---:|
| Elementary | 37 | 144 | **0.216** |
| Middle | 46 | 280 | **0.271** |
| High | 193 | 1113 | **0.073** |
| College | 298 | 1838 | **0.042** |

**Finding F1**: Knowledge density **peaks at Middle school**, then declines sharply. The transition from Middle (0.271) to High (0.073) represents a **3.7× drop** in concept density. This contradicts a simple "density decreases monotonically" narrative — instead, the middle school curriculum acts as a **density hub** where foundational concepts are tightly interconnected before branching into specialized domains.

**Finding F2**: College-level mathematics has the lowest density (0.042), despite having the most concepts (298). This reflects the modular, specialized nature of university mathematics — subfields like analysis, linear algebra, and topology operate largely independently.

### 3.2 Hierarchy Depth Structure (HDS)

We computed the longest prerequisite chain for each concept using BFS on prerequisite-type relations. Figure 5 shows the distribution:

| Metric | Value |
|--------|-------|
| Maximum chain depth | **8** |
| Mean depth | **0.40** |
| Concepts with no prerequisites (roots) | ~83% |

**Finding F3**: The maximum prerequisite depth is only 8, with a mean of 0.40. This means that **mathematical knowledge is predominantly a shallow web, not a deep tree**. Over 83% of concepts have no prerequisite chains at all.

### 3.3 Cross-Language Structural Divergence (LDS) — Textbook Pipeline

> ⚠️ This section previously used Wikipedia corpus values. The current pipeline
> produces different textbook LDS-K values. The values below reflect the
> current pipeline results from 03_results.md §3.7.

We computed LDS-K across three language pairs using the textbook knowledge graph pipeline (556 concepts, 3 languages). Figure 4 shows the heatmap:

| Pair | LDS-K | Interpretation |
|------|:-----:|---------------|
| ZH–EN | **0.934** | Highest divergence |
| DE–EN | **0.938** | Near-maximum divergence |
| ZH–DE | **0.519** | Lowest divergence — Chinese and German math textbooks are structurally more similar

**Finding F4**: ZH-DE shows the lowest structural divergence (LDS-K=0.519), while DE-EN shows the highest (0.938). This is counterintuitive — German and Chinese textbooks are structurally more similar to each other than either is to English textbooks. Degree-preserving randomization (Structure Null) produces LDS-K values of 0.957 for all pairs, confirming that real textbook graphs are more similar than chance — textbook knowledge structures converge across languages.

**Finding F5**: Within the 5 topics analyzed, LDS varies by up to 0.2 within each language pair, suggesting that **cross-language structural divergence is topic-dependent**, not uniform across all knowledge domains.

### 3.4 Human Validation: Cognitive Graphs from Multilingual Respondents

To validate whether textbook-level structural divergence reflects genuine cognitive differences, we collected 101 open-ended responses from N=8 multilingual participants (4 ZH-native, 2 DE-native, 2 EN-native) across 5 social topics (Freedom, Justice, Success, Responsibility, Home) in all three languages. Extraction was performed with qwen-plus (validated F1=0.939 on 92 gold labels), achieving 89.1% extraction coverage.

**Within-subject LDS (DE-EN).** Three bilingual participants answered the same questions in both German and English, enabling direct within-subject comparison. Mean within-subject LDS was **0.773** (SD=0.10), confirming significant language-driven concept divergence at the individual level. Notably, for participant S002, the DE and EN concept sets for Freedom showed zero overlap (Node Jaccard=0.000), with the German response centered on "Glück" (happiness) while the English response referenced "freedom, choice, responsibility" — a qualitative difference invisible to surface-level content analysis.

**Between-subject LDS.** Aggregating responses by native language group produced the following cross-language comparison:

| Language Pair | Mean LDS | Interpretation |
|:-------------:|:-------:|---------------|
| DE–ZH | **0.751** | Highest divergence |
| DE–EN | 0.727 | Moderate divergence |
| ZH–EN | 0.704 | Lowest divergence |

**Cross-level consistency.** The rank order of divergence (DE–ZH > DE–EN > ZH–EN) is identical across human data and the textbook corpus, though the textbook pair rankings differ between the old Wikipedia corpus and the current pipeline:

| Pair | Textbook LDS-K | Human LDS (Between) | Difference |
|:----:|:--------------:|:------------------:|:---------:|
| DE–ZH | 0.519 | 0.751 | +0.232 |
| DE–EN | 0.938 | 0.727 | −0.211 |
| ZH–EN | 0.934 | 0.704 | −0.230 |

This comparison reveals a key insight: for DE-ZH, human cognitive divergence (LDS-C=0.751) is larger than textbook structural divergence (LDS-K=0.519), while for DE-EN and ZH-EN the pattern reverses. This supports the ΔLDS framework that isolates language-specific cognitive effects from textbook-level structural patterns.
