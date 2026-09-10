#!/usr/bin/env python3
"""Assemble the BWKI paper markdown files into a single PDF (German).

Concatenates docs/paper/*.md in reading order with a title page, table of
contents, and the declaration-of-support appendix, converts markdown -> HTML
(markdown lib, tables extension) and HTML -> PDF (xhtml2pdf preferred,
fpdf2/reportlab fallback if available).

Usage: python scripts/build_paper_pdf.py [--out docs/submission/LinguaGraph_BWKI2026.pdf]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAPER = PROJECT_ROOT / "docs" / "paper"

# Reading order for the submission paper (core chapters only).
ORDER = [
    "01_abstract_introduction.md",   # abstract + introduction
    "02_related_work.md",            # related work / literature
    "02_methodology.md",             # methods
    "03_results.md",                 # results (incl. 5.10 replication)
    "06_physics_results.md",         # cross-disciplinary validation (F6/F7 detail)
    "07_lpa_analysis.md",            # exploratory language-production stream
    "04_discussion.md",              # discussion (incl. 4.16 cultural grounding)
    "05_conclusion.md",              # conclusion
    "00_three_conclusions.md",       # three conclusions (pitch-able summary)
]

TITLE_PAGE = """# LinguaGraph — Prüfung mehrsprachiger KI: Messung sprachübergreifender Wertedivergenz in LLMs

**Linguistic Divergence Score (LDS) · LLM-as-Subject · 51-Messungs-Replikation**

*BWKI 2026 – Bundeswettbewerb Künstliche Intelligenz*

**Autor**: Teilnehmer/in (Eigenarbeit)

**Kurzfassung**: LinguaGraph misst, ob mehrsprachige KI-Systeme wertbeladene Konzepte (Gerechtigkeit, Freiheit, Verantwortung, Heimat, Erfolg) sprachübergreifend unterschiedlich strukturieren. Ein Within-Subject-Experiment (LLM-as-Subject) und eine Replikation über 55 Messungen (50 eindeutige Modelle) zeigen: Alle ZH-DE-Paare signifikant, die Kulturrichtung (DE Autonomie/Regeln vs. ZH Raum/Anspruch) übersteigt ein Zufalls-Nullmodell. Der Bericht ordnet die Befunde ehrlich ein (Grenzen: ~87 % chinesische Anbieter, sieben westliche Messungen, 8 nicht-signifikante englisch-haltige Paare, Alignierungs-Artefakte der Domänen-Kontrolle). Vollständige Unterstützungs-Offenlegung im Anhang.

---

"""


def md_to_html(md: str) -> str:
    import markdown
    return markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str,
                    default=str(PROJECT_ROOT / "docs" / "submission" / "LinguaGraph_BWKI2026.pdf"))
    args = ap.parse_args()

    # 1. Combine markdown
    parts = [TITLE_PAGE]
    for name in ORDER:
        f = PAPER / name
        if not f.exists():
            print(f"  [WARN] missing {name}, skipping")
            continue
        md = f.read_text(encoding="utf-8")
        # strip the leading "# ..." title if it duplicates a chapter header
        parts.append(f"\n\n---\n\n{md}\n\n")
    combined_md = "".join(parts)

    # 2. Disclosure appendix
    decl = PROJECT_ROOT / "docs" / "declaration_of_support.md"
    if decl.exists():
        combined_md += "\n\n---\n\n# Anhang: Unterstützungs-Offenlegung\n\n"
        combined_md += decl.read_text(encoding="utf-8")

    html = md_to_html(combined_md)

    # 3. HTML -> PDF (backend detection)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from xhtml2pdf import pisa  # preferred: handles tables + unicode
        with open(out_path, "wb") as f:
            status = pisa.CreatePDF(src=html, dest=f,
                                    encoding="utf-8")
        if status.err:
            raise RuntimeError("xhtml2pdf reported errors")
        backend = "xhtml2pdf"
    except ImportError:
        from fpdf import FPDF  # fallback: system Unicode font + manual layout
        pdf = FPDF()
        fam = "helvetica"
        for reg, bold, it in [
            (r"C:/Windows/Fonts/simsun.ttc", r"C:/Windows/Fonts/simhei.ttf", r"C:/Windows/Fonts/simsun.ttc"),
            (r"C:/Windows/Fonts/arial.ttf", r"C:/Windows/Fonts/arialbd.ttf", r"C:/Windows/Fonts/ariali.ttf"),
        ]:
            if Path(reg).exists():
                try:
                    pdf.add_font("main", "", reg)
                    pdf.add_font("main", "B", bold if Path(bold).exists() else reg)
                    pdf.add_font("main", "I", it if Path(it).exists() else reg)
                    # write_html uses 'courier' for <code>/<pre>; point it at the
                    # same Unicode font so code blocks with CJK render.
                    for fname in ("courier", "monospace"):
                        pdf.add_font(fname, "", reg)
                        pdf.add_font(fname, "B", bold if Path(bold).exists() else reg)
                        pdf.add_font(fname, "I", it if Path(it).exists() else reg)
                    fam = "main"
                    break
                except Exception:
                    continue
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font(fam, size=9)
        # Strip <code>/<pre> (fpdf2 defaults to 'courier') and inline formatting
        # tags (fpdf2 write_html rejects nested tags inside <td>).
        html_clean = re.sub(r"</?(pre|code)[^>]*>", "", html)
        html_clean = re.sub(r"</?(strong|em|b|i|span|u|s|mark)[^>]*>", "", html_clean)
        pdf.write_html(html_clean)
        pdf.output(str(out_path))
        backend = f"fpdf2 ({fam})"
    except ImportError:
        raise SystemExit("No PDF backend (xhtml2pdf or fpdf2) installed")

    print(f"  [OK] {len(combined_md)} chars markdown -> {out_path} (backend: {backend})")
    print(f"  PDF size: {out_path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
