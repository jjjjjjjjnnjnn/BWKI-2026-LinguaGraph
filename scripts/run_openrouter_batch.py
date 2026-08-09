#!/usr/bin/env python3
"""Autonomous OpenRouter free-tier batch for LinguaGraph LLM-as-Subject.

OpenRouter free models carry a daily "free-models-per-day" quota that resets at
the provider's midnight. This orchestrator polls the quota with a minimal
1-token probe and, as soon as it is free, runs the 10 free models SEQUENTIALLY
(P1, k=10) so the shared daily quota is never oversubscribed by parallel jobs.

The per-model subject run inherits the abort-after-3-consecutive-EMPTY rule
(LDS_ABORT_AFTER) and resume-by-unit-id, so a genuinely unusable model is
skipped without wasting quota and a partially-collected model resumes.

Run:  python scripts/run_openrouter_batch.py   (blocking; run in background)
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
API_URL = "https://openrouter.ai/api/v1"
PROBE_MODEL = "openai/gpt-oss-20b:free"  # quota probe (cheap, known-good)

# Free models reachable via the account (2026-08-09 smoke-verified 9/10;
# gemma-4-31b had a transient 429 but is worth retrying).
MODELS = [
    "openai/gpt-oss-20b:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "google/gemma-4-26b-a4b-it:free",
    "google/gemma-4-31b-it:free",
    "poolside/laguna-s-2.1:free",
    "poolside/laguna-xs-2.1:free",
    "inclusionai/ling-3.0-tiny:free",
    "cohere/north-mini-code:free",
]

POLL_SECONDS = 300  # 5 min between quota probes


def load_key() -> str:
    env = PROJECT_ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                if k.strip() == "OPENROUTER_API_KEY":
                    return v.strip()
    return ""


def quota_free() -> bool:
    """Minimal 1-token probe. 429/5xx -> still limited (keep polling);
    anything else (2xx or non-quota 4xx) -> assume free, let the subject
    script handle per-model issues (avoids infinite poll on a bad probe)."""
    body = json.dumps({"model": PROBE_MODEL,
                       "messages": [{"role": "user", "content": "hi"}],
                       "max_tokens": 1}).encode()
    req = urllib.request.Request(
        f"{API_URL}/chat/completions", data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {load_key()}",
                 "User-Agent": "curl/8.0"})
    try:
        urllib.request.urlopen(req, timeout=30).read()
        return True
    except urllib.error.HTTPError as e:
        if e.code in (429, 500, 502, 503, 504):
            return False
        return True
    except Exception:
        return False  # transient network: keep polling


def main() -> None:
    print(f"[orchestrator] start {time.strftime('%Y-%m-%d %H:%M:%S')} "
          f"— polling OpenRouter free quota every {POLL_SECONDS // 60} min", flush=True)
    tries = 0
    while not quota_free():
        tries += 1
        print(f"[orchestrator] quota still limited (probe {tries}); "
              f"retry in {POLL_SECONDS // 60} min", flush=True)
        time.sleep(POLL_SECONDS)
    print(f"[orchestrator] QUOTA FREE at {time.strftime('%H:%M:%S')} — starting batch", flush=True)

    for i, m in enumerate(MODELS, 1):
        print(f"\n[orchestrator] === [{i}/{len(MODELS)}] {m} ===", flush=True)
        r = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts" / "lds_c_llm_subject.py"),
             "--model", m, "--api-url", API_URL, "--probes", "P1", "--k", "10"],
            cwd=str(PROJECT_ROOT))
        print(f"[orchestrator] {m} exit code {r.returncode}", flush=True)

    print(f"[orchestrator] done {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)


if __name__ == "__main__":
    main()
