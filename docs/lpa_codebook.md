# LPA Codebook — Coding Dimensions, Definitions, and Rules

> **Version**: 0.2 (exploratory) | **N pilot**: 6 DE
> **Status**: Pre-registration ready | **Last updated**: 2026-07-01

---

## Overview

This codebook defines the coding dimensions and criteria for the Language Production Analysis (LPA), an exploratory qualitative coding framework for open-ended cross-linguistic linguistic data (Krippendorff, 2018). Each dimension is coded at the **criterion level** using binary (present/absent) or nominal decisions. No composite scores are formed; dimensions are reported independently.

### Coding Principles

1. **Binary coding per criterion**: Each criterion is marked present (1) or absent (0). Partial credit is not assigned.
2. **Independent dimensions**: Each dimension is coded and reported separately. Cross-dimension aggregation requires prior empirical validation (e.g., factor analysis at N ≥ 120).
3. **Refusal handling**: Missing responses or explicit refusals ("Kann kein Englisch sorry") are coded as `refused: 1`. They are reported separately and excluded from criterion counts on a per-task basis.
4. **Threshold-coded criteria**: For continuous features (e.g., word count, number of clauses), binary thresholds are defined below with explicit rationale.

---

## D1: Spatial Granularity

**Construct definition**: Spatial Granularity captures the degree of detail with which speakers describe motion events (Talmy, 2000) and static spatial configurations (Levinson, 2003; Pederson et al., 1998) in spontaneous language production. Higher granularity indicates more spatial subcomponents encoded.

**Relevant literature**: Levinson (2003) on spatial reference frames; Slobin (1996, 2000) on "thinking for speaking" in motion event encoding; Talmy (2000, Vol. I) on motion event typology (Manner vs. Path languages).

### Motion Event Coding (Task 5)

| # | Criterion | Definition | Inclusion | Exclusion | Example (present) | Example (absent) |
|---|-----------|-----------|-----------|-----------|-------------------|------------------|
| 1 | Source encoded | Speaker specifies the origin location of motion | *aus dem Raum, from the room, 从房间(里出来)* | Time or reason of motion | *Mike kommt aus einem Raum* | *Mike geht* |
| 2 | Path encoded | Speaker specifies the trajectory of motion | *durch das Wohnzimmer, through/across, 穿过/经过* | Goal only (without trajectory) | *geht durch das Wohnzimmer* | *Mike geht in den Garten* |
| 3 | Goal encoded | Speaker specifies the destination of motion | *in den Garten, into/betritt/enters, 进入/到* | Path only (without destination) | *betritt den Garten* | *Mike geht durch den Raum* |
| 4 | Manner verb | Speaker uses a motion-verb that encodes manner separate from path (Slobin, 2000) | *läuft (runs), rennt (rushes), 跑/走* | Generic path verbs: *geht, kommt, betritt* | *läuft durch das Wohnzimmer* | *geht durch* |

**Boundary cases**:
- If the entire response is code-switched or in a different language than the task language, code based on what is produced.
- If both the English prompt and German response contain the spatial elements, code the German response only.

### Static Spatial Coding (Task 6)

| # | Criterion | Definition | Inclusion | Exclusion | Example (present) | Example (absent) |
|---|-----------|-----------|-----------|-----------|-------------------|------------------|
| 5 | Object 1 present | First reference object (cup/Tasse/杯子) mentioned | Any mention of cup or its equivalent | Generic deixis (*da/dort/there*) | *Die Tasse steht…* | Only *da* |
| 6 | Object 2 present | Second reference object (pen/Stift/笔) mentioned | Any mention of pen or its equivalent | Referring to both objects collectively | *Der Stift liegt…* | *beide Sachen* |
| 7 | Relation encoded | At least one spatial relation specified between objects | Spatial prepositions: *hinter/vor/neben/auf/unter*, etc. (Levinson, 2003) | Deictic only (*hier/da*); temporal only; English loanwords without DE spatial preposition | *hinter dem Buch* | *die Tasse und das Buch* |
| 8 | Second relation | A second distinct spatial relation is specified | Two or more spatial prepositions or relational phrases | Repetition of the same relation; synonyms without new spatial information | *links neben dem Buch* after already describing *parallel zum Buch* | *hinter…und dann auch dahinter* |
| 9 | Orientation detail | Speaker specifies orientation beyond basic spatial relation | Handle direction (*Henkel rechts*), writing-side (*Schreibseite*), parallel configuration (*parallel*) | Repetition of basic relation | *Henkel zeigt nach rechts* | *neben dem Buch* |
| 10 | Multi-frame | Speaker uses more than one spatial reference frame (intrinsic + relative; Levinson, 2003: Ch. 1) | Combination of intrinsic (object-centered: *parallel zum Buch*) and relative (viewer-centered: *links neben*) | Only one frame type | *parallel zum Buch* (intrinsic) + *links neben* (relative) | Only relative *links neben* |

**Boundary cases**:
- *neben* (next to) is coded as a spatial relation regardless of whether it is ambiguous between intrinsic and relative reading (allow coding, flag as ambiguous if relevant to analysis).
- If the respondent corrects themselves mid-description, code the final version.

---

## D2: Temporal Framing

**Construct definition**: Temporal framing captures how speakers resolve the well-documented ambiguity of spatial metaphors for time (Boroditsky, 2000; Lakoff & Johnson, 1980, Ch. 9). The "moved forward" construction in Task 7 is ambiguous between "earlier" (time-moving: the exam moves toward the present from the future) and "later" (ego-moving: the exam moves forward with the ego's timeline).

**Relevant literature**: Boroditsky (2000) on metaphorical structuring of time; Lakoff & Johnson (1980) on conceptual metaphor theory; Núñez & Cooperrider (2013) on the space-time mapping cross-culturally; Gentner et al. (2002) on metaphor in relational language.

| Code | Label | Definition | Example | Linguistic markers |
|:----:|-------|-----------|---------|-------------------|
| T+ | Unambiguous "earlier" | Speaker clearly interprets the temporal shift as making the event occur earlier | *Der Test wurde um zwei Tage vorverlegt* | *vorverlegt*; *提前*; *brought forward* (without ambiguity) |
| T? | Ambiguous / avoidant | Speaker uses a direction-neutral formulation, avoiding the metaphoric ambiguity | *Die Prüfung wurde um zwei Tage verschoben* | *verschoben* (direction-neutral "shifted"); *改期*; *rescheduled* |
| T~ | Non-standard | Speaker attempts a literal translation of the English spatial metaphor | *wurde um zwei Tage vorwärts bewegt* | *vorwärts bewegt*; *moved forward* (no idiomatic counterpart); *向前移* |
| T- | Incomplete | Response is missing, refused, or too short to categorize (≤5 characters) | *.. ..... * / *Kann kein Englisch* / — | Any non-response or refusal |

**Coding decision rule**: If the speaker uses any unambiguous lexical marker of "earlier" (e.g., *vorverlegt*), code T+. If the speaker uses a direction-neutral or ambiguous verb (*verschoben, 推迟, shifted, rescheduled*), code T?. The T~ category is reserved for literal translations from English that are non-idiomatic in the target language.

---

## D3: Conceptual Flexibility

**Construct definition**: Conceptual flexibility captures strategies speakers employ when faced with conceptually demanding linguistic tasks: explaining culture-specific concepts bilingually (Pavlenko, 2005), navigating unexpected social situations (Goffman, 1967), and construing events from alternative perspectives (Talmy, 2000, Vol. II; Croft, 2012).

**Relevant literature**: Pavlenko (2005) on bilingual conceptual representation; Grosjean (2010) on bilingual language mode; Goffman (1967) on face-to-face interaction and face-work; Talmy (2000, Vol. II) on event conflation and perspective; Croft (2012) on causal structure in events.

### Bilingual Explanation (Task 2)

| # | Criterion | Definition | Example (Present) | Example (Absent) |
|---|-----------|-----------|-------------------|------------------|
| 1 | Bilingual attempt | Speaker attempts explanation in more than one language | *DE definition + "the feeling that..."* | Only DE (*Das Gefühl...*) |
| 2 | True bilingual parallel | Both languages convey equivalent conceptual content | *DE: Fernweh ist der Wille zu reisen + EN: a desire to travel* | DE only, or EN only |
| 3 | Code-switching | Speaker alternates between languages within a single utterance | *"its a Desiree tot Go far away from Home"* after DE intro | Separate monolingual sentences per language |

### Social Script (Task 3)

| # | Criterion | Definition | Example |
|---|-----------|-----------|---------|
| 4 | Multi-clause | Response contains more than one clause or >10 words | *Niemand ist perfekt, jeder kann mal Fehler machen* |
| 5 | Apology strategy | Speaker apologizes or admits error | *Das tut mir leid, mir ist ein Fehler unterlaufen* |
| 6 | Defiance strategy | Speaker reframes situation as humorous or defiant | *da hab ich euch verarscht* |
| 7 | Philosophical strategy | Speaker generalizes to a universal norm | *Niemand ist perfekt* |
| 8 | Hedging strategy | Speaker uses discourse markers of uncertainty | *Ich meine...* |
| 9 | De-escalation strategy | Speaker actively manages group reaction | *Alle beruhigen sich jetzt Mal* |

**Strategy coding is NOT exclusive**: one response may show multiple strategies (e.g., apology + philosophical). Code all strategies present.

### Event Construal (Tasks 8–9)

| # | Criterion | Definition | Example (Present) | Example (Absent) |
|---|-----------|-----------|-------------------|------------------|
| 10 | Perspective shift | Speaker narrates event from non-default agent perspective | *Girl took umbrella* (girl as agent) | *Mother gave girl umbrella* (mother as agent) |
| 11 | Causal subordination | Speaker explicitly marks causality with subordinating conjunction | *da es regnete; because it was raining; 因为下雨* | *wegen des Regens* (prepositional, not subordinate clause) |
| 12 | Natural expression | Response is >20 characters and deviates from literal translation | Reformulated sentence with natural syntax | Word-for-word translation |

---

## D4: Lexical Production

**Construct definition**: Lexical production captures strategies in two divergent tasks: free association, which taps into semantic network structure (Collins & Loftus, 1975), and neologism formation, which reveals word-formation strategies (Štekauer, 2005; Clark, 1993).

**Relevant literature**: Collins & Loftus (1975) on spreading activation in semantic networks; Clark (1993) on lexical innovation in language acquisition; Štekauer (2005) on the nature of word-formation rules.

### Free Association (Task 1)

| # | Criterion | Definition | Example (Present) | Example (Absent) |
|---|-----------|-----------|-------------------|------------------|
| 1 | Associative diversity | Words cover ≥3 distinct semantic categories (measurement, institutional, pressure, calendar, temporal, digital) | *Uhr* (measurement), *Schulzeit* (institutional), *spät* (pressure) — 3 categories | All words in 1 category |
| 2 | Beyond prototype | At least 2 of 5 words are non-prototypical (not *Uhr/clock/time/时间* for ZEIT) | *Schulzeit, bildschirmzeit, Monat* — none directly mean "clock" | *Uhr, Uhrzeit, Uhrzeiger* — all clock-related |

**Category inventory** (for criterion 1):
- **Measurement**: time units, instruments — *Uhr, Zeiger, Sekunde, Minute, Stunde*
- **Institutional**: school, work — *Schulzeit, Schulstunde, 学习, 工作*
- **Pressure**: urgency, lateness — *hetzen, spät, beeilen, 忙, 迟*
- **Calendar**: dates, months, years — *Monat, Jahr, Tag*
- **Temporal-deictic**: *später, vorhin, 以前, 以后*
- **Digital/modern**: *bildschirmzeit, 屏幕时间*

### Robot Naming (Task 10)

| # | Criterion | Definition | Example (Present) | Example (Absent) |
|---|-----------|-----------|-------------------|------------------|
| 3 | Multi-word name | Name consists of ≥2 orthographic words | *Medizinischer Stationsassistenz-Roboter* | *krankenschwester* |
| 4 | Functional specification | Name encodes at least one function from the task description (Štekauer's functional naming) | Contains *assist-/medizin-/kranken-/nurse/医疗/护理* | *Maximus Aura* — no functional information |
| 5 | Creative/original | Name is non-trivial — not a direct profession label and >15 characters or contains non-initial uppercase | *Der (Allesmacher)*, *Robot 200 Maximus Aura* | *krankenschwester* |
| 6 | Bilingual element | Name incorporates lexical material from a second language | *Krankenschwester **bot***; *Medizinischer **Roboter*** | Monolingual name only |

---

## Inter-Rater Reliability Protocol

### Procedure

1. **Sample**: 20 responses (or until κ ≥ 0.70 achieved per dimension, whichever is larger)
2. **Coders**: Primary coder + independent coder, blind to each other's coding
3. **Training phase**: Both coders independently code 5 responses, compare, discuss disagreements
4. **Coding phase**: Both coders independently code the remaining 15 responses
5. **Calculation**: Cohen's κ per criterion (Cohen, 1960); percentage agreement for reference (Landis & Koch, 1977)

### Thresholds (Landis & Koch, 1977)

| κ | Interpretation | Action |
|:---:|---------------|--------|
| ≥ 0.80 | Almost perfect | Accept |
| 0.61–0.79 | Substantial | Accept, review borderline criteria |
| 0.41–0.60 | Moderate | Refine criterion definition, re-code |
| ≤ 0.40 | Fair/poor | Revise criterion or exclude |

### Implementation

```bash
python scripts/analyze_lpa.py --irr --coder1 coder1.json --coder2 coder2.json
```

---

## References

Boroditsky, L. (2000). Metaphoric structuring: Understanding time through spatial metaphors. *Cognition*, 75(1), 1–28.

Clark, E. V. (1993). *The lexicon in acquisition*. Cambridge University Press.

Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, 20(1), 37–46.

Collins, A. M., & Loftus, E. F. (1975). A spreading-activation theory of semantic processing. *Psychological Review*, 82(6), 407–428.

Croft, W. (2012). *Verbs: Aspect and causal structure*. Oxford University Press.

Gentner, D., Imai, M., & Boroditsky, L. (2002). As time goes by: Evidence for two systems in processing space → time metaphors. *Language and Cognitive Processes*, 17(5), 537–565.

Goffman, E. (1967). *Interaction ritual: Essays on face-to-face behavior*. Anchor Books.

Grosjean, F. (2010). *Bilingual: Life and reality*. Harvard University Press.

Krippendorff, K. (2018). *Content analysis: An introduction to its methodology* (4th ed.). Sage.

Lakoff, G., & Johnson, M. (1980). *Metaphors we live by*. University of Chicago Press.

Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics*, 33(1), 159–174.

Levinson, S. C. (2003). *Space in language and cognition: Explorations in cognitive diversity*. Cambridge University Press.

Núñez, R., & Cooperrider, K. (2013). The tangle of space and time in human cognition. *Trends in Cognitive Sciences*, 17(5), 220–229.

Pavlenko, A. (2005). Bilingualism and thought. In J. F. Kroll & A. M. B. De Groot (Eds.), *Handbook of bilingualism: Psycholinguistic approaches* (pp. 433–453). Oxford University Press.

Pederson, E., Danziger, E., Levinson, S. C., Kita, S., Senft, G., & Wilkins, D. (1998). Semantic typology and spatial conceptualization. *Language*, 74(3), 557–589.

Slobin, D. I. (1996). From "thought and language" to "thinking for speaking." In J. J. Gumperz & S. C. Levinson (Eds.), *Rethinking linguistic relativity* (pp. 70–96). Cambridge University Press.

Slobin, D. I. (2000). Verbalized events: A dynamic approach to linguistic relativity and determinism. In S. Niemeier & R. Dirven (Eds.), *Evidence for linguistic relativity* (pp. 107–138). John Benjamins.

Štekauer, P. (2005). *Meaning predictability in word formation*. John Benjamins.

Talmy, L. (2000). *Toward a cognitive semantics* (Vol. I: Concept structuring systems; Vol. II: Typology and process in concept structuring). MIT Press.
