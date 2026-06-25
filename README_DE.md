<p align="center">
  <a href="README.md">🇬🇧 English</a> · <a href="README_DE.md">🇩🇪 Deutsch</a> · <a href="README_ZH.md">🇨🇳 中文</a>
</p>

---

<p align="center">
  <img src="cognitive-space/web/screenshot.png" alt="LinguaGraph — Cross-Lingual Knowledge Structure Analysis" width="100%">
</p>

<h1 align="center">🧠 LinguaGraph</h1>


<p align="center">
  <a href="https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/portal/" style="display:inline-block;padding:14px 36px;background:linear-gradient(135deg,#60a5fa,#a78bfa);color:#fff;border-radius:10px;font-weight:700;font-size:1.15rem;text-decoration:none;box-shadow:0 4px 16px rgba(96,165,250,.3)">
    🧠 Forschungsportal →
  </a>
  &nbsp;&nbsp;
  <a href="https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/" style="display:inline-block;padding:14px 28px;background:#1e293b;border:1px solid #2d3a50;color:#e2e8f0;border-radius:10px;font-weight:600;font-size:1.05rem;text-decoration:none">
    🌌 CognitiveSpace 3D
  </a>
  &nbsp;&nbsp;
  <a href="docs/paper/" style="display:inline-block;padding:14px 28px;background:#1e293b;border:1px solid #2d3a50;color:#e2e8f0;border-radius:10px;font-weight:600;font-size:1.05rem;text-decoration:none">
    📄 Paper
  </a>
</p>


<p align="center">
  <b>Wie organisieren verschiedene Sprachen und Bildungssysteme das gleiche Wissen?</b>
</p>

<p align="center">
  <a href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/stargazers">
    <img src="https://img.shields.io/github/stars/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph?style=flat-square&logo=github&color=gold" alt="Stars">
  </a>
  <a href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-All%20Rights%20Reserved-blue?style=flat-square" alt="Lizenz">
  </a>
  <a href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/commits/master">
    <img src="https://img.shields.io/github/last-commit/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph?style=flat-square&logo=git" alt="Last Commit">
  </a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/BWKI-2026-8A2BE2?style=flat-square" alt="BWKI 2026">
  <img src="https://img.shields.io/badge/gold_labels-92-success?style=flat-square" alt="92 Gold-Standard">
  <img src="https://img.shields.io/badge/concepts-1,160%2B-informational?style=flat-square" alt="1160+ Konzepte">
  <img src="https://img.shields.io/badge/languages-ZH%20%7C%20EN%20%7C%20DE-green?style=flat-square" alt="ZH/EN/DE">
  <img src="https://img.shields.io/badge/subjects-Math%20%7C%20Physics%20%7C%20Chemistry-orange?style=flat-square" alt="Math/Physics/Chemistry">
  <img src="https://img.shields.io/badge/coverage-NRW%2034%25%20%7C%20UK%2082%25%20%7C%20US%2076%25-yellow?style=flat-square" alt="Coverage Scores">
  <img src="https://img.shields.io/badge/human_validation-N%3D8-purple?style=flat-square" alt="Humanvalidierung N=8">
  <img src="https://img.shields.io/badge/simulation-300-blue?style=flat-square" alt="300 Simulationsbasislinie">
</p>

<p align="center">
  🇩🇪 <a href="README_DE.md">Deutsche Version</a> &nbsp;·&nbsp; 🇨🇳 <a href="README_ZH.md">中文版本</a>
</p>

---

## 📑 Inhaltsverzeichnis

<details>
<summary><b>Click to expand / collapse</b></summary>

- [🔥 Warum LinguaGraph?](#-why-linguagraph)
- [📐 Metriken im Uberblick](#-metrics-at-a-glance)
- [🏆 12 Erkenntnisse (F1–F12)](#-12-findings-f1f12)
- [📊 Datensatz](#-dataset)
- [✅ Extraktion und Humanvalidierung](#-extraction--human-validation)
- [🚀 Schnellstart](#-quick-start)
- [🧪 Modelllvergleich](#-model-benchmark)
- [📁 Projektstruktur](#-project-structure)
- [📚 Key Literaturverzeichnis](#-key-references)
- [📜 Zitationshinweis](#-citation)
- [📜 Lizenz & Compliance](#-license--compliance)
- [🤝 Kontakt](#-contact)

</details>

---

## 🔥 Warum LinguaGraph?

Mathematical truth is universal, but the way it is organized in textbooks varies dramatically across languages and educational systems. Existing curriculum analysis tools are qualitative, manual, and cannot scale across multiple languages or disciplines.

**LinguaGraph is the first automated framework that:**

- 🧩 Constructs **multilingual knowledge graphs** from textbooks at scale (1,160+ concepts, 3 languages)
- 📏 Quantifies **structural differences** between languages, education systems, and disciplines
- 🎯 Measures **textbook-curriculum alignment** across 4 educational systems (Germany, UK, US, China)
- ✅ Validates extraction quality with **92 gold-standard annotations** (F1 = 0.939)

> **It turns the invisible structure of knowledge into visible, measurable metrics.**

---

## 📐 Metriken im Uberblick

| Metrik | Bezeichnung | Formel | Bedeutung |
|--------|-----------|---------|-----------------|
| **CDS** | Concept Density Score | 2\|E\|/(\|V\|·(\|V\|−1)) | Knowledge interconnection density per education level |
| **HDS** | Hierarchy Depth Score | BFS on prerequisite graph | Maximum prerequisite chain length |
| **LDS** | Language Drift Score | 1 − mean(GED, Jaccard_node, Jaccard_edge) | Cross-language structural divergence |
| **CS** | Coverage Score | \|V_textbook ∩ V_curriculum\| / \|V_curriculum\| | Textbook-curriculum alignment |

---

## 🏆 12 Erkenntnisse (F1–F12)

| # | Erkenntnis | Beleg | Auswirkung |
|---|---------|----------|--------|
| **F1** | CDS peaks at **Middle school** (0.271), not Elementary | Confirmed independently in ZH, EN, DE | Challenges "knowledge gets denser with level" assumption |
| **F2** | **3.7× density drop** from Middle to High school | 0.271 → 0.073; concept count 4.2× | Curriculum diversification after integration hub |
| **F3** | HDS ≤ **8** (mean 0.40); 83% of concepts are roots | BFS on 3,538 prerequisite relations | Mathematik is a shallow web, not a deep tree |
| **F4** | **ZH–DE** divergence highest (LDS=0.907), ZH–EN lowest (0.802) | Wikipedia corpus, 5 social topics | Counterintuitive: European languages not structurally closer |
| **F5** | LDS is **topic-dependent** | ~0.2 variation within pairs | Cross-language divergence varies by knowledge domain |
| **F6** | **Physics** peaks at **Elementary** (0.222), Math at Middle (0.271) | 366 physics concepts, 3 languages | Both follow "integrate-early, diverge-late" pattern |
| **F7** | Physics has **2.1× deeper** prerequisite chains | HDS mean 0.85 vs 0.40 | Physics knowledge is more cumulative and sequential |
| **F8** | **Chemistry** peaks at Middle (0.042), 6.5× lower than Math | 220 chemistry concepts | STEM density pattern is universal across subjects |
| **F9** | **Coverage Score** varies dramatically across systems | NRW 34%, UK 82%, US 76%, China 8% | Educational system design fundamentally affects textbook alignment |
| **F10** | Coverage trajectories reveal **system design philosophy** | UK ↑ 53→90% (exam-driven); NRW ↘ 50→31% (specialization) | Assessment structure shapes curriculum-textbook relationship |
| **F11** | **Human LDS** Rangfolge ubereinstimmend mit Wikipedia corpus ✅ | N=8 Probanden, 90 Antworten, 3 levels | Cross-level consistency: individual → textbook → curriculum |
| **F12** | Human LDS (**0.727**) ubertrifft Simulationsbasislinie (**0.647**, p=0.05) | 300 simulated responses, mock extraction | Divergence is genuine, not random variation |

---

## 📊 Datensatz

| Fach | Konzepte | Beziehungen | Lehrbucher | Sprachen | Lehrplanabdeckung |
|---------|:--------:|:---------:|:---------:|:---------:|:------------------:|
| **Mathematik** | 574 | 3,538 | 68 | ZH/EN/DE | NRW 34% · UK 82% · US 76% |
| **Physics** | 366 | 383 | 94 editions | ZH/EN/DE | NRW 38% |
| **Chemistry** | 220 | 215 | 18 editions | ZH/EN/DE | NRW 36% |
| **Gesamt** | **1,160+** | **4,100+** | **180+** | **3 languages** | **4 educational systems** |

---

## ✅ Extraktion und Humanvalidierung

**92 gold-standard annotations** across 2 domains and 3 languages (qwen-plus, Bailian API):

| Bereich | ZH F1 | DE F1 | EN F1 | Gesamt | n |
|--------|:-----:|:-----:|:-----:|:-------:|:-:|
| **Soziale Konzepte** | **0.974** | **0.949** | **0.882** | **0.939** | 72 |
| **Mathematik** | 0.857 | 0.506 | 0.711 | 0.674 | 20 |
| **All** | **0.974** | **0.949** | **0.882** | **0.939** | **92** |

> Fehleranalyse: 29% of errors are from very short responses (1-2 words); 40% from partial omissions. No systematic misdirection.

**🧑 Humanvalidierung Study (N=8)**
- 101 responses from ZH/DE/EN native speakers across 5 social topics
- Innerhalb der Versuchspersonen DE-EN LDS: **0.773** (same person, different language, different concepts)
- Zwischen den Gruppen LDS rank order: **DE–ZH (0.751) > DE–EN (0.727) > ZH–EN (0.704)**
- ✅ **Identical rank order** to Wikipedia corpus — Ebenenubergreifende Validierung

**🤖 Simulationsbasislinie (300 responses)**
- Mean simulated LDS: **0.647** (SD=0.086)
- **Human LDS (0.727) > Simulation LDS (0.647)**, p=0.05
- Confirms cross-language divergence exceeds random expectation

> See [`docs/paper/02_methodology.md`](docs/paper/02_methodology.md) for full methodology, [`scripts/analyze_human_pilot.py`](scripts/analyze_human_pilot.py) for human analysis, and [`scripts/analyze_sim_baseline.py`](scripts/analyze_sim_baseline.py) for simulation.

---


## 🚀 Selbst hosten

The Forschungsportal is a **zero-build static site**. Deploy anywhere:

| Platform | Publish Directory |
|----------|------------------|
| **GitHub Pages** | Deployment bundle contents:
_deploy/data.js
_deploy/docs/annotation_guideline_v1.md
_deploy/docs/annotation_guideline_v2.md
_deploy/docs/ARCHITECTURE.md
_deploy/docs/audit-report.md
_deploy/docs/bwki-compliance-review.md
_deploy/docs/bwki_paper_outline.md
_deploy/docs/bwki_paper_outline_v2.md
_deploy/docs/CHANGELOG.md
_deploy/docs/cognitive_metrics_framework.md
_deploy/docs/CONSOLIDATION_REPORT.md
_deploy/docs/CONTRIBUTORS.md
_deploy/docs/corpus-status.md
_deploy/docs/coverage_score_definition.md
_deploy/docs/creative_submission.md
_deploy/docs/curriculum_layer_plan.md
_deploy/docs/data_arrival_checklist.md
_deploy/docs/data_expansion_task.md
_deploy/docs/demo_script.md
_deploy/docs/error_analysis.md
_deploy/docs/evidence_milestones.md
_deploy/docs/experiment-design.md
_deploy/docs/experiment_conductor.md
_deploy/docs/figure_plan.md
_deploy/docs/gold_dataset_schema_v1.md
_deploy/docs/handoff_multi_subject.md
_deploy/docs/infrastructure_audit.md
_deploy/docs/judge_qa.md
_deploy/docs/limitations.md
_deploy/docs/literature_matrix.md
_deploy/docs/logos_integration.md
_deploy/docs/mcl_definition.md
_deploy/docs/methodology.md
_deploy/docs/metrics_validation_report.md
_deploy/docs/mimo_prompt.md
_deploy/docs/model_strategy.md
_deploy/docs/paper_results_skeleton.md
_deploy/docs/pilot-study.md
_deploy/docs/pilot_quality_report.md
_deploy/docs/pitch_10min.md (auto) |
| **Cloudflare Pages** |  |
| **Vercel** |  |
| **Local** | Open  |


## 🚀 Schnellstart

```bash
# 1. Install & configure
git clone https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph.git
cd BWKI-2026-LinguaGraph
pip install openai numpy
export BAILIAN_API_KEY="your-api-key"

# 2. Validate extraction quality (5 min)
python scripts/batch_process_responses.py --gold-only
python scripts/evaluate_gold.py

# 3. Generate 300-response Simulationsbasislinie
python scripts/simulate_baseline.py --mock

# 4. Full analysis pipeline
python scripts/extract_all_via_api.py
python scripts/compute_lds_from_db.py
```

### Beliebiges Modelll testen
```bash
python scripts/batch_process_responses.py --model qwen-plus --gold-only
python scripts/batch_process_responses.py --model glm-4.6 --gold-only
```

---

## 🧪 Modelllvergleich

20 models tested on identical 20 gold labels (20 social + 20 math) via [Alibaba Cloud Bailian](https://bailian.console.aliyun.com/):

| Modell | Bereich | ZH F1 | DE F1 | EN F1 | Geschwindigkeit |
|-------|--------|:-----:|:-----:|:-----:|:-----:|
| **qwen-plus** | **Social** | **0.974** | **0.949** | **0.882** | 2-3s |
| qwen-turbo | Math | 0.714 | 0.448 | 0.810 | 1s |
| qwen3.7-max | Math | 0.980 | 0.551 | 0.778 | 2-3s |
| glm-4.6 | Math | 0.951 | 0.595 | 0.689 | 10-20s |

Vollstandige Ergebnisse: [`research/findings/bailian_benchmark_complete.json`](research/findings/bailian_benchmark_complete.json)

---

## 📁 Projektstruktur

```
├── scripts/              # Analysis pipelines (batch extraction, evaluation, benchmark)
├── docs/
│   ├── paper/            # Full research paper (abstract → conclusion)
│   ├── review/           # Quality audits & critical assessments
│   ├── ethics/           # GDPR compliance & consent forms
│   └── creative_submission.md  # BWKI competition submission
├── config/
│   ├── expert_graphs/    # Knowledge graphs (JSON) — Math, Physics, Chemistry, Curricula
│   └── concept_mapping.json    # 174 cross-lingual concept alignments
├── cognitive-space/      # 3D knowledge graph visualization (Three.js)
├── research/findings/    # Benchmark outputs, evaluation reports
└── .gitignore            # API keys, DB, PII excluded
```

---

## 📚 Literaturverzeichnis

### Academic Papers

| # | Reference | Relevance |
|---|-----------|-----------|
| 1 | **Novak, J. D. & Cañas, A. J.** (2008). *The theory underlying concept maps and how to construct and use them.* | Foundational — concept mapping theory underpinning CDS/HDS |
| 2 | **Ausubel, D. P.** (1963). *The psychology of meaningful verbal learning.* Grune & Stratton. | Assimilation theory — knowledge is structured, not listed |
| 3 | **Schmidt, W. H. et al.** (2001). *Why schools matter: A cross-national comparison of curriculum and learning.* Jossey-Bass. | TIMSS curriculum coherence — Coverage Score inspiration |
| 4 | **Liang, L. L. & Heckmann, K.** (2013). *Comparing German and Chinese mathematics textbooks.* ZDM, 45(6). | Cross-national textbook comparison methodology |
| 5 | **Boroditsky, L.** (2001). *Does language shape thought?: Mandarin and English speakers' conceptions of time.* Cognitive Psychology, 43(1). | Linguistic relativity — research question context |
| 6 | **Siew, C. S. Q.** (2019). *Applications of network science to education research.* In: Network Science in Education. Springer. | Network analysis of cognitive/educational structures |
| 7 | **Ain, Q. T., Chatti, M. A., & Qussa, H.** (2025). *An optimized pipeline for automatic educational knowledge graph construction.* arXiv. | Most directly relevant EKG pipeline methodology |
| 8 | **Alatrash, R., Chatti, M. A., & Wibowo, A.** (2025). *Inferring prerequisite knowledge concepts in educational knowledge graphs.* arXiv. | Prerequisite inference — supports HDS metric |
| 9 | **Fan, L., Zhu, Y., & Miao, Z.** (2013). *Textbook research in mathematics education.* ESM. | Cross-national textbook problem analysis |
| 10 | **OECD.** (2023). *Education at a Glance 2023.* OECD Publishing. | Cross-national curriculum structure data |
| 11 | **IEA.** (2019). *TIMSS 2019 International Results in Mathematik and Science.* | Curriculum coverage analysis methodology |
| 12 | **Vaswani, A. et al.** (2017). *Attention Is All You Need.* NeurIPS. | Transformer architecture — foundational for LLMs used |

### Open Source Libraries

| Library | Usage | Lizenz |
|---------|-------|---------|
| [openai/openai-python](https://github.com/openai/openai-python) | LLM API client for concept extraction | MIT |
| [networkx/networkx](https://github.com/networkx/networkx) | Graph construction and analysis (CDS, HDS) | BSD-3 |
| [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) | Figure generation (Fig 3-7) | PSF |
| [numpy/numpy](https://github.com/numpy/numpy) | Numerical computation, similarity metrics | BSD-3 |
| [scipy/scipy](https://github.com/scipy/scipy) | Statistical analysis, correlation tests | BSD-3 |
| [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) | Baseline models and evaluation | BSD-3 |
| [Three.js](https://github.com/mrdoob/three.js) | 3D knowledge graph visualization (CognitiveSpace) | MIT |
| [Flask](https://github.com/pallets/flask) | Workbench web application | BSD-3 |
| [seaborn/seaborn](https://github.com/mwaskom/seaborn) | Statistical data visualization | BSD-3 |

### Curriculum Standards (Primary Sources)

| Standard | Publisher |
|----------|-----------|
| Kernlehrplan Mathematik/Physik/Chemie NRW (Sek I 2019, Sek II 2023) | MSB NRW |
| UK National Curriculum (Mathematik, Science) | DfE England |
| US Next Generation Science Standards (NGSS) | NGSS Lead States |
| Chinese National Curriculum Standards (数学/物理/化学) | MoE China |

### Textbook Corpora

Textbook content used for knowledge graph construction (academic research, fair use). Full attribution in graph metadata files.

**ZH** (33+ publishers): 人教版, 沪科版, 北师大版, 苏科版, 粤教版, 鲁科版, 马文蔚, 程守洙, 漆安慎, 赵凯华, 汪志诚, 杨福家, 梁昆淼, 郭硕鸿, 曾谨言

**EN** (34+ publishers): Khan Academy, CK-12, AP Physics, IB, IGCSE, GCSE, Halliday Resnick Walker, Serway Jewett, Young Freedman, Griffiths, Kittel, Feynman Lectures, Stewart Calculus, Strang Linear Algebra

**DE** (27+ publishers): Duden, Lambacher Schwere, Westermann, Cornelsen, Klett, Auer, Dorn-Bader, Kern, Thieme, Tipler, Demtröder, Jackson, Papula, Fischer

### Acknowledgments

- **BWKI 2026** — Competition platform
- **Alibaba Cloud Bailian** — Free API quota (1M tokens per model)
- **OpenRouter** — Modell routing (tested)
- **LM Studio** — Local inference (initial development)## 📜 Zitationshinweis

```bibtex
@misc{linguaGraph2026,
  author = {Rongjing, J.},
  title = {LinguaGraph: Cross-Lingual Knowledge Structure Analysis Framework},
  year = {2026},
  publisher = {GitHub},
  journal = {BWKI 2026 — Bundeswettbewerb K{\"u}nstliche Intelligenz},
  url = {https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph}
}
```

---

## 📜 Lizenz & Compliance

- **Lizenz**: Alle Rechte vorbehalten — BWKI 2026 competition project
- **Privacy**: Participant data fully anonymized. No PII in repository. See [`docs/ethics/`](docs/ethics/) for GDPR compliance.
- **AI Ethics**: LLM usage limited to concept extraction from textbook text. No synthetic data presented as human data.
- **Data Sources**: Textbook excerpts used for academic research under fair use principles.

---

## 🤝 Kontakt

- **Competition**: [BWKI 2026](https://www.bw-ki.de/)
- **Repository**: [github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph](https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph)
- **3D Demo**: Open [`cognitive-space/web/index.html`](cognitive-space/web/index.html) in your browser
- **Author**: Rongjing J. — bilingual researcher (ZH/DE), passionate about AI & education

<p align="center">
  <sub>Built with ❤️ for BWKI 2026 — because knowledge should be understood, not just taught.</sub>
</p>
<p align="center">
  <a href="https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/portal/" style="display:inline-block;padding:14px 36px;background:linear-gradient(135deg,#60a5fa,#a78bfa);color:#fff;border-radius:10px;font-weight:700;font-size:1.15rem;text-decoration:none">
    🧠 LinguaGraph Forschungsportal →
  </a>
  <br>
  <span style="color:#94a3b8;font-size:0.85rem">Forschungsfragen · Erkenntniss · Interaktives 3D · Validation · Paper</span>
</p>



<p align="center">
  <a href="README_DE.md">🇩🇪 Deutsch</a> · <a href="README_ZH.md">🇨🇳 中文</a>
</p>
