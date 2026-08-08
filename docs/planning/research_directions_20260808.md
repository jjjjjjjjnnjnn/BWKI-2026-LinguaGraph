# LinguaGraph — 可行研究方向探索（文献前沿 + 现状诊断）

> **生成**: 2026-08-08 | **状态**: 分析文档（方向筛选，供决策）
> **背景**: N=15 三层阴性结果已确立（无语言信号，组间设计混淆）。本文基于当前文献前沿 + 项目现状资产，提出 4 个可在 6 周内完成、可复现、可发表的深度研究方向，并逐一评估科学价值 / 可行性 / 资产复用度 / 风险。
> **文献检索**: OpenAlex API（本地 search MCP / WebSearch / WebFetch 在此环境不可用）。所有引用可追溯（标题 + DOI）。

---

## 0. 核心诊断：阴性结果打开了一条更干净的路

N=15 组间设计的核心教训：**组间设计无法分离语言效应与个体差异**（Split-Half 底 ≈ 观测 LDS-C ≈ 标签置换）。这同时指出了唯一科学上干净的补救路径：

> **把"参与者"换成受控的 LLM —— 同一个模型，用 ZH/DE/EN 三种语言提示词回答同一组问题。** 此时"参与者"恒为同一权重集合，语言是唯一变化量 —— **组内设计在构造上成立**，组间混淆彻底消失。这一设计同时满足"可复现""低成本（复用 deepseek API）""6 周内可完成"三个约束。

下文 D1 即基于此诊断；D2–D4 为互补方向。

---

## D1. LLM-as-Subject 组内设计：语言驱动的概念图分歧（**最优先，主推**）

### 科学问题
将 ΔLDS 假说（语言 → 认知概念图分歧）放到**真正可检验**的设计上：
> 同一 LLM（deepseek-v4-flash）分别用 ZH / DE / EN 提示词回答 5 个社会主题开放题 → 每语言 3 次独立采样 → 提取概念图 → LDS-C 语言对比较 → 组内 Split-Half（同一语言 3 次采样间）作为噪声底 → 若 LDS-C(跨语言) > Split-Half(语言内)，则语言驱动信号存在。

### 文献锚点（直接支撑该方法的合法性）
| 引用 | 要点 |
|------|------|
| Binz & Schulz, *PNAS* 2023, "Using cognitive psychology to understand GPT-3" (DOI 10.1073/pnas.2218523120) | **LLM 作为认知被试**的范式奠基：把认知心理学任务套到 LLM 上检验其行为是否匹配人类模型。本项目将其推广为"多语言条件化被试"。 |
| *Behav Res Methods* 2026, "How well do LLMs mirror human cognition of word concepts?" (DOI 10.3758/s13428-025-02938-2) | **直接先例**：检验 LLM 概念认知是否镜像人类 —— 与本项目概念图提取完全同构。 |
| *Behav Res Methods* 2026, "Adding LLMs to the psycholinguistic norming toolbox" (DOI 10.3758/s13428-026-03129-3) | LLM 已开始替代人类心理语言学评分的实践路线。 |
| Arora et al., *PNAS Nexus* 2024, "Cultural bias and cultural alignment of large language models" (DOI 10.1093/pnasnexus/pgae346) | **同一模型存在语言条件化文化偏置** —— 直接为"语言提示改变 LLM 行为"提供证据。 |
| Zhu et al., *PNAS* 2024, "GPT is an effective tool for multilingual psychological text analysis" (DOI 10.1073/pnas.2308950121) | 多语言 LLM 心理文本分析的可靠性。 |
| Grossmann et al., *PNAS Nexus* 2024, "Perils and opportunities in using LLMs in psychological research" (DOI 10.1093/pnasnexus/pgae245) | 诚实地报告 LLM-as-subject 的边界（幻觉、模板化、采样方差）—— 论文方法学部分直接可引用。 |

### 科学价值
1. **直接回答 RQ3 的净化版本**：语言是否改变同一认知架构输出的概念结构？不再受参与者混淆污染。
2. **ΔLDS 可重算**：LLM 概念级 LDS-C（语言对）对比已有 LDS-K（教材），检验"人类/模型认知表达 vs 制度知识"的三方结构。
3. **方法学贡献可发表**：把"LLM 作为多语言组内被试"系统化，是心理语言学研究范式的新应用（对标 Binz & Schulz 路线）。

### 可行性（复用现有资产）
| 步骤 | 复用 | 新增工作量 |
|------|------|-----------|
| 三语提示词（5 主题 × 3 语言 × 3 采样 = 45 次调用） | `lds_c_extract.py` 的提示词/抽取机制（改语言条件） | 低（改 SYSTEM_PROMPT + 语言参数） |
| 概念提取 | 同上（deepseek-v4-flash，max_tokens=8192） | 0（机制已验证） |
| 对齐 + LDS-C + Bootstrap + Split-Half | `lds_c_compute.py`（canonical_key 已就绪） | 低 |
| 主题分类（若做方向分析） | `lds_c_thematic.py`（6 类 Codebook） | 低 |
| ΔLDS vs 教材 | 已有 LDS-K 数值 | 0 |

### 风险 / 边界（须在论文诚实报告）
- LLM 采样方差 vs 人类个体差异——这不是缺点而是**受控优点**，但需如实说明"模型 ≠ 人类认知"。
- deepseek 推理爆炸坑（`.env` 已配；大调用仍可能 `finish=length`）→ 沿用"按主题小调用 + 空结果显式重试"对策。
- 文化偏置可能来自训练语料而非"语言本身"——这正是可讨论的机制问题，不是缺陷。

### 一句话
**主推。** 成本最低、复用度最高、直接补上组间设计的漏洞，且有 2023–2026 文献背书。

---

## D2. 跨语言嵌入空间分析：5 主题在三语语义空间中的邻域结构（互补，可并行）

### 科学问题
不依赖显式概念图，直接在多语言嵌入空间中测：
> 同一批概念（如 Freiheit / Gerechtigkeit / …）在 LaBSE / mBERT / XLM-R 三语对齐空间中，其 ZH 邻域 vs DE 邻域 vs EN 邻域是否显著不同？用最近邻重合度、邻域拓扑、概念间距离矩阵相似度量化。

### 文献锚点
- *ACL* 2022, "Challenges and Strategies in Cross-Cultural NLP" (DOI 10.18653/v1/2022.acl-long.482) —— 跨文化 NLP 的方法论批判与对策。
- *COLI* 2023, "Can LLMs Transform Computational Social Science?" (DOI 10.1162/coli_a_00502) —— LLM 文本→构念映射的规范。
- SimLex-999 (Hill, Reichart & Korhonen, *Computational Linguistics* 2015, DOI 10.1162/coli_a_00237) 与 BabelNet (Navigli & Ponzetto 2010) —— 语义相似度 / 多语语义网络的既有基准（DOI 需二次核验后再引用）。

### 科学价值
- 提供**不依赖人工提取的对偶证据**：若嵌入空间也无语言信号 → 三层阴性升级为四层一致；若嵌入有信号而显式图无 → 证明信号藏在语义表征而非表面词集。
- 直接回答"对齐是否是瓶颈"（此前仅 5% 词法合并）的更严格版本。

### 可行性
需 LaBSE/mBERT（`sentence-transformers` 或 HuggingFace）—— 本地跑；语料 + 15 份人类 gloss 均可作为锚概念。工作量大头在脚本，无 API 成本。

### 风险
中文网络环境下载 HF 模型可能受阻（需镜像/离线）。评估：中。

---

## D3. 跨语言自由联想规范（SWOW）对照：人类概念图的语言特异性来源（验证性）

### 科学问题
> 人类概念图的跨语言差异，究竟来自"语言结构"还是"联想统计"？用跨语言自由联想规范（SWOW：英语/中文/西语已发布）作为独立基准：若人类概念图语言间差异与 SWOW 语言间差异同构 → 概念图差异是联想统计的副产物而非语言认知驱动。

### 文献锚点
- De Deyne et al., *Behav Res Methods* 2019, "The 'Small World of Words' English word association norms for over 12,000 cue words" (DOI 10.3758/s13428-018-1115-7) —— SWOW-EN。
- *Behav Res Methods* 2024, "A large-scale database of Mandarin Chinese word associations from the Small World of Words Project" (DOI 10.3758/s13428-024-02513-1) —— SWOW-ZH（直接可用作中文联想底）。
- *Behav Res Methods* 2023, SWOW-Rioplatense Spanish —— SWOW 多语可扩展性的先例。

### 科学价值
- 给阴性结果一个**机制解释**：若概念图差异 ≈ 联想规范差异 → 差异源于统计规律（语料分布）而非认知组织 → 深化 §4.6 的方法学反思。
- 发表角度：作为 ΔLDS 框架的验证层，回答"度量的是什么"这一审稿人必问问题。

### 可行性
SWOW 数据集公开可下（EN/ZH）；DE 版本缺失是限制——可用 LLM 生成对照或仅做 EN/ZH 两语。评估：中（数据获取需网络）。

---

## D4. 语法性别式 Whorfian 探针 + 概念图（拓展，可选）

### 科学问题
复制心理语言学经典的"语法性别→属性归类"范式（德语桥/钥匙 vs 西语相反性别），但用**概念图 + LLM 分类**替代人工评分：
> 对 DE 有语法性别的社会概念，LLM（DE 条件）与 LLM（EN/ZH 条件）对被试给出的属性归类是否不同？—— 在**受控被试**下重新检验"语言语法结构 → 认知归类"。

### 文献锚点
- Sato & Athanasopoulos, *Psychon Bull Rev* 2019, "Grammatical gender and linguistic relativity: A systematic review" (DOI 10.3758/s13423-019-01652-3) —— 该范式的系统综述与批评。
- *Front Lang Sci* 2016, "Neurolinguistic Relativity" (DOI 10.1111/lang.12186) —— 神经语言学相对性的机制。

### 科学价值
- 若 DE 语法性别概念在 LLM 三语条件下产生不同归类 → **语法驱动的信号**（比词集更深的语言结构层）。
- 与 D1 形成"表层（词集）vs 深层（语法）"双探针叙事。

### 可行性
需设计属性配对（桥/钥匙范式）到社会概念域 —— 有一定设计难度；LLM 分类用 6 类 Codebook 或新 Codebook。评估：中。

---

## 综合建议

| 方向 | 科学价值 | 6 周可行性 | 资产复用 | 建议 |
|------|:-------:|:----------:|:--------:|:----:|
| **D1 LLM-as-Subject 组内设计** | ★★★★★ | ★★★★★ | ★★★★★ | **立即做（主）** |
| **D2 嵌入空间分析** | ★★★★☆ | ★★★★☆ | ★★★★☆ | 与 D1 并行（可佐证） |
| D3 SWOW 对照 | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | D1 后按需做（机制解释） |
| D4 语法性别探针 | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | 时间允许再做（拓展） |

**推荐执行序列**（6 周内）：
1. **W1–W2**：D1 三语 LLM 数据采集（45 调用）+ LDS-C + 组内 Split-Half + ΔLDS 重算 → 产出 D1 结果表。
2. **W2–W3**：D2 嵌入空间分析（与 D1 结果交叉验证）。
3. **W3–W4**：论文整合 D1/D2 结果 + 方法学章节（LLM-as-subject 范式 + 诚实边界）。
4. **W4–W5**：D3 SWOW 对照（若网络/数据可用）作为机制解释层。
5. **W6**：数字 SSOT 对齐 + 提交组装。

**D1 是唯一能把"阴性结果"转化为"干净设计下的新证据"的方向** —— 它不推翻阴性结论，而是把"语言效应是否存在"重新放回一个可以回答问题的实验设计上。

---

## 引用清单（全部可追溯）

1. Binz & Schulz (2023). *PNAS*. DOI 10.1073/pnas.2218523120
2. (2026). *Behav Res Methods*. DOI 10.3758/s13428-025-02938-2
3. (2026). *Behav Res Methods*. DOI 10.3758/s13428-026-03129-3
4. Arora et al. (2024). *PNAS Nexus*. DOI 10.1093/pnasnexus/pgae346
5. Zhu et al. (2024). *PNAS*. DOI 10.1073/pnas.2308950121
6. Grossmann et al. (2024). *PNAS Nexus*. DOI 10.1093/pnasnexus/pgae245
7. Hershcovich et al. (2022). *ACL*. DOI 10.18653/v1/2022.acl-long.482
8. Ziems et al. (2023). *COLI*. DOI 10.1162/coli_a_00502
9. De Deyne et al. (2019). *Behav Res Methods*. DOI 10.3758/s13428-018-1115-7
10. (2024). *Behav Res Methods*. DOI 10.3758/s13428-024-02513-1
11. Sato & Athanasopoulos (2019). *Psychon Bull Rev*. DOI 10.3758/s13423-019-01652-3
12. (2016). *Front Lang Sci*. DOI 10.1111/lang.12186
13. Hill, Reichart & Korhonen (2015). *Computational Linguistics*. DOI 10.1162/coli_a_00237 (SimLex-999)
