#!/usr/bin/env python3
"""Muse Spark (in-client free tier) textbook re-extraction — T1 arm, ensemble-compatible.

Mirrors scripts/tools/bailian_reextract.py PROMPT + parse rules for comparability
with the 7 ensemble_v2 arms (same frozen PROMPT, same schema rules).
Transport v2 (2026-09-18): in-client `opencode run` (free tier gated to
in-OpenCode use). Parser repair ladder (rung logged) for agent escaping.

Key: none needed (in-client free tier).
Usage: python scripts/tools/spark_zen_reextract.py <basename> [--model ID] [--transport zc-free|minimax|r4|sn] [--ns NS] [--run N] [--timeout S]
Output (always): research/mimo_spark_replication/stage/<model>/<basename>.r<N>.spark.json
Output (parsed): research/ensemble_v2/<model>/<basename>.r<N>.json (+ gate field, + manifest)
Exit: 0=filed 1=usage 2=target exists 3=call/parse failed (staged only)
"""
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OPENCODE = r"C:\Users\rongj\AppData\Roaming\npm\opencode.cmd"
DEFAULT_MODEL = "muse-spark-1.3-contributor-free"
DEFAULT_TRANSPORT = "zc-free"
STAGE_ROOT = os.path.join(BASE_DIR, "research", "mimo_spark_replication", "stage")
SANDBOX = os.path.join(BASE_DIR, "research", "mimo_spark_replication", "sandbox_empty")
SHORT_INSTR = "The task is in the attached file. Follow it exactly. Output only the required JSON."
MM_URL = "https://api.minimaxi.com/anthropic/v1/messages"
R4_URL = "https://api.r4.codes/v1/chat/completions"
SN_URL = "https://token.sensenova.cn/v1/chat/completions"
MAX_TOKENS = 8000
CHUNK_CHARS = 30000
CHUNK_OVERLAP = 2000

# FROZEN T1 prompt v1 — verbatim from bailian_reextract.py PROMPT (ensemble standard).
# SHA256 recorded in research/mimo_spark_replication/PROMPT_FROZEN_v1.md.
PROMPT = """TASK: Extract knowledge-graph JSON from the textbook text at the end. Do NOT ask questions. Do NOT converse. Do NOT explain. Output ONLY the JSON object, nothing else before or after it.

Schema:
{"extracted_concepts": [{"name": "<source-language name>", "aliases": ["english", "chinese"], "definition_snippet": "<short>", "category": "concept|operation|theorem|property"}],
 "extracted_relations": [{"source": "<name from concepts>", "target": "<name from concepts>", "type": "requires|representation|generalization|inverse_of|part_of", "importance": 0.0-1.0, "evidence": "<short>"}]}
Keys MUST be exactly "extracted_concepts" and "extracted_relations" (never "nodes"/"edges"/"concepts"/"relations"). Aim 15-40 concepts, 10-30 relations. Every source/target must be a listed concept name. No placeholders. Empty lists are FORBIDDEN.

TEXTBOOK (%s / %s):
%s
BEGIN JSON NOW:"""

PROMPT_SHA256 = hashlib.sha256(PROMPT.encode("utf-8")).hexdigest()

LANGS = {"de": "German", "en": "English", "zh": "Chinese"}


def load_key():
    return "in-client-free-tier"


def load_env(name):
    try:
        lines = open(os.path.join(BASE_DIR, ".env"), encoding="utf-8").read().splitlines()
    except OSError:
        lines = []
    for line in lines:
        line = line.strip()
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip()
    return os.environ.get(name, "")


def call_minimax(model, user, timeout):
    import requests
    key = load_env("MINIMAX_API_KEY")
    if not key:
        raise RuntimeError("MINIMAX_API_KEY unset")
    r = requests.post(MM_URL,
                      headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                               "Content-Type": "application/json"},
                      json={"model": model, "max_tokens": 8000, "temperature": 0,
                            "messages": [{"role": "user", "content": user}]},
                      timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError("HTTP_%d %s" % (r.status_code, r.text[:160]))
    parts = [b.get("text", "") for b in r.json().get("content", [])
             if isinstance(b, dict) and b.get("type") == "text" and b.get("text")]
    if not parts:
        raise RuntimeError("empty_text_blocks")
    return "".join(parts)


def call_r4(model, user, timeout):
    import requests
    key = load_env("R4_API_KEY")
    if not key:
        raise RuntimeError("R4_API_KEY unset")
    r = requests.post(R4_URL,
                      headers={"Authorization": "Bearer " + key,
                               "Content-Type": "application/json"},
                      json={"model": model, "max_tokens": 8000, "temperature": 0,
                            "messages": [{"role": "user", "content": user}]},
                      timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError("HTTP_%d %s" % (r.status_code, r.text[:160]))
    msg = r.json()["choices"][0]["message"]
    content = msg.get("content") or ""
    if not (isinstance(content, str) and content.strip()):
        content = msg.get("reasoning_content") or ""
    if not (isinstance(content, str) and content.strip()):
        raise RuntimeError("empty_content")
    return content


def call_sn(model, user, timeout):
    import requests
    key = load_env("SENSENOVA_API_KEY")
    if not key:
        raise RuntimeError("SENSENOVA_API_KEY unset")
    r = requests.post(SN_URL,
                      headers={"Authorization": "Bearer " + key,
                               "Content-Type": "application/json"},
                      json={"model": model, "max_tokens": 8000, "temperature": 0,
                            "messages": [{"role": "user", "content": user}]},
                      timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError("HTTP_%d %s" % (r.status_code, r.text[:160]))
    msg = r.json()["choices"][0]["message"]
    content = msg.get("content") or ""
    if not (isinstance(content, str) and content.strip()):
        content = msg.get("reasoning_content") or ""
    if not (isinstance(content, str) and content.strip()):
        raise RuntimeError("empty_content")
    return content


def run_cli(model, message, timeout, prompt_id="p"):
    """In-client call via prompt-FILE attach (argv mangling drops long/CJK
    messages; verified 2026-09-18). explore agent + empty --dir sandbox
    (read-only, contamination-free). Returns concatenated assistant text."""
    import subprocess
    os.makedirs(SANDBOX, exist_ok=True)
    pf = os.path.join(STAGE_ROOT, "prompts", "%s.txt" % prompt_id)
    os.makedirs(os.path.dirname(pf), exist_ok=True)
    open(pf, "w", encoding="utf-8").write(message)
    r = subprocess.run([OPENCODE, "run", "--format", "json", "--agent", "explore",
                        "--dir", SANDBOX, "-m", "opencode/" + model,
                        SHORT_INSTR, "-f", pf],
                       capture_output=True, timeout=timeout,
                       cwd=BASE_DIR)
    stdout = (r.stdout or b"").decode("utf-8", errors="ignore")
    chunks = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("type") == "text":
            part = ev.get("part", {})
            t = part.get("text", "") if isinstance(part, dict) else ""
            if isinstance(t, str) and t:
                chunks.append(t)
    if chunks:
        return "".join(chunks)
    raise RuntimeError("no_text_events rc=%s" % r.returncode)


def repair_loads(raw):
    """Parser repair ladder. Returns (obj, rung) or (None, -1)."""
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return None, -1
    cand = m.group()
    try:
        return json.loads(cand), 0
    except Exception:
        pass
    try:
        return json.loads(cand.replace('\\"', '"')), 1
    except Exception:
        return None, -1


def call(model, prompt, key, timeout, prompt_id="p", transport="zc-free"):
    if transport == "minimax":
        return call_minimax(model, prompt, timeout)
    if transport == "r4":
        return call_r4(model, prompt, timeout)
    if transport == "sn":
        return call_sn(model, prompt, timeout)
    return run_cli(model, prompt, timeout, prompt_id)


def parse(raw):
    obj, _ = repair_loads(raw)
    if obj is None:
        return None
    d = obj
    if not isinstance(d, dict) or "extracted_concepts" not in d or "extracted_relations" not in d:
        return None
    cs = d["extracted_concepts"]
    if not isinstance(cs, list) or len(cs) == 0:
        return None
    names = {c.get("name", "") for c in cs if isinstance(c, dict)}
    if any(v in ("...", "..", "") for v in names):
        return None
    return d


def gate(parsed):
    """Ensemble audit gate (same as ensemble_refill_one.audit). Returns (ok, reason)."""
    try:
        cs = parsed["extracted_concepts"]
        rs = parsed.get("extracted_relations", [])
        assert isinstance(cs, list) and 15 <= len(cs) <= 40, "concepts=%d" % len(cs)
        assert isinstance(rs, list) and 10 <= len(rs) <= 30, "relations=%d" % len(rs)
        names = {c.get("name", "") for c in cs if isinstance(c, dict)}
        assert not any(v in ("...", "..", "") for v in names), "placeholder"
        for c in cs:
            blob = (c.get("name", "") or "") + "".join(c.get("aliases", []) or [])
            assert "?" not in blob and "�" not in blob, "mojibake"
        for r in rs:
            assert r.get("source") in names and r.get("target") in names, "dangling"
        return True, ""
    except AssertionError as e:
        return False, str(e)


def norm_name(s):
    return "".join(str(s).lower().split()).replace("-", "").replace("_", "")


def merge_chunks(payloads):
    """Union concepts by normalized name (first-seen wins), keep relations with live endpoints."""
    seen = {}
    for p in payloads:
        for c in p.get("extracted_concepts", []):
            k = norm_name(c.get("name", ""))
            if k and k not in seen:
                seen[k] = c
    names = {c.get("name", "") for c in seen.values()}
    rels, rseen = [], set()
    for p in payloads:
        for r in p.get("extracted_relations", []):
            if r.get("source") in names and r.get("target") in names:
                k = (r.get("source"), r.get("target"), r.get("type"))
                if k not in rseen:
                    rseen.add(k)
                    rels.append(r)
    return {"extracted_concepts": list(seen.values()), "extracted_relations": rels}


def split_chunks(text):
    parts, cur = [], []
    n = 0
    for para in text.split("\n"):
        cur.append(para)
        n += len(para) + 1
        if n >= CHUNK_CHARS:
            parts.append("\n".join(cur))
            tail = "\n".join(cur)[-CHUNK_OVERLAP:]
            cur, n = [tail], len(tail)
    if cur:
        parts.append("\n".join(cur))
    return parts


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args or not args or args[0].startswith("-"):
        print("Usage: spark_zen_reextract.py <basename> [--model ID] [--transport zc-free|minimax|r4] [--ns NS] [--run N] [--timeout S]")
        return 1
    base = args[0]
    run = args[args.index("--run") + 1] if "--run" in args else "1"
    timeout = int(args[args.index("--timeout") + 1]) if "--timeout" in args else 300
    model = args[args.index("--model") + 1] if "--model" in args else DEFAULT_MODEL
    transport = args[args.index("--transport") + 1] if "--transport" in args else DEFAULT_TRANSPORT
    if transport not in ("zc-free", "minimax", "r4", "sn"):
        print("ERROR: --transport must be zc-free|minimax|r4|sn", file=sys.stderr)
        return 1
    ns = args[args.index("--ns") + 1] if "--ns" in args else model.replace("/", "_").replace(":", "_")
    key = load_key()
    safe = ns
    stage_dir = os.path.join(BASE_DIR, "research", "mimo_spark_replication", "stage", safe)
    ens_dir = os.path.join(BASE_DIR, "research", "ensemble_v2", safe)
    os.makedirs(stage_dir, exist_ok=True)
    os.makedirs(ens_dir, exist_ok=True)
    target = "%s.r%s.json" % (base, run)
    if os.path.exists(os.path.join(ens_dir, target)):
        print("SKIP target exists: %s" % target)
        return 2
    txt_p = os.path.join(BASE_DIR, "data", "textbook", base + ".txt")
    if not os.path.exists(txt_p):
        rec = {"base": base, "model": model, "parsed": None, "note": "source_txt_missing",
               "raw": "", "attempts": []}
        json.dump(rec, open(os.path.join(stage_dir, base + ".r%s.spark.json" % run),
                            "w", encoding="utf-8"), ensure_ascii=False)
        print("SOURCE_TXT_MISSING: %s" % base)
        return 3
    text = open(txt_p, encoding="utf-8", errors="ignore").read()
    lang = LANGS.get(base.split("_")[0], "German")
    inp_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    chunked = len(text) > 2 * CHUNK_CHARS
    windows = split_chunks(text) if chunked else [text]
    attempts, payloads, raws = [], [], []
    parsed = None
    rung = -1
    for attempt in range(3):
        try:
            if chunked:
                payloads, raws = [], []
                for w in windows:
                    raw = call(model, PROMPT % (lang, base, w), key, timeout,
                                 "t1_" + safe + "_" + base + "_w%d" % len(raws), transport)
                    raws.append(raw)
                    obj, rg = repair_loads(raw)
                    p = obj if obj is not None else None
                    if p is None or parse(raw) is None:
                        raise ValueError("chunk_parse_fail")
                    payloads.append(p)
                    rung = rg
                parsed = merge_chunks(payloads)
            else:
                raw = call(model, PROMPT % (lang, base, text), key, timeout,
                             "t1_" + safe + "_" + base, transport)
                raws = [raw]
                obj, rung = repair_loads(raw)
                parsed = parse(raw)
            attempts.append({"n": attempt + 1, "ok": parsed is not None, "rung": rung,
                             "err": "" if parsed else "parse_fail"})
            if parsed:
                break
        except Exception as e:
            attempts.append({"n": attempt + 1, "ok": False, "rung": -1,
                             "err": "%s" % type(e).__name__})
            time.sleep(10 * (attempt + 1))
    rec = {"base": base, "model": model, "ns": ns,
           "transport": {"zc-free": "opencode-run/file-attach/explore/sandbox (in-client free tier)",
                         "minimax": "minimax-anthropic-direct " + MM_URL,
                         "r4": "r4-openai-direct " + R4_URL,
                         "sn": "sensenova-openai-direct " + SN_URL}[transport],
           "temperature": 0, "max_tokens": 8000,
           "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "prompt_sha256": PROMPT_SHA256, "input_sha256": inp_sha,
           "input_chars": len(text), "chunked": chunked, "n_windows": len(windows),
           "attempts": attempts, "parsed": parsed,
           "raw": raws[0][:8000] if len(raws) == 1 else [x[:8000] for x in raws]}
    json.dump(rec, open(os.path.join(stage_dir, base + ".r%s.spark.json" % run),
                        "w", encoding="utf-8"), ensure_ascii=False)
    if parsed is None:
        print("CALL_PARSE_FAILED after %d attempts (staged)" % len(attempts))
        return 3
    ok, reason = gate(parsed)
    filed = {"base": base, "model": model, "parsed": parsed, "rung": rung,
             "gate_pass": ok, "gate_reason": reason}
    json.dump(filed, open(os.path.join(ens_dir, target), "w", encoding="utf-8"), ensure_ascii=False)
    upd_manifest(ens_dir, model, target, True, "" if ok else "gate:" + reason)
    print("OK %s c=%d r=%d gate=%s rung=%s" % (target, len(parsed["extracted_concepts"]),
                                               len(parsed["extracted_relations"]), ok, rung))
    return 0


def upd_manifest(ens_dir, model, target, ok, note):
    mp = os.path.join(ens_dir, "_manifest.json")
    m = json.load(open(mp, encoding="utf-8")) if os.path.exists(mp) else {
        "model": model, "done": [], "missing": [], "failed": [], "do_not_retry": []}
    key = "done" if ok else "failed"
    if target not in m[key]:
        m[key].append(target)
    json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.exit(main())
