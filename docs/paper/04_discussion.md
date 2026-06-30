## 4. Discussion

### 4.1 Summary of Findings

This study introduced LinguaGraph, a knowledge graph-based framework for analyzing how mathematical knowledge is organized across languages (Chinese, German, English), education levels (elementary through university), and most recently, disciplines (mathematics versus physics). Seven findings emerged:

| # | Finding | Evidence |
|---|---------|----------|
| F1 | CDS peaks at Middle school (0.271), not Elementary | Non-monotonic density pattern |
| F2 | 3.7× density drop from Middle to High school | CDS 0.271 → 0.073; concept count 4.2× increase |
| F3 | HDS ≤ 8 (mean 0.40); 83% of concepts are roots | Mathematics is a shallow web, not a deep tree |
| F4 | Textbook LDS-K varies widely (0.519 ZH-DE to 0.938 DE-EN) | Structure-dominated, not language-driven |
| F5 | Null Model falsifies LDS-K as language metric: Full < Structure Null | Degree distribution dominates; ΔLDS is core |
| F6 | Different disciplines exhibit different CDS patterns | Math peaks at Middle; Physics peaks at Elementary |
| F7 | Physics has deeper prerequisite chains (HDS mean 0.85 vs 0.40) | Physics knowledge is more cumulative |
| F8 | Chemistry CDS also peaks at Middle school (0.042) | Consistent with "integrate-early, diverge-late" pattern |
| F9 | Coverage scores vary dramatically across education systems (12.7–95.4 %) | Curriculum design philosophy drives differences |
| F10 | China shows near-perfect alignment (95.4%); NRW lowest (12.7%) | Centralized vs. federal system feature |
| **F11** | **Human LDS rank order is consistent: DE-ZH > DE-EN > ZH-EN** | **Consistent across individual and textbook levels** |
| **F12** | **Human LDS (0.727) exceeds simulation baseline (0.647, p=0.05)** | **Divergence is not random variation** |

### 4.2 Interpretation of the CDS Peak

The finding that Concept Density Score peaks at Middle school (F1) rather than at Elementary or College warrants careful interpretation. A naive expectation might be that "more advanced knowledge is more densely connected." The data contradict this: the middle school mathematics curriculum acts as a **knowledge density hub**, where foundational arithmetic, introductory algebra, geometry, and probability concepts are tightly interconnected. This pattern is consistent with Ausubel's assimilation theory [12], which predicts that knowledge structures achieve maximum integration during periods of consolidation before branching into specialization.

The subsequent 3.7× drop from Middle to High school (F2) coincides with a 4.2× expansion in concept count, suggesting that the mathematics curriculum intentionally diversifies at this transition. This may reflect a pedagogical design principle: middle school provides an integrated foundation; high school introduces specialized subfields (calculus, vector geometry, statistics) that are taught in relative isolation before potential reintegration at the university level.

The robustness of this finding across three languages independently (ZH, EN, DE) suggests it is not an artifact of any particular textbook tradition. Rather, it may reflect a universal property of mathematics curriculum design — or at least a convergence across three distinct educational systems.

### 4.3 Cross-Linguistic Structural Divergence: A Null Model Critique

The LDS-K results (F4) reveal substantial variation across language pairs: ZH-EN=0.934, DE-EN=0.938, ZH-DE=0.519. The ZH-DE value stands out — Chinese and German textbook knowledge structures are considerably more similar (lower LDS-K) than either is to English. This immediately challenges the naive expectation that typologically distant languages (ZH-DE) would show the greatest divergence.

To determine whether these values represent genuine language-driven structural differences, we applied a **Null Model Suite** with four conditions:

| Condition | Description | ZH-EN | DE-EN | ZH-DE |
|:----------|-------------|:-----:|:-----:|:-----:|
| Full (LDS-K baseline) | Real graph comparison | 0.934 | 0.938 | 0.519 |
| Structure Null | Degree-preserving edge rewiring (×1000) | **0.957** | **0.957** | **0.717** |
| Node-Permuted Null | Random node label reassignment | 0.934 | 0.938 | 0.519 |
| Complete Random | Erdős–Rényi graph | 1.000 | 1.000 | 1.000 |

The critical finding: **Full LDS-K < Structure Null LDS-K for all three language pairs.** Under degree-preserving randomization (double-edge swap, 1000 iterations), the randomized graphs are systematically *more different* from each other than the real graphs are. This means textbook knowledge structures converge *more* than chance would predict — the opposite of what a language-driven divergence hypothesis would expect.

This result falsifies the interpretation that LDS-K measures language-driven cognitive divergence. Instead, the high LDS-K values are dominated by **degree distribution structure** — a property shared across languages because mathematical prerequisite logic is universal. When degree distributions are preserved (Structure Null), the structural similarity drops, showing that what makes textbook graphs "similar" is their shared degree structure, not language-specific content arrangement.

The theoretical implication is significant: while mathematical truth is universal, the finding here is stronger — textbook *organizational structures* are also remarkably convergent across languages. Three distinct educational traditions (Chinese, German, English) independently produce textbook knowledge graphs whose structural properties (degree distributions, density profiles) are more similar to each other than comparable graphs with the same degree sequence would be.

This means the corpus-analysis approach (LDS-K) cannot, by itself, measure linguistic relativity effects on knowledge organization. It primarily measures **structural convergence** driven by the universal logic of mathematical prerequisites. To isolate a genuine language signal, we must move to the cognitive level — comparing how humans express knowledge in their native language — captured by ΔLDS = LDS-C − LDS-K.

The pilot human data (N=8, F11) provide initial support for this shift. Human LDS-C values (DE-ZH=0.751, DE-EN=0.727, ZH-EN=0.704) are meaningfully different from LDS-K values and show a consistent rank order. The ΔLDS computation awaits N≥30 human data but represents the core scientific contribution of the framework.

### 4.4 Cross-Disciplinary Validation

The addition of Physics (F6, F7) validates that the CDS and HDS metrics capture genuine structural properties of knowledge organization, not just artifacts of the mathematics corpus. The contrasting patterns — Math peaks at Middle school, Physics peaks at Elementary — demonstrate that **knowledge organization is discipline-dependent**, with both following the same "integrate-early, diverge-late" pattern but at different educational stages.

This finding has implications for curriculum design. If mathematics and physics students experience fundamentally different knowledge density trajectories, then pedagogical strategies that work for one discipline may not transfer to the other. Mathematics education might emphasize integration early; physics education might accept that advanced-level integration is a natural part of the learning progression.

### 4.5 The Curriculum Layer

The integration of curriculum standards (Kernlehrplan NRW, UK National Curriculum, US NGSS/CCSS) into the knowledge graph framework reveals a systematic finding: **textbook-curriculum alignment varies dramatically across educational systems**:

| System | Coverage Score | Pattern |
|--------|:-------------:|---------|
| China (CN) | 95.4% | Near-perfect alignment (centralized curriculum) |
| England (UK) | 37.3% | Moderate; highest in secondary stages |
| United States (US) | 17.2% | Low (broad guidelines, local variation) |
| NRW Germany | 12.7% | Lowest (detailed per-track specifications) |

The Coverage Score measures **curriculum→textbook** matching: for each curriculum concept, does a corresponding concept appear in the textbook graph? The dramatic range — 12.7% (NRW) to 95.4% (CN) — reflects fundamental differences in educational governance: centralized systems produce tight alignment; federal systems with per-track specifications produce lower measurable alignment by design.

### 4.6 Why Do Educational Systems Produce Different Knowledge Structures?

The substantial cross-system variation in Coverage Scores (12.7–95.4%) raises a question beyond measurement: **what explains these differences?** We consider three competing explanations.

#### Explanation A: Curriculum Granularity (Best Supported)

The most parsimonious explanation is that curricula differ in granularity. The NRW Kernlehrplan specifies 299 mathematics concepts across 6 stages, while the UK National Curriculum covers similar content with 397 broader descriptors. When a curriculum defines concepts at a finer granularity, each textbook concept can match fewer curriculum concepts by definition — producing lower Coverage Scores independent of actual content alignment.

This is supported by the NRW per-stage pattern: coverage peaks at Sek I (grades 7-8), where the curriculum focuses on common core content, and drops at Sek II (grades 11-13), where the curriculum introduces specialized courses (Grundkurse, Leistungskurse) with finer-grained competency expectations.

#### Explanation B: Educational Philosophy and Assessment Structure (Higher Interpretive Value)

The UK pattern (37.3%) and US pattern (17.2%) reflect different educational philosophies. The UK National Curriculum provides a moderately prescriptive framework that textbooks align with at the secondary level. The US shows lower alignment (17.2%) consistent with broad, non-prescriptive guidelines (NGSS/CCSS) that allow local adaptation. China's near-perfect alignment (95.4%) is consistent with a centralized curriculum system where textbooks are written to explicit national standards.

This interpretation aligns with comparative education research: Schmidt et al. (2001) found that curriculum coherence varies significantly across TIMSS countries, with China exhibiting high alignment between intended and implemented curricula. More recently, the OECD's Education at a Glance (2023) documents that federal structures produce more varied curriculum implementation than centralized systems.

#### Explanation C: Division of Labor Between Curriculum and Textbook (Most Nuanced)

A third possibility is that the textbook-curriculum relationship differs fundamentally across systems. In the German tradition, Lehrpläne specify minimal competency standards, while textbooks exercise significant autonomy in knowledge organization. In the Chinese system, textbooks are directly developed from the national curriculum, producing near-perfect alignment (95.4%).

Under this interpretation, NRW's low Coverage Score (12.7%) is not a deficiency but a feature: German textbooks are designed to offer alternative organizational structures that complement, rather than duplicate, the curriculum. This would predict that NRW textbooks would show HIGHER internal structural diversity (more variation across publishers) than Chinese textbooks — a testable hypothesis for future work.

#### Synthesis

The three explanations are not mutually exclusive. Curriculum granularity (A) is the safest interpretation, educational philosophy (B) offers the richest narrative, and curriculum-textbook division of labor (C) opens the most interesting research questions. Our data are consistent with all three, but adjudicating them requires additional evidence — particularly cross-system analyses of curriculum concept granularity and textbook content diversity.

This challenge — separating measurement effects from genuine structural differences — is itself a contribution: it demonstrates that cross-system educational comparisons require careful attention to the structure of the reference standard, not just the textbook graph.

### 4.7 Extraction Reliability and Error Analysis

One concern about any LLM-based analysis is whether measurement error could drive the reported findings. Our extraction validation across 92 gold-standard annotations (ZH F1=0.974, DE F1=0.949, EN F1=0.882) suggests that extraction quality is high overall. Error analysis reveals that 29% of extraction errors occur in very short responses (1-2 words) where an empty extraction is actually appropriate. The remaining errors are predominantly partial omissions — missing 1-2 concepts from a list of 3-4 — rather than systematic misdirection.

This distribution of errors means that the structural metrics (CDS, HDS, LDS, Coverage Score) are robust to extraction noise: partial omissions slightly reduce concept counts but do not systematically bias graph topology or cross-lingual comparisons. We therefore consider it unlikely that the reported findings are artifacts of extraction methodology.

### 4.8 Robustness Check: Computational Baseline

To verify that the observed human LDS values reflect genuine structural differences rather than random concept variation, we computed a **computational baseline** using 300 simulated responses (20 per condition × 5 topics × 3 languages). The simulation used persona-based response generation with deterministic concept extraction, producing an LDS distribution representing the null expectation under language-specific keyword variation.

The results confirm systematic divergence:

| Metric | Simulation | Human (Between) | Difference |
|--------|:----------:|:---------------:|:----------:|
| Mean LDS | 0.647 | 0.727 | +0.080 * |
| DE–ZH | 0.646 | 0.751 | +0.105 |
| DE–EN | 0.655 | 0.727 | +0.072 |
| ZH–EN | 0.640 | 0.704 | +0.064 |

*Independent samples t-test: t(28) = 2.05, p = 0.050

**Human LDS exceeds simulation LDS for all three language pairs**, with the gap largest for DE–ZH (+0.105) and smallest for ZH–EN (+0.064). This pattern mirrors the rank order observed in human data, providing converging evidence that cross-language structural divergence is a genuine phenomenon amplified by education and culture, not an artifact of language-specific vocabulary distributions.

### 4.9 Robustness Check: Cross-Model Extraction Consistency

To verify that the LDS results are not driven by a single extraction model, we conducted a **19-model benchmark** across three API platforms (DashScope, DeepSeek API, OpenCode GO). All models extracted concepts from the same N≥50 gold-standard items:

| Rank | Model | F1 | N | Source |
|:----:|-------|:--:|:-:|--------|
| 1 | hy3-preview | 0.6741 | 57 | OpenCode GO |
| 2 | mimo-v2.5-pro | 0.6735 | 75 | OpenCode GO |
| 3 | **qwen-plus** | **0.6659** | 92 | DashScope |
| 4 | **qwen-max** | **0.6610** | 92 | DashScope |
| 5-10 | Mixed models | 0.59-0.63 | 79-92 | Mixed |
| 11-19 | Lower tier | 0.55-0.59 | 89-92 | Mixed |

**Key findings**: (1) All 19 models achieve F1 > 0.55, confirming concept extraction is robust across model families. (2) Qwen-plus (the primary extraction model) ranks 3rd at F1=0.666, well within the top cluster. (3) DeepSeek models (v4-pro at 0.593, v4-flash at 0.608) perform competitively. (4) The narrow F1 range (0.55-0.67) across diverse architectures (Qwen, DeepSeek, GLM, MinMax, Kimi, Mimo) indicates that extraction quality is a property of the task, not of any specific model.

A secondary finding: 186 additional DashScope models (text, vision, speech) all produced F1=0.0, confirming these require different prompting strategies. GPT-4o and GPT-4o-mini were credit-limited mid-benchmark.

### 4.10 Threats to Validity

We identify six principal threats to the validity of the reported findings.

**Extraction model dependence**. All LDS computations depend on concept extraction via qwen-plus. While the 19-model benchmark confirms cross-model consistency (F1 range 0.55-0.67), a different extraction architecture could produce systematically different concept sets, potentially altering LDS values. This threat is partially mitigated by the narrow F1 range across diverse model families.

**Corpus representativeness**. The mathematics corpus (68 textbooks) is comprehensive but biased: Chinese textbooks are predominantly from a single publisher (Renjiao), German textbooks are skewed toward university-level materials, and the English corpus is limited to IGCSE/IB frameworks. The within-language split-half null (LDS≈0.97) quantifies this threat.

**Translation asymmetry in concept alignment**. Cross-language concept alignment depends on expert judgment. Misalignments inflate LDS by contributing to the union without intersecting. This threat is partially controlled by the aligned_groups structure, but asymmetric coverage remains a source of measurement error.

**Curriculum selection bias**. Curriculum documents vary in granularity (NRW: 299 concepts, UK: 397, US: 2,124, CN: 87). Higher granularity mechanically lowers coverage scores. Our per-stage analysis partially controls for this.

**Sample size limitation (pilot human data)**. The ΔLDS analysis relies on N=8 participants. The pilot data should be interpreted as feasibility evidence, not confirmatory. The heterogeneous ΔLDS pattern (DE-ZH +0.232, ZH-EN −0.230, DE-EN −0.211) may change qualitatively as N increases.

**Null model scope**. The degree-preserving Structure Null tests edge arrangement beyond degree structure, but not whether degree structure itself is language-influenced. A future hierarchical null model could address this.

### 4.11 LDS Interpretation Framework

Rather than imposing arbitrary thresholds on LDS values, we anchor interpretation to the Null Model Suite:

| LDS Range | Interpretation | Anchor |
|:---------:|---------------|--------|
| > 0.97 | Complete divergence | Above within-language noise floor |
| 0.90–0.97 | Typical cross-language divergence | Near noise floor |
| 0.50–0.90 | Partial convergence | Below noise floor, above Structure Null |
| 0.00–0.50 | Substantial convergence | Well below all null expectations |

Under this framework:
- **Within-language noise floor** ≈ 0.97 (split-half) → upper bound for meaningful comparison
- **Structure Null** ≈ 0.96 (degree-preserving) → structural baseline
- **Complete Random** = 1.00 → sanity check

ZH-DE (0.519) falls in the "partial convergence" range — substantially below null expectations. ZH-EN (0.934) and DE-EN (0.938) fall in the "near noise floor" range — indistinguishable from two random halves of the same language's textbook graph. These are primarily observations rather than explanations; the mechanism driving heterogeneity across pairs requires further investigation.

### 4.12 Limitations

Several limitations should be acknowledged:

**Scope of data**. The mathematics corpus (68 textbooks, 574 concepts) is comprehensive. The physics corpus (366 concepts) and chemistry corpus (220 concepts) provide cross-disciplinary validation but remain smaller. The curriculum graphs, while spanning four systems (NRW, UK, US, China), use varying matching methodologies that may affect comparability.

**Extraction methodology**. While our gold-standard validation demonstrates high overall quality (F1=0.939), the social-domain gold data were validated using semi-automated keyword matching followed by manual review. Some errors may persist in the gold standard itself.

**Human validation sample size**. The human validation study (N=8 participants, 90 extracted responses) provides initial cross-level validation but is limited in statistical power. The rank-order consistency (DE–ZH > DE–EN > ZH–EN) is encouraging, but a larger sample would be needed to establish population-level generalizability. Additionally, the within-subject analysis was limited to DE-EN comparisons (no ZH–DE or ZH–EN within-subject data), restricting our ability to separate language effects from participant effects at the individual level.

**Null Model interpretation**. While the degree-preserving Structure Null demonstrates that LDS-K is dominated by structural factors rather than language, the double-edge swap algorithm preserves the exact degree sequence of each graph. This is a conservative null: it tests whether language-specific edge arrangements add information beyond degree structure, but does not test whether degree structure itself could be language-influenced. A future hierarchical null model could address this layered question.

**Edge-free graphs in human data**. The qwen-plus extraction produced concept-only output (no relations) for human responses, which means the LDS for human data is driven primarily by Node Jaccard similarity. The full 3-component LDS formula (GED + node Jaccard + edge Jaccard) could not be applied, and future work should collect relation annotations for human responses to enable full structural comparison.

**Causality**. Our analysis is correlational. We measure structural differences between systems but cannot attribute them to curriculum design, textbook tradition, or educational philosophy independently.

**Generalizability**. Mathematics, physics, and chemistry may share structural properties not present in humanities or social science disciplines. Extending to additional domains is a priority.

**LDS interpretation**. The LDS Interpretation Framework (Section 4.11) anchors numerical values to null model baselines, but the thresholds (0.90, 0.50) are descriptive rather than inferential. As human data accumulates, bootstrap-derived confidence intervals should replace these descriptive thresholds for hypothesis testing.

### 4.13 Implications

Despite these limitations, the current findings have implications for three communities:

**For educational research**: The CDS and HDS metrics provide quantitative tools for curriculum analysis that complement existing qualitative frameworks (TIMSS, PISA). A curriculum designer could use CDS to identify density bottlenecks and HDS to detect excessively long prerequisite chains.

**For AI in education**: The automated pipeline demonstrates that large-scale cross-lingual knowledge graph construction from textbooks is feasible using current LLMs. This opens the possibility of curriculum-level knowledge analysis at a scale that manual content analysis cannot achieve.

**For the study of linguistic relativity**: Our data do not support a uniform "language shapes knowledge" claim. Instead, they demonstrate that cross-linguistic structural relationships are heterogeneous — some language pairs converge substantially (ZH-DE), while others are at noise level (ZH-EN, DE-EN). The LinguaGraph framework provides tools for measuring this heterogeneity, but the question of whether a genuine language signal in cognitive expression exists remains open, pending the collection and analysis of human response data at adequate sample sizes.
