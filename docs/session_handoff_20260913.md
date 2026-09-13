# Session Handoff — 2026-09-13 (v23e-audit: Full-Repo-Alignment)

> Stand: master `f19149e` (gepusht) | Nächster Meilenstein: Plattform-Eintragung (bis 9/13-Manuel-Upload) → Tag `v1.0-bwki-submission` → Puffer bis 20.09.

## Was diese Session geliefert hat (Commit f19149e, 41 Dateien)

Vollständige Datei/Doku/Abb./Paper/Programm-Aktualisierung + Prüfung (Plan: 3 parallele Read-Only-Audits → Build-Ausführung A→B→C→D→E). Evidenzregel durchgehend: Unsicheres nur in **Evidenz-unzureichend/Versuch**-Zonen, nie als formale Aussage.

### Paper A1–A7 (docs/paper/)
- A1 `04:102` F1-Dreisprachig → Sozial-Subgruppen-Label (n=72; gewichtet 0,881)
- A2 `00:32,39` Physik-Wurzeln 64 % → **60 %** (219/367)
- A3 `06:3` 81 → **83 Titel** (94 Refs; +NPTEL/LEIFI aus v18)
- A4 `04:140` qwen-plus-Scope → LDS-K/Gold; N=15-LDS-C = deepseek-v4-flash
- A5 Coverage-Granularitäts-Confound (CN 87 vs. US 2124 vs. NRW 299) in `02:210`, `05:26,52`; `04:70` Governance → Hypothese
- A6 219-Einheitenmix → Gruppen≠Konzepte-Notiz (`01:18`, `02:94`)
- A7 `46 von 56` → Datei-Wahrheits-Label (03:393, 04:222); `03:165` p=0,08-SE/CI-Ehrlichkeitsnote (keine Signifikanz-Deutung, ≥1000-Perm. ausstehend)

### Portal B1–B7 + Deploy-Hygiene
- B7: 4 tote Übersetzungen aktiviert (`figBases` +19→20…→23 Einträge: wikipedia/fig4_heatmap/fig5_hds/fig6_cds); Fig5-Caption dreisprachig + Forensik-Hinweis
- B1 wasd.toggle (fehlender Key) → wasd.on; B2 Footer-Mojibake verifiziert **bereits sauber** (0 U+FFFD); B3 portal/README 366→367, cspace soon_d Chemie→live; README_DE/ZH Badge-alt + NRW-NA übersetzt
- B4 PDF-Drift behoben (s. C1); B5 `_deploy/README*.md` Screenshot-Pfad → `web/screenshot.png`; B6 3 Streudateien aus `_deploy` gelöscht + Workflow-Ausschlussregel; `_deploy/index.html` nach Workflow-Logik neu aufgebaut
- SSOT-web: Textbooks 204-Titel-Summe (P2b#8 alt-180 retired), Wave-2-Frische-Notiz (CSV-neuer-als-PNG = Design, Gate MAE=0,000)

### C-Rechecks / D-Smoke
- C1: `docs/submission`-PDF war v22-vorherig (222388B); neu **229717B/172010 chars** (inkl. A-Fixes), 3 Orte byte-identisch + Checklisten-Anti-Drift-Regel
- C2/C3: EN-stale + CSV-neuer-als-PNG als benign verifiziert (`figures_i18n_wave2.py --check` ALL OK)
- D1: pytest **84/84**, `release.py --dry-run` OK (Nebenwirkungen revertiert: manifest.json/quality_history/data-manifest), Freeze-Repro exakt (0,9336/0,9382/0,5188), Manifest-Null-Drift
- D2: `plattform_antworten` 2 Overclaims repariert (§7 Konvergenz→T1-Wording; §5 stark→konsistent); `feld_mapping` Zeichenzahlen neu vermessen (§6 = **1682**, nur 18 unter 1700-Limit!); `docs/submission`-Spiegel (plattform/code) aus final/ synchronisiert; `code_einreichung` statsmodels→scikit-learn, final/README API-Key-Irrtum korrigiert
- E: Retired-Sweep (1179/§8.17/43-DashScope/64 %/81-Titel) null Treffer in paper+final; 5 Spiegelpaare SAME

## Offen / Nächste Schritte
1. **Plattform-Upload (User)**: `submission/final/plattform_antworten.md` + `feld_mapping.md` (Achtung §6 1682 Zeichen — bei kürzerem Feld zuerst Tabellen kompaktieren)
2. Tag `v1.0-bwki-submission` erst nach Eintragung
3. **Lokal-Welle läuft weiter** (supervisor v2, phi-4-mini; `data/lds_c/llm_subject/*_20260913.json` wächst) — bewusst nicht angefasst, nicht committet
4. C4 Mono-Control-Bug (`fig4:395-401`, CSV-Row8 leer) weiter **eingefroren** als bekannte Limitation (keine Entscheidung → kein Fix)
5. B7-folge: `sync_readmes.py` bleibt **verboten** (body_map Alt-Stand 366/1160+/N=8) — READMEs nur manuell synchronisieren

## Zähl-SSOT (unverändert bestätigt)
- 556/525/219 · 204 = 32+83+89 · 68/72/32 · 55/50/165 (file-truth 56/51/168) · F1 gewichtet 0,881 (sozial 0,939) · N=15 Δ≈0 · Freeze 0,9336/0,9382/0,5188 · T1 0,52→0,99
