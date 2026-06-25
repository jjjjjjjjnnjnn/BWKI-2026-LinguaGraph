# LinguaGraph Annotation Guideline v2.0

> For Second Annotator — Gold Dataset Expansion
> Domain: Social Issues (Freedom, Justice, Success, Responsibility, Home)
> Languages: Chinese, German, English

---

## 1. Overview

### 1.1 Task Description

You will read participant responses to 5 open-ended questions in Chinese, German, or English. For each response, you need to:

1. **Extract concepts** — what ideas does the participant mention?
2. **Extract relations** — how does the participant connect these ideas?
3. **Mark missing hints** — what connections is the participant aware of but can't articulate?

### 1.2 Why This Matters

Your annotations become the **Gold Standard** ("ground truth") against which our AI extraction is measured. If your annotations are accurate, we can trust the pipeline. If not, the entire experiment fails.

### 1.3 Timeline

- **Training**: 5 practice annotations → compare with first annotator → discuss differences
- **Full annotation**: ~100 responses (20 participants × 5 questions)
- **Estimated time**: 15-25 minutes per response, ~25-40 hours total

---

## 2. Concept Extraction Rules

### 2.1 What IS a Concept?

A concept is a **substantive idea** that the participant uses to explain their thinking. It is NOT every noun in the sentence.

| ✅ Extract (Concepts) | ❌ Do NOT Extract |
|-----------------------|------------------|
| Freedom, justice, responsibility | Think, feel, believe |
| Individual, society, family | People, person (generic) |
| Equality, opportunity, choice | Good, bad, important |
| Law, rights, duty | Life, world (too broad) |
| Effort, achievement, wealth | Always, never, sometimes |
| Self-determination, autonomy | Things, stuff, something |

### 2.2 Domain-Specific Concepts (Social Issues)

These are the **expected concepts** per topic. Annotate them when the participant mentions them. Also add concepts NOT on this list if they appear.

**Freedom**:
| ZH | DE | EN |
|----|----|------|
| 自由, 个体, 权利, 选择 | Freiheit, Individuum, Recht, Wahl | freedom, individual, right, choice |
| 责任, 社会, 限制, 自律 | Verantwortung, Gesellschaft, Grenze | responsibility, society, limit, discipline |
| 平等, 言论, 民主 | Gleichheit, Meinungsfreiheit | equality, speech, democracy |

**Justice**:
| ZH | DE | EN |
|----|----|------|
| 公平, 平等, 法律, 正义 | Gerechtigkeit, Gleichheit, Gesetz | justice, fairness, equality, law |
| 分配, 机会, 教育 | Verteilung, Chance, Bildung | distribution, opportunity, education |
| 社会, 权利, 程序 | Gesellschaft, Recht, Verfahren | society, rights, procedure |

**Success**:
| ZH | DE | EN |
|----|----|------|
| 成功, 努力, 成就, 家庭 | Erfolg, Anstrengung, Leistung, Familie | success, effort, achievement, family |
| 幸福, 财富, 目标 | Glück, Reichtum, Ziel | happiness, wealth, goal |
| 社会, 责任, 教育 | Gesellschaft, Verantwortung, Bildung | society, responsibility, education |

**Responsibility**:
| ZH | DE | EN |
|----|----|------|
| 责任, 义务, 自由, 选择 | Verantwortung, Pflicht, Freiheit, Wahl | responsibility, duty, freedom, choice |
| 道德, 法律, 后果 | Moral, Gesetz, Konsequenz | morality, law, consequence |
| 家庭, 社会, 承诺 | Familie, Gesellschaft, Versprechen | family, society, commitment |

**Home**:
| ZH | DE | EN |
|----|----|------|
| 家, 家庭, 父母, 归属 | Heimat, Familie, Eltern, Zugehörigkeit | home, family, parents, belonging |
| 安全, 爱, 传统 | Sicherheit, Liebe, Tradition | safety, love, tradition |
| 记忆, 身份, 温暖 | Erinnerung, Identität, Geborgenheit | memory, identity, warmth |

### 2.3 Normalization Rules

| Situation | Rule | Example |
|-----------|------|---------|
| Synonyms | Choose the most standard term | "job" and "career" → "career" |
| Same word in different languages | Keep in the answer's language | ZH answer → ZH concepts |
| Technical terms | Keep as-is | "positive freedom" → "positive freedom" |
| Vague/generic concepts | Do NOT extract | "things", "people", "way of life" |
| Negated concepts | Extract if the IDEA is present | "not about money" → extract "money" |
| Compound expressions | Split into components | "individual freedom" → ["individual", "freedom"] |

### 2.4 Concept Frequency

- **Minimum**: 3 concepts per response (otherwise it's too_short)
- **Typical**: 5-12 concepts per response
- **Maximum**: No upper limit, but don't extract every noun
- **Rule of thumb**: If removing it would lose meaning → extract. If it's filler → skip.

---

## 3. Relation Extraction Rules

### 3.1 Relation Types (Closed Set)

Use ONLY these 8 relation types:

| Type | Definition | Direction | Example |
|------|------------|-----------|---------|
| `is_a` | A is a type of B | A → B | "freedom is a right" → freedom is_a right |
| `has_part` | A has B as a component | A → B | "justice includes equality" → justice has_part equality |
| `implies` | A implies/leads to B | A → B | "success requires effort" → success implies effort |
| `opposes` | A opposes/conflicts with B | A ↔ B | "freedom versus security" → freedom opposes security |
| `similar_to` | A is similar to B | A → B | "fairness is like equality" → fairness similar_to equality |
| `enables` | A makes B possible | A → B | "freedom enables choice" → freedom enables choice |
| `requires` | A needs B to exist | A → B | "responsibility requires free will" → responsibility requires free will |
| `relates_to` | A is generally connected to B (weakest) | A → B | "success and happiness" → success relates_to happiness |

### 3.2 When to Extract a Relation

✅ **Extract** when:
- Participant explicitly says "X is Y" or "X means Y"
- Participant says "X depends on Y" or "X requires Y"
- Participant contrasts X and Y ("X vs Y")
- Participant lists X as an example of Y

❌ **Do NOT extract** when:
- X and Y appear in the same sentence but unrelated
- X is a metaphor or figure of speech
- Participant is quoting someone else's view without endorsing it

### 3.3 How to Determine Direction

The arrow `→` always means: "A relates TO B" in the direction the participant expressed.

```
"Freedom requires responsibility"
→ freedom requires responsibility
✓ CORRECT: freedom → responsibility

"Success comes from hard work"
→ success implies effort
✓ CORRECT: success → effort
```

If the direction is unclear, use `relates_to` (bidirectional weakest relation).

### 3.4 Confidence Score

| Score | Meaning | When to Use |
|-------|---------|-------------|
| 1.0 | Certain | Direct quotation: "X is Y" |
| 0.8 | Likely | Strong implication: "X means Y to me" |
| 0.6 | Uncertain | Vague connection: "X and Y are related somehow" |

---

## 4. Missing Hints

### 4.1 What IS a Missing Hint?

A missing hint is when the participant **shows awareness of a gap** in their own understanding.

✅ Examples:
- "I know freedom is important but I'm not sure why"
- "Success obviously involves money but that can't be all"
- "There must be more to justice than just laws"

❌ NOT missing hints:
- Concepts the participant simply didn't mention (absence ≠ gap)
- Things the participant got wrong (error ≠ gap)
- What YOU think should be there (your opinion ≠ their gap)

### 4.2 How to Mark

```json
{
  "from": "freedom",
  "to": "limit",
  "reason": "Participant says freedom is unlimited but seems uncertain",
  "confidence": 0.7
}
```

---

## 5. Cross-Language Mapping Rules

### 5.1 Language of Annotation

**ALWAYS annotate in the answer's language.**

| Answer Language | Concepts | Relations |
|-----------------|----------|-----------|
| Chinese | 自由, 权利, 社会 | 自由 → 权利 |
| German | Freiheit, Recht, Gesellschaft | Freiheit → Recht |
| English | freedom, right, society | freedom → right |

**DO NOT translate** the participant's concepts. If a ZH participant writes "自由", you write "自由", not "freedom".

### 5.2 Cross-Language Equivalence (for Analysis, NOT Annotation)

The system will automatically map concepts using `config/cross_language_mapping.json`. You don't need to worry about this during annotation.

Example: German "Recht" and Chinese "权利" both map to shared ID "rights".
→ This happens AFTER annotation, not during.

---

## 6. Annotation JSON Format

```json
{
  "response_id": "R001_zh_q1",
  "annotator": "annotator_B",
  "date": "2026-07-01",
  "concepts": ["自由", "个体", "权利", "责任", "社会", "选择"],
  "relations": [
    {"source": "自由", "target": "个体", "type": "is_a", "confidence": 0.9},
    {"source": "自由", "target": "责任", "type": "implies", "confidence": 0.8},
    {"source": "自由", "target": "权利", "type": "is_a", "confidence": 1.0}
  ],
  "missing_hints": [],
  "quality_rating": "rich",
  "annotator_confidence": 4,
  "notes": ""
}
```

### Quality Ratings

| Rating | Criteria |
|--------|----------|
| `rich` | 6+ concepts, 3+ relations, structured argument |
| `moderate` | 3-5 concepts, 1-2 relations, some reasoning |
| `thin` | 1-2 concepts, 0 relations, short answer |
| `empty` | "I don't know" or blank |

---

## 7. Examples (20 Cases)

### Example 1: Freedom (ZH, Rich)

**Response**: "自由对我来说意味着能够按照自己的意愿生活，但同时也要对自己的选择负责。真正的自由不是为所欲为，而是在尊重他人权利的前提下做自己想做的事。自由和社会责任是分不开的。"

**Annotation**:
```json
{
  "concepts": ["自由", "意愿", "选择", "责任", "尊重", "权利", "社会"],
  "relations": [
    {"source": "自由", "target": "意愿", "type": "enables", "confidence": 1.0},
    {"source": "自由", "target": "选择", "type": "implies", "confidence": 1.0},
    {"source": "自由", "target": "责任", "type": "implies", "confidence": 1.0},
    {"source": "自由", "target": "权利", "type": "requires", "confidence": 0.9},
    {"source": "自由", "target": "社会", "type": "relates_to", "confidence": 0.9}
  ],
  "quality": "rich"
}
```

### Example 2: Freedom (DE, Moderate)

**Response**: "Freiheit bedeutet für mich, selbstbestimmt leben zu können. Man kann seine eigenen Entscheidungen treffen."

**Annotation**:
```json
{
  "concepts": ["Freiheit", "Selbstbestimmung", "Entscheidung"],
  "relations": [
    {"source": "Freiheit", "target": "Selbstbestimmung", "type": "enables", "confidence": 1.0},
    {"source": "Freiheit", "target": "Entscheidung", "type": "enables", "confidence": 0.9}
  ],
  "quality": "moderate"
}
```

### Example 3: Freedom (EN, Thin)

**Response**: "Freedom is doing what you want."

**Annotation**:
```json
{
  "concepts": ["freedom", "choice"],
  "relations": [
    {"source": "freedom", "target": "choice", "type": "enables", "confidence": 0.8}
  ],
  "quality": "thin"
}
```

### Example 4: Justice (ZH, Rich)

**Response**: "公平就是每个人都能得到应有的对待。一个公平的社会应该保证每个人都有平等的机会去接受教育和实现自己的价值。法律面前人人平等，但公平不仅仅是法律问题，还涉及社会资源的合理分配。"

**Annotation**:
```json
{
  "concepts": ["公平", "对待", "社会", "机会", "教育", "价值", "法律", "平等", "分配"],
  "relations": [
    {"source": "公平", "target": "对待", "type": "is_a", "confidence": 0.9},
    {"source": "公平", "target": "机会", "type": "has_part", "confidence": 1.0},
    {"source": "公平", "target": "教育", "type": "relates_to", "confidence": 0.9},
    {"source": "公平", "target": "法律", "type": "relates_to", "confidence": 0.8},
    {"source": "公平", "target": "分配", "type": "has_part", "confidence": 0.9}
  ],
  "quality": "rich"
}
```

### Example 5: Justice (DE, Moderate)

**Response**: "Gerechtigkeit ist für mich, wenn alle Menschen vor dem Gesetz gleich sind und die gleichen Chancen im Leben haben."

**Annotation**:
```json
{
  "concepts": ["Gerechtigkeit", "Gesetz", "Gleichheit", "Chance"],
  "relations": [
    {"source": "Gerechtigkeit", "target": "Gesetz", "type": "relates_to", "confidence": 0.9},
    {"source": "Gerechtigkeit", "target": "Gleichheit", "type": "has_part", "confidence": 1.0},
    {"source": "Gerechtigkeit", "target": "Chance", "type": "has_part", "confidence": 0.9}
  ],
  "quality": "moderate"
}
```

### Example 6: Justice (EN, Rich)

**Response**: "Justice means everyone gets what they deserve. It's about fairness in how people are treated by institutions like courts and schools. But justice isn't just about punishment—it's also about making sure people have what they need to live well."

**Annotation**:
```json
{
  "concepts": ["justice", "fairness", "deserve", "institution", "court", "punishment", "need"],
  "relations": [
    {"source": "justice", "target": "fairness", "type": "similar_to", "confidence": 1.0},
    {"source": "justice", "target": "institution", "type": "relates_to", "confidence": 0.9},
    {"source": "justice", "target": "punishment", "type": "has_part", "confidence": 0.8},
    {"source": "justice", "target": "need", "type": "relates_to", "confidence": 0.8}
  ],
  "quality": "rich"
}
```

### Example 7: Success (ZH, Rich)

**Response**: "成功不仅仅是赚多少钱，更重要的是对家庭和社会有没有贡献。一个人如果能照顾好家人、在工作上有所成就、并且内心感到满足，这就是成功的人生。"

**Annotation**:
```json
{
  "concepts": ["成功", "财富", "家庭", "社会", "贡献", "事业", "满足"],
  "relations": [
    {"source": "成功", "target": "财富", "type": "relates_to", "confidence": 0.7},
    {"source": "成功", "target": "家庭", "type": "has_part", "confidence": 1.0},
    {"source": "成功", "target": "社会", "type": "has_part", "confidence": 0.9},
    {"source": "成功", "target": "满足", "type": "has_part", "confidence": 0.9}
  ],
  "quality": "rich"
}
```

### Example 8: Success (DE, Moderate)

**Response**: "Erfolg bedeutet für mich, meine beruflichen Ziele zu erreichen und dabei finanziell unabhängig zu sein. Dazu gehört auch, dass ich mich persönlich weiterentwickle."

**Annotation**:
```json
{
  "concepts": ["Erfolg", "Ziel", "Karriere", "Unabhängigkeit", "Entwicklung"],
  "relations": [
    {"source": "Erfolg", "target": "Ziel", "type": "requires", "confidence": 1.0},
    {"source": "Erfolg", "target": "Karriere", "type": "relates_to", "confidence": 0.9},
    {"source": "Erfolg", "target": "Unabhängigkeit", "type": "enables", "confidence": 0.8},
    {"source": "Erfolg", "target": "Entwicklung", "type": "has_part", "confidence": 0.9}
  ],
  "quality": "moderate"
}
```

### Example 9: Home (ZH, Rich)

**Response**: "家对我来说就是父母所在的地方，是无论走到哪里都会牵挂的地方。家里有温暖、有亲情、有从小到大的一切记忆。传统节日一家人团聚，这就是家的意义。"

**Annotation**:
```json
{
  "concepts": ["家", "父母", "牵挂", "温暖", "亲情", "记忆", "传统", "团聚"],
  "relations": [
    {"source": "家", "target": "父母", "type": "has_part", "confidence": 1.0},
    {"source": "家", "target": "温暖", "type": "has_part", "confidence": 0.9},
    {"source": "家", "target": "记忆", "type": "relates_to", "confidence": 0.8},
    {"source": "家", "target": "传统", "type": "has_part", "confidence": 0.9}
  ],
  "quality": "rich"
}
```

### Example 10: Home (DE, Rich)

**Response**: "Heimat ist für mich der Ort, wo ich aufgewachsen bin, wo ich die Sprache und die Menschen kenne. Es ist ein Gefühl von Zugehörigkeit und Sicherheit. Auch wenn ich jetzt woanders lebe, bleibt Heimat ein Teil meiner Identität."

**Annotation**:
```json
{
  "concepts": ["Heimat", "Ort", "Sprache", "Mensch", "Zugehörigkeit", "Sicherheit", "Identität"],
  "relations": [
    {"source": "Heimat", "target": "Ort", "type": "is_a", "confidence": 0.9},
    {"source": "Heimat", "target": "Zugehörigkeit", "type": "has_part", "confidence": 1.0},
    {"source": "Heimat", "target": "Sicherheit", "type": "has_part", "confidence": 0.9},
    {"source": "Heimat", "target": "Identität", "type": "implies", "confidence": 0.9}
  ],
  "quality": "rich"
}
```

### Example 11-15: Short/Edge Cases

**Example 11** (Empty): "I don't know" → `"concepts": [], "quality": "empty"`

**Example 12** (Off-topic): "Freedom is a song by George Michael" → Flag as off_topic

**Example 13** (Language mix): ZH answer with DE terms → Annotate ZH terms, add note about DE

**Example 14** (Contradiction): "Success is about money... no wait, it's not about money at all" → Extract both "wealth" and note the contradiction

**Example 15** (Missing hint): "I know responsibility is important but I can't really explain why" →
```json
{
  "missing_hints": [{"from": "responsibility", "to": "reason", "reason": "Participant aware of gap in understanding"}]
}
```

### Example 16-20: Ambiguous Cases

**Example 16** — Is "good life" a concept? → YES (for Success topic)

**Example 17** — Is "government" the same as "state"? → NO. Extract separately if both appear.

**Example 18** — Should I extract "my parents" as a concept? → YES, as "family/parents"

**Example 19** — No relations expressed → Still annotate concepts, mark `"relations": []`

**Example 20** — Participant changes mind mid-answer → Annotate both perspectives

---

## 8. Inter-Annotator Agreement (Cohen's Kappa)

### 8.1 What We Measure

After you and the first annotator each annotate the same 20 responses, we calculate:

| Metric | Target | Calculation |
|--------|--------|-------------|
| Concept overlap | κ ≥ 0.70 | Jaccard similarity of concept sets |
| Relation overlap | κ ≥ 0.65 | Per-relation type agreement |
| Quality rating | ≥ 80% | Exact match on rich/moderate/thin/empty |

### 8.2 Calculation

```python
from sklearn.metrics import cohen_kappa_score

# Example: 20 responses, each with concept set
annotator_A = [set(["自由", "权利"]), set(["公平", "法律"]), ...]
annotator_B = [set(["自由", "权利", "责任"]), set(["公平"]), ...]

# Convert to per-concept presence vectors
all_concepts = sorted(set().union(*annotator_A, *annotator_B))
vec_A = [[1 if c in a else 0 for c in all_concepts] for a in annotator_A]
vec_B = [[1 if c in b else 0 for c in all_concepts] for b in annotator_B]

kappa = cohen_kappa_score(vec_A, vec_B)
print(f"Cohen's Kappa: {kappa:.3f}")
# Target: kappa ≥ 0.70
```

### 8.3 If κ < 0.70

1. Both annotators review disagreements
2. Identify systematic differences (e.g., always missing same relation type)
3. Update this guideline
4. Re-annotate a subset of 10 responses
5. Recalculate κ
6. Repeat until κ ≥ 0.70

---

## 9. Conflict Resolution

| Situation | Resolution |
|-----------|------------|
| Annotator A says concept exists, B says no | Discuss. If disagreement remains, include it (lenient) |
| Different relation types for same pair | Choose the more specific type. "is_a" > "relates_to" |
| Different direction for same relation | Check original text. If ambiguous, use `relates_to` |
| One annotator misses a relation | Include it (union of both annotations) |
| Both annotators mark missing_hints differently | Keep the more conservative (higher confidence) one |

---

## 10. Quick Reference Card

```
CONCEPTS → substantive ideas only (not filler words)
RELATIONS → only 8 types: is_a, has_part, implies, opposes, similar_to, enables, requires, relates_to
DIRECTION → arrow follows participant's logic
CONFIDENCE → 1.0=explicit, 0.8=implicit, 0.6=vague
LANGUAGE → annotate in the answer's language, NOT translated
MISSING → only if participant shows awareness of gap
QUALITY → rich(6+), moderate(3-5), thin(1-2), empty(0)
KAPPA → target ≥ 0.70
```

---

*Version 2.0 — June 2026 — For LinguaGraph BWKI 2026 Gold Dataset Expansion*
