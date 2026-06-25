# Evidence Milestones — 证据生产路线图

> 冻结所有新功能开发。未来只做一件事：产出证据。

---

## E1: 教材知识图谱对比 ✅

**目标**：证明不同教育体系组织同一概念的方式不同
**状态**：已完成
**产出**：`data/evidence/curriculum_comparison_zh_de.json`
**内容**：
- 中国（人教版）vs 德国（Abitur）微积分课程对比
- 10 个核心概念 + 10 条关系 × 2 套课程
- 4 个结构性差异维度
- 3 个概念漂移案例

---

## E2: 不可译概念分析 ✅

**目标**：证明跨语言认知结构差异
**状态**：已完成
**产出**：`data/evidence/untranslatable_concepts.json`
**内容**：6 个不可译概念（孝/面子/缘分/Schadenfreude/Fernweh/Heimat）
- 每个概念的中德英认知图谱
- MCL 分析：每种语言平均丢失 2-3 个核心组件
- 关键发现：概念图结构差异显著

---

## E3: Wikipedia 跨语言对比 ✅

**目标**：用公开数据证明概念定义结构差异
**状态**：已完成
**产出**：`data/evidence/wikipedia_comparison.json`
**内容**：导数/积分/极限的中德英维基百科对比
- 定义结构差异
- 强调重点差异
- 对 MCL 的影响分析

---

## E4: Gold Dataset 扩展 → 50 条

**目标**：建立可靠的 Ground Truth
**状态**：待开始
**产出**：`data/gold/gold_dataset_v1.json`
**计划**：
- 从现有 20 条扩展到 50 条
- 每种语言至少 15 条
- 覆盖 easy/medium/hard 三个难度
- 双标注员验证（Kappa > 0.7）

---

## E5: 真实学生数据（5 人试点）

**目标**：第一批真实证据
**状态**：等待伙伴收集
**产出**：`data/students/student_001.json` ... `student_005.json`
**计划**：
- 中文 2 人 + 德语 2 人 + 英语 1 人
- 每人回答 v3 问卷（9 题）
- LLM 自动提取 → 人工校验

---

## E6: LLM vs Human 对比

**目标**：证明 MCL 检测的有效性
**状态**：等 E4 + E5 完成
**产出**：`data/results/extraction_validation.json`
**计划**：
- 用 Gold Dataset 计算 Concept F1 / Relation F1
- 用真实学生数据计算 MCL Precision / Recall
- 生成统计报告

---

## E7: 失败案例库

**目标**：记录系统局限性（BWKI 评委喜欢）
**状态**：部分完成（5 案例）
**产出**：`data/failure_cases/README.md`
**计划**：
- 扩展到 15-20 个案例
- 按类型分类：FORM/CASE/SEMA/MISS/REL
- 分析失败原因和改进方向

---

## 时间线

```
Week 1 (6/17-6/23):  E1✅ E2✅ E3✅ + E4(Gold 50)
Week 2 (6/24-6/30):  E5(5人试点) + E6(F1计算)
Week 3 (7/1-7/7):    E7(失败案例) + E6(MCL验证)
Week 4 (7/8-7/14):   统计报告 + 可视化
```

---

## 关键指标（BWKI 提交时必须有）

| 指标 | 目标值 | 当前值 |
|------|--------|--------|
| Gold Dataset | 50+ 条 | 20 条 |
| 真实学生数据 | 20+ 人 | 0 人 |
| Cohen's Kappa | > 0.7 | 未计算 |
| Concept F1 | > 0.80 | 0.74 (mock) |
| Relation F1 | > 0.70 | 0.41 (mock) |
| MCL F1 | > 0.60 | 未计算 |
| 失败案例 | 15+ 个 | 5 个 |
