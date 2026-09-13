#!/usr/bin/env python3
"""Build grounding_lookup.js from expert-graph grounding JSONs (W0 data layer).

Reads:
  config/expert_graphs/text_grounding_20260912.json
    graphs.physics / graphs.chemistry -> items[].name / zh_grounded[{file,term,count,snippet}]
  config/expert_graphs/text_grounding_en_semantic_20260912.json
    results[].name / semantic_hit / evidence
  config/expert_graphs/cn_textbook_mapping.json
    books[].book / chapters[].chapter / sections[]{section, maps_to[]} (reverse maps_to -> node)

Writes:
  cognitive-space/web/grounding_lookup.js
    var GROUNDING_LOOKUP = {<name>:{zh:[{f,t,c,s}], en:{hit,ev}, cn:[{b,ch,s}]}};

Notes:
  - snippet (zh) and evidence sent (en) are truncated to 120 chars, then JSON-escaped
    (json.dumps ensure_ascii=False + </script> / U+2028/29 neutralisation, valid as JS).
  - zh entry: {f: file, t: term, c: count, s: snippet[:120]}
  - en entry: {hit: bool, ev: null | {f: file, s: sent[:120]}}
  - cn entry: {b: book, ch: chapter, s: section}
"""
import json
import sys
from pathlib import Path

SNIP_LEN = 120

ROOT = Path(__file__).resolve().parent.parent
P_ZH = ROOT / "config" / "expert_graphs" / "text_grounding_20260912.json"
P_EN = ROOT / "config" / "expert_graphs" / "text_grounding_en_semantic_20260912.json"
P_CN = ROOT / "config" / "expert_graphs" / "cn_textbook_mapping.json"
P_OUT = ROOT / "cognitive-space" / "web" / "grounding_lookup.js"


def trunc(s, n=SNIP_LEN):
    if s is None:
        return ""
    s = str(s)
    return s[:n]


def main():
    zh_data = json.loads(P_ZH.read_text(encoding="utf-8"))
    en_data = json.loads(P_EN.read_text(encoding="utf-8"))
    cn_data = json.loads(P_CN.read_text(encoding="utf-8"))

    lookup = {}

    def ensure(name):
        if name not in lookup:
            lookup[name] = {"zh": [], "en": {"hit": False, "ev": None}, "cn": []}
        return lookup[name]

    # 1) ZH substring grounding (physics + chemistry)
    graphs = zh_data.get("graphs", {})
    for gname in ("physics", "chemistry"):
        items = graphs.get(gname, {}).get("items", [])
        for it in items:
            name = it.get("name")
            if not name:
                continue
            e = ensure(name)
            for g in it.get("zh_grounded", []) or []:
                e["zh"].append({
                    "f": str(g.get("file", "")),
                    "t": str(g.get("term", "")),
                    "c": int(g.get("count", 0) or 0),
                    "s": trunc(g.get("snippet", "")),
                })

    # 2) EN semantic grounding
    for r in en_data.get("results", []) or []:
        name = r.get("name")
        if not name:
            continue
        e = ensure(name)
        hit = bool(r.get("semantic_hit"))
        ev = r.get("evidence")
        ev_out = None
        if hit and isinstance(ev, dict):
            ev_out = {"f": str(ev.get("file", "")), "s": trunc(ev.get("sent", ""))}
        elif hit and isinstance(ev, str):
            ev_out = {"f": "", "s": trunc(ev)}
        e["en"] = {"hit": hit, "ev": ev_out}

    # 3) CN textbook mapping (reverse maps_to -> node)
    for book in cn_data.get("books", []) or []:
        b = str(book.get("book", ""))
        for ch in book.get("chapters", []) or []:
            chn = str(ch.get("chapter", ""))
            for sec in ch.get("sections", []) or []:
                s = str(sec.get("section", ""))
                for node in sec.get("maps_to", []) or []:
                    if not node:
                        continue
                    e = ensure(str(node))
                    e["cn"].append({"b": b, "ch": chn, "s": s})

    # Emit JS: JSON is valid JS object literal; neutralise script-breakers.
    payload = json.dumps(lookup, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</script", "<\\/script")
    payload = payload.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    out = "var GROUNDING_LOOKUP = " + payload + ";\n"
    P_OUT.write_text(out, encoding="utf-8")

    n_zh = sum(1 for v in lookup.values() if v["zh"])
    n_en = sum(1 for v in lookup.values() if v["en"]["hit"])
    n_cn = sum(1 for v in lookup.values() if v["cn"])
    print(f"nodes={len(lookup)} zh_nodes={n_zh} en_hit_nodes={n_en} cn_nodes={n_cn}")
    print(f"wrote {P_OUT.relative_to(ROOT)} bytes={len(out.encode('utf-8'))}")


if __name__ == "__main__":
    sys.exit(main())
