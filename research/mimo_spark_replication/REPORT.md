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

F1-Spalte = A2 (fails als 0 über alle 92 Gold-IDs, D-S6). Sozial-Spalte = A2 über die
72 sozialen IDs (fails als 0); Werte in Klammern = valid-only über valide Items
(alt — nur 6.8/glm betroffen, da einzige Arme mit fails). Arme mit 92/92 sind identisch.

| Modell | F1 (A2) | 95%-CI | P / R | pred_n (gold 2,16) | math (sauber) | sozial (seed-fremd) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-free | 0,199 | [0,160–0,243] | 0,135 / 0,639 | 11,7 | 0,384 [0,269–0,495] | 0,148 [0,111–0,188] |
| muse-spark-1.2-free | 0,160 | [0,127–0,195] | 0,097 / 0,613 | 13,2 | 0,253 [0,165–0,336] | 0,135 [0,103–0,165] |
| MiniMax-M3 | 0,167 | [0,136–0,201] | 0,102 / 0,637 | 13,4 | 0,295 [0,205–0,379] | 0,131 [0,099–0,160] |
| deepseek-v4.1-flash (r4) | 0,132 | [0,103–0,165] | 0,080 / 0,600 | 16,8 | 0,205 [0,121–0,298] | 0,112 [0,084–0,138] |
| sensenova-6.8-flash-lite | 0,121 (0,146) | [0,092–0,154] | 0,089 / 0,599 | 15,0 | 0,199 (n=19) | 0,102 (valid-only 0,129) |
| glm-5.2 (r4-direct) | 0,159 (0,161) | [0,124–0,198] | 0,105 / 0,553 | 12,8 | 0,235 (n=20) | 0,138 (valid-only 0,140) |
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

Pro Sprache (mean F1, overall inkl. Mathe-Domäne — paper §2.9 zeigt dagegen Sozial-only): spark-1.3 zh 0,276 / de 0,223 / en 0,070; spark-1.2 0,227/0,193/0,036;
MiniMax 0,224/0,190/0,065; r4 0,205/0,159/0,005; 6.8-lite 0,226/0,177/0,000 (valid-only; A2: 0,201/0,134/0,000);
glm-5.2 0,263/0,188/0,000 (valid-only; A2: 0,256/0,188/0,000 — s. V2_MATRIX).
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

## 6. Deep-Dive (2026-09-18, deterministisch, zero API — exploratory)

`T2_DEEPDIVE.json/md` (Seed/B wie Matrix) + `T1_PAIRWISE.json/md`. Kerne:

- **Zell-CIs**: Math-Zellen (n=6–7) CI-Breiten ~0,2–0,5 (z. B. en_math 1.3 [0,056–0,383]) —
  keine Zell-Rankings möglich; nur Sozial-Zellen (n=21–29) sind informativ. Formalisiert G3.
- **gold_n-Schichtung**: neue Arme n1 (37 Items) F1 ~0,06–0,13 vs. n2 (55) ~0,16–0,25
  (Überproduktion wird auf Singletons härtest bestraft); qwen INVERTIERT (n1 0,84 > n2 0,55) —
  qwen trifft Singletons mit Gold-Kardinalität. Stärkste F2-Stütze aus vorhandenen Daten.
- **Paired dF1** (prä-deklarierte Paare): 1.3−qwen −0,467 [−0,558–−0,384] (Gap formal);
  1.3−1.2 +0,039 [+0,009–+0,073] (klein, aber gepaart signifikant — schärfer als CI-Überlapp-Blick);
  minimax−glm +0,007 [−0,027–+0,036] (null). Exploratory-Paare deskriptiv, Bonferroni (α≈0,003) beachten.
- **pred_n–F1**: Pearson r −0,31…−0,43 pro Arm (außer 6.8: +0,23 — 429-Fails verzerren, offengelegt);
  Bins monoton fallend (pred 10→20: F1 0,23→0,07). Korrelativ, nicht kausal; pro Sprache konfundiert.
- **T1-Pairwise** (5×11/11-Arme): F1 0,42–0,61 (Mittel 0,53) — Modelle stimmen untereinander
  deutlich mehr überein als mit mimo (micro-P 0,21–0,32; andere Metrik, explizit).
  Stützt „mimo = noisy reference" (M4-Herausforderung) — C22 bleibt Developing mit schärferer Caveat.
- **Difficulty**: n=9 (alle Mathe) — Negativbefund per Design, DO-NOT-USE.
- **Power**: gepaartes Design braucht n≈32–71 für Δ=0,1; n=6–7-Zellen detektieren nur Δ≈0,4+.

## 7. Harness v2 (2026-09-18/19, prereg A11–A17 vor erstem Call)

Cells: P1 (CARD-only) / P2 (LANG-only, EN+DE+zh10) / P3 (BOTH) + P0-cal Drift. Anker: glm-5.2-r4, deepseek-v4.1-flash-r4, 6.8-sn (+ big-pickle P3 western, P0 partial-46). minimax EXCLUDED (owner), F5/qwen CUT (owner).

| Arm | P0 (v1) | P1 | P2 (EN/DE) | P3 | pred_n P0→P3 |
|---|---|---|---|---|---|
| glm-5.2-r4 | 0,159 | 0,500 | 0,167 (EN 0,019, CJK 0 %) | 0,555 (soc 0,544) | 12,8→2,1 |
| deepseek-r4 | 0,132 | 0,545 | 0,197 (EN 0,136, CJK 0 %) | 0,539 (soc 0,544) | 16,8→2,2 |
| 6.8-sn | 0,121 | 0,395 | 0,141 (EN 0,000, CJK 0 %) | 0,421 (soc 0,395) | 15,0→2,6 |
| big-pickle (west) | — (P0 partial-46) | — | — | 0,608 (soc 0,580, EN 0,377) | →2,1 |

Paired dF1 (A2, 95 %-CI): P1−P0 +0,34/+0,41/+0,27 (alle CI≠0); P3−P0 +0,40/+0,41/+0,30;
P2−P0 +0,03/+0,07/+0,02. Drift P0-cal: deepseek −0,03 / 6.8 +0,03 (≈0, sauber);
**glm +0,32 [0,15–0,52] — Serving-Drift über Nacht** (gleicher Prompt/Transport: P0cal pred_n ~5,
en_001 F1=1,0 unter P0!). glm-Lifts daher drift-konfundiert (obere Schranke), deepseek/6.8 sauber.

A13-Verdikte:
- **F1 CARD: CONFIRMED** (2× sauber + 1× caveatiert). pred_n 12–17 → ~2–3; n1-Rettung > n2 (s. V2_MATRIX).
- **F2 LANG: MODEL-SIDE FAILURE.** CJK-Fix in P2/P3 überall befolgt (EN-CJK v1 5–56 % →
  0,0 % bei allen 3 Ankern; Ausnahme: P1-deepseek 9,8 % Rest — CARD-only ohne Sprachklausel),
  EN-F1 bleibt 0,02/0,14/0,00 (Schwelle >0,30 klar verfehlt). DE hebt sich gemischt (glm 0,19→0,24, deepseek ≈, 6.8 ≈).
  Zusatz: EN-Lift kommt aus Kardinalität (P1-EN 0,31/0,23/0,04 ≈ P3-EN), nicht aus Sprachklausel.
- **P3: deepseek V2-VALIDATED** (soc 0,544 ∈ [0,40–0,65]); glm validiert-mit-Drift-Caveat (0,544);
  **6.8 MARGINAL MISS** (soc 0,395 < 0,40 — kein Aufrunden, residual-Seite); big-pickle deskriptiv 0,580 (partial control).
- C9b unverändert Developing. C21 → v2-partial-repro (quantitativ). C23 → gehärtet (CARD 2× sauber).
  Neu C24: Western-EN-Effekt (big-pickle EN 0,377 höchst — Sprachfamiliarität).
- E1 EXTENDED gegenstandslos (alle lauffähigen Arme in CORE); E3/E2 offen (E2 sinnvoll: P3-Lift steht);
  Panel Phase 2 bereit (big-pickle = Western-Rater).
- **E2 P3b (A18, glm n=30): ROBUST.** |P3b−P3| +0,024 [−0,047–+0,091] < 0,05 — P3-Lift ist nicht
  wortlaut-fragil (`t2_v2-glm52r4-P3b.json`, SHAs f91a3dad/8058b210; Kontrast-Produkt `P3B_CONTRAST.json`).

## 8. Agent-Panel Screen (2026-09-19, A-Judge — falsify-only)

5 Rater (deepseek-r4 / glm-r4 / 6.8-sn / cohere-openrouter 51/72 daily-park / big-pickle-zen),
Consensus `--import` (`panel_IMPORT.json`): rejects 15, **Gold-Übereinstimmung (vs-gold) 0,389**,
qwen-F1 0,419 → **MAINTAIN**. (Nicht zu verwechseln mit inter-rater κ=0,56.)
Fleiss κ=0,56, Jaccard ~0,1 (Rauschen hoch!). **Dissent-Kern: 11/72 einstimmige Rejects**
(A005/A006/A014/A018/A020/A022/A027/A028/A032/A035/A041) — Falsifizierungs-grade Gold-Qualitätslücke (~15 %);
R2 (glm, 36 Rejects, 14 solo) = Rater-Rauschen. Spot-Check (owner, 12 Items) + R4-Full offen.
Details `research/gold_review_v2/PANEL_SCREEN.md`. C9b bleibt Developing (schärfere Caveat).
