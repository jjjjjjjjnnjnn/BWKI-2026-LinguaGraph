# 人类盲审记账（2026-09-16，待人工/待决策）

> agent-panel 已闭环（verdict maintain C9b），以下须人类到场，agent 不可替代。

## H1 72 盲审二评（ blocking v1.0 tag）

- 发包物就绪：`research/gold_review_v2/{review_72.json,PROTOCOL.md,workbench.html}`＋`scripts/gold_blind_audit.py`
  （PASS_F1=0.85 / PASS_AGR=0.80 / per-lang 0.70）。
- 缺：具名三语（zh/de/en）外部二评 1 人（姓名＋日期＋联系方式）；gold-file access revoke 盲态管理执行人；
  邀约函模板（用户定：无人选，暂不写模板——有人选时补）。
- agent 基线：`review_72_filled_agent.json`（65 accept+edit / 7 reject）届时转预标注比对，
  人类 verdict 以 `--import` 为准；reject 7 条须第二双眼睛复核（PROTOCOL §10）。
- Owner：用户（找人＋发包）；Frist：v1.0 tag 前。

## H2 gloss-30 人审

- agent 已决：28 accept / G012→real estate / G017→negative liberty / G001·G020 双收；
  zh 清洗后（14 条）结论不变。
- 待人：G012/G017 终裁签字＋G030/G007 去重确认＋13 条 zh 污染清洗复核。
- Owner：用户或德语领域人审。

## H3 LEDGER 第二签

- v21 一签已落（opencode-agent/2026-09-16/pytest84）；二签位空。Owner：用户。

## H4 Push 决策（origin/master 落后 ~16 commits）

- CI-Erstlauf 须 push 才触发；push 含 ensemble 14.6MiB＋lds＋vectors除外。
  风险：公开仓库暴露未发表数据。Owner：用户（push / 不 push / 新建私有远端三选一）。

## H5 Video 叙事对齐

- 4K 母带（09-12）vs v26 paper＋门户新段（Two-Tier/探针/L4-L5）未对齐；需人工看片核对＋必要时补录。
  Owner：用户。
