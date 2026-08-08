#!/usr/bin/env python3
"""LinguaGraph — D1: P3 association glossing post-pass.

Problem: P3 free associations are output in the SOURCE language (e.g. ZH 自由),
but lds_c_compute.canonical_key only extracts Latin tokens, so cross-language
association LDS would be empty for ZH. To make the M2 comparison (concept
divergence vs association divergence) comparable, gloss each association word
to English, then canonicalize in the same key space as concepts.

Design: for each (language, topic) cell, collect the union of association words
across its k samples, batch-gloss them to English in ONE call per cell
(15 cells = 3 langs x 5 topics). Small mapping task (not clustering), so
deepseek-v4-flash should be reliable at BATCH<=~80 words.

Output: data/lds_c/llm_subject/assoc_gloss_<date>.json
  { cells: [ {lang, topic, words: [{word, en}] } ] }
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

API_URL = "https://opencode.ai/zen/go/v1"
MODEL = "deepseek-v4-flash"
OUT_DIR = PROJECT_ROOT / "data" / "lds_c" / "llm_subject"
TOPICS = ["Freiheit", "Gerechtigkeit", "Verantwortung", "Heimat", "Erfolg"]

GLOSS_SYSTEM = (
    "You are a bilingual lexicographer. For each word, give a concise single-word "
    "or short-phrase English translation/gloss capturing its core meaning. "
    "Respond ONLY with valid JSON."
)
GLOSS_PROMPT = """Give the English gloss for each word below. Return ONLY compact JSON:
{{"glosses":[{{"word":"<original>","en":"<english gloss>"}}]}}

Words:
{words}
"""


def load_env_key() -> str:
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                if k.strip() == "OPENAI_API_KEY":
                    return v.strip()
    return os_environ_key()


def os_environ_key() -> str:
    import os
    return os.environ.get("OPENAI_API_KEY", "")


def _parse_json(raw: str) -> Optional[dict]:
    cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    if "```json" in cleaned:
        cleaned = cleaned.split("```json")[1].split("```")[0].strip()
    elif "```" in cleaned:
        cleaned = cleaned.split("```")[1].split("```")[0].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                return None
        return None


def call(client, system: str, user: str, max_tokens: int = 4096, timeout: int = 180):
    start = time.time()
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            temperature=0.0,
            max_tokens=max_tokens,
            timeout=timeout,
        )
        raw = resp.choices[0].message.content or ""
        return raw, {
            "latency_ms": int((time.time() - start) * 1000),
            "tokens_in": resp.usage.prompt_tokens if resp.usage else 0,
            "tokens_out": resp.usage.completion_tokens if resp.usage else 0,
        }
    except Exception as e:
        return f"ERROR: {e}", {"latency_ms": int((time.time() - start) * 1000)}


def collect_cells(units: List[dict]) -> List[dict]:
    """Union of association words per (lang, topic) cell."""
    by_cell: Dict[tuple, Dict[str, str]] = {}
    for u in units:
        if u.get("probe") != "P3":
            continue
        lang, topic = u["language"], u["topic"]
        for w in u.get("associations", []):
            w = w.strip()
            if w:
                by_cell.setdefault((lang, topic), {})[w] = w
    cells = []
    for (lang, topic), words in sorted(by_cell.items()):
        cells.append({"lang": lang, "topic": topic, "words": sorted(words)})
    return cells


def gloss_cell(client, lang: str, topic: str, words: List[str]) -> dict:
    """One batch call per cell (simple mapping task, deepseek-safe at this size)."""
    lines = "\n".join(words)
    raw, meta = call(client, GLOSS_SYSTEM, GLOSS_PROMPT.format(words=lines), 4096, 180)
    glosses: Dict[str, str] = {}
    note = "OK"
    if not raw.startswith("ERROR"):
        parsed = _parse_json(raw)
        if parsed and "glosses" in parsed:
            for g in parsed["glosses"]:
                w = (g.get("word") or "").strip()
                en = (g.get("en") or "").strip()
                if w and en:
                    glosses[w] = en
            missing = [w for w in words if w not in glosses]
            if missing:
                note = f"partial ({len(missing)}/{len(words)} missing)"
        else:
            note = f"parse-fail, raw={raw[:80]!r}"
    else:
        note = raw[:80]
    return {"lang": lang, "topic": topic, "n_words": len(words),
            "n_glossed": len(glosses), "note": note, "glosses": glosses}


def main() -> None:
    ap = argparse.ArgumentParser(description="P3 association glossing post-pass")
    ap.add_argument("--in", dest="in_file", type=str, default=None,
                    help="collection json; default = latest llm_subject_*.json")
    ap.add_argument("--out", type=str, default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.in_file:
        data = json.loads(Path(args.in_file).read_text(encoding="utf-8"))
    else:
        files = sorted(OUT_DIR.glob("llm_subject_*.json"))
        if not files:
            print("ERROR: no collection file found")
            sys.exit(1)
        data = json.loads(files[-1].read_text(encoding="utf-8"))
    units = data.get("units", [])

    cells = collect_cells(units)
    print(f"  P3 units: {sum(1 for u in units if u.get('probe') == 'P3')}")
    print(f"  Cells (lang x topic): {len(cells)}")
    for c in cells:
        print(f"    {c['lang']} / {c['topic']}: {len(c['words'])} unique words")
    if args.dry_run:
        return

    key = load_env_key()
    if not key:
        print("ERROR: OPENAI_API_KEY not found")
        sys.exit(1)
    from openai import OpenAI
    client = OpenAI(base_url=API_URL, api_key=key)

    out_path = OUT_DIR / (args.out or f"assoc_gloss_{datetime.now().strftime('%Y%m%d')}.json")
    done = {}
    if out_path.exists():
        try:
            prev = json.loads(out_path.read_text(encoding="utf-8"))
            for c in prev.get("cells", []):
                done[(c["lang"], c["topic"])] = c
            print(f"  Resume: {len(done)} cells done")
        except json.JSONDecodeError:
            pass

    results = []
    for i, cell in enumerate(cells, 1):
        key_ = (cell["lang"], cell["topic"])
        if key_ in done:
            results.append(done[key_])
            continue
        print(f"  [{i}/{len(cells)}] {cell['lang']}/{cell['topic']} "
              f"({len(cell['words'])} words)...", end=" ", flush=True)
        res = gloss_cell(client, cell["lang"], cell["topic"], cell["words"])
        print(f"{res['note']} ({res['n_glossed']}/{res['n_words']}, {res.get('_lat', 0)}ms)")
        results.append(res)
        out_path.write_text(json.dumps(
            {"model": MODEL, "generated_at": datetime.now().isoformat(),
             "cells": results}, ensure_ascii=False, indent=1), encoding="utf-8")
        time.sleep(0.3)

    print(f"\n  Saved: {out_path}")
    n_ok = sum(1 for c in results if c["n_glossed"] == c["n_words"])
    print(f"  Cells fully glossed: {n_ok}/{len(results)}")


if __name__ == "__main__":
    main()
