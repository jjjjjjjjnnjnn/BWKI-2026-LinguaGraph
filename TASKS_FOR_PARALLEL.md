# LinguaGraph — 并行任务说明（供 mimo code / 其他 AI 执行）

---

## 任务 1: 批量 Wikipedia 概念提取

### 目标
从 ZH/EN/DE 三种语言的 Wikipedia 页面中提取概念结构，用于 LDS 稳健性检验（Fig 4 消融实验中的 Wikipedia-only 条件）。

### 输入

**主题列表**（5 个社会主题，每个主题 3 种语言 = 15 个独立任务）：

| 主题 | ZH URL | EN URL | DE URL |
|------|--------|--------|--------|
| Freedom/自由/Freiheit | `https://zh.wikipedia.org/wiki/自由` | `https://en.wikipedia.org/wiki/Freedom` | `https://de.wikipedia.org/wiki/Freiheit` |
| Justice/正义/Gerechtigkeit | `https://zh.wikipedia.org/wiki/正义` | `https://en.wikipedia.org/wiki/Justice` | `https://de.wikipedia.org/wiki/Gerechtigkeit` |
| Responsibility/责任/Verantwortung | `https://zh.wikipedia.org/wiki/责任` | `https://en.wikipedia.org/wiki/Responsibility` | `https://de.wikipedia.org/wiki/Verantwortung` |
| Home/家/Heimat | `https://zh.wikipedia.org/wiki/家` | `https://en.wikipedia.org/wiki/Home` | `https://de.wikipedia.org/wiki/Heimat` |
| Success/成功/Erfolg | `https://zh.wikipedia.org/wiki/成功` | `https://en.wikipedia.org/wiki/Success` | `https://de.wikipedia.org/wiki/Erfolg` |

### 执行方法

对于每个 `(语言, 主题)` 对：

1. 获取 Wikipedia 页面的纯文本内容（跳过信息框、引用、目录）
2. 将文本输入概念提取 prompt（下方给出）
3. 保存结果为 JSON 到 `data/wikipedia_extractions/{topic}_{lang}.json`

### 概念提取 Prompt

```
从以下文本中提取关键概念及其关系。

任务：提取 10-20 个核心概念，并按以下 JSON Schema 输出：

{
  "topic": "{topic}",
  "language": "{lang}",
  "source_url": "{wikipedia_url}",
  "concepts": [
    {
      "name": "概念名称（原始语言）",
      "category": "核心概念/相关概念/具体事例",
      "related_concepts": ["相关概念1", "相关概念2"],
      "definition_snippet": "一句话定义"
    }
  ],
  "relations": [
    {
      "source": "概念A",
      "target": "概念B",
      "type": "隶属于/导致/对立/相关"
    }
  ]
}

文本内容：
{article_text}
```

### 输出格式

```json
{
  "topic": "freedom",
  "language": "zh",
  "source_url": "https://zh.wikipedia.org/wiki/自由",
  "extracted_at": "2026-06-29T...",
  "concepts": [...],
  "relations": [...]
}
```

保存到: `data/wikipedia_extractions/{topic}_{lang}.json`

---

## 任务 2: 多模型提取对比

### 目标
用不同 LLM 在相同的 92 条 gold 标准数据上运行概念提取，评估 LDS 对模型选择的敏感性（Fig 5 Panel C）。

### 输入
- `data/gold/gold_dataset.json`（92 条标注数据）
- 提取 prompt: `config/prompts/extract.md`

### 执行方法

每个模型为独立任务。模型列表：

| 任务 ID | 模型 | API |
|---------|------|-----|
| model_qwen_plus | qwen-plus (基线) | 已有 |
| model_qwen_max | qwen-max | 需 API |
| model_gpt4o_mini | gpt-4o-mini | 需 API |
| model_gpt4o | gpt-4o | 需 API |

### 输出
每个模型输出到 `data/model_comparison/{model_name}_results.json`，包含：

```json
{
  "model": "qwen-plus",
  "run_at": "2026-06-29T...",
  "total_items": 92,
  "results": [...]
}
```

### 评估方法
运行 `python scripts/evaluate_gold.py --results data/model_comparison/{model_name}_results.json` 计算 F1。

---

## 任务 3: LDS 消融条件计算

### 目标
从已有数据计算 Fig 4 所需的 4 种消融条件的 LDS 值。

### 输入
- `data/math_extractions/merged/aligned_data.json`
- `config/expert_graphs/{domain}.json`

### 条件（每个为独立任务）

| 条件 | 方法 | 预期 |
|------|------|------|
| `ablation_full` | 完整数据计算 LDS | 基线 |
| `ablation_no_lang` | 随机打乱语言标签后计算 LDS | LDS 应显著下降 |
| `ablation_random_graph` | 保持节点数，随机重连边（度分布不变） | LDS ≈ 0 |
| `ablation_wikipedia_only` | 仅用 Wikipedia 来源的概念计算 LDS | LDS 趋势与 full 一致 |

### 输出
每个条件输出到 `outputs/ablation/{condition}_lds.json`：

```json
{
  "condition": "ablation_full",
  "lds_values": {
    "ZH-EN": 0.934,
    "DE-EN": 0.938,
    "ZH-DE": 0.519
  },
  "run_at": "2026-06-29T..."
}
```

---

## 任务 4: 覆盖度分数重新计算

### 目标
重新计算 4 个教育体系（NRW/UK/US/CN）对每个概念组的覆盖度。

### 输入
- `config/expert_graphs/aligned_data.json`（对齐组）
- `config/expert_graphs/curriculum_*.json`（各体系课标图）

### 执行
对每个教育体系，计算其课标图与对齐概念组的交集比例。

### 输出
输出到 `config/expert_graphs/coverage_scores.json`：

```json
{
  "NRW": {"math": 0.34, "physics": 0.28, "chemistry": 0.15},
  "UK": {"math": 0.82, "science": 0.45},
  ...
}
```

---

## 优先级

| 任务 | 优先级 | 是否阻塞论文 |
|------|--------|-------------|
| 任务 1: Wikipedia 提取 | P1 | Fig 4 消融需要 |
| 任务 2: 多模型对比 | P1 | Fig 5 Panel C 需要 |
| 任务 3: 消融 LDS | **P0** | Fig 4 核心图 |
| 任务 4: 覆盖度 | P2 | Fig 6 需要 |

---

## 文件结构约束

所有输出文件必须放在以下位置（不要创建新目录）：

```
data/wikipedia_extractions/     ← 任务 1
data/model_comparison/          ← 任务 2
outputs/ablation/               ← 任务 3
config/expert_graphs/           ← 任务 4
```
