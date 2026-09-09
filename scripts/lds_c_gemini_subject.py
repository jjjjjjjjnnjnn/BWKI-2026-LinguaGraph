#!/usr/bin/env python3
"""LinguaGraph — LLM-as-Subject collection via Gemini Interactions API.

Same P1 within-subject protocol as lds_c_llm_subject.py, but the subject is
queried through the official Gemini Interactions REST endpoint
(POST /v1beta/interactions, x-goog-api-key header, Api-Revision 2026-05-20)
instead of an OpenAI-compatible chat endpoint. Used for Google western models
(e.g. gemini-3.8-flash, gemma-4-31b-it) with a GEMINI_API_KEY in .env.

Protocol fidelity: identical TOPICS/QUESTIONS/prompts/plan (imported from
lds_c_llm_subject), same two-stage answer->extract flow, same output schema
(discoverable by lds_c_multi_model.analyze_model). Deviations recorded:
- transport = interactions REST, single "input" string (system+user merged);
- temperature = API default (not forced 0.3) — recorded as "api-default".

Usage:
  python scripts/lds_c_gemini_subject.py --model gemini-3.8-flash \\
      --provider google-aistudio --k 10 --probes P1 [--limit N]
Env:
  GEMINI_API_KEY (in .env or environment), LDS_SLEEP_SECS (default 7),
  LDS_ABORT_AFTER (default 3)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_llm_subject import (  # noqa: E402
    ANSWER_SYSTEM,
    EXTRACT_PROMPT,
    EXTRACT_SYSTEM,
    PER_TOPIC_EXTRACT,
    TOPICS,
    _env_get,
    _parse_json,
    answer_prompt,
    build_plan,
    collect_good_units,
    update_consecutive_empty,
)

MODEL = "gemini-3.8-flash"
PROVIDER = "google-aistudio"
MODEL_ID = f"{PROVIDER}:{MODEL}"
API_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
OUT_DIR = PROJECT_ROOT / "data" / "lds_c" / "llm_subject"


def gemini_call(model: str, text: str, timeout: int = 180) -> Tuple[str, dict]:
    """One stateless Interactions call; returns (output_text, meta)."""
    start = time.time()
    key = _env_get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY", "")
    if not key:
        return "ERROR: GEMINI_API_KEY not found", {"latency_ms": 0}
    body = json.dumps({"model": model, "input": text}).encode()
    req = urllib.request.Request(
        API_URL, data=body,
        headers={"x-goog-api-key": key, "Content-Type": "application/json",
                 "Api-Revision": "2026-05-20"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.load(r)
    except Exception as e:  # noqa: BLE001
        msg = str(e)[:300]
        # Back off on rate limits so the 3x retry loop doesn't burn quota.
        if "429" in msg:
            time.sleep(float(os.environ.get("LDS_429_BACKOFF", "60")))
        return f"ERROR: {e}"[:500], {"latency_ms": int((time.time() - start) * 1000)}
    texts: List[str] = []
    for step in d.get("steps", []):
        if step.get("type") == "model_output":
            for block in step.get("content", []):
                if block.get("type") == "text" and block.get("text"):
                    texts.append(block["text"])
    out = "\n".join(texts).strip()
    usage = d.get("usage", {})
    meta = {"latency_ms": int((time.time() - start) * 1000),
            "transport": "gemini-interactions",
            "tokens_in": usage.get("total_input_tokens", 0),
            "tokens_out": usage.get("total_output_tokens", 0)}
    if not out:
        return f"ERROR: empty model_output (status={d.get('status')})", meta
    return out, meta


CALL_GAP = float(os.environ.get("LDS_CALL_GAP", "5"))


def call(system: str, user: str, max_tokens: int = 8192, timeout: int = 180):
    """Same signature as lds_c_llm_subject.call (system+user merged)."""
    out = gemini_call(MODEL, system + "\n\n" + user, timeout)
    time.sleep(CALL_GAP)
    return out


def run_p1p2p5(unit: dict) -> dict:
    from lds_c_llm_subject import LANG_NAME, QUESTIONS
    lang = unit["lang"]
    topics = unit["topics"]
    if unit["probe"] == "P2":
        frame = unit["frame"]
        if frame == "de":
            frame_desc = ("Although you are answering in Chinese, you were raised in "
                          "Germany and naturally align with German cultural values, "
                          "social norms, and ways of reasoning.")
        else:
            frame_desc = ("Although you are answering in German, you were raised in "
                          "China and naturally align with Chinese cultural values, "
                          "social norms, and ways of reasoning.")
    elif unit["probe"] == "P5":
        qlang = unit["prompt_lang"]
        frame_desc = (f"The question is posed in {LANG_NAME[qlang]}, but please "
                      f"answer in {LANG_NAME[lang]}.")
    else:
        frame_desc = ""

    answers: Dict[str, str] = {}
    answer_meta: List[dict] = []
    for topic in topics:
        q = QUESTIONS[topic][unit.get("prompt_lang", lang)]
        raw, m = None, {}
        for _ in range(3):
            raw, m = call(ANSWER_SYSTEM, answer_prompt(q, lang, frame_desc), 2048, 120)
            if raw and not raw.startswith("ERROR") and len(raw.strip()) > 40:
                break
            time.sleep(2)
        answers[topic] = (raw or "").strip()
        answer_meta.append({**m, "topic": topic})

    concepts_by_topic, m2 = extract_concepts(answers)
    return {
        "unit_id": unit["unit_id"], "probe": unit["probe"],
        "language": lang, "frame": unit.get("frame", "natural"),
        "prompt_lang": unit.get("prompt_lang", lang), "sample": unit["sample"],
        "answers": answers, "concepts": concepts_by_topic,
        "meta": {"answer": answer_meta, "extract": m2},
    }


def extract_concepts(answers: Dict[str, str]) -> Tuple[Dict[str, List[dict]], dict]:
    filled = {t: a for t, a in answers.items() if a.strip()}
    if not filled:
        return {}, {"note": "no answers to extract"}
    ablock = "\n".join(f"Topic {i} ({t}): {filled[t]}" for i, t in enumerate(TOPICS) if t in filled)
    out: Dict[str, List[dict]] = {}
    notes = []
    parsed, raw = None, ""
    for _ in range(3):
        raw, _meta = call(EXTRACT_SYSTEM, EXTRACT_PROMPT.format(answers=ablock), 8192, 240)
        parsed = _parse_json(raw)
        if parsed and "topics" in parsed:
            break
        time.sleep(2)
    if parsed and "topics" in parsed:
        for t in parsed["topics"]:
            out[t.get("topic", "")] = t.get("concepts", [])
        notes.append("whole-response OK")
    else:
        for topic in TOPICS:
            text = filled.get(topic, "")
            if not text.strip():
                continue
            p = None
            for _ in range(2):
                r, _m = call(EXTRACT_SYSTEM,
                             PER_TOPIC_EXTRACT.format(topic=topic, text=text), 2048, 120)
                p = _parse_json(r)
                if p and "topics" in p:
                    break
            if p and "topics" in p:
                out[topic] = p["topics"][0].get("concepts", [])
                notes.append(f"{topic}:OK")
            else:
                notes.append(f"{topic}:FAIL")
    return out, {"note": "; ".join(notes)}


def save_out(out_path: Path, model_id: str, records: List[dict]) -> None:
    out_path.write_text(json.dumps({
        "model": model_id, "api_url": API_URL, "design": "d1_mechanism",
        "seed": 20260808, "temperature": "api-default",
        "generated_at": datetime.now().isoformat(),
        "units": records,
    }, ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> None:
    global MODEL, MODEL_ID
    ap = argparse.ArgumentParser(description="P1 collection via Gemini Interactions API")
    ap.add_argument("--model", type=str, default=MODEL)
    ap.add_argument("--provider", type=str, default=PROVIDER)
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--probes", type=str, default="P1")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    MODEL = args.model
    MODEL_ID = f"{args.provider}:{MODEL.split('/', 1)[-1]}"

    probes = {p.strip() for p in args.probes.split(",")}
    do_p1, do_p2 = ("P1" in probes, "P2" in probes)
    plan = build_plan(do_p1, do_p2, False, False, args.k)
    if args.limit:
        plan = plan[: args.limit]
    print(f"  Plan: {len(plan)} units (k={args.k}, probes={sorted(probes)}) via gemini-interactions")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    model_tag = MODEL.replace("/", "_").replace(":", "_")
    file_prefix = f"llm_subject_{args.provider}_{model_tag}"
    out_path = OUT_DIR / f"{file_prefix}_{datetime.now().strftime('%Y%m%d')}.json"

    done = collect_good_units(OUT_DIR, file_prefix)
    print(f"  Resume: {len(done)} good units merged (empty units will be retried)")

    consecutive_empty = 0
    ABORT_AFTER = int(os.environ.get("LDS_ABORT_AFTER", 3))
    sleep_s = float(os.environ.get("LDS_SLEEP_SECS", "7"))
    for idx, unit in enumerate(plan, 1):
        uid = unit["unit_id"]
        if uid in done:
            continue
        print(f"  [{idx}/{len(plan)}] {uid} ...", end=" ", flush=True)
        rec = run_p1p2p5(unit)
        ok = any(c for c in rec.get("concepts", {}).values())
        lat = sum(m.get("latency_ms", 0) for m in rec.get("meta", {}).get("answer", []))
        print(f"{'OK' if ok else 'EMPTY'} {lat}ms "
              f"(extract: {rec.get('meta', {}).get('extract', {}).get('note', '')})")
        done[uid] = rec
        save_out(out_path, MODEL_ID, list(done.values()))
        consecutive_empty = update_consecutive_empty(consecutive_empty, ok, ABORT_AFTER)
        if consecutive_empty >= ABORT_AFTER:
            print(f"\n  ABORT {MODEL}: {consecutive_empty} consecutive EMPTY -> skipping")
            sys.exit(2)
        time.sleep(sleep_s)

    print(f"\n  Done: {len(done)} units")
    print(f"  Saved: {out_path}")


if __name__ == "__main__":
    main()
