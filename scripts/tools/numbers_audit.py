#!/usr/bin/env python3
"""Numbers gate: assert whitelisted numbers, fail on known-stale phrasing.

Checks (file, must_not_contain, must_contain):
- portal ZH mm_margin_src '55 个完整运行' -> must be 59
- portal ZH '8 个含 EN 测试不显著' (isolated) -> 9
- portal 'that is the 58-run replication' -> 59-run
- portal ZH glos_7 must carry file-truth suffix like EN/DE
- build_paper_pdf.py TITLE '55-Messungs-Replikation' -> 59
- plattform_antworten §5 F1 line must carry Developing suffix
Usage: python scripts/tools/numbers_audit.py [--help]
Exit 0 = gate pass; 1 = stale numbers found.
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check(path, banned, required=None):
    t = open(os.path.join(BASE, path), encoding="utf-8").read()
    errs = []
    for b in banned:
        if b in t:
            errs.append("STALE %s contains %r" % (path, b))
    for r in (required or []):
        if r not in t:
            errs.append("MISSING %s lacks %r" % (path, r))
    return errs


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: numbers_audit.py [--help]")
        print("  Asserts SSOT numbers (research/numbers_ssot_20260916.json), fails on stale phrasing.")
        return 0
    errs = []
    p = "cognitive-space/portal/index.html"
    errs += check(p, ["55 个完整运行", "8 个含 EN 测试不显著",
                      "that is the 58-run replication below"],
                  ["59 full runs", "59 vollständige Runs", "59 次测量"])
    errs += check(p, [], ["标签 shuffling，如中德 59/59、p＜0.004（500 perm.，file-truth 62/62）"])
    errs += check("scripts/build_paper_pdf.py", ["55-Messungs-Replikation"],
                  ["59 Messungen (54 eindeutige Modelle)"])
    for q in ("docs/submission/plattform_antworten.md",
              "submission/final/plattform_antworten.md"):
        errs += check(q, [], ["Developing"])
    if errs:
        print("\n".join(errs))
        print("NUMBERS_GATE FAIL (%d)" % len(errs))
        return 1
    print("NUMBERS_GATE PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
