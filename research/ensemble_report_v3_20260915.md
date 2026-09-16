# Ensemble 总报告 v3 20260915（终局汇总·只引用不重算）

> 地位：替代 stale 的 `ensemble_report_v2_20260914.md`（其"bailian 0 缺席"声明已过时）。
> 汇总 `research/consensus_v3_20260915.md` + `research/multi_model_verdict_v3_20260915.md` +
> 红蓝 v3。离线口径继承：归一化=小写+去全部空白；Jaccard=|交|/|并|（空空=1.0）；缺席一律不计分。
> 外线引用：LDS-C 双复现 p=0.0（待入库）+ kimi incomplete；wiki 宽松 28/30、严格 21/30（needs_review）；
> 理化 J~0.02 初探；pytest 84（修数前后两绿）。

## ① 矩阵与覆盖终局（7 模型 depth 落盘 / manifest）

| 模型 | depth 落盘/72 | 缺席 | intra (n) | inter 行均值 | vs mimo (n) |
|---|---|---|---|---|---|
| deepseek-v4-pro-0813 | 12 | 60（403+截断，探索） | 0.6029 (5) | 0.5819（小样本） | 0.2575 (5) |
| deepseek-v4.1-flash | ~40 | ~32（通道天花板，4 不再重试） | 0.6393 (14) | 0.5739 | 0.2271 (18) |
| kimi-k3 | 71 | 1（en_ap r3 两败，永久） | 0.7291 (24) | 0.4917 | 0.2427 (24) |
| qwen3.7-flash | 72 全勤 | 0 | 0.6035 (24) | 0.4759 | 0.2583 (24) |
| qwen3.8-27b | 72 全勤 | 0 | 0.5862 (24) | 0.5382 | 0.2228 (24) |
| qwen3.8-max | 71 | 1（wahrsch r3 三败，永久） | 0.6276 (24) | 0.5666 | 0.2239 (24) |
| qwen3.8-max-0902 | 72 全勤 | 0 | 0.6304 (24) | 0.5527 | 0.2315 (24) |

- 广度：qwen 四模型 bmiss 清零（done 113/112/113/112）；ds 系 breadth 不同分母（探索）。
- inter 全局 **0.5401**（v2 0.4629 系配额截断值，不可比，Δ+0.077 为分母 artefact；max–max0902 0.6572 最高，厂商聚类延续）。
- 表决 v3（thr=n//2+1，源数 6–9 浮动）：收录 **540** / Solid **194** / Weak **736** / Hypo **1716** / mimo 独有候选删 **73**。
- 本轮入库约 120 文件，全过审计门（15–40 概念/10–30 关系/引用闭合/无 `?�` 乱码/fresh-stage 守卫）；拦截复本污染 1 起（27b abitur r2，已回滚重跑）。

## ② 核心数字（只引用 consensus_v3 行号）

- intra 0.59–0.73（n=24 齐整，qwen 四模型 + kimi）；temp=0 run 间分歧 ~30–40%。
- inter 0.5401：缺席敏感快照（C2 降级令），禁进 headline、禁报趋势。
- vs mimo 0.22–0.26：单次快照，双方皆未确证；mimo 维持基线。
- gold bench v2 不变（max-0902 0.7376 > max 0.7325 > 3.7 ≈ flash 0.711 > 27b 0.698 > kimi 0.554；ds 系 harness 不兼容）。

## ③ 裁决摘要（verdict v3 C1–C7）

- C1 intra：temp=0 非确定，带波动带。【V】
- C2 inter：红降级令（ artefact ），禁 headline。【V+降级】
- C3 vs mimo：快照，73 候选删。【V】
- C4 ds：pro 三数全禁（unmeasurable）；v41 须并列审计声明；聚合未剔除→维持污染快照章。【V】
- C5 缺席：保守口 + thr 浮动须拆分（R5）；4 缺席=天花板。【V+L1】
- C6 外线沿 v2；C7 Two-Tier 沿 v2 + L4/L5 追记。【V】

## ④ 可登记口径（5 条，见 verdict_v3 §②原样）

## ⑤ 禁止清单（v2 9 条延续 + v3 新增 3 条，见 verdict_v3 §③）

## ⑥ 待办 R1–R5 / F1–F4 / 解冻 L1–L3（见 verdict_v3 §④；修数①②已执行，见 §⑦）

## ⑦ 修数状态（2026-09-15/16）

- ①删幻觉边 2 + ②去重 24 = 26 删边执行（10 文件，备份 `research/prune_backup_20260915/`），复扫 141→115，pytest 84 绿。
- 挂起：③纠 13（对照表 `research/prune_fix_r3_review_20260916.md` 待逐条勾选）④破 10 环 ⑤bad_length 65 + 归档 2。清零前不得冻结。
