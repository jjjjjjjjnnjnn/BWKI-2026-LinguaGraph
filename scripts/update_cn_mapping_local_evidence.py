"""Attach mirror-PDF arrivals to cn_textbook_mapping.json (staging).
Local PDFs are scans (no text layer) — OCR pending, so text_available stays False.
Usage: python scripts/update_cn_mapping_local_evidence.py
"""
import json
from pathlib import Path

MAP = Path("config/expert_graphs/cn_textbook_mapping.json")
D = Path("data/textbook/cn_mirror")

FILES = {
    "物理必修第三册": "zh_物理必修3_普通高中教科书.pdf",
    "物理选择性必修第一册": "zh_物理选必1_普通高中教科书.pdf",
    "物理选择性必修第二册": "zh_物理选必2_普通高中教科书.pdf",
    "物理选择性必修第三册": "zh_物理选必3_普通高中教科书.pdf",
    "化学选择性必修1": "zh_化学选必1_化学反应原理.pdf",
    "化学选择性必修2": "zh_化学选必2_物质结构与性质.pdf",
    "化学选择性必修3": "zh_化学选必3_有机化学基础.pdf",
}


def main() -> None:
    m = json.loads(MAP.read_text(encoding="utf-8"))
    for b in m["books"]:
        hit = next((f for title, f in FILES.items() if title in b["book"]), None)
        b["local_evidence"] = {
            "date": "2026-09-12",
            "mirror": "https://github.com/TapXWorld/ChinaTextbook (third-party copy, provenance unverified; official source: basic.smartedu.cn)",
            "file": hit,
            "exists": bool(hit and (D / hit).exists()),
            "size_mb": round((D / hit).stat().st_size / 1e6, 1) if hit and (D / hit).exists() else 0,
            "format": "scanned PDF, no text layer (264 image XObjects, 0 ToUnicode on sampled file)",
            "ocr": "pending — no local OCR engine (tesseract/paddleocr absent)",
            "license": "copyrighted PEP textbook; local research use only, never committed, prefer official copies",
        }
    m["meta"]["text_available"] = False
    m["meta"]["pdfs_local"] = "7/7 mirror scans arrived 2026-09-12 (OCR pending)"
    MAP.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    print("books:", len(m["books"]),
          "exists:", sum(1 for b in m["books"] if b["local_evidence"]["exists"]))


if __name__ == "__main__":
    main()
