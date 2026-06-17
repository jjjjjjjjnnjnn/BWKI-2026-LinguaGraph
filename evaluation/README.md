# LinguaGraph — 评估框架

> **目的**: 对比不同概念提取方法的 F1，建立标准化评测基准
> **原则**: 不修改核心 Pipeline，只做外部对比评估
> **基于**: ConceptNet 关系分类法 + CoCo-Ex 提取基线

---

## 评测目标

| 对比维度 | Keyword | CoCo-Ex | LLM (LinguaGraph) |
|----------|:-------:|:-------:|:-----------------:|
| 概念提取 F1 | ⬜ | ⬜ | ⬜ |
| 关系提取 F1 | — | — | ⬜ |
| 多语言支持 | ✅ | ❌ 仅英语 | ✅ ZH/DE/EN |
| 速度 | ✅ 快 | 🟡 中等 | ❌ 需 API |
| 可离线 | ✅ | ✅ | ❌ |

## 使用方法

```bash
# 对比所有提取器
python evaluation/extractor_benchmark.py

# 只跑 LLM 提取器
python evaluation/extractor_benchmark.py --extractor llm

# 只跑 CoCo-Ex 基线
python evaluation/extractor_benchmark.py --extractor cocoex
```

## 数据集

使用 `data/gold/gold_dataset.json` 中的 20 条人工标注数据作为 Ground Truth。
