# Human vs Simulation Comparison Framework

**Project**: LinguaGraph — BWKI 2026
**Date**: 2026-06-17
**Purpose**: Define the complete comparison methodology for Human data vs LLM Simulation baseline

---

## 1. Overview

This framework defines how we will compare cognitive structures extracted from **human respondents** (9 pilot / 30 main study) against **LLM simulation baseline** (300 simulated responses). The comparison validates whether LLM persona simulation captures human-like cross-language cognitive patterns.

### Data Sources

| Source | N | Status | Description |
|--------|---|--------|-------------|
| Wikipedia Corpus | 813 texts | ✅ Complete | Internet reference baseline |
| Simulation Baseline | 300 responses | ⏳ Template only | LLM-generated with persona prompts |
| Pilot Study | 9 respondents | ⏳ Not started | 3 ZH + 3 DE + 3 EN native speakers |
| Main Study | 30 respondents | ⏳ Not started | 10 ZH + 10 DE + 10 EN native speakers |

### Comparison Dimensions

We compare across **4 independent dimensions**, each capturing a different aspect of cognitive structure similarity:

1. **LDS Correlation** — Do the language drift scores rank topics the same way?
2. **Concept Overlap** — Do humans and simulations use the same concepts?
3. **Centrality Ranking** — Are the most important concepts the same?
4. **Graph Structure** — Are the relationship patterns similar?

---

## 2. Metric Definitions

### 2.1 LDS Correlation

**What it measures**: Whether the Language Drift Score ranks topics consistently between human and simulation data.

**Formula**:
```
For each topic t ∈ {freedom, justice, success, responsibility, home}:
  LDS_human(t) = mean(LDS_human(t, zh-en), LDS_human(t, zh-de), LDS_human(t, de-en))
  LDS_sim(t) = mean(LDS_sim(t, zh-en), LDS_sim(t, zh-de), LDS_sim(t, de-en))

Spearman ρ = rank_correlation(LDS_human, LDS_sim)
```

**Statistical method**:
- **Primary**: Spearman rank correlation (ρ) — non-parametric, robust to outliers
- **Secondary**: Pearson r — measures linear relationship of absolute values
- **Significance**: Permutation test (1000 iterations) — shuffle topic labels and recompute ρ
- **Confidence interval**: Bootstrap 95% CI (1000 resamples)

**Interpretation**:
| ρ range | Interpretation |
|---------|----------------|
| ρ > 0.7 | Strong agreement — simulation captures human drift patterns |
| 0.4 < ρ ≤ 0.7 | Moderate agreement — partial capture |
| 0 ≤ ρ ≤ 0.4 | Weak agreement — simulation misses key patterns |
| ρ < 0 | Disagreement — simulation inverts human patterns |

**Per-pair breakdown**: Compute ρ separately for each language pair (zh-en, zh-de, de-en) to identify which pairs the simulation handles best/worst.

### 2.2 Concept Overlap (Jaccard Index)

**What it measures**: How much the set of extracted concepts overlaps between human and simulation for the same topic and language.

**Formula**:
```
For each (topic, language) cell:
  C_human = {mapped_concepts from human responses}
  C_sim = {mapped_concepts from simulation responses}
  Jaccard(t, l) = |C_human ∩ C_sim| / |C_human ∪ C_sim|
```

**Concept mapping**: Uses `config/cross_language_mapping.json` to map language-specific concepts to shared IDs (e.g., "自由" → "CONCEPT_FREEDOM").

**Aggregation**:
- Per-cell Jaccard (5 topics × 3 languages = 15 cells)
- Mean Jaccard across all cells
- Mean Jaccard per language (to see if simulation matches ZH/DE/EN differently)
- Mean Jaccard per topic (to see which concepts are easier to simulate)

**Statistical method**:
- **Significance**: Binomial test — is observed overlap greater than chance?
- **Chance baseline**: |C_human| × |C_sim| / |U| where U is the universal concept pool

### 2.3 Centrality Ranking Similarity

**What it measures**: Whether the most central/important concepts are the same in human and simulation graphs.

**Formula**:
```
For each (topic, language) cell:
  Rank_human = sorted concepts by centrality (descending)
  Rank_sim = sorted concepts by centrality (descending)
  Kendall τ = concordance(Rank_human, Rank_sim)
```

**Centrality definition**: Degree centrality in the concept graph (number of connections a concept has).

**Statistical method**:
- **Primary**: Kendall τ (tau-b for ties) — measures ordinal association
- **Secondary**: Top-k overlap — do the top 3 concepts match?
- **Significance**: Permutation test on concept labels

**Interpretation**:
| τ range | Interpretation |
|---------|----------------|
| τ > 0.7 | Same "most important" concepts |
| 0.4 < τ ≤ 0.7 | Partially overlapping importance |
| τ ≤ 0.4 | Different concepts prioritized |

### 2.4 Graph Structure Similarity

**What it measures**: Whether the overall relationship patterns (not just node identities) are similar.

**Method A — Edge Pattern Similarity**:
```
For each (topic, language) cell:
  E_human = {(mapped_src, mapped_tgt) for all edges}
  E_sim = {(mapped_src, mapped_tgt) for all edges}
  Edge_Jaccard = |E_human ∩ E_sim| / |E_human ∪ E_sim|
```

**Method B — Degree Distribution Similarity**:
```
For each (topic, language) cell:
  deg_human = [degree(c) for c in concepts]
  deg_sim = [degree(c) for c in concepts]
  KS_stat, p_value = ks_2samp(deg_human, deg_sim)
```

**Method C — Graph Edit Distance (GED)** (if computationally feasible):
```
GED = minimum_edit_operations(G_human, G_sim) / max(|G_human|, |G_sim|)
```

**Recommended**: Use Method A (Edge Pattern) as primary, Method B (Degree Distribution) as secondary. Method C is optional for the full paper.

---

## 3. Statistical Methods Summary

| Test | Purpose | Implementation |
|------|---------|----------------|
| Spearman ρ | LDS rank correlation | `scipy.stats.spearmanr` |
| Pearson r | LDS value correlation | `scipy.stats.pearsonr` |
| Kendall τ | Centrality rank correlation | `scipy.stats.kendalltau` |
| Jaccard index | Concept/edge overlap | Custom (set intersection/union) |
| Permutation test | Significance without distributional assumptions | Custom (1000 iterations) |
| Bootstrap CI | Confidence intervals | Custom (1000 resamples, BCa method) |
| Binomial test | Concept overlap vs chance | `scipy.stats.binomtest` |
| KS test | Degree distribution similarity | `scipy.stats.ks_2samp` |

### Power Analysis

With N=5 topics:
- Spearman ρ: minimum detectable ρ ≈ 0.80 at α=0.05, power=0.80
- For more reliable estimates, need N ≥ 8 topics (currently we have 5)

**Mitigation**: Report effect sizes (ρ, τ) alongside p-values. Focus on practical significance over statistical significance given small N.

---

## 4. Visualization Design

### 4.1 Scatter Plot: LDS Human vs LDS Simulation

```
X-axis: LDS_simulation (mean across language pairs)
Y-axis: LDS_human (mean across language pairs)
Points: 5 topics (freedom, justice, success, responsibility, home)
Diagonal line: y=x (perfect agreement)
Regression line: fitted linear model
Color: topic-specific
Annotations: topic labels next to points
```

### 4.2 Bar Chart: Per-Pair Spearman ρ

```
X-axis: Language pairs (zh-en, zh-de, de-en)
Y-axis: Spearman ρ
Bars: grouped (overall ρ, per-pair ρ)
Error bars: 95% bootstrap CI
Reference line: ρ=0.7 (strong agreement threshold)
```

### 4.3 Heatmap: Concept Jaccard Matrix

```
Rows: Topics (freedom, justice, success, responsibility, home)
Columns: Languages (zh, en, de)
Cell color: Jaccard index (0-1, blue scale)
Cell text: numeric Jaccard value
```

### 4.4 Radar Chart: Centrality Comparison (per topic)

```
For each topic:
  Axes: top 5 concepts by centrality
  Two polygons: human (filled) vs simulation (outline)
  Overlap area = agreement
```

### 4.5 Grouped Bar: LDS Ranking Comparison

```
X-axis: Topics (sorted by human LDS)
Y-axis: LDS value
Groups: human (blue) vs simulation (red)
Error bars: std dev across language pairs
```

---

## 5. Expected Results (Predictions)

Based on existing Wikipedia LDS data and simulation baseline characteristics:

### LDS Correlation
- **Expected ρ**: 0.6–0.8 (moderate-to-strong)
- **Rationale**: LLM persona simulation should capture broad cultural patterns but miss nuanced human-specific associations
- **Risk**: If ρ < 0.4, the simulation baseline is not valid as a comparison standard

### Concept Overlap
- **Expected Jaccard**: 0.3–0.5 (moderate)
- **Rationale**: LLMs use similar vocabulary but may not capture all human-extracted concepts
- **Risk**: If Jaccard < 0.2, the concept mapping system needs revision

### Centrality Ranking
- **Expected τ**: 0.5–0.7 (moderate)
- **Rationale**: Core concepts (freedom, success) should be similarly central; peripheral concepts may differ
- **Risk**: If τ < 0.3, the simulation does not replicate human cognitive priorities

### Graph Structure
- **Expected Edge Jaccard**: 0.2–0.4 (low-to-moderate)
- **Rationale**: Exact edge matches are harder; structural similarity is more realistic
- **Risk**: If Edge Jaccard < 0.1, the relationship extraction is not comparable

---

## 6. Implementation Checklist

- [ ] Run simulation pipeline (`simulate_baseline.py --generate`)
- [ ] Run LDS on simulation data (`simulate_baseline.py --pipeline`)
- [ ] Collect pilot data (9 respondents)
- [ ] Run full pipeline on pilot data
- [ ] Implement comparison script (`compare_human_vs_model.py` — already exists)
- [ ] Generate all 4 visualizations
- [ ] Write results section draft

---

## 7. Files Reference

| File | Role |
|------|------|
| `scripts/compare_human_vs_model.py` | Existing comparison implementation |
| `scripts/simulate_baseline.py` | Simulation data generator |
| `src/scoring.py` | LCD calculation logic |
| `config/cross_language_mapping.json` | Concept mapping for cross-language alignment |
| `data/baseline/computational_baseline.json` | Current simulation data |
| `research/findings/bwki_analysis_report.md` | Current LDS results (Wikipedia only) |
| `data/questionnaires/expected_differences.json` | Hypothesized concept differences |
