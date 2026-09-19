# T2 Matrix (deterministic, zero API)

CI = bootstrap 95% (B=1000, seed 20260918). en/de_cjk_frac = fraction of predicted names containing CJK (exploratory).
F1_n92 = A2-compliant primary (fails as 0 over all 92 gold IDs, D-S6); F1 = valid-only secondary.
**Nenner-Hinweis (Reaudit 2026-09-19, D-V11)**: die `social`-Spalte ist valid-only (Social-Subset, n≈72) — kein A2; echte A2-social-Werte s. `T2_MATRIX.json` (`social_f1_n92`) bzw. Reaudit-Datei. Fails fließen nur in `F1_n92` ein.

| model | n | P | R | F1 | 95%CI | F1_n92 | 95%CI_n92 | social | math | pred_n/gold_n |
|---|---|---|---|---|---|---|---|---|---|---|
| muse-spark-1.3-free | 92 | 0.1353 | 0.6386 | 0.1989 | [0.1599, 0.2432] | 0.1989 | [0.1599, 0.2432] | 0.1475 | 0.3839 | 11.7/2.2 |
| muse-spark-1.2-free | 92 | 0.0973 | 0.6125 | 0.1602 | [0.1274, 0.1947] | 0.1602 | [0.1274, 0.1947] | 0.1345 | 0.2528 | 13.2/2.2 |
| minimax-m3 | 92 | 0.1025 | 0.6371 | 0.1665 | [0.1359, 0.2005] | 0.1665 | [0.1359, 0.2005] | 0.1309 | 0.2947 | 13.4/2.2 |
| deepseek-v4.1-flash-r4 | 92 | 0.0799 | 0.6002 | 0.1319 | [0.1032, 0.1649] | 0.1319 | [0.1032, 0.1649] | 0.1116 | 0.2048 | 16.8/2.2 |
| sensenova-6.8-flash-lite | 76 | 0.0886 | 0.5985 | 0.1463 | [0.113, 0.1789] | 0.1208 | [0.0917, 0.1538] | 0.1288 | 0.1989 | 15.0/2.3 |
| glm-5.2-r4 | 91 | 0.1049 | 0.5526 | 0.1610 | [0.1232, 0.2019] | 0.1592 | [0.1242, 0.1982] | 0.1401 | 0.2349 | 12.8/2.2 |
| qwen-plus (Bailian hist) | 92 | 0.6418 | 0.7188 | 0.6659 | [0.5866, 0.7518] | 0.6659 | [0.5866, 0.7518] | 0.6497 | 0.7244 | 2.5/2.2 |
| qwen-max (Bailian hist) | 92 | 0.6421 | 0.7020 | 0.6610 | [0.5832, 0.746] | 0.6610 | [0.5832, 0.746] | 0.6483 | 0.7068 | 2.5/2.2 |

## Script-mismatch (exploratory)
| model | EN predicted CJK-frac | DE predicted CJK-frac |
|---|---|---|
| muse-spark-1.3-free | 0.4281 | 0.0000 |
| muse-spark-1.2-free | 0.5634 | 0.0691 |
| minimax-m3 | 0.2050 | 0.0130 |
| deepseek-v4.1-flash-r4 | 0.5204 | 0.0344 |
| sensenova-6.8-flash-lite | 0.0530 | 0.0000 |
| glm-5.2-r4 | 0.1966 | 0.0000 |
