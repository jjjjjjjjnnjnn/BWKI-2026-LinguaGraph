# Technical Methodology — BWKI CognitiveSpace Pipeline 证据综合

> 从 8 篇知识库条目综合提炼，验证 LLM extraction → graph → MCL 管线的技术基础。
> 生成日期: 2026-06-17

---

## 1. LLM Extraction Validation Approach

### 1.1 现有方法综述

| 方法 | 代表论文 | 精度 | 适用性 |
|------|----------|------|--------|
| LLM + 判断 LLM + 人工审核 | Kommineni et al. (2024) P036, 194 citations | 高（需人工） | 三语专家图谱构建 |
| 迭代 zero-shot prompting | Carta et al. (2023) P037, 132 citations | 中等 | 新领域快速原型 |
| LLM + 传统 NLP 混合管道 | Trajanoska et al. (2023) P038, 175 citations | 高 | 最适合 LinguaGraph |
| 本体驱动 LLM | Feng et al. (2024) P041, 27 citations | 高一致性 | 三语概念对齐 |
| 教育三元组提取 | Sun et al. (2024) P040 LLM4EduKG, 19 citations | 教育专用 | **直接适用** |
| 自动构建 KG | AlRabah et al. (2026) P042 InstructKG | 人工的 85% | 专家图谱方法 |
| 知识组件标注 | Ozyurt et al. (2024) P043 KCQRL | 80%+ | 概念提取评估 |

### 1.2 验证方案

**推荐管线**: 混合方法（Trajanoska et al.）

```
Step 1: LLM zero-shot 提取概念和关系（Carta 方法）
Step 2: 判断 LLM 评估提取质量（Kommineni 方法）
Step 3: 本体驱动约束一致性（Feng 方法）
Step 4: 教育领域适配（LLM4EduKG）
```

**精度基线**: InstructKG 达到人工的 85%，KCQRL 达到 80%+。LinguaGraph 需验证三语一致性，这是全新方向——文献搜索 "LLM concept extraction cross-lingual consistency" 返回 0 篇论文。

### 1.3 关键发现

- 分层 KG（粗粒度→细粒度）优于扁平 KG（Wang et al. 2026）
- 概念提取准确率高于关系提取（AlRabah et al.）
- 零样本方法适合新领域但精度低于有标注方法（Carta et al.）
- 符号知识集成仅需 10% 训练数据即可达 0.80 AUC（Hooshyar et al. 2026）

---

## 2. Graph Similarity Metrics for MCL

### 2.1 指标分类

| 类别 | 指标 | 计算复杂度 | LinguaGraph 用途 |
|------|------|-----------|-----------------|
| 基于集合 | Jaccard, Cosine of edges | O(n) | 快速筛选 |
| 基于结构 | Graph Edit Distance (GED) | NP-hard (精确) | **核心指标** |
| 基于结构 | Maximum Common Subgraph (MCS) | NP-hard | GED 互补 |
| 基于嵌入 | TransE/GraphSAGE + cosine | O(n) | 语义补充 |
| 基于特征 | 度分布, 中心性 | O(n) | 辅助分析 |
| 基于核 | Weisfeiler-Lehman 核 | O(n·h) | 局部结构比较 |

### 2.2 GED 深度分析

**为什么 GED 是核心**: GED 衡量将一个认知图转换为另一个的最小编辑操作代价，直接反映认知结构差异。

**近似方法** (精确 GED 是 NP-hard):

| 方法 | 论文 | 特点 |
|------|------|------|
| 神经图匹配 | Piao et al. (2023) P048, 67 citations | 学习近似 GED，效率高 |
| 扩散模型 | Huang et al. (2025) P052 DiffGED | 前沿方法 |
| 节点匹配模式 | Lee & Kim (2025) P051 | 最新方法 |
| 噪声鲁棒 GED | Ebsch et al. (2020) P053 | 认知图有噪声时适用 |
| 自动参数学习 | Serratosa (2021) P050 | 适合认知图参数 |

**度量约束**: Serratosa (2019) P049 确认 GED 需满足对称性、三角不等式等才能作为有效度量。

### 2.3 推荐指标组合

LinguaGraph 应综合多指标，不依赖单一:

```
GraphSimilarity(G1, G2) = α × Jaccard(E1, E2) + β × (1 - GED_norm) + γ × Cosine(emb1, emb2)
```

**推荐权重**: α=0.3 (Jaccard), β=0.4 (GED), γ=0.3 (embedding)

### 2.4 图嵌入方案

| 方法 | 论文 | 优点 | 缺点 |
|------|------|------|------|
| TransE | Bordes et al. (2013) | 简单高效，h+r≈t | 难处理复杂关系 |
| GraphSAGE | Hamilton et al. (2017) | 归纳学习，可处理新图 | 需要节点特征 |
| Sentence-BERT | — | 直接编码概念名 | 忽略图结构 |
| **综合方案** | — | 结构+语义 | 复杂度高 |

**综合嵌入伪代码**:
```python
def comprehensive_embedding(G):
    structural = node2vec_embedding(G)  # 结构信息
    semantic = mean_bert_embedding([node for node in G.nodes()])  # 语义信息
    return concatenate(structural, semantic)
```

### 2.5 图核方法

| 核方法 | 比较内容 | 适用性 |
|--------|----------|--------|
| 随机游走核 | 随机游走分布 | 整体结构 |
| 子图核 | 子图结构 | 局部模式 |
| Weisfeiler-Lehman 核 | 邻域结构 | **推荐用于认知图局部比较** |
| 最短路径核 | 路径分布 | Borgwardt et al. (2005) 经典 |

---

## 3. Cross-lingual KG Alignment Methods

### 3.1 方法分类

| 方法类别 | 代表论文 | 核心思路 |
|----------|----------|----------|
| 图匹配神经网络 | Xu et al. (2019) P060, 340 citations | 结构信息 + 神经匹配 |
| 元关系感知 | Mao et al. (2020) P061 MRAEA, 261 citations | 关系信息提升鲁棒性 |
| GCN 对齐 | Xiong & Gao (2019) P064 | 邻域信息捕获 |
| 多视图表示 | Wang et al. (2023) P065 FuAlign, 64 citations | 多方面信息融合 |
| 关系感知 | Zhu et al. (2023) P066 | 关系是关键 |
| 自举对齐 | Sun et al. (2020) P068 BootEA | 扩展种子集 |
| 多通道 GCN | Tang et al. (2020) P069 | 多关系类型 |
| 语义感知 | Wang et al. (2020) P072 | 语义信息 |
| 翻译嵌入 | Chen et al. (2017) P067 MTransE | 跨语言嵌入基础 |

### 3.2 对 CognitiveSpace 的直接适用性

**核心洞察**: 跨语言 KG 对齐主要研究**实体级对齐**。LinguaGraph 研究更高层次的**结构级对齐**——认知图结构的比较。

**推荐方法**:
1. **GMNN (Xu et al. 2019)** — 340 citations，直接适用于认知图跨语言对齐
2. **MRAEA (Mao et al. 2020)** — 关系信息对认知图对齐很重要
3. **FuAlign (Wang et al. 2023)** — 多视图方法捕获认知图不同方面

### 3.3 鲁棒性考虑

- Pei et al. (2020) P063: 噪声感知模块提升对齐鲁棒性
- Zhang et al. (2021) P071: 对齐方法容易受对抗攻击影响，需要验证

### 3.4 关键研究空白

| 空白 | 证据 | LinguaGraph 机会 |
|------|------|-----------------|
| 跨语言认知诊断 | 搜索 "cross-lingual cognitive diagnosis" → 0 篇 | 首次扩展 |
| 语言回答的知识追踪 | 搜索 "knowledge tracing from natural language" → 极少 | 新方法 |
| 知识组织结构量化 | 搜索 "knowledge organization graph comparison" → 0 篇 | 首次量化 |
| LLM 提取跨语言一致性 | 搜索 "LLM concept extraction cross-lingual consistency" → 0 篇 | 首次验证 |

---

## 4. Benchmark Comparisons with Existing Systems

### 4.1 已有系统对比

| 系统 | 功能 | 语言 | 评估标准 | vs LinguaGraph |
|------|------|------|----------|---------------|
| BKT/DKT/AKT | 知识追踪 | 英语 | AUC | 追踪"知道什么" vs 追踪"如何组织" |
| InstructKG | 课程 KG 构建 | 英语 | 人工对比 85% | 单语言 vs 跨语言 |
| DeepTutor | 个性化辅导 | 英语 | 效果提升 10.8% | 单语言 vs 跨语言 |
| AgentSchool | 多代理模拟 | 英语 | 状态转换相似度 | 模拟 vs 真实跨语言 |
| 3C 框架 | 缺失知识检测 | 英语 | 85.21% AUC | 行为数据 vs 语言数据 |
| GraphRAG | 分层 KG + RAG | 英语 | 推荐效果 | 单语言 vs 跨语言 |

### 4.2 数据集适用性

| 数据集 | 语言 | 规模 | LinguaGraph 适用性 |
|--------|------|------|-------------------|
| ASSISTments | 英语 | 大 | ❌ 单语言 |
| EdNet | 英语 | 巨大 | ❌ 单语言 |
| Junyi Academy | 中英 | 中 | ⚠️ 可参考 |
| EduData | 多语言 | 大 | ⚠️ 可参考但需适配 |

### 4.3 可用工具

| 工具 | 功能 | 用途 |
|------|------|------|
| EduStudio | 认知建模 | baseline |
| pyedmine | 知识追踪 | baseline |
| Agent4Edu | 数据生成 | 测试数据生成 |

### 4.4 已有基准数据集上的结果

- **InstructKG**: 自动 KG 达到人工的 85%（AlRabah et al. 2026）
- **KCQRL**: 知识组件标注 80%+ 准确率（Ozyurt et al. 2024）
- **3C 框架**: 缺失知识检测 85.21% AUC（Li et al. 2026）
- **神经符号 KT**: 10% 训练数据达到 0.80 AUC（Hooshyar et al. 2026）
- **DeepTutor**: 个性化指标提升效果 10.8%（Zhao et al. 2026）
- **分层 KG**: 比扁平 KG 预测准确率高 12%（Liu & Li 2026）
- **GMNN**: 在 CN-DBpedia 和 XLORE 上显著优于基线（Xu et al. 2019, 340 citations）

---

## 5. Recommended Metrics for BWKI Evaluation

### 5.1 LLM Extraction 质量指标

| 指标 | 测量内容 | 目标值 | 来源 |
|------|----------|--------|------|
| Concept Extraction F1 | 概念提取精度+召回 | ≥80% | KCQRL baseline |
| Relation Extraction F1 | 关系提取精度+召回 | ≥70% | InstructKG: 概念>关系 |
| Cross-lingual Consistency | 三语提取一致性 | 全新指标 | LinguaGraph 贡献 |
| Human Agreement Rate | 与人工标注一致性 | ≥85% | InstructKG baseline |

### 5.2 Graph Similarity 指标

| 指标 | 用途 | 权重 | 实现 |
|------|------|------|------|
| Jaccard Edge Similarity | 快速筛选 | 0.3 | `len(E1∩E2) / len(E1∪E2)` |
| Normalized GED | 结构比较 | 0.4 | 近似算法 (Piao/DiffGED) |
| Cosine Embedding Distance | 语义比较 | 0.3 | TransE + sentence-transformers |
| WL Kernel | 局部结构 | 辅助 | Weisfeiler-Lehman |
| Degree Distribution Similarity | 统计特征 | 辅助 | KL 散度 |

### 5.3 MCL 评估指标

| 指标 | 测量内容 | 基线 |
|------|----------|------|
| AUC | 缺失知识检测 | 85.21% (3C framework) |
| Hit@K | Top-K 预测准确率 | 待定 |
| Knowledge Gain | 学习前后变化 | 待定 |
| LDS (Language Drift Score) | 跨语言认知漂移 | **LinguaGraph 新指标** |

### 5.4 系统级评估

| 维度 | 指标 | 方法 |
|------|------|------|
| 三语一致性 | 三语提取的 Cohen's Kappa | 人工评估子集 |
| 图结构保真度 | 分层 vs 扁平结构对比 | Wang et al. 方法 |
| 跨语言对齐精度 | 实体对齐 Hit@1/10 | CN-DBpedia/XLORE 协议 |
| 认知距离有效性 | 图相似度与人工判断相关性 | Pearson/Spearman |

---

## 6. 核心论文索引

### LLM Extraction (12 papers)

| ID | 作者 | 年份 | 引用 | 核心贡献 |
|----|------|------|------|----------|
| P036 | Kommineni et al. | 2024 | 194 | LLM+判断LLM+人工审核 |
| P037 | Carta et al. | 2023 | 132 | 迭代 zero-shot |
| P038 | Trajanoska et al. | 2023 | 175 | LLM+传统NLP混合 |
| P039 | Bian | 2025 | 19 | LLM KG 构建综述 |
| P040 | Sun et al. | 2024 | 19 | LLM4EduKG 教育KG |
| P041 | Feng et al. | 2024 | 27 | 本体驱动LLM |
| P042 | AlRabah et al. | 2026 | 新 | InstructKG 85%人工水平 |
| P043 | Ozyurt et al. | 2024 | 中 | KCQRL 80%+ |
| P044 | Wang et al. | 2026 | 新 | 分层KG>扁平KG |
| P045 | Li et al. | 2026 | 新 | 3C框架 85.21% AUC |
| P046 | Hooshyar et al. | 2026 | 新 | 神经符号KT 10%数据0.80 AUC |
| P047 | Ye et al. | 2026 | 新 | AgentSchool 模拟 |

### GED (12 papers)

| ID | 作者 | 年份 | 引用 | 核心贡献 |
|----|------|------|------|----------|
| P048 | Piao et al. | 2023 | 67 | 神经图匹配GED |
| P049 | Serratosa | 2019 | 35 | GED度量性质 |
| P050 | Serratosa | 2021 | 42 | 自动学习GED参数 |
| P051 | Lee & Kim | 2025 | 新 | 节点匹配模式 |
| P052 | Huang et al. | 2025 | 3 | DiffGED扩散模型 |
| P053 | Ebsch et al. | 2020 | 10 | 噪声子图匹配 |
| P054 | Bunke & Shearer | 1998 | 经典 | MCS互补 |
| P055 | Zhang | 1994 | 经典 | 近似图同构 |
| P056 | Barthélemy & Guenoche | 1991 | 经典 | 树编辑距离 |
| P057 | Hubert | 1978 | 经典 | 对称矩阵缩放 |
| P058 | Gao et al. | 2010 | 经典 | 图核综述 |
| P059 | Borgwardt et al. | 2005 | 经典 | 最短路径图核 |

### Cross-lingual KG (12 papers)

| ID | 作者 | 年份 | 引用 | 核心贡献 |
|----|------|------|------|----------|
| P060 | Xu et al. | 2019 | 340 | GMNN图匹配对齐 |
| P061 | Mao et al. | 2020 | 261 | MRAEA元关系感知 |
| P062 | Xu et al. | 2020 | 61 | 协调推理 |
| P063 | Pei et al. | 2020 | 78 | 鲁棒实体对齐 |
| P064 | Xiong & Gao | 2019 | 15 | GCN对齐 |
| P065 | Wang et al. | 2023 | 64 | FuAlign多视图 |
| P066 | Zhu et al. | 2023 | 19 | 关系感知 |
| P067 | Chen et al. | 2017 | 经典 | MTransE翻译嵌入 |
| P068 | Sun et al. | 2020 | 经典 | BootEA自举 |
| P069 | Tang et al. | 2020 | 经典 | 多通道GCN |
| P070 | Liu et al. | 2020 | 经典 | KG对齐综述 |
| P071 | Zhang et al. | 2021 | 21 | 对抗攻击 |
| P072 | Wang et al. | 2020 | 经典 | 语义感知对齐 |

### 其他关键论文

| 论文 | 核心贡献 |
|------|----------|
| Li et al. (2019) GMN | 端到端学习图相似度 |
| Bordes et al. (2013) TransE | 翻译嵌入 h+r≈t |
| Hamilton et al. (2017) GraphSAGE | 归纳图嵌入 |
| Liu & Li (2026) | 分层KG+自适应边权重，比扁平高12% |

---

## 7. CognitiveSpace Pipeline 技术路线图

```
Phase 1: LLM Extraction
├── 方法: 混合管道 (Trajanoska) + 本体驱动 (Feng) + 教育适配 (LLM4EduKG)
├── 三语: 中/德/英概念+关系提取
├── 验证: 判断LLM评估 + 人工子集标注
└── 目标: 概念F1≥80%, 关系F1≥70%, 三语一致性Cohen's Kappa≥0.7

Phase 2: Graph Construction
├── 结构: 分层KG (Wang et al. 方法)
├── 层次: 学科→章节→概念→关系
├── 边权重: 自适应 (Liu & Li 方法)
└── 嵌入: TransE + Sentence-BERT 综合方案

Phase 3: Cross-lingual Alignment
├── 方法: GMNN (Xu et al. 2019) 或 FuAlign (Wang et al. 2023)
├── 对齐: 概念级 + 结构级
├── 鲁棒性: 噪声感知 (Pei et al. 2020)
└── 验证: CN-DBpedia/XLORE 协议适配

Phase 4: MCL Detection
├── 指标: 综合图相似度 (Jaccard 0.3 + GED 0.4 + Embedding 0.3)
├── GED: 神经近似 (Piao et al. 2023) 或 DiffGED (Huang et al. 2025)
├── 输出: LDS (Language Drift Score) 新指标
└── 验证: 与人工判断的相关性 (Pearson/Spearman)
```
