# LinguaGraph — Evidence Register

> **Purpose**: Maps each scientific claim to its supporting evidence, maturity level, and confidence.
> **Principle**: All claims must be traceable to evidence. Claims without sufficient evidence are labeled as such.
> **Updated**: 2026-07-01

---

## Register

| # | Claim | Evidence Stream | Supporting Data | Maturity | Confidence | Notes |
|---|-------|:---------------:|----------------|:--------:|:----------:|-------|
| C1 | Educational knowledge follows an "integrate-early, diverge-late" pattern across disciplines | LDS-K | CDS by education level: Math (0.271@Middle → 0.041@College), Physics (0.222@Elementary → 0.035@College), Chemistry (0.042@Middle → 0.030@College) | **Mature** | **High** | Consistent across 3 disciplines, 3 languages |
| C2 | Prerequisite depth is universally bounded | LDS-K | HDS max 8 (Math), 6 (Physics); 83% of math concepts are root nodes | **Mature** | **High** | BFS on 3,538 prerequisite relations |
| C3 | Cross-linguistic knowledge structure relationships are heterogeneous | LDS-K | ZH-DE=0.519 (convergence), ZH-EN=0.934 (near noise floor), DE-EN=0.938 (near noise floor) | **Mature** | **High** | Null Model confirms Full < Structure Null for all pairs |
| C4 | Within-language variation sets a noise floor for LDS interpretation | LDS-K | Within-language split-half LDS ≈ 0.97; cross-language pairs at 0.52–0.94 | **Mature** | **High** | Null Model Suite finding |
| C5 | Textbook structures converge more than random expectation | LDS-K | Full < Structure Null for all language pairs | **Mature** | **High** | Fundamental reframing of LDS |
| C6 | LDS-K cannot be interpreted as "language-driven divergence" | LDS-K | All three language pairs at or below within-language noise floor | **Mature** | **High** | Core narrative shift |
| C7 | ΔLDS = LDS-C − LDS-K shows heterogeneous patterns across language pairs | LDS-C + LDS-K | Pilot N=8: DE-ZH ΔLDS=+0.232, ZH-EN ΔLDS=−0.230, DE-EN ΔLDS=−0.211 | **Developing** | **Medium** | Effect sizes: DE-ZH d=0.84, ZH-EN d=−0.63, DE-EN d=−0.56 |
| C8 | Human concept structures vary systematically across languages | LDS-C | N=8 pilot: DE-ZH=0.751, DE-EN=0.727, ZH-EN=0.704 | **Developing** | **Medium** | Awaiting N ≥ 30 for confirmatory analysis |
| C9 | Gold-standard extraction quality is domain-dependent | LDS-K / LDS-C | Social F1=0.939 (n=72), Math F1=0.674 (n=20), DE Math F1=0.506 (n=20) | **Mature** | **High** | 92 gold labels, qwen-plus extraction |
| C10 | 19 LLMs show consistent F1 ranking across API platforms | Method | hy3-preview 0.6741, mimo-v2.5-pro 0.6735, qwen-plus 0.6659; range 0.55–0.67 | **Mature** | **High** | 3 API platforms, identical 40 gold labels |
| C11 | Curriculum–textbook coverage varies dramatically by educational governance | LDS-K | NRW 12.7%, UK 37.3%, US 17.2%, CN 95.4% | **Mature** | **High** | Coverage Score methodology |
| C12 | Spatial granularity varies substantially within a single language | LPA | DE pilot N=6: SGS criteria 3/9–9/9 | **Exploratory** | **Low** | IRR pending; N=6 only |
| C13 | Temporal metaphor ambiguity replicates in naturalistic production | LPA | DE pilot N=6: 1/5 T+, 3/5 T?, 1/5 T~ | **Exploratory** | **Low** | N=6 only; consistent with Boroditsky (2000) |
| C14 | Bilingual code-switching occurs in concept-explanation tasks | LPA | DE pilot N=6: 2/6 true bilingual explanations | **Exploratory** | **Low** | N=6 only |
| C15 | Social script strategies show high intra-lingual pragmatic variation | LPA | DE pilot N=6: 6 distinct strategy types | **Exploratory** | **Low** | N=6 only |

---

## Summary by Evidence Stream

| Stream | Total Claims | Mature | Developing | Exploratory |
|--------|:-----------:|:------:|:----------:|:-----------:|
| **LDS-K** | C1–C6, C9, C11 | **8** | 0 | 0 |
| **LDS-C** | C7–C8 | 0 | **2** | 0 |
| **LPA** | C12–C15 | 0 | 0 | **4** |

---

## Principles for Updating

1. **New claims** require an entry before they appear in any discussion or conclusion.
2. **Maturity promotion** (Exploratory → Developing → Mature) requires documented evidence (sample size, κ, effect size, null model).
3. **Confidence downgrade** (High → Medium → Low) is explicitly permitted when new evidence conflicts with prior claims.
4. **Superseded claims** are marked as `SUPERSEDED` with a pointer to the replacing claim, not deleted.
5. **Pending claims** (e.g., "ΔLDS will confirm language-driven cognitive divergence") are flagged as `PENDING` with the required evidence threshold.
