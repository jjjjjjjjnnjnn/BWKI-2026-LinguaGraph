#!/usr/bin/env python3
"""Free-tier multi-model gold-harness benchmark — T2 arm (in-client transport).

Call CONTENT mirrors scripts/batch_model_benchmark.py evaluate_model
(system prompt, EXTRACT_PROMPT_TEMPLATE, temperature 0.1, max_tokens 2048,
text[:2000], exact-match set overlap, macro mean). Transport adaptation:
in-client `opencode run` (free tier gated); system prompt inlined as
[SYSTEM-ROLE] head (content identical, SHA kept). Parser repair ladder logged.

Key: none needed (in-client free tier).
Usage: python scripts/tools/spark_zen_gold_bench.py [--model ID] [--transport zc-free|minimax|r4|sn] [--ns NS] [--timeout S] [--sleep F] [--max-items N]
Output: research/mimo_spark_replication/t2_<ns>.json (resume-safe)
"""
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Transport v2 (2026-09-18): in-client `opencode run` — free tier is gated to
# in-OpenCode use (direct HTTP -> FreeTierError; paid balance insufficient).
# Model ids are bare zen ids, addressed as opencode/<id> on the CLI.
OPENCODE = r"C:\Users\rongj\AppData\Roaming\npm\opencode.cmd"
DEFAULT_MODEL = "muse-spark-1.3-contributor-free"
DEFAULT_TRANSPORT = "zc-free"
GOLD_PATH = os.path.join(BASE_DIR, "data", "gold", "gold_dataset.json")
OUT_DIR = os.path.join(BASE_DIR, "research", "mimo_spark_replication")
SANDBOX = os.path.join(OUT_DIR, "sandbox_empty")
SHORT_INSTR = "The task is in the attached file. Follow it exactly. Output only the required JSON."
MM_URL = "https://api.minimaxi.com/anthropic/v1/messages"
R4_URL = "https://api.r4.codes/v1/chat/completions"
SN_URL = "https://token.sensenova.cn/v1/chat/completions"
ENV_KEYS = {"minimax": "MINIMAX_API_KEY", "r4": "R4_API_KEY", "sn": "SENSENOVA_API_KEY"}
TRANSPORT_LABEL = {"zc-free": "opencode-run/file-attach/explore/sandbox (in-client free tier)",
                   "minimax": "minimax-anthropic-direct " + MM_URL,
                   "r4": "r4-openai-direct " + R4_URL,
                   "sn": "sensenova-openai-direct " + SN_URL}

# FROZEN T2 prompts v1 — verbatim from batch_model_benchmark.py L29-50 (template)
# and L137 (system). SHAs recorded in PROMPT_FROZEN_v1.md.
SYSTEM = "\u4f60\u662f\u6982\u5ff5\u63d0\u53d6\u4e13\u5bb6\u3002\u8f93\u51fa\u4e25\u683c JSON \u683c\u5f0f\u3002\u6982\u5ff5\u540d\u79f0\u4f7f\u7528\u539f\u59cb\u8bed\u8a00\uff0c\u7981\u6b62 ASCII \u7f16\u7801\u3002\u8f93\u51fa UTF-8 \u4e2d\u6587\u3002"
TEMPLATE = """\u4ece\u4ee5\u4e0b\u6587\u672c\u4e2d\u63d0\u53d6\u5173\u952e\u6982\u5ff5\u53ca\u5176\u5173\u7cfb\u3002

\u4efb\u52a1\uff1a\u63d0\u53d6 10-20 \u4e2a\u6838\u5fc3\u6982\u5ff5\uff0c\u5e76\u6309\u4ee5\u4e0b JSON Schema \u8f93\u51fa\uff1a

{{
  "topic": "[topic]",
  "language": "[lang]",
  "concepts": [
    {{
      "name": "\u6982\u5ff5\u540d\u79f0\uff08\u539f\u59cb\u8bed\u8a00\uff09",
      "category": "\u6838\u5fc3\u6982\u5ff5/\u76f8\u5173\u6982\u5ff5/\u5177\u4f53\u4e8b\u4f8b",
      "related_concepts": ["\u76f8\u5173\u6982\u5ff51", "\u76f8\u5173\u6982\u5ff52"],
      "definition_snippet": "\u4e00\u53e5\u8bdd\u5b9a\u4e49"
    }}
  ],
  "relations": [
    {{"source": "\u6982\u5ff5A", "target": "\u6982\u5ff5B", "type": "\u96b6\u5c5e\u4e8e/\u5bfc\u81f4/\u5bf9\u7acb/\u76f8\u5173"}}
  ]
}}

\u6587\u672c\u5185\u5bb9\uff1a
{text}"""

SYSTEM_SHA256 = hashlib.sha256(SYSTEM.encode("utf-8")).hexdigest()
TEMPLATE_SHA256 = hashlib.sha256(TEMPLATE.encode("utf-8")).hexdigest()


# T2 system prompt is INLINED at the head of the user message for the
# opencode-run transport (CLI takes message only). Content identical (SHA kept);
# adaptation logged as transport caveat in the prereg addendum.
COMPOSED_HEAD = "[SYSTEM-ROLE]\n" + SYSTEM + "\n\n[TASK]\n"


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


def load_key():
    return "in-client-free-tier"


def call_minimax(model, system, user, timeout, temperature):
    import requests
    key = load_env("MINIMAX_API_KEY")
    if not key:
        raise RuntimeError("MINIMAX_API_KEY unset")
    r = requests.post(MM_URL,
                      headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                               "Content-Type": "application/json"},
                      json={"model": model, "max_tokens": 2048, "temperature": temperature,
                            "system": system,
                            "messages": [{"role": "user", "content": user}]},
                      timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError("HTTP_%d %s" % (r.status_code, r.text[:160]))
    d = r.json()
    parts = [b.get("text", "") for b in d.get("content", [])
             if isinstance(b, dict) and b.get("type") == "text" and b.get("text")]
    if not parts:
        raise RuntimeError("empty_text_blocks")
    return "".join(parts)


def call_r4(model, system, user, timeout, temperature):
    import requests
    key = load_env("R4_API_KEY")
    if not key:
        raise RuntimeError("R4_API_KEY unset")
    r = requests.post(R4_URL,
                      headers={"Authorization": "Bearer " + key,
                               "Content-Type": "application/json"},
                      json={"model": model, "max_tokens": 8192, "temperature": temperature,
                            "messages": [{"role": "system", "content": system},
                                         {"role": "user", "content": user}]},
                      timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError("HTTP_%d %s" % (r.status_code, r.text[:160]))
    msg = r.json()["choices"][0]["message"]
    content = msg.get("content") or ""
    field = "content"
    if not (isinstance(content, str) and content.strip()):
        content = msg.get("reasoning_content") or ""
        field = "reasoning_content"
    if not (isinstance(content, str) and content.strip()):
        raise RuntimeError("empty_content")
    return content, field


def call_sn(model, system, user, timeout, temperature):
    import requests
    key = load_env("SENSENOVA_API_KEY")
    if not key:
        raise RuntimeError("SENSENOVA_API_KEY unset")
    r = requests.post(SN_URL,
                      headers={"Authorization": "Bearer " + key,
                               "Content-Type": "application/json"},
                      json={"model": model, "max_tokens": 2048, "temperature": temperature,
                            "messages": [{"role": "system", "content": system},
                                         {"role": "user", "content": user}]},
                      timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError("HTTP_%d %s" % (r.status_code, r.text[:160]))
    msg = r.json()["choices"][0]["message"]
    content = msg.get("content") or ""
    field = "content"
    if not (isinstance(content, str) and content.strip()):
        content = msg.get("reasoning_content") or ""
        field = "reasoning_content"
    if not (isinstance(content, str) and content.strip()):
        raise RuntimeError("empty_content")
    return content, field


def run_cli(model, message, timeout, prompt_id="p"):
    """In-client call via prompt-FILE attach (argv mangling drops long/CJK
    messages; verified 2026-09-18). explore agent + empty --dir sandbox
    (read-only, contamination-free). Returns concatenated assistant text."""
    import subprocess
    os.makedirs(SANDBOX, exist_ok=True)
    pf = os.path.join(OUT_DIR, "stage", "prompts", "%s.txt" % prompt_id)
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


def repair_loads(s):
    """Parser repair ladder. Returns (obj, rung) or (None, -1)."""
    m = re.search(r"\{.*\}", s, re.DOTALL)
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


def call(model, text, key, timeout, prompt_id="p", transport="zc-free"):
    user = TEMPLATE.format(text=text[:2000])
    if transport == "minimax":
        return call_minimax(model, SYSTEM, user, timeout, 0.1), "system-param"
    if transport == "r4":
        return call_r4(model, SYSTEM, user, timeout, 0.1)
    if transport == "sn":
        return call_sn(model, SYSTEM, user, timeout, 0.1)
    composed = COMPOSED_HEAD + user
    return run_cli(model, composed, timeout, prompt_id), hashlib.sha256(composed.encode("utf-8")).hexdigest()


def score_item(gold, raw):
    """Harness scoring (verbatim logic) + repair ladder. Returns
    (predicted, p, r, f1, rung) or (None, 0, 0, 0, -1)."""
    obj, rung = repair_loads(raw)
    if obj is None:
        return None, 0.0, 0.0, 0.0, -1
    try:
        predicted = {c.get("name", "") for c in obj.get("concepts", [])
                     if isinstance(c, dict) and c.get("name", "")}
    except Exception:
        return None, 0.0, 0.0, 0.0, -1
    if not predicted:
        return None, 0.0, 0.0, 0.0, -1
    tp = len(set(gold) & predicted)
    prec = tp / max(len(predicted), 1)
    rec = tp / max(len(gold), 1)
    f1 = 2 * prec * rec / max(prec + rec, 0.001)
    return sorted(predicted), prec, rec, f1, rung


def main():
    timeout = 180
    sleep_s = 5.0
    model = DEFAULT_MODEL
    transport = DEFAULT_TRANSPORT
    ns = None
    max_items = 0
    for i, a in enumerate(sys.argv[1:]):
        if a == "--timeout":
            timeout = int(sys.argv[2 + i])
        if a == "--sleep":
            sleep_s = float(sys.argv[2 + i])
        if a == "--model":
            model = sys.argv[2 + i]
        if a == "--transport":
            transport = sys.argv[2 + i]
        if a == "--ns":
            ns = sys.argv[2 + i]
        if a == "--max-items":
            max_items = int(sys.argv[2 + i])
    if transport not in ("zc-free", "minimax", "r4", "sn"):
        print("ERROR: --transport must be zc-free|minimax|r4|sn", file=sys.stderr)
        return 1
    if ns is None:
        ns = model.replace("/", "_").replace(":", "_")
    os.makedirs(OUT_DIR, exist_ok=True)
    lock = os.path.join(OUT_DIR, ".t2_%s.lock" % ns)
    if os.path.exists(lock):
        try:
            pid = int(open(lock, encoding="utf-8").read().strip())
            os.kill(pid, 0)
            print("LOCKED by live pid %d — refuse overlapping run" % pid, file=sys.stderr)
            return 5
        except Exception:
            pass
    open(lock, "w", encoding="utf-8").write(str(os.getpid()))
    try:
        return run_all(model, timeout, sleep_s, transport, ns, max_items)
    finally:
        try:
            if open(lock, encoding="utf-8").read().strip() == str(os.getpid()):
                os.remove(lock)
        except Exception:
            pass


def run_all(model, timeout, sleep_s, transport, ns, max_items=0):
    from datetime import datetime as _dt
    key = load_key()
    safe = ns
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "t2_%s.json" % safe)
    done = {}
    if os.path.exists(out_path):
        try:
            old = json.load(open(out_path, encoding="utf-8"))
            if old.get("parked") and "--force-resume" not in sys.argv:
                print("PARKED file %s (after %s) — resume requires --force-resume" % (
                    out_path, old.get("parked_after")), file=sys.stderr)
                return 7
            for r in old.get("items", []):
                if r.get("valid"):
                    done[r["sample_id"]] = r
            print("RESUME %d valid items loaded" % len(done))
        except Exception as e:
            print("RESUME_READ_FAIL %s" % e)
    items = json.load(open(GOLD_PATH, encoding="utf-8"))
    for it in items:
        if "gold_concepts" not in it:
            hl = it.get("human_labels", {})
            it["gold_concepts"] = hl.get("concepts", []) if isinstance(hl, dict) else []
    os.makedirs(OUT_DIR, exist_ok=True)
    recs = []
    comp_sha = hashlib.sha256((COMPOSED_HEAD + TEMPLATE).encode("utf-8")).hexdigest()

    def build_out(recs, complete):
        valid = [r for r in recs if r["valid"]]

        def mean(ks):
            return {k: round(sum(r[k] for r in valid) / max(len(valid), 1), 4)
                    for k in ks} if valid else {}

        def subset(pred_fn):
            s = [r for r in valid if pred_fn(r)]
            return {"n": len(s), "mean_f1": round(sum(r["f1"] for r in s) / max(len(s), 1), 4)} if s else {"n": 0}

        return {"model": model, "ns": ns,
                "transport": TRANSPORT_LABEL[transport],
                "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "temperature": 0.1,
                "max_tokens": {"zc-free": 2048, "minimax": 2048, "r4": 8192, "sn": 2048}[transport],
                "max_tokens_note": "r4 raised 2048->8192 for reasoning-trace headroom (Deviation-001); ceiling only, non-binding below",
                "text_window": "text[:2000]",
                "system_sha256": SYSTEM_SHA256, "template_sha256": TEMPLATE_SHA256,
                "composed_head_sha256": comp_sha,
                "system_transport_note": "zc-free: system inlined as [SYSTEM-ROLE] head (CLI takes message only); minimax/r4: native system role/param",
                "complete": complete,
                "total_items": len(items), "valid": len(valid),
                "failed": len(recs) - len(valid),
                "failed_items": [r["sample_id"] for r in recs if not r["valid"]],
                "rung_counts": {str(k): sum(1 for r in valid if r.get("rung") == k) for k in (0, 1)},
                "summary": mean(["p", "r", "f1"]),
                "subsets": {
                    "math_annotator_1": subset(lambda r: r["annotator"] == "annotator_1"),
                    "social_auto_accepted": subset(lambda r: r["annotator"] == "auto_accepted"),
                    "zh": subset(lambda r: r["language"] == "zh"),
                    "de": subset(lambda r: r["language"] == "de"),
                    "en": subset(lambda r: r["language"] == "en")},
                "items": recs}

    for idx, item in enumerate(items):
        if max_items and idx >= max_items:
            print("MAX_ITEMS %d reached (smoke mode)" % max_items)
            break
        sid = item.get("sample_id", item.get("id", "unknown"))
        if sid in done:
            recs.append(done[sid])
            continue
        text = item.get("text", item.get("content", ""))
        gold = item.get("gold_concepts", item.get("concepts", []))
        rec = {"sample_id": sid, "language": item.get("language", ""),
               "annotator": item.get("annotator", ""), "gold_n": len(gold),
               "gold": gold, "predicted": [], "p": 0.0, "r": 0.0, "f1": 0.0,
               "valid": False, "rung": -1, "attempts": [], "raw": ""}
        if not text or not gold:
            rec["attempts"].append({"n": 0, "ok": False, "err": "empty_text_or_gold"})
            recs.append(rec)
            continue
        for attempt in range(3):
            import time as _t
            t0 = _t.time()
            try:
                print("  CALL %s att%d %s" % (
                    _dt.now().strftime("%H:%M:%S"), attempt + 1, sid), flush=True)
                raw, _ = call(model, text, key, timeout, "t2_" + safe + "_" + sid,
                                transport)
                pred, p, r, f1, rung = score_item(gold, raw)
                ok = pred is not None
                rec["attempts"].append({"n": attempt + 1, "ok": ok,
                                        "secs": round(_t.time() - t0, 1),
                                        "err": "" if ok else "parse_or_empty"})
                if ok:
                    rec.update({"predicted": pred, "p": round(p, 4), "r": round(r, 4),
                                "f1": round(f1, 4), "valid": True, "rung": rung,
                                "raw": raw[:4000]})
                    break
            except Exception as e:
                rec["attempts"].append({"n": attempt + 1, "ok": False,
                                        "secs": round(_t.time() - t0, 1),
                                        "err": "%s %s" % (type(e).__name__, str(e)[:80])})
                time.sleep(10 * (attempt + 1))
        recs.append(rec)
        print("  [%d/%d] %s f1=%.4f valid=%s rung=%s" % (idx + 1, len(items), sid,
                                                         rec["f1"], rec["valid"],
                                                         rec["rung"]), flush=True)
        json.dump(build_out(recs, False), open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
        tail = [r for r in recs[-5:]]
        if len(tail) == 5 and not any(r.get("valid") for r in tail):
            out = build_out(recs, False)
            out["parked"] = True
            out["parked_after"] = sid
            out["park_note"] = "circuit breaker: 5 consecutive total-fails (A9-5)"
            json.dump(out, open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
            print("BREAKER_PARKED after %s" % sid, flush=True)
            return 6
        time.sleep(sleep_s)
    out = build_out(recs, True)
    json.dump(out, open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
    print("SUMMARY valid=%d/%d mean=%s" % (out["valid"], out["total_items"], out["summary"]))
    print("SUBSETS %s" % json.dumps(out["subsets"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
