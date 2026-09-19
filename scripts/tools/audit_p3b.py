#!/usr/bin/env python3
"""Audit P3b cell: schema-keyword identity + SHAs. Zero API."""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
cells = json.load(open(os.path.join(BASE, "research", "mimo_spark_replication",
                                    "_v2_cells.json"), encoding="utf-8"))
assert cells["P0"]["system_sha256"].startswith("72c5424f")
assert cells["P0"]["template_sha256"].startswith("31b8e6eb")
assert cells["P1"]["template_sha256"].startswith("ee4e986e")
assert cells["P2"]["system_sha256"].startswith("704cbb21")
s, t = cells["P3b"]["system"], cells["P3b"]["template"]
keys = ["topic", "language", "concepts", "name", "category",
        "related_concepts", "definition_snippet", "relations",
        "source", "target", "type"]
missing = [k for k in keys if ('"' + k + '"') not in t]
assert not missing, missing
assert "1-7" in t and "CJK" in s
print("P3b-sys:", cells["P3b"]["system_sha256"][:16],
      "tpl:", cells["P3b"]["template_sha256"][:16])
print("P0-P3 UNCHANGED + P3b SCHEMA-OK")
