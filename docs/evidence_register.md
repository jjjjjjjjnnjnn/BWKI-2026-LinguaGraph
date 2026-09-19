# LinguaGraph — Evidence Register

> **Purpose**: Maps each scientific claim to its supporting evidence, maturity level, and confidence.
> **Principle**: All claims must be traceable to evidence. Claims without sufficient evidence are labeled as such.
> **Updated**: 2026-09-14 (C9 split C9a/C9b; social F1 Developing pending 72-label blind review)

---

## Register

| # | Claim | Evidence Stream | Supporting Data | Maturity | Confidence | Notes |
|---|-------|:---------------:|----------------|:--------:|:----------:|-------|
| C1 | Educational knowledge follows an "integrate-early, diverge-late" pattern across disciplines | LDS-K | CDS by education level: Math (0.271@Middle → 0.041@College), Physics (0.222@Elementary → 0.035@College), Chemistry (0.042@Middle → 0.030@College) | **Mature** | **High** | Consistent across 3 disciplines, 3 languages |
| C2 | Prerequisite depth is universally bounded | LDS-K | HDS max 8 (Math), 6 (Physics); 83% of math concepts are root nodes | **Mature** | **High** | BFS on 3,538 prerequisite relations |
| C3 | Cross-linguistic knowledge structure relationships are heterogeneous | LDS-K | ZH-DE=0.519 (convergence), ZH-EN=0.934 (near noise floor), DE-EN=0.938 (near noise floor) | **Mature** | **Medium** | DOWNGRADED 2026-09-12: ZH-DE raw is contamination artefact (T1 decontaminated 0.990); convergence reading SUPERSEDED by C16 |
| C4 | Within-language variation sets a noise floor for LDS interpretation | LDS-K | Within-language split-half LDS ≈ 0.97; cross-language pairs at 0.52–0.94 | **Mature** | **High** | Null Model Suite finding |
| C5 | Textbook structures converge more than random expectation | LDS-K | Full < Structure Null for all language pairs | **Mature** | **High** | Fundamental reframing of LDS |
| C6 | LDS-K cannot be interpreted as "language-driven divergence" | LDS-K | All three language pairs at or below within-language noise floor | **Mature** | **High** | Core narrative shift |
| C7 | ΔLDS = LDS-C − LDS-K shows heterogeneous patterns across language pairs | LDS-C + LDS-K | Pilot N=8: DE-ZH ΔLDS=+0.232, ZH-EN ΔLDS=−0.230, DE-EN ΔLDS=−0.211 | **Developing** | **Medium** | DOWNGRADED 2026-09-12: N=8 pilot superseded by N=15 (C17); do not cite without C17 |
| C8 | Human concept structures vary systematically across languages | LDS-C | N=8 pilot: DE-ZH=0.751, DE-EN=0.727, ZH-EN=0.704 | **Developing** | **Low** | DOWNGRADED 2026-09-12: superseded by N=15 null result (C17); N>=30 still ausstehend |
| C9a | Gold-standard extraction quality, math batch (clean) | LDS-K / LDS-C | Math F1=0.674 (n=20: 7 ZH / 7 DE / 6 EN), hand-annotated from scratch (`annotator_1`) | **Mature** | **High** | Batch A; no seed-evaluation overlap |
| C9b | Gold-standard extraction quality, social batch (seed-confounded) | LDS-K / LDS-C | Social F1=0.939† (n=72: 29 ZH / 22 DE / 21 EN), machine-seeded (qwen-plus temp 0.3) + human-accepted (`auto_accepted`); target 100 → realized 92 (8 empty dropped); independent harness social ~0.65 vs DB path 0.939 (qwen-plus math 0.7244/social 0.6497; qwen-max 0.7068/0.6483; ranking +0.0176 holds on clean math) | **Developing** | **Medium** | DOWNGRADED 2026-09-14 (2B): pending full 72-label blind review; `research/gold_review/` missing (documented gap); details G3 `research/gold_deconfound_2026-09-14.md` |
| C10 | 19 LLMs show consistent F1 range across API platforms | Method | hy3-preview 0.6741 (N=57), mimo-v2.5-pro 0.6735 (N=75), qwen-plus 0.6659 (N=92); range 0.55–0.67 | **Mature** | **High** | 3 API platforms; N varies 57–92 per model (failures excluded — disclosed `docs/figure_first_design.md:99-119`); gold contains 72 qwen-seeded labels → qwen-family ranks carry home advantage (G3); narrowed claim: family-range robustness only, not exact ranks; selection rationale = full N=92 + top-3 |
| C11 | Curriculum–textbook coverage varies dramatically by educational governance | LDS-K | NRW 12.7%, UK 37.3%, US 17.2%, CN 95.4% | **Mature** | **High** | Coverage Score methodology |
| C12 | Spatial granularity varies substantially within a single language | LPA | DE pilot N=6: SGS criteria 3/9–9/9 | **Exploratory** | **Low** | IRR pending; N=6 only |
| C13 | Temporal metaphor ambiguity replicates in naturalistic production | LPA | DE pilot N=6: 1/5 T+, 3/5 T?, 1/5 T~ | **Exploratory** | **Low** | N=6 only; consistent with Boroditsky (2000) |
| C14 | Bilingual code-switching occurs in concept-explanation tasks | LPA | DE pilot N=6: 2/6 true bilingual explanations | **Exploratory** | **Low** | N=6 only |
| C15 | Social script strategies show high intra-lingual pragmatic variation | LPA | DE pilot N=6: 6 distinct strategy types | **Exploratory** | **Low** | N=6 only |
| C16 | ZH-DE LDS-K "convergence" is a CJK-label contamination artefact | LDS-K | T1: 167/219 ZH-DE edges carry CJK de-labels; J 0.556→0.020, LDS 0.52→0.990 after decontamination; Fig8 | **Mature** | **High** | SUPERSEDES the convergence reading of C3 (2026-09-12) |
| C17 | No separable language signal in human between-subject data (N=15) | LDS-C | pooled 0.963/0.932/0.936 ≈ floor 0.959/0.924/0.922; permutation p=0.08/1.0/1.0 (n_iter=200, fragile — needs_review) | **Developing** | **Medium** | Negative result; C7 pilot superseded |
| C18 | Within-subject LLM data shows clear language-code signal | LDS-C | LLM 0.955/0.930/0.945 vs floor 0.875/0.846/0.862; margin +0.08–0.09; permutation p<0.01 | **Mature** | **High** | Same amplitude as human, floor separated |
| C19 | 59-model replication: ZH-DE separable in every model | LDS-C | 62 ok runs (61×n=30 + qwen-max n=26) / 57 identities / 186 pairs; ZH-DE 59/59 formal at p<0.004 (500 perm. resolution limit); 9 EN n.s. | **Mature** | **High** | Public headline 59/54/177 (qwen-max partial withheld); file truth 62/57/186 |
| C20 | Published CDS/HDS values are frozen June-2026 dense-graph outputs | LDS-K | CDS middle 46/280→0.271, high 175/1113→0.073; HDS 556/459/8/0.40; pipeline lost, 16+96 exhaustion negative | **Mature** | **High** | Frozen + forensic notes (fig3/fig5); not recomputable, direction intact |
| C21 | Seed-independent re-extraction: v1-non-repro → v2-partial-repro (quantitative) | Method | v1: 6 seed-fremde Arme social 0.102–0.148 (A2); v2 (A11–A17, 3 Anker + Western): P1−P0 dF1 +0.27–+0.41, P3 social 0.40–0.58 (deepseek 0.544 V2-validated; glm 0.544 drift-caveated; 6.8 0.395 marginal miss); beide A5-Äste verfehlt; DB 0.939 vs harness-qwen ~0.65 vs v2 ~0.5 → C9b bleibt Developing | **Developing** | **High** | Prereg A1–A10 + v1.2 (A11–A17); REPORT §7; `V2_MATRIX.json` |
| C22 | §2.3 textbook extractions are model-dependent (low cross-model agreement) | Method | T1 (11 Basen, deterministischer Match): micro-P vs. mimo 0.21–0.32, rel_agree 0.8–2.0/Datei; konsistent mit Ensemble vs-mimo 0.22–0.26 | **Developing** | **Medium** | Baseline-relativ (mimo unverifiziert); `T1_AGREEMENT.md` |
| C23 | Gold harness v1 conflates prompt-obedience with extraction quality (v2-confirmed) | Method | v2-Faktor-Test: CARD-fix hebt F1 um +0.27–+0.41 (2× drift-sauber); LANG-fix befolgt (EN-CJK →0 %) ohne EN-Lift (Modell-Seite); P3 social 0.40–0.58 | **Developing** | **High** | v2-Datenbefund (A11–A17); REPORT §7; Empfehlung Harness v2 (P3) als Default |
| C24 | Western-model EN advantage under P3 (language familiarity) | Method | big-pickle P3 (92/92): EN 0.377 höchst (glm 0.315, deepseek 0.215, 6.8 0.037); overall 0.608/social 0.580; P0-Kontrolle partial-46 (paired n=46, d=+0.32) | **Developing** | **Medium** | v2-Datenbefund; Western-Rater-Kandidat für Panel Phase 2 |

---

## Summary by Evidence Stream

| Stream | Total Claims | Mature | Developing | Exploratory |
|--------|:-----------:|:------:|:----------:|:-----------:|
| **LDS-K** | C1–C6, C9a, C9b, C11, C16, C20 | **10** | **1** | 0 |
| **LDS-C** | C7–C8, C17–C19 | **1** | **3** | 0 |
| **LPA** | C12–C15 | 0 | 0 | **4** |

> LDS-K total 11 (10 Mature + 1 Developing: C9b social batch pending blind review) — v25 Gold-Provenance-Härtung 2026-09-14.

---

## IRR Status (2026-07-01)

| Dimension | Mean κ | Criteria ≥ 0.70 | Status |
|-----------|:------:|:---------------:|:------:|
| D1 Spatial | 0.801 | 9/13 (69%) | ✅ Above threshold; 4 criteria need revision |
| D2 Temporal | 0.400 | 0/1 (0%) | 🔧 Codebook revision needed (refusal handling) |
| D3 Flexibility | 0.851 | 10/14 (71%) | ✅ Above threshold; 4 criteria need revision |
| D4 Lexical | 0.515 | 3/10 (30%) | 🔧 Major revision needed; free association criteria low |
| **Overall** | **0.782** | **19/30 (63%)** | ✅ Above 0.70; next target: 80%+ at N=20 |

**Next**: Revise codebook v0.3 → recode → 20-sample IRR with 2nd human coder.

---

## Principles for Updating

1. **New claims** require an entry before they appear in any discussion or conclusion.
2. **Maturity promotion** (Exploratory → Developing → Mature) requires documented evidence (sample size, κ, effect size, null model).
3. **Confidence downgrade** (High → Medium → Low) is explicitly permitted when new evidence conflicts with prior claims.
4. **Superseded claims** are marked as `SUPERSEDED` with a pointer to the replacing claim, not deleted.
5. **Pending claims** (e.g., "ΔLDS will confirm language-driven cognitive divergence") are flagged as `PENDING` with the required evidence threshold.
