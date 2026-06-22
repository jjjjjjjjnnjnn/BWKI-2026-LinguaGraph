#!/usr/bin/env python3
"""Comprehensive BaiLian model benchmark — test ALL free-quota models on 20 gold labels."""

import json, re, sqlite3, sys, time
from collections import defaultdict
from openai import OpenAI
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from evaluate_gold import compute_f1

API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
API_KEY = "***"

# ALL models with free quota (skip VL, test everything)
MODELS = [
    # Original working models
    "qwen-turbo", "qwen-plus", "qwen-plus-latest", "qwen-max",
    # NEW from user's list
    "qwen3.7-plus",
    "qwen3.7-max-2026-05-17",
    "qwen3.6-plus",
    "qwen3.6-flash-2026-04-16",
    "qwen3-30b-a3b",
    "qwen-plus-2025-07-28",
    "qwen-plus-2025-01-25",
    "qwen-math-turbo",
    "qwen-mt-flash",
    "qwen-mt-lite",
    "qwen-coder-plus",
    "qwen-coder-turbo",
    # Third-party
    "deepseek-r1-distill-qwen-7b",
    "glm-5",
    "glm-4.5",
    "glm-4.6",
]

# Skip VL models (test if they even work for text)
VL_MODELS = {"qwen3-vl-235b-a22b-thinking", "qwen3-vl-32b-thinking", "qwen3-vl-30b-a3b-thinking", "qwen3-vl-plus", "qwen-omni-turbo"}

def load_gold_data():
    conn = sqlite3.connect(str(Path(__file__).parent.parent / "linguaGraph.db"))
    conn.text_factory = bytes
    items = conn.execute("""
        SELECT gl.response_id, gl.concepts, r.answer_text, r.language
        FROM gold_labels gl JOIN responses r ON gl.response_id = r.response_id
        ORDER BY r.language
    """).fetchall()
    conn.close()
    return items

def test_model(model, items):
    client = OpenAI(base_url=API_URL, api_key=API_KEY, max_retries=2)
    examples = {
        "zh": '{"concepts": ["自由", "责任"]}',
        "en": '{"concepts": ["freedom", "responsibility"]}',
        "de": '{"concepts": ["Freiheit", "Verantwortung"]}',
    }
    results = []

    for item in items:
        resp_id = item[0].decode("utf-8")
        gold_c = json.loads(item[1].decode("utf-8"))
        text = item[2].decode("utf-8") if item[2] else ""
        lang = item[3].decode("utf-8")
        example = examples.get(lang, examples["en"])

        try:
            system_msg = "你是概念提取助手。只输出JSON。"
            if any(v in model for v in ["glm"]):
                system_msg = "你是一个概念提取器。只输出JSON。"

            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": f"{example}\n\nText: {text}\n\n提取概念为JSON格式。"},
                ],
                temperature=0.3, max_tokens=256, timeout=30,
            )
            raw = resp.choices[0].message.content or ""
        except Exception as e:
            results.append({"lang": lang, "f1": 0.0, "note": str(e)[:80]})
            continue

        cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        try:
            pred_c = json.loads(match.group()).get("concepts", []) if match else []
        except:
            pred_c = []

        gold_set = set(c.strip().lower() for c in gold_c)
        pred_set = set(c.strip().lower() for c in pred_c if c and c.strip())
        metrics = compute_f1(gold_set, pred_set)
        results.append({"lang": lang, "f1": metrics["f1"], "resp_id": resp_id, "gold": gold_c, "pred": pred_c})

    return results

gold_items = load_gold_data()
all_results = {}
errors = {}

for model in MODELS:
    print(f"\n=== {model} ===", flush=True)
    t0 = time.time()

    try:
        results = test_model(model, gold_items)
        elapsed = time.time() - t0

        by_lang = defaultdict(list)
        for r in results:
            by_lang[r["lang"]].append(r)

        scores = {}
        for lang in ["zh", "de", "en"]:
            items_l = by_lang.get(lang, [])
            f1_vals = [i["f1"] for i in items_l]
            scores[lang] = round(sum(f1_vals) / len(f1_vals), 4) if f1_vals else 0.0
        scores["overall"] = round(sum(i["f1"] for i in results) / len(results), 4) if results else 0.0
        scores["time"] = round(elapsed, 1)
        all_results[model] = scores

        print(f"  ZH={scores['zh']:.4f}  DE={scores['de']:.4f}  EN={scores['en']:.4f}  Overall={scores['overall']:.4f}  ({elapsed:.0f}s)")

    except Exception as e:
        errors[model] = str(e)[:100]
        print(f"  FAILED: {e}")

# Final table
print("\n" + "=" * 90)
print(f"{'Model':<35s} {'ZH F1':>8s} {'DE F1':>8s} {'EN F1':>8s} {'Overall':>8s} {'Time':>6s}")
print("-" * 90)
for model in MODELS + list(VL_MODELS):
    if model in all_results:
        s = all_results[model]
        print(f"{model:<35s} {s['zh']:>8.4f} {s['de']:>8.4f} {s['en']:>8.4f} {s['overall']:>8.4f} {s['time']:>5.0f}s")
    elif model in errors:
        print(f"{model:<35s} {'FAILED':>30s}")
    elif model not in all_results:
        print(f"{model:<35s} {'SKIPPED':>30s}")

# Save results
out_path = Path(__file__).parent.parent / "research" / "findings" / "bailian_benchmark_complete.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"results": all_results, "errors": errors}, f, ensure_ascii=False, indent=2)
print(f"\nSaved to {out_path}")
