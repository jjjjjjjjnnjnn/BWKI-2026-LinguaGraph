## 5. Conclusion

### 5.1 Research Answer

This study investigated how different languages and educational systems organize the same knowledge, using a cross-lingual knowledge graph framework applied to mathematics and physics textbooks across Chinese, German, and English, alongside the NRW Kernlehrplan curriculum standard.

### 5.2 Core Findings

Three principal findings emerge from this analysis:

**Finding 1: Knowledge density follows a non-monotonic, discipline-dependent pattern.** Mathematics CDS peaks at Middle school (0.271), not Elementary; Physics CDS peaks at College (0.065). The density hub at intermediate levels reflects curriculum integration before disciplinary specialization — a pattern that persists across all three languages independently.

**Finding 2: Knowledge hierarchy has a bounded depth, and its mean depth varies by discipline.** Mathematics exhibits HDS ≤ 7 (mean 0.40) with 83% root concepts, indicating a shallow, web-like structure with many independent entry points. Physics exhibits deeper prerequisite chains (mean HDS 1.17) with only 49% roots, reflecting the cumulative nature of physics knowledge. The maximum depth bound (7–9) across both disciplines suggests an upper limit on prerequisite depth in educational knowledge organization.

**Finding 3: Cross-language structural divergence is substantial and asymmetric.** LDS values range from 0.80 to 0.91 across language pairs, with ZH–DE showing the highest divergence (0.907) and ZH–EN the lowest (0.802). This pattern is counterintuitive — two European languages do not share more structural similarity with each other than either shares with Chinese — and suggests that curriculum tradition, not language family, drives knowledge organization.

### 5.3 Significance

These results demonstrate that knowledge organization in education is not strictly linear, but follows structured, quantifiable patterns that vary across educational stages, languages, and disciplines. The finding that CDS peaks at intermediate levels rather than monotonically increasing or decreasing challenges the implicit assumption that "advanced knowledge is more densely connected." The bounded HDS (≤ 7) suggests that educational curricula respect a natural depth limit on prerequisite structures — a constraint that may apply across disciplines.

Methodologically, this study demonstrates that large-scale cross-lingual knowledge graph construction from textbooks is feasible using current LLMs, and that the resulting graphs can support quantitative structural analysis beyond what manual content analysis can achieve.

### 5.4 Contribution

We introduce LinguaGraph, a cross-lingual educational knowledge structure analysis framework that integrates:

- **Automated knowledge graph construction** from multilingual textbook content and curriculum standards
- **Three structural metrics**: Concept Density Score (CDS), Hierarchy Depth Score (HDS), and Language Drift Score (LDS), each capturing a distinct dimension of knowledge organization
- **Cross-lingual alignment** enabling direct structural comparison across Chinese, German, and English
- **Cross-disciplinary validation** through parallel analysis of mathematics and physics
- **Curriculum layer integration** for comparing textbook knowledge graphs to official curriculum standards

The framework is open-source and designed to be extensible to additional languages, disciplines, and knowledge sources.

---

### Final Statement

> **Knowledge in education exhibits a non-linear structural organization that varies across languages and educational systems, and can be quantitatively characterized using graph-based structural metrics.**

This work represents, to our knowledge, the first systematic cross-lingual, cross-disciplinary analysis of educational knowledge structure using graph-based metrics, and the first automated pipeline that connects textbook content and curriculum standards through a unified knowledge graph framework.
