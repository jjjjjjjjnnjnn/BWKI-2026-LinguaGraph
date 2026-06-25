# LinguaGraph — Human Validation Rationale

> **Purpose:** Justify the choice of cognitive-linguistic tasks, their relationship to cognitive structure, and their connection to LDS.
> **Target audience:** BWKI reviewers, thesis committee.
> **Status:** Draft v1.0 · 2026-06-18

---

## 1. Why These 10 Questions?

### 1.1 Task Selection Criteria

The cognitive-linguistic battery was designed to probe **five distinct cognitive dimensions** that are theorized to be language-dependent:

| Dimension | Question(s) | Cognitive Construct | Language Dependence |
|:----------|:------------|:--------------------|:--------------------|
| **Semantic association** | q8 (time word association) | Semantic network structure | Strong — word associations differ across languages (Boroditsky, 2001) |
| **Cultural schema** | q9 (explain "孝") | Culturally-unique concept representation | Very strong — "孝" has no direct translation in DE/EN |
| **Social cognition** | q10 (emotional reaction) | Social norm internalization | Medium — display rules vary across cultures (Matsumoto, 1990) |
| **Spatial language** | q11, q13, q15 (describe spatial scenes) | Spatial frame of reference | Strong — languages differ in absolute vs relative frames (Levinson, 1996; Majid et al., 2004) |
| **Cross-linguistic syntax** | q12, q14, q16 (translation tasks) | Grammatical structure transfer | Very strong — motion events, temporal concepts, and complex clauses vary systematically across languages (Slobin, 1996) |

### 1.2 Theoretical Motivation

Why these five dimensions?

1. **Semantic association** reveals how concepts are organized in the mental lexicon — are time concepts structured by space metaphors (Boroditsky, 2001)?

2. **Cultural concepts** test whether deeply embedded cultural values ("孝" in Chinese) are systematically simplified or lost in non-native languages — evidence for the linguistic encoding of cultural cognition (Wierzbicka, 1997).

3. **Emotional scripts** examine whether social norms around public behavior are language-dependent — do bilinguals switch emotional display rules when switching languages? (Pavlenko, 2005)

4. **Spatial descriptions** probe whether speakers of different languages attend to different aspects of spatial scenes — e.g., path vs manner salience (Talmy, 2000; Slobin, 1996).

5. **Translation tasks** directly test whether syntactic structures from L1 interfere with L2 production — and whether this interference produces measurable differences in cognitive graph topology.

### 1.3 Why Not the Original Social Issues Questions?

The original questionnaire (q1-q4: freedom, justice, success, family) was designed for the Wikipedia-corpus analysis where we compared *cultural-level* language differences. For *individual-level* human validation, we need:

- **More granularity:** 10 diverse tasks > 4 abstract topics for graph construction
- **Cognitive specificity:** Each task targets a specific cognitive mechanism (spatial, temporal, emotional, etc.)
- **Cross-linguistic contrast:** Translation tasks directly force cross-language comparison
- **Test-retest feasibility:** Concrete tasks (describe a picture) are more replicable than abstract essays

---

## 2. How These Questions Measure Cognitive Structure

### 2.1 From Response to Cognitive Graph

Each task produces a text response from which we extract:

```
Response text
    ↓  (LLM extraction)
Concepts (nodes) + Relations (edges)
    ↓  (NetworkX)
Cognitive graph (DiGraph)
    ↓  (LDS)
Cross-language comparison
```

### 2.2 What Each Task Contributes to the Graph

| Task | Expected Concepts | Expected Relations | Graph Structure |
|:-----|:-----------------|:-------------------|:----------------|
| q8 (word association) | Time-related terms | Association links | Star-like hub ("time" → many associations) |
| q9 (孝 explanation) | Cultural values, family roles | Hierarchical (孝 → subset of behaviors) | Tree structure |
| q11/13/15 (spatial) | Object names, spatial relations | Spatial prepositions | Relational (object₁ → [spatial] → object₂) |
| q12/14/16 (translation) | Agents, actions, objects | Causal/temporal sequences | Sequential (A → do → B) |

### 2.3 Cross-Language Graph Differences as Cognitive Differences

If the Sapir-Whorf hypothesis holds, we expect:

- **Translation tasks:** Different graph topologies for the *same* input sentence — L1 syntax reshapes the cognitive representation
- **Cultural concept:** Richer subgraph for "孝" in ZH (more child nodes) than in DE/EN
- **Spatial tasks:** Different frame-of-reference preferences across languages (absolute vs relative)
- **Emotional scripts:** Different intensity/type of social concepts across languages

If no systematic cross-language graph differences appear, the null hypothesis (language does not measurably shape cognitive structure) is supported.

---

## 3. How LDS Relates to These Questions

### 3.1 LDS Measures Structural Difference, Not Content

LDS is defined as:
```
LDS(L₁, L₂) = 1 − mean(GED_sim, Jaccard_node, Jaccard_edge)
```

It quantifies **how differently two graphs are organized** — not whether the answers are "correct" or "similar" in meaning.

### 3.2 What LDS Values Mean for Each Task

| LDS | Interpretation | Example |
|:---:|:---------------|:--------|
| 0.0 | Identical cognitive graphs | Word-for-word identical translations |
| 0.0–0.3 | Low drift | Same concepts, same relations — language didn't change structure |
| 0.3–0.7 | Moderate drift | Overlapping concepts but different relational structure |
| 0.7–1.0 | High drift | Nearly disjoint concept sets — fundamentally different cognitive organization |

### 3.3 Predictions for Each Task

| Task | Predicted LDS | Rationale |
|:-----|:-------------:|:----------|
| q9 (孝) | **High** (ZH vs DE/EN) | Cultural concept should produce richer ZH graph |
| q12 (motion translation) | **Moderate** | English→DE similar (both Germanic), ZH→both different |
| q13 (spatial) | **Low–Moderate** | Basic spatial relations are universal but frames differ |
| q14 (time translation) | **Moderate–High** | "brought forward" temporal concept already challenging in ZH |
| q16 (complex translation) | **Moderate** | Complex syntax tests linguistic structure transfer |

### 3.4 Limitations of LDS in This Context

1. **LDS does not distinguish between "different" and "wrong".** A translation error (e.g., P003's metaphorical q16) produces a high LDS, but this may reflect L2 proficiency, not cognitive structure.
2. **Graph sparsity.** With ~3-7 concepts per graph, LDS variance is high. Bootstrap CIs are essential.
3. **Extraction noise.** LLM extraction may miss or hallucinate concepts, inflating LDS.

---

## 4. Quality Control

### 4.1 Extraction Validation

- Gold-standard annotations (30 ZH/DE/EN samples) for concept F1 ≥ 0.80
- Relation F1 ≥ 0.70
- Annotator agreement (Cohen's Kappa ≥ 0.70)

### 4.2 Data Quality Thresholds

| Criterion | Threshold | Action if violated |
|:----------|:---------:|:-------------------|
| Completion rate | ≥ 80% | Exclude participant |
| Response length | ≥ 10 chars | Flag for review |
| Translation fidelity | ≥ 2/3 key elements | Flag, may exclude |
| Consent | = 1 | Exclude entirely (GDPR) |

---

## 5. Relation to Prior Work

This validation design is informed by:
- **Slobin (1996):** "Thinking for Speaking" — language shapes online cognitive processing during production
- **Boroditsky (2001):** Time metaphors differ across languages, shaping time cognition
- **Levinson (1996):** Spatial frames of reference vary systematically across languages
- **Pavlenko (2005):** Bilinguals may display different emotional repertoires in each language
- **Wierzbicka (1997):** Cultural keywords are language-specific and lose meaning in translation

---

## 6. References to Cite

1. Boroditsky, L. (2001). Does language shape thought? Mandarin and English speakers' conceptions of time. *Cognitive Psychology*, 43(1), 1–22.
2. Levinson, S. C. (1996). Frames of reference and Molyneux's question. In *Language and Space*.
3. Majid, A., et al. (2004). Can language restructure cognition? The case for space. *Trends in Cognitive Sciences*, 8(3), 108–114.
4. Matsumoto, D. (1990). Cultural similarities and differences in display rules. *Motivation and Emotion*, 14(3), 195–214.
5. Pavlenko, A. (2005). *Emotions and Multilingualism*. Cambridge University Press.
6. Slobin, D. I. (1996). From "thought and language" to "thinking for speaking". In *Rethinking Linguistic Relativity*.
7. Talmy, L. (2000). *Toward a Cognitive Semantics*. MIT Press.
8. Wierzbicka, A. (1997). *Understanding Cultures Through Their Key Words*. Oxford University Press.

---

*Document: docs/validation_rationale.md · Version: v1.0 · 2026-06-18*
