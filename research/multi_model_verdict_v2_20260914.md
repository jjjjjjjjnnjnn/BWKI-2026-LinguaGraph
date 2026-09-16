# 多模型终审裁决 v2（2026-09-14）：终审裁决员 v2

- 地位：本文件为红 `red_attack_v2_20260914.md` × 蓝 `blue_defense_v2_20260914.md` 的终审裁决，冻结 `consensus_v2_20260914.md` + `bailian_gold_v2_20260914.md` + LDS-C / wiki / 理化三条外线的可登记口径。只新增本文件，不改它文件。
- 依据（行号可查）：red v2 §A1–A6 + §②1–8 + §③；blue v2 §B1–B5 + §债务D1–D5 + §③可登记口径；consensus v2 覆盖表/intra/inter/vs mimo/表决；gold v2 §1–§5。
- 证据分级（继承 blue v2）：**V=文件已验证 / A=断言未入库，只记方向不进 verified**。

## ① 逐条裁决

### C1. intra ~0.55–0.73：红 A1-后半 + A6 部分成立 →「非确定性定量成立」，temperature=0 确定性主张死刑【V】
- 实测（consensus v2 §1）：v41flash 0.5625 / 27b 0.5534 / max 0.6079 / max-0902 0.6042 / 3.7flash 0.6035 / kimi 0.7347 / ds-pro 0.6667（n=1，仅参考）。主力区间 0.55–0.73，均值 ~0.6。
- gold v2 §3 佐证：temperature=0 下 flash zh 0.7173→0.7839（Δ=0.066），flash overall +0.0283、max +0.0112。
- 裁决：**红对**。单模型 temp=0 仍有 ~40% run 间概念分歧（1−0.6），「temperature=0=确定可复现」禁报。所有单次 F1 / Jaccard 均为一次抽样，必须带波动带（flash 级 Δ~0.03–0.06，max 级 Δ~0.01）。排序稳定（B2）可报，绝对值精确引用禁报。
- 登记句（允许）：「intra 概念 Jaccard 0.55–0.73（kimi 0.73 最高），temp=0 下 run 间分歧 ~40%，单次值为快照」。

### C2. inter 均值 0.4629：红"证伪"不成立，蓝"宏观分层"成立 → 0.46≠证伪，归因=粒度差+厂商偏置【V】
- 实测（consensus v2 §2）：非对角 21 对均值 0.4629；行均值 ds-pro 0.4572 / v41 0.4580 / kimi 0.4283 / 3.7flash 0.4038 / 27b 0.5067 / max 0.5005 / max-0902 0.4859。qwen 系内 max–max0902 0.5985 为全矩阵最高，厂商聚类成立。
- 裁决：**红错、蓝对**。0.46 处于"同任务不同粒度/抽取风格"的预期带（v1 宏观/微观分层原则延续）：概念归一化=小写+去空白的粗口径下，27b 行均值最高（0.51）恰说明"中庸粒度最易相交"，不是"最准"。inter 分歧只许报「粒度差+厂商偏置混杂」，不许报「方法证伪」，亦不许报「模型能力排序」。
- 连带：T1 去污 artefact（red A6，ZH-DE J 0.556→0.020）在七模型共用同一对齐表/同一 CJK 混入下完全相关，ensemble 投票是 artefact 放大器。裁决：ensemble 表决集（§4）在去污重算前只许报「污染快照」，禁报「共识真相」。

### C3. vs mimo 0.21–0.38：红"单次快照"成立 → mimo 维持、待清洗，双方各打五十大板【V】
- 实测（consensus v2 §3）：v41 0.2137 / max 0.2295 / max-0902 0.2415 / kimi 0.2427 / 27b 0.2492 / 3.7flash 0.2583 / ds-pro 0.3809（n=2，小样本上浮，不可引用）。
- 表决（§4）：收录概念 491 / Solid 145 / Weak 506 / Hypo 1554 / mimo 独有候选删 76。
- 裁决：**「单次快照」成立**。任一单模型 vs mimo 0.21–0.38 均不得证伪 mimo，亦不得确证任一 ensemble 成员。mimo 24/24 全覆盖维持基线地位，但 76 个 mimo 独有概念在去污+T1 重算前只许报「候选删」，禁报「已删/已确证」。表决四数（491/145/506/1554）只许并列覆盖表报「配额截断快照」，禁报「完成品 canonical 集」。

### C4. ds 系 harness 不兼容：红 A1-前半 + 判例 2 全成立 → F1 数字无效，聚合必须剔除 ds 系或标 harness 失败【V】
- 实测（gold v2 §1–§2）：ds-pro overall 0.0652（parse 86/92，fail 93.48%）、v41flash 0.3626（parse 52/92，fail 56.52%）；抽查结论空 content raw_len=0、疑 reasoning_content 字段未接。
- 排序（gold v2）：max-0902 0.7376 > max 0.7325 > 3.7flash 0.7114 ≈ flash 0.7113 > 27b 0.6977 > kimi 0.5535 >> deepseek（无效）。
- 裁决：**红全对，蓝 D1 自认有效**。ds-pro/v41flash 两行 F1 禁止作能力值、禁止进排序（排序分母只许到 kimi 为止，且必须注 max_tokens 16000 vs 8000、parse 口径差异）。任何 ensemble 聚合（投票/平均/inter 均值）二选一：(a) 剔除 ds 系重算，或 (b) 保留但整列标「harness 不兼容快照（parse 86/52）」。把空 content 计入分母的 0.065/0.36 只许报「通道不兼容快照」，违者按归因错位记违规。
- 表述纠偏（blue B1/B5）：「qwen 系 0.70–0.74 零失败」禁语；精确只许「头部三模型 max-0902/max/3.7-flash 0.71–0.74 零失败；flash fail 1.09%（parse 1）、27b fail 4.35%（exc 1+parse 3）」。

### C5. 配额 403 = 未完成非失败，覆盖表冻结：红 A2 + 判例 1/7 成立 → 缺席禁计 0 分，聚合禁报完成品【V】
- 实测（consensus v2 覆盖表 + manifest 取证）：深度 24 done：kimi 24 / 3.7flash 24 / 27b 17 / max 15 / max-0902 15 / v41 10 / ds-pro 2；mimo 24/24，spark 11/24，bailian 0。ds-pro manifest done 3 + failed 49 连 quota（direct probe 403 验证）+ missing 60；kimi 尾部 8 quota + genuine 3；v41 中文整块 missing 66；3.7flash breadth 9/9 探针 403。
- gold v2 §5「本次无 403 缺席」仅限 gold n=92 小 bench，不得掩盖 ensemble 大矩阵缺席（红 A2 对）。
- 裁决：**配额条目记基础设施天花板，不记模型失败；missing/failed（quota 注记者）一律缺席不计分，禁计 0 分拉均值**（consensus「缺席一律不计分」维持）。gold 空 content 按 parse_fail 计入分母已是最严口径，维持。任何 ensemble 聚合数必须并列七模型 done/missing/failed/quota 四列，否则按幸存者偏差整段划掉。canonical/共识集只许报「配额截断快照（snapshot），待补跑」。

### C6. LDS-C 双复现 p=0.0 + kimi incomplete：蓝 B3/B4 维持 → 方向成立、verified 禁报【V（extraction 存在）+ A（LDS-C 复现）】
- 已验（V）：kimi extraction 102 data 有返回、wiki 30/30 有返回均为真实产出；ds-pro/v41 的 LDS-C 输入残缺（done 3/中文缺席）故其 LDS-C 差值不可归因。
- 未验（A）：「LDS-C ds-pro 与 max-0902 双双复现 p=0.0」「temp 拒收系冻结管线参数问题」——全仓无 LDS-C 产物 JSON/perm 表/temp 拒收 log，维持 A。
- 裁决：p=0.0 方向记「待入库复现信号」，在产物 + perm 表入库前，任何「LDS-C 已双复现 verified」「temp 拒收已定为管线问题」「kimi LDS-C 可用/不可用」三句全部禁报，只许报「extraction 返回存在、LDS-C 待算；跨模型 LDS-C 差值在参数兼容矩阵（temp/max_tokens/parse×模型）补齐前禁报」。

### C7. wiki 三方 + 理化 0.02：红 A4/A5 基本成立 → wiki 宽松可用、严格禁报；理化 0.02=粒度错位，verification 子集为真信号方向【V 数字 + A 解释】
- wiki 实测（V）：qwen flash vs max 交叉一致 28/30=93.3%（G012/G017 分歧），flash 对源 27/30、max 对源 26/30；kimi 30/30 有返回；三方严格（源×双模型×kimi/人工 accept 全过）21/30=70%；人工 accept/notes 全空。
- 裁决 wiki：28/30 只许报「qwen 双模型交叉一致率（非对源正确率），人工 accept 未闭环，维持 needs_review」——**宽松引用可用（必须带 needs_review 声明），严格 21/30 未过盲审门（0.85/0.8）禁作内容证据**，「wiki 验证数学」禁报（baseline_board §7 维持）。
- 理化实测（V）：物理 middle 0.0208、化学 high 0.0298（compare_table2），量级 ~0.02，比数学最烂 khan3-4（0.044）还低一半；physchem 仅 24 文件（各 3 章×2 模型×2 run），depth24/breadth41 均不含理化。
- 裁决理化：0.02 只许报「初探值、待解释」，禁进 headline、禁与数学 556 节点并列作规模证据（219 vs 556 不可混算）。解释方向记 A：**全量 0.02=粒度错位（方法口径与理化层级不对齐），verification 子集 0.09–0.24 为真信号方向**——在口径冻结（差值/CDS/误差带三选一定位）前，数学结论不得外推理化。

## ② 最终可登记口径

### 允许清单（只许这样报）
1. gold 头部：「temp=0、n=92（zh36/de29/en27）同 prompt 分拆运行：max-0902 0.7376、max 0.7325、3.7-flash 0.7114，三模型 fail 0.00%；flash 0.7113（fail 1.09%）、27b 0.6977（fail 4.35%）；复跑 Δ（flash +0.0283、max +0.0112）在波动带内；排序 max-0902>max≈flash>27b/3.7-flash>kimi 0.5535>>deepseek（通道不兼容快照，不作能力解读）。temp=0 仍有 run 间波动（flash zh Δ~0.06），单次值为快照。」
2. 共识快照：「深度 24，intra 0.55–0.73（kimi 0.73 最高）、inter 均值 0.4629、vs mimo 0.21–0.38；表决收录 491 / Solid 145 / Weak 506 / Hypo 1554 / mimo 独有候选删 76；覆盖 kimi 24、3.7flash 24、27b 17、max 15、max-0902 15、v41 10、ds-pro 2。以上为配额截断快照（去污重算前为污染快照），非完成品。」
3. 缺席口径：「七 manifest done/missing/failed/quota 四数并报；FREE_QUOTA_EXHAUSTED_403（direct probe 2026-09-15）记基础设施天花板；kimi genuine 3 条除外；缺席不计分、禁计 0 分。」
4. ds 口径：「ds-pro 0.065（parse 86/92）、v41flash 0.36（parse 52/92）为 harness 不兼容快照（空 content / reasoning_content 未接），F1 无效；聚合须剔除 ds 系或整列标 harness 失败。」
5. wiki 口径：「qwen 交叉一致 28/30（G012/G017 分歧）、flash 对源 27/30、max 对源 26/30，accept 未闭环维持 needs_review；kimi 30/30 有返回，打分待 accept 规则入库重算。」
6. LDS-C/理化口径：「LDS-C p=0.0 为待入库方向（产物+perm 表到位前禁报 verified）；理化 J~0.02 初探待解释，verification 子集 0.09–0.24 为真信号方向；跨模型 LDS-C 差值待参数兼容矩阵。」

### 禁止清单（出现即违规，再报按学术不端嫌疑记）
1. 报 ds-pro 0.065 / v41 0.36 为能力值或进能力排序。
2. 报「qwen 系全员零失败」「temperature=0 确定可复现」「单次 F1 精确值」（不带波动带者）。
3. 报任何 ensemble 聚合数不附七模型缺席四列；用 gold「无 403」掩盖大矩阵 403。
4. 报跨模型 LDS-C 差值不附参数兼容矩阵；报「LDS-C 已双复现 verified」「temp 拒收已定管线问题」。
5. 报 403 缺席为模型失败；缺席计 0 分拉均值。
6. 报理化规模（367/220）不并列 0.0208/0.0298；数学↔理化混算外推；理化 0.02 进 headline。
7. 报 wiki 只报 28/30=93.3% 不并列三方严格 21/30=70% + needs_review；报「wiki 验证数学」。
8. 报 canonical65/共识集为完成品；报「异构矩阵验证鲁棒性」「全教材已覆盖」。
9. v1 禁报延续：precision 下限 0.78（实测 0.70）、recall 下限 0.27（实测 0.22）、「5 review/1 fail」（实为 10/2）、「flash-vs-max J 0.54」（无出处）。

## ③ 执行令：修数 vs Future 分类 + 补跑优先级

### A. 修数（改数字/重算即闭环，不进 Future）
- R1. 共识聚合 ds 系处理：按 C4(a)/(b) 二选一重算 inter 均值 + 表决（去污前标污染快照）。关闭条件：聚合表附剔除/标注声明。
- R2. T1 去污重算：167/219 德标签 CJK 剔除后重跑 ZH-DE J + 表决 491/145/506/1554 全量更新。关闭条件：去污前后对照表入库。
- R3. wiki accept 闭环：qwen 侧 accept/notes + kimi 侧 match_source 口径 + 裁决表入库，重算宽松分（28/30 转正或修正）。关闭条件：裁决表 + 人工 accept 行入库。
- R4. 表述修数：「qwen 全员零失败」→头部三模型限定；单次 F1 一律加波动带注脚。关闭条件：grep 全仓禁语清零。

### B. Future（需新实验/配额/口径冻结， verdict 冻结期只追记 A→V）
- F1. deepseek 换通道重跑（读 reasoning_content / 换兼容端点）→ D1 转正，方可报 deepseek 能力行。
- F2. LDS-C 产物入库（ds-pro/max-0902 perm 表 + kimi LDS-C 计算 + temp 拒收 log）→ B3/B4 转 V。
- F3. 理化口径冻结（0.02 定位：方法错/口径错二选一 + verification 0.09–0.24 复算）→ D2 转正。
- F4. 参数兼容矩阵（temp/max_tokens/parse×模型）→ 跨模型 LDS-C 对照解禁前提。

### C. 配额恢复后补跑优先级（按解冻价值排序）
1. **P1 ds-pro depth**：done 3→depth24 补齐（配额杀伤最大，inter/vs mimo 表的 ds-pro 行 n=1–2 全不可用；补齐后 C2/C3 小样本上浮消除）。
2. **P2 kimi tail**：选修 2-2 ch1.5 起 8 连 quota + genuine 3（en_ap r2/r3、en_probability）→ kimi 是唯一 depth24 全勤（24/24），尾部补齐即全矩阵唯一完整列。
3. **P3 v41 中文**：中文概率论/线代/微分方程/选修整块 missing 66（最大非随机缺席；补齐后中文子集 inter 可算，否则中德分层结论永久冻结）。
4. **P4 breadth**：3.7flash breadth 9/9 探针 403 + max/max-0902 cap100 截断部分（广度只在 P1–P3 闭环后开工；开工前 breadth41 禁报覆盖率分母）。
- 铁律：补跑只许顺序低并发（gold v2 §2 并发拥塞教训），每模型附 direct probe 行；新增证据只追记 A→V，不改本 verdict 行号。
