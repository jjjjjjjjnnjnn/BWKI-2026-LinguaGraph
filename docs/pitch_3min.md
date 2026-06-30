# LinguaGraph — 3-Minute Pitch

> For project presentations, lab meetings, or short talks

---

## 1. The Problem (30s)

Mathematics is universal. But the way knowledge is organized in textbooks — what comes first, what connects to what, how deep the chain goes — varies dramatically across languages and education systems. Existing curriculum analysis tools are qualitative, manual, and cannot scale across languages or disciplines.

**We need a way to measure these structural differences quantitatively.**

## 2. The Framework (45s)

LinguaGraph builds multi-lingual knowledge graphs from textbook corpora using LLM-based concept extraction (qwen-plus, 92 gold labels, F1=0.939 for social concepts). We then measure four structural indicators:

| Metric | What it measures | Range |
|--------|-----------------|-------|
| **CDS** | How densely connected knowledge is | 0.042–0.271 |
| **HDS** | How deep prerequisite chains go | Max 8 |
| **LDS-K** | How different languages structure the same topic | 0.52–0.94 |
| **CS** | How well textbooks cover official curricula | 12.7%–95.4% |

## 3. The Surprising Findings (60s)

**F1:** Knowledge density peaks at **middle school** (CDS=0.271), not college. The transition to high school brings a **3.7× drop**. Both physics and chemistry follow the same early-peak-later-decline pattern.

**F4:** LDS-K reveals structural **convergence**: ZH-DE=0.519 (convergent), while ZH-EN=0.934 and DE-EN=0.938 approach noise level. Curriculum tradition, not language family, drives this.

**F9:** Coverage scores range from **12.7% (NRW) to 95.4% (China)**. NRW's low score reflects specialization depth, while China's high score reflects broad curriculum alignment.

## 4. The Big Picture (45s)

LinguaGraph is the first framework that can automatically:
- Build multilingual knowledge graphs from textbooks
- Quantify structural differences across languages and disciplines
- Measure textbook-curriculum alignment at scale

**Three disciplines, three languages, four education systems. One framework.**

## 5. Next Steps

- Deepen the Coverage Score analysis across all subjects
- Expand to additional education systems (France, Japan, Singapore)
- Develop interactive exploration tools for education researchers
- Publish the full framework as an open educational resource

---

*Read the full paper at `docs/paper/` · Explore the data at `config/expert_graphs/` · Interactive 3D: `cognitive-space/web/story/`*
