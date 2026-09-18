# Spark Replication Arm — Final Report (2026-09-18, Datenstand 21:30, rev4)

Frage: Hält die §2.3/§2.8-Extraktionsqualität mit seed-fremden Modellen?
Protokoll: `research/mimo_spark_replication/PROMPT_FROZEN_v1.md` ·
Prereg: `docs/osf_preregistration_addendum_v1.1_spark.md` (A1–A10) ·
Deviations: `research/deviation_log_20260918_spark.md` (D-S1–D-S7).

## 1. Datenvollständigkeit

| Arm | muse-spark-1.3-free | muse-spark-1.2-free | mimo-v2.5-free | MiniMax-M3 (direct) | deepseek-v4.1-flash (r4) | sensenova-6.8-flash-lite | sensenova-6.7-flash-lite | glm-5.2 (r4-direct) |
|---|---|---|---|---|---|---|---|---|
| T1 (11 Basen) | 11/11 filed | 11/11 filed | ARCHIVIERT (36 Dateien, s. u.) | 11/11 filed | 10/11 filed | 11/11 filed | 0/11 (Breaker-Park) | 11/11 filed |
| T2 (92 Gold) | 92/92 | 92/92 | nie gestartet (pending→retired) | 92/92 | 92/92 | 92 Items / 76 valide | 5 Items / 0 valide (Breaker-Park) | 92 Items / 91 valide |

- mimo-v2.5-free: Owner-Retirement 2026-09-18, 36 Dateien archiviert
  (`research/archive_mimo-v2.5-free_20260918/` + README), aus allen Matrizen entfernt.
- u1-fast + u1.5-lite: Bildgenerierungs-Modelle (Owner-Angabe) → EXCLUDED, nie gelaufen.
- T1-Fehlstand r4-deepseek: `de_wahrscheinlichkeit_ch1-8` (wiederholte Versuche:
  3 stage-belegt — 2× RuntimeError + 1× parse_fail — plus Vorlauf-Timeouts aus der
  D-S1-Pilotphase; staged, keine weiteren Retries). **glm-5.2 (gleicher Transport r4)
  löst dieselbe Base im 1. Versuch (c=40/r=30, gate=True, rung=0)** — Fehlstand ist
  modellseitig, nicht transportseitig.
- sensenova-Quota-Bill (gezählt aus attempt-Logs): **~416 Calls** (T1 254 + T2 162),
  davon Großteil 9-Parallel-Sturm-Fehlversuche (s. D-S4).
- r4-Bill glm-5.2: **~96 Calls** (T1 1 + T2 3 Smoke + 92 Full + 1 Fehlstand zh_033×3 in
  den 92 enthalten); separater Key/Kontingent, nicht Teil der sensenova-Bill.
- Restliche sn-Arme (deepseek-v4-flash 2/11, deepseek-v4-pro 2/11 aus Sturm;
  kimi-k3, u1.5-fast leer): partiell, nur nach Owner-Freigabe fortgesetzt.

## 2. T2-Ergebnisse (harness-exakt, inkl. Bootstrap-95%-CI, B=1000, seed 20260918)

F1-Spalte = A2-konform (fails als 0 über alle 92 Gold-IDs, D-S6); Werte in Klammern =
valid-only (alt). Arme mit 92/92 sind identisch.

| Modell | F1 (A2) | 95%-CI | P / R | pred_n (gold 2,16) | math (sauber) | sozial (seed-fremd) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-free | 0,199 | [0,160–0,243] | 0,135 / 0,639 | 11,7 | 0,384 [0,269–0,495] | 0,148 [0,111–0,188] |
| muse-spark-1.2-free | 0,160 | [0,127–0,195] | 0,097 / 0,613 | 13,2 | 0,253 [0,165–0,336] | 0,135 [0,103–0,165] |
| MiniMax-M3 | 0,167 | [0,136–0,201] | 0,102 / 0,637 | 13,4 | 0,295 [0,205–0,379] | 0,131 [0,099–0,160] |
| deepseek-v4.1-flash (r4) | 0,132 | [0,103–0,165] | 0,080 / 0,600 | 16,8 | 0,205 [0,121–0,298] | 0,112 [0,084–0,138] |
| sensenova-6.8-flash-lite | 0,121 (0,146) | [0,092–0,154] | 0,089 / 0,599 | 15,0 | 0,199 (n=19) | 0,129 (n=57; n72=0,102) |
| glm-5.2 (r4-direct) | 0,159 (0,161) | [0,124–0,198] | 0,105 / 0,553 | 12,8 | 0,235 (n=20) | 0,140 (n=71; n72=0,138) |
| qwen-plus (Historie) | 0,666 | [0,587–0,752] | 0,642 / 0,719 | 2,5 | 0,724 | 0,650 |
| qwen-max (Historie) | 0,661 | [0,583–0,746] | 0,642 / 0,702 | 2,5 | 0,707 | 0,648 |

6.8-Details: 76/92 valide (16 fails offengelegt); EN-Subgruppe 22/22 valide alle F1=0,000
(vollständiger EN-Kollaps, s. F2b); T1 micro-P/R 0,285/0,447 (höchste P unter den
serien-sensenova-Armen; über alle 11/11-Arme führt spark-1.2 mit 0,316).
6.7: Breaker-Park T1 (5×3) + T2 (5×3), 0 valide Outputs — Gateway-Inkompatibilität,
kein Qualitätsurteil möglich.
glm-5.2-Details: 91/92 valide (1 fail zh_033, 3× parse_or_empty offengelegt);
EN-Subgruppe 27/27 valide alle F1=0,000 (zweiter vollständiger EN-Kollaps nach 6.8);
T1 micro-P/R 0,253/0,356 (11/11; wahrscheinlichkeit-Base löst glm im 1. Versuch,
die r4-deepseek 6× scheiterte — s. §1).

Pro Sprache (mean F1): spark-1.3 zh 0,276 / de 0,223 / en 0,070; spark-1.2 0,227/0,193/0,036;
MiniMax 0,224/0,190/0,065; r4 0,205/0,159/0,005; 6.8-lite 0,226/0,177/0,000;
glm-5.2 0,263/0,188/0,000.
EN-Kollaps: 5–56 % der EN-Predictions
enthalten CJK-Zeichen (System-Prompt befiehlt wörtlich „输出UTF-8中文" UND „原始语言" —
widersprüchlich; qwen-Historie: EN/DE 0 % CJK, ZH 99 % CJK, d. h. Quellsprache).

## 3. Befunde (mit Status-Kennzeichnung)

- **F1 (prä-registriert, A5)**: Kein Arm reproduziert 0,939. Beide A5-Äste
  (0,60–0,70 / ≥0,85) VERFEHLT (sozial A2-konform 0,10–0,15; valid-only 0,11–0,15). Die prä-registrierten
  Deutungen greifen nicht; alles Folgende ist POST-HOC/exploratory.
- **F2 (post-hoc, Mechanismus)**: Die Lücke erklärt sich vollständig aus zwei
  unkontrollierten Verhaltensdimensionen: (a) Kardinalität — Prompt verlangt 10–20,
  Gold hat 2,16, qwen predicts 2,5 (prompt-d disobedient, belohnt), neue Arme 11,7–16,8
  (prompt-obedient, bestraft: P 0,08–0,14 bei R ~0,6; glm pred_n 12,8); (b) Ausgabesprache
  (s. EN-Kollaps — glm: 27/27 EN valide, alle F1=0,000, bei nur 20 % CJK-Anteil).
  Fazit: T2-F1 misst Prompt-Gehorsam × Exaktmatch, nicht Extraktionsqualität.
  Ob 0,939 ein Seed-Artefakt ist, bleibt UNENTSCHIEDEN (C9b unverändert Developing).
- **F3 (prä-registrierbar gewesen, jetzt Befund)**: Harness-Designfehler — 10–20 vs.
  2,16 Gold; widersprüchliche Sprachanweisungen; 2048-Ceiling bindet Reasoning-Modelle
  (D-S1). Empfehlung: Harness v2 (kardinalitätskontrolliert), KEIN retroaktives Rescoring.
- **F4 (T1, deterministisch)**: Modellabhängigkeit der §2.3-Inputs bestätigt —
  micro-P vs. mimo 0,21–0,32, rel_agree 0,8–2,0/Datei; konsistent mit Ensemble-Verdict
  (vs. mimo 0,22–0,26). Details `T1_AGREEMENT.md`.
- **F5 (Methodik)**: Intra-Run-Varianz trotz temp≈0 (zh_001 Pilot 0,353 vs. Vollauf 0,400) —
  stützt Ensemble-C1 („temp=0 nicht deterministisch"). Ranking spark-1.3 > 1.2 auf
  Math (0,384 vs. 0,253) hat überlappende CIs → KEIN Rank-Claim (G3-Disziplin).
- **F6 (Scope)**: Alle Schlüsse gelten nur für exakte (Modell, Endpoint, Datum)-Tripel;
  free≠paid, Provider≠Provider (A7/A8).

## 4. Rigor-Ledger (Kurzfassung)

Prereg A1–A10 vor jeweiliger Datenerhebung (A8 inkl. D-S1-Verweis; A9 Parallel-Disziplin,
die nach Owner-Order auf seriell (A10) umgestellt wurde; A10 Image-Ausschluss + Reihenfolge);
Prompts SHA-gefroren
(T1 `9ad3d51b…`, T2-System `72c5424f…`/Template `31b8e6eb…`, T2≡Harness-Template 391 chars);
Transport v1→v3 + sn-Direkt dokumentiert (Cloudflare-1010, Modell-ID ohne Präfix, argv-Mangling,
Custom-Agent-403, Sandbox-Kontamination-Ausschluss); D-S1 (r4-Ceiling, per Bounds-Argument
2026-09-18 CLOSED: qwen längstes Output 150 Zeichen ≪ 2048-Token-Ceiling), D-S2 (Orphan-Bereinigung, CLOSED), D-S3 (T2-Summary-
Print-NameError, datenneutral, CLOSED), D-S4 (9-Parallel-Sturm: KeyError-`sn` +
fehlender Breaker + fehlende Smoke-Gate + grobe Err-Logs; Korrekturen verifiziert:
Breaker parkte 6.7 zweimal korrekt; Quota-Bill ~416); D-S5 (opencode-Wrapper-Timeout
vs. Direkt-Treiber: Langläufe für Direkt-Transporte per `python3 scripts/tools/…` im
Hintergrund + Log-Polling, nicht via Agent-Wrapper; `--max-items`-Flag für Smoke;
kein Dateneinfluss); D-S6 (A2-Nenner-Korrektur: F1-Spalte = fails-als-0/92, valid-only
in Klammern; nur 6.8/glm betroffen); D-S7 (glm sn→r4 + 8192 Nachtrag: Prompt unverändert,
Ceiling-Bindung nicht nachweisbar, konservativ-ungenutzt); Keys nur `.env` (ignored),
Rotation empfohlen.

## 5. Paper-Vorschläge (angewendet, factual only)

- §2.9-Tabelle: 6 neue Zeilen (Sozial-Spalte + Gesamt, mit Developing-Markierung;
  6.8-lite + glm-5.2 mit Valide-Nenner- flag, P3-Entscheid 2026-09-18).
- §2.8: Mechanismus-Absatz (Kardinalität + Sprachausgabe + A5-verfehlt + Harness-v2-Empfehlung).
- Keine Änderung an bestehenden Behauptungen/C9b-Status.
