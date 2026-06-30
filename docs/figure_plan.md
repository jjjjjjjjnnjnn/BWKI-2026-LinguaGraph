# BWKI Paper — Figure Plan

**Project**: LinguaGraph — BWKI 2026
**Date**: 2026-06-17
**Paper Language**: German (BWKI official)
**Total Figures**: 7

---

## Figure 1: System Architecture (Pipeline Overview)

**Section**: Method / Methode
**Position**: Early in Method section, after pipeline description

### Content
```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Survey   │ →  │ LLM      │ →  │ Graph    │ →  │ Cross-   │
│ Response │    │ Extract  │    │ Build    │    │ Language │
│ (ZH/DE/  │    │ Concepts │    │ NetworkX │    │ Compare  │
│  EN)     │    │ + Rels   │    │          │    │ LDS      │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     ↓               ↓               ↓               ↓
  CSV/JSON      Extractions     Graphs         LDS Scores
  (raw)         (structured)    (per lang)     (per pair)
```

### Specifications
- **Type**: Flowchart / process diagram
- **Tool**: Draw.io or Mermaid → export as SVG
- **Size**: Full width (170mm for A4)
- **Color**: Grayscale with blue accents for key outputs
- **Labels**: Bilingual (German primary, English in parentheses)
- **Data source**: `src/main.py` pipeline structure

### Key Elements to Show
1. Input: Trilingual survey responses
2. Processing: LLM concept extraction (src/extract.py)
3. Processing: Graph construction (src/graph.py)
4. Processing: Concept mapping (config/cross_language_mapping.json)
5. Output: LDS scores (src/scoring.py)

---

## Figure 2: LDS Calculation Flow

**Section**: Method / Methode (sub-section on LDS)
**Position**: After Figure 1, explaining the core metric

### Content
```
For each topic:
  Language Pair (e.g., ZH-DE)
      ↓
  Extract concepts from ZH responses → Graph_G_ZH
  Extract concepts from DE responses → Graph_G_DE
      ↓
  Apply concept mapping (cross-language alignment)
      ↓
  Calculate edge overlap:
    LCD = 1 - (|E_ZH ∩ E_DE| / |E_ZH ∪ E_DE|)
      ↓
  LDS = mean(LCD across all pairs)
```

### Specifications
- **Type**: Mathematical flowchart
- **Tool**: Draw.io or TikZ
- **Size**: Full width
- **Includes**: Formula block for LDS computation
- **Data source**: `src/scoring.py:93-135` (calculate_lcd_score)

### Key Elements to Show
1. Input: Two language graphs for same topic
2. Concept mapping step
3. Edge set intersection/union
4. LCD formula
5. LDS aggregation

---

## Figure 3: Top Drift Ranking (LDS by Topic)

**Section**: Results / Ergebnisse
**Position**: First results figure, establishing main finding

### Content
Horizontal bar chart:
```
ZH-EN          ████████████████████ 0.934
DE-EN          ████████████████████ 0.938
ZH-DE          ██████████░░░░░░░░░░ 0.519
```

### Specifications
- **Type**: Horizontal bar chart
- **Tool**: matplotlib + seaborn (Python)
- **Size**: 170mm × 100mm
- **Color**: Gradient from red (high drift) to blue (low drift)
- **Error bars**: Std dev across language pairs
- **Annotations**: LDS value labels on bars
- **Data source**: `research/findings/bwki_analysis_report.md` (LDS values)
- **Output**: `docs/figures/fig3_top_drift.png` (300 DPI)

### Data
```python
pairs = ["ZH-EN", "DE-EN", "ZH-DE"]
lds_values = [0.934, 0.938, 0.519]
lds_std = [0.02, 0.02, 0.05]  # approximate from bootstrap
```

---

## Figure 4: Cognitive City (3D Visualization Screenshot)

**Section**: Results / Ergebnisse or Visualization section
**Position**: After quantitative results, showing qualitative visualization

### Content
Screenshot of Three.js Cognitive City showing:
- 3 cities (ZH red, EN blue, DE gold) side by side
- Buildings representing concepts (height = centrality)
- Roads representing relationships (width = strength)
- Bridges connecting equivalent concepts across cities
- LDS bars at bottom showing drift scores

### Specifications
- **Type**: Screenshot / rendered image
- **Source**: `visualization_v3/index.html` (Task 2 output)
- **Resolution**: 1920×1080 (Full HD)
- **Capture method**: Browser screenshot or Three.js `toDataURL()`
- **Topic shown**: "ZH-DE" (most interesting convergence, LDS=0.519)
- **View**: Overview angle showing all 3 cities
- **Output**: `docs/figures/fig4_cognitive_city.png`
- **Caption**: "Cognitive City für das Konzept 'Freiheit'. Gebäudehöhe = Zentralität der Konzepte, Straßenbreite = Stärke der Beziehungen, Brücken = äquivalente Konzepte über Sprachen hinweg."

### Capture Settings
```javascript
// In visualization_v3:
renderer.render(scene, camera);
const dataURL = renderer.domElement.toDataURL('image/png');
// Or use html2canvas for full HUD capture
```

---

## Figure 5: Human vs Simulation Comparison

**Section**: Results / Ergebnisse (Computational Control Model)
**Position**: After Figure 3, showing validation of simulation baseline

### Content
Scatter plot:
```
Y (Human LDS)
  1.0 │         × Success
      │       × Responsibility
  0.8 │     × Justice    × Freedom
      │   × Home
  0.6 │
      │
  0.4 │
      └──────────────────────────
        0.4   0.6   0.8   1.0
              X (Simulation LDS)

Regression line: y = ax + b
ρ = [value] (Spearman)
```

### Specifications
- **Type**: Scatter plot with regression line
- **Tool**: matplotlib + scipy
- **Size**: 120mm × 100mm (square-ish)
- **Points**: 5 topics, labeled
- **Regression**: Linear fit with 95% CI band
- **Reference line**: y=x (perfect agreement, dashed)
- **Color**: Points in project blue (#4a7dff)
- **Annotations**: ρ value, equation, R²
- **Data source**: `research/findings/human_vs_model_comparison.json` (after pipeline run)
- **Output**: `docs/figures/fig5_human_vs_simulation.png`

### Fallback
If human data is not yet available, use Wikipedia LDS vs Simulation LDS comparison with placeholder annotation "Pilot data pending".

---

## Figure 6: Questionnaire Results (Survey Response Patterns)

**Section**: Results / Ergebnisse (Human Study)
**Position**: After Figure 5, showing human data analysis

### Content
Grouped bar chart showing concept frequency per language:
```
                ZH        DE        EN
Freedom:    [family,  [rights,  [choice,
             society]   law]      liberty]

Success:    [effort,  [career,  [achievement,
             family]   skill]    opportunity]
```

Or radar chart per topic showing concept profiles across languages.

### Specifications
- **Type**: Grouped bar chart OR radar chart (depending on data richness)
- **Tool**: matplotlib / plotly
- **Size**: 170mm × 120mm
- **Axes**: Concepts (x) × Frequency (y), grouped by language
- **Color**: ZH=red, DE=gold, EN=blue (consistent with project palette)
- **Data source**: Pilot/main study responses after pipeline processing
- **Output**: `docs/figures/fig6_survey_results.png`

### Fallback
If pilot data not yet available, show Wikipedia-based concept frequency comparison with annotation "Pilot data: N=9".

---

## Figure 7: Concept Overlap Heatmap

**Section**: Results / Ergebnisse (Cross-language Analysis)
**Position**: After Figure 6, showing cross-language concept sharing

### Content
Heatmap matrix:
```
              ZH-EN    ZH-DE    DE-EN
Freedom:      0.61     0.82     0.87
Justice:      0.70     0.89     0.88
Responsibility:0.77    0.88     0.84
Success:      0.92     1.00     1.00
```

### Specifications
- **Type**: Heatmap
- **Tool**: seaborn (Python)
- **Size**: 120mm × 100mm
- **Color scale**: White (0) → Blue (1) (sequential)
- **Cell text**: Numeric Jaccard value
- **Annotations**: Significance stars (* p<0.05, ** p<0.01)
- **Data source**: `research/findings/` cross-language JSON files
- **Output**: `docs/figures/fig7_concept_heatmap.png`

### Data
```python
import seaborn as sns
data = {
    "Freedom": [0.614, 0.821, 0.872],
    "Justice": [0.699, 0.891, 0.877],
    "Responsibility": [0.773, 0.881, 0.838],
    "Success": [0.917, 1.000, 1.000],
}
```

---

## Summary Table

| Fig | Title | Type | Section | Data Source | Status |
|-----|-------|------|---------|-------------|--------|
| 1 | System Architecture | Flowchart | Method | Pipeline design | Ready to draw |
| 2 | LDS Calculation | Math flowchart | Method | src/scoring.py | Ready to draw |
| 3 | Top Drift Ranking | Bar chart | Results | Existing LDS data | Ready to plot |
| 4 | Cognitive City | Screenshot | Results | visualization_v3 | Needs Task 2 |
| 5 | Human vs Simulation | Scatter plot | Results | Needs pilot data | Placeholder ready |
| 6 | Survey Results | Grouped bar | Results | Needs pilot data | Placeholder ready |
| 7 | Concept Overlap | Heatmap | Results | Existing LDS data | Ready to plot |

---

## Figure Production Pipeline

```python
# For each figure:
# 1. Prepare data (JSON/CSV)
# 2. Generate plot (matplotlib/seaborn)
# 3. Export as PNG (300 DPI)
# 4. Add German captions
# 5. Place in docs/figures/

# Example for Figure 3:
import matplotlib.pyplot as plt
import seaborn as sns

topics = ["ZH-EN", "DE-EN", "ZH-DE"]
lds = [0.934, 0.938, 0.519]
colors = sns.color_palette("RdYlBu_r", len(topics))

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.barh(topics, lds, color=colors)
ax.set_xlabel("Language Drift Score (LDS)")
ax.set_title("Top Drift Ranking nach Konzept")
for bar, val in zip(bars, lds):
    ax.text(val + 0.01, bar.get_y() + bar.get_height()/2, f"{val:.3f}", va='center')
plt.tight_layout()
plt.savefig("docs/figures/fig3_top_drift.png", dpi=300)
```

---

## German Caption Templates

**Fig 1**: "Abbildung 1: LinguaGraph-Pipeline — Von der Datenerhebung bis zum Language Drift Score"

**Fig 2**: "Abbildung 2: Berechnung des Language Drift Score (LDS) durch Graphvergleich"

**Fig 3**: "Abbildung 3: LDS-K nach Sprachpaar — ZH-EN 0.934, DE-EN 0.938, ZH-DE 0.519"

**Fig 4**: "Abbildung 4: Cognitive City — 3D-Visualisierung der kognitiven Strukturen für 'Erfolg'"

**Fig 5**: "Abbildung 5: Human vs. Simulation — LDS-Vergleich (Spearman ρ = [value])"

**Fig 6**: "Abbildung 6: Konzeptverteilung nach Sprache (Pilotstudie, N=9)"

**Fig 7**: "Abbildung 7: Konzept-Overlap Heatmap (Jaccard-Index pro Sprachpaar)"
