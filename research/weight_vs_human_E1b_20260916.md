# E1b 执行报告：group-id 节点身份 kNN 图 J_edge-only(gid)（2026-09-16，A线）

> **状态：E1b 测量 EXECUTED；口径 Hypothesis/PENDING；解释 Hypothesis/PENDING。**本文件所有新统计均为 **exploratory appendix-only**，不得进入主结论。
> **红线核验**：只读 `data/` 既有（含 `data/lds_c`）与既有向量文件；未改 `tests/`、`freeze/`、`_deploy/`、`linguaGraph.db`、`data/`；未改 `scripts/tools/weight_graph_audit.py` 及其输出 `research/weight_graph_audit_20260916.json`；新增概念 **0**；未扩语料；未改 LDS v3 公式（冻结公式 `1-(J_node+J_edge)/2`，`docs/lds_formal_definition.md §8.1` 逐字复用，与 audit 脚本同一实现）。
> EN 上限 / ZH-DE 采信规则（沿用 E1 §红蓝）：涉 EN 断言停在分布级；zh-de（主对 n=65）永不单独承载结论，三语对并列。人类 pilot N=8：禁一切显著/通过/报警断言。
> **输入 hash 声明（A7）**：本报告输入（`aligned_data.json` 219 行、`weight_vectors_934x768_20260916.term2vec.json` 934×768）**无 hash 落盘**，字节一致性未验证；复现仅靠行数/行序人工对账。
> **指标改称声明（A1）**：本文件旧称 `LDS-VEC(gid)` 全面改称为 **`J_edge-only(gid)`**。因三语 gid 集完全相同（J_node=1.0 系构造），冻结公式退化为 **`J_edge-only(gid)=(1-J_edge)/2`**，纯系边重合度的单调变换；**值域 [0,0.5] 不对称**，与 LDS-K 跨量纲、禁一切数值互证（正反两方向皆禁）。该指标为本次新造、未经独立验证，**嫌疑声明**：不得视为 LDS 验证，不得进主结论；rank 对照仅为方法笔记，**E3-full 前禁用**。

## §1 E1b 方法（冻结）

- 输入（只读，无 hash）：`research/weight_vectors_934x768_20260916.term2vec.json`（934×768，`text-embedding-nomic-embed-text-v1.5`）+ `data/math_extractions/merged/aligned_data.json`（219 行）。
- 执行：`python scripts/tools/weight_graph_E1b.py`（新文件，原 audit 脚本未动）→ `research/weight_graph_E1b_20260916.json`（机器输出）。
- 翻译层 term→gid，四规则：
  - R-intra：同一对齐组的三语标签视为**同一节点**（gid）。
  - R-gid：同 gid 多行折叠到文件序**首行**（18 处 id 碰撞全部记录；16 处标签完全相同亦取首行——**取首行即选择偏倚**，2 处单标签变体见 §3：`math_calculus_洛必达法则` de 槽变体、`math_calculus_散度` en 槽变体；**无末行重算前，禁一切“无损/干净”措辞**）。
  - R-cross：跨**不同** gid 的相同表面标签映射到文件序首个 gid 并记录；节点**不合并**（若按表面相等合并节点，节点存活将重新依赖表面相等，J_node 去污失效）。
  - R-loop：自环（gid==gid）剔除并计数（唯一 gid 键下构造性为 0；E1 行空间基线自环同步重算以供对照）。
- 图：逐语对称 kNN（k=5/10/15，余弦距离，ties 按文件序稳定排序，与 E1 稳定排序同规则）；节点集为 gid 集，边集按 **gid 对**比较；重算 **`J_edge-only(gid)`**（冻结公式在 J_node=1.0 下的退化，新指标嫌疑，未验证）。
- 方法可信锚限域（A7）：同一 numpy kNN 以行空间（含重复）**逐值复现**冻结 E1 字符串空间三 k 值（`e1_reproduction_check=true`）——该复现**仅行空间旧路径冒烟，gid 新路径无独立验证**；gid 测量与 E1 仅共享 kNN 代码路径，不共享验证结论。

## §2 E1b 结果（只记数值，序不可解释）

| k | zh-de J_edge-only(gid) | zh-en J_edge-only(gid) | de-en J_edge-only(gid) | 序（升序，仅记录，禁解释） |
|---|---|---|---|---|
| 5 | 0.2932（J_node=1.0，J_edge=0.4137） | 0.4401（1.0 / 0.1197） | 0.4356（1.0 / 0.1287） | zh-de < de-en < zh-en |
| 10 | 0.2941（1.0 / 0.4118） | 0.4423（1.0 / 0.1153） | 0.4406（1.0 / 0.1188） | zh-de < de-en < zh-en |
| 15 | 0.2956（1.0 / 0.4087） | 0.4409（1.0 / 0.1182） | 0.4383（1.0 / 0.1234） | zh-de < de-en < zh-en |

- 冻结 LDS-K 序（升序，仅作方法笔记对照，E3-full 前禁用）：zh-de（0.519）< zh-en（0.934）< de-en（0.938）。
- **Rank 对照（方法笔记，E3-full 前禁用，待复核）**：三 k 下 J_edge-only(gid) 序均为 zh-de < de-en < zh-en；Spearman **ρ=0.5**（n=3，描述性；精确双侧置换 p=**1.0**）。**n=3 无判别力，序不可解释**；k-一致性（三 k 同序）不充数，不记任何方向性叙事。
- zh-de 最小数值的记录（描述性，待 E3-full 复核）：zh-de 在 gid 空间三 k 取最小；EN 对间隙 gid 空间仅 0.0017–0.0045，**禁止任何 EN 序差断言**（T-P5-3 类比：数值接近≠可排序）。本条不记支持、不记印证，仅待复核记录。
- k-平坦记录（描述性，待 E3-full 复核）：gid 值随 k 变化小（zh-de 0.2932→0.2956；EN 对 ±0.003），E1 字符串空间 zh-de 随 k 变化（0.5245→0.5457）并列记录。本条不记因果、不记来源归因，k-敏感性记账待 E3-full。
- **禁比数值声明**：不许说“向量验证/证实了 LDS-K 数值”，亦不许说“0.29/0.44 证伪了 0.519/0.93”。J_node=1.0 系构造使然（同 199 gid 集），J_edge-only(gid)=(1−J_edge)/2 值域 [0,0.5] 不对称，纯系边重合度的单调变换，与 LDS-K 跨量纲、禁一切数值互证句（正反两方向皆禁）。新指标嫌疑声明见文件头。

## §3 口径复核（217→219 未定 + 去重/自环，Hypothesis/PENDING）

- 行普查：对齐表 **219 行 = 201 唯一 gid + 18 同 gid 重复行**。18 处 id 碰撞取首行即选择偏倚，如实记录；其中 2 处单标签变体点名（取首行，未做末行重算敏感性分析）：
  - `math_calculus_洛必达法则`（行12/39）：de 首行 `Regel von L'Hospital`，重复行 `洛必达法则`（取首行）；
  - `math_calculus_散度`（行21/61）：en 首行 `Divergence`，重复行 `Divergence (vector)`（取首行）。
  - 其余 16 处三标签完全相同，同样取首行，选择偏倚同样未排除；**禁一切“无损/干净”措辞**。
- 缺失 2 组（MNAR，非随机缺失；行级与 gid 级一致，缺失率 gid 口径 2/201=1.0%）：`math_linear_algebra_基`（三语标签皆 `基`）、`math_linear_algebra_维数`（三语皆 `维数`）。原因：两标签既不在 700 去重抽取概念名中，又因三语表面全同、所属全部 6 个主对被表面相同规则剔除，从未进入 434 主对增补集，故 934 词表无其向量——属输入口径后果，非本层可修复（零新文本口径下禁补；缺失机制记 MNAR）。
- 向量覆盖：每语 217 行有向量；折叠后每语 **199 唯一 gid**有向量，三语 gid 集完全相同 → J_node=1.0 系构造（非测量）。
- 口径声明：E1 的“217/语”重复计算了 18 个同 gid 行；本口径为 **199/201 有偏口径**（MNAR 缺失 2/201 + 首行选择偏倚 18 处未做末行重算）。E1 影响待评估；禁称 E1 定量结论层面的影响判断。
- 跨 gid 同标签映射（gid 折叠后，逐语）：zh 4 键/4 余份、en 7 键/7 余份、de 7 键/7 余份，共 18 条记录（`cross_gid_duplicates`）；映射 term→首 gid 已落盘，节点未合并（理由见 R-cross）。**`term_first_gid` 字段未引用声明**：本次测量实际使用 `first_gid` 映射落盘；名为 `term_first_gid` 的字段（如存在）未被引用、无验证，特此声明。
- 去污状态声明（A5）：**J_node 去污、J_edge 仍污染**。J_node=1.0 系构造去污（同 gid 集）；J_edge 仍污染，机制点名：(1) de 槽 CJK 残留——de cross_gid 重复中 `三角形/体积/圆/面积/长方形/原函数/线性方程组` 等以 CJK 表面存于 de 槽，跨 gid 首-gid 映射改变近邻；(2) 孪生对机制——18 重复行折叠 + 跨 gid 同标签首-gid 映射 + E1 行空间自环/零距离近邻结构，均可渗入边集。故禁一切“剥离/去污染/干净”措辞。
- 自环：E1 行空间基线自环 k=5 时 zh 16 / en 22 / de 20（zh 16 与 E1 报告 16/709 数值同，来源为同一旧路径重算，非独立验证），k=10/15 时 zh 21 / en 23–24 / de 23；**E1b gid 空间三 k 三语自环均为 0**（构造性为 0，非测量成功）。

## §4 稀疏度（E3 上下文：仍 MISMATCH）

- 人类教材图基线：556 节点 / 238 边 / 密度 0.001543。
- gid kNN（199 节点/语）：k=5 边 719–768（密度 0.036–0.039）、k=10 边 1370–1512（0.070–0.077）、k=15 边 2009–2249（0.102–0.114），仍为人类图的 **24–74 倍**：跨密度 Jaccard 混杂持续，E3 匹配对照仍缺（subsample 至 238 边重算 = E3-full，不在本文件范围，维持 PENDING）。

## §5 阶段门禁自评（测量 EXECUTED、口径与解释均 Hypothesis/PENDING）

| 项 | 裁决 | 说明 |
|---|---|---|
| E1b 测量 | **EXECUTED** | gid 重算三 k + rank 方法笔记 + numpy 行空间旧路径复现逐值通过，公式冻结；输入无 hash |
| R5 节点口径 | **Hypothesis/PENDING** | 行→gid 审计已记账：id 碰撞 18 处首行选择偏倚未排除、MNAR 缺失 2/201、跨 gid 映射 18 条、自环 gid 空间构造性 0；待末行重算 + E3-full |
| E1b 解释 | **Hypothesis/PENDING（维持）** | n=3 无判别力（p=1.0，序不可解释）+ 稀疏失配持续 + zh-de n=65 降权三重封顶；rank 对照与 k-平坦均待 E3-full 复核 |
| 升 Developing | **否** | 唯一升级路径 E3-full（238 边稀疏匹配重算 + k 敏感性记账）未执行；E1b 只覆盖 group-id 身份，不解决密度失配 |
| E2 / 分支1/2 | **PENDING（不变）** | 无冻结数学频次表 / 无语义去污判官 |

- 对 R1 的回应（Hypothesis 级方法笔记，不入结论，待 E3-full 复核）：E1 的 ρ=1.0 与本文件 ρ=0.5（p=1.0）均在 n=3 无判别力下，序不可解释；不记方向性叙事。
- 对 R5 的回应（Hypothesis/PENDING）：本报告为 E1b 记账交付；217≠219 与自环已记账为 199/201 有偏口径 + 行空间自环数并列 + gid 空间构造性 0；口径与解释均未升级，待末行重算与 E3-full。

## §6 输出清单

- `research/weight_graph_E1b_20260916.json`（机器输出：翻译层/三 k gid 值/rank 方法笔记/稀疏/门禁自评，`exploratory_appendix_only=true`）
- 本报告（E1b 唯一新建叙事文件）
- `scripts/tools/weight_graph_E1b.py`（新脚本；原 audit 脚本与 `research/weight_graph_audit_20260916.json` 未动）

## §7 fix_rev（2026-09-16 红队 A1–A8 定稿修复记账，不改数值）

- A1：旧指标名全文件改称 `J_edge-only(gid)`；声明退化式 `(1-J_edge)/2`、值域 [0,0.5] 不对称、新指标嫌疑；rank 对照降为方法笔记、E3-full 前禁用。9 格值与 J_edge 值不动。
- A2：删方向性叙事；只留 n=3 无判别力、p=1.0、序不可解释；k-一致性不充数。
- A3：18 重复取首行记选择偏倚，点名洛必达 / 散度两变体；无末行重算前禁“无损/干净”类措辞。
- A4：缺 2 组记 MNAR，缺失率 2/201；改称 199/201 有偏口径；删 E1 影响判断与干净口径类措辞。
- A5：J_node 去污、J_edge 仍污染；点名 de 槽 CJK 残留 + 孪生对机制；`term_first_gid` 未引用如实声明。
- A6：rank 对照与 k-平坦移入待 E3-full 复核；删印证类叙事。
- A7：复现锚限域为行空间旧路径冒烟、gid 新路径无独立验证；输入无 hash 声明。
- A8：门禁为测量 EXECUTED、口径与解释均 Hypothesis/PENDING；删升级类措辞。
