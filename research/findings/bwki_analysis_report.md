# LinguaGraph — BWKI Analysis Report

Generated: 2026-06-17 18:02

---

## 1. Three-Way LDS Comparison

| Language Pair | Internet LDS | Model LDS | Human LDS |

|--------------|-------------|-----------|-----------|

| de-en | 0.8950 | — | — |

| zh-de | 0.8897 | — | — |

| zh-en | 0.7646 | — | — |


## 2. Cross-Source Correlation

| Source A | Source B | Pearson r | Spearman ρ |

|----------|----------|-----------|------------|

| Internet LDS | Model LDS | N/A (n=0 < 3) | N/A (n=0 < 3) |

| Internet LDS | Human LDS | N/A (n=0 < 3) | N/A (n=0 < 3) |

| Model LDS | Human LDS | N/A (n=0 < 3) | N/A (n=0 < 3) |


## 3. Data Volume by Source

| Source | Pairs with Data | Topics |

|--------|----------------|--------|

| Internet LDS | 3 | 3 |

| Model LDS | 0 | 0 |

| Human LDS | 0 | 0 |


## 4. Figure Data (for plotting)

```json

{
  "labels": [
    "de-en",
    "zh-de",
    "zh-en"
  ],
  "internet": [
    0.895,
    0.8897,
    0.7646
  ],
  "model": [
    null,
    null,
    null
  ],
  "human": [
    null,
    null,
    null
  ]
}

```


## 5. Interpretation


### Human LDS Prediction (from Internet LDS)

Based on Internet LDS mean = 0.8498, we predict Human LDS in range:

- Expected: 0.8498 ± 0.10

- Range: [0.7498, 0.9498]
