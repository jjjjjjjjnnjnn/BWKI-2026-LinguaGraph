# RSA Bridge — RDM × Tier1/Tier2/H (T5 spec, frozen 2026-09-14)

> 目标：把 §8.10–8.16 的 Within/Between 结论转成可复算的 RSA 关环协议。
> 只定义、不跑数；跑数前必须满足密度守卫与 perm 下限，否则判 `offen`。
> 基线引用以 `docs/BASELINE_LEDGER.md` 为准，档案 JSON 值不得引用（见 Ledger §10 档案声明）。

## 0. 来源锚点

- 论文 §8.10–8.16：`docs/paper/04_discussion.md:136-239`
  - Threats (§8.10:136-150)：Between N=15 power 0.06–0.12，Within N=15 0.11–0.44；R1 注册 Within N≥30/臂。
  - 解释框架 (§8.11:152-168)：Rauschboden ≈0.97，Struktur-Null ≈0.96，ZH-DE 0.519 部分收敛，ZH-EN/DE-EN 近噪声地板。
  - 限制 (§8.12:171-188)：人类边稀疏（162 边：DE 59/ZH 67/EN 36），个体级边不可释；LDS 阈值 0.90/0.50 为描述性，需 bootstrap CI 替代。
  - LLM-as-Subject (§8.14:200-213)：Between 无分离信号 vs Within 有信号（+0.08~+0.09）；LMM 分离 same_lang +0.038 p<0.001 / same_frame +0.001 p=0.90；M2 自由联想解释 EN 对、不解释 ZH-DE；P2-Recheck 数学 J_node=0.556 含对齐/尺寸伪影。
  - 58 模型复制 (§8.15:216-228)：59 测量全 LDS-C>floor，59/59 ZH-DE 显著；177 测试中 9 个 n.s. 全为 EN 对；marge +0.03~+0.42；vote ≥10: 237 vs 157±4 / ≥20: 72 vs 14±2 (p<0.001)；perm 分辨率 500 不足（Bonferroni 0.05/177≈0.0003 不可分辨）；dedupe 54/54 仍显著；小模型链断在提取（密度阈值 ≈50 概念/语言）。
  - 文化方向 (§8.16:229-239)：DE 自主/规则/目标 vs ZH 空间/边界/诉求 — 仅解释性假设，非因果。
- 基线台账：`docs/BASELINE_LEDGER.md`
  - §1 Structure Null verified：point 0.9571/0.9568/0.7154，5-seed 均值 0.9562±0.0010/0.9555±0.0024/0.7170±0.0013。
  - §2.3 LDS-C label perm needs_review：默认 n_iter 200→1000，p=0.08 在 n=200 时 SE≈0.019（CI 跨 0.05 线，不得做显著性解读）；转正需 `--perm-iters 1000 --floor-iters 200`。
  - §3 Human floor needs_review：官方 floor 取 `data/lds_c/llm_subject/design_effect_20260810.json` 0.959/0.924/0.922（margin 0.005/0.009/0.014）；旧 `lds_c_results_20260808.json` 0.958/0.923/0.922 已退役。
  - §5 教材 within-floor verified：point 0.9695/0.9744/0.9615；5-seed 0.9700±0.0061/0.9692±0.0055/0.9682±0.0085；Mono 列已填。
  - §6 size-match verified：k=15/25/35 gap −0.023/−0.053/−0.080（wiki>math 全负）；k=45/60/100 自动跳过（wiki 每语言 ≤47 节点）；全尺寸 ZH-DE LDS math 0.519 vs wiki 0.819。
  - §8 公式裁决：二元 `1-mean(J_node,J_edge)` verified（0.9336→0.934/0.9382→0.938/0.5188→0.519）；三元/GED 路线放弃。
  - §9 margin ≥0.10 needs_review 悬置（启发式，非审计阈）。
  - §10 Fig4/Fig8 frozen 快照（Full/Null/floor/perm 点值与 5-seed 分布）。
- 数据布局（只列目录，未读内容；`data/lds_c/outputs` 不存在）：
  - `data/lds_c/`：`lds_k_deep/` + `llm_subject/` + 顶层 JSON（extractions/relations/thematic/divergence_drivers/lds_c_results）。
  - `data/lds_c/llm_subject/`：P1 主体 `llm_subject_*_20260810.json`、复制波 `*_20260909/0910/0912/0913.json`、分析 `design_effect_*.json` / `multi_model_replication_*.json` / `sw_fix_analyses_*.json` / `per_topic_*.json`。
  - `outputs/`：`figures/` + `tables/` + `ablation/` + LDS-C/人机对照 JSON（`human_pilot_*`、`lds_c_v3_*`、`sim_baseline_lds.json`）。

## 1. RDM 单元：语言对 × 5 主题 = 15 cell

- 语言对（固定序）：`[ZH-EN, DE-EN, ZH-DE]`（Ledger §10 Full 基线序）。
- 主题（固定序，`scripts/lds_c_compute.py:44`）：`[Freiheit, Gerechtigkeit, Verantwortung, Heimat, Erfolg]`。
- 一个 RDM 向量 = 15 个 LDS-C（或 LDS-K 对齐子集）按 `pair-major × topic-minor` 展平：
  `idx = pair_i*5 + topic_j`，共 15 维。矩阵形式为 15×15 距离矩阵或 15 维向量视实现而定，但**单元与顺序冻结**，跨 Tier/H 比较时必须同一展平。
- 缺失 cell（如空提取致 NaN，见 §8.15 hy-mt2/gemma  quarantine）不插值，直接触发密度守卫（§4）。

## 2. Tier1 / Tier2 / H 三矩阵列定义

| 矩阵 | 内容（每 cell 一个 LDS 值） | 公式/协议 | 列（15 维）定义 |
|------|---------------------------|-----------|-----------------|
| Tier1 教材结构 | 教材图 LDS-K（对齐子集；5 主题映射到 `figures_i18n_wave2.py:349-350` topics） | 二元冻结 `1-mean(J_node,J_edge)`（Ledger §8a/§10；`reproduce_lds_binary.py`）；Structure Null 对照 Ledger §1 | `T1[pair_i,topic_j]`：该 pair×topic 下教材子图 LDS-K；附 Null 列（structure-null 5-seed 均值±SD）仅作锚，不进 RSA |
| Tier2 LLM Within | LLM-as-Subject Within LDS-C（P1 协议：3 语言 × k=10，`scripts/lds_c_llm_subject.py:50` TOPICS） | `lds_c_compute.py` + floor/split-half + label-perm（perm≥1000，见 §3）；floor 取模型内 within（§8.15：典型 0.70–0.87，command-a ~0.49 需 ratio 并报） | `T2[pair_i,topic_j]`：同模型同协议下 per-topic LDS-C；跨模型比较时每个模型一个 15 维向量，禁止跨提取密度模型混拼绝对 marge（Befund 2 注记） |
| H 人类 Between | 人类 N=15 LDS-C v3（Node+Edge Jaccard；162 边 DE59/ZH67/EN36，`§8.12:182`） | v3 全公式；floor 取 `design_effect_20260810.json` 0.959/0.924/0.922（Ledger §3 单源；旧 0808 结果退役） | `H[pair_i,topic_j]`：人类 per-topic LDS-C；个体级边稀疏 → H 的边分量只做组级解读 |

- 对齐约束：Tier1↔Tier2/H 比较前先过 size-k 检查（§5）；数学 J_node 0.556 含对齐/尺寸伪影（§8.14 P2-Recheck），Tier1 数学 cell 不得单独作收敛证据。
- 版本约束：人类 N=15 提取器 `deepseek-v4-flash` vs 教材 `qwen-plus`（§8.10/§8.7），跨提取器比较只报方向，不报绝对差（Ledger §8.8 尺度漂移）。

## 3. RSA 统计：Spearman + Mantel，perm ≥ 1000

1. 主量：Tier 向量间 Spearman ρ（15 点；`compare_human_vs_model.py:77-96` 同函数；n=15 时 CI 宽 — 必须报 CI，`gate_review_layer1` 注记）。
2. 矩阵量：Mantel（Spearman 秩版）对 15×15 RDM，perm **≥1000**（下限来自 Ledger §2.3 n=1000 SE≈0.0086 + §8.15 perm=500 不足辨 Bonferroni；177 检验全局推断只做 meta 计数：期望假阳性 177×p_perm vs 观测全超）。
3. CI：bootstrap（≥1000 resamples）报 ρ 95% CI；perm p 报单侧 + SE(p)=sqrt(p(1-p)/n)。
4. 多重性：3 矩阵对（T1-T2/T1-H/T2-H）× 可选 per-topic 不做逐格显著性宣称；显著性只用于 ZH-DE 主对 + vote meta（§8.15a 逻辑）。
5. Floor 归一化敏感性：marge 与 ratio（LDS-C/floor）Spearman 并报（§8.15e：0.997/TOP5 同为通过线；command-a 类低 floor 模型 ratio 必报）。

## 4. 密度守卫：<50 unresolved

- 阈值：任一语言 `concepts/language < 50` → 该模型/条件判 **unresolved**，不进 RSA、不做 null/signal 宣称（§8.15 Kleinstmodell-Grenze：phi-4-mini ~140/语言通过；qwen2.5-0.5b zh 36 → floor NaN 诚实零；hy-mt2 空 topic 集 → marge 未定义 retired；gemma-3-270m 不遵 schema → quarantine）。
- 检查点：跑 RSA 前输出每语言概念计数 + 空 topic 集清单；NaN cell 计数>0 直接 unresolved。
- 人类 H 侧：边总数 <50/语言时边分量只组级描述（§8.12 稀疏注记）。

## 5. Size-k 检查

- 沿用 Ledger §6：k=15/25/35 下 math vs wiki gap（−0.023/−0.053/−0.080；wiki>math 全负为通过方向）；k=45/60/100 因 wiki 每语言 ≤47 自动跳过。
- RSA 关环前必须跑 size-matched 对照：若 full-size 结论在 k-matched 下反转（如 §8.14 数学 J_node 反转注记），则 Tier1 相关 ρ 判伪影，不得关环。
- 复现：`$env:PYTHONHASHSEED=0; python scripts/p2_size_match.py`（入口断言 + sorted 冻结，Ledger §6）。

## 6. 关环判据（三合一，否则 offen）

`CLOSED ≡ (ρCI>0) ∧ (vote超额) ∧ (M2一致)`，任一不满足 → **`offen`**（不得写 closed/证实）：

1. **ρCI>0**：目标对（Tier2-H 主检，Tier1-T2 辅检）Spearman/Mantel ρ 的 bootstrap 95% CI 下界 >0。点估计>0 不算；CI 含 0 → offen。
2. **vote超额**：ZH-DE 方向 vote（per-concept max(DE,ZH)≥t 计数）超频率适配随机 null（concept 总频固定、方向 p=0.5），阈值 ≥10 且 ≥20 双过，p<0.001（§8.15 Befund 3：237 vs 157±4；72 vs 14±2）；dedupe（54 去重）+ 双 host 上限 10 票偏置敏感性并报。
3. **M2一致**：机制分解与 §8.14 一致 — LMM same_lang 显著而 same_frame 不显著（+0.038 p<0.001 vs +0.001 p=0.90 方向），且自由联想 mediation 对 EN 对成立、对 ZH-DE 不成立（结构层超出联想统计）。任一反转 → offen；数学 knot 伪影（对齐标签/`de` 含中文/size 反转）未排除前 Tier1 不得单独关环。
- 诚实边界并记：§2.3/§3 blocked（perm/floor ≥1000 重算未跑）、§7 gloss 无盲抽（wiki 对照不用作内容证据）、§9 margin 0.10 悬置（不用作阈）、81% CN 供应商 + 9 EN n.s. + luna 去除敏感性（§8.15 Befund 1/2/ **▲**）。

## 7. 产物与复现占位（待跑数时填）

- 输入清单：`design_effect_20260810.json`（H floor）+ 选定模型 `llm_subject_*`（Tier2）+ 教材子图 LDS-K 快照（Tier1）+ `sw_fix_analyses_*.json`（vote/marge 分布）。
- 命令占位：`python scripts/lds_c_compute.py --perm-iters 1000 --floor-iters 200`（Ledger §2.3 转正条件）；`signal_table(..., n_floor=200)` 取 `return_stats` 报 CI（Ledger §3）。
- 输出：15 维三向量 CSV + ρ/CI/perm-p 表 + vote 表 + size-k 表 + `CLOSED/offen` 一行裁决。
