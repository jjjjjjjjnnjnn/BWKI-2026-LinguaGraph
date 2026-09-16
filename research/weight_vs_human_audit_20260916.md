# 人类教材图 vs 权重向量图只读审计（Lane-3，2026-09-16）

> **只读审计**：未修改 `tests/`、`freeze/`、`_deploy/`、`data/` 既有文件、`linguaGraph.db`；新增概念 0（≤20 红线内为 0）；未扩语料；未改 LDS v3 公式（LDS Jaccard 形式为 `docs/lds_formal_definition.md §8.1` 逐字复用）。
> **本文件所有新统计均为 exploratory appendix-only**，不得进入主结论。
> 脚本：`scripts/tools/weight_graph_audit.py`（新建，stdlib-only）→ 输出 `research/weight_graph_audit_20260916.json`（本 Lane 唯一机器输出）。
> 输入（复用，不重跑大模型）：219 对齐组 / 434 主对（`data/math_extractions/merged/aligned_data.json` 冻结表）+ nomic 768 维聚合距离（`%TEMP%/opencode/openweight_embed_audit.json` 只读复核）。

## 0. 输入核验（EXECUTED，实测）

| 核验项 | 实测值 | 来源 |
|---|---|---|
| 对齐组 | **219** | `aligned_data.json` 重数（脚本 R1） |
| 主对总数 | **434**（zh-de 65 / zh-en 184 / de-en 185） | 同上，与 `two_tier_benchmark_20260914.md §1` 一致 |
| 表面相同剔除 | de-zh **154**、en-zh **35**、de-en **34**（合计 223；657−223=434 ✓） | 脚本 R1（归一化=小写+去空格/连字符/下划线+ß→ss） |
| 空标签组 | **0** | 脚本 R1 |
| 向量聚合复核 | 四格 n/mean 与 Two-Tier 报告**逐格一致**（match=true） | 脚本 R2（只读 TEMP 缓存） |
| 人类教材图稀疏基线 | 556 节点 / 238 边 / 无向密度 **0.001543** / 平均度 **0.8561** / 稀疏度 0.998457 | 脚本 R3（`visualization_data.json` 只读） |
| LM Studio 探针 | **OFFLINE**（`127.0.0.1:1234` connection refused） | 脚本 R4（本次 PENDING 的直接原因） |

冻结引用值（复述，不重算）：LDS-K zh-en **0.934**、de-en **0.938**、zh-de **0.519**（`scripts/analyze_human_lds.py:23-28`）；向量 drift 均值 zh-en **0.5249**、de-en **0.4888**、zh-de **0.4804**（Two-Tier §2）。

## 1. E1–E3 方法与执行状态

### E1 — kNN 图 LDS-VEC（k=5/10/15）：**PENDING（未执行）**

- 方法：以 219 对齐标签为节点集（分语言 zh/en/de），用 nomic 768 维向量余弦距离建对称 kNN 图（k=5/10/15），逐语对以冻结 LDS Jaccard 公式算 LDS-VEC。脚本内 `knn_edges()` + `lds_jaccard()` 已实现，`--vectors <term2vec.json>` 传入 934×768 词矩阵即转 EXECUTED。
- 未执行原因：**逐词向量从未落盘**——TEMP 缓存只有逐语对聚合（mean/std/min/max），`sem_emb_cache.json` 的 10615×768 是英文语料**句子**向量（对象错误，不可代用）；LM Studio 离线，本 Lane 禁止重跑大模型。
- 所需模型：`text-embedding-nomic-embed-text-v1.5` 经 LM Studio `http://127.0.0.1:1234/v1`（或等价持久化 934×768 词矩阵），恢复在线后重嵌 934 去重概念词。

### E2 — 频次–相似偏相关：**PENDING（未执行）**

- 方法：Spearman + 偏相关（控制表面形式同一性），ZH-DE vs EN 分开报。
- 未执行原因：**无冻结数学语料频次表**。`data/corpus/corpus_analysis.json` 是维基**社会主题**试点（freedom/justice 等），领域错配，禁止代用；教材原文 referenced-only 未版本化，新建频次表=扩语料（红线禁止）；逐对（n=434）余弦距离亦无落盘（仅聚合）。
- 所需数据：已用数学教材暴露集的**冻结**逐概念频次（零新文本）+ 持久化 434 对逐对距离。

### E3 — 稀疏度匹配对照：**PARTIAL（人类侧 EXECUTED，向量侧 PENDING）**

- 人类侧已执行（§0 表 R3）：未来 kNN 图必须先稀疏度匹配（同密度/同边数，对照目标：密度 0.001543 / 平均度 0.8561；k=5/10/15 时每语言对称化后上界 ≤1095/2190/3285 边）再比 LDS-VEC vs LDS-K，否则两边稀疏度不同，Jaccard 不可比。
- 向量侧 PENDING：同 E1 所需模型。
- ZH-DE vs EN 分层报告：已执行计数组（65/184/185），向量侧数值比较 PENDING。

## 2. 污染四分叉表

| # | 分支 | 状态 | 说明 |
|---|---|---|---|
| 1 | 频次污染（预训练频次驱动相似，非结构） | **PENDING** | 同 E2：无数学频次表，扩语料被禁。所需：冻结数学频次 + 逐对距离 |
| 2 | 改写污染（复述/翻译改写样本，字面去重检不出；Yang et al. 2023） | **PENDING** | 本 Lane 无新权重运行；现有 `norm()` 字面去重按文献不足以保证干净。所需模型：**多语言 paraphrase 嵌入模型或 LLM 语义去污染判官**（本地无在线权重；LM Studio 离线），对 934 词 + 434 对做语义级去污染声明 |
| 3 | ZH-DE 不对称（主对最薄 n=65，多数组表面相同被剔除） | **PARTIAL（重数 EXECUTED，解释降权）** | 实测剔除 de-zh 154（§0）。采信规则见 §4 |
| 4 | 层间混淆（向量层↔图谱层跨量纲误读） | **PENDING（权重侧层特异性检验）；方法学护栏 EXECUTED（§3 禁比声明）** | 完整层间分离检验需 E1 向量（kNN 序结构是否复现图谱序结构）。所需模型：同 E1（nomic-embed-text-v1.5 在线或 934×768 矩阵）。在向量落盘前，只许 §3 的护栏式陈述，不许层间数值结论 |

## 3. 跨量纲禁比数值声明（EXECUTED 护栏）

- 余弦距离（分布复述邻近度）与 LDS-K=`1−mean(节点/边 Jaccard)`（课程结构差异）**无公共量纲**，禁止一切数值直比。
- 只许"序结构"陈述：向量三语对均值极差 **0.0445**（窄带）vs 图谱 LDS-K 极差 **0.419**（≈9.4 倍，结构化）；向量序 zh-en> de-en >zh-de 未复现图谱序 zh-en≈de-en≫zh-de。
- 禁句：不许说"向量验证/证实了 LDS-K 数值"；zh-de 两列接近（−0.0386）纯属量纲巧合。
- 以上复述 `two_tier_benchmark_20260914.md §3`，本 Lane 未改任一数字。

## 4. EN 上限 / ZH-DE 采信规则（EXECUTED 规则）

- **EN 上限**：涉 EN 向量断言永远停在分布级（"向量层未复现图谱层语对序结构"），不许下沉到单概念验证句；任何 EN 结论需 E1 落盘后重审。
- **ZH-DE 采信规则**：zh-de 主对 n=65 为三语对最薄（剔除主因=中德表面同形 154 组），估计降权；**永不以 zh-de 单独承载结论**，三语对必须并列报告。

## 5. PENDING 解锁清单（需新权重/数据，不在本 Lane 执行）

1. LM Studio 恢复（`text-embedding-nomic-embed-text-v1.5` 在线）→ 重嵌 934 词 → E1/E3-向量侧/分支 4 权重检验转 EXECUTED。
2. 多语言 paraphrase 嵌入或 LLM 语义去污染判官在线 → 分支 2 转 EXECUTED。
3. 冻结数学频次表（零新文本口径）+ 434 逐对距离落盘 → E2/分支 1 转 EXECUTED（若需新文本则超出红线，须另立 Lane 审批）。
