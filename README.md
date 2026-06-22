# 🧠 LinguaGraph — Cross-Lingual Knowledge Structure Analysis Framework

> **BWKI 2026 — Bundeswettbewerb Künstliche Intelligenz**

---

## 📋 Research Question / Forschungsfrage / 研究问题

> **EN:** How do different languages and educational systems organize the same knowledge?
>
> **DE:** Wie organisieren verschiedene Sprachen und Bildungssysteme dasselbe Wissen?
>
> **ZH:** 不同语言和教育体系是如何组织同一知识的？

LinguaGraph is a quantitative framework that analyzes how **mathematics, physics, and chemistry** knowledge is organized across **Chinese, German, and English** textbooks, and how textbook knowledge aligns with **official curriculum standards** (Germany, UK, US, China). It introduces four graph-based metrics to make invisible structural patterns measurable.

---

## 🏆 Key Findings

| Finding | Description | Evidence |
|---------|-------------|----------|
| **F1** | CDS peaks at **Middle school** (0.271), not Elementary | Non-monotonic density — 3.7× drop to High |
| **F2** | Density hub at middle school, then curriculum diversifies | 574 concepts, 4 education levels, 3 languages independently |
| **F3** | HDS ≤ **8** (mean 0.40); 83% of math concepts are roots | Mathematics is a shallow web, not a deep tree |
| **F4** | **ZH–DE** structural divergence highest (LDS=0.907) | ZH–EN lowest (0.802) — counterintuitive |
| **F5** | Cross-language divergence is **topic-dependent** | ~0.2 variation within language pairs |
| **F6** | **Physics** CDS peaks at **Elementary** (0.222), Math at Middle | Both follow "integrate-early, diverge-late" |
| **F7** | Physics has deeper prerequisite chains (HDS mean 0.85 vs 0.40) | Physics knowledge is more cumulative |
| **F8** | **Chemistry** CDS also peaks at Middle (0.042), 6.5× lower than Math | STEM density pattern is universal |
| **F9** | **Coverage Score** varies dramatically: NRW 34%, UK 82%, US 76% | Educational system differences in curriculum-textbook alignment |
| **F10** | Coverage trajectories reveal **exam-driven** vs **specialization-driven** design | UK increases toward GCSE; NRW drops in Oberstufe |

---

## 📐 Metrics

| Metric | Formula | What It Measures |
|--------|---------|-----------------|
| **CDS** | 2\|E\|/(\|V\|·(\|V\|−1)) | Knowledge density — how interconnected concepts are at each education level |
| **HDS** | BFS prerequisite chain depth | Knowledge depth — how many prerequisite layers exist |
| **LDS** | 1 − mean(GED_sim, Jaccard_node, Jaccard_edge) | Cross-language structural divergence |
| **CS** | \|V_textbook ∩ V_curriculum\| / \|V_curriculum\| | Textbook-curriculum alignment |

---

## 🗂️ Dataset

| Subject | Concepts | Relations | Textbooks | Languages |
|---------|:--------:|:---------:|:---------:|:---------:|
| **Mathematics** | 574 | 3,538 | 68 | ZH/EN/DE |
| **Physics** | 366 | 383 | 94 editions | ZH/EN/DE |
| **Chemistry** | 220 | 215 | 18 editions | ZH/EN/DE |
| **NRW Curriculum** | 805 (M+P+C) | — | — | DE |
| **UK Curriculum** | 186 | — | — | EN |
| **US NGSS** | 27 | — | — | EN |
| **Gold Labels** | 92 (ZH=36, DE=29, EN=27) | — | — | ZH/EN/DE |

**Total: 1,160+ concepts, 4,100+ relations, 3 languages, 4 educational systems**

---

## 🧪 Extraction Quality

Validated on 92 gold-standard human annotations:

| Domain | Language | F1 | Precision | Recall | n |
|--------|----------|:--:|:---------:|:------:|:-:|
| **Social** | ZH | **0.974** | 1.000 | 0.950 | 29 |
| **Social** | DE | **0.949** | 0.959 | 0.941 | 22 |
| **Social** | EN | **0.882** | 0.914 | 0.857 | 21 |
| **Math** | ZH | 0.857 | 1.000 | 0.798 | 7 |
| **Math** | DE | 0.506 | 0.536 | 0.512 | 7 |
| **Math** | EN | 0.711 | 0.722 | 0.722 | 6 |
| **Overall** | All | **0.939** | 0.957 | 0.926 | **92** |

20 models benchmarked; qwen-plus selected as production model (social domain F1≥0.88 across all languages).

---

## 🔬 Methodology

<p align="center">
  <code>Textbook PDF → LLM Concept Extraction → Knowledge Graph → Metric Computation → Cross-Lingual Comparison</code>
</p>

1. **Data Collection**: 68+ multilingual textbooks spanning elementary to university level
2. **LLM Extraction**: Qwen-plus extracts concepts and prerequisite relations from textbook text
3. **Graph Construction**: Directed knowledge graphs with typed edges (prerequisite, part_of, cause_effect, represents, inverse_of)
4. **Concept Alignment**: Cross-lingual concept mapping (174 entries) for fair comparison across ZH/EN/DE
5. **Metric Computation**: CDS, HDS, LDS, Coverage Score per education level and language
6. **Curriculum Analysis**: Coverage Score comparing textbook graphs to official curriculum standards

---

## 📁 Repository Structure

```
├── scripts/              # Analysis pipelines (Python)
│   ├── batch_process_responses.py  # Batch LLM extraction
│   ├── evaluate_gold.py            # Gold label evaluation
│   ├── compute_lds_from_db.py      # LDS from pre-computed extractions
│   ├── simulate_baseline.py        # 300-response simulation baseline
│   └── expand_gold_dataset.py      # Gold dataset 20→100 expansion
├── docs/
│   ├── paper/            # Full research paper (ZH/DE sections)
│   │   ├── 00_three_conclusions.md
│   │   ├── 02_methodology.md
│   │   ├── 04_discussion.md
│   │   └── ...
│   └── review/           # Quality audits and assessments
├── config/
│   ├── expert_graphs/    # Knowledge graphs (JSON)
│   └── concept_mapping.json    # Cross-lingual alignment (174 entries)
├── cognitive-space/      # 3D visualization (Three.js)
├── research/
│   └── findings/         # Benchmark results, analysis outputs
└── linguaGraph.db        # SQLite database (local only — gitignored)
```

---

## 🚀 Quick Start

```bash
# 1. Set up environment
export BAILIAN_API_KEY="your-api-key"

# 2. Run extraction on gold labels
python scripts/batch_process_responses.py --gold-only

# 3. Evaluate extraction quality
python scripts/evaluate_gold.py

# 4. Generate 300-response simulation baseline
python scripts/simulate_baseline.py --mock

# 5. Compute LDS from existing extractions
python scripts/compute_lds_from_db.py

# 6. Test different models
python scripts/batch_process_responses.py --model qwen-plus --gold-only
python scripts/batch_process_responses.py --model glm-4.6 --gold-only
```

---

## 📄 Paper Status

| Section | Status |
|---------|:------:|
| Abstract + Introduction | ✅ Complete |
| Related Work | ✅ Complete (19+ references) |
| Methodology | ✅ Complete (incl. 20-model benchmark) |
| Results (F1–F10) | ✅ Complete |
| Discussion | ✅ Complete (incl. 3 competing explanations) |
| Conclusion | ✅ Complete |
| Error Analysis | ✅ Complete |
| **Creative Submission (BWKI)** | ✅ **Submitted (June 28)** |

---

## 📊 Model Benchmark

20 models tested on 20 gold labels (math domain) + 92 gold labels (social domain):

| Model | Domain | ZH F1 | DE F1 | EN F1 | Speed |
|-------|--------|:-----:|:-----:|:-----:|:-----:|
| qwen-plus | Social | **0.974** | **0.949** | **0.882** | 2-3s |
| qwen-plus-latest | Social | 0.952 | 0.367 | 0.745 | 2-3s |
| qwen3.7-max | Math | 0.980 | 0.551 | 0.778 | 2-3s |
| glm-4.6 | Math | 0.951 | 0.595 | 0.689 | 10-20s |
| qwen-turbo | Math | 0.714 | 0.448 | 0.810 | 1s |

---

## 📚 Selected References

- Ausubel, D. P. (1963). *The psychology of meaningful verbal learning.*
- Novak, J. D. & Cañas, A. J. (2008). *The theory underlying concept maps.*
- Schmidt, W. H. et al. (2001). *Why schools matter: A cross-national comparison of curriculum and learning.*
- Liang, L. L. & Heckmann, K. (2013). *Comparing German and Chinese mathematics textbooks.*
- Boroditsky, L. (2001). *Does language shape thought?* Cognitive Psychology.

---

## 📜 License

This project is developed for **BWKI 2026** (Bundeswettbewerb Künstliche Intelligenz). All rights reserved.

---

## 🔗 Links

- [BWKI 2026 — Official Website](https://www.bw-ki.de/)
- [GitHub Repository](https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph)
- [CognitiveSpace 3D Visualization](cognitive-space/web/index.html)
