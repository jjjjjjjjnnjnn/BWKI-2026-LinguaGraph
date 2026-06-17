# 🧠 LinguaGraph — 语言如何塑造思维？ / Mapping How Language Shapes Thinking

> **BWKI 2026 (Bundeswettbewerb Künstliche Intelligenz) — 参赛项目**
>
> *Bundeswettbewerb Künstliche Intelligenz 2026 Entry*

---

<div align="center">

## 中文简介

**LinguaGraph** 是一个跨学科研究项目，旨在通过人工智能与图论方法，量化回答**"语言是否改变人的思维方式？"**这一经典语言学问题。

### 核心创新

| 创新点 | 说明 |
|--------|------|
| **LDS (Language Drift Score)** | 首个在图结构层面量化跨语言认知差异的指标 |
| **Cognitive City** | 3D 可视化隐喻：概念=建筑，关系=道路 |
| **三语比较** | 中文、德语、英语三种语言系统的认知图谱分析 |

### 研究框架

```
学生回答 (ZH/DE/EN)
    ↓
LLM 提取概念与关系
    ↓
构建认知图谱 (NetworkX DiGraph)
    ↓
跨语言概念对其 (30个共享概念ID)
    ↓
计算 LDS / LCD / 概念Shift
    ↓
3D Cognitive City 可视化
```

### 技术栈

- **AI**: OpenAI GPT-4.1-mini / Qwen3-8B / Ollama (插件式 Provider)
- **图论**: NetworkX, Graph Edit Distance, Jaccard 相似度
- **数据库**: SQLite (linguaGraph.db, 10 张表)
- **可视化**: Three.js (3D Cognitive City)
- **数据**: 300 条计算基线 + Wikipedia 多语语料

### 实验设计

- **30 名参与者** (10 ZH, 10 DE, 10 EN)
- **5 主题 × 3 语言** = 15 道开放式问题
- **组内 + 组间混合设计**
- **统计功效**: 效应量 d=0.6-0.8, α=0.05, power>0.80

### 合规与伦理

- ✅ GDPR 合规 (Art. 6, 7, 8, 13, 15, 16, 17, 33, 34, 77)
- ✅ 三语知情同意书 (ZH/DE/EN)
- ✅ 未成年人参与保护机制
- ✅ 数据匿名化处理

---

## English Introduction

**LinguaGraph** is an interdisciplinary research project that uses AI and graph theory to quantify whether **language shapes the structure of human thought** — the classic Sapir-Whorf hypothesis of linguistic relativity.

### Key Innovation

| Innovation | Description |
|-----------|-------------|
| **LDS (Language Drift Score)** | First metric quantifying cross-lingual cognitive differences at the graph-structure level |
| **Cognitive City** | 3D visualization: concepts as buildings, relations as roads |
| **Trilingual Comparison** | Chinese, German, and English cognitive graph analysis |

### Tech Stack

- **AI**: OpenAI GPT-4.1-mini / Qwen3-8B / Ollama (pluggable Provider system)
- **Graph**: NetworkX, Graph Edit Distance, Jaccard similarity
- **Database**: SQLite (10 tables, 75+ records)
- **Visualization**: Three.js (3D Cognitive City)
- **Data**: 300 computational baselines + multilingual Wikipedia corpus

### Experiment Design

- **30 participants** (10 ZH, 10 DE, 10 EN)
- **5 topics × 3 languages** = 15 open-ended questions
- **Mixed within-subject + between-subject design**
- **Power analysis**: d=0.6-0.8, α=0.05, power>0.80

### Ethics & Compliance

- ✅ GDPR compliant (Art. 6, 7, 8, 13, 15, 16, 17, 33, 34, 77)
- ✅ Trilingual consent forms (ZH/DE/EN)
- ✅ Minor participant protection
- ✅ Data anonymization

---

## 📁 项目结构 / Project Structure

```
BWKI-2026-LinguaGraph/
├── src/                  # 核心库
│   ├── extract.py        # 概念提取 (LLM + mock)
│   ├── graph.py          # 认知图谱构建 (NetworkX)
│   ├── scoring.py        # LDS / LCD 计算
│   ├── compare.py        # 缺失链接检测
│   ├── cross_language.py # 跨语言概念对齐
│   ├── explain.py        # 结果解释生成
│   ├── providers/        # LLM Provider 插件系统
│   └── main.py           # 端到端管道入口
├── scripts/              # 工具脚本
│   ├── db_init.py        # 数据库初始化
│   ├── ingest_all.py     # 批量数据导入
│   ├── analyze_student.py # 单学生完整分析
│   ├── analyze_pilot.py  # Pilot 数据分析
│   ├── simulate_baseline.py # 计算基线生成
│   ├── survey_entry.py   # 数据录入 CLI (伙伴用)
│   └── evaluate_pipeline.py # LLM 提取质量评估
├── experiments/          # 数据采集脚本
├── config/               # 配置文件
│   ├── cross_language_mapping.json  # 跨语言概念映射
│   ├── normalization_map.json       # 同义词规范化
│   └── prompts/          # LLM Prompt 模板
├── data/                 # 数据
│   ├── corpus/           # Wikipedia 语料 (ZH/DE/EN)
│   ├── gold/             # 人工标注数据集
│   ├── baseline/         # 计算基线数据
│   └── questionnaires/   # 问卷定义
├── docs/                 # 文档
│   ├── ethics/           # 伦理文件包 (GDPR, 同意书)
│   ├── methodology.md    # LDS 数学定义
│   └── experiment-design.md # 实验方案
├── research/             # 研究发现
│   └── findings/         # 分析结果
├── visualization/        # 2D 可视化
├── web/                  # Web 前端
│   └── threejs/          # Three.js Cognitive City 3D
├── tests/                # 测试套件
├── references/           # 参考文献 (140+ 论文笔记)
└── linguaGraph.db        # SQLite 数据库
```

---

## 🚀 快速开始 / Quick Start

```bash
# 安装依赖 / Install dependencies
pip install -r requirements.txt

# 运行完整管道 / Run the full pipeline
python src/main.py

# 查看数据状态 / Check data status
python scripts/db_init.py
python scripts/survey_entry.py status

# 运行测试 / Run tests
python -m pytest tests/ -v

# 启动 3D 可视化 / Start 3D visualization
python web/server.py
# Open http://localhost:8080
```

---

## 📊 项目状态 / Project Status

| 模块 / Module | 完成度 | 状态 |
|--------------|--------|------|
| 核心管道 / Core Pipeline | 90% | ✅ |
| LDS 指标 / LDS Metric | 90% | ✅ |
| 可视化 / Visualization | 75% | 🟡 |
| 问卷 / Questionnaire | 95% | ✅ |
| 伦理合规 / Ethics | 100% | ✅ |
| GitHub / Version Control | 100% | ✅ |
| 人类数据 / Human Data | 5% | 🔴 |

---

## 📖 引用 / Citation

如果你在研究中使用 LinguaGraph，请引用：

```bibtex
@software{linguagraph2026,
  title = {LinguaGraph: Mapping How Language Shapes Thinking},
  author = {Rong, Jiajun},
  year = {2026},
  url = {https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph}
}
```

或查看 [`CITATION.cff`](CITATION.cff)。

---

## © 版权声明 / Copyright

© 2026 Jiajun Rong. 保留所有权利。

本项目代码及相关文档仅供 **BWKI 2026 竞赛评审** 及 **学术研究** 目的公开查看。

**未经作者书面许可，禁止任何商业用途的复制、分发或修改。**

*This repository is publicly accessible for BWKI 2026 competition review and academic research purposes. All rights reserved. No commercial use, reproduction, or modification without written permission from the author.*

---

**BWKI 2026 · Bundeswettbewerb Künstliche Intelligenz**
