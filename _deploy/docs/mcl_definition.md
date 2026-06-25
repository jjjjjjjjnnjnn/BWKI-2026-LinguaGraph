# Missing Cognitive Links (MCL) 定义

## 正式定义

> **Missing Cognitive Link (MCL)**: 指在专家知识图谱中应存在，但在学习者估计知识图谱中缺失，并能够解释其错误表现的概念连接。

## 数学表示

```
MCL = E_expert - E_learner

其中：
- E_expert = 专家知识图谱中的边集合
- E_learner = 学习者估计知识图谱中的边集合
- MCL = 两个集合的差集
```

## MCL Score

```
MCL Score = |MCL| / |E_expert| × 100%

其中：
- |MCL| = 缺失连接数量
- |E_expert| = 专家图谱总边数
```

## 分级标准

| MCL Score | 等级 | 说明 |
|-----------|------|------|
| 0-20% | Complete | 知识完整 |
| 20-40% | Minor Gaps | 轻微缺口 |
| 40-60% | Moderate Gaps | 中等缺口 |
| 60%+ | Critical Gaps | 严重缺口 |

## 示例

```
专家图谱：
极限 → 导数定义 (prerequisite)
导数定义 → 导数 (part_of)
导数 → 变化率 (represents)
导数 → 切线斜率 (represents)
积分 → 导数 (inverse_of)
积分 → 面积 (represents)

总边数：6

学生图谱：
导数 → 变化率 (represents)

学生边数：1

MCL = 6 - 1 = 5条缺失
MCL Score = 5/6 = 83.3%
等级：Critical Gaps
```

## 评价指标

### 1. Concept Precision（概念准确率）
```
Precision = 正确提取的概念数 / AI提取的总概念数
```

### 2. Relation Precision（关系准确率）
```
Precision = 正确提取的关系数 / AI提取的总关系数
```

### 3. MCL Recall（缺失连接召回率）
```
Recall = AI找到的缺失连接数 / 真正的缺失连接数
```

### 4. Coverage（覆盖率）
```
Coverage = 学生概念数 / 专家概念数
```
