# LinguaGraph Research Portal

> The unified entry point for the LinguaGraph project — findings, data, visualizations and paper.

## Quick Start

Open `index.html` in any browser. No build step required.

## Sections

| # | Section | Content |
|---|---------|---------|
| 1 | Hero | Research question, stat wall (1,140+ concepts, F1=0.939), scope footnote, CTAs |
| 2 | Research Questions | RQ1 (Language), RQ2 (Discipline), RQ3 (Education System) |
| 3 | Contributions | 4 core contributions of the project |
| 4 | Methodology | Pipeline diagram + 4 metric definitions (CDS/HDS/LDS/CS) |
| 5 | Finding A | "Knowledge density peaks early" — CDS across 3 disciplines |
| 6 | Finding B | "Knowledge structures stay shallow" — HDS |
| 7 | Finding C | "Languages organize knowledge differently" — LDS |
| 8 | Finding D | "Education systems differ in curriculum design" — Coverage Score |
| 9 | Finding E | "N=15 falsifies between-subject ΔLDS" — human validation (F11–F12) |
| 10 | CognitiveSpace | Click-to-load 3D viewer (porcelain cover, saves 429KB first paint) |
| 11 | Curriculum | Coverage scores by education system + 3 competing explanations |
| 12 | Validation | Gold dataset F1 table + interactive 19-model benchmark chart |
| 13 | Limitations | 6 methodological boundaries with mitigations |
| 14 | Paper | Citation, BibTeX with copy button |
| 15 | Open Science | Links to code, data, paper, figures, benchmarks |

## Theme

`indigo-porcelain` — same tokens as the BWKI video (`nach/presentation/src/styles/tokens.css`):
porcelain `#f1f3f5`, indigo ink `#0a1f3d`, accent `#1e3a8a`. Playfair Display italic (EN numerals),
Noto Serif SC (CN display), IBM Plex Sans (body), IBM Plex Mono (kickers).

## Tech Stack

- Hand-written CSS (custom properties, no framework)
- Google Fonts (Playfair Display + Noto Serif SC + IBM Plex Sans/Mono)
- Mermaid.js v11 (light theme config, `securityLevel: sandbox`)
- Chart.js v4 (indigo-scale palette)
- Bootstrap Icons
- Vanilla JavaScript (IntersectionObserver reveals, count-up, i18n EN/DE/ZH)

## Numbers (SSOT: `docs/SSOT-web.md`)

- Hero totals = full project: Math 556 + Physics 366 + Chemistry 220 = 1,140+ concepts.
- 3D section = mathematics subgraph only: 556 nodes · 525 relations · 219 groups (`manifest.json`).
- 12 findings (F1–F12, paper §discussion); 19-model benchmark (chart has 19 labels).

## Deployment (`_deploy/` = Pages root mirror)

Source of truth is `cognitive-space/`. After any change, mirror these
(single-direction copy, verify with `Get-FileHash` + `linkcheck.py`):

| Source | Mirror |
|---|---|
| `portal/index.html` + `portal/cspace.html` | `_deploy/portal/` |
| `web/index.html` + `data.js` + `i18n.js` | `_deploy/web/` (portal iframe target) **and** `_deploy/` root (full-screen target) |
| `web/story/index.html` | `_deploy/story/index.html` |
| `web/figures/fig4_null_model.png` | `_deploy/figures/` |
| `docs/submission/LinguaGraph_BWKI2026.pdf` | `_deploy/docs/submission/` |

Known mirror-only patch: `_deploy/index.html` uses `portal/index.html`
(source uses `../portal/index.html`). Never back-port this line to source.

```
https://<user>.github.io/BWKI-2026-LinguaGraph/portal/
```

## Figures

Key figures are in `../web/figures/` (relative path from portal directory).
Deployed set: 14 PNGs (~1.7 MB) — fig3, fig4_null_model, fig7 in EN/DE/ZH
(fig5 EN-only: source graph superseded, see `docs/SSOT-web.md` P2b/D-section),
figure1, figure3 (EN) + legacy fig4_lds_heatmap (superseded, kept for reference).
