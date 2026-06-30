# OSF Pre-Registration: LinguaGraph — Cross-Lingual Knowledge Graph Analysis

**Date**: 2026-06-30
**Version**: v1.0

---

## 1. Research Questions

**RQ1**: Do textbook knowledge structures differ systematically across languages (Chinese, German, English)?

**RQ2**: If textbook structures converge (as our pilot data suggest), does human cognitive expression diverge across languages in ways that textbook analysis cannot capture?

**RQ3**: Can the **ΔLDS = LDS-C − LDS-K** metric isolate a language-specific component of knowledge organization that textbook-only analysis misses?

### Hypotheses

| # | Hypothesis | Prediction | Status |
|---|-----------|-----------|--------|
| H1 | LDS-K > Structure Null = language-driven textbook divergence | **FALSIFIED** — Full < Structure Null for all 3 pairs | Textbook structures converge |
| H0 | LDS-K ≤ Structure Null = structure dominates, not language | **ACCEPTED** — degree distribution drives LDS-K | Null confirmed |
| H2 | LDS-C > LDS-K = cognitive expression shows greater language influence | Not yet tested (N < 30) | Core prediction |
| H3 | ΔLDS > 0 for all language pairs = genuine language signal | Not yet tested (N < 30) | Core prediction |
| H4 | Abstract topics (freedom, justice) show larger ΔLDS than concrete topics (home) | Not yet tested (N < 30) | Secondary prediction |

---

## 2. Methodology

### 2.1 Design

Mixed design:
- **Within-subject**: Bilingual participants (DE-EN) answer identical questions in both languages → within-subject LDS
- **Between-subject**: Monolingual participants (ZH, DE, EN) answer in native language → between-subject LDS

### 2.2 Participants

| Group | N (target) | Current | Language(s) | Condition |
|-------|:----------:|:-------:|-------------|-----------|
| ZH | 15 | 4 | Mandarin Chinese | Native-only |
| DE | 15 | 3 | German | Bilingual (DE-EN) |
| EN | 15 | 1 | English | Native-only |

**Target total**: N = 30 (10 per language group)
**Current**: N = 8
**Recruitment**: University students, native speakers, no formal linguistics training

### 2.3 Materials

**5 social topics** (selected for cultural variability):
1. Freedom (自由/Freiheit/freedom)
2. Justice (正义/Gerechtigkeit/justice)
3. Responsibility (责任/Verantwortung/responsibility)
4. Home (家/Zuhause/home)
5. Success (成功/Erfolg/success)

Each topic presented as an open-ended prompt: *"Please describe what [TOPIC] means to you in your own words. What concepts are most important for understanding [TOPIC]?"*

### 2.4 Extraction Pipeline

All responses → LLM concept extraction → graph construction:

| Step | Method | Tool |
|------|--------|------|
| Concept extraction | LLM (qwen-plus, validated F1=0.939) | `scripts/run_one_model.py` |
| Graph construction | Node set = unique concepts per participant | `scripts/math_graph_pipeline/` |
| Cross-language alignment | Shared concept group IDs | `aligned_data.json` |
| LDS computation | J(V_a,V_b) + J(E_a,E_b) / 2 | `docs/lds_formal_definition.md` |

### 2.5 LDS Computation

Given graphs G_a = (V_a, E_a) and G_b = (V_b, E_b):

**LDS(G_a, G_b) = 1 - (J(V_a, V_b) + J(E_a, E_b)) / 2**

where J is Jaccard similarity. Range [0,1], symmetric.

For edge-free human data (no relations extracted), LDS_cognitive = 1 - Node_Jaccard.

---

## 3. Null Model Suite (for Textbook Analysis)

| Null Model | Method | Purpose |
|-----------|--------|---------|
| Structure Null | Double-edge swap (1000 iterations), preserves degree sequence | Tests whether edges carry language signal beyond degree structure |
| Node-Permuted Null | Random node label reassignment | Tests effect of node identity |
| Complete Random | Erdős–Rényi G(n,M) | Upper bound baseline |

**Key finding (completed)**: Structure Null > Full for all language pairs → H1 falsified.

---

## 4. Analysis Plan

### 4.1 Primary Analysis

1. Compute LDS-C for each language pair (within-subject & between-subject)
2. Compare LDS-C vs LDS-K via ΔLDS = LDS-C − LDS-K
3. Test H2: LDS-C > LDS-K (paired Wilcoxon or t-test)
4. Test H3: ΔLDS > 0 (one-sample t-test)

### 4.2 Secondary Analysis

1. Topic-specific LDS-C variation (ANOVA: topic × language pair)
2. Abstract vs. concrete topic comparison
3. Within-subject vs. between-subject LDS comparison (DE-EN only)

### 4.3 Power Analysis

- Effect size estimate from pilot (N=8): Cohen's d ≈ 0.8 (ΔLDS for DE-ZH)
- Required N for 80% power (α = 0.05, two-tailed): N = 15 per group
- Target: N = 30 (10 per group) → 86% power for ΔLDS > 0

### 4.4 Exclusion Criteria

Exclude if:
- Response is empty (< 5 words)
- Extraction fails (model returns invalid JSON × 3 retries)
- Bilingual participant shows < 50% response overlap across languages (potential comprehension issue)
- Participant reports non-native proficiency in their assigned language

---

## 5. Status

| Component | Status | Notes |
|-----------|--------|-------|
| Textbook analysis (LDS-K) | **Complete** | 556 concepts, 3 languages, 4 null models |
| Human collection (N=8) | **In progress** | Target N=30 |
| LDS-C computation | **Not yet** | Waits N ≥ 30 |
| ΔLDS computation | **Not yet** | Waits N ≥ 30 |
| 19-model benchmark | **Complete** | F1 range 0.55-0.67 |
| Coverage analysis | **Complete** | 4 systems, new methodology |
| Wikipedia negative control | **Complete** | LDS = 1.0 (validates metric) |

---

## 6. Pre-registration Commitment

The following are **committed before data collection completes**:
- LDS formula (Jaccard-based) — **frozen**
- Null Model methodology (Structure / Node-Permuted / Complete Random) — **frozen**
- Extraction model (qwen-plus) — **frozen**
- Gold dataset (92 items) — **frozen**
- Topic set (5 social topics) — **frozen**

The following are **confirmatory tests** (will be run after N ≥ 30):
- H2 (LDS-C > LDS-K) — one-tailed Wilcoxon
- H3 (ΔLDS > 0) — one-sample t-test
- H4 (topic effect on ΔLDS) — ANOVA

---

## 7. Deviations

If any of the above frozen components change, this pre-registration must be updated with a version bump.
