#!/usr/bin/env python3
"""Multi-agent blind-review judge driver (falsify/screen only, never matures C9b).

Reads research/gold_review_v2/review_72.json, sends each rater ONLY
{audit_id, language, question, text} + frozen judge prompt (no sample_id,
no gold, no predictions). Single-turn per item, <=3 attempts.
Outputs research/gold_review_v2/panel_<rater>.json in review_72 filled
schema (sample_id joined OFFLINE by dispatcher) + consensus via
panel_consensus.py. Feed consensus to gold_blind_audit.py --import.
Transports: r4 / sn / zc-free / openrouter (key names only; values in-process).
Usage: python scripts/tools/panel_judge.py --rater R1 [--max-items N] [--timeout S] [--sleep F]
Raters frozen in A-judge amendment (exact triples).
"""
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(BASE_DIR, "research", "gold_review_v2")
SANDBOX = os.path.join(BASE_DIR, "research", "mimo_spark_replication", "sandbox_empty")
R4_URL = "https://api.r4.codes/v1/chat/completions"
SN_URL = "https://token.sensenova.cn/v1/chat/completions"
OR_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENCODE = r"C:\Users\rongj\AppData\Roaming\npm\opencode.cmd"

JUDGE_SYS = ("You are an independent concept reviewer. Judge ONLY the text below. "
             "Output strict JSON only.")
JUDGE_TEMPLATE = """Review task {audit_id} (language: {language}).

Question: {question}

Text:
{text}

List the concepts that this text genuinely warrants (1 or more; single-word answers may warrant exactly 1).
Then give your verdict in EXACTLY this JSON shape:
{{
  "audit_id": "{audit_id}",
  "decision": "accept|edit|reject",
  "concepts": ["concept 1", "concept 2"]
}}
Rules: decision=accept only if the text fully supports a clean list; edit if partially (give corrected list);
reject if the text is a fragment, empty, or concept-less. Concept names in the text's own language. No translation."""

JUDGE_SYS_SHA = hashlib.sha256(JUDGE_SYS.encode("utf-8")).hexdigest()
JUDGE_TPL_SHA = hashlib.sha256(JUDGE_TEMPLATE.encode("utf-8")).hexdigest()

# rater -> (model, transport, key-env). Triples frozen in A-judge amendment.
RATERS = {
    "R1": ("deepseek-v4.1-flash", "r4", "R4_API_KEY"),
    "R2": ("glm-5.2", "r4", "R4_API_KEY"),
    "R3": ("sensenova-6.8-flash-lite", "sn", "SENSENOVA_API_KEY"),
    "R4": ("cohere/north-mini-code:free", "openrouter", "OPENROUTER_API_KEY"),
    "R5": ("big-pickle", "zc-free", None),
}


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


def call_openai_compat(url, key, model, system, user, timeout, temp=0.0, ceil=2048):
    import requests
    r = requests.post(url, headers={"Authorization": "Bearer " + key,
                                    "Content-Type": "application/json"},
                      json={"model": model, "max_tokens": ceil, "temperature": temp,
                            "messages": [{"role": "system", "content": system},
                                         {"role": "user", "content": user}]},
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
    import subprocess
    os.makedirs(SANDBOX, exist_ok=True)
    pf = os.path.join(OUT_DIR, "panel_prompts", "%s.txt" % prompt_id)
    os.makedirs(os.path.dirname(pf), exist_ok=True)
    open(pf, "w", encoding="utf-8").write(message)
    r = subprocess.run([OPENCODE, "run", "--format", "json", "--agent", "explore",
                        "--dir", SANDBOX, "-m", "opencode/" + model,
                        "The task is in the attached file. Follow it exactly. Output only the required JSON.",
                        "-f", pf], capture_output=True, timeout=timeout, cwd=BASE_DIR)
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


def call_rater(model, transport, user, timeout, prompt_id):
    if transport == "r4":
        return call_openai_compat(R4_URL, load_env("R4_API_KEY"), model, JUDGE_SYS, user, timeout, 0.0, 8192)
    if transport == "sn":
        return call_openai_compat(SN_URL, load_env("SENSENOVA_API_KEY"), model, JUDGE_SYS, user, timeout, 0.0, 2048)
    if transport == "openrouter":
        return call_openai_compat(OR_URL, load_env("OPENROUTER_API_KEY"), model, JUDGE_SYS, user, timeout, 0.0, 2048)
    return run_cli(model, JUDGE_SYS + "\n\n" + user, timeout, prompt_id)


def repair_loads(s):
    m = re.search(r"\{.*\}", s, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group())
    except Exception:
        try:
            return json.loads(m.group().replace('\\"', '"'))
        except Exception:
            return None


def main():
    rater = None
    timeout = 180
    sleep_s = 5.0
    max_items = 0
    model_override = None
    for i, a in enumerate(sys.argv[1:]):
        if a == "--rater":
            rater = sys.argv[2 + i]
        if a == "--timeout":
            timeout = int(sys.argv[2 + i])
        if a == "--sleep":
            sleep_s = float(sys.argv[2 + i])
        if a == "--max-items":
            max_items = int(sys.argv[2 + i])
        if a == "--model":
            model_override = sys.argv[2 + i]
    if rater not in RATERS:
        print("ERROR: --rater must be one of %s" % sorted(RATERS), file=sys.stderr)
        return 1
    model, transport, _ = RATERS[rater]
    if model_override:
        # REAUDIT 2026-09-19 (D-J2): --model silently replaces the frozen (model, transport)
        # triple with no "override used" marker — violates amendment J4 freeze semantics.
        # Documented only; add a hard guard before any future panel run.
        model = model_override
    os.makedirs(OUT_DIR, exist_ok=True)
    lock = os.path.join(OUT_DIR, ".panel_%s.lock" % rater)
    if os.path.exists(lock):
        try:
            pid = int(open(lock, encoding="utf-8").read().strip())
            os.kill(pid, 0)
            print("LOCKED by live pid %d" % pid, file=sys.stderr)
            return 5
        except Exception:
            pass
    open(lock, "w", encoding="utf-8").write(str(os.getpid()))
    try:
        src = json.load(open(os.path.join(OUT_DIR, "review_72.json"), encoding="utf-8"))
        records = src.get("records", src if isinstance(src, list) else [])
        amap = {r["audit_id"]: r for r in records}
        out_path = os.path.join(OUT_DIR, "panel_%s.json" % rater)
        done = {}
        if os.path.exists(out_path):
            try:
                old = json.load(open(out_path, encoding="utf-8"))
                for r in old.get("records", []):
                    if r.get("decision") in ("accept", "edit", "reject"):
                        done[r["audit_id"]] = r
                print("RESUME %d judged" % len(done))
            except Exception as e:
                print("RESUME_READ_FAIL %s" % e)
        recs = [done[k] for k in sorted(done)]
        n_new = 0
        for aid in sorted(amap):
            if aid in done:
                continue
            if max_items and n_new >= max_items:
                print("MAX_ITEMS %d reached (smoke mode)" % max_items)
                break
            it = amap[aid]
            user = JUDGE_TEMPLATE.format(audit_id=aid, language=it.get("language", ""),
                                         question=it.get("question", ""), text=it.get("text", ""))
            rec = {"audit_id": aid, "sample_id": it.get("sample_id", ""),
                   "reviewer": rater, "decision": "", "edited_concepts": [],
                   "attempts": []}
            for attempt in range(3):
                t0 = time.time()
                try:
                    print("  CALL %s att%d %s" % (
                        datetime.now(timezone.utc).strftime("%H:%M:%S"), attempt + 1, aid), flush=True)
                    raw = call_rater(model, transport, user, timeout, "panel_%s_%s" % (rater, aid))
                    obj = repair_loads(raw)
                    ok = (isinstance(obj, dict) and obj.get("decision") in ("accept", "edit", "reject")
                          and isinstance(obj.get("concepts"), list))
                    rec["attempts"].append({"n": attempt + 1, "ok": ok,
                                            "secs": round(time.time() - t0, 1)})
                    if ok:
                        rec["decision"] = obj["decision"]
                        rec["edited_concepts"] = [str(c) for c in obj["concepts"] if str(c).strip()]
                        break
                except Exception as e:
                    rec["attempts"].append({"n": attempt + 1, "ok": False,
                                            "secs": round(time.time() - t0, 1),
                                            "err": "%s %s" % (type(e).__name__, str(e)[:80])})
                    time.sleep(10 * (attempt + 1))
            recs.append(rec)
            n_new += 1
            print("  [%s] %s decision=%s n_concepts=%d" % (
                aid, "OK" if rec["decision"] else "FAIL", rec["decision"], len(rec["edited_concepts"])), flush=True)
            json.dump({"meta": {"rater": rater, "model": model, "transport": transport,
                                "judge_sys_sha": JUDGE_SYS_SHA, "judge_tpl_sha": JUDGE_TPL_SHA,
                                "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                "non_human": True, "mature_never": True},
                       "records": recs},
                      open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
            tail = recs[-5:]
            if len(tail) == 5 and not any(r.get("decision") for r in tail):
                print("BREAKER_PARKED", flush=True)
                return 6
            time.sleep(sleep_s)
        print("DONE judged=%d/%d" % (len([r for r in recs if r.get("decision")]), len(amap)))
        return 0
    finally:
        try:
            if open(lock, encoding="utf-8").read().strip() == str(os.getpid()):
                os.remove(lock)
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
