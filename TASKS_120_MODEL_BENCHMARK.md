# 阿里云 120 模型全规模基准测试 — 执行方案

## 目标

在阿里云 DashScope/Bailian 上批量测试所有可用文本生成模型在概念提取任务上的 F1 表现，产生论文级别的模型基准排行榜。

## 为什么这很重要

| 当前状态 | 如果完成 120 模型 |
|----------|------------------|
| Fig 5 Panel C: 仅 2 个模型 (qwen) | → 120 模型的完整分布 + 排名 |
| 论文可宣称: "LDS 在 2 个模型上稳定" | → 可宣称: "LDS 在 XX 个模型上一致" |
| 无模型比较的说服力 | → **单篇论文最大规模的 LLM 概念提取基准** |

## 策略: 两阶段筛选 (节省 70% 调用)

### 阶段 1: 快速筛选 (约 600 次 API 调用)
- **对所有 120 个模型**, 用 5 个代表性 gold 样本 (覆盖 ZH/EN/DE) 测试
- 计算粗 F1 → 淘汰 F1 < 0.3 的模型
- 预期: 约 40-60 个模型通过筛选

### 阶段 2: 完整评估 (约 5000 次 API 调用)
- 对通过筛选的模型, 用全部 N=92 gold 样本测试
- 计算精确 F1
- 输出完整排行榜

### 总调用量 ~5600 次, 远低于 120×92=11040

## 代码准备

```python
#!/usr/bin/env python3
"""
batch_model_benchmark.py — 阿里云 DashScope 批量模型评估

使用方法:
  python batch_model_benchmark.py --stage screen    # 阶段 1: 快速筛选 (5 items × 120 models)
  python batch_model_benchmark.py --stage full      # 阶段 2: 完整评估 (92 items × passed models)
  python batch_model_benchmark.py --stage report    # 生成排行榜
"""

import json, os, sys, time, glob
from pathlib import Path

PROJECT = Path("C:/Users/rongj/Desktop/学校/BWKI-2026-备战")

# API 配置
BAILIAN_API_KEY = os.environ.get("BAILIAN_API_KEY", "")
API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# Gold 数据集
GOLD_PATH = PROJECT / "data" / "gold" / "gold_dataset.json"

# 提取提示词 (需与已有实验一致)
EXTRACT_PROMPT = """从以下文本中提取关键概念及其关系。

任务：提取 10-20 个核心概念，并按以下 JSON Schema 输出：

{
  "topic": "[topic]",
  "language": "[lang]",
  "concepts": [
    {
      "name": "概念名称（原始语言）",
      "category": "核心概念/相关概念/具体事例",
      "related_concepts": ["相关概念1", "相关概念2"],
      "definition_snippet": "一句话定义"
    }
  ],
  "relations": [
    {"source": "概念A", "target": "概念B", "type": "隶属于/导致/对立/相关"}
  ]
}

文本内容：
{text}
"""

# 模型列表文件
MODEL_LIST_PATH = PROJECT / "config" / "model_list.txt"  # 每行一个模型名


def discover_models():
    """列出 DashScope 上可用的文本生成模型."""
    # 通过 API 查询可用模型
    import requests
    headers = {"Authorization": f"Bearer {BAILIAN_API_KEY}"}
    resp = requests.get(f"{API_BASE}/models", headers=headers)
    models = resp.json().get("data", {}).get("models", [])
    
    # 只保留文本生成模型
    text_models = []
    for m in models:
        mid = m.get("model_id", "")
        capabilities = m.get("capabilities", {})
        # 检查是否支持文本生成
        if capabilities.get("text_generation") or capabilities.get("chat"):
            text_models.append(mid)
    
    # 写入文件
    with open(MODEL_LIST_PATH, "w", encoding="utf-8") as f:
        for mid in sorted(text_models):
            f.write(mid + "\n")
    
    print(f"Discovered {len(text_models)} text generation models")
    return text_models


def load_gold_items(n_items=None):
    """加载 gold 数据集."""
    d = json.load(open(GOLD_PATH, encoding="utf-8"))
    items = d.get("items", d.get("results", d.get("data", [])))
    if n_items:
        items = items[:n_items]
    return items


def evaluate_model(model_name, items):
    """对单个模型运行概念提取并计算 F1."""
    import requests
    from collections import Counter
    
    total_precision = 0
    total_recall = 0
    total_f1 = 0
    n_valid = 0
    failed = 0
    failed_items = []
    
    headers = {
        "Authorization": f"Bearer {BAILIAN_API_KEY}",
        "Content-Type": "application/json"
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
                {"role": "system", "content": "你是概念提取专家。输出严格 JSON 格式。"},
                {"role": "user", "content": EXTRACT_PROMPT.format(text=text[:2000])}
            ],
            "temperature": 0.1,
            "max_tokens": 2048,
        }
        
        try:
            resp = requests.post(
                f"{API_BASE}/chat/completions",
                headers=headers, json=payload, timeout=60
            )
            result = resp.json()
            
            if "choices" not in result:
                failed += 1
                failed_items.append(sample_id)
                continue
            
            content = result["choices"][0]["message"]["content"]
            
            # 解析 JSON
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if not json_match:
                failed += 1
                failed_items.append(sample_id)
                continue
            
            extracted = json.loads(json_match.group())
            predicted = {c.get("name", "") for c in extracted.get("concepts", [])
                        if c.get("name", "")}
            
            if not predicted:
                failed += 1
                failed_items.append(sample_id)
                continue
            
            # 计算 F1
            tp = len(gold & predicted)
            precision = tp / max(len(predicted), 1)
            recall = tp / max(len(gold), 1)
            f1 = 2 * precision * recall / max(precision + recall, 0.001)
            
            total_precision += precision
            total_recall += recall
            total_f1 += f1
            n_valid += 1
            
        except Exception as e:
            failed += 1
            failed_items.append(sample_id)
        
        # Rate limit
        time.sleep(0.3)
    
    result = {
        "model": model_name,
        "total_items": len(items),
        "valid": n_valid,
        "failed": failed,
        "failed_items": failed_items[:10],
        "summary": {
            "mean_f1": round(total_f1 / max(n_valid, 1), 4),
            "mean_precision": round(total_precision / max(n_valid, 1), 4),
            "mean_recall": round(total_recall / max(n_valid, 1), 4),
        }
    }
    
    # 保存中间结果
    out_dir = PROJECT / "data" / "model_comparison"
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_name = model_name.replace("/", "_").replace(":", "_")
    out_path = out_dir / f"batch_{safe_name}_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["discover", "screen", "full", "report"], required=True)
    parser.add_argument("--n-screen", type=int, default=5, help="Screening sample size")
    args = parser.parse_args()
    
    if args.stage == "discover":
        models = discover_models()
        print(f"Found {len(models)} models. Saved to {MODEL_LIST_PATH}")
        return
    
    if not BAILIAN_API_KEY:
        print("ERROR: BAILIAN_API_KEY not set")
        return
    
    if args.stage == "screen":
        models = [m.strip() for m in open(MODEL_LIST_PATH) if m.strip()]
        items = load_gold_items(n_items=args.n_screen)
        print(f"Screening {len(models)} models on {len(items)} items...")
        
        for i, model in enumerate(models):
            print(f"  [{i+1}/{len(models)}] {model}...")
            result = evaluate_model(model, items)
            print(f"    F1={result['summary']['mean_f1']:.4f}, failed={result['failed']}")
    
    elif args.stage == "full":
        # 读取所有 screen 结果, 筛选 F1 > 0.3 的模型
        screen_dir = PROJECT / "data" / "model_comparison"
        passed = []
        for f in sorted(screen_dir.glob("batch_*_results.json")):
            d = json.load(open(f, encoding="utf-8"))
            if d["summary"]["mean_f1"] >= 0.3:
                passed.append(d["model"])
        
        print(f"Full evaluation for {len(passed)} models (screened from screening)...")
        items = load_gold_items()
        
        for i, model in enumerate(passed):
            print(f"  [{i+1}/{len(passed)}] {model}...")
            result = evaluate_model(model, items)
            print(f"    F1={result['summary']['mean_f1']:.4f}")
    
    elif args.stage == "report":
        results = []
        for f in sorted(Path("data/model_comparison").glob("batch_*_results.json")):
            d = json.load(open(f, encoding="utf-8"))
            if d["valid"] >= args.n_screen or d["valid"] >= 50:  # full eval has ~92 valid
                results.append(d)
        
        results.sort(key=lambda x: -x["summary"]["mean_f1"])
        
        print(f"\n=== MODEL BENCHMARK ({len(results)} models) ===\n")
        print(f"{'Rank':<5} {'Model':<40} {'F1':<8} {'Prec':<8} {'Recall':<8} {'N':<5}")
        print("-"*75)
        for i, r in enumerate(results, 1):
            s = r["summary"]
            print(f"{i:<5} {r['model'][:40]:<40} {s['mean_f1']:<8.4f} {s['mean_precision']:<8.4f} {s['mean_recall']:<8.4f} {r['valid']:<5}")
        
        # 保存排行榜
        rank_path = PROJECT / "outputs" / "figures" / "model_benchmark_full.json"
        with open(rank_path, "w", encoding="utf-8") as f:
            json.dump(rank_results, f, ensure_ascii=False, indent=2)
        print(f"\nSaved to {rank_path}")


if __name__ == "__main__":
    main()
```

## 给 mimo code 的 prompt

```
请执行阿里云 120 模型概念提取基准测试。

## 步骤

1. 先运行 `discover` 阶段发现可用模型:
   python batch_model_benchmark.py --stage discover

2. 运行 `screen` 阶段快速筛选:
   python batch_model_benchmark.py --stage screen --n-screen 5

3. 查看结果, 筛选 F1 >= 0.3 的模型

4. 对通过的模型运行完整评估:
   python batch_model_benchmark.py --stage full

5. 生成排行榜:
   python batch_model_benchmark.py --stage report

## 输出

- `data/model_comparison/batch_{model}_results.json` — 每个模型的完整结果
- `outputs/figures/model_benchmark_full.json` — 合并排行榜

## 注意事项

- 使用环境变量 BAILIAN_API_KEY
- 每两次调用之间 sleep 0.3 秒避免限流
- 模型名可能包含 "/", 保存文件时替换为 "_"
- 只评估文本生成/对话模型
- JSON 解析使用正则匹配 `{...}` 块, 可以处理模型输出中的多余文本
```

要不要我现在就把这个脚本写到项目里？
