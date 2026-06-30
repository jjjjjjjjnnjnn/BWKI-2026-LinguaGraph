# LinguaGraph — 并行任务 第 2 轮 (修正 + 扩展)

> 背景: 第 1 轮并行任务全部完成, 但发现数据质量问题需要修正。本轮聚焦于修复和扩展。

---

## 任务 A: 模型对比重做 (N=92, UTF-8 编码)

### 问题

第 1 轮的 `data/model_comparison/` 有以下缺陷:
1. **仅 N=20** (需要 N=92 以匹配 gold 数据集)
2. **非 qwen 模型输出乱码** (GPT-4o 和 GPT-4o-mini 产生 "姒傚康A/姒傚康B/鏂归潰/鍏崇郴/鍥犵礌" 等伪概念)
3. **部分模型 F1 完全相同** (qwen-max 和 gpt-4o 都是 0.5408, 疑似共享评估管道错误)

### 要求

对 4 个模型 (qwen-plus, qwen-max, gpt-4o, gpt-4o-mini) 重新运行概念提取, 使用:

1. **输入**: `data/gold/gold_dataset.json` 的 N=92 条标注数据
2. **提取提示词**: `config/prompts/extract.md` (或等效的多语言概念提取提示词)
3. **编码**: UTF-8 输出, 无 GBK 转换
4. **输出格式**: 每模型一个 JSON 文件到 `data/model_comparison/{model_name}_results.json`

```json
{
  "model": "{model_name}",
  "run_at": "ISO-8601 timestamp",
  "total_items": 92,
  "summary": {
    "mean_f1": 0.0,
    "mean_precision": 0.0,
    "mean_recall": 0.0
  },
  "results": [
    {
      "sample_id": "zh_001",
      "language": "zh",
      "gold_concepts": ["导数", "变化率", "极限"],
      "predicted_concepts": ["导数", "变化率"],
      "precision": 1.0,
      "recall": 0.667,
      "f1": 0.8
    }
  ]
}
```

5. **编码修复**: 非 qwen 模型必须在提示词中强调 "输出原始中文/德文, 禁止使用 ASCII 编码替代"

6. **独立评估**: 每个模型的结果独立计算 precision/recall/F1, 不与任何其他模型共享评估管道

### 验证方法

运行后执行:
```bash
python -c "
import json
for fname in ['qwen-plus','qwen-max','gpt-4o','gpt-4o-mini']:
    d = json.load(open(f'data/model_comparison/{fname}_results.json', encoding='utf-8'))
    # 检查: total_items=92, results 长度=92
    # 检查: 无 '姒傚康' 或 '鏂归潰' 等乱码
    # 检查: 4 个模型的 F1 不完全相同
    # 检查: DE/EN 样本的 predicted_concepts 不包含中文伪概念
    print(f'{fname}: items={d[\"total_items\"]}, F1={d[\"summary\"][\"mean_f1\"]:.4f}')
    # 抽查 zh_001 的中文是否正确
    if fname == 'gpt-4o':
        zh = [r for r in d['results'] if r['sample_id']=='zh_001'][0]
        print(f'  zh_001 gold: {zh[\"gold_concepts\"]}')
        print(f'  zh_001 pred: {zh[\"predicted_concepts\"]}')
"
```

### 交付物

- `data/model_comparison/qwen-plus_results.json` (N=92)
- `data/model_comparison/qwen-max_results.json` (N=92)
- `data/model_comparison/gpt-4o_results.json` (N=92)
- `data/model_comparison/gpt-4o-mini_results.json` (N=92)

---

## 任务 B: 覆盖度重新计算 (课标→教材匹配)

### 问题

第 1 轮的 `coverage_all_curricula.json` 使用教材概念→课标概念匹配, 几乎 100%。
**正确方法**: 课标概念→教材概念匹配 (原 `coverage_scores.json` 的方法论)

具体而言:
- **错误方法** (mimo code): 教材有 197 个概念, 看多少出现在课标中 → 94-100%
- **正确方法** (原始): NRW 课标有 299 个概念, 看多少被教材覆盖 → 各学段 2.6%-23.7%

### 要求

对 4 个教育体系重新计算覆盖率:

1. **输入**:
   - 课标概念列表: `config/expert_graphs/curriculum_*.json` (NRW/UK/US/CN 课标定义)
   - 教材概念库: `config/expert_graphs/math_full.json` (197 个教材概念, 三语标注)

2. **方法**:
   - 对每个课标概念, 检查是否在教材中有对应概念 (通过 keyword matching + cross-language mapping)
   - Coverage Score = matched_curriculum_concepts / total_curriculum_concepts
   - 按学段 (stage) 分别计算

3. **输出格式**: 覆盖 `config/expert_graphs/coverage_scores.json`

```json
{
  "NRW": {
    "seki_erprobung": {"stage": "seki_erprobung", "curriculum_concepts": 58, "matched": 6, "coverage": 0.103},
    "overall": {"curriculum_concepts": 299, "matched": 37, "coverage": 0.124}
  },
  "UK": {
    "uk_ks1_y1": {"curriculum_concepts": 30, "matched": 15, "coverage": 0.50},
    "overall": {"curriculum_concepts": 397, "matched": 320, "coverage": 0.807}
  },
  "US": {
    "overall": {"curriculum_concepts": 2124, "matched": 1615, "coverage": 0.76}
  },
  "China": {
    "overall": {"curriculum_concepts": 120, "matched": 8, "coverage": 0.067}
  }
}
```

### 验证

- NRW overall coverage 应在 10-40% 范围内 (而非 94%)
- UK overall 应在 70-90% 范围内
- CN overall 应 < 15%
- 每个学段应有独立的 coverage 值

---

## 任务 C: Wikipedia 中文编码修复

### 问题

5 个中文 Wikipedia 文件 (`freedom_zh.json`, `justice_zh.json`, `home_zh.json`, `responsibility_zh.json`, `success_zh.json`) 中 `category` 和 `type` 字段出现编码错误:
- "鏍稿績姒傚康" ← 应该是 "核心概念"
- "闅跺睘浜? ← 应该是 "隶属于"
- "瀵圭珛" ← 应该是 "对立"
- "鐩稿叧" ← 应该是 "相关"

### 要求

1. 重新提取中文 Wikipedia 内容 (或直接修复编码)
2. 确保 `category` 字段使用正确的中文: "核心概念", "相关概念", "具体事例", "对立概念"
3. 确保 `type` 字段使用正确的中文: "隶属于", "导致", "对立", "相关", "represents", "relates_to"
4. 覆盖 `data/wikipedia_extractions/{topic}_zh.json` 文件

---

## 任务 D (可选项): 补充缺失的 Wikipedia 英文提取

第 1 轮有 3 个文件缺少英文版 (`home_zh.json` 被错误标记为 `language: en`, `justice_zh.json` 同样, `success_zh.json` 同样)

检查并修复 `data/wikipedia_extractions/` 中 language 字段与文件名不一致的问题:
- home_zh.json 的 language 应为 "zh" (不是 "en")
- justice_zh.json 的 language 应为 "zh" (不是 "en")
- responsibility_zh.json 的 language 应为 "zh" (不是 "en")
- success_zh.json 的 language 应为 "zh" (不是 "en")

---

## 优先级

| 任务 | 优先级 | 论文阻塞 | 预计工作量 |
|------|:------:|:--------:|:---------:|
| 任务 A: 模型对比重做 | **P0** | Fig 5 Panel C | 4 模型 × 92 items = 368 API 调用 |
| 任务 B: 覆盖度重算 | **P0** | Fig 6 + C4 | ~100 行 Python + 手工概念映射 |
| 任务 C: Wikipedia 编码修复 | P1 | Bonus fig | 5 文件重新提取 |
| 任务 D: Language 字段修复 | P2 | — | 5 文件 metadata 修复 |

---

## 文件约束

```
data/model_comparison/          ← 任务 A
config/expert_graphs/           ← 任务 B
data/wikipedia_extractions/     ← 任务 C, D
```

所有输出使用 UTF-8 编码。不要创建新目录。
