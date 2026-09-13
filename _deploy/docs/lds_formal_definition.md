# LDS — Formal Definition, Variants, and Null Hypothesis Framework

> LinguaGraph Core Metric Specification v2.0
> Purpose: Define LDS-K, LDS-C, ΔLDS, and their null model falsification framework for paper-level rigor.

---

## 1. LDS Core Definition

**Linguistic Divergence Score (LDS)** measures the structural dissimilarity between two knowledge graphs expressed in different languages.

### 1.1 Formal Definition

Given two graphs \(G_a = (V_a, E_a)\) and \(G_b = (V_b, E_b)\) representing the same knowledge domain expressed in languages \(L_a\) and \(L_b\):

\[
\text{LDS}(G_a, G_b) = 1 - \frac{J(V_a, V_b) + J(E_a, E_b)}{2}
\]

where \(J(X, Y) = \frac{|X \cap Y|}{|X \cup Y|}\) is the Jaccard similarity coefficient.

**Properties**:
- **Range**: \(0 \leq \text{LDS} \leq 1\)
- **LDS = 0**: Identical node sets AND identical edge sets (complete structural identity)
- **LDS = 1**: Zero overlap in both nodes and edges (complete structural divergence)
- **Symmetry**: \(\text{LDS}(G_a, G_b) = \text{LDS}(G_b, G_a)\)

### 1.2 Component Interpretation

| Component | Meaning | Example |
|-----------|---------|---------|
| \(J(V_a, V_b)\) | Concept-level overlap — **what** is taught | If both graphs contain "derivative/Ableitung/导数", node Jaccard is high |
| \(J(E_a, E_b)\) | Relation-level overlap — **how** concepts are connected | If both graphs link "derivative → limit" in the same way, edge Jaccard is high |
| \(1 - \text{mean}(J_v, J_e)\) | Structural divergence — the complement of mean overlap | LDS=0.9 means 90% of possible concepts/relations are different |

### 1.3 Node Alignment

LDS requires cross-language node alignment: concept \(v_i \in V_a\) mapped to \(v_j \in V_b\) via shared concept group ID in `aligned_data.json`. Unaligned concepts contribute to the union but never the intersection.

---

## 2. LDS Variants

### 2.1 LDS-K (Knowledge LDS)

**Definition**: LDS computed on **textbook-derived knowledge graphs** — expert/LLM-extracted concept structures from educational materials (math, physics, chemistry textbooks).

**Data source**: `config/expert_graphs/` + `data/math_extractions/merged/aligned_data.json`

**Interpretation**: Measures structural divergence in **institutional knowledge** — how educational systems organize the same body of knowledge.

**Key finding**: LDS-K ≈ Structure Null LDS for ZH-EN and DE-EN. This means textbook knowledge structures are **more similar than expected by chance under degree-preserving randomization**.

| Pair | LDS-K | Structure Null | Interpretation |
|------|:-----:|:-------------:|----------------|
| ZH-EN | 0.934 | 0.957 | Structure dominates (real MORE similar) |
| DE-EN | 0.938 | 0.957 | Structure dominates (real MORE similar) |
| ZH-DE | 0.519 | 0.717 | Real more similar than null |

**Scientific implication**: LDS-K **does NOT measure language-driven cognitive divergence**. It primarily reflects:
1. The inherent structure of the knowledge domain (mathematical prerequisites are universal)
2. Degree distribution of the concept graph
3. Textbook authoring conventions within an educational system

### 2.2 LDS-C (Cognitive LDS)

**Definition**: LDS computed on **human-generated knowledge graphs** — concept structures extracted from questionnaire responses where participants express their understanding of a topic in their native language.

**Data source**: Human questionnaire data → LLM extraction → graph construction (N ≥ 30 participants, within-subject design)

**Interpretation**: Measures structural divergence in **spontaneous cognitive expression** — how humans from different language communities organize the same concepts when freely expressing their understanding.

**Expected property**: LDS-C > LDS-K, because:
1. Textbook knowledge is constrained by universal mathematical truth
2. Human expression is influenced by language-specific framing, cultural metaphors, and individual cognitive styles

**Status**: ✅ Computed (2026-08-08). Human N=15 between-subject: LDS-C 0.93–0.96 ≈ noise floor (null — design artifact, see §6.2). LLM-as-Subject within-subject (D1): LDS-C 0.93–0.96 ≫ floor 0.85–0.87 (signal present). See `docs/session_handoff_20260808.md`.

> **Presence-only metric (audit M16)**: LDS-C counts concept *presence* (union-deduplicated) — a concept mentioned once or ten times contributes equally to the Jaccard. Frequency weighting is NOT part of the frozen metric; it is only used in the divergence-driver analysis (`lds_c_divergence_drivers.py`). This is a deliberate design choice: LDS-C measures structural divergence of the expressed concept *set*, not salience.

### 2.3 ΔLDS (Delta LDS)

**Definition**:

\[
\Delta\text{LDS} = \text{LDS}_C - \text{LDS}_K
\]

**Interpretation**: The **language-driven cognitive divergence** — the additional structural difference introduced by human cognitive expression beyond what textbook structure alone predicts.

**Expected relationship**: ΔLDS > 0 if language affects how humans organize and express knowledge beyond how textbooks organize it.

**Core scientific claim**: ΔLDS > 0 and statistically significant → evidence for **linguistic relativity in knowledge organization**: language influences not what people can know (the universal mathematical truth), but **how they express, connect, and frame** what they know.

---

## 3. Null Hypothesis Framework

### 3.1 Why Null Models?

LDS alone cannot distinguish between:
- **Language-driven divergence** (the phenomenon we claim to measure)
- **Structural artifacts** (differences driven by graph topology, degree distribution, or extraction noise)

Null models destroy the hypothesized signal while preserving structural properties, allowing us to test: **is the observed LDS different from what we would expect if only structure (not language) mattered?**

### 3.2 The Three Null Models

| Null Model | What It Preserves | What It Destroys | Tests |
|------------|-------------------|------------------|-------|
| **Structure Null** | Degree distribution (double-edge swap rewiring) | Edge identity (which specific concepts are connected) | Does degree structure alone explain LDS? |
| **Node-Permuted Null** | Graph topology, group alignment | Label-to-concept assignments | Do specific concept-label assignments carry language signal? |
| **Complete Random** | N, E (Erdős–Rényi with same node/edge counts) | Everything (topology, labels, degree) | Is LDS > 0 at all? (sanity check) |

### 3.3 Structure Null (Degree-Preserving Rewiring)

**Method**: Double-edge swap algorithm.

```
For each language graph G_l = (V_l, E_l):
    1. Select two edges (a,b) and (c,d) where a,b,c,d are all distinct
    2. Swap endpoints to create (a,d) and (c,b)
    3. Repeat 1000 times (ensures thorough mixing)
    4. Verify no self-loops or parallel edges created
    5. Result: graph G'_l with same degree sequence, randomized edge identity
```

Then compute LDS(G'_a, G'_b) and compare to LDS(G_a, G_b).

**H0**: LDS(G_a, G_b) > LDS(G'_a, G'_b) — real graphs are MORE divergent than degree-randomized graphs (language signal exists).

**Rejection**: If LDS(G_a, G_b) ≤ LDS(G'_a, G'_b), the observed LDS is **fully explained by degree distribution** — no evidence for language-driven structure.

**Actual result**: H0 rejected for all language pairs. Real graphs are **more similar** than degree-randomized graphs.

### 3.4 Node-Permuted Null

**Method**:
```
For each concept group with labels (zh_label, en_label, de_label):
    1. Collect all label triples
    2. Randomly permute labels within each language column
    3. This preserves: graph topology, concept count per group
    4. This destroys: semantic relationship between labels and graph position
```

**H0**: Permuting labels changes LDS (specific label assignments carry signal).

**Actual result**: Node-permuted LDS = Full LDS for all pairs. This is expected because permuting labels **within already-aligned concept groups** doesn't change the graph — it merely swaps which label is assigned to which group, and since both sides swap together, the Jaccard similarity is unchanged.

### 3.5 Complete Random Null

**Method**: Erdős–Rényi random graph with same N nodes and E edges per language.

**H0**: Any graph structure with these parameters produces similar LDS (LDS is meaningless).

**Actual result**: LDS = 1.0000 (complete divergence), confirming that real graphs have meaningful structure.

### 3.6 Cross-Source Null (Proposed, Not Yet Implemented)

Compares LDS across **different knowledge sources** (e.g., textbook vs Wikipedia) for the same topic in the same language. This tests whether LDS measures source-specific structure rather than language-specific structure.

| Comparison | Meaning |
|------------|---------|
| \( \text{LDS}(G^{textbook}_{zh}, G^{wikipedia}_{zh}) \) | Source divergence within ZH |
| \( \text{LDS}(G^{textbook}_{en}, G^{wikipedia}_{en}) \) | Source divergence within EN |

If intra-language source divergence ≈ inter-language textbook divergence, then LDS is primarily a **source metric**, not a language metric.

---

## 4. Wikipedia Negative Control

### 4.1 Method

Extract concept graphs from ZH/EN/DE Wikipedia articles on 5 social topics (Freedom, Justice, Responsibility, Home, Success) using the same LLM (qwen-plus) and the same extraction prompt.

### 4.2 Result (revised 2026-08-08)

**Early (unaligned) analysis reported LDS = 1.0000** — this was an **alignment artifact**: Chinese concepts (e.g. 自由) reduce to empty keys under `canonical_key` (Latin-only), so ZH contributed nothing to the intersection.

**After glossing 96 unique ZH+DE concepts to English** (`scripts/lds_k_wiki_gloss.py`) and aligning all three languages in the same canonical key space, real LDS values emerge:

| Quelle | ZH-EN | DE-EN | ZH-DE |
|:------|:-----:|:-----:|:-----:|
| Wikipedia (sozial, aligniert) | 0.698 | 0.723 | **0.819** |
| Mathematik-Lehrbücher (zum Vergleich) | 0.934 | 0.938 | **0.519** |

### 4.3 Interpretation (revised)

1. The earlier LDS=1.0 was **not** evidence of structural difference — it was a zero-alignment artifact (Latin-only canonical keys dropped all Chinese concepts).
2. The aligned values reveal a **reversed pattern vs. institutional knowledge**: in the social domain ZH-DE is the **most divergent** pair (0.82), whereas in mathematics it is the most convergent (0.52).
3. This supports the interpretation that **institutional knowledge (universal logic) masks language effects, while social/cultural concepts let language structure through** — consistent with the LLM-as-Subject within-subject finding.
4. The textbook LDS values (0.52–0.94) remain genuine: the cross-source comparison (textbook-math vs. wiki-social, LDS=1.0) is confounded by domain (math ⊥ social), not by language.

---

## 5. Scientific Claim Chain

```
Axiom 1: Mathematical truth is universal
  → If knowledge organization were purely truth-driven, graphs would be identical
  → LDS would be 0

Axiom 2: Educational systems impose structure on knowledge
  → Different systems organize the same truth differently
  → LDS-K captures the divergence of institutional cognition

Axiom 3: Language influences cognitive expression
  → Humans from different language communities express and connect concepts differently
  → LDS-C captures spontaneous cognitive expression divergence

Claim 1: LDS-K is dominated by structural factors (degree distribution)
  → Evidence: Structure Null > Full LDS for all pairs

Claim 2: LDS-C should exceed LDS-K
  → Hypothesis: Human expression is less constrained than textbook authoring
  → Evidence: Pending (N ≥ 30 required)

Claim 3: ΔLDS > 0 → language-driven cognitive divergence exists
  → Core scientific contribution of LinguaGraph
  → Pending (requires LDS-C computation)
```

---

## 6. Falsification Conditions

Each condition, if met, would **falsify** the corresponding claim:

| Claim | Falsification Condition | Test |
|-------|------------------------|------|
| LDS-K measures language divergence | Structure Null ≥ Full LDS | ✅ Tested → **Falsified** |
| LDS-C > LDS-K | LDS-C ≤ LDS-K (ΔLDS ≤ 0) | ⏳ Human N=15 (between): not detected; LLM within-subject: signal present |
| Wikipedia LDS < 1.0 | Aligned social concepts show real structure | ✅ Tested → **Confirmed after alignment** (ZH-EN 0.70, DE-EN 0.72, ZH-DE 0.82); earlier 1.0 was an alignment artifact |
| LDS is robust to model choice | Different models produce different LDS ranking | ⚠️ Partially tested (data quality issues) |
| LDS is robust to source | Intra-source LDS ≈ Inter-source LDS | ⚠️ Tested → source is a strong driver (wiki-vs-human = 0.94, domain-clean), but language effect independent (LLM within-subject) |

### 6.1 Adversarial Null Models (Added per Reviewer Feedback)

These null models are designed to **threaten** the interpretation, not support it:

| Null Model | What It Tests | Threat Level | Result |
|------------|---------------|:------------:|--------|
| **Within-language split-half** | Random split of one language's graph → establishes noise floor | **High** — if cross-lang LDS ≈ within-lang LDS, language signal is noise | Within-lang LDS = 0.96-0.97. ZH-EN (0.93) and DE-EN (0.94) near floor; ZH-DE (0.52) **far below** → convergence confirmed |
| **Monolingual control** | LDS between two halves of same language (separate "textbooks") | **High** — directly tests if cross-lang > same-lang variation | Same-lang LDS = 0.96-0.97. Cross-lang ZH-DE (0.52) far lower → **genuine convergence** |
| **Language-label permutation** | Randomly reassign language labels at group level | **Medium** — tests if label assignments carry signal | Permuted LDS (0.67-0.87) differs from Full LDS (0.52-0.94) → label assignments DO carry signal |

> **注（层级差异）**: §6.1 的 Language-label permutation 是**分组级**置换（重新分配语言标签到响应/组），与 §3.4 的 Node-Permuted Null（**组内**置换对齐组标签，不改变图）是**不同层级**的空模型，结论因此不同——前者保留图结构、破坏语言-响应对应；后者不改变图本身。二者不矛盾。

**Interpretation**: The within-language baseline (LDS ≈ 0.97) represents the metric's noise floor — even within the same language, randomly splitting a graph produces substantial divergence. Against this baseline:
- ZH-DE LDS = 0.52 → **far below noise floor** (strong evidence for structural convergence)
- ZH-EN LDS = 0.93 → **near noise floor** (typical divergence)
- DE-EN LDS = 0.94 → **near noise floor** (typical divergence)

This strengthens the conclusion that LDS-K measures structural convergence, not divergence. The ZH-DE pair is genuinely special — Chinese and German mathematics textbooks converge to a degree that within-language textbook random splits do not.

### 6.2 Design-Effect Proof (Added 2026-08-08, LLM-as-Subject extension)

The human N=15 between-subject null (§6 row 2) raises the question: is it "no language effect" or a design artifact? A within-subject design using a multilingual LLM as a controlled subject resolves this, and a follow-up decomposition (`scripts/lds_c_design_effect.py`) makes the artifact quantitative:

| Observation | Human (between, N=15) | LLM (within, k=10) |
|------------|:---:|:---:|
| LDS-C (pooled, all pairs) | 0.93–0.96 | 0.93–0.96 |
| Within-language split-half floor | 0.92–0.96 | 0.85–0.87 |
| signal/floor ratio | **≈ 1.00 (submerged)** | **≈ 1.09–1.10 (visible)** |

**Interpretation**:
1. **The cross-language divergence magnitude is identical** in humans and the LLM (LDS-C 0.93–0.96 both) — the human null is NOT "language has no effect".
2. The difference is the **noise floor**: human within-language participant heterogeneity (0.92–0.96) matches the signal, submerging it; LLM sampling of the same weights is homogeneous (0.85–0.87), revealing it.
3. **Not a sample-size effect**: the LLM signal survives even at N=3 per language (margin +0.02–0.04); it is not an N≥10 artifact.
4. **Decisive control**: analyzing the LLM samples with the *exact human between-subject pipeline* at human N (=6/language) still detects the signal (margin +0.06–0.07) — so neither "no effect" nor "between-subject design per se" explains the null. The decisive variance source is **individual heterogeneity within a language group**, which a within-subject design (or a homogeneous subject like an LLM) eliminates.

**Falsification framing**: the claim "human between-subject null ⇒ no language-driven cognitive divergence" is **falsified** by the design-effect proof: the same metric, same prompts, same extraction produce the null under between-subject human data and a positive under within-subject controlled data, and the signal magnitude is equal.

### 6.3 Node/Edge Decomposition of the Reversal (Added 2026-08-08)

The social/institutional ZH-DE reversal (§4) is decomposed into node vs edge components (`scripts/lds_c_node_edge_decomp.py`):

| Source | Pair | node-only LDS | edge contribution |
|:---|:---:|:---:|:---:|
| Math (institutional) | ZH-DE | 0.444 | **0.074** |
| Wikipedia social | ZH-DE | **0.800** | 0.019 |
| Human cognitive | ZH-DE | 0.915 | 0.038 |

**Interpretation**: The reversal (math convergent vs social divergent for ZH-DE) is **node-driven** (concept choice), not edge-driven: institutional knowledge converges on *which* concepts are taught (J_node 0.556) while relational organization (J_edge 0.407) still diverges substantially. The edge contribution is *largest* in math — i.e., within an institutionally convergent domain, the relation structure is the residual divergent component. This separates "concept selection" from "relational structure" as distinct mechanisms, consistent with the M2 (lexical-associative) dominance in the LLM within-subject analysis (§5.6).

---

## 7. Statistical Appendix

### 7.1 Bootstrap Confidence Intervals for LDS

LDS is a deterministic function of two graphs, but its statistical properties can be estimated via bootstrap resampling:

```python
import random, statistics

def bootstrap_lds_ci(nodes_a, nodes_b, edges_a, edges_b,
                     n_iterations=1000, ci_level=0.95) -> dict:
    """Bootstrap estimate of LDS confidence interval.

    Resamples concepts (nodes) WITH REPLACEMENT within each language,
    recomputing LDS each time. Returns percentile CI.
    """
    lds_values = []
    for _ in range(n_iterations):
        # Resample nodes with replacement
        samp_a = [random.choice(nodes_a) for _ in range(len(nodes_a))]
        samp_b = [random.choice(nodes_b) for _ in range(len(nodes_b))]
        # Resample edges with replacement
        ea_list = list(edges_a)
        eb_list = list(edges_b)
        samp_ea = [random.choice(ea_list) for _ in range(len(ea_list))]
        samp_eb = [random.choice(eb_list) for _ in range(len(eb_list))]
        lds = lds_jaccard(samp_a, samp_b, samp_ea, samp_eb)
        lds_values.append(lds["lds_score"])

    lds_values.sort()
    lower_idx = int((1 - ci_level) / 2 * n_iterations)
    upper_idx = int((1 + ci_level) / 2 * n_iterations)
    return {
        "mean": round(statistics.mean(lds_values), 4),
        "ci_lower": round(lds_values[lower_idx], 4),
        "ci_upper": round(lds_values[upper_idx], 4),
        "std": round(statistics.stdev(lds_values), 4),
    }
```

### 7.2 Effect Size: Cohen's d for LDS Comparisons

When comparing LDS between two conditions (e.g., LDS-C vs LDS-K, or human vs simulation):

\[
d = \frac{\bar{x}_1 - \bar{x}_2}{s_{pooled}}, \quad
s_{pooled} = \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1 + n_2 - 2}}
\]

Interpretation thresholds:
| Cohen's d | Interpretation |
|:---------:|---------------|
| 0.0–0.2 | Negligible |
| 0.2–0.5 | Small |
| 0.5–0.8 | Medium |
| 0.8+ | Large |

For the LLM within-subject signal (D1: LDS-C 0.93–0.96 vs floor 0.85–0.87, margin ≈ +0.08):
- Between-subject human study: the within-language floor (0.92–0.96) already equals
  the cross-language signal → a between-subject design has **negligible power to
  separate language from participant heterogeneity** (this is the design-effect
  proof, §6.2). The LLM signal survives a between-subject lens only because LLM
  samples are homogeneous.
- Within-subject design (required): N ≈ 10 matched samples per language detects
  the +0.08 margin at high power (the D1 k=10 design does so; permutation p<0.01).

### 7.3 Multiple Comparison Correction

When testing multiple language pairs (ZH-EN, DE-EN, ZH-DE) simultaneously:

**Bonferroni correction**: Divide α by number of comparisons.
- 3 language pairs → α_adj = 0.05 / 3 = 0.0167

**Holm-Bonferroni (less conservative)**:
```
1. Sort p-values ascending: p₁ ≤ p₂ ≤ p₃
2. Reject H₁ if p₁ < 0.05/3
3. Reject H₂ if p₂ < 0.05/2
4. Reject H₃ if p₃ < 0.05/1
```

### 7.4 Sensitivity Analysis Plan

To test whether LDS findings are robust to methodological choices:

| Parameter | Default | Sensitivity Range |
|-----------|---------|-------------------|
| Extraction model | qwen-plus | All 19 benchmark models (F1 0.55-0.67) |
| Node alignment | Group IDs | Relaxed (synonym match) / Strict (exact match) |
| Edge direction | Directed | Undirected (ignore direction) |
| Jaccard threshold | 2-overlap | 1-overlap / 3-overlap |
| Graph size | Full | Minimum 10 concepts per language |

### 7.5 Power Analysis for Human Study

Based on the D1 within-subject signal (2026-08-08; supersedes the N=8 pilot):

| Design | Effect | N needed (80% power, α=0.05) |
|--------|:------:|:------------------------------:|
| Between-subject human (language × participant confounded) | margin +0.08 but floor ≈ signal | **Infeasible** (floor already equals signal; §6.2) |
| Within-subject (matched, e.g. bilinguals or repeated) | margin +0.08, floor 0.85–0.87 | ≈ 10 samples/language (D1 k=10 achieves p<0.01) |

**Recommendation**: Any human follow-up must use a **within-subject design** (bilinguals answering both languages, or repeated measures); the D1 LLM experiment provides the expected effect direction and magnitude. See `docs/session_handoff_20260808.md` §3.6 for the design-effect proof.

### 7.6 Statistical Reporting Template

For the final paper, each LDS finding should report:

```text
LDS(ZH-EN) = 0.934 [95% CI: 0.891, 0.967], n = 219 aligned groups
ΔLDS = +0.080, 95% CI: [+0.012, +0.148], d = 0.82, p = 0.050
Bonferroni-adjusted α = 0.0167 (3 comparisons)
```

---

## 8. Implementation

### 8.1 LDS Computation (Standard)

```python
# Inline Jaccard-only LDS (no networkx dependency needed)
def lds_jaccard(nodes_a, nodes_b, edges_a, edges_b):
    set_a, set_b = set(nodes_a), set(nodes_b)
    node_jac = len(set_a & set_b) / max(len(set_a | set_b), 1)
    edge_jac = len(set(edges_a) & set(edges_b)) / max(len(set(edges_a) | set(edges_b)), 1)
    lds = 1.0 - (node_jac + edge_jac) / 2
    return {"lds_score": round(lds, 4), "jaccard_node": round(node_jac, 4), "jaccard_edge": round(edge_jac, 4)}
```

### 8.2 Structure Null Implementation

```python
def degree_preserving_rewire(edges, n_swaps=1000):
    """Double-edge swap: preserves degree sequence."""
    edge_list = list(edges)
    for _ in range(n_swaps):
        i, j = random.randrange(len(edge_list)), random.randrange(len(edge_list))
        if i == j: continue
        a, b = edge_list[i]; c, d = edge_list[j]
        if len({a, b, c, d}) < 4: continue  # Need 4 distinct nodes
        if a == d or b == c: continue         # No self-loops
        if (a, d) in edge_list or (c, b) in edge_list: continue  # No parallel edges
        edge_list[i] = (a, d); edge_list[j] = (c, b)
    return edge_list
```

### 8.3 Script Reference

| Script | Function |
|--------|----------|
| `scripts/figures/fig4_null_model.py` | LDS-K + 4 null models |
| `scripts/figures/fig1_lds_k_heatmap.py` | Domain-level LDS-K |
| `scripts/figures/fig5_falsification.py` | Language swap + graph permutation + model comparison |
| `scripts/figures/fig_wikipedia_lds.py` | Wikipedia social concept LDS (negative control) |

---

*LDS Formal Definition v3.0 | 2026-06-30 | LinguaGraph Core Metric Specification*
