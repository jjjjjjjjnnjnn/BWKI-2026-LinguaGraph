# LinguaGraph 实验设计方案

> 基于 CCKG (Cultural Commonsense Knowledge Graph, EACL 2026) 方法论借鉴

## 1. 实验目标

验证核心假设：**不同语言是否会塑造不同的思维结构？**

## 2. 实验设计（借鉴 CCKG）

### 2.1 三语问卷设计

借鉴 CCKG 的 5 国跨文化比较方法，设计三语（中/德/英）开放式问题：

| 主题 | 中文问题 | Deutsche Frage | English Question |
|------|---------|----------------|------------------|
| 自由 | 什么是自由？ | Was ist Freiheit? | What is freedom? |
| 知识 | 知识和权力的关系是什么？ | Was ist die Beziehung zwischen Wissen und Macht? | What is the relationship between knowledge and power? |
| 时间 | 时间是线性的还是循环的？ | Ist die Zeit linear oder zirkulär? | Is time linear or circular? |
| 身份 | 什么定义了一个人的身份？ | Was definiert die Identität einer Person? | What defines a person's identity? |
| 社会 | 个人和社会的关系是什么？ | Was ist die Beziehung zwischen Individuum und Gesellschaft? | What is the relationship between individual and society? |

### 2.2 被试招募

| 组别 | 人数 | 语言 | 来源 |
|------|------|------|------|
| 中国学生 | 5 | 中文回答 | 德国学校的中国留学生 |
| 德国学生 | 5 | 德语回答 | 同校德国同学 |
| 英语学生 | 5 | 英语回答 | 国际学校/在线招募 |
| **总计** | **15** | | |

### 2.3 数据收集流程

```
1. 发放问卷（Google Forms / 纸质）
2. 每人回答 5 个问题（每题 3-5 句话）
3. 收集回答 → JSON 格式
4. 运行 extract_v2.py 提取概念
5. 运行 compare.py 计算 LDS
6. 运行 3D 可视化展示结果
```

## 3. 评估指标

### 3.1 概念提取质量

| 指标 | 定义 | 目标 |
|------|------|------|
| Concept Precision | 提取概念中人工标注的比例 | ≥ 70% |
| Concept Recall | 人工标注概念中被提取的比例 | ≥ 60% |
| Relation F1 | 关系提取的 F1 分数 | ≥ 50% |

### 3.2 跨语言比较

| 指标 | 定义 | 预期 |
|------|------|------|
| Language Drift Score (LDS) | 1 - mean(GED, Jaccard, Cosine) | 0.3-0.7 |
| Concept Overlap | 三语共有概念比例 | ≥ 30% |
| Conceptual Stability | 概念跨语言一致性 | 0.5-0.9 |

### 3.3 创新验证

| 创新点 | 验证方法 |
|--------|----------|
| 跨语言认知图比较 | LDS 在不同语言对上有显著差异 |
| LLM 概念提取一致性 | 三语提取的 Concept F1 差异 < 10% |
| Language Drift Score | LDS 与 Conceptualizer baseline 相关性 > 0.5 |

## 4. 时间线

| 日期 | 任务 | 产出 |
|------|------|------|
| 6/18 | 完善问卷 | 三语问卷定稿 |
| 6/19-20 | 招募被试 | 15 名学生 |
| 6/21-22 | 收集数据 | 75 份回答 |
| 6/23 | 运行 pipeline | LDS 结果 + 3D 可视化 |
| 6/24-25 | 分析结果 | 实验报告 |
| 6/26-27 | 撰写论文 | BWKI 提交材料 |
| 6/28 | **BWKI 创意提交** | **截止日** |

## 5. CCKG 方法论借鉴点

| CCKG 做法 | LinguaGraph 适配 |
|-----------|-----------------|
| 5 国跨文化比较 | 3 语言跨认知比较 |
| iterative prompt framework | 两阶段概念提取 |
| xNext/xEffect/xNeed 关系 | requires/causes/equivalent 关系 |
| 37K+ 英语推断链 | 三语概念对齐数据 |
| 语言特异性分析 | LDS 量化语言对思维的影响 |
