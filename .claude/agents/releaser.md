# Releaser Agent (release chain operator)

> Kette: `run_pipeline.py` → `quality_report.py --check-quality-gates`
> → `release.py` → `_deploy/` → Pages. Gate 2/3.

## Auftrag

1. **Vor jedem Release**: `python scripts/release.py --dry-run`. Bei Gate-FAIL stoppen,
   `data/quality_history/quality_report_latest.json` als Beleg anfügen.
2. **Standard-Release** (reine Dok-Änderungen): `python scripts/release.py --skip-pipeline`.
   Volle Pipeline nur bei neuen Daten — braucht API-Key, vorher Quota prüfen
   (08-10: Bailian-Undisclosed/Arrears-Ereignis, siehe `declaration_of_support.md`).
3. **Nach dem Lauf verifizieren**:
   - `manifest.json`: build_time + provenance.commit aktuell; 556/238/219/525 stabil
     (238 = Vis-Links, 525 = Alignierungs-Relationen — unterschiedliche Nenner).
   - Hashes: `cognitive-space/web/data.js` == `_deploy/data.js` == `release/data.js`.
   - Diff-Umfang: nur Timestamps + Domain-Order erwartet; mehr → anhalten.
4. **PDF**: `python scripts/build_paper_pdf.py` (fpdf2-Fallback ok; Glyphen-Warnungen normal).
   Output: `docs/submission/LinguaGraph_BWKI2026.pdf` → Kopie nach `submission/final/`.
5. **Commit-Protokoll**: explizite Dateilisten (`git add <paths>`, nie `-A`);
   `_temp/`, `.wrangler/`, `participant_data/`, `.env`, `*.db` nie stagen.
