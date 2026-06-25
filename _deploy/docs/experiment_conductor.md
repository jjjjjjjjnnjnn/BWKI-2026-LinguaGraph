# LinguaGraph — Experiment Conductor's Manual

> This is the FINAL document. No new code, no new concepts, no new corpus.
> From here, only humans and data collection move the project forward.

---

## What Exists (Complete Infrastructure)

| Component | Script | Status |
|-----------|--------|--------|
| **300 Simulation Baseline** | `scripts/simulate_baseline.py` | Template ready, fill with `--batch 1/2/3 --pipeline` |
| **Pilot Analysis** | `scripts/analyze_pilot.py` | `python analyze_pilot.py --data data/pilot_responses.json` |
| **Annotator Agreement** | `scripts/annotator_agreement.py` | `python annotator_agreement.py --annotator_a ... --annotator_b ... --report` |
| **Human vs Model** | `scripts/compare_human_vs_model.py` | `python compare_human_vs_model.py --report` |
| **BWKI Final Analysis** | `scripts/bwki_analysis.py` | Produces three-way table + correlation |
| **Cognitive City Data** | `research/visualization/cognitive_cities_v2.json` | Ready for Three.js |
| **Consent Forms** | `docs/ethics/*.md` | Fill [Name] [Email], print, sign |

---

## What You Do Next (In Order)

### Step 1: Fill In Paperwork (20 min)
- Edit `docs/ethics/consent_zh.md`, `consent_de.md`, `consent_en.md`
- Replace `[Name]` and `[Email]` with your real info
- Print enough copies for 30 participants + parents

### Step 2: Launch Google Form (30 min)
- Questions are in: `data/questionnaires/` and `docs/questionnaire_validation.md`
- Use the bias-corrected versions from the validation doc
- Add a "Language" section at the start

### Step 3: Recruit 9 People for Pilot (1-3 days)
- 3 Chinese native, 3 German native, 3 English native
- NOT trilingual — this is the control comparison
- Each answers in their NATIVE language only

### Step 4: Run Pilot Analysis (30 min)
```bash
python scripts/analyze_pilot.py --data data/pilot/pilot_responses.json --report
```
- Fix any survey issues found
- Update questionnaire if needed

### Step 5: Generate 300 Simulation Baseline (with LLM running)
```bash
python scripts/simulate_baseline.py --batch 1
python scripts/simulate_baseline.py --batch 2
python scripts/simulate_baseline.py --batch 3
python scripts/simulate_baseline.py --pipeline
```

### Step 6: Recruit 30 for Full Experiment (1-2 weeks)
- Partner handles WeChat + school mailing lists
- Each participant answers 5 questions × 3 languages (within-subject)

### Step 7: Second Annotator (parallel with Step 6)
- Give them `docs/annotation_guideline_v2.md`
- Both annotate 20 same responses
- Run: `python scripts/annotator_agreement.py --annotator_a ... --annotator_b ... --report`
- Target: κ ≥ 0.70

### Step 8: Run Full Analysis
```bash
python scripts/bwki_analysis.py --export-figures
```
- This fills the three-way table: Internet LDS | Model LDS | Human LDS

### Step 9: Three.js Cognitive City
- Give Mimo: `research/visualization/cognitive_cities_v2.json`
- Show three cities side by side

### Step 10: Creative Submission (June 28!)
- Use `docs/creative_submission.md` for the 150-word abstract

---

## The Three-Way Table (What BWKI Judges Will See)

After steps above, this table fills automatically:

```
| Concept   | Internet LDS | Model LDS | Human LDS |
|-----------|-------------|-----------|-----------|
| Success   | 0.97        | 0.79      | 0.76      |
| Freedom   | 0.81        | 0.68      | 0.66      |
| Home      | 0.31        | 0.28      | 0.24      |
                                r = 0.82
```

This table is worth more than any additional corpus expansion.

---

## Frozen Items (Do Not Touch)

- [LOCKED] LDS/LCD algorithm
- [LOCKED] Pipeline architecture
- [LOCKED] Corpus expansion (Wikipedia/Reddit/Quora)
- [LOCKED] New concept topics
- [LOCKED] New metric development
- [LOCKED] Analysis module creation

---

## Active Items (Let Humans Handle)

- [HUMAN] Participant recruitment
- [HUMAN] Google Form distribution
- [HUMAN] Consent form signing
- [HUMAN] Second annotator training
- [HUMAN] Pilot response collection
- [HUMAN] Three.js Cognitive City (Mimo)

---

## Files Referenced

| Purpose | File |
|---------|------|
| This manual | `docs/experiment_conductor.md` |
| Creative submission | `docs/creative_submission.md` |
| Ethics package | `docs/ethics/` |
| Questionnaire validation | `docs/questionnaire_validation.md` |
| Annotation guideline | `docs/annotation_guideline_v2.md` |
| BWKI paper outline | `docs/bwki_paper_outline.md` |
| Simulation protocol | `docs/simulation_protocol.md` |
| Project log | `docs/PROJECT_LOG.md` |
| Pilot analysis | `scripts/analyze_pilot.py` |
| Annotator agreement | `scripts/annotator_agreement.py` |
| Model comparison | `scripts/compare_human_vs_model.py` |
| BWKI analysis | `scripts/bwki_analysis.py` |
| Simulation generator | `scripts/simulate_baseline.py` |
| Cognitive City data | `research/visualization/cognitive_cities_v2.json` |
| Research rules | `research/RESEARCH_RULES.md` |
| DB (empty, awaiting data) | `linguaGraph.db` |
