<p align="center">
  <a href="README.md">🇬🇧 English</a> · <a href="README_DE.md">🇩🇪 Deutsch</a> · <a href="README_ZH.md">🇨🇳 中文</a>
</p>

---

<p align="center">
  <img src="cognitive-space/web/screenshot_zh.png" alt="LinguaGraph — Cross-Lingual Knowledge Structure Analysis" width="100%">
</p>

<p align="center">
  <a href="https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/portal/"><img src="cognitive-space/web/portal_hero_zh.png" alt="研究门户——实拍截图" width="49%"></a>
  <a href="https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/web/?graph=steam"><img src="cognitive-space/web/steam_overview_zh.png" alt="STEAM总览——三学科融合3D" width="49%"></a>
  <br><sub>左：研究门户 · 右：STEAM总览（1,143节点 · 849边 · 10桥）——点击直达 live</sub>
</p>

<h1 align="center">🧠 LinguaGraph</h1>


<p align="center">
  <b>How do different languages and educational systems organize the same knowledge?</b>
</p>

<p align="center">
  <a href="https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/portal/" style="display:inline-block;padding:14px 36px;background:linear-gradient(135deg,#60a5fa,#a78bfa);color:#fff;border-radius:10px;font-weight:700;font-size:1.15rem;text-decoration:none;box-shadow:0 4px 16px rgba(96,165,250,.3)">
    🧠 研究门户 →
  </a>
  &nbsp;&nbsp;
  <a href="submission/final/LinguaGraph_BWKI2026.pdf" style="display:inline-block;padding:14px 28px;background:#1e293b;border:1px solid #2d3a50;color:#e2e8f0;border-radius:10px;font-weight:600;font-size:1.05rem;text-decoration:none">
    📄 论文（PDF）
  </a>
  &nbsp;&nbsp;
  <a href="https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/" style="display:inline-block;padding:14px 28px;background:#1e293b;border:1px solid #2d3a50;color:#e2e8f0;border-radius:10px;font-weight:600;font-size:1.05rem;text-decoration:none">
    🌌 CognitiveSpace 3D
  </a>
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
  <img src="https://img.shields.io/badge/human_validation-N%3D15-purple?style=flat-square" alt="人工验证 N=15">
</p>

<p align="center">
  🇩🇪 <a href="README_DE.md">Deutsche Version</a> &nbsp;·&nbsp; 🇨🇳 <a href="README_ZH.md">中文版本</a>
</p>

---

## 🔥 为什么需要 LinguaGraph?

数学真理是普遍的，但它在教材中的组织方式在不同语言和教育体系之间差异巨大。现有的课程分析工具是定性的、手动的，无法跨多种语言或学科扩展。

**LinguaGraph 是首个实现以下功能的自动化框架：**

- 🧩 从教材中大规模构建**多语言知识图谱**（1,140+ 概念，3 种语言）
- 📏 量化语言、教育体系和学科之间的**结构差异**
- 🎯 衡量跨4个教育体系（德国、英国、美国、中国）的**教材-课程对齐度**
- ✅ 使用 **92 个黄金标准标注**验证提取质量（加权 F1 = 0.881；社会概念子集 F1 = 0.939）
- 🔬 自我证伪：T1 去污染检验使 headline 中德趋同（0.52 → 0.99）崩塌，结果如实报告——见 [🏆 12 项发现](#-12-项发现-f1f12)（F4/F5）与 [📊 数据集](#-数据集)

> **它将知识的无形结构转化为可见、可衡量的指标——包括与它不一致的测量。**

---

## 🗺️ 项目导航（从这里开始）

| 入口 | 内容 | 适合谁 |
|-------|--------------|----------|
| [🧠 研究门户](https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/portal/) | 发现 F1–F12、复刻名录（**59/54/177**）、边际星系图、验证区 | **评委与审稿人——从这里开始** |
| [🌐 STEAM 总览](https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/web/?graph=steam) | 三学科同一 3D 图（1,143 节点 · 849 边 · 10 桥）+ 对比面板 | 跨学科对比 |
| [📄 论文（PDF）](submission/final/LinguaGraph_BWKI2026.pdf) | 论文全文，冻结图表 + 数值 | 学术阅读、引用 |
| [🌌 CognitiveSpace 3D](https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/) | 交互式 3D 知识图谱（1,140+ 概念） | 现场演示、观众 |
| [`submission/final/`](submission/final/) | BWKI 提交包（平台回答、披露、代码指南） | 竞赛提交 |
| [`docs/`](docs/) | 80+ 文档——论文源文件、审计、台账（[`INDEX.md`](docs/INDEX.md)） | 深入研究、验证 |

---

## 🎯 核心结论（30 秒）

- **59/54/177 复刻**：同一 P1 协议（中/德/英 × 10 提示）下 59 次完整测量（54 个独立模型）——每个中德语对显著（p<0.05）；文件实情 62/57/186（含部分 qwen-max 运行 n=26/30）。
- **提取质量**：92 个黄金标注——社会概念 F1 **0.939**†（n=72，Batch B Developing——见下注），数学 F1 0.674（n=20），加权总体 **0.881**。
- **自我证伪（T1）**：剔除含 CJK 文字的德语标签（167/219）后，中德"趋同" 0.52 → 0.99 崩塌——F4 解读是标签伪影，如实报告。
- **人类研究（N=15）**：被试间设计下无可分离语言信号（LDS-C ≈ 底线）——语言效应需要被试内设计（LLM：+0.08–0.09 ≫ 底线）。
- **规模**：1,140+ 概念 · 1,100+ 关系 · 204 本教材 · 4 套课程（中国 95.4% · 英国 37.3% · 美国 17.2% · 北威州 12.7%）。

---

## ✅ 提取与人类验证

**92 个黄金标准标注**覆盖 2 个领域和 3 种语言（百联 API 提取）：

| 领域 | 中文 F1 | 德文 F1 | 英文 F1 | 总体 | n |
|--------|:-----:|:-----:|:-----:|:-------:|:-:|
| **社会概念** | **0.974** | **0.949** | **0.882** | **0.939** | 72 |
| **数学** | 0.857 | 0.506 | 0.711 | 0.674 | 20 |
| **全部（加权）** | 0.951 | 0.842 | 0.844 | **0.881** | **92** |

> 总体为领域加权均值（(72×0.939+20×0.674)/92≈0.881）。标题数字 0.939 仅适用于社会概念子集。注：72 条社会标注为机器接受（`auto_accepted`）；数学德语（0.506）仅 n=7，方差大。构成：Batch A 数学 20 条人工从零标注（Mature/C9a）；Batch B 社会 72 条机器预提+人工接受（Developing/C9b，72 条盲审待补；独立 harness 复算约 0.65 vs DB 路径 0.939——见 G3 注记 `research/gold_deconfound_2026-09-14.md`）。

<p align="center">
  <img src="cognitive-space/web/figures/fig8_lds_decontamination_zh.png" alt="图8 —— T1去污染：中德趋同从0.52崩塌到0.99" width="85%">
  <br><sub><b>图8（T1）</b>——标题中的中德趋同未能通过去污染检验。冻结值：ZH-EN 0.9336 / DE-EN 0.9382 / ZH-DE 0.5188。</sub>
</p>

> 误差分析：29% 的错误来自极短的回答（1-2 个词）；40% 来自部分遗漏。没有系统性的误导。

**🧑 人类验证研究（N=15 扩展；N=8 试点未被复制）**
- 扩展研究（6 德 · 6 中 · 3 英）：概念层 LDS-C **0.93–0.96 ≈ 语言内 split-half 底线（0.92–0.96）≈ 标签置换（0.94）**——**ΔLDS ≈ 0**（−0.05…+0.05）；N=8 试点值（0.70–0.75）未被复制，仅为透明起见保留。

**🧪 零模型（结构 vs 完整图）**
- 完整图 LDS-K **0.73** vs 仅结构 **0.77**（均值）——所有语对 Full < Structure；分类解释了大部分方差。

> **LLM 被试双账：**公开口径 **59 完成测量 / 54 独立模型 / 177 配对**剔除了部分 qwen-max 运行（n=26/30，中德同样显著）；文件实情为 **62 / 57 / 186**。**26 collecting** = 23 未完成 + 2 边界 + 1 隔离（论文 §8.15：84 启动，61×n=30）。见 [🧪 模型基准测试](#-模型基准测试)。

> 完整方法论参见 [`docs/paper/02_methodology.md`](docs/paper/02_methodology.md)，冻结基线台账参见 [`docs/BASELINE_LEDGER.md`](docs/BASELINE_LEDGER.md)。

---

## 🧪 模型基准测试

**59 次完整测量（54 个独立模型）**，使用相同 P1 协议（3 语言 × k=10）；另有 19 模型提取基准（F1 范围 0.55–0.67）——最佳提取结果如下。复制数据：[`data/lds_c/llm_subject/multi_model_replication_20260913.json`](data/lds_c/llm_subject/multi_model_replication_20260913.json)；59 个中德语对全部显著（p<0.05），9 个含英语对不显著（8× R1/Distill + phi-4-mini 中英）。

| 模型 | 领域 | 中文 F1 | 德文 F1 | 英文 F1 | 速度 |
|-------|--------|:-----:|:-----:|:-----:|:-----:|
| **qwen-plus** | **社会** | **0.974** | **0.949** | **0.882** | 2-3s |
| qwen-turbo | 数学 | 0.714 | 0.448 | 0.810 | 1s |
| qwen3.7-max | 数学 | 0.980 | 0.551 | 0.778 | 2-3s |
| glm-4.6 | 数学 | 0.951 | 0.595 | 0.689 | 10-20s |

完整结果：[`data/lds_c/llm_subject/multi_model_replication_20260913.json`](data/lds_c/llm_subject/multi_model_replication_20260913.json)

> 双账：已发表 **59/54/177** 剔除部分 qwen-max 运行（n=26/30）；文件实情 **62/57/186**。Collecting：**26** = 23 未完成 + 2 边界 + 1 隔离。

---

## 📊 数据集

| 学科 | 概念 | 关系 | 教材 | 语言 | 课程覆盖率 |
|---------|:--------:|:---------:|:---------:|:---------:|:------------------:|
| **数学** | 556 | 525 直接（+约3000条传递） | 68（32 图内引用） | ZH/EN/DE | NRW 12.7% · UK 37.3% · US 17.2% · CN 95.4% |
| **物理** | 367 | 386 | 83 书名（96 引用） | ZH/EN/DE | NRW 覆盖暂无 |
| **化学** | 220 | 215 | 89 书名 | ZH/EN/DE | NRW 36% |
| **总计** | **1,140+** | **1,100+ 直接** | **204** | **3 种语言** | **4 个教育体系** |

> **计数口径（2026-09-12 冻结）：**数学三层——**68** 输入语料册数（75 JSON 提取文件，含章节拆分）/ **72** 原始馆藏书名（去重前目录）/ **32** 图内引用书名（`source_references`，唯一可引用层）。书名总数 **204 = 32（数学）+ 83（物理）+ 89（化学）** = 门户 `#sources`。物理 367/386 含 Sensor 节点（`physics_em_传感器` + 3 条 requires 链接）；化学 220/215 为回填后基线（218+2，0 悬空）。

> SSOT：数学图谱数字来自 `manifest.json`（556 节点 / 525 直接关系 / 219 三语组）。物理/化学数字来自旧管线（见 `docs/review/rnd_project_review_20260811.md` §7）。完整口径表：`docs/SSOT-web.md`（口径冻结）。

---

## 📐 核心指标一览

| 指标 | 全称 | 公式 | 含义 |
|--------|-----------|---------|-----------------|
| **CDS** | Concept Density Score | 2\|E\|/(\|V\|·(\|V\|−1)) | 每教育阶段的知识互联密度 |
| **HDS** | Hierarchy Depth Score | BFS on prerequisite graph | 最大前提知识链长度 |
| **LDS** | Linguistic Divergence Score (LDS) | 1 − (Jaccard_node + Jaccard_edge) / 2 | 跨语言结构（不）相似度 |
| **CS** | Coverage Score | \|V_textbook ∩ V_curriculum\| / \|V_curriculum\| | 教材与课程对齐度 (updated: CN 95.4%, NRW 12.7%, UK 37.3%, US 17.2%) |

> LDS 采用冻结 v3 公式（2 分量：节点 + 边 Jaccard）。`src/scoring.py` 中的 3 分量变体无法复现已发表数值——见 `docs/BASELINE_LEDGER.md` §8。

---

## 🏆 12 项发现 (F1–F12)

<details>
<summary><b>点击展开完整发现表</b></summary>

| # | 发现 | 证据 | 影响 |
|---|---------|----------|--------|
| **F1** | CDS 在**初中**达到峰值（0.271），而非小学 | 在中文、英文、德文中独立确认 | 挑战"知识随阶段增长而变密"的假设 |
| **F2** | **密度下降 3.7 倍**从初中到高中 | 0.271 → 0.073；概念数量 4.2 倍 | 整合枢纽后的课程多样化 |
| **F3** | HDS ≤ **8**（均值 0.40）；83% 的概念是根节点 | 对 525 条直接关系进行 BFS（+约3000条传递关系） | 数学是一个浅层网络，而非深层树状结构 |
| **F4** | **LDS-K 揭示异质性趋同**：中德 (0.519) 趋同；中英 (0.934)、德英 (0.938) 接近噪声底线 | 教材图直接计算（冻结值：0.9336/0.9382/0.5188，`outputs/figures/reproduce_lds_binary.log`） | 知识结构 LDS 与表层语言预期不一致——但 Null Model（F5）证伪了语言解读；多数数学节点是对齐标签产物（见 `docs/p2_methodology_rechecks.md`） |
| **F5** | LDS 与**话题相关**；**Null Model** 确认所有语对的 Full < Structure | 语对内部差异约 0.2；Full LDS-K=0.73, Structure LDS-K=0.77 | 跨语言差异因知识领域而异；分类本身解释了大部分方差 |
| **F6** | **物理**在**小学**达到峰值（0.222），数学在初中（0.271） | 367 个物理概念，3 种语言 | 两者都遵循"早期整合，后期分化"的模式 |
| **F7** | 物理的前提知识链**深 2.1 倍** | HDS 均值 0.85 对比 0.40 | 物理知识更具累积性和顺序性 |
| **F8** | **化学**在初中达到峰值（0.042），比数学低 6.5 倍 | 220 个化学概念 | 与跨学科密度模式一致，但不构成确证（绝对差距仅 0.012，未检验） |
| **F9** | **覆盖率**在不同教育体系中差异巨大 | 北威州 12.7%，英国 37.3%，美国 17.2%，中国 95.4%（关键词匹配；粒度混淆：CN 87 vs US 2124 vs NRW 299 课程概念） | 测量强、归因弱——覆盖差距首先是假设（见 F10） |
| **F10** | 覆盖轨迹提示**治理假设** | 英国考试驱动趋同；NRW 专业化分化；中国集中式全覆盖 | 仅为假设：集中（中国教育部）vs 联邦（德国各州/KMK）制度背景有公开文献支撑（TIMSS 2023 Encyclopedia；OECD EAG 2025），课堂实施链未经检验 |
| **F11** | **N=15 在被试间设计下证伪 ΔLDS > 0**；**ΔLDS** 保留为被试内指标 | N=15（6 德 · 6 中 · 3 英）：LDS-C 0.93–0.96 ≈ 被试内 split-half 底线；N=8 试点未被复制 | 被试间设计无法分离语言与个体差异；需被试内设计 |
| **F12** | 概念层 **ΔLDS ≈ 0**（−0.05…+0.05）；关系层 Δ 不可比 | N=15 + LLM 被试内实验（LDS-C 超底线 +0.08–0.09） | 语言信号在被试内存在（LLM）、在被试间缺席（人类）——设计伪影假设，非无效应证明；早期模拟比较已撤回 |

> **T1 去污染（图8）：**剔除含 CJK 文字的德语标签（167/219，保留 52）后，中德趋同 0.52 → 0.99 崩塌——F4 的"趋同"是标签伪影，**已被证伪**。图表：`outputs/figures/fig8_lds_decontamination.png`（+`_de`/`_zh`，CSV 同目录），脚本 `scripts/figures/fig8_lds_decontamination.py`。图4 零模型套件：`scripts/figures/fig4_null_model.py`。

</details>

---

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

# 3. 复现冻结值（LDS-K 0.9336/0.9382/0.5188；Fig4/Fig8）
python scripts/figures/reproduce_lds_binary.py
python scripts/figures/fig4_null_model.py
python scripts/figures/fig8_lds_decontamination.py
```

产物：`outputs/figures/reproduce_lds_binary.log`、`fig4_null_model_data.csv`、`fig8_lds_decontamination_data.csv`（+ PNG，镜像至 `cognitive-space/web/figures/`）。台账：`docs/BASELINE_LEDGER.md` §8/§10。

> 研究门户是零构建静态网站，由 `_deploy/` 经 GitHub Pages 发布（推送 master 时经 `.github/workflows/deploy-cognitive-space.yml`）。本地预览：在浏览器中打开 `cognitive-space/portal/index.html`。

### 方法论五步（参见 `docs/paper/02_methodology.md` §§2.1–2.5）
1. **教材语料**——68 册数学（+ 物理 367 节点 / 化学 220 节点图），中/英/德
2. **概念提取（MIMO）**——结构化 LLM 提示词 → 75 JSON 文件 → 556 概念、525 关系
3. **图构建与融合**——合并 → 去重（556）→ 有向图（+约3000条传递边）
4. **跨语言对齐**——30 共享 ID → 219 三语组（39%）→ CDS/HDS/LDS/CS 指标
5. **验证与证伪**——92 黄金标注、N=15 人类研究、零模型套件、T1 去污染

### 工具分层（论文 §2.12，Eigenständigkeit）
自有贡献：设计、LDS 定义、全部发现/证伪分析。已披露辅助工具分层记账（不与字符串匹配计数混用）：**networks/graphs** NetworkX + 3d-force-graph · **figures** matplotlib（`scripts/figures/`）· **文本提取** pymupdf + RapidOCR-ONNX（DirectML-GPU）· **语义** nomic-embed-v1.5 预筛 + Muse-Spark 裁决（temp-0，`scripts/semantic_ground_en.py`）· **概念提取（D1）** 百炼 API qwen-plus（黄金 N=92，社会 F1 0.939）。

---

## 📁 项目结构

```
├── scripts/              # 分析流程（批量提取、评估、基准测试）
│   ├── math_graph_pipeline/  # 规范管线（SSOT：合并→对齐→导出→校验）
│   ├── figures/              # 确定性图表脚本（Fig2/Fig4/Fig8 + 冻结值 + 工具）
│   ├── release.py            # 统一发布（门禁→导出→manifest→打包）
│   └── build_paper_pdf.py    # 论文组装（docs/paper → submission PDF）
├── docs/
│   ├── INDEX.md          # 全部 83 文档导航
│   ├── SSOT-web.md       # 门户/3D 数字口径 + 口径冻结
│   ├── BASELINE_LEDGER.md # 基线台账（8 基线 + Fig4/Fig8 冻结值）
│   ├── paper/            # 完整研究论文（阅读顺序见 ORDER in build_paper_pdf.py）
│   ├── review/           # 质量审计与批判性评估
│   ├── ethics/           # GDPR 合规与知情同意书
│   └── submission/       # BWKI 提交材料（PDF + 平台回答 + 检查表）
├── submission/
│   ├── final/            # 终版包（PDF + 回答 + 披露 + 代码指南）
│   ├── pitch/            # 视频 pitch（脚本 v2 + 分镜；录制另附）
│   └── idea/             # Ideenanmeldung 28.06.（历史）
├── config/
│   ├── expert_graphs/    # 知识图谱（JSON）——数学、物理、化学、课程
│   └── cross_language_mapping.json  # 30 共享概念 ID（冻结）
├── cognitive-space/      # 3D 可视化（Three.js）+ portal/
├── research_lab/         # 沙盒实验（gitignored skills/）
├── release/              # 不可变快照（manifest + data.js + 校验和）
├── freeze/               # 冻结调研样本（不可变）
└── manifest.json         # SSOT 数字（556/525/219）
```

---

## 📚 参考文献

### 学术论文

| # | 参考文献 | 论文 | 相关性 |
|---|-----------|-------|-----------|
| 1 | **Novak, J. D. & Cañas, A. J.** (2008). *The theory underlying concept maps and how to construct and use them.* | [13] | 基础性——支撑 CDS/HDS 的概念映射理论 |
| 2 | **Ausubel, D. P.** (1963). *The psychology of meaningful verbal learning.* Grune & Stratton. | [12] | 同化理论——知识是结构化的，而非列表式的 |
| 3 | **Schmidt, W. H. et al.** (2001). *Why schools matter: A cross-national comparison of curriculum and learning.* Jossey-Bass. | [54] | TIMSS 课程一致性——覆盖率评分的灵感来源 |
| 4 | **Liang, S. & Heckmann, K.** (2013). *Comparing German and Chinese mathematics textbooks.* ZDM, 45(5), 743–756. | [8] | 跨国教材比较方法论 |
| 5 | **Boroditsky, L.** (2001). *Does language shape thought?: Mandarin and English speakers' conceptions of time.* Cognitive Psychology, 43(2). | [53] | 语言相对论——研究问题背景 |
| 6 | **Siew, C. S. Q.** (2019). *Applications of network science to education research.* In: Network Science in Education. Springer. | —（背景） | 认知/教育结构的网络分析 |
| 7 | **Ain, Q. U., Chatti, M. A., & Qussa, J.** (2025). *An optimized pipeline for automatic educational knowledge graph construction.* arXiv:2509.05392. | [3] | 最直接相关的 EKG 流程方法论 |
| 8 | **Alatrash, R., Chatti, M. A., & Wibowo, N.** (2025). *Inferring prerequisite knowledge concepts in educational knowledge graphs.* arXiv:2509.05393. | [5] | 前驱关系推理——支持 HDS 指标 |
| 9 | **Fan, L., Zhu, Y., & Miao, Z.** (2013). *Textbook research in mathematics education.* ICMT. | [9] | 跨国教材问题分析 |
| 10 | **OECD.** (2025). *Education at a Glance 2025.* OECD Publishing. | [32] | 跨国课程结构数据 |
| 11 | **IEA.** (2023). *TIMSS 2023.* | [6] / [30] | 课程覆盖率分析方法论 |
| 12 | **Vaswani, A. et al.** (2017). *Attention Is All You Need.* NeurIPS. | —（背景） | Transformer 架构——所用大语言模型的基础 |

<details>
<summary><b>开源库、课程标准、教材语料、致谢</b></summary>

### 开源库

| 库 | 用途 | 许可 |
|---------|-------|---------|
| [openai/openai-python](https://github.com/openai/openai-python) | LLM API 客户端，用于概念提取 | MIT |
| [networkx/networkx](https://github.com/networkx/networkx) | 图构建与分析（CDS, HDS） | BSD-3 |
| [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) | 图表生成（Fig 2/4/8 等） | PSF |
| [numpy/numpy](https://github.com/numpy/numpy) | 数值计算，相似度指标 | BSD-3 |
| [scipy/scipy](https://github.com/scipy/scipy) | 统计分析，相关性检验 | BSD-3 |
| [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) | 基线模型与评估 | BSD-3 |
| [Three.js](https://github.com/mrdoob/three.js) | 3D 知识图谱可视化（CognitiveSpace） | MIT |
| [Flask](https://github.com/pallets/flask) | Workbench 网络应用 | BSD-3 |
| [seaborn/seaborn](https://github.com/mwaskom/seaborn) | 统计数据可视化 | BSD-3 |

### 课程标准（原始来源）

| 标准 | 发布者 |
|----------|-----------|
| Kernlehrplan Mathematik/Physik/Chemie NRW (Sek I 2019, Sek II 2023) | MSB NRW |
| UK National Curriculum (Mathematics, Science) | DfE England |
| US Next Generation Science Standards (NGSS) | NGSS Lead States |
| Chinese National Curriculum Standards (数学/物理/化学) | MoE China |

### 教材语料库

Textbook content used for knowledge graph construction (academic research, fair use). Full attribution in graph metadata files.

**ZH** (33+ publishers): 人教版, 沪科版, 北师大版, 苏科版, 粤教版, 鲁科版, 马文蔚, 程守洙, 漆安慎, 赵凯华, 汪志诚, 杨福家, 梁昆淼, 郭硕鸿, 曾谨言

**EN** (34+ publishers): Khan Academy, CK-12, AP Physics, IB, IGCSE, GCSE, Halliday Resnick Walker, Serway Jewett, Young Freedman, Griffiths, Kittel, Feynman Lectures, Stewart Calculus, Strang Linear Algebra

**DE** (27+ publishers): Duden, Lambacher Schwere, Westermann, Cornelsen, Klett, Auer, Dorn-Bader, Kern, Thieme, Tipler, Demtröder, Jackson, Papula, Fischer

### 致谢

- **BWKI 2026** — 竞赛平台 and framework
- **Schloss Heessen** — 德国哈姆寄宿学校；机构支持与教育指导
- **OpenCode GO** — AI 服务平台，提供模型 API 接入
- **Claude Code** — AI 辅助开发平台（Anthropic）
- **MimoCode** — AI 服务平台（通过 OpenCode GO）
- **阿里云百联** — 免费 API 额度（每个模型 100 万 token）
- **OpenRouter** — 模型路由（已测试）
- **LM Studio** — 本地推理（初期开发）

</details>

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
