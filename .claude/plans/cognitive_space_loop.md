# CognitiveSpace Extraction Loop — Runbook

## Pattern: Sequential (safe mode)
## Stop condition: All 6 new textbook chapters extracted + pipeline validated
## Status: ✅ COMPLETE

## Loop Results

| Iter | Textbook File | Language | Concepts | Relations |
|------|--------------|----------|----------|-----------|
| 1 | zh_选修2-2_ch1_sec1.2.txt | zh | 9 | 6 |
| 2 | zh_选修2-2_ch1_sec1.3.txt | zh | 5 | 6 |
| 3 | zh_选修2-2_ch2_sec2.1.txt | zh | 11 | 9 |
| 4 | en_stewart_ch3_sec3.1.txt | en | 7 | 6 |
| 5 | en_stewart_ch3_sec3.2.txt | en | 6 | 7 |
| 6 | de_forster_analysis1_ch5_sec5.1.txt | de | 11 | 8 |

## Final Pipeline Output
- **9 extraction files** → 46 unique concepts, 41 unique relations
- **Calculus expert graph**: 21 concepts, 24 relations (all with real data)
- **Visualization**: 48 nodes, 24 links
- **Structural conflicts**: 0
- **Tests**: 45/45 pass

## Quality Gates
- [x] Each JSON has source_textbook, extracted_concepts, extracted_relations
- [x] Concepts use original language names
- [x] All relations have evidence field
- [x] Pipeline runs clean: 0 structural conflicts
- [x] Tests still pass after pipeline run
