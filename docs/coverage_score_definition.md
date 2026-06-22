# Coverage Score (CS) — Definition v1.0

> **Date**: 2026-06-22
> **Purpose**: Quantify how well a textbook knowledge graph covers an official curriculum standard
> **Relationship to LinguaGraph**: Third metric family, alongside LDS (cross-language) and CDS/HDS (structural)

---

## 1. Definition

### 1.1 Coverage Score (CS)

Given a **curriculum graph** G_c = (V_c, E_c) and a **textbook graph** G_t = (V_t, E_t) for the same domain and language:

```
CS(G_t, G_c) = |V_t ∩ V_c| / |V_c|
```

where V_t ∩ V_c is the set of concepts that appear in both the textbook and the curriculum.

**Interpretation**: CS = 0.8 means the textbook covers 80% of the concepts the curriculum requires.

### 1.2 Level-Specific Coverage

Since knowledge is organized by education level, coverage should be computed **per level**:

```
CS_l(G_t, G_c) = |V_t(l) ∩ V_c(l)| / |V_c(l)|
```

where V(l) is the set of concepts at education level l ∈ {elementary, middle, high, college}.

### 1.3 Weighted Coverage Score (WCS)

An optional extension that weights concepts by their curricular importance:

```
WCS(G_t, G_c) = Σ_i w_i · 𝟙(concept_i ∈ V_t) / Σ_i w_i
```

where w_i is the weight assigned by the curriculum (e.g., core concepts weight 3, supporting concepts weight 1).

---

## 2. Concept Matching

For the purpose of computing V_t ∩ V_c, two concepts match if:

1. **Exact label match**: The textbook concept's label for the target language appears identically in the curriculum graph's labels for the same language
2. **Cross-lingual match** (for trilingual curricula): The concept shares the same cross-lingual ID in the alignment map (`config/concept_mapping.json`)
3. **Human review** (for ambiguous cases): A domain expert confirms equivalence

Matching is **case-insensitive** and ignores leading/trailing whitespace.

---

## 3. Examples

### Example 1: Middle School Math

```
V_curriculum (middle) = {Natürliche Zahlen, Brüche, Dezimalzahlen, 
                         Negative Zahlen, Terme, Gleichungen,
                         Funktionen, Dreiecke, Kreis, Zufall}
V_textbook (middle)    = {Natürliche Zahlen, Brüche, Dezimalzahlen,
                         Terme, Gleichungen, Dreiecke, Zufall}

CS_middle = 7 / 10 = 0.70
```

Interpretation: The textbook covers 70% of the middle school curriculum. Missing concepts: Negative Zahlen, Funktionen, Kreis.

### Example 2: Curriculum vs Textbook Gap Analysis

```
Missing concepts:
  middle: Negative Zahlen, Funktionen, Kreis
  high:  (consult curriculum)

Concentration ratio:
  Coverage is highest in elementary (0.85) and lowest in high (0.62).
  → Textbook diverges most from curriculum at advanced levels.
```

---

## 4. Implementation

```python
def coverage_score(textbook_concepts, curriculum_concepts, level=None):
    """Compute CS per level or overall.
    
    Args:
        textbook_concepts: list of concept dicts with 'name' and 'level'
        curriculum_concepts: list of concept dicts with 'name' and 'level'
        level: optional filter (elementary|middle|high|college)
    
    Returns:
        cs: float in [0, 1]
        matched: list of matched concept names
        missing: list of curriculum concepts not in textbook
    """
    # Filter by level if specified
    tc = {c['name'] for c in textbook_concepts 
          if level is None or c.get('level') == level}
    cc = {c['name'] for c in curriculum_concepts
          if level is None or c.get('level') == level}
    
    if not cc:
        return 0.0, [], list(cc)
    
    matched = tc & cc
    missing = cc - tc
    cs = len(matched) / len(cc)
    
    return cs, sorted(matched), sorted(missing)
```

---

## 5. References

CS is a simplified educational variant of graph recall, inspired by:

- TIMSS Curriculum Coverage Analysis (IEA, 2019)
- Novak's concept map alignment (Novak & Cañas, 2008)
- Alatrash et al.'s prerequisite coverage (2025)

It deliberately avoids:
- Semantic similarity scoring (over-engineered for v1)
- Embedding-based matching (unnecessary when concepts share labels)
- LLM-based evaluation (non-deterministic)
