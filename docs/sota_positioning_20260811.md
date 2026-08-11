# LinguaGraph — SOTA 定位表与先进性论证（2026-08-11）

> **目的**: 回答 R&D 审查 §2.3 的 Gap——"论文 related_work 以教育知识图谱为中心，未对照 LLM 文化对齐/多语言价值评测 SOTA"。本文档完成实时查新并对标。
> **方法**: arXiv API 实时查询（`export.arxiv.org/api/query`，2026-08-11，urllib + SSL 规避，8 组检索词按日期倒序）——非标题臆断，每篇关键论文均抓取摘要刻画其方法。
> **前置**: `docs/review/rnd_project_review_20260811.md` §2.3 · `docs/paper/02_related_work.md`（论文 4 线索 related work）

---

## 1. 一句话定位

**多语言 LLM 价值对齐领域的所有现有工作，测的都是"选择/评分/准确率"（道德小故事分类、价值评分预测、推理正确率、线性表示方向）；没有一项测量"跨语言价值概念图的结构分歧"。LinguaGraph 是这一领域的结构化、图基（graph-based）补充——并首次在 51 模型/47 唯一模型的跨提供方面板上验证。** 这是真实、可辩护、但需诚实界定边界的差异化。

---

## 2. 最相近的 6 篇工作（逐篇方法刻画，来自摘要）

| # | 论文 (arXiv ID) | 年份 | 方法 | 语言 | 模型 | 与 LinguaGraph 关系 |
|---|-----------------|------|------|------|------|---------------------|
| 1 | Xu et al., *Exploring Multilingual Concepts of Human Value in LLMs* (2402.18120) | 2024 | 价值概念作为**表示空间中的线性方向**（probe/线性表示分析） | 16 语 | 3 系列 | 机制层面最接近：也是"值概念跨语言"；但测**表示方向**而非**图结构** |
| 2 | Agarwal et al., *Ethical Reasoning Depends on the Language we Prompt in* (2404.18460) | 2024 | **道德两难小故事 + 规范伦理学分类**（道义/美德/后果主义） | 6 语 | 3 模型 (GPT-4/ChatGPT/Llama2) | 概念上最接近：prompt 语言影响道德判断；但测**分类选择**，非结构 |
| 3 | Farid et al., *One Model, Many Morals* (2509.21443) | 2025 | **翻译两个道德推理基准**到 5 语 + 零样本评估 | 5 语 | 多模型 | 同样发现跨语言道德错位；但方法=基准翻译+准确率 |
| 4 | Wang et al., *Under the Shadow of Babel* (2506.16151) | 2025 | **BICAUSE 双语因果推理数据集**（正/反因果形式，ZH/EN） | 2 语 | 多模型 | 直接测试语言相对论（语言塑造推理）；但测**推理正确率**，2 语 |
| 5 | Lee et al., *MET: Theory-Grounded Culture-Aware Multilingual Moral Reasoning* (2607.11736) | 2026-07 | **MCLASH 道德决策基准** + 文化适配 + 推理/训练对齐方法 | 多语 | 多模型 | 最新（2026-07）：文化感知多语言道德基准；但=决策基准 + 对齐训练 |
| 6 | Zhao et al., *WorldValuesBench* (2404.16308) | 2024 | **世界价值观调查衍生评分预测**基准（按人口背景给出价值评分） | 多国 | LM | 最大规模文化价值基准；但=**价值评分预测**（监督/选择），非结构 |

### 关键共同点（SOTA 的统一方法范式）

所有 6 篇都用 **"给模型一个预置情境/题目 → 模型输出一个选择/评分/分类 → 与基准或跨语言对比"**。即使是最接近的 2402.18120（表示方向）与 2506.16151（推理正确率），也都不提取模型**自由生成的价值概念及其关系结构**。

---

## 3. 更广景观（其余相关簇）

| 簇 | 代表工作 | 与 LinguaGraph 关系 |
|----|---------|---------------------|
| 文化对齐适配 | CuMA (2601.04885, 2026-01)；HKGAI-V1 (2507.11502) | **对齐训练**（把模型拉向某文化），非测量 |
| 文化冲突/决策 | CCD-Bench (2510.03553, 2025-10)；LKValues (2607.20410, 2026-07) | 决策冲突基准/区域价值对齐，非结构 |
| 多语言道德基准 | BengaliMoralBench (2511.03180)；MFTCXplain (2506.19073)；Histoires Morales (2501.17117) | 各语言道德基准，方法=分类/评分 |
| 文化偏见审计 | Cross-Lingual Gender Bias Audit (2605.30804)；Occupational Prompting (2606.12443)；Prompt Programming (2603.16827) | 单维偏见（性别/职业），非价值概念结构 |
| 文化翻译/本地化 | Cultural Translation of Math Word Problems (2606.11009, 2026-06) | 数学题文化翻译审计——**数学域**对照，方法=问题改写 |

---

## 4. LinguaGraph 的差异化（诚实可辩护）

| 维度 | SOTA 现状 | LinguaGraph |
|------|-----------|-------------|
| **测量对象** | 选择/评分/分类/表示方向/推理正确率 | **概念图结构**（Jaccard over 概念节点 + 关系边）——LDS v3 |
| **刺激** | 预置道德小故事/价值题目/基准翻译 | **同一 5 主题自由应答 × 3 语 × k=10**，同一模型 |
| **设计** | 多为组间/提示语对照 | **LLM-as-Subject within-subject**：同一模型三语 → 语言是唯一变量 |
| **模型面板** | 3~数个模型 | **51 测量 / 47 唯一模型**跨提供方（DeepSeek/GLM/Kimi/MiniMax/Qwen/OpenRouter + NVIDIA 美） |
| **方向性证据** | 聚合准确率/评分差 | **方向一致性空模型**（固定频次+方向随机，≥10 票 204 vs 129±4，p<0.001）+ 具体概念驱动者 |
| **文化方向** | 泛文化"不一致" | **DE 自主/规则 vs ZH 空间/应得**——结构化的、方向化的、可解释的 |

### 具体创新主张（用于论文 related work 或答辩）

1. **LDS v3（结构化分歧度量）**：把"语言间价值分歧"从"模型选了什么"推进到"模型怎么组织概念关系"。
2. **Within-subject LLM-as-Subject**：同模型三语，构造上排除提供方/训练分布混杂（人类组间设计做不到）。
3. **51 模型跨提供方面板**：比 SOTA 的 3~数个模型广度大一个量级；含美国模型（nemotron-3-ultra-free）确认非单一来源假象。
4. **方向一致性 + 空模型**：把"分歧"升级为"有方向的分歧"（DE-自主/ZH-空间），并有统计对照。

### 诚实的边界（必须同时陈述）

- LinguaGraph **不做基准准确率对比**（不是更强的 WorldValuesBench/MET 预测器）——是互补的测量工具，非竞争基准。
- 面板 **88% 中国提供方**（DashScope/zen 免费配额现实）；gpt-oss 部分收集（17/30，OpenRouter 配额停滞）——西方前沿模型覆盖不足，已在论文 §8.15/§5.10 披露。
- LDS 是**结构差异度量**，不回答"哪个更正确"（规范性问题超出范围，Positioning C）。
- 领域对照（数学 vs 文化）因对齐伪影**已降级**（P2-C8）——不把"制度趋同/文化分歧"作为内容证据。

---

## 5. 数据血缘与可复现

- 查询时间: 2026-08-11（arXiv 当日倒序；含 2026-07/08 最新工作）
- 端点: `export.arxiv.org/api/query`，8 组检索词（value alignment×multilingual、cross-cultural×LLM、moral reasoning×multilingual、linguistic relativity×LLM、cross-lingual×value×LM、WorldValuesBench、cultural bias×LLM、within-subject×LM）
- 关键论文摘要均逐一抓取核对（非标题推断）
- **注意**: 网络为 Windows SSL 证书规避 + 单次 3 秒限速；若需在论文中正式引用，建议在可联网环境对 8 篇关键论文做最终核验（arXiv ID 均已给出）

---

## 6. 论文 related_work 落点建议（可选后续）

将以下 3 句（德文草稿）插入 `docs/paper/02_related_work.md`（§2.5 Research Gap 附近），使论文直接对照 SOTA：

> "Während bestehende multilinguale Wert- und Moral-Benchmarks (WorldValuesBench, 2024; One Model, Many Morals, 2025; MET, 2026) die *Auswahl* von Werten über Sprachen hinweg messen, erfasst LinguaGraph mit dem LDS die *strukturelle Organisation* von Wertkonzepten (Knoten + Kanten) — ein komplementäres, bisher ungemessenes Maß."

（执行与否由用户决定；本文档提供依据。）

---

*版本: v1.0 | 2026-08-11 | 与 `docs/review/rnd_project_review_20260811.md` 构成"先进性论证"交付物*
