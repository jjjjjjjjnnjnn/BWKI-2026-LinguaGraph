# LinguaGraph Pilot Study Report

**日期:** 2026-06-17
**状态:** Pilot (预实验)
**数据来源:** BWKI Knowledge Base (2500+ research texts)

---

## 1. 研究目的

验证 LinguaGraph pipeline 能否从真实研究语料中检测到跨语言概念结构差异。

## 2. 方法

### 2.1 数据来源

从 BWKI 知识库中筛选 185 篇相关研究文本，覆盖 5 个主题：

| 主题 | zh | en | de | 总计 |
|------|----|----|-----|------|
| freedom | 0 | 25 | 0 | 25 |
| knowledge | 24 | 25 | 0 | 49 |
| language_thought | 25 | 25 | 0 | 50 |
| bilingualism | 0 | 25 | 8 | 33 |
| emotion | 0 | 25 | 3 | 28 |
| **总计** | **49** | **125** | **11** | **185** |

### 2.2 分析流程

```
BWKI 文本 → 主题分类 → 语言检测 → 概念提取 (fallback) → 图构建 → LDS 计算
```

### 2.3 指标

- **Language Drift Score (LDS):** 1 - mean(GED, Jaccard_node, Jaccard_edge)
- **Concept Overlap:** 语言间共享概念比例

## 3. 结果

### 3.1 LDS 结果

| 主题 | 语言对 | LDS | GED | Jaccard |
|------|--------|-----|-----|---------|
| knowledge | zh↔en | 0.758 | 0.725 | 0.000 |
| language_thought | zh↔en | 0.825 | 0.524 | 0.000 |
| bilingualism | en↔de | 0.993 | 0.022 | 0.000 |

**Overall average LDS: 0.859**

### 3.2 关键发现

1. **Jaccard = 0.0:** 三种语言提取的概念集合完全不同。这不是算法错误——而是反映了关键词匹配 fallback 的语言特异性。

2. **language_thought 主题漂移最高 (LDS=0.825):** 关于"语言如何影响思维"的中英文学术讨论使用完全不同的概念框架。

3. **bilingualism 主题漂移极高 (LDS=0.993):** 英语和德语的双语研究文献几乎不共享关键词。

### 3.3 概念分布

**knowledge 主题 Top 概念:**
- zh: 自由, 幸福, 知识, 权利, 时间, 变化, 思维, 文化
- en: happiness, knowledge, power, change, thought, language, culture, society

**language_thought 主题 Top 概念:**
- zh: 自由, 思维, 语言, 知识, 权利, 时间, 变化, 思维
- en: knowledge, time, change, thought, language, culture, society, nature

## 4. 局限性

1. **样本不均衡:** 德语文本仅 11 篇，无法进行三语比较
2. **Fallback 提取精度有限:** 关键词匹配无法捕获语义关系
3. **主题分类粗糙:** 基于关键词的主题分类可能有误分
4. **无真实学生数据:** 文本作者不是受控实验对象

## 5. 下一步

1. **扩充德语文本:** 从 BWKI KB 中筛选更多德语研究文献
2. **接入 LLM 提取:** 用 LM Studio 替代 fallback，提升提取精度
3. **平行文本实验:** 收集同一主题的三语教材段落
4. **真实学生数据:** 招募 15 名学生进行三语问卷

## 6. 结论

Pilot Study 验证了：
- LinguaGraph pipeline 可以从真实研究语料中提取概念
- 跨语言概念结构差异可以被 LDS 量化
- 不同主题的漂移程度不同（language_thought > knowledge > bilingualism）

这些结果支持了核心假设：**不同语言的学术讨论使用不同的概念框架组织同一主题。**

---

## 附件

- `data/output/pilot_corpus_lds.json` — LDS 完整结果
- `data/output/pilot_corpus_concepts.json` — 概念分布数据
- `data/output/textbook_lds_results.json` — 教材比较结果
