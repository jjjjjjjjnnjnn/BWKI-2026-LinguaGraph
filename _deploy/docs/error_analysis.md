# LinguaGraph Error Analysis Framework

## Error Taxonomy

### Type 1: Concept Omission (概念遗漏)

**Definition:** A concept present in the text is not extracted.

**Example:**
- Text: "自由需要责任来平衡" (Freedom needs responsibility for balance)
- Extracted: ["自由"] (missing "责任", "平衡")
- Omitted: 责任, 平衡

**Causes:**
- Keyword not in dictionary (fallback mode)
- LLM prompt too restrictive
- Concept expressed indirectly

**Measurement:**
```
Omission Rate = omitted_concepts / total_concepts_in_text
```

### Type 2: Relation Error (关系错误)

**Definition:** An extracted relation is incorrect (wrong type or wrong direction).

**Example:**
- Text: "知识就是权力" (Knowledge is power)
- Extracted: {"from": "知识", "to": "权力", "type": "causes"}
- Correct: {"from": "知识", "to": "权力", "type": "equivalent"}

**Causes:**
- LLM misinterprets relationship
- Ambiguous text
- Keyword matching ignores semantics

**Measurement:**
```
Relation Error Rate = incorrect_relations / total_relations
```

### Type 3: Concept Conflation (概念混淆)

**Definition:** Two distinct concepts are merged into one.

**Example:**
- Text: "民主和自由是不同的" (Democracy and freedom are different)
- Extracted: ["自由"] (democracy merged with freedom)
- Correct: ["民主", "自由"]

**Causes:**
- Concepts semantically similar
- Keyword overlap
- LLM simplification

**Measurement:**
```
Conflation Rate = conflated_pairs / total_concepts
```

### Type 4: Cross-lingual Inconsistency (跨语言不一致)

**Definition:** The same question produces different concept sets across languages.

**Example:**
- Chinese: ["自由", "责任", "社会"]
- German: ["Freiheit", "Recht"] (missing responsibility concept)
- Expected: Both should have responsibility concept

**Causes:**
- Cultural differences in emphasis
- Language-specific expression patterns
- Extraction quality varies by language

**Measurement:**
```
Inconsistency Rate = inconsistent_concepts / total_concepts
```

## Current Error Profile (Fallback Mode)

Based on keyword matching limitations:

| Error Type | Estimated Rate | Primary Cause |
|-----------|---------------|---------------|
| Concept Omission | ~40% | Limited keyword dictionary |
| Relation Error | ~80% | All relations marked as co_occurs |
| Concept Conflation | ~10% | Low (keywords are specific) |
| Cross-lingual Inconsistency | ~30% | Different keyword coverage per language |

## Error Analysis Procedure

1. **Collect** 20+ annotated responses (gold dataset)
2. **Run** extraction (LLM or fallback)
3. **Compare** extracted vs human-annotated
4. **Classify** each error by type
5. **Compute** error rates per type
6. **Identify** systematic patterns
7. **Report** with examples and statistics

## Known Issues (Current Implementation)

1. `fallback_extract` returns only `co_occurs` relations — no semantic distinction
2. `extract_concepts_from_response` in cross_language.py uses character overlap — not semantic
3. Gold dataset has only 7 samples — insufficient for reliable error estimation
