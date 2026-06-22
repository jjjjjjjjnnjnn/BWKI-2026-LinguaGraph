#!/usr/bin/env python3
"""
LinguaGraph — Multi-Model Benchmark Runner
============================================
Tests multiple LLM models on the 20 gold labels and evaluates each.

Usage:
    python scripts/run_model_benchmark.py
    python scripts/run_model_benchmark.py --models qwen-turbo,qwen-max

API config: uses --api-url, --api-key from env OPENROUTER_API_KEY or BAILIAN_API_KEY
"""

import json
import os
import sqlite3
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / "scripts"))
sys.path.insert(0, str(PROJECT_DIR / "src"))

from db_utils import get_connection

# Bailian
BAILIAN_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
BAILIAN_KEY = os.environ.get("BAILIAN_API_KEY", "")

# Models to test
BAILIAN_MODELS = [
    "qwen-turbo",
    "qwen-plus",
    "qwen-max",
]

LOCAL_MODELS = [
    ("qwen/qwen3-8b", "http://localhost:1234/v1"),
]


def clean_extractions(conn):
    conn.execute("DELETE FROM extractions")
    conn.commit()


def run_extraction(model: str, api_url: str, api_key: str) -> bool:
    """Run batch extraction on gold labels. Returns True if successful."""
    cmd = [
        sys.executable, str(PROJECT_DIR / "scripts" / "batch_process_responses.py"),
        "--api-url", api_url,
        "--model", model,
        "--api-key", api_key,
        "--gold-only",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    print(result.stdout[-300:] if result.stdout else "")
    if result.returncode != 0:
        print(f"  [ERROR] {result.stderr[-200:]}")
        return False
    return True


def run_evaluation() -> dict:
    """Run evaluation and return per-language F1 scores."""
    from evaluate_gold import evaluate_gold_labels, print_report
    conn = get_connection()
    results = evaluate_gold_labels(conn, mode="auto")

    by_lang = defaultdict(list)
    for r in results:
        by_lang[r["language"]].append(r)

    scores = {}
    for lang in ["zh", "de", "en"]:
        items = by_lang.get(lang, [])
        if items:
            f1 = sum(i["f1"] for i in items) / len(items)
        else:
            f1 = 0.0
        scores[lang] = round(f1, 4)

    scores["overall"] = round(sum(r["f1"] for r in results) / len(results), 4)
    conn.close()
    return scores


def main():
    conn = get_connection()

    print(f"\n{'='*60}")
    print(f"  LinguaGraph — Multi-Model Benchmark")
    print(f"{'='*60}")

    results_table = {}

    # Bailian models
    if BAILIAN_KEY:
        for model in BAILIAN_MODELS:
            print(f"\n  [{model}] extracting...")
            clean_extractions(conn)
            ok = run_extraction(model, BAILIAN_URL, BAILIAN_KEY)
            if ok:
                scores = run_evaluation()
                results_table[model] = scores
                print(f"  [{model}] ZH={scores['zh']:.4f} DE={scores['de']:.4f} EN={scores['en']:.4f}")

    # Local LM Studio models
    for model, url in LOCAL_MODELS:
        print(f"\n  [{model}] (local)...")
        clean_extractions(conn)
        ok = run_extraction(model, url, "")
        if ok:
            scores = run_evaluation()
            results_table[model] = scores
            print(f"  [{model}] ZH={scores['zh']:.4f} DE={scores['de']:.4f} EN={scores['en']:.4f}")

    # Print final comparison table
    print(f"\n{'='*60}")
    print(f"  Model Comparison Results")
    print(f"{'='*60}")
    print(f"  {'Model':<30s} {'ZH F1':>8s} {'DE F1':>8s} {'EN F1':>8s} {'Overall':>8s}")
    print(f"  {'-'*30} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for model, scores in results_table.items():
        print(f"  {model:<30s} {scores['zh']:>8.4f} {scores['de']:>8.4f} {scores['en']:>8.4f} {scores['overall']:>8.4f}")

    conn.close()


if __name__ == "__main__":
    main()
