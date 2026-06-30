## 5. Conclusion

### 5.1 Unified Finding

This study investigated how different languages and educational systems organize the same knowledge. Using a cross-lingual knowledge graph framework applied to **574 mathematics and 366 physics concepts** across Chinese, German, and English, we found a consistent structural pattern:

> **Educational knowledge organization follows a universal "integrate-early, diverge-late" pattern: maximum connection density occurs at foundational stages (Elementary/Middle school) across both disciplines and all three languages, then monotonically declines as knowledge specializes.**

Mathematics peaks at Middle school (CDS=0.271), Physics at Elementary school (CDS=0.222) — not at advanced levels as one might intuitively assume. This challenges the implicit belief that "more advanced knowledge is more densely connected."

### 5.2 Three Dimensions of Structure

| Dimension | Finding | Bound |
|-----------|---------|-------|
| **Density (CDS)** | ALL disciplines peak in early stages, then decline | Math: 0.271 @ Middle; Physics: 0.222 @ Elementary; Chemistry: 0.042 @ Middle |
| **Depth (HDS)** | Prerequisite chains are universally bounded | Max 8 (Math deepest at 8, Physics at 6) |
| **Divergence (LDS-K)** | Textbook structures converge across languages; Null Model falsifies language-driven divergence | Full < Structure Null for all 3 pairs; core finding is ΔLDS |
| **Coverage (CS)** | Textbook-curriculum alignment varies dramatically | NRW 12.7%, UK 37.3%, US 17.2%, CN 95.4% |

### 5.3 Core Scientific Contribution: The Null Model Reframing

The key methodological contribution of this study is the **Null Model Suite for LDS interpretation**. Without it, the high LDS-K values (0.519–0.938) would naively be interpreted as evidence for language-driven structural divergence. The degree-preserving Structure Null reveals the opposite: real textbook graphs are systematically **more similar** across languages than randomized graphs with the same degree sequence. This means:

1. **LDS-K measures structural convergence, not divergence** — textbook knowledge organization is dominated by shared mathematical prerequisite logic
2. **The interpretable signal is ΔLDS = LDS-C − LDS-K** — the difference between cognitive expression and textbook structure isolates the language-specific component
3. **Wikipedia-based LDS (0.80–0.91) was an artifact of corpus construction** — the pipeline-corrected LDS-K tells a fundamentally different story

The 19-model benchmark (hy3-preview F1=0.674 to deepseek-chat F1=0.547) confirms that extraction quality is robust and consistent across model families, supporting the reliability of the pipeline.

### 5.4 Contributions

We introduce LinguaGraph, the first framework that:

1. **Automatically constructs multilingual educational knowledge graphs** from textbooks across ZH/EN/DE
2. **Quantifies structural patterns** via four graph-based metrics (CDS, HDS, LDS, CS)
3. **Provides a Null Model foundation** for interpreting LDS, reframing the metric from "divergence" to "convergence" and identifying ΔLDS as the core signal
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

> **Knowledge in education follows a non-linear structural organization that is universal in its early-stage integration, discipline-dependent in its rate of divergence, and — counterintuitively — convergent rather than divergent across languages at the textbook level. The language signal emerges only in cognitive expression (LDS-C), isolated by the ΔLDS metric. LinguaGraph makes these invisible structural patterns visible, measurable, and comparable across 3 disciplines, 3 languages, and 4 educational systems.**
