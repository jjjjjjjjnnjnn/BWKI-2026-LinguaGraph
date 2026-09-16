# Statistics Rerun 2026-09-16 (Agent A, independent)

Scope: re-derive key published statistics from frozen inputs only. No fixes applied (stop-line policy).
Frozen input of record: `data/lds_c/llm_subject/multi_model_replication_20260913.json` (formal set = n==30 AND ZH-DE perm_p<0.05 AND margin non-NaN),
`research/consensus_v4_20260916.json`, `research/thr_sensitivity_v4_20260916.json`,
`research/weight_e3_repeats_20260916.json`, `research/weight_cka_rsa_20260916.json`,
`research/numbers_ssot_20260916.json`.
Generating scripts: `scripts/lds_c_multi_model.py` + `scripts/lds_c_compute.py` (perm),
`scripts/sw_fix_analyses.py` (strata/Youden), `scripts/tools/thr_sensitivity_v4.py` + `scripts/tools/consensus_vote_v2.py` (vote),
`scripts/tools/weight_e3_repeats.py` (+ `scripts/tools/weight_graph_E3.py`), `scripts/tools/weight_cka_rsa.py`.

## Match table (claim vs rerun)

| # | Statistic (published claim) | Rerun value | Match | Rerun command / seed |
|---|---|---|---|---|
| 1a | macro_perm n_perm=500 | 500 in code (`lds_c_multi_model.py:96` n_iter=500 via `label_permutation_null`) | MATCH (code param) | code inspection; perm RNG `random.seed(_ACTIVE_SEED)` in `lds_c_compute.py`; pipeline itself not re-executed (see non-rerunnable) |
| 1b | macro_perm margin_floor 0.033 | min formal ZH-DE margin 0.0332 -> 0.033 | MATCH | inline read of frozen replication JSON (no seed; deterministic min) |
| 1c | macro_perm p resolution 0.004 | min nonzero perm_p in formal set = 0.004; distinct values {0.0, 0.004, 0.04, 0.052, 0.06, 0.224, 0.384, 0.444, 0.472, 0.476, 0.672} | MATCH | inline read of frozen replication JSON |
| 2 | Youden 0.12 (CI 0.12-0.13, heuristic) | opt 0.1238 -> 0.12; bootstrap CI [0.1238, 0.1285] -> [0.12, 0.13]; J=1.0; median 0.123; heuristic 0.10 outside CI | MATCH | Youden+bootstrap logic of `sw_fix_analyses.py` replicated read-only, `numpy.random.default_rng(20260908)`, 2000 bootstraps |
| 3a | dedup stratum cn 48/48 (0.130) | 48/48, mean 0.1297 -> 0.130 | MATCH | inline stratification with `WESTERN_MARKERS` vendor rule from `sw_fix_analyses.py` (deterministic, no seed) |
| 3b | dedup stratum west 11/11 (0.155) | 11/11, mean 0.1548 -> 0.155 | MATCH | same as 3a |
| 3c | west ohne luna 10/10 (0.148) | 10/10, mean 0.1481 -> 0.148 | MATCH | same as 3a, luna key excluded |
| 3d | dedup 54/54 (0.137) | 54/54, mean 0.1372 -> 0.137 (proper dual-host pairing: flash/pro/glm-5.2/kimi-k2.6/laguna-s-2.1) | MATCH with caveat | inline dedup (deterministic). Caveat: naive suffix-identity collides the two Kilo `:free` hosts (nemotron-super vs laguna) while splitting the true laguna pair; net count still 54. Alternate tie-break (drop DashScope side) gives mean 0.1354. |
| 4 | en_ns 9/177 | 9 n.s. among 177 formal tests, all EN-involving (incl. phi-4-mini ZH-EN p=0.224; 6 R1/Distill-involving) | MATCH | inline count on frozen replication JSON |
| 5a | file-truth 62/57/186 | 61x n=30 + qwen-max n=26/30 = 62 entries; 57 identities; 62x3 = 186 tests | MATCH | inline count on frozen replication JSON |
| 5b | published 59/54/177 | formal rule yields 59 entries; 54 identities; 59x3 = 177 tests | MATCH | inline count on frozen replication JSON |
| 5c | margin span +0.03...+0.42 | formal ZH-DE margins 0.0332...0.4242 | MATCH | inline min/max |
| 6 | consensus_v4 vote 546/203/884/1905/70 | live recount from frozen vote inputs: accepted 546 MATCH; solid 203 MATCH; mimo_only 70 MATCH; weak 883 vs 884 MISMATCH (-1); hypo 1903 vs 1905 MISMATCH (-2) | PARTIAL MISMATCH (recorded, not fixed) | `thr_sensitivity_v4.load_all` + `vote_at(shift=0)` replicated read-only (deterministic counting, no seed; `main()` not called, nothing written). Per-file drift in 6 files, n_sources unchanged: de_westermann_9-10 hypo 112 vs 113; en_khan_academy_3-4 weak 49/hypo 99 vs 50/98; en_khan_academy_5-6 hypo 128 vs 129; en_khan_academy_6-8 hypo 100 vs 99; en_khan_academy_k-2 hypo 152 vs 153; zh_初中数学_九年级 hypo 22 vs 23. Working tree clean for input dirs, so drift predates this rerun (committed input change or loader-version difference at freeze time). Note: `thr_sensitivity_v4.py --help` self-check gate (exit 3) would now FAIL on current inputs. |
| 6b | consensus_v4 mixed-scale, correctly banned | thr histogram shift0 = {5: 16 files, 6: 8 files} (mixed thr5/6 scale); n_sources {8: 2, 9: 14, 10: 8}; banned-from-headline confirmed in `numbers_ssot_20260916.json` ("vote totals 546/203/884/1905/70 as final" banned; consensus_v4 "snapshot, banned from headline (verdict C2/L1-L3)") | MATCH | same recount as #6 + `numbers_ssot_20260916.json` read |
| 7 | weight E3 repeats N=200 (base 30260916) | k=5: rho 0.7441+-0.2399 [0.5, 1.0], orders {83, 117} EXACT; k=10: 0.7588+-0.2434 [0.5, 1.0], {94, 106} EXACT; k=15: 0.7044+-0.2807 [-1.0, 1.0], {128, 68, 1, 1, 1, 1} EXACT; threshold contrasts k=5/10/15 values+asc+rho all EXACT | MATCH | `weight_e3_repeats.build_pools` + repeat loop replicated read-only, N=200, `numpy.random.default_rng(30260916+i)`; script `main()` not called, nothing written |
| 8a | linear CKA shared n=199: zh-de 0.4251 / zh-en 0.3057 / de-en 0.2831 | n_shared 199; 0.4251 / 0.3057 / 0.2831 EXACT | MATCH | CKA routine of `weight_cka_rsa.py` replicated read-only on `research/weight_vectors_934x768_20260916.term2vec.json` + aligned groups (deterministic, no seed) |
| 8b | RSA emb-vs-graphdist: zh 0.17 / en 0.02 / de 0.07 (n=19701) | zh 0.1655 / en 0.0237 / de 0.0651, pairs 19701 EXACT | MATCH | RSA routine replicated read-only incl. BFS textbook graph distances over `data/math_extractions/*.json` (deterministic, no seed) |

## Non-rerunnable (with reason)

1. LLM-as-subject API measurement phase (84 started measurements across DashScope / zen / OpenRouter / Kilo / Cohere / NIM / Cloudflare / LM-Studio / opencode-terminal): quota-blocked, cost-stopped, and model-EOL channels; frozen `llm_subject_*.json` inputs cannot be regenerated. Temperature N/A (measurement, not generation), no seed.
2. Full perm pipeline re-execution (`scripts/lds_c_multi_model.py`): seed-fixed (`random.seed(_ACTIVE_SEED)`, n_iter=500) but re-running writes/overwrites the frozen replication JSON; only code params + stored values verified.
3. `scripts/sw_fix_analyses.py` as-is: writes a new dated `sw_fix_analyses_<today>.json` (would add files, violating rerun-only mandate); logic replicated read-only with identical seed 20260908 instead.
4. `scripts/tools/weight_e3_repeats.py`, `scripts/tools/weight_cka_rsa.py`, `scripts/tools/thr_sensitivity_v4.py` as-is: each writes `research/*.json/.md`; replicated read-only inline instead. The thr script's self-check gate would now exit 3 on current inputs (see #6 mismatch).
5. E3 single-draw §2 J_edge-only values (k=5/10/15 per-pair, seeds 20261416...20262418): executing `weight_graph_E3.main` rewrites the frozen E3 JSON; values read from frozen JSON only, not independently recomputed. Repeats (N=200) and threshold contrasts fully recomputed instead (#7).
6. `research/stat_methods_review_20260916.md`: not read (agent-A isolation constraint).
