# OSF Preregistration Amendment A-Judge — Multi-Agent Blind-Review Panel (2026-09-19, pre-data)

Parent: `docs/osf_preregistration_addendum_v1.1_spark.md` (A1–A10) + v1.2 (A11–A18).
This amendment freezes the agent panel BEFORE the first judge call.
Human `gold_blind_audit.py` gates (F1≥0.85/agr≥0.80/per-lang≥0.70) DO NOT apply to agents.

## J1. Role: falsify/screen ONLY, never mature
- Consensus `--import` fail → `maintain (stay Developing, C9b)`, filed as falsification/screen.
- Consensus `--import` pass → `candidate — human confirm required`. C9b matures ONLY on a pre-registered
  single-human `--import` pass. No agent outcome upgrades any claim.

## J2. Panel (5 raters, 5 families; Qwen quarantined)
- R1 deepseek-v4.1-flash via r4; R2 glm-5.2 via r4-direct; R3 sensenova-6.8-flash-lite via sn;
  R4 OpenRouter non-CN model (exact id frozen at probe, see J6); R5 big-pickle via zc-free.
- Qwen-family excluded from majority (seed vendor). No rater judges with extraction prompts.

## J3. Blinding
- Dispatcher sends ONLY {audit_id, language, question, text} + frozen judge prompt.
- `sample_id` NEVER in prompt; joined OFFLINE by dispatcher for `--import`.
- Sandbox/no-mount per A7; single-turn per item; per-rater shuffled order (seeds logged).
- Post-hoc leak grep (`human_labels/predicted_concepts/gold_dataset` in outputs → discard rater).

## J4. Frozen judge prompt (SHA in driver header; any byte-change = D-Jx)
- System + template in `scripts/tools/panel_judge.py` (`JUDGE_SYS_SHA`/`JUDGE_TPL_SHA`).
- Output schema: {audit_id, decision: accept|edit|reject, concepts: [...]}. ≤3 attempts/item.

## J5. Aggregation + gates
- Majority ≥3/5 per item; ties → `edit` + `needs_human` flag (never silent accept).
- Consensus file (same filled schema, meta.annotator lists 5 triples + non-human) → `gold_blind_audit.py --import` unchanged (reject-as-0).
- Per-rater imports scored for diagnostics only; verdict from consensus only.
- Screen flags (report-only): `strong-falsify` iff consensus agr<0.60 or F1<0.60 or any-lang<0.50.
- `candidate` requires consensus meeting human gates AND Fleiss κ≥0.6 AND all-5-reject overlap on every consensus-reject.
- Agreement appendix (deterministic): Fleiss κ on decisions + mean pairwise Jaccard on edited_concepts + exact-match rate.

## J6. Execution
- Smoke 3 items/rater (≥2/3 parsed + schema-valid) before full 72; breaker 5-consecutive-fail park; resume-safe; serial per key.
- R4 model probe: 1-item probe on OpenRouter candidates until first schema-valid parse; FROZEN 2026-09-19: `cohere/north-mini-code:free` (A001 accept, 1 concept, schema-valid first try).
- Budget: 72–216 calls/rater; 360–1080 total. Stop rules per A10/D-S4 (no parallel storms).
- Outputs ONLY `research/gold_review_v2/panel_<rater>.json` + consensus + appendix. Never `data//freeze/`.

## J7. Human spot-check (owner, ~30 min)
- 12 items: all consensus-rejects + all needs_human ties + 1 zh/1 de/1 en stratified accepts.
- Same task as PROTOCOL §5. Filed as appendix; gates never recomputed from 12.

Frozen 2026-09-19 BEFORE first judge call. Owner: methods.
