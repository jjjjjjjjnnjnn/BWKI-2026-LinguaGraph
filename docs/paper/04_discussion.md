## 4. Discussion

### 4.1 Summary of Findings

This study introduced LinguaGraph, a knowledge graph-based framework for analyzing how mathematical knowledge is organized across languages (Chinese, German, English), education levels (elementary through university), and most recently, disciplines (mathematics versus physics). Seven findings emerged:

| # | Finding | Evidence |
|---|---------|----------|
| F1 | CDS peaks at Middle school (0.271), not Elementary | Non-monotonic density pattern |
| F2 | 3.7× density drop from Middle to High school | CDS 0.271 → 0.073; concept count 4.2× increase |
| F3 | HDS ≤ 8 (mean 0.40); 83% of concepts are roots | Mathematics is a shallow web, not a deep tree |
| F4 | ZH–DE structural divergence is highest (LDS=0.907) | ZH–EN lowest (0.802) |
| F5 | Cross-language divergence is topic-dependent | ~0.2 variation within language pairs across topics |
| F6 | Different disciplines exhibit different CDS patterns | Math peaks at Middle; Physics peaks at Elementary |
| F7 | Physics has deeper prerequisite chains (HDS mean 0.85 vs 0.40) | Physics knowledge is more cumulative |
| F8 | Chemistry CDS also peaks at Middle school (0.042) | Consistent with "integrate-early, diverge-late" pattern |
| F9 | Coverage scores vary dramatically across education systems (8–82 %) | Curriculum design philosophy drives differences |
| F10 | NRW shows consistent coverage across 3 STEM disciplines (34–38 %) | System-level feature, not discipline-specific |
| **F11** | **Human LDS rank order matches Wikipedia corpus** | **Consistent across individual, corpus, and curriculum levels** |
| **F12** | **Human LDS (0.727) exceeds simulation baseline (0.647, p=0.05)** | **Divergence is not random variation** |

### 4.2 Interpretation of the CDS Peak

The finding that Concept Density Score peaks at Middle school (F1) rather than at Elementary or College warrants careful interpretation. A naive expectation might be that "more advanced knowledge is more densely connected." The data contradict this: the middle school mathematics curriculum acts as a **knowledge density hub**, where foundational arithmetic, introductory algebra, geometry, and probability concepts are tightly interconnected. This pattern is consistent with Ausubel's assimilation theory [12], which predicts that knowledge structures achieve maximum integration during periods of consolidation before branching into specialization.

The subsequent 3.7× drop from Middle to High school (F2) coincides with a 4.2× expansion in concept count, suggesting that the mathematics curriculum intentionally diversifies at this transition. This may reflect a pedagogical design principle: middle school provides an integrated foundation; high school introduces specialized subfields (calculus, vector geometry, statistics) that are taught in relative isolation before potential reintegration at the university level.

The robustness of this finding across three languages independently (ZH, EN, DE) suggests it is not an artifact of any particular textbook tradition. Rather, it may reflect a universal property of mathematics curriculum design — or at least a convergence across three distinct educational systems.

### 4.3 Cross-Linguistic Structural Divergence

The LDS results (F4) reveal that structural divergence between language pairs is substantial (0.802–0.907) even when the conceptual content is the same (mathematics). This is notable: mathematical truth is universal, yet its knowledge organization varies considerably across languages.

The finding that ZH–DE shows higher divergence (0.907) than ZH–EN (0.802) is counterintuitive. One might expect two European languages (DE–EN) to share more structural similarity than either shares with Chinese. The data suggest the opposite: Chinese and English textbook traditions share more structural features at the knowledge graph level than either shares with the German tradition. This may reflect the influence of the Anglo-American mathematics curriculum tradition (including IGCSE, AP, and IB frameworks) on Chinese textbook design, while the German *Gymnasium* tradition maintains a distinct structural approach.

This interpretation is consistent with Liang and Heckmann's (2013) finding that Chinese and German mathematics textbooks differ in problem complexity and representation style [8]. Our graph-based analysis extends their content-level comparison to the structural level, revealing differences that surface-level content analysis cannot capture.

### 4.4 Cross-Disciplinary Validation

The addition of Physics (F6, F7) validates that the CDS and HDS metrics capture genuine structural properties of knowledge organization, not just artifacts of the mathematics corpus. The contrasting patterns — Math peaks at Middle school, Physics peaks at Elementary — demonstrate that **knowledge organization is discipline-dependent**, with both following the same "integrate-early, diverge-late" pattern but at different educational stages.

This finding has implications for curriculum design. If mathematics and physics students experience fundamentally different knowledge density trajectories, then pedagogical strategies that work for one discipline may not transfer to the other. Mathematics education might emphasize integration early; physics education might accept that advanced-level integration is a natural part of the learning progression.

### 4.5 The Curriculum Layer

The integration of curriculum standards (Kernlehrplan NRW, UK National Curriculum, US NGSS) into the knowledge graph framework reveals a systematic finding: **textbook-curriculum alignment varies dramatically across educational systems**:

| System | Coverage Score | Pattern |
|--------|:-------------:|---------|
| England (UK) | 82.4% | Monotonic increase: 53% (KS1) → 90% (KS4) |
| United States | 75.7% | High overall (NGSS framework) |
| NRW Germany | 34.1% | Mid-level peak: 50% (grade 7-8) → 31% (grade 12-13) |
| China | 7.5% | Likely methodological (cross-lingual matching) |

The Coverage Score distinguishes three types of structure:
- **Curriculum-driven**: patterns present in both textbook and curriculum graphs
- **Textbook-author-driven**: patterns present only in textbooks (the ~66% unmatched in NRW)
- **Universal**: patterns persisting across languages, curricula, and textbooks

### 4.6 Why Do Educational Systems Produce Different Knowledge Structures?

The substantial cross-system variation in Coverage Scores (34–82%) raises a question beyond measurement: **what explains these differences?** We consider three competing explanations.

#### Explanation A: Curriculum Granularity (Best Supported)

The most parsimonious explanation is that curricula differ in granularity. The NRW Kernlehrplan specifies 299 mathematics concepts across 6 stages, while the UK National Curriculum covers similar content with 397 broader descriptors. If a curriculum defines concepts at a finer granularity, each textbook concept can match fewer curriculum concepts by definition — producing lower Coverage Scores independent of actual content alignment.

This is supported by the NRW per-stage pattern: coverage peaks at Sek I (grades 7-8, 50.0%), where the curriculum focuses on common core content, and drops at Sek II (grades 11-13, ~31%), where the curriculum introduces specialized courses (Grundkurse, Leistungskurse) with finer-grained competency expectations.

#### Explanation B: Educational Philosophy and Assessment Structure (Higher Interpretive Value)

The UK pattern — monotonic increase from KS1 (53.3%) to KS4 (90.0%) — is consistent with an examination-oriented system where the GCSE curriculum (KS4) drives strong textbook alignment. In contrast, the NRW pattern — mid-level peak with upper-secondary decline — reflects the German *Gymnasium* tradition where the transition to Oberstufe shifts from content coverage to competency development.

This interpretation aligns with comparative education research: Schmidt et al. (2001) found that curriculum coherence varies significantly across TIMSS countries, with Germany exhibiting lower coherence between intended and implemented curricula than England. More recently, the OECD's Education at a Glance (2023) documents that Germany's federal structure produces more varied curriculum implementation than England's centralized National Curriculum.

#### Explanation C: Division of Labor Between Curriculum and Textbook (Most Nuanced)

A third possibility is that the textbook-curriculum relationship differs fundamentally across systems. In the German tradition, Lehrpläne specify minimal competency standards, while textbooks exercise significant autonomy in knowledge organization. In the English system, the National Curriculum is more prescriptive, and textbooks align closely with it.

Under this interpretation, NRW's low Coverage Score is not a deficiency but a feature: German textbooks are designed to offer alternative organizational structures that complement, rather than duplicate, the curriculum. This would predict that NRW textbooks would show HIGHER internal structural diversity (more variation across publishers) than UK textbooks — a testable hypothesis for future work.

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

**Human LDS exceeds simulation LDS for all three language pairs**, with the gap largest for DE–ZH (+0.105) and smallest for ZH–EN (+0.064). This pattern mirrors the rank order observed in both human and Wikipedia data, providing converging evidence that cross-language structural divergence is a genuine phenomenon amplified by education and culture, not an artifact of language-specific vocabulary distributions.

### 4.8 Limitations

Several limitations should be acknowledged:

**Scope of data**. The mathematics corpus (68 textbooks, 574 concepts) is comprehensive. The physics corpus (366 concepts) and chemistry corpus (220 concepts) provide cross-disciplinary validation but remain smaller. The curriculum graphs, while spanning four systems (NRW, UK, US, China), use varying matching methodologies that may affect comparability.

**Extraction methodology**. While our gold-standard validation demonstrates high overall quality (F1=0.939), the social-domain gold data were validated using semi-automated keyword matching followed by manual review. Some errors may persist in the gold standard itself.

**Human validation sample size**. The human validation study (N=8 participants, 90 extracted responses) provides initial cross-level validation but is limited in statistical power. The rank-order consistency between human LDS and Wikipedia LDS (DE–ZH > DE–EN > ZH–EN) is encouraging, but a larger sample would be needed to establish population-level generalizability. Additionally, the within-subject analysis was limited to DE-EN comparisons (no ZH–DE or ZH–EN within-subject data), restricting our ability to separate language effects from participant effects at the individual level.

**Edge-free graphs in human data**. The qwen-plus extraction produced concept-only output (no relations) for human responses, which means the LDS for human data is driven primarily by Node Jaccard similarity. The full 3-component LDS formula (GED + node Jaccard + edge Jaccard) could not be applied, and future work should collect relation annotations for human responses to enable full structural comparison.

**Causality**. Our analysis is correlational. We measure structural differences between systems but cannot attribute them to curriculum design, textbook tradition, or educational philosophy independently.

**Generalizability**. Mathematics, physics, and chemistry may share structural properties not present in humanities or social science disciplines. Extending to additional domains is a priority.

**LDS formula**. The 3-component LDS (GED + node Jaccard + edge Jaccard) has the advantage of capturing multiple structural dimensions, but the statistical properties of the averaged score are not fully characterized. Edge Jaccard is sensitive to direction assignments, and GED similarity depends on graph size.

### 4.9 Implications

Despite these limitations, the current findings have implications for three communities:

**For educational research**: The CDS and HDS metrics provide quantitative tools for curriculum analysis that complement existing qualitative frameworks (TIMSS, PISA). A curriculum designer could use CDS to identify density bottlenecks and HDS to detect excessively long prerequisite chains.

**For AI in education**: The automated pipeline demonstrates that large-scale cross-lingual knowledge graph construction from textbooks is feasible using current LLMs. This opens the possibility of curriculum-level knowledge analysis at a scale that manual content analysis cannot achieve.

**For the study of linguistic relativity**: While our data do not directly address whether "language shapes thought," they demonstrate that language-specific knowledge organization patterns exist and can be quantified. This provides a methodological foundation for future work connecting textbook structure to cognitive structure.
