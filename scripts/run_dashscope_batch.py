#!/usr/bin/env python3
"""Parallel DashScope batch: run the P1 LLM-as-Subject protocol on many models.

DashScope grants ~1M free tokens per model, so running models in parallel is
safe (no shared daily quota like OpenRouter). 8 workers launch one subject
script process per model (k=10); each process has its own retry + abort rules.

Run:  python scripts/run_dashscope_batch.py   (blocking; run in background)
"""
from __future__ import annotations

import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
WORKERS = 6  # was 8; 8-parallel may have contributed to the account block
K = 10

# ONLY models with free quota (user's 137-model free list, 2026-08-10).
# Chat-capable subjects only (excluded: image/vl/mt/math/coder/ocr/gui/
# analysis/audio; and anything NOT on the free list would charge the account).
MODELS = [
    # DeepSeek (all on free list)
    "deepseek-v3", "deepseek-v3.1", "deepseek-v3.2", "deepseek-v4-flash",
    "deepseek-v4-pro", "deepseek-r1", "deepseek-r1-0528",
    "deepseek-r1-distill-qwen-7b", "deepseek-r1-distill-qwen-14b",
    "deepseek-r1-distill-qwen-32b",
    # GLM (all on free list)
    "glm-4.5", "glm-4.5-air", "glm-4.6", "glm-4.7", "glm-5", "glm-5.1", "glm-5.2",
    # Kimi / Moonshot
    "kimi-k2.5", "kimi-k2.6", "kimi-k2.7-code", "kimi-k2-thinking",
    "Moonshot-Kimi-K2-Instruct",
    # MiniMax
    "MiniMax-M2.1", "MiniMax-M2.5",
    # Qwen
    "qwen-max", "qwen-plus", "qwen-turbo", "qwen-flash",
    "qwen3-max", "qwen3.5-plus", "qwen3.5-flash", "qwen3.6-plus", "qwen3.6-flash",
    "qwen3.7-plus", "qwen3.7-flash", "qwen3.7-max", "qwen3.8-max",
    "qwen3-8b", "qwen3-14b", "qwen3-32b", "qwen3-30b-a3b", "qwen3-235b-a22b",
    "qwen3.5-27b", "qwen3.5-35b-a3b", "qwen3.5-122b-a10b", "qwen3.5-397b-a17b",
    "qwen3.6-27b", "qwen3.6-35b-a3b",
    "qwq-plus",
]


def run_model(model: str) -> tuple:
    t0 = time.time()
    r = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "lds_c_llm_subject.py"),
         "--model", model, "--provider", "dashscope",
         "--api-url", API_URL, "--probes", "P1", "--k", str(K)],
        cwd=str(PROJECT_ROOT))
    return (model, r.returncode, time.time() - t0)


def main() -> None:
    print(f"[dashscope-batch] {len(MODELS)} models, {WORKERS} workers, "
          f"k={K} — start {time.strftime('%H:%M:%S')}", flush=True)
    done = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = {ex.submit(run_model, m): m for m in MODELS}
        for i, fut in enumerate(futures, 1):
            model, rc, sec = fut.result()
            done.append((model, rc, sec))
            print(f"[dashscope-batch] [{i}/{len(MODELS)}] {model} "
                  f"exit={rc} {sec/60:.1f}min", flush=True)
    print(f"[dashscope-batch] done {time.strftime('%H:%M:%S')} — "
          f"{len([d for d in done if d[1] == 0])}/{len(done)} exit 0", flush=True)


if __name__ == "__main__":
    main()
