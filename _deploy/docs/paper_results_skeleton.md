# LinguaGraph — Full Paper Skeleton

> **Status:** Template · **Target:** BWKI 2026 Full Submission
> **Generated:** 2026-06-18
> **Pipeline:** `python scripts/run_pipeline.py` fills results automatically

---

## 1. Introduction

> *Brief context: Sapir-Whorf hypothesis, cognitive graph formalism, and the research question.*

### 1.1 Background
- Language-thought relationship (Sapir-Whorf / linguistic relativity)
- Prior work: Boroditsky (2001), Levinson (1996), Slobin (1996), Pavlenko (2005), Wierzbicka (1997)
- Gap: Quantifiable, reproducible cross-language cognitive comparison at the graph structure level

### 1.2 The LinguaGraph Approach
- From text responses → cognitive graphs → Language Drift Score (LDS)
- Three languages: Chinese, German, English
- Five conceptual domains: governance, individual, society, culture, economy
- **Technology reusability:** Core components (provider abstraction, quantization pipeline, LoRA adaptation) are framework-agnostic and have been extracted into a standalone runtime, demonstrating the project's value beyond a single experiment (see `docs/technology_transfer.md`)

### 1.3 Research Questions
- **RQ1:** Do speakers of different languages produce measurably different cognitive graphs when describing the same concepts?
- **RQ2:** Does LDS magnitude vary by topic (cultural vs universal domains)?
- **RQ3:** Can LLM-based concept extraction reliably reproduce human-annotated cognitive structures?

---

## 2. Related Work

> *Brief outline — full content in `docs/related_work.md`*

- Linguistic relativity and its empirical tests
- Cross-lingual semantic spaces (Conceptualizer, CCKG)
- Graph-based cognitive modeling
- LLM concept extraction for social science research

---

## 3. Cognitive Graph Framework

### 3.1 Graph Definition
A cognitive graph is a directed graph G = (V, E) where:
- **V** = concepts extracted from a participant's response (e.g., "freedom", "rights", "choice")
- **E** = semantic relations between concepts (e.g., implies, opposes, requires, is_a)
- Each response in language L produces one graph
- Graphs are compared within-participant across languages

### 3.2 Concept Taxonomy v1
30 shared concept IDs across 5 clusters, derived bottom-up from trilingual corpus co-occurrence:

| Cluster | Concepts | Color |
|---------|----------|:-----:|
| Governance & Politics | democracy, law, rights, power, revolution, liberalism, socialism, domination | #ef4444 |
| Individual & Freedom | freedom, individual, choice, autonomy, free_will, liberation, speech | #3b82f6 |
| Society & Collective | society, equality, justice, responsibility, security | #10b981 |
| Culture & Heritage | religion, philosophy, history, identity, tradition, education | #8b5cf6 |
| Economy & Development | economy, progress, success, family, reason | #f59e0b |

Cross-language mapping uses the taxonomy ID (not string matching), with fallback to edit-distance for out-of-taxonomy concepts.

### 3.3 Language Drift Score (LDS)

**Formula:**
```
LDS(L₁, L₂) = 1 − mean(GED_sim, Jaccard_node, Jaccard_edge)
```

**Components:**
- **GED_sim** (Graph Edit Distance similarity): `1 − GED(G₁, G₂) / max(|V₁|, |V₂|)`
  - Cost: node substitution = 1.0, insert/delete = 1.0, edge substitution = 0.5
  - Exact solution via NetworkX; O(n³) worst case, feasible for graphs < 15 nodes
- **Jaccard_node**: `|V₁ ∩ V₂| / |V₁ ∪ V₂|` — shared concept ratio
- **Jaccard_edge**: `|E₁ ∩ E₂| / |E₁ ∪ E₂|` — shared relation ratio

**Interpretation:**

| LDS Range | Interpretation |
|:---------:|:--------------|
| 0.0–0.3 | Low drift — similar cognitive organization |
| 0.3–0.7 | Moderate drift — notable structural differences |
| 0.7–1.0 | High drift — fundamentally different conceptual organization |

**Uncertainty quantification:**
- Bootstrap 95% CI: resample nodes with replacement (preserving edges per node), 1000 iterations
- Standard error reported alongside mean LDS

---

## 4. Methods

### 4.1 Participants

> *To be filled with final counts.*

| Language | Target N | Pilot N | Recruitment |
|:--------:|:--------:|:-------:|:------------|
| Chinese (ZH) | 10 | 8 | Chinese international students at German schools |
| German (DE) | 10 | _ | German classmates of ZH participants |
| English (EN) | 10 | _ | International school / online |

**Inclusion criteria:** Native or near-native speaker of the target language, age 10–18 (pilot: 10–55), written informed consent (parental consent for minors).

**Demographics collected:** Age group, native language, L2(s), L2 start age, years in Germany. No names, addresses, or other PII (fully anonymous protocol, GDPR Art. 6(1)(a)).

### 4.2 Instruments

#### Cognitive-Linguistic Battery (10 tasks)

| Dimension | Task | Cognitive Construct | LDS Prediction |
|-----------|------|-------------------|:--------------:|
| Semantic association | q8 — Time-related word association | Semantic network structure | Medium |
| Cultural schema | q9 — Explain "孝" (xiào) | Culturally-unique concept | High (ZH vs DE/EN) |
| Social cognition | q10 — Emotional reaction description | Social norm internalization | Medium |
| Spatial language | q11 — Vase picture description | Spatial frame of reference | Low–Medium |
| Cross-linguistic syntax | q12 — Translate motion event | Grammatical structure transfer | Moderate |
| Spatial language | q13 — Picture spatial description | Spatial frames (absolute/relative) | Low–Medium |
| Cross-linguistic syntax | q14 — Translate temporal concept | Temporal reasoning | Moderate–High |
| Spatial language | q15 — Picture exchange description | Perspective-taking | Low–Medium |
| Cross-linguistic syntax | q16 — Translate complex clause | Clause structure transfer | Moderate |
| Professional description | q17 — Describe a robot | Register-specific vocabulary | Low |

Each participant completes all 10 tasks in their native language (L1). Tasks are presented in randomized order to mitigate order effects. Each task is on a separate page/screen to prevent answer carryover.

#### Questionnaire Versions

Three per-language native versions were designed (not direct translations), each using culturally-appropriate examples:
- **ZH version:** Uses 孝 (xiào, filial piety) as the cultural concept example
- **DE version:** Uses Fernweh (wanderlust/yearning for distant places) as the cultural concept example
- **EN version:** Uses Privacy as the cultural concept example

### 4.3 Procedure

1. **Recruitment:** Participants recruited through partner schools and online channels
2. **Consent:** Written informed consent obtained (GDPR Art. 7); parental consent for minors (GDPR Art. 8)
3. **Questionnaire:** Self-administered, paper-based or digital (Google Forms), ~15 minutes per language
4. **Data storage:** Encrypted local storage, no cloud upload. Anonymized at collection (pseudonym IDs P001–P008 for pilot)
5. **Retention:** 12 months post-project, then permanent deletion (GDPR Art. 17)

### 4.4 Cognitive Graph Construction

**Pipeline:**
```
Response text → LLM concept extraction → Concept mapping → Graph building
```

1. **Extraction:** Each response is processed by an LLM (GPT-4.1-mini via pluggable `Provider` architecture) to extract:
   - Concepts (list of noun phrases and key terms)
   - Relations (typed edges: `implies`, `opposes`, `requires`, `is_a`, `has_part`, `similar_to`, `enables`)
2. **Normalization:** Extracted concepts are mapped to the Concept Taxonomy v1 (30 IDs) where possible; unmapped concepts retained via normalized string (lowercase, stemmed)
3. **Graph assembly:** NetworkX `DiGraph`; one graph per participant × language × topic
4. **Quality gate:** Graphs with < 3 nodes or < 2 edges flagged for review

**LLM Provider architecture:**
- Abstract `Provider` base class with `extract(text) → ExtractionResult`
- Concrete implementations: `GPTProvider` (OpenAI), `QwenProvider` (local), `MockProvider` (testing)
- Provider selected via config; fallback chain if primary unavailable

### 4.5 LDS Computation

For each participant with data in ≥ 2 languages:
1. Construct graphs G_ZH, G_DE, G_EN per topic
2. Compute pairwise LDS for each language pair (zh-de, zh-en, de-en)
3. Bootstrap CI: 1000 iterations, node-level resampling

**Software:** Python 3.11, NetworkX 3.x, NumPy, SciPy
**Reproducibility:** `python scripts/run_pipeline.py` regenerates all results from the database.

### 4.6 Statistical Analysis

> *Final inferential tests will be selected based on sample characteristics and assumption checks (normality, homogeneity of variance). The following plan is provisional.*

**Primary analysis:**
- LDS magnitudes reported as mean ± SD per language pair and topic
- Bootstrap 95% confidence intervals (1000 iterations) accompany all LDS estimates
- Cohen's d reported for pairwise language comparisons

**Inferential tests (to be determined):**
- If assumptions met (normal residuals, equal variance): mixed-design ANOVA (language pair × topic) with Tukey HSD post-hoc
- If normality violated: aligned rank transform ANOVA or Kruskal-Wallis test
- If unequal group sizes/sphericity violated: Welch ANOVA with Games-Howell post-hoc

**Multiple comparison correction:**
- 5 topics × 3 language pairs = 15 comparisons
- Benjamini-Hochberg FDR (q = 0.05) as primary; Bonferroni (α' = 0.05/15 = 0.0033) reported for sensitivity

**Power analysis (pre-registered):**
- Medium effect f = 0.25 (η² = 0.06), α = 0.05, power = 0.80
- Required: n = 18–20 per language group (G*Power: mixed ANOVA, between factors)
- Pilot: n = 8 (ZH) to verify effect direction; full study targets n = 30 (10 per language)

**Software:** Python 3.11 (SciPy, statsmodels), R 4.x (optional, for mixed ANOVA with `afex`)

---

## 5. Results (Production Pipeline)

All results are produced by a single command:

```bash
python scripts/run_pipeline.py
```

This generates:
- `results/tables/participant_summary.csv` — participant demographics
- `results/tables/table1_demographics.md` — Table 1: demographics by language
- `results/tables/table2_lds_by_topic.md` — Table 2: LDS by topic and language pair
- `results/tables/lds_report_template.md` — LDS report (with bootstrap CIs)
- `results/figures/figure1_lds_distribution.png` — LDS distribution by pair
- `results/figures/figure2_lds_heatmap.png` — Topic × language pair heatmap *(reserved when DE/EN arrives)*
- `results/figures/figure3_topic_comparison.png` — Topic comparison bar chart
- `docs/pilot_quality_report.md` — data quality assessment

---

## 6. Results

### 6.1 Dataset Overview

> *To be filled after pilot completes (ZH + DE + EN).*

**Participants:**
- Total N: [ZH: 8, DE: _, EN: _]
- Age range: 10–55 years (pilot)
- Recruitment: Partner schools (Chinese international students in Germany)

**Table 1: Participant Demographics**
```
Auto-generated: results/tables/table1_demographics.md
```

**Response Summary:**
| Language | Participants | Responses | Completion Rate |
|:--------:|:------------:|:---------:|:--------------:|
| ZH | 8 | 80 | 100% |
| DE | _ | _ | _ |
| EN | _ | _ | _ |

---

### 6.2 Cognitive Graph Construction

Cognitive graphs were constructed from extracted concepts and relations using NetworkX DiGraph. Each participant yields one graph per language × per topic.

**Graph Statistics (ZH Pilot):**

| Metric | Mean | SD | Min | Max |
|--------|:----:|:--:|:---:|:---:|
| Nodes per graph | | | | |
| Edges per graph | | | | |
| Graph density | | | | |

**Figure 1:** Example cognitive graph for one participant × topic. *[Three.js screenshot]*

---

### 6.3 Language Drift Score Analysis

> *Core result. Requires DE + EN data for cross-language comparison.*

**Table 2: Mean LDS by Language Pair**
```
Auto-generated: results/tables/table2_lds_by_topic.md
```

| Language Pair | Overall LDS | ZH-DE | ZH-EN | DE-EN |
|:-------------:|:-----------:|:-----:|:-----:|:-----:|
| Mean (SD) | | | | |
| 95% CI | | | | |

**Figure 2: LDS heatmap** *(reserved — generated when DE/EN data is available)*

**Table 3: LDS by Topic**

| Topic | ZH-DE | ZH-EN | DE-EN |
|-------|:-----:|:-----:|:-----:|
| Time Association | | | |
| Cultural Concept | | | |
| Spatial Description | | | |
| Translation | | | |
| Professional Description | | | |

**Key findings (to be filled):**
1. [Language pair] shows the highest LDS = _, suggesting _
2. [Topic] shows the most cross-language consistency with LDS = _
3. Bootstrap 95% CIs indicate [stable/unstable] estimates

---

### 6.4 Human Validation

**Extraction Quality (Gold Labels):**

| Metric | Value | Target |
|--------|:-----:|:------:|
| Concept Precision | | ≥ 0.80 |
| Concept Recall | | ≥ 0.80 |
| Concept F1 | | ≥ 0.80 |
| Relation Precision | | ≥ 0.70 |
| Relation Recall | | ≥ 0.70 |
| Relation F1 | | ≥ 0.70 |

**Annotator Agreement:**
- Cohen's Kappa: _ (target ≥ 0.70)
- Annotators: [names], both native speakers, trained on annotation guideline v2

**Data Quality (Pilot):**
- Completion rate: 100% (80/80 responses)
- Invalid responses flagged: 1 (P006 q12 — residual character contamination)
- Translation errors detected: 4/8 participants on q14 ("brought forward" temporal concept)
- Short answers (<5 chars): 8 (10.0%)
- Language-mixed answers: 7 (8.8%)

---

### 6.5 Limitations

1. **Intra-language variation may exceed inter-language variation.** Pilot data shows substantial differences even within ZH responses (e.g., P001 "漫长、延伸、短促" vs P008 "钟、表、太阳" for time association). Future work should quantify within-language vs between-language LDS variance.

2. **Sample size is exploratory.** N = 8 (ZH) + pending DE/EN. The full study targets N = 30 (10 per language) for adequate statistical power.

3. **Concept extraction quality depends on LLM.** Current pilot uses GPT-4.1-mini / Qwen3-8B. Extraction F1 on the social-issues domain should be validated against gold-standard annotations.

4. **Cross-language concept mapping is incomplete.** The current taxonomy covers 30 concepts; unseen concepts fall back to string matching, which may inflate LDS.

5. **Task order effects.** Pilot data shows one case of cross-question contamination (P006 q12), suggesting task ordering should be randomized in the full study.

6. **Translation tasks may measure language proficiency, not cognitive structure.** The "brought forward" misinterpretation by 4/8 participants could reflect English proficiency rather than cognitive organization. Future iterations should control for L2 proficiency.

7. **Cross-project technology transfer is early-stage.** The MML Runtime concept (see `docs/technology_transfer.md`) represents an architecture vision validated in prototype; production-grade extraction of shared components is planned post-BWKI. Preliminary tests confirm that the base GGUF model and quantization pipeline transfer without modification.

---

## 7. Discussion (Outline)

### 7.1 Interpretation of LDS Patterns

### 7.2 Comparison with Related Work

### 7.3 Implications for the Sapir-Whorf Hypothesis

### 7.4 Methodological Contributions

### 7.5 Technology Reusability

LinguaGraph's core infrastructure — provider abstraction, GGUF quantization, LoRA adaptation, structured extraction — was designed to be framework-agnostic. These components have been extracted into a conceptual **MML Runtime** (Minimal Model Loader) that can serve different task adapters.

An independent game project (reincarnation simulator, Godot 4) reuses the same runtime with a different LoRA adapter for NPC dialogue and narrative generation, confirming the architecture's generality.

See [`docs/technology_transfer.md`](technology_transfer.md) for the full architecture diagram, component mapping, and future WebGPU deployment roadmap.

---

## 8. Conclusion (Outline)

---

## Appendix

### A. Trilingual Questionnaire (Cognitive-Linguistic Battery v1)

#### English Version
| ID | Task | Prompt |
|:--:|:----:|:-------|
| q8 | Word Association | "What words come to mind when you think of 'time'?" |
| q9 | Cultural Concept | "What does 'privacy' mean to you?" |
| q10 | Emotional Reaction | "Describe a situation that made you feel proud and explain why." |
| q11 | Spatial Description | "Describe the image below. Focus on the spatial relationships between objects." |
| q12 | Translation (motion) | "Translate: Mike walked from the kitchen through the living room into the bedroom." |
| q13 | Spatial Description | "Describe this scene. Pay attention to where things are located." |
| q14 | Translation (temporal) | "Translate: The meeting was brought forward from Friday to Wednesday." |
| q15 | Spatial Description | "Two people are exchanging a book. Describe what you see." |
| q16 | Translation (complex) | "Translate: After the rain stopped, the children ran outside to play, but they forgot to take their umbrella." |
| q17 | Professional Description | "Describe what a robot does in 50–100 words. Write as if you are explaining it to a 12-year-old." |

#### German Version (equivalent prompts, culturally adapted)

| ID | Task | Prompt |
|:--:|:----:|:-------|
| q8 | Wortassoziation | "Welche Wörter fallen dir zum Wort 'Zeit' ein?" |
| q9 | Kulturelles Konzept | "Was bedeutet 'Fernweh' für dich?" |
| q10 | Emotionale Reaktion | "Beschreibe eine Situation, in der du stolz warst, und erkläre warum." |
| q11 | Raumbeschreibung | "Beschreibe das Bild unten. Achte auf die räumlichen Beziehungen zwischen den Gegenständen." |
| q12 | Übersetzung (Bewegung) | "Übersetze ins Deutsche: Mike walked from the kitchen through the living room into the bedroom." |
| q13 | Raumbeschreibung | "Beschreibe diese Szene. Achte darauf, wo sich die Dinge befinden." |
| q14 | Übersetzung (zeitlich) | "Übersetze ins Deutsche: The meeting was brought forward from Friday to Wednesday." |
| q15 | Raumbeschreibung | "Zwei Personen tauschen ein Buch aus. Beschreibe, was du siehst." |
| q16 | Übersetzung (komplex) | "Übersetze ins Deutsche: After the rain stopped, the children ran outside to play, but they forgot to take their umbrella." |
| q17 | Fachbeschreibung | "Beschreibe, was ein Roboter tut (50–100 Wörter). Schreib so, als würdest du es einem 12-Jährigen erklären." |

#### Chinese Version (equivalent prompts, culturally adapted)

| ID | Task | Prompt |
|:--:|:----:|:-------|
| q8 | 词语联想 | "提到'时间'，你会想到哪些词语？" |
| q9 | 文化概念 | "你认为'孝'是什么意思？" |
| q10 | 情绪反应 | "描述一个让你感到自豪的情景，并解释原因。" |
| q11 | 空间描述 | "描述下图。注意物体之间的空间关系。" |
| q12 | 翻译（动作） | "翻译成中文：Mike walked from the kitchen through the living room into the bedroom." |
| q13 | 空间描述 | "描述这个场景。注意东西的位置。" |
| q14 | 翻译（时间） | "翻译成中文：The meeting was brought forward from Friday to Wednesday." |
| q15 | 空间描述 | "两个人在交换一本书。描述你看到的场景。" |
| q16 | 翻译（复杂句） | "翻译成中文：After the rain stopped, the children ran outside to play, but they forgot to take their umbrella." |
| q17 | 专业描述 | "描述机器人的功能（50–100字）。用你能让12岁孩子听懂的方式写。" |

---

### B. Concept Taxonomy v1 (Full Table)

| ID | Cluster | ZH | DE | EN |
|:--:|:---------|:---|:---|:---|
| 01 | Governance | 民主 | Demokratie | democracy |
| 02 | Governance | 法律 | Gesetz | law |
| 03 | Governance | 权利 | Rechte | rights |
| 04 | Governance | 权力 | Macht | power |
| 05 | Governance | 革命 | Revolution | revolution |
| 06 | Governance | 自由主义 | Liberalismus | liberalism |
| 07 | Governance | 社会主义 | Sozialismus | socialism |
| 08 | Governance | 统治 | Herrschaft | domination |
| 09 | Individual | 自由 | Freiheit | freedom |
| 10 | Individual | 个体 | Individuum | individual |
| 11 | Individual | 选择 | Wahl | choice |
| 12 | Individual | 自治 | Autonomie | autonomy |
| 13 | Individual | 自由意志 | freier Wille | free_will |
| 14 | Individual | 解放 | Befreiung | liberation |
| 15 | Individual | 言论 | Rede | speech |
| 16 | Society | 社会 | Gesellschaft | society |
| 17 | Society | 平等 | Gleichheit | equality |
| 18 | Society | 公平 | Gerechtigkeit | justice |
| 19 | Society | 责任 | Verantwortung | responsibility |
| 20 | Society | 安全 | Sicherheit | security |
| 21 | Culture | 宗教 | Religion | religion |
| 22 | Culture | 哲学 | Philosophie | philosophy |
| 23 | Culture | 历史 | Geschichte | history |
| 24 | Culture | 认同 | Identität | identity |
| 25 | Culture | 传统 | Tradition | tradition |
| 26 | Culture | 教育 | Bildung | education |
| 27 | Economy | 经济 | Wirtschaft | economy |
| 28 | Economy | 进步 | Fortschritt | progress |
| 29 | Economy | 成功 | Erfolg | success |
| 30 | Economy | 家庭 | Familie | family |

---

### C. LDS Bootstrap Derivation

**Algorithm:** Node-based resampling with replacement, preserving edge topology.

```
For each language pair (L₁, L₂):
  1. Let G₁ = (V₁, E₁), G₂ = (V₂, E₂) be the two cognitive graphs
  2. For iteration b = 1 to 1000:
     a. Sample |V₁| nodes from V₁ with replacement → V₁*
        Retain all edges in E₁ whose source AND target are in V₁* → E₁*
     b. Same for V₂ → V₂*, E₂*
     c. Compute LDS* = 1 − mean(GED_sim(G₁*, G₂*), Jaccard_node(V₁*, V₂*), Jaccard_edge(E₁*, E₂*))
  3. Bootstrap CI: [LDS_2.5%, LDS_97.5%] percentile interval
```

**Properties:**
- Preserves graph topology (edges are tied to their nodes, not resampled independently)
- Accounts for node-level uncertainty (which specific concepts a participant expressed)
- Wider CIs = less stable LDS estimates (small graphs, sparse responses)

---

## References

> *Full bibliography maintained in `docs/related_work.md`*

1. Boroditsky, L. (2001). Does language shape thought? Mandarin and English speakers' conceptions of time. *Cognitive Psychology*, 43(1), 1–22.
2. Levinson, S. C. (1996). Frames of reference and Molyneux's question. In P. Bloom et al. (Eds.), *Language and space* (pp. 109–169). MIT Press.
3. Pavlenko, A. (2005). *Emotions and multilingualism*. Cambridge University Press.
4. Slobin, D. I. (1996). From "thought and language" to "thinking for speaking." In J. J. Gumperz & S. C. Levinson (Eds.), *Rethinking linguistic relativity* (pp. 70–96).
5. Talmy, L. (2000). *Toward a cognitive semantics*. MIT Press.
6. Wierzbicka, A. (1997). *Understanding cultures through their key words*. Oxford University Press.
7. Matsumoto, D. (1990). Cultural similarities and differences in display rules. *Motivation and Emotion*, 14(3), 195–214.
8. Lakoff, G., & Johnson, M. (1980). *Metaphors we live by*. University of Chicago Press.

---

*Template version: v2.0 · Generated 2026-06-18*
*Results filled automatically when DE/EN data arrives via `python scripts/run_pipeline.py`*
