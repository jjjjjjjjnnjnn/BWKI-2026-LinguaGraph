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
  <img src="https://img.shields.io/badge/concepts-1,160%2B-informational?style=flat-square" alt="1160+ 概念">
  <img src="https://img.shields.io/badge/languages-ZH%20%7C%20EN%20%7C%20DE-green?style=flat-square" alt="ZH/EN/DE">
  <img src="https://img.shields.io/badge/subjects-Math%20%7C%20Physics%20%7C%20Chemistry-orange?style=flat-square" alt="Math/Physics/Chemistry">
  <img src="https://img.shields.io/badge/coverage-NRW%2012.7%25%20%7C%20UK%2037.3%25%20%7C%20US%2017.2%25%20%7C%20CN%2095.4%25-yellow?style=flat-square" alt="Coverage Scores">
  <img src="https://img.shields.io/badge/human_validation-N%3D8-purple?style=flat-square" alt="Human Validation N=8">
  <img src="https://img.shields.io/badge/simulation-300-blue?style=flat-square" alt="300 Simulation Baseline">
</p>

<p align="center">
  🇩🇪 <a href="README_DE.md">Deutsche Version</a> &nbsp;·&nbsp; 🇨🇳 <a href="README_ZH.md">中文版本</a>
</p>

---

## 📑 目录

<details>
<summary><b>Click to expand / collapse</b></summary>

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

- 🧩 从教材中大规模构建**多语言知识图谱**（1,160+ 概念，3 种语言）
- 📏 量化语言、教育体系和学科之间的**结构差异**
- 🎯 衡量跨4个教育体系（德国、英国、美国、中国）的**教材-课程对齐度**
- ✅ 使用 **92 个黄金标准标注**验证提取质量（F1 = 0.939）

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
| **F3** | HDS ≤ **8**（均值 0.40）；83% 的概念是根节点 | 对 3,538 条前提关系进行 BFS | 数学是一个浅层网络，而非深层树状结构 |
| **F4** | **LDS-K reveals heterogeneous convergence**: ZH-DE (0.519) converges; ZH-EN (0.934), DE-EN (0.938) near noise floor | 19-model benchmark, 3 API platforms, 20 labels | Knowledge-structure LDS diverges from surface-language expectations |
| **F5** | LDS **依赖于话题**; **Null Model** confirms Full < Structure for all pairs | 语对内部差异约 0.2; Full LDS-K=0.73, Structure LDS-K=0.77 | 跨语言差异因知识领域而异; taxonomy alone explains most variance |
| **F6** | **物理**在**小学**达到峰值（0.222），数学在初中（0.271） | 366 个物理概念，3 种语言 | 两者都遵循"早期整合，后期分化"的模式 |
| **F7** | 物理的前提知识链**深 2.1 倍** | HDS 均值 0.85 对比 0.40 | 物理知识更具累积性和顺序性 |
| **F8** | **化学**在初中达到峰值（0.042），比数学低 6.5 倍 | 220 个化学概念 | STEM 密度模式跨学科具有普遍性 |
| **F9** | **覆盖率**在不同教育体系中差异巨大 | 北威州 12.7%，英国 37.3%，美国 17.2%，中国 95.4% | 教育体系设计从根本上影响教材对齐度; China's centralized curriculum drives near-universal coverage |
| **F10** | Coverage trajectories reveal **governance model** | UK exam-driven convergence; NRW specialization divergence; China centralized near-total alignment | Curriculum governance (centralized vs federal vs exam-driven) determines coverage trajectory |
| **F11** | **Human LDS-C** rank order distinct from **LDS-K**; **ΔLDS** proposed as core metric | N=8 participants, 90 responses; 19-model benchmark | Surface (concept naming) ≠ structural (relation) divergence; gap itself is informative |
| **F12** | 人类 LDS (**0.727**) 超过模拟基线 (**0.647**, p=0.05) | 300 条模拟回答，模拟提取 | 差异是真实存在的，而非随机波动 |

---

## 📊 数据集

| 学科 | 概念 | 关系 | 教材 | 语言 | 课程覆盖率 |
|---------|:--------:|:---------:|:---------:|:---------:|:------------------:|
| **数学** | 574 | 3,538 | 68 | ZH/EN/DE | NRW 12.7% · UK 37.3% · US 17.2% · CN 95.4% |
| **物理** | 366 | 383 | 94 个版本 | ZH/EN/DE | NRW coverage NA |
| **化学** | 220 | 215 | 18 个版本 | ZH/EN/DE | NRW 36% |
| **总计** | **1,160+** | **4,100+** | **180+** | **3 种语言** | **4 个教育体系** |

---

## ✅ 提取与人类验证

**92 个黄金标准标注**覆盖 2 个领域和 3 种语言（qwen-plus，百联 API）：

| 领域 | 中文 F1 | 德文 F1 | 英文 F1 | 总体 | n |
|--------|:-----:|:-----:|:-----:|:-------:|:-:|
| **社会概念** | **0.974** | **0.949** | **0.882** | **0.939** | 72 |
| **数学** | 0.857 | 0.506 | 0.711 | 0.674 | 20 |
| **全部** | **0.974** | **0.949** | **0.882** | **0.939** | **92** |

> 误差分析：29% 的错误来自极短的回答（1-2 个词）；40% 来自部分遗漏。没有系统性的误导。

**🧑 人类验证研究（N=8）**
- 来自中文/德文/英文母语者的 101 份回答，覆盖 5 个社会话题
- Within-subject DE-EN LDS-C: **0.773** (same person, different language, different concepts)
- Between-subject LDS-C rank order: **DE–ZH (0.751) > DE–EN (0.727) > ZH–EN (0.704)**
- Textbook LDS-K rank order: **ZH–EN (0.934) ≈ DE–EN (0.938) ≫ ZH–DE (0.519)** — structure-level divergence shows a different pattern from concept-level

**🤖 模拟基线（300 条回答）**
- Mean simulated LDS-C: **0.647** (SD=0.086)
- **Human LDS-C (0.727) > Simulation LDS-C (0.647)**, p=0.05
- 确认跨语言差异超出了随机预期

**🧪 Null Model (Structure vs Full Graphs)**
- Full knowledge-graph LDS-K: **0.73** (mean across all pairs)
- Structure-only (taxonomy) LDS-K: **0.77** (mean)
- **Full < Structure for all pairs** — adding edge relations reduces rather than amplifies divergence
- Taxonomy (shared concept organization) accounts for most variance; language-specific relations are convergent

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

## Test any model
```bash
python scripts/batch_process_responses.py --model qwen-plus --gold-only
python scripts/batch_process_responses.py --model glm-4.6 --gold-only
```

---

## 🧪 模型基准测试

19 models tested across 3 API platforms (Bailian, OpenRouter, LM Studio) on identical 20 gold labels (20 social + 20 math), F1 range 0.55–0.67 — best results shown below:

| 模型 | 领域 | 中文 F1 | 德文 F1 | 英文 F1 | 速度 |
|-------|--------|:-----:|:-----:|:-----:|:-----:|
| **qwen-plus** | **Social** | **0.974** | **0.949** | **0.882** | 2-3s |
| qwen-turbo | Math | 0.714 | 0.448 | 0.810 | 1s |
| qwen3.7-max | Math | 0.980 | 0.551 | 0.778 | 2-3s |
| glm-4.6 | Math | 0.951 | 0.595 | 0.689 | 10-20s |

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

## 学术论文

| # | Reference | Relevance |
|---|-----------|-----------|
| 1 | **Novak, J. D. & Cañas, A. J.** (2008). *The theory underlying concept maps and how to construct and use them.* | Foundational — concept mapping theory underpinning CDS/HDS |
| 2 | **Ausubel, D. P.** (1963). *The psychology of meaningful verbal learning.* Grune & Stratton. | Assimilation theory — knowledge is structured, not listed |
| 3 | **Schmidt, W. H. et al.** (2001). *Why schools matter: A cross-national comparison of curriculum and learning.* Jossey-Bass. | TIMSS curriculum coherence — Coverage Score inspiration |
| 4 | **Liang, L. L. & Heckmann, K.** (2013). *Comparing German and Chinese mathematics textbooks.* ZDM, 45(6). | Cross-national textbook comparison methodology |
| 5 | **Boroditsky, L.** (2001). *Does language shape thought?: Mandarin and English speakers' conceptions of time.* Cognitive Psychology, 43(1). | Linguistic relativity — research question context |
| 6 | **Siew, C. S. Q.** (2019). *Applications of network science to education research.* In: Network Science in Education. Springer. | Network analysis of cognitive/educational structures |
| 7 | **Ain, Q. T., Chatti, M. A., & Qussa, H.** (2025). *An optimized pipeline for automatic educational knowledge graph construction.* arXiv. | Most directly relevant EKG pipeline methodology |
| 8 | **Alatrash, R., Chatti, M. A., & Wibowo, A.** (2025). *Inferring prerequisite knowledge concepts in educational knowledge graphs.* arXiv. | Prerequisite inference — supports HDS metric |
| 9 | **Fan, L., Zhu, Y., & Miao, Z.** (2013). *Textbook research in mathematics education.* ESM. | Cross-national textbook problem analysis |
| 10 | **OECD.** (2023). *Education at a Glance 2023.* OECD Publishing. | Cross-national curriculum structure data |
| 11 | **IEA.** (2019). *TIMSS 2019 International Results in 数学和 Science.* | Curriculum coverage analysis methodology |
| 12 | **Vaswani, A. et al.** (2017). *Attention Is All You Need.* NeurIPS. | Transformer architecture — foundational for LLMs used |

## 开源库

| 库 | 用途 | 许可 |
|---------|-------|---------|
| [openai/openai-python](https://github.com/openai/openai-python) | LLM API client for concept extraction | MIT |
| [networkx/networkx](https://github.com/networkx/networkx) | Graph construction and analysis (CDS, HDS) | BSD-3 |
| [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) | Figure generation (Fig 3-7) | PSF |
| [numpy/numpy](https://github.com/numpy/numpy) | Numerical computation, similarity metrics | BSD-3 |
| [scipy/scipy](https://github.com/scipy/scipy) | Statistical analysis, correlation tests | BSD-3 |
| [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) | Baseline models and evaluation | BSD-3 |
| [Three.js](https://github.com/mrdoob/three.js) | 3D knowledge graph visualization (CognitiveSpace) | MIT |
| [Flask](https://github.com/pallets/flask) | Workbench web application | BSD-3 |
| [seaborn/seaborn](https://github.com/mwaskom/seaborn) | Statistical data visualization | BSD-3 |

## 课程标准（原始来源）

| 标准 | 发布者 |
|----------|-----------|
| Kernlehrplan Mathematik/Physik/Chemie NRW (Sek I 2019, Sek II 2023) | MSB NRW |
| UK National Curriculum (Mathematics, Science) | DfE England |
| US Next Generation Science Standards (NGSS) | NGSS Lead States |
| Chinese National Curriculum Standards (数学/物理/化学) | MoE China |

## 教材语料库

Textbook content used for knowledge graph construction (academic research, fair use). Full attribution in graph metadata files.

**ZH** (33+ publishers): 人教版, 沪科版, 北师大版, 苏科版, 粤教版, 鲁科版, 马文蔚, 程守洙, 漆安慎, 赵凯华, 汪志诚, 杨福家, 梁昆淼, 郭硕鸿, 曾谨言

**EN** (34+ publishers): Khan Academy, CK-12, AP Physics, IB, IGCSE, GCSE, Halliday Resnick Walker, Serway Jewett, Young Freedman, Griffiths, Kittel, Feynman Lectures, Stewart Calculus, Strang Linear Algebra

**DE** (27+ publishers): Duden, Lambacher Schwere, Westermann, Cornelsen, Klett, Auer, Dorn-Bader, Kern, Thieme, Tipler, Demtröder, Jackson, Papula, Fischer

## 致谢

- **BWKI 2026** — 竞赛平台与框架
- **Schloss Heessen** — 德国哈姆寄宿学校；机构支持与教育指导
- **Hamm-Lippstadt 应用科学大学（HSHL）** — 学术咨询与专业顾问
- **OpenCode GO** — AI 服务平台，提供模型 API 接入
- **Claude Code** — AI 辅助开发平台（Anthropic）
- **MimoCode** — AI 服务平台（通过 OpenCode GO）
- **阿里云百联** — 免费 API 额度（每个模型 100 万 token）
- **OpenRouter** — 模型路由（已测试）
- **LM Studio** — 本地推理（初期开发）

## 📜 引用说明

```bibtex
@misc{linguaGraph2026,
  author = {Rongjing, J.},
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
- **作者**：Rongjing J. — 双语研究者（中/德），对 AI 与教育充满热情

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
