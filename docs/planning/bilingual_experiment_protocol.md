# LinguaGraph — Bilingual Translation-Control Experiment Protocol
## Version 1.0 | 2026-06-25
## Status: Ready for data collection

---

## 1. Research Question

> Does the same person organize the same knowledge differently in different languages?

**Within-subject**: LDS(participant_i, topic_j, lang_A, lang_B) — measures the degree to which one person's conceptual structure changes when switching languages.

---

## 2. Design

### 2.1 Overall Design

| Dimension | Specification |
|-----------|---------------|
| Type | Mixed: within-subject (language) + between-subject (native language group) |
| N target | 30 (18 ZH-native, 6 DE-native, 6 EN-native) |
| Materials | 5 social topics × questionnaire languages |
| Measurement | LDS (Language Drift Score) per topic per language pair |
| Duration | ~15 minutes online |

### 2.2 Participant Groups

| Group | N | Native Lang | Language 1 | Language 2 | Language 3 |
|-------|:--:|:-----------:|:----------:|:----------:|:----------:|
| ZH+EN bilingual | 12 | ZH | ZH | EN | — |
| ZH+DE bilingual | 6 | ZH | ZH | DE | — |
| DE+EN bilingual | 4 | DE | DE | EN | — |
| EN+ZH bilingual | 4 | EN | EN | ZH | — |
| EN+DE bilingual | 2 | EN | EN | DE | — |
| DE+ZH bilingual | 2 | DE | DE | ZH | — |

**Within-subject comparisons available**:
- ZH-EN: 16 participants
- ZH-DE: 8 participants
- DE-EN: 6 participants

### 2.3 Power Analysis

```
Effect size (d) = 0.50 (based on pilot: mean LDS diff = 0.08, SD ≈ 0.1)
α = 0.05, power = 0.80 → n required = 27 per comparison

Available within-subject:
  ZH-EN: n=16  → power ≈ 0.60 (under-powered, but directionally informative)
  ZH-DE: n=8   → power ≈ 0.35 (exploratory)
  DE-EN: n=6   → power ≈ 0.28 (exploratory)

Between-subject (N=30 total):
  All pairs → power ≈ 0.80 for detecting d=0.50
```

**Interpretation**: Within-subject serves as directional validation. Between-subject with N=30 provides the primary statistical evidence.

---

## 3. Materials

### 3.1 Questionnaire

**5 Topics × Target Language**:

| # | Topic | ZH Question | DE Question | EN Question |
|---|-------|-------------|-------------|-------------|
| Q1 | Freedom | 什么是自由？请用自己的话解释。（写3-5句话，无正确/错误之分） | Was ist Freiheit? Erklären Sie in eigenen Worten. (3-5 Sätze, es gibt keine richtigen oder falschen Antworten) | What is freedom? Please explain in your own words. (Write 3-5 sentences. There are no right or wrong answers.) |
| Q2 | Justice | 什么是公平？一个公平的社会是什么样的？ | Was ist Gerechtigkeit? Wie sieht eine gerechte Gesellschaft aus? | What is justice? What does a just society look like? |
| Q3 | Success | 什么是成功？你如何定义成功的人生？ | Was ist Erfolg? Wie definieren Sie ein erfolgreiches Leben? | What is success? How do you define a successful life? |
| Q4 | Responsibility | 责任对你来说意味着什么？一个负责任的人是什么样的？ | Was bedeutet Verantwortung für Sie? Was macht einen verantwortungsvollen Menschen aus? | What does responsibility mean to you? What makes someone responsible? |
| Q5 | Home | "家"对你来说意味着什么？ | Was bedeutet "Heimat" für Sie? | What does "home" mean to you? |

### 3.2 Control Questions (Added to Assess Baseline Stability)

| # | ZH | DE | EN |
|---|----|----|----|
| C1 | 请描述一个普通的苹果。 | Beschreiben Sie einen gewöhnlichen Apfel. | Describe an ordinary apple. |
| C2 | 描述今天的天气。 | Beschreiben Sie das heutige Wetter. | Describe today's weather. |

**Expected**: Control LDS < 0.3 (concrete, universal concepts). If control LDS > 0.5 → method failure.

### 3.3 Counterbalancing

```
Randomize language order across participants using 6 permutations:
Perm 1: ZH → EN → (DE if applicable)
Perm 2: EN → ZH → (DE if applicable)
Perm 3: ZH → DE → (EN if applicable)
...
```

**Within-subject**: Latin square for language order. Topics always in same order (Q1→Q5).

### 3.4 Demographics Form

| Field | Type | Purpose |
|-------|------|---------|
| Age | Integer | Covariate (13-18 target) |
| Native language | Dropdown (ZH/DE/EN) | Group assignment |
| Other fluent languages | Multi-select | Group assignment |
| Years in Germany (if applicable) | Integer | Covariate for DE |
| Gender (optional) | M/F/NB | Descriptive stats |
| Self-rated proficiency (per language) | 1-5 Likert | Covariate |
| "How often do you discuss abstract concepts (freedom, justice, etc.)?" | 1-5 Likert | Topic familiarity covariate |

---

## 4. Procedure

### 4.1 Participant Flow

```
Recruitment → Consent → Demographics → Instructions → Block 1 (Lang A, Q1-Q5) → Break (30s) → Block 2 (Lang B, Q1-Q5) → Debrief
```

### 4.2 Instructions (All 3 Languages)

**ZH**:
"你将用不同的语言回答5个简短的开放性问题。请用指定的语言回答，不要翻译，而是用那种语言自然思考。写3-5句话。没有正确或错误的回答——我们感兴趣的是你个人如何思考这些概念。整个过程大约需要15分钟。"

**DE**:
"Sie werden 5 kurze offene Fragen in verschiedenen Sprachen beantworten. Bitte antworten Sie in der angegebenen Sprache — übersetzen Sie nicht, sondern denken Sie natürlich in dieser Sprache. Schreiben Sie 3-5 Sätze. Es gibt keine richtigen oder falschen Antworten — wir interessieren uns dafür, wie Sie persönlich über diese Begriffe denken. Die Bearbeitung dauert etwa 15 Minuten."

**EN**:
"You will answer 5 short open-ended questions in different languages. Please answer in the designated language — do not translate, but think naturally in that language. Write 3-5 sentences. There are no right or wrong answers — we are interested in how you personally think about these concepts. It takes about 15 minutes."

### 4.3 Debrief (Post-Completion)

"Have you ever noticed that you think differently about abstract concepts in different languages? This study measures exactly that effect. Thank you for your participation."

---

## 5. Data Handling

### 5.1 Storage

| Layer | Format | Location |
|-------|--------|----------|
| Raw responses | Google Form → JSON | `data/collected/raw_responses_YYYYMMDD.json` |
| Anonymized | student_id mapped | `linguaGraph.db` → `responses` table |
| Extractions | qwen-plus output | `linguaGraph.db` → `extractions` table |
| LDS results | JSON | `outputs/human_pilot_N30_lds.json` |

### 5.2 Anonymization

```
Real name → S### (sequential) with mapping file stored separately
Mapping file: NOT committed to git (in .gitignore)
```

### 5.3 Consent

- **Language**: Available in ZH, DE, EN
- **Content**: Purpose of study, data usage, right to withdraw, anonymity guarantee
- **Parental consent**: Required for participants under 18
- **Storage**: PDF → `data/consent/` (gitignored)

---

## 6. Analysis Pipeline

### 6.1 Extraction

```bash
# After data collection:
python scripts/extract_all_via_api.py \
  --source responses --filter "student_id LIKE 'S__'" \
  --model qwen-plus --batch-size 20
```

### 6.2 LDS Computation

```bash
# Within-subject:
python scripts/analyze_human_pilot.py --output outputs/human_pilot_N30_lds.json

# Between-subject:
python scripts/analyze_human_between.py --output outputs/human_between_N30_lds.json
```

### 6.3 Statistical Analysis

```python
# Core analyses:
# 1. Paired t-test: within-subject LDS vs 0.647 (simulation baseline)
# 2. Repeated-measures ANOVA: LDS ~ language_pair + topic
# 3. Spearman rank correlation: human LDS vs Wikipedia LDS
# 4. Linear mixed model: LDS ~ topic + (1|participant) + (1|language_pair)
# 5. Control check: control LDS < 0.3
```

---

## 7. Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Protocol finalization | 1 day | This document → final |
| OSF pre-registration | 1 day | Register hypotheses + analysis plan |
| Recruitment | 10-14 days | Schools, universities, online |
| Data collection | 10-14 days | Rolling as participants complete |
| Extraction | 1 day | Batch qwen-plus |
| Analysis | 2 days | All statistical tests |
| Paper update | 2 days | Replace N=8 data with N=30 |

**Total**: ~30 days from start to paper update.
