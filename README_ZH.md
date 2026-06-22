<p align="center">
  <a href="README.md">🇬🇧 English</a> · <a href="README_DE.md">🇩🇪 Deutsch</a> · <a href="README_ZH.md">🇨🇳 中文</a>
</p>

---

<p align="center">
  <img src="cognitive-space/web/screenshot.png" alt="LinguaGraph — 跨语言知识结构分析框架" width="100%">
</p>

<h1 align="center">🧠 LinguaGraph</h1>

<p align="center">
  <b>不同语言和教育体系是如何组织同一知识的？</b>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph?style=flat-square&logo=github&color=gold" alt="Stars">
  <img src="https://img.shields.io/badge/许可证-All%20Rights%20Reserved-blue?style=flat-square" alt="许可证">
  <img src="https://img.shields.io/badge/BWKI-2026-8A2BE2?style=flat-square" alt="BWKI 2026">
  <img src="https://img.shields.io/badge/黄金标注-92-success?style=flat-square" alt="92 黄金标注">
  <img src="https://img.shields.io/badge/概念数-1,160%2B-informational?style=flat-square" alt="1160+ 概念">
  <img src="https://img.shields.io/badge/语言-ZH%20%7C%20EN%20%7C%20DE-green?style=flat-square" alt="ZH/EN/DE">
  <img src="https://img.shields.io/badge/学科-数学%20%7C%20物理%20%7C%20化学-orange?style=flat-square" alt="数学/物理/化学">
</p>

---

## 🔥 为什么需要 LinguaGraph？

数学真理是普适的，但知识在教材中的组织方式在不同语言和教育体系之间存在显著差异。现有的课程分析工具是定性的、人工的，无法跨语言或跨学科规模化。

**LinguaGraph 是第一个能够自动完成以下任务的框架：**

- 🧩 从教材中大规模构建**多语言知识图谱**（1160+ 概念，3 种语言）
- 📏 量化语言、教育体系和学科之间的**结构差异**
- 🎯 衡量 4 个教育体系的**教材-课程标准覆盖率**（德国、英国、美国、中国）
- ✅ 使用 **92 条黄金标准标注**验证提取质量（F1 = 0.939）

---

## 📐 核心指标

| 指标 | 公式 | 含义 |
|------|------|------|
| **CDS** | 2\|E\|/(\|V\|·(\|V\|−1)) | 各学段的知识连接密度 |
| **HDS** | 先修关系的 BFS 深度 | 知识链最大深度 |
| **LDS** | 1 − mean(GED, Jaccard_Node, Jaccard_Edge) | 跨语言结构差异度 |
| **CS** | \|V_教材 ∩ V_课标\| / \|V_课标\| | 教材-课标对齐度 |

---

## 🏆 10 项发现（F1–F10）

| # | 发现 | 证据 |
|---|------|------|
| **F1** | CDS 峰值在**初中**（0.271），而非小学 | ZH/EN/DE 三语独立验证，574 概念 |
| **F2** | 初中到高中**密度下降 3.7 倍** | 0.271 → 0.073 |
| **F3** | HDS ≤ **8**（均值 0.40）; 83% 为根概念 | 数学是浅层网络，非深层树状结构 |
| **F4** | **中-德**结构差异最大（LDS=0.907） | 中-英差异最小（0.802）|
| **F5** | LDS **因主题而异** | 语对内部差异可达 0.2 |
| **F6** | **物理**峰值在**小学**（0.222），数学在初中 | 均遵循"早期整合，后期分化"模式 |
| **F7** | 物理知识链**深度是数学的 2.1 倍** | HDS 均值 0.85 vs 0.40 |
| **F8** | **化学**峰值也在初中（0.042） | STEM 密度模式具有普遍性 |
| **F9** | **覆盖率差异显著** | NRW 34%、英国 82%、美国 76%、中国 8% |
| **F10** | 覆盖率轨迹反映**体系设计哲学** | 英国 ↑ 53→90%（考试驱动）；德国 ↘ 50→31%（专业分化）|

---

## 📊 数据集

| 学科 | 概念数 | 关系数 | 教材数 | 语言 | 课标覆盖率 |
|------|:------:|:------:|:------:|:----:|:----------:|
| **数学** | 574 | 3,538 | 68 | ZH/EN/DE | NRW 34% · 英国 82% · 美国 76% |
| **物理** | 366 | 383 | 94 版本 | ZH/EN/DE | NRW 38% |
| **化学** | 220 | 215 | 18 版本 | ZH/EN/DE | NRW 36% |
| **总计** | **1,160+** | **4,100+** | **180+** | **3 语言** | **4 教育体系** |

---

## ✅ 提取质量验证

**92 条黄金标准标注**，涵盖 2 个领域和 3 种语言：

| 领域 | 中文 F1 | 德语 F1 | 英语 F1 | 总体 | n |
|------|:------:|:------:|:------:|:----:|:-:|
| **社会概念** | **0.974** | **0.949** | **0.882** | **0.939** | 72 |
| **数学概念** | 0.857 | 0.506 | 0.711 | 0.674 | 20 |
| **全部** | **0.974** | **0.949** | **0.882** | **0.939** | **92** |

---

## 🚀 快速开始

```bash
# 1. 安装配置
git clone https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph.git
cd BWKI-2026-LinguaGraph
pip install openai numpy
export BAILIAN_API_KEY="你的 API Key"

# 2. 验证提取质量
python scripts/batch_process_responses.py --gold-only
python scripts/evaluate_gold.py

# 3. 完整分析管线
python scripts/compute_lds_from_db.py
```

---

## 📜 参考文献

- Novak & Cañas (2008) — 概念图理论
- Ausubel (1963) — 有意义言语学习心理学
- Schmidt et al. (2001) — TIMSS 课程一致性研究
- Liang & Heckmann (2013) — 中德数学教材比较
- Boroditsky (2001) — 语言塑造思维吗？
- OECD (2023) — 教育概览

---

## 📜 许可与合规

- **许可**：保留所有权利 — BWKI 2026 竞赛项目
- **隐私**：所有参与者数据已匿名化处理。详见 [`docs/ethics/`](docs/ethics/) 的 GDPR 合规文档。
- **AI 伦理**：LLM 使用仅限于从教材文本中提取概念。

---

<p align="center">
  <a href="README.md">🇬🇧 English</a> · <a href="README_DE.md">🇩🇪 Deutsch</a>
</p>
