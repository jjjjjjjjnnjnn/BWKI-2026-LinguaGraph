# 多源共识投票 v2 20260914

离线计算，不调 API。归一化=小写+去全部空白；Jaccard=|交|/|并|（空空=1.0）。intra=每模型≥2 runs 文件的两两 run 概念 Jaccard 均值再按文件平均；inter=深度 24 上代表 run（r1，缺则 r2/r3）两两模型共存文件均值；vs mimo=代表 run vs mimo 概念 Jaccard；表决 v2=深度 24 每文件可用源严格多数（thr=n//2+1）：概念≥thr 收录，关系≥thr=Solid，==1=Hypothetical，中间=Weak，mimo 独有=候选删。

输入：mimo `24/24`（深度内）+ spark audit `12` 个（深度内 `11`）+ ensemble 7 模型 + bailian `*.bailian.json` `62` 个（缺席，missing 不计分）；缺席一律不计分。

## 覆盖表（深度 24）

| 模型 | done | 缺席 | 代表run r1 | 回退r2/r3 | intra_n | intra 均值 | vs_mimo_n | vs_mimo 均值 | inter 行均值 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek-v4-pro-0813 | 22 | 2 | 22 | 0 | 20 | 0.5206 | 22 | 0.222 | 0.4706 |
| deepseek-v4.1-flash | 24 | 0 | 24 | 0 | 24 | 0.6 | 24 | 0.2338 | 0.5166 |
| kimi-k3 | 24 | 0 | 24 | 0 | 24 | 0.7291 | 24 | 0.2427 | 0.4778 |
| qwen3.7-flash | 24 | 0 | 24 | 0 | 24 | 0.6035 | 24 | 0.2583 | 0.4564 |
| qwen3.8-27b | 24 | 0 | 24 | 0 | 24 | 0.5862 | 24 | 0.2228 | 0.5172 |
| qwen3.8-max | 24 | 0 | 24 | 0 | 24 | 0.6276 | 24 | 0.2239 | 0.5352 |
| qwen3.8-max-0902 | 24 | 0 | 24 | 0 | 24 | 0.6304 | 24 | 0.2315 | 0.5326 |

mimo 深度覆盖：24/24；spark audit 深度覆盖：11/24；bailian：62（无 `*.bailian.json`，全部缺席）。

## 1) intra-model 自一致性（概念 Jaccard）

| 模型 | 文件数(≥2runs) | 均值 |
|---|---:|---:|
| deepseek-v4-pro-0813 | 20 | 0.5206 |
| deepseek-v4.1-flash | 24 | 0.6 |
| kimi-k3 | 24 | 0.7291 |
| qwen3.7-flash | 24 | 0.6035 |
| qwen3.8-27b | 24 | 0.5862 |
| qwen3.8-max | 24 | 0.6276 |
| qwen3.8-max-0902 | 24 | 0.6304 |

## 2) inter-model 矩阵（深度 24，代表 run，概念 Jaccard；括号=n 共存文件）

|  | deepseek-v4-pro-0813 | deepseek-v4.1-flash | kimi-k3 | qwen3.7-flash | qwen3.8-27b | qwen3.8-max | qwen3.8-max-0902 |
|---|---|---|---|---|---|---|---|
| deepseek-v4-pro-0813 | 1.0000 | 0.508 (22) | 0.4389 (22) | 0.4065 (22) | 0.499 (22) | 0.4988 (22) | 0.4721 (22) |
| deepseek-v4.1-flash | 0.508 (22) | 1.0000 | 0.4913 (24) | 0.4574 (24) | 0.5447 (24) | 0.5703 (24) | 0.5282 (24) |
| kimi-k3 | 0.4389 (22) | 0.4913 (24) | 1.0000 | 0.4612 (24) | 0.477 (24) | 0.481 (24) | 0.5175 (24) |
| qwen3.7-flash | 0.4065 (22) | 0.4574 (24) | 0.4612 (24) | 1.0000 | 0.4854 (24) | 0.4582 (24) | 0.4696 (24) |
| qwen3.8-27b | 0.499 (22) | 0.5447 (24) | 0.477 (24) | 0.4854 (24) | 1.0000 | 0.546 (24) | 0.5514 (24) |
| qwen3.8-max | 0.4988 (22) | 0.5703 (24) | 0.481 (24) | 0.4582 (24) | 0.546 (24) | 1.0000 | 0.6572 (24) |
| qwen3.8-max-0902 | 0.4721 (22) | 0.5282 (24) | 0.5175 (24) | 0.4696 (24) | 0.5514 (24) | 0.6572 (24) | 1.0000 |

矩阵均值（非对角 21 对的均值）：**0.5009**。

## 3) vs mimo（概念 Jaccard，深度 24 共存文件）

| 模型 | n | 均值 |
|---|---:|---:|
| deepseek-v4-pro-0813 | 22 | 0.222 |
| deepseek-v4.1-flash | 24 | 0.2338 |
| kimi-k3 | 24 | 0.2427 |
| qwen3.7-flash | 24 | 0.2583 |
| qwen3.8-27b | 24 | 0.2228 |
| qwen3.8-max | 24 | 0.2239 |
| qwen3.8-max-0902 | 24 | 0.2315 |

## 4) 多数表决 v2（深度 24，thr=n//2+1）

- 收录概念：**546**；Solid 关系：**203**；Weak 关系（2..thr-1）：**884**；Hypothetical（1 源）：**1905**；候选删（mimo 独有）：**70**。

| basename | 源数 | 阈值 | 收录概念 | 候选删 | Solid | Weak | Hypo | 源列表 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| de_abitur_lk | 9 | 5 | 23 | 5 | 2 | 53 | 101 | mimo+spark+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_dgl_pde_ch9-11 | 9 | 5 | 19 | 3 | 2 | 54 | 72 | mimo+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_fischer_lineare_algebra_ch7-8_sec7.1-8.3 | 9 | 5 | 27 | 1 | 25 | 17 | 27 | mimo+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_forster_analysis1_ch5_sec5.1 | 9 | 5 | 20 | 0 | 17 | 19 | 39 | mimo+spark+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_lambacher_5-8 | 10 | 6 | 39 | 2 | 7 | 51 | 44 | mimo+spark+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_lambacher_5-8_erweitert | 9 | 5 | 31 | 8 | 12 | 41 | 82 | mimo+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_wahrscheinlichkeit_ch1-8 | 8 | 5 | 35 | 2 | 11 | 32 | 59 | mimo+spark+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_westermann_9-10 | 9 | 5 | 23 | 4 | 1 | 48 | 113 | mimo+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_ap_calculus_ab_bc | 8 | 5 | 34 | 5 | 11 | 36 | 46 | mimo+bailian+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_ib_math_aa_sl | 10 | 6 | 22 | 1 | 4 | 43 | 104 | mimo+spark+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_igcse_math_0580 | 9 | 5 | 20 | 7 | 1 | 38 | 129 | mimo+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_khan_academy_3-4 | 10 | 6 | 19 | 3 | 3 | 50 | 98 | mimo+spark+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_khan_academy_5-6 | 9 | 5 | 22 | 8 | 7 | 34 | 129 | mimo+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_khan_academy_6-8 | 10 | 6 | 22 | 6 | 4 | 52 | 99 | mimo+spark+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_khan_academy_k-2 | 9 | 5 | 12 | 3 | 1 | 30 | 153 | mimo+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_stewart_ch3_sec3.1 | 10 | 6 | 21 | 0 | 6 | 47 | 59 | mimo+spark+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_偏微分方程_ch10_sec10.1-10.3 | 9 | 5 | 24 | 0 | 16 | 30 | 25 | mimo+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_初中数学_七年级 | 9 | 5 | 29 | 3 | 21 | 29 | 37 | mimo+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_初中数学_九年级 | 9 | 5 | 22 | 6 | 14 | 11 | 23 | mimo+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_小学数学_一年级下 | 9 | 5 | 28 | 2 | 20 | 20 | 49 | mimo+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_微分方程_ch3_sec3.2-3.4 | 10 | 6 | 8 | 0 | 0 | 40 | 145 | mimo+spark+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_微分方程_ch4_sec4.1-4.3 | 10 | 6 | 20 | 1 | 5 | 35 | 94 | mimo+spark+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_选修2-2_ch1_sec1.2 | 10 | 6 | 12 | 0 | 1 | 50 | 100 | mimo+spark+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| zh_选修2-2_ch1_sec1.3 | 9 | 5 | 14 | 0 | 12 | 24 | 78 | mimo+bailian+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |

明细见 `research/consensus_v2_20260914.json`。
