# LinguaGraph — BWKI 2026 Paper Outline

> Skeleton structure for final submission document (PDF, German)
> Total estimated: 25-30 pages

---

## Abstract (1 page)
- **Status**: 📝 Content missing
- **Content**: Research question, method (LLM + graph), main finding (Top Drift ranking), significance
- **Key phrase**: "Sprache formt nicht nur wie wir sprechen, sondern wie wir denken — und KI kann diesen Unterschied messen"

---

## 1. Introduction (3-4 pages)

### 1.1 Personal Motivation (0.5 page)
- **Status**: ✅ Draft exists in project plan
- **Content**: Bilingual experience (ZH native, DE school, EN academic)
- **Key**: Make it personal — BWKI values Eigenständigkeit

### 1.2 Research Question (0.5 page)
- **Status**: ✅ Clear
- **Content**: "Does language shape thinking? Can AI measure this change?"
- **Sub-questions**:
  - Do ZH/DE/EN speakers conceptualize the same topics differently?
  - Can LLM-extracted cognitive graphs capture these differences?
  - How stable is the Language Drift Score across topics?

### 1.3 Contribution Statement (1 page)
- **Status**: ✅ Draft exists
- **3 contributions**:
  1. **Language-Dependent Cognitive Structure**: First computational comparison of cognitive graphs across ZH/DE/EN
  2. **Language Drift Score (LDS)**: Novel metric quantifying cross-language cognitive divergence
  3. **Pilot Evidence**: Top Drift ranking for 5 social concepts

### 1.4 Paper Structure (0.5 page)
- **Status**: 📝 Not started
- **Content**: Roadmap of sections

---

## 2. Related Work (3-4 pages)

### 2.1 Linguistic Relativity (1 page)
- **Status**: ✅ Content in `data/evidence/research_foundation.md`
- **Must cite**: Boroditsky (2001, 2011), Lucy (1992), Slobin (1996), Winawer et al. (2007)
- **Key argument**: Language affects cognition in color, space, time — we extend to abstract social concepts

### 2.2 Bilingual Cognition (0.5 page)
- **Status**: ✅ Content exists
- **Must cite**: Athanasopoulos et al. (2015), Kroll & Stewart (1994), Bialystok (2001)

### 2.3 AI for Cognitive Science (1 page)
- **Status**: 📝 Need to write
- **Must cite**: RISE (ICLR 2026), Separating Tongue from Thought (ACL 2025), NLLB-200
- **Key argument**: We're the first to use LLM-extracted cognitive graphs for cross-language comparison

### 2.4 Knowledge Graphs in Education (0.5 page)
- **Status**: 📝 Need to write
- **Must cite**: Novak & Cañas (2008), Collins & Quillian (1969)

### 2.5 Research Gap (0.5 page)
- **Status**: ✅ Content in `research_foundation.md`
- **Claim**: No existing work compares ZH/DE/EN cognitive graphs for abstract social concepts

---

## 3. Methodology (5-6 pages)

### 3.1 Overall Pipeline (1 page)
- **Status**: ✅ Code complete, diagram needed
- **Content**: Student Response → LLM Extraction → Cognitive Graph → Cross-language Comparison → LDS

### 3.2 Concept Extraction (1 page)
- **Status**: ✅ `src/extract.py`
- **Content**: LLM prompt design, provider abstraction, concept mapping layer
- **Figure**: Prompt template + extraction example

### 3.3 Graph Construction (1 page)
- **Status**: ✅ `src/graph.py`
- **Content**: Co-occurrence-based graph construction from extracted concepts
- **Figure**: Example cognitive graph for "Freedom" in ZH vs DE vs EN

### 3.4 Cross-Language Comparison (1.5 pages)
- **Status**: ✅ `src/scoring.py`, `src/cross_language.py`
- **Content**:
  - Language Drift Score (LDS) = 1 - Graph Similarity
  - Concept Shift (set difference)
  - Relation Shift (edge difference)
  - Concept mapping layer (`config/cross_language_mapping.json`)

### 3.5 Pilot Study Design (1 page)
- **Status**: ✅ `research/experiment_design.md`
- **Content**: 5 topics × 3 languages, within-subject design
- **Table**: Topics, expected drift, LDS from pilot

### 3.6 Validation Strategy (0.5 page)
- **Status**: ✅ `evaluate_pipeline.py`
- **Content**: Human annotation, Cohen's Kappa, F1 scoring
- **Target**: Concept F1 ≥ 0.80

---

## 4. Pilot Study Results (4-5 pages)

### 4.1 Top Drift Ranking (1 page)
- **Status**: ✅ `research/findings/top_drift_concepts.md`
- **Content**: Table of 5 concepts ranked by LDS
- **Figure**: Bar chart: Success > Responsibility > Justice > Freedom > Home
- **Key finding**: Success has highest LDS (0.97), Freedom lowest (0.81)

### 4.2 Concept Shift Analysis (1 page)
- **Status**: ✅ Data in DB
- **Content**: Per-concept set differences across languages
- **Table**: Unique concepts per language per topic

### 4.3 Graph Structure Comparison (1 page)
- **Status**: ✅ `cognitive_cities_v2.json`
- **Content**: Node count, edge density, centrality distribution
- **Figure**: Side-by-side cognitive graphs (ZH vs DE vs EN for Success)

### 4.4 LDS Stability (1 page)
- **Status**: ✅ `research/findings/lds_stability_report.md`
- **Content**: Cross-version consistency, within-topic variance
- **Key finding**: Ranking stable across v2/v3 method changes

### 4.5 Case Study: Success (0.5 page)
- **Status**: 📝 Need to write
- **ZH**: Family + Effort. **DE**: Career + Competence. **EN**: Opportunity + Choice

### 4.6 Case Study: Heimat (0.5 page)
- **Status**: 📝 Need to write [currently TBD]
- **Key**: Untranslatable concept → unique methodological challenge

---

## 5. Human Study Protocol (3 pages)

### 5.1 Research Design (0.5 page)
- **Status**: ✅ `research/experiment_design.md`
- **Content**: Within-subject + between-subject mixed design
- **N**: 30 (10 ZH, 10 DE, 10 EN)

### 5.2 Materials (0.5 page)
- **Status**: ✅ Questionnaires exist
- **Content**: 5 topics × 3 languages = 15 open-ended questions
- **Table**: Question-Hypothesis mapping

### 5.3 Procedure (0.5 page)
- **Status**: 📝 Not started
- **Content**: Recruitment, consent, survey administration, language order randomization

### 5.4 Ethics (0.5 page)
- **Status**: 📝 GDPR package needed (see ethics docs)
- **Content**: Informed consent, data protection, voluntary participation, withdrawal

### 5.5 Statistical Analysis Plan (0.5 page)
- **Status**: ✅ Draft in experiment_design.md
- **Content**: t-test (H₁: LDS > 0.5), ANOVA (LDS × language), post-hoc Tukey
- **Power analysis**: d=0.6, n=10/group, α=0.05, power>0.80

### 5.6 Quality Control (0.5 page)
- **Status**: ✅ `docs/annotation_guideline_v2.md`
- **Content**: Inter-annotator agreement κ≥0.70, response quality filtering, exclusion criteria

---

## 6. Expected Results (2 pages)

### 6.1 Expected LDS Pattern (0.5 page)
- **Content**: Success > Responsibility > Justice > Freedom > Home (same as pilot)
- **If confirmed**: Strong validation of LDS metric

### 6.2 Expected Language Group Differences (1 page)
| Topic | ZH Expected | DE Expected | EN Expected |
|-------|-------------|-------------|-------------|
| Success | Family + Effort | Career + Competence | Opportunity |
| Responsibility | Duty + Society | Causality + Law | Free Will + Choice |
| Justice | Social Harmony | Procedure + Law | Rights + Equality |

### 6.3 Negative Results (0.5 page)
- Control topics (Food, Weather) should show LDS < 0.5
- If control LDS > 0.5 → method failure → report transparency

---

## 7. Limitations (1-2 pages)

### 7.1 Known Limitations
| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Small sample (n=30) | Low power for between-group | Focus on within-subject analysis |
| Wikipedia corpus only | May not reflect lived cognition | Supplement with questionnaire data |
| Keyword matching (pilot) | Lower accuracy than LLM | Upgrade to LLM for human study |
| Single annotator | No reliability check | Second annotator planned |
| Age range (13-18) | Developmental confound | Age as covariate |

### 7.2 Alternative Explanations
- LDS may reflect cultural differences, not linguistic
- Education system may confound language effects
- Translation artifacts may inflate LDS

### 7.3 Generalizability
- Social concepts only: may not extend to concrete domains
- ZH/DE/EN only: may not extend to other language families
- Bilingual participants only: may not extend to monolinguals

---

## 8. Future Work (1 page)

| Direction | Priority | Timeline |
|-----------|----------|----------|
| Cognitive City 3D visualization | P1 | Before Sep submission |
| LLM extraction upgrade (GPT/Qwen) | P2 | After human study |
| Cross-cultural extension (JP, FR, AR) | P3 | After BWKI |
| Neurocognitive validation (fMRI) | Long-term | Research program |

---

## 9. Conclusion (1 page)

- **Restate**: Language shapes cognitive structure, measurable via LDS
- **Claim**: First cross-linguistic cognitive graph comparison for social concepts
- **Impact**: Understanding bilingual cognition → improving education
- **Closing**: Personal note — a bilingual student's perspective

---

## References (3-4 pages)

### Tier 1 — Core Theory (must cite)
| # | Paper | Section |
|---|-------|---------|
| 1 | Boroditsky (2001) — Does language shape thought? | 2.1 |
| 2 | Slobin (1996) — Thinking for Speaking | 2.1 |
| 3 | Athanasopoulos et al. (2015) — Two languages, two minds | 2.2 |
| 4 | Novak & Cañas (2008) — Concept maps | 2.4 |
| 5 | Collins & Quillian (1969) — Semantic memory | 2.4 |

### Tier 2 — Method (strongly recommended)
| # | Paper | Section |
|---|-------|---------|
| 6 | Winawer et al. (2007) — Russian blues | 2.1 |
| 7 | Lucy (1992) — Grammatical categories | 2.1 |
| 8 | Kroll & Stewart (1994) — Bilingual lexical access | 2.2 |
| 9 | RISE (ICLR 2026) — Riemannian cross-lingual | 2.3 |
| 10 | Separating Tongue from Thought (ACL 2025) | 2.3 |

### Tier 3 — Context (optional)
- Additional 10-15 papers from research_foundation.md

---

## Figures & Tables Checklist

| # | Figure | Status | Section |
|---|--------|--------|---------|
| F1 | Pipeline diagram | 📝 Not created | 3.1 |
| F2 | Cognitive graph example (ZH vs DE vs EN) | 📝 Not created | 3.3 |
| F3 | Top Drift bar chart | 📝 Not created | 4.1 |
| F4 | Language × Topic heatmap | 📝 Not created | 4.2 |
| F5 | Cognitive City mockup (Three.js screenshot) | ⏳ After V1 | 4.3 |
| T1 | Concept extraction statistics | ✅ Data ready | 4.1 |
| T2 | LDS per topic per pair | ✅ Data ready | 4.1 |
| T3 | Unique concepts per language | ✅ Data ready | 4.2 |
| T4 | Control vs experimental LDS | 📝 After human study | 6.3 |

---

## Completion Summary

| Section | Est. Pages | Content Status | Notes |
|---------|-----------|----------------|-------|
| Abstract | 1 | ❌ Not started | Write last |
| Introduction | 3-4 | ✅ 60% | Needs personal story polish |
| Related Work | 3-4 | ✅ 50% | Expand AI+cog sci section |
| Methodology | 5-6 | ✅ 80% | Add pipeline diagram |
| Pilot Results | 4-5 | ✅ 70% | Add figures |
| Human Study Protocol | 3 | 📝 30% | Add ethics + procedure |
| Expected Results | 2 | ✅ 30% | Fill from human data |
| Limitations | 1-2 | ✅ 40% | Expand |
| Future Work | 1 | ✅ 50% | Add timeline |
| Conclusion | 1 | ❌ Not started | Write last |
| References | 3-4 | ✅ 50% | Need full bibliography |
| **Total** | **27-33** | **~55%** | |

---

*Generated from pilot data and project documentation — June 2026*
*Next step: fill Figures, write abstract, and integrate human study results*
