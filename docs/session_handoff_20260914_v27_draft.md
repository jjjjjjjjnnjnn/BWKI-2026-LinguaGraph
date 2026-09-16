# Session Handoff — 2026-09-14 (v27 draft, W5 项目管理整理)

> 基线：v26-nobridges + `research/checkpoint_20260914.md`（T6，只读，沿用不改）+ `research/ARCHIVE_POLICY.md`（新建）。
> 本次可写仅 2 个新文件（本文件 + ARCHIVE_POLICY），禁区不动，不打 tag。

## W5 新增 6（research/*.md，untracked，待入库）

| # | 文件 | 任务 | 状态 |
|---|------|------|------|
| 1 | `research/narrative_fix_diff.md` | T1 只读扫描 | N01–N33 共 33 条，原文未改，转正 0/33 |
| 2 | `research/compare_table2.md` | T2 学科×学段对照 | 唯一新增文件，full-graph 口径，待转正文引用 |
| 3 | `research/baseline_board.md` | T3 可引用基线看板 | verified/needs_review/drop 三态，Ledger v20 为准 |
| 4 | `research/tier2_emb_baseline.md` | T4 只读复用验证 | 未跑 `--test/--full`，不重算不写盘 |
| 5 | `research/rsa_bridge.md` | T5 RDM×Tier1/Tier2/H spec | 只定义不跑数，跑数前须过密度守卫 |
| 6 | `research/checkpoint_20260914.md` | T6 只读核查+红队+同步差 | 已写定，同步差沿用其 §5（本次不重测不修改） |

W1–W4 已跟踪产出（状态）：
- `research/gold_deconfound_2026-09-14.md/.json` — committed，独立 harness 社会 F1 ~0.65 vs DB 0.939†
- `research/gold_freeze_2026-09-14.md/.sha256` — committed，gold 仍 PILOT，72 项不得引作 Mature
- `research/steam_bridges_retired_2026-09-14.json` — committed，10 bridges 退役，STEAM 1143/839/0
- `research/wiki_gloss_audit_30.json` — committed，30 条 accept/notes 全空，待 key
- `research/gold_review_v2/` — committed，`review_72.json` + `PROTOCOL.md` + `workbench.html`

## Offen 更新（v26 → v27）

1. **T1 转正数：0/33。** N01–N33 扫描完成（universal/Konvergenz/proves/first/validated/bare 0.519/bare 0.939/GED三元合规不计条/Fusion），判定 `删/加限定/降级` + 受控词表已定，原文零修改，待逐条应用。
2. **盲审仍 pending。** 72er-Blindaudit：全仓 `*filled*` 0 命中；`review_72.json`（n=72，concepts_blank 全空）+ workbench 待用户跑 → `--import` verdict（Pass: F1≥0.85 且 agreement≥0.8 且每语言≥0.7）。Gloss-30 待 BAILIAN key，禁编造 cross。
3. **平台 §6 = 1087 待粘。** `submission/final/plattform_antworten.md` §6（Kritische Einschätzung）1087 口径待用户粘贴到平台；粘前先对 `einreichung_checkliste.md` §平台字段。
4. **tag pending。** `git tag --list` 无 `v1.0-bwki-submission`；顺序：72 盲审 → `--import` → 平台录入 → 才打 tag。本次不打 tag。
5. **P0 签字 / Video / luna。** declaration 12398B 版（09-14）仅签署块模板，无湿签名；Video 未录制（脚本 v2 + storyboard 就绪，srt 15 cues 时码估计值待校准）；luna 出处未澄清（portal `origin undisclosed` / final README `Herkunft ungeklärt`）。均只登记不执行。

## 同步复检（沿用 checkpoint §5，只列不改）

- #1–#4 一致：PDF（235200B `074048DE…`，旧 229178B/229717B 作废）、`plattform_antworten.md`、`feld_mapping.md`、`code_einreichung.md` 三处同哈希。
- #5 差：`final/declaration_of_support.md` 12398B（`C4688B8A…`）最新未同步到 `_deploy`（11991B `090DD9512…`）；`docs/submission/` 完全缺此文件。
- #6 差：`docs/submission/` 缺 final README（2700B）；反向 #10：`einreichung_checkliste.md` 4888B 仅 docs 层有（可接受，final 包按设计不含）。
- #7–#9 差：`fig3/fig5_forensic.md` + `BASELINE_LEDGER.md` 仅 final 有，未进 `docs/submission` / `_deploy`。
- stale：`_deploy/portal/README.md:48`（556 nodes·525 relations + 1143/849/10 bridges 旧文案）与 `_deploy/docs/SSOT-web.md:74`（849 旧）未重镜；源已是 238 rendered of 525 + 839 intra / 0 bridges。根 README 与 portal index.html 已新鲜一致。
- P0 行动（只登记）：declaration 同步 + 口径书面化 + 9 JSON 登记入库 + Video/srt/luna/湿签名 + 72 盲审 + gloss key（详见 checkpoint §6）。

## 下一步

1. T1 N01–N33 逐条转正文并复检（0/33 → 待清零）。
2. 72 盲审找具名外部二评 → `--import` → C9b 是否升 Mature。
3. 平台粘 §6（1087）→ 录入 → 打 `v1.0-bwki-submission`。
4. 归档执行按 `research/ARCHIVE_POLICY.md` 三类门槛走；本次之后仍禁区不动。
