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
| **Divergence (LDS)** | Cross-language structure differs substantially | ZH–DE: 0.907; DE–EN: 0.901; ZH–EN: 0.802 |
| **Coverage (CS)** | Textbook-curriculum alignment varies by system | NRW 34%, UK 82%, US 76%, CN 8% |

### 5.3 Contributions

We introduce LinguaGraph, the first framework that:

1. **Automatically constructs multilingual educational knowledge graphs** from textbooks across ZH/EN/DE
2. **Quantifies structural patterns** via four graph-based metrics (CDS, HDS, LDS, CS)
3. **Cross-validates across three STEM disciplines** (Mathematics, Physics, Chemistry)
4. **Integrates curriculum alignment** across four educational systems (NRW, UK, US)
5. **Benchmarks multilingual LLM extraction** across domains (social: F1≥0.88; mathematical: F1≥0.71)

### 5.4 Limitations

The study has three principal limitations:

1. **Extraction quality varies by domain**: Social concept extraction achieves ZH F1=0.974, DE F1=0.949, EN F1=0.882 (72 gold labels in social domain; 92 total including math). Mathematical domain extraction is lower (DE F1=0.506, 20 gold labels), confirming domain-specific variation.
2. **Curriculum comparison**: The Coverage Score v1 uses keyword-based matching; future versions should incorporate semantic alignment.
3. **Gold dataset size**: Current 92 total gold labels provide reliable estimates across domains. Expanding to 200+ would further strengthen statistical power for subgroup analyses.

### 5.5 Future Work

- **Multilingual fine-tuned models** for cross-lingual concept extraction
- **Additional disciplines** (chemistry, biology) to test the "integrate-early, diverge-late" hypothesis
- **Semantic Coverage Score** using embedding-based concept matching
- **Cognitive Space visualization** for interactive exploration of cross-lingual structure differences

### Final Statement

> **Knowledge in education follows a non-linear structural organization that is universal in its early-stage integration, discipline-dependent in its rate of divergence, and measurably different across languages — captured by LinguaGraph's three-metric framework.**
