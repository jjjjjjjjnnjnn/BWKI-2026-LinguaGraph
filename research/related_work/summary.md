# LinguaGraph Related Work — Gap Analysis & Positioning

## Summary Statistics

| Area | Repos | Papers | Total |
|------|-------|--------|-------|
| ConceptNet / Concept Graphs | 5 | 5 | 10 |
| WordNet / Lexical Networks | 5 | 4 | 9 |
| BabelNet / Multilingual KG | 4 | 5 | 9 |
| Cross-lingual Embeddings | 5 | 5 | 10 |
| KG Visualization | 8 | 3 | 11 |
| Human Annotation Agreement | 5 | 5 | 10 |
| Linguistic Relativity | 4 | 7 | 11 |
| Additional | 4 | 5 | 9 |
| Future Directions (Phase 2-3) | 3 | 0 | 3 |
| **Total** | **43** | **39** | **82** |

---

## Q1: What is LinguaGraph's TRUE innovation?

### Unique contributions that exist NOWHERE ELSE:

1. **LDS (Language Drift Score) as a graph-structure metric**
   - No existing work computes cross-lingual cognitive difference at the graph-structure level
   - ConceptNet/BabelNet measure semantic similarity; RISE measures geometric distance; LDS measures **structural organization difference**
   - This is genuinely novel

2. **Cognitive City visualization metaphor**
   - 3d-force-graph is generic; no one has applied the city metaphor to cognitive graphs
   - Combines force-directed layout + semantic meaning (buildings = concepts, roads = relations)
   - No comparable visualization in the literature

3. **LLM-as-extraction + graph-comparison pipeline**
   - CoCo-Ex maps text → ConceptNet; CauseNet builds causality graphs
   - But NO ONE uses LLMs to extract cognitive graphs from individual human responses and then compares them across languages
   - This is a novel methodology

4. **Individual-level cross-lingual cognitive comparison**
   - Existing work (ConceptNet, BabelNet, CCKG) operates at the population/language level
   - LinguaGraph operates at the individual level (each person has their own graph)
   - Enables fine-grained analysis that population-level work cannot

---

## Q2: What is LinguaGraph MISSING compared to existing work?

### Critical gaps:

| Gap | Severity | Existing Alternative | How to Address |
|-----|----------|---------------------|----------------|
| **No human annotation data yet** (5% complete) | 🔴 CRITICAL | ConceptNet has 21M crowdsourced edges | Complete human experiment ASAP |
| **No inter-annotator agreement** | 🔴 CRITICAL | Standard practice: Cohen's Kappa ≥ 0.67 | Run annotation study, report kappa |
| **No established evaluation benchmark** | 🟡 MEDIUM | ConceptNet evaluated on MEN, RW, SimLex | Create LinguaGraph benchmark dataset |
| **Single LLM provider** (GPT-4.1-mini) | 🟡 MEDIUM | Multi-method approaches common | Already supports Ollama; add comparison |
| **Limited language coverage** (3 languages) | 🟡 LOW | BabelNet: 150+ languages | Appropriate for BWKI scope |
| **No reproducible baselines** | 🟡 MEDIUM | Published baselines expected | Already have 300 computational baselines |

### Specific missing methodological elements:

1. **Formal evaluation framework**: ConceptNet uses word similarity benchmarks. LinguaGraph needs equivalent benchmarks for graph-level cognitive comparison.

2. **Statistical significance testing**: Need to show LDS differences are statistically significant, not just numerical.

3. **Ablation study**: Which component of LDS matters most? (GED vs Jaccard_node vs Jaccard_edge)

4. **Error analysis**: When does LLM extraction fail? What are systematic biases?

---

## Q3: Where does LinguaGraph STRONG compared to existing work?

### Advantages:

1. **Methodological novelty**: Graph-level cross-lingual comparison is a new approach. Existing work uses embeddings, similarity scores, or annotation. LinguaGraph uses graph structure.

2. **Visualization**: Cognitive City is more intuitive than force-directed layouts or heatmaps. Judges can immediately "see" cognitive differences.

3. **Accessibility**: 3D visualization makes abstract linguistic relativity tangible. No prior work has made cross-lingual cognitive differences visually intuitive.

4. **Interdisciplinary**: Combines NLP (LLM extraction) + graph theory (NetworkX) + visualization (Three.js) + cognitive science (Sapir-Whorf). Most existing work stays in one field.

5. **BWKI fit**: The project demonstrates AI application to a humanistic question (does language shape thought?). This aligns with BWKI's goal of showing AI's societal impact.

6. **Reproducibility**: Open-source pipeline with clear documentation. Most cognitive science studies are not reproducible.

---

## Recommended Related Work for Paper

### Must-cite (5 core references):

1. **ConceptNet5** (Havasi et al., 2017) — foundational commonsense KG
2. **BabelNet** (Navigli & Ponzetto, 2012) — multilingual semantic network
3. **Conceptualizer** (Liu et al., ACL 2023) — cross-lingual concept alignment
4. **CCKG** (EACL 2026) — cultural commonsense KG
5. **Separating Tongue from Thought** (ACL 2025) — computational Sapir-Whorf

### Should-cite (3 methodological references):

6. **Cohen's Kappa** (Cohen, 1960) — annotation agreement
7. **Krippendorff's Alpha** (Krippendorff, 2004) — content analysis reliability
8. **NetworkX graph_edit_distance** — algorithmic foundation

### Nice-to-cite (2 context references):

9. **Slobin (1996)** — "Thinking for Speaking" theoretical framework
10. **Boroditsky (2001)** — empirical evidence for linguistic relativity

---

## Positioning Statement (for Related Work section)

> LinguaGraph builds on three research traditions: (1) commonsense knowledge graphs (ConceptNet, BabelNet) that represent human knowledge as concept-relation graphs; (2) cross-lingual semantics (Conceptualizer, MUSE) that align concepts across languages; and (3) computational linguistic relativity (Boroditsky, Slobin) that tests whether language shapes cognition. 
>
> Unlike knowledge graphs, LinguaGraph extracts **individual cognitive graphs** from human responses rather than building population-level KBs. Unlike cross-lingual embeddings, LinguaGraph compares **graph structure** rather than vector similarity. Unlike experimental linguistic relativity studies, LinguaGraph provides a **quantitative, scalable, and visually intuitive** framework for measuring cognitive differences.
>
> The three novel contributions are: (1) LDS — the first graph-structure metric for cross-lingual cognitive comparison; (2) Cognitive City — a 3D visualization metaphor that makes abstract cognitive differences tangible; and (3) an end-to-end LLM-to-graph-to-comparison pipeline that scales to any language pair.

---

## Priority Actions for Related Work Chapter

1. ✅ **This database** — done
2. ⬜ **Write Related Work section** using the positioning statement above
3. ⬜ **Add missing citations** to methodology.md and README.md
4. ⬜ **Create evaluation benchmark** (LinguaGraph needs its own evaluation dataset)
5. ⬜ **Run annotation study** and report Cohen's Kappa / Krippendorff's Alpha
