#!/usr/bin/env python3
"""
LinguaGraph — LDS-C Concept Extraction (deepseek-v4-flash via opencode GO)

Reads eligible responses from the freeze SSOT (eligible.csv), extracts
per-topic concepts with English glosses from the LLM, saves to
data/lds_c/extractions_<date>.json with full provenance.

Design (A1 of restart_plan.md):
  - Per-response, per-topic extraction (5 topics: Freiheit, Gerechtigkeit,
    Verantwortung, Heimat, Erfolg).
  - Each concept carries an English gloss for cross-language alignment
    (avoids a separate translation step; aligns by normalized gloss).
  - One API call per response (all 5 topics in one structured prompt).

Endpoint: opencode GO (OpenAI-compatible), model deepseek-v4-flash.
API key: read from gitignored .env (OPENAI_API_KEY).

Usage:
    python scripts/lds_c_extract.py --limit 3          # pilot 3 responses
    python scripts/lds_c_extract.py --dry-run          # show what would run
    python scripts/lds_c_extract.py                    # all eligible responses

Output: data/lds_c/extractions_YYYYMMDD.json
"""

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ── Canonical topic labels (topicIdx order, frozen) ──────────
TOPICS = ["Freiheit", "Gerechtigkeit", "Verantwortung", "Heimat", "Erfolg"]

API_URL = "https://opencode.ai/zen/go/v1"
MODEL = "deepseek-v4-flash"
FREEZE_TAGS = ["freeze_survey_20260703", "freeze_survey_20260712"]
OUT_DIR = PROJECT_ROOT / "data" / "lds_c"

# Language-specific system prompt for extraction quality
SYSTEM_PROMPT = (
    "You are a precise cognitive-linguistics concept extractor. "
    "Extract only meaningful CONTENT concepts: nouns and noun phrases that "
    "carry conceptual weight (e.g. 'freedom', 'boundaries', 'family duty'). "
    "REJECT function words, particles, pronouns, fillers, and grammatical "
    "fragments (e.g. 'something', 'within', 'being able to'). "
    "Respond ONLY with valid JSON, no explanation, no markdown fences."
)

EXTRACTION_PROMPT = """For each of the {n} topics below, extract the 5-6 most important CONCEPTS the person uses to explain that topic. Include each concept in its ORIGINAL language, an English gloss for cross-language alignment, and a 0-1 importance weight.

Be concise: do NOT add reasoning or commentary. Return ONLY compact valid JSON with no trailing commas:
{{"topics":[{{"topic":"<label>","concepts":[{{"concept":"<original>","en":"<gloss>","importance":0.9}}]}}]}}

Person's answers:
{answers}
"""


def load_env_key() -> str:
    """Load OPENAI_API_KEY from gitignored .env."""
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                if k.strip() == "OPENAI_API_KEY":
                    return v.strip()
    return os.environ.get("OPENAI_API_KEY", "")


def load_eligible(tags: List[str]) -> List[dict]:
    """Load eligible records from freeze eligible.csv files (q1-q5 order is canonical)."""
    import csv

    records = []
    for tag in tags:
        path = PROJECT_ROOT / "freeze" / tag / "eligible.csv"
        if not path.exists():
            print(f"  [WARN] freeze not found: {path}")
            continue
        for row in csv.DictReader(path.open(encoding="utf-8")):
            answers = {TOPICS[i]: (row.get(f"q{i+1}", "") or "").strip()
                       for i in range(5)}
            records.append({
                "response_id": row["response_id"],
                "language": row["language"],
                "answers": answers,
            })
    return records


def build_answers_block(answers: Dict[str, str]) -> str:
    """Build the per-topic answer block for the prompt."""
    lines = []
    for i, topic in enumerate(TOPICS, 1):
        text = answers.get(topic, "") or ""
        lines.append(f"Topic {i} ({topic}): {text}")
    return "\n".join(lines)


def _parse_json(raw: str) -> Optional[dict]:
    """Robustly parse JSON from LLM output (strip think tags/fences)."""
    cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL)
    cleaned = cleaned.strip()
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


def call_extract(client, answers_block: str, n_topics: int) -> Tuple[Optional[dict], Optional[str], Dict]:
    """Call the LLM. Returns (parsed_topics, raw_text, meta)."""
    start = time.time()
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": EXTRACTION_PROMPT.format(n=n_topics, answers=answers_block)},
            ],
            temperature=0.3,
            max_tokens=8192,
            timeout=180,
        )
        raw = resp.choices[0].message.content or ""
        elapsed_ms = int((time.time() - start) * 1000)
        parsed = _parse_json(raw)
        meta = {
            "latency_ms": elapsed_ms,
            "tokens_in": resp.usage.prompt_tokens if resp.usage else 0,
            "tokens_out": resp.usage.completion_tokens if resp.usage else 0,
        }
        return parsed, raw, meta
    except Exception as e:
        return None, f"ERROR: {e}", {"latency_ms": int((time.time() - start) * 1000)}


PER_TOPIC_PROMPT = """Extract the 5-6 most important CONCEPTS this person uses to explain the topic "{topic}". Include each concept in its ORIGINAL language, an English gloss for cross-language alignment, and a 0-1 importance weight.

Be concise: do NOT add reasoning or commentary. Return ONLY compact valid JSON with no trailing commas:
{{"topics":[{{"topic":"{topic}","concepts":[{{"concept":"<original>","en":"<gloss>","importance":0.9}}]}}]}}

The person's answer on {topic}:
{text}
"""


def call_extract_per_topic(client, topic: str, text: str) -> Tuple[Optional[dict], Optional[str], Dict]:
    """Extract concepts for ONE topic in a small, reliable call."""
    start = time.time()
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": PER_TOPIC_PROMPT.format(topic=topic, text=text)},
            ],
            temperature=0.3,
            max_tokens=2048,
            timeout=90,
        )
        raw = resp.choices[0].message.content or ""
        elapsed_ms = int((time.time() - start) * 1000)
        parsed = _parse_json(raw)
        meta = {
            "latency_ms": elapsed_ms,
            "tokens_in": resp.usage.prompt_tokens if resp.usage else 0,
            "tokens_out": resp.usage.completion_tokens if resp.usage else 0,
        }
        return parsed, raw, meta
    except Exception as e:
        return None, f"ERROR: {e}", {"latency_ms": int((time.time() - start) * 1000)}


def extract_per_topic_fallback(client, answers: Dict[str, str]) -> Tuple[List[dict], str]:
    """Per-topic extraction fallback for responses that fail whole-response calls.
    Returns (topics_out, notes)."""
    topics_out = []
    notes = []
    for topic in TOPICS:
        text = answers.get(topic, "") or ""
        if not text.strip():
            continue
        parsed, raw, meta = None, "", {}
        for attempt in range(2):
            parsed, raw, meta = call_extract_per_topic(client, topic, text)
            if parsed and "topics" in parsed:
                break
        if parsed and "topics" in parsed:
            topics_out.extend(parsed["topics"])
            notes.append(f"{topic}:OK({meta['latency_ms']}ms)")
        else:
            notes.append(f"{topic}:FAIL")
    return topics_out, "; ".join(notes)


def main() -> None:
    ap = argparse.ArgumentParser(description="LDS-C concept extraction via opencode GO")
    ap.add_argument("--limit", type=int, default=None, help="Max responses to process (pilot)")
    ap.add_argument("--dry-run", action="store_true", help="Show what would run, don't call API")
    ap.add_argument("--out", type=str, default=None, help="Output filename override")
    args = ap.parse_args()

    key = load_env_key()
    if not key:
        print("ERROR: OPENAI_API_KEY not found in .env or env")
        sys.exit(1)

    records = load_eligible(FREEZE_TAGS)
    if args.limit:
        records = records[: args.limit]

    print(f"  Eligible responses: {len(records)}")
    print(f"  Model: {MODEL} @ {API_URL}")
    print(f"  Dry run: {args.dry_run}")

    if args.dry_run:
        for r in records:
            n_topics = sum(1 for t in TOPICS if r["answers"].get(t))
            print(f"    {r['response_id']} ({r['language']}), {n_topics} topics")
        return

    from openai import OpenAI
    client = OpenAI(base_url=API_URL, api_key=key)

    out_dir = OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    out_path = out_dir / (args.out or f"extractions_{date_str}.json")

    # Resume: merge existing successful responses so re-runs never lose data
    all_results: Dict[str, dict] = {}
    done_ids: set = set()
    if out_path.exists():
        try:
            prev = json.loads(out_path.read_text(encoding="utf-8"))
            for r in prev.get("responses", []):
                if r.get("topics"):
                    all_results[r["response_id"]] = r
            done_ids = set(all_results.keys())
            print(f"  Resuming: {len(done_ids)} already extracted successfully; "
                  f"{len(prev.get('responses', [])) - len(done_ids)} failed will retry")
        except json.JSONDecodeError:
            print("  [WARN] existing output unreadable, starting fresh")

    results = []
    n_topics_total = len(TOPICS)
    t0 = time.time()
    for idx, rec in enumerate(records, 1):
        rid = rec["response_id"]
        if rid in done_ids:
            print(f"  [{idx}/{len(records)}] {rid} skip (done)")
            continue
        answers_block = build_answers_block(rec["answers"])
        print(f"  [{idx}/{len(records)}] {rid} ({rec['language']})...", end=" ", flush=True)
        parsed, raw, meta = None, "", {}
        for attempt in range(3):
            parsed, raw, meta = call_extract(client, answers_block, n_topics_total)
            truncated = meta.get("tokens_out", 0) >= 8000
            if parsed and "topics" in parsed and not truncated:
                break
            if attempt < 2:
                print(f"[retry{attempt + 1}]", end=" ", flush=True)
                time.sleep(1.5)
        if parsed and "topics" in parsed:
            topics_out = parsed["topics"]
            n_conc = sum(len(t.get("concepts", [])) for t in topics_out)
            print(f"OK {n_conc} concepts ({meta['latency_ms']}ms)")
            raw_used = raw
            meta_used = meta
        else:
            # Fallback: per-topic extraction for stubborn responses
            print(f"[per-topic] ", end="", flush=True)
            topics_out, notes = extract_per_topic_fallback(client, rec["answers"])
            n_conc = sum(len(t.get("concepts", [])) for t in topics_out)
            print(f"{'OK' if topics_out else 'FAIL'} {n_conc} concepts ({notes})")
            raw_used = raw or notes
            meta_used = {**meta, "note": notes}
        all_results[rid] = {
            "response_id": rid,
            "language": rec["language"],
            "topics": topics_out,
            "raw": raw_used,
            "meta": meta_used,
        }
        results.append(rid)
        # Incremental save for resume safety (merged full set)
        out_path.write_text(json.dumps({
            "model": MODEL,
            "api_url": API_URL,
            "prompt_version": "v1",
            "extracted_at": datetime.now().isoformat(),
            "responses": list(all_results.values()),
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        time.sleep(0.3)

    elapsed = time.time() - t0
    print(f"\n  Done: {len(results)} processed in {elapsed:.0f}s")
    print(f"  Total in output: {len(all_results)}")
    print(f"  Saved: {out_path}")


if __name__ == "__main__":
    main()
