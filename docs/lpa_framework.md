# Language Production Analysis (LPA) — Exploratory Coding Framework

> **Version**: 0.2 (exploratory) | **Status**: Pilot phase | **N pilot**: 6 DE
> **Last updated**: 2026-07-01

---

## Positioning

LPA is an **exploratory coding framework** for analyzing open-ended language production data across languages. It is NOT a validated psychometric instrument. The dimensions and coding criteria below represent hypotheses about how linguistic behavior can be systematically described — not established scales.

### Methodological Status

LPA is in an **early methodological stage** (codebook draft, pilot coding, inter-rater reliability pending). It is designed as a **third, independent evidence stream** alongside LDS-K and LDS-C. Its primary contribution at this stage is methodological: a reproducible coding scheme for cross-linguistic language production data. See `docs/lpa_codebook.md` for the full coding manual.

### Research Positioning

LPA is not an appendix of LDS. It is a **separate research direction** within a broader research program:

```
Research Program: Language, Knowledge & Cognition
│
├── LDS-K  — Knowledge structure comparison (educational materials)
├── LDS-C  — Concept structure comparison (human responses)
└── LPA    — Language production analysis (open-ended linguistic tasks)
```

Each direction has its own research question, methodology, and evidentiary standards. They share the overarching theme of "how language relates to cognition" but do not depend on each other for validation.

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

Each stream addresses a **descriptive question** (not a confirmatory hypothesis):

| Stream | Research Question | Type |
|--------|------------------|------|
| **LDS-K** | How is educational knowledge organized across languages? | Descriptive-comparative |
| **LDS-C** | How are human conceptual structures organized across languages? | Descriptive-comparative |
| **LPA** | How do speakers produce language during open-ended linguistic tasks? | Descriptive-exploratory |

---

## Selection of Coding Dimensions

The four LPA dimensions were selected to span complementary aspects of language production rather than to constitute an exhaustive taxonomy.

**Rationale**:
- **D1 — Spatial Granularity**: Spatial language is one of the most extensively studied domains in cross-linguistic cognition (Levinson, 2003; Slobin, 1996; Talmy, 2000). Including it provides a direct bridge to established findings.
- **D2 — Temporal Framing**: Temporal reference is a well-documented site of cross-linguistic variation (Boroditsky, 2000; Lakoff & Johnson, 1980). It tests whether spatial metaphor ambiguity replicates in naturalistic production.
- **D3 — Conceptual Flexibility**: Bilingual representation (Pavlenko, 2005), social scripts (Goffman, 1967), and event construal (Croft, 2012) tap into different levels of conceptual organization. This dimension is the most exploratory.
- **D4 — Lexical Production**: Free association and neologism formation probe lexical strategies from complementary angles — one receptive (semantic networks: Collins & Loftus, 1975), one productive (word formation: Štekauer, 2005).

**Excluded dimensions** (for transparency): Phonological production, prosody, syntactic complexity, and discourse coherence were considered but excluded because (a) the task battery was not designed to elicit them systematically, and (b) reliable coding would require additional instrumentation (e.g., acoustic analysis for prosody). These remain options for future expansion.

**Language note**: All references to prior work indicate *theoretical grounding* or *methodological inspiration*, not validation of the current coding scheme. The phrase "informed by" is used throughout; "validated by" does not appear.

---

## LPA Dimensions & Coding Scheme

*For the complete codebook with inclusion/exclusion criteria, positive/negative examples, and boundary cases, see `docs/lpa_codebook.md`.*

### D1: Spatial Granularity (Tasks 5–6)

Informed by Talmy (2000) on motion event typology, Levinson (2003) on spatial reference frames, and Slobin (1996) on thinking-for-speaking.

| # | Criterion | Range | Task |
|---|-----------|:-----:|:----:|
| 1 | Source encoded (origin of motion) | 0/1 | Q5 |
| 2 | Path encoded (trajectory of motion) | 0/1 | Q5 |
| 3 | Goal encoded (destination of motion) | 0/1 | Q5 |
| 4 | Manner verb (vs. generic motion verb) | 0/1 | Q5 |
| 5 | Object 1 present (cup) | 0/1 | Q6 |
| 6 | Object 2 present (pen) | 0/1 | Q6 |
| 7 | Spatial relation encoded | 0/1 | Q6 |
| 8 | Second relation encoded | 0/1 | Q6 |
| 9 | Orientation detail beyond basic relation | 0/1 | Q6 |

### D2: Temporal Framing (Task 7)

Informed by Boroditsky (2000) on time-moving vs. ego-moving ambiguity and Lakoff & Johnson (1980) on conceptual metaphor theory.

| Code | Label | Definition |
|:----:|-------|-----------|
| T+ | Unambiguous "earlier" | Speaker clearly interprets shift as earlier (*vorverlegt*) |
| T? | Ambiguous / avoidant | Direction-neutral formulation (*verschoben*) |
| T~ | Non-standard | Literal translation of spatial metaphor (*vorwärts bewegt*) |
| T- | Incomplete | Missing, refused, or too short to categorize |

### D3: Conceptual Flexibility (Tasks 2, 3, 8, 9)

Informed by Pavlenko (2005) on bilingual representation, Goffman (1967) on social scripts, and Croft (2012) on event structure.

| # | Criterion | Task |
|---|-----------|:----:|
| 1 | Bilingual explanation attempted | Q2 |
| 2 | True bilingual parallel content | Q2 |
| 3 | Code-switching within utterance | Q2 |
| 4 | Multi-clause social script response | Q3 |
| 5 | Sophisticated strategy (apology, philosophical, de-escalation) | Q3 |
| 6 | Perspective shift in event narration | Q8/Q9 |
| 7 | Causal subordination (*da, because, 因为*) | Q9 |

### D4: Lexical Production (Tasks 1, 10)

Informed by Collins & Loftus (1975) on semantic network structure and Štekauer (2005) on word-formation.

| # | Criterion | Task |
|---|-----------|:----:|
| 1 | Associative diversity (≥3 semantic categories) | Q1 |
| 2 | Beyond-prototype associations (≥2 non-prototypical) | Q1 |
| 3 | Multi-word name (≥2 orthographic words) | Q10 |
| 4 | Functional name specification | Q10 |
| 5 | Creative/original coinage | Q10 |
| 6 | Bilingual element in name | Q10 |

---

## Inter-Rater Reliability Protocol

### Predefined Decision Rules (Landis & Koch, 1977; adapted)

| Cohen's κ | Interpretation | Action |
|:---------:|---------------|--------|
| ≥ 0.80 | Almost perfect agreement | Accept criterion as reliable |
| 0.70–0.79 | Substantial agreement | Accept, but flag for minor discussion |
| 0.60–0.69 | Moderate agreement | Review criterion definition, adjudicate disagreements, re-code |
| < 0.60 | Less than moderate | Revise criterion or exclude from analysis |

**These thresholds are defined a priori** — no post-hoc adjustment after IRR calculation.

### Procedure

1. **Sample**: 20 responses (or 100% of pilot, whichever is smaller)
2. **Coders**: Primary coder + independent coder, blind to each other
3. **Training**: 5 responses coded jointly, discussed, discrepancies resolved
4. **Coding**: Remaining responses coded independently
5. **Computation**: Cohen's κ per criterion; percentage agreement for reference
6. **Decision**: Each criterion accepted/flagged/revised per the threshold table above

---

## Dataset Value

The primary output of this study is NOT a set of scores — it is a **cross-linguistic open-response dataset**:

- **DE**: ~120 respondents × 10 tasks → ~1,200 open-ended responses (in collection)
- **ZH**: 30+ target → ~300+ responses (questionnaire ready)
- **EN**: 30+ target → ~300+ responses (questionnaire ready)
- **Total**: ~1,800+ open-ended linguistic responses across 3 languages

This dataset has independent value for NLP research, cognitive linguistics, bilingualism studies, and qualitative methodology development. It is designed to be extended, not consumed within a single analysis.

---

## Reporting Principles

1. **No composite scores.** Each dimension reported separately.
2. **No cross-dimension weighting.** No evidence for combining dimensions.
3. **No causal arrows between evidence streams.** LPA does not validate LDS-K or LDS-C.
4. **Exploratory qualifiers.** All findings use *observed, exploratory, suggests, is consistent with*.
5. **Effect sizes instead of p-values** where appropriate at full sample size.
6. **Inter-rater reliability mandatory** for all coded dimensions before any cross-linguistic comparison.

---

## Methodological Maturity

The three evidence streams in this research program are at different stages of methodological maturity. This is transparently acknowledged.

| Stream | Type | Maturity |
|--------|------|:--------:|
| **LDS-K** | Graph-theoretic comparison with validated null models | High |
| **LDS-C** | Concept graph comparison from open-ended responses | Medium (pending N ≥ 30) |
| **LPA** | Exploratory qualitative coding framework | Early (codebook pilot, IRR pending) |

These maturity differences do NOT weaken the research program. They clarify what each stream can and cannot claim.
