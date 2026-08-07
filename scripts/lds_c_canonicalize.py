#!/usr/bin/env python3
"""
LinguaGraph — LLM Semantic Canonicalization of glosses

Bridges lexical gaps in concept alignment that deterministic synonym/stem
matching cannot (e.g. ZH "cage of power" ~ DE "absence of coercion" ~ EN
"boundaries"). Uses deepseek-v4-flash semantic judgment to cluster glosses
that refer to the SAME underlying concept.

Saves a gloss -> canonical_term mapping (reproducible) consumed by
lds_c_compute.py via --canonical.

Usage:
    python scripts/lds_c_canonicalize.py                  # cluster all glosses
    python scripts/lds_c_canonicalize.py --dry-run        # show gloss count only

Output: data/lds_c/gloss_clusters_<date>.json
"""

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
API_URL = "https://opencode.ai/zen/go/v1"
MODEL = "deepseek-v4-flash"
CHUNK = 30

CANON_PROMPT = """You are aligning concepts extracted from Chinese, German, and English responses about abstract topics (freedom, justice, responsibility, home, success).

Below is a list of English glosses. Group them into clusters where members denote the SAME underlying concept (true synonyms / near-equivalent expressions of one idea).

RULES:
- Merge ONLY when they clearly denote the same idea (e.g. 'duty', 'obligation', 'responsibility' -> 'responsibility').
- Do NOT merge merely-related but distinct concepts (e.g. 'freedom' vs 'choice' vs 'autonomy' are related but should stay separate; 'negative freedom' vs 'freedom' are distinct).
- Preserve genuine nuance. If unsure, keep separate (conservative).
- For each gloss, output the canonical term (choose the most representative member of its cluster; if a gloss is a singleton, canonical = itself).

Return ONLY JSON, no explanation:
{{"gloss1": "canonical1", "gloss2": "canonical2", ...}}

Glosses:
{glosses}
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
    return os.environ.get("OPENAI_API_KEY", "")


def collect_glosses() -> List[str]:
    import glob
    files = sorted(glob.glob(str(PROJECT_ROOT / "data" / "lds_c" / "extractions_*.json")))
    if not files:
        raise FileNotFoundError("No extractions found")
    glosses = set()
    for fp in files:
        data = json.loads(Path(fp).read_text(encoding="utf-8"))
        for r in data.get("responses", []):
            for t in r.get("topics", []):
                for c in t.get("concepts", []):
                    en = (c.get("en", "") or "").strip().lower()
                    if en:
                        glosses.add(en)
    return sorted(glosses)


def call_canonical(client, glosses: List[str]) -> Dict[str, str]:
    prompt = CANON_PROMPT.format(glosses="\n".join(f"- {g}" for g in glosses))
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a precise lexical-semantic aligner. Answer directly with the JSON mapping; do NOT show chain-of-thought reasoning. Respond ONLY with JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=8192,
        timeout=180,
    )
    raw = resp.choices[0].message.content or ""
    # strip think tags / fences
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
            return json.loads(m.group())
        raise ValueError(f"Unparseable canonical response: {raw[:200]}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    glosses = collect_glosses()
    print(f"  Unique glosses: {len(glosses)}")
    if args.dry_run:
        return

    key = load_env_key()
    if not key:
        sys.exit("ERROR: OPENAI_API_KEY not found")
    from openai import OpenAI
    client = OpenAI(base_url=API_URL, api_key=key)

    mapping: Dict[str, str] = {}
    for i in range(0, len(glosses), CHUNK):
        chunk = glosses[i : i + CHUNK]
        print(f"  Chunk {i // CHUNK + 1}/{(len(glosses) - 1) // CHUNK + 1} ({len(chunk)} glosses)...", flush=True)
        for attempt in range(3):
            try:
                part = call_canonical(client, chunk)
                missing = [g for g in chunk if g not in part]
                if missing:
                    print(f"    [WARN] {len(missing)} glosses not mapped by model, keeping self")
                    for g in missing:
                        part[g] = g
                mapping.update(part)
                break
            except Exception as e:
                if attempt < 2:
                    print(f"    [retry {attempt + 1}] {e}")
                    time.sleep(2)
                else:
                    print(f"    [FAIL] chunk {i // CHUNK + 1}: {e}")
                    for g in chunk:
                        mapping[g] = g

    out_dir = PROJECT_ROOT / "data" / "lds_c"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"gloss_clusters_{datetime.now().strftime('%Y%m%d')}.json"
    out_path.write_text(json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")

    # stats
    clusters = Counter(mapping.values())
    multi = {k: v for k, v in clusters.items() if v > 1}
    print(f"\n  Mapped {len(mapping)} glosses -> {len(clusters)} canonical clusters")
    print(f"  Multi-member clusters: {len(multi)}")
    for canon, cnt in sorted(multi.items(), key=lambda x: -x[1])[:15]:
        members = [g for g, c in mapping.items() if c == canon]
        print(f"    [{canon}] ({cnt}) <- {members[:6]}")
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()
