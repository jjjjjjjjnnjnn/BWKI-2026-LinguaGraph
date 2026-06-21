# LinguaGraph — 假设检验结果模板

> **用途**: 数据来后直接运行统计检验，填入结果
> **原理**: LDS Bootstrap (1000 iterations) → Mixed ANOVA → post-hoc

---

## H1: 跨语言存在认知差异

**原假设 H0**: LDS = 0 (跨语言认知图相同)

**检验**: 单样本 t-test (LDS vs 0)

| 语言对 | 平均 LDS | SD | t | df | p | Cohen's d | 95% CI | 结论 |
|--------|:--------:|:-:|:-:|:-:|:-:|:--------:|:------:|:----:|
| ZH-DE | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ZH-EN | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DE-EN | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

> 预期: LDS 显著 > 0，H0 被拒绝

---

## H2: 语言对间 LDS 存在差异

**原假设 H0**: 所有语言对的平均 LDS 相等

**检验**: Mixed ANOVA (3 语言组 × 5 主题)

| 来源 | SS | df | MS | F | p | η² |
|------|:--:|:--:|:--:|:-:|:-:|:--:|
| 语言组 (between) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 主题 (within) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 语言组 × 主题 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 误差 | ⬜ | ⬜ | ⬜ | | | |

**Post-hoc (Tukey HSD)**:

| 对比 | 差 | SE | t | p-tukey |
|------|:-:|:-:|:-:|:-------:|
| ZH-DE vs ZH-EN | ⬜ | ⬜ | ⬜ | ⬜ |
| ZH-DE vs DE-EN | ⬜ | ⬜ | ⬜ | ⬜ |
| ZH-EN vs DE-EN | ⬜ | ⬜ | ⬜ | ⬜ |

---

## H3: 概念漂移在不同主题间不一致

**原假设 H0**: 所有主题的 LDS 相等

**检验**: Repeated Measures ANOVA 或 Friedman Test (非正态时)

| 主题 | Mean LDS | SD | 与其他主题显著不同? |
|------|:--------:|:--:|:------------------:|
| 自由 (freedom) | ⬜ | ⬜ | ⬜ |
| 正义 (justice) | ⬜ | ⬜ | ⬜ |
| 责任 (responsibility) | ⬜ | ⬜ | ⬜ |
| 成功 (success) | ⬜ | ⬜ | ⬜ |
| 家庭 (family) | ⬜ | ⬜ | ⬜ |

---

## H4: Human LDS ≈ Simulation LDS

**原假设 H0**: 人类 LDS 与模型模拟 LDS 无差异

**检验**: 独立样本 t-test 或 Mann-Whitney U (非正态时)

| 指标 | Human LDS (n=60) | Model LDS (n=300) | 差异 | t / U | p | d / r |
|------|:----------------:|:-----------------:|:----:|:-----:|:-:|:-----:|
| 平均 LDS | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ZH-DE LDS | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ZH-EN LDS | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DE-EN LDS | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

---

## H5: Inter-Annotator Agreement (κ > 0.70)

**检验**: Cohen's Kappa

| 标注维度 | κ | 标准误 | z | p | 结论 |
|----------|:-:|:------:|:-:|:-:|:----:|
| 概念提取 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 关系提取 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| 质量评级 | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

> 目标: κ ≥ 0.70 (概念), ≥ 0.65 (关系)

---

## 多重比较校正

| 比较组 | 比较数 | 校正方法 | 校正后 α |
|--------|:------:|:---------:|:--------:|
| LDS by 语言对 × 主题 | 15 | BH-FDR | q = 0.05 |
| Post-hoc 语言对比 | 3 | Tukey HSD | α' = 0.05 |
| 主题对比 | 10 | Bonferroni | α' = 0.005 |

---

## 统计功效验证

| 检验 | 所需 n | 实际 n | 达到的功效 | 最小可检测效应量 |
|------|:------:|:------:|:---------:|:--------------:|
| Mixed ANOVA (组间) | 18/组 | ⬜ | ⬜ | f = 0.25 |
| 单样本 t-test | ⬜ | ⬜ | ⬜ | d = ⬜ |
| 独立样本 t-test | ⬜ | ⬜ | ⬜ | d = ⬜ |

---

## 运行命令

数据来后执行:

```bash
# LDS 批量计算
python scripts/analyze_student.py --all

# Bootstrap CI
python -c "from src.scoring import bootstrap_lcd_ci; ..."

# Human vs Simulation 对比
python scripts/compare_human_vs_model.py

# 标注一致性
python scripts/annotator_agreement.py
```

---

*模板版本: v1.0 | 2026-06-17*
