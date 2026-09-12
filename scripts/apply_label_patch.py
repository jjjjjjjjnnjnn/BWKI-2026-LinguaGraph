#!/usr/bin/env python3
"""v13: apply hand-authored label translations to cognitive-space/web/data.js.

Usage: python scripts/apply_label_patch.py
- Loads scripts/label_patch_{zh_a,zh_d1,zh_d2,de,en_a,en_b}.json
- For each node: fills MISSING label langs and placeholder langs (value copied
  from another lang), renames single wrong-script keys (CJK value under en/de).
- Never overwrites a real (distinct) translation; conflicts are reported.
- Re-run safe (idempotent). If release.py regenerates data.js, re-run this.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "cognitive-space" / "web" / "data.js"
Q = '"'


def load(name):
    d = json.loads((ROOT / "scripts" / name).read_text(encoding="utf-8"))
    d.pop("_note", None)
    return d


ZH = {}
for f in ("label_patch_zh_a.json", "label_patch_zh_d1.json", "label_patch_zh_d2.json"):
    ZH.update(load(f))
DE = load("label_patch_de.json")
EN = {}
for f in ("label_patch_en_a.json", "label_patch_en_b.json"):
    EN.update(load(f))

CJK = re.compile(r"[\u4e00-\u9fff]")

# Benign known variants: unmatched curriculum-topic nodes whose pre-existing
# real labels legitimately differ (plural/topic form) from the singular
# triple-concept patch. Never overwritten; listed here to keep reruns clean.
KNOWN_VARIANTS = {
    ("极限", "en", "limits"),
    ("极限", "de", "Grenzwerte"),
    ("微分", "en", "differentiation"),
    ("微分", "de", "Differentiation"),
    ("积分", "en", "integration"),
    ("积分", "de", "Integration"),
    ("特征值", "de", "Eigenwerte"),
    ("特征向量", "de", "Eigenvektoren"),
    ("拉格朗日乘数", "de", "Lagrange-Multiplikatoren"),
    ("分数", "de", "Brüche"),
    ("小数", "de", "Dezimalzahlen"),
    ("中心对称", "en", "point symmetry"),
}


def is_cjk(s):
    return bool(CJK.search(s or ""))


text = DATA.read_text(encoding="utf-8")
assert '\\"' not in text, "escaped quotes present - parser assumptions break"
assert text.count("{") == text.count("}"), "brace mismatch"

ids = re.findall(r'"id"\s*:\s*"([^"]+)"', text)
parts = text.split('"labels"')
assert len(parts) - 1 == len(ids) == 556, (len(parts) - 1, len(ids))

# value pattern: "xx" : "v"  (no escaped quotes, no braces in values)
WS = r"[ \t\r\n]*"
PAIR = re.compile(Q + r"([a-z][a-z])" + Q + WS + r":" + WS + Q + r"([^" + Q + r"]*)" + Q)
assert all("{" not in v and "}" not in v for m in PAIR.finditer(text) for v in [m.group(2)])

filled = {"zh": 0, "en": 0, "de": 0}
renamed = 0
conflicts = []
missing_concepts = []
touched_nodes = 0
out = [parts[0]]

for i, chunk in enumerate(parts[1:]):
    nid = ids[i]
    # find labels { ... } span (first balanced braces)
    start = chunk.index("{")
    depth, j = 0, start
    while True:
        if chunk[j] == "{":
            depth += 1
        elif chunk[j] == "}":
            depth -= 1
            if depth == 0:
                break
        j += 1
    body = chunk[start : j + 1]
    rest = chunk[j + 1 :]
    cur = dict(PAIR.findall(body))
    langs = [k for k in cur if k in ("zh", "en", "de")]

    # pick concept + map
    concept, mp, kind = None, None, None
    if "zh" in cur and (len(langs) > 1 or is_cjk(cur.get("zh", ""))):
        concept, mp, kind = cur["zh"], ZH, "zh"
    elif len(langs) == 1:
        k = langs[0]
        v = cur[k]
        if is_cjk(v):
            concept, mp, kind = v, ZH, "zh-rename"
        elif k == "de":
            concept, mp, kind = v, DE, "de"
        elif k == "en":
            concept, mp, kind = v, EN, "en"
    if concept is None:  # unexpected shape -> try CJK rescue, else keep+report
        cjk_vals = [(k, v) for k, v in cur.items() if k in ("zh", "en", "de") and is_cjk(v)]
        if cjk_vals:
            concept, mp, kind = cjk_vals[0][1], ZH, "zh-rename"
            entry = mp.get(concept)
            if entry is None:
                missing_concepts.append((nid, kind, concept, ["zh", "en", "de"]))
                out.append(chunk)
                continue
        else:
            conflicts.append((nid, "shape", cur))
            out.append(chunk)
            continue
    entry = mp.get(concept)
    if entry is None:
        # no patch needed if nothing missing/placeholder?
        need = [L for L in ("zh", "en", "de") if L not in cur] + [
            L
            for L in ("en", "de")
            if L in cur and "zh" in cur and (cur[L] == cur["zh"] or is_cjk(cur[L]))
        ]
        if need:
            missing_concepts.append((nid, kind, concept, need))
        out.append(chunk)
        continue

    new = dict(cur)
    changed = False
    # rename single wrong-script key: rebuild canonical triple
    if kind in ("zh-rename", "zh") and len([k for k in cur if k in ("zh", "en", "de")]) == 1 and "zh" in cur:
        # pure zh-mono node: add missing en/de
        for L in ("en", "de"):
            if L not in new and entry.get(L):
                new[L] = entry[L]
                filled[L] += 1
                changed = True
    elif kind == "zh-rename":
        new = {"zh": concept}
        for L in ("en", "de"):
            if entry.get(L):
                new[L] = entry[L]
                filled[L] += 1
        if "zh" not in cur:
            filled["zh"] += 1
        changed = True
        renamed += 1
    else:
        if kind in ("de", "en") and len(langs) == 1:
            for L in ("zh", "en", "de"):
                if L not in new and entry.get(L):
                    new[L] = entry[L]
                    filled[L] += 1
                    changed = True
        else:  # triple node: only fix placeholders
            for L in ("en", "de"):
                if L in new and "zh" in new and entry.get(L):
                    if new[L] == new["zh"] or (L in ("en", "de") and is_cjk(new[L])):
                        new[L] = entry[L]
                        filled[L] += 1
                        changed = True
    # conflict check: real existing value differs from patch
    for L in ("zh", "en", "de"):
        if L in cur and entry.get(L) and L in new and cur[L] != new.get(L, cur[L]):
            pass  # new[L] is cur[L] here unless just filled; filled only when placeholder/missing
        if L in cur and entry.get(L) and cur[L] != entry[L]:
            # allow if cur[L] was a placeholder of zh (copy or CJK synonym) or L missing handled
            if (
                not (
                    L in ("en", "de")
                    and "zh" in cur
                    and (cur[L] == cur["zh"] or is_cjk(cur[L]))
                )
                and (concept, L, cur[L]) not in KNOWN_VARIANTS
            ):
                conflicts.append((nid, L, cur[L], entry[L]))
    if changed:
        touched_nodes += 1
        # rebuild block: original key order, new keys appended in zh,en,de order
        indent = body.split("\n")[1][: len(body.split("\n")[1]) - len(body.split("\n")[1].lstrip())] if "\n" in body else "        "
        order = [k for k in cur if k in ("zh", "en", "de")] + [L for L in ("zh", "en", "de") if L not in cur and L in new]
        inner = (",\n" + indent).join(Q + L + Q + ": " + Q + new[L] + Q for L in order)
        close_indent = indent[: max(0, len(indent) - 2)]
        new_body = "{\n" + indent + inner + "\n" + close_indent + "}"
        out.append(chunk[:start] + new_body + rest)
    else:
        out.append(chunk)

DATA.write_text('"labels"'.join(out), encoding="utf-8")
print("touched nodes:", touched_nodes)
print("filled:", filled, "renamed keys:", renamed)
print("missing concepts:", len(missing_concepts))
for m in missing_concepts[:40]:
    print("  MISSING:", m)
print("conflicts:", len(conflicts))
for c in conflicts[:40]:
    print("  CONFLICT:", c)
