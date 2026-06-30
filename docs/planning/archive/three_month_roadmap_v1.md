# LinguaGraph — 3-Month Strategic Roadmap
## Target: BWKI 2026 Full Submission (Deadline: 2026-09-21)

---

## Current State: High Maturity (Estimated 88%)

| Dimension | Status | Gap |
|-----------|--------|-----|
| Textbook KG | 1,160 concepts, 4,136 relations, 3 disciplines | None |
| Extraction validation | 92 gold, F1=0.939, 20-model benchmark | None |
| Human validation | N=8 pilot, 6 within-subject + 15 between-subject LDS | **N too small** |
| Simulation baseline | 300 responses, LDS=0.647, human > sim (p=0.05) | None |
| Cross-disciplinary | Math (574), Physics (366), Chemistry (220) | None |
| Curriculum alignment | NRW, UK, US, CN — 4 systems | Methodology refinement |
| LDS theory | 3-component formula (GED + NodeJac + EdgeJac) | **No formal properties proof** |
| Paper | 9 sections (DE), 12 findings (F1-F12) | Limitation audit done |
| Portal | 5 findings, 3D CognitiveSpace, charts | None |
| Speeches | 30s/3min/10min (DE) | None |

---

## Strategy: Depth Over Breadth

**Core thesis**: "LDS is the first quantifiable metric for measuring how language shapes knowledge structure. It operates consistently across three levels — individual cognition, educational materials, and curriculum policy."

**Decision**: Option A (single-point breakthrough) with selective demo enhancements.

---

## Month 1: Human Validation Scale-Up (Jul 1 – Jul 31)

### Goal: N=30, within-subject bilingual, statistically significant

| Week | Action | Deliverable | Status |
|------|--------|-------------|--------|
| W1 | Finalize experiment protocol + ethics | Protocol doc, consent forms (ZH/DE/EN) | To do |
| W1 | Register analysis plan on OSF | OSF preregistration | To do |
| W2-3 | Recruit 22+ participants | 22 signed consents | To do |
| W3-4 | Data collection | 30 × 5 topics × 2-3 languages ≈ 300-450 responses | To do |
| W4 | Batch extraction via qwen-plus | ~300 extractions in DB | To do |

### Key Design Decision: Bilingual Translation-Control

**Protocol**: Each participant answers the same 5 social topics in their TWO strongest languages (ZH+EN, DE+EN, or ZH+DE).

**This allows separation of**:
- Language effect (within-subject, same topic, different language)
- Individual effect (between-subject, same language, different person)
- Topic effect (within-subject, same language, different topic)

### Analysis Plan (Pre-Registered)

```
H1 (Language effect): Within-subject LDS > simulation baseline LDS
  → Paired t-test: mean(individual LDS) vs 0.647

H2 (Language pair difference): DE-ZH LDS > ZH-EN LDS
  → Repeated measures ANOVA: LDS ~ language_pair + topic

H3 (Level consistency): Rank order preserved across individual/corpus/curriculum
  → Spearman rank correlation between human and Wikipedia LDS

H4 (Topic effect): abstract concepts (Freedom, Justice) > concrete (Home)
  → Linear mixed model: LDS ~ topic + (1|participant)
```

---

## Month 2: Theory + Analysis (Aug 1 – Aug 31)

### Goal: Formalize LDS + run full analysis on N=30 data

| Week | Action | Deliverable |
|------|--------|-------------|
| W5-6 | Run pipeline on new data | LDS values for all 30 participants |
| W6-7 | Statistical analysis (R/Python) | All hypothesis tests, figures |
| W7-8 | LDS theoretical properties proof | Formal math appendix |

### LDS Theory Package

1. **Metric properties**: Prove non-negativity, symmetry, boundedness (0 ≤ LDS ≤ 1)
2. **Sensitivity analysis**: How does LDS respond to node addition/removal?
3. **Comparison with alternatives**: Jaccard-only, GED-only, Wasserstein
4. **Confidence intervals**: Bootstrap CI methodology formalized

### Cross-Discipline Narrative Refinement

**Claim**: The "integrate-early, diverge-late" pattern holds across Math/Physics/Chemistry, but at different stages:

| Discipline | CDS Peak | Peak Stage | CDS at Peak |
|------------|----------|------------|:-----------:|
| Mathematics | Middle | 初中 (grade 7-9) | 0.271 |
| Physics | Elementary | 小学 (grade 1-6) | 0.222 |
| Chemistry | Middle | 初中 (grade 7-9) | 0.042 |

**Unifying narrative**: "All three STEM disciplines share the same structural pattern — density peaks at introductory stages, then declines as specialization increases — but the timing of the peak reflects the discipline's pedagogical role in the curriculum."

---

## Month 3: Demo + Delivery (Sep 1 – Sep 21)

### Goal: Polished submission package

| Week | Action | Deliverable |
|------|--------|-------------|
| W9-10 | Final paper review + polish | Complete DE paper |
| W10-11 | Real-time demo | Portal with live LDS computation |
| W11-12 | Speech refinement + rehearsal | 3 final presentations |
| W12 | Final package assembly | All submission materials |

### Real-Time Demo Technical Spec

**Goal**: Juror types a concept → 3 seconds → tri-lingual cognitive graph comparison + LDS

**Architecture**:
```
User input (e.g., "Freiheit")
  → Wikipedia API fetch (ZH/DE/EN articles)
  → qwen-plus extraction (3 API calls, parallel)
  → Graph construction (3 graphs)
  → LDS computation (3 pairs)
  → Visual output (3-column graph display + LDS matrix)
```

**Fallback**: Pre-computed cache for 20 common concepts (freedom, justice, etc.)
to guarantee 3-second response even if API is slow.

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|:----------:|:------:|------------|
| Cannot recruit 22 bilinguals in time | Medium | High | Fallback to Option C (10 bilingual + 20 monolingual) |
| qwen-plus API rate limit | Low | Medium | Batch processing, rate limit handling in pipeline |
| N=30 still not significant | Low | Medium | Pre-compute power analysis; accept and report honestly |
| Real-time demo fails during jury | Low | High | Pre-recorded video backup |

---

## Decision Log

| # | Decision | Rationale | Date |
|---|----------|-----------|------|
| D1 | No new disciplines/languages | Existing 3×3 matrix sufficient | 2026-06-25 |
| D2 | No API/REST layer | Not needed for submission; GitHub Pages is deployed | 2026-06-25 |
| D3 | Code open-sourced on GitHub | Already done; satisfies reproducibility | 2026-06-25 |
| D4 | Bilingual translation-control protocol | Strongest causal inference for within-subject LDS | 2026-06-25 |
