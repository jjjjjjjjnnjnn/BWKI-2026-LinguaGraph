# BASELINE_LEDGER — 基线推导台账 (frozen 2026-09-12, v20)

> 每个基线四列：定义 → 代码 → 产物 → 复现命令。状态三态：**verified**（可引用）/ **needs_review**（ directional only，补实验后转正）/ **drop**（退役）。
> 精度政策：测量值报 **3 位小数 + CI**（第 4 位为计算对账位，提取误差 ΔLDS≈0.0014 已淹没第 4 位）。
> 容差政策：确定性重算 0.001（舍入级）/ 随机重采样 0.01（SE 级）/ 跨版本 0.02。
> 审计方法：蓝方举证 → 红方质询（9 组，7 致命）→ 蓝方作答（8 认罚）→ 红方复验 → 裁决人终审。红方复验 3 个"不通过"中 2 个为误伤（只搜 JSON 未查 CSV，已纠正），1 个成立（6.2 逻辑跳跃，已收窄）。

## §1 Structure Null（度保持重连）— needs_review
- 定义：`docs/lds_formal_definition.md:107-134`
- 代码：`scripts/figures/_lds_utils.py:77-102` + `fig4_null_model.py:55-69`
- 产物：`outputs/figures/fig4_null_model_data.csv:3` → 0.957/0.955/0.714
- 复现：`python scripts/figures/fig4_null_model.py`（产物 CSV）
- 缺口：无 CI、无 seed 清单 → 补多 seed 分布后转 verified。

## §2 Permutation 家族（必须分三类，不可混用）
### §2.1 Node-Permuted（组内顺序置换）— drop（退役）
- 代码只 `shuffle` 列表顺序，`set()` 后恒等，检验力恒为 0（蓝方实测 `set_equal=True`）。
- 从正表移除，保留本条作废记录。修复方向：真置换（边端点重配）后补实验。

### §2.2 Language-label permutation（教材图组级）— needs_review
- 代码：`fig4_null_model.py:196-239`（seed 硬编码 42+999=1041）
- 产物：`fig4_null_model_data.csv:7` → 0.841/0.870/0.670
- 复现：多 seed 实测 1041/2026/9999 → ±0.01~0.03，方向不翻转（红方"全局值无源"指控不成立：出处即 CSV 第 7 行）。
- 缺口：单 seed 点估计、无分布 → 补 ≥5 seed 均值±SD；函数 seed 参数化。

### §2.3 LDS-C label permutation（人类 N=15，p 值）— needs_review
- 代码：`scripts/lds_c_compute.py:333-379`（n_iter=200，被 cap 钳住，CLI 加 iterations 也救不了）
- 产物：`data/lds_c/lds_c_results_20260808.json:95-109` → p=0.08/1.0/1.0
- 缺口：p=0.08 的 SE=0.019，95%CI [0.042,0.118] 跨 0.05 线 → **不得做显著性解读**；补 ≥1000 置换 + perm/iterations 解耦。

## §3 Human N=15 floor — needs_review
- 代码：`lds_c_compute.py:297-330`（参与者分半）
- 产物（官方）：`data/lds_c/llm_subject/design_effect_20260810.json:30,41,52` → floor 0.959/0.924/0.922，margin 0.005/0.009/0.014
- 旧版 `lds_c_results_20260808.json:90-93`（0.958/0.923/0.922，n_iter 不同）退役 → 以 design_effect 为单源。
- 缺口：floor 无 CI → 补分半重复分布。

## §4 LDS-C 人机同幅 / floor 分离 — verified（全文最稳）
- 人类 0.963/0.932/0.936 vs LLM 0.955/0.930/0.945（幅度同）；floor 0.92-0.96 vs 0.875/0.846/0.862；margin 0.005-0.014 vs 0.081-0.084。
- 产物：`design_effect_20260810.json` + `outputs/figures/fig_a7_1_delta_lds.csv:2-4`。
- N=3 仍 margin+0.02-0.04，排除样本量解释。

## §5 Within-language floor 0.97（教材图分半）— needs_review
- 代码：`fig4_null_model.py:122-150`
- 产物：`fig4_null_model_data.csv:6` → 0.970/0.974/0.962（红方"LDS 域无源"不成立：出处即 CSV 第 6 行）。
- 缺口：单次分半无 CI；Mono Control 列为空（键映射 bug，`fig4:395-401`）→ 修 bug + 补 200× 分布。
- 与 §3 不可混用（参与者异质性 vs 图分半）。

## §6 Size-match k=15/25/35 — needs_review（方向成立，点值不成立）
- 代码：`scripts/p2_size_match.py`（rng 看似固定，实被 `PYTHONHASHSEED` + 集合序破坏；跨进程抖 ±0.002）
- 结论：wiki>math、gap 全负，方向成立；点值 exact reproducibility 不成立。
- 补实验：`PYTHONHASHSEED=0` + `sorted(nodes)` 后重冻，报均值±SD。

## §7 Wikipedia control — needs_review
- 对齐后：`data/lds_c/lds_k_deep/lds_k_deepen_20260808.json` → wiki 0.698/0.723/0.819 vs math 0.934/0.938/0.519（公式字段自标 frozen v3 二元）。
- 旧 1.0（`fig_wikipedia_lds_data.csv` 全 1.0）为 Latin-only 对齐伪影，作废；旧 CSV 无 git 历史，待移 `_archive/`。
- 缺口：96 条 gloss 系 deepseek-v4-flash 英文化，无人工抽检、无第二模型交叉 → 补盲抽 ≥30/96 + qwen-plus 交叉 gloss，否则不得作内容证据。

## §8 公式裁决（W1.3，终审）— 二元 verified / 三元收窄
- **(a) verified**：发表 LDS-K 由二元管线 `1-mean(J_node,J_edge)` 精确产生。
  复现：`python scripts/figures/reproduce_lds_binary.py`（冻结，log：`outputs/figures/reproduce_lds_binary.log`）
  `ZH-EN 0.9336→0.934 / DE-EN 0.9382→0.938 / ZH-DE 0.5188→0.519`（裁决人亲跑）。
- **(b) needs_review（观察句）**：三元 as-implemented（`src/scoring.py`，fallback ged_sim=0.5）在 219 节点超时（12 节点子图 180s 亦超时；仅 ≤6 节点玩具图可算），且 fallback 版不命中发表值（距 0.145/0.146/0.007）。
- **(c) 收窄**："三元家族都不对"表述 drop——三元家族欠定（GED_needed=0.065/0.062/0.481 按构造必中，同义反复），无 GED 规约则不可证伪。
- 对齐动作（v20）：paper §2.7 二元为准 + 本台账指针；`src/scoring.py` 加 VERDICT 注（行为不动，4 条管线在用）；Fig2 重画为二元流程；portal 公式卡改回二元。

## §9 Margin ≥0.10 — needs_review（悬置）
- 产物：`sw_fix_analyses_20260910.json` span 0.033-0.424，median 0.126，0.10 在 CI 外（自标启发式）。
- 依赖 §2.2/§5 缺失的 CI → CI 补齐前悬置，不可作审计阈值引用。

## §10 Fig4 / Fig8 frozen figure values（2026-09-12，可引用绘图快照）
- **Fig4**（`scripts/figures/fig4_null_model.py` → `outputs/figures/fig4_null_model_data.csv` + `fig4_null_model{,_de,_zh}.png`）：Full 基线 **0.9336 / 0.9382 / 0.5188**（ZH-EN / DE-EN / ZH-DE；快照 `outputs/figures/reproduce_lds_binary.log`，发表取整 0.934/0.938/0.519）；Structure Null 0.9571/0.9546/0.7142；Within-Lang floor 0.9695/0.9744/0.9615；Label-Permute 0.8407/0.8701/0.6704（seed 42+999=1041）。复现：`python scripts/figures/fig4_null_model.py`。
- **Fig8**（`scripts/figures/fig8_lds_decontamination.py` → `outputs/figures/fig8_lds_decontamination_data.csv` + `fig8_lds_decontamination{,_de,_zh}.png`，确定性快照、不重算）：Full 0.934/0.938/0.519 vs Structure Null 0.957/0.957/0.717 vs 去污染 T1 FilterA（167/219 CJK-de 标签剔除、52 保留）0.985/0.985/0.990；ZH-DE 箭头 +0.47（T1 falsifiziert）。复现：`python scripts/figures/fig8_lds_decontamination.py`。

## 补实验优先级
- P0：§2.2 多 seed 分布、§5 floor/perm 200× 分布 + CI、§2.3 n_iter≥1000 重算。
- P1：§7 gloss 抽检 + 交叉、§6 排序冻结重跑、Mono bug 修复。
- P2：GED 近似路线或正式弃 GED 冻结、旧 1.0 CSV 归档。
