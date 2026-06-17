# Gate Review Layer 1: Scientific Method Audit

**Date**: 2026-06-17
**Reviewer**: Senior Research Methodology Reviewer
**Scope**: Deep audit of 5 specific methodological risks in the LinguaGraph BWKI 2026 project

---

## Risk 1: LDS Circular Reasoning

### Severity: HIGH

### Evidence

**Defining claim** (`docs/methodology.md:7-10`):
```
LDS(L1, L2) = 1 - mean(GED_sim, Jaccard_node, Jaccard_edge)
```
LDS is defined as "how differently two languages organize the same conceptual space."

**Actual implementation** (`src/scoring.py:93-135`):
`calculate_lcd_score` does NOT compute the formula declared in methodology.md. It computes only edge-set Jaccard:
```python
similarity = len(intersection) / max(len(union), 1)
lcd = 1 - similarity
```
No GED similarity, no node Jaccard averaging. The implementation is a strict subset of the declared metric. If the declared three-component formula were implemented, node Jaccard alone (`src/compare.py:147`) would inflate similarity artificially since shared high-frequency vocabulary (e.g., "society", "individual") would create node overlap even when relational structures differ.

**Independent validation is absent.** No file in `src/` or `scripts/` computes LDS against an external baseline (e.g., human similarity judgments, known translation difficulty, or behavioral measures). The only validation path is internal: LDS(L1, L2) vs. LDS(L1, L3) vs. LDS(L2, L3), which is purely circular.

**Falsifiability problem**: What would falsify LDS? Consider a concrete scenario:
- A trilingual student writes structurally identical answers in all three languages, but uses different vocabulary in each (synonyms, paraphrases).
- Under the current `calculate_lcd_score`, the different words produce different nodes, so edge overlap drops, producing a "high drift" score.
- But the claim is that LDS measures *cognitive* drift, not *vocabulary* drift. The metric cannot distinguish between "genuinely different cognitive organization" and "same thought expressed in different words."

Conversely, if the LLM extractor normalizes concepts aggressively (mapping synonyms to canonical IDs via `normalize_concepts` in `src/extract.py:167-208`), it can *artificially inflate* similarity, producing a "low drift" score even when responses are cognitively different. Both failure modes are possible, and neither is testable within the current design.

### Impact

For BWKI submission: The core metric is vulnerable to the criticism that it measures *lexical surface form overlap*, not *cognitive structure*. A reviewer at the BWKI level (Jugend forscht / Jugend forscht) will note that:
- "Graph similarity" and "cognitive drift" are treated as the same thing, which is definitional, not empirical.
- There is no experiment that could disprove LDS — it is a tautology: "We define drift as graph distance, measure graph distance, and conclude there is drift."
- The mismatch between `docs/methodology.md` (3-component formula) and `src/scoring.py` (edge-Jaccard only) creates an reproducibility failure if a jury member reads the documentation and checks the code.

### Fix Cost: Medium

### Fix Suggestion

1. **Align implementation with documentation**: Either implement the full 3-component LDS formula (GED + node Jaccard + edge Jaccard) in `src/scoring.py`, or update `docs/methodology.md` to reflect what is actually computed. The current mismatch is a reproducibility failure.

2. **Add a linguistic control experiment**: Create a parallel corpus where the same semantic content is expressed in different words within the same language (e.g., formal vs. informal paraphrases). Compute LDS on these paraphrases. If LDS is a valid measure of *cognitive* drift (not *lexical* drift), same-language paraphrases should produce LDS near 0. If they produce LDS > 0.3, the metric measures vocabulary overlap, not cognition.

3. **State the falsification condition explicitly**: Define in `docs/methodology.md` what empirical observation would constitute evidence *against* LDS validity. Without this, the metric is unfalsifiable by design.

---

## Risk 2: Concept Mapping Bias

### Severity: CRITICAL

### Evidence

**30 shared concept IDs are researcher-imposed** (`config/cross_language_mapping.json:1-38`). Each mapping groups zh/de/en terms under a single researcher-chosen ID. Examples:

| Shared ID | ZH | DE | EN | Problem |
|-----------|-----|-----|-----|---------|
| `equality` | 平等, 公平 | Gleichheit | equality, fairness | ZH 公平 maps to both "equality" AND "justice" IDs (line 7 vs. line 29) |
| `justice` | 公正, 正义 | Gerechtigkeit | justice | `config/normalization_map.json:11-12` maps 公正→公平 and 正义→公平, collapsing justice into fairness |
| `family` | 家庭, 家 | Familie, Heimat | family, home | `social_issues_graph.py:31` assigns "Heimat" to 家庭, but validation doc says Heimat is untranslatable |
| `security` | 安全, 秩序 | Sicherheit, Ordnung | security, order, protection | Collapses order (秩序/Ordnung) with safety (安全/Sicherheit) — distinct concepts in political theory |
| `domination` | 统治, 压迫 | Herrschaft, Unterdrückung | domination, slavery, oppression | "Slavery" under "domination" ID skips a critical distinction |

The questionnaire validation doc itself warns about this:
- `docs/questionnaire_validation.md:27`: "『Heimat』has no ZH translation. 『家』and 『home』are not synonyms. The three prompts ask fundamentally different things" — rated CRITICAL severity
- `docs/questionnaire_validation.md:38`: "『公平』maps to both 'fairness' and 'justice'. EN uses 'justice' which is more formal/philosophical"
- `docs/questionnaire_validation.md:182-221`: Full page documenting that the "Home" question has a "CRITICAL TRANSLATION ISSUE" and "fundamental conceptual asymmetry"

**The mapping encodes the expected conclusion**. For example:
- The researcher's hypothesis (`research/questionnaire_hypotheses.md:16`) expects Chinese responses to "cluster around 努力+家庭+责任". The mapping (`cross_language_mapping.json:23`) maps 责任 to `responsibility` ID. The normalization map (`normalization_map.json:38`) maps `responsibility` → `responsibility` (identity). So if a Chinese participant writes 责任 and a German participant writes Verantwortung, both are mapped to the SAME canonical node `responsibility` — making them appear as "shared concepts" and thus reducing LDS.
- Conversely, if a Chinese participant writes 集体 (collective) and an English participant writes "individual", the mapping (`cross_language_mapping.json:6`) maps 集体→`society` ID (line 12), and individual→`individual` ID (line 8). Different IDs → different nodes → LDS increases. But whether this difference is cognitive or linguistic is indeterminate: the mapping *assumes* the concepts are different by placing them under different IDs.

**Cross-contamination between mapping files**: `config/normalization_map.json:11-12` maps 公正→公平 and 正义→公平, which are then looked up in the cross_language_mapping where 公平 maps to `equality` ID. But the correct mapping for 正义/justice should arguably be the `justice` ID. This causes a systematic mapping error where Chinese justice-related terms are assigned to `equality` rather than `justice`.

### Impact

For BWKI submission: The concept mappings are researcher-imposed and encode the very cultural-linguistic assumptions the study claims to discover. If the null hypothesis is "the concepts are the same across languages," the mapping already assumes that by grouping them. A jury will identify this as circular: the study cannot discover cultural differences in concepts when the measurement framework pre-defines which concepts are "the same."

The "Heimat ≠ 家 ≠ home" problem (self-diagnosed CRITICAL in the validation doc) is the most visible vulnerability. If this reaches the jury, it undermines all other mapping claims.

### Fix Cost: Medium

### Fix Suggestion

1. **Conduct a free-listing pilot**: Before fixing the mapping, collect free associations from native speakers of each language (e.g., "What words come to mind when you hear 公平? Gerechtigkeit? Fairness?"). Use the resulting co-occurrence data to derive concept clusters empirically rather than imposing them. This is standard practice in cross-cultural cognitive anthropology (Romney et al., 1986; Weller & Romney, 1988).

2. **Remove the "Heimat" question** or reframe it as a qualitative meta-analysis of translation difficulty, not as a comparable LDS data point. The current approach maps Heimat→`family` ID, which is indefensible.

3. **Document mapping uncertainty**: Add confidence scores for each mapping pair, reflecting whether the mapping is literal (高→high) or culturally contested (fairness→justice). Flag the contested mappings in all downstream LDS analyses.

4. **Sensitivity analysis**: Recompute LDS twice — once with the current mapping, once removing the 5 most contested mappings. Report both. If results flip, the mapping is driving the conclusion.

---

## Risk 3: Questionnaire Construct Validity

### Severity: HIGH

### Evidence

**The questionnaire is not validated for measuring cognitive differences.** The 5 topics (freedom, justice, success, responsibility, family/home) are chosen based on pilot LDS values from Wikipedia corpus analysis (`research/questionnaire_hypotheses.md:15`): "LDS = 0.269 (highest among all topics)." This means the questionnaire topics are selected *post hoc* based on the very metric being validated — a selection bias.

**Multiple plausible confounds are unmeasured**:

- **Education level / academic vocabulary**: `data/questionnaires/questionnaire_en.json:20` asks "How do you define success?" — the verb "define" is flagged as academic vocabulary by the project's own validation doc (`docs/questionnaire_validation.md:17`: "B1-level vocabulary check needed"). A participant who has taken philosophy classes will write a more elaborate response, producing more graph nodes, which changes LDS. The questionnaire measures educational exposure, not cognitive structure.

- **Self-censorship**: `docs/questionnaire_validation.md:107`: "Self-censorship: Participants may avoid sensitive political statements." The freedom and justice questions touch on politically sensitive topics. Chinese participants may self-censor on topics like 自由 (freedom) and 民主 (democracy), while German participants face no such pressure. This produces asymmetric response richness, which the graph-based LDS will detect as "drift" — but the drift is caused by censorship, not cognition.

- **Language proficiency confound**: Chinese participants at a German school (target population) are asked to answer in German for the DE questionnaire. A participant with B1 German will write shorter, simpler responses with fewer concepts and relations. The LDS between their ZH response (elaborate, concepts in Chinese) and DE response (short, limited vocabulary) will be high. This drift reflects language proficiency, not cognitive reorganization.

- **No control questions for convergent/divergent validity**: The questionnaire has no items that should produce LOW LDS across all participants (e.g., "What is water? / 什么是水? / Was ist Wasser?") as a baseline measure. Without control questions, any observed LDS could be attributed to any aspect of language difference, not specifically cognitive structure.

**Construct validity matrix is absent**: There is no demonstration that:
- Responses from participants who share the same native language converge (within-group similarity)
- The 5 topics are tapping a single construct of "cognitive organization" (internal consistency)
- LDS correlates with theoretically related constructs (convergent validity, e.g., behavioral measures of cultural cognition)
- LDS does NOT correlate with theoretically unrelated constructs (divergent validity, e.g., digit span memory)

### Impact

For BWKI submission: The construct validity defense is weak. A jury member will ask: "How do you know you're measuring cognitive structure and not language proficiency / educational level / self-censorship?" Without control questions or validated scales, the answer is "we don't."

The selection of high-LDS topics from Wikipedia corpus data and then testing human participants on those same topics creates an expectation confirmation loop: the investigation is designed to find differences where the researcher already knows differences exist.

### Fix Cost: Medium

### Fix Suggestion

1. **Add control questions**: Include at least 2 concrete, universal topics where LDS should be near 0 (e.g., "What is water? / 什么是水? / Was ist Wasser?" and "What is the color of the sky? / 天空是什么颜色? / Welche Farbe hat der Himmel?"). If these also show LDS > 0.2, the metric is measuring confounds (language proficiency, response style, etc.), not cognitive drift.

2. **Demographic covariates**: Already recommended in the validation doc (`docs/questionnaire_validation.md:233`) but not yet implemented in the actual questionnaire JSON files. Add: years abroad, self-rated proficiency in each language, age group, frequency of discussing the topics.

3. **Thematic analysis triangulation**: For a subset of responses, conduct blind thematic analysis (annotators unaware of language) to identify whether the *content* of responses differs qualitatively by language, not just the graph structure.

4. **Remove or flag the "define" verb** from Q3 across all languages, as per the validation doc's own recommendation.

---

## Risk 4: Training Data Contamination

### Severity: HIGH

### Evidence

**Exact overlap between Wikipedia corpus and LLM training data**: The corpus files in `data/corpus/` contain verbatim Wikipedia articles:
- `data/corpus/freedom/en_freedom_wikipedia.txt`: Exact text from English Wikipedia "Freedom" page
- `data/corpus/freedom/zh_自由_wikipedia.txt`: Exact text from Chinese Wikipedia "自由" page
- `data/corpus/freedom/de_freiheit_wikipedia.txt`: Exact text from German Wikipedia "Freiheit" page

All are licensed CC-BY-SA and retrieved 2026-06-17 (`:3`).

**The contamination has two forms:**

1. **Wikipedia corpus → human LDS expectation**: The corpus LDS computed from these articles is used as the "expected" drift pattern (via `student_id='WIKIPEDIA_CORPUS'` in `scripts/bwki_analysis.py:42-45`). The research hypotheses in `research/questionnaire_hypotheses.md` are directly derived from these corpus LDS values (e.g., H1: "LDS = 0.269 (highest among all topics)").

2. **Wikipedia corpus → LLM simulation**: The simulation script (`scripts/simulate_baseline.py`) uses LLM (likely GPT-4, Qwen, or similar) to generate simulated human responses. These LLMs were trained on internet text that includes the Wikipedia article corpus. The EXACT same Wikipedia articles used for "corpus analysis" were likely in the LLM training data.

This creates a **triple contamination loop**:
```
Wikipedia articles (in LLM training data)
    → used for corpus LDS calculation
    → corpus LDS → research hypotheses
    → same LLM generates simulation responses
    → simulation LDS compared to human LDS
    → conclusion: "LLM captures human cognitive patterns"
```

**Evidence of the problem in the simulation design** (`scripts/simulate_baseline.py:67-74`):
The simulation generates responses for the SAME 5 topics (freedom, justice, success, responsibility, home) using the SAME questions as the human questionnaire. The LLM "remembers" Wikipedia content on these topics and may reproduce its conceptual structure, making simulation LDS artificially close to Wikipedia corpus LDS.

**The language distribution imbalance in the corpus** (`docs/corpus-status.md:42-44`) further compounds the problem:
- English: 1556 files (99.7%)
- Chinese: 5 files (0.3%)
- German: 1 file (0.1%)

The LLM has been trained on vastly more English content than Chinese or German. This means LLM-generated English responses naturally exhibit richer concept association (more nodes, denser graphs from more training data), while Chinese and German responses are sparser. The LDS between en-zh or en-de will be inflated by this training data imbalance, and the inflation will be labeled as "cognitive drift."

### Impact

For BWKI submission: This is the most technically complex vulnerability but also the most defensible if properly addressed. The key risk is the circular reasoning chain:

> "We analyzed Wikipedia articles (written in English, Chinese, German) and found LDS differences. We then used a model trained on Wikipedia to simulate human responses. The simulation reproduces the LDS pattern. This proves human cognition is language-dependent."

A jury member with ML background will identify that the simulation and corpus analyses share a data source (Wikipedia). The "replication" of corpus LDS by model LDS is expected, not surprising — both are drawing from the same underlying text distribution.

### Fix Cost: Medium

### Fix Suggestion

1. **Replace Wikipedia corpus with a non-LLM-training source**: Use pre-LLM-era text (e.g., Project Gutenberg books published before 2010, pre-2015 newspaper archives) or controlled text that is known to be OUTSIDE the LLM training distribution. If LDS from this held-out corpus still correlates with human LDS, the claim is stronger.

2. **Compute corpus LDS from parallel translation corpus**: Instead of unrelated Wikipedia articles, use a genuine parallel corpus (e.g., EU parliament debates translated into all languages). This controls for content while varying language, isolating the language effect.

3. **Ablation analysis**: Document which LDS values survive when corpus contribution is removed. If human LDS correlates with model LDS but NOT with Wikipedia corpus LDS, the claim is robust. Currently all three are expected to correlate because they share data sources.

4. **Acknowledge explicitly in the BWKI submission**: State: "The simulation model was trained on data that includes Wikipedia articles on these topics. The corpus analysis also uses Wikipedia. This overlap means model-corus correlation is inflated." Then argue for the independent contribution of human data.

---

## Risk 5: Data Leakage in Human vs Simulation Comparison

### Severity: MEDIUM

### Evidence

**The DB queries appear clean** (`scripts/compare_human_vs_model.py:36-57`):
- Human data explicitly excludes `source='simulation'` and `source='gold_import'`
- Simulation data is filtered by `student_id='SIMULATION'`
- Wikipedia data is filtered by `student_id='WIKIPEDIA_CORPUS'`

**However, there are three subtler leakage paths:**

**Leakage Path A — Same LLM extractor for both human and simulation data**:
`scripts/analyze_student.py:133`:
```python
extracted = extract_concepts(combined_text, language=lang, use_mock=use_mock)
```
This function is called for BOTH human students and simulation data (via `run_pipeline_on_simulation` in `simulate_baseline.py:449`). The same LLM-based extraction pipeline with the same system prompt, the same normalization map, and the same relation extraction logic processes both datasets.

If the extraction LLM has a systematic bias (e.g., it consistently extracts "rights" from English freedom responses but "duty" from Chinese freedom responses), that bias will appear in BOTH human-derived graphs and simulation-derived graphs. The resulting LDS correlation between human and simulation data will partly reflect extraction bias, not genuine cognitive similarity.

**Leakage Path B — Persona stereotypes encode expected results**:
`scripts/simulate_baseline.py:46-63` defines personas with culturally stereotyped descriptions:
- ZH persona: "Collectivist cultural background... Naturally expresses concepts through relationships and social context."
- DE persona: "Individualist cultural background with strong philosophical tradition... Naturally expresses concepts through principles, systems, and categorical distinctions."
- EN persona: "Individualist cultural background emphasizing personal choice and opportunity... Naturally expresses concepts through individual agency, rights, and practical outcomes."

These persona prompts explicitly instruct the LLM to produce the exact patterns the research hypothesizes (see `research/questionnaire_hypotheses.md:16` for ZH: "Chinese texts emphasize effort/family/collective achievement"). The LLM complies — it generates Chinese responses that are collectivist and German responses that are philosophical.

The simulation then produces "high drift" between ZH and DE responses. This drift is then compared to human drift and interpreted as "the model captures human cognitive patterns." But the model was explicitly told to produce those patterns. This is not a discovery; it's stereotype enactment.

**Leakage Path C — Same normalization and graph pipeline**:
The normalization map (`config/normalization_map.json`) and concept mapping (`config/cross_language_mapping.json`) are applied identically to both human and simulation data via `normalize_concepts` in `src/extract.py:167-208`. The same mapping biases (Risk 2) affect both datasets equally, artificially aligning the comparison.

**The mock extraction mode is non-functional for social issues**: In `src/extract.py:88-164`, the `_mock_extract` function only handles calculus vocabulary (derivative, integral, limit). It returns empty results for social issues responses. Since `analyze_student_responses` defaults to `use_mock=True`, the pipeline may silently produce empty graphs for social issues data in mock mode. This needs verification — if empty graphs are being treated as "zero drift" (identical empty graphs), this would inflate similarity in both human and simulation results.

### Impact

For BWKI submission: The persona stereotype prompts (Leakage Path B) are the most visible problem. If a jury member reads the persona definitions and the hypothesis document side by side, they will see that the personas were designed to produce the expected results. The argument "our simulation confirms that LLMs capture human cognitive patterns" collapses when the simulation was explicitly instructed to produce those patterns.

The shared extraction pipeline (Leakage Path A) is a subtler issue but equally damaging if identified. In ML research, training/evaluation pipelines must be independent.

### Fix Cost: Low to Medium

### Fix Suggestion

1. **Remove cultural stereotypes from persona prompts** (`scripts/simulate_baseline.py:46-63`): Replace value-laden descriptions with neutral ones. For example:
   - CURRENT: "Collectivist cultural background. Family and social harmony are important reference points."
   - REPLACEMENT: "Native speaker of [language]. Participating in a survey about everyday concepts."
   
   If the simulation still produces cross-language LDS patterns that correlate with humans without the stereotype instructions, the finding is meaningful. If LDS disappears without the instructions, the original finding was artifact.

2. **Use different extraction models**: Extract concepts from simulation data using a different LLM than the one used for human data. Or better, use deterministic keyword-based extraction (the `_mock_extract` pattern) for BOTH, extended to handle social issues vocabulary. This eliminates shared extraction bias.

3. **Cross-source extraction audit**: As a sensitivity check, run a subset of human responses through the simulation-version extractor and vice versa. Confirm that extraction outputs are consistent regardless of which model version processes them. Report disagreements.

4. **Add ablation tests in `bwki_analysis.py`**: Add a mode that computes model-vs-human correlation WITH and WITHOUT persona stereotypes. Report both. If ρ drops significantly without stereotypes, the persona prompts were driving the result, not genuine cognitive modeling.

5. **Fix the mock extractor to support social issues** or change the default to `use_mock=False` with a warning. Currently, `analyze_student_responses` defaults to a mock mode that only works for calculus, creating a silent failure path for the actual study domain.

---

## Summary Table

| # | Risk | Severity | Key Evidence | Impact | Fix Cost |
|---|------|----------|-------------|--------|----------|
| 1 | LDS Circular Reasoning | HIGH | `src/scoring.py:122-126` implements edge-Jaccard only, not the declared 3-component formula; no falsification condition in `docs/methodology.md` | Core metric is definitional, not falsifiable; implementation misaligns with documentation | Medium |
| 2 | Concept Mapping Bias | CRITICAL | `config/cross_language_mapping.json:7-14` maps 公平 to both `equality` and `justice` IDs; `normalization_map.json:11-12` collapses 公正/正义 into 公平; `docs/questionnaire_validation.md:27` self-diagnoses Heimat ≠ 家 ≠ home as CRITICAL | Mapping pre-encodes expected conclusions; "Heimat" problem indefensible | Medium |
| 3 | Questionnaire Construct Validity | HIGH | `data/questionnaires/questionnaire_en.json:20` uses academic verb "define"; no control questions; no demographic covariates in questionnaire JSONs; selection of topics from corpus LDS values | Cannot distinguish cognitive differences from language proficiency / education / self-censorship | Medium |
| 4 | Training Data Contamination | HIGH | `data/corpus/freedom/en_freedom_wikipedia.txt:1-16` is verbatim Wikipedia content; same topics used for corpus LDS → hypothesis generation → simulation → human comparison; corpus is 99.7% English | Triple contamination loop; model-simulation correlation is inflated by shared Wikipedia training data | Medium |
| 5 | Data Leakage in Comparison | MEDIUM | `scripts/simulate_baseline.py:46-63` persona stereotypes encode expected cultural patterns; same LLM extractor processes both human and simulation data via `src/extract.py:31-85` | Persona prompts instruct LLM to produce expected results; shared extraction pipeline inflates correlation | Low to Medium |

---

## Cross-Cutting Recommendations

1. **Pre-register the analysis plan** before collecting human data. Specify: exact LDS formula, exclusions rules, statistical tests, and the minimum effect size considered meaningful. Currently, analysis is exploratory and risks capitalizing on chance.

2. **Blind the LLM extractor to language**: The extraction prompt in `src/extract.py:57` includes `Language: {language}`. This means the extractor knows which language it's processing and could theoretically adjust extraction behavior (e.g., extract more concepts from English, fewer from Chinese). Consider a language-agnostic extraction pipeline where the language parameter is used only for character encoding, not for extraction heuristics.

3. **Report the null distribution**: Simulate random responses (shuffled language labels) and compute LDS. If LDS from random data is > 0, the metric has a non-zero baseline. Report LDS as deviation from this baseline, not as absolute value.

4. **Address the 5-topic limitation**: With only 5 topics, the Spearman correlation in `scripts/compare_human_vs_model.py:125` operates on at most 15 data points (5 topics × 3 language pairs). This is insufficient for reliable correlation estimates. The script itself notes: "If n < 3, returns None (too few points)." At n=15, the confidence intervals are very wide (for ρ=0.5 with n=15, 95% CI is approximately [-0.02, 0.81]). Report confidence intervals alongside point estimates.

5. **Triangulate with at least one non-graph method**: Add lexical diversity analysis (type-token ratio), semantic similarity (cosine distance between response embeddings), or qualitative thematic coding as complementary measures. Currently, all conclusions depend on a single metric (LDS) with known circularity issues.

---

*End of Gate Review Layer 1. This review identifies methodological vulnerabilities that must be addressed before the BWKI submission. Risks marked CRITICAL would likely be identified by jury members with research methodology training and could significantly weaken the submission's scientific credibility.*
