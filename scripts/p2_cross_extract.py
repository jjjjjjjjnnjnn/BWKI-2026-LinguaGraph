#!/usr/bin/env python3
"""P2-3 (H3): cross-extraction sensitivity — is the divergence an extraction artifact?

The multi-model replication extracts each model's concepts with THE SAME model
as the subject. This rechecks whether the cross-language divergence survives an
INDEPENDENT extractor: we re-extract concepts from the BASELINE deepseek-v4-flash
P1 answers (data/lds_c/llm_subject/llm_subject_20260808.json) using qwen-max
(DashScope, a different model), then recompute LDS-C vs the within-language
floor.

If the divergence persists under cross-extraction, it is a property of the
ANSWERS (genuine), not of the subject model's self-extraction behavior.

Usage: python scripts/p2_cross_extract.py [--n-samples 6] [--extractor qwen-max]
Needs DASHSCOPE_API_KEY (free quota). Output: console table + JSON.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_llm_analyze import OUT_DIR as LLM_OUT, unit_to_record  # noqa: E402
from lds_c_design_effect import signal_table  # noqa: E402
from lds_c_llm_subject import EXTRACT_SYSTEM, EXTRACT_PROMPT  # noqa: E402

API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"


def load_baseline_answers(n_samples: int) -> dict:
    """lang -> sample -> {topic: answer_text}, from deepseek-v4-flash P1."""
    f = sorted(LLM_OUT.glob("llm_subject_*.json"))
    data = None
    for cand in f:
        d = json.loads(cand.read_text(encoding="utf-8"))
        if d.get("model") == "deepseek-v4-flash":
            data = d
            break
    if not data:
        raise RuntimeError("deepseek-v4-flash baseline file not found")
    out = {}
    for u in data["units"]:
        if u.get("probe") != "P1":
            continue
        lang = u["language"]
        out.setdefault(lang, {})[u["sample"]] = u.get("answers", {})
    # take first n_samples per language
    return {lang: dict(list(samples.items())[:n_samples]) for lang, samples in out.items()}


def cross_extract(client, model: str, answers: dict) -> dict:
    """Extract concepts from per-topic answers using an INDEPENDENT extractor."""
    filled = {t: a for t, a in answers.items() if a and not a.startswith("ERROR")}
    ablock = "\n".join(f"Topic {i} ({t}): {filled[t]}" for i, t in enumerate(filled))
    raw = None
    for _ in range(3):
        try:
            r = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": EXTRACT_SYSTEM},
                          {"role": "user", "content": EXTRACT_PROMPT.format(answers=ablock)}],
                temperature=0.1, max_tokens=2048, timeout=120)
            raw = r.choices[0].message.content or ""
            m = re.search(r"\{.*\}", raw, re.DOTALL)
            if not m:
                continue
            parsed = json.loads(m.group())
            topics = {}
            # format A: {"topics":[{"topic":..., "concepts":[...]}]}
            for t in parsed.get("topics", []):
                cs = t.get("concepts", [])
                if cs:
                    topics[t.get("topic", "")] = cs
            # format B: {"concepts":[{"concept"/"name","en"}...]} (single topic)
            if not topics and parsed.get("concepts"):
                cs = parsed["concepts"]
                if cs:
                    topics["ALL"] = cs
            if any(topics.values()):
                return topics
        except Exception:
            time.sleep(1.5)
    return {}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-samples", type=int, default=6)
    ap.add_argument("--extractor", type=str, default="qwen-max")
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    from openai import OpenAI
    from lds_c_llm_subject import load_key_for_url
    key = load_key_for_url(API_URL)
    client = OpenAI(base_url=API_URL, api_key=key)

    answers = load_baseline_answers(args.n_samples)
    print(f"  baseline answers: { {l: len(s) for l, s in answers.items()} } "
          f"per language, extractor={args.extractor}")

    # Cross-extract -> records
    records = []
    for lang, samples in answers.items():
        for sample, topic_answers in samples.items():
            concepts = cross_extract(client, args.extractor, topic_answers)
            records.append({
                "response_id": f"X{lang}_s{sample}", "language": lang,
                "probe": "P1", "topics": [{"topic": t, "concepts": c}
                                          for t, c in concepts.items()],
            })
    n_good = sum(1 for r in records if any(r.get("topics")))
    print(f"  cross-extracted: {n_good}/{len(records)} units with concepts")

    # Signal table on cross-extracted records
    sig = signal_table(records, tag=f"cross-{args.extractor}", n_floor=100)
    print("\n=== Cross-extracted LDS-C vs floor (ZH-DE focus) ===")
    for pair in ("ZH-EN", "DE-EN", "ZH-DE"):
        b = sig["by_pair"].get(pair)
        if b:
            print(f"  {pair}: LDS-C={b['lds_c']}  floor={b['split_half_floor']}  "
                  f"margin={b['signal_margin']}")

    # Reference: deepseek SELF-extracted baseline (from committed data)
    ref = {
        "ZH-EN": {"lds_c": 0.9552, "floor": 0.8745, "margin": 0.0807},
        "DE-EN": {"lds_c": 0.93, "floor": 0.8456, "margin": 0.0844},
        "ZH-DE": {"lds_c": 0.9446, "floor": 0.8618, "margin": 0.0828},
    }
    print("\n=== Reference: deepseek SELF-extracted (committed, k=10) ===")
    for pair in ("ZH-EN", "DE-EN", "ZH-DE"):
        r = ref[pair]
        print(f"  {pair}: LDS-C={r['lds_c']}  floor={r['floor']}  margin={r['margin']}")

    out = {"design": "cross_extraction_sensitivity",
           "extractor": args.extractor, "n_samples": args.n_samples,
           "cross": {p: sig["by_pair"].get(p) for p in ("ZH-EN", "DE-EN", "ZH-DE")},
           "self_reference": ref,
           "note": "If cross LDS-C >> cross floor (positive margin) similar to self, "
                   "the divergence is in the ANSWERS, not the subject's extraction."}
    out_path = PROJECT_ROOT / "data" / "lds_c" / "llm_subject" / (
        args.out or f"cross_extraction_{args.extractor}_{time.strftime('%Y%m%d')}.json")
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()
