<p align="center">
  <a href="README.md">🇬🇧 English</a> · <a href="README_DE.md">🇩🇪 Deutsch</a> · <a href="README_ZH.md">🇨🇳 中文</a>
</p>

---

<p align="center">
  <img src="cognitive-space/web/screenshot.png" alt="LinguaGraph — Cross-Lingual Knowledge Structure Analysis" width="100%">
</p>

<h1 align="center">🧠 LinguaGraph</h1>


<p align="center">
  <a href="https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/portal/" style="display:inline-block;padding:14px 36px;background:linear-gradient(135deg,#60a5fa,#a78bfa);color:#fff;border-radius:10px;font-weight:700;font-size:1.15rem;text-decoration:none;box-shadow:0 4px 16px rgba(96,165,250,.3)">
    🧠 研究门户 →
  </a>
  &nbsp;&nbsp;
  <a href="https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/" style="display:inline-block;padding:14px 28px;background:#1e293b;border:1px solid #2d3a50;color:#e2e8f0;border-radius:10px;font-weight:600;font-size:1.05rem;text-decoration:none">
    🌌 CognitiveSpace 3D
  </a>
  &nbsp;&nbsp;
  <a href="docs/paper/" style="display:inline-block;padding:14px 28px;background:#1e293b;border:1px solid #2d3a50;color:#e2e8f0;border-radius:10px;font-weight:600;font-size:1.05rem;text-decoration:none">
    📄 Paper
  </a>
</p>


<p align="center">
  <b>How do different languages and educational systems organize the same knowledge?</b>
</p>

<p align="center">
  <a href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/stargazers">
    <img src="https://img.shields.io/github/stars/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph?style=flat-square&logo=github&color=gold" alt="Stars">
  </a>
  <a href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-All%20Rights%20Reserved-blue?style=flat-square" alt="License">
  </a>
  <a href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/commits/master">
    <img src="https://img.shields.io/github/last-commit/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph?style=flat-square&logo=git" alt="Last Commit">
  </a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/BWKI-2026-8A2BE2?style=flat-square" alt="BWKI 2026">
  <img src="https://img.shields.io/badge/gold_labels-92-success?style=flat-square" alt="92 黄金标注">
  <img src="https://img.shields.io/badge/concepts-1,140%2B-informational?style=flat-square" alt="1140+ 概念">
  <img src="https://img.shields.io/badge/languages-ZH%20%7C%20EN%20%7C%20DE-green?style=flat-square" alt="ZH/EN/DE">
  <img src="https://img.shields.io/badge/subjects-Math%20%7C%20Physics%20%7C%20Chemistry-orange?style=flat-square" alt="Math/Physics/Chemistry">
  <img src="https://img.shields.io/badge/coverage-NRW%2012.7%25%20%7C%20UK%2037.3%25%20%7C%20US%2017.2%25%20%7C%20CN%2095.4%25-yellow?style=flat-square" alt="Coverage Scores">
  <img src="https://img.shields.io/badge/human_validation-N%3D15-purple?style=flat-square" alt="Human Validation N=15">
  <img src="https://img.shields.io/badge/simulation-300-blue?style=flat-square" alt="300 Simulation Baseline">
</p>

<p align="center">
  🇩🇪 <a href="README_DE.md">Deutsche Version</a> &nbsp;·&nbsp; 🇨🇳 <a href="README_ZH.md">中文版本</a>
</p>

---

## 📑 目录

<details>
<summary><b>点击展开/折叠</b></summary>

- [🔥 为什么需要 LinguaGraph?](#-为什么需要-linguagraph)
- [📐 核心指标一览](#-核心指标一览)
- [🏆 12 项发现 (F1–F12)](#-12-项发现-f1f12)
- [📊 数据集](#-数据集)
- [✅ 提取与人类验证](#-提取与人类验证)
- [🚀 快速开始](#-快速开始)
- [🧪 模型基准测试](#-模型基准测试)
- [📁 项目结构](#-项目结构)
- [📚 参考文献](#-参考文献)
- [📜 引用说明](#-引用说明)
- [📜 许可与合规](#-许可与合规)
- [🤝 联系方式](#-联系方式)

</details>

---

## 🔥 为什么需要 LinguaGraph?

数学真理是普遍的，但它在教材中的组织方式在不同语言和教育体系之间差异巨大。现有的课程分析工具是定性的、手动的，无法跨多种语言或学科扩展。

**LinguaGraph 是首个实现以下功能的自动化框架：**

- 🧩 从教材中大规模构建**多语言知识图谱**（1,140+ 概念，3 种语言）
- 📏 量化语言、教育体系和学科之间的**结构差异**
- 🎯 衡量跨4个教育体系（德国、英国、美国、中国）的**教材-课程对齐度**
- ✅ 使用 **92 个黄金标准标注**验证提取质量（加权 F1 = 0.881；社会概念子集 F1 = 0.939）

> **它将知识的无形结构转化为可见、可衡量的指标。**

---

## 📐 核心指标一览

| 指标 | 全称 | 公式 | 含义 |
|--------|-----------|---------|-----------------|
| **CDS** | Concept Density Score | 2\|E\|/(\|V\|·(\|V\|−1)) | 每教育阶段的知识互联密度 |
| **HDS** | Hierarchy Depth Score | BFS on prerequisite graph | 最大前提知识链长度 |
| **LDS** | Linguistic Divergence Score (LDS) | 1 − (Jaccard_node + Jaccard_edge) / 2 | Cross-language structural (dis)similarity |
| **CS** | Coverage Score | \|V_textbook ∩ V_curriculum\| / \|V_curriculum\| | 教材与课程对齐度 (updated: CN 95.4%, NRW 12.7%, UK 37.3%, US 17.2%) |

---

## 🏆 12 项发现 (F1–F12)

| # | 发现 | 证据 | 影响 |
|---|---------|----------|--------|
| **F1** | CDS 在**初中**达到峰值（0.271），而非小学 | 在中文、英文、德文中独立确认 | 挑战"知识随阶段增长而变密"的假设 |
| **F2** | **密度下降 3.7 倍**从初中到高中 | 0.271 → 0.073；概念数量 4.2 倍 | 整合枢纽后的课程多样化 |
| **F3** | HDS ≤ **8**（均值 0.40）；83% 的概念是根节点 | 对 525 条直接关系进行 BFS（+约3000条传递关系） | 数学是一个浅层网络，而非深层树状结构 |
| **F4** | **LDS-K 揭示异质性趋同**：中德 (0.519) 趋同；中英 (0.934)、德英 (0.938) 接近噪声底线 | 教材图直接计算 | 知识结构 LDS 与表层语言预期不一致——但 Null Model（F5）证伪了语言解读；多数数学节点是对齐标签产物（见 `docs/p2_methodology_rechecks.md`） |
| **F5** | LDS 与**话题相关**；**Null Model** 确认所有语对的 Full < Structure | 语对内部差异约 0.2；Full LDS-K=0.73, Structure LDS-K=0.77 | 跨语言差异因知识领域而异；分类本身解释了大部分方差 |
| **F6** | **物理**在**小学**达到峰值（0.222），数学在初中（0.271） | 366 个物理概念，3 种语言 | 两者都遵循"早期整合，后期分化"的模式 |
| **F7** | 物理的前提知识链**深 2.1 倍** | HDS 均值 0.85 对比 0.40 | 物理知识更具累积性和顺序性 |
| **F8** | **化学**在初中达到峰值（0.042），比数学低 6.5 倍 | 220 个化学概念 | 与跨学科密度模式一致，但不构成确证（绝对差距仅 0.012，未检验） |
| **F9** | **覆盖率**在不同教育体系中差异巨大 | 北威州 12.7%，英国 37.3%，美国 17.2%，中国 95.4%（关键词匹配；粒度混淆：CN 87 vs US 2124 vs NRW 299 课程概念） | 测量强、归因弱——覆盖差距首先是假设（见 F10） |
| **F10** | 覆盖轨迹提示**治理假设** | 英国考试驱动趋同；NRW 专业化分化；中国集中式全覆盖 | 仅为假设：集中（中国教育部）vs 联邦（德国各州/KMK）制度背景有公开文献支撑（TIMSS 2023 Encyclopedia；OECD EAG 2025），课堂实施链未经检验 |
| **F11** | **N=15 在被试间设计下证伪 ΔLDS > 0**；**ΔLDS** 保留为被试内指标 | N=15（6 德 · 6 中 · 3 英）：LDS-C 0.93–0.96 ≈ 被试内 split-half 底线；N=8 试点未被复制 | 被试间设计无法分离语言与个体差异；需被试内设计 |
| **F12** | 概念层 **ΔLDS ≈ 0**（−0.05…+0.05）；关系层 Δ 不可比 | N=15 + LLM 被试内实验（LDS-C 超底线 +0.08–0.09） | 语言信号在被试内存在（LLM）、在被试间缺席（人类）——设计伪影假设，非无效应证明；早期模拟比较已撤回 |

---

## 📊 数据集

| 学科 | 概念 | 关系 | 教材 | 语言 | 课程覆盖率 |
|---------|:--------:|:---------:|:---------:|:---------:|:------------------:|
| **数学** | 556 | 525 直接（+约3000条传递） | 68 | ZH/EN/DE | NRW 12.7% · UK 37.3% · US 17.2% · CN 95.4% |
| **物理** | 366 | 383 | 94 版本 | ZH/EN/DE | NRW 覆盖 NA |
| **化学** | 220 | 215 | 18 个版本 | ZH/EN/DE | NRW 36% |
| **总计** | **1,140+** | **1,100+ 直接** | **180** | **3 种语言** | **4 个教育体系** |

> SSOT：数学图谱数字来自 `manifest.json`（556 节点 / 525 直接关系 / 219 三语组）。物理/化学来自旧管线（见 `docs/review/rnd_project_review_20260811.md` §7）。

---

## ✅ 提取与人类验证

**92 个黄金标准标注**覆盖 2 个领域和 3 种语言（百联 API 提取）：

| 领域 | 中文 F1 | 德文 F1 | 英文 F1 | 总体 | n |
|--------|:-----:|:-----:|:-----:|:-------:|:-:|
| **社会概念** | **0.974** | **0.949** | **0.882** | **0.939** | 72 |
| **数学** | 0.857 | 0.506 | 0.711 | 0.674 | 20 |
| **全部（加权）** | 0.951 | 0.842 | 0.844 | **0.881** | **92** |

> 总体为领域加权均值（(72×0.939+20×0.674)/92≈0.881）。标题数字 0.939 仅适用于社会概念子集。

> 误差分析：29% 的错误来自极短的回答（1-2 个词）；40% 来自部分遗漏。没有系统性的误导。

**🧑 人类验证研究（N=15 扩展；N=8 试点未被复制）**
- 扩展研究（6 德 · 6 中 · 3 英）：概念层 LDS-C **0.93–0.96 ≈ 语言内 split-half 底线（0.92–0.96）≈ 标签置换（0.94）**——被试间设计下无可分离语言信号；**ΔLDS ≈ 0**（概念层；关系层不可比）
- N=8 试点值（0.70–0.75）**未被复制**——仅为透明起见保留
- 教材 LDS-K 排序：**ZH–EN (0.934) ≈ DE–EN (0.938) ≫ ZH–DE (0.519)**——但见 Null Model：LDS-K 不度量语言差异

**🤖 模拟基线（300 条回答，探索性）**
- 模拟 LDS 均值：**0.647**（关键词模拟提取——与生产模型提取不可比；仅描述性，无 p 值）
- 早期人类 vs 模拟比较（p=0.05）**已撤回**：测量尺度漂移使其无效（见 `docs/paper/04_discussion.md` §8.11–8.12）

**🧪 零模型（结构 vs 完整图）**
- 完整知识图谱 LDS-K：**0.73**（所有语对均值）
- 仅结构（分类）LDS-K：**0.77**（均值）
- **所有语对的 Full < Structure** — 添加边关系并未放大分歧，反而缩小了分歧
- 分类（共享概念组织）解释了大部分方差；语言特定关系呈现趋同

> 完整方法论参见 [`docs/paper/02_methodology.md`](docs/paper/02_methodology.md)，人类分析脚本参见 [`scripts/analyze_human_pilot.py`](scripts/analyze_human_pilot.py)，模拟基线脚本参见 [`scripts/analyze_sim_baseline.py`](scripts/analyze_sim_baseline.py)。

---


## 🚀 自行部署

研究门户是一个**零构建静态网站**。可部署到任何地方：

| 平台 | 发布目录 |
|----------|------------------|
| **GitHub Pages** | 部署包内容：
_deploy/data.js
_deploy/docs/annotation_guideline_v1.md
_deploy/docs/annotation_guideline_v2.md
_deploy/docs/ARCHITECTURE.md
_deploy/docs/audit-report.md
_deploy/docs/bwki-compliance-review.md
_deploy/docs/bwki_paper_outline.md
_deploy/docs/bwki_paper_outline_v2.md
_deploy/docs/CHANGELOG.md
_deploy/docs/cognitive_metrics_framework.md
_deploy/docs/CONSOLIDATION_REPORT.md
_deploy/docs/CONTRIBUTORS.md
_deploy/docs/corpus-status.md
_deploy/docs/coverage_score_definition.md
_deploy/docs/creative_submission.md
_deploy/docs/curriculum_layer_plan.md
_deploy/docs/data_arrival_checklist.md
_deploy/docs/data_expansion_task.md
_deploy/docs/demo_script.md
_deploy/docs/error_analysis.md
_deploy/docs/evidence_milestones.md
_deploy/docs/experiment-design.md
_deploy/docs/experiment_conductor.md
_deploy/docs/figure_plan.md
_deploy/docs/gold_dataset_schema_v1.md
_deploy/docs/handoff_multi_subject.md
_deploy/docs/infrastructure_audit.md
_deploy/docs/judge_qa.md
_deploy/docs/limitations.md
_deploy/docs/literature_matrix.md
_deploy/docs/logos_integration.md
_deploy/docs/mcl_definition.md
_deploy/docs/methodology.md
_deploy/docs/metrics_validation_report.md
_deploy/docs/mimo_prompt.md
_deploy/docs/model_strategy.md
_deploy/docs/paper_results_skeleton.md
_deploy/docs/pilot-study.md
_deploy/docs/pilot_quality_report.md
_deploy/docs/pitch_10min.md (auto) |
| **Cloudflare Pages** |  |
| **Vercel** |  |
| **Local** | Open  |


## 🚀 快速开始

```bash
# 1. 安装与配置
git clone https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph.git
cd BWKI-2026-LinguaGraph
pip install openai numpy
export BAILIAN_API_KEY="your-api-key"

# 2. 验证提取质量（5 分钟）
python scripts/batch_process_responses.py --gold-only
python scripts/evaluate_gold.py

# 3. 生成 300 条回答的模拟基线
python scripts/simulate_baseline.py --mock

# 4. 完整分析流程
python scripts/extract_all_via_api.py
python scripts/compute_lds_from_db.py
```

#
## Test any model
```bash
python scripts/batch_process_responses.py --model qwen-plus --gold-only
python scripts/batch_process_responses.py --model glm-4.6 --gold-only
```

---

## 🧪 模型基准测试

**55 次完整测量（50 个独立模型）**：DashScope 42 个、zen/OpenRouter 7 个 + D1 基线、Kilo 2 个、Cohere/NIM/opencode-go 各 1 个，使用相同 P1 协议（3 语言 × k=10）；另有 19 模型提取基准（F1 范围 0.55–0.67）——最佳提取结果如下。复制数据：[`data/lds_c/llm_subject/multi_model_replication_20260910.json`](data/lds_c/llm_subject/multi_model_replication_20260910.json)；55 个中德语对全部显著（p<0.05），8 个含英语对不显著。

| 模型 | 领域 | 中文 F1 | 德文 F1 | 英文 F1 | 速度 |
|-------|--------|:-----:|:-----:|:-----:|:-----:|
| **qwen-plus** | **社会** | **0.974** | **0.949** | **0.882** | 2-3s |
| qwen-turbo | 数学 | 0.714 | 0.448 | 0.810 | 1s |
| qwen3.7-max | 数学 | 0.980 | 0.551 | 0.778 | 2-3s |
| glm-4.6 | 数学 | 0.951 | 0.595 | 0.689 | 10-20s |

完整结果：[`research/findings/bailian_benchmark_complete.json`](research/findings/bailian_benchmark_complete.json)

---

## 📁 项目结构

```
├── scripts/              # 分析流程（批量提取、评估、基准测试）
├── docs/
│   ├── paper/            # 完整研究论文（摘要 → 结论）
│   ├── review/           # 质量审计与批判性评估
│   ├── ethics/           # GDPR 合规与知情同意书
│   └── creative_submission.md  # BWKI 竞赛提交材料
├── config/
│   ├── expert_graphs/    # 知识图谱（JSON）——数学、物理、化学、课程
│   └── concept_mapping.json    # 174 个跨语言概念对齐
├── cognitive-space/      # 3D 知识图谱可视化（Three.js）
├── research/findings/    # 基准测试输出、评估报告
└── .gitignore            # 排除 API 密钥、数据库、个人隐私信息
```

---

## 📚 参考文献

#
## 学术论文

| # | 参考文献 | 相关性 |
|---|-----------|-----------|
| 1 | **Novak, J. D. & Cañas, A. J.** (2008). *The theory underlying concept maps and how to construct and use them.* | 基础性——支撑 CDS/HDS 的概念映射理论 |
| 2 | **Ausubel, D. P.** (1963). *The psychology of meaningful verbal learning.* Grune & Stratton. | 同化理论——知识是结构化的，而非列表式的 |
| 3 | **Schmidt, W. H. et al.** (2001). *Why schools matter: A cross-national comparison of curriculum and learning.* Jossey-Bass. | TIMSS 课程一致性——覆盖率评分的灵感来源 |
| 4 | **Liang, S. & Heckmann, K.** (2013). *Comparing German and Chinese mathematics textbooks.* ZDM, 45(5), 743-756. | 跨国教材比较方法论 |
| 5 | **Boroditsky, L.** (2001). *Does language shape thought?: Mandarin and English speakers' conceptions of time.* Cognitive Psychology, 43(2). | 语言相对论——研究问题背景 |
| 6 | **Siew, C. S. Q.** (2019). *Applications of network science to education research.* In: Network Science in Education. Springer. | 认知/教育结构的网络分析 |
| 7 | **Ain, Q. U., Chatti, M. A., & Qussa, J.** (2025). *An optimized pipeline for automatic educational knowledge graph construction.* arXiv:2509.05392. | 最直接相关的 EKG 流程方法论 |
| 8 | **Alatrash, R., Chatti, M. A., & Wibowo, N.** (2025). *Inferring prerequisite knowledge concepts in educational knowledge graphs.* arXiv:2509.05393. | 前驱关系推理——支持 HDS 指标 |
| 9 | **Fan, L., Zhu, Y., & Miao, Z.** (2013). *Textbook research in mathematics education.* ESM. | 跨国教材问题分析 |
| 10 | **OECD.** (2025). *Education at a Glance 2025.* OECD Publishing. | 跨国课程结构数据 |
| 11 | **IEA.** (2023). *TIMSS 2023 International Results in 数学和 Science.* | 课程覆盖率分析方法论 |
| 12 | **Vaswani, A. et al.** (2017). *Attention Is All You Need.* NeurIPS. | Transformer 架构——所用大语言模型的基础 |

#
## 开源库

| 库 | 用途 | 许可 |
|---------|-------|---------|
| [openai/openai-python](https://github.com/openai/openai-python) | LLM API 客户端，用于概念提取 | MIT |
| [networkx/networkx](https://github.com/networkx/networkx) | 图构建与分析（CDS, HDS） | BSD-3 |
| [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) | 图表生成（图 3-7） | PSF |
| [numpy/numpy](https://github.com/numpy/numpy) | 数值计算，相似度指标 | BSD-3 |
| [scipy/scipy](https://github.com/scipy/scipy) | 统计分析，相关性检验 | BSD-3 |
| [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) | 基线模型与评估 | BSD-3 |
| [Three.js](https://github.com/mrdoob/three.js) | 3D 知识图谱可视化（CognitiveSpace） | MIT |
| [Flask](https://github.com/pallets/flask) | Workbench 网络应用 | BSD-3 |
| [seaborn/seaborn](https://github.com/mwaskom/seaborn) | 统计数据可视化 | BSD-3 |

#
## 课程标准（原始来源）

| 标准 | 发布者 |
|----------|-----------|
| Kernlehrplan Mathematik/Physik/Chemie NRW (Sek I 2019, Sek II 2023) | MSB NRW |
| UK National Curriculum (Mathematics, Science) | DfE England |
| US Next Generation Science Standards (NGSS) | NGSS Lead States |
| Chinese National Curriculum Standards (数学/物理/化学) | MoE China |

#
## 教材语料库

Textbook content used for knowledge graph construction (academic research, fair use). Full attribution in graph metadata files.

**ZH** (33+ publishers): 人教版, 沪科版, 北师大版, 苏科版, 粤教版, 鲁科版, 马文蔚, 程守洙, 漆安慎, 赵凯华, 汪志诚, 杨福家, 梁昆淼, 郭硕鸿, 曾谨言

**EN** (34+ publishers): Khan Academy, CK-12, AP Physics, IB, IGCSE, GCSE, Halliday Resnick Walker, Serway Jewett, Young Freedman, Griffiths, Kittel, Feynman Lectures, Stewart Calculus, Strang Linear Algebra

**DE** (27+ publishers): Duden, Lambacher Schwere, Westermann, Cornelsen, Klett, Auer, Dorn-Bader, Kern, Thieme, Tipler, Demtröder, Jackson, Papula, Fischer

#
## 致谢

- **BWKI 2026** — 竞赛平台 and framework
- **Schloss Heessen** — 德国哈姆寄宿学校；机构支持与教育指导
- **OpenCode GO** — AI 服务平台，提供模型 API 接入
- **Claude Code** — AI 辅助开发平台（Anthropic）
- **MimoCode** — AI 服务平台（通过 OpenCode GO）
- **阿里云百联** — 免费 API 额度（每个模型 100 万 token）
- **OpenRouter** — 模型路由（已测试）
- **LM Studio** — 本地推理（初期开发）

## 📜 引用说明

```bibtex
@misc{linguaGraph2026,
  author = {Rong, Jiajun and Lan, Zhenxi},
  title = {LinguaGraph: Cross-Lingual Knowledge Structure Analysis Framework},
  year = {2026},
  publisher = {GitHub},
  journal = {BWKI 2026 — Bundeswettbewerb K{\"u}nstliche Intelligenz},
  url = {https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph}
}
```

---

## 📜 许可与合规

- **许可**：保留所有权利 — BWKI 2026 竞赛项目
- **隐私**：参与者数据完全匿名化。仓库中不包含个人身份信息。GDPR 合规详情参见 [`docs/ethics/`](docs/ethics/)。
- **AI 伦理**：LLM 使用仅限于从教材文本中提取概念。没有将合成数据呈现为人类数据。
- **数据来源**：教材摘录在合理使用原则下用于学术研究。

---

## 🤝 联系方式

- **竞赛**：[BWKI 2026](https://www.bw-ki.de/)
- **Repository**: [github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph](https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph)
- **3D Demo**: Open [`cognitive-space/web/index.html`](cognitive-space/web/index.html) in your browser
- **作者**：戎嘉浚 & 兰振熙 — Schloss Heessen 私立学校（BWKI 2026 团队）

<p align="center">
  <sub>用 ❤️ 为 BWKI 2026 打造——因为知识应该被理解，而不仅仅是被告知。</sub>
</p>
<p align="center">
  <a href="https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/portal/" style="display:inline-block;padding:14px 36px;background:linear-gradient(135deg,#60a5fa,#a78bfa);color:#fff;border-radius:10px;font-weight:700;font-size:1.15rem;text-decoration:none">
    🧠 LinguaGraph 研究门户 →
  </a>
  <br>
  <span style="color:#94a3b8;font-size:0.85rem">研究问题 · 发现 · 交互式 3D · 验证 · 论文</span>
</p>



<p align="center">
  <a href="README_DE.md">🇩🇪 Deutsch</a> · <a href="README_ZH.md">🇨🇳 中文</a>
</p>
