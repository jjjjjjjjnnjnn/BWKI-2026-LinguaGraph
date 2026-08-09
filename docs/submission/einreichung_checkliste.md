# LinguaGraph — Einreichungs-Checkliste (BWKI 2026)

> **Stand**: 2026-08-09 | **Frist**: 20.09.2026 | **Ziel**: 3 vollständige Einreichungsbestandteile (Dokumentation / Code / Video-Pitch)
> **Narrative**: AI-Audit-Framing (Entscheid 2026-08-09) — siehe `docs/pitch_3min.md` + `docs/video_script.md`

---

## Gesamtstatus

| # | Bestandteil | Status | Verantwortlich | Fällig |
|---|-------------|--------|----------------|--------|
| 1 | **Projektdokumentation** (Plattform-Fragen) | 🟡 Entwurf v1 fertig; plattformspezifische Fragen final | Du | 9/13 |
| 2 | **Code** (lauffähig + strukturiert) | 🟡 Pipeline ✅; Einreichungs-Guide ✅; Teil-Finalisierung offen | Du | 9/06 |
| 3 | **Video-Pitch** (2–4 Min) | 🔴 Skript v2 fertig; **nicht aufgenommen** | Du | 8/29–9/05 |

---

## Bestandteil 1: Projektdokumentation

- [x] `docs/submission/plattform_antworten.md` — Antwortentwürfe (Idee/Methoden/Umsetzung/Ergebnisse/Fehlerquellen/kritische Einschätzung/Entwicklung/Offenlegung)
- [ ] Plattformspezifische Fragenfelder abgleichen und Antworten ggf. anpassen (9/06–9/13)
- [x] Unterstützungs-Offenlegung: `docs/declaration_of_support.md` ✅
- [x] `docs/CONTRIBUTORS.md` aktualisiert ✅

## Bestandteil 2: Code

- [x] Pipeline reproduzierbar (60+ pytest ✅, `docs/submission/code_einreichung.md`)
- [x] Datasets/Modelle/Frameworks offengelegt (Code-Guide §3 + declaration_of_support.md)
- [x] PII/API-Keys von Einreichung ausgeschlossen (vermerkt)
- [ ] **README** um "BWKI-Einreichung"-Abschnitt ergänzen (Reproduktionsbefehl + Offenlegung) — 9/06
- [ ] `requirements.txt` prüfen/ergänzen

## Bestandteil 3: Video-Pitch

- [x] `docs/video_script.md` v2 (AI-Audit-Framing, ~3 Min, DE-Narration + EN-Untertitel, Fakten-Check-Tabelle)
- [ ] **Aufnahme** (8/29–9/05): Screen-Recording der Konzeptgraphen + LDS-Balken + Treiberliste + Divergenzbericht-Mockup
- [ ] Schnitt auf 2–4 Min · 1080p · H.264
- [ ] Musik/Assets-Lizenz dokumentieren (falls verwendet)

## Bestandteil 4 (Supporting): Wissenschaftliche Arbeit → PDF

- [x] Narrative reframed: Abstract + Einleitung + Schlussfolgerung + 3-Schlussfolgerungen (AI-Audit-Framing) ✅
- [ ] **PDF-Assemblierung** — ⚠️ **Toolchain-Entscheid offen** (siehe unten)
- [ ] Titelblatt + Inhaltsverzeichnis + Referenzen + Offenlegungs-Anhang (DE)
- [ ] Formatprüfung (Konsistenz der Zahlen, Diagramme, Referenzen)

### PDF-Toolchain-Entscheid (⚠️ Entscheidung nötig)

Aktuell installiert: **kein** pandoc/LaTeX; Python nur `markdown` (kein weasyprint/reportlab/fpdf).

| Option | Aufwand | Ergebnis |
|--------|---------|----------|
| **A. GitHub Actions markdown→PDF** | ~1h, bei Restore der GitHub-Verbindung | Automatisch, reproduzierbar, Referenzen-Pflege manuell |
| **B. pandoc + MiKTeX installieren** (choco/winget) | ~30–60 Min lokal | Standard, beste Layout-Kontrolle |
| **C. VSCode Markdown→PDF (Markdown-PDF-Plugin)** | ~15 Min | Schnell, mittlere Qualität |
| **Empfehlung**: **B** nach inhaltlichem Freeze (9/13) — beste Qualität für Begutachtung; A als Fallback.

---

## Inhaltliche Restarbeiten

- [ ] **`docs/paper/04_discussion.md`** "so-what"-Anwendungsebene prüfen (Abschnitt 4.x Anwendung mehrsprachige KI) — leichte Ergänzung optional
- [ ] `_deploy/docs/*.md` sind Stand 6/23 (veraltet) — bei finaler Verpackung aktualisieren
- [ ] Manifest-Zahlen-Abgleich (556/557, 219/247) — Governance-A0, unabhängig von Einreichung
- [ ] `pitch_10min.md`/`demo_script.md` als LEGACY markiert ✅ — Finals-Deck (11/13) wird aus neuem Rahmen neu gebaut

---

## Rückwärtsplan (bis 20.09)

```
8/09–13  Inhaltlicher Freeze der Dokumentation (Plattform-Antworten finalisieren)
8/14–28  Video aufnehmen + schneiden (Skript liegt vor)
8/29–09/05 Code-README/requirements finalisieren
9/06–13  PDF-Assemblierung (Toolchain-Option B/A) + Formatprüfung
9/13–20  Plattform-Eintragung + Endkontrolle (Zahlen, Offenlegung, Code läuft) + Puffer
```

## Risiken

| Risiko | Auswirkung | Gegenmaßnahme |
|--------|-----------|---------------|
| Video-Aufnahme ist der größte Restposten | Zeit | Skript fertig; Aufnahmefenster 8/14–28 reservieren |
| GitHub offline (PDF via Actions nicht möglich) | PDF-Toolchain | Lokale Option B (pandoc+MiKTeX) nutzen |
| Plattform-Fragen weichen vom Entwurf ab | Dokumentation | Entwurf deckt alle in Teilnahmebedingungen genannten Felder ab |
