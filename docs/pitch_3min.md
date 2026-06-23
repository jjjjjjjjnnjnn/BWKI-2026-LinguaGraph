# LinguaGraph — 3-Minute Pitch

> For project presentations, lab meetings, or short talks

---

## 1. The Problem (30s)

Mathematics is universal. But the way knowledge is organized in textbooks — what comes first, what connects to what, how deep the chain goes — varies dramatically across languages and education systems. Existing curriculum analysis tools are qualitative, manual, and cannot scale across languages or disciplines.

**We need a way to measure these structural differences quantitatively.**

## 2. The Framework (45s)

LinguaGraph builds multi-lingual knowledge graphs from textbook corpora using LLM-based concept extraction (qwen-plus, 92 gold labels, F1=0.939). We then measure four structural indicators:

| Metric | What it measures | Range |
|--------|-----------------|-------|
| **CDS** | How densely connected knowledge is | 0.042–0.271 |
| **HDS** | How deep prerequisite chains go | Max 8 |
| **LDS** | How different languages structure the same topic | 0.80–0.91 |
| **CS** | How well textbooks cover official curricula | 8%–82% |

## 3. The Surprising Findings (60s)

**F1:** Knowledge density peaks at **middle school** (CDS=0.271), not college. The transition to high school brings a **3.7× drop**. Both physics and chemistry follow the same early-peak-later-decline pattern.

**F4:** Chinese and German textbooks show the **highest structural divergence** (LDS=0.907), while Chinese and English are surprisingly close (0.802). Curriculum tradition, not language family, drives this.

**F9:** Coverage scores range from **8% (China) to 82% (UK)**. But China's low score reflects selective depth, not poor alignment — their textbooks go deeper on fewer topics.

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
