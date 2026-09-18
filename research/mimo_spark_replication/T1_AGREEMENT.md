# T1 Agreement vs mimo baseline (baseline-relative; mimo unverified)

Matcher: normalized name equality OR alias cross-match. rel_agree: ordered endpoint pairs, type ignored.

| arm | files | micro-P | micro-R | mean rel_agree |
|---|---|---|---|---|
| muse-spark-1.3-contributor-free | 11 | 0.2712 | 0.3913 | 1.09 |
| muse-spark-1.2-contributor-free | 11 | 0.3160 | 0.4209 | 2.00 |
| mm-minimax-m3 | 11 | 0.2427 | 0.4447 | 0.82 |
| r4-deepseek-v4.1-flash | 10 | 0.2079 | 0.4243 | 0.90 |
| sn-sensenova-6.7-flash-lite | 0 | missing/partial | | |
| sn-deepseek-v4-flash | 2 | 0.2213 | 0.4355 | 0.00 |
| sn-glm-5.2 | 11 | 0.2525 | 0.3557 | 1.45 |
| sn-sensenova-6.8-flash-lite | 11 | 0.2846 | 0.4466 | 1.00 |
| sn-deepseek-v4-pro | 2 | 0.3214 | 0.5000 | 0.00 |
| sn-kimi-k3 | 0 | missing/partial | | |
| sn-sensenova-u1.5-fast | 0 | missing/partial | | |

## Per-file

| arm | base | P | R | inter | new/ref | rel_agree | gate |
|---|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor-free | de_abitur_lk | 0.342 | 0.346 | 28 | 82/81 | 1 | True |
| muse-spark-1.3-contributor-free | de_forster_analysis1_ch5_sec5.1 | 0.308 | 0.606 | 20 | 65/33 | 0 | True |
| muse-spark-1.3-contributor-free | de_lambacher_5-8 | 0.330 | 0.689 | 31 | 94/45 | 2 | True |
| muse-spark-1.3-contributor-free | de_wahrscheinlichkeit_ch1-8 | 0.430 | 0.529 | 37 | 86/70 | 4 | True |
| muse-spark-1.3-contributor-free | en_ib_math_aa_sl | 0.442 | 0.442 | 23 | 52/52 | 4 | True |
| muse-spark-1.3-contributor-free | en_khan_academy_3-4 | 0.028 | 0.069 | 2 | 72/29 | 0 | True |
| muse-spark-1.3-contributor-free | en_khan_academy_6-8 | 0.278 | 0.182 | 20 | 72/110 | 1 | True |
| muse-spark-1.3-contributor-free | en_stewart_ch3_sec3.1 | 0.234 | 0.524 | 11 | 47/21 | 0 | True |
| muse-spark-1.3-contributor-free | zh_微分方程_ch3_sec3.2-3.4 | 0.143 | 0.333 | 6 | 42/18 | 0 | True |
| muse-spark-1.3-contributor-free | zh_微分方程_ch4_sec4.1-4.3 | 0.125 | 0.429 | 9 | 72/21 | 0 | True |
| muse-spark-1.3-contributor-free | zh_选修2-2_ch1_sec1.2 | 0.239 | 0.423 | 11 | 46/26 | 0 | True |
| muse-spark-1.2-contributor-free | de_abitur_lk | 0.273 | 0.296 | 24 | 88/81 | 4 | True |
| muse-spark-1.2-contributor-free | de_forster_analysis1_ch5_sec5.1 | 0.483 | 0.879 | 29 | 60/33 | 1 | True |
| muse-spark-1.2-contributor-free | de_lambacher_5-8 | 0.395 | 0.667 | 30 | 76/45 | 3 | True |
| muse-spark-1.2-contributor-free | de_wahrscheinlichkeit_ch1-8 | 0.398 | 0.614 | 43 | 108/70 | 6 | True |
| muse-spark-1.2-contributor-free | en_ib_math_aa_sl | 0.404 | 0.442 | 23 | 57/52 | 0 | True |
| muse-spark-1.2-contributor-free | en_khan_academy_3-4 | 0.100 | 0.172 | 5 | 50/29 | 0 | True |
| muse-spark-1.2-contributor-free | en_khan_academy_6-8 | 0.482 | 0.245 | 27 | 56/110 | 7 | True |
| muse-spark-1.2-contributor-free | en_stewart_ch3_sec3.1 | 0.250 | 0.524 | 11 | 44/21 | 0 | True |
| muse-spark-1.2-contributor-free | zh_微分方程_ch3_sec3.2-3.4 | 0.156 | 0.389 | 7 | 45/18 | 0 | True |
| muse-spark-1.2-contributor-free | zh_微分方程_ch4_sec4.1-4.3 | 0.204 | 0.429 | 9 | 44/21 | 1 | True |
| muse-spark-1.2-contributor-free | zh_选修2-2_ch1_sec1.2 | 0.109 | 0.192 | 5 | 46/26 | 0 | True |
| mm-minimax-m3 | de_abitur_lk | 0.123 | 0.173 | 14 | 114/81 | 0 | False |
| mm-minimax-m3 | de_forster_analysis1_ch5_sec5.1 | 0.328 | 0.576 | 19 | 58/33 | 0 | True |
| mm-minimax-m3 | de_lambacher_5-8 | 0.270 | 0.756 | 34 | 126/45 | 0 | False |
| mm-minimax-m3 | de_wahrscheinlichkeit_ch1-8 | 0.424 | 0.714 | 50 | 118/70 | 5 | False |
| mm-minimax-m3 | en_ib_math_aa_sl | 0.174 | 0.308 | 16 | 92/52 | 2 | False |
| mm-minimax-m3 | en_khan_academy_3-4 | 0.071 | 0.207 | 6 | 85/29 | 0 | False |
| mm-minimax-m3 | en_khan_academy_6-8 | 0.424 | 0.409 | 45 | 106/110 | 2 | False |
| mm-minimax-m3 | en_stewart_ch3_sec3.1 | 0.197 | 0.571 | 12 | 61/21 | 0 | True |
| mm-minimax-m3 | zh_微分方程_ch3_sec3.2-3.4 | 0.136 | 0.444 | 8 | 59/18 | 0 | False |
| mm-minimax-m3 | zh_微分方程_ch4_sec4.1-4.3 | 0.143 | 0.476 | 10 | 70/21 | 0 | False |
| mm-minimax-m3 | zh_选修2-2_ch1_sec1.2 | 0.289 | 0.423 | 11 | 38/26 | 0 | True |
| r4-deepseek-v4.1-flash | de_abitur_lk | 0.271 | 0.395 | 32 | 118/81 | 0 | True |
| r4-deepseek-v4.1-flash | de_forster_analysis1_ch5_sec5.1 | 0.354 | 0.879 | 29 | 82/33 | 0 | True |
| r4-deepseek-v4.1-flash | de_lambacher_5-8 | 0.310 | 0.800 | 36 | 116/45 | 2 | True |
| r4-deepseek-v4.1-flash | en_ib_math_aa_sl | 0.217 | 0.500 | 26 | 120/52 | 3 | True |
| r4-deepseek-v4.1-flash | en_khan_academy_3-4 | 0.075 | 0.310 | 9 | 120/29 | 0 | True |
| r4-deepseek-v4.1-flash | en_khan_academy_6-8 | 0.244 | 0.200 | 22 | 90/110 | 3 | True |
| r4-deepseek-v4.1-flash | en_stewart_ch3_sec3.1 | 0.139 | 0.524 | 11 | 79/21 | 0 | True |
| r4-deepseek-v4.1-flash | zh_微分方程_ch3_sec3.2-3.4 | 0.092 | 0.333 | 6 | 65/18 | 0 | True |
| r4-deepseek-v4.1-flash | zh_微分方程_ch4_sec4.1-4.3 | 0.173 | 0.429 | 9 | 52/21 | 1 | True |
| r4-deepseek-v4.1-flash | zh_选修2-2_ch1_sec1.2 | 0.104 | 0.192 | 5 | 48/26 | 0 | True |
| sn-deepseek-v4-flash | de_forster_analysis1_ch5_sec5.1 | 0.424 | 0.758 | 25 | 59/33 | 0 | True |
| sn-deepseek-v4-flash | en_khan_academy_3-4 | 0.032 | 0.069 | 2 | 63/29 | 0 | False |
| sn-glm-5.2 | de_abitur_lk | 0.229 | 0.309 | 25 | 109/81 | 2 | True |
| sn-glm-5.2 | de_forster_analysis1_ch5_sec5.1 | 0.528 | 0.576 | 19 | 36/33 | 0 | True |
| sn-glm-5.2 | de_lambacher_5-8 | 0.278 | 0.778 | 35 | 126/45 | 4 | False |
| sn-glm-5.2 | de_wahrscheinlichkeit_ch1-8 | 0.407 | 0.686 | 48 | 118/70 | 5 | True |
| sn-glm-5.2 | en_ib_math_aa_sl | 0.088 | 0.115 | 6 | 68/52 | 0 | True |
| sn-glm-5.2 | en_khan_academy_3-4 | 0.043 | 0.069 | 2 | 46/29 | 0 | True |
| sn-glm-5.2 | en_khan_academy_6-8 | 0.267 | 0.145 | 16 | 60/110 | 5 | True |
| sn-glm-5.2 | en_stewart_ch3_sec3.1 | 0.207 | 0.286 | 6 | 29/21 | 0 | True |
| sn-glm-5.2 | zh_微分方程_ch3_sec3.2-3.4 | 0.263 | 0.556 | 10 | 38/18 | 0 | True |
| sn-glm-5.2 | zh_微分方程_ch4_sec4.1-4.3 | 0.170 | 0.381 | 8 | 47/21 | 0 | True |
| sn-glm-5.2 | zh_选修2-2_ch1_sec1.2 | 0.139 | 0.192 | 5 | 36/26 | 0 | True |
| sn-sensenova-6.8-flash-lite | de_abitur_lk | 0.273 | 0.333 | 27 | 99/81 | 1 | True |
| sn-sensenova-6.8-flash-lite | de_forster_analysis1_ch5_sec5.1 | 0.404 | 0.636 | 21 | 52/33 | 0 | True |
| sn-sensenova-6.8-flash-lite | de_lambacher_5-8 | 0.302 | 0.711 | 32 | 106/45 | 2 | True |
| sn-sensenova-6.8-flash-lite | de_wahrscheinlichkeit_ch1-8 | 0.417 | 0.614 | 43 | 103/70 | 7 | False |
| sn-sensenova-6.8-flash-lite | en_ib_math_aa_sl | 0.284 | 0.442 | 23 | 81/52 | 0 | False |
| sn-sensenova-6.8-flash-lite | en_khan_academy_3-4 | 0.066 | 0.138 | 4 | 61/29 | 0 | True |
| sn-sensenova-6.8-flash-lite | en_khan_academy_6-8 | 0.410 | 0.291 | 32 | 78/110 | 0 | True |
| sn-sensenova-6.8-flash-lite | en_stewart_ch3_sec3.1 | 0.260 | 0.619 | 13 | 50/21 | 0 | True |
| sn-sensenova-6.8-flash-lite | zh_微分方程_ch3_sec3.2-3.4 | 0.208 | 0.556 | 10 | 48/18 | 0 | True |
| sn-sensenova-6.8-flash-lite | zh_微分方程_ch4_sec4.1-4.3 | 0.167 | 0.476 | 10 | 60/21 | 0 | True |
| sn-sensenova-6.8-flash-lite | zh_选修2-2_ch1_sec1.2 | 0.196 | 0.423 | 11 | 56/26 | 1 | True |
| sn-deepseek-v4-pro | de_forster_analysis1_ch5_sec5.1 | 0.583 | 0.636 | 21 | 36/33 | 0 | True |
| sn-deepseek-v4-pro | en_stewart_ch3_sec3.1 | 0.125 | 0.286 | 6 | 48/21 | 0 | True |
