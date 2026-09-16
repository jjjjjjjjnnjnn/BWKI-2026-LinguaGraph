#!/usr/bin/env python3
"""Muse Spark direct-API re-extraction (single-turn, no agentic wrapper).
Key: read from .env OPENCODE_ZEN_API_KEY in-process, NEVER printed/written.
Endpoint: https://opencode.ai/zen/go/v1/chat/completions
Model: opencode-go/muse-spark-1.3-contributor
Usage: python scripts/tools/spark_reextract_api.py <basename> [--model ...]
"""
import json, os, sys, urllib.request
from pathlib import Path

API_URL = "https://opencode.ai/zen/go/v1/chat/completions"
DEFAULT_MODEL = "opencode-go/muse-spark-1.3-contributor"

PROMPT_TMPL = """Extract key mathematical CONCEPTS and RELATIONS from the textbook outline below.
Names in source language; add English + Chinese aliases where known.
Return ONLY valid JSON, no prose, no placeholders:
{{"extracted_concepts": [{{"name": "...", "aliases": ["en","zh"], "definition_snippet": "...", "category": "concept|operation|theorem|property"}}],
 "extracted_relations": [{{"source": "...", "target": "...", "type": "requires|representation|generalization|inverse_of|part_of", "importance": 0.85, "evidence": "..."}}]}}
Rules: every source/target must be a listed concept name. 15-40 concepts, 10-30 relations.

TEXTBOOK ({lang} / {title}):
{text}
"""

def load_key(root: Path) -> str:
    for line in (root / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("OPENCODE_ZEN_API_KEY="):
            return line.split("=", 1)[1].strip()
    return os.environ.get("OPENCODE_ZEN_API_KEY", "")

def call(model, prompt, key):
    body = json.dumps({"model": model, "messages": [
        {"role": "system", "content": "Knowledge-graph extractor. Output strict JSON only."},
        {"role": "user", "content": prompt}], "temperature": 0.0,
        "max_tokens": 4096}).encode()
    req = urllib.request.Request(API_URL, data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key,
                 "User-Agent": "curl/8.0", "Accept": "application/json"})
    resp = json.loads(urllib.request.urlopen(req, timeout=180).read())
    return resp["choices"][0]["message"]["content"]

def main():
    import argparse, re
    ap = argparse.ArgumentParser()
    ap.add_argument("basename"); ap.add_argument("--model", default=DEFAULT_MODEL)
    a = ap.parse_args()
    root = Path(__file__).resolve().parent.parent.parent
    key = load_key(root)
    if not key: print("ERROR: no key"); sys.exit(1)
    text = (root / "data" / "textbook" / (a.basename + ".txt")).read_text(encoding="utf-8")
    out = root / "research" / "mimo_spark_audit" / (a.basename + ".spark.json")
    content = call(a.model, PROMPT_TMPL.format(
        lang=a.basename.split("_")[0], title=a.basename, text=text[:12000]), key)
    m = re.search(r"\{.*\}", content, re.DOTALL)
    payload = None
    if m:
        try:
            cand = json.loads(m.group())
            names = [c.get("name", "") for c in cand.get("extracted_concepts", [])]
            if names and not any(n.strip() in ("...", "") for n in names):
                payload = cand
        except Exception as e:
            print(f"[warn] parse: {e}", file=sys.stderr)
    out.write_text(json.dumps({"model": a.model, "source": a.basename,
        "parsed": payload, "raw": content[:12000]}, ensure_ascii=False, indent=1), encoding="utf-8")
    nc = len(payload.get("extracted_concepts", [])) if payload else 0
    nr = len(payload.get("extracted_relations", [])) if payload else 0
    print(f"saved {out.name} concepts={nc} relations={nr} parsed={payload is not None}")

if __name__ == "__main__":
    main()
