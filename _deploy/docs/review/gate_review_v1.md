# LinguaGraph — Gate Review 完整风险矩阵

> **审查日期**: 2026-06-17 (Research Audit Day)
> **审查范围**: 5 层并行审计（科学方法 / 统计 / 复现性 / 伦理合规 / BWKI评委视角）
> **项目阶段**: 进入人类实验前的 Gate Review

---

## 总览

| 指标 | 数值 |
|------|------|
| 总风险数 | 25 |
| CRITICAL | 6 |
| HIGH | 9 |
| MEDIUM | 8 |
| LOW | 2 |
| 阻塞 Gate（CRITICAL + 影响提交） | 3 |

---

## 1. CRITICAL 风险（6项）

| # | 风险 | 层 | 影响 | 修复成本 | 是否阻塞 Gate |
|---|------|---|------|----------|-------------|
| C1 | **Google Forms 收集未成年人数据违反 GDPR** | L4 | 德国学校当局不会批准实验；违反 GDPR Art. 28/44。需替换为自托管方案或纸质问卷 | High | **✅ 是** |
| C2 | **LDS 无方差估计，无法做推断统计** | L2 | 核心指标只有点估计。无法判断 LDS 值是否有显著差异；无法回答研究问题 | High | **✅ 是** |
| C3 | **统计功效虚标——n=30 实际功效不足** | L2 | README 声称 d=0.6-0.8 @80%，实际最小可检测效应量为 d≈1.14。实验结果将无法解释 | Medium | **✅ 是** |
| C4 | **概念映射有研究者偏见** | L1 | 30 个概念 ID 是研究者预设的。`cross_language_mapping.json` 中 公平 同时映射到 equality 和 justice，已在编码结论 | Medium | 否* |
| C5 | **无真实被试数据（0/30）** | L5 | 从评委视角看：没有人类数据 = 没有科学结论。核心实验未开始 | N/A | 否（这是计划中的） |
| C6 | **教科书语料 15 文件无版权声明** | L4 | 可能是原文摘录却无来源/许可证，若提交含此内容则构成侵权 | Low | 否（不用于提交） |

> *C4 是根本性问题但修复成本高 —— 需用数据驱动方法替代人工映射。建议比赛后修复。

---

## 2. HIGH 风险（9项）

| # | 风险 | 层 | 影响 | 修复成本 |
|---|------|---|------|----------|
| H1 | **LDS 实现与文档不一致** | L1 | `scoring.py` 只算边 Jaccard，文档声明 GED + 节点Jaccard + 边Jaccard | Low |
| H2 | **训练语料三重污染** | L1 | Wikipedia→LLM→Simulation 同一来源，语料 99.7% 英文，LDS 排序被训练数据不平衡主导 | High |
| H3 | **问卷建构效度——无控制题无协变量** | L1 | 无法区分语言影响 vs 教育水平 vs 文化知识 | Medium |
| H4 | **Human vs Simulation 数据泄漏** | L1 | 提示词明确要求产生假设中的文化刻板印象 | Medium |
| H5 | **统计检验未实现** | L2 | "t-test, ANOVA, post-hoc Tukey" 写在论文大纲，代码不存在 | Medium |
| H6 | **Cohen's Kappa 代码有 bug** | L2 | `annotation_guideline_v2.md:467-481` 传到 `cohen_kappa_score` 的 2D 向量会报错 | Low |
| H7 | **多重比较未校正** | L2 | 15 组比较族系错误率 53.7%，无 Bonferroni/FDR | Low |
| H8 | **复现性评分 D——第三方无法复现** | L3 | `load_expert_graph()` 崩溃、测试文件引用不存在数据、`main.py` 无 mock 模式 | Medium |
| H9 | **README Quick Start 缺少关键步骤** | L3 | 未说明 Python 版本、venv、API Key、mock 模式、DB 初始化 | Low |

---

## 3. MEDIUM 风险（8项）

| # | 风险 | 层 | 修复成本 |
|---|------|---|----------|
| M1 | 模拟提示词编码文化刻板印象 | L1 | Medium |
| M2 | 年龄范围自相矛盾（13-18 vs 16-19 vs 13-15） | L4 | Low |
| M3 | 德文同意书法律精度不足（缺 Schulbehörde、Datenschutzbeauftragter） | L4 | Low |
| M4 | 数据删除机制仅存于文档未实现 | L4 | Low |
| M5 | Pilot 数据集文件缺许可证（60+ 文件） | L4 | Medium |
| M6 | 依赖描述不完整（4 个 phantom 依赖） | L3 | Low |
| M7 | 测试套件覆盖率不足（19 测试，4/6 文件非 pytest） | L3 | Medium |
| M8 | 无概念提取错误分析 | L5 | Medium |

---

## 4. 综合 Gate 判定

### ❌ Gate 未通过 — 进入人类实验前必须修复 3 个阻塞项

```
C1 — Google Forms + 未成年人数据违反 GDPR
     ↓
     替换为自托管问卷或纸质问卷
     ↓
     预计成本：2-3 天

C2 — LDS 无方差估计
     ↓
     实现 Bootstrap 置信区间
     ↓
     预计成本：1 天

C3 — n=30 统计功效不足
     ↓
     重新计算所需样本量，或调整实验设计
     ↓
     预计成本：1 天
```

### 建议的非阻塞修复（高优先级）

```
H1 — LDS 实现与文档对齐：1 小时
H6 — 修复 Cohen's Kappa 代码 bug：1 小时
H8 — 添加 mock 模式、修复测试文件：2 小时
H9 — 补全 README：30 分钟
M2 — 统一年龄范围：30 分钟
M3 — 补全同意书字段：30 分钟
M4 — 实现数据删除脚本：1 小时
```

---

## 5. BWKI 评委最可能提的 10 个问题

来自 L5 审计，按杀伤力排序：

| # | 问题 | 杀伤力 | 对应风险 |
|---|------|--------|----------|
| 1 | "你们用了多少个真实被试？" | 🛑 毁灭性 | C5 |
| 2 | "LDS 和随机噪声有什么区别？" | 🛑 毁灭性 | C2 |
| 3 | "你们怎么知道是语言差异不是文化差异？" | 🔴 严重 | H3 |
| 4 | "样本量 30 够检验你们的假设吗？" | 🔴 严重 | C3 |
| 5 | "为什么不用 Google Forms？" | 🔴 严重 | C1 |
| 6 | "概念映射是谁做的？有标注者间一致性吗？" | 🔴 严重 | C4, H6 |
| 7 | "模拟数据和真人数据的区别？" | 🟡 中等 | H4 |
| 8 | "这个结果换一台电脑能复现吗？" | 🟡 中等 | H8 |
| 9 | "和其他指标比 LDS 优势在哪？" | 🟡 中等 | H1 |
| 10 | "你引用了 Wikipedia 文章——版权没问题？" | 🟢 轻微 | C6 |

---

## 6. 项目完成度修正后评估

| 模块 | 原估值 | 修正后 | 原因 |
|------|--------|--------|------|
| 核心管道 Pipeline | 90% | 80% | `load_expert_graph()` 崩溃，mock 模式缺失 |
| LDS 指标 | 90% | 60% | 实现与文档不一致，无方差估计，无基线对比 |
| 可视化 Visualization | 75% | 75% | 不变（未审计） |
| 问卷 Questionnaire | 95% | 70% | 无控制题，无人口学协变量，建构效度未验证 |
| 伦理合规 Ethics | 100% | 60% | Google Forms 致命问题，年龄矛盾，同意书缺字段 |
| 版本控制 GitHub | 100% | 70% | 复现性不足，文档缺失关键步骤 |
| 人类数据 Human Data | 5% | 5% | 不变（计划中的） |

---

*本报告由 5 层并行审计合成。各层完整报告见：*
- `docs/review/gate_review_layer1_scientific.md`
- `docs/review/gate_review_layer2_statistical.md`
- `docs/review/gate_review_layer3_reproducibility.md`
- `docs/review/gate_review_layer4_ethics.md`
- `docs/review/gate_review_layer5_bwki_judge.md`
