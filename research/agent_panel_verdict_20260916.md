# Agent-Panel 审查终审（2026-09-16，六 persona 背对背）

- Panel：P1 严苛词典学家 / P2 宽容双语者 / P3 形态学家（语义弃权）/ P4 德语母语 / P5 中文母语 / P6 红队。
  盲态：禁读 `data/gold/`、`data/wikipedia_extractions/`、互不可见；`--import` 评分由主程序执行（非 persona）。
- 产物：`research/gold_review_v2/review_72_filled_agent.json`（annotator=agent-panel，非人类）、
  `research/wiki_gloss_audit_30_agent.json`；模板原文件不动，人类盲审位保留。

## 72 条多数决（5 有效票，edit=附条件 accept）

- accept 61＋edit 4（A016/A019/A030/A070）＋reject 7（A005/A006/A022/A028/A041/A049/A072）。
- reject 主因：截断残片（sondern/aber/dass/but/and开头或无谓语：A005/A006/A022/A028/A041）、
  单字无所指（A049 统一）、语言错配＋离题（A072）。
- `--import` 评分：agreement_overall 0.4157（门 0.8 未过）、per-lang de 0.3258 / en 0.2516 / zh 0.6027
  （floor 0.7 未过）、qwen_plus_social_f1 0.5346（门 0.85 未过，n_f1_valid=69）。
- **verdict：maintain（stay Developing, C9b）**——panel 抽取概念与 auto_accepted gold 显著分歧，
  与 paper 现有 Developing 评级一致，无升级，不降级。

## 30 gloss 联合裁决

- accept 28（20 clean＋8 元数据 flagged）/ 源 reject 2 / 平票双收 2。
- G012→real estate（4-2，property 过宽）、G017→negative liberty（4-2，Berlin 术语）；
  G001 dwelling/residence 双收（3-3）、G020 guilt 暂留＋debt/fault 别名（3-3）。
- 新发现（P5/P6）：13 条 zh 字段混入德语（G006/G008/G011/G013/G016/G018/G021/G022/G025/G028/G030
  及 G017/G019/G020 题头）——gloss 本体对等但管线语言污染，立 P0 修（wiki 抽取 zh 列清洗＋重审）。
- G030 与 G007 gloss 撞车（justice）待去重。

## 诚实声明

- 本审查为人机替代过渡物：`docs/paper` 中 Blind-Review 表述由 `ausstehend` 改
  `agent-panel-reviewed, human-review pending`，claim 不升级；人类 72 二评＋gloss 人审仍记账待发。
