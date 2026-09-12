# Fig3-CDS-Forensik (2026-09-12)

**Claim (publiziert)**: CDS middle = 0.271 → high = 0.073 (3.7× Abfall, F2).

**Befund**: Unter allen archivierten Graph/Definitions-Kombinationen
(`outputs/figures/fig3_forensic_data.csv`, 16 Zeilen, deterministisch via
`scripts/fig3_forensic.py`) ist 0.271/0.073 **nicht reproduzierbar**:

| Quelle | Definition | middle | high |
|---|---|---|---|
| math_full raw (3833 nodes) | density, alle internen Kanten | 0.0053 | 0.0002 |
| math_full raw | density, requires-only (same-level) | 0.0328 | 0.0251 |
| math_full raw | density, prerequisite-only (same-level) | 0.0582 | 0.0833 |
| physics_comparison snapshot (556/238) | density (archiviert) | 0.0038 | 0.0025 |
| **publiziert** | **?** | **0.271** | **0.073** |

Die Richtung (middle > high) gilt in Snapshot + requires-Rechnung, nicht die
Größenordnung. Fig5-Präzedenz (`scripts/figures_i18n.py` L9: Re-Render würde
Balken fälschen) greift: **publizierte Fig3 bleibt eingefroren**; diese Notiz
ist der Prüfpfad.

**Optionen (User-Entscheidung fällig)**:
1. Frozen + Fußnote (empfohlen): F2-Claim als "indikativ (Rechenweg derzeit
   nicht aus Archiv rekonstruierbar)" kennzeichnen — Portal/Story/Paper je
   ein Satz.
2. Claim-Downgrade: nur Richtung ("Dichte fällt") ohne Zahlen behaupten.
3. Weiter forensisch: verlorene Pipeline (525-Link-Graph) rekonstruieren —
   aufwendig, Erfolg unsicher.

## Durchbruch 2026-09-12 abends (User-Order: Ursache finden oder löschen)

Zwei unabhängige Agenten, Befund konvergent — **Ursache gefunden, kein Löschen**:

- **Arithmetik**: middle n=46, e=280 → 2·280/(46·45)=0.2705→0.271 ✓;
  high n=175, e=1113 → 2·1113/(175·174)=0.0731→0.073 ✓ (einzige
  treffende Kombination; gerichtet halbiert 0.135/0.037 trifft nicht).
- **Provenienz**: `eeca788` (2026-06-21) definiert CDS + Tabelle
  (Middle 46|280|0.2705, High 193|1116|0.0602); `2ffd963` (2026-06-22)
  publiziert erstmals exakt 0.271/0.073
  (`scripts/generate_paper_figures.py::compute_cds`, Input
  `cognitive-space/web/data.js`, LV-Partition, round4); `763b836`
  friert ein + handgeschriebene ZH/EN/DE-Dreifach-0.271.
- **Verlorene Pipeline**: dichter Graph (574-Knoten-Validierung →
  556-Knoten/3375-Kanten-Terrain-Matrix in `cds-terrain.html:54`);
  High-Partition unterwegs revidiert (193|1116 → 175|1113, unerklärt).
  Ausgaben erschöpft: 16 (forensic) + 96 (aligned_data-Exhaustion) = keine
  trifft; `figures_i18n.py`-Asserts beweisen, dass der Snapshot zur
  Renderzeit noch die alten Werte trug (jetzt überschrieben:
  0.0038/0.0025).
- **Status**: Ursache = eingefrorene Publikation aus verlorener dichter
  Pipeline. Entscheidung: **Option 1 umgesetzt** — Portal finding_a_body
  (EN/DE/ZH), Story-F1-Zeile, `figures_i18n.py`-Assert-Meldungen mit
  Forensik-Verweis versehen. `docs/paper/03_results.md` enthält kein 0.271
  (nur Alt-Entwurf `03_results_text.md`, historisch).
