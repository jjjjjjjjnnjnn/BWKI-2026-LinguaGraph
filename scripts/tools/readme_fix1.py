#!/usr/bin/env python3
"""README fixes batch 1 (read exact lines, minimal replacements)."""
import io

# 1. final README: merge F12 duplex rows, fix Stand note, fix 55 composition
p = "submission/final/README.md"
ls = io.open(p, encoding="utf-8").read().splitlines()
assert ls[16].startswith("| F12 |") and ls[17].startswith("| F12 |")
merged = ("| F12 | LLM-within-subject Signal +0,08\u20130,09 (59 Messungen, 54 Modelle; "
          "file truth 62/57/186 incl. qwen-max n=26/30) | ~81 % CN-Anbieter; 9 EN-Paare n. s.; "
          "177er-Ma\u00dfzahl unverifiziert \u2014 nicht \u00fcbernommen |")
ls[16] = merged
del ls[17]
t = "\n".join(ls) + "\n"
old55 = "55 Messungen: 42 DashScope + 8 zen/OpenRouter + 2 Ki"
assert t.count(old55) == 1, t.count(old55)
t = t.replace(old55, "59 Messungen: 42 DashScope + 8 zen/OpenRouter + 2 Kilo + 1 Cohere + 1 NIM + 1 Cloudflare + 1 LM-Studio + 3 opencode-go (54 Modelle)")
old_note = "(uncommitted, nur Arbeitsstand)"
assert t.count(old_note) == 1
t = t.replace(old_note, "(committed 2026-09-16)")
io.open(p, "w", encoding="utf-8").write(t)
print("final README done")

# 2. docs/submission README: same 55 composition (mirror of final baseline)
p = "docs/submission/README.md"
t = io.open(p, encoding="utf-8").read()
assert t.count(old55) == 1, t.count(old55)
t = t.replace(old55, "59 Messungen: 42 DashScope + 8 zen/OpenRouter + 2 Kilo + 1 Cohere + 1 NIM + 1 Cloudflare + 1 LM-Studio + 3 opencode-go (54 Modelle)")
io.open(p, "w", encoding="utf-8").write(t)
print("docs/submission README done")

# 3. pitch README
p = "submission/pitch/README.md"
t = io.open(p, encoding="utf-8").read()
o2 = "55 Messungen/50 Modelle; ~87 % CN"
assert t.count(o2) == 1
t = t.replace(o2, "59 Messungen/54 Modelle; ~81 % CN")
io.open(p, "w", encoding="utf-8").write(t)
print("pitch README done")

# 4. portal README
p = "cognitive-space/portal/README.md"
t = io.open(p, encoding="utf-8").read()
o3 = "55-margin fused replication chart"
assert t.count(o3) == 1
t = t.replace(o3, "59-measurement fused replication chart (file-truth 62/57/186)")
io.open(p, "w", encoding="utf-8").write(t)
print("portal README done")

# 5. cognitive-space README: 574 + textbook split
p = "cognitive-space/README.md"
t = io.open(p, encoding="utf-8").read()
o4 = "**574** (557 unique, 17 aligned)"
assert t.count(o4) == 1
t = t.replace(o4, "**556** nodes (525 relations, 219 groups; frozen 2026-09-12)")
o5 = "**68** (45 ZH / 20 EN / 10 DE)"
assert t.count(o5) == 1
t = t.replace(o5, "**68** (39 ZH / 18 EN / 11 DE)")
io.open(p, "w", encoding="utf-8").write(t)
print("cognitive-space README done")
