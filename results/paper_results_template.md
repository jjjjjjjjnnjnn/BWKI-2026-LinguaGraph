# LinguaGraph — 论文结果部分模板

> **用途**: 数据到后直接填入，无需额外分析
> **原则**: 不伪造数据，只搭建框架

---

## 1. Table 1: Participant Demographics

| 特征 | 中文组 (n=20) | 德语组 (n=20) | 英语组 (n=20) | 总计 (n=60) |
|------|:-------------:|:-------------:|:-------------:|:-----------:|
| 年龄 (M ± SD) | ⬜ | ⬜ | ⬜ | ⬜ |
| 女性 (%) | ⬜ | ⬜ | ⬜ | ⬜ |
| 在德国年数 (M ± SD) | ⬜ | ⬜ | ⬜ | ⬜ |
| 第三语言 (%) | ⬜ | ⬜ | ⬜ | ⬜ |
| 知情同意签署 | ✅ | ✅ | ✅ | ✅ |

---

## 2. Table 2: LDS by Language Group

| 语言对 | 中文-德语 | 中文-英语 | 德语-英语 | F(2,57) | p | η² |
|--------|:--------:|:--------:|:--------:|:-------:|:-:|:--:|
| 自由 (freedom) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 正义 (justice) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 责任 (responsibility) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 成功 (success) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 家庭 (family) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| **整体 (Overall)** | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

> 注: LDS = 1 − 边 Jaccard 相似度。Bootstrap 95% CI 使用 1000 次重采样。
> FDR Benjamini-Hochberg 校正应用于 15 组比较。

---

## 3. Table 3: Concept Extraction Quality

| 提取器 | 概念 Precision | 概念 Recall | 概念 F1 | 关系 F1 |
|--------|:-------------:|:----------:|:-------:|:-------:|
| Keyword 匹配 | 0.00 | 0.00 | 0.00 | 0.20 |
| CoCo-Ex (传统 NLP) | ⬜ | ⬜ | ⬜ | ⬜ |
| **LLM (LinguaGraph)** | ⬜ | ⬜ | ⬜ | ⬜ |

> 评估基于人工标注 Gold Dataset (n=20)。F1 = 2 × P × R / (P + R)。

---

## 4. Table 4: Hypothesis Testing Summary

| 假设 | 检验方法 | 结果 | 效应量 | 95% CI | 支持? |
|------|----------|:----:|:------:|:------:|:-----:|
| H1: LDS > 0 (跨语言存在认知差异) | 单样本 t-test | ⬜ | Cohen's d | ⬜ | ⬜ |
| H2a: ZH-DE > ZH-EN LDS | 独立样本 t-test | ⬜ | Cohen's d | ⬜ | ⬜ |
| H2b: ZH-DE > DE-EN LDS | 独立样本 t-test | ⬜ | Cohen's d | ⬜ | ⬜ |
| H3: LDS 在不同主题间不一致 | Repeated Measures ANOVA | ⬜ | η² | ⬜ | ⬜ |
| H4: Human LDS ≈ Simulation LDS | 独立样本 t-test | ⬜ | Cohen's d | ⬜ | ⬜ |

> 所有检验 α = 0.05，多重比较使用 Benjamini-Hochberg FDR 校正。

---

## 5. Figure 1: Cross-Language LDS Distribution

```
📊 figure1_lds_distribution.png

类型: 箱线图 (Box Plot)
X轴: 5 主题 (freedom, justice, responsibility, success, family)
Y轴: LDS (0.0 − 1.0)
颜色: 3 语言对 (ZH-DE / ZH-EN / DE-EN)
辅助: Bootstrap 95% CI whiskers
```

---

## 6. Figure 2: Human vs Simulation Comparison

```
📊 figure2_human_vs_simulation.png

类型: 散点图 + 回归线 (Scatter + Regression)
X轴: Model LDS (300 simulations)
Y轴: Human LDS (60 participants)
点色: 5 主题
辅助: y=x 参考线, Pearson r 标注
```

---

## 7. Figure 3: Top Drift Concepts (Bar Chart)

```
📊 figure3_top_drift_concepts.png

类型: 水平柱状图
Y轴: 30 个跨语言概念 (按 LDS 排序)
X轴: LDS
颜色: 3 语言 (ZH=红 / DE=蓝 / EN=绿)
辅助: Bootstrap CI error bars
```

---

## 8. Figure 4: Language × Topic Interaction

```
📊 figure4_language_topic_heatmap.png

类型: 热力图 (Heatmap)
X轴: 5 主题
Y轴: 3 语言组
颜色: 平均节点度数 / 概念重叠率
辅助: 标注显著差异
```

---

## 9. Figure 5: Cognitive City 展示

```
📊 figure5_cognitive_city.png

类型: Three.js 截图
内容: 三个并排的 Cognitive City
  中文城市 / 德语城市 / 英语城市
  相同概念 (freedom) 的不同建筑布局
```

---

## 10. 开放科学声明

```text
数据与代码可用性:
- 代码: https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph (MIT)
- 数据: 因 GDPR 和未成年人保护，原始回答不公开。
         匿名化 LDS 数据和统计分析见 Supplementary Materials。
- 分析管道: 完整端到端可复现 (见 README.md)
```

---

## 11. 检查清单

数据来后逐项确认：

- [ ] Table 1: 人口统计学 → 填入
- [ ] Table 2: LDS by 语言组 → Mixed ANOVA 运行
- [ ] Table 3: 概念提取质量 → `python evaluation/extractor_benchmark.py --extractor llm`
- [ ] Table 4: 假设检验 → t-test / ANOVA 运行
- [ ] Figure 1: 箱线图 → Python script 运行
- [ ] Figure 2: Human vs Simulation → 散点图生成
- [ ] Figure 3: Top Drift → 排序柱状图
- [ ] Figure 4: Language × Topic → 热力图
- [ ] Figure 5: Cognitive City → Mimo 截图

---

*模板版本: v1.0 | 2026-06-17*
