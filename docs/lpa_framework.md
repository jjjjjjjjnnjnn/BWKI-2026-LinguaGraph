# Language Production Analysis (LPA) — Exploratory Coding Framework
> **Version**: 0.1 (exploratory) | **Status**: Pilot phase | **N pilot**: 6 DE

---

## Positioning

LPA is an **exploratory coding framework** for analyzing open-ended language production data across languages. It is NOT a validated psychometric instrument. The dimensions and coding criteria below represent hypotheses about how linguistic behavior can be systematically described — not established scales.

### Three Evidence Streams (Parallel, No Causal Hierarchy)

```
              Language
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
 Knowledge   Concepts    Production
 Structure   (LDS-C)     (LPA)
 (LDS-K)
      │          │           │
      ▼          ▼           ▼
 Educational  Human open-  Elicited
  textbooks   ended        linguistic
              responses    tasks
```

Each stream addresses a **different research question**:
- **LDS-K**: How do educational materials organize knowledge across languages?
- **LDS-C**: Do human conceptual representations follow similar cross-linguistic patterns?
- **LPA**: What systematic patterns appear in spontaneous language production across languages?

The three streams can **inform** each other but do not **depend** on each other. Convergent patterns across streams strengthen the overall research program; divergent patterns are equally informative.

---

## Coding Dimensions

### D1: Spatial Granularity (Tasks 5–6)

**Question**: How detailed are spatial descriptions within and across languages?

| Criterion | Description | Task |
|-----------|-------------|:----:|
| Source mention (*aus dem Raum, from the room, 从房间*) | Motion origin encoded | Q5 |
| Path mention (*durch das Wohnzimmer, through the living room, 穿过客厅*) | Motion trajectory encoded | Q5 |
| Goal mention (*in den Garten, into the garden, 进入花园*) | Motion destination encoded | Q5 |
| Manner verb (*läuft, runs, 跑*) vs generic (*geht, goes, 走*) | Motion quality encoded | Q5 |
| Object 1 presence (cup/Tasse/杯子) | First reference object | Q6 |
| Object 2 presence (pen/Stift/笔) | Second reference object | Q6 |
| Spatial relation (hinter/vor/neben/behind/front/next to) | Spatial relationship encoded | Q6 |
| Second spatial relation | Both objects located w.r.t. reference | Q6 |
| Orientation detail (handle/writing-side/direction) | Beyond basic relation | Q6 |
| Multiple reference frames (intrinsic + relative) | Combinatorial frame use | Q6 |

Reported as: **individual criterion flags**, not a summed score.

### D2: Temporal Framing (Task 7)

**Question**: How do speakers resolve temporal metaphor ambiguity?

| Category | Label | Description |
|:--------:|:-----:|-------------|
| T+ | Unambiguous | *vorverlegt* — clear "earlier" interpretation |
| T? | Ambiguous/avoidant | *verschoben* — direction-neutral |
| T~ | Non-standard | *vorwärts bewegt* — literal translation attempt |
| T- | Incomplete | Missing or refused response |

Reported as: **categorical distribution** per language.

### D3: Conceptual Flexibility (Tasks 2, 3, 8, 9)

**Question**: What strategies do speakers use for conceptually demanding tasks?

| Criterion | Description | Task |
|-----------|-------------|:----:|
| Bilingual attempt | Speaker tries to explain in 2+ languages | Q2 |
| True bilingual parallel | Both languages, equivalent content | Q2 |
| Code-switching | Alternates languages within utterance | Q2 |
| Multi-clause social script | >1 clause in embarrassment response | Q3 |
| Sophisticated strategy | Apology, philosophical, or de-escalation | Q3 |
| Perspective shift | Agent differs from default (mother→girl) | Q8/Q9 |
| Causal subordination | *da, because, 因为* clause | Q9 |

Reported as: **individual criterion flags** + **strategy type distribution**.

### D4: Lexical Production (Tasks 1, 10)

**Question**: What lexical strategies appear in free association and naming?

| Criterion | Description | Task |
|-----------|-------------|:----:|
| Associative diversity | ≥3 distinct semantic categories in Q1 | Q1 |
| Non-prototypical associates | Beyond the most obvious response | Q1 |
| Multi-word name | ≥2 words in robot name | Q10 |
| Functional specification | Name encodes function/domain | Q10 |
| Creative/original | Non-trivial coinage | Q10 |
| Bilingual element | Code-mixing in naming | Q10 |

Reported as: **individual criterion flags** + **strategy type inventory**.

---

## Inter-Rater Reliability Protocol

To establish coding reliability before any cross-linguistic comparison:

1. **Sample**: 20 responses (or 100% of pilot) randomly selected
2. **Coders**: Primary coder (automated/L1 speaker) + independent coder
3. **Metric**: Cohen's κ per criterion (≥0.70 threshold), percentage agreement
4. **Reconciliation**: Disagreements reviewed, criteria refined, re-coded
5. **Report**: κ values reported alongside all LPA results

Implementation: `scripts/analyze_lpa.py --irr` flag for automated inter-rater comparison.

---

## Dataset Value

The primary output of this study is NOT a set of scores — it is a **cross-linguistic open-response dataset**:

- **DE**: ~120 respondents × 10 tasks → ~1,200 open-ended responses
- **ZH**: TBD (target 30+) → ~300+ responses
- **EN**: TBD (target 30+) → ~300+ responses
- **Total**: ~1,800+ open-ended linguistic responses across 3 languages

This dataset has independent value for:
- NLP research (cross-linguistic text generation)
- Cognitive linguistics (spatial/temporal reference across languages)
- Bilingualism research (code-switching patterns)
- Methodology development (automated coding of open-ended responses)

---

## Reporting Principles

1. **No composite scores.** Each dimension is reported separately with its own criteria.
2. **No cross-dimension weighting.** No evidence supports combining SGS + TFP + CFI + LCS.
3. **No causal arrows.** LPA does not "support" or "validate" LDS-K or LDS-C.
4. **Exploratory qualifiers.** All findings use *observed, exploratory, suggests, is consistent with*.
5. **Effect sizes, not p-values.** Cohen's d or similar for cross-language comparisons.
6. **Inter-rater reliability.** κ values mandatory for all coded dimensions.
