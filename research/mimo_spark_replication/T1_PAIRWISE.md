# T1 Pairwise Agreement (deterministic, zero API)

5 complete arms x 11 shared bases. Consensus != correctness.

| pair | bases | P | R | F1 | mean shared rels |
|---|---|---|---|---|---|
| muse-spark-1.3-contributor-free vs muse-spark-1.2-contributor-free | 11 | 0.5589 | 0.6053 | 0.5812 | 5.45 |
| muse-spark-1.3-contributor-free vs mm-minimax-m3 | 11 | 0.4781 | 0.3765 | 0.4212 | 2.09 |
| muse-spark-1.3-contributor-free vs sn-glm-5.2 | 11 | 0.4630 | 0.4741 | 0.4685 | 3.82 |
| muse-spark-1.3-contributor-free vs sn-sensenova-6.8-flash-lite | 11 | 0.4986 | 0.4584 | 0.4777 | 3.64 |
| muse-spark-1.2-contributor-free vs mm-minimax-m3 | 11 | 0.5979 | 0.4347 | 0.5034 | 3.64 |
| muse-spark-1.2-contributor-free vs sn-glm-5.2 | 11 | 0.5504 | 0.5203 | 0.5350 | 4.82 |
| muse-spark-1.2-contributor-free vs sn-sensenova-6.8-flash-lite | 11 | 0.6662 | 0.5655 | 0.6117 | 4.91 |
| mm-minimax-m3 vs sn-glm-5.2 | 11 | 0.4574 | 0.5947 | 0.5171 | 2.91 |
| mm-minimax-m3 vs sn-sensenova-6.8-flash-lite | 11 | 0.5135 | 0.5995 | 0.5532 | 5.45 |
| sn-glm-5.2 vs sn-sensenova-6.8-flash-lite | 11 | 0.6129 | 0.5504 | 0.5800 | 5.18 |

## Appendix: r4 (10-base intersection, wahrscheinlichkeit missing)

| pair | bases | P | R | F1 | mean shared rels |
|---|---|---|---|---|---|
| muse-spark-1.3-contributor-free vs r4-deepseek-v4.1-flash(10-base) | 10 | 0.5807 | 0.4202 | 0.4876 | 4.50 |
| muse-spark-1.2-contributor-free vs r4-deepseek-v4.1-flash(10-base) | 10 | 0.6855 | 0.4360 | 0.5330 | 6.60 |
| mm-minimax-m3 vs r4-deepseek-v4.1-flash(10-base) | 10 | 0.5068 | 0.4607 | 0.4826 | 2.90 |
| sn-glm-5.2 vs r4-deepseek-v4.1-flash(10-base) | 10 | 0.5479 | 0.3663 | 0.4391 | 3.40 |
| sn-sensenova-6.8-flash-lite vs r4-deepseek-v4.1-flash(10-base) | 10 | 0.5919 | 0.4596 | 0.5174 | 5.10 |
