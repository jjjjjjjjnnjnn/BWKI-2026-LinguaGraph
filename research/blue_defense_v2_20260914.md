# 蓝队防守书 v2（2026-09-14）：界定可用边界，不洗白

- 立场：蓝队 v2（防守方）。只为"方法可用、失败可归因、排序可复现"辩护；凡红队锤实或本文件核验缺口，全部记债务。不扩大、不反杀。
- 已读（本文件断言的唯一依据，行号可查）：
  - `research/ensemble_v2/*/_manifest.json`（7 个：max-0902 / max / 27b / 3.7-flash / kimi-k3 / ds-pro-0813 / v41-flash）+ `research/ensemble_v2/depth24.json` + `research/ensemble_v2/kimi-k3/` 目录（103 entries = 1 manifest + 102 data）+ `research/ensemble_v2/physchem/`（24 entries）。
  - `research/bailian_gold_v2_20260914.md` + `.json`（temperature=0，n=92：zh=36 / de=29 / en=27）。
  - `research/wiki_gloss_kimi_20260914.json`（n=30，每条均有 `kimi-k3` 返回）+ `research/gloss_cross_report_20260914.md`（qwen cross 28/30）。
  - v1 防守书 `research/blue_defense_20260914.md`（mimo 基线口径，本文件不重写，只继承"宏观/微观分层"原则）。
- 证据分级（全文有效）：**V=文件已验证** / **A=用户断言、产物未入库、不得登记为 verified**。A 级只记方向，不进可登记口径。

## ① 防守证据（5 条，每条注明 V/A）

**B1. qwen 系 gold F1 头部 0.71–0.74、头部三模型零失败【V，部分纠偏用户口径】**
`bailian_gold_v2_20260914.md:9-18` + `.json:scores`：max-0902 overall **0.7376**（zh 0.8266 / de 0.6708 / en 0.6907，fail 0.00%）；max **0.7325**（fail 0.00%）；qwen3.7-flash **0.7114**（fail 0.00%）；flash **0.7113**（fail 1.09%，parse=1）；27b **0.6977**（fail 4.35%，exc=1+parse=3）。纠偏：用户口径"qwen 系 0.70–0.74 零失败"不精确——精确表述是**头部三模型（max-0902/max/3.7-flash）0.71–0.74 零失败**，系内全谱 0.6977–0.7376。防守点：失败率最低的三席恰是 F1 最高的三席，高分不是靠"吞失败"换来的；flash/27b 的少量 fail 均已按 `fail_rate=(exc+parse)/总数` 全额计入分母（`bailian_gold_v2_20260914.md:22`），非藏数。

**B2. 复跑 Δ 在波动带内、模型间排序稳定【V】**
`bailian_gold_v2_20260914.md:28-30`：基线 flash 0.6830→0.7113（Δ=+0.0283）、max 0.7213→0.7325（Δ=+0.0112）；temperature=0 下仍有 run 间波动（flash zh 0.7173→0.7839），Δ 在预期波动带内；排序 max-0902 > max ≈ flash > 27b / 3.7-flash > kimi-k3 >> deepseek。防守点：红队若以"单次涨 0.02 即方法不稳"攻击，与文件记录的波动带解释矛盾；排序稳定是比绝对值更硬的可复现信号。另：本次 v2 **无 403/404 整模型缺席**（8 模型均有有效返回，deepseek 失败为 200 空 content，`bailian_gold_v2_20260914.md:37-39`）——gold 层的"零缺席"与 extraction 层的"配额缺席"不在同一层，不得混用（见债务 D3）。

**B3. LDS-C ds-pro 与 max-0902 双双复现（p=0.0）【A：断言未入库，本文件不背书为 V】**
用户指令称"LDS-C ds-pro 与 max-0902 双双复现 p=0.0"。本轮已 grep 全仓（`research/` + `scripts/` + `outputs/` 索引）：未找到 ds-pro/max-0902 的 LDS-C 产物 JSON 或 perm 表。防守只做到：该方向若产物补齐且确为双模型 p=0.0，则构成跨提取器的宏观复现；**在产物入库前，任何"LDS-C 已双复现 verified"表述禁报**。另用户称"LDS-C 的 temp 拒收是冻结管线参数问题非模型问题"亦记 A：冻结管线确以 temperature=0 跑 gold（`bailian_gold_v2_20260914.md:3`），但 temp 拒收的 log/报错行未入库，不排除模型侧原因之前，只能报"原因待查"，不得报"已定为管线问题"。

**B4. kimi extraction / wiki 双线有返回，不是全灭【V（返回存在）+ A（可用性打分待补）】**
- extraction 存在性【V】：`ensemble_v2/kimi-k3/` 目录 102 个 data JSON + `_manifest.json:done` 清单对应；`quota_note` 明记尾部 8 连 HTTPError + direct probe 403（见 B5），即**前段是模型真实产出、尾部是配额拒收**，不是"模型全程无能力"。
- wiki 存在性【V】：`wiki_gloss_kimi_20260914.json` n=30，每条均有 `kimi-k3` gloss（如 G012 房产→real estate, property；G017 negative Freiheit→negative liberty），即 **30/30 有返回**。
- 打分【A】：用户称"wiki 宽松 28/30"——`gloss_cross_report_20260914.md:10` 的 28/30 是 **qwen flash vs max 一致率**，不是 kimi 对源匹配率；kimi 宽松口径（dwelling≈residence、homeless≈homelessness 是否计 hit）的 accept 规则未入库（qwen 侧 `accept/notes` 全空，`gloss_cross_report_20260914.md:35`），kimi 侧更无裁决表。故"wiki 宽松 28/30"记 A，**不得登记为 kimi 成绩**，待 `match_source` 口径 + 人工 accept 补齐后重算。
- temp 兼容【A】：manifest 未记录 kimi 调用 temperature；"temp 兼容"无参数行可引，记 A。

**B5. 缺席已全标注、配额 403 是基础设施天花板【V】**
- 全标注【V】：kimi-k3 manifest 区分 `quota_blocked_hint`（8 个选修尾部）vs `genuine_failed_hint`（en_ap_calculus r2/r3、en_probability 共 3 个）；ds-pro manifest `quota_blocked_hint` 49 连 + `genuine_failed_hint: []` + `quota_note` 明记"first OK 后 49 HTTPError 连续，direct probe 403 AllocationQuota.FreeTierOnly，failed entries from this window are quota-refusals, not model content failures"。
- 天花板非方法失败【V】：两 manifest 的 quota_note 均有 direct probe 验证（2026-09-15），与 gold 层"v2 无 403/404 缺席"对照，说明 403 是 extraction 大并发窗口的免费配额耗尽，不是抽取 prompt/解析器的方法失败。防守边界：只覆盖注记为 quota 的条目；genuine 3 条（kimi）不得搭车记免。
- 缺席≠0 分【V】：manifest 语义 `done/missing/failed` 三分，missing=未尝试（配额墙后未发起，如 3.7-flash note "breadth_403blocked_9of9_probe403_remaining_unattempted"），failed=已尝试未得；两类均不产生 F1 0 分直接拉均值——gold F1 只在 n=92 全返回集合上计算（deepseek 空 content 按 parse_fail 计入分母已是最严口径，`bailian_gold_v2_20260914.md:5,22`）。

## ② 承认的债务（红队可直接引用，蓝队不辩）

1. **ds-pro / v41-flash harness 不兼容，需换通道（方法债，不记模型死刑）**【V】：`bailian_gold_v2_20260914.md:24` 抽查结论：多数调用返回空 content（raw_len=0，疑 reasoning 输出走 reasoning_content 字段），按口径记 parse_fail（ds-pro fail 93.48%、v41-flash 56.52%）。认：当前 harness 取 content 字段对 deepseek 系不兼容；在换通道（读 reasoning_content / 换兼容端点）重跑前，deepseek 两行 F1（0.0652 / 0.3626）**不得引用为模型能力结论**，只可引用为"通道不兼容快照"。
2. **理化 0.02 待解释（数字债）**【V 数字、A 解释】：`compare_table2.md:22` 物理 middle 精确值 0.0208（§6.1 舍入口径 0.029 差异已注记）；`ensemble_v2/physchem/` 仅 24 个文件（理化各 3 章 × 2 模型 × 2 run），`depth24.json` 的 depth24/breadth41 均不含理化。认：理化样本窄 + 0.02 量级含义（差值/CDS/误差带？）未在 v2 写清；在口径冻结前，理化数字只许报"初探值、待解释"，不许进 headline。
3. **配额耗尽致覆盖不全（覆盖债）**【V】：max-0902 done 44 级/missing 50+/failed 20 级（`_manifest.json:101-127` note "run_absent=20"）；max missing 35 + failed 35；27b missing 60+；3.7-flash missing 37（breadth 403 墙）；ds-pro 49 连 quota；kimi 尾部 8 quota + genuine 3。认：depth-first cap100 + 免费配额墙 = breadth 尾部系统性缺席；任何"全教材覆盖结论"禁报，覆盖率必须按 manifest done/missing/failed 三数并报。
4. **kimi LDS-C incomplete（产物债）**【A 转债务】：与 B3 对称——kimi extraction 有返回 ≠ kimi LDS-C 已算出；LDS-C 计算产物未入库前，"kimi LDS-C 可用/不可用"双方都禁报，只许报"extraction 返回存在、LDS-C 待算"。
5. **qwen 系 fail 口径需逐模型单报（表述债）**【V】：B1 已纠偏；此后凡报"qwen 零失败"必须限定名单（max-0902/max/3.7-flash），flash（1 parse）与 27b（1 exc+3 parse）不得省略。

## ③ 可登记口径（只许这样报；出现禁语即判违规）

- **允许报（gold 头部）**："temperature=0、n=92（zh36/de29/en27）同 prompt/同参数分拆运行：qwen3.8-max-0902 overall 0.7376、qwen3.8-max 0.7325、qwen3.7-flash 0.7114，三模型 fail_rate 0.00%；flash 0.7113（fail 1.09%）、27b 0.6977（fail 4.35%）；复跑 Δ（flash +0.0283、max +0.0112）在波动带内，排序 max-0902 > max ≈ flash > 27b/3.7-flash > kimi-k3 >> deepseek（deepseek 为通道不兼容快照，不得作能力解读）。"
- **允许报（extraction 缺席）**："ensemble_v2 七 manifest done/missing/failed 三数并报；注记为 FREE_QUOTA_EXHAUSTED_403（direct probe 2026-09-15 验证）的条目记基础设施天花板，不记模型内容失败；kimi genuine 3 条（en_ap r2/r3、en_probability）除外。depth24/breadth41 外的理化 24 文件为初探，不进覆盖率分母。"
- **允许报（wiki）**："qwen flash vs max 交叉一致 28/30（G012/G017 分歧，`gloss_cross_report_20260914.md:10`），flash 对源 27/30、max 对源 26/30，人工 accept 未闭环故维持 needs_review；kimi 30/30 有返回（`wiki_gloss_kimi_20260914.json`），宽松口径打分待 accept 规则入库后重算。"
- **允许报（宏观分层，继承 v1）**："宏观 LDS-C 结论与微观抽取噪声不在同一检验对象上；微观噪声不颠覆宏观、宏观显著亦不得反证微观无错（`blue_defense_20260914.md:30-31`）。v2 新增的 LDS-C 双复现断言在产物入库前不适用本条。"
- **禁语清单**："qwen 系全员零失败""LDS-C 已双复现 verified""temp 拒收已定为管线问题""kimi wiki 28/30 已得分""配额条目即模型失败""缺席按 0 分计""理化 0.02 已解释""deepseek F1 即能力定论""全教材已覆盖"。其中"qwen 系全员零失败"特禁：与 `.json:scores` 的 flash/27b fail 数直接矛盾。
- **转正规则**：B3（LDS-C 产物 + perm 表入库）→ A 转 V 方可报复现；B4（kimi/qwen wiki accept 规则 + 裁决表入库）→ 方可报宽松分；D1（deepseek 换通道重跑）→ 方可报 deepseek 能力行；D2（理化口径冻结）→ 方可报理化 headline。在此之前 verdict 冻结，新增证据只追记 A→V 状态变更。
