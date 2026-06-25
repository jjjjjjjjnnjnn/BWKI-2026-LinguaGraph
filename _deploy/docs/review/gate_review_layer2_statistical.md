# Gate Review — Layer 2: Statistical Methodology Audit

**Reviewer**: Senior Statistics Reviewer  
**Date**: 2026-06-17  
**Scope**: LinguaGraph BWKI 2026 project statistical design, power analysis, test selection, inter-annotator agreement, multiple comparisons, and variance estimation.

---

## Issue 1: Power Analysis — Claim Does Not Match Design

- **Risk**: Inflated statistical power claim
- **Severity**: CRITICAL
- **Evidence**:
  - `README.md` lines 52, 85-88: claims d=0.6-0.8, alpha=0.05, power>0.80, n=30 (10 per language group)
  - `docs/bwki_paper_outline.md` line 160-161: restates the same claim
  - `docs/experiment-design.md` lines 25-30: says n=15 (5 per group), NOT n=30 — there is a sample-size contradiction between documents
  - No actual G\*Power calculation or power-analysis script exists anywhere in the repository
- **Impact**: For a **3-group between-subjects ANOVA** (the stated design), with n=10 per group (total N=30), alpha=0.05, power=0.80: the minimum detectable effect is Cohen's f approximately 0.57, which corresponds to Cohen's d approximately 1.14 between the extreme groups. This is a **very large** effect (beyond Cohen's "large" = 0.8). The claim that d=0.6 is detectable at 80% power is **incorrect** for a 3-group design. At d=0.6, the actual power is approximately 0.45 — below the conventional 0.80 threshold. The claim would be roughly correct for a **two-group** t-test with n=15 per group, but the project uses 3 language groups.
  - For the **mixed design** actually planned (3 native-language groups between-subject, 3 response languages within-subject, 5 topics), power is even lower because the between-subject comparison (the main hypothesis) uses only n=10 per cell, and within-subject correlations among repeated measures are not modeled.
  - No pilot human data exists to estimate realistic effect sizes. The pilot LDS values (0.76-0.99) are raw metric values, not standardized effect sizes — they cannot substitute for Cohen's d estimates.
- **Fix cost**: Medium
- **Fix suggestion**:
  1. Resolve the n=15 vs n=30 contradiction between `experiment-design.md` and `README.md`. The database currently has only 3 students — decide the feasible sample size and be honest about it.
  2. Run a proper G\*Power or `pwr` R package calculation and document the full parameter set (test family, numerator df, number of groups, number of repeated measures, correlation among measures, non-centrality parameter).
  3. Report the **actual minimum detectable effect size** for the feasible design, not the aspirational one. If n=15 is the true target, the detectable effect at 80% power is approximately d > 1.5 (extremely large).
  4. Frame the power limitation transparently in the BWKI submission: exploratory study, effect-size estimation rather than hypothesis testing, confidence intervals instead of p-values.

---

## Issue 2: Statistical Test Plan Is Vague and Partially Unimplemented

- **Risk**: Mismatch between planned tests, actual analysis code, and experimental design
- **Severity**: HIGH
- **Evidence**:
  - `docs/bwki_paper_outline.md` line 160: says "t-test (H1: LDS > 0.5), ANOVA (LDS x language), post-hoc Tukey"
  - `scripts/analyze_pilot.py`: implements only participant-level quality checks, word count statistics, and placeholder LDS output — **no inferential tests at all**
  - `scripts/analyze_student.py`: computes LCD scores per student, stores results — computes no t-tests, no ANOVAs, no post-hoc tests
  - `scripts/bwki_analysis.py`: computes only descriptive statistics (mean, std), Pearson r, and Spearman rho — no inferential tests of the main hypothesis
  - `scripts/compare_human_vs_model.py`: computes Spearman correlation without testing the main effect of language
- **Impact**: The entire inferential statistical analysis plan exists only as a 1-line note in the paper outline. No actual ANOVA, t-test, or post-hoc test has been written, tested, or validated. The BWKI submission would lack the core quantitative evidence supporting the claim that "language shapes thinking." For a competition requiring empirical validation, this is a critical gap.
  - The planned "t-test (H1: LDS > 0.5)" tests whether LDS exceeds a threshold, which is a fundamentally different question from "do language groups differ?" A significant t-test against 0.5 could occur even if all three language groups have identical LDS, as long as LDS > 0.5. This does not address the research hypothesis.
  - There is no code to test the **interaction** between native language and response language (the core scientific question: do native ZH speakers produce different graphs when answering in ZH vs DE vs EN?).
- **Fix cost**: Medium-High (requires writing statistical test code, interpreting results, and potentially collecting more data)
- **Fix suggestion**:
  1. Implement a mixed ANOVA with native language as between-subject factor (ZH/DE/EN), response language as within-subject factor (ZH/DE/EN), and topic as within-subject factor (5 levels). The dependent variable should be a graph-similarity or node-overlap measure.
  2. If the data is too sparse for ANOVA, implement paired t-tests for within-subject comparisons (each participant's ZH graph vs their DE graph) with appropriate corrections.
  3. Remove the "t-test (H1: LDS > 0.5)" plan unless the research question is explicitly about an absolute LDS threshold.
  4. Include the analysis code in the submission package with documented output.

---

## Issue 3: Cohen's Kappa — Target Appropriate but Implementation Has Errors

- **Risk**: Risk of reporting invalid Kappa values / metric confusion
- **Severity**: HIGH
- **Evidence**:
  - `scripts/annotator_agreement.py` lines 50-71: implements Cohen's Kappa correctly but **only for quality ratings** (4-category ordinal: rich/moderate/thin/empty)
  - `scripts/annotator_agreement.py` lines 92-96: uses **Jaccard similarity** for concept and relation agreement — not Kappa
  - `docs/annotation_guideline_v2.md` lines 459-462: sets target as "concept overlap Kappa >= 0.70" but the code computes Jaccard, not Kappa — the guideline and code disagree on what metric is used
  - `docs/annotation_guideline_v2.md` lines 467-481: example code attempts to pass 2D per-concept presence vectors to `sklearn.metrics.cohen_kappa_score`, which expects 1D label arrays. This code **would raise an error or produce incorrect output** when run. The `vec_A` is a list of lists (each inner list is a 0/1 vector spanning all concepts), but `cohen_kappa_score` expects flat label arrays.
  - `docs/questionnaire_validation.md` lines 284-290: targets Concept Jaccard >= 0.70 and **Relation Cohen's kappa >= 0.65**, but the code computes Relation Jaccard instead of Kappa
  - **No pair of annotators has actually run the script** — there are no Kappa values in the database
- **Impact**:
  - **Metric confusion**: The guideline claims Kappa, the code computes Jaccard. A BWKI judge reading the guideline would expect Kappa values; the code produces Jaccard values. These are different metrics with different interpretations (Kappa corrects for chance agreement, Jaccard does not).
  - **Prevalence problem**: For concept extraction, if most concepts are absent in a given response (sparse annotation, which is expected — a 200-word response only yields 5-15 concepts), Cohen's Kappa can be paradoxically low even with high observed agreement (the "Kappa paradox" or "prevalence problem"). Jaccard avoids this but does not correct for chance agreement. The choice should be justified, not confused.
  - **Implementation bug**: The code example in the guideline would fail at runtime. If a reviewer copies it, they get no result.
  - **No actual Kappa values exist**: The project cannot currently demonstrate inter-annotator reliability.
- **Fix cost**: Low-Medium
- **Fix suggestion**:
  1. Decide on a single metric: either Kappa (with awareness of the prevalence problem) or Jaccard (acknowledging it does not correct for chance). For concept extraction with sparse binary decisions, **Fleiss' Kappa** or **Gwet's AC1** would be more appropriate than Cohen's Kappa.
  2. Fix the code example in `annotation_guideline_v2.md` lines 475-479. The correct approach for Kappa on concept extraction is to flatten each response into a binary label per concept, then compute Kappa across all (response x concept) pairs.
  3. If using Jaccard instead of Kappa, update the guideline to not call it "Cohen's Kappa" and set appropriate targets.
  4. Run the annotator agreement script on at least 20 double-annotated responses before submission.
  5. For the guideline's relation agreement target: either implement actual Cohen's Kappa for relation types, or rename the target to "Relation Jaccard."

---

## Issue 4: No Multiple Comparison Correction Planned

- **Risk**: Inflated Type I error rate
- **Severity**: HIGH
- **Evidence**:
  - The full search of `docs/` and `scripts/` finds no mention of Bonferroni, FDR, Holm-Bonferroni, Benjamini-Hochberg, or any multiple comparison correction procedure
  - `docs/bwki_paper_outline.md` line 160: mentions "post-hoc Tukey" for within-ANOVA pairwise comparisons but does not address the across-test multiplicity
  - `scripts/bwki_analysis.py` runs 6 Pearson/Spearman correlations (3 source-pairs) without any correction
  - `scripts/compare_human_vs_model.py` compares LDS across 5 topics x 3 language pairs = 15 separate data points without correction
- **Impact**: With the default alpha = 0.05, and at least 15 explicit LDS comparisons (5 topics x 3 language pairs), the **family-wise error rate** is:
  
  FWER = 1 - (0.95)^15 = 0.537
  
  There is a **greater than 50% chance of at least one false positive** across the reported comparisons. If 6 correlations are also reported, FWER rises further. A BWKI reviewer or judge who notices missing correction will question the validity of all significance claims.
  - Tukey's HSD only corrects for pairwise comparisons **within a single ANOVA**. If the project runs 5 separate ANOVAs (one per topic), each with Tukey correction, the across-topic multiplicity remains uncorrected.
  - Uncorrected p-values weaken the core claim of "significant cross-language differences."
- **Fix cost**: Low
- **Fix suggestion**:
  1. Document a formal multiple comparison strategy in `docs/experiment-design.md`. Recommended approach:
     - **Global test first**: Mixed ANOVA with language pair as factor, topics as repeated measures. Only if the global F is significant, proceed to pairwise tests.
     - If global testing is not feasible (e.g., different topics use different concept sets), apply **Benjamini-Hochberg FDR** at q=0.10 across the 15 topic-pair tests. This is less conservative than Bonferroni (which would require p < 0.0033) and more appropriate for exploratory research.
  2. For the 6 Spearman/Pearson correlations in `bwki_analysis.py`, apply Bonferroni correction: report significance at p < 0.0083 (0.05/6).
  3. Add a dedicated section in the BWKI paper titled "Multiple Comparison Correction" explaining the approach.

---

## Issue 5: LDS Has No Variance Estimate — Cannot Test Significance

- **Risk**: Core metric cannot support inferential claims
- **Severity**: CRITICAL
- **Evidence**:
  - `src/scoring.py` lines 93-135 (`calculate_lcd_score`): computes LDS as a single point value: `1 - len(intersection)/len(union)`. No variance, no confidence interval, no standard error.
  - `src/scoring.py` lines 20-50 (`calculate_mcl_score`): same issue — point estimate only.
  - `scripts/analyze_student.py` line 211: stores `lcd_score` in the database as a single float. No CI column exists in the `cross_language_analysis` table.
  - `scripts/bwki_analysis.py` lines 156-157: computes mean and std across multiple LDS values but does not compute confidence intervals for individual LDS values.
  - No bootstrap, jackknife, or resampling code exists anywhere in the codebase (confirmed by grep for "bootstrap|confiden.*interval|variance|sem|se\\." in src/).
  - `docs/methodology.md` lines 44-49: acknowledges limitations of GED and string-exact matching but does not mention the absence of variance estimation.
- **Impact**: Without a variance estimate, the project **cannot**:
  - Determine if LDS = 0.3 is "significantly different" from LDS = 0.2 (the difference could be within the noise floor).
  - Construct confidence intervals for effect sizes.
  - Perform any statistical test that requires a standard error (t-test, ANOVA, post-hoc).
  - Answer the BWKI judge question: "Is an LDS of 0.7 really different from 0.5, or is that just measurement noise?"
  
  The entire quantitative argument of the project depends on comparing LDS values across language pairs and topics. Without variance, these comparisons are purely **descriptive** — they cannot support inferential claims about language shaping thinking.
  
  The Spearman/Pearson correlations in `bwki_analysis.py` use point-estimate mean LDS values, which ignores measurement uncertainty. This overstates precision.
  
  **The project currently has no way to test its core hypothesis statistically.**
- **Fix cost**: Medium
- **Fix suggestion**:
  1. **Immediate**: Implement **non-parametric bootstrap** to estimate the sampling distribution of LDS:
     - For each participant, resample their 5 topic-level graphs with replacement (B = 1000 iterations).
     - Compute LDS per resample, store the distribution.
     - Report median LDS and 95% percentile bootstrap confidence interval.
     - This allows answering "is LDS = 0.3 different from LDS = 0.2" — check if the 95% CIs overlap.
  2. **Alternative**: Implement a **permutation test** for comparing LDS between two language pairs:
     - Pool graphs from both language pairs, randomly permute the pair labels, recompute the LDS difference.
     - The proportion of permuted differences exceeding the observed difference is the p-value.
  3. **Add columns** to the `cross_language_analysis` table: `lds_ci_lower`, `lds_ci_upper`, `bootstrap_n`.
  4. Document the LDS variance estimation method in `docs/methodology.md` and include it in the BWKI paper's Methods section. Without this, the statistical analysis is incomplete.

---

## Summary

| # | Issue | Severity | Currently Blocks BWKI? |
|---|-------|----------|----------------------|
| 1 | Power analysis claim does not match design | CRITICAL | Potentially — if a judge checks power calculations |
| 2 | Statistical test plan unimplemented | HIGH | Yes — no test of the core hypothesis exists |
| 3 | Cohen's Kappa: metric confusion + buggy example | HIGH | No — but a judge reading the code would find errors |
| 4 | No multiple comparison correction | HIGH | Yes — risk of reporting inflated significance |
| 5 | LDS has no variance estimate | CRITICAL | **Yes — core metric cannot support inferential claims** |

**Bottom line**: The project has a well-designed LDS metric and a functional graph extraction pipeline, but the statistical layer is incomplete. The single most critical gap is **Issue 5** (no LDS variance), which means the project currently cannot perform any inferential statistical test on its primary outcome measure. Issue 2 compounds this by not having any statistical test code implemented at all.

**Recommended path**: Prioritize bootstrap confidence intervals for LDS (Issue 5, fix cost Medium) and implement the mixed ANOVA with appropriate multiple comparison correction (Issues 2 + 4, fix cost Medium-High). The power analysis (Issue 1) should be reframed as a limitation rather than an aspirational claim.
