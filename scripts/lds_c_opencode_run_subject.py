#!/usr/bin/env python3
"""LinguaGraph — LLM-as-Subject collection via `opencode run` (terminal models).

Same P1 within-subject protocol as lds_c_llm_subject.py, but the subject is
queried through the local opencode terminal (`opencode run -m provider/model`)
instead of an OpenAI-compatible HTTP endpoint. Used for models only reachable
via the terminal (e.g. opencode-go/grok-4.6, gpt-5.6-luna, muse-spark-*).

Protocol fidelity: identical TOPICS/QUESTIONS/prompts/plan (imported from
lds_c_llm_subject), same two-stage answer->extract flow, same output schema
(discoverable by lds_c_multi_model + analyze_model). Deviations recorded in
meta: temperature is the terminal default (not forced 0.3); transport is
`opencode run` subprocess (fresh session per call, no context accumulation).

Cost note: each call bills to the operator's opencode account (~$0.001-0.02
after prompt caching). P1/k=10 = 30 units x ~2 calls = ~60 calls/model.

Usage:
  python scripts/lds_c_opencode_run_subject.py --model opencode-go/grok-4.6 \\
      --provider opencode-go --k 10 --probes P1 [--limit N]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_llm_subject import (  # noqa: E402
    ANSWER_SYSTEM,
    EXTRACT_PROMPT,
    EXTRACT_SYSTEM,
    PER_TOPIC_EXTRACT,
    RANDOM_SEED,
    TOPICS,
    _parse_json,
    answer_prompt,
    build_plan,
    collect_good_units,
    save_out,
    update_consecutive_empty,
)

MODEL = "opencode-go/grok-4.6"
PROVIDER = "opencode-go"
MODEL_ID = f"{PROVIDER}:{MODEL.split('/', 1)[-1]}"
OUT_DIR = PROJECT_ROOT / "data" / "lds_c" / "llm_subject"
PROBE_DIR = Path(os.environ.get("OPENCODE_PROBE_DIR",
                               "C:/Users/rongj/AppData/Local/Temp/opencode/probe"))
CALL_TIMEOUT = int(os.environ.get("OPENCODE_CALL_TIMEOUT", "300"))
OPENCODE_BIN = os.environ.get(
    "OPENCODE_BIN",
    r"C:\Users\rongj\AppData\Roaming\npm\node_modules\opencode-ai\bin\opencode.exe",
)


def opencode_call(model: str, message: str) -> Tuple[str, dict]:
    """One fresh `opencode run` session; returns (text, meta)."""
    start = time.time()
    cmd = [OPENCODE_BIN, "run", "-m", model, "--format", "json",
           "--dir", str(PROBE_DIR), message]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace",
                              timeout=CALL_TIMEOUT)
    except subprocess.TimeoutExpired:
        return "ERROR: opencode run timeout", {"latency_ms": int((time.time() - start) * 1000)}
    except Exception as e:  # noqa: BLE001
        return f"ERROR: {e}", {"latency_ms": int((time.time() - start) * 1000)}
    if proc.returncode != 0 and not proc.stdout.strip():
        return f"ERROR: exit={proc.returncode} {proc.stderr[-300:]}", {
            "latency_ms": int((time.time() - start) * 1000)}
    texts, cost = [], 0.0
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "text":
            t = ev.get("part", {}).get("text", "")
            if t:
                texts.append(t)
        if ev.get("type") == "step_finish":
            try:
                cost += float(ev.get("part", {}).get("cost", 0) or 0)
            except (TypeError, ValueError):
                pass
    text = "\n".join(texts).strip()
    if not text:
        return f"ERROR: empty text (exit={proc.returncode})", {
            "latency_ms": int((time.time() - start) * 1000)}
    return text, {"latency_ms": int((time.time() - start) * 1000),
                  "transport": "opencode-run", "cost_usd": round(cost, 6)}


def call(system: str, user: str, max_tokens: int = 8192, timeout: int = 180):
    """Same signature as lds_c_llm_subject.call (system+user merged)."""
    return opencode_call(MODEL, system + "\n\n" + user)


def run_p1p2p5(unit: dict) -> dict:
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
        from lds_c_llm_subject import LANG_NAME
        qlang = unit["prompt_lang"]
        frame_desc = (f"The question is posed in {LANG_NAME[qlang]}, but please "
                      f"answer in {LANG_NAME[lang]}.")
    else:
        frame_desc = ""

    from lds_c_llm_subject import QUESTIONS
    answers: Dict[str, str] = {}
    answer_meta: List[dict] = []
    for topic in topics:
        q = QUESTIONS[topic][unit.get("prompt_lang", lang)]
        raw, m = None, {}
        for _ in range(3):
            raw, m = call(ANSWER_SYSTEM, answer_prompt(q, lang, frame_desc), 2048, 120)
            if raw and not raw.startswith("ERROR") and len(raw.strip()) > 40:
                break
            time.sleep(1.2)
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
    from lds_c_llm_subject import QUESTIONS  # noqa: F401
    filled = {t: a for t, a in answers.items() if a.strip()}
    if not filled:
        return {}, {"note": "no answers to extract"}
    ablock = "\n".join(f"Topic {i} ({t}): {filled[t]}" for i, t in enumerate(TOPICS) if t in filled)
    out: Dict[str, List[dict]] = {}
    notes = []
    parsed, raw, meta = None, "", {}
    for _ in range(3):
        raw, meta = call(EXTRACT_SYSTEM, EXTRACT_PROMPT.format(answers=ablock), 8192, 240)
        parsed = _parse_json(raw)
        if parsed and "topics" in parsed:
            break
        time.sleep(1.5)
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


def main() -> None:
    global MODEL, MODEL_ID
    ap = argparse.ArgumentParser(description="P1 collection via `opencode run`")
    ap.add_argument("--model", type=str, default=MODEL)
    ap.add_argument("--provider", type=str, default=PROVIDER)
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--probes", type=str, default="P1")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    MODEL = args.model
    MODEL_ID = f"{args.provider}:{MODEL.split('/', 1)[-1]}"

    probes = {p.strip() for p in args.probes.split(",")}
    do_p1, do_p2, do_p3, do_p5 = ("P1" in probes, "P2" in probes,
                                  "P3" in probes, "P5" in probes)
    if do_p3 or do_p5 or do_p2:
        print("NOTE: this driver implements P1/P2 answer+extract; P3/P5 unsupported")
    plan = build_plan(do_p1, do_p2, False, False, args.k)
    if args.limit:
        plan = plan[: args.limit]
    print(f"  Plan: {len(plan)} units (k={args.k}, probes={sorted(probes)}) via opencode run")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    model_tag = MODEL.replace("/", "_").replace(":", "_")
    file_prefix = f"llm_subject_{args.provider}_{model_tag}"
    out_path = OUT_DIR / f"{file_prefix}_{datetime.now().strftime('%Y%m%d')}.json"

    import lds_c_llm_subject as S
    S.MODEL, S.MODEL_ID = MODEL, MODEL_ID
    done = collect_good_units(OUT_DIR, file_prefix)
    print(f"  Resume: {len(done)} good units merged (empty units will be retried)")

    total_cost = 0.0
    consecutive_empty = 0
    ABORT_AFTER = int(os.environ.get("LDS_ABORT_AFTER", 3))
    sleep_s = float(os.environ.get("LDS_SLEEP_SECS", "2"))
    for idx, unit in enumerate(plan, 1):
        uid = unit["unit_id"]
        if uid in done:
            continue
        print(f"  [{idx}/{len(plan)}] {uid} ...", end=" ", flush=True)
        rec = run_p1p2p5(unit)
        ok = any(c for c in rec.get("concepts", {}).values())
        lat = sum(m.get("latency_ms", 0) for m in rec.get("meta", {}).get("answer", []))
        total_cost += sum(m.get("cost_usd", 0) for m in rec.get("meta", {}).get("answer", []))
        print(f"{'OK' if ok else 'EMPTY'} {lat}ms "
              f"(extract: {rec.get('meta', {}).get('extract', {}).get('note', '')})")
        done[uid] = rec
        save_out(out_path, list(done.values()))
        consecutive_empty = update_consecutive_empty(consecutive_empty, ok, ABORT_AFTER)
        if consecutive_empty >= ABORT_AFTER:
            print(f"\n  ABORT {MODEL}: {consecutive_empty} consecutive EMPTY -> skipping")
            sys.exit(2)
        time.sleep(sleep_s)

    print(f"\n  Done: {len(done)} units, est. cost ${total_cost:.4f}")
    print(f"  Saved: {out_path}")


if __name__ == "__main__":
    main()
