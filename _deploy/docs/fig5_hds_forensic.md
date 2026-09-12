# Fig5-HDS-Forensik (2026-09-12)

**Claim (publiziert)**: Math HDS max 8 / mean 0.40 / 459 roots (83%) auf 556
Konzepten; Fig5 EN-only (`fig5_hds_distribution.png`, 4× byte-identisch:
outputs + web/figures + cognitive-space/figures + _deploy/figures).

**Befund**: Zwei unabhängige Agenten, Befund konvergent —
**Ursache gefunden, kein Löschen** (gleiche verlorene Pipeline wie Fig3):

- **Geburt in 4 Phasen** (alle `jjjjjjjjnnjnn`): `eeca788` (2026-06-21, HDS-Definition
  longest prerequisite chain, 574-Graph: max 5 / mean 0.34) →
  `2ffd963` (2026-06-22, `generate_paper_figures.py::compute_hds` auf
  damaliger `data.js`, max 7 / mean 0.40) → `8ad379a` (459 roots erstmals,
  max 9 / mean 0.42) → `897f04e` (Freeze: max 8 / exakt 0.4029 /
  BFS on 3,538 Relationen) → `0962982` (Dedup 574−18=556 Nenner).
  Publikations-Kombination 556/459/8/0.40 ist **mehrstufig zusammengeführt**,
  kein Single-Run-Output.
- **Verlorene Pipeline**: konsistenter 556/525-ID-Graph (June-2026 dense,
  selbe Generation wie Fig3-Terrain-Matrix); `merged_relations.json` heute:
  557 Konzepte (+1 nicht dedupiert) + 525 Relationen, davon **6 dangling**
  (darunter requires-Kette → … → Fourierreihe = Kandidat für die
  fehlende 8. Schicht).
- **Exhaustion**: 3 Quellen (aligned 219 / 556-238-Snapshot / math_full 3833)
  × alle Sinn-Varianten (Kantentyp × Richtung × Stufen-Scope × Tiefen-Def):
  **kein Treffer**. Nächste: merged-557 PREREQ5-reversiert 460/7/0.27
  (Δroots +1, Δmax −1). max=8 erscheint in keinem prereq-Filter je.
- **Unfall `6f1d5b2`** (2026-09-12): math-Sektion von
  `outputs/physics_comparison.json` mit 238-Link-Maßstab überschrieben
  (jetzt 556/238/max3/0.1691/489). Publikationswerte im Arbeitsbaum-JSON
  verloren — nur via `git show 6f1d5b2^:outputs/physics_comparison.json`
  + Freeze-PNG + Text-Claims erhalten.
- **Implementierungs-Hinweis**: `compute_hds` zählt downstream-Höhe
  (Blatt=0), Dokument definiert upstream-Tiefe (root=0) — max identisch,
  mean verschieden; zusätzlich Richtungs-Bug (requires-source als
  Vorgänger). Beides dokumentiert, nicht repariert (Freeze-Policy).

**Status**: Ursache = eingefrorene Publikation aus verlorener dichter
Pipeline. **Frozen + Fußnote umgesetzt** (Portal finding_b_body EN/DE/ZH,
Story-F3/F7-Zeilen + fig5_caption EN/DE, Assert-Guard analog Fig3 entfällt
— fig5 wird per Policy gar nicht gerendert). Paper-Tabellen
(`06_physics_results.md`, `05_conclusion.md`) bleiben Publikationsstand,
Offenlegung trägt diese Notiz.
