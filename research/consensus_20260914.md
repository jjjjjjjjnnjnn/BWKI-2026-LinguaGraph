# 三源多数表决共识 20260914

方法：概念归一化=小写+去全部空白；概念≥2源=收录；关系有序端点对一致≥2源=Solid，1源=Hypothetical（忽略 type）；mimo 独有且他源无=候选删/审。
输入：`data/math_extractions/`（mimo）、`research/mimo_spark_audit/*.audit.json`（spark）、`research/bailian_audit/*.bailian.json`（parsed）；对象=12 个有三源（或两源）的 basename（11×三源 + 1×两源 `zh_选修2-2_ch1_sec1.1`）。

## 三类总数

- 收录概念（≥2源）：**230**
- Solid 关系（≥2源）：**96**
- Hypothetical 关系（1源）：**456**
- 候选删/审（mimo 独有）：**22**

## 分文件表

| basename | 源数 | mimo概念 | spark概念 | bailian概念 | 收录概念≥2 | 候选删mimo独有 | mimo关系 | spark关系 | bailian关系 | Solid≥2 | Hypothetical=1 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| de_abitur_lk | 3 | 28 | 34 | 40 | 30 | 5 | 21 | 21 | 30 | 16 | 40 |
| de_forster_analysis1_ch5_sec5.1 | 3 | 11 | 15 | 31 | 14 | 0 | 8 | 12 | 30 | 8 | 34 |
| de_lambacher_5-8 | 3 | 15 | 30 | 40 | 28 | 2 | 10 | 20 | 30 | 11 | 36 |
| de_wahrscheinlichkeit_ch1-8 | 3 | 24 | 36 | 39 | 31 | 2 | 15 | 24 | 30 | 16 | 34 |
| en_ib_math_aa_sl | 3 | 18 | 38 | 40 | 27 | 1 | 14 | 20 | 29 | 14 | 32 |
| en_khan_academy_3-4 | 3 | 10 | 31 | 37 | 15 | 3 | 12 | 16 | 30 | 6 | 45 |
| en_khan_academy_6-8 | 3 | 37 | 39 | 39 | 33 | 8 | 22 | 18 | 30 | 13 | 39 |
| en_stewart_ch3_sec3.1 | 3 | 7 | 22 | 30 | 13 | 0 | 6 | 16 | 30 | 1 | 50 |
| zh_微分方程_ch3_sec3.2-3.4 | 3 | 6 | 22 | 29 | 9 | 0 | 5 | 16 | 28 | 3 | 43 |
| zh_微分方程_ch4_sec4.1-4.3 | 3 | 7 | 24 | 28 | 13 | 1 | 7 | 17 | 30 | 5 | 44 |
| zh_选修2-2_ch1_sec1.1 | 2 | 4 | 18 | 0 | 4 | 0 | 2 | 12 | 0 | 1 | 12 |
| zh_选修2-2_ch1_sec1.2 | 3 | 9 | 22 | 22 | 13 | 0 | 12 | 16 | 23 | 2 | 47 |

合计：收录概念 230 / Solid 96 / Hypothetical 456 / 候选删 22。

明细见 `research/consensus_20260914.json`（每文件含 accepted/mimo_only/solid/hypothetical 列表）。
