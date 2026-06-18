# LinguaGraph — Comprehensive Research Report

> **Generated**: 2026-06-17 | **Scope**: Full project audit + corpus analysis + compliance review
> **Method**: 8 parallel agents + synthesis

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Project Health Score** | 65/100 |
| **Top Strength** | Research methodology + cross-language corpus analysis quality |
| **Top Risk** | LDS implementation doesn't match specification — only 1/3 of formula in production |
| **Human Validation Readiness** | 35/100 — 5 blocking issues |
| **Compliance Status** | GDPR mostly OK; copyright gaps in `data/textbook/` |

### Top 5 Strengths

1. **Cross-language corpus analysis is thorough and high-quality** — 12 Wikipedia files across 4 topics × 3 languages reveal systematic ZH/DE/EN conceptual framing differences that are genuine and reproducible
2. **GitHub repo is well-structured** — CLAUDE.md, PROJECT_CYCLE.md, Gate Review, evaluation framework, all in place
3. **Ethics package is comprehensive** — 3 consent forms + GDPR package cover most requirements
4. **Related work positioning is solid** — 43 repos + 39 papers analyzed, LinguaGraph's unique contribution is clear
5. **Pipeline architecture is modular** — extract → graph → compare → explain, pluggable LLM providers

### Top 5 Risks

1. **🛑 CRITICAL: LDS production code implements only 1/3 of spec** — GED and node Jaccard missing
2. **🛑 CRITICAL: Bootstrap CI is statistically invalid** — resampling destroys graph topology
3. **🛑 CRITICAL: Concept mapping never wired into production pipeline** — all DB LDS values use raw unmapped strings
4. **🛑 HIGH: Pilot pipeline not ready (35/100)** — 5 blockers before real data can flow
5. **🟡 MEDIUM: Gold dataset is calculus domain, not social issues** — benchmark scores meaningless for current task

---

## Audit Results

### Code Quality & Security

| Severity | Count | Key Findings |
|----------|:-----:|-------------|
| CRITICAL | 2 | LDS spec mismatch; Bootstrap CI invalid |
| HIGH | 3 | Broken imports in 3 experiment scripts; No mock mode in main pipeline |
| MEDIUM | 5 | Type annotation gaps; Dead code; Prompt placeholder substitution |
| LOW | 8 | Minor naming inconsistencies; Debug print statements |

**Key code issues:**
- `experiments/pilot_corpus_analysis.py`, `experiments/textbook_comparison.py`, `research/validate_method.py`: All import functions that no longer exist (`compare_graphs`, `compare_three_languages`, `fallback_extract`)
- The two independent extraction paths (`survey_pipeline/annotate.py` vs `src/extract.py`) will diverge over time
- `config/prompts/extract.md` has `{language}` and `{text}` placeholders that are never substituted — raw placeholder text is sent to the LLM

### Data Compliance

| Metric | Value |
|--------|:-----:|
| Total files checked | ~50 |
| Files with proper license | 15 (12 Wikipedia + 3 config) |
| Files without license | ~35 (textbook corpus, pilot dataset, baseline data) |
| **Gap count** | 4 |

**Copyright risk assessment:**
| Path | Risk | Action |
|------|:----:|--------|
| `data/corpus/*.txt` | ✅ 12/12 have CC-BY-SA 4.0 headers | Good |
| `data/textbook/*.txt` | ❌ 15 files, NO source/attribution | Remove or add headers |
| `data/gold/gold_dataset.json` | ❌ No license declaration | Add CC-BY-SA note |
| `data/baseline/*.json` | ❌ No license declaration | Add generation note |
| `data/pilot_dataset/` | ❌ 60+ files from web, no license | Add source notes |

### Ethics & GDPR

| Issue | Severity | Status |
|-------|:--------:|--------|
| Consent forms reference correct GDPR articles | ✅ Good | Verified |
| DE consent form legal precision | 🟡 MEDIUM | Missing Schulbehörde, Datenschutzbeauftragter |
| `[Name]` `[Email]` placeholders unfilled | 🟡 MEDIUM | User must supply |
| Data deletion mechanism documented | ✅ Good | `gdpr_package.md` describes process |
| Data deletion mechanism implementable | ❌ WEAK | No deletion script exists |
| Google Forms for minor data | 🟡 MEDIUM | Acceptable with parental consent |
| Age range consistency (13-18 vs 16-19 vs 13-15) | ❌ CONTRADICTION | Must unify |

### Research Methodology

| Dimension | Assessment |
|-----------|------------|
| Research question clarity | ✅ Strong: "Does language shape the structure of thought?" |
| Hypothesis specificity | ✅ H1-H5 clearly defined |
| Experimental design | ✅ Mixed ANOVA, 5 topics × 3 languages |
| Construct validity | 🟡 Questionable: No control questions, no covariates |
| Concept mapping validity | 🟡 Researcher-imposed mapping may encode conclusions |
| Statistical power | 🟡 n=30 insufficient for medium effects (d=0.6 at ~45% power) |
| Replicability | 🟡 Missing: No cross-validation, no independent replication |

---

## Data Analysis Results

### Wikipedia Corpus Analysis

#### Corpus Size by Language and Topic

| Topic | ZH (chars) | DE (words) | EN (words) | Total |
|-------|:----------:|:----------:|:----------:|:-----:|
| Freedom | 474 | 185 | 266 | 925 |
| Justice | 470 | 193 | 268 | 931 |
| Responsibility | 335 | 164 | 272 | 771 |
| Success | 558 | 148 | 260 | 966 |
| **Total** | **1,837** | **690** | **1,066** | **3,593** |

**ZH dominates**: 51% of total corpus, 2-3× longer than DE articles

#### Cross-Language Conceptual Patterns

**Freedom**:
- ZH emphasizes social boundaries (他人/others, 法律/law, 集体/collective)
- EN distinguishes liberty vs freedom (Berlin, Pettit)
- DE frames as capability (Möglichkeit) and tension (Freiheit vs Sicherheit/Gleichheit)

**Justice**:
- ZH splits 公平 (fairness) and 正义 (justice) as distinct concepts, Confucian roots
- DE: 6 formal distribution principles (Distributionsprinzipien), Kohlberg's stages
- EN: Rawls-Nozick debate, retributive vs restorative justice

**Responsibility**:
- ZH: Binary frame (legal + moral), Confucian hierarchical 修身-家-国-天下
- DE: Formal three-place relation (Subject-Bereich-Instanz), Hans Jonas future ethics
- EN: Control conditions, moral luck (Nagel), reactive attitudes (Strawson)

**Success**:
- ZH: Most collectivist - 社会/society, 家庭/family, 责任/obligation
- DE: Most critical - Erfolgsreligion/Erfolgssucht critique
- EN: Most individualist - American Dream, self-made myth, CEO depression

#### Language-Specific Unique Concepts

| ZH Unique | DE Unique | EN Unique |
|-----------|-----------|-----------|
| Confucian self-cultivation (修身齐家治国平天下) | Hans Jonas future-generations ethics | Orlando Patterson: slavery origins of freedom |
| Roosevelt's Four Freedoms | Verantwortungsdiffusion | Philip Pettit: freedom as non-domination |
| 共同富裕 (common prosperity) | Kohlberg's moral stages | Thomas Nagel: four types of moral luck |
| Daoist natural justice | Erfolgsreligion/Erfolgssucht | AI/robot moral responsibility debate |
| 有教无类 (education for all) | Flow theory (Csikszentmihalyi) | Max Weber's Protestant work ethic |

### LDS Validation

| Criterion | Finding |
|-----------|---------|
| Implementation matches spec? | ❌ **No**: Only 1/3 (edge-Jaccard), missing GED + node-Jaccard |
| Test coverage | 🟡 **Inadequate**: 21 tests but no bootstrap, no multi-edge, no weighted MCL |
| Bootstrap correctness | ❌ **Invalid**: Resamples edges independently, destroys topology |
| Stability evidence | 🟡 **Weak**: 4 concepts only, single source (Wikipedia), no human data |
| Edge cases | 6 identified (empty graphs, single-node, relation-typing blind, dense saturation, string-exact matching, topology destruction) |
| **Overall confidence** | **LOW** — structural issues reduce metric credibility |

### Pilot Readiness

| Dimension | Score |
|-----------|:-----:|
| Pipeline design | 80/100 |
| CSV import | 50/100 |
| Extraction pipeline | 30/100 |
| Benchmark framework | 40/100 |
| Result templates | 90/100 |
| Documentation | 60/100 |
| **Overall** | **35/100** |

**5 blocking issues:**
1. CSV column header matching drops 3/17 questions (Q9: `responsible` vs `responsibility`, Q18: `just` vs `justice`, Q19: German-only keywords for English meta-question)
2. 74% responses flagged `short` under current thresholds
3. Zero real LLM extractions ever run — all 57 extractions in DB are mock
4. Gold dataset is calculus domain, not social issues
5. Prompt template `{language}` `{text}` placeholders never substituted

---

## Compliance Checklist

| Item | Status | Notes |
|------|:------:|-------|
| GDPR Art. 6 (consent) | ✅ | Covered in all 3 consent forms |
| GDPR Art. 7 (conditions) | ✅ | Explicit opt-in documented |
| GDPR Art. 8 (minor consent) | 🟡 | Over-16: self-consent OK. Under-16: parental consent needed |
| GDPR Art. 13 (privacy notice) | ✅ | Covered in gdpr_package.md |
| GDPR Art. 17 (erasure) | 🟡 | Documented but no deletion script exists |
| GDPR Art. 28 (processor) | 🟡 | Google Forms usage needs DPA |
| Copyright — Wikipedia | ✅ | All 12 files have CC-BY-SA 4.0 headers |
| Copyright — textbook | ❌ | 15 files with NO attribution |
| Copyright — pilot dataset | ❌ | 60+ files from web, no license |
| BWKI independence | ✅ | Core methods (LDS, pipeline, experiment) are original |
| AI data separation | ✅ | Simulation data marked `source=simulation` |

---

## Overall Recommendations

### Immediate (Before Pilot — this week)

1. **Fix LDS implementation**: Add GED + node Jaccard to `calculate_lcd_score` to match spec. The `calculate_graph_similarity` in `compare.py` already has weighted overlap — extend it.
2. **Wire concept mapping into production**: `analyze_student.py` must pass `concept_mapping` from `research/concept_mapping.py` to scoring functions.
3. **Fix CSV column mapping**: Add `responsible`, `just`, `native language influence` keywords to `import_csv.py`.
4. **Fix prompt template substitution**: Replace `{language}` and `{text}` placeholders in `config/prompts/extract.md` before they reach the LLM.
5. **Create social-issues gold dataset**: Annotate 5-10 real/simulated responses in the social-issues domain for meaningful benchmark scores.

### Medium-term (Before Main Study — 2 weeks)

6. **Fix Bootstrap CI**: Use node-based resampling (sample nodes with replacement, keep incident edges) to preserve topology.
7. **Run real LLM end-to-end test**: Use mock data through the full pipeline with GPT-4.1-mini to validate extraction works.
8. **Calibrate quality thresholds**: Set MIN_WORD_COUNT to 10-15 based on real response length distribution.
9. **Remove dead code**: Archive experiment scripts with broken imports, consolidate extraction logic into `src/extract.py`.
10. **Unify naming**: Align LCD/LDS naming across codebase and documentation.

### Long-term (Before BWKI Submission — 3 months)

11. **Increase sample size**: n=30 minimum, n=60 ideal for medium effect sizes (d=0.6 at 80% power).
12. **Recruit second annotator**: Cohen's Kappa target ≥ 0.70.
13. **Add control questions**: To distinguish language effects from education/knowledge effects.
14. **Publish formal bibliography**: DOI list for all 140+ references.
15. **Fill ethics placeholders**: `[Name]`, `[Email]`, `[Phone]` in all consent forms.

---

*Report generated by 8 parallel audit agents across code quality, data compliance, ethics, methodology, corpus analysis, findings synthesis, LDS validation, and pipeline readiness.*
