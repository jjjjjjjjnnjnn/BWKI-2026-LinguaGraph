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

## 📑 目录

<details>
<summary><b>点击展开</b></summary>

- [🔥 为什么需要 LinguaGraph？](#-为什么需要-linguagraph)
- [📐 核心指标](#-核心指标)
- [🏆 10 项发现（F1–F10）](#-10-项发现f1f10)
- [📊 数据集](#-数据集)
- [✅ 提取质量验证](#-提取质量验证)
- [🚀 快速开始](#-快速开始)
- [📜 参考文献](#-参考文献)
- [📜 许可与合规](#-许可与合规)

</details>

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

## 📚 参考文献

### 学术论文

| # | 文献 | 关联性 |
|---|------|--------|
| 1 | **Novak, J. D. & Cañas, A. J.** (2008). 概念图理论. | CDS/HDS 指标的理论基础 |
| 2 | **Ausubel, D. P.** (1963). 有意义言语学习心理学. | 同化理论 — 知识是结构化的 |
| 3 | **Schmidt, W. H. 等** (2001). *Why schools matter* (TIMSS). | 课程一致性 — Coverage Score 的灵感来源 |
| 4 | **Liang, L. L. & Heckmann, K.** (2013). 中德数学教材比较. ZDM, 45(6). | 跨国教材比较方法论 |
| 5 | **Boroditsky, L.** (2001). *Does language shape thought?* Cognitive Psychology, 43(1). | 语言相对论 — 研究问题背景 |
| 6 | **Siew, C. S. Q.** (2019). *Network science in education.* Springer. | 认知/教育结构的网络分析 |
| 7 | **Ain, Q. T., Chatti, M. A., & Qussa, H.** (2025). *Automated educational KG construction.* arXiv. | 教育知识图谱管线方法论 |
| 8 | **Alatrash, R., Chatti, M. A., & Wibowo, A.** (2025). *Prerequisite inference in EKGs.* arXiv. | 前置知识推理 — 支持 HDS 指标 |
| 9 | **OECD.** (2023). *Education at a Glance 2023.* OECD Publishing. | 跨国课程结构数据 |
| 10 | **IEA.** (2019). *TIMSS 2019 International Results.* | 课程覆盖率分析方法论 |

### 开源库

| 库 | 用途 | 协议 |
|-----|------|------|
| [openai/openai-python](https://github.com/openai/openai-python) | LLM API 调用的概念提取客户端 | MIT |
| [networkx/networkx](https://github.com/networkx/networkx) | 图构建与分析（CDS, HDS） | BSD-3 |
| [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) | 图表生成（Fig 3-7） | PSF |
| [numpy/numpy](https://github.com/numpy/numpy) | 数值计算、相似度度量 | BSD-3 |
| [Three.js](https://github.com/mrdoob/three.js) | 3D 知识图谱可视化（CognitiveSpace） | MIT |
| [Flask](https://github.com/pallets/flask) | Workbench Web 应用 | BSD-3 |

### 课程标准（原始来源）

| 标准 | 发布机构 |
|------|----------|
| Kernlehrplan Mathematik/Physik/Chemie NRW | MSB NRW |
| UK National Curriculum (数学/科学) | DfE England |
| US Next Generation Science Standards (NGSS) | NGSS Lead States |
| 中国国家课程标准（数学/物理/化学） | 教育部 |

### 教材语料

用于知识图谱构建的教材内容（学术研究，合理使用）。

**中文教材**（33+ 出版社）：人教版、沪科版、北师大版、苏科版、粤教版、鲁科版、马文蔚、程守洙、漆安慎、赵凯华、汪志诚、杨福家、梁昆淼、郭硕鸿、曾谨言

**英文教材**（34+ 出版社）：Khan Academy、CK-12、AP Physics、IB、IGCSE、GCSE、Halliday Resnick Walker、Serway Jewett、Young Freedman、Griffiths、Kittel、Feynman Lectures

**德文教材**（27+ 出版社）：Duden、Lambacher Schwere、Westermann、Cornelsen、Klett、Auer、Dorn-Bader、Kern、Thieme、Tipler、Demtröder、Jackson、Papula、Fischer

### 致谢

- **BWKI 2026** — 竞赛平台
- **阿里云百炼** — 免费 API 额度（每个模型 100 万 Token）
- **LM Studio** — 本地模型推理（初期开发）

---

## 📜 引用

```bibtex
@misc{linguaGraph2026,
  author = {Rongjing, J.},
  title = {LinguaGraph: Cross-Lingual Knowledge Structure Analysis Framework},
  year = {2026},
  publisher = {GitHub},
  journal = {BWKI 2026},
  url = {https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph}
}
```

---

## 📜 许可与合规

- **许可**：保留所有权利 — BWKI 2026 竞赛项目
- **第三方代码**：所有开源库均基于 MIT、BSD-3 或 Apache-2.0 协议。详见各仓库的完整许可条款。
- **教材内容**：摘录用于学术研究的合理使用。完整来源记录在图元数据文件中。
- **隐私**：所有参与者数据已匿名化处理。仓库中不包含个人身份信息。
- **AI 伦理**：LLM 使用仅限于从教材文本中提取概念。提取质量已通过 92 条黄金标准标注验证。
- **课程标准**：官方文件用于学术比较。版权归各相关机构所有。