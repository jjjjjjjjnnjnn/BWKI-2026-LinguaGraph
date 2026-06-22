<p align="center">
  <img src="cognitive-space/web/screenshot.png" alt="LinguaGraph — Cross-Lingual Knowledge Structure Analysis" width="100%">
</p>

<h1 align="center">🧠 LinguaGraph</h1>

<p align="center">
  <b>How do different languages and educational systems organize the same knowledge?</b><br>
  <i>Wie organisieren verschiedene Sprachen und Bildungssysteme dasselbe Wissen?</i><br>
  <em>不同语言和教育体系是如何组织同一知识的？</em>
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
  <a href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph">
    <img src="https://img.shields.io/github/repo-size/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph?style=flat-square&logo=github" alt="Repo Size">
  </a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/BWKI-2026-8A2BE2?style=flat-square" alt="BWKI 2026">
  <img src="https://img.shields.io/badge/gold_labels-92-success?style=flat-square" alt="92 Gold Labels">
  <img src="https://img.shields.io/badge/concepts-1160%2B-informational?style=flat-square" alt="1160+ Concepts">
  <img src="https://img.shields.io/badge/languages-ZH%20%7C%20EN%20%7C%20DE-green?style=flat-square" alt="ZH/EN/DE">
  <img src="https://img.shields.io/badge/subjects-Math%20%7C%20Physics%20%7C%20Chemistry-orange?style=flat-square" alt="Math/Physics/Chemistry">
</p>

---

## 🔥 Why LinguaGraph?

<details open>
<summary><b>🇬🇧 English</b></summary>

Mathematical truth is universal, but the way it is organized in textbooks varies dramatically across languages and educational systems. Existing curriculum analysis tools are qualitative, manual, and cannot scale across multiple languages or disciplines.

**LinguaGraph is the first automated framework that:**

- Constructs **multilingual knowledge graphs** from textbooks at scale (1,160+ concepts, 3 languages)
- Quantifies **structural differences** between languages, education systems, and disciplines
- Measures **textbook-curriculum alignment** across 4 educational systems (Germany, UK, US, China)
- Validates extraction quality with **92 gold-standard annotations** (F1 = 0.939)

**It turns the invisible structure of knowledge into visible, measurable metrics.**
</details>

<details>
<summary><b>🇩🇪 Deutsch</b></summary>

Mathematische Wahrheit ist universell, aber ihre Organisation in Lehrbüchern variiert stark zwischen Sprachen und Bildungssystemen. Bestehende Analysetools sind qualitativ, manuell und nicht skalierbar.

**LinguaGraph ist das erste automatisierte Framework, das:**

- Mehrsprachige Wissensgraphen aus Lehrbüchern in großem Maßstab erstellt (1.160+ Konzepte, 3 Sprachen)
- Strukturelle Unterschiede zwischen Sprachen, Bildungssystemen und Disziplinen quantifiziert
- Die Lehrplanabdeckung in 4 Bildungssystemen misst (Deutschland, UK, USA, China)
- Die Extraktionsqualität mit 92 Goldstandard-Annotationen validiert (F1 = 0,939)

**Es verwandelt die unsichtbare Struktur von Wissen in sichtbare, messbare Metriken.**
</details>

<details>
<summary><b>🇨🇳 中文</b></summary>

数学真理是普适的，但知识在教材中的组织方式在不同语言和教育体系之间存在显著差异。现有的课程分析工具是定性的、人工的，无法跨语言或跨学科规模化。

**LinguaGraph 是第一个能够自动完成以下任务的框架：**

- 从教材中大规模构建多语言知识图谱（1160+ 概念，3 种语言）
- 量化语言、教育体系和学科之间的结构差异
- 衡量 4 个教育体系的教材-课程标准覆盖率（德国、英国、美国、中国）
- 使用 92 条黄金标准标注验证提取质量（F1 = 0.939）

**它将知识不可见的结构转化为可见、可量化的指标。**
</details>

---

## 📐 Metrics at a Glance

| Metric | Full Name | Formula | What It Reveals |
|--------|-----------|---------|-----------------|
| **CDS** | Concept Density Score | 2\|E\|/(\|V\|·(\|V\|−1)) | Knowledge interconnection density per education level |
| **HDS** | Hierarchy Depth Score | BFS on prerequisite graph | Maximum prerequisite chain length |
| **LDS** | Language Drift Score | 1 − mean(GED, Jaccard_node, Jaccard_edge) | Cross-language structural divergence |
| **CS** | Coverage Score | \|V_textbook ∩ V_curriculum\| / \|V_curriculum\| | Textbook-curriculum alignment |

---

## 🏆 10 Findings (F1–F10)

<details>
<summary><b>See all findings</b></summary>

| # | Finding | Evidence | Impact |
|---|---------|----------|--------|
| **F1** | CDS peaks at **Middle school** (0.271), not Elementary | 3 languages independently, 574 concepts | Challenges "knowledge gets denser with level" assumption |
| **F2** | **3.7× density drop** from Middle to High school | 0.271 → 0.073 | Curriculum diversification after integration hub |
| **F3** | HDS ≤ **8** (mean 0.40); 83% of concepts are roots | BFS on 3,538 prerequisite relations | Math is a shallow web, not a deep tree |
| **F4** | **ZH–DE** divergence highest (LDS=0.907), ZH–EN lowest (0.802) | Wikipedia corpus, 5 topics | Counterintuitive: European languages not more similar |
| **F5** | LDS is **topic-dependent** | ~0.2 variation within pairs | Cross-language divergence varies by knowledge domain |
| **F6** | **Physics** peaks at **Elementary** (0.222), Math at Middle (0.271) | 366 physics concepts | Both follow "integrate-early, diverge-late" |
| **F7** | Physics has **2.1× deeper** prerequisite chains | HDS mean 0.85 vs 0.40 | Physics is more sequential and cumulative |
| **F8** | **Chemistry** peaks at Middle (0.042), 6.5× lower than Math | 220 chemistry concepts | STEM density pattern is universal |
| **F9** | **Coverage Score** varies dramatically | NRW 34%, UK 82%, US 76%, China 8% | Educational system design affects textbook alignment |
| **F10** | Coverage trajectories reveal system design | UK ↑ 53→90% (exam-driven), NRW ↘ 50→31% (specialization) | Assessment structure shapes curriculum alignment |
</details>

---

## 📊 Dataset

| Subject | Concepts | Relations | Textbooks | Languages | Curriculum |
|---------|:--------:|:---------:|:---------:|:---------:|:----------:|
| **Mathematics** | 574 | 3,538 | 68 | ZH/EN/DE | ✅ NRW + UK + US |
| **Physics** | 366 | 383 | 94 editions | ZH/EN/DE | ✅ NRW |
| **Chemistry** | 220 | 215 | 18 editions | ZH/EN/DE | ✅ NRW |
| **Total** | **1,160+** | **4,100+** | **180+** | **3** | **4 systems** |

---

## ✅ Extraction Validation

**92 gold-standard annotations** across 2 domains and 3 languages (qwen-plus, Bailian API):

| Domain | ZH F1 | DE F1 | EN F1 | Overall | n |
|--------|:-----:|:-----:|:-----:|:-------:|:-:|
| **Social** | **0.974** | **0.949** | **0.882** | **0.939** | 72 |
| **Mathematics** | 0.857 | 0.506 | 0.711 | 0.674 | 20 |
| **All** | **0.974** | **0.949** | **0.882** | **0.939** | **92** |

> Error analysis shows 29% of errors are from very short responses (1-2 words), 40% from partial omissions — no systematic misdirection. See [`docs/paper/02_methodology.md`](docs/paper/02_methodology.md) for details.

---

## 🚀 Quick Start

### Requirements
- **Python 3.10+**
- **Bailian API key** ([free quota: 1M tokens per model](https://bailian.console.aliyun.com/))
- **LM Studio** (optional, for local inference)

### 1. Set up

```bash
git clone https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph.git
cd BWKI-2026-LinguaGraph
pip install openai numpy
export BAILIAN_API_KEY="your-api-key"
```

### 2. Validate extraction quality

```bash
python scripts/evaluate_gold.py --status
python scripts/batch_process_responses.py --gold-only
python scripts/evaluate_gold.py
```

### 3. Run full pipeline

```bash
# Generate 300-response simulation baseline
python scripts/simulate_baseline.py --mock

# Extract all survey responses
python scripts/extract_all_via_api.py

# Compute LDS
python scripts/compute_lds_from_db.py
```

### 4. Test any model

```bash
python scripts/batch_process_responses.py \
  --model qwen-plus --gold-only
```

---

## 🧪 Model Benchmark

20 models tested on identical gold labels:

| Model | ZH F1 | DE F1 | EN F1 | Speed |
|-------|:-----:|:-----:|:-----:|:-----:|
| **qwen-plus** (social) | **0.974** | **0.949** | **0.882** | 2-3s |
| qwen3.7-max | 0.980 | 0.551 | 0.778 | 2-3s |
| glm-4.6 | 0.951 | 0.595 | 0.689 | 10-20s |
| qwen-turbo | 0.714 | 0.448 | 0.810 | 1s |

Full results: [`research/findings/bailian_benchmark_complete.json`](research/findings/bailian_benchmark_complete.json)

---

## 📁 Repository Structure

```
├── scripts/              # Analysis pipelines (batch extraction, evaluation, benchmark)
├── docs/
│   ├── paper/            # Full research paper (abstract → conclusion)
│   ├── review/           # Quality audits & critical assessments
│   └── creative_submission.md  # BWKI submission (June 28)
├── config/
│   ├── expert_graphs/    # Knowledge graphs (JSON) — Math, Physics, Chemistry, Curricula
│   └── concept_mapping.json    # 174 cross-lingual concept alignments
├── cognitive-space/      # 3D visualization (Three.js) — browser-ready
├── research/findings/    # Benchmark outputs, evaluation reports
└── linguaGraph.db        # SQLite database (local, gitignored)
```

---

## 📚 Literature

Key works motivating and contextualizing this research:

| Area | Reference | Link |
|------|-----------|------|
| **Concept Maps** | Novak & Cañas (2008) — *The theory underlying concept maps* | [ResearchGate](https://www.researchgate.net/publication/228633562) |
| **Assimilation Theory** | Ausubel (1963) — *The psychology of meaningful verbal learning* | — |
| **Curriculum Coherence** | Schmidt et al. (2001) — *Why schools matter* (TIMSS) | [TIMSS](https://timssandpirls.bc.edu/) |
| **Cross-National Textbooks** | Liang & Heckmann (2013) — Comparing German & Chinese math textbooks | [ZDM](https://link.springer.com/article/10.1007/s11858-013-0492-1) |
| **Linguistic Relativity** | Boroditsky (2001) — *Does language shape thought?* | [Cognitive Psychology](https://doi.org/10.1006/cogp.2000.0740) |
| **Knowledge Graphs** | Alatrash et al. (2025) — Prerequisite structure extraction with LLMs | *In submission* |
| **Curriculum Analysis** | Ain et al. (2025) — CS curriculum mapping | — |
| **CDS/HDS/LDS** | Siew (2019) — Network science in education | [Springer](https://link.springer.com/chapter/10.1007/978-3-030-14474-6_12) |
| **Educational Philosophy** | OECD (2023) — *Education at a Glance* | [OECD](https://www.oecd.org/education/education-at-a-glance/) |

---

## 🔬 For Researchers

- **Paper**: Full manuscript in [`docs/paper/`](docs/paper/) (EN/DE mixed)
- **Creative Submission**: [`docs/creative_submission.md`](docs/creative_submission.md) (DE, submitted June 28)
- **Poster**: Poster structure in creative submission
- **Citation**: Use the repository's CITATION.cff or cite this work as:

> Rongjing, J. (2026). *LinguaGraph: Cross-Lingual Knowledge Structure Analysis Framework*. BWKI 2026. GitHub: https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph

---

## 📜 License & Compliance

- **License**: All Rights Reserved — BWKI 2026 competition project
- **Privacy**: Participant data is fully anonymized. No PII stored in repository. See [`docs/ethics/`](docs/ethics/) for GDPR compliance documentation.
- **AI Ethics**: LLM usage is limited to concept extraction from textbook text. No synthetic participant data is presented as human data.
- **Data Sources**: Textbook excerpts used for academic research under fair use/citation principles. All sources documented in graph metadata.

---

## 🤝 Contact & Community

- **Competition**: [BWKI 2026 — Bundeswettbewerb Künstliche Intelligenz](https://www.bw-ki.de/)
- **Repository**: [github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph](https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph)
- **3D Visualization**: Open [`cognitive-space/web/index.html`](cognitive-space/web/index.html) in your browser
- **Author**: Rongjing J. — 15-year-old researcher, bilingual (ZH/DE), passionate about AI, linguistics, and education

<p align="center">
  <sub>Built with ❤️ for BWKI 2026 — because knowledge should be understood, not just taught.</sub>
</p>

---

<p align="center">
  <a href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/stargazers">
    <img src="https://img.shields.io/github/stars/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph?style=social" alt="Star">
  </a>
  <a href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/network/members">
    <img src="https://img.shields.io/github/forks/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph?style=social" alt="Fork">
  </a>
</p>
