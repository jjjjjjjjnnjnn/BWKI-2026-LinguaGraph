#!/usr/bin/env python3
"""Force full evaluation for all screen-passed models."""
import json, sys, glob, os, re, time, requests
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
PROJECT = Path(__file__).resolve().parent.parent
API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"
API_KEY = os.environ["BAILIAN_API_KEY"]
GOLD = json.load(open(PROJECT / "data/gold/gold_dataset.json", encoding="utf-8"))
OUT = PROJECT / "data/model_comparison"

EXTRACT = '从以下文本中提取关键概念及其关系。\n任务：提取 10-20 个核心概念，并按以下 JSON Schema 输出：\n{{"topic":"[topic]","language":"[lang]","concepts":[{{"name":"概念名称","category":"核心概念/相关概念/具体事例","related_concepts":["相关概念"],"definition_snippet":"一句话定义"}}],"relations":[{{"source":"概念A","target":"概念B","type":"隶属于/导致/对立/相关"}}]}}\n文本内容：\n{text}'

models = [
    'MiniMax-M2.1', 'MiniMax-M2.5', 'codeqwen1.5-7b-chat',
    'qwen-flash-character', 'qwen-flash-character-2026-02-26',
    'qwen3.5-omni-flash', 'qwen3.5-omni-flash-2026-03-15',
    'qwen3.5-omni-plus', 'qwen3.5-omni-plus-2026-03-15',
    'tongyi-xiaomi-analysis-flash',
]

for mi, model in enumerate(models):
    safe = model.replace("/", "_").replace(":", "_")
    out_f = OUT / f"batch_{safe}_results.json"
    if out_f.exists():
        old = json.load(open(out_f, encoding="utf-8"))
        if old.get("total_items", 0) >= 90:
            print(f"  [{mi+1}/{len(models)}] {model}...SKIP ({old['total_items']} items)")
            continue

    print(f"  [{mi+1}/{len(models)}] {model}...", end=" ", flush=True)
    tp_sum = pr_sum = rc_sum = 0.0
    valid = failed = 0
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    for item in GOLD:
        text = item.get("text", "")
        gold = set(item.get("human_labels", {}).get("concepts", []))
        if not text or not gold:
            continue
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "你是概念提取专家。输出严格 JSON。概念用原始语言，禁止 ASCII 编码。"},
                {"role": "user", "content": EXTRACT.format(text=text[:2000])},
            ],
            "temperature": 0.1, "max_tokens": 2048,
        }
        try:
            resp = requests.post(f"{API_BASE}/chat/completions", headers=headers, json=payload, timeout=60)
            r = resp.json()
            if "choices" not in r:
                failed += 1; continue
            content = r["choices"][0]["message"]["content"]
            m = re.search(r"\{.*\}", content, re.DOTALL)
            if not m:
                failed += 1; continue
            ext = json.loads(m.group())
            pred = {c.get("name", "") for c in ext.get("concepts", []) if c.get("name", "")}
            if not pred:
                failed += 1; continue
            tp = len(gold & pred)
            p = tp / max(len(pred), 1)
            r2 = tp / max(len(gold), 1)
            f1 = 2 * p * r2 / (p + r2) if (p + r2) > 0 else 0
            tp_sum += p; pr_sum += r2; rc_sum += f1; valid += 1
        except:
            failed += 1
        time.sleep(0.3)

    n = len(GOLD)
    result = {
        "model": model, "run_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_items": n, "valid": valid, "failed": failed,
        "summary": {
            "mean_f1": round(rc_sum / max(valid, 1), 4),
            "mean_precision": round(tp_sum / max(valid, 1), 4),
            "mean_recall": round(pr_sum / max(valid, 1), 4),
        },
    }
    with open(out_f, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"F1={result['summary']['mean_f1']:.4f} valid={valid}/{n} failed={failed}")
