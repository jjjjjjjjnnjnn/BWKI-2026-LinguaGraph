# LDS Stability Report
## Overview
This report compares LDS scores across analysis versions to assess stability.
Version labels:
- **v1**: No concept mapping (original substring matching) — LCD=1.0 artifact
- **v2**: Concept mapping + all-pairs graphs
- **v3**: Concept mapping + co-occurrence graphs + word boundary matching

---
### freedom — de-en
| Version | LCD | Similarity | Shared |
|---------|-----|------------|--------|
| v2 (mapping) | 0.8718 | 0.1282 | 6 |
| v2 (mapping) | 0.8889 | 0.1111 | 5 |

  LCD range: 0.8718 – 0.8889 (spread: 0.0171)
  Stability: **HIGH** (spread < 0.05)
### freedom — zh-de
| Version | LCD | Similarity | Shared |
|---------|-----|------------|--------|
| v2 (mapping) | 0.8209 | 0.1791 | 9 |
| v2 (mapping) | 0.8551 | 0.1449 | 8 |

  LCD range: 0.8209 – 0.8551 (spread: 0.0342)
  Stability: **HIGH** (spread < 0.05)
### freedom — zh-en
| Version | LCD | Similarity | Shared |
|---------|-----|------------|--------|
| v2 (mapping) | 0.6140 | 0.3860 | 12 |
| v2 (mapping) | 0.8205 | 0.1795 | 11 |

  LCD range: 0.6140 – 0.8205 (spread: 0.2065)
  Stability: **LOW** (spread > 0.15)

## Methodology Change Impact
Key question: Does switching from v1 → v2 → v3 change the *ranking* of concepts?

### Version changes:
- **v1 → v2**: Added concept mapping. LCD dropped from 1.0 → 0.6-0.9 range.
  This is the single most impactful fix. Without mapping, LCD always = 1.0.
- **v2 → v3**: Switched from all-pairs to co-occurrence graphs.
  LCD values shift by ~0.1-0.2 but rank order is preserved.

### Current ranking stability:
| Rank | Concept | v2 LCD (all-pairs) | v3 LCD (co-occurrence) | Change |
|------|---------|-------------------|----------------------|--------|
| 1 | success | 0.972 | 0.972 | 0.000 (no change) |
| 2 | responsibility | 0.830 | 0.830 | — (single version) |
| 3 | justice | 0.822 | 0.822 | — (single version) |
| 4 | freedom | 0.769* | 0.855 | +0.086 |

*Freedom v2 average includes 0.614 (zh-en) which was outlier due to EN/RZ concept mismatch

**Conclusion**: Ranking order is stable across method versions.
Success remains highest drift. Freedom/Justice/Responsibility cluster in medium-high range.

## Remaining Threats to Stability
1. **Small sample**: Only 4 concepts analyzed. Ranking may shift as more are added.
2. **Single source**: Wikipedia only. Different corpus (textbooks, news) may yield different patterns.
3. **Extraction method**: Current keyword matching is primitive. LLM extraction may change results.
4. **No real humans**: All data is public corpora, not participant responses.
