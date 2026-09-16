# T6 独立检查点 — 2026-09-14（只读核查 + 逻辑博弈 + 同步核查）

> 范围：只写本文件，不改其它，不打 tag，不碰禁区（PII/API-Key/版权教材原文）。
> 基线：`docs/session_handoff_20260914_v26.md`（v26-nobridges）+ `docs/SSOT-web.md` + `manifest.json`。

## 1. 只读 Git 状态（T6-1）

- `git status --short --branch`：`## master...origin/master`，工作树干净除 9 个未跟踪：
  `data/lds_c/llm_subject/llm_subject_{cohere_north-mini-code,ling-3.0-tiny,lmstudio_hy-mt2-1.8b,lmstudio_phi-4-mini,lmstudio_qwen2.5-0.5b,mistral-medium-latest,nvidia_nemotron-3-nano-30b,openrouter_nvidia_nemotron-3-ultra-550b,poolside_laguna-s-2.1}_free_20260913.json`
  → 9 个 20260913 新测量 JSON 尚未入库/登记（影响 59-54-177 双账，见 §4）。
- `git log --oneline -5`：
  `0acce22 docs-handoff-0914: session_handoff_20260914_v26 (DE) + ...` /
  `d5cea60 v26-nobridges ...` / `8fc81ef v26-nobridges ...` /
  `9874971 g2-workbench ...` / `7397d47 readme-i18n-shots ...`
- `git tag --list`：`v0.1, v0.13.1-pre, v0.4, v0.5, v0.6, v0.6.1, v0.9.1-pre-human-validation, v0.9.2-human-validation-ready`
  → 无 `v1.0-bwki-submission`（与 handoff 里程碑一致：平台录入后才打）。

## 2. 盲审输入核查（T6-2，全仓 `*filled*` glob）

- 全仓 glob `**/*filled*`：**0 命中** → 无已填盲审回传。
- 模板存在且未动：`research/gold_review_v2/review_72.json`（meta seed 20260914, n=72, auto_accepted 社会子集，
  `concepts_blank` 全空）+ `PROTOCOL.md`（分级线 F1≥0.85 且 agreement≥0.8 且每语言≥0.7）+ 离线 `workbench.html`。
- 结论：**72 盲审 pending**（G2 verdict 未出；freeze 注明 gold 仍为 PILOT，72 项不得引作 Mature）。
- gloss：`research/wiki_gloss_audit_30.json`（seed 20260914, n=30/96）：30 条 `accept/notes/qwen_cross_gloss` 全空，
  `qwen_cross_status = pending (BAILIAN_API_KEY unset, no cross results fabricated)` → **gloss 待 key**，不得编造 cross 结果。

## 3. 检查点数字（门户/SSOT 口径，2026-09-14 实测）

- 门户/数学：**556 节点 · 238 rendered links（of 525 aligned relations）· 219 groups**（`manifest.json` 实测：
  total_nodes 556 / total_links 238 / aligned_groups 219 / total_relations 525；`graph_density 0.001543`）。
- STEAM：**1143 节点 · 839 学科内边 · 0 bridges**（10 条手工 bridges 2026-09-14 退役，
  归档 `research/steam_bridges_retired_2026-09-14.json`；`scripts/build_steam_graph.py` Assert 839）。
- 双账：**59/54/177**（发布口径，剔除 qwen-max 部分运行 n=26/30）/ 文件真相 **62/57/186**；
  另有 §1 的 9 个 20260913 未跟踪 JSON 待登记（collecting 26 = 23 incomplete + 2 sparse + 1 quarantine 口径需复核是否扩大）。
- 冻结值：LDS-K **0.9336 / 0.9382 / 0.5188**（ZH-EN/DE-EN/ZH-DE）；T1 去污 0.52→0.99（167/219 含 CJK 的 DE 标签剔除后收敛崩塌）。
- F1：加权总数 **0.881** = (72×0.939+20×0.674)/92；**0.939 仅社会子集**（n=72, Developing, machine-seeded/auto_accepted）；
  独立 harness 社会 F1 ≈0.65（qwen-plus 0.6497 / qwen-max 0.6483，`research/gold_deconfound_2026-09-14.md`）。
- HDS：数学 ≤8（均值 0.40，83% 根概念）/ 物理 ≤6（均值 0.85）；值冻结自 2026-06 稠密图，当前存档不可重算（见 fig5 forensic）。
- P0：**Video 未录制**（checklist 🔴；脚本 v2 + storyboard 就绪；srt 15 cues 时码为估计值待校准）；
  **luna 出处未澄清**（portal `West · origin undisclosed`；final README v0.13.2 行列其为" Herkunft ungeklärt"）；
  declaration §8 仅签署块模板，无湿签名。

## 4. 红队博弈（六点：每点 红问→蓝答→裁决；PEP 展开三问三答）

### R1 · 0.519（F4 ZH-DE 收敛）
- 红问：0.5188 是否证明"中文与德文知识组织更接近"？
- 蓝答：否。T1 去污显示它是标签 artefact（167/219 德标签含 CJK 文本）；F5 零模型 Full 0.73 < Structure 0.77，
  分类法解释主要方差；final README 已降级 C1 为"indikativ（P2-Recheck：对齐标签）"。
- 裁决：维持"指示性、不得作语言收敛 headline"；引用必须并列 T1 证伪句。

### R2 · 0.939（社会 F1）
- 红问：门户 hero 写 F1=0.939 是否 over-claim？
- 蓝答：0.939 是 DB-path + seed 同源特定值（paper value），独立 harness 仅 ~0.65；
  总 headline 须为加权 0.881，且社会子集标注 Developing + blind pending（portal README 与主 README 已注 † 与 harness 注）。
- 裁决：维持双数字记账（0.939† 社会 / 0.881 加权）；G2 通过前不得升级 Mature。

### R3 · GED（图编辑距离缺席）
- 红问：方法论文献称 GED 为核心指标，为何 headline 只用 LDS（Jaccard）？
- 蓝答：精确 GED NP-hard；LDS 冻结为 v3 双分量公式（node+edge Jaccard）以保可复现；
  GED 退居背景/附录方法（`data/evidence/technical_methodology.md` §2.2），`src/scoring.py` 三分量变体已声明不复现发布值。
- 裁决：维持现状；评审问及时出示 BASELINE_LEDGER §8 + 复现脚本链。

### R4 · HDS≤8（不可重算的冻结值）
- 红问：HDS≤8 既然"当前存档不可重算"，凭什么进 F3 headline？
- 蓝答：凭取证链（fig5 forensic：aligned 219 / 556-238 快照 / math_full 3833 三源穷举；portal finding_b_body 三语均注"冻结自六月稠密图"），
  且均值 0.40 + 83% 根概念与"浅网"结论方向一致。
- 裁决：可引用但必须带冻结注；重算链重建前不得升级措辞强度。

### R5 · 学段（CDS 中段峰值 0.271）
- 红问：F1–F3 均为描述性、无 CI，是否只是样本巧合？
- 蓝答：中段峰值在 ZH/EN/DE 三语独立复现（0.271→0.073 高段 3.7× 稀释）；化学中段峰值差绝对值小（0.012）已如实降级为"consistent with, not confirming"。
- 裁决：描述性结论成立，因果/治理外推禁止（归 F10 假设）。

### R6 · PEP（三问三答）
- Q1：版权 PEP 教材扫描件是否进仓？A1：否。`DATA_MANIFEST.md` 明确"本地研究专用·永不进仓·以 smartedu 官方本为准"；
  仓内仅映射 JSON 与 OCR 事实级 txt（后者在 gitignored 路径）。评审索要原文时指向官方渠道。
- Q2：CS 12.7%–95.4% 能否归因"集权 vs 联邦"治理？A2：不能作为结论。F9 测量强、F10 治理归因仅假设
  （粒度混杂：CN 87 vs US 2124 vs NRW 299 课程概念；课堂实施链未测）。
- Q3：物理"1 pending sensor node"与节映射 pending 是否瞒报？A3：否。portal scope-note 与 cn_mapping 注记均公开缺口
  （传感器单元 0 节点已知缺口见 physics_sourcing P0-3；11 册中 7 mapped + 4 stubs）。
- 裁决：三答均有出处；平台填报时 Q2 必须写假设措辞，Q1/Q3 写数据来源注。

## 5. 数据同步差表（submission/final 9 文件 vs docs/submission vs _deploy）

实测（字节数 + SHA256）：

| # | 文件 | submission/final | docs/submission | _deploy/docs/submission | 判定 |
|---|------|------------------|-----------------|-------------------------|------|
| 1 | `LinguaGraph_BWKI2026.pdf` | 235200B `074048DE…0973A65` | 235200B 同哈希 ✅ | 235200B 同哈希 ✅ | 三处一致（注：checklist/handoff 所记 229178B/229717B 已是旧构建，PDF 自 09-13 后又重建过） |
| 2 | `plattform_antworten.md` | 8725B `3E7003A8…` | 同哈希 ✅ | 同哈希 ✅ | 一致 |
| 3 | `feld_mapping.md` | 1498B | 同哈希 ✅ | 同哈希 ✅ | 一致 |
| 4 | `code_einreichung.md` | 5529B `697B281E…` | 同哈希 ✅ | 同哈希 ✅（_deploy 根同名文件亦同） | 一致 |
| 5 | `declaration_of_support.md` | **12398B**（09-14 08:29）`C4688B8A…` | ❌ 缺失 | 11991B（09-13）`090DD9512…` | **差：final 最新未同步到 _deploy；docs/submission 完全缺此文件** |
| 6 | `README.md`（final 包说明） | 2700B | ❌ 缺失（仅有 `einreichung_checkliste.md` 4888B 为 docs 独有） | 2700B ✅ | 差：docs/submission 缺 final README |
| 7 | `fig3_cds_forensic.md` | 2924B | ❌ 缺失 | ❌ 缺失（_deploy 未镜像 forensic） | 差：仅 final 有（按设计亦应在 docs 有 `docs/fig3_cds_forensic.md` 对应，提交包内缺镜像） |
| 8 | `fig5_hds_forensic.md` | 2537B | ❌ 缺失 | ❌ 缺失 | 同上 |
| 9 | `BASELINE_LEDGER.md` | 6092B | ❌ 缺失（docs 根有 `docs/BASELINE_LEDGER.md` 对应源） | ❌ 缺失 | 差：提交包冻结账本未进 docs/submission |
| 10 | `einreichung_checkliste.md` | ❌（属 docs 层） | 4888B 独有 | 4888B ✅ | 反向差：final 包缺 checklist（按设计 checklist 不进 final，可接受，但平台录入前需对一遍 §平台字段） |

_Deploy stale（portal README 系）：
- `_deploy/portal/README.md:48` 仍写"556 nodes · 525 relations" + "1143 nodes · 849 links · 10 bridges"（v24 旧文案）；
  源 `cognitive-space/portal/README.md:48` 已为"238 rendered links of 525" + "839 intra / 0 bridges" → **_deploy 该文件 stale，需重镜**。
- `_deploy/docs/SSOT-web.md:74` 仍写"849 links (238+386+215 + 10 Bridges)"；源 `docs/SSOT-web.md:80` 已为"839 links (…0 bridges)" → **同 stale**。
- 新鲜对照：根 `README.md` == `_deploy/README.md`（`B8FA61E5…` ✅）；`cognitive-space/portal/index.html` == `_deploy/portal/index.html`（`B996B8A7…` ✅）——
  stale 仅限上述两个 md 镜像 + declaration，viewer/portal 生效页不受影响。

## 6. P0 行动（签字/Video/luna，不在本任务执行，仅登记）

1. `declaration_of_support.md`（12398B 版）同步到 `_deploy/docs/submission/`；`docs/submission/` 补或明确不补 declaration/README/forensic/BASELINE（需一个书面口径）。
2. `_deploy/portal/README.md` + `_deploy/docs/SSOT-web.md` 按源重镜（849→839，补 238 rendered 限定语）。
3. 9 个 20260913 未跟踪 `llm_subject_*` JSON 登记入库（维持 59-54-177 双账可审计）。
4. Video 录制 + srt 时码校准；luna 出处澄清或维持"undisclosed"并承担披露后果；declaration §8 湿签名。
5. 72 盲审找具名外部二评（≥14 天延迟自评仅封顶 maintain）；gloss 30 待 BAILIAN key 后做 qwen cross。

---
* predates v1.0；下一步按 handoff：72 盲审 → `--import` verdict → 平台录入 → Tag `v1.0-bwki-submission`。*

## W6终验（2026-09-14，只跑不改；追加段）

- 1) `git diff --stat`：7 文件，与 W1 一致仍在：
  `cognitive-space/portal/index.html | 60 ++++----` /
  `cognitive-space/web/story/index.html | 28 ++++----` /
  `docs/paper/00_three_conclusions.md | 12 ++++----` /
  `docs/paper/02_methodology.md | 10 ++---` /
  `docs/paper/02_related_work.md | 6 ++--` /
  `docs/paper/03_results.md | 18 ++++----` /
  `docs/paper/04_discussion.md | 16 ++++----`；
  合计 `7 files changed, 75 insertions(+), 75 deletions(-)`。
  `git status --short`：M 即上述 7 文件；?? 为 `data/lds_c/llm_subject/llm_subject_*_20260913.json ×9` +
  `docs/session_handoff_20260914_v27_draft.md` + `research/*.md ×9`（ARCHIVE_POLICY/baseline_board/checkpoint/compare_table2/debate_verdict/deep_evidence/narrative_fix_diff/narrative_fix_skipped/rsa_bridge/tier2_emb_baseline，含本文件）。
- 2) 禁区：`git diff --name-only -- tests/ data/lds_c/ llm_subject/ _deploy/` 为空；
  `git status --short -- tests/ _deploy/ *.db **/*.db` 为空 → tests/llm_subject/linguaGraph.db/_deploy 跟踪区无手改。
  注：`data/lds_c/llm_subject/` 下 9 个 20260913 JSON 为未跟踪新测量（§1 已登记待入库），非跟踪文件改动。
- 3) 裸词复检（W1 七文件口径，`git grep -n` 工作树）：
  `proves` = 0；`first automated`（-i） = 0；`validated F1=0.939` = 0；
  `universell` story/portal = 0；W1 全集 = 2，均在 `docs/paper/00_three_conclusions.md:14,50` 且为限定/否定式
  （L14 `keine universelle Eigenschaft` + Preliminary/sample-begrenzt；L50 `Obwohl mathematische Wahrheit universell ist … kein Dominanz-Beweis` + Einschränkung/P2-Recheck），非裸断言；
  `融合` story = 0，portal = 1（`cognitive-space/portal/index.html:2167 val_roster_desc: '融合视图——59 个完整运行…'`，功能标签未清零）。
  → 除 portal `融合视图` 1 处外，其余裸词在 W1 口径清零；universell 仅剩 2 处合格限定句。
- 4) `python -m pytest -q`：只跑不改，`84 passed in 22.72s`（<120s，无需降级 --collect-only）。
