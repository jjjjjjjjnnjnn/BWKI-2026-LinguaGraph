# LinguaGraph — Einreichungs-Checkliste (BWKI 2026)

> **Stand**: 2026-09-19 (v22) | **Frist**: 20.09.2026 | **Ziel**: 3 vollständige Einreichungsbestandteile (Dokumentation / Code / Video-Pitch)
> **Narrative**: AI-Audit-Framing (Entscheid 2026-08-09) — siehe `docs/pitch_3min.md` + `docs/video_script.md`
> **Neu seit v21**: Seal `b7b17f3` (tag) + 7 Post-seal-Portal-Commits + Reaudit B1–B6 (keine neuen Experimente) + PDF-Rebuild (s. unten).
> Plattformspezifischer Feldabgleich + CI-Erstlauf: Stand unten, Owner-Entscheidungen markiert mit **[OWNER]**.

---

## Gesamtstatus

| # | Bestandteil | Status | Verantwortlich | Fällig |
|---|-------------|--------|----------------|--------|
| 1 | **Projektdokumentation** (Plattform-Fragen) | 🟡 Final-Entwürfe in `submission/final/`; Plattform-Felderabgleich offen **[OWNER]** | Du | 9/20 |
| 2 | **Code** (lauffähig + strukturiert) | 🟢 Pipeline ✅; Guide ✅ (84 tests); CI-Grün zu verifizieren (s. Must-3) | Du | 9/19 |
| 3 | **Video-Pitch** (2–4 Min) | 🟢 **EINGEREICHT 09-19: `LinguaGraph_BWKI2026_Pitch_4K.mp4` (DE ohne Untertitel, 3840×2160@60, 203.55s, ffprobe-verifiziert)**; EN/ZH-Hardsubs als Alternativen | done | ✅ |
| 4 | **Paper-PDF** (Supporting) | 🟢 Rebuilt 2026-09-19: 253600B/39p, 3 Orte hash-identisch (Reaudit-Stand B1–B2) | done | ✅ |

---

## Bestandteil 1: Projektdokumentation

- [x] `submission/final/plattform_antworten.md` — Final-Entwürfe (Idee/Methoden/Umsetzung/Ergebnisse/Fehlerquellen/kritische Einschätzung/Entwicklung/Offenlegung, v0.13.2-Zahlen; Reaudit-Check 09-19: keine E2/P2-Claims enthalten ✅)
- [ ] Plattformspezifische Fragenfelder abgleichen und Antworten ggf. anpassen **[OWNER, bis 9/20]**
- [x] Unterstützungs-Offenlegung: `submission/final/declaration_of_support.md` ✅ (42 DashScope + West-Set, v0.14.0; Reaudit-Check 09-19: keine stale Claims ✅)
- [x] `docs/CONTRIBUTORS.md` aktualisiert ✅

## Bestandteil 2: Code

- [x] Pipeline reproduzierbar (84 pytest, `submission/final/code_einreichung.md`)
- [x] Datasets/Modelle/Frameworks offengelegt (Code-Guide §3 + declaration_of_support.md)
- [x] PII/API-Keys von Einreichung ausgeschlossen (Scan 09-19: Dateinamen 0 Treffer, Inhalte 0 Treffer, `.env` ignored, untracked 0 ✅)
- [x] README enthält BWKI-Reproduktionspfad (Project Structure + Quick Start)
- [x] `requirements.txt` Install-Smoke-Test (deps-import-ok + pytest 84 green 2026-09-16; frische Venv-Installation ausstehend, optional)
- [ ] CI-Erstlauf auf GitHub Actions prüfen **[laufend, Must-3]**

## Bestandteil 3: Video-Pitch (separater Workflow — siehe `submission/pitch/README.md`)

- [x] `docs/video_script.md` v2 (AI-Audit-Framing, ~3 Min, DE-Narration + EN-Untertitel, Fakten-Check-Tabelle)
- [x] Storyboard + Fakten-Check (v0.13.2) in `submission/pitch/README.md`
- [x] **Aufnahme**: vorhanden seit 09-12 (`LinguaGraph_BWKI2026_Pitch_4K.mp4` 15MB ftyp-verifiziert + subs_en/subs_zh + subtitles_de/en.srt); Narrativ-Abgleich vs v26-Paper ausstehend
- [x] Schnitt 2–4 Min · 1080p · H.264 (4K-Master + Untertitel-Varianten vorhanden)
- [x] Musik/Assets-Lizenz dokumentieren: [Small Signs of Change – Sascha Ende](https://ende.app/en/song/13867-documentary-music-small-signs-of-change) (ende.app, CC BY 4.0) — s. `submission/pitch/upload_description.md`, Portal-Fußzeile, `declaration_of_support.md` §6
- [x] `submission/pitch/assets/` vorhanden (09-12) ✅
- [x] Reaudit-Check 09-19: Video erzählt 59-Modell-Replikation (LDS-C), keine v2/Panel-Claims → von E2-Downgrade unberührt ✅
- [ ] Endfassung-Wahl (4K-Master vs. Hardsub-Variante) **[OWNER]**

## Bestandteil 4 (Supporting): Wissenschaftliche Arbeit → PDF

- [x] Narrative reframed: Abstract + Einleitung + Schlussfolgerung + 3-Schlussfolgerungen (AI-Audit-Framing) ✅
- [x] **PDF-Assemblierung**: `scripts/build_paper_pdf.py` (fpdf2) → `docs/submission/` + `submission/final/` + `_deploy/docs/submission/` (drei Orte, hash-identisch; Stand 2026-09-19: 253600B/39p, Reaudit B1–B2 drin: E2-Downgrade, 0.395, TRACE, Hedge-Fixes — Textprobe verifiziert) ✅
- [x] Formatprüfung (Zahlen-Stichprobe im PDF: 0,395×4, weak×4, TRACE×2, P3b×2 ✅; Stand 09-19)
- **PDF-Regel (ab 2026-09-13, kein erneuter Drift)**: jede `docs/paper/*`-Änderung → `python scripts/build_paper_pdf.py` + `Copy-Item docs/submission/LinguaGraph_BWKI2026.pdf submission/final/LinguaGraph_BWKI2026.pdf -Force` + `Copy-Item docs/submission/LinguaGraph_BWKI2026.pdf _deploy/docs/submission/LinguaGraph_BWKI2026.pdf -Force` → Commit-Message `PDF rebuilt XXXXB/YYp` (Format wie v22-pdf).
- [x] Manifest-Zahlen abgeglichen (556/517/219 SSOT, v0.13.2) ✅
- [x] `_deploy/`-Spiegel synchronisiert ✅

---

## Inhaltliche Restarbeiten

- [ ] **`docs/paper/04_discussion.md`** "so-what"-Anwendungsebene prüfen — optional, nur wenn Zeit (SW-Fixforschung geht vor)
- [x] SW-Fixforschung (Step 4): SW1 Power-Analyse + Literatur · SW2 Provider-Stratifizierung ✅ + **West-Erweiterung (v0.14.0, 09-10)**: gpt-oss-20b (NIM), command-a (Cohere), laguna + nemotron-super (Kilo), gpt-5.6-luna (Terminal) → **59 Messungen / 54 Identitäten, ZH-DE 59/59 sig, West 11/11** · SW3 EN-Hub-Framing + Literatur · SW4 Youden-Kalibrierung (Optimum 0,12, CI 0,12–0,13)
- [ ] `pitch_10min.md`/`demo_script.md` als LEGACY markiert ✅ — Finals-Deck (11/13) wird aus neuem Rahmen neu gebaut

---

## Rückwärtsplan (bis 20.09)

```
9/08–09  Final-Dok-Fixes + Checkliste refresh ✅ (dieser Commit)
9/09–10  Reproduktions-Smoke-Test + CI-Erstlauf + SW-Fixforschung (offline)
9/11–13  PDF-Formatprüfung + Plattform-Felderabgleich (+ Video-Aufnahme, separat)
9/13–20  Plattform-Eintragung + Endkontrolle (Zahlen, Offenlegung, Code läuft) + Puffer → Tag v1.0
```

## Owner-Rest (Abend 09-19, vor Frist 20.09)

1. Plattform-Felderabgleich + Eintragung (feld-mapping v22).
2. Video-Timeline auf Key-Screens prüfen (mp4 nicht grep-bar) — Datei-Wahl geschlossen.
3. Konsolen-Quick-Check (zen/MiniMax/r4/sensenova/OpenRouter): keine abnormalen Abbuchungen → sonst erst revoke, dann einreichen.
4. CI-Grün (Must-3-Ergebnis abwarten); v1.0-Tag nur auf ausdrückliche Order (封盘≠Release-Disziplin).

## Risiken

| Risiko | Auswirkung | Gegenmaßnahme |
|--------|-----------|---------------|
| Video-Aufnahme ist der größte Restposten | Zeit | Skript + Storyboard fertig; separater Workflow |
| Plattform-Fragen weichen vom Entwurf ab | Dokumentation | Feld-für-Feld-Abgleich bis 9/13 (Step 5) |
| API-Quota für West-Modell-Replikation (SW2-A) | Evidenz | ✅ Gelöst (v0.14.0): NIM + Cohere + Kilo + Terminal, 7 westliche Messungen |
