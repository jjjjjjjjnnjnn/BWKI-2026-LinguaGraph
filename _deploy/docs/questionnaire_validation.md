# LinguaGraph Questionnaire Validation Report

> Human Study Preparation — Bias Audit & Annotation Specification
> Date: 2026-06-17

---

## 1. Bias Audit

### 1.1 Education Background Bias

| Risk | Severity | Affected Questions | Mitigation |
|------|----------|-------------------|------------|
| Academic framing ("define success") may favor university-track students | HIGH | Q3 (Success) | Rephrase: "How do you know if your life is going well?" instead of "define success" |
| Western philosophical tradition assumed (Plato, Kant, Rawls) | MEDIUM | Q2 (Justice), Q4 (Freedom) | Add instruction: "No philosophy knowledge needed — just your everyday understanding" |
| Abstract questioning may confuse younger participants (age 13-15) | MEDIUM | Q2-Q4 | Include example: "Like when you say 'that's not fair!' — what makes something unfair?" |
| Vocabulary difficulty: "accountability", "autonomy", "distributive" | HIGH | All | B1-level vocabulary check needed. Replace: "accountability" → "being responsible for what you do" |

**Recommendation**: Add B1-level equivalent phrasing for each question. Test with a 14-year-old before launch.

### 1.2 Cultural Knowledge Bias

| Risk | Severity | Affected | Mitigation |
|------|----------|----------|------------|
| Eurocentric framing of justice as legal procedure | HIGH | Q2 DE/EN | ZH version currently frames justice as social harmony — this is an advantage. DE/EN should be equally open |
| "Success" framed as individual achievement (Western bias) | HIGH | Q3 EN | EN version already uses "successful life" but needs explicit permission for non-material definitions |
| "Home" vs "Heimat" — false equivalence | CRITICAL | Q5 | "Heimat" has no ZH translation. "家" and "home" are not synonyms. The three prompts ask fundamentally different things |
| Assumption of democratic political context | MEDIUM | Q2, Q4 | Add: "based on your own experience" to all questions |
| Confucian values may be invisible to non-ZH annotators | MEDIUM | Q1 ZH | Annotation training must cover 孝 (filial piety) as a distinct concept |

**Recommendation**: The "Heimat" problem is critical. Either accept it as an untranslatable concept (which is itself interesting) or replace with a more equivalent topic (e.g., "Belonging").

### 1.3 Translation Bias

| Item | ZH Version | DE Version | EN Version | Discrepancy |
|------|-----------|------------|------------|-------------|
| Q1 | 什么是自由? 请用自己的话解释。 | Was ist Freiheit? Erklären Sie mit eigenen Worten. | What is freedom? Explain in your own words. | ✅ Good |
| Q2 | 什么是公平? 它和什么有关？ | Was ist Gerechtigkeit? Womit hängt sie zusammen? | What is justice? What is it related to? | ⚠️ "公平" maps to both "fairness" and "justice". EN uses "justice" which is more formal/philosophical |
| Q3 | 什么是成功? 你怎么定义成功？ | Was ist Erfolg? Wie definieren Sie Erfolg? | What is success? How do you define success? | ⚠️ "定义" (define) is academic. DE "definieren" equally academic. EN is same problem |
| Q4 | 家庭对你来说意味着什么？ | Was bedeutet Familie für Sie? | What does family mean to you? | ✅ Good |

**Detailed Analysis of Translation Issues**:

```
Q2 (Justice):
  ZH: 公平 = fairness, justice, equity (broad, everyday)
  DE: Gerechtigkeit = justice, fairness, righteousness (philosophical/legal)
  EN: justice = justice (formal, institutional)
  
  ⚠ Problem: ZH and DE versions allow broader everyday interpretations.
  EN version biases toward institutional/legal justice.
  
  Fix: EN Q2 should use "fairness" alongside "justice":
  "What is fairness/justice? What does a fair society look like?"

Q3 (Success):
  ZH: 你如何定义成功的人生？(How do you define a successful life?)
  DE: Wie definieren Sie ein erfolgreiches Leben?
  EN: How do you define a successful life?
  
  ⚠ Problem: "define" is an academic verb. In DE, "Sie" is formal.
  Participants may feel pressure to give dictionary definitions.
  
  Fix: "How do you know if someone's life is going well?"
  ZH: 你怎么知道一个人的生活过得好不好？
  DE: Woran erkennt man ein gutes Leben?
  EN: How can you tell if someone's life is going well?
```

---

## 2. Question-by-Question Validation

### Q1: Freedom / 自由 / Freiheit

**Measurement Target**:
- Concept set: Individual autonomy vs. social responsibility vs. political rights
- Relation: Strength of connection between "freedom" and "limits"
- Expected drift direction: ZH → responsibility-focused; DE → positive/negative liberty; EN → rights

**Extraction Target**:
| Construct | Keywords (ZH) | Keywords (DE) | Keywords (EN) |
|-----------|---------------|---------------|---------------|
| Individual autonomy | 个体, 个人, 自己 | Individuum, Selbst | individual, self |
| Rights | 权利, 人权 | Recht, Menschenrecht | rights, liberty |
| Responsibility | 责任, 义务 | Verantwortung | responsibility |
| Limits | 限制, 边界 | Grenze, Schranke | limit, boundary |
| Society | 社会, 集体 | Gesellschaft | society |

**Scoring Criteria**:
| Score | Meaning | Evidence |
|-------|---------|----------|
| 3 (Rich) | 5+ concepts with clear relations | Multiple connections between autonomy/responsibility/limits |
| 2 (Moderate) | 3-4 concepts, some relations | Mentions key concepts but limited structure |
| 1 (Thin) | 1-2 concepts, no clear relations | Single word or short phrase |
| 0 (Empty) | No meaningful content | "I don't know" or blank |

**Annotation Guideline**:
1. Extract ALL concepts the participant introduces (not just vocabulary from the question)
2. Mark relations ONLY when participant explicitly connects them (e.g., "freedom means you can choose, but you're also responsible")
3. Do NOT mark implied relations — only stated ones
4. For "missing hints": mark ONLY if the participant shows awareness of a gap (e.g., "I know freedom is important but I'm not sure why")
5. Language: annotate in the answer's language. Do NOT translate.

**Potential Confounds**:
- Political exposure: Participants from different educational systems may have different baseline knowledge of "rights" discourse
- Self-censorship: Participants may avoid sensitive political statements
- Age: Older participants (17-18) may have more nuanced views than younger ones (13-14)

---

### Q2: Justice / 公平 / Gerechtigkeit

**Measurement Target**:
- Concept set: Equality vs. fairness vs. law vs. distribution
- Relation: Connection between "justice" and "equality" (stronger in EN) vs. "justice" and "harmony" (stronger in ZH)
- Expected drift direction: ZH → social harmony/distribution; DE → procedural/law; EN → rights/opportunity

**Extraction Target**:
| Construct | Keywords (ZH) | Keywords (DE) | Keywords (EN) |
|-----------|---------------|---------------|---------------|
| Equality | 平等, 同等 | Gleichheit | equality |
| Fairness | 公平, 公正 | Gerechtigkeit, Fairness | fairness |
| Law | 法律, 法治 | Gesetz, Recht | law, legal |
| Distribution | 分配, 资源 | Verteilung | distribution |
| Opportunity | 机会, 可能 | Chance | opportunity |
| Harmony | 和谐, 和睦 | Harmonie? | harmony? |

**Scoring Criteria**: Same as Q1 (3/2/1/0 scale)

**Annotation Guideline**:
1. Distinguish between "fairness" (everyday) and "justice" (systemic) when possible
2. Note if participant explicitly mentions legal/formal systems vs. interpersonal fairness
3. For ZH: "公平" and "正义" are different — note which character the participant uses
4. For DE: Note if participant distinguishes between "Gerechtigkeit" (abstract) and "Fairness" (concrete)
5. For EN: Note if participant uses "justice" (institutional) or "fairness" (everyday)

**Potential Confounds**:
- Educational background: Students who have taken law/politics classes will use different vocabulary
- Media exposure: Crime news coverage varies significantly by country
- Personal experience: Participants who have experienced discrimination may have different frameworks

---

### Q3: Success / 成功 / Erfolg

**Measurement Target**:
- Concept set: Achievement vs. family/community vs. wealth/status vs. happiness
- Relation: Is success connected to "helping others" (ZH) or "personal achievement" (DE/EN)?
- Expected drift direction: ZH → family/effort/hard work; DE → career/competence; EN → opportunity/individual choice

**Extraction Target**:
| Construct | Keywords (ZH) | Keywords (DE) | Keywords (EN) |
|-----------|---------------|---------------|---------------|
| Achievement | 成就, 成绩 | Leistung | achievement |
| Effort/Hard work | 努力, 勤奋 | Anstrengung, Fleiß | effort, hard work |
| Family | 家庭, 家人 | Familie | family |
| Wealth | 财富, 钱 | Reichtum, Geld | wealth, money |
| Happiness | 幸福, 快乐 | Glück, Zufriedenheit | happiness |
| Career | 事业, 职业 | Karriere, Beruf | career |
| Competition | 竞争 | Wettbewerb | competition |
| Society/Others | 社会, 他人 | Gesellschaft, Andere | society, others |

**Scoring Criteria**: Same as Q1

**Annotation Guideline**:
1. Pay special attention to whether success is framed as individual or collective
2. Note any mentions of "balance" (work-life, material-spiritual) — this may be a ZH-specific dimension
3. For DE: German "Erfolg" in business context = financial result. In everyday use = achievement. Note which.
4. For ZH: "成功" often implies social recognition. Note if participant mentions 面 (face/social standing).

**Potential Confounds**:
- Socioeconomic background: Wealthy vs. struggling participants will have different success concepts
- Peer pressure: School environment (competitive vs. collaborative) strongly shapes success definitions
- Parental expectations: Strong confound for ZH participants with immigrant parents

---

### Q4: Home / 家 / Heimat

**⚠ CRITICAL TRANSLATION ISSUE**

This question has a fundamental conceptual asymmetry:

| Language | Word | Core Meaning |
|----------|------|-------------|
| ZH | 家 | Family, household, lineage (关系性) |
| DE | Heimat | Homeland, region of origin, cultural identity (地域性) |
| EN | Home | Physical dwelling, emotional safety, family (空间+情感) |

These three words do NOT map to the same concept. "Heimat" has no ZH equivalent. "家" has no DE equivalent. "Home" sits somewhere between but overlaps with neither fully.

**Measurement Target** (despite asymmetry):
- ZH: Family relationships, filial piety, lineage continuity
- DE: Regional/cultural belonging, nostalgia, rootedness
- EN: Physical safety, emotional comfort, personal space

**Extraction Target**:
| Construct | Keywords (ZH) | Keywords (DE) | Keywords (EN) |
|-----------|---------------|---------------|---------------|
| Family | 家人, 亲人, 父母 | Familie, Eltern | family, parents |
| Belonging | 归属, 属于 | Zugehörigkeit | belonging |
| Safety | 安全, 保护 | Sicherheit, Geborgenheit | safety, security |
| Tradition | 传统, 习俗 | Tradition, Brauch | tradition |
| Identity | 身份, 认同 | Identität, Heimat | identity |
| Love | 爱, 感情 | Liebe | love |

**Scoring Criteria**: Same as Q1

**Annotation Guideline**:
1. Do NOT try to map ZH "家" to DE "Heimat". Mark them separately
2. Note any mention of "missing" or "longing" — this may indicate home as absent/lost (common for ZH participants abroad)
3. For DE: "Heimat" is a politically loaded term in German discourse. Note if participant contextualizes it
4. For ZH: Note if participant distinguishes between "家" (family home) and "家" (hometown)

**Potential Confounds**:
- Migration status: ENTIRELY confounded for ZH participants in Germany. They may describe 家 as "where parents are" (China) and Heimat as "where I live now" (Germany)
- Age: Younger participants may not have developed a strong "Heimat" concept
- Duration abroad: For ZH participants, years in Germany directly affects both "家" and "Heimat" responses

**Recommendation**: Either (a) explicitly frame this as "the concept is NOT equivalent across languages — that's the point", or (b) replace with a more equivalent topic like "Belonging / 归属 / Zugehörigkeit"

---

## 3. Revised Questionnaire (Bias-Corrected Version)

| Original | Issue | Correction |
|----------|-------|------------|
| Q2 EN: "What is justice? What is it related to?" | Too abstract + institutional framing | "What is fairness? What does it mean to treat people fairly?" |
| Q3 all: "How do you define success?" | Academic verb "define" | "How can you tell if someone's life is going well?" |
| Q5: "What does home mean to you?" | Heimat ≠ 家 ≠ home | Add meta-question: "Is there a word in your native language that doesn't translate well?" |
| All: No demographic questions | Missing confounders | Add: age group, years abroad, self-rated language proficiency, discussion frequency of topics |

**Corrected Question Set**:

```
Q1 (Freedom):
  ZH: 什么是自由? 你觉得"自由"和什么有关系？
  DE: Was ist Freiheit? Was hat Freiheit Ihrer Meinung nach mit anderen Dingen zu tun?
  EN: What is freedom? What do you think freedom is connected to?

Q2 (Justice):
  ZH: 什么是公平? 什么叫"对人公平"？
  DE: Was ist Gerechtigkeit? Was bedeutet es, Menschen fair zu behandeln?
  EN: What is fairness? What does it mean to treat people fairly?

Q3 (Success):
  ZH: 你怎么知道一个人的生活过得好不好？什么样的人生算是好的人生？
  DE: Woran erkennt man ein gutes Leben? Was macht ein gelungenes Leben aus?
  EN: How can you tell if someone's life is going well? What makes a good life?

Q4 (Home):
  ZH: "家"对你来说意味着什么？说到"家"你会想到什么？
  DE: Was bedeutet "Heimat" für Sie? Woran denken Sie, wenn Sie das Wort hören?
  EN: What does "home" mean to you? What comes to mind when you think of "home"?

Q5 (Responsibility):
  ZH: "责任"对你来说意味着什么？什么样的人算是有责任感的人？
  DE: Was bedeutet "Verantwortung" für Sie? Was macht einen verantwortungsvollen Menschen aus?
  EN: What does "responsibility" mean to you? What makes someone responsible?
```

---

## 4. Annotation Specification

### 4.1 Annotator Requirements
- Minimum 2 annotators per response
- Each annotator must be a native or C1+ speaker of the answer's language
- Annotators should NOT know the research hypotheses
- Training: 5 practice annotations → compare → discuss → finalize

### 4.2 Annotation Workflow

```
Step 1: Read the full response
Step 2: Extract concepts (5-15 per answer)
Step 3: Extract relations (2-8 per answer)
Step 4: Mark missing hints (0-3 per answer)
Step 5: Rate quality (Rich/Moderate/Thin/Empty)
Step 6: Confidence rating for own annotation (1-5)
```

### 4.3 Inter-Annotator Agreement Targets

| Metric | Target | Minimum |
|--------|--------|---------|
| Concept Jaccard | ≥ 0.70 | ≥ 0.60 |
| Relation Cohen's κ | ≥ 0.65 | ≥ 0.50 |
| Quality rating agreement | ≥ 80% | ≥ 70% |

### 4.4 Annotation Schema (JSON)

```json
{
  "response_id": "R001_zh_q1",
  "annotator": "annotator_A",
  "concepts": ["自由", "个体", "权利", "责任", "社会", "选择"],
  "relations": [
    {"source": "自由", "target": "个体", "type": "belongs_to"},
    {"source": "自由", "target": "责任", "type": "implies"},
    {"source": "自由", "target": "权利", "type": "is_a"}
  ],
  "missing_hints": [],
  "quality_rating": "rich",
  "annotator_confidence": 4,
  "notes": "Participant made clear distinction between personal freedom and social responsibility"
}
```

### 4.5 Relation Types (Social Issues Domain)

| Type | Definition | Example |
|------|------------|---------|
| `is_a` | A is a type/example of B | "Freedom is a right" → freedom is_a right |
| `has_part` | A has B as a component | "Justice includes equality" → justice has_part equality |
| `implies` | A implies/leads to B | "Success requires effort" → success implies effort |
| `opposes` | A opposes/conflicts with B | "Freedom versus security" → freedom opposes security |
| `similar_to` | A is similar to B | "Fairness is like equality" → fairness similar_to equality |
| `enables` | A makes B possible | "Freedom enables choice" → freedom enables choice |
| `requires` | A needs B to exist | "Responsibility requires free will" → responsibility requires free will |

---

## 5. Quality Control

### 5.1 Response Quality Criteria

| Flag | Condition | Action |
|------|-----------|--------|
| `too_short` | < 20 words | Exclude from main analysis; include in sensitivity check |
| `off_topic` | Answer doesn't address question | Exclude; document reason |
| `language_mismatch` | Wrong language used | Tag; analyze separately |
| `copied` | Suspicious similarity to another response | Cross-check timestamps; exclude if confirmed |
| `valid` | ≥ 20 words, on topic, correct language | Include in analysis |

### 5.2 Data Exclusion Rules

1. Exclude participants who complete < 2/3 languages (minimum 2 of 3)
2. Exclude individual responses flagged `too_short` or `off_topic`
3. Do NOT exclude based on LDS outcome (no cherry-picking)
4. Report all exclusions in final paper with reasons

### 5.3 Privacy & GDPR Compliance

- No real names collected — use anonymous participant IDs
- Age grouped (13-15, 16-18) not exact age
- School name optional, not required
- Data stored locally (linguaGraph.db), not uploaded
- Participants can withdraw at any time; data deleted on request
- Consent form: `data/consent_form.md` — must be signed before participation

---

## 6. Summary of Recommended Changes

| Priority | Change | Reason | Impact |
|----------|--------|--------|--------|
| 🔴 CRITICAL | Fix Q2 EN: "justice" → "fairness/justice" | Translation bias | Changes EN questionnaire JSON |
| 🔴 CRITICAL | Fix Q3 all: remove "define" | Academic vocabulary bias | Changes all three questionnaires |
| 🔴 CRITICAL | Add Q5 meta-question about untranslatable words | "Heimat" ≠ "家" asymmetry | New questionnaire item |
| 🟡 HIGH | Add demographic covariates (age, years abroad, proficiency) | Confounder control | New metadata fields |
| 🟡 HIGH | Test questionnaire with 14-year-old before launch | Age-appropriateness | Need pilot test |
| 🟡 HIGH | Update annotation guideline for social issues domain | Old guideline is calculus-focused | Update docs/annotation_guideline_v1.md |
| 🟢 MEDIUM | Add B1-level synonyms for difficult vocabulary | Accessibility | Minor wording changes |
| 🟢 MEDIUM | Include 2 control questions (food, weather) | Method validation | New questionnaire items |

---

## References

- Original questionnaires: `data/questionnaires/`
- Experiment design: `research/experiment_design.md`
- Annotation guideline (old): `docs/annotation_guideline_v1.md`
- Gold dataset: `data/gold/gold_dataset.json`
- Concept mapping: `config/cross_language_mapping.json`
- BWKI scoring guide: (local knowledge base)
