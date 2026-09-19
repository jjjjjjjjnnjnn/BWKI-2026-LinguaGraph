#!/usr/bin/env python3
"""Stage0 helper: derive v2 cells from frozen v1 driver strings. Zero API."""
import hashlib
import importlib.util
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = importlib.util.spec_from_file_location(
    "bench", os.path.join(BASE, "scripts", "tools", "spark_zen_gold_bench.py"))
bench = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bench)

SYSTEM, TEMPLATE = bench.SYSTEM, bench.TEMPLATE
print("v1 sys sha:", hashlib.sha256(SYSTEM.encode()).hexdigest())
print("v1 tpl sha:", hashlib.sha256(TEMPLATE.encode()).hexdigest())
assert hashlib.sha256(SYSTEM.encode()).hexdigest().startswith("72c5424f")
assert hashlib.sha256(TEMPLATE.encode()).hexdigest().startswith("31b8e6eb")

OLD_CARD = "任务：提取 10-20 个核心概念，并按以下 JSON Schema 输出："
NEW_CARD = "任务：提取 1-7 个真正独立的核心概念（通常 2-3 个；宁缺勿滥，禁止为凑数拆分或填充），并按以下 JSON Schema 输出："
assert TEMPLATE.count(OLD_CARD) == 1
P1_TEMPLATE = TEMPLATE.replace(OLD_CARD, NEW_CARD)
P2_SYSTEM = ("你是概念提取专家。只输出严格 JSON 格式。"
             "概念名称必须使用文本源语言（中文文本用中文，德文文本用德文，"
             "英文文本用英文）；严禁翻译；英文或德文文本中严禁输出任何 CJK 字符。")
CELLS = {"P0": (SYSTEM, TEMPLATE), "P1": (SYSTEM, P1_TEMPLATE),
         "P2": (P2_SYSTEM, TEMPLATE), "P3": (P2_SYSTEM, P1_TEMPLATE)}
out = {}
for cell, (s, t) in CELLS.items():
    out[cell] = {"system": s, "template": t,
                 "system_sha256": hashlib.sha256(s.encode()).hexdigest(),
                 "template_sha256": hashlib.sha256(t.encode()).hexdigest()}
json.dump(out, open(os.path.join(BASE, "research", "mimo_spark_replication",
                                "_v2_cells.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
for cell, v in out.items():
    print(cell, v["system_sha256"][:16], v["template_sha256"][:16])
print("STAGE0-CELLS-OK")
