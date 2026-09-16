#!/usr/bin/env python3
"""Muse Spark re-extraction audit for mimo math extractions.
Reads source textbook txt from data/textbook/<name>.txt,
calls `opencode run -m opencode-go/muse-spark-1.3-contributor` with the
mimo schema prompt, saves raw Spark output to
research/mimo_spark_audit/<name>.spark.json (NEVER into data/math_extractions/).
Usage: python scripts/tools/spark_reextract.py <basename> [--timeout 300]
"""
import json, subprocess, sys
from pathlib import Path

MODEL = "opencode-go/muse-spark-1.3-contributor"
OPECODE = r"C:\Users\rongj\AppData\Roaming\npm\opencode.cmd"

PROMPT_TMPL = """TASK: Extract knowledge-graph JSON from the textbook text at the end. Do NOT ask questions. Do NOT converse. Do NOT explain. Output ONLY the JSON object, nothing else before or after it.

Schema:
{{"extracted_concepts": [{{"name": "<source-language name>", "aliases": ["english", "chinese"], "definition_snippet": "<short>", "category": "concept|operation|theorem|property"}}],
 "extracted_relations": [{{"source": "<name from concepts>", "target": "<name from concepts>", "type": "requires|representation|generalization|inverse_of|part_of", "importance": 0.0-1.0, "evidence": "<short>"}}]}}
Keys MUST be exactly "extracted_concepts" and "extracted_relations" (never "nodes"/"edges"/"concepts"/"relations"). Example:
{{"extracted_concepts": [{{"name": "Differentiation", "aliases": ["differentiation", "微分"], "definition_snippet": "Berechnung der Ableitung", "category": "concept"}}, {{"name": "Grenzwerte", "aliases": ["limits", "极限"], "definition_snippet": "Wert, dem sich eine Funktion naehert", "category": "concept"}}],
 "extracted_relations": [{{"source": "Differentiation", "target": "Grenzwerte", "type": "requires", "importance": 0.95, "evidence": "Ableitung ist ein Grenzwert"}}]}}
Aim 15-40 concepts, 10-30 relations. Every source/target must be a listed concept name. No placeholders. Empty lists are FORBIDDEN — extract from the text.

TEXTBOOK ({lang} / {title}):
{text}
BEGIN JSON NOW:"""

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("basename")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--model", default=MODEL)
    a = ap.parse_args()
    root = Path(__file__).resolve().parent.parent.parent
    src = root / "data" / "textbook" / (a.basename + ".txt")
    out = root / "research" / "mimo_spark_audit" / (a.basename + ".spark.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    lang = a.basename.split("_")[0]
    title = a.basename
    prompt = PROMPT_TMPL.format(lang=lang, title=title, text=text[:12000])
    r = subprocess.run([OPECODE, "run", "--format", "json", "-m", a.model, prompt],
                       capture_output=True, timeout=a.timeout, cwd=str(root))
    stdout = (r.stdout or b"").decode("utf-8", errors="ignore")
    text_out = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        # collect assistant text deltas across known event shapes
        for key in ("delta", "text", "content"):
            v = ev.get(key)
            if isinstance(v, str):
                text_out.append(v)
        for key in ("part", "message", "data"):
            v = ev.get(key)
            if isinstance(v, dict):
                for k2 in ("delta", "text", "content"):
                    if isinstance(v.get(k2), str):
                        text_out.append(v[k2])
    raw = "".join(text_out) if text_out else stdout
    # try to isolate JSON
    import re
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    payload = None
    if m:
        try:
            cand = json.loads(m.group())
            # accept mimo schema OR agent schema (concepts/relations); reject placeholders
            names = [c.get("name", "") for c in
                     cand.get("extracted_concepts", cand.get("concepts", []))]
            if names and not any(n.strip() in ("...", "") for n in names):
                # normalize agent schema to mimo schema
                if "extracted_concepts" not in cand and "concepts" in cand:
                    conv_c = []
                    for c in cand["concepts"]:
                        lab = c.get("labels", {}) or {}
                        conv_c.append({"name": c.get("name", ""),
                            "aliases": [lab.get("en", ""), lab.get("zh", "")],
                            "definition_snippet": "", "category": "concept"})
                    conv_r = [{"source": r.get("source", ""), "target": r.get("target", ""),
                        "type": r.get("type", "requires"), "importance": 0.85,
                        "evidence": ""} for r in cand.get("relations", [])]
                    cand = {"extracted_concepts": conv_c, "extracted_relations": conv_r}
                payload = cand
        except Exception:
            payload = None
    out.write_text(json.dumps({"model": a.model, "source": a.basename,
        "parsed": payload, "raw": raw[:12000]}, ensure_ascii=False, indent=1), encoding="utf-8")
    nc = len(payload.get("extracted_concepts", [])) if payload else 0
    nr = len(payload.get("extracted_relations", [])) if payload else 0
    print(f"saved {out} concepts={nc} relations={nr} parsed={payload is not None}")

if __name__ == "__main__":
    main()
