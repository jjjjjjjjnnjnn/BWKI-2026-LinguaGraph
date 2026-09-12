"""Append 4 book stubs (必修1/2 phys+chem) to cn_textbook_mapping.json.
Chapters from OCR TOC reports; sections empty with mapping-pending note.
Usage: python scripts/extend_mapping_bx.py
"""
import json
from pathlib import Path

MAP = Path("config/expert_graphs/cn_textbook_mapping.json")
MIRROR = ("https://github.com/TapXWorld/ChinaTextbook (third-party copy, "
          "provenance unverified; official source: basic.smartedu.cn)")

BOOKS = [
    {"book": "人教版高中物理必修第一册(2019)", "subject": "physics",
     "full_file": "physics_full.json",
     "pdf": "zh_物理必修1_普通高中教科书.pdf",
     "chapters": ["第一章 运动的描述", "第二章 匀变速直线运动的研究",
                  "第三章 相互作用—力", "第四章 运动和力的关系"]},
    {"book": "人教版高中物理必修第二册(2019)", "subject": "physics",
     "full_file": "physics_full.json",
     "pdf": "zh_物理必修2_普通高中教科书.pdf",
     "chapters": ["第五章 抛体运动", "第六章 圆周运动",
                  "第七章 万有引力与宇宙航行", "第八章 机械能守恒定律"]},
    {"book": "人教版高中化学必修第一册(2019)", "subject": "chemistry",
     "full_file": "chemistry_full.json",
     "pdf": "zh_化学必修1_普通高中教科书.pdf",
     "chapters": ["第一章 物质及其变化", "第二章 海水中的重要元素——钠和氯",
                  "第三章 铁 金属材料", "第四章 物质结构 元素周期律"]},
    {"book": "人教版高中化学必修第二册(2019)", "subject": "chemistry",
     "full_file": "chemistry_full.json",
     "pdf": "zh_化学必修2_普通高中教科书.pdf",
     "chapters": ["第五章 化工生产中的重要非金属元素", "第六章 化学反应与能量",
                  "第七章 有机化合物", "第八章 化学与可持续发展"]},
]


def main() -> None:
    m = json.loads(MAP.read_text(encoding="utf-8"))
    have = {b["book"] for b in m["books"]}
    for b in BOOKS:
        if b["book"] in have:
            print("skip (exists):", b["book"])
            continue
        m["books"].append({
            "book": b["book"], "subject": b["subject"],
            "full_file": b["full_file"],
            "chapters": [{"chapter": ch, "sections": [],
                          "note": "section mapping pending (stub 2026-09-12)"}
                         for ch in b["chapters"]],
            "local_evidence": {
                "date": "2026-09-12", "mirror": MIRROR, "file": b["pdf"],
                "exists": (Path("data/textbook/cn_mirror") / b["pdf"]).exists(),
                "format": "scanned PDF, OCR chapter txts in data/textbook/",
                "license": "copyrighted PEP textbook; local research use only, never committed",
            },
        })
        print("added:", b["book"])
    m["meta"]["books_total"] = f"{len(m['books'])}/11 (7 mapped + 4 stubs)"
    MAP.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    print("books now:", len(m["books"]))


if __name__ == "__main__":
    main()
