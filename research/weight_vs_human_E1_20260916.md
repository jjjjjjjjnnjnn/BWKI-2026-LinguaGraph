# E1 转正执行报告：kNN 图 LDS-VEC（2026-09-16，A线）

> **状态：E1 测量 EXECUTED；解释封顶 Hypothesis。**本文件所有新统计均为 **exploratory appendix-only**，不得进入主结论。
> **红线核验**：只读 `data/` 既有（含 `data/lds_c`）、未改 `tests/`、`freeze/`、`_deploy/`、`linguaGraph.db`；新增概念 **0**；未扩语料；未改 LDS v3 公式（冻结公式 `1-(J_node+J_edge)/2`，`docs/lds_formal_definition.md §8.1` 逐字复用）。
> EN 上限 / ZH-DE 采信规则（沿用审计报告 §4）：涉 EN 断言停在分布级；zh-de（n=65）永不单独承载结论，三语对并列。

## §0 探活与向量落盘（EXECUTED）

- 探活：`GET http://127.0.0.1:1234/v1/models` **ALIVE**；可用 embedding 模型为 **`text-embedding-nomic-embed-text-v1.5`**（8 个在线模型中唯一的 embedding 模型，其余为 chat/LLM，无需替代方案，**无模型替换**）。
- 词表口径（与 `scripts/tools/openweight_embed_audit.py` 逐行一致）：`data/math_extractions/*.json` 去重概念名 **700** ∪ 434 主对增补项 → 并集 **934**（`sorted()` unicode 排序，无抽样）。
- 抽取：batch **32**（30 batch），模型 `text-embedding-nomic-embed-text-v1.5`，实测 dim=**768**。
- 落盘：`research/weight_vectors_934x768_20260916.json`（**934 行 × 768 列**，附模型名/revision/时间戳/dim/terms 排序口径；15.9MB）+ 同目录 `.term2vec.json`（纯 `{term: vec}` 平面格式，供 `--vectors` 重跑）。
  - revision：LM Studio `/v1/models` 只暴露 id 列表，**revision 不可考**（如实记录，见 §红蓝 R6）。

## §1 E1 方法（冻结）

- 节点集：219 对齐组分语言标签（实际落向量 **217/语**，缺 2 组见 §3）；对称 kNN 图（k=5/10/15，余弦距离）；逐语对以冻结 Jaccard 公式算 LDS-VEC。
- 执行：`python scripts/tools/weight_graph_audit.py --vectors research/weight_vectors_934x768_20260916.term2vec.json` → `E1_knn_lds_vec: EXECUTED`（`research/weight_graph_audit_20260916.json` 已追加 `E1_EXECUTED` 段）。

## §2 E1 结果（只比序结构，禁比数值）

| k | zh-de LDS-VEC | zh-en LDS-VEC | de-en LDS-VEC | 序（升序） |
|---|---|---|---|---|
| 5 | 0.5245 | 0.9392 | 0.9416 | zh-de < zh-en < de-en |
| 10 | 0.5309 | 0.9428 | 0.9446 | zh-de < zh-en < de-en |
| 15 | 0.5457 | 0.9476 | 0.9477 | zh-de < zh-en < de-en |

- 冻结 LDS-K 序（升序）：zh-de（0.519）< zh-en（0.934）< de-en（0.938）。
- **Rank corr**：三 k 下 LDS-VEC 序与 LDS-K 序完全一致，Spearman **ρ=1.0**（n=3，描述性；精确双侧 p≈0.333，**不显著**——n=3 时 ρ=1.0 无判别力，仅记序匹配）。
- **禁比数值声明**：不许说"向量验证/证实了 LDS-K 数值"。涉英两对 LDS-VEC≈0.94 与 LDS-K≈0.93 的接近是**量纲巧合**：en 对 J_node 恒为 ~0.081（k 无关），LDS-VEC≈0.94 几乎是"节点几乎不交"的算术推论，不是几何互证。k=15 时 zh-en 与 de-en 差仅 0.0001——禁止一切序差断言（沿用逻辑报告 T-P5-3）。

## §3 稀疏度对照与节点口径（E3-vector：已测量但 MISMATCH）

| 图 | 节点 | 边 | 密度 | 平均度 |
|---|---|---|---|---|
| 人类教材图（基线） | 556 | 238 | 0.001543 | 0.8561 |
| kNN k=5（分语言） | 217 | 642–709 | 0.027–0.030 | 5.9–6.5 |
| kNN k=10 | 217 | 1214–1345 | 0.052–0.057 | 11.2–12.4 |
| kNN k=15 | 217 | 1769–1936 | 0.075–0.083 | 16.3–17.8 |

- kNN 图比人类图密 **18–54 倍**：跨密度 Jaccard 不可比，E3 匹配对照仍缺（需 subsample kNN 至 238 边重算，列为 E3-full 前置）。
- 节点口径披露：217≠219——2 组符号标签（`math_linear_algebra_*` 两组）既不在 700 概念名中、又只出现在表面相同剔除对里，故无向量（缺失率 0.9%）；组间重复标签 22–24/语 → 自环边（如 zh k=5 有 16/709 条，2.3%）。影响量级小，但口径声明为 Developing（待 E1b 用 group-id 去重后复核）。
- J_node 组分：zh-de **0.552**（k 无关；已知 de 标签 167/219 含中文的标签交叠伪影 T1），zh-en 0.0808 / de-en 0.0812。**跨语 Jaccard 非零只能来自表面相同字符串**—— rank 匹配可能是污染的复现，不是几何的复现（见 §红蓝 R1）。

## §4 阶段门禁（Gate）

| 项 | 裁决 | 说明 |
|---|---|---|
| E1 测量 | **EXECUTED** | 934×768 落盘 + 三 k LDS-VEC + rank corr，公式冻结 |
| E1 解释 | **Hypothesis** | 污染混杂 + n=3 无力 + 稀疏失配三重封顶 |
| E3-vector | **Developing**（已测量，未匹配） | 密度失配 18–54×，匹配重算前不许比 |
| E2 / 分支1 | **PENDING**（不变） | 无冻结数学频次表 |
| 分支2（改写污染） | **PENDING**（不变） | 无语义去污染判官 |
| 分支4（层间） | 测量 EXECUTED / 解释 **Hypothesis** | 层特异性检验已跑，但混杂未除 |

## §5 红蓝对抗（§红蓝，6 攻 6 防）

- **R1 污染复现攻击**：跨语节点/边 Jaccard 的非零项只能是表面相同字符串；zh-de J_node=0.552 正是 T1 已证伪的标签交叠。ρ=1.0 可能复现的是污染结构，不是向量几何。→ **防御**：rank 结论降 **Hypothesis**；**升级路径 E1b**：以 group-id 为节点身份（对齐组内三语标签视为同一节点），边集按组 id 比较，彻底剥离表面形式后再重算 rank corr。
- **R2 稀疏度不匹配攻击**：kNN 密度是人类图的 18–54 倍；且 zh-de LDS-VEC 随 k 漂移（0.5245→0.5457），结论 k-不稳定。→ **防御**：E3 解释降 **Developing**；**升级路径**：kNN 边按权重 subsample 至 238 边（同密度）+ 同边数双重匹配后重算，k 敏感性作为必报项。
- **R3 跨量纲数值互证攻击**：0.94≈0.93 的"接近"极易被误读为互证；且 J_node 恒定使 LDS-VEC≈0.94 近乎同义反复。→ **防御**：维持禁比数值护栏，任何数值互证句直接判 **Hypothesis** 并禁止入结论；只许序结构陈述。
- **R4 zh-de 薄弱攻击**：zh-de 主对 n=65 最薄，且其 LDS-VEC 几乎完全由 J_node=0.552 锚定（边分量随 k 漂移 0.399→0.357）。→ **防御**：沿用采信规则——zh-de 永不单载，三语对并列；zh-de 单独解释 **Hypothesis**。
- **R5 节点口径攻击**：217≠219（2 组缺失）+ 组间重复标签（22–24/语）+ 自环边（2.3%）→ "节点集都不是 219，图也含自环"。→ **防御**：如实披露，影响 <3%，测量维持；口径声明 **Developing**，E1b（group-id 去重、无自环）复核后方可升 Mature。
- **R6 缓存可复现性攻击**：15.9MB 纯 JSON 无 hash、无 `.npy`；模型 revision 未暴露，换权重版本即不可复现；`--vectors` 需平面格式，归档 JSON 不能直接喂脚本。→ **防御**：已记 timestamp+model id+dim+terms 口径双文件互备；可复现性 **Developing**；**升级路径**：补 sha256 + `.npy` 双格式 + LM Studio 模型文件 hash，下轮补齐。

## §6 解锁清单更新

1. E1b（group-id 节点身份 + 稀疏匹配重算）→ 本报告 Hypothesis/Developing 项的唯一升级路径。
2. E2/分支1：仍需冻结数学频次表（零新文本口径），否则保持 PENDING。
3. 分支2：仍需多语言 paraphrase 判官，保持 PENDING。

## §7 输出清单

- `research/weight_vectors_934x768_20260916.json`（934×768 + 元数据）/ `.term2vec.json`（重跑平面格式）
- `research/weight_graph_audit_20260916.json`（`E1_knn_lds_vec: EXECUTED` + 追加 `E1_EXECUTED` 段；脚本自有字段未改，SSOT 保持）
- 本报告（E1 转正唯一新建叙事文件）
