# LinguaGraph — Limitation Audit (Formal Documentation)
## 2026-06-25 | Version 1.0

---

## 1. Data Limitations

### 1.1 Textbook Corpus Coverage

| Limitation | Impact | Severity | Mitigation |
|-----------|--------|----------|------------|
| Mathematics corpus (574 concepts, 68 textbooks) is comprehensive; physics (366) and chemistry (220) are smaller | Cross-disciplinary comparisons may be affected by corpus size differences | **Medium** | All metrics normalize by graph size (CDS density, HDS proportions) |
| ZH textbooks (45) outnumber EN (20) and DE (10) by a wide margin | ZH concepts may be over-represented in merged graphs | **Low** | Per-language subgraphs are compared separately; merged graph is only used for global statistics |
| Textbook selection biases: ZH uses standardized Renjiao series; DE uses Gymnasium-track only | Results may not generalize to other textbook traditions within each language | **Medium** | Acknowledged in Discussion §4.8; future work should sample multiple publishers per language |

### 1.2 Human Validation Data

| Limitation | Impact | Severity | Mitigation |
|-----------|--------|----------|------------|
| N=8 participants (4 ZH, 2 DE, 2 EN) | Statistical power is limited; population-level conclusions cannot be drawn | **High** | Explicitly noted in Discussion §4.8; results presented as validation of direction, not effect size |
| Within-subject comparisons limited to DE-EN only | ZH cross-language comparisons must rely on between-subject design, confounding individual differences | **High** | Noted in Limitations; future work should recruit ZH bilingual participants |
| 11/101 responses not extracted (89.1% coverage) | Missing data may bias topic-level LDS estimates for certain participants | **Low** | Coverage is high; missing extractions affect <11% of responses |
| Recruitment via convenience sampling (WeChat, university) | Sample may not be representative of general population | **Medium** | Typical for pilot studies; acknowledged in limitations |

### 1.3 Simulation Baseline Data

| Limitation | Impact | Severity | Mitigation |
|-----------|--------|----------|------------|
| Mock extraction uses keyword matching, not LLM | Simulation LDS reflects keyword distributions, not cognitive processes | **Medium** | Baseline serves as lower bound; real human LDS exceeding it provides conservative validation |
| 20 responses per condition may not saturate concept space | Simulation LDS estimates may be noisy | **Low** | 300 total responses provide stable aggregate statistics |

---

## 2. Methodology Limitations

### 2.1 Extraction Quality

| Limitation | Impact | Severity | Mitigation |
|-----------|--------|----------|------------|
| Extraction quality varies by domain: social concepts (F1=0.939) >> math DE (F1=0.506) | Cross-domain LDS comparisons may be affected by extraction quality differences | **Medium** | Social concept LDS uses validated extraction; math LDS is caveated in paper |
| Human extraction produced concepts only (no relations) | Full 3-component LDS cannot be applied; results driven by Node Jaccard | **Medium** | Acknowledged in Discussion; metric is conservative (no edge contribution) |
| Relations inferred via transitive closure (~3000 added) | May introduce artificial edges that inflate CDS | **Low** | Transitive inference is deterministic and consistent across languages |

### 2.2 LDS Formula

| Limitation | Impact | Severity | Mitigation |
|-----------|--------|----------|------------|
| 3-component LDS (GED + NodeJac + EdgeJac) averages heterogeneous quantities | GED similarity depends on graph size; EdgeJac penalizes empty edge sets differently | **Medium** | All three components are reported separately; LDS interpreted as ordinal, not absolute |
| No theoretical upper-bound calibration | LDS=0.907 is "high" but the scale is relative | **Low** | Simulation baseline (0.647) provides reference point; human LDS > simulated LDS validates metric |
| Edge Jaccard = 0 for human data (no edges) | Pulls LDS artifactually high for edge-free graphs | **Medium** | Noted explicitly; future work should extract relations for human responses |

### 2.3 Coverage Score (CS)

| Limitation | Impact | Severity | Mitigation |
|-----------|--------|----------|------------|
| Keyword-based matching for curriculum alignment | May miss semantically equivalent but lexically different concepts | **Medium** | Future version should use embedding-based matching |
| NCSS (US) only has 27 concepts vs NRW's 299 | Coverage scores not directly comparable across systems of different granularity | **High** | Comparison focuses on trajectories and patterns, not absolute values |
| China CS=8% may reflect alignment methodology, not genuine gap | ZH curriculum matched from English-translated documents | **High** | Caveated in Discussion; labeled as "methodological" finding |

---

## 3. Design Limitations

| Limitation | Impact | Severity | Mitigation |
|-----------|--------|----------|------------|
| No causality: correlational design cannot separate language effects from culture/education | Results document structural differences but cannot explain their origin | **High** | Three competing explanations presented in Discussion §4.6; causal claims avoided |
| Social concepts only for human validation | Cognitive patterns may differ for technical/mathematical concepts | **Medium** | Textbook analysis provides math/physics/chemistry validation; noted for future work |
| No control topic (e.g., "food", "weather") in human data | Cannot assess whether LDS is artificially inflated by topic salience | **Medium** | Recommendation for future data collection |
| No retest reliability | LDS stability over time is unknown | **Medium** | Future work should include 2-week retest for 5+ participants |

---

## 4. Generalizability

| Limitation | Impact | Severity | Mitigation |
|-----------|--------|----------|------------|
| STEM only (mathematics, physics, chemistry) | May not generalize to humanities, social sciences, or professional domains | **Medium** | Noted as priority for future work |
| Three languages only (ZH, EN, DE) | May not generalize to other language families (e.g., Arabic, Romance, Slavic) | **Medium** | Framework is language-agnostic; extension is implementable |
| K-12 + university textbook focus | Professional or informal knowledge organizations may differ | **Low** | Consistent with project scope (formal education analysis) |
| DE textbooks limited to Gymnasium track | Excludes Hauptschule, Realschule, Gesamtschule within Germany | **Medium** | German educational diversity is underrepresented |

---

## 5. Ethical & Compliance

| Limitation | Impact | Severity | Mitigation |
|-----------|--------|----------|------------|
| Human participants N=8 is below typical IRB thresholds | Cannot make population claims | **Medium** | Framed as pilot validation, not epidemiological study |
| Consent obtained but no formal ethics board review (BWKI context) | May not meet formal publication standards at some venues | **Medium** | Standard for school-level research; higher standard for academic publication |
| LLM extraction cost: 400+ API calls for model benchmark | Financial cost is nontrivial for reproducibility | **Low** | Open-source models (qwen3-8B) tested as local alternative |

---

## 6. Key Strengths (Counterbalance)

| Strength | Evidence |
|----------|----------|
| Cross-validation across three independent data sources | Wikipedia LDS, Human LDS, and simulation baseline all show consistent rank order |
| Reproducible pipeline | All extraction, graph construction, and analysis scripts are version-controlled and deterministic |
| Multi-metric framework | Four complementary metrics (CDS, HDS, LDS, CS) provide converging evidence |
| Open data and code | Full dataset (929 JSON, 108 TXT, 23 PDF) and code (58 Python scripts) publicly available |
| Computational baseline validation | Human LDS > Simulation LDS (p=0.05), confirming metric validity |

---

## 7. Action Items (Priority Order)

| Priority | Action | Target | Owner |
|----------|--------|--------|-------|
| P1 | Collect human data from 20+ additional participants | Complete submission (Sep 21) | Researcher |
| P2 | Add control topics (food, weather) to future questionnaires | Ongoing | Researcher |
| P3 | Extract relations (not just concepts) for human responses | Future work | Qwen-plus prompt engineering |
| P4 | Extend to additional languages (e.g., Arabic, Japanese) | Future work | N/A |
| P5 | Implement embedding-based Coverage Score | Future work | N/A |
