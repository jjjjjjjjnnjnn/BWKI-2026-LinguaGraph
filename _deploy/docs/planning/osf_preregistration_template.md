# LinguaGraph — OSF Pre-Registration Template
## Study: Bilingual Translation-Control Validation of the Language Drift Score (LDS)
## Template Version 1.0 | Target: osf.io registration

---

## Study Information

**Title**: Within-Subject Validation of the Language Drift Score: Does Language Shape Conceptual Structure?

**Authors**: [Author Name]

**Registration Type**: AsPredicted (Standard Pre-Data Collection)

**Data Collection Status**: Data collection has not started.

---

## 1. Hypotheses

### H1: Language Drift Exceeds Random Expectation

> Within-subject LDS (comparing the same person's concept graphs across two languages) will significantly exceed a computational simulation baseline (mean LDS = 0.647, SD = 0.086).

- **Test**: One-sample t-test (one-tailed, α = 0.05)
- **Predictor**: Mean individual within-subject LDS across all participants and topics
- **Expected direction**: Human LDS > 0.647

### H2: Language Pair Difference Preserved

> The rank order of LDS across language pairs observed in the Wikipedia corpus (DE–ZH > DE–EN > ZH–EN) will be preserved in individual human data.

- **Test**: Repeated-measures ANOVA: LDS ~ language_pair + topic
- **Post-hoc**: Tukey HSD for pairwise comparisons
- **Expected**: DE–ZH > DE–EN > ZH–EN

### H3: Abstract Concepts Diverge More Than Concrete Concepts

> LDS will be higher for abstract socio-political concepts (Freedom, Justice) than for concrete experiential concepts (Home, Apple).

- **Test**: Linear mixed model: LDS ~ topic + (1|participant)
- **Contrast**: (Freedom + Justice) vs (Home + Apple_control)
- **Expected direction**: Abstract > Concrete

### H4: Control Concepts Show Minimal Drift

> Control questions (apple description, weather description) will show LDS < 0.3, validating that the extraction pipeline does not inflate drift for universal, concrete concepts.

- **Test**: One-sample t-test: mean(control LDS) < 0.3
- **Expected**: Mean control LDS < 0.3

---

## 2. Design Plan

### Study Type

Mixed experimental design:
- **Within-subject factor**: Language (2 levels per participant: Lang_A, Lang_B)
- **Between-subject factor**: Native language group (ZH, DE, EN)
- **Repeated measure**: Topic (Freedom, Justice, Success, Responsibility, Home + 2 control)

### Sample Size

- **Target N**: 30
- **Rationale**: Power analysis (d = 0.50, α = 0.05, β = 0.80) → n = 27 required for between-subject comparison. N = 30 provides buffer.
- **Within-subject power**: ZH-EN n=16 → power ≈ 0.60. DE-EN n=6 → exploratory.

### Stopping Rule

Data collection stops when:
1. N = 30 participants with complete data (all 5 topics in 2+ languages), OR
2. Recruitment period reaches 4 weeks (whichever comes first).

---

## 3. Variables

### Independent Variables

| Variable | Type | Levels |
|----------|------|--------|
| Language pair | Categorical | ZH-DE, DE-EN, ZH-EN |
| Topic | Categorical | Freedom, Justice, Success, Responsibility, Home, Apple (control), Weather (control) |
| Native language | Categorical | ZH, DE, EN |
| Language order | Categorical | 6 permutations (counterbalanced) |

### Dependent Variable

**Language Drift Score (LDS)** for each (participant, topic, language_pair) combination.

LDS(A, B) = 1 − mean(GED_sim, Node_Jaccard, Edge_Jaccard)

Computed from LLM-extracted concept graphs via qwen-plus.

### Covariates (Exploratory)

- Age
- Gender
- Self-rated language proficiency (1-5 per language)
- Topic discussion frequency (1-5)
- Years in Germany (if applicable)

---

## 4. Analysis Plan

### 4.1 Exclusion Criteria

A participant's response is excluded if:
- Answer text < 100 characters (insufficient content for extraction)
- Extraction produces 0 concepts
- Language quality flag raised (excessive code-switching, wrong language)

If >30% of a participant's responses are excluded, the entire participant is dropped.

### 4.2 Primary Analysis

```python
# H1: Human LDS > Simulation baseline
from scipy import stats
t_stat, p_value = stats.ttest_1samp(human_lds_values, 0.647)
# One-tailed: p/2 if t > 0

# H2: Language pair effect
import statsmodels.api as sm
from statsmodels.formula.api import ols
model = ols('LDS ~ C(language_pair) + C(topic)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

# H3: Topic effect (abstract vs concrete)
from statsmodels.formula.api import mixedlm
model = mixedlm('LDS ~ topic_abstractness', data=df, groups='participant_id').fit()

# H4: Control LDS < 0.3
t_stat, p_value = stats.ttest_1samp(control_lds_values, 0.3)
```

### 4.3 Multiple Comparison Correction

- H2 post-hoc: Tukey HSD (controls family-wise error rate)
- Exploratory analyses: Benjamini-Hochberg FDR correction

### 4.4 Robustness Checks

1. **Jackknife**: Remove one participant at a time, recompute mean LDS
2. **Bootstrap CI**: 1000 iterations, node-based resampling (preserving topology)
3. **Extraction quality filter**: Exclude extractions with confidence < threshold

---

## 5. Sampling Plan

### Recruitment Method

| Channel | Expected N | Rationale |
|---------|:---------:|-----------|
| International school networks | 8-12 | Access to ZH/DE/EN bilingual students |
| University language programs | 6-10 | Advanced language learners |
| Online (social media, WeChat, school forums) | 5-10 | Supplementary |

### Inclusion Criteria

- Age 13-19 (secondary school target)
- B2+ proficiency in at least 2 of {ZH, DE, EN} (self-reported)
- Informed consent (parental for <18)

### Exclusion Criteria

- Monolingual (cannot complete within-subject comparison)
- Professional linguist/philosopher (topic expertise confound)

---

## 6. Data Collection

### Instrument

Online questionnaire (Google Forms or Qualtrics), delivered in two blocks:
- Block 1: Lang_A, all 5 topics + demographics
- Block 2: Lang_B, all 5 topics + control questions

### Timing

- Per participant: ~15 minutes
- Block order: counterbalanced across participants
- 30-second break between blocks

### Quality Control

- Minimum response length: 3 sentences (monitored but not enforced)
- Language check: automated detection of code-switching
- Attention check: control questions embedded

---

## 7. Data Exclusion Reporting

**Standard disclosure** (Simmons, Nelson, & Simonsohn, 2011):

> "We report how we determined our sample size, all data exclusions (if any), all manipulations, and all measures in the study."

Any post-hoc exclusions will be:
1. Explicitly documented with rationale
2. Reported with and without exclusion for sensitivity analysis
3. Not based on the outcome variable (LDS)

---

## 8. Known Differences from AsPredicted

If any analyses deviate from this plan, the final report will:
1. Flag the deviation explicitly
2. Explain why the deviation was necessary
3. Present both planned and actual analyses where feasible

---

## 9. References

- Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-positive psychology. *Psychological Science*, 22(11), 1359-1366.
- Boroditsky, L. (2001). Does language shape thought? *Cognitive Psychology*, 43(1), 1-22.
