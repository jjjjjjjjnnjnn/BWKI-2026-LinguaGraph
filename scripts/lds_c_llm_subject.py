#!/usr/bin/env python3
"""LinguaGraph — D1: LLM-as-Subject within-subject data collection.

Design (see docs/planning/d1_mechanism_design.md):
  Same model (deepseek-v4-flash) prompted in ZH/DE/EN on the same 5 social
  topics = within-subject by construction (identical weights, language varies).

Probes:
  P1  language main effect   : 3 langs x k=10 natural answers -> extract concepts
  P2  frame-code decoupling  : ZH-code+DE-frame / DE-code+ZH-frame (M3)
  P3  free association       : 3 langs x 5 topics x k=10 associations (M2)
  P5  answer-vs-prompt lang  : ZH question/DE answer etc. (M5)

Hygiene (true within-subject):
  - every call is an INDEPENDENT API request (no context accumulation)
  - topic order counterbalanced per sample
  - temperature 0.3 fixed (matches human pipeline)
  - k=10 resamples per condition (robust split-half floor: C(10,2)=45 pairs)

Two-stage for P1/P2/P5: (1) LLM answers the questions as a subject, (2) extract
concepts from that answer — mirroring the human pipeline exactly. P3 outputs
associations directly (no extraction stage).

Resume: incremental save keyed by unit_id; re-runs merge, never lose data.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

API_URL = "https://opencode.ai/zen/go/v1"
MODEL = "deepseek-v4-flash"
OUT_DIR = PROJECT_ROOT / "data" / "lds_c" / "llm_subject"
RANDOM_SEED = 20260808

# ── Canonical topics (frozen order) ────────────────────────────────
TOPICS = ["Freiheit", "Gerechtigkeit", "Verantwortung", "Heimat", "Erfolg"]

# ── Trilingual question stimuli (from data/questionnaires/form_questions.md) ──
# topic -> {lang: question text}. The actual survey questions per canonical topic:
QUESTIONS = {
    "Freiheit": {
        "zh": '请描述“自由”的边界在哪里。',
        "de": 'Beschreiben Sie, wo die Grenzen der „Freiheit“ liegen.',
        "en": 'Describe where the boundaries of "freedom" lie.',
    },
    "Gerechtigkeit": {
        "zh": '请描述“正义”对您意味着什么。',
        "de": 'Beschreiben Sie, was „Gerechtigkeit“ für Sie bedeutet.',
        "en": 'Describe what "justice" means to you.',
    },
    "Verantwortung": {
        "zh": '请描述“责任”和“自由”之间的关系。',
        "de": 'Beschreiben Sie die Beziehung zwischen „Verantwortung“ und „Freiheit“.',
        "en": 'Describe the relationship between "responsibility" and "freedom".',
    },
    "Heimat": {
        "zh": '“家”和“房子”有什么区别？',
        "de": 'Was ist der Unterschied zwischen „Zuhause“ und „Haus“?',
        "en": 'What is the difference between "home" and "house"?',
    },
    "Erfolg": {
        "zh": '请用3-5句话描述“成功”对您意味着什么。',
        "de": 'Beschreiben Sie in 3-5 Sätzen, was „Erfolg“ für Sie bedeutet.',
        "en": 'Describe in 3-5 sentences what "success" means to you.',
    },
}

LANG_NAME = {"zh": "Chinese", "de": "German", "en": "English"}
LANG_NATIVE = {
    "zh": "中文母语者（以中文思考和表达）",
    "de": "ein deutscher Muttersprachler (denkt und spricht auf Deutsch)",
    "en": "a native English speaker (thinks and speaks in English)",
}

# ── Answer-generation prompts (LLM as subject) ─────────────────────
ANSWER_SYSTEM = (
    "You are a participant in a study on language and thought. "
    "Answer the questions below as a natural person expressing your genuine "
    "thinking. Write 3-5 sentences per question. Do NOT mention that you are "
    "an AI model. Do NOT use markdown headers. Answer ONLY in the requested "
    "language."
)

def answer_prompt(question: str, answer_lang: str, frame_desc: str = "") -> str:
    """Build the user prompt for ONE topic's answer (per-topic, deepseek-safe).

    frame_desc optionally injects a cultural-frame instruction (P2).
    Per-topic calls are used because whole-response multi-item calls trigger
    deepseek-v4-flash reasoning explosion (documented pitfall).
    """
    frame_line = f"\n{frame_desc}" if frame_desc else ""
    return (
        f"You are {LANG_NATIVE.get(answer_lang, answer_lang)}.{frame_line}\n"
        f"Please answer the following question in {LANG_NAME[answer_lang]}, "
        f"3-5 sentences, as a natural person expressing your genuine thinking.\n\n"
        f"{question}"
    )

# ── Free-association prompt (P3) ────────────────────────────────────
ASSOC_SYSTEM = (
    "You are a participant in a word-association study. For each cue word, "
    "write the FIRST words that come to mind — spontaneous, not reasoned. "
    "No explanations, no full sentences. Only words."
)
ASSOC_PROMPT = (
    'Cue word: "{topic}" (in {lang_name}).\n'
    "Write the first 10 single words that come to mind when you see this cue. "
    'Return ONLY a JSON array of strings: ["w1","w2",...]'
)


def _env_get(name: str) -> str:
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                if k.strip() == name:
                    return v.strip()
    return os.environ.get(name, "")


def load_env_key() -> str:
    """Key for the classic paid gateway (zen/go)."""
    return _env_get("OPENAI_API_KEY")


def load_key_for_url(url: str) -> str:
    """Pick the API key by gateway: OpenRouter uses OPENROUTER_API_KEY,
    everything else (opencode zen) uses OPENAI_API_KEY."""
    if "openrouter" in url.lower():
        return _env_get("OPENROUTER_API_KEY")
    return _env_get("OPENAI_API_KEY")


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


def call(client, system: str, user: str, max_tokens: int = 8192, timeout: int = 180):
    """Single independent API call (fresh session, no context accumulation)."""
    start = time.time()
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            temperature=0.3,
            max_tokens=max_tokens,
            timeout=timeout,
        )
        raw = resp.choices[0].message.content or ""
        meta = {
            "latency_ms": int((time.time() - start) * 1000),
            "tokens_in": resp.usage.prompt_tokens if resp.usage else 0,
            "tokens_out": resp.usage.completion_tokens if resp.usage else 0,
            "finish": resp.choices[0].finish_reason if resp.choices else None,
        }
        return raw, meta
    except Exception as e:
        return f"ERROR: {e}", {"latency_ms": int((time.time() - start) * 1000)}


# ── Condition plan ──────────────────────────────────────────────────
def build_plan(do_p1=True, do_p2=True, do_p3=True, do_p5=True, k: int = 10) -> List[dict]:
    """Return the full unit plan: list of {probe, unit_id, ...} dicts."""
    rng = random.Random(RANDOM_SEED)
    plan: List[dict] = []

    def shuffled_topics():
        ts = TOPICS[:]
        rng.shuffle(ts)
        return ts

    if do_p1:
        for lang in ["zh", "de", "en"]:
            for s in range(k):
                plan.append({
                    "probe": "P1", "unit_id": f"P1_{lang}_s{s:02d}",
                    "lang": lang, "frame": "natural", "sample": s,
                    "topics": shuffled_topics(),
                })
    if do_p2:
        # cross conditions (natural diagonal reuses P1)
        for code, frame in [("zh", "de"), ("de", "zh")]:
            for s in range(k):
                plan.append({
                    "probe": "P2", "unit_id": f"P2_{code}code_{frame}frame_s{s:02d}",
                    "lang": code, "frame": frame, "sample": s,
                    "topics": shuffled_topics(),
                })
    if do_p3:
        for lang in ["zh", "de", "en"]:
            for topic in TOPICS:
                for s in range(k):
                    plan.append({
                        "probe": "P3", "unit_id": f"P3_{lang}_{topic}_s{s:02d}",
                        "lang": lang, "topic": topic, "sample": s,
                    })
    if do_p5:
        # answer-vs-prompt language decoupling (ZH focus pair)
        for prompt_lang, answer_lang in [("zh", "de"), ("de", "de")]:
            for s in range(k):
                plan.append({
                    "probe": "P5", "unit_id": f"P5_{prompt_lang}q_{answer_lang}a_s{s:02d}",
                    "lang": answer_lang, "prompt_lang": prompt_lang, "sample": s,
                    "topics": shuffled_topics(),
                })
    return plan


# ── Per-probe execution ─────────────────────────────────────────────
def build_questions_block(topics: List[str], lang: str) -> str:
    lines = []
    for i, t in enumerate(topics, 1):
        lines.append(f"Question {i}: {QUESTIONS[t][lang]}")
    return "\n".join(lines)


def run_p1p2p5(client, unit: dict) -> dict:
    """Two-stage, per-topic: LLM answers each question -> extract concepts.

    Per-topic answer generation avoids deepseek-v4-flash reasoning explosion
    on multi-item prompts (documented pitfall: whole-response calls burn the
    token budget on chain-of-thought, finish=length, empty content).
    """
    lang = unit["lang"]
    topics = unit["topics"]

    # Frame / prompt-language instruction (P2 / P5)
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

    # Stage 1: per-topic answer generation (5 small independent calls)
    answers: Dict[str, str] = {}
    answer_meta: List[dict] = []
    for topic in topics:
        q = QUESTIONS[topic][unit.get("prompt_lang", lang)]
        raw, m = None, {}
        for attempt in range(3):
            raw, m = call(client, ANSWER_SYSTEM, answer_prompt(q, lang, frame_desc),
                          2048, 120)
            if raw and not raw.startswith("ERROR") and len(raw.strip()) > 40:
                break
            time.sleep(1.2)
        answers[topic] = (raw or "").strip()
        answer_meta.append({**m, "topic": topic})

    # Stage 2: extract concepts from the generated answers (whole-response, per-topic fallback)
    concepts_by_topic, m2 = extract_concepts(client, answers)

    return {
        "unit_id": unit["unit_id"], "probe": unit["probe"],
        "language": lang, "frame": unit.get("frame", "natural"),
        "prompt_lang": unit.get("prompt_lang", lang), "sample": unit["sample"],
        "answers": answers, "concepts": concepts_by_topic,
        "meta": {"answer": answer_meta, "extract": m2},
    }


def _parse_answers(raw: str, topics: List[str]) -> Dict[str, str]:
    """Best-effort parse of the generated answer into per-topic text."""
    if raw.startswith("ERROR"):
        return {t: "" for t in topics}
    # naive: split on 'Question N:' markers if present, else keep raw under first topic
    out: Dict[str, str] = {t: "" for t in topics}
    segs = re.split(r"(?i)\b(?:question\s*)?(\d+)\s*[:.)]", raw)
    # if no numbered segments, put whole text on the first topic and try line split
    numbered = re.findall(r"(?i)\bquestion\s*(\d+)\s*[:.)]", raw)
    if len(numbered) >= 2:
        # segment by consecutive question markers
        parts = re.split(r"(?i)\bquestion\s*\d+\s*[:.)]", raw)
        for idx, t in enumerate(topics):
            out[t] = parts[idx + 1].strip() if idx + 1 < len(parts) else ""
    else:
        # fallback: whole text to first topic
        out[topics[0]] = raw.strip()
    return out


# ── Concept extraction (reuse lds_c_extract logic) ─────────────────
EXTRACT_SYSTEM = (
    "You are a precise cognitive-linguistics concept extractor. "
    "Extract only meaningful CONTENT concepts: nouns and noun phrases that "
    "carry conceptual weight. REJECT function words, particles, pronouns, "
    "fillers, and grammatical fragments. Respond ONLY with valid JSON."
)
EXTRACT_PROMPT = """For each topic below, extract the 5-6 most important CONCEPTS the person uses to explain that topic. Include each concept in its ORIGINAL language, an English gloss for cross-language alignment, and a 0-1 importance weight.

Be concise: do NOT add reasoning. Return ONLY compact valid JSON:
{{"topics":[{{"topic":"<label>","concepts":[{{"concept":"<original>","en":"<gloss>","importance":0.9}}]}}]}}

Person's answers:
{answers}
"""
PER_TOPIC_EXTRACT = """Extract the 5-6 most important CONCEPTS this person uses to explain the topic "{topic}". Include each concept in its ORIGINAL language, an English gloss, and a 0-1 importance weight.

Return ONLY compact JSON:
{{"topics":[{{"topic":"{topic}","concepts":[{{"concept":"<original>","en":"<gloss>","importance":0.9}}]}}]}}

Person's answer on {topic}:
{text}
"""


def extract_concepts(client, answers: Dict[str, str]) -> Tuple[Dict[str, List[dict]], dict]:
    """Whole-response extraction with per-topic fallback (deepseek-safe)."""
    filled = {t: a for t, a in answers.items() if a.strip()}
    if not filled:
        return {}, {"note": "no answers to extract"}
    ablock = "\n".join(f"Topic {i} ({t}): {filled[t]}" for i, t in enumerate(TOPICS) if t in filled)
    out: Dict[str, List[dict]] = {}
    notes = []
    parsed, raw, meta = None, "", {}
    for attempt in range(3):
        raw, meta = call(client, EXTRACT_SYSTEM, EXTRACT_PROMPT.format(answers=ablock), 8192, 240)
        parsed = _parse_json(raw)
        truncated = meta.get("tokens_out", 0) >= 8000
        if parsed and "topics" in parsed and not truncated:
            break
        time.sleep(1.5)
    if parsed and "topics" in parsed:
        for t in parsed["topics"]:
            out[t.get("topic", "")] = t.get("concepts", [])
        notes.append("whole-response OK")
    else:
        # per-topic fallback
        for topic in TOPICS:
            text = filled.get(topic, "")
            if not text.strip():
                continue
            p, r, m = None, "", {}
            for attempt in range(2):
                r, m = call(client, EXTRACT_SYSTEM,
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


def run_p3(client, unit: dict) -> dict:
    """Free association (P3) — associations are the output, no extraction stage."""
    lang = unit["lang"]
    topic = unit["topic"]
    raw, meta = call(client, ASSOC_SYSTEM,
                     ASSOC_PROMPT.format(topic=topic, lang_name=LANG_NAME[lang]),
                     1024, 90)
    words: List[str] = []
    if not raw.startswith("ERROR"):
        parsed = _parse_json(raw)
        if isinstance(parsed, list):
            words = [str(w) for w in parsed if str(w).strip()]
        else:
            m = re.findall(r'"([^"]+)"', raw)
            words = [w for w in m if w.strip()]
    return {
        "unit_id": unit["unit_id"], "probe": "P3",
        "language": lang, "topic": topic, "sample": unit["sample"],
        "associations": words, "meta": meta,
    }


# ── Save / resume ───────────────────────────────────────────────────
def save_out(out_path: Path, records: List[dict]) -> None:
    out_path.write_text(json.dumps({
        "model": MODEL, "api_url": API_URL, "design": "d1_mechanism",
        "seed": RANDOM_SEED, "temperature": 0.3,
        "generated_at": datetime.now().isoformat(),
        "units": records,
    }, ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> None:
    global MODEL, API_URL
    ap = argparse.ArgumentParser(description="D1 LLM-as-subject data collection")
    ap.add_argument("--model", type=str, default=MODEL,
                    help="model id to use as subject (default: deepseek-v4-flash)")
    ap.add_argument("--api-url", type=str, default=API_URL,
                    help="OpenAI-compatible base URL (default: zen/go/v1; "
                         "free tier: https://opencode.ai/zen/v1)")
    ap.add_argument("--k", type=int, default=10, help="resamples per condition")
    ap.add_argument("--probes", type=str, default="P1,P2,P3,P5",
                    help="comma-separated probes to run")
    ap.add_argument("--limit", type=int, default=None, help="max units (pilot)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", type=str, default=None, help="output filename override")
    args = ap.parse_args()

    MODEL = args.model
    API_URL = args.api_url

    probes = {p.strip() for p in args.probes.split(",")}
    do_p1, do_p2, do_p3, do_p5 = ("P1" in probes, "P2" in probes,
                                  "P3" in probes, "P5" in probes)

    key = load_key_for_url(API_URL)
    if not key:
        print("ERROR: API key not found in .env for this gateway")
        sys.exit(1)

    plan = build_plan(do_p1, do_p2, do_p3, do_p5, args.k)
    if args.limit:
        plan = plan[: args.limit]
    print(f"  Plan: {len(plan)} units (k={args.k}, probes={sorted(probes)})")
    if args.dry_run:
        for u in plan[:8]:
            print(f"    {u['unit_id']}  probe={u['probe']} lang={u.get('lang')} "
                  f"frame={u.get('frame')} prompt={u.get('prompt_lang','-')}")
        if len(plan) > 8:
            print(f"    ... and {len(plan)-8} more")
        return

    from openai import OpenAI
    client = OpenAI(base_url=API_URL, api_key=key)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    model_tag = MODEL.replace("/", "_").replace(":", "_")
    out_path = OUT_DIR / (args.out or
                          f"llm_subject_{model_tag}_{datetime.now().strftime('%Y%m%d')}.json")

    # Resume: merge GOOD units from ALL date files of this model (cross-day
    # resume — the filename date-rolls daily, so yesterday's good units must be
    # picked up). Only units with extracted concepts are kept, so previously
    # empty (e.g. quota-failed) units are retried automatically instead of
    # being silently skipped.
    done: Dict[str, dict] = {}
    for f in sorted(OUT_DIR.glob(f"llm_subject_{model_tag}_*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"  [WARN] unreadable {f.name}, skipping")
            continue
        for u in data.get("units", []):
            if not u.get("unit_id"):
                continue
            if u.get("probe") == "P3":
                is_good = bool(u.get("associations"))
            else:
                is_good = any(c for c in u.get("concepts", {}).values())
            if is_good:
                done[u["unit_id"]] = u
    print(f"  Resume: {len(done)} good units merged from {model_tag} "
          f"files (empty units will be retried)")

    t0 = time.time()
    consecutive_empty = 0
    ABORT_AFTER = int(os.environ.get("LDS_ABORT_AFTER", 3))
    for idx, unit in enumerate(plan, 1):
        uid = unit["unit_id"]
        if uid in done:
            continue
        print(f"  [{idx}/{len(plan)}] {uid} ...", end=" ", flush=True)
        if unit["probe"] == "P3":
            rec = run_p3(client, unit)
            ok = bool(rec.get("associations"))
        else:
            rec = run_p1p2p5(client, unit)
            ok = any(c for c in rec.get("concepts", {}).values())
        ans_meta = rec.get("meta", {}).get("answer", [])
        lat_ms = sum(m.get("latency_ms", 0) for m in ans_meta) if isinstance(ans_meta, list) else 0
        print(f"{'OK' if ok else 'EMPTY'} {lat_ms}ms "
              f"(extract: {rec.get('meta', {}).get('extract', {}).get('note', '')})")
        done[uid] = rec
        save_out(out_path, list(done.values()))
        if ok:
            consecutive_empty = 0
        else:
            consecutive_empty += 1
            if consecutive_empty >= ABORT_AFTER:
                # every call already retried 3x inside run_p1p2p5; N consecutive
                # EMPTY units = model is unusable as a subject -> abort, let the
                # batch driver move on to the next model.
                print(f"\n  ABORT {MODEL}: {consecutive_empty} consecutive EMPTY units "
                      f"after per-call retries -> skipping this model")
                sys.exit(2)
        time.sleep(0.3)

    elapsed = time.time() - t0
    print(f"\n  Done: {len(done)} units in {elapsed/60:.1f} min")
    print(f"  Saved: {out_path}")
    empty = [u for u in done.values() if (u.get("probe") == "P3" and not u.get("associations"))
             or (u.get("probe") != "P3" and not any(c for c in u.get("concepts", {}).values()))]
    if empty:
        print(f"  WARN: {len(empty)} empty units to retry: "
              f"{[u['unit_id'] for u in empty][:10]}")


if __name__ == "__main__":
    main()
