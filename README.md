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
    🧠 Research Portal →
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
  <b>How do different languages and educational systems organize the same knowledge?</b>
</p>

<p align="center">
  <a href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/stargazers">
    <img src="https://img.shields.io/github/stars/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph?style=flat-square&logo=github&color=gold" alt="Stars">
  </a>
  <a href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-All%20Rights%20Reserved-blue?style=flat-square" alt="License">
  </a>
  <a href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/commits/master">
    <img src="https://img.shields.io/github/last-commit/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph?style=flat-square&logo=git" alt="Last Commit">
  </a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/BWKI-2026-8A2BE2?style=flat-square" alt="BWKI 2026">
  <img src="https://img.shields.io/badge/gold_labels-92-success?style=flat-square" alt="92 Gold Labels">
  <img src="https://img.shields.io/badge/concepts-1,140%2B-informational?style=flat-square" alt="1140+ Concepts">
  <img src="https://img.shields.io/badge/languages-ZH%20%7C%20EN%20%7C%20DE-green?style=flat-square" alt="ZH/EN/DE">
  <img src="https://img.shields.io/badge/subjects-Math%20%7C%20Physics%20%7C%20Chemistry-orange?style=flat-square" alt="Math/Physics/Chemistry">
  <img src="https://img.shields.io/badge/coverage-NRW%2012.7%25%20%7C%20UK%2037.3%25%20%7C%20US%2017.2%25%20%7C%20CN%2095.4%25-yellow?style=flat-square" alt="Coverage Scores">
  <img src="https://img.shields.io/badge/human_validation-N%3D15-purple?style=flat-square" alt="Human Validation N=15">
  <img src="https://img.shields.io/badge/simulation-300-blue?style=flat-square" alt="300 Simulation Baseline">
</p>

<p align="center">
  🇩🇪 <a href="README_DE.md">Deutsche Version</a> &nbsp;·&nbsp; 🇨🇳 <a href="README_ZH.md">中文版本</a>
</p>

---

## 📑 Table of Contents

<details>
<summary><b>Click to expand / collapse</b></summary>

- [🔥 Why LinguaGraph?](#-why-linguagraph)
- [📐 Metrics at a Glance](#-metrics-at-a-glance)
- [🏆 12 Findings (F1–F12)](#-12-findings-f1f12)
- [📊 Dataset](#-dataset)
- [✅ Extraction & Human Validation](#-extraction--human-validation)
- [🚀 Quick Start](#-quick-start)
- [🧪 Model Benchmark](#-model-benchmark)
- [📁 Project Structure](#-project-structure)
- [📚 Key References](#-key-references)
- [📜 Citation](#-citation)
- [📜 License & Compliance](#-license--compliance)
- [🤝 Contact](#-contact)

</details>

---

## 🔥 Why LinguaGraph?

Mathematical truth is universal, but the way it is organized in textbooks varies dramatically across languages and educational systems. Existing curriculum analysis tools are qualitative, manual, and cannot scale across multiple languages or disciplines.

**LinguaGraph is the first automated framework that:**

- 🧩 Constructs **multilingual knowledge graphs** from textbooks at scale (1,160+ concepts, 3 languages)
- 📏 Quantifies **structural differences** between languages, education systems, and disciplines
- 🎯 Measures **textbook-curriculum alignment** across 4 educational systems (Germany, UK, US, China)
- ✅ Validates extraction quality with **92 gold-standard annotations** (weighted F1 = 0.881; social subset F1 = 0.939)

> **It turns the invisible structure of knowledge into visible, measurable metrics.**

---

## 📐 Metrics at a Glance

| Metric | Full Name | Formula | What It Reveals |
|--------|-----------|---------|-----------------|
| **CDS** | Concept Density Score | 2\|E\|/(\|V\|·(\|V\|−1)) | Knowledge interconnection density per education level |
| **HDS** | Hierarchy Depth Score | BFS on prerequisite graph | Maximum prerequisite chain length |
| **LDS** | Linguistic Divergence Score (LDS) | 1 − (Jaccard_node + Jaccard_edge) / 2 | Cross-language structural (dis)similarity |
| **CS** | Coverage Score | \|V_textbook ∩ V_curriculum\| / \|V_curriculum\| | Textbook-curriculum alignment (updated: CN 95.4%, NRW 12.7%, UK 37.3%, US 17.2%) |

---

## 🏆 12 Findings (F1–F12)

| # | Finding | Evidence | Impact |
|---|---------|----------|--------|
| **F1** | CDS peaks at **Middle school** (0.271), not Elementary | Confirmed independently in ZH, EN, DE | Challenges "knowledge gets denser with level" assumption |
| **F2** | **3.7× density drop** from Middle to High school | 0.271 → 0.073; concept count 4.2× | Curriculum diversification after integration hub |
| **F3** | HDS ≤ **8** (mean 0.40); 83% of concepts are roots | BFS on 525 direct relations (+~3000 transitive) | Mathematics is a shallow web, not a deep tree |
| **F4** | **LDS-K reveals heterogeneous convergence**: ZH-DE (0.519) converges; ZH-EN (0.934), DE-EN (0.938) near noise floor | Direct computation on textbook graphs | Knowledge-structure LDS diverges from surface-language expectations — but Null Model (F5) falsifies the language reading; math nodes are partly alignment-label artefacts (see `docs/p2_methodology_rechecks.md`) |
| **F5** | LDS is **topic-dependent**; **Null Model** confirms Full < Structure for all pairs | ~0.2 variation within pairs; Full LDS-K=0.73, Structure LDS-K=0.77 | Cross-language divergence varies by knowledge domain; taxonomy alone explains most variance |
| **F6** | **Physics** peaks at **Elementary** (0.222), Math at Middle (0.271) | 366 physics concepts, 3 languages | Both follow "integrate-early, diverge-late" pattern |
| **F7** | Physics has **2.1× deeper** prerequisite chains | HDS mean 0.85 vs 0.40 | Physics knowledge is more cumulative and sequential |
| **F8** | **Chemistry** peaks at Middle (0.042), 6.5× lower than Math | 220 chemistry concepts | Consistent with, but not confirming, the cross-subject density pattern (small absolute gap 0.012, no test) |
| **F9** | **Coverage Score** varies dramatically across systems | NRW 12.7%, UK 37.3%, US 17.2%, CN 95.4% (keyword matching; granularity confound: CN 87 vs US 2124 vs NRW 299 curriculum concepts) | Measurement strong, governance attribution weak — CS gap is primarily a hypothesis (see F10) |
| **F10** | Coverage trajectories suggest a **governance hypothesis** | UK exam-driven convergence; NRW specialization divergence; China centralized near-total alignment | Hypothesis only: centralized (CN MOE) vs federal (DE Länder/KMK) institutional context is documented (TIMSS 2023 Encyclopedia; OECD EAG 2025), but classroom-implementation chain is untested |
| **F11** | **N=15 falsifies ΔLDS > 0 under between-subject design**; **ΔLDS** retained as metric for within-subject use | N=15 (6 DE · 6 ZH · 3 EN): LDS-C 0.93–0.96 ≈ split-half floor; pilot N=8 not replicated | Between-subject designs cannot separate language from participant variance; within-subject design required |
| **F12** | Concept-level **ΔLDS ≈ 0** (−0.05…+0.05); relation-level Δ not comparable | N=15 + LLM within-subject (LDS-C ≫ floor +0.08–0.09) | Language signal exists within-subject (LLM), absent between-subject (human) — design artefact, not proof of no effect; earlier sim comparison withdrawn |

---

## 📊 Dataset

| Subject | Concepts | Relations | Textbooks | Languages | Curriculum Coverage |
|---------|:--------:|:---------:|:---------:|:---------:|:------------------:|
| **Mathematics** | 556 | 525 direct (+~3000 transitive) | 68 | ZH/EN/DE | NRW 12.7% · UK 37.3% · US 17.2% · CN 95.4% |
| **Physics** | 366 | 383 | 94 editions | ZH/EN/DE | NRW coverage NA |
| **Chemistry** | 220 | 215 | 18 editions | ZH/EN/DE | NRW 36% |
| **Total** | **1,140+** | **1,100+ direct** | **180+** | **3 languages** | **4 educational systems** |

> SSOT: math-graph counts from `manifest.json` (556 nodes / 525 direct relations / 219 trilingual groups). Physics/chemistry counts from legacy pipelines (see `docs/review/rnd_project_review_20260811.md` §7).

---

## ✅ Extraction & Human Validation

**92 gold-standard annotations** across 2 domains and 3 languages (production extraction model, Bailian API):

| Domain | ZH F1 | DE F1 | EN F1 | Overall | n |
|--------|:-----:|:-----:|:-----:|:-------:|:-:|
| **Social concepts** | **0.974** | **0.949** | **0.882** | **0.939** | 72 |
| **Mathematics** | 0.857 | 0.506 | 0.711 | 0.674 | 20 |
| **All (weighted)** | 0.951 | 0.842 | 0.844 | **0.881** | **92** |

> Overall = weighted mean over domains ((72×0.939+20×0.674)/92≈0.881). The headline 0.939 applies to the social subset only.

> Error analysis: 29% of errors are from very short responses (1-2 words); 40% from partial omissions. No systematic misdirection.

**🧑 Human Validation Study (N=15 extended; N=8 pilot not replicated)**
- Extended study (6 DE · 6 ZH · 3 EN): concept-level LDS-C **0.93–0.96 ≈ within-language split-half floor (0.92–0.96) ≈ label permutation (0.94)** — no separable language signal under between-subject design; **ΔLDS ≈ 0** (−0.05…+0.05, concept level; relation-level Δ not comparable across sparsity regimes)
- Pilot N=8 values (0.70–0.75, rank DE–ZH > DE–EN > ZH–EN) **not replicated** by N=15 — reported for transparency only
- Textbook LDS-K rank order: **ZH–EN (0.934) ≈ DE–EN (0.938) ≫ ZH–DE (0.519)** — but see Null Model: LDS-K does not measure language divergence

**🤖 Simulation Baseline (300 responses, exploratory)**
- Mean simulated LDS-C: **0.647** (mock keyword extraction — not comparable to production-model extraction; descriptive only, no p-value)
- The earlier human-vs-simulation comparison (p=0.05) is **withdrawn**: measurement-scale drift makes it invalid (see `docs/paper/04_discussion.md` §8.11–8.12)

**🧪 Null Model (Structure vs Full Graphs)**
- Full knowledge-graph LDS-K: **0.73** (mean across all pairs)
- Structure-only (taxonomy) LDS-K: **0.77** (mean)
- **Full < Structure for all pairs** — adding edge relations reduces rather than amplifies divergence
- Taxonomy (shared concept organization) accounts for most variance; language-specific relations are convergent

> See [`docs/paper/02_methodology.md`](docs/paper/02_methodology.md) for full methodology, [`scripts/analyze_human_pilot.py`](scripts/analyze_human_pilot.py) for human analysis, and [`scripts/analyze_sim_baseline.py`](scripts/analyze_sim_baseline.py) for simulation.

---


## 🚀 Deploy Your Own

The Research Portal is a **zero-build static site** published from `_deploy/` via GitHub Pages
(`.github/workflows/deploy-cognitive-space.yml` on push to master):

| Source | Deployed as | Notes |
|--------|-------------|-------|
| `cognitive-space/web/*` | `_deploy/` root | 3D visualization + `data.js` (via `scripts/release.py`) |
| `cognitive-space/portal/` | `_deploy/portal/` | Research Portal (Finding E: N=15 narrative) |
| `docs/` | `_deploy/docs/` | Paper + reviews (mirrored; see `docs/INDEX.md`) |
| `README*.md` | `_deploy/README*.md` | Trilingual mirrors (via `sync_readmes.py`) |

Local preview: open `cognitive-space/portal/index.html` or `cognitive-space/web/index.html` in a browser.


## 🚀 Quick Start

```bash
# 1. Install & configure
git clone https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph.git
cd BWKI-2026-LinguaGraph
pip install openai numpy
export BAILIAN_API_KEY="your-api-key"

# 2. Validate extraction quality (5 min)
python scripts/batch_process_responses.py --gold-only
python scripts/evaluate_gold.py

# 3. Generate 300-response simulation baseline
python scripts/simulate_baseline.py --mock

# 4. Full analysis pipeline
python scripts/extract_all_via_api.py
python scripts/compute_lds_from_db.py
```

### Test any model
```bash
python scripts/batch_process_responses.py --model qwen-plus --gold-only
python scripts/batch_process_responses.py --model glm-4.6 --gold-only
```

---

## 🧪 Model Benchmark

**55 complete measurements (50 unique models)** across DashScope (42), zen/OpenRouter (7) + D1 baseline, Kilo (2), Cohere (1), NIM (1) and opencode-go (1) on the identical P1 protocol (3 languages × k=10), plus the 19-model extraction benchmark (F1 range 0.55–0.67) — best extraction results shown below. Replication: [`data/lds_c/llm_subject/multi_model_replication_20260910.json`](data/lds_c/llm_subject/multi_model_replication_20260910.json); all 55 ZH–DE pairs significant (p<0.05), 8 English-involved pairs not (all EN-related, mostly R1/Distill).

| Model | Domain | ZH F1 | DE F1 | EN F1 | Speed |
|-------|--------|:-----:|:-----:|:-----:|:-----:|
| **qwen-plus** | **Social** | **0.974** | **0.949** | **0.882** | 2-3s |
| qwen-turbo | Math | 0.714 | 0.448 | 0.810 | 1s |
| qwen3.7-max | Math | 0.980 | 0.551 | 0.778 | 2-3s |
| glm-4.6 | Math | 0.951 | 0.595 | 0.689 | 10-20s |

Full results: [`data/lds_c/llm_subject/multi_model_replication_20260810.json`](data/lds_c/llm_subject/multi_model_replication_20260810.json)

---

## 📁 Project Structure

```
├── scripts/              # Analysis pipelines (batch extraction, evaluation, benchmark)
│   ├── math_graph_pipeline/  # Canonical pipeline (SSOT: merge→align→export→validate)
│   ├── release.py            # Unified release (gates→export→manifest→bundle)
│   └── build_paper_pdf.py    # Paper assembly (docs/paper → submission PDF)
├── docs/
│   ├── INDEX.md          # Navigation for all 83 docs
│   ├── paper/            # Full research paper (reading order: see ORDER in build_paper_pdf.py)
│   ├── review/           # Quality audits & critical assessments
│   ├── ethics/           # GDPR compliance & consent forms
│   └── submission/       # BWKI submission (PDF + platform answers + checklist)
├── submission/
│   ├── final/            # Final package (PDF + answers + disclosure + code guide)
│   ├── pitch/            # Video pitch (script v2 + storyboard; recording separate)
│   └── idea/             # Ideenanmeldung 28.06. (historical)
├── config/
│   ├── expert_graphs/    # Knowledge graphs (JSON) — Math, Physics, Chemistry, Curricula
│   └── cross_language_mapping.json  # 30 shared concept IDs (frozen)
├── cognitive-space/      # 3D visualization (Three.js) + portal/
├── research_lab/         # Sandboxed experiments (gitignored skills/)
├── release/              # Immutable snapshot (manifest + data.js + checksums)
├── freeze/               # Frozen survey samples (immutable)
└── manifest.json         # SSOT numbers (556/525/219)
```

---

## 📚 References

### Academic Papers

| # | Reference | Paper | Relevance |
|---|-----------|-------|-----------|
| 1 | **Novak, J. D. & Cañas, A. J.** (2008). *The theory underlying concept maps and how to construct and use them.* | [13] | Foundational — concept mapping theory underpinning CDS/HDS |
| 2 | **Ausubel, D. P.** (1963). *The psychology of meaningful verbal learning.* Grune & Stratton. | [12] | Assimilation theory — knowledge is structured, not listed |
| 3 | **Schmidt, W. H. et al.** (2001). *Why schools matter: A cross-national comparison of curriculum and learning.* Jossey-Bass. | [54] | TIMSS curriculum coherence — Coverage Score inspiration |
| 4 | **Liang, S. & Heckmann, K.** (2013). *Comparing German and Chinese mathematics textbooks.* ZDM, 45(5), 743–756. | [8] | Cross-national textbook comparison methodology |
| 5 | **Boroditsky, L.** (2001). *Does language shape thought?: Mandarin and English speakers' conceptions of time.* Cognitive Psychology, 43(2). | [53] | Linguistic relativity — research question context |
| 6 | **Siew, C. S. Q.** (2019). *Applications of network science to education research.* In: Network Science in Education. Springer. | — (background) | Network analysis of cognitive/educational structures |
| 7 | **Ain, Q. U., Chatti, M. A., & Qussa, J.** (2025). *An optimized pipeline for automatic educational knowledge graph construction.* arXiv:2509.05392. | [3] | Most directly relevant EKG pipeline methodology |
| 8 | **Alatrash, R., Chatti, M. A., & Wibowo, N.** (2025). *Inferring prerequisite knowledge concepts in educational knowledge graphs.* arXiv:2509.05393. | [5] | Prerequisite inference — supports HDS metric |
| 9 | **Fan, L., Zhu, Y., & Miao, Z.** (2013). *Textbook research in mathematics education.* ICMT. | [9] | Cross-national textbook problem analysis |
| 10 | **OECD.** (2025). *Education at a Glance 2025.* OECD Publishing. | [32] | Cross-national curriculum structure data |
| 11 | **IEA.** (2023). *TIMSS 2023.* | [6] / [30] | Curriculum coverage analysis methodology |
| 12 | **Vaswani, A. et al.** (2017). *Attention Is All You Need.* NeurIPS. | — (background) | Transformer architecture — foundational for LLMs used |

### Open Source Libraries

| Library | Usage | License |
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
| UK National Curriculum (Mathematics, Science) | DfE England |
| US Next Generation Science Standards (NGSS) | NGSS Lead States |
| Chinese National Curriculum Standards (数学/物理/化学) | MoE China |

### Textbook Corpora

Textbook content used for knowledge graph construction (academic research, fair use). Full attribution in graph metadata files.

**ZH** (33+ publishers): 人教版, 沪科版, 北师大版, 苏科版, 粤教版, 鲁科版, 马文蔚, 程守洙, 漆安慎, 赵凯华, 汪志诚, 杨福家, 梁昆淼, 郭硕鸿, 曾谨言

**EN** (34+ publishers): Khan Academy, CK-12, AP Physics, IB, IGCSE, GCSE, Halliday Resnick Walker, Serway Jewett, Young Freedman, Griffiths, Kittel, Feynman Lectures, Stewart Calculus, Strang Linear Algebra

**DE** (27+ publishers): Duden, Lambacher Schwere, Westermann, Cornelsen, Klett, Auer, Dorn-Bader, Kern, Thieme, Tipler, Demtröder, Jackson, Papula, Fischer

### Acknowledgments

- **BWKI 2026** — Competition platform and framework
- **Schloss Heessen** — Boarding school in Hamm, Germany; institutional support and educational guidance
- **OpenCode GO** — AI service platform providing model API access
- **Claude Code** — AI-assisted development platform (Anthropic)
- **MimoCode** — AI service platform via OpenCode GO
- **Alibaba Cloud Bailian** — Free API quota (1M tokens per model)
- **OpenRouter** — Model routing (tested)
- **LM Studio** — Local inference (initial development)

## 📜 Citation

```bibtex
@misc{linguaGraph2026,
  author = {Rong, Jiajun and Lan, Zhenxi},
  title = {LinguaGraph: Cross-Lingual Knowledge Structure Analysis Framework},
  year = {2026},
  publisher = {GitHub},
  journal = {BWKI 2026 — Bundeswettbewerb K{\"u}nstliche Intelligenz},
  url = {https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph}
}
```

---

## 📜 License & Compliance

- **License**: All Rights Reserved — BWKI 2026 competition project
- **Privacy**: Participant data fully anonymized. No PII in repository. See [`docs/ethics/`](docs/ethics/) for GDPR compliance.
- **AI Ethics**: LLM usage limited to concept extraction from textbook text. No synthetic data presented as human data.
- **Data Sources**: Textbook excerpts used for academic research under fair use principles.

---

## 🤝 Contact

- **Competition**: [BWKI 2026](https://www.bw-ki.de/)
- **Repository**: [github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph](https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph)
- **3D Demo**: Open [`cognitive-space/web/index.html`](cognitive-space/web/index.html) in your browser
- **Authors**: Jiajun Rong & Zhenxi Lan — Privatschule Schloss Heessen (BWKI 2026 team)

<p align="center">
  <sub>Built with ❤️ for BWKI 2026 — because knowledge should be understood, not just taught.</sub>
</p>
<p align="center">
  <a href="https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/portal/" style="display:inline-block;padding:14px 36px;background:linear-gradient(135deg,#60a5fa,#a78bfa);color:#fff;border-radius:10px;font-weight:700;font-size:1.15rem;text-decoration:none">
    🧠 LinguaGraph Research Portal →
  </a>
  <br>
  <span style="color:#94a3b8;font-size:0.85rem">Research Questions · Findings · Interactive 3D · Validation · Paper</span>
</p>



<p align="center">
  <a href="README_DE.md">🇩🇪 Deutsch</a> · <a href="README_ZH.md">🇨🇳 中文</a>
</p>
