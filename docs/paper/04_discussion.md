## 4. Discussion

### 4.1 Summary of Findings

This study introduced LinguaGraph, a knowledge graph-based framework for analyzing how mathematical knowledge is organized across languages (Chinese, German, English), education levels (elementary through university), and most recently, disciplines (mathematics versus physics). Seven findings emerged:

| # | Finding | Evidence |
|---|---------|----------|
| F1 | CDS peaks at Middle school (0.271), not Elementary | Non-monotonic density pattern |
| F2 | 3.7× density drop from Middle to High school | CDS 0.271 → 0.073; concept count 4.2× increase |
| F3 | HDS ≤ 7 (mean 0.40); 66% of concepts are roots | Mathematics is a shallow web, not a deep tree |
| F4 | ZH–DE structural divergence is highest (LDS=0.907) | ZH–EN lowest (0.802) |
| F5 | Cross-language divergence is topic-dependent | ~0.2 variation within language pairs across topics |
| F6 | Different disciplines exhibit different CDS patterns | Math peaks at Middle; Physics peaks at College |
| F7 | Physics has deeper prerequisite chains (HDS mean 1.17 vs 0.42) | Physics knowledge is more cumulative |

### 4.2 Interpretation of the CDS Peak

The finding that Concept Density Score peaks at Middle school (F1) rather than at Elementary or College warrants careful interpretation. A naive expectation might be that "more advanced knowledge is more densely connected." The data contradict this: the middle school mathematics curriculum acts as a **knowledge density hub**, where foundational arithmetic, introductory algebra, geometry, and probability concepts are tightly interconnected. This pattern is consistent with Ausubel's assimilation theory [12], which predicts that knowledge structures achieve maximum integration during periods of consolidation before branching into specialization.

The subsequent 3.7× drop from Middle to High school (F2) coincides with a 4.2× expansion in concept count, suggesting that the mathematics curriculum intentionally diversifies at this transition. This may reflect a pedagogical design principle: middle school provides an integrated foundation; high school introduces specialized subfields (calculus, vector geometry, statistics) that are taught in relative isolation before potential reintegration at the university level.

The robustness of this finding across three languages independently (ZH, EN, DE) suggests it is not an artifact of any particular textbook tradition. Rather, it may reflect a universal property of mathematics curriculum design — or at least a convergence across three distinct educational systems.

### 4.3 Cross-Linguistic Structural Divergence

The LDS results (F4) reveal that structural divergence between language pairs is substantial (0.802–0.907) even when the conceptual content is the same (mathematics). This is notable: mathematical truth is universal, yet its knowledge organization varies considerably across languages.

The finding that ZH–DE shows higher divergence (0.907) than ZH–EN (0.802) is counterintuitive. One might expect two European languages (DE–EN) to share more structural similarity than either shares with Chinese. The data suggest the opposite: Chinese and English textbook traditions share more structural features at the knowledge graph level than either shares with the German tradition. This may reflect the influence of the Anglo-American mathematics curriculum tradition (including IGCSE, AP, and IB frameworks) on Chinese textbook design, while the German *Gymnasium* tradition maintains a distinct structural approach.

This interpretation is consistent with Liang and Heckmann's (2013) finding that Chinese and German mathematics textbooks differ in problem complexity and representation style [8]. Our graph-based analysis extends their content-level comparison to the structural level, revealing differences that surface-level content analysis cannot capture.

### 4.4 Cross-Disciplinary Validation

The addition of Physics (F6, F7) validates that the CDS and HDS metrics capture genuine structural properties of knowledge organization, not just artifacts of the mathematics corpus. The contrasting patterns — Math peaks at Middle school, Physics peaks at College — demonstrate that **knowledge organization is discipline-dependent**.

This finding has implications for curriculum design. If mathematics and physics students experience fundamentally different knowledge density trajectories, then pedagogical strategies that work for one discipline may not transfer to the other. Mathematics education might emphasize integration early; physics education might accept that advanced-level integration is a natural part of the learning progression.

### 4.5 The Curriculum Layer

The ongoing integration of the Kernlehrplan (NRW mathematics curriculum standards) addresses the most significant limitation of the textbook-only analysis: the question of whether our findings reflect textbook author decisions or deeper curriculum-design principles. By comparing textbook graphs to curriculum graphs via Coverage Score, we will be able to distinguish:

- **Curriculum-driven structure**: patterns that originate in the official curriculum
- **Textbook-author-driven structure**: patterns introduced by textbook publishers
- **Universal structure**: patterns that persist across languages, curricula, and textbooks

### 4.6 Limitations

Several limitations should be acknowledged:

**Scope of data**. The mathematics corpus (68 textbooks, 574 concepts) is comprehensive, but the physics corpus (87 concepts) remains small for robust cross-disciplinary comparison. The curriculum graph (41 concepts) is still in prototype phase. Expanding these datasets is a priority.

**Extraction methodology**. Concept extraction currently combines LLM-based extraction with rule-based fallback. While this has produced consistent results, the reliance on a single extraction methodology means that measurement error in extraction propagates to downstream metrics. Gold-standard human annotation (in progress) will quantify this error.

**Causality**. Our analysis is correlational. We measure structural differences but cannot attribute them to language, educational system, or textbook tradition independently. These factors are confounded: Chinese textbooks are written for the Chinese education system in the Chinese language.

**Generalizability**. Mathematics may be a special case. Its highly structured, cumulative nature may produce knowledge organization patterns that do not generalize to less structured domains. The physics results provide initial support for generalizability, but more disciplines are needed.

**LDS formula**. The 3-component LDS (GED + node Jaccard + edge Jaccard) has the advantage of capturing multiple structural dimensions, but the statistical properties of the averaged score are not fully characterized. Edge Jaccard is sensitive to direction assignments, and GED similarity depends on graph size.

### 4.7 Implications

Despite these limitations, the current findings have implications for three communities:

**For educational research**: The CDS and HDS metrics provide quantitative tools for curriculum analysis that complement existing qualitative frameworks (TIMSS, PISA). A curriculum designer could use CDS to identify density bottlenecks and HDS to detect excessively long prerequisite chains.

**For AI in education**: The automated pipeline demonstrates that large-scale cross-lingual knowledge graph construction from textbooks is feasible using current LLMs. This opens the possibility of curriculum-level knowledge analysis at a scale that manual content analysis cannot achieve.

**For the study of linguistic relativity**: While our data do not directly address whether "language shapes thought," they demonstrate that language-specific knowledge organization patterns exist and can be quantified. This provides a methodological foundation for future work connecting textbook structure to cognitive structure.
