# Top Drift Concepts Ranking
Generated from 15 cross-language analysis records
---
## Overall Ranking (by avg LDS)
| Rank | Concept | Avg LDS | Avg Similarity | Concept Shift | Drift Group |
|------|---------|---------|----------------|---------------|-------------|
| 1 | **success** | 0.9722 | 0.0278 | 5 | HIGH |
| 2 | **responsibility** | 0.8305 | 0.1695 | 7 | MEDIUM |
| 3 | **justice** | 0.8222 | 0.1778 | 9 | MEDIUM |
| 4 | **freedom** | 0.8119 | 0.1881 | 11 | MEDIUM |

## Per-Pair Breakdown

### success (avg LDS=0.9722)
| Pair | LDS | Similarity | Shared | Unique Observations |
|------|-----|------------|--------|---------------------|
| de-en | 1.0000 | 0.0000 | 1 | EN: education, individual |
| zh-de | 1.0000 | 0.0000 | 1 | ZH: 经济, 教育, 家庭, 历史 |
| zh-en | 0.9167 | 0.0833 | 3 | ZH: 经济, 家庭, 历史, 进步 |

### responsibility (avg LDS=0.8305)
| Pair | LDS | Similarity | Shared | Unique Observations |
|------|-----|------------|--------|---------------------|
| de-en | 0.8378 | 0.1622 | 4 | DE: Entscheidung, Bildung, Geschichte, Recht; EN: free will, law |
| zh-de | 0.8810 | 0.1190 | 5 | ZH: 平等, 家庭, 自由意志, 个体; DE: Entscheidung, Bildung, Geschichte |
| zh-en | 0.7727 | 0.2273 | 6 | ZH: 平等, 家庭, 个体, 公正 |

### justice (avg LDS=0.8222)
| Pair | LDS | Similarity | Shared | Unique Observations |
|------|-----|------------|--------|---------------------|
| de-en | 0.8765 | 0.1235 | 5 | DE: Fortschritt, Vernunft, Sicherheit, Erfolg; EN: economy, history, individual, law |
| zh-de | 0.8913 | 0.1087 | 5 | ZH: 统治, 经济, 教育, 家庭; DE: Fortschritt, Vernunft, Religion, Erfolg |
| zh-en | 0.6989 | 0.3011 | 8 | ZH: 统治, 教育, 家庭, 安全; EN: history, power, religion |

### freedom (avg LDS=0.8119)
| Pair | LDS | Similarity | Shared | Unique Observations |
|------|-----|------------|--------|---------------------|
| de-en | 0.8718 | 0.1282 | 6 | DE: reason, security, revolution, economy; EN: domination, free_will, democracy, power |
| de-en | 0.8889 | 0.1111 | 5 | DE: Wirtschaft, Gleichheit, Vernunft, Revolution; EN: choice, democracy, domination, free will |
| zh-de | 0.8209 | 0.1791 | 9 | ZH: individual, free_will, domination, liberation; DE: reason, security, equality |
| zh-de | 0.8551 | 0.1449 | 8 | ZH: 选择, 民主, 统治, 家庭; DE: Gleichheit, Vernunft, Sicherheit |
| zh-en | 0.6140 | 0.3860 | 12 | ZH: individual, revolution, family, society |
| zh-en | 0.8205 | 0.1795 | 11 | ZH: 经济, 家庭, 个体, 法律 |

## Drift Groups for Questionnaire Design

### HIGH DRIFT (LDS >= 0.85)
- **success** (LDS=0.9722)

### MEDIUM DRIFT (LDS 0.70-0.85)
- **responsibility** (LDS=0.8305)
- **justice** (LDS=0.8222)
- **freedom** (LDS=0.8119)

### LOW DRIFT (LDS < 0.70)
*(No concepts in this category yet)*

## Questionnaire Recommendations
### Include (High Drift — likely to show cognitive differences):
- **success** — LDS=0.9722
  - de-en: EN unique: ['education', 'individual']
  - zh-de: ZH unique: ['经济', '教育', '家庭']
  - zh-en: ZH unique: ['经济', '家庭', '历史']

## Remaining Concepts (Reserve for future expansion)
Priority for next batch: Democracy, Equality, Family, Education, Honor, Duty, Happiness, Independence, Authority, Competition
Selection strategy: pick those expected to have HIGH drift based on linguistic/cultural theory.
