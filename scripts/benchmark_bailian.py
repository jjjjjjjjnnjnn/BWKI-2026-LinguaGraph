#!/usr/bin/env python3
"""Complete BaiLian model benchmark — tests every accessible model on 20 gold labels."""

import json, re, sqlite3, sys
from collections import defaultdict
from openai import OpenAI
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from evaluate_gold import compute_f1

API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
API_KEY = "***"
MODELS = ["qwen-turbo", "qwen-plus", "qwen-plus-latest", "qwen-max", "qwen-omni-turbo"]

conn = sqlite3.connect(str(Path(__file__).parent.parent / "linguaGraph.db"))
conn.text_factory = bytes
gold_items = conn.execute("""
    SELECT gl.response_id, gl.concepts, r.answer_text, r.language
    FROM gold_labels gl JOIN responses r ON gl.response_id = r.response_id
    ORDER BY r.language
""").fetchall()
conn.close()

EXAMPLES = {
    "zh": '{"concepts": ["自由", "责任"]}',
    "en": '{"concepts": ["freedom", "responsibility"]}',
    "de": '{"concepts": ["Freiheit", "Verantwortung"]}',
}

all_results = {}

for model in MODELS:
    print(f"\n=== {model} ===")
    client = OpenAI(base_url=API_URL, api_key=API_KEY)
    per_item = []

    for item in gold_items:
        resp_id = item[0].decode()
        gold_c = json.loads(item[1].decode())
        text = item[2].decode() if item[2] else ""
        lang = item[3].decode()
        example = EXAMPLES.get(lang, EXAMPLES["en"])

        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是概念提取助手。只输出JSON。"},
                    {"role": "user", "content": f"{example}\n\nText: {text}\n\n提取概念为JSON格式。"},
                ],
                temperature=0.3,
                max_tokens=256,
                timeout=30,
            )
            raw = resp.choices[0].message.content.strip()
        except Exception as e:
            per_item.append({"lang": lang, "f1": 0.0, "note": str(e)[:60]})
            continue

        cleaned = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
        match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        try:
            pred_c = json.loads(match.group()).get("concepts", []) if match else []
        except:
            pred_c = []

        gold_set = set(c.strip().lower() for c in gold_c)
        pred_set = set(c.strip().lower() for c in pred_c if c and c.strip())
        metrics = compute_f1(gold_set, pred_set)
        per_item.append({"lang": lang, "f1": metrics["f1"], "resp_id": resp_id, "pred": pred_c, "gold": gold_c})

    # Aggregate
    by_lang = defaultdict(list)
    for r in per_item:
        by_lang[r["lang"]].append(r)

    scores = {}
    for lang in ["zh", "de", "en"]:
        items = by_lang.get(lang, [])
        f1_vals = [i["f1"] for i in items]
        scores[lang] = round(sum(f1_vals) / len(f1_vals), 4) if f1_vals else 0.0
    scores["overall"] = round(sum(i["f1"] for i in per_item) / len(per_item), 4)
    all_results[model] = scores

    print(f"  ZH={scores['zh']:.4f}  DE={scores['de']:.4f}  EN={scores['en']:.4f}  Overall={scores['overall']:.4f}")

# Final table
print("\n" + "=" * 70)
print(f"{'Model':<22s} {'ZH F1':>8s} {'DE F1':>8s} {'EN F1':>8s} {'Overall':>8s}")
print("-" * 70)
for model in MODELS:
    s = all_results[model]
    print(f"{model:<22s} {s['zh']:>8.4f} {s['de']:>8.4f} {s['en']:>8.4f} {s['overall']:>8.4f}")

# Save to file
out_path = Path(__file__).parent.parent / "research" / "findings" / "bailian_benchmark.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)
print(f"\nSaved to {out_path}")
