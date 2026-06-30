## 5. Conclusion

### 5.1 Summary of Observations

This study introduces LinguaGraph, a knowledge graph-based framework for measuring how knowledge is organized across languages (Chinese, German, English), disciplines (Mathematics, Physics, Chemistry), and educational systems (NRW, UK, US, China). The consistent structural pattern across all three disciplines is:

> **Educational knowledge organization follows a universal "integrate-early, diverge-late" pattern: maximum connection density occurs at foundational stages (Elementary/Middle school) across both disciplines and all three languages, then monotonically declines as knowledge specializes.**

The cross-linguistic LDS analysis reveals a more nuanced picture. Rather than a uniform "language effect," we observe **heterogeneous cross-linguistic structural relationships**:

| Language Pair | LDS-K (Textbook) | Interpretation |
|:-------------:|:----------------:|---------------|
| ZH–DE | 0.519 | **Substantial convergence** — far below within-language noise floor (0.97) |
| ZH–EN | 0.934 | **Near noise floor** — not distinguishable from within-language variation |
| DE–EN | 0.938 | **Near noise floor** — not distinguishable from within-language variation |

The critical finding is not that "language affects knowledge structure" but that **different language pairs exhibit systematically different degrees of structural convergence**, with ZH-DE showing a pattern that standard null models (degree-preserving randomization, within-language split-half) cannot explain. This heterogeneity — rather than uniformity — is the primary observation our framework enables.

### 5.2 Three Dimensions of Structure

| Dimension | Finding | Bound |
|-----------|---------|-------|
| **Density (CDS)** | ALL disciplines peak in early stages, then decline | Math: 0.271 @ Middle; Physics: 0.222 @ Elementary; Chemistry: 0.042 @ Middle |
| **Depth (HDS)** | Prerequisite chains are universally bounded | Max 8 (Math deepest at 8, Physics at 6) |
| **Divergence (LDS-K)** | Heterogeneous: ZH-DE converges (0.52); ZH-EN and DE-EN at noise level (0.93-0.94) | Within-language noise floor: ~0.97 |
| **Coverage (CS)** | Textbook-curriculum alignment varies by governance model | NRW 12.7%, UK 37.3%, US 17.2%, CN 95.4% |

### 5.3 Core Scientific Contribution: A Framework for Measuring Cross-Linguistic Structural Heterogeneity

The key contribution of this study is **not** a universal finding about language and cognition, but rather a **methodological framework** that makes heterogeneous cross-linguistic structural relationships visible and quantifiable. Specifically:

1. **LDS alone is insufficient** — the Null Model Suite shows that LDS-K values must be interpreted against multiple baselines (Structure Null, within-language noise floor, Complete Random)
2. **LDS-K reveals structural convergence, not divergence** — all three language pairs show LDS-K values at or below their within-language noise floors
3. **ΔLDS = LDS-C − LDS-K is proposed as the interpretable language signal**, but requires N ≥ 30 human data for statistical validation
4. **Pilot data (N=8) shows heterogeneous ΔLDS**: only DE-ZH (+0.232) supports the ΔLDS > 0 hypothesis; ZH-EN (−0.230) and DE-EN (−0.211) do not. The explanation for this pattern is not yet known and requires further investigation.

The 19-model benchmark (F1 range 0.55–0.67) and Wikipedia negative control (LDS=1.0) confirm that these observations are not artifacts of extraction methodology.

### 5.4 Contributions

We introduce LinguaGraph, a framework that:

1. **Automatically constructs multilingual educational knowledge graphs** from textbooks across ZH/EN/DE
2. **Quantifies structural patterns** via four graph-based metrics (CDS, HDS, LDS, CS)
3. **Provides a Null Model foundation** for interpreting LDS, revealing heterogeneous cross-linguistic structural relationships rather than a uniform language effect
4. **Cross-validates across three STEM disciplines** (Mathematics, Physics, Chemistry)
5. **Integrates curriculum alignment** across four educational systems (NRW 12.7%, UK 37.3%, US 17.2%, CN 95.4%)
6. **Benchmarks 19 multilingual LLMs** for concept extraction (F1 range 0.55–0.67), confirming cross-model robustness

### 5.5 Limitations

The study has five principal limitations:

1. **Extraction quality varies by domain**: Social concept extraction achieves ZH F1=0.974, DE F1=0.949, EN F1=0.882 (72 gold labels in social domain; 92 total including math). Mathematical domain extraction is lower (DE F1=0.506, 20 gold labels), confirming domain-specific variation.
2. **Human validation sample size**: The human validation study (N=8) demonstrates cross-level consistency but requires larger samples for population-level conclusions. The ΔLDS computation awaits N ≥ 30.
3. **Null Model scope**: The degree-preserving null is conservative — it tests edge arrangement beyond degree structure but not whether degree structure itself is language-influenced.
4. **Curriculum comparison**: The Coverage Score uses keyword-based matching; future versions should incorporate semantic alignment.
5. **Gold dataset size**: Current 92 total gold labels provide reliable estimates across domains. Expanding to 200+ would further strengthen statistical power for subgroup analyses.

### 5.6 Future Work

- **Multilingual fine-tuned models** for cross-lingual concept extraction with higher F1
- **ΔLDS computation** with N ≥ 30 human data to isolate the language signal
- **Additional disciplines** (biology, history) to test the "integrate-early, diverge-late" hypothesis across knowledge types
- **Semantic Coverage Score** using embedding-based concept matching
- **Hierarchical Null Models** to separate degree-structure effects from edge-arrangement effects
- **Cognitive Space visualization** for interactive exploration of cross-lingual structure differences

### Final Statement

> **Knowledge in education follows a non-linear structural organization that is universal in its early-stage integration and discipline-dependent in its rate of divergence. Cross-linguistic structural relationships are heterogeneous: textbook structures converge to varying degrees across language pairs, with ZH-DE showing substantially greater convergence than ZH-EN or DE-EN relative to within-language baselines. The LinguaGraph framework makes these invisible structural patterns visible, measurable, and comparable — providing a methodological foundation for investigating when, why, and to what extent language-specific knowledge organization exists. The question of whether a genuine language signal in cognitive expression exists remains open, pending the collection and analysis of N ≥ 30 human responses.**
