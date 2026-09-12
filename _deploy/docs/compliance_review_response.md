# Compliance-Review-Response (2026-09-12)

Punktweise Antwort auf `docs/bwki-compliance-review.md` (2026-06-17).
Status: ✅ gelöst / 🟡 teilweise / 🔴 offen.

## 1. Eigenständigkeit (6/10: LLM/Tools nicht markiert) — 🟡 teilweise
- ✅ `docs/paper/02_methodology.md` §2.12 Technische Werkzeuge + `docs/declaration_of_support.md` v2.0 als Hauptoffenlegung.
- 🔴 Sync fällig (v21-p0a): `CONTRIBUTORS.md` + `submission/final/code_einreichung.md` §3 + Portal/Story-Toolchain übernehmen die §2.12-Tabelle 1:1 (nomic-embed-v1.5, Spark-Adjudikation, RapidOCR-ONNX, pymupdf, matplotlib, NetworkX, 3d-force-graph).
- Regel: eigene Leistung = Design, LDS-Definition, alle Befund-/Falsifikationsanalysen; Hilfsmittel offengelegt.

## 2. Originalität (8/10) — ✅ gelöst
LDS + Null-Suite + 55-Modell-Replikation, Literatur [1]–[54].

## 3. Schwierigkeit (5/10: keine echten Daten, keine p-Werte) — ✅ gelöst
N=15 between-subject + LLM within-subject k=10 + 55 Messungen + LMM p<0.001/0.90.

## 4. Wissenschaftlichkeit (4/10: keine Fehler/ Grenzen/ Baselines) — 🟡 teilweise
- ✅ `docs/BASELINE_LEDGER.md` (8 Baselines, verified/needs_review/drop) + Paper §8.10–8.16 + P2-Rechecks.
- 🔴 Rest (v21–v22): §1/§2.2/§2.3/§3/§5/§6/§7/§9 needs_review-Abschluss (CIs, Seeds, Gloss-Audit); `docs/evidence_register.md` C16–C20 neu, C3/C7/C8 downgraded (2026-09-12).

## 5. Ausblick (7/10) — ✅ gelöst
Audit-Werkzeug + EU AI Act + Schwelle Youden 0.13.

## 6. Relevanz (5/10: keine Nutzerfälle) — 🟡 teilweise
Entwickler/Regulierer/Forscher-Szenarien vorhanden; echte Nutzervalidierung ausstehend (als Grenze deklariert, kein Claim).

## 7. Code (7/10: kein pytest/README) — ✅ gelöst
84 Tests, requirements, code_einreichung.

## Top-5-Risiken
- R1 keine echten Daten → ✅ gelöst. R2 keine Fehleranalyse → ✅ gelöst (`error_analysis` + §8.10).
- R3 LDS-Mathe unverifiziert → 🟡 teilweise (binär verified, ternär dropped, structure-null needs_review).
- R4 Dokumentation fehlt → ✅ gelöst (222KB PDF; v22-pdf rebuild fällig). R5 Video fehlt → ✅ gelöst (173s ×3 + srt + poster).
