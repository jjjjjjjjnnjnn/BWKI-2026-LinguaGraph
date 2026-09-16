# Baseline Board — 可引用基线看板 (T3, 2026-09-14)

> 来源冻结：`docs/BASELINE_LEDGER.md` v20 (frozen 2026-09-12, §1/2.2/5/6 verified 2026-09-14) + `outputs/figures/fig4_null_model_data.csv` (12 行) + `docs/p2_methodology_rechecks.md` + `research/gold_deconfound_2026-09-14.md/.json`
> 精度政策：3 位小数 + CI（第 4 位对账位）；容差：确定性 0.001 / 随机重采样 0.01 / 跨版本 0.02。
> 状态三态：**verified**=可引用 / **needs_review**=directional only / **drop**=退役。§2.1 Node-Permuted 已 drop，不进正表。

## A. Verified 值表 (§1 / §2.2 / §4 / §5 / §6)

列顺序统一：ZH-EN / DE-EN / ZH-DE。5-seed 均为 seeds `42,999,2026,7,1234`，`$env:PYTHONHASHSEED=0`。

| Ledger § | 条件 | 单 seed 点值 | 5-seed mean±SD | 状态 / 出处 |
|---|---|---|---|---|
| §1 | Structure Null（度保持重连） | 0.9571 / 0.9568 / 0.7154 (CSV:3) | **0.9562±0.0010 / 0.9555±0.0024 / 0.7170±0.0013** (CSV:9) | verified (B1/B2)。代码 `scripts/figures/_lds_utils.py:77-102` + `fig4_null_model.py:63-89` (`sorted(key=repr)` 冻结)。旧值 0.9571/0.9546/0.7142，漂移 +0.0022/+0.0012 < 0.01 容差，方向不变 (full−null 为负: converge) |
| §2.2 | Language-label permutation（教材图组级） | 0.8407 / 0.8701 / 0.6704 (CSV:7，与旧值比特一致) | **0.8561±0.0059 / 0.8572±0.0140 / 0.6737±0.0069** (CSV:10) | verified (B1/B2)。代码 `fig4_null_model.py:221-264` (legacy 单 seed 行 seed=1041=42+999) |
| §4 | LDS-C 人机同幅 / floor 分离（全文最稳） | 人类 0.963/0.932/0.936 vs LLM 0.955/0.930/0.945；floor 0.92–0.96 vs 0.875/0.846/0.862；margin 0.005–0.014 vs 0.081–0.084 | N/A（确定性快照，无 multiseed；N=3 仍 margin +0.02–0.04，排除样本量解释） | verified。产物 `data/lds_c/llm_subject/design_effect_20260810.json` + `outputs/figures/fig_a7_1_delta_lds.csv:2-4` |
| §5 | Within-language floor 0.97（教材图分半） | 0.9695 / 0.9744 / 0.9615 (CSV:6，哈希稳定，边交集恒 0) | **0.9700±0.0061 / 0.9692±0.0055 / 0.9682±0.0085** (CSV:11；列映射 ZH-EN←ZH / DE-EN←DE / ZH-DE←EN)；Mono Control 单 seed 0.9695/0.9615/0.9744 (CSV:8)，5-seed 0.9700/0.9682/0.9692 ±0.0061/0.0085/0.0055 (CSV:12，B5 键修 `ZH-ZH/EN-EN/DE-DE`，与 within 同构同源) | verified (B5)。代码 `fig4_null_model.py:142-174` + 外循环 `--seeds` (403-440)。与 §3 不可混用（图分半 vs 参与者异质性） |
| §6 | Size-match k=15/25/35（方向 + 冻结值） | 全尺寸参照 ZH-DE LDS math 0.519 vs wiki 0.819 (J_node 0.556 vs 0.200；旧 0.444 系 node-only ablation `figures_i18n_wave2.py:372`，旧 0.800 系过期 wiki 口径，均退役) | k=15: math **0.030±0.029** vs wiki **0.053±0.037**, gap **−0.023**；k=25: **0.048±0.032** vs **0.101±0.037**, gap **−0.053**；k=35: **0.069±0.030** vs **0.149±0.030**, gap **−0.080** (`n_iter=200, seed=20260810`，双进程比特一致) | verified (B6)。代码 `scripts/p2_size_match.py` (:28-38 PYTHONHASHSEED 守卫 + :55 `sorted(key=repr)` + :63-89 均值±SD)。结论 wiki>math、gap 全负。复现 `$env:PYTHONHASHSEED=0; python scripts/p2_size_match.py` (k=45/60/100 因 wiki≤47 节点跳过) |

方法学去 confound 背书 (`docs/p2_methodology_rechecks.md`)：
- P2-1：§6 wiki>math 与 size-match 反转一致；数学全尺寸 0.556 含 `labels["de"]` 110 中文伪影 + 对齐循环性 + 采样近全宇宙伪影，原"0.444 vs 0.800 制度趋同/文化分歧"已诚实降级，不作内容证据。
- P2-2 (H2)：q≈0.8 实际稀疏度余量 +0.05–0.06 未坍缩，仅 q=0.30 过度稀疏单点 +0.014 拟合人类 +0.015 → "一致性演示"非因果证明。
- P2-3 (H3)：qwen-plus 交叉提取保留 ZH-DE 76% / DE-EN 79%，ZH-EN 仅 23% (+0.041→+0.010) → ZH-DE 核心稳健，ZH-EN 幅度慎读。

## B. Blocked 清单 (§2.3 / §3 / §7 / §9) — needs_review，不可作审计阈值引用

统一转正门：**置换 n≥1000**（SE 门）/ **gloss 盲抽 ≥30/96 + 第二模型交叉** / **盲审门 F1≥0.85 ∧ Agr≥0.8 ∧ 每语≥0.7**（三者合取，任一不满足即 blocked）。

| Ledger § | 当前冻结值（仅 directional） | Blocked 原因 | 转正条件 |
|---|---|---|---|
| §2.3 LDS-C label permutation (N=15, p) | `data/lds_c/lds_c_results_20260808.json:95-109` → p=0.08/1.0/1.0；p=0.08 在 n=200 时 SE≈0.019，95%CI [0.042,0.118] 跨 0.05 线 → 不得显著性解读 | **n≥1000 未跑**：代码就绪 (`lds_c_compute.py:355-401` 默认 200→1000 + `build_report:419-481` 解耦 `floor_iter/perm_iter` + CLI)，但全量重跑贵 + 写盘涉 `data/lds_c/` 禁区，B 组仅 `--help`/签名冒烟 + 37 单测绿。注意默认漂移：旧 p 仅显式 `n_iter=200` 复现 | 跑 `python scripts/lds_c_compute.py --perm-iters 1000 --floor-iters 200` (p=0.08 在 n=1000 时 SE≈0.0086) 并更新产物 JSON |
| §3 Human N=15 floor | 官方 `data/lds_c/llm_subject/design_effect_20260810.json:30,41,52` → floor 0.959/0.924/0.922, margin 0.005/0.009/0.014 (旧 `lds_c_results_20260808.json:90-93` 0.958/0.923/0.922 退役，单源 design_effect) | **分布重算 blocked**：代码就绪 (`lds_c_compute.py:297-353` 默认 100→200 + `return_stats=True` 报 mean/std/n，调用方兼容已验)，但写盘涉 `data/lds_c/llm_subject/` 禁区 + bootstrap 贵，仅单函数冒烟 + `test_lds_c_deepen` 37/37 | A 组或解禁后跑 `signal_table(..., n_floor=200)` 取 `return_stats` std 报 CI |
| §7 Wikipedia control | 对齐后 `data/lds_c/lds_k_deep/lds_k_deepen_20260808.json` → wiki 0.698/0.723/0.819 vs math 0.934/0.938/0.519 (旧 `fig_wikipedia_lds_data.csv` 全 1.0 系 Latin-only 伪影作废，待移 `_archive/`) | **30 抽检 + 交叉未完成**：96 条 gloss 系 deepseek-v4-flash 英文化，无人工抽检、无第二模型交叉。模板 `research/wiki_gloss_audit_30.json` (seed 20260914, n=30/96, G001–G030 `accept/notes` 空白，`qwen_cross_gloss` PENDING：BAILIAN_API_KEY 未设，未伪造) → **盲审门 F1≥0.85∧Agr≥0.8∧每语≥0.7 未验**，不得作内容证据 | 补盲抽 ≥30/96 人审 + qwen-plus 交叉 gloss，三门全过才转正 |
| §9 Margin ≥0.10 | `sw_fix_analyses_20260910.json` span 0.033–0.424, median 0.126, 0.10 在 CI 外（自标启发式） | **悬置**：依赖 §2.2/§5 缺失的 CI（现 §2.2/§5 CI 已补，但 §9 未重算联动）+ gold 盲审门未过 | CI 补齐联动重算前悬置，不可作审计阈值引用 |

Gold 去 confound (`research/gold_deconfound_2026-09-14.md/.json`, n=92: math annotator_1 n=20 + social auto_accepted n=72)：
- 独立 harness F1：qwen-plus math 0.7244 / social 0.6497；qwen-max math 0.7068 / social 0.6483；overall macro 0.665927→0.6659 与 summary 一致 (PASS)。
- 排名 qwen-plus>qwen-max 同号保持 (math +0.0176 / social +0.0014，n=2 不做 Spearman)。
- **0.939 系 DB-path + seed 共源特值，不可引用为 harness F1**；harness social ~0.65 **未过盲审门 F1≥0.85** → 模型选择只保排名、绝对值降级。

## C. Fig4 快照引用（可引用绘图快照）

- 数据：`outputs/figures/fig4_null_model_data.csv` (Full 基线 :2 → **0.9336/0.9382/0.5188**，发表取整 0.934/0.938/0.519；各 null 行见 A 表 :3/:6/:7/:8 + multiseed :9/:10/:11/:12)。
- 图：`outputs/figures/fig4_null_model{,_de,_zh}.png`。
- 复现：`$env:PYTHONHASHSEED=0; python scripts/figures/fig4_null_model.py [--seeds "42,999,2026,7,1234"]`。
- 一致性：Fig8 (`scripts/figures/fig8_lds_decontamination.py` → `fig8_lds_decontamination_data.csv`) struct 列为 09-12 冻结快照 (0.957/0.957/0.717)，与当前 point 差 ≤0.003 (ZH-DE 0.717 vs 0.7154)；去污染 T1 FilterA (167/219 CJK-de 剔除) 0.985/0.985/0.990、ZH-DE 箭头 +0.47 结论只依赖 full vs 去污染，不受影响。档案 JSON 内旧 0.9546 等冻结前值为档案，不得引用，以本看板 A 表为准。
