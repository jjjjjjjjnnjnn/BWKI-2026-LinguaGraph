# Pre-release check 2026-09-16 (SSOT: research/numbers_ssot_20260916.json)

Scope: docs/paper/, docs/submission/, submission/final/, submission/pitch/, cognitive-space/portal/index.html, README*.md. Figures: docs/paper/ + portal (+ mirrors outputs/figures/, cognitive-space/figures/, cognitive-space/web/figures/). Generators: scripts/figures/, scripts/figures_i18n*.py, scripts/tools/.

## 1. Banned-phrase sweep (hit = FAIL item)

Banned list: "inter 0.5009 trend" / "vote totals 546/203/884/1905/70 as final" / "bare F1 without Developing suffix" / "vectors confirm LDS-K" / "model failed".

| # | Phrase | docs/paper/ | docs/submission/ | submission/final/ | submission/pitch/ | portal/index.html (current) | README*.md |
|---|--------|-------------|------------------|-------------------|-------------------|-----------------------------|------------|
| 1 | inter 0.5009 (trend use) | 0 | 1 FAIL: docs/submission/BASELINE_LEDGER.md:89 (`inter 0.5009`, ledger line with thr note) | 1 FAIL: submission/final/BASELINE_LEDGER.md:89 (same copy) | 0 | 0 | 0 |
| 2 | 546/203/884/1905/70 as final | 0 | 1 FAIL: docs/submission/BASELINE_LEDGER.md:90 (ledger vote line) | 1 FAIL: submission/final/BASELINE_LEDGER.md:90 (same copy) | 0 | 0 | 0 |
| 3 | bare F1 without Developing | 0 (spot-check: 0.939/0.94 always with Developing C9b + harness ~0.65 + blind-pending, e.g. 02_methodology.md:162-180, 04_discussion.md:102) | 0 | 0 | 0 | 0 (F1 stat carries Developing + harness + blind-pending, index.html:292) | 0 |
| 4 | vectors confirm LDS-K | 0 | 0 | 0 | 0 | 0 (Tier-2 worded as control-only, rank-order-only, index.html:333-335; the negated warning string lives only in index.v1-20260916.html:851 archive, not headline) | 0 |
| 5 | model failed | 0 | 0 | 0 | 0 | 0 ("8 bare-hosts" at index.html:361 is host wording, not a model-failed claim) | 0 |

Notes: ledger hits are inside BASELINE_LEDGER context lines that also cite thr sensitivity, not headline claims — but per strict 0-hit rule they are FAIL items (2 files, same 2 lines mirrored). research/ + docs/BASELINE_LEDGER.md + session_handoff files contain 0.5009/vote strings outside the tasked scope and were not counted. submission/pitch/video_script.md has no banned string but cites stale roster "55/50" (line 52-55) vs SSOT 59/54/177 — fix before recording, not counted as banned hit.

Section verdict: NOGO (2 files x 2 mirrored ledger lines must be reworded or removed from submission copies before release).

## 2. Figure integrity (source file + generating script; orphans)

docs/paper/ holds no local *.png/*.svg/*.jpg and no `![]` embeds; figures are referenced by path/name only: Fig4 + Fig8 (02_methodology.md:153), Fig8 + CDS/HDS frozen values (03_results.md:10,125), Abb.6 fig6_cds_comparison (06_physics_results.md:55), Fig.8 (00_three_conclusions.md:44, 04_discussion.md:168).
Current cognitive-space/portal/index.html holds zero `<img>` figure embeds (only CSS .figure-box + lightbox shell); v1 archive (index.v1-20260916.html:455-458,738-744,771-799) embedded fig2_lds_flow, fig3_cds_by_level, fig7_three_subject_cds, fig5_hds_distribution, fig4_null_model, fig8_lds_decontamination from ../figures/.

| Figure (mirror sets: outputs/figures/ 77 files, web/figures/ 60, cognitive-space/figures/ 8) | Source / generator | Status |
|---|---|---|
| fig4_null_model(.png/_de/_zh + data.csv) | scripts/figures/fig4_null_model.py + _lds_utils.py::lds_jaccard, log reproduce_lds_binary.log | traced |
| fig8_lds_decontamination(.png/_de/_zh + data.csv) | scripts/figures/fig8_lds_decontamination.py (deterministic snapshot) | traced |
| fig1_lds_k_heatmap | scripts/figures/fig1_lds_k_heatmap.py | traced |
| fig2_lds_flow | scripts/figures/fig2_lds_flow.py | traced |
| fig5_falsification | scripts/figures/fig5_falsification.py | traced |
| fig6_coverage | scripts/figures/fig6_coverage.py | traced |
| fig_wikipedia_lds | scripts/figures/fig_wikipedia_lds.py | traced |
| fig_a7_1..5 | scripts/figures/fig_a7_core.py | traced |
| fig3_cds_by_level / fig7_three_subject_cds | scripts/figures_i18n.py:120,154 (+ wave2 overlay) | traced (i18n path) |
| fig4_lds_heatmap (legacy) | scripts/figures_i18n_wave2.py:245,566 (linguaGraph.db WIKIPEDIA_CORPUS, superseded, kept for reference) | traced as legacy |
| figure1_lds_distribution / figure3_topic_comparison | scripts/pilot_pipeline.py:306-340 (pilot) + figures_i18n_wave2.py:1022,1086 overlays | traced as pilot-only |
| Two-Tier vectors control | scripts/tools/openweight_embed_audit.py | traced (control baseline) |
| ORPHAN fig5_hds_distribution.png | no primary generator found; self-disclosed frozen bars, source graph superseded (portal README.md:79; v1 label docs/fig5_hds_forensic.md) | ORPHAN (disclosed, do not re-render) |
| ORPHAN fig4_ablation.png (outputs/figures/) | no script in scripts/figures/; only wave2 overlay entry | ORPHAN |
| ORPHAN fig6_cds_comparison.png | data 8ad379a physics_comparison.json + wave2 overlay-only (:297,876); no primary matplotlib generator in scripts/figures/ | ORPHAN (data-traced, generator-missing) |
| ORPHAN pitch_poster.jpg, favicon.svg, web/ portal_hero*.png, screenshot*.png, steam_overview*.png | manual export/screenshot, no script | ORPHAN (expected; keep as static assets, label as such) |
| Naming collision | v1 portal uses "Fig 8" for both LDS decontamination (:798) and coverage score (:871) | FIX before release |

Section verdict: NOGO (3 generator-orphan PNGs + Fig8 collision + current index.html ships zero figure embeds while v1/PDF still cite Figs 3/4/5/7/8; either restore embeds or point portal to web/figures/ mirror explicitly).

## 3. Reporting self-check (minimal STROBE-like, vs docs/paper/*.md)

| Item | Result |
|---|---|
| Methods present | PASS: 02_methodology.md (extraction qwen-plus, align 219 groups, LDS 2-comp freeze, null-test 500 perms, replication §5.10, bench §8.9, tool/provenance ledger :232); App W gates exploratory-only |
| Results present | PASS: 03_results.md (CDS/HDS/LDS-K + N=15 LDS-C + LLM within-subject + replication), 06_physics_results.md, 07_lpa_analysis.md (N=6 pilot, N>=120 planned), 08_appendixW (E1/E1b/E3 EXECUTED, Hypothesis/PENDING) |
| Limitations present | PASS: 04_discussion.md:140-182 (same-source, N=15 between-design, extraction method, edge sparsity) + 05_conclusion.md:59-63 + portal limits (index.html:371-378) |
| Sample sizes stated | PASS: human N=15 (6/6/3), pilot N=8 (0.704/0.727/0.751 placeholder, no claim); gold 92 (20 C9a + 72 C9b); bench 19 models F1 0.55-0.67; replication 59/54/177 + file-truth 62/57/186; collecting 26; perms 500 (resolution 0.004) |
| Absent-data disclosed | PASS: 23 incomplete + 2 sparse-boundary + 1 quarantine; qwen-max n=26/30 parked; 5 dual-host models (59 vs 54); 9/177 EN n.s.; luna provenance; HF SHAs UNVERIFIED; phi community-quant break (04_discussion.md:222-226, App W) |
| Heuristic labels kept | PASS: Developing C9b + harness ~0.65 + blind-pending on every 0.939; margin >=0.10 heuristic; Youden heuristic; App W n=3 no-power + Hypothesis/PENDING; pilot placeholder no pass/alarm |

Residuals (non-blocking but fix): video_script.md stale 55/50 roster; Fig8 double-use; current portal dropped forensic/method boxes present in v1.

Section verdict: GO (with listed residuals fixed opportunistically; no blocking misreporting found in paper markdown).
