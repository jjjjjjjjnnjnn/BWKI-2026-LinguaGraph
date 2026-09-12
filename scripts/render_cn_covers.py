"""Render cover + TOC pages of the 7 mirrored PEP PDFs for visual verification."""
import pymupdf
from pathlib import Path

D = Path("data/textbook/cn_mirror")
OUT = Path("C:/Users/rongj/AppData/Local/Temp/opencode/cn_covers")
OUT.mkdir(parents=True, exist_ok=True)

for pdf in sorted(D.glob("*.pdf")):
    doc = pymupdf.open(pdf)
    print(pdf.name, "pages:", doc.page_count)
    for i in (0, min(2, doc.page_count - 1)):
        pix = doc[i].get_pixmap(dpi=80)
        pix.save(OUT / f"{pdf.stem}_p{i}.png")
    doc.close()
print("done")
