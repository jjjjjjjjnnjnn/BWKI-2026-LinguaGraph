# Session Handoff v28 — 多模型集成重验证全记录（2026-09-15）

- 基地：`C:\Users\rongj\Desktop\学校\BWKI-2026-备战`
- 前序：v26（`docs/session_handoff_20260914_v26.md`）+ v27 draft；本文件覆盖 09-14/15 新增的 ensemble-v2 全线。
- 禁区延续：不改 `tests/` 断言、不打 tag、不碰 `freeze/`、`_deploy/`、`data/lds_c/llm_subject/` 既有文件、`linguaGraph.db`（只读 SELECT）；`pytest 84 passed` 门禁（09-15 两次全绿）。
- 口径冻结：`556 nodes / 238 rendered links (of 525) / 219 groups`；双账 `59/54/177` vs `62/57/186`；`F1≈0.881 weighted`、`0.939† Developing`、`harness~0.65`。
- 密钥规则：任何 `sk-` **禁写入文件/日志/git**，只经 bash 内 `$env:BAILIAN_API_KEY='...'` 内存提供。本文件只记 key 前缀与授权状态，不记完整新 key（新 key 在本对话记录中，格式 `sk-ws-H.PH…`，恢复时从对话取）。

## 1. 已完成（按时间倒序）

- **Ensemble-v2 七模型矩阵**（DashScope 兼容端点，temperature=0，prompt=mimo-schema统一）：
  matrix = mimo（底座68文件）+ Spark 1.3（12 audits）+ 7 API：`qwen3.8-max`、`qwen3.8-max-0902`、`deepseek-v4-pro-0813`、`kimi-k3`、`qwen3.8-27b`、`deepseek-v4.1-flash`、`qwen3.7-flash`。
- 深度24名单中央定死：`research/ensemble_v2/depth24.json`（旧12：6首审+6次审；新12：de×4/en×4/zh×4；`zh_选修2-2_ch1_sec1.1`源缺失剔除，换1.3； breadth=65交集−24=41）。
- 覆盖（配额烧到 `403 AllocationQuota.FreeTierOnly` 为止）：kimi-k3 102文件（depth 24/24全）、3.7-flash 73（depth全，广度曾403blocked）、max 44、max-0902 43、27b 48、v41flash 18、ds-pro 3。输出 `research/ensemble_v2/<model>/*.rN.json` + `_manifest.json`（calls/done/missing/failed）。
- 核心数字（`research/consensus_v2_20260914.md`）：intra自一致 0.55–0.73（kimi最高0.73；temp=0仍~40% run间分歧，非确定性定量成立）；inter均值 **0.46**（max–max0902 0.60最高，同家族偏置实证）；vs mimo 0.21–0.38（单次快照成立）；表决v2：收录491 / Solid145 / Weak506 / Hypo1554 / mimo独有76（污染快照，禁报完成品）。
- Gold bench（n=92，temp=0）：max-0902 **0.738** > max 0.733 > 3.7-flash 0.711 ≈ flash 0.711 > 27b 0.698 > kimi 0.554；ds-pro 0.065/v41flash 0.36判 **harness不兼容**（空content走reasoning_content；已加回退分支重跑 `bailian_gold_dsfix_20260914`：pro 0.139/fb命中74中仅7有效，维持原判，聚合剔除ds系）。输出 `research/bailian_gold_v2_20260914.md+json`。
- LDS-C subject复制：ds-pro 与 max-0902 **双双复现**（ZH-DE LDS-C 0.967/0.945 vs floor，perm p=0.0）；kimi-k3因冻结管线temp=0.3被拒收判incomplete（管线参数问题）。输出3个新subject + `multi_model_replication_20260914.json`。
- Wiki：kimi 30/30，宽松三方28/30可用，严格21/30禁作证据（`research/wiki_gloss_kimi_20260914.json`）。
- 理化：6条目J均值0.02系粒度错位，verification子集0.09–0.24为真信号方向，禁进headline。
- 向量对照（本地e5零成本）：三语对压进0.48–0.52窄带（极差0.0445）vs LDS-K极差0.419 → 教学编排断层≠语义不对齐。
- 红蓝终审v1+v2：`red/blue_attack/defense_20260914.md`、`multi_model_verdict_20260914.md`、`red_attack_v2.../blue_defense_v2.../multi_model_verdict_v2...`。旧汇总已按终审修订（12文件10review/2fail，precision下限0.70）。
- DAG：685节点/665边/11环/prune141/51去向（补35/纠13/删1/归档2）。门户补丁未贴（`research/portal_patch_20260914.md`，等确认）。
- 总报告：`research/ensemble_report_v2_20260914.md`（覆盖+数字+裁决+口径+补跑+禁语）。

## 2. 密钥状态（恢复时用）

- 老key（`sk-6f…24a`）：qwen系+ds系配额耗尽（403），flash剩~699K/max剩~674K时即已打空；仅认 `qwen3.8-*`（flash/turbo 403）。
- 新key（本对话中，`sk-ws-H.PH…`）：已验权 DashScope兼容端点可用（ds-pro/kimi/max-0902/flash均OK；`deepseek-chat`404系无此模型名；DeepSeek官方端点401不用）。赛后轮换两key。
- ds-pro注意：reasoning占token，extraction须 `max_tokens=16000`（8000回空）；gold harness已修回退分支但仍不兼容，ds分数禁作能力解读。

## 3. 未完成（新对话继续，优先级P1→P4）

- P1 ds-pro depth补跑（16000通道，按_manifest missing+failed续跑，~100 calls封顶）——子任务曾因切换被取消，未跑。
- P2 kimi tail（quota_blocked约8个选修）+ P3 v41中文missing ——同上，未跑。
- P4 qwen四模型广度缺口（max 35/max-0902 50/27b 60/3.7-flash 36；3.7先探针1个再续）——未跑。
- 之后：表决v3重算 → 终审v3 → Two-Tier/Limitations追加非确定性实证 → 贴门户补丁 → 修数任务（删幻觉边/纠错边/去重24/破11环，修数清零前不得冻结）。
- 续跑通用做法：`$env:BAILIAN_API_KEY='<新key>'` + 按 `research/ensemble_v2/<model>/_manifest.json` 的missing/failed用 `scripts/tools/bailian_reextract.py --model <M>` 跑 → 改名 `research/ensemble_v2/<model>/<base>.rN.json`（已存在跳过，失败重试1次记缺席）。

## 4. 关键文件索引

- 抽样与输出：`research/ensemble_v2/depth24.json`、`research/ensemble_v2/<model>/`（7目录+physchem）、`research/bailian_audit/`（flash 11+max 3）、`research/mimo_spark_audit/`（12 audits）。
- 报告：`ensemble_report_v2_20260914.md`（总）、`consensus_v2_20260914.md`、`bailian_gold_v2_20260914.md`、`multi_model_verdict_v2_20260914.md`、`two_tier_benchmark_20260914.md`、`human_vs_machine_20260914.md`、`limitations_20260914.md`、`dag_validation_20260914.md`、`portal_patch_20260914.md`。
- 脚本：`scripts/tools/bailian_reextract.py`（temp0/8k）、`consensus_vote_v2.py`、`openweight_embed_audit.py`、`bailian_gold_bench.py`（+reasoning回退）、`rule_prune_candidates.py`。
- 可登记口径与禁语10条见 verdict_v2 §②与 ensemble_report_v2 §④⑥；旧数字（6文件/0.78下限/0.54 Jaccard/193低优先级）已作废禁报。
