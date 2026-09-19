# LinguaGraph — Video-Pitch (separater Workflow)

> Spec: 2–4 Min · 1080p · H.264 | Skript: `video_script.md` v2 (AI-Audit-Framing, DE-Narration + EN-Untertitel)
> Status: **EINGEREICHT 2026-09-19: `LinguaGraph_BWKI2026_Pitch_4K.mp4` (DE ohne Untertitel, 3840×2160@60, 64.9 MB, 203.55s, H.264+AAC, keine eingebetteten Untertitelspuren — ffprobe-verifiziert)**. EN/ZH-Hardsub-Varianten als Alternativen. Quelle: Benutzerschnitt (`202609171822`, 203.55s) + ≤100MB-Kompression + neu gebrannte EN/ZH-Untertitel (62 Cues, klein, unten). Dieses Verzeichnis hält nur die **Einbettungs-Kopien** für Repo + Portal.

## Finals (Einbettungs-Kopien, Stand 2026-09-17, 203.55s / 3840×2160@60 / H.264+AAC)

| Datei | Inhalt | Größe |
|---|---|---|
| `LinguaGraph_BWKI2026_Pitch_4K.mp4` | DE ohne Untertitel — **EINGEREICHTE Fassung** | 64.9 MB |
| `LinguaGraph_BWKI2026_Pitch_4K_subs_en.mp4` | gleicher Schnitt + EN-Untertitel (eingebrannt, 62 Cues, klein/unten) | 51.7 MB |
| `LinguaGraph_BWKI2026_Pitch_4K_subs_zh.mp4` | gleicher Schnitt + ZH-Untertitel (eingebrannt, 62 Cues, klein/unten) | 51.1 MB |
| `subtitles_{de,en,zh}.srt` | Untertitel-Quellen (62 Cues, 0→190s, Wort-Timestamps via faster-whisper) | — |
| `assets/pitch_poster.jpg` | Poster-Frame (t60s, aus dem 204s-Schnitt) | — |

> Quelle: Benutzerschnitt `202609171822.mp4` (Desktop, 250 MB) → CRF14/slow ≤100MB (`202609171822_100MB.mp4`, 64.9 MB) → EN/ZH-Burn CRF17/fast mit Audio-Copy. Kopien in `submission/pitch/`, `cognitive-space/portal/pitch/` (= Pages-Quelle) und `_deploy/portal/pitch/` (Deploy-Spiegel) identisch.

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

- 556 Konzepte / 517 Relationen / 219 Gruppen; F1 sozial 0,939, gewichtet 0,881
- N=15 Δ≈0 (Between); LLM-within +0,08–0,09; 59 Messungen/54 Modelle; ~81 % CN
- Kein §8.17-N=1-Fall; kein p=0,05-Sim-Vergleich; Schwelle ≥0,10 heuristisch
- Musik/Assets-Lizenzen dokumentieren ✅ erledigt: Musik [Small Signs of Change – Sascha Ende](https://ende.app/en/song/13867-documentary-music-small-signs-of-change) (ende.app, CC BY 4.0) — Nachweis in Videobeschreibung (`upload_description.md`), Portal-Fußzeile und `declaration_of_support.md` §6

## Assets

`assets/` — fehlend, vor Aufnahme beschaffen:
- [ ] CognitiveSpace-Screenshot (PNG, 1080p)
- [ ] LDS-Diagramm (PNG/SVG)
- [ ] Divergenzbericht-Mockup (PNG)
