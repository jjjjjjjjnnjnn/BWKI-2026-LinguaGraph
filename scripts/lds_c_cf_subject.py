#!/usr/bin/env python3
"""LinguaGraph — LLM-as-Subject collection via Cloudflare Workers AI.

Same P1 within-subject protocol as lds_c_llm_subject.py, but the subject is
queried through Cloudflare Workers AI
(POST /client/v4/accounts/{id}/ai/run/{model}) instead of an
OpenAI-compatible chat endpoint. Used for western models hosted on CF
(e.g. @cf/meta/llama-3.3-70b-instruct-fp8-fast,
@cf/mistralai/mistral-small-3.1-24b-instruct, @cf/openai/gpt-oss-20b).

Protocol fidelity: identical TOPICS/QUESTIONS/prompts/plan (imported from
lds_c_llm_subject), same two-stage answer->extract flow, same output schema
(discoverable by lds_c_multi_model.analyze_model). Deviations recorded:
- transport = workers-ai REST, OpenAI-style messages array;
- temperature = API default — recorded as "api-default".

Usage:
  python scripts/lds_c_cf_subject.py --model @cf/meta/llama-3.3-70b-instruct-fp8-fast \\
      --provider cloudflare --k 10 --probes P1 [--limit N]
Env:
  CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID (in .env),
  LDS_SLEEP_SECS (default 10), LDS_CALL_GAP (default 4),
  LDS_ABORT_AFTER (default 3)
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
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

MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
PROVIDER = "cloudflare"
MODEL_ID = f"{PROVIDER}:{MODEL}"
OUT_DIR = PROJECT_ROOT / "data" / "lds_c" / "llm_subject"


def cf_chat(model: str, system: str, user: str, timeout: int = 240,
            max_tokens: int = 2048) -> Tuple[str, dict]:
    """One Workers AI call; returns (response_text, meta)."""
    start = time.time()
    tok = _env_get("CLOUDFLARE_API_TOKEN")
    acct = _env_get("CLOUDFLARE_ACCOUNT_ID")
    if not tok or not acct:
        return "ERROR: CLOUDFLARE_API_TOKEN/ACCOUNT_ID missing", {"latency_ms": 0}
    body = json.dumps({"messages": [{"role": "system", "content": system},
                                    {"role": "user", "content": user}],
                       "max_tokens": max_tokens}).encode()
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{acct}/ai/run/{model}",
        data=body,
        headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.load(r)
    except Exception as e:  # noqa: BLE001
        return f"ERROR: {e}"[:500], {"latency_ms": int((time.time() - start) * 1000)}
    if not d.get("success"):
        return f"ERROR: {json.dumps(d.get('errors'))[:300]}", {
            "latency_ms": int((time.time() - start) * 1000)}
    out = str((d.get("result") or {}).get("response", "") or "").strip()
    meta = {"latency_ms": int((time.time() - start) * 1000),
            "transport": "cloudflare-workers-ai"}
    if not out:
        return "ERROR: empty response", meta
    return out, meta


CALL_GAP = float(os.environ.get("LDS_CALL_GAP", "4"))


def call(system: str, user: str, max_tokens: int = 8192, timeout: int = 180):
    """Same signature as lds_c_llm_subject.call."""
    out = cf_chat(MODEL, system, user, max(240, timeout),
                  min(max_tokens, 4096))
    time.sleep(CALL_GAP)
    return out


def parse_lenient(raw: str):
    """CF-driver-local tolerant JSON parse (frozen _parse_json untouched).

    Some CF-hosted models return single-quoted pseudo-JSON. Try strict first,
    then ast.literal_eval on the largest {...} span (safe: no code execution).
    """
    p = _parse_json(raw)
    if p and "topics" in p:
        return p
    m = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if not m:
        return None
    try:
        p2 = ast.literal_eval(m.group())
        if isinstance(p2, dict) and "topics" in p2:
            return p2
    except (SyntaxError, ValueError):
        return None
    return None


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
            time.sleep(3)
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


JSON_STRICT_SUFFIX = "\nIMPORTANT: Use DOUBLE quotes for all JSON strings and keys."


def extract_concepts(answers: Dict[str, str]) -> Tuple[Dict[str, List[dict]], dict]:
    filled = {t: a for t, a in answers.items() if a.strip()}
    if not filled:
        return {}, {"note": "no answers to extract"}
    ablock = "\n".join(f"Topic {i} ({t}): {filled[t]}" for i, t in enumerate(TOPICS) if t in filled)
    out: Dict[str, List[dict]] = {}
    notes = []
    parsed, raw = None, ""
    for _ in range(3):
        raw, _meta = call(EXTRACT_SYSTEM, EXTRACT_PROMPT.format(answers=ablock) + JSON_STRICT_SUFFIX, 8192, 240)
        parsed = parse_lenient(raw)
        if parsed and "topics" in parsed:
            break
        time.sleep(3)
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
                             PER_TOPIC_EXTRACT.format(topic=topic, text=text) + JSON_STRICT_SUFFIX, 2048, 120)
                p = parse_lenient(r)
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
        "model": model_id,
        "api_url": "https://api.cloudflare.com/client/v4/accounts/{id}/ai/run/",
        "design": "d1_mechanism", "seed": 20260808, "temperature": "api-default",
        "generated_at": datetime.now().isoformat(),
        "units": records,
    }, ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> None:
    global MODEL, MODEL_ID
    ap = argparse.ArgumentParser(description="P1 collection via Cloudflare Workers AI")
    ap.add_argument("--model", type=str, default=MODEL)
    ap.add_argument("--provider", type=str, default=PROVIDER)
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--probes", type=str, default="P1")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    MODEL = args.model
    MODEL_ID = f"{args.provider}:{MODEL}"

    probes = {p.strip() for p in args.probes.split(",")}
    do_p1, do_p2 = ("P1" in probes, "P2" in probes)
    plan = build_plan(do_p1, do_p2, False, False, args.k)
    if args.limit:
        plan = plan[: args.limit]
    print(f"  Plan: {len(plan)} units (k={args.k}, probes={sorted(probes)}) via cloudflare")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    model_tag = MODEL.replace("/", "_").replace(":", "_").replace("@", "").replace(".", "_")
    file_prefix = f"llm_subject_{args.provider}_{model_tag}"
    out_path = OUT_DIR / f"{file_prefix}_{datetime.now().strftime('%Y%m%d')}.json"

    done = collect_good_units(OUT_DIR, file_prefix)
    print(f"  Resume: {len(done)} good units merged (empty units will be retried)")

    consecutive_empty = 0
    ABORT_AFTER = int(os.environ.get("LDS_ABORT_AFTER", 3))
    sleep_s = float(os.environ.get("LDS_SLEEP_SECS", "10"))
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
