# Gold Freeze Note (2026-09-14)

Frozen (SHA256 in `research/gold_freeze_2026-09-14.sha256`): `data/gold/gold_dataset.json`,
`data/gold/gold_dataset_expanded.json` (identical hash: expanded file is currently a
byte copy, no expansion applied), `data/model_comparison/qwen-plus_results.json`,
`data/model_comparison/qwen-max_results.json`, and the G3 deconfound md+json.

Status: gold stays PILOT, not Mature. The 72 social items are `auto_accepted`
(machine-seeded, never second-judged); only the 20 math items carry `annotator_1`.

Gap / middleware missing: no `research/` review middleware existed before today
(`research/` directory itself was absent); there is no accept/edit/reject log, no
second-annotator record, no v2 gold. G2 now scaffolds exactly that
(`scripts/gold_blind_audit.py`, `research/gold_review_v2/review_72.json`,
`research/gold_review_v2/PROTOCOL.md`), but the 72 blind re-judgements are still
pending. Until the G2 verdict passes (F1>=0.85 and agreement>=0.8), no file in
this freeze may be cited as Mature gold.

Verify: `Get-FileHash <path> -Algorithm SHA256` and compare against the .sha256 file.
