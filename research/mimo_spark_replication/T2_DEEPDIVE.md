# T2 Deep-Dive (deterministic, zero API — exploratory unless noted)

Seed/B = 20260918/1000 (same as T2_MATRIX). A2 rule (invalid=0/92).
Cell n = A2 denominator (incl. fails); n_valid per cell in JSON.
Primary paired comparisons pre-declared; all other pairs exploratory (Bonferroni over 15 pairs: α≈0.003).

## 1. Cell CIs (language x domain)

| arm | zh_math n/mean/CI | zh_soc | de_math | de_soc | en_math | en_soc |
|---|---|---|---|---|---|---|
| muse-spark-1.3-free | 7 0.564 [0.3819, 0.7646] | 29 0.207 [0.1445, 0.2797] | 7 0.357 [0.2286, 0.4429] | 22 0.181 [0.1297, 0.2331] | 6 0.206 [0.0555, 0.3833] | 21 0.031 [0.0, 0.075] |
| muse-spark-1.2-free | 7 0.420 [0.3347, 0.5143] | 29 0.180 [0.1352, 0.2332] | 7 0.262 [0.1627, 0.3565] | 22 0.171 [0.1161, 0.233] | 6 0.048 [0.0, 0.1429] | 21 0.033 [0.0, 0.074] |
| minimax-m3 | 7 0.471 [0.3871, 0.5739] | 29 0.164 [0.1241, 0.2109] | 7 0.248 [0.1595, 0.3265] | 22 0.172 [0.1155, 0.2303] | 6 0.144 [0.0, 0.2974] | 21 0.042 [0.006, 0.0811] |
| deepseek-v4.1-flash-r4 | 7 0.406 [0.2737, 0.5846] | 29 0.157 [0.1172, 0.202] | 7 0.179 [0.1102, 0.2456] | 22 0.153 [0.1067, 0.208] | 6 0.000 [0.0, 0.0] | 21 0.006 [0.0, 0.0179] |
| sensenova-6.8-flash-lite | 7 0.357 [0.2863, 0.441] | 29 0.163 [0.108, 0.2278] | 7 0.182 [0.1116, 0.2542] | 22 0.118 [0.0746, 0.1635] | 6 0.000 [0.0, 0.0] | 21 0.000 [0.0, 0.0] |
| glm-5.2-r4 | 7 0.420 [0.332, 0.5417] | 29 0.216 [0.1416, 0.2995] | 7 0.252 [0.1576, 0.3274] | 22 0.167 [0.107, 0.2303] | 6 0.000 [0.0, 0.0] | 21 0.000 [0.0, 0.0] |
| qwen-plus (Bailian hist) | 7 0.973 [0.9402, 1.0] | 29 0.712 [0.5621, 0.8404] | 7 0.499 [0.3197, 0.6728] | 22 0.581 [0.3964, 0.749] | 6 0.697 [0.4111, 0.8968] | 21 0.635 [0.4412, 0.8102] |
| qwen-max (Bailian hist) | 7 0.916 [0.8209, 0.9841] | 29 0.721 [0.5717, 0.846] | 7 0.513 [0.3333, 0.6864] | 22 0.586 [0.4013, 0.7522] | 6 0.689 [0.3889, 0.9111] | 21 0.613 [0.4127, 0.7937] |

## 2. gold_n stratification (1 vs >=2)

| arm | n1/mean/CI | n2/mean/CI |
|---|---|---|
| muse-spark-1.3-free | 37 0.126 [0.0858, 0.1874] | 55 0.248 [0.1901, 0.3105] |
| muse-spark-1.2-free | 37 0.087 [0.0678, 0.1059] | 55 0.209 [0.1608, 0.2584] |
| minimax-m3 | 37 0.093 [0.0756, 0.1096] | 55 0.216 [0.1632, 0.265] |
| deepseek-v4.1-flash-r4 | 37 0.081 [0.0634, 0.0957] | 55 0.166 [0.1213, 0.216] |
| sensenova-6.8-flash-lite | 37 0.062 [0.0416, 0.0808] | 55 0.161 [0.1168, 0.2075] |
| glm-5.2-r4 | 37 0.116 [0.0689, 0.1738] | 55 0.189 [0.1404, 0.2395] |
| qwen-plus (Bailian hist) | 37 0.838 [0.7027, 0.9459] | 55 0.550 [0.4505, 0.6457] |
| qwen-max (Bailian hist) | 37 0.838 [0.7027, 0.9459] | 55 0.542 [0.443, 0.6329] |

## 3. Paired dF1 (primary first)

| pair | primary | mean_d | 95%CI | 0 in CI? |
|---|---|---|---|---|
| muse-spark-1.3-free vs qwen-plus (Bailian hist) | True | -0.4670 | [-0.5582, -0.3836] | False |
| muse-spark-1.3-free vs muse-spark-1.2-free | True | 0.0387 | [0.0086, 0.073] | False |
| minimax-m3 vs glm-5.2-r4 | True | 0.0073 | [-0.0271, 0.0359] | True |
| muse-spark-1.3-free vs minimax-m3 | False | 0.0324 | [0.0011, 0.0673] | False |
| muse-spark-1.3-free vs deepseek-v4.1-flash-r4 | False | 0.0671 | [0.041, 0.0987] | False |
| muse-spark-1.3-free vs sensenova-6.8-flash-lite | False | 0.0781 | [0.0463, 0.1155] | False |
| muse-spark-1.3-free vs glm-5.2-r4 | False | 0.0397 | [0.0001, 0.0793] | False |
| muse-spark-1.2-free vs minimax-m3 | False | -0.0063 | [-0.0265, 0.0113] | True |
| muse-spark-1.2-free vs deepseek-v4.1-flash-r4 | False | 0.0283 | [0.0097, 0.0465] | False |
| muse-spark-1.2-free vs sensenova-6.8-flash-lite | False | 0.0393 | [0.0213, 0.0581] | False |
| muse-spark-1.2-free vs glm-5.2-r4 | False | 0.0010 | [-0.0303, 0.0243] | True |
| minimax-m3 vs deepseek-v4.1-flash-r4 | False | 0.0347 | [0.0131, 0.0572] | False |
| minimax-m3 vs sensenova-6.8-flash-lite | False | 0.0457 | [0.0224, 0.0701] | False |
| deepseek-v4.1-flash-r4 vs sensenova-6.8-flash-lite | False | 0.0110 | [-0.0079, 0.0298] | True |
| deepseek-v4.1-flash-r4 vs glm-5.2-r4 | False | -0.0273 | [-0.0544, -0.005] | False |
| sensenova-6.8-flash-lite vs glm-5.2-r4 | False | -0.0384 | [-0.0684, -0.0163] | False |

## 4. pred_n-F1 mechanism

| arm | Pearson r | mean pred_n |
|---|---|---|
| muse-spark-1.3-free | -0.3612 | 11.7 |
| muse-spark-1.2-free | -0.3752 | 13.2 |
| minimax-m3 | -0.4321 | 13.4 |
| deepseek-v4.1-flash-r4 | -0.3821 | 16.8 |
| sensenova-6.8-flash-lite | 0.2308 | 12.4 |
| glm-5.2-r4 | -0.3126 | 12.7 |
| qwen-plus (Bailian hist) | -0.1611 | 2.5 |
| qwen-max (Bailian hist) | -0.1598 | 2.5 |
| pooled-new6 | -0.2113 | — |

Binned (new6, bins n>=5): pred=0: n=17 F1=0.000; pred=1: n=5 F1=0.400; pred=3: n=6 F1=0.367; pred=10: n=49 F1=0.225; pred=11: n=7 F1=0.244; pred=12: n=146 F1=0.206; pred=13: n=16 F1=0.147; pred=14: n=43 F1=0.125; pred=15: n=113 F1=0.124; pred=16: n=33 F1=0.138; pred=17: n=16 F1=0.071; pred=18: n=37 F1=0.106; pred=20: n=44 F1=0.065

## 5. Difficulty (negative result — DO NOT USE)

| arm | n(med+hard) | mean |
|---|---|---|
| muse-spark-1.3-free | 9 | 0.302 |
| muse-spark-1.2-free | 9 | 0.261 |
| minimax-m3 | 9 | 0.259 |
| deepseek-v4.1-flash-r4 | 9 | 0.177 |
| sensenova-6.8-flash-lite | 9 | 0.206 |
| glm-5.2-r4 | 9 | 0.256 |
| qwen-plus (Bailian hist) | 9 | 0.625 |
| qwen-max (Bailian hist) | 9 | 0.633 |

Power note (normal approx, ΔF1=0.1, 80% power): paired same-item design needs n≈32–71 (σ_diff 0.20–0.30); existing per-language cells n=6–7 detect only Δ≈0.4+; n=72/92 pools approach Δ≈0.1–0.16.
