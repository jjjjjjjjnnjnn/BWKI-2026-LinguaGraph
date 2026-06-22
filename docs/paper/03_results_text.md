## 3. Results

### 3.1 Concept Density Structure (CDS)

We computed the Concept Density Score (CDS = 2|E|/(|V|·(|V|-1))) for each education level's subgraph. Figure 3 shows a clear non-monotonic pattern:

| Level | Concepts (|V|) | Edges (|E|) | CDS |
|-------|:----------:|:-------:|:---:|
| Elementary | 37 | 144 | **0.216** |
| Middle | 46 | 280 | **0.271** |
| High | 175 | 1113 | **0.073** |
| College | 298 | 1838 | **0.042** |

**Finding F1**: Knowledge density **peaks at Middle school**, then declines sharply. The transition from Middle (0.271) to High (0.073) represents a **3.7× drop** in concept density. This contradicts a simple "density decreases monotonically" narrative — instead, the middle school curriculum acts as a **density hub** where foundational concepts are tightly interconnected before branching into specialized domains.

**Finding F2**: College-level mathematics has the lowest density (0.042), despite having the most concepts (298). This reflects the modular, specialized nature of university mathematics — subfields like analysis, linear algebra, and topology operate largely independently.

### 3.2 Hierarchy Depth Structure (HDS)

We computed the longest prerequisite chain for each concept using BFS on prerequisite-type relations. Figure 5 shows the distribution:

| Metric | Value |
|--------|-------|
| Maximum chain depth | **8** |
| Mean depth | **0.40** |
| Concepts with no prerequisites (roots) | ~66% |

**Finding F3**: The maximum prerequisite depth is only 8, with a mean of 0.40. This means that **mathematical knowledge is predominantly a shallow web, not a deep tree**. Over 66% of concepts have no prerequisite chains at all.

### 3.3 Cross-Language Structural Divergence (LDS)

We computed LDS across three language pairs using the Wikipedia corpus for 5 social topics. Figure 4 shows the heatmap:

| Pair | Average LDS | Interpretation |
|------|:---------:|---------------|
| ZH–DE | **0.907** | Highest divergence |
| DE–EN | **0.901** | Near-maximum divergence |
| ZH–EN | **0.802** | Lowest divergence |

**Finding F4**: ZH–DE shows the highest structural divergence (LDS=0.907), while ZH–EN shows the lowest (0.802). This is counterintuitive — one might expect ZH to diverge more from both European languages. Instead, the data suggests that Chinese and English textbooks share more structural similarity at the concept-relation level than either shares with German textbooks.

**Finding F5**: Within the 5 topics analyzed, LDS varies by up to 0.2 within each language pair, suggesting that **cross-language structural divergence is topic-dependent**, not uniform across all knowledge domains.
