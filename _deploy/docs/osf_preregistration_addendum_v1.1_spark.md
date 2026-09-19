# OSF Pre-Registration Addendum v1.1 — Muse Spark Replication Arm (2026-09-18)

> Status: COMMITTED BEFORE ANY API CALL of this arm. v1.0 (`docs/osf_preregistration.md`)
> bleibt eingefroren; dieses Addendum ergänzt nur den Replikations-Arm.
> Protokoll: `research/mimo_spark_replication/PROMPT_FROZEN_v1.md`.

## A1. Hintergrund und Fragestellung

- C9b-Limitation (paper §2.8): Sozial-F1 0,939† ist DB-Pfad + Same-Source-Seed
  (qwen-plus) — harness-reberechnet ~0,65, Blind-Review ausstehend.
- Ensemble-Matrix (research/ensemble_v2, 7 Modelle, depth24, r1–r3) misst
  intra/inter/vs-mimo — aber kein Arm mit seed-fremdem Modell auf Gold.
- Replikationsfrage: **Hält die Extraktionsqualität mit einem vom Seed-Modell
  unabhängigen Modell (Muse Spark 1.3 Contributor)?**
  - T2 misst absolute Qualität (Batch B erstmals seed-fremd).
  - T1 misst Modellabhängigkeit der §2.3-Inputs (Spark vs mimo agreement).

## A2. Arme und Samples (frozen)

- **T2**: alle 92 Items `data/gold/gold_dataset.json` (sha s. Frozen-Protokoll).
  Keine Subgruppen-Auswahl, keine Items ausgeschlossen außer leere
  (text/gold leer → als failed mit Grund geloggt, zählt im Nenner).
- **T1**: 11 Basen (12 audits − `zh_选修2-2_ch1_sec1.1`, source_txt fehlt —
  prä-registrierte Exklusion, kein Ersatz). Single-run (r1); r2/r3 nur nach
  separater Freigabe (außerhalb dieses Addendums).

## A3. Eingefrorene Parameter

T1: Prompt-SHA `9ad3d51b…`, temp 0, max_tokens 8000, Volltext-Input,
Chunk-Fallback erst >60000 chars / 2× Timeout. T2: System-SHA `72c5424f…`,
Template-SHA `31b8e6eb…`, temp **0.1**, text[:2000], max 3 Versuche/Item.
Modell-ID + Endpoint + Run-Datum pro Output geloggt; served-Revision als
UNVERIFIED gebucht (§2.12-Ehrlichkeitsregel).

## A4. Metriken und Entscheidungsregeln (vorab)

1. Primär: deterministische Skripte (T1: norm. Match P/R + rel_agree;
   T2: harness P/R/F1 + Subset-Mittel + Bootstrap-CIs).
2. Batch A (n=20): nur Richtung + Größenordnung, keine Rang-Claims.
3. Filing: jede geparste Ausgabe gefiled (kein Gate als Filing-Hürde —
   Selektionsbias-Verbot); Gate als Feld.
4. Leere/ungeparste Outputs: ≤3 Versuche, alle Versuche geloggt;
   danach als `failed` im Nenner (kein stilles Droppen — 09-14-Failmode).
5. Drittmodell-Judge (Key folgt): nur Disput-Subset, eigenes frozen Prompt,
   separater Anhang; ändert keine Primärzahlen.

## A5. Vorab-Interpretationen (Anti-HARKing)

- **T2-Batch-B (n=72, seed-fremd)**:
  - Falls Spark-social ≈ 0,60–0,70 → bestätigt Harness-Niveau; 0,939 als
    DB-Pfad-Wert eingemauert, paper-Formulierung bleibt (ggf. verschärft).
  - Falls Spark-social ≥ 0,85 → Seed-Konfundierungs-Narrativ geschwächt;
    dann Modellabhängigkeit statt Seed-Artefakt als Arbeitshypothese,
    paper §2.8 + G3-Notiz werden revidiert (kein nachträgliches Uminterpretieren
    ohne diese Revision).
  - Dazwischen (0,70–0,85) → unentschieden, nur als Zahl berichtet + CI.
- **T1**: agreement wird NUR als baseline-relative Modellabhängigkeit berichtet
  (mimo selbst unverifiziert — kein Arm darf mimo als Wahrheit behandeln).
- **68-vs-75-Befund** (P0): 68 reale Extraktionsdateien + 5 Derivate + 1 gelöschtes
  Manifest = 74 Artefakte; „75" aus History nicht rekonstruierbar (nur 35 Pfade je
  git-added). Paper-§2.3-Zahl bleibt bis P3 unberührt; P3 schlägt Fußnote vor
  („68 Arbeitsstand-Dateien; 75 = Juni-Stand inkl. Kapitel-Splits").

## A6. Quarantäne und Verbote

- Outputs nur `research/mimo_spark_replication/` + `research/ensemble_v2/muse-spark-1.3-contributor/`;
  **Verbot**: Schreiben nach `data/math_extractions/`, `freeze/`, `tests/`-Änderungen.
- Key (`OPENCODE_ZEN_API_KEY`) nur in-process aus `.env`; nie geloggt/gedruckt/committet.
- Paper-Edits erst in P3 und nur Ergebniszeilen (keine neuen Behauptungen ohne
  diese Daten); jede Protokolländerung nach dem ersten Call = Deviation
  (hier + `research/deviation_log_*.md`).

## A7. Transport v3 + Free-Modell-Matrix (2026-09-18, VOR Datenerhebung)

Ersetzt den bezahlten zen-Direktzugang (Insufficient balance) und Transport v1/v2.
Alle Nachweise VOR dem ersten Extraktions-Call; Prompt-Inhalte unverändert (SHAs gelten).

1. **Transport**: Prompt per `-f`-Datei attachiert (argv verstümmelt lange/CJK-Messages;
   Agent sah „Empty prompt" — nachgewiesen), Agent `explore` (read-only),
   `--dir` Sandbox-Leerverzeichnis (Kontaminations-Ausschluss: kein Repo-Zugriff).
   Kurz-Instruktion ASCII. Custom `--agent` löst FreeTier-403 aus (nachgewiesen,
   `.opencode/`-Versuch restlos entfernt) → Default-Pfad.
2. **Temperatur**: per CLI nicht setzbar; Agent-Default per Docs „typically 0".
   T1 (frozen temp 0) exakt; T2 (frozen 0.1) mit Default-Temp als dokumentierte
   Abweichung — Richtung konservativ (weniger Varianz), im Report offengelegt.
3. **Repair-Ladder** (parser, geloggt pro Item): rung0 direkt; rung1
   Backslash-Unescape (`\"`→`"`); danach fail (max. 3 Versuche).
4. **Frozen Modell-Liste (6)**: `muse-spark-1.3-contributor-free`,
   `muse-spark-1.2-contributor-free`, `mimo-v2.5-free`, `ling-3.0-flash-fin-free`,
   `nemotron-3.5-lightning-free`, `nemotron-3-ultra-free` (alle per Ping verifiziert).
   Exkludiert (prä-registriert): `deepseek-v4-flash-free` (direkt-400 + in-client
   Server-Error). Kein nachträgliches Hinzufügen/Entfernen nach Ergebnissicht.
5. **Umfang**: 6 × (92 T2 + 11 T1) = 618 Calls; pro Modell eigene Output-Dateien,
   resume-sicher (valide Items bleiben). Persistente Modell-Ausfälle (>20% failed
   nach Retries) → Modell als `incomplete` berichtet, kein Ersatz, kein Droppen.
6. **Free≠Paid**: keine Äquivalenzbehauptung zwischen `-free`-IDs und Bezahl-Modellen;
   Schlüsse gelten nur für die exakten IDs + Run-Datum.
7. Drittmodell-Judge-Key steht aus (Nutzer); falls nie geliefert: deterministisch-only
   + Offenlegung (kein Silent-Drop des Adjudikations-Arms).

## A8. Direkt-Transporte: MiniMax M3 + DeepSeek-v4.1-flash (2026-09-18, VOR Datenerhebung)

Anlass: zen-Free-Quota erschöpft (nachgewiesen: 1h Null-Output + Orphan-Prozesse,
bereinigt 2026-09-18). Nutzer stellt zwei Keys (`.env`, git-ignored).

1. **Frozen Paare**: `MiniMax-M3` × `https://api.minimaxi.com/anthropic/v1/messages`
   (Anthropic-Form, nativer `system`-Param); `deepseek-v4.1-flash` ×
   `https://api.r4.codes/v1/chat/completions` (OpenAI-Form, native `system`-Role).
   Beide per Ping verifiziert (HTTP 200 + Modell-Output).
2. **Temperatur-Restauration**: T1 = 0, T2 = 0.1 — exakt die frozen Werte;
   Transport-v3-Default-Temp-Abweichung ist damit gegenstandslos.
   System-Trennung (T2) ebenfalls restauriert. Prompt-Inhalte/SHAs unverändert.
3. **Namespace-Trennung**: Outputs `t2_mm-minimax-m3.json` /
   `t2_r4-deepseek-v4.1-flash.json`; Ensemble-Dirs
   `ensemble_v2/mm-minimax-m3/` + `ensemble_v2/r4-deepseek-v4.1-flash/` —
   KEINE Vermischung mit den Bailian-Armen (`minimax-m3/`, `deepseek-v4.1-flash/`
   existieren bereits); Provider-Differenz wird als Feld geloggt.
4. **Umfang**: 2 × (92 T2 + 11 T1) = 206 Calls; Ausführung zweigleisig-parallel
   (je Modell serial: T1→T2; Lock pro Namespace; Checkpoint/Heartbeat wie bisher).
5. **Free≠Paid + Provider≠Provider**: keine Äquivalenz zwischen `-free`-IDs,
   Bezahl-Modellen oder Provider-Routen desselben Gewichts-Namens; Schlüsse nur
   für exakte (Modell, Endpoint, Datum)-Tripel. Cross-Provider-Vergleiche
   (Bailian vs. direkt) nur exploratory.
6. Key-Hygiene: Keys nur `.env` (in-process, nie geloggt/gedruckt/committet);
   Rotation nach Versuchsende empfohlen (Chat-Log-Persistenz).
7. mimo-T2 bleibt `incomplete-pending` (A7-Regel 5); diese Matrix ersetzt sie nicht.
8. Deviation-001 (D-S1): T2-r4 max_tokens 2048→8192 (Reasoning-Headroom; ceiling
   only) — s. `research/deviation_log_20260918_spark.md`. Prompt/Metrik unberührt.

## A9. Sensenova-Matrix + mimo-Retirement (2026-09-18, VOR Datenerhebung)

1. **mimo-v2.5-free retired** (Owner-Entscheidung): 36 Dateien archiviert unter
   `research/archive_mimo-v2.5-free_20260918/` (+README); aus ARMS/Matrizen entfernt;
   August-Historie/Disclosures unberührt. T1_AGREEMENT neu berechnet (ohne mimo).
2. **Frozen 9er-Liste** (`https://token.sensenova.cn/v1/models`, verifiziert 2026-09-18):
   `sensenova-6.7-flash-lite`, `deepseek-v4-flash`, `glm-5.2`, `sensenova-u1-fast`,
   `sensenova-6.8-flash-lite`, `sensenova-u1.5-lite`, `deepseek-v4-pro`, `kimi-k3`,
   `sensenova-u1.5-fast`. Kein Hinzufügen/Entfernen nach Ergebnissicht.
3. **Transport `sn`** (OpenAI-Form, `SENSENOVA_API_KEY` aus `.env`): temp T1=0/T2=0.1,
   max_tokens 8000/2048, user-only (T1) / native system (T2), Prompt-SHAs unverändert,
   Namespace `sn-<id>`, Endpoint+Datum geloggt.
4. **Ausführung**: 9 Linien parallel, linien-intern serial (T1→T2), per-ns Lock,
   sleep 10 / timeout 300 / 3 Versuche (429 gleich behandelt, geloggt), Checkpoint+Heartbeat.
5. **熔断**: 5 aufeinanderfolgende Totalausfälle → Linie parken (incomplete), kein Burn.
6. **Reasoning-Regel**: content→reasoning_content-Fallback (geloggt); falls
   empty-content+reasoning → Modell-Ceiling auf 8192 + D-Sx-Log (D-S1-Präzedenz).
7. Cross-Gateway-Vergleiche (sensenova vs. Bailian/r4 bei Namensgleichheit) nur exploratory.
8. Paper §2.9: ob 9er-Zeilen aufgenommen werden, entscheidet P3-Review (kein Vorab-Versprechen).

## A10. Image-Ausschluss + serielle Reihenfolge (2026-09-18, VOR sensenova-Vollauf)

1. `sensenova-u1-fast` + `sensenova-u1.5-lite` sind Bildgenerierungs-Modelle
   (Owner-Angabe) → EXCLUDED, nie gelaufen, keine Outputs, aus ARMS entfernt.
2. Ausführung seriell (Owner-Entscheidung ersetzt A9-Parallel): zuerst
   `sensenova-6.8-flash-lite` (Smoke: T1+T2 OK), dann `sensenova-6.7-flash-lite`
   (Smoke: beide fail — läuft trotzdem auf Owner-Order; Breaker begrenzt Burn
   auf max. 5 Items × 3 Versuche, danach Park mit Evidence).
3. Restliche sn-Arme (deepseek-v4-flash, glm-5.2, deepseek-v4-pro, kimi-k3,
   sensenova-u1.5-fast) nur nach weiterer Owner-Freigabe.
