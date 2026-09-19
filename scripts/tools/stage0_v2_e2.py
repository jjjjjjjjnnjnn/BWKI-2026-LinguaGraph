#!/usr/bin/env python3
"""Append P3b + E2-ID freeze to addendum v1.2. Zero API. Run BEFORE first P3b call."""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
cells = json.load(open(os.path.join(BASE, "research", "mimo_spark_replication",
                                    "_v2_cells.json"), encoding="utf-8"))
P = os.path.join(BASE, "docs", "osf_preregistration_addendum_v1.2_v2.md")
E2_IDS = ("de_002,de_005,de_007,de_008,de_009,de_012,de_013,de_020,de_021,de_026,"
          "en_003,en_004,en_009,en_011,en_014,en_020,en_024,en_025,en_028,en_029,"
          "zh_006,zh_012,zh_017,zh_018,zh_019,zh_023,zh_025,zh_028,zh_031,zh_040")
assert len(E2_IDS.split(",")) == 30
v = cells["P3b"]
L = ["", "## A18. E2 P3b-paraphrase (frozen BEFORE first P3b call, 2026-09-19)",
     "Purpose: brittleness screen for P3 lift (F8). Same semantics (1-7 + source-language-only),",
     "different wording (English-first); schema keys byte-identical (audit_p3b.py).",
     "### P3b — system_sha256 `%s`" % v["system_sha256"],
     "`" + v["system"].replace("`", "'") + "`",
     "### P3b — template_sha256 `%s`" % v["template_sha256"],
     "```", v["template"], "```", "",
     "E2 IDs (n=30, 10/lang, seed 20260918, 5x gold_n1 + 5x gold_n2 per lang):",
     "`%s`" % E2_IDS,
     "Gate: |P3b−P3| <0.05 paired on same 30 → robust; ≥0.10 → brittle (P3 numbers reported as range).",
     "Arm: glm-5.2-r4 only. Output `t2_v2-glm52r4-P3b.json`. Driver `--only-ids` + `--cell P3b`.",
     ""]
open(P, "a", encoding="utf-8").write("\n".join(L))
print("A18-APPENDED")
