"""Render P2 visual-closure sample pages."""
import pymupdf

JOBS = [
    ("data/textbook/cn_mirror/zh_物理选必2_普通高中教科书.pdf", [60, 94],
     "xb2sample"),
    ("data/textbook/cn_mirror/zh_化学必修1_普通高中教科书.pdf", [28, 57],
     "bx1sample"),
    ("data/textbook/cn_mirror/zh_物理必修2_普通高中教科书.pdf", [35],
     "bx2sample"),
    ("data/textbook/cn_mirror/zh_化学选必3_有机化学基础.pdf", [57],
     "xb3sample"),
]
for pdf, pages, tag in JOBS:
    doc = pymupdf.open(pdf)
    for p in pages:
        doc[p].get_pixmap(dpi=100).save(
            f"C:/Users/rongj/AppData/Local/Temp/opencode/{tag}_p{p}.png")
    doc.close()
print("done")
