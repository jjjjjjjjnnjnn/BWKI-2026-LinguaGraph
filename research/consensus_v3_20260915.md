# 多源共识投票 v2 20260914

离线计算，不调 API。归一化=小写+去全部空白；Jaccard=|交|/|并|（空空=1.0）。intra=每模型≥2 runs 文件的两两 run 概念 Jaccard 均值再按文件平均；inter=深度 24 上代表 run（r1，缺则 r2/r3）两两模型共存文件均值；vs mimo=代表 run vs mimo 概念 Jaccard；表决 v2=深度 24 每文件可用源严格多数（thr=n//2+1）：概念≥thr 收录，关系≥thr=Solid，==1=Hypothetical，中间=Weak，mimo 独有=候选删。

输入：mimo `24/24`（深度内）+ spark audit `12` 个（深度内 `11`）+ ensemble 7 模型 + bailian `*.bailian.json` `54` 个（缺席，missing 不计分）；缺席一律不计分。

## 覆盖表（深度 24）

| 模型 | done | 缺席 | 代表run r1 | 回退r2/r3 | intra_n | intra 均值 | vs_mimo_n | vs_mimo 均值 | inter 行均值 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek-v4-pro-0813 | 5 | 19 | 5 | 0 | 5 | 0.6029 | 5 | 0.2575 | 0.5819 |
| deepseek-v4.1-flash | 18 | 6 | 16 | 2 | 14 | 0.6393 | 18 | 0.2271 | 0.5739 |
| kimi-k3 | 24 | 0 | 24 | 0 | 24 | 0.7291 | 24 | 0.2427 | 0.4917 |
| qwen3.7-flash | 24 | 0 | 24 | 0 | 24 | 0.6035 | 24 | 0.2583 | 0.4759 |
| qwen3.8-27b | 24 | 0 | 24 | 0 | 24 | 0.5862 | 24 | 0.2228 | 0.5382 |
| qwen3.8-max | 24 | 0 | 24 | 0 | 24 | 0.6276 | 24 | 0.2239 | 0.5666 |
| qwen3.8-max-0902 | 24 | 0 | 24 | 0 | 24 | 0.6304 | 24 | 0.2315 | 0.5527 |

mimo 深度覆盖：24/24；spark audit 深度覆盖：11/24；bailian：54（无 `*.bailian.json`，全部缺席）。

## 1) intra-model 自一致性（概念 Jaccard）

| 模型 | 文件数(≥2runs) | 均值 |
|---|---:|---:|
| deepseek-v4-pro-0813 | 5 | 0.6029 |
| deepseek-v4.1-flash | 14 | 0.6393 |
| kimi-k3 | 24 | 0.7291 |
| qwen3.7-flash | 24 | 0.6035 |
| qwen3.8-27b | 24 | 0.5862 |
| qwen3.8-max | 24 | 0.6276 |
| qwen3.8-max-0902 | 24 | 0.6304 |

## 2) inter-model 矩阵（深度 24，代表 run，概念 Jaccard；括号=n 共存文件）

|  | deepseek-v4-pro-0813 | deepseek-v4.1-flash | kimi-k3 | qwen3.7-flash | qwen3.8-27b | qwen3.8-max | qwen3.8-max-0902 |
|---|---|---|---|---|---|---|---|
| deepseek-v4-pro-0813 | 1.0000 | 0.6962 (4) | 0.5052 (5) | 0.4915 (5) | 0.5942 (5) | 0.6551 (5) | 0.549 (5) |
| deepseek-v4.1-flash | 0.6962 (4) | 1.0000 | 0.5086 (18) | 0.4899 (18) | 0.5751 (18) | 0.602 (18) | 0.5717 (18) |
| kimi-k3 | 0.5052 (5) | 0.5086 (18) | 1.0000 | 0.4612 (24) | 0.477 (24) | 0.481 (24) | 0.5175 (24) |
| qwen3.7-flash | 0.4915 (5) | 0.4899 (18) | 0.4612 (24) | 1.0000 | 0.4854 (24) | 0.4582 (24) | 0.4696 (24) |
| qwen3.8-27b | 0.5942 (5) | 0.5751 (18) | 0.477 (24) | 0.4854 (24) | 1.0000 | 0.546 (24) | 0.5514 (24) |
| qwen3.8-max | 0.6551 (5) | 0.602 (18) | 0.481 (24) | 0.4582 (24) | 0.546 (24) | 1.0000 | 0.6572 (24) |
| qwen3.8-max-0902 | 0.549 (5) | 0.5717 (18) | 0.5175 (24) | 0.4696 (24) | 0.5514 (24) | 0.6572 (24) | 1.0000 |

矩阵均值（非对角 21 对的均值）：**0.5401**。

## 3) vs mimo（概念 Jaccard，深度 24 共存文件）

| 模型 | n | 均值 |
|---|---:|---:|
| deepseek-v4-pro-0813 | 5 | 0.2575 |
| deepseek-v4.1-flash | 18 | 0.2271 |
| kimi-k3 | 24 | 0.2427 |
| qwen3.7-flash | 24 | 0.2583 |
| qwen3.8-27b | 24 | 0.2228 |
| qwen3.8-max | 24 | 0.2239 |
| qwen3.8-max-0902 | 24 | 0.2315 |

## 4) 多数表决 v2（深度 24，thr=n//2+1）

- 收录概念：**540**；Solid 关系：**194**；Weak 关系（2..thr-1）：**736**；Hypothetical（1 源）：**1716**；候选删（mimo 独有）：**73**。

| basename | 源数 | 阈值 | 收录概念 | 候选删 | Solid | Weak | Hypo | 源列表 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| de_abitur_lk | 9 | 5 | 23 | 5 | 3 | 53 | 97 | mimo+spark+bailian+deepseek-v4-pro-0813+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_dgl_pde_ch9-11 | 8 | 5 | 18 | 3 | 0 | 52 | 68 | mimo+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_fischer_lineare_algebra_ch7-8_sec7.1-8.3 | 8 | 5 | 25 | 1 | 15 | 22 | 30 | mimo+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_forster_analysis1_ch5_sec5.1 | 9 | 5 | 20 | 0 | 17 | 19 | 39 | mimo+spark+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_lambacher_5-8 | 9 | 5 | 39 | 2 | 9 | 46 | 38 | mimo+spark+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_lambacher_5-8_erweitert | 6 | 4 | 24 | 9 | 3 | 30 | 88 | mimo+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_wahrscheinlichkeit_ch1-8 | 8 | 5 | 32 | 2 | 11 | 34 | 57 | mimo+spark+bailian+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_westermann_9-10 | 7 | 4 | 23 | 4 | 2 | 33 | 84 | mimo+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_ap_calculus_ab_bc | 7 | 4 | 33 | 6 | 17 | 27 | 46 | mimo+bailian+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_ib_math_aa_sl | 8 | 5 | 22 | 1 | 4 | 38 | 81 | mimo+spark+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_igcse_math_0580 | 6 | 4 | 14 | 9 | 3 | 22 | 80 | mimo+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_khan_academy_3-4 | 8 | 5 | 18 | 3 | 4 | 38 | 82 | mimo+spark+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_khan_academy_5-6 | 7 | 4 | 23 | 8 | 7 | 27 | 98 | mimo+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_khan_academy_6-8 | 8 | 5 | 24 | 6 | 5 | 27 | 102 | mimo+spark+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_khan_academy_k-2 | 8 | 5 | 8 | 3 | 1 | 25 | 140 | mimo+bailian+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_stewart_ch3_sec3.1 | 9 | 5 | 23 | 0 | 8 | 43 | 54 | mimo+spark+bailian+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_偏微分方程_ch10_sec10.1-10.3 | 8 | 5 | 23 | 0 | 15 | 26 | 27 | mimo+bailian+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_初中数学_七年级 | 8 | 5 | 28 | 3 | 17 | 27 | 37 | mimo+bailian+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_初中数学_九年级 | 8 | 5 | 22 | 5 | 13 | 13 | 25 | mimo+bailian+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_小学数学_一年级下 | 8 | 5 | 27 | 2 | 18 | 21 | 44 | mimo+bailian+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_微分方程_ch3_sec3.2-3.4 | 9 | 5 | 16 | 0 | 0 | 30 | 143 | mimo+spark+bailian+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_微分方程_ch4_sec4.1-4.3 | 9 | 5 | 24 | 1 | 11 | 27 | 70 | mimo+spark+bailian+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_选修2-2_ch1_sec1.2 | 9 | 5 | 15 | 0 | 1 | 35 | 123 | mimo+spark+bailian+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_选修2-2_ch1_sec1.3 | 7 | 4 | 16 | 0 | 10 | 21 | 63 | mimo+bailian+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |

明细见 `research/consensus_v2_20260914.json`。
