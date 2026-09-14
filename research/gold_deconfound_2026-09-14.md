# G3 Gold Deconfound Note (2026-09-14)

Scope: `data/gold/gold_dataset.json` (92 items: annotator_1 math n=20, auto_accepted social n=72)
joined by `sample_id` against per-item `f1` in
`data/model_comparison/qwen-plus_results.json` / `qwen-max_results.json` (each has 92 `results`).

## 1. Recomputed table (group means of per-item F1)

| model | subset | n | mean F1 |
|---|---|---|---|
| qwen-plus | math (annotator_1) | 20 | 0.7244 |
| qwen-plus | social (auto_accepted) | 72 | 0.6497 |
| qwen-max | math (annotator_1) | 20 | 0.7068 |
| qwen-max | social (auto_accepted) | 72 | 0.6483 |

Assertion check: qwen-plus overall macro mean recomputed = 0.665927 -> round4 = 0.6659,
matches `summary.mean_f1 = 0.6659`. PASS.

## 2. Ranking note (no inflation)

n=2 models, so NO Spearman rank correlation is claimed.
Only report: gap same-sign, qwen-plus > qwen-max on both subsets:
math gap +0.0176, social gap +0.0014.

## 3. Prompt A — batch harness extract path (scripts/batch_model_benchmark.py)

Source: L29-50 `EXTRACT_PROMPT_TEMPLATE`; scoring logic L129-175
(exact-match set overlap, per-item P/R/F1, macro mean); system message L137.

System prompt (L137, verbatim):

```text
你是概念提取专家。输出严格 JSON 格式。概念名称使用原始语言，禁止 ASCII 编码。输出 UTF-8 中文。
```

User template (L29-50, verbatim):

```text
从以下文本中提取关键概念及其关系。

任务：提取 10-20 个核心概念，并按以下 JSON Schema 输出：

{{
  "topic": "[topic]",
  "language": "[lang]",
  "concepts": [
    {{
      "name": "概念名称（原始语言）",
      "category": "核心概念/相关概念/具体事例",
      "related_concepts": ["相关概念1", "相关概念2"],
      "definition_snippet": "一句话定义"
    }}
  ],
  "relations": [
    {{"source": "概念A", "target": "概念B", "type": "隶属于/导致/对立/相关"}}
  ]
}}

文本内容：
{text}
```

Call shape: `temperature 0.1, max_tokens 2048`, text truncated to `text[:2000]`
(L134-142); predicted set = `{c.name for c in extracted.concepts}` (L165).

## 4. Prompt B — DB extraction path (scripts/lds_c_extract.py -> scripts/compute_lds_from_db.py)

Source: `scripts/lds_c_extract.py:50-57 SYSTEM_PROMPT`, L59-66 `EXTRACTION_PROMPT`,
L159-166 `PER_TOPIC_PROMPT` (model `deepseek-v4-flash`, temperature 0.3).
`scripts/compute_lds_from_db.py` does NOT re-extract; it loads pre-computed
`extractions` rows from DB and scores `1 - Jaccard(concepts_a, concepts_b)`.

System prompt (verbatim):

```text
You are a precise cognitive-linguistics concept extractor. Extract only meaningful CONTENT concepts: nouns and noun phrases that carry conceptual weight (e.g. 'freedom', 'boundaries', 'family duty'). REJECT function words, particles, pronouns, fillers, and grammatical fragments (e.g. 'something', 'within', 'being able to'). Respond ONLY with valid JSON, no explanation, no markdown fences.
```

Whole-response user prompt (verbatim):

```text
For each of the {n} topics below, extract the 5-6 most important CONCEPTS the person uses to explain that topic. Include each concept in its ORIGINAL language, an English gloss for cross-language alignment, and a 0-1 importance weight.

Be concise: do NOT add reasoning or commentary. Return ONLY compact valid JSON with no trailing commas:
{{"topics":[{{"topic":"<label>","concepts":[{{"concept":"<original>","en":"<gloss>","importance":0.9}}]}}]}}

Person's answers:
{answers}
```

Per-topic fallback prompt (verbatim):

```text
Extract the 5-6 most important CONCEPTS this person uses to explain the topic "{topic}". Include each concept in its ORIGINAL language, an English gloss for cross-language alignment, and a 0-1 importance weight.

Be concise: do NOT add reasoning or commentary. Return ONLY compact valid JSON with no trailing commas:
{{"topics":[{{"topic":"{topic}","concepts":[{{"concept":"<original>","en":"<gloss>","importance":0.9}}]}}]}}

The person's answer on {topic}:
{text}
```

## 5. Conclusion

- 0.939 is a DB-path + seed co-origin specific value (paper value), NOT comparable
  to independent-harness numbers.
- Independent-harness social F1 is ~0.65 for both models (0.6497 / 0.6483).
- Ranking qwen-plus > qwen-max holds on the clean math (annotator_1) subset
  (gap +0.0176, same sign as social +0.0014).
- Model-selection claim keeps the ranking but MUST downgrade the absolute value:
  do not cite 0.939 as harness F1.

Machine-readable numbers: `research/gold_deconfound_2026-09-14.json`.
