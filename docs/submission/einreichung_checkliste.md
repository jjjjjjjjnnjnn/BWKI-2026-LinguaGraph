# LinguaGraph — Einreichungs-Checkliste (BWKI 2026)

> **Stand**: 2026-09-08 (v0.13.2) | **Frist**: 20.09.2026 | **Ziel**: 3 vollständige Einreichungsbestandteile (Dokumentation / Code / Video-Pitch)
> **Narrative**: AI-Audit-Framing (Entscheid 2026-08-09) — siehe `docs/pitch_3min.md` + `docs/video_script.md`

---

## Gesamtstatus

| # | Bestandteil | Status | Verantwortlich | Fällig |
|---|-------------|--------|----------------|--------|
| 1 | **Projektdokumentation** (Plattform-Fragen) | 🟡 Final-Entwürfe in `submission/final/`; Plattform-Felderabgleich offen | Du | 9/13 |
| 2 | **Code** (lauffähig + strukturiert) | 🟡 Pipeline ✅; Guide ✅ (84 tests); Reproduktions-Smoke-Test offen | Du | 9/10 |
| 3 | **Video-Pitch** (2–4 Min) | 🔴 Skript v2 fertig; **nicht aufgenommen** (separater Workflow) | Du | 9/13 |

---

## Bestandteil 1: Projektdokumentation

- [x] `submission/final/plattform_antworten.md` — Final-Entwürfe (Idee/Methoden/Umsetzung/Ergebnisse/Fehlerquellen/kritische Einschätzung/Entwicklung/Offenlegung, v0.13.2-Zahlen)
- [ ] Plattformspezifische Fragenfelder abgleichen und Antworten ggf. anpassen (bis 9/13)
- [x] Unterstützungs-Offenlegung: `submission/final/declaration_of_support.md` ✅ (42 DashScope + West-Set, v0.14.0)
- [x] `docs/CONTRIBUTORS.md` aktualisiert ✅

## Bestandteil 2: Code

- [x] Pipeline reproduzierbar (84 pytest, `submission/final/code_einreichung.md`)
- [x] Datasets/Modelle/Frameworks offengelegt (Code-Guide §3 + declaration_of_support.md)
- [x] PII/API-Keys von Einreichung ausgeschlossen (vermerkt)
- [x] README enthält BWKI-Reproduktionspfad (Project Structure + Quick Start)
- [ ] `requirements.txt` Install-Smoke-Test (frisch installieren + pytest — bis 9/10)
- [ ] CI-Erstlauf auf GitHub Actions prüfen (`.github/workflows/ci.yml`, neu)

## Bestandteil 3: Video-Pitch (separater Workflow — siehe `submission/pitch/README.md`)

- [x] `docs/video_script.md` v2 (AI-Audit-Framing, ~3 Min, DE-Narration + EN-Untertitel, Fakten-Check-Tabelle)
- [x] Storyboard + Fakten-Check (v0.13.2) in `submission/pitch/README.md`
- [ ] **Aufnahme**: Screen-Recording der Konzeptgraphen + LDS-Balken + Treiberliste + Divergenzbericht-Mockup
- [ ] Schnitt auf 2–4 Min · 1080p · H.264
- [ ] Musik/Assets-Lizenz dokumentieren (falls verwendet)
- [ ] `submission/pitch/assets/` beschaffen (Screenshots, LDS-Diagramm, Mockup)

## Bestandteil 4 (Supporting): Wissenschaftliche Arbeit → PDF

- [x] Narrative reframed: Abstract + Einleitung + Schlussfolgerung + 3-Schlussfolgerungen (AI-Audit-Framing) ✅
- [x] **PDF-Assemblierung**: `scripts/build_paper_pdf.py` (fpdf2) → `submission/final/LinguaGraph_BWKI2026.pdf` + `docs/submission/LinguaGraph_BWKI2026.pdf` ✅
- [ ] Formatprüfung (Konsistenz der Zahlen, Diagramme, Referenzen) — bis 9/13
- [x] Manifest-Zahlen abgeglichen (556/525/219 SSOT, v0.13.2) ✅
- [x] `_deploy/`-Spiegel synchronisiert ✅

---

## Inhaltliche Restarbeiten

- [ ] **`docs/paper/04_discussion.md`** "so-what"-Anwendungsebene prüfen — optional, nur wenn Zeit (SW-Fixforschung geht vor)
- [x] SW-Fixforschung (Step 4): SW1 Power-Analyse + Literatur · SW2 Provider-Stratifizierung ✅ + **West-Erweiterung (v0.14.0, 09-10)**: gpt-oss-20b (NIM), command-a (Cohere), laguna + nemotron-super (Kilo), gpt-5.6-luna (Terminal) → **55 Messungen / 50 Identitäten, ZH-DE 55/55 sig, West 7/7** · SW3 EN-Hub-Framing + Literatur · SW4 Youden-Kalibrierung (Optimum 0,13)
- [ ] `pitch_10min.md`/`demo_script.md` als LEGACY markiert ✅ — Finals-Deck (11/13) wird aus neuem Rahmen neu gebaut

---

## Rückwärtsplan (bis 20.09)

```
9/08–09  Final-Dok-Fixes + Checkliste refresh ✅ (dieser Commit)
9/09–10  Reproduktions-Smoke-Test + CI-Erstlauf + SW-Fixforschung (offline)
9/11–13  PDF-Formatprüfung + Plattform-Felderabgleich (+ Video-Aufnahme, separat)
9/13–20  Plattform-Eintragung + Endkontrolle (Zahlen, Offenlegung, Code läuft) + Puffer → Tag v1.0
```

## Risiken

| Risiko | Auswirkung | Gegenmaßnahme |
|--------|-----------|---------------|
| Video-Aufnahme ist der größte Restposten | Zeit | Skript + Storyboard fertig; separater Workflow |
| Plattform-Fragen weichen vom Entwurf ab | Dokumentation | Feld-für-Feld-Abgleich bis 9/13 (Step 5) |
| API-Quota für West-Modell-Replikation (SW2-A) | Evidenz | ✅ Gelöst (v0.14.0): NIM + Cohere + Kilo + Terminal, 7 westliche Messungen |
