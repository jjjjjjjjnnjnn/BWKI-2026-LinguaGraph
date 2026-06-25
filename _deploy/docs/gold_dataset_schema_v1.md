# Gold Dataset V1 — Schema Specification

> **版本**: v1.0
> **状态**: 草稿
> **覆盖**: Dataset A (Concept Extraction) + Dataset C (Graph Completion)
> **数据源**: CognitiveSpace 知识图谱（574 节点, 3538 链接, 68 教材）

---

## 1. 通用约定

### 1.1 文件格式

- 存储格式：**JSONL**（每行一个独立 JSON 对象）
- 编码：UTF-8
- 命名：`{task_abbr}_{language}.jsonl`
  - 例：`ce_zh.jsonl`, `gc_en.jsonl`
- 分语言存储，保留跨语言训练的可能性

### 1.2 统一记录结构

每条记录遵循以下顶层结构：

```
{
  "id":          string,   // 全局唯一 ID
  "task":        string,   // 任务标识
  "language":    string,   // 语言代码: zh|en|de
  "source":      string,   // 数据来源: textbook|graph|synthetic
  "input":       object,   // 模型输入
  "output":      object,   // 标准答案
  "provenance":  object,   // 溯源信息（可选）
  "metadata":    object    // 扩展元数据（可选）
}
```

### 1.3 ID 生成规则

```
{task_abbr}_{6位序号}
```

- `ce` — Concept Extraction
- `gc` — Graph Completion
- 序号从 000001 开始，按语言独立编号

示例：`ce_zh_000001`, `gc_de_000042`

### 1.4 溯源字段格式

```
"provenance": {
  "textbook":   string,   // 教材名称
  "chapter":    string,   // 章节
  "section":    string,   // 小节（可选）
  "source_ids": string[], // 源概念 ID 列表
  "confidence": number,   // 置信度 [0, 1]
  "generated":  boolean,  // 是否自动生成（非人工标注）
}
```

溯源字段是可选但推荐的。BWKI 论文要求每条数据的来源可追溯。

---

## 2. Dataset A — Concept Extraction

### 2.1 任务定义

给定一段教材文本，输出该文本中出现的数学概念列表。

```
Text
 ↓
[概念1, 概念2, 概念3, ...]
```

### 2.2 记录格式

```
{
  "id":        "ce_zh_000001",
  "task":      "concept_extraction",
  "language":  "zh",
  "source":    "graph",              // 见 §2.4 数据来源
  "input": {
    "text":    "导数建立在极限概念之上，用于描述函数的变化率。"
  },
  "output": {
    "concepts": [
      "导数",
      "极限",
      "函数"
    ]
  },
  "provenance": {
    "textbook":   "人教版高中数学选修2-2",
    "chapter":    "第一章 导数及其应用",
    "section":    "1.1 变化率与导数",
    "source_ids": ["math_calculus_导数", "math_calculus_极限"],
    "confidence": 0.85,
    "generated":  true
  },
  "metadata": {
    "node_count":    2,
    "relation_type": "depends_on",
    "level":         "high"
  }
}
```

### 2.3 输出约束

```javascript
// output.concepts 约束
{
  // 必须
  "concepts": string[]  // 概念名称列表，长度 ≥ 1

  // 不要求
  // - 概念的位置标注（BIO/span）
  // - 概念的排序
  // - 重复概念去重
}
```

### 2.4 数据来源

| 来源 | 策略 | 覆盖 |
|------|------|------|
| **evidence 文本** | 从链接的 `evidence` 字段提取自然语句，关联 source/target 概念 | 3538 条链接 → ~3000 样本 |
| **教材映射** | 从 `cross_references` 构造教材章节 → 概念列表映射 | 574 节点 → ~800 样本 |
| **合成句** | 用模板从关系三元组生成："{A}{关系词}{B}（模板填充）" | 可扩展 |

### 2.5 文本生成策略（证据来源）

链接数据结构：

```json
{
  "source": "math_calculus_导数",
  "target": "math_calculus_极限",
  "type": "related_to",
  "evidence": "导数建立在极限概念之上",
  "importance": 0.8,
  "inferred": false
}
```

生成逻辑：
```
evidence_text = link.evidence
source_concept = node[link.source].name
target_concept = node[link.target].name
→ input.text = evidence_text
→ output.concepts = [source_concept, target_concept, ...同句其他概念]
```

注意：evidence 文本可能存在语言混用（证据文本与实际语言不符）。需要在生成时按 `link.source` 的语言分类。

---

## 3. Dataset C — Graph Completion

### 3.1 任务定义

给定一个概念和一个关系类型，预测与目标概念存在该关系的另一个概念。

```
(概念A, 关系R)
 ↓
概念B
```

### 3.2 变体

#### 3.2.1 Forward（正向预测）

```
{
  "id":        "gc_zh_000001",
  "task":      "graph_completion",
  "language":  "zh",
  "source":    "graph",
  "input": {
    "source":   "导数",
    "relation": "depends_on"
  },
  "output": {
    "target":   "极限"
  },
  "provenance": {
    "source_ids": ["math_calculus_导数", "math_calculus_极限"],
    "confidence": 0.92,
    "generated":  true
  }
}
```

#### 3.2.2 Reverse（反向预测）

```
{
  "id":        "gc_zh_000042",
  "task":      "graph_completion",
  "language":  "zh",
  "source":    "graph",
  "input": {
    "target":   "导数",
    "relation": "depended_by"
  },
  "output": {
    "source":   "极限"
  },
  "provenance": {
    "source_ids": ["math_calculus_极限", "math_calculus_导数"],
    "confidence": 0.85,
    "generated":  true
  }
}
```

#### 3.2.3 Multiple Choice（多项选择）

```
{
  "id":        "gc_zh_000100",
  "task":      "graph_completion_mcq",
  "language":  "zh",
  "source":    "graph",
  "input": {
    "question": "导数依赖哪个概念？",
    "choices": [
      "矩阵",
      "极限",
      "概率",
      "向量"
    ]
  },
  "output": {
    "answer_index": 1  // 正确答案在 choices 中的索引（0-based）
  },
  "provenance": {
    "source_ids": ["math_calculus_导数", "math_calculus_极限"],
    "confidence": 0.95,
    "generated":  true
  }
}
```

### 3.3 关系类型映射

图谱中的 `link.type` 需要映射到可读的关系标签：

| link.type | 关系标签 | 正向描述 | 反向标签 |
|-----------|---------|---------|---------|
| `depends_on` | `depends_on` | A 依赖 B | `depended_by` |
| `related_to` | `related_to` | A 与 B 相关 | `related_to` |
| `part_of` | `part_of` | A 是 B 的一部分 | `has_part` |
| `representation` | `represents` | A 表示 B | `represented_by` |
| `prerequisite` | `requires` | A 需要 B | `required_by` |
| 默认 | `related_to` | A 与 B 相关 | `related_to` |

### 3.4 负采样策略

Multiple Choice 的干扰项从同层级的其他概念中采样：

```javascript
function sampleDistractors(correctTarget, sourceNode, allNodes, count=3) {
    // 1. 从 same group + different level 采
    // 2. 如果不够，从 same level + different group 采
    // 3. 随机填充
    // 要求：distractor ≠ correctTarget, distractor ∉ neighbors(sourceNode)
}
```

### 3.5 关系重要性过滤

- `importance > 0.7` 的关系生成正向/反向样本
- `importance > 0.8` 的关系还生成 MC 样本
- `importance ≤ 0.6` 的推断关系不生成训练样本（可用于评估）

### 3.6 Graph Completion vs Extraction 对比

| 维度 | Graph Completion | Concept Extraction |
|------|-----------------|-------------------|
| 输入 | 概念 + 关系 | 自然文本 |
| 输出 | 概念/索引 | 概念列表 |
| 数据量 | ~7000 条 | ~3000 条 |
| 难度 | 低（直接映射） | 中（需要 NLP） |
| 信噪比 | 高 | 中 |

---

## 4. 质量控制

### 4.1 自动过滤规则

```
□ 过滤 self-loop 边（source === target）
□ 过滤 importance < 0.3 的关系
□ 过滤 labels 中缺少对应语言的节点
□ 过滤 evidence 文本长度 < 5 字符
□ 过滤 MC 中干扰项与正确答案相同的情况
```

### 4.2 抽样验证流程

```
生成后 → 每语言随机抽 50 条 → 人工检查 → 报告准确率
```

### 4.3 去重

- 对 `input.text` 完全相同的 Concept Extraction 样本去重
- 对 `(source, relation, target)` 完全相同的 Graph Completion 样本去重

---

## 5. 文件结构

```
gold/
├── dataset_schema_v1.md              # 本文件
├── metadata.json                      # 数据统计摘要
├── ce_zh.jsonl                        # 中文概念抽取
├── ce_en.jsonl                        # 英文概念抽取
├── ce_de.jsonl                        # 德文概念抽取
├── gc_zh.jsonl                        # 中文图补全
├── gc_en.jsonl                        # 英文图补全
├── gc_de.jsonl                        # 德文图补全
└── mc_zh.jsonl                        # 中文多项选择（可选）
    mc_en.jsonl
    mc_de.jsonl
```

---

## 6. 数据规模预估

| 数据集 | 语言 | 预估样本数 |
|--------|------|-----------|
| Concept Extraction | ZH | ~1200 |
| Concept Extraction | EN | ~1000 |
| Concept Extraction | DE | ~800 |
| Graph Completion | ZH | ~2500 |
| Graph Completion | EN | ~2000 |
| Graph Completion | DE | ~1500 |
| Multiple Choice | ZH | ~800 |
| **总计** | **3 语言** | **~9800** |

---

## 7. 冻结条件

Schema v1 在所有以下条件满足时冻结：
- [ ] Dataset A 格式通过人工审查
- [ ] Dataset C 三种变体格式通过人工审查
- [ ] 溯源字段结构最终确定
- [ ] ID 命名规范确认
- [ ] 质量控制规则确认
- [ ] 文件结构确认

冻结后如需修改，必须更新版本号（v1.1, v1.2, ...）并记录变更日志。
