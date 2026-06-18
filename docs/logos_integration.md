# LinguaGraph × LOGOS — Methodological Integration Plan

> **Status:** Planning Phase · **Priority:** Low (BWKI), Medium (Post-BWKI)
>
> **Date:** 2026-06-18 · **Reference:** arXiv:2509.24294 (LOGOS: LLM-driven Grounded Theory)

---

## 1. What We Borrow from LOGOS

We adopt **three methodological concepts** from LOGOS. We do NOT borrow code, models, or architecture.

| LOGOS Concept | LinguaGraph Adaptation | Scope |
|:--------------|:-----------------------|:-----:|
| **Semantic Clustering** of codes | Concept Canonicalization Layer (embedding-based dedup) | ~50 LOC |
| **Reusable Codebook** | LinguaGraph Concept Taxonomy v1 (hierarchical) | One config file |
| **Schema-Level Alignment** | Cluster-level cross-language comparison | Add-on analysis |

### What We Do NOT Borrow

| LOGOS Feature | Decision | Reason |
|:--------------|:--------:|:-------|
| End-to-end grounded theory | ❌ Skip | Out of scope for cognitive graph comparison |
| Iterative refinement loop | ❌ Skip | Requires human-in-the-loop, delays BWKI |
| Graph reasoning for theory induction | ❌ Skip | LDS is frozen — no metric changes |
| Full automation of qualitative coding | ❌ Skip | We already have extraction + graph pipeline |
| 5-dimensional evaluation metric | ❌ Skip | LDS + bootstrap CI is our validated metric |

---

## 2. Integration #1: Concept Canonicalization Layer

### Problem

Currently, `normalize_concepts()` only handles **known synonym pairs** from a static map:

```python
# Current: extract.py → normalize_concepts()
norm_map = {
    "demokratisches System": "Demokratie",  # Only if manually listed
    "民主制度": "民主",
}
```

If a German answer uses `"demokratische Teilhabe"` (democratic participation) and the English answer uses `"democratic engagement"`, the current system treats them as **unrelated concepts**, inflating LDS artificially.

### Solution

Insert a **canonicalization step** between extraction and graph building:

```text
Before:            After:

extraction         extraction
   ↓                   ↓
normalize()      normalize()
   ↓                   ↓
   ───           canonicalize()    ← NEW (~50 LOC)
   ↓                   ↓
graph build        graph build
```

### Design

```
scripts/canonicalize.py (or src/canonicalize.py)
┌─────────────────────────────────────────────────────┐
│ Input:  [concept1, concept2, ...]                   │
│                                                      │
│ 1. Embed each concept using sentence-transformers   │
│ 2. Cluster by cosine similarity (threshold >= 0.85) │
│ 3. Map cluster → canonical label                    │
│     (prefer: existing concept ID from mapping)       │
│ 4. Output: [canonical_concept1, canonical_concept2]  │
│                                                      │
│ Config: config/normalization_map.json (extended)     │
└─────────────────────────────────────────────────────┘
```

### Canonicalization Strategy (3-level)

| Level | Method | Quality | Speed | Dependency |
|:-----:|:-------|:-------:|:-----:|:----------:|
| 1 | **Static map** (current) | ★★ | ⚡ Instant | None |
| 2 | **String similarity** (Levenshtein) | ★★★ | ⚡ Instant | `thefuzz` |
| 3 | **Embedding similarity** (sentence-BERT) | ★★★★ | 🐢 ~50ms/concept | `sentence-transformers` |

**Default: Level 1+2 (no new dependencies).**
Level 3 is optional — enabled only when `sentence-transformers` is installed.

### Implementation Sketch

```python
# src/canonicalize.py
def canonicalize_concepts(
    concepts: List[str],
    language: str,
    concept_mapping: Dict[str, str],
    use_embeddings: bool = False
) -> List[str]:
    """
    Canonicalize extracted concepts to canonical labels.
    
    1. Try concept_mapping lookup (exact/fuzzy)
    2. Try static norm_map lookup
    3. Try Levenshtein similarity to known concepts
    4. (Optional) Try embedding clustering
    
    Returns canonicalized concept list.
    """
    ...
```

### Integration Point

In `scripts/analyze_student.py` and any pipeline code that calls `build_graph()`:

```python
# Before:
concepts = extracted.get("concepts", [])
G = build_graph({"concepts": concepts, "relations": ...})

# After:
from src.canonicalize import canonicalize_concepts
concepts = extracted.get("concepts", [])
canonical = canonicalize_concepts(concepts, language=lang, concept_mapping=mapping)
G = build_graph({"concepts": canonical, "relations": ...})
```

No other module changes. LDS, graph.py, cross_language.py — all untouched.

### Validation

```
Baseline (no canonicalization) vs Level 2 vs Level 3:
- LDS variance across language pairs
- Concept F1 against gold labels
- Number of unique concepts per language
```

---

## 3. Integration #2: LinguaGraph Concept Taxonomy v1

### Problem

The 30 concept IDs in `config/cross_language_mapping.json` are flat. There's no hierarchical organization. When a reviewer asks "why these concepts and not others?", we need a structured answer.

### Solution

Create a **hierarchical concept taxonomy** as a config file:

```text
config/
├── cross_language_mapping.json    (existing — 30 flat concept IDs)
└── concept_taxonomy.json          (NEW — hierarchical)
```

### Taxonomy Structure

```json
{
  "version": "1.0",
  "domain": "social_issues",
  "clusters": [
    {
      "id": "governance",
      "label": {"zh": "治理", "de": "Staat & Politik", "en": "Governance & Politics"},
      "description": {"zh": "与政治体制和治理相关的概念", "de": "Konzepte zu politischen Systemen", "en": "Concepts related to political systems and governance"},
      "concepts": ["democracy", "law", "rights", "power", "revolution", "liberalism", "socialism"]
    },
    {
      "id": "individual",
      "label": {"zh": "个人与自由", "de": "Individuum & Freiheit", "en": "Individual & Freedom"},
      "concepts": ["freedom", "individual", "choice", "autonomy", "free_will", "liberation"]
    },
    {
      "id": "society",
      "label": {"zh": "社会与集体", "de": "Gesellschaft & Kollektiv", "en": "Society & Collective"},
      "concepts": ["society", "equality", "justice", "responsibility", "security"]
    },
    {
      "id": "culture",
      "label": {"zh": "文化与价值观", "de": "Kultur & Werte", "en": "Culture & Values"},
      "concepts": ["religion", "philosophy", "history", "tradition", "identity", "education"]
    },
    {
      "id": "economy",
      "label": {"zh": "经济与发展", "de": "Wirtschaft & Entwicklung", "en": "Economy & Development"},
      "concepts": ["economy", "progress", "success", "family"]
    }
  ]
}
```

### Benefits

| Benefit | For Whom | Impact |
|:--------|:---------|:-------|
| Explainable concept selection | BWKI reviewers | ★★★★★ |
| Structured comparison framework | Paper writing | ★★★★ |
| Cluster-level analysis foundation | Future work | ★★★ |
| Easy to validate | Annotators | ★★★ |

### Generation Method (LOGOS-inspired)

We can derive the taxonomy **bottom-up** from our pilot data:

1. Run extraction on all ZH/DE/EN answers (existing corpus)
2. Count co-occurrence of concepts across answers
3. Build a concept co-occurrence matrix
4. Cluster co-occurring concepts → reveals natural groupings
5. Name clusters → taxonomy

This mirrors LOGOS's "coding → clustering → schema" flow, applied to our domain.

---

## 4. Integration #3: Schema-Level Analysis

### Problem

LDS compares individual node/edge sets. But cognitive differences might appear at the **cluster level** (e.g., "German participants emphasize Governance more than Chinese participants") that individual concept overlap doesn't capture.

### Solution

After LDS computation, add a **cluster distribution analysis**:

```text
LDS (node-level)              Schema Analysis (cluster-level)
     │                                │
     ▼                                ▼
  LDS score                    ┌─────────────────────┐
  GED_sim                      │ topic_distribution: │
  jaccard_node                 │   governance: 0.25  │
  jaccard_edge                 │   individual: 0.30  │
                               │   society:    0.20  │
  (unchanged)                  │   culture:    0.15  │
                               │   economy:    0.10  │
                               └─────────────────────┘
                               │ cluster_shift: 0.12  │ (Earth Mover's Distance)
                               └──────────────────────┘
```

### Design

```python
# src/schema_analysis.py (NEW)
def compute_cluster_distribution(
    graph: nx.DiGraph,
    taxonomy: Dict
) -> Dict[str, float]:
    """
    Compute distribution of concepts across clusters.
    
    Returns: {cluster_id: proportion_of_concepts}
    """

def compute_cluster_shift(
    dist_l1: Dict[str, float],
    dist_l2: Dict[str, float],
    method: str = "emd"  # Earth Mover's Distance or JS divergence
) -> float:
    """
    Compute cross-language cluster shift.
    0.0 = identical distribution, 1.0 = completely different.
    """

def generate_schema_report(
    graphs: Dict[str, nx.DiGraph],
    taxonomy: Dict,
    lds_results: Dict
) -> Dict:
    """
    Full schema-level analysis report for one student.
    Combines LDS results with cluster-level findings.
    """
```

### This Is NOT a New Metric

- LDS remains the **primary metric** (frozen)
- Schema analysis is a **diagnostic add-on** for interpretability
- It explains *where* differences come from, not *how much*
- Will be used in Results section to answer: "Which topics show the most cross-language drift?"

---

## 5. Pipeline Integration Summary

### Before (current)

```
Text → extract() → normalize() → build_graph() → LDS()
```

### After (with all 3 additions)

```
Text → extract() → normalize() → canonicalize() → build_graph() → LDS()
                                            │                       │
                                            ↓                       ↓
                                      Taxonomy v1           Schema Analysis
                                      (codebook)            (cluster-level)
```

**Files changed:**
| File | Change | Lines |
|:-----|:-------|:-----:|
| `src/canonicalize.py` | **NEW** — concept canonicalization | ~80 |
| `config/concept_taxonomy.json` | **NEW** — hierarchical taxonomy | ~60 |
| `src/schema_analysis.py` | **NEW** — cluster-level analysis | ~100 |
| `scripts/analyze_student.py` | **EDIT** — add canonicalization call | ~5 |
| `src/extract.py` | **EDIT** — integrate canonicalization | ~3 |

**Files NOT changed:**
- `src/scoring.py` — LDS frozen
- `src/graph.py` — untouched
- `src/cross_language.py` — untouched
- `src/providers/` — untouched

---

## 6. Timeline & Priority

### When to Build Each Component

| Component | Effort | Dependency | Suggested Timing | BWKI Impact |
|:----------|:------:|:-----------|:----------------:|:-----------:|
| Concept Canonicalization | 2-3 hours | Gold data | **After Pilot** | ★★★ |
| Concept Taxonomy v1 | 1-2 hours | Existing mapping | **Anytime** | ★★★★★ |
| Schema-Level Analysis | 3-4 hours | Taxonomy v1 | **After Pilot** | ★★★ |

### Order of Execution

```
Week 1                  Week 2                  Week 3
├───────────────────────┼───────────────────────┼──────────────────────
Ideenanmeldung ✅       Pilot (3+3+3)          Pilot Analysis
                        ↓                       ↓
Taxonomy v1 (1h)      Canonicalize (3h)       Schema Analysis (4h)
                        ↓                       ↓
                    Fix normalization         Final Results Report
```

### Critical Path

```
Ideenanmeldung (done)
    ↓
Human Pilot ← YOU ARE HERE (priority #1)
    ↓
Pilot Analysis → Canonicalization → Schema Analysis
    ↓
Full Study (60 participants)
    ↓
BWKI Submission (Sept 21)
```

---

## 7. Citation & Attribution

For the final paper:

```bibtex
@article{logos2025,
  author    = {LOGOS-Hub},
  title     = {LOGOS: LLM-driven End-to-End Grounded Theory Development
               and Schema Induction for Qualitative Research},
  journal   = {arXiv preprint arXiv:2509.24294},
  year      = {2025}
}
```

Paper text:

> *"Our concept canonicalization layer is inspired by the semantic clustering approach in LOGOS (arXiv:2509.24294), which similarly groups fine-grained codes into higher-level schemas for cross-structure comparison."*

---

## 8. Key Decision Log

| # | Decision | Date | Rationale |
|---|----------|:----:|-----------|
| 1 | Adopt methodology only, NOT code | 2026-06-18 | LOGOS is grounded theory, not cognitive graphs |
| 2 | LDS remains frozen | 2026-06-18 | Already validated, audited, tested |
| 3 | Canonicalization is a small module | 2026-06-18 | ~50 LOC, no pipeline rebuild |
| 4 | Taxonomy first (1 hour), canon + schema after Pilot | 2026-06-18 | Highest BWKI value for lowest effort |
| 5 | Embedding clustering optional (Level 3) | 2026-06-18 | Keeps zero new dependencies for basic use |

---

*Document version: v1.0 · 2026-06-18*
*Companion to: docs/model_strategy.md, docs/PRIORITIES.md, docs/methodology.md*
