#!/usr/bin/env python3
"""
openrouter_screen.py — Screen 20 models on 5 items, then full eval on best.
Usage: export OPENROUTER_KEY=sk-...
"""
import json, os, re, sys, time, urllib.request
from pathlib import Path

API_KEY = os.environ.get("OPENROUTER_KEY", "")
if not API_KEY:
    print("ERROR: OPENROUTER_KEY env var not set")
    sys.exit(1)

PROJECT = Path(__file__).resolve().parent.parent
API_URL = "https://openrouter.ai/api/v1/chat/completions"
GOLD_PATH = PROJECT / "data/gold/gold_dataset.json"
OUT_DIR = PROJECT / "data/model_comparison"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPT = """从以下文本中提取关键概念。输出严格JSON格式:
{{"concepts": [{{"name": "概念名称"}}]}}
概念名称使用原始语言UTF-8。禁止ASCII编码。
文本: {text}"""

d = json.load(open(GOLD_PATH, encoding="utf-8"))
all_items = d if isinstance(d, list) else d.get("items", d.get("results", d.get("data", [])))

# Models to test: diverse providers, skip already-tested
ALREADY_TESTED = {"qwen-plus","qwen-max","deepseek-chat","deepseek-v4-pro","deepseek-v4-flash"}

MODELS = [
    # Anthropic
    "anthropic/claude-sonnet-4-6", "anthropic/claude-haiku-4-5",
    # OpenAI
    "openai/gpt-5.5-pro", "openai/gpt-chat-latest", "openai/gpt-mini-latest",
    # Google
    "google/gemini-3.5-flash", "google/gemini-3.1-flash-lite",
    # Qwen variants (not tested)
    "qwen/qwen3.7-plus", "qwen/qwen3.7-max", "qwen/qwen3.6-flash", "qwen/qwen3.5-plus-20260420",
    # Others
    "mistralai/mistral-medium-3-5", "z-ai/glm-5.2",
    "moonshotai/kimi-k2.7-code", "minimax/minimax-m3",
    "x-ai/grok-4.3", "cohere/north-mini-code:free",
    "meta-llama/llama-4-scout", "sakana/fugu-ultra",
]

def evaluate(model_name, items, label=""):
    total_f1, total_p, total_r = 0, 0, 0
    n_valid, failed = 0, 0
    for item in items:
        sid = item.get("sample_id", "?")
        text = item.get("text", "")
        gold = set(item.get("human_labels", {}).get("concepts", []))
        if not text or not gold: continue

        payload = json.dumps({
            "model": model_name,
            "messages": [
                {"role": "system", "content": "你是概念提取专家。输出严格JSON格式。概念名称使用原始语言UTF-8。"},
                {"role": "user", "content": PROMPT.format(text=text[:2000])},
            ],
            "temperature": 0.1, "max_tokens": 1024,
        }).encode()

        try:
            req = urllib.request.Request(API_URL, data=payload, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
                "HTTP-Referer": "https://lingua-graph.com",
            })
            resp = json.loads(urllib.request.urlopen(req, timeout=60).read())
            content = resp["choices"][0]["message"]["content"]
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if not match: failed += 1; continue
            extracted = json.loads(match.group())
            pred = {c["name"] for c in extracted.get("concepts", []) if c.get("name")}
            if not pred: failed += 1; continue
            tp = len(gold & pred)
            prec = tp / max(len(pred), 1)
            rec = tp / max(len(gold), 1)
            f1 = 2 * prec * rec / max(prec + rec, 0.001)
            total_f1 += f1; total_p += prec; total_r += rec; n_valid += 1
        except: failed += 1
        time.sleep(0.3)

    return {
        "model": model_name,
        "valid": n_valid, "failed": failed,
        "f1": round(total_f1 / max(n_valid,1), 4),
        "precision": round(total_p / max(n_valid,1), 4),
        "recall": round(total_r / max(n_valid,1), 4),
    }

# Stage 1: Screen all 20 models on 5 items
print("=== Stage 1: Screen 20 models on 5 items ===\n")
screen_items = all_items[:5]
results = []
for i, model_name in enumerate(MODELS):
    print(f"  [{i+1}/{len(MODELS)}] {model_name}...", end=" ", flush=True)
    r = evaluate(model_name, screen_items)
    results.append(r)
    print(f"F1={r['f1']:.4f}  valid={r['valid']}/{r['failed']}")

# Rank and save
results.sort(key=lambda x: -x["f1"])
print("\n=== Screen Results (ranked) ===")
for r in results:
    tag = " <<< PROMISING" if r["f1"] >= 0.5 else ""
    print(f"  {r['model']:45s} F1={r['f1']:.4f}  v={r['valid']}{tag}")

# Stage 2: Full eval on F1>=0.5 models
print("\n=== Stage 2: Full eval (N=92) on promising models ===\n")
promising = [r for r in results if r["f1"] >= 0.5]
for r in promising:
    print(f"  Running full eval: {r['model']}...", end=" ", flush=True)
    full = evaluate(r["model"], all_items)
    print(f"F1={full['f1']:.4f}  valid={full['valid']}/{len(all_items)}  failed={full['failed']}")

    safe_name = r["model"].replace("/", "_").replace(":", "_")
    out_path = OUT_DIR / f"or_{safe_name}_results.json"
    json.dump({
        "model": r["model"],
        "total_items": len(all_items),
        "valid": full["valid"],
        "failed": full["failed"],
        "summary": {"mean_f1": full["f1"], "mean_precision": full["precision"], "mean_recall": full["recall"]},
    }, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"    Saved to {out_path.name}")
