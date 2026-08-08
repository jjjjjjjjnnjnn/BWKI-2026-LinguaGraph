# LinguaGraph — 完整项目状态交接文档（研究重启后 v0.9）

> **生成时间**: 2026-08-08 | **版本**: v0.9（v0.8 + 设计效应证明 A3 + A5 分歧驱动者 + 节点/边分解 D）
> **上一交接**: v0.8（已被 v0.9 取代）
> **新 AI 加载顺序**: ① 本文件 → ② `docs/planning/restart_plan.md` → ③ `.claude/CLAUDE.md`（治理）

---

## 1. 当前阶段与核心状态

**阶段**: Month 2「理论 + 分析」（8 月）。BWKI 提交截止 **2026-09-20/21**（约 6 周）。

**研究主线（已完成，三层完整证据链 + 深化证明）**:

> **"语言是否驱动认知概念结构分歧？"——是，但只在剥开制度知识强制统一之后可见；且人类组间阴性已被证明是设计伪影（信号幅度与 LLM 相同，差异在底噪）。**

| 层 | 结果 | 一句话 |
|----|------|--------|
| 人类 N=15 组间 | 阴性（LDS-C ≈ 噪声底） | 组间设计测不出 → **设计伪影** |
| **LLM 组内（D1）** | **阳性（LDS-C ≫ 底）** | 同一模型三语 → **语言信号真实存在** |
| **设计效应证明（A3）** | **人类/LLM 信号幅度相同（0.93-0.96），底噪不同（0.92-0.96 vs 0.85-0.87）** | **人类阴性 = 组内个体异质性，非"无效应"、非"组间设计本身"** |
| 语料深化（A4） | 社会 Wikipedia ZH-DE 0.82 vs 数学 0.52 | **制度知识抹平语言，文化概念暴露语言** |
| 机制（LMM） | 代码层主导，框架次级 | 语言像轨道，文化框架是轨道内小车 |
| **分歧驱动者（A5/C）** | ZH-DE 由框架负载概念驱动（DE 自主/规则 vs ZH 空间/应得） | **RQ4 已答** |
| **节点/边分解（D）** | 反转是节点驱动；边贡献数学最大（0.074） | **制度收敛于概念选择，关系组织仍分歧** |

**三大不可违反原则**（.claude/CLAUDE.md §1）: SSOT=manifest.json · Immutable Release · Validated Pipeline。

---

## 2. 数据状态

### 2.1 人类数据 SSOT（已完成，勿重跑）
| 批次 | 语言分布 | 状态 |
|------|---------|------|
| `freeze/freeze_survey_20260703/` | 6 DE + 5 ZH | ✅ 已提交 (57257ac) |
| `freeze/freeze_survey_20260712/` | 1 ZH + 3 EN | ✅ 已提交 (4317bd8) |
| **合计** | **15 合格（6 DE + 6 ZH + 3 EN）** | 3 EN 为双语 ZH 母语者，作试点 |

### 2.2 LLM-as-Subject 数据（D1，已完成，勿重跑）
`data/lds_c/llm_subject/`：
- `llm_subject_20260808.json` — 220 units（P1 30 + P2 20 + P3 150 + P5 20），0 空
- `assoc_gloss_20260808.json` — 285 联想词英文化（15/15 cell）
- `wiki_gloss_20260808.json` — 96 个 ZH+DE Wikipedia 概念英文化（A4 用）

### 2.3 分析结果
- `data/lds_c/` — 人类三层分析（概念/主题/关系）
- `data/lds_c/llm_subject/analysis_20260808.json` — D1 四探针机制结果
- `data/lds_c/llm_subject/lmm_20260808.json` — 混合效应模型
- `data/lds_c/llm_subject/per_topic_20260808.json` — 主题分解
- `data/lds_c/lds_k_deep/lds_k_deepen_20260808.json` — A4 语料深化

**API key**: `.env`（gitignored）存 `OPENAI_API_KEY`（opencode GO，deepseek-v4-flash）。**⚠️ key 曾出现在对话中，建议轮换**。端点 `https://opencode.ai/zen/go/v1`。

---

## 3. 核心科研发现（完整证据链）

### 3.1 人类 N=15 组间：三层一致阴性（§3.1–3.3 沿用 v0.7）
概念级 LDS-C 0.93–0.96 ≈ split-half 底 ≈ 标签置换 → 组间参与者变异性主导。

### 3.2 🔑 D1 LLM-as-Subject 组内设计（核心突破）
同一模型（deepseek-v4-flash）分别用 ZH/DE/EN 回答同 5 主题 → **组内设计构造上成立**（语言是唯一变化量）。

| 语言对 | LDS-C (pooled) | 95% CI | 组内 Split-Half 底 | 标签置换 |
|:---:|:---:|:---:|:---:|:---:|
| ZH-EN | 0.955 | [0.935, 0.966] | 0.875 | 0.879 |
| DE-EN | 0.930 | [0.912, 0.955] | 0.846 | 0.880 |
| ZH-DE | 0.945 | [0.932, 0.961] | 0.862 | 0.879 |

**LDS-C 超出噪声底 +0.08~0.09 → 语言信号真实存在。** 与人类组间阴性对比 → **人类阴性是设计伪影**（组间混淆语言与个体差异）。

### 3.3 LMM 机制判定（D1 核心修正）
`y ~ same_lang + same_frame + (1|topic)`，50 dyadic cell-pairs：
- **same_lang +0.038 (p<0.001, 置换 p=0.000)** → **语言代码是主导组织层（M2 词汇/联想统计）**
- **same_frame +0.001 (p=0.90, 置换 p=0.779)** → **文化框架无跨代码边际贡献（次级，代码内调节器）**

> ⚠️ **早期 P2 表述已纠正**："框架 ≈ 跨语言效应 → M3 主机制" 是过度解读。框架效应 LDS 0.91 是同代码轨道内差异（J 0.12→0.088），非跨代码（0.088 ≫ 全异基线 0.05）。**代码层主导，框架次级。**

### 3.4 语料深化（A4）—— 社会 vs 制度模式相反
**方法学修复**：Wikipedia 负对照此前 LDS=1.0 是**未对齐伪影**（ZH 概念 → 空 key）。补齐 96 词英文化后：

| 来源 | ZH-EN | DE-EN | ZH-DE |
|:---|:---:|:---:|:---:|
| 数学教材（制度知识） | 0.934 | 0.938 | **0.519** |
| Wikipedia 社会（文化知识） | 0.698 | 0.723 | **0.819** |

**ZH-DE：数学最趋同（0.52）→ 社会最分歧（0.82）——模式相反！** 制度知识由普遍逻辑驱动 → 语言趋同；社会文化概念由语言/文化框架驱动 → 语言分歧。为"语言效应存在但被制度知识掩盖"提供语料侧直接证据。

**其他 A4 发现**：
- 数学 ZH-DE 收敛贯穿全部教育阶段（0.39–0.80），ZH-DE 边分量贡献 3–4×（0.075）
- 跨源空模型（§3.6 首次实现）：教材-vs-Wiki=1.0 是**域混淆**（数学⊥社会）；同域跨源 Wiki(zh)-vs-Human(zh)=0.94 → 来源是强驱动但语言效应独立
- 敏感性全维度稳健：方向 Δ≤0.004、对齐松紧 Δ≤0.05、重要性阈值 Δ≤0.02

### 3.5 机制分解总结
| 机制 | 判定 | 证据 |
|:---|:---:|------|
| M1 表层词法 | 证伪 | 对齐只合并 ~5% |
| **M2 联想统计（代码层）** | **主机制** | LMM same_lang +0.038 (p<0.001)；EN 对概念分歧≈联想分歧 |
| M3 文化框架 | 次级 | 同代码内有效（P2），无跨代码贡献（LMM p=0.90） |
| M4 采样方差 | 控制为底 | k=10 Split-Half |
| M5 提示语条件化 | 证伪 | P5 0.815 < 组内底 |

### 3.6 🔑 设计效应证明（A3，v0.9 新增）
`scripts/lds_c_design_effect.py` → `design_effect_20260808.json`。把"人类阴性 = 设计伪影"从推断升级为**定量证明**：

| 语言对 | 人类 LDS-C | 人类底 | 人类 s/f | LLM LDS-C | LLM 底 | LLM s/f |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| ZH-EN | 0.963 | 0.958 | 1.005 | 0.955 | 0.875 | **1.092** |
| DE-EN | 0.932 | 0.924 | 1.009 | 0.930 | 0.846 | **1.100** |
| ZH-DE | 0.936 | 0.922 | 1.015 | 0.945 | 0.862 | **1.096** |

1. **信号幅度相同**：人类与 LLM 的 LDS-C 均 0.93–0.96 → 人类阴性**不是"无语言效应"**。
2. **差异在底噪**：人类组内个体异质性（0.92–0.96）≈ 信号 → 淹没；LLM 同权重采样（0.85–0.87）≪ 信号 → 可见。
3. **非样本量效应**：LLM 在 N=3/语 仍有信号（margin +0.02–0.04），N=10 达 +0.08。
4. **决定性对照（virtual between-subject lens）**：LLM 样本按人类组间管线 + 人类 N（6/语）重分析，**信号仍存活**（margin +0.06–0.07）→ 人类阴性既非"无效应"也非"组间设计本身"，而是**组内个体异质性**这一方差源。

### 3.7 A5 分歧驱动者（RQ4 已答，v0.9 新增）
`scripts/lds_c_divergence_drivers.py` → `divergence_drivers_20260808.json`。
- ZH-DE 分歧由**框架负载文化概念**驱动：DE 侧 equal opportunity / freedom limit / goal own（自主/规则/目标），ZH 侧 physical space / boundary freedom / due treatment（空间/边界/应得）——与 §4.4 方向性趋势互相印证。
- 共享概念极少（每语言对 20–27，跨 5 主题）→ 与 LDS-C ≈ 0.93–0.96 一致。
- 关系驱动者（人类）：DE-only `responsibility→consequence`，ZH-only `success→goal` → 结构性分工同样存在。

### 3.8 节点/边分解（D，v0.9 新增）
`scripts/lds_c_node_edge_decomp.py` → `node_edge_decomp_20260808.json`。
社会/制度反转（数学 ZH-DE 0.52 vs 社会 0.82）分解后：

| 来源 | node-only LDS | 边贡献 |
|:---|:---:|:---:|
| 数学 | **0.444** | **0.074** |
| Wikipedia 社会 | **0.800** | 0.019 |
| 人类认知 | 0.915 | 0.038 |

**反转是节点驱动的**（数学最趋同 vs 社会最分歧在概念选择层）；边分量不反转——数学边贡献**最大**（0.074）。**制度知识收敛于"教什么"（概念），"怎么连接"（关系）仍系统性分歧。** 修正 A4 §3.8 表述：0.075 是"边驱动的分歧"，非"边驱动的趋同"。

---

## 4. 已构建的脚本（全部可复现）

| 脚本 | 功能 | 关键点 |
|------|------|--------|
| `scripts/lds_c_extract.py` | 人类概念提取 | deepseek，按主题，英文 gloss，三重回退 |
| `scripts/lds_c_compute.py` | 概念级 LDS-C | canonical_key、Bootstrap、split-half、标签置换 |
| `scripts/lds_c_thematic.py` | 主题级分析 | 6 类 Codebook，BATCH≤15，χ²+置换 |
| `scripts/lds_c_extract_relations.py` | 关系提取 | 7 类型，按主题，8192 token |
| `scripts/lds_c_compute_v3.py` | v3 节点+边 LDS | 冻结公式 |
| **`scripts/lds_c_llm_subject.py`** | **D1 采集** | P1/P2/P3/P5，k=10，per-topic 作答（避爆炸），独立 session，断点续跑 |
| **`scripts/lds_c_llm_gloss_assoc.py`** | P3 联想英文化 | canonical_key 只认拉丁 → 必须 gloss |
| **`scripts/lds_c_llm_analyze.py`** | D1 机制分析 | P1-P5 判定 + 空模型 |
| **`scripts/lds_c_llm_per_topic.py`** | 主题分解 | P1/P2/P3 每主题 |
| **`scripts/lds_c_llm_lmm.py`** | **混合效应模型** | scipy 实现（无需 statsmodels），50 dyadic pairs |
| **`scripts/lds_k_wiki_gloss.py`** | **Wikipedia 英文化** | 96 ZH+DE 概念 |
| **`scripts/lds_k_deepen.py`** | **A4 语料深化** | 主题分解+敏感性+跨源空模型 |
| **`scripts/lds_c_design_effect.py`** | **设计效应证明（A3）** | 信号幅度相等 + 底噪 + N-scan + 虚拟组间 lens |
| **`scripts/lds_c_divergence_drivers.py`** | **A5 分歧驱动者（RQ4）** | 概念/关系不对称 + 频次加权 |
| **`scripts/lds_c_node_edge_decomp.py`** | **节点/边分解对称（D）** | 三来源反转分解，复用 lds_k_deepen |
| **`scripts/figures/fig_a7_core.py`** | **A7 核心图表** | 5 图 + CSV |

**复现顺序**：`lds_c_llm_subject.py` → `lds_c_llm_gloss_assoc.py` → `lds_c_llm_analyze.py` + `lds_c_llm_per_topic.py` + `lds_c_llm_lmm.py`；`lds_k_wiki_gloss.py` → `lds_k_deepen.py`；**深化**：`lds_c_design_effect.py` + `lds_c_divergence_drivers.py` + `lds_c_node_edge_decomp.py` → `fig_a7_core.py`。

---

## 5. ⚠️ 关键踩坑（新 AI 必读）

1. **deepseek-v4-flash 推理爆炸**: 多词聚类/关系任务 `finish=length, reasoning=8192, content=''`。
   - **对策**: 分类 BATCH≤15；**作答按主题小调用（per-topic，整卷会爆炸）**；空结果显式重试；断点续跑。
2. **`.env` key 曾入对话** → 建议轮换。
3. **GitHub 不可连接** → 只用本地 git。
4. **对齐是瓶颈的误判**: 词法对齐只合并 5% → 高 LDS 非对齐噪音。
5. **`outputs/` 被 gitignore** → 结果存 `data/lds_c/` 才入库。
6. **canonical_key 只认拉丁字符** → ZH 概念（人类/LLM/Wikipedia）必须英文化后才能对齐，否则 LDS=1.0 伪影。
7. **Wikipedia LDS=1.0 是伪影非负对照** → 已修复（A4 §3.4）。
8. **uv/pip 安装 statsmodels 曾失败**（网络）→ LMM 用 scipy 实现，无新依赖。

---

## 6. 论文状态

| 文件 | 状态 |
|------|------|
| `docs/paper/03_results.md` | ✅ §4 N=15 + **§5 LLM-as-Subject + §3.8 A4 + §5.9 A3/C/D 深化** |
| `docs/paper/04_discussion.md` | ✅ F11/F12 + §4.14 LLM 方法学 + 设计伪影精确化 + 节点/边解读 |
| `docs/paper/05_conclusion.md` | ✅ N=15 + D1 + Wikipedia 修正 |
| `docs/paper/00_three_conclusions.md` | ✅ N=15 + D1 叙事 |
| `docs/paper/01_abstract_introduction.md` | ✅ N=15 + D1 摘要 |
| `docs/lds_formal_definition.md` | ✅ §4 Wikipedia 负对照 + §6 证伪表 + **§6.2 设计效应 + §6.3 节点/边分解** |
| 其余章节 (02,06,07) | 未受影响 |

---

## 7. 待办事项（按优先级）

### P0 — 提交前必做（9 月中旬）
- [ ] **manifest 数字口径对齐**（A0 遗留: 556/557、219/247）— 唯一遗留的治理项
- [ ] **A6 模拟基线调和**（0.647 vs 0.667）— 论文 §4.8 已标注"方法上不再成立"，可标注为历史
- [ ] 最终 Release 打包 + 视频演讲（BWKI 评分项）

### P1 — 已完成（本会话 v0.9）
- [x] **D1 LLM-as-Subject 组内设计**（采集+分析+LMM+主题分解）
- [x] **A4 LDS-K 深化**（主题分解+敏感性+跨源空模型）
- [x] **A7 核心图表**（ΔLDS、主题热图、空模型、机制、敏感性）
- [x] **A3 设计效应证明**（信号幅度相等 + 底噪 + N-scan + 虚拟组间 lens）
- [x] **A5 分歧驱动者（RQ4）**（ZH-DE 框架负载概念 + 关系驱动者）
- [x] **D 节点/边分解**（反转是节点驱动，边不反转）
- [x] **论文整合**（D1 + A4 + A3 + A5 + D 全部写入）

### P2 — 未来研究（讨论部分 Future Work）
- [ ] 组内设计 Human 新数据（D1 提供设计蓝图）
- [ ] EN 补量至 10 / 换非推理模型重跑语义规范化
- [ ] D2 嵌入空间分析 / D3 SWOW 对照（方向文档已备）

---

## 8. 关键文档索引

| 资源 | 位置 |
|------|------|
| 研究重启计划 | `docs/planning/restart_plan.md` |
| 方向探索（D1-D4） | `docs/planning/research_directions_20260808.md` |
| **D1 机制设计** | `docs/planning/d1_mechanism_design.md` |
| **D1 机制结果** | `docs/d1_mechanism_results.md` |
| **A4 语料深化结果** | `docs/a4_ldsk_deepen_results.md` |
| LDS 正式定义 | `docs/lds_formal_definition.md` |
| 项目治理 | `.claude/CLAUDE.md` |
| 人类数据 SSOT | `freeze/freeze_survey_20260703/` + `freeze_survey_20260712/` |
| 图表 | `outputs/figures/fig_a7_*.png`（gitignored，可重新生成） |

---

## 9. Git 状态

**核心科学工作已全部提交**。本次会话累计提交（从 v0.7 交接后）：
- `f683ee5` D1 机制分析（语言信号可检测）
- `ff22823` D1 主题分解 + LMM（代码层主导）
- `5ad5a94` 论文整合 D1
- `1be8ede` A4 语料深化（Wikipedia 对齐修复）
- `01ce620` A7 核心图表
- `98aea29` 论文整合 A4
- `0cdd94a` legacy gloss 归档（零删除）

**未提交**: 无（`.wrangler/` 为 Cloudflare 缓存，可忽略）。

**GitHub**: `github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph`（当前不可达，仅本地）。
