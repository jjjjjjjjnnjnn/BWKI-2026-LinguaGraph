#!/usr/bin/env python3
"""Submission wording fixes batch 1: q-hedge + F1 Developing suffix (docs + final)."""
import io

edits = [
    ("reproduziert exakt die menschliche Marge (+0.014 \u2248 +0.015;",
     "reproduziert nahezu die menschliche Marge (+0.014 \u2248 +0.015; Punktsch\u00e4tzung ohne CI;"),
    ("konsistent auf die aggregationsbedingte Sparsity als Mechanismus zur\u00fcckgef\u00fchrt",
     "im Einklang mit aggregationsbedingter Sparsity als Mechanismus-Hypothese gedeutet"),
    ("(soziale Konzepte F1\u22480.94, deutsche Mathematik F1\u22480.51)",
     "(soziale Konzepte F1\u22480.94, deutsche Mathematik F1\u22480.51; Developing C9b, Harness ~0,65, Blind-Review pending, keine Validierungs-Behauptung)"),
]
for p in ("docs/submission/plattform_antworten.md",
          "submission/final/plattform_antworten.md"):
    t = io.open(p, encoding="utf-8").read()
    for old, new in edits:
        assert t.count(old) == 1, "match!=1 in %s: %s" % (p, old[:40])
        t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(t)
    print("fixed", p)
