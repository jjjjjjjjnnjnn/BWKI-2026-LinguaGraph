# Stat Methods Review (blind agent B) — 2026-09-16

Scope: judged METHOD from inputs + claimed outputs only.
Read: docs/paper/02_methodology.md, docs/paper/03_results.md (through 5.10),
  docs/BASELINE_LEDGER.md (v21), research/limitations_20260914.md,
  research/numbers_ssot_20260916.json, research/consensus_v4_20260916.md,
  research/thr_sensitivity_v4_20260916.md, research/human_review_ledger_20260916.md,
  docs/planning/osf_preregistration_template.md, docs/paper/04_discussion.md 8.15-8.16.
Not read (blind): scripts/tools/reproduce_headline.py, *rerun*, *recompute*,
  research/stat_rerun_20260916.md, research/reproduce_headline_20260916.*.

## 1. SAP existed? No.

No locked Statistical Analysis Plan exists. `docs/planning/osf_preregistration_template.md`
is an unregistered AsPredicted-style template ("Target: osf.io", "Data collection has
not started"). Gate reviews state the analysis is exploratory without preregistration
(`docs/review/gate_review_layer1_scientific.md`, layer2 statistical). Thresholds
(margin >=0.10, Youden) and n_iter defaults were set/changed post hoc
(LEDGER 2.3, 9). All inferential claims below must therefore be read as exploratory.

## 2. Reconstructed SAP-lock (what should have been locked)

Assumptions: LDS frozen v3 binary `1-mean(J_node,J_edge)` as sole published pipeline
(LEDGER 8a verified); ternary/GED abandoned as unfalsifiable (8d, user decision 2026-09-14);
node-permuted null dropped as power-0 (2.1); hard-match normalization (lowercase +
strip space/hyphen/underscore + ss + synonym map) fixed before scoring.
Sample: human between-subject N=30 target (OSF power d=0.5) — actual N=15 (6 DE/6 ZH/3 EN)
is underpowered placeholder; LLM within-subject k=10 sessions/condition, temp 0.3,
counterbalanced order, independent sessions; replication = availability sample
(84 started, 61x n=30), complete-case rule (n=30 + ZH-DE sig + margin non-NaN) fixed a priori.
Outcomes: primary LDS-C vs split-half floor + label permutation (two-sided, report exact
n_iter and SE(p)); human concept-level DeltaLDS on node-only scale, relational v3 kept
separate (no cross-scale mixing); margin>=0.10 and Youden-0.12 as HEURISTIC only,
banned from headline until CI complete; consensus vote totals banned from headline while
mixed-thr (thr 5/6); missing = not scored, no imputation, no "model failed" language;
gold social F1 reported only with Developing-C9b + same-source + harness-~0.65 suffix
until human blind second review (H1) closes.

## 3. Verdict table

| Item | Verdict | Reason |
|---|---|---|
| Randomization (human) | reject (as confirmatory) | Between-subject, convenience N=15, no random assignment described; valid only as exploratory / negative-result lesson (03 4.6). |
| Randomization/control (LLM P1) | accept-with-note | Within-subject by construction (same weights), counterbalanced order, independent sessions stated (03 5.1); k=10 and temp 0.3 are arbitrary, seed lock not shown in methods. |
| Null-model controls | accept | Three nulls separated (structure / split-half / label-perm / cross-source); power-0 node-permuted honestly retired (LEDGER 2.1); structure-null hash-order fix documented (LEDGER 1). |
| Wikipedia control | accept-with-note | Aligned values disclosed, Latin-only 1.0 artifact voided; but 96 glosses unaudited, no second-model cross (LEDGER 7 needs_review) — directional only. |
| Gold-72 blind protocol | reject (as validated) | Batch B is machine-seeded (qwen-plus) + human-accepted with same-source evaluator confound; harness ~0.65 vs DB-path 0.939 (02 2.8 fn). Human second review is still blocking (H1: external rater, revoke, PROTOCOL 10 second-eyes for 7 rejects). See blindness limits below. |
| Sample-size basis / collecting 26 | accept-with-note | Dual accounting honest: published 59/54/177 vs file-truth 62/57/186; collecting 26 = 23 incomplete + 2 sparse small-model boundary + 1 quarantine; qwen-max n=26/30 parked and disclosed. Note: checkpoint flags 9 untracked 20260913 JSONs pending registry; availability sample, no preregistered matrix (03 5.10, 04 8.15d). |
| SAP lock | reject | No SAP (see 1). Post-hoc thresholds correctly suspended (LEDGER 9 margin, 2.3 human p). |
| Consensus mixed-scale void | accept | Void correct. thr=n//2+1 floats with source count (5 vs 6); totals 546/203/884/1905/70 are mixed-scale sums; thr-sensitivity doc proves drift (683/321 at -1, 426/126 at +1) and SSOT bans headline use. Snapshot-only use is the only honest handling. |
| Youden heuristic | accept-with-note | Labeling sufficient IF ban holds: 0.12 (CI 0.12-0.13, 59 margins) called heuristic/not-validated/median-split-tautological in 04 8.15 and SSOT; margin>=0.10 below CI, sensitivity-inclusive. LEDGER 9 needs_review respected. Any headline use without calibration = reject. |
| Absent handling (ds-pro/mimo/bailian 62) | accept-with-note | No imputation: consensus doc "missing not scored"; v41 stale kept missing+do_not_retry, ds-pro row frozen, bailian 62 absent (LEDGER 11, consensus_v4). Honest provided frozen/disclosed status and SSOT ban on "model failed" hold. Sparse-model boundary (qwen2.5 NaN floor, hy-mt2 empty-set LDS=1.0 artifact, gemma quarantine) correctly excluded from 59, not counted as signal. |
| Macro perm (500, p<0.004) | accept-with-note | Resolution limit correctly stated as 1/500, no exact p=0.0, ZH-DE 59/59 meta-expected-0.12 argument disclosed (03 5.10, 04 8.15). No multiplicity correction over 177 tests — disclosed as limitation; ZH-DE-only meta claim acceptable, EN-pair claims stay non-significant (9/177 EN n.s. honestly reported). |
| Human LDS-C p=0.08/1.0/1.0 | accept | Honestly non-significant; SE~0.019 / CI crosses 0.05 stated, no significance reading, >=1000-perm recompute blocked and logged (LEDGER 2.3, 03 4.3). Floor 0.92-0.96 ~= signal correctly yields design-artifact interpretation capped as consistency demonstration (q=0.30 is 3x sparser than human q~0.76-0.91; 04 8.15). |

## 4. Agent-blindness limits (explicit)

I am a blind methods reviewer: I did not execute or inspect rerun/reproduce code and
cannot verify computation. More importantly, the project's "agent-panel review" is NOT
blind in the human-trial sense: the 72 Batch-B labels were seeded by qwen-plus and the
agent baseline (`review_72_filled_agent.json`: 65 accept+edit / 7 reject) is a
pre-annotation comparator, not an independent blind rater; seed model = evaluation model
confound stands until H1 human second review (named trilingual external rater, access
revoke, PROTOCOL-gated import) closes with PASS_F1=0.85 / PASS_AGR=0.80 / per-lang 0.70.
Any "validated / frozen" wording for social F1 before H1 is therefore disallowed;
Developing-C9b + harness-~0.65 dual reporting is the maximum honest claim.
