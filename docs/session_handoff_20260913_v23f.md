# Session Handoff — 2026-09-13 spät (v23f-replication58)

> Stand: 09-13-Replikation eingepflegt (58/53/174) | Nächster Meilenstein: Plattform-Eintragung → Tag `v1.0-bwki-submission` → Puffer bis 20.09.

## Was diese Session geliefert hat

`multi_model_replication_20260913.json` (10:01) löst 09-10 ab. Drei Modelle promoviert (alle n=30 OK, per Skript verifiziert):
- **grok-4.6**: LDS 0.9519/0.9322/0.9258, Marge +0.09 (xAI, US)
- **llama-3.3-70b**: 0.7988/0.7652/0.8367, Marge +0.12 (Meta-Gewichte, US → Western)
- **muse-spark**: 0.9480/0.9130/0.9343, Marge +0.12 (Herkunft offengelegt → Western)

Formale Zahlen: **58 n=30 / 53 Identitäten / 174 Tests**; file-truth **59/54/177** (inkl. qwen-max n=26/30: 3 Quota-Leerläufe gestrippt, LDS stabil 0.9331/0.9488/0.9582); 81 Keys (6 Dubletten bereinigt); collecting 24 (22 ERR + qwen-max + phi-4-mini n=25, ZH-DE-Voter per min-units=5).

Nachzählung (Skript, `direction_consistency` + Replikations-JSON):
- EN n.s. 8/174, alle EN-haltig (R1/Distill 6/10 EN-Tests, EN-Boden 0.844 vs 0.775 übrige)
- Strata: CN 48/48 (0.130) vs West 10/10 (0.162); ohne luna 9/9 (0.155); CN-Anteil ~83 %
- Votes (60 Voter): ≥3: 1179/919 · ≥10: 236/156 · ≥20: 72/14; Heimat:safety 48 DE / physical space 45 ZH / equal opportunity 45 → Paper-Zähler „48 von 59"
- Dedup 53/53 (0.138 vs 0.135); Youden 0.12 (CI 0.12–0.13), Heuristik 0.10 sensitiv-inklusiv; West-Ratio 1.242 vs CN 1.169; Spearman Marge/Ratio 0.997, Top-5 identisch

Angefasste Orte: Portal-Roster 58-row (strikt desc, spark/llama einsortiert, gpt-oss-Sortfix auch in Galaxie), MARGIN 58×3, Collecting-Tabelle aus 09-13-Keys neu (24, inkl. phi-4-mini n=25), cspace-Galeriekarte, SSOT-web (+v23f), Paper 01/02/03/04/05, Plattform §6 + feld_mapping (1684/1700 — nur 16 Puffer!), final/README + declaration (docs-Spiegel mit), Root-README-Trio, evidence C19, PDF 229964B ×3, `sw_fix_analyses.py` → 09-13 (+llama-Marker), `_deploy`-Spiegel komplett.

## Offen
1. Plattform-Upload (User): §6 = 1684 Zeichen — bei kürzerem Feld zuerst Tabelle kompaktieren
2. Tag `v1.0-bwki-submission` erst nach Eintragung
3. Lokal-Welle weiter laufend — `*_20260913.json`-Neuzugänge nicht committet
4. C4 Mono-Control-Bug weiter eingefroren; Video/SRT baked-freeze unberührt; `sync_readmes.py` weiter verboten
5. session_handoff_20260913.md (v23e) als Historie belassen

## Zähl-SSOT (aktuell)
- 556/525/219 · 204 = 32+83+89 · **58/53/174** (file-truth 59/54/177) · qwen-max n=26/30 · F1 0,881/0,939 · N=15 Δ≈0 · Freeze 0,9336/0,9382/0,5188 · T1 0,52→0,99
