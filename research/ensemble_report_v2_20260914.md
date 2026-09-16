# Ensemble 总报告 v2 20260914（汇总·只引用不重算）

> 地位：本文件为唯一新文件，汇总 `research/consensus_v2_20260914.md` + `research/bailian_gold_v2_20260914.md` + `research/multi_model_verdict_v2_20260914.md`。所有数字均为引用，不重算。离线口径继承 consensus v2：归一化=小写+去全部空白；Jaccard=|交|/|并|（空空=1.0）；缺席一律不计分。
> 输入快照：mimo 深度 24/24；spark audit 深度 11/24（总数 12）；bailian `*.bailian.json` 0 个（缺席）。
> 外线状态（任务给定引用）：LDS-C 双复现 p=0.0 + kimi incomplete；wiki 三方 21/28；理化 J 0.02 + verification 0.09–0.24；配额 403 未完成；pytest 84。

## ① 矩阵与覆盖（7 模型 × 深度/广度 done/缺席表）

### 1.1 深度 24 覆盖表（引用 consensus v2 §覆盖表 + JSON coverage）

| 模型 | depth done /24 | 缺席 | 代表 run r1 | 回退 r2/r3 | intra_n | total_bases（含广度+深度） | total_runs |
|---|---:|---:|---:|---:|---:|---:|---:|
| deepseek-v4-pro-0813 | 2 | 22 | 1 | 1 | 1 | 2 | 3 |
| deepseek-v4.1-flash | 10 | 14 | 8 | 2 | 6 | 10 | 18 |
| kimi-k3 | 24 | 0 | 24 | 0 | 23 | 56 | 102 |
| qwen3.7-flash | 24 | 0 | 24 | 0 | 24 | 25 | 73 |
| qwen3.8-27b | 17 | 7 | 16 | 1 | 16 | 17 | 48 |
| qwen3.8-max | 15 | 9 | 15 | 0 | 15 | 15 | 44 |
| qwen3.8-max-0902 | 15 | 9 | 15 | 0 | 14 | 15 | 43 |

- mimo 深度覆盖 24/24；spark audit 深度覆盖 11/24；bailian 0（全部缺席，missing 不计分）。
- 广度侧（引用 verdict v2 C5/C③-C）：ds-pro manifest done 3 + failed 49（连 quota，direct probe 403 验证）+ missing 60；kimi 尾部 8 quota + genuine 3；v41 中文整块 missing 66；3.7-flash breadth 9/9 探针 403；max/max-0902 cap100 截断部分。广度 breadth41 在 P1–P3 闭环前禁报覆盖率分母。
- 口径铁律（引用 verdict C5）：配额条目记基础设施天花板，不记模型失败；missing/failed（quota 注记者）一律缺席不计分，禁计 0 分拉均值；gold v2 §5「本次无 403 缺席」仅限 gold n=92 小 bench，不得掩盖大矩阵缺席。

### 1.2 inter 模型矩阵（引用 consensus v2 §2，深度 24 代表 run，概念 Jaccard，括号=n 共存文件）

|  | ds-pro | v41flash | kimi-k3 | 3.7-flash | 27b | max | max-0902 |
|---|---|---|---|---|---|---|---|
| ds-pro | 1.0000 | 0.5 (1) | 0.3296 (2) | 0.3189 (2) | 0.5556 (1) | 0.5988 (2) | 0.4402 (2) |
| v41flash | 0.5 (1) | 1.0000 | 0.4069 (10) | 0.3663 (10) | 0.4951 (10) | 0.5111 (9) | 0.4686 (9) |
| kimi-k3 | 0.3296 (2) | 0.4069 (10) | 1.0000 | 0.4612 (24) | 0.4888 (17) | 0.4193 (15) | 0.4638 (15) |
| 3.7-flash | 0.3189 (2) | 0.3663 (10) | 0.4612 (24) | 1.0000 | 0.4787 (17) | 0.3813 (15) | 0.4161 (15) |
| 27b | 0.5556 (1) | 0.4951 (10) | 0.4888 (17) | 0.4787 (17) | 1.0000 | 0.4937 (14) | 0.5283 (14) |
| max | 0.5988 (2) | 0.5111 (9) | 0.4193 (15) | 0.3813 (15) | 0.4937 (14) | 1.0000 | 0.5985 (15) |
| max-0902 | 0.4402 (2) | 0.4686 (9) | 0.4638 (15) | 0.4161 (15) | 0.5283 (14) | 0.5985 (15) | 1.0000 |

- 矩阵均值（非对角 21 对均值）：**0.4629**。行均值：ds-pro 0.4572 / v41 0.4580 / kimi 0.4283 / 3.7-flash 0.4038 / 27b 0.5067 / max 0.5005 / max-0902 0.4859。全矩阵最高为 qwen 系内 max–max0902 0.5985（厂商聚类成立）。
- ds-pro 行 n=1–2 全为小样本，不可用（待 P1 补齐）。

### 1.3 多数表决 v2 总数 + 逐文件覆盖（引用 consensus v2 §4，thr=n//2+1）

- 总数：收录概念 **491**；Solid 关系 **145**；Weak（2..thr-1）**506**；Hypothetical（1 源）**1554**；mimo 独有候选删 **76**。明细见 `research/consensus_v2_20260914.json`。
- 逐文件（basename | 源数 | 阈值 | 收录 | 候选删 | Solid | Weak | Hypo）：de_abitur_lk 7/4/20/5/2/40/92；de_dgl_pde_ch9-11 7/4/25/3/7/40/63；de_fischer 7/4/25/1/15/20/29；de_forster 9/5/17/0/14/21/41；de_lambacher_5-8 7/4/36/2/8/34/45；de_lambacher_erweitert 6/4/24/9/3/30/88；de_wahrscheinlichkeit 7/4/35/2/12/29/57；de_westermann 7/4/23/4/2/33/84；en_ap 6/4/29/7/15/23/42；en_ib 8/5/22/1/4/38/81；en_igcse 6/4/14/9/3/22/80；en_khan_3-4 8/5/18/3/4/38/82；en_khan_5-6 7/4/23/8/7/27/98；en_khan_6-8 8/5/24/6/5/27/102；en_khan_k-2 7/4/12/3/2/20/126；en_stewart 6/4/17/0/3/29/44；zh_偏微分ch10 4/3/18/0/6/14/36；zh_初中七年级 4/3/30/3/12/12/41；zh_初中九年级 3/2/23/7/14/0/26；zh_小学一年级下 3/2/23/2/0/0/59；zh_微分方程ch3 4/3/9/0/0/1/67；zh_微分方程ch4 4/3/10/1/0/7/60；zh_选修2-2_ch1.2 4/3/4/0/1/1/70；zh_选修2-2_ch1.3 3/2/10/0/6/0/41。
- 定性（引用 verdict C3）：四数只许并列覆盖表报「配额截断快照」，禁报「完成品 canonical 集」；去污重算前为「污染快照」，禁报「共识真相」。

## ② 核心数字（只引用）

### 2.1 intra 自一致性（引用 consensus v2 §1，概念 Jaccard）

| 模型 | 文件数(≥2runs) | 均值 |
|---|---:|---:|
| deepseek-v4-pro-0813 | 1 | 0.6667（n=1，仅参考） |
| deepseek-v4.1-flash | 6 | 0.5625 |
| kimi-k3 | 23 | 0.7347 |
| qwen3.7-flash | 24 | 0.6035 |
| qwen3.8-27b | 16 | 0.5534 |
| qwen3.8-max | 15 | 0.6079 |
| qwen3.8-max-0902 | 14 | 0.6042 |

- 主力区间 0.55–0.73，均值 ~0.6；temp=0 下 run 间分歧 ~40%（1−0.6）。gold v2 §3 佐证：flash zh 0.7173→0.7839（Δ=0.066），flash overall +0.0283、max +0.0112。

### 2.2 inter（引用 §1.2）

- 全局 0.4629；行均值见 §1.2；归因只许「粒度差+厂商偏置混杂」，不许报「方法证伪」或「模型能力排序」。

### 2.3 vs mimo（引用 consensus v2 §3，深度 24 共存）

| 模型 | n | 均值 |
|---|---:|---:|
| deepseek-v4-pro-0813 | 2 | 0.3809（小样本上浮，不可引用） |
| deepseek-v4.1-flash | 10 | 0.2137 |
| kimi-k3 | 24 | 0.2427 |
| qwen3.7-flash | 24 | 0.2583 |
| qwen3.8-27b | 17 | 0.2492 |
| qwen3.8-max | 15 | 0.2295 |
| qwen3.8-max-0902 | 15 | 0.2415 |

- 区间 0.21–0.38 均为「单次快照」，不得证伪 mimo，亦不得确证任一成员；mimo 24/24 维持基线，76 独有只许报「候选删」。

### 2.4 gold bench v2（引用 gold v2 §1–§5，n=92 zh36/de29/en27，temp=0，同 prompt 分拆运行）

| model | zh F1 | de F1 | en F1 | overall | fail_rate |
|---|---|---|---|---|---|
| qwen3.8-flash | 0.7839 | 0.6584 | 0.6713 | 0.7113 | 1.09%（exc0+parse1） |
| qwen3.8-max | 0.8348 | 0.6564 | 0.6777 | 0.7325 | 0.00% |
| qwen3.8-max-0902 | 0.8266 | 0.6708 | 0.6907 | 0.7376 | 0.00% |
| deepseek-v4-pro-0813 | 0.0833 | 0.0345 | 0.0741 | 0.0652 | 93.48%（parse86） |
| kimi-k3 | 0.6016 | 0.5356 | 0.5085 | 0.5535 | 7.61%（parse7） |
| qwen3.8-27b | 0.8008 | 0.6020 | 0.6630 | 0.6977 | 4.35%（exc1+parse3） |
| deepseek-v4.1-flash | 0.5305 | 0.2227 | 0.2889 | 0.3626 | 56.52%（parse52） |
| qwen3.7-flash | 0.8358 | 0.6552 | 0.6060 | 0.7114 | 0.00% |

- 排序：max-0902 0.7376 > max 0.7325 > 3.7-flash 0.7114 ≈ flash 0.7113 > 27b 0.6977 > kimi 0.5535 >> deepseek（无效）。
- ds harness 不兼容：ds-pro/v41 空 content raw_len=0、疑 reasoning_content 未接，按口径记 parse_fail；F1 无效，排序分母只许到 kimi 为止（注 max_tokens 16000 vs 8000、parse 口径差异）。
- 基线对照：已有 qwen3.8-flash 0.6830、max 0.7213；本次 flash Δ=+0.0283、max Δ=+0.0112，在波动带内，排序稳定。
- 8 并行初跑 ~12 条/模型 Connection error（DE 段集中，本地并发拥塞），已顺序重试，上表为终值。补跑铁律：只许顺序低并发。

### 2.5 LDS-C / wiki / 理化外线（引用 verdict C6–C7，只引用数字）

- LDS-C：双复现 p=0.0 为待入库方向（A）；kimi extraction 102 data 有返回为 V（存在性），LDS-C 待算；ds-pro/v41 LDS-C 输入残缺（done 3/中文缺席）差值禁归因；temp 拒收系冻结管线参数问题维持 A。
- wiki：qwen flash vs max 交叉一致 28/30=93.3%（分歧 G012 房产 property vs real estate、G017 negative Freiheit liberty vs freedom）；flash 对源 27/30、max 对源 26/30；kimi 30/30 有返回；三方严格 21/30=70%；人工 accept/notes 全空，维持 needs_review。金标重叠对照句 13 条。
- 理化：物理 middle 0.0208、化学 high 0.0298，量级 ~0.02（比数学最烂 khan3-4 0.044 还低一半）；physchem 仅 24 文件（各 3 章×2 模型×2 run），depth24/breadth41 均不含理化；verification 子集 0.09–0.24 为真信号方向（A）。
- 配额 403 未完成；pytest 84（任务给定引用，本三输入外）。

## ③ 裁决摘要（引用 verdict v2 ① C1–C7）

- C1 intra：红对。temp=0 确定性主张死刑；单次值均为快照，必须带波动带（flash 级 Δ~0.03–0.06，max 级 Δ~0.01）；排序可报，绝对值精确引用禁报。【V】
- C2 inter 0.4629：红错、蓝对。0.46≠证伪，归因=粒度差+厂商偏置；27b 行均值最高（0.51）系中庸粒度最易相交；T1 去污 artefact 下 ensemble 投票是放大器，去污重算前只许「污染快照」。【V】
- C3 vs mimo 0.21–0.38：单次快照成立；mimo 维持基线，76 独有只许候选删；491/145/506/1554 只许配额截断快照。【V】
- C4 ds harness：红全对。ds-pro 0.065 / v41 0.36 禁作能力值、禁进排序；聚合二选一：(a)剔除 ds 系重算，或 (b)整列标 harness 不兼容快照。【V】
- C5 配额 403：红 A2+判例成立。记天花板不记失败；缺席禁计 0 分；聚合必须并列 done/missing/failed/quota 四列；canonical 只许快照待补跑。【V】
- C6 LDS-C p=0.0+kimi incomplete：方向成立、verified 禁报。【V（extraction 存在）+A（复现）】产物+perm 表+temp 拒收 log 入库前三句禁报。
- C7 wiki+理化：wiki 宽松可用（须带 needs_review）、严格 21/30 未过盲审门（0.85/0.8）禁作内容证据，「wiki 验证数学」禁报；理化 0.02 只许初探待解释、禁进 headline、禁与数学 556 节点并列（219 vs 556 不可混算），verification 0.09–0.24 为真信号方向。【V 数字+A 解释】

## ④ 可登记口径（引用 verdict v2 ②允许清单，原样转录）

1. gold 头部：「temp=0、n=92（zh36/de29/en27）同 prompt 分拆运行：max-0902 0.7376、max 0.7325、3.7-flash 0.7114，三模型 fail 0.00%；flash 0.7113（fail 1.09%）、27b 0.6977（fail 4.35%）；复跑 Δ（flash +0.0283、max +0.0112）在波动带内；排序 max-0902>max≈flash>27b/3.7-flash>kimi 0.5535>>deepseek（通道不兼容快照，不作能力解读）。temp=0 仍有 run 间波动（flash zh Δ~0.06），单次值为快照。」
2. 共识快照：「深度 24，intra 0.55–0.73（kimi 0.73 最高）、inter 均值 0.4629、vs mimo 0.21–0.38；表决收录 491 / Solid 145 / Weak 506 / Hypo 1554 / mimo 独有候选删 76；覆盖 kimi 24、3.7flash 24、27b 17、max 15、max-0902 15、v41 10、ds-pro 2。以上为配额截断快照（去污重算前为污染快照），非完成品。」
3. 缺席口径：「七 manifest done/missing/failed/quota 四数并报；FREE_QUOTA_EXHAUSTED_403（direct probe 2026-09-15）记基础设施天花板；kimi genuine 3 条除外；缺席不计分、禁计 0 分。」
4. ds 口径：「ds-pro 0.065（parse 86/92）、v41flash 0.36（parse 52/92）为 harness 不兼容快照（空 content / reasoning_content 未接），F1 无效；聚合须剔除 ds 系或整列标 harness 失败。」
5. wiki 口径：「qwen 交叉一致 28/30（G012/G017 分歧）、flash 对源 27/30、max 对源 26/30，accept 未闭环维持 needs_review；kimi 30/30 有返回，打分待 accept 规则入库重算。」
6. LDS-C/理化口径：「LDS-C p=0.0 为待入库方向（产物+perm 表到位前禁报 verified）；理化 J~0.02 初探待解释，verification 子集 0.09–0.24 为真信号方向；跨模型 LDS-C 差值待参数兼容矩阵。」

## ⑤ 补跑优先级 P1–P4（引用 verdict v2 ③-C，按解冻价值排序）

1. **P1 ds-pro depth**：done 3→depth24 补齐（配额杀伤最大，inter/vs mimo 表 ds-pro 行 n=1–2 全不可用；补齐后 C2/C3 小样本上浮消除）。
2. **P2 kimi tail**：选修 2-2 ch1.5 起 8 连 quota + genuine 3（en_ap r2/r3、en_probability）→ kimi 唯一 depth24 全勤（24/24），尾部补齐即全矩阵唯一完整列。
3. **P3 v41 中文**：中文概率论/线代/微分方程/选修整块 missing 66（最大非随机缺席；补齐后中文子集 inter 可算，否则中德分层结论永久冻结）。
4. **P4 breadth**：3.7flash breadth 9/9 探针 403 + max/max-0902 cap100 截断部分（广度只在 P1–P3 闭环后开工；开工前 breadth41 禁报覆盖率分母）。
- 铁律：补跑只许顺序低并发（gold v2 §2 并发拥塞教训），每模型附 direct probe 行；新增证据只追记 A→V，不改 verdict 行号。
- 修数 vs Future（引用 verdict ③-A/B，不新增实验）：R1 ds 系处理重算、R2 T1 去污重算、R3 wiki accept 闭环、R4 表述修数；F1 deepseek 换通道、F2 LDS-C 入库、F3 理化口径冻结、F4 参数兼容矩阵。

## ⑥ 禁语清单（引用 verdict v2 ②禁止清单，出现即违规）

1. 报 ds-pro 0.065 / v41 0.36 为能力值或进能力排序。
2. 报「qwen 系全员零失败」「temperature=0 确定可复现」「单次 F1 精确值」（不带波动带者）。
3. 报任何 ensemble 聚合数不附七模型缺席四列；用 gold「无 403」掩盖大矩阵 403。
4. 报跨模型 LDS-C 差值不附参数兼容矩阵；报「LDS-C 已双复现 verified」「temp 拒收已定管线问题」。
5. 报 403 缺席为模型失败；缺席计 0 分拉均值。
6. 报理化规模（367/220）不并列 0.0208/0.0298；数学↔理化混算外推；理化 0.02 进 headline。
7. 报 wiki 只报 28/30=93.3% 不并列三方严格 21/30=70% + needs_review；报「wiki 验证数学」。
8. 报 canonical65/共识集为完成品；报「异构矩阵验证鲁棒性」「全教材已覆盖」。
9. v1 禁报延续：precision 下限 0.78（实测 0.70）、recall 下限 0.27（实测 0.22）、「5 review/1 fail」（实为 10/2）、「flash-vs-max J 0.54」（无出处）。
10. 补充：精确「头部三模型 0.71–0.74 零失败」之外一律禁报「qwen 系 0.70–0.74 零失败」；mimo 独有 76 禁报「已删/已确证」；表决四数禁报「共识真相」（去污前）。

---
*来源行号可查：consensus v2 覆盖表/intra/inter/vs mimo/表决；gold v2 §1–§5；verdict v2 ①–③。*
