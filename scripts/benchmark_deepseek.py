#!/usr/bin/env python3
"""
benchmark_deepseek.py — Run concept extraction benchmark on DeepSeek.

Usage:
    export DEEPSEEK_API_KEY=sk-...
    python scripts/benchmark_deepseek.py
"""

import json, os, re, sys, time, urllib.request
from pathlib import Path

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
if not API_KEY:
    print("ERROR: DEEPSEEK_API_KEY env var not set")
    sys.exit(1)

PROJECT = Path(__file__).resolve().parent.parent
API_URL = "https://api.deepseek.com/chat/completions"
GOLD_PATH = PROJECT / "data/gold/gold_dataset.json"
OUT_DIR = PROJECT / "data/model_comparison"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPT = """从以下文本中提取关键概念。输出严格JSON格式:
{{"concepts": [{{"name": "概念名称"}}]}}
概念名称使用原始语言UTF-8。禁止ASCII编码。
文本: {text}"""


def evaluate_model(model_name="deepseek-chat", max_items=None):
    d = json.load(open(GOLD_PATH, encoding="utf-8"))
    items = d if isinstance(d, list) else d.get("items", d.get("results", d.get("data", [])))
    if max_items:
        items = items[:max_items]

    total_f1, total_p, total_r = 0, 0, 0
    n_valid, failed = 0, 0
    failed_items = []

    for item in items:
        sid = item.get("sample_id", "?")
        text = item.get("text", "")
        gold = set(item.get("human_labels", {}).get("concepts", []))
        if not text or not gold:
            continue

        payload = json.dumps({
            "model": model_name,
            "messages": [
                {"role": "system", "content": "你是概念提取专家。输出严格JSON格式。概念名称使用原始语言，UTF-8，禁止ASCII编码。"},
                {"role": "user", "content": PROMPT.format(text=text[:2000])},
            ],
            "temperature": 0.1,
            "max_tokens": 1024,
        }).encode()

        try:
            req = urllib.request.Request(API_URL, data=payload, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            })
            resp = json.loads(urllib.request.urlopen(req, timeout=60).read())
            content = resp["choices"][0]["message"]["content"]

            match = re.search(r"\{.*\}", content, re.DOTALL)
            if not match:
                failed += 1
                failed_items.append(sid)
                continue

            extracted = json.loads(match.group())
            pred = {c["name"] for c in extracted.get("concepts", []) if c.get("name")}
            if not pred:
                failed += 1
                failed_items.append(sid)
                continue

            tp = len(gold & pred)
            prec = tp / max(len(pred), 1)
            rec = tp / max(len(gold), 1)
            f1 = 2 * prec * rec / max(prec + rec, 0.001)

            total_f1 += f1
            total_p += prec
            total_r += rec
            n_valid += 1

        except Exception as e:
            failed += 1
            failed_items.append(sid)

        time.sleep(0.2)

    result = {
        "model": model_name,
        "run_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_items": len(items),
        "valid": n_valid,
        "failed": failed,
        "failed_items_sample": failed_items[:10],
        "summary": {
            "mean_f1": round(total_f1 / max(n_valid, 1), 4),
            "mean_precision": round(total_p / max(n_valid, 1), 4),
            "mean_recall": round(total_r / max(n_valid, 1), 4),
        },
    }

    safe_name = model_name.replace("/", "_").replace(":", "_")
    out_path = OUT_DIR / f"deepseek_{safe_name}_results.json"
    json.dump(result, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n=== DONE: {model_name} ===")
    print(f"  F1={result['summary']['mean_f1']:.4f}, valid={n_valid}/{len(items)}, failed={failed}")
    print(f"  Saved to {out_path}")
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="deepseek-chat", help="Model name (e.g. deepseek-chat, deepseek-reasoner)")
    parser.add_argument("--max-items", type=int, default=None, help="Limit items for quick test")
    args = parser.parse_args()
    evaluate_model(args.model, args.max_items)
