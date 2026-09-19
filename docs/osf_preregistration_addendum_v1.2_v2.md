# OSF Preregistration Addendum v1.2 — Harness v2 (2026-09-18, pre-data)

Parent: `docs/osf_preregistration_addendum_v1.1_spark.md` (A1–A10, frozen).
This file freezes v2 BEFORE the first v2 API call. v1 (`PROMPT_FROZEN_v1.md`,
SHAs `72c5424f…`/`31b8e6eb…`) stays frozen and valid; no retroactive rescoring.
Anchors (minimax UNAVAILABLE per owner 2026-09-18; Western 5th rater CANCELLED):
`glm-5.2-r4`, `r4-deepseek-v4.1-flash`, `sn-sensenova-6.8-flash-lite` (r4 first, sensenova last).

## A11. Purpose + non-retroactivity per factor
- F1 CARD (P1): range-match removes known precision penalty; no claim that v1 models are bad.
- F2 LANG (P2): removes contradictory language clause; no claim of model-inherent EN failure until P2 fails.
- P3 BOTH: only cell callable fairer instrument. F4 window/F5 DB-path CUT (F4 audit-proven non-binding; F5 incomparable instrument).
- v1 numbers stay frozen; all v2 comparisons paired same-ID (cell vs archival P0).

## A12. Frozen cells (full texts + SHAs)
### P0 — system_sha256 `72c5424fdcfbad8fe59f1fd50f518004eb1351406358a710433ab38a1d330b61`
`你是概念提取专家。输出严格 JSON 格式。概念名称使用原始语言，禁止 ASCII 编码。输出 UTF-8 中文。`
### P0 — template_sha256 `31b8e6eb9775f9da41191b9c46fabb1c30039339cb5c598054c0820d512d7b59`
```
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

### P1 — system_sha256 `72c5424fdcfbad8fe59f1fd50f518004eb1351406358a710433ab38a1d330b61`
`你是概念提取专家。输出严格 JSON 格式。概念名称使用原始语言，禁止 ASCII 编码。输出 UTF-8 中文。`
### P1 — template_sha256 `ee4e986e85a0ff6f798d837301c37d44bde4d819c0466867ec6ffac7e1a610b2`
```
从以下文本中提取关键概念及其关系。

任务：提取 1-7 个真正独立的核心概念（通常 2-3 个；宁缺勿滥，禁止为凑数拆分或填充），并按以下 JSON Schema 输出：

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

### P2 — system_sha256 `704cbb2191bfa659745e357579ec605f6d7038b276eedfe646369caae52b2b18`
`你是概念提取专家。只输出严格 JSON 格式。概念名称必须使用文本源语言（中文文本用中文，德文文本用德文，英文文本用英文）；严禁翻译；英文或德文文本中严禁输出任何 CJK 字符。`
### P2 — template_sha256 `31b8e6eb9775f9da41191b9c46fabb1c30039339cb5c598054c0820d512d7b59`
```
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

### P3 — system_sha256 `704cbb2191bfa659745e357579ec605f6d7038b276eedfe646369caae52b2b18`
`你是概念提取专家。只输出严格 JSON 格式。概念名称必须使用文本源语言（中文文本用中文，德文文本用德文，英文文本用英文）；严禁翻译；英文或德文文本中严禁输出任何 CJK 字符。`
### P3 — template_sha256 `ee4e986e85a0ff6f798d837301c37d44bde4d819c0466867ec6ffac7e1a610b2`
```
从以下文本中提取关键概念及其关系。

任务：提取 1-7 个真正独立的核心概念（通常 2-3 个；宁缺勿滥，禁止为凑数拆分或填充），并按以下 JSON Schema 输出：

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

Byte-diff attested: P1 = P0 with exactly the cardinality sentence replaced (asserted count==1 in `stage0_v2_cells.py`);
P2 = P0 with system replaced; P3 = P1 template + P2 system. Schema/keys/temp/window/scoring unchanged.

## A13. Metrics + decision thresholds (paired, A2 denominator fails=0/92)
- F1 CARD (P1−P0 full-92 primary; social-72 + gold_n splits secondary): confirmed iff paired mean dF1 ≥ +0.10, CI excludes 0, pred_n → 2–6, n1-lift > n2-lift. Partial if pred_n falls but dF1 < +0.10. Failed if pred_n stays >8.
- F2 LANG (P2−P0 EN+DE n=56 primary, EN-social n=21 key, zh-spot ±0.05): prompt-bug confirmed iff EN-F1 ~0.00 → >0.30 (paired CI excludes 0) AND EN CJK-frac → <10%. Model-side failure iff EN-F1 <0.10 despite CJK <10%. zh regression >0.05 invalidates fix.
- P3 BOTH (P3−P0 full-92): V2-validated iff social F1 enters 0.40–0.65 (NOT DB 0.939), paired CI excludes 0, CJK <10%, pred_n 2–6. Residual-gap iff P3 <0.25 despite both fixes.
- Power: primary = pooled-92 + social-72; EN-social-21 only for large Δ (≥0.3); math cells + 6-way cells descriptive only; exploratory pairs Bonferroni α≈0.003.

## A14. Arms x cells + budget cap + gates
- CORE (786 nominal): P1 full-92 ×3 anchors (276) + P3 full-92 ×3 (276) + P2 EN+DE+zh10 ×3 (198) + P0-cal n=12 ×3 (36). Retries → ~860–940.
- 1200-nominal cap. Trim order: E4(qwen, CUT) > E2 > E3-shrink; never cut CORE P1/P3.
- EXTENDED gated: E1 (P3 remaining runnable arms full-92) iff CORE P3 paired lift CI-excludes-0 on ≥2/3 anchors; E3 (temp 0 vs 0.1, glm P3 same-30-IDs, 60 calls) anytime; E2 (P3b paraphrase, glm n=30, 30 calls) iff P3 lift exists, |d|≥0.10 → brittle.
- Smoke per cell×arm: `--max-items 5` (2en+2de+1zh, mixed gold_n); gate ≥4/5 parse-valid AND directional (P1 pred_n<P0; P2 EN-CJK≤P0; P3 both). Fail → investigate, no full launch, deviation log.
- Serial per arm/key (A10); per-ns lock; checkpoint+heartbeat; breaker 5-fail park (A9-5); resume-safe.

## A15. Quarantine / naming / transport
- Outputs only `research/mimo_spark_replication/t2_v2-<arm>-<cell>.json` (+ stage/prompts/locks with `v2-` prefix).
- FORBIDDEN writes: `t2_<ns>.json` (v1), `data/math_extractions/`, `freeze/`, `data/lds_c/`, `tests/`.
- Per-record provenance: model + endpoint + date + temperature actually used + input_sha256/chars + cell + prompt SHAs + rung + attempts (err-class, no keys). free≠paid / provider≠provider scope stands. Keys in-process from `.env` only.

## A16. Analysis plan (deterministic, zero extra API)
- Reuse deep-dive pipeline (cell CIs informative cells only, gold_n stratification, pre-declared paired dF1 P1−P0/P2−P0/P3−P0 per anchor, pred_n–F1 Pearson+bins per cell, CJK-frac + per-language means per cell, difficulty n=9 DO-NOT-USE). Bootstrap B=1000 seed 20260918 unchanged.

## A17. Claim mapping
- P1 lifts strongly → v1 lows were penalty artefacts; C9b stays Developing (blind review pending); C21 refined (v2-partial-repro); C23 hardens (Mature candidate).
- P2 lifts EN → language bug masking; same statuses as P1.
- P3 reaches 0.40–0.65 → dual-harness narrative at fairer instrument; C21 quantitative v2-gap; C23 confirmed, P3 recommended default.
- All fail (P3 <0.25, EN ~0) → mechanisms exhausted, gap looks model/seed (C21 severity up, still Developing); C23 downgraded to hypothesis, mimo-noise line becomes lead.

Frozen 2026-09-18 BEFORE first v2 call. Any byte-change after = deviation D-Vx. Owner: methods.
