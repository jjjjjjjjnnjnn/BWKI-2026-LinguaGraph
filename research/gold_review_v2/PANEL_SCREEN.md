# Agent-Panel Blind-Review Screen (2026-09-19 — falsify/screen ONLY, never matures C9b)

Panel: R1 deepseek-r4 / R2 glm-r4 / R3 sn-6.8 / R4 cohere-openrouter (51/72, daily-quota park) / R5 big-pickle-zen.
Prereg: `docs/osf_preregistration_amendment_A-judge.md` (J1–J7, falsify-only).
Tooling: `scripts/tools/panel_judge.py` + `panel_consensus.py` (deterministic).
J3 leak-grep (2026-09-19, post-hoc): `human_labels|predicted_concepts|gold_dataset` → 0 hits in all 5 panel files. NEGATIVE (no seed leakage into judge outputs).

## Verdict: MAINTAIN — weak, single-run, uncalibrated (stay Developing, C9b)
- Consensus `--import` (`panel_IMPORT.json`): n=72, rejects=15,
  **Gold-Übereinstimmung (vs-gold Jaccard) 0.389** (zh 0.707 / en 0.359 / **de 0.000**),
  qwen-F1 vs consensus-gold 0.419. All gates missed (0.85/0.80/0.70).
  (Vs-gold ≠ inter-rater: paarweise Decision-Übereinstimmung 0.807, Fleiss κ=0.563.)
- Per-rater Gold-Übereinstimmung (`panel_IMPORT.json`): R1 0.520 / R2 0.301 / R3 0.541 /
  R4 0.501 (partial n=51) / R5 0.438.
- Inter-rater: Fleiss κ=0.563 (decisions; below 0.61 substantiality bar — stability unproven),
  pairwise concept-Jaccard 0.44–0.77 (mean ~0.63;
  R1–R3 0.77, R1–R4 0.75, R3–R5 0.72), exact-agreement 20/72 incl. 4-rater items
  (strict 5-rater unanimity: 16/72).
  (BUGFIX 2026-09-19: `panel_consensus.py` had `judged[b]` instead of `judged[b][i]` —
  sb was always empty, old table 0.06–0.28 was wrong; table regenerated, consensus records unchanged.)
- R4 parked after five consecutive 429s at A052–A056 (OpenRouter free daily quota); 51/72 judged, resumes after reset.
  Consensus from A052 on is 4-rater: A055/A068 (4/4 reject), A061/A067 (3/4 fragile reject),
  A071 (2/0/2 edit — single-vote-sensitive) need R4-full before use.

## Methodological reservations (reaudit 2026-09-19 — verdict strength capped by these)
- Single run per item (no test-retest); no position-swap measurement; J3 "per-rater shuffle + seeds logged"
  NOT implemented (deterministic `sorted()` order — new deviation entry D-J1, prereg violation).
- Self-preference uncontrolled: R2 = glm-5.2, same family as a judged anchor; only Qwen was quarantined.
- Task underspecified (no Maybe/Tie/abstain at rater side); `needs_human` is post-hoc derived.
- No human-human κ baseline — judge-human κ (0.563/0.389) has no anchor; human blind review still replaces nothing.
- J3 leak-grep pattern inadequate (pipeline variable names, tautological 0 hits); prompt audit trail only for R5-CLI path.
  True leak audit parked (needs quota: sample_id-in-prompt check, gold-concept overlap, transport logs).
- `n_f1_valid 71 vs 72` in `panel_IMPORT.json` unexplained (open).

## Dissent analysis (the honest core)
- **Unanimous-5 rejects: 11/72 (15%)** — A005/A006/A014/A018/A020/A022/A027/A028/A032/A035/A041.
  Five model endpoints (independence unmeasured — NOT proven "independent families") agree these gold items are unwarranted.
  Pilot 6-persona flagged 7 (A005/A006/A022/A028/A041/A049/A072): overlap 5/7 (A049/A072 NOT confirmed).
- **R2 outlier**: 36 rejects, 13 R2-only excl. A030 (A004/A026/A034/A046/A048/A049/A050/A054/A056/A058/A064/A070/A072;
  A030 has R3/R5-edit votes — NOT R2-only; A054/A056/A058/A064/A070/A072 lack R4 votes, so "noise not signal" is unprovable there).
  R2 (glm) is hyper-critical as judge — rater noise AND uncontrolled self-preference (same family as judged anchor).
- Consensus rejects = 15 (11 unanimous + A055/A068 + 2 majority). needs_human ties: A030/A065/A071.
- Interpretation: raters agree with EACH OTHER moderately-to-strongly (Jaccard ~0.63) but jointly
  diverge from gold (vs-gold 0.389) → `maintain` is genuine gold-vs-rater divergence, NOT rater noise.
  The 11 unanimous rejects weigh heavier under this reading; everything else is undecided.

## Human spot-check list (owner, ~30 min, J7 — note: J7 design needs ≥21 items, this is a reduced 12)
11 unanimous + A065 (needs_human; A030/A071 deferred — A030 has R3/R5-edit votes, A071 needs R4-full first):
`A005 A006 A014 A018 A020 A022 A027 A028 A032 A035 A041 A065`

## What this changes / doesn't
- Changes: gold quality caveat quantified (11/72 unanimous-reject); C9b stays Developing with sharper caveat.
- Doesn't: mature C9b (agents never mature); validate extraction quality; replace human blind review.
- R4-full + human spot-check remain open; rerun consensus then.
