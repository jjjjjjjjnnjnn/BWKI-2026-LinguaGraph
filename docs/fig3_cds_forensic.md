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
