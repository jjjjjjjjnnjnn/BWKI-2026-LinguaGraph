# LinguaGraph — 项目数据字典 & Agent 协作指南

## 项目路径

| 别名 | 路径 |
|------|------|
| `$PROJECT_DIR` | `C:\Users\rongj\Desktop\学校\BWKI-2026-备战` |
| `$DATA_DIR` | `$PROJECT_DIR\data` |
| `$SCRIPTS_DIR` | `$PROJECT_DIR\scripts` |
| `$SRC_DIR` | `$PROJECT_DIR\src` |
| `$CONFIG_DIR` | `$PROJECT_DIR\config` |
| `$DOCS_DIR` | `$PROJECT_DIR\docs` |
| `$DB_PATH` | `$PROJECT_DIR\linguaGraph.db` |

## 数据库连接

```python
import sqlite3
DB_PATH = r"C:\Users\rongj\Desktop\学校\BWKI-2026-备战\linguaGraph.db"
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
```

## 数据字典

| 表名 | 行数 | 用途 |
|------|------|------|
| students | 3 | 参与者 |
| questionnaires | 3 | 三语问卷 |
| responses | 25 | 学生回答 |
| gold_labels | 20 | 人工标注 |
| extractions | 1 | LLM提取结果 |
| graphs | 1 | 认知图谱 |
| cross_language_analysis | 15 | LDS结果 |
| expert_graphs | 3 | 专家参考图谱 |
| evaluation_results | 0 | LLM评估指标 |
| research_expectations | 4 | 研究预期 |

## 关键脚本

| 脚本 | 功能 |
|------|------|
| `scripts/db_init.py` | 创建数据库 |
| `scripts/ingest_all.py` | 批量导入数据 |
| `scripts/analyze_student.py` | 单学生完整分析 |
| `scripts/analyze_pilot.py` | Pilot数据分析 |
| `scripts/annotator_agreement.py` | Cohen's Kappa |
| `scripts/simulate_baseline.py` | 300模拟基线 |
| `scripts/compare_human_vs_model.py` | 人类vs模型 |
| `scripts/bwki_analysis.py` | BWKI最终分析 |

## 目录结构

```
BWKI-2026-备战/
├── src/         核心库 (~13模块)
├── scripts/     工具脚本 (~17个)
├── experiments/ 数据收集 (~9脚本)
├── data/        语料与标注
├── config/      配置文件
├── docs/        文档与伦理
├── research/    研究与发现
├── references/  参考文献
├── tests/       测试套件
└── web/         前端可视化
```

## 命名约定

| 项目 | 格式 | 示例 |
|------|------|------|
| student_id | S + 3位数字 | S001 |
| response_id | R + student + lang + question | RS001_zh_q1 |
| extraction_id | E_日期_编号 | E_20260617_001 |
| analysis_id | A_日期_编号 | A_20260617_001 |
