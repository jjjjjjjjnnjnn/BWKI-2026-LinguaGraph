# LinguaGraph — 结果目录

> **用途**: 存放论文级别的结果数据、图表和统计报告
> **状态**: ⏳ 等待人类实验数据

---

## 目录

| 路径 | 内容 | 状态 |
|------|------|------|
| `figure_templates.md` | 5 张论文图表的规格说明 | ✅ 已准备 |
| `paper_results_template.md` | 结果表格模板 (Table 1-4, Figure 1-5) | ✅ 已准备 |
| `hypothesis_results_template.md` | 假设检验框架 (H1-H5) | ✅ 已准备 |
| `findings/` | 语料分析发现 (Pilot 阶段) | ✅ 已有 |

---

## 数据来后的处理流程

```bash
# 1. 导入数据
python participant_data/import.py --input raw/survey_export.csv

# 2. 匿名化
python participant_data/anonymize.py --batch pilot_001

# 3. 批量运行 Pipeline
python scripts/analyze_student.py --all

# 4. 生成论文图表
python scripts/bwki_analysis.py --all-figures

# 5. 概念提取评估
python evaluation/extractor_benchmark.py --all

# 6. 标注一致性
python scripts/annotator_agreement.py
```

---

*最后更新: 2026-06-17*
