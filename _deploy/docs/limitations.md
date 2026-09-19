# LinguaGraph Limitations

> **Wegweiser (Stand 2026-09-17)**: Die nachstehenden Abschnitte sind ein allgemeines Template (Frühphase).
> Die verbindlichen, zahlenbelegten Einschränkungen stehen in:
> `paper/04_discussion.md` §8.10/§8.12 (Power 0,06–0,12 Between vs. Within-Design-Folge, registrierte Folgeuntersuchung R1),
> `docs/p2_methodology_rechecks.md` (Alignierungs-Artefakte: P2-Recheck, Size-Matching-Umkehr),
> `docs/BASELINE_LEDGER.md` §6/§10 (retired Ablation-Werte, T1-Dekontamination Fig8),
> `docs/evidence_register.md` C16/C17 (Herabstufungen).
> Für die Begutachtung gelten diese vier Quellen; dieses Dokument dient nur als Überblick.

## Method Limitations

### 1. Concept Extraction Accuracy

**Issue:** The fallback extraction (keyword matching) has limited coverage. LLM extraction depends on prompt design and model quality.

**Impact:** Concepts may be missed or incorrectly extracted, affecting graph structure.

**Mitigation:** 
- LLM extraction with structured prompts
- Human validation on gold dataset
- Error analysis with systematic classification

### 2. Graph Edit Distance Scalability

**Issue:** GED computation is NP-hard in general. NetworkX's exact algorithm becomes slow for graphs with >15 nodes.

**Impact:** Cannot scale to large knowledge graphs without approximation.

**Mitigation:**
- Current graphs are small (5-20 nodes)
- For larger graphs, approximate algorithms (A*) can be used
- Documented as a known limitation

### 3. Node Matching is String-Exact

**Issue:** GED uses exact string matching for nodes. "freedom" and "Freiheit" are treated as completely different.

**Impact:** Cross-lingual comparison requires pre-aligned concept names.

**Mitigation:**
- Concepts are extracted in their native language
- Translation pairs are defined for comparison
- Future work: semantic node matching

## Data Limitations

### 4. Small Sample Size

**Issue:** Planned sample is 15-30 participants (5 per language group).

**Impact:** Limited statistical power, results may not generalize.

**Mitigation:**
- Within-subject design (same person, 3 languages)
- Effect size analysis (Cohen's d)
- Power analysis to justify sample size
- Acknowledged as a limitation in the report

### 5. Language-Culture Confound

**Issue:** Chinese, German, and English speakers may differ culturally, not just linguistically.

**Impact:** LDS may measure cultural differences, not pure language effects.

**Mitigation:**
- Control for bilingual participants
- Compare asymmetric pairs (AB vs BC vs CA)
- Reference converging evidence from fMRI studies (Nature 2026)

### 6. Question Domain Specificity

**Issue:** Results are limited to the 5 question topics chosen (freedom, knowledge, time, identity, society).

**Impact:** May not generalize to other domains.

**Mitigation:**
- Questions chosen to cover abstract, social, cognitive, emotional domains
- Future work: expand to 20+ question types

## Threats to Validity

### Internal Validity
- Concept extraction consistency across languages
- Graph construction reproducibility

### External Validity
- Sample representativeness (students at one school)
- Cultural generalizability

### Construct Validity
- Does LDS actually measure "language drift"?
- Alternative explanation: LLM extraction artifacts

## Future Improvements

1. Semantic node matching (not string-exact)
2. Larger sample (100+ participants)
3. More languages (add French, Spanish, Japanese)
4. Automated baseline comparison
5. Integration with neural evidence (fMRI/EEG)
