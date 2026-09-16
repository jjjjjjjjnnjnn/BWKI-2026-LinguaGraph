# Table 2：学科 × 学段对照表（nodes / links / density / CDS / HDS）

> 来源冻结口径（T2）：`manifest.json` / `outputs/physics_comparison.json` /
> `outputs/chemistry_comparison.json` / `config/expert_graphs/physics_full.json` /
> `config/expert_graphs/chemistry_full.json`（level 分布实计数）/
> `docs/paper/06_physics_results.md`（§6 全节，frozen 引用值）。
> 本文件为唯一新增文件，不改其它文件。

## 1. 学科 × 学段主表（full-graph 口径）

`density = CDS = 2E / (N·(N−1))`（无向密度；已用 outputs 值验算一致）。
`links` 即各 comparison JSON 中该学段 `edges`；`nodes` 即该学段 `nodes`。

| 学科 | 学段 | nodes | links (edges) | density (= CDS) | 来源 |
|------|------|------:|--------------:|:---------------:|------|
| 数学 Math（全图 556） | elementary（小学） | 26 | 2 | 0.0062 | `outputs/physics_comparison.json: math.cds.elementary`（`chemistry_comparison.json` 同值） |
| 数学 Math | middle（初中） | 57 | 6 | 0.0038 | 同上 `math.cds.middle` |
| 数学 Math | high（高中） | 200 | 49 | 0.0025 | 同上 `math.cds.high` |
| 数学 Math | college（大学） | 273 | 105 | 0.0028 | 同上 `math.cds.college` |
| 数学 Math | **合计** | **556** | **238（relations；另见 manifest total_links 238）** | **全图 density 0.001543** | `manifest.json: graph` + comparison JSON `math.concepts/relations` |
| 物理 Physics（全图 367） | elementary（小学） | 10 | 10 | 0.2222 | `outputs/physics_comparison.json: physics.cds.elementary`；`physics_full.json` 实计数 `elementary=10` 一致 |
| 物理 Physics | middle（初中） | 93 | 89 | 0.0208 | 同上 `physics.cds.middle`；`physics_full.json` 实计数 `middle=93` 一致 |
| 物理 Physics | high（高中） | 137 | 117 | 0.0126 | 同上 `physics.cds.high`；`physics_full.json` 实计数 `high=137` 一致 |
| 物理 Physics | college（大学） | 127 | 86 | 0.0107 | 同上 `physics.cds.college`；`physics_full.json` 实计数 `college=127` 一致 |
| 物理 Physics | **合计** | **367** | **386（relations；302? 不，386）** | **全图 density 0.00575（=2·386/(367·366)）** | `physics_comparison.json: physics.concepts/relations`；`physics_full.json: len(concepts)=367, len(relations)=386` |
| 化学 Chemistry（全图 220） | elementary（小学） | 0 | 0 | 0.0 | `outputs/chemistry_comparison.json: chemistry.cds.elementary`；`chemistry_full.json` 实计数无 `elementary`（见口径注 4） |
| 化学 Chemistry | middle（初中） | 46 | 43 | 0.0415 | 同上 `chemistry.cds.middle`；`chemistry_full.json` 实计数 `middle=46` 一致 |
| 化学 Chemistry | high（高中） | 51 | 38 | 0.0298 | 同上 `chemistry.cds.high`；`chemistry_full.json` 实计数 `high=51` 一致 |
| 化学 Chemistry | college（大学） | 123 | 94 | 0.0125 | 同上 `chemistry.cds.college`；`chemistry_full.json` 实计数 `college=123` 一致 |
| 化学 Chemistry | **合计** | **220** | **215** | **全图 density 0.00893（=2·215/(220·219)）** | `chemistry_comparison.json: chemistry.concepts/relations`；`chemistry_full.json: len=220/215` |

level 分布实计数复核（`config/expert_graphs/`）：

- `physics_full.json`：`Counter({'high': 137, 'college': 127, 'middle': 93, 'elementary': 10})`，合计 367；`len(relations)=386`。
- `chemistry_full.json`：`Counter({'college': 123, 'high': 51, 'middle': 46})`，合计 220，无 `elementary`；`len(relations)=215`。

## 2. HDS 总表（max / mean / roots）

| 学科 | HDS max（最大深度） | HDS mean（平均深度） | roots（根概念数） | 口径说明 |
|------|:-----------------:|:-----------------:|:----------------:|----------|
| 数学 Math | **8（frozen，论文引用值）**；outputs 重算值为 3（不可用，见注 2） | **0.40（frozen）**；outputs 重算值 0.1691（不可用） | **459（83%，frozen）**；outputs 重算值 489（不可用） | frozen 值取 `06_physics_results.md §6.2`（`Max 8 / Mean 0.40 / Roots 459`）及 `§6.7` 复述；重算值出自 `outputs/*_comparison.json: math.hds` |
| 物理 Physics | 6（frozen 与 outputs 一致） | 0.85（frozen；outputs 精确值 0.8365） | **219（60%，frozen）vs 233（outputs，差异见注 3）** | frozen 取 `§6.2` / `§6.7`；outputs 取 `physics_comparison.json: physics.hds {max_depth 6, mean_depth 0.8365, root_count 233}` |
| 化学 Chemistry | 3（frozen 与 outputs 一致） | 0.20（frozen；outputs 精确值 0.2045） | 184（84%，frozen 与 outputs 一致） | frozen 取 `§6.7`；outputs 取 `chemistry_comparison.json: chemistry.hds {3, 0.2045, 184}` |

论文 CDS 对照（frozen，`§6.1` / `§6.7`，保留原文逗号小数写法溯源）：

- `§6.1` Physics CDS：Grundschule **0,222** / Mittelstufe 0,029 / Oberstufe 0,013 / Hochschule 0,011；Mathe CDS：0,216 / 0,271 / 0,073 / 0,042。
- `§6.7` Chemie CDS：Mittelstufe **0,042** / Oberstufe 0,030 / Hochschule 0,013（无 Grundschule 行）。
- 注意：`§6.1` 物理 Mittel 0,029 与 outputs 精确值 0.0208 存在舍入外差异；数学四档 CDS（0,216 / 0,271 / 0,073 / 0,042）与 outputs 数学 CDS（0.0062 / 0.0038 / 0.0025 / 0.0028）为不同口径（219 对齐子图 vs 556 全图，见注 1），**不可直接比较**，本主表采用 outputs 全图口径。

## 3. 口径注（必读，6 条）

1. **219 vs 556 不可混用。** `manifest.json: alignment {aligned_groups 219, trilingual_groups 219, level_distribution {college 118, high 79, elementary 11, middle 11}}` 是**三语对齐子集口径**（219 组）；`manifest.json: graph {total_nodes 556, total_links 238, graph_density 0.001543}` 与本表主表（数学 26/57/200/273 = 556；物理 10/93/137/127 = 367；化学 0/46/51/123 = 220）是**全图口径**。`§6.6` 数据存量表（Mathe 556/525、Physik 367/386、Chemie 220/215，其中数学 relations 525 为对齐关系总数，非 graph links 238）亦不可与主表 `links` 列混用。任何 219 口径的分布（118/79/11/11）不得与 556 口径的 nodes/CDS/HDS 混算比例或均值。

2. **数学 max 8 frozen，不可重算。** 论文 `§6.2` / `§6.7` 冻结值 `Math HDS max 8 / mean 0.40 / roots 459 (83%)` 为引用权威值。`outputs/physics_comparison.json` 与 `outputs/chemistry_comparison.json` 中的 `math.hds {max_depth 3, mean_depth 0.1691, root_count 489}` 是另一管线口径的重算结果，**不得覆盖 frozen 值，不得在本表中使用，不得另行重算**。本表 HDS 总表数学行以 frozen 值为准，重算值仅列出以示排除。

3. **物理 roots 219 vs 233 差异注。** 论文 frozen 值 `§6.2` / `§6.7`：`Physik Wurzelkonzepte 219 (60%)`；outputs 值 `physics_comparison.json: physics.hds.root_count 233`。差 +14 来自版本漂移与口径差：`physics_full.json` 头部 `baseline {concepts 366, relations 383}` vs 当前 `len(concepts) 367 / len(relations) 386`（+1/+3），`metadata {total_concepts 366, total_relations 383}` 仍为旧基线快照。引用论文时用 **219**，追溯 outputs 计算时用 **233**，两者不可混为一数；max（6）与 mean（0.85 ≈ 0.8365）不受此差异影响。

4. **化学 elem 0 说明。** `chemistry_full.json` 实计数无 `elementary` level（仅 middle/high/college），`chemistry_comparison.json: chemistry.cds.elementary {nodes 0, edges 0, cds 0.0}`。论文 `§6.7` 明确“Der Chemie-Korpus enthält keine Grundstufen-Konzepte … daher entfällt die Grundstufen-Zeile”。0 不是缺失数据，而是语料设计（受查教材中化学自初中起始）；作图/建模时应**删去小学行**而非补 0 参与拟合。

5. **Demtröder 目录引用污染警告。** `physics_full.json` 实测：college 127 个概念**全部**含 `Demtröder` textbook 引用（`college: 127` 全中；全库含 Demtröder 引用的 ref 条数 381）。即大学段 grounding 计数被单一目录型教科书（Demtröder Experimentalphysik 系列）系统性垫高。**不得用 `total_refs / source_references` 条数论证大学段覆盖质量或层次深度**；引用数与概念数/边数/CDS/HDS 无关，需做去混杂（deconfound）后另议。本表所有密度与 HDS 均不受引用数影响。

6. **PEP 镜像限定。** 三语覆盖均为**镜像抽样**而非普查：ZH 侧以人教版（PEP：人教版小学科学/初中化学等）为镜像主干（物理 ZH 33 / 化学 ZH 33，`publisher_counts` 见各 `*_full.json` 头部；物理 EN 34 / DE 27，化学 EN 32 / DE 24），EN 侧为 Khan/CK-12/AP/IB/Halliday/Serway/Griffiths 等镜像，DE 侧为 Duden/Cornelsen/Klett/Dorn-Bader/Demtröder 等镜像（书目见 `§6.3`）。跨学科、跨学段比较仅在“镜像对镜像”意义下成立，不得外推为中/英/德全国教材普查结论；`§6.6` 注“NRW、中国课程图在本文范围外”同样适用。
