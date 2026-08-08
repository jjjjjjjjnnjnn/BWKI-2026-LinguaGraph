#!/usr/bin/env python3
"""LinguaGraph — A4: Wikipedia concept glossing (ZH -> EN) for cross-source LDS.

Why: Wikipedia social-topic extractions (data/wikipedia_extractions/*_zh.json) hold
concepts in Chinese. lds_c_compute.canonical_key only extracts Latin tokens, so ZH
concepts collapse to empty keys and any cross-language LDS is trivially 1.0 — an
alignment artifact, not a real finding (fig_wikipedia_lds.py reports exactly this).

Fix: gloss every unique ZH concept to English (deepseek-v4-flash, batch mapping
task — proven reliable in lds_c_llm_gloss_assoc.py), then run the EN/DE concepts
and the ZH glosses through canonical_key so all three languages live in the same
canonical key space, exactly like the human (LDS-C) and LLM-as-subject pipelines.

Output: data/wikipedia_extractions/zh_to_en_gloss_<date>.json
  { "glosses": { "自由": "freedom", ... } }
"""

from __future__ import annotations

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
WIKI_DIR = PROJECT_ROOT / "data" / "wikipedia_extractions"

GLOSS_SYSTEM = (
    "You are a multilingual lexicographer. For each word (Chinese or German), give "
    "a concise single-word or short-phrase English translation/gloss capturing its "
    "core meaning. Respond ONLY with valid JSON."
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


def collect_zh_concepts() -> Dict[str, str]:
    """Unique concepts (ZH + DE) -> themselves, across all 5 topics.

    Both ZH and DE Wikipedia concepts are glossed to English so all 3 languages
    align in the same canonical key space (EN passes through)."""
    out: Dict[str, str] = {}
    for suffix in ("_zh", "_de"):
        for fpath in sorted(WIKI_DIR.glob(f"*{suffix}.json")):
            d = json.loads(fpath.read_text(encoding="utf-8"))
            for c in d.get("concepts", []):
                name = (c.get("name") or "").strip()
                if name:
                    out.setdefault(name, name)
            for r in d.get("relations", []):
                s = (r.get("source") or "").strip()
                t = (r.get("target") or "").strip()
                if s:
                    out.setdefault(s, s)
                if t:
                    out.setdefault(t, t)
    return out


def gloss_batch(client, words: List[str]) -> Dict[str, str]:
    """One deepseek call per batch (mapping task, BATCH<=60 to stay reliable)."""
    lines = "\n".join(words)
    start = time.time()
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": GLOSS_SYSTEM},
                      {"role": "user", "content": GLOSS_PROMPT.format(words=lines)}],
            temperature=0.0,
            max_tokens=4096,
            timeout=180,
        )
        raw = resp.choices[0].message.content or ""
    except Exception as e:
        return {}, f"ERROR: {e}"
    glosses: Dict[str, str] = {}
    parsed = _parse_json(raw)
    if parsed and "glosses" in parsed:
        for g in parsed["glosses"]:
            w = (g.get("word") or "").strip()
            en = (g.get("en") or "").strip()
            if w and en:
                glosses[w] = en
    return glosses, raw[:120]


def main() -> None:
    import argparse
    import os
    ap = argparse.ArgumentParser(description="A4: ZH Wikipedia concept glossing")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    zh = collect_zh_concepts()
    print(f"  Unique ZH+DE Wikipedia concepts (incl. relation labels): {len(zh)}")

    out_path = WIKI_DIR / f"wiki_gloss_{datetime.now().strftime('%Y%m%d')}.json"
    # resume: load both the new combined file and the legacy zh-only file
    done: Dict[str, str] = {}
    if out_path.exists():
        prev = json.loads(out_path.read_text(encoding="utf-8"))
        done.update(prev.get("glosses", {}))
    legacy = WIKI_DIR / f"zh_to_en_gloss_{datetime.now().strftime('%Y%m%d')}.json"
    if legacy.exists():
        prev = json.loads(legacy.read_text(encoding="utf-8"))
        done.update(prev.get("glosses", {}))
    print(f"  Resume: {len(done)} already glossed")

    missing = [w for w in zh if w not in done]
    if args.dry_run:
        print(f"  To gloss: {len(missing)} (ZH+DE)")
        print("  Missing sample:", missing[:20])
        return
    if not missing:
        print("  All concepts already glossed.")
        return

    key = load_env_key()
    if not key:
        print("ERROR: OPENAI_API_KEY not found")
        sys.exit(1)
    from openai import OpenAI
    client = OpenAI(base_url=API_URL, api_key=key)

    BATCH = 60
    for i in range(0, len(missing), BATCH):
        chunk = missing[i:i + BATCH]
        g, note = gloss_batch(client, chunk)
        done.update(g)
        still = [w for w in chunk if w not in done]
        if still:
            # retry empty/missing once with a second attempt
            for _ in range(2):
                g2, _ = gloss_batch(client, still)
                done.update(g2)
                still = [w for w in still if w not in done]
                if not still:
                    break
        print(f"  [{i + len(chunk)}/{len(missing)}] glossed {len(g)} "
              f"({len(still)} missing)" + (f" note={note}" if still else ""))
        out_path.write_text(json.dumps(
            {"model": MODEL, "generated_at": datetime.now().isoformat(),
             "glosses": done}, ensure_ascii=False, indent=1), encoding="utf-8")
        time.sleep(0.3)

    missing_final = [w for w in zh if w not in done]
    print(f"\n  Saved: {out_path}")
    print(f"  Coverage: {len(done) - len(zh) + len(missing_final) + len(zh) - len(missing_final)}/? "
          f"final missing: {len(missing_final)}")
    if missing_final:
        print(f"  Missing: {missing_final}")


if __name__ == "__main__":
    main()
