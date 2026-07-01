# Language Production Analysis (LPA) — Framework & Execution Plan
> **Status**: Active | **N target**: 120 (DE), 30+ ZH, 30+ EN
> **Integration**: Third evidence layer in LinguaGraph triangulation framework

---

## Scientific Positioning

### Three-Layer Evidence Architecture

```
Layer 1: Textbook Knowledge Structure (LDS-K)          ✅ COMPLETE
  → "How do educational materials organize knowledge across languages?"

Layer 2: Human Concept Structure (LDS-C)                🔶 COLLECTING
  → "Do human conceptual representations follow similar patterns?"

Layer 3: Language Production Analysis (LPA)             🔶 NEW
  → "Do spontaneous language production patterns show 
     systematic cross-linguistic variation?"
```

**Core argument**: Three independent methods converge on the same conclusion — language systematically shapes cognition, visible at multiple levels (knowledge structure, concept representation, language production).

### Key Hypotheses

| Hypothesis | Layer 1 (LDS-K) | Layer 2 (LDS-C) | Layer 3 (LPA) |
|------------|:---------------:|:---------------:|:-------------:|
| H1: ZH-DE closer than ZH-EN/DE-EN | ✅ ZH-DE=0.519 | 🔶 Pending N≥30 | 🔶 Pending |
| H2: Within-language variation > cross-language expectation | ✅ Null Model | 🔶 Pending | Plausible |
| H3: Systematic cross-linguistic patterns in language production | — | — | Testable now |

---

## LPA Dimensions & Coding Scheme

### D1: Spatial Cognition (Tasks 5–6)
**Metric**: Spatial Granularity Score (SGS, 0–10)

| Criterion | Points | Coding |
|-----------|:------:|--------|
| Motion: Source mentioned | 1 | *aus dem Raum* |
| Motion: Path mentioned | 1 | *durch das Wohnzimmer* |
| Motion: Goal mentioned | 1 | *in den Garten* |
| Motion: Manner verb | 1 | *läuft* vs *geht* |
| Static: Object 1 presence | 1 | Cup mentioned |
| Static: Object 2 presence | 1 | Pen mentioned |
| Static: Spatial relation 1 | 1 | *hinter/vor/neben* |
| Static: Spatial relation 2 | 1 | Both objects related to book |
| Static: Orientation detail | 1 | *Henkel, Schreibseite, parallel* |
| Static: Reference frame | 1 | Intrinsic + relative combined |

**Pilot scores (N=6)**: R1=6, R2=2, R3=6, R4=5, R5=9, R6=9

### D2: Temporal Cognition (Task 7)
**Metric**: Temporal Frame Preference (TFP)

| Category | Code | Description |
|----------|:----:|-------------|
| Correct-unambiguous | T+ | *vorverlegt* (earlier) |
| Ambiguous-avoidant | T? | *verschoben* (shifted) |
| Non-standard | T~ | *vorwärts bewegt* (literal) |
| Incomplete | T- | Missing or partial response |

### D3: Conceptual Flexibility (Tasks 2, 3, 8, 9)
**Metric**: Conceptual Flexibility Index (CFI, 0–8)

| Criterion | Points | Task Source |
|-----------|:------:|:-----------:|
| Bilingual explanation attempted | 1 | Q2 |
| True bilingual (DE+EN parallel) | 2 | Q2 |
| Code-switching within utterance | 1 | Q2 |
| Social script >1 clause | 1 | Q3 |
| Perspective shift from default | 1 | Q8/Q9 (agent change) |
| Causal subordination | 1 | Q9 (*da es regnete*) |
| Naturalness (not literal translation) | 1 | Q9 |

### D4: Lexical Creativity (Tasks 1, 10)
**Metric**: Lexical Creativity Score (LCS, 0–6)

| Criterion | Points | Source |
|-----------|:------:|--------|
| >3 unique associates in Q1 | 1 | Q1 |
| Non-prototypical associates | 1 | Q1 (not Uhr) |
| Multi-word name in Q10 | 1 | Q10 |
| Functional-precise name | 1 | Q10 |
| Creative/original name | 1 | Q10 |
| Bilingual hybrid name | 1 | Q10 |

---

## Analysis Pipeline

```python
analyze_lpa.py
├── read_csv()          # Read survey responses (DE/EN/ZH)
├── code_spatial()      # Code D1: SGS scores
├── code_temporal()     # Code D2: TFP categories
├── code_flexibility()  # Code D3: CFI scores
├── code_creativity()   # Code D4: LCS scores
├── compute_profiles()  # Aggregate across dimensions
├── cross_language_compare()  # ZH vs EN vs DE
└── report()           # Generate analysis report
```

---

## Immediate Execution Plan

### Phase 1: Create ZH & EN Questionnaire Versions (HOURS)
- Translate all 10 tasks to Chinese and English
- Maintain identical task structure for cross-linguistic comparability
- Deploy as static HTML survey (like LinguaGraph survey)

### Phase 2: Code Existing DE Pilot (HOURS)
- Apply coding scheme to 6 existing responses
- Validate inter-rater reliability if possible
- Generate pilot LPA report

### Phase 3: Build Analysis Script (DAY)
- Python script implementing the full LPA pipeline
- Statistical comparison framework
- Visualization generation

### Phase 4: Data Collection (WEEKS)
- Distribute ZH/EN versions alongside DE version
- Target: 30+ per language group
- Target: 120 total across all languages

### Phase 5: Paper Integration (WEEKS)
- §3.x Language Production Analysis results
- §4.x Triangulation across three evidence layers
- §5.x Summary: convergent evidence for cross-linguistic cognitive variation

---

## Paper Integration

### Suggested Structure

**New subsection in Results**: `§3.4 Language Production Analysis (Exploratory)`

> "To complement the structural knowledge graph analysis, we conducted an exploratory language production study..."

**New subsection in Discussion**: `§4.x Triangulation Across Three Evidence Layers`

> "The three independent methods — textbook knowledge graphs (LDS-K), human concept graphs (LDS-C), and language production analysis (LPA) — provide convergent evidence for systematic cross-linguistic cognitive variation..."
