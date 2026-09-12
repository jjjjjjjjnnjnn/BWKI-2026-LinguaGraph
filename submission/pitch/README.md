# LinguaGraph — Video-Pitch (separater Workflow)

> Spec: 2–4 Min · 1080p · H.264 | Skript: `video_script.md` v2 (AI-Audit-Framing, DE-Narration + EN-Untertitel)
> Status: **Finals vorhanden (2026-09-11, 173s, gleicher Schnitt)** — Master: separates Video-Repo (`nach/`, v4-Pipeline, 32 Steps, Narration-SSOT `nach/docs/narration_de.md`, Faktencheck `nach/docs/faktencheck.md` unterschrieben). Dieses Verzeichnis hält nur die **Einbettungs-Kopien** für Repo + Portal.

## Finals (Einbettungs-Kopien, Stand 2026-09-11)

| Datei | Inhalt | Größe |
|---|---|---|
| `LinguaGraph_BWKI2026_Pitch_4K.mp4` | DE ohne Untertitel (Default-Quelle, 3840×2160 h264/aac) | 14.3 MB |
| `LinguaGraph_BWKI2026_Pitch_4K_subs_en.mp4` | gleicher Schnitt + EN-Untertitel (eingebrannt) | 23.8 MB |
| `LinguaGraph_BWKI2026_Pitch_4K_subs_zh.mp4` | gleicher Schnitt + ZH-Untertitel (eingebrannt) | 22.1 MB |
| `assets/pitch_poster.jpg` | Poster-Frame (t60s) | — |

> Quelle: `nach/renders/final/` (Video-Repo, wird dort gepflegt — hier nicht rendern, nur kopieren). 112-MB-4K-Master bleibt im Video-Repo/Release, nicht im Git.

## Storyboard (aus `video_script.md` v2)

| # | Szene | Material | Quelle |
|---|-------|----------|--------|
| 1 | Problem: mehrsprachige KI, blinder Fleck Evaluation | Titel + Portal-Screenshot | `cognitive-space/portal/index.html` |
| 2 | Methode: MIMO-Extraktion → KG → LDS | Pipeline-SVG | `submission/idea/assets/` |
| 3 | Beleg: Konzeptgraph 3D | Screen-Recording | `cognitive-space/web/index.html` |
| 4 | Beleg: LDS-Balken + Treiberliste | Screen-Recording | Portal Finding E / §5.10 |
| 5 | Ehrlichkeit: N=15-Negativ + P2-Recheck + 8 n. s. | Divergenzbericht-Mockup | `docs/paper/03_results.md` §5.10 |
| 6 | Nutzen: Entwickler/Regulierer/Forscher + heuristische Schwelle 0,10 | Schlusstitel | `docs/paper/00_three_conclusions.md` |

## Fakten-Check (Pflicht vor Upload — v0.13.2-Zahlen)

- 556 Konzepte / 525 Relationen / 219 Gruppen; F1 sozial 0,939, gewichtet 0,881
- N=15 Δ≈0 (Between); LLM-within +0,08–0,09; 55 Messungen/50 Modelle; ~87 % CN
- Kein §8.17-N=1-Fall; kein p=0,05-Sim-Vergleich; Schwelle ≥0,10 heuristisch
- Musik/Assets-Lizenzen dokumentieren (falls verwendet)

## Assets

`assets/` — fehlend, vor Aufnahme beschaffen:
- [ ] CognitiveSpace-Screenshot (PNG, 1080p)
- [ ] LDS-Diagramm (PNG/SVG)
- [ ] Divergenzbericht-Mockup (PNG)
