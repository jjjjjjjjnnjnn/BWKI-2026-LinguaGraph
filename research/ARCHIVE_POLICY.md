# ARCHIVE_POLICY — 归档三类 + 归档位 + 重启用门 (2026-09-14, W5)

> 只定政策，不动文件，不改禁区（PII/API-Key/版权教材原文），不打 tag。
> 基线：`research/checkpoint_20260914.md` §3–§5 + `docs/BASELINE_LEDGER.md` + `docs/session_handoff_20260914_v26.md`。

## 类 A · frozen 不可重算（引用必须带冻结注，不得升级措辞）

范围：
- HDS 数学 ≤8（均值 0.40）/ 物理 ≤6（均值 0.85），冻结自 2026-06 稠密图
- LDS-K Freeze 0.9336 / 0.9382 / 0.5188（frozen v3 双分量 Jaccard）
- 退役 10 bridges（`research/steam_bridges_retired_2026-09-14.json`，839 intra / 0 bridges）
- Fig4/Fig8 快照、`research/gold_freeze_2026-09-14.md/.sha256`

归档位：
- 原位保留（`docs/fig3_cds_forensic.md`、`docs/fig5_hds_forensic.md`、`research/steam_bridges_retired_*.json`、`research/gold_freeze_*`）
- 旧口径只进 `_archive/20260912_superseded/` 或 `_archive/20260910_shelved_probes/`，不删原位冻结件

重启用门（须同时满足，缺一不可）：
1. 重算链重建（脚本 + seed + 输入哈希可复现当前冻结值±容差）
2. `docs/BASELINE_LEDGER.md` 升版并双人复核签字
3. handoff 明确解冻版本号；解冻前引用一律加“冻结自六月稠密图，当前存档不可重算”

## 类 B · 待 key / 待数据（pending，不得编造，不得引作结论）

范围：
- 72 盲审 pending（`research/gold_review_v2/review_72.json` + `PROTOCOL.md` + `workbench.html`，全仓 `*filled*` 0 命中）
- gloss-30 pending（`research/wiki_gloss_audit_30.json`，`qwen_cross_status=pending`，BAILIAN_API_KEY unset）
- 9 个 20260913 未跟踪 `data/lds_c/llm_subject/llm_subject_*_free_20260913.json`（未入库，双账维持 59-54-177，文件真相 62/57/186）
- Video 未录（脚本 v2 + storyboard 就绪，srt 15 cues 时码估计值待校准）、luna 出处未澄清、declaration §8 无湿签名

归档位：
- 原位 pending，不移入 `_archive/`；9 个 JSON 保持未跟踪直到登记入库
- 状态登记只写 `research/checkpoint_*.md` 与 handoff Offen，不另开账本

重启用门：
1. 盲审：`python scripts/gold_blind_audit.py --import review_72_filled.json`，Pass 需 F1≥0.85 且 agreement≥0.8 且每语言≥0.7（reject=F1 0，code enforced）
2. gloss：BAILIAN key 到位后跑 qwen cross，禁 fabricate
3. 9 JSON：登记入库并复核 collecting 26 口径（23 incomplete + 2 sparse + 1 quarantine）后方可并入双账
4. P0：湿签名 + Video 实录 + srt 校准 + luna 出处澄清（或书面维持 undisclosed 并承担后果）

## 类 C · 目录引用未转正文（仅目录/清单引用，未升为正文依据）

范围：
- W5 新增 6（未跟踪）：`research/baseline_board.md`（T3）、`research/compare_table2.md`（T2）、`research/narrative_fix_diff.md`（T1，N01–N33 只读扫描）、`research/rsa_bridge.md`（T5 spec 只定义不跑数）、`research/tier2_emb_baseline.md`（T4 只读复用）、`research/checkpoint_20260914.md`（T6）
- `docs/submission/` 缺 `declaration_of_support.md` / final README / forensic / BASELINE 镜像（checkpoint §5 #5–#9）
- `_deploy` stale 镜像：`_deploy/portal/README.md:48`（849+10 bridges 旧文案）、`_deploy/docs/SSOT-web.md:74`（同旧）

归档位：
- 新增 6 保持 `research/` 原位 untracked，不提前移 `_archive/`，不手改已跟踪文件
- 缺失镜像问题只登记不补（本次任务禁改）；书面口径待定（补 vs 明确不补）

重启用门：
1. T1 N01–N33 转正文：逐条按 `删/加限定/降级` 受控词表改原文并复检（当前 0/33，见 handoff v27 Offen）
2. T5 跑数前必须过密度守卫 + perm 下限，否则判 `offen`
3. 缺失/ stale 镜像：按源重镜并字节+SHA256 对账（`submission/final` 为准），checklist §平台字段对一遍后再定 tag
4. 平台录入后才打 `v1.0-bwki-submission`；此前任何转正不得打 tag
