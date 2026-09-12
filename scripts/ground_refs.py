"""Text-grounding: match graph concept labels against local textbook texts.
ZH labels -> 31 CN chapter txts; EN labels -> 72 OpenStax sections + MIT chs.
Writes config/expert_graphs/text_grounding_20260912.json (tracked evidence).
Usage: python scripts/ground_refs.py
"""
import glob
import json
from pathlib import Path

ROOT = Path(".")
CN_FILES = sorted(glob.glob("data/textbook/zh_物理*.txt") +
                  glob.glob("data/textbook/zh_化学*.txt"))
EN_FILES = sorted(glob.glob("data/textbook/open/en_openstax_*sec*.txt")) + sorted(
    glob.glob("data/textbook/en_mit801_notes_ch*.txt"))

print(f"CN files: {len(CN_FILES)}, EN files: {len(EN_FILES)}")
cn_texts = {f: Path(f).read_text(encoding="utf-8") for f in CN_FILES}
en_texts = {f: Path(f).read_text(encoding="utf-8") for f in EN_FILES}


def core_terms(label: str) -> list:
    label = (label or "").strip()
    if not label:
        return []
    terms = [label]
    # strip common affixes for recall: 定律/定理/效应/原理/法则/常数/反应/结构
    for aff in ["定律", "定理", "效应", "原理", "法则", "常数"]:
        if label.endswith(aff) and len(label) > len(aff) + 1:
            terms.append(label[: -len(aff)])
    return terms


def ground(label: str, texts: dict, cap: int = 5) -> list:
    hits = []
    for term in core_terms(label):
        if len(term) < 2:
            continue
        for f, t in texts.items():
            n = t.count(term)
            if n > 0:
                i = t.find(term)
                hits.append({"file": Path(f).name, "term": term,
                             "count": n,
                             "snippet": t[max(0, i - 30):i + 30].replace("\n", " ")})
                if len(hits) >= cap:
                    return hits
        if hits:
            break
    return hits


def main() -> None:
    out = {"date": "2026-09-12", "method": "substring grounding (fact-level)",
           "graphs": {}}
    for gf, key in [("config/expert_graphs/physics_full.json", "physics"),
                    ("config/expert_graphs/chemistry_full.json", "chemistry")]:
        d = json.loads(Path(gf).read_text(encoding="utf-8"))
        nodes, zh_hit, en_hit = [], 0, 0
        for c in d["concepts"]:
            lab = c.get("labels", {}) or {}
            zh, en = lab.get("zh", ""), lab.get("en", "")
            zh_h, en_h = ground(zh, cn_texts), ground(en, en_texts)
            zh_hit += bool(zh_h)
            en_hit += bool(en_h)
            nodes.append({"name": c.get("name"), "zh": zh, "en": en,
                          "zh_grounded": zh_h, "en_grounded": en_h,
                          "de_text": "unavailable (LEIFI link-only)"})
        n = len(nodes)
        out["graphs"][key] = {"nodes": n,
                              "zh_grounded": zh_hit,
                              "zh_rate": round(zh_hit / n, 4) if n else 0,
                              "en_grounded": en_hit,
                              "en_rate": round(en_hit / n, 4) if n else 0,
                              "items": nodes}
        print(f"{key}: {n} nodes, zh {zh_hit} ({zh_hit/n:.1%}), "
              f"en {en_hit} ({en_hit/n:.1%})")
    Path("config/expert_graphs/text_grounding_20260912.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote text_grounding_20260912.json")


if __name__ == "__main__":
    main()
