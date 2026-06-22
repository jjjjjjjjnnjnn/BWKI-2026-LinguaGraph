# Cognitive Metrics Framework v0.1

> **Date**: 2026-06-21
> **Status**: Draft
> **Scope**: LDS · CDS · HDS
> **Purpose**: Formal definitions for quantifying knowledge structure characteristics

---

## 1. Language Distance Score (LDS)

### 1.1 Definition

LDS quantifies the structural divergence between two language-specific knowledge graphs extracted from the same or comparable content.

Given two graphs G_A = (V_A, E_A) and G_B = (V_B, E_B) representing the same conceptual domain in languages A and B, LDS is a 3-component average:

```
LDS(A, B) = 1 − mean(GED_sim(A, B), Jaccard_node(A, B), Jaccard_edge(A, B))
```

where:
- `GED_sim(A, B)` = normalized Graph Edit Distance similarity ∈ [0, 1], measuring the structural edit cost to transform G_A into G_B
- `Jaccard_node(A, B)` = |V_A ∩ V_B| / |V_A ∪ V_B|, the node set Jaccard coefficient
- `Jaccard_edge(A, B)` = |E_A ∩ E_B| / |E_A ∪ E_B|, the edge set Jaccard coefficient

### 1.2 Properties

| Property | Range | Interpretation |
|----------|-------|---------------|
| Identity | LDS(A, A) = 0 | Same language → no divergence |
| Maximum | LDS(A, B) → 1 | Completely disjoint concept sets |
| Symmetry | LDS(A, B) = LDS(B, A) | Order-independent |
| Triangle inequality | LDS(A, C) ≤ LDS(A, B) + LDS(B, C) | Holds approximately |

### 1.3 Variants

**LDS-Standard** (3-component): Uses GED similarity + node Jaccard + edge Jaccard as above.

**LDS-Jaccard** (node-only): Uses Jaccard coefficient for quick estimation when GED is too expensive:
```
LDS_jaccard(A, B) = 1 − |V_A ∩ V_B| / |V_A ∪ V_B|
```

**LDS-Cosine** (weighted): Uses cosine similarity with concept importance weighting:
```
LDS_cos(A, B) = 1 − Σ_i w_Ai · w_Bi / (√Σ_i w_Ai² · √Σ_i w_Bi²)
```
where w_Xi is the importance weight of concept i in language X.

### 1.4 Validation Results

Computed on CognitiveSpace dataset using the 3-component LDS formula (574 concepts, 317 ZH + 374 EN + 323 DE with labels):

| Language Pair | Shared Concepts | LDS | Interpretation |
|--------------|----------------|-----|----------------|
| ZH–EN | 229 | **0.5043** | Moderate divergence—different curriculum traditions |
| ZH–DE | 229 | **0.4428** | Lower divergence than ZH–EN (surprising, needs investigation) |
| EN–DE | 229 | **0.5107** | Highest divergence—despite shared European mathematical tradition |

**Key finding**: All three language pairs show LDS values around 0.44–0.51, indicating substantial cross-language structural divergence despite identical mathematical content. This supports the core hypothesis: language and curriculum traditions shape knowledge organization independently of mathematical truth. The ZH–DE pair showing lower LDS than ZH–EN is a notable result that warrants further investigation—possibly reflecting structural similarities between Chinese and German curriculum design.

---

## 2. Concept Density Score (CDS)

### 2.1 Definition

CDS measures how densely interconnected concepts are within a knowledge graph. Higher density indicates a more tightly integrated knowledge structure.

Given a graph G = (V, E) with |V| = n nodes and |E| = m edges:

```
CDS(G) = 2m / (n × (n − 1))
```

This is the standard graph density formula: the ratio of actual edges to maximum possible edges in an undirected graph.

### 2.2 Properties

| Property | Range | Interpretation |
|----------|-------|---------------|
| Minimum | CDS = 0 | No connections (isolated concepts) |
| Maximum | CDS = 1 | Complete graph (every concept connects to every other) |
| Scale-free | Not directly | Large graphs naturally have lower density |

### 2.3 Normalization

For comparing graphs of different sizes, use normalized CDS:

```
CDS_norm(G) = CDS(G) / CDS_ref
```

where CDS_ref is the density of a reference corpus at the same education level.

### 2.4 Validation Results

Computed on CognitiveSpace dataset (574 concepts, 3538 relations, 68 textbooks):

| Level | Nodes | Internal Edges | CDS |
|-------|-------|---------------|-----|
| Elementary | 37 | 145 | **0.2177** |
| Middle | 46 | 280 | **0.2705** |
| High | 193 | 1,116 | **0.0602** |
| College | 298 | 1,845 | **0.0417** |

**Key finding**: CDS **decreases** with education level. This contradicts the naive expectation that "advanced knowledge is denser." The actual pattern reflects a fundamental property of knowledge organization: foundational knowledge (elementary, middle) forms a tightly interconnected core, while advanced knowledge (high, college) expands into specialized branches that are more sparsely connected to each other. The dramatic drop from middle (CDS=0.27) to high (CDS=0.06) corresponds to the explosion in concept count (46→193) as mathematics diversifies into algebra, geometry, calculus, probability, etc.

### 2.5 Validation

| Test | Method | Expected | Status |
|------|--------|----------|--------|
| Level discrimination | CDS(elementary) vs CDS(college) | CDS increases with level | ⏳ |
| Language invariance | CDS(ZH) vs CDS(DE) for same level | Similar CDS for same domain | ⏳ |
| Domain specificity | CDS(math) vs CDS(physics) | Different domains → different CDS | ⏳ |

---

## 3. Hierarchy Depth Score (HDS)

### 3.1 Definition

HDS measures how deeply knowledge is organized hierarchically. A high HDS indicates a structure where concepts build on prerequisites in a deep chain; a low HDS indicates a flat, associative structure.

Given a directed graph G = (V, E) where edges A → B mean "A depends on B" or "B is prerequisite for A":

```
HDS(G) = max_{v ∈ V} depth(v)
```

where depth(v) is the length of the longest directed path ending at v, computed via topological sorting or BFS from root nodes (nodes with no prerequisites).

### 3.2 Variant: Mean HDS

For a more robust measure that is less sensitive to outliers:

```
HDS_mean(G) = (1/|V|) × Σ_{v ∈ V} depth(v)
```

### 3.3 Variant: Normalized HDS

To compare across graph sizes:

```
HDS_norm(G) = HDS(G) / log₂(|V|)
```

### 3.4 Properties

| Property | Range | Interpretation |
|----------|-------|---------------|
| Minimum | HDS = 0 | No hierarchical structure |
| Maximum | HDS ≤ n − 1 | Single chain (theoretical max) |
| Robust | HDS_mean more stable | Less sensitive to outliers |

### 3.5 Validation Results

Computed on CognitiveSpace dataset (574 nodes, 275 directed prerequisite/requires edges):

| Metric | Value | Interpretation |
|--------|-------|---------------|
| HDS (max) | **5** | Longest dependency chain spans 5 concepts |
| HDS (mean) | **0.34** | Most concepts have shallow (0–1) prerequisite depth |
| Nodes with hierarchy | 107 / 574 | 18.6% of concepts participate in dependency chains |

**Key finding**: The CognitiveSpace graph exhibits a relatively shallow hierarchy (max depth 5, mean 0.34). This reflects the nature of mathematics—concepts at the same level are more often related laterally (related_to) than hierarchically (prerequisite). The deep chains tend to follow cross-level dependencies (e.g., elementary arithmetic → middle algebra → high calculus).

### 3.6 Validation

| Test | Method | Expected | Status |
|------|--------|----------|--------|
| Level discrimination | HDS(elementary) vs HDS(college) | HDS increases with level | ⏳ |
| Curriculum comparison | HDS(ZH) vs HDS(DE) for calculus | Different curricula→different depth | ⏳ |
| Chain interpretation | Manual inspection of deepest paths | Paths correspond to real learning progressions | ⏳ |

---

## 4. Combined Framework

### 4.1 Knowledge Structure Profile

Each text produces a three-dimensional profile:

```
KSP(text) = (CDS, HDS, LDS)
```

This profile characterizes how knowledge is organized in the text along three independent axes:

- **CDS**: How densely connected (integration)
- **HDS**: How hierarchically structured (depth)
- **LDS**: How language-specific (divergence)

### 4.2 Interpretation Guide

| CDS | HDS | LDS | Implication |
|-----|-----|-----|-------------|
| High | High | High | Dense, deep, language-specific structure |
| High | Low | Low | Broad survey, many connections, shallow |
| Low | High | Medium | Focused, deep, moderately divergent |
| Low | Low | Low | Simple, universal content |

---

## 5. Implementation Plan

### 5.1 Data Sources

All three metrics can be computed from the existing CognitiveSpace graph data (574 nodes, 3538 edges). No new data collection needed.

### 5.2 Computation

| Metric | Data Required | Algorithm | Status |
|--------|--------------|-----------|--------|
| LDS | Multi-language graph pairs | 3-component mean(GED_sim, Jaccard_node, Jaccard_edge) | ✅ Formula defined |
| CDS | Node/edge counts | Graph density formula | ✅ Formula defined |
| HDS | Directed edge structure | Longest path via BFS | ✅ Formula defined |

### 5.3 Next Steps

1. Compute CDS and HDS for the full CognitiveSpace graph
2. Compute CDS and HDS per education level (elementary, middle, high, college)
3. Compute LDS per language pair (ZH-EN, ZH-DE, EN-DE)
4. Verify metrics discriminate between known-different texts
5. Integrate into Workbench analysis dashboard
