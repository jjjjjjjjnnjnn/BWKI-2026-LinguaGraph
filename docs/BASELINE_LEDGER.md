# BASELINE_LEDGER — 基线推导台账 (frozen 2026-09-12, v20)

> 每个基线四列：定义 → 代码 → 产物 → 复现命令。状态三态：**verified**（可引用）/ **needs_review**（ directional only，补实验后转正）/ **drop**（退役）。
> 精度政策：测量值报 **3 位小数 + CI**（第 4 位为计算对账位，提取误差 ΔLDS≈0.0014 已淹没第 4 位）。
> 容差政策：确定性重算 0.001（舍入级）/ 随机重采样 0.01（SE 级）/ 跨版本 0.02。
> 审计方法：蓝方举证 → 红方质询（9 组，7 致命）→ 蓝方作答（8 认罚）→ 红方复验 → 裁决人终审。红方复验 3 个"不通过"中 2 个为误伤（只搜 JSON 未查 CSV，已纠正），1 个成立（6.2 逻辑跳跃，已收窄）。

## §1 Structure Null（度保持重连）— verified（2026-09-14，B1/B2）
- 定义：`docs/lds_formal_definition.md:107-134`
- 代码：`scripts/figures/_lds_utils.py:77-102` + `fig4_null_model.py:63-89`（seed 参数化 + `sorted(...,key=repr)` 冻结；`_lds_utils` 本体未动，重连仍经 `RANDOM_SEED` 覆盖逐 seed 生效，见 45-51/403-440）
- 产物：`outputs/figures/fig4_null_model_data.csv:3` 单 seed 点值 → **0.9571/0.9568/0.7154**；`:9` 5-seed 均值±SD → **0.9562±0.0010 / 0.9555±0.0024 / 0.7170±0.0013**（seeds 42,999,2026,7,1234）
- 复现：`$env:PYTHONHASHSEED=0; python scripts/figures/fig4_null_model.py [--seeds "42,999,2026,7,1234"]`
- 新旧差异（诚实记录）：旧 CSV 点值 0.9571/0.9546/0.7142；新值 DE-EN +0.0022、ZH-DE +0.0012。原因：旧值带 `list(set)` 哈希序污染（同 seed=42 在 PYTHONHASHSEED=1/2 下得 0.7177 vs 0.7166），`sorted` 冻结后哈希稳定（1/2/0 三进程比特一致）；残差 < 随机重采样容差 0.01，方向结论不变（full−null 仍为负：converge）。
- 缺口关闭：有 5-seed 分布 + seed 清单（CSV notes 列）。

## §2 Permutation 家族（必须分三类，不可混用）
### §2.1 Node-Permuted（组内顺序置换）— drop（退役）
- 代码只 `shuffle` 列表顺序，`set()` 后恒等，检验力恒为 0（蓝方实测 `set_equal=True`）。
- 从正表移除，保留本条作废记录。修复方向：真置换（边端点重配）后补实验。

### §2.2 Language-label permutation（教材图组级）— verified（2026-09-14，B1/B2）
- 代码：`fig4_null_model.py:221-264`（seed 参数化，默认 42；legacy 单 seed 行仍用 1041=42+999）
- 产物：`fig4_null_model_data.csv:7` 单 seed → 0.8407/0.8701/0.6704（与旧值比特一致，未漂移）；`:10` 5-seed 均值±SD → **0.8561±0.0059 / 0.8572±0.0140 / 0.6737±0.0069**
- 复现：`$env:PYTHONHASHSEED=0; python scripts/figures/fig4_null_model.py`（`--seeds` 同 §1）
- 缺口关闭：≥5 seed 均值±SD 已补；函数 seed 参数化已做。红方"全局值无源"指控不成立（出处即 CSV 第 7 行）维持。

### §2.3 LDS-C label permutation（人类 N=15，p 值）— needs_review（代码就绪，实验 blocked）
- 代码：`scripts/lds_c_compute.py:355-401`（默认 n_iter **200→1000**；p 值二项 SE 注释 `SE(p)=sqrt(p(1-p)/n)` 已加：p=0.08 在 n=200 时 SE≈0.019、n=1000 时 SE≈0.0086）；`build_report:419-481` 解耦（新增 `floor_iter/perm_iter` 参数 + CLI `--floor-iters/--perm-iters`，替代 legacy `max(200,iterations//5)` 钳制；显式 n_iter 的调用方 `lds_c_llm_analyze:190-192`/`lds_c_multi_model:96`/`design_effect:112`/`r3:71` 不受影响，签名兼容已冒烟验证）
- 产物（未变）：`data/lds_c/lds_c_results_20260808.json:95-109` → p=0.08/1.0/1.0
- 缺口：p=0.08 的 SE=0.019，95%CI [0.042,0.118] 跨 0.05 线 → **不得做显著性解读**（维持）；≥1000 置换重算 **blocked**（全量 LDS-C 重跑贵 + 写盘涉 `data/lds_c/`，B 组未执行，只做了 `--help`/单函数签名冒烟 + 37 个相关单测全绿）。
- 默认路径漂移声明：已发表 p=0.08/1.0/1.0 仅在显式 `n_iter=200` 下复现；新默认（perm 1000 / floor 200）裸调用不再复现旧值 —— 复现有旧行为请显式传参。
- 转正条件：跑 `python scripts/lds_c_compute.py --perm-iters 1000 --floor-iters 200` 并更新产物 JSON。

## §3 Human N=15 floor — needs_review（代码就绪，实验 blocked）
- 代码：`lds_c_compute.py:297-353`（参与者分半；默认 n_iter **100→200**；新增 `return_stats=True` 报 mean/std/n，默认返回 `{pair: mean}` 保持调用方兼容：`design_effect:112`/`llm_analyze:190,280`/`r3:71`/`fig_a7_core:161` 均传显式 n_iter 且取均值，不受影响；`build_report` 额外存 `null_models.within_language_split_half_stats` + `null_iters{floor_n,perm_n}`）
- 产物（官方，未变）：`data/lds_c/llm_subject/design_effect_20260810.json:30,41,52` → floor 0.959/0.924/0.922，margin 0.005/0.009/0.014
- 旧版 `lds_c_results_20260808.json:90-93`（0.958/0.923/0.922，n_iter 不同）退役 → 以 design_effect 为单源（维持）。
- 缺口：floor 分半重复分布重算 **blocked**（`design_effect` 写盘目标在 `data/lds_c/llm_subject/` 禁区 + 全量 bootstrap 贵；B 组只做单函数冒烟：`within_language_split_half` 默认 200 生效、`return_stats` 正常、`test_lds_c_deepen` 37/37 绿）。
- 转正条件：A 组或解禁后跑 `signal_table(..., n_floor=200)` 取 `return_stats` 的 std 报 CI。

## §4 LDS-C 人机同幅 / floor 分离 — verified（全文最稳）
- 人类 0.963/0.932/0.936 vs LLM 0.955/0.930/0.945（幅度同）；floor 0.92-0.96 vs 0.875/0.846/0.862；margin 0.005-0.014 vs 0.081-0.084。
- 产物：`design_effect_20260810.json` + `outputs/figures/fig_a7_1_delta_lds.csv:2-4`。
- N=3 仍 margin+0.02-0.04，排除样本量解释。

## §5 Within-language floor 0.97（教材图分半）— verified（2026-09-14，B5）
- 代码：`fig4_null_model.py:142-174`（单次确定性分半/seed 已在函数 docstring 写明；不支持内部多 seed → 按 B5 决议纳入 `--seeds` 外循环，见 403-440；`_mean_sd_rows:371` + `_adv_cell:383` 键映射）
- 产物：`fig4_null_model_data.csv:6` 单 seed → 0.9695/0.9744/0.9615（哈希稳定：PYTHONHASHSEED=1/2 双进程比特一致，因边交集恒 0、LDS=1−node_jac/2 只依赖确定性节点序；与旧值一致）；`:11` 5-seed 均值 → ZH-EN←ZH **0.9700±0.0061** / DE-EN←DE **0.9692±0.0055** / ZH-DE←EN **0.9682±0.0085**；`:8/:12` **Mono Control 列已填值**（B5 bug 修：键 `ZH-ZH/EN-EN/DE-DE` 位置映射 → 单 seed 0.9695/0.9615/0.9744；5-seed 均值 0.9700/0.9682/0.9692±0.0061/0.0085/0.0055；mono 与 within 同构故数值同源，已在 CSV notes 注明）
- 复现：`$env:PYTHONHASHSEED=0; python scripts/figures/fig4_null_model.py`
- 缺口关闭：Mono 空列修好 + 5-seed 分布已补（SE≈0.003；200× 更紧 SE 为 P1 可选项，非转正必需）。
- 与 §3 不可混用（参与者异质性 vs 图分半）（维持）。

## §6 Size-match k=15/25/35 — verified（2026-09-14，B6；方向 + 冻结值）
- 代码：`scripts/p2_size_match.py`（`:28-38` 入口 `PYTHONHASHSEED` 断言非 0 即退出；`:55` `sorted(nodes,key=repr)` 冻结采样序；`:63-89` 报均值±SD；调用源 `math_pooled/wiki_pooled` 返回 set 已在注释中记因）
- 产物（`$env:PYTHONHASHSEED=0` 下双进程比特一致；`n_iter=200, seed=20260810`）：
  - k=15：math **0.030±0.029** vs wiki **0.053±0.037**，gap **−0.023**
  - k=25：math **0.048±0.032** vs wiki **0.101±0.037**，gap **−0.053**
  - k=35：math **0.069±0.030** vs wiki **0.149±0.030**，gap **−0.080**
  - 全尺寸参照（同跑输出，2026-09-14 核对）：ZH-DE **LDS math 0.519 vs wiki 0.819**（J_node math 0.556 vs wiki 0.200；docstring 已按此重写：旧 0.444 系 node-only ablation ZH-DE 值 `figures_i18n_wave2.py:372`，旧 0.800 系过期 wiki 口径，已退役并在 docstring 注明出处）
- 复现：`$env:PYTHONHASHSEED=0; python scripts/p2_size_match.py`（k=45/60/100 因 wiki 每语言 ≤47 节点自动跳过）
- 结论：wiki>math、gap 全负，方向成立；点值 exact reproducibility 成立（守卫 + 排序冻结 + 双跑一致）。旧"跨进程抖 ±0.002"已消除。

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
- **(d) GED 路线正式放弃（2026-09-14，用户决策）**：三元家族欠定不可证伪，不再寻求近似；二元冻结为唯一发表管线（`src/scoring.py` VERDICT 区已追加同句注释，行为代码未动）。
- 对齐动作（v20）：paper §2.7 二元为准 + 本台账指针；`src/scoring.py` 加 VERDICT 注（行为不动，4 条管线在用）；Fig2 重画为二元流程；portal 公式卡改回二元。

## §9 Margin ≥0.10 — needs_review（悬置）
- 产物：`sw_fix_analyses_20260910.json` span 0.033-0.424，median 0.126，0.10 在 CI 外（自标启发式）。
- 依赖 §2.2/§5 缺失的 CI → CI 补齐前悬置，不可作审计阈值引用。

## §10 Fig4 / Fig8 frozen figure values（2026-09-14 更新，B1/B2/B5 重跑，可引用绘图快照）
- **Fig4**（`$env:PYTHONHASHSEED=0; python scripts/figures/fig4_null_model.py [--seeds "42,999,2026,7,1234"]` → `outputs/figures/fig4_null_model_data.csv` + `fig4_null_model{,_de,_zh}.png`）：Full 基线 **0.9336 / 0.9382 / 0.5188**（ZH-EN / DE-EN / ZH-DE；发表取整 0.934/0.938/0.519）；Structure Null 点值 **0.9571/0.9568/0.7154**（sorted 冻结，旧快照 0.9571/0.9546/0.7142 见 §1 差异说明）+ 5-seed 均值±SD **0.9562±0.0010 / 0.9555±0.0024 / 0.7170±0.0013**；Within-Lang floor 点值 0.9695/0.9744/0.9615 + 5-seed 均值 0.9700/0.9692/0.9682（±0.0061/0.0055/0.0085）；Label-Permute 点值 0.8407/0.8701/0.6704 + 5-seed 均值 0.8561±0.0059/0.8572±0.0140/0.6737±0.0069；Mono Control 列已填（点值 0.9695/0.9615/0.9744，5-seed 均值 0.9700/0.9682/0.9692）。
- **Fig8**（`scripts/figures/fig8_lds_decontamination.py` → `outputs/figures/fig8_lds_decontamination_data.csv` + `fig8_lds_decontamination{,_de,_zh}.png`，确定性快照、不重算）：Full 0.934/0.938/0.519 vs Structure Null 0.957/0.957/0.717 vs 去污染 T1 FilterA（167/219 CJK-de 标签剔除、52 保留）0.985/0.985/0.990；ZH-DE 箭头 +0.47（T1 falsifiziert）。复现：`python scripts/figures/fig8_lds_decontamination.py`。快照基底声明（2026-09-14）：Fig8 struct 列为 09-12 冻结快照（3 位小数），与当前 point（0.9571/0.9568/0.7154）差 ≤0.003（ZH-DE 0.717 vs 0.7154）；箭头结论只依赖 full vs 去污染，与 struct 列无关，不受影响。
- **fig_a7_3 语义**（2026-09-14）：`fig_a7_core.py` 改首行胜出 → fig_a7_3 取 legacy point（非 multiseed 均值）；EN/DE/ZH 三图已按此重建（`fig_a7_3_null_models{,_de,_zh}.png`）。
- **档案声明**：`data/lds_c/**` 历史 JSON（如 `metric_robustness_20260811.json`、`multi_model_replication_202608*.json` 内 0.9546）保留冻结前值为档案，**不得引用**；引用以本台账 §1/§10 为准。

## 补实验优先级
- P0（2026-09-14 状态）：§2.2 多 seed 分布 ✅、§5 floor 分布 + Mono 修 ✅（均为 5-seed；200× 更紧 SE 为可选项）、§1 sorted 冻结 ✅；§2.3 n_iter≥1000 重算 ⏳blocked（代码就绪，待跑 `--perm-iters 1000`）。
- P1：§7 gloss 抽检 + 交叉、§6 ✅ 已重冻（docstring 旧数 0.444/0.800 待 A 组核对）、Mono bug ✅ 已修。
- P2：GED 近似路线 ✅ 已正式放弃并冻结（§8d，用户决策 2026-09-14）、旧 1.0 CSV 归档。
