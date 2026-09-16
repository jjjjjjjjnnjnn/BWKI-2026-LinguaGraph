# 多源共识投票 v2 20260914

离线计算，不调 API。归一化=小写+去全部空白；Jaccard=|交|/|并|（空空=1.0）。intra=每模型≥2 runs 文件的两两 run 概念 Jaccard 均值再按文件平均；inter=深度 24 上代表 run（r1，缺则 r2/r3）两两模型共存文件均值；vs mimo=代表 run vs mimo 概念 Jaccard；表决 v2=深度 24 每文件可用源严格多数（thr=n//2+1）：概念≥thr 收录，关系≥thr=Solid，==1=Hypothetical，中间=Weak，mimo 独有=候选删。

输入：mimo `24/24`（深度内）+ spark audit `12` 个（深度内 `11`）+ ensemble 7 模型 + bailian `*.bailian.json` `0` 个（缺席，missing 不计分）；缺席一律不计分。

## 覆盖表（深度 24）

| 模型 | done | 缺席 | 代表run r1 | 回退r2/r3 | intra_n | intra 均值 | vs_mimo_n | vs_mimo 均值 | inter 行均值 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek-v4-pro-0813 | 2 | 22 | 1 | 1 | 1 | 0.6667 | 2 | 0.3809 | 0.4572 |
| deepseek-v4.1-flash | 10 | 14 | 8 | 2 | 6 | 0.5625 | 10 | 0.2137 | 0.458 |
| kimi-k3 | 24 | 0 | 24 | 0 | 23 | 0.7347 | 24 | 0.2427 | 0.4283 |
| qwen3.7-flash | 24 | 0 | 24 | 0 | 24 | 0.6035 | 24 | 0.2583 | 0.4038 |
| qwen3.8-27b | 17 | 7 | 16 | 1 | 16 | 0.5534 | 17 | 0.2492 | 0.5067 |
| qwen3.8-max | 15 | 9 | 15 | 0 | 15 | 0.6079 | 15 | 0.2295 | 0.5005 |
| qwen3.8-max-0902 | 15 | 9 | 15 | 0 | 14 | 0.6042 | 15 | 0.2415 | 0.4859 |

mimo 深度覆盖：24/24；spark audit 深度覆盖：11/24；bailian：0（无 `*.bailian.json`，全部缺席）。

## 1) intra-model 自一致性（概念 Jaccard）

| 模型 | 文件数(≥2runs) | 均值 |
|---|---:|---:|
| deepseek-v4-pro-0813 | 1 | 0.6667 |
| deepseek-v4.1-flash | 6 | 0.5625 |
| kimi-k3 | 23 | 0.7347 |
| qwen3.7-flash | 24 | 0.6035 |
| qwen3.8-27b | 16 | 0.5534 |
| qwen3.8-max | 15 | 0.6079 |
| qwen3.8-max-0902 | 14 | 0.6042 |

## 2) inter-model 矩阵（深度 24，代表 run，概念 Jaccard；括号=n 共存文件）

|  | deepseek-v4-pro-0813 | deepseek-v4.1-flash | kimi-k3 | qwen3.7-flash | qwen3.8-27b | qwen3.8-max | qwen3.8-max-0902 |
|---|---|---|---|---|---|---|---|
| deepseek-v4-pro-0813 | 1.0000 | 0.5 (1) | 0.3296 (2) | 0.3189 (2) | 0.5556 (1) | 0.5988 (2) | 0.4402 (2) |
| deepseek-v4.1-flash | 0.5 (1) | 1.0000 | 0.4069 (10) | 0.3663 (10) | 0.4951 (10) | 0.5111 (9) | 0.4686 (9) |
| kimi-k3 | 0.3296 (2) | 0.4069 (10) | 1.0000 | 0.4612 (24) | 0.4888 (17) | 0.4193 (15) | 0.4638 (15) |
| qwen3.7-flash | 0.3189 (2) | 0.3663 (10) | 0.4612 (24) | 1.0000 | 0.4787 (17) | 0.3813 (15) | 0.4161 (15) |
| qwen3.8-27b | 0.5556 (1) | 0.4951 (10) | 0.4888 (17) | 0.4787 (17) | 1.0000 | 0.4937 (14) | 0.5283 (14) |
| qwen3.8-max | 0.5988 (2) | 0.5111 (9) | 0.4193 (15) | 0.3813 (15) | 0.4937 (14) | 1.0000 | 0.5985 (15) |
| qwen3.8-max-0902 | 0.4402 (2) | 0.4686 (9) | 0.4638 (15) | 0.4161 (15) | 0.5283 (14) | 0.5985 (15) | 1.0000 |

矩阵均值（非对角 21 对的均值）：**0.4629**。

## 3) vs mimo（概念 Jaccard，深度 24 共存文件）

| 模型 | n | 均值 |
|---|---:|---:|
| deepseek-v4-pro-0813 | 2 | 0.3809 |
| deepseek-v4.1-flash | 10 | 0.2137 |
| kimi-k3 | 24 | 0.2427 |
| qwen3.7-flash | 24 | 0.2583 |
| qwen3.8-27b | 17 | 0.2492 |
| qwen3.8-max | 15 | 0.2295 |
| qwen3.8-max-0902 | 15 | 0.2415 |

## 4) 多数表决 v2（深度 24，thr=n//2+1）

- 收录概念：**491**；Solid 关系：**145**；Weak 关系（2..thr-1）：**506**；Hypothetical（1 源）：**1554**；候选删（mimo 独有）：**76**。

| basename | 源数 | 阈值 | 收录概念 | 候选删 | Solid | Weak | Hypo | 源列表 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| de_abitur_lk | 7 | 4 | 20 | 5 | 2 | 40 | 92 | mimo+spark+deepseek-v4-pro-0813+kimi-k3+qwen3.7-flash+qwen3.8-max+qwen3.8-max-0902 |
| de_dgl_pde_ch9-11 | 7 | 4 | 25 | 3 | 7 | 40 | 63 | mimo+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_fischer_lineare_algebra_ch7-8_sec7.1-8.3 | 7 | 4 | 25 | 1 | 15 | 20 | 29 | mimo+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_forster_analysis1_ch5_sec5.1 | 9 | 5 | 17 | 0 | 14 | 21 | 41 | mimo+spark+deepseek-v4-pro-0813+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_lambacher_5-8 | 7 | 4 | 36 | 2 | 8 | 34 | 45 | mimo+spark+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_lambacher_5-8_erweitert | 6 | 4 | 24 | 9 | 3 | 30 | 88 | mimo+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_wahrscheinlichkeit_ch1-8 | 7 | 4 | 35 | 2 | 12 | 29 | 57 | mimo+spark+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| de_westermann_9-10 | 7 | 4 | 23 | 4 | 2 | 33 | 84 | mimo+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_ap_calculus_ab_bc | 6 | 4 | 29 | 7 | 15 | 23 | 42 | mimo+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_ib_math_aa_sl | 8 | 5 | 22 | 1 | 4 | 38 | 81 | mimo+spark+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_igcse_math_0580 | 6 | 4 | 14 | 9 | 3 | 22 | 80 | mimo+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_khan_academy_3-4 | 8 | 5 | 18 | 3 | 4 | 38 | 82 | mimo+spark+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_khan_academy_5-6 | 7 | 4 | 23 | 8 | 7 | 27 | 98 | mimo+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_khan_academy_6-8 | 8 | 5 | 24 | 6 | 5 | 27 | 102 | mimo+spark+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_khan_academy_k-2 | 7 | 4 | 12 | 3 | 2 | 20 | 126 | mimo+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b+qwen3.8-max+qwen3.8-max-0902 |
| en_stewart_ch3_sec3.1 | 6 | 4 | 17 | 0 | 3 | 29 | 44 | mimo+spark+deepseek-v4.1-flash+kimi-k3+qwen3.7-flash+qwen3.8-27b |
| zh_偏微分方程_ch10_sec10.1-10.3 | 4 | 3 | 18 | 0 | 6 | 14 | 36 | mimo+kimi-k3+qwen3.7-flash+qwen3.8-27b |
| zh_初中数学_七年级 | 4 | 3 | 30 | 3 | 12 | 12 | 41 | mimo+kimi-k3+qwen3.7-flash+qwen3.8-27b |
| zh_初中数学_九年级 | 3 | 2 | 23 | 7 | 14 | 0 | 26 | mimo+kimi-k3+qwen3.7-flash |
| zh_小学数学_一年级下 | 3 | 2 | 23 | 2 | 0 | 0 | 59 | mimo+kimi-k3+qwen3.7-flash |
| zh_微分方程_ch3_sec3.2-3.4 | 4 | 3 | 9 | 0 | 0 | 1 | 67 | mimo+spark+kimi-k3+qwen3.7-flash |
| zh_微分方程_ch4_sec4.1-4.3 | 4 | 3 | 10 | 1 | 0 | 7 | 60 | mimo+spark+kimi-k3+qwen3.7-flash |
| zh_选修2-2_ch1_sec1.2 | 4 | 3 | 4 | 0 | 1 | 1 | 70 | mimo+spark+kimi-k3+qwen3.7-flash |
| zh_选修2-2_ch1_sec1.3 | 3 | 2 | 10 | 0 | 6 | 0 | 41 | mimo+kimi-k3+qwen3.7-flash |

明细见 `research/consensus_v2_20260914.json`。
