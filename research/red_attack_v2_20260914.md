# 红队攻击报告 v2：异构矩阵未完成、harness 惨案、跨域零重合（2026-09-14）

- 立场：红队（攻击方），只找死穴，不洗地。v1 攻击 mimo 基线；v2 攻击 ensemble_v2 + bailian_gold_v2 + LDS-C/理化/wiki 三条外线。
- 取证范围：`research/ensemble_v2/*/_manifest.json` 7 模型全读（done/missing/failed/quota_note 逐数）、`research/bailian_gold_v2_20260914.md` 全读（含 §5 缺席口径）、`research/compare_table2.md`（理化 Jaccard）、`research/baseline_board.md §7` + `research/wiki_gloss_kimi_20260914.json`（wiki 交叉）、`research/gloss_cross_report_20260914.md`。
- 本文件为唯一新产出，不碰其它文件。

## ① 最强攻击点（按杀伤力排序）

### A1. Bailian Gold v2 harness 惨案：ds-pro 0.065 / v41flash 0.36 不是"能力差"，是 harness 不兼容——"异构矩阵"叙事被污染（最强）
- 实测（`bailian_gold_v2_20260914.md §1`，n=92，temperature=0，同 prompt 同参数）：`deepseek-v4-pro-0813 overall=0.0652, fail_rate=93.48% (parse=86)`；`deepseek-v4.1-flash overall=0.3626, fail_rate=56.52% (parse=52)`；`kimi-k3 overall=0.5535`；qwen 系 0.6977~0.7376（max-0902 最高 0.7376）。
- 同文件 §2 自认：deepseek 多数调用返回**空 content（raw_len=0，疑 reasoning 输出走 reasoning_content 字段），属模型/通道兼容问题，按口径记 parse_fail**。
- 红队翻译：ds-pro 的 0.065 里 86/92 是 harness 没接到输出，不是模型答错。把两个"接线都没接对"的成员计入"异构多样性"，等于把**断路器当发电机**报装机容量。任何 ensemble 聚合（投票/平均/多样性增益）只要含 ds 系权重，即被空 content 稀释——**分母是 92，分子是空气**。
- 连带杀伤：§3 自认 temperature=0 下仍有 run 间波动（flash zh 0.7173→0.7839，Δ=+0.0283）。"temperature=0=确定性可复现"的承诺已死；单次运行的任何 headline F1 都是**一次抽样**，不带 CI 即不可引用。

### A2. Ensemble_v2 七模型覆盖率惨案：配额耗尽 403 = 实验未完成，所谓"矩阵"是残缺矩阵
- ds-pro（`ensemble_v2/deepseek-v4-pro-0813/_manifest.json`）：calls=100，**done 仅 3**，missing 60，failed 49；quota_note 自认 `FREE_QUOTA_EXHAUSTED_403 AllocationQuota.FreeTierOnly verified by direct probe 2026-09-15; all 49 HTTPError consecutive after first OK`。 genuine_failed_hint=[]——**49 个 failed 全是配额拒绝，不是模型内容失败**。
- kimi-k3（`ensemble_v2/kimi-k3/_manifest.json`）：quota_note 自认 `kimi tail 8x HTTPError consecutive; direct probe 403`；failed 11 中 8 个（选修 2-2 ch1.5 起整段）为 quota_blocked，genuine 仅 3（en_ap r2/r3、en_probability）。
- v41flash（`ensemble_v2/deepseek-v4.1-flash/_manifest.json`）：done 18 / failed 30 / **missing 66（含中文全系 60+：概率论/线代/微分方程/选修整段缺席）**。
- qwen3.7-flash：note 自认 `depth72_done_breadth_403blocked_9of9_probe403_remaining_unattempted`——breadth 9/9 探针全 403，剩余未敢再试。
- qwen3.8-max / max-0902：cap=100 截断，missing 30~50（max-0902 note `run_success=4`，max note `run_absent=34`）。
- 红队翻译：缺席**非随机**——ds-pro 中文概率论/线代整块 missing、v41flash 中文整块 missing、breadth 全 403。任何跨模型聚合指标（canonical65、一致率、Jaccard 均值）都建立在**幸存者偏差**上：分母是"配额还剩谁"，不是"设计要谁"。`bailian_gold_v2 §5` 写"本次无 403 整模型缺席"只覆盖 gold 92 条小 bench，**ensemble 大矩阵的 403 缺席照样成立**，两文件口径不得互抵。

### A3. LDS-C 线 kimi-k3 temperature 不兼容 + incomplete：跨模型可比性已死
- 取证：gold v2 在 temperature=0 下 kimi-k3 可跑（F1 0.5535，parse 7）；LDS-C 链上 kimi-k3 出现 temperature 参数不兼容（通道拒收/行为异常）导致 incomplete——**同一模型在两条 harness 上参数语义不一致**。
- 红队翻译：harness 按模型各行其是（gold：temp=0 强塞；LDS-C：temp 不兼容直接 incomplete；deepseek：max_tokens 16000 vs kimi 8000，见 kimi manifest note `per-model max_tokens`）。三处口径都不统一，报"跨模型 LDS-C 对照"等于**用摄氏度减华氏度**。凡报跨模型对照，必须先附"参数兼容矩阵（temp/max_tokens/parse 口径×模型）"，缺此表即死。

### A4. 理化 Jaccard 均值 ~0.02：重提方法在新域零重合，数学域结论不得外推
- 实测（`compare_table2.md`）：物理 middle **0.0208**，化学 high **0.0298**；§6.1 物理 Mittel 0.029（舍入外差异已自认）——量级一致：**百分之二**。
- 对照 v1 A3：数学域 mimo–bailian 概念 J 已是 0.04~0.41、关系 J 0.00~0.11；理化 0.02 比数学最烂的 khan3-4（0.044）还烂一半。
- 红队翻译：两种可能，无中间选项——（a）重提方法在理化域全错（公式/结构化文本抽取链对物理化学失效）；（b）理化图根本不可比（粒度/层级口径与数学不统一）。无论哪种，"数学 ensemble 验证了方法"的叙事都**不得外推到理化**。凡在 poster/论文里把理化 220/367 节点数与数学 556 并列当"规模证据"，而不同时并列 0.02 重合率，即选择性报告。

### A5. Wiki 三方严格仅 21/30=70%：对照证据未转正，"wiki 验证数学"禁报
- 实测：`bailian_gold_v2 §4` 双模型宽松一致 28/30=93.3%（分歧 G012 房产 property vs real estate、G017 negative Freiheit liberty vs freedom；flash 匹配源 27/30、max 26/30）。**三方严格口径（源×双模型×kimi 或人工 accept 全过）仅 21/30=70%**。
- `baseline_board.md §7` 已判：wiki gloss 系 deepseek-v4-flash 英文化、无人工抽检、无第二模型交叉时"**盲审门 F1≥0.85∧Agr≥0.8∧每语≥0.7 未验，不得作内容证据**"；`wiki_gloss_audit_30.json` accept/notes 全空、`gloss_cross_report` 自认缺人工 accept。
- 红队翻译：93.3% 是"两个 qwen 互相抄作业的一致率"，不是"对错率"；70% 是离转正门还差 15 个百分点的**未完成品**。任何"wiki 对照支持数学 LDS 结论"的句子，引用的是未转正证据，按 BWKI 诚信规则等同于**引用草稿当定理**。

### A6. T1 去污 + size-match 反转仍悬在头顶：ensemble 越大，artefact 放大器越大
- `debate_verdict R2`：T1 去污 167/219 德标签含 CJK，剔除后 ZH-DE J_node 0.556→0.020（LDS 0.52→0.99）；size-match k=15/25/35 gap 全负（−0.023/−0.053/−0.080，wiki>math）。
- 红队补刀：ensemble 矩阵把 7 个带同一标签污染的提取器拼在一起，投票投出的是**污染的共识**，不是真相的共识。多样性只在"错误不相关"时成立；标签 artefact 在七模型间完全相关（同一对齐表、同一 CJK 混入），ensemble 是 artefact 的**放大器**，不是**过滤器**。

## ② 若我是 BWKI 评委，我会如何逐条判死刑

1. **"异构 ensemble 矩阵验证了结论鲁棒性"** —— 死刑。ds-pro done 3/100、v41flash 中文整块缺席、breadth 9/9 探针 403，矩阵残缺且缺席非随机。鲁棒性要求"缺席随机或补齐"，本案两者皆无，最多叫"**配额幸存者子集的描述统计**"。
2. **"ds-pro F1 0.065 说明该模型不适合本任务"** —— 死刑。86/92 是空 content harness 不兼容（reasoning_content 字段未接），不是任务失败。把接线问题报成能力问题，是**归因错位**；正确表述是"本 harness 下 ds 系不可测（unmeasurable），F1 数字无效"。
3. **"kimi-k3 F1 0.55 / v41flash 0.36 构成能力排序 max>flash>kimi>>deepseek"** —— 死刑。排序混杂了 parse 口径（kimi parse 7 vs ds-pro parse 86）、max_tokens 口径（16000 vs 8000）、temp 兼容性三处混杂。排序成立的前提是"同 harness 同口径"，本案三处全破，排序只是**harness 亲和度排序**。
4. **"理化重提复用了数学管线，规模更大"** —— 死刑。Jaccard 0.02（物理 0.0208/化学 0.0298）面前谈规模是转移话题。评委只接受：先解释 0.02（方法错还是口径错），再谈节点数；**0.02 未解前一切理化规模数字都是装饰**。
5. **"wiki 双模型一致 93.3%"** —— 死刑（降级为中性描述，不许当证据）。三方严格 70% 未过盲审门（0.85/0.8），93.3% 是模型间互相抄作业率。报 93.3% 不报 21/30 即 cherry-picking。
6. **"temperature=0，结果确定可复现"** —— 死刑。gold v2 自认 temp=0 下 flash zh 0.7173→0.7839（Δ 0.066）。确定性主张与自家数据矛盾；所有单次 F1 必须带 run 间波动声明，否则按**虚假精度**处理。
7. **任何引用 ensemble 聚合数字（投票/平均/Jaccard 均值）而不附缺席表者** —— 死刑。缺席表 = 每模型 done/missing/failed/quota 四列（manifest 原数）。无缺席表的聚合数一律视为**幸存者偏差**，评委有权直接划掉整段。
8. **"LDS-C 跨模型对照显示…"** —— 死刑（在参数兼容矩阵补齐前）。temp 不兼容 + max_tokens 双标 + parse 口径三分，跨模型差值里模型效应与 harness 效应完全混杂，不可归因。

## ③ 结论降级与禁报清单

### 必须降级的结论
- "异构矩阵" → 降级为"**残缺矩阵（配额截断版）**：ds-pro done 3、v41flash 中文缺席、breadth 403 冻结；一切聚合仅描述幸存者子集"。
- "ds-pro/v41flash 能力垫底" → 降级为"**本 harness 下不可测**（空 content / parse_fail），F1 数字无效，不得排序"。
- "跨模型分歧揭示模型差异" → 降级为"**分歧 = 模型差异 + harness 差异 + 配额缺席三混杂**，未解耦前不得归因模型"。
- "方法可迁移理化" → 降级为"理化 Jaccard ~0.02，迁移失败（原因未定位），数学结论不得外推"。
- "wiki 对照支持主结论" → 降级为"三方严格 21/30=70%，盲审门未过，**不得作内容证据**（baseline_board §7 维持）"。

### 数字不许再报（再报即判学术不端嫌疑）
1. 不许报 ds-pro F1 0.065 / v41flash F1 0.36 为"能力值"——只许报"**harness 不兼容下无效值**（parse 86/92、52/92）"。
2. 不许报任何 ensemble 聚合数而不附七模型缺席四列（done/missing/failed/quota，manifest 原数）；不许用 gold 小 bench 的"无 403 缺席"（§5）掩盖大矩阵的 403 缺席。
3. 不许报跨模型 LDS-C 差值而不附参数兼容矩阵（temp/max_tokens/parse×模型）。
4. 不许报理化节点规模（367/220）而不并列 Jaccard 0.0208/0.0298；不许把数学 CDS/HDS 口径与理化混算（compare_table2 注 1：219 vs 556 不可混用）。
5. 不许报 wiki 一致率只报 28/30=93.3%——必须并列三方严格 21/30=70% + 盲审门未过声明。
6. 不许报 temperature=0 单次 F1 为精确值——必须注明 run 间波动带（flash zh Δ级 0.06，max Δ 0.01）。
7. 不许报"canonical65/共识集"为完成品——在 ds-pro 3 done + v41flash 66 missing + breadth 403 冻结下，只许报"**配额截断快照（snapshot），待补跑**"。
8. v1 禁报延续：precision 下限 0.78（实测 0.70）、recall 下限 0.27（实测 0.22）、"5 review/1 fail"（实为 10/2）、"flash-vs-max J 0.54"（无出处）均继续禁报。
