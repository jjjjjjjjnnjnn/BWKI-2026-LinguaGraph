# LinguaGraph — 论文图表模板

> **用途**: 数据来后直接运行脚本生成论文级别的图表
> **工具**: Python (matplotlib/seaborn) + Three.js 截图

---

## Figure 1: Cross-Language LDS Distribution

- **类型**: 箱线图 (Box Plot)
- **文件**: `results/figure1_lds_distribution.png`
- **数据**: `cross_language_analysis` 表
- **脚本**: `scripts/bwki_analysis.py --figure 1`
- **预期**: 展示 LDS 在 5 主题 × 3 语言对上的分布

```python
# 生成命令
python scripts/bwki_analysis.py --figure 1
```

---

## Figure 2: Human vs Simulation Comparison

- **类型**: 散点图 + 回归线
- **文件**: `results/figure2_human_vs_simulation.png`
- **数据**: `cross_language_analysis` 表 (source=human vs source=simulation)
- **脚本**: `scripts/compare_human_vs_model.py --plot`
- **预期**: y=x 对角线; 点越接近对角线说明模型越接近人类

---

## Figure 3: Top Drift Concepts

- **类型**: 水平柱状图
- **文件**: `results/figure3_top_drift_concepts.png`
- **数据**: `cross_language_analysis` 表按概念聚合
- **脚本**: `scripts/bwki_analysis.py --figure 3`
- **预期**: 30 个概念按 LDS 排序，展示最高/最低漂移概念

---

## Figure 4: Language × Topic Heatmap

- **类型**: 热力图
- **文件**: `results/figure4_language_topic_heatmap.png`
- **数据**: 各语言组在各主题上的概念重叠率
- **脚本**: `scripts/bwki_analysis.py --figure 4`

---

## Figure 5: Cognitive City 截图

- **类型**: Three.js 截图
- **文件**: `results/figure5_cognitive_city.png`
- **来源**: Mimo 的 Three.js 展示
- **要求**: 三个并排 Cognitive City，相同概念不同布局
