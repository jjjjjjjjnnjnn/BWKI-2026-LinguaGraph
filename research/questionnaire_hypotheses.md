# LinguaGraph Research Hypotheses & Questionnaire Design

**Role:** Cognitive Linguistics Researcher
**Date:** 2026-06-17
**Based on:** Pilot Study with 813 texts, 5 topics, 3 languages

---

## Part 1: 10 Research Hypotheses

### H1: Success Conceptualization Differs Across Languages

**If** language influences cognition,
**then** Chinese, English, and German speakers will organize "success" around different core concepts when asked to define it.
**Reason:** LDS = 0.269 (highest among all topics). Chinese texts emphasize effort/family/collective achievement; English texts emphasize opportunity/individual achievement; German texts emphasize competence/efficiency/career.
**Expected result:** Chinese responses cluster around 努力+家庭+责任; English around achievement+choice+opportunity; German around Leistung+Karriere+Selbstständigkeit.

### H2: Responsibility is Framed Differently Across Cultures

**If** language shapes moral reasoning,
**then** the relationship between "responsibility" and "freedom" will be stronger in German culture than in Chinese or English culture.
**Reason:** LDS = 0.265. German philosophical tradition (Kant) tightly links Verantwortung with Freiheit; Chinese tradition links 责任 with 社会/集体; English tradition links responsibility with individual choice.
**Expected result:** German responses will show more Kantian duty-based reasoning; Chinese responses will show more collectivist framing; English responses will show more contractual framing.

### H3: Home/Heimat is the Most Universal Concept

**If** language has minimal influence on basic spatial/relational concepts,
**then** "home" will show the lowest cross-lingual drift.
**Reason:** LDS = 0.239 (lowest). Home/家/Heimat all refer to a physical and emotional space that is relatively consistent across cultures.
**Expected result:** High concept overlap across all three languages; LDS significantly lower than success/responsibility.

### H4: Freedom Shows Cultural Specificity in Definition

**If** political concepts are culturally constructed,
**then** "freedom" will show different emphasis patterns: Chinese (social harmony), English (individual rights), German (self-determination).
**Reason:** LDS = 0.226, but Jaccard = 0.435 (highest overlap) — the concepts are shared but their relational structure differs.
**Expected result:** Chinese responses emphasize 责任+社会; English emphasize rights+choice; German emphasize Selbstbestimmung+Recht.

### H5: High-Drift Concepts Predict Questionnaire Differentiation

**If** internet text analysis predicts human cognitive differences,
**then** concepts with higher LDS in internet corpora will also show higher differentiation in human questionnaire responses.
**Reason:** This is the core validation hypothesis connecting pilot data to formal experiment.
**Expected result:** Success > Responsibility > Freedom > Home in terms of between-language variance in human responses.

### H6: Concept Centrality Differs Across Languages

**If** language organizes conceptual networks differently,
**then** the most central (highest degree) concept in "success" will differ: Chinese (努力/effort), English (achievement), German (Leistung/performance).
**Reason:** Graph centrality reflects what a culture considers most important about a concept.
**Expected result:** Different hub nodes in each language's cognitive graph for the same topic.

### H7: Relation Types Vary by Cultural Framework

**If** cultural values shape how concepts relate,
**then** Chinese texts will show more "requires" and "part_of" relations (hierarchical), while English texts will show more "leads_to" and "enables" relations (causal/agentive).
**Reason:** Collectivist cultures emphasize structural relationships; individualist cultures emphasize causal agency.
**Expected result:** Relation type distribution differs significantly across languages.

### H8: Bilingual Individuals Show Intermediate LDS

**If** bilingualism creates cognitive flexibility,
**then** bilingual individuals' cognitive graphs will fall between their two monolingual counterparts on the LDS scale.
**Reason:** Bilinguals have access to both conceptual frameworks, potentially creating intermediate structures.
**Expected result:** Bilingual LDS < monolingual LDS for the same language pair.

### H9: Concept Concreteness Predicts Drift Magnitude

**If** abstract concepts are more culturally variable than concrete concepts,
**then** abstract concepts (success, justice, freedom) will show higher LDS than concrete concepts (home, family, food).
**Reason:** Concrete concepts are grounded in universal physical experience; abstract concepts are culturally constructed.
**Expected result:** Abstract concepts cluster at LDS > 0.25; concrete concepts cluster at LDS < 0.20.

### H10: LDS Correlates with Hofstede's Cultural Dimensions

**If** cross-lingual cognitive differences reflect underlying cultural dimensions,
**then** LDS will correlate with Hofstede's individualism-collectivism dimension (China=20, Germany=67, USA=91).
**Reason:** Individualist cultures should emphasize different concepts than collectivist cultures.
**Expected result:** Higher LDS between China and Western cultures on collectivism-related concepts (responsibility, family, success).

---

## Part 2: Concept Drift Classification

### High Drift (LDS > 0.25) — Experimental Group

| Concept | LDS | Jaccard | Why High Drift |
|---------|-----|---------|----------------|
| **Success** | 0.269 | 0.381 | Most culturally variable — achievement vs. effort vs. competence |
| **Responsibility** | 0.265 | 0.355 | Moral framing varies: duty vs. contract vs. collective |
| **Justice** | — | — | (data pending, but expected high) |
| **Democracy** | — | — | (data pending, but expected high) |

**Why these concepts drift:** They are abstract, culturally constructed, and tied to value systems that differ across civilizations.

### Medium Drift (LDS 0.20-0.25) — Transition Zone

| Concept | LDS | Jaccard | Why Medium Drift |
|---------|-----|---------|-----------------|
| **Freedom** | 0.226 | 0.435 | Shared core but different relational structures |
| **Fairness** | — | — | (expected medium) |
| **Education** | — | — | (expected medium) |

**Why these drift moderately:** Universal core meaning but culturally specific framing and emphasis.

### Low Drift (LDS < 0.20) — Control Group

| Concept | LDS | Jaccard | Why Low Drift |
|---------|-----|---------|--------------|
| **Home** | 0.239 | 0.351 | Physical/emotional space is relatively universal |
| **Family** | — | — | (expected low) |
| **Food** | — | — | (expected very low) |
| **Body** | — | — | (expected very low) |

**Why these drift less:** Grounded in universal human experience, less culturally constructed.

---

## Part 3: Questionnaire Design

### Design Principles

1. **Measure cognition, not education** — questions should reveal HOW people think, not WHAT they know
2. **Open-ended preferred** — allow natural concept emergence
3. **Scenario-based** — put concepts in context to reveal relational structures
4. **Trilingual parallel** — exact same questions in zh/en/de

### Topic: Success (High Drift — Experimental)

#### Q1: Open Definition
**zh:** 请用3-5句话描述"成功"对你意味着什么。
**en:** Describe in 3-5 sentences what "success" means to you.
**de:** Beschreiben Sie in 3-5 Sätzen, was "Erfolg" für Sie bedeutet.

**Measures:** Core concept extraction, centrality analysis

#### Q2: Association Task
**zh:** 想到"成功"时，你最先想到的5个词是什么？
**en:** What are the first 5 words that come to mind when you think of "success"?
**de:** Was sind die ersten 5 Wörter, die Ihnen beim Thema "Erfolg" einfallen?

**Measures:** Concept clustering, prototype analysis

#### Q3: Scenario
**zh:** 一个学生考试得了满分，但牺牲了所有社交时间。这个人成功吗？为什么？
**en:** A student got a perfect score but sacrificed all social time. Is this person successful? Why?
**de:** Ein Schüler hat eine perfume Note erhalten, aber alle sozialen Kontakte aufgegeben. Ist diese Person erfolgreich? Warum?

**Measures:** Value prioritization, trade-off reasoning

### Topic: Responsibility (High Drift — Experimental)

#### Q4: Open Definition
**zh:** 请描述"责任"和"自由"之间的关系。
**en:** Describe the relationship between "responsibility" and "freedom."
**de:** Beschreiben Sie die Beziehung zwischen "Verantwortung" und "Freiheit."

**Measures:** Conceptual relationship structure

#### Q5: Association Task
**zh:** 想到"责任"时，你最先想到的5个词是什么？
**en:** What are the first 5 words that come to mind when you think of "responsibility"?
**de:** Was sind die ersten 5 Wörter, die Ihnen beim Thema "Verantwortung" einfallen?

**Measures:** Concept clustering

#### Q6: Scenario
**zh:** 一个人有能力帮助别人，但选择不帮。他有责任吗？
**en:** A person has the ability to help others but chooses not to. Are they responsible?
**de:** Eine Person hat die Möglichkeit, anderen zu helfen, entscheidet sich aber dagegen. Ist sie verantwortlich?

**Measures:** Moral reasoning framework (duty vs. contract vs. virtue)

### Topic: Freedom (Medium Drift — Experimental)

#### Q7: Open Definition
**zh:** 请描述"自由"的边界在哪里。
**en:** Describe where the boundaries of "freedom" lie.
**de:** Beschreiben Sie, wo die Grenzen der "Freiheit" liegen.

**Measures:** Conceptual boundary definition

#### Q8: Scenario
**zh:** 如果一个人的自由选择伤害了他人，这种自由应该被限制吗？
**en:** If a person's free choice harms others, should that freedom be restricted?
**de:** Wenn die freie Wahl einer anderen Person schadet, sollte diese Freiheit eingeschränkt werden?

**Measures:** Freedom-responsibility trade-off reasoning

### Topic: Home (Low Drift — Control)

#### Q9: Open Definition
**zh:** "家"和"房子"有什么区别？
**en:** What is the difference between "home" and "house"?
**de:** Was ist der Unterschied zwischen "Zuhause" und "Haus"?

**Measures:** Emotional vs. physical conceptualization

#### Q10: Association Task
**zh:** 想到"家"时，你最先想到的5个词是什么？
**en:** What are the first 5 words that come to mind when you think of "home"?
**de:** Was sind die ersten 5 Wörter, die Ihnen beim Thema "Zuhause" einfallen?

**Measures:** Concept clustering (expected high overlap across languages)

---

## Part 4: Scoring Rubric

### For Each Response

1. **Extract concepts** (5-15 per response)
2. **Map to canonical forms** (using concept_mapping.py)
3. **Build cognitive graph** (concepts + relations)
4. **Compare across languages** (pairwise LDS)

### Aggregate Metrics

- **Concept Shift:** Which concepts are language-specific?
- **Relation Shift:** Which relationships differ?
- **Centrality Shift:** Which concept is the hub in each language?
- **LDS:** Overall structural difference

### Statistical Tests

- **Permutation test:** Is observed LDS significantly different from random?
- **Effect size:** Cohen's d between language groups
- **Power analysis:** Is n=5 per group sufficient?

---

## Part 5: Expected Outcomes

### If H1-H5 are confirmed:

The pilot study provides strong evidence that:
1. Cross-lingual cognitive differences exist in abstract concepts
2. LDS is a valid metric for measuring these differences
3. Internet text analysis predicts human questionnaire results

### If H6-H10 are confirmed:

The research extends to:
1. Bilingualism as cognitive flexibility
2. Concreteness as a moderator of cultural variation
3. Connection to established cultural dimension theories

### For BWKI Submission:

These hypotheses and questionnaire design form the core of the "Wissenschaftliches Arbeiten" (scientific methodology) section, addressing the 4/10 score identified in the compliance review.
