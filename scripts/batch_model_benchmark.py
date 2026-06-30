#!/usr/bin/env python3
"""
batch_model_benchmark.py — 阿里云 DashScope 批量模型评估

120 models × 92 gold items, 两阶段筛选策略。
在 Fig 5 Panel C 中产出论文级模型基准排行榜。

使用方法:
  export BAILIAN_API_KEY=sk-...
  python scripts/batch_model_benchmark.py --stage discover   # 发现可用模型
  python scripts/batch_model_benchmark.py --stage screen     # 阶段1: 快速筛选
  python scripts/batch_model_benchmark.py --stage full       # 阶段2: 完整评估
  python scripts/batch_model_benchmark.py --stage report     # 生成排行榜
"""

import json, os, re, sys, time, glob
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent

BAILIAN_API_KEY = os.environ.get("BAILIAN_API_KEY", "")
API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"

GOLD_PATH = PROJECT / "data" / "gold" / "gold_dataset.json"
MODEL_LIST_PATH = PROJECT / "config" / "model_list.txt"
OUT_DIR = PROJECT / "data" / "model_comparison"
OUT_DIR.mkdir(parents=True, exist_ok=True)

EXTRACT_PROMPT_TEMPLATE = """从以下文本中提取关键概念及其关系。

任务：提取 10-20 个核心概念，并按以下 JSON Schema 输出：

{{
  "topic": "[topic]",
  "language": "[lang]",
  "concepts": [
    {{
      "name": "概念名称（原始语言）",
      "category": "核心概念/相关概念/具体事例",
      "related_concepts": ["相关概念1", "相关概念2"],
      "definition_snippet": "一句话定义"
    }}
  ],
  "relations": [
    {{"source": "概念A", "target": "概念B", "type": "隶属于/导致/对立/相关"}}
  ]
}}

文本内容：
{text}"""


def discover_models():
    """通过 DashScope API 发现可用文本生成模型."""
    import requests
    headers = {"Authorization": f"Bearer {BAILIAN_API_KEY}"}
    resp = requests.get(f"{API_BASE}/models", headers=headers, timeout=30)
    raw = resp.json()
    # DashScope returns {"data": [...]} or {"data": {"models": [...]}}
    data = raw.get("data", raw)
    if isinstance(data, dict):
        models = data.get("models", data.get("list", []))
    elif isinstance(data, list):
        models = data
    else:
        models = []

    text_models = []
    for m in models:
        if isinstance(m, str):
            text_models.append(m)
            continue
        mid = m.get("id", m.get("model_id", ""))
        if not mid:
            continue
        # Filter: keep only text/chat models, skip embedding/audio/vision
        skip = ["embed", "audio", "vision", "image", "tts", "whisper", "rerank"]
        if any(s in mid.lower() for s in skip):
            continue
        text_models.append(mid)

    with open(MODEL_LIST_PATH, "w", encoding="utf-8") as f:
        for mid in sorted(text_models):
            f.write(mid + "\n")

    print(f"[discover] Found {len(text_models)} text generation models")
    print(f"[discover] Saved to {MODEL_LIST_PATH}")
    return text_models


def load_gold_items(n_items=None):
    """加载 gold 数据集, 可选截取前 n 条用于快速筛选."""
    d = json.loads(GOLD_PATH.read_text(encoding="utf-8"))
    # gold_dataset.json is a flat list of items
    if isinstance(d, list):
        items = d
    elif isinstance(d, dict):
        items = d.get("items", d.get("results", d.get("data", [])))
    else:
        items = []
    # Normalize: extract gold_concepts from human_labels if present
    for item in items:
        if "gold_concepts" not in item:
            hl = item.get("human_labels", {})
            item["gold_concepts"] = hl.get("concepts", []) if isinstance(hl, dict) else []
    if n_items:
        items = items[:n_items]
    print(f"[gold] Loaded {len(items)} items" + (f" (first {n_items})" if n_items else ""))
    return items


def evaluate_model(model_name, items):
    """对单个模型运行概念提取, 计算 F1, 保存结果."""
    import requests

    total_p, total_r, total_f1 = 0.0, 0.0, 0.0
    n_valid = 0
    failed = 0
    failed_items = []

    headers = {
        "Authorization": f"Bearer {BAILIAN_API_KEY}",
        "Content-Type": "application/json",
    }

    for item in items:
        sample_id = item.get("sample_id", item.get("id", "unknown"))
        text = item.get("text", item.get("content", ""))
        gold = set(item.get("gold_concepts", item.get("concepts", [])))

        if not text or not gold:
            continue

        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "你是概念提取专家。输出严格 JSON 格式。概念名称使用原始语言，禁止 ASCII 编码。输出 UTF-8 中文。"},
                {"role": "user", "content": EXTRACT_PROMPT_TEMPLATE.format(text=text[:2000])},
            ],
            "temperature": 0.1,
            "max_tokens": 2048,
        }

        try:
            resp = requests.post(
                f"{API_BASE}/chat/completions",
                headers=headers, json=payload, timeout=60,
            )
            result = resp.json()

            if "choices" not in result:
                failed += 1
                failed_items.append(sample_id)
                continue

            content = result["choices"][0]["message"]["content"]

            json_match = re.search(r"\{.*\}", content, re.DOTALL)
            if not json_match:
                failed += 1
                failed_items.append(sample_id)
                continue

            extracted = json.loads(json_match.group())
            predicted = {c.get("name", "") for c in extracted.get("concepts", []) if c.get("name", "")}

            if not predicted:
                failed += 1
                failed_items.append(sample_id)
                continue

            tp = len(gold & predicted)
            prec = tp / max(len(predicted), 1)
            rec = tp / max(len(gold), 1)
            f1 = 2 * prec * rec / max(prec + rec, 0.001)

            total_p += prec
            total_r += rec
            total_f1 += f1
            n_valid += 1

        except Exception as e:
            failed += 1
            failed_items.append(sample_id)

        time.sleep(0.3)  # rate limit

    n_total = len(items)
    result = {
        "model": model_name,
        "run_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_items": n_total,
        "valid": n_valid,
        "failed": failed,
        "encoding_errors": 0,
        "failed_items_sample": failed_items[:10],
        "summary": {
            "mean_f1": round(total_f1 / max(n_valid, 1), 4),
            "mean_precision": round(total_p / max(n_valid, 1), 4),
            "mean_recall": round(total_r / max(n_valid, 1), 4),
        },
    }

    safe_name = model_name.replace("/", "_").replace(":", "_")
    out_path = OUT_DIR / f"batch_{safe_name}_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    status = f"F1={result['summary']['mean_f1']:.4f}  valid={n_valid}/{n_total}  failed={failed}"
    print(f"    {status}")
    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description="DashScope 120-model concept extraction benchmark")
    parser.add_argument("--stage", choices=["discover", "screen", "full", "report"], required=True)
    parser.add_argument("--n-screen", type=int, default=5, help="筛选阶段每模型样本数")
    parser.add_argument("--model", type=str, default=None, help="仅评估单个模型 (调试用)")
    args = parser.parse_args()

    if args.stage == "discover":
        discover_models()
        return

    if not BAILIAN_API_KEY:
        print("ERROR: BAILIAN_API_KEY 环境变量未设置")
        sys.exit(1)

    if args.stage == "screen":
        if not MODEL_LIST_PATH.exists():
            print(f"模型列表不存在, 先运行 --stage discover")
            return
        models = [m.strip() for m in MODEL_LIST_PATH.read_text(encoding="utf-8").splitlines() if m.strip()]
        if args.model:
            models = [args.model]

        items = load_gold_items(n_items=args.n_screen)
        print(f"[screen] Evaluating {len(models)} models on {len(items)} items...")

        for i, model in enumerate(models):
            print(f"  [{i+1}/{len(models)}] {model}...", end="")
            evaluate_model(model, items)

    elif args.stage == "full":
        pattern = str(OUT_DIR / "batch_*_results.json")
        screen_results = sorted(glob.glob(pattern))
        if not screen_results:
            print("未找到筛选结果, 先运行 --stage screen")
            return

        passed = []
        for fpath in screen_results:
            d = json.loads(open(fpath, encoding="utf-8").read())
            f1 = d["summary"]["mean_f1"]
            if f1 >= 0.3:
                passed.append(d["model"])

        if args.model:
            passed = [args.model]

        items = load_gold_items()
        print(f"[full] Evaluating {len(passed)} models (F1>=0.3) on {len(items)} items...")

        for i, model in enumerate(passed):
            existing = OUT_DIR / f"batch_{model.replace('/', '_').replace(':', '_')}_results.json"
            if existing.exists():
                old = json.loads(existing.read_text(encoding="utf-8"))
                if old.get("total_items", 0) >= 50:
                    print(f"  [{i+1}/{len(passed)}] {model}...SKIP (already complete)")
                    continue
            print(f"  [{i+1}/{len(passed)}] {model}...", end="")
            evaluate_model(model, items)

    elif args.stage == "report":
        results = []
        for fpath in sorted(glob.glob(str(OUT_DIR / "batch_*_results.json"))):
            d = json.loads(open(fpath, encoding="utf-8").read())
            if d["valid"] >= 5:
                results.append(d)

        results.sort(key=lambda x: -x["summary"]["mean_f1"])

        print(f"\n=== MODEL BENCHMARK ({len(results)} models) ===\n")
        print(f"{'Rank':<5} {'Model':<45} {'F1':<8} {'Prec':<8} {'Recall':<8} {'N':<5}")
        print("-" * 80)
        for i, r in enumerate(results, 1):
            s = r["summary"]
            print(f"{i:<5} {r['model'][:45]:<45} {s['mean_f1']:<8.4f} {s['mean_precision']:<8.4f} {s['mean_recall']:<8.4f} {r['valid']:<5}")

        rank_path = PROJECT / "outputs" / "figures" / "model_benchmark_full.json"
        json.dump(results, open(rank_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"\n[saved] {rank_path}")


if __name__ == "__main__":
    main()
