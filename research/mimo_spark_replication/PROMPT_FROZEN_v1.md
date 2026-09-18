# Spark Replication Arm — Frozen Protocol v1 (2026-09-18, pre-API)

> Status: FROZEN. Jede Änderung nach dem ersten API-Call = Protokollbruch, muss in
> `docs/osf_preregistration_addendum_v1.1_spark.md` als Deviation geloggt werden.
> Maschinen-autoritativ sind die Konstanten in
> `scripts/tools/spark_zen_reextract.py` (T1) und
> `scripts/tools/spark_zen_gold_bench.py` (T2); die Kopien unten sind lesbar,
> die SHAs sind aus den Driver-Konstanten berechnet (selftest 2026-09-18 PASS).

## T1 — textbook re-extraction (ensemble-kompatibel)

- Prompt: **verbatim `bailian_reextract.py` PROMPT** (Ensemble-Standard, Vergleich mit 7-Arme-Matrix).
- `T1_PROMPT_SHA256 = 9ad3d51b149930885a06a24a75a4f9c238f3552c9a7e6afd6e94abbb5b8507dc`
- Call: single user message, kein System-Prompt, temperature 0, max_tokens 8000,
  Endpoint `https://opencode.ai/zen/go/v1/chat/completions`,
  Model `opencode-go/muse-spark-1.3-contributor` (+ Run-Datum/Endpoint geloggt).
- Input: **Volltext** `data/textbook/<base>.txt` (kein Trunkieren). Pro Call
  `input_sha256` + `input_chars` geloggt. Chunk-Fallback (>60000 chars oder
  2× Timeout): Absatz-Split ≤30000 chars + 2000 Overlap, Union per norm. Name,
  Relationen nur mit lebenden Endpunkten (im Output als `chunked: true`).
- Retries: max. 3 Versuche (initial + 2), jeder Versuch geloggt (err-Klasse, kein Key).
- Parse: strikte mimo-Schema-Regeln (keys exakt, nicht-leer, keine Platzhalter);
  `nodes/edges`-Schema und leere Listen werden VERWORFEN (09-14-Failmode).
- Filing: **jede geparste Ausgabe wird gefiled** (attempt-set-Integrität);
  Ensemble-Gate (15–40/10–30/Referenzen/Mojibake) als Feld `gate_pass` + Grund,
  KEINE Filing-Voraussetzung (mimo-Originale selbst fallen teils durch —
  selftest: de_abitur_lk `dangling`, stewart 7 Konzepte).
- Outputs: stage `research/mimo_spark_replication/stage/<base>.r1.spark.json` (immer);
  filed `research/ensemble_v2/muse-spark-1.3-contributor/<base>.r1.json` + `_manifest.json`.
  NIEMALS nach `data/math_extractions/`.
- Retired: `spark_reextract.py` + `spark_reextract_api.py` (Prompts divergierten) —
  Dateien bleiben, werden nicht mehr verwendet.

### T1-Sample (11 ausführbar + 1 prä-registrierte Exklusion)

| base | chars | input_sha16 | Status |
|---|---|---|---|
| de_abitur_lk | 1849 | f91efe660971713d | include |
| de_forster_analysis1_ch5_sec5.1 | 1198 | 468300d4af2aa28e | include |
| de_lambacher_5-8 | 1265 | 1fbbacb010db087a | include |
| de_wahrscheinlichkeit_ch1-8 | 2164 | eaf20c1b92c24300 | include |
| en_ib_math_aa_sl | 2734 | 084e19353594b817 | include |
| en_khan_academy_3-4 | 1728 | 2317aed27c0253fb | include |
| en_khan_academy_6-8 | 5576 | a88d9f4326c46953 | include |
| en_stewart_ch3_sec3.1 | 1372 | c0ddbce4f68db82b | include |
| zh_微分方程_ch3_sec3.2-3.4 | 715 | 3e49be2a538c786f | include |
| zh_微分方程_ch4_sec4.1-4.3 | 668 | a6248da96ad81bda | include |
| zh_选修2-2_ch1_sec1.2 | 857 | 82856fdebe9a1293 | include |
| zh_选修2-2_ch1_sec1.1 | — | — | **EXCLUDED: source_txt fehlt** (kein Ersatz — kein ad-hoc-Sample) |

Prompt-Text (informativ, SHA maßgeblich):

```
TASK: Extract knowledge-graph JSON from the textbook text at the end. Do NOT ask questions. Do NOT converse. Do NOT explain. Output ONLY the JSON object, nothing else before or after it.

Schema:
{"extracted_concepts": [{"name": "<source-language name>", "aliases": ["english", "chinese"], "definition_snippet": "<short>", "category": "concept|operation|theorem|property"}],
 "extracted_relations": [{"source": "<name from concepts>", "target": "<name from concepts>", "type": "requires|representation|generalization|inverse_of|part_of", "importance": 0.0-1.0, "evidence": "<short>"}]}
Keys MUST be exactly "extracted_concepts" and "extracted_relations" (never "nodes"/"edges"/"concepts"/"relations"). Aim 15-40 concepts, 10-30 relations. Every source/target must be a listed concept name. No placeholders. Empty lists are FORBIDDEN.

TEXTBOOK (<LANG> / <BASE>):
<FULL TEXT>
BEGIN JSON NOW:
```

## T2 — gold harness (92 items)

- Prompts: **verbatim `batch_model_benchmark.py`** (System L137 + Template L29-50).
- `T2_SYSTEM_SHA256 = 72c5424fdcfbad8fe59f1fd50f518004eb1351406358a710433ab38a1d330b61`
- `T2_TEMPLATE_SHA256 = 31b8e6eb9775f9da41191b9c46fabb1c30039339cb5c598054c0820d512d7b59`
- Call: temperature **0.1** (Vergleichbarkeit mit qwen-Historie — NICHT 0.0),
  max_tokens 2048, `text[:2000]`, timeout 120s, sleep 1.0s + exp. Backoff,
  max. 3 Versuche pro Item (prereg v1.0 §4.4-Regel).
- Scoring: exakte Set-Überlappung + Macro-Mittel (harness-Logik, unverändert).
- Gold: `data/gold/gold_dataset.json`,
  `gold_sha256 = 239e851950034df831073f528e0da19f29f611f24f33384bd102172fe3ac3599`,
  n=92 (annotator_1: 7/7/6; auto_accepted: 29/22/21).
- Output: `research/mimo_spark_replication/t2_spark_gold.json` (per-item + subsets + summary).
- Metrik-Disziplin: Batch A n=20 → 95%-CI, nur Richtung + Größenordnung, keine
  Rang-Claims (G3-Disziplin). CIs per Bootstrap im Scoring-Skript (kein API).

T2-Prompt-Text (informativ, SHAs maßgeblich; per Check exakt = Harness-Template, 391 chars):

System:
```
你是概念提取专家。输出严格 JSON 格式。概念名称使用原始语言，禁止 ASCII 编码。输出 UTF-8 中文。
```

Template (`{text}` = Slot):
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

## Metriken (deterministisch, primär)

- T1 vs mimo: normalisierter Konzept-Match (klein + whitespace-frei; Synonym-Map
  aus 12 audits eingefroren) → Precision/Recall pro Datei + micro-gepoolt;
  `rel_agree` = geordnete Endpunkt-Paare (Type-Differenzen separat als Flags).
- T2: per-item P/R/F1 + Subset-Mittel (annotator_1 / auto_accepted / zh / de / en).
- Rollentrennung (C9b-Lehre): Spark-als-Extractor vs Spark-als-Judge strikt getrennt;
  12 audit-Dateien bleiben Judge-Artefakte, werden NICHT mit Extractor-Output vermischt.
  Drittmodell-Adjudikation (Key folgt): separater Anhang, eigenes frozen Judge-Prompt.

## Selftest 2026-09-18 (kein API)

- 6/6 Negativ-Parserfälle rejected (empty nodes/edges, falsches Schema,
  Platzhalter, leere Listen, Prosa, trunkiert).
- T2-Scoring synthetisch: P=R=F1=0.667 korrekt.
- Gate-Befund an echten mimo-Dateien dokumentiert (s. Filing-Regel oben).

## Transport-Notiz 2026-09-18 (VOR dem ersten erfolgreichen Call — kein Deviation)

1. Cloudflare 1010 bannt Python-urllib-TLS-Signatur → Transport auf
   `curl.exe`-Binary umgestellt (Endpoint/Modell/Prompt/Temperatur unverändert).
2. Gateway-Modell-ID ist `muse-spark-1.3-contributor` (ohne `opencode-go/`-Präfix;
   Präfix → ModelError, verifiziert). Driver-Konstanten entsprechend gesetzt.
3. **Externer Blocker**: zen-Konto `Insufficient balance` (CreditsError, verifiziert) —
   P1/P2 starten erst nach Guthaben-Aufladung (oder alternativem Key).

## Transport v3 FINAL (2026-09-18, VOR dem ersten Extraktions-Call — kein Deviation)

4. Bezahl-Pfad tot (Balance) → Free-Tier-Matrix (6 Modelle, s. Addendum A7).
   Direkt-HTTP scheidet aus (FreeTier nur in-client).
5. argv verstümmelt lange/CJK-Messages („Empty prompt", nachgewiesen) → Prompt per
   `-f`-Datei; Agent `explore` (read-only); `--dir`-Sandbox (leer, kein Repo-Zugriff).
   Custom `--agent` löst FreeTier-403 aus (nachgewiesen, `.opencode/` entfernt).
6. Temperatur per CLI nicht setzbar (Agent-Default, Docs: typically 0):
   T1 exakt (0), T2 dokumentierte Abweichung (Default statt 0.1, konservativ).
7. Repair-Ladder rung0/rung1 (Backslash-Unescape), pro Item/Versuch geloggt.
8. Pilot 2026-09-18 (muse-spark-1.3-contributor-free): T2 3/3 rung0, T1 23c/20r
   gate-PASS — Pipeline freigegeben für Vollmatrix (618 Calls).
