# 多模型终审裁决书 multi_model_verdict（2026-09-14）

- 裁决员立场：终审。红队 `research/red_attack_20260914.md`、蓝队 `research/blue_defense_20260914.md` 已全读。
- 抽查验证（5 个 audit.json ＋ bailian/model 字段 ＋ DAG）：
  - 12 audit 复算：10 review / 2 fail；precision 最低 0.70（khan3-4，mimo_c=10/spark_c=31/TP=7）；recall 区间 0.222（选修1.1）~0.765（abitur）。与红队 A1/A2 数字一致。
  - 选修1.2 audit：verdict=fail，3 条关系幻觉（微分方程的阶→微分方程 / 微分的几何意义→微分 / 无穷级数→收敛）＋6 条裸导数泛化，属实。
  - lambacher audit：16 条中 6 组端点对重复、去重后 10 组独立端点对，属实；Kreis→Fläche 超源配公式记为 dangling（非 hallucination 标签）。
  - wahrscheinlichkeit audit：Fehler 1./2. Art 判 hallucination×2，源文无字样，属实。
  - stewart audit：mimo_c=7/recall=0.318（严格 0.273）/precision=1.0（含 leniency）、R4 反向＋R6 FTC 误配，属实。
  - bailian：11 文件中 2 个 parsed=None（de_abitur_lk max、de_wahrscheinlichkeit flash）属实；11 个 base 各仅单一模型输出（flash 7＋max 4，无同 base 配对双跑），flash-vs-max J 口径在库内无出处属实。
  - DAG `dag_validation_20260914.md`：11 环、prune 141（1自环＋65 bad_length＋51 dangling＋24 dup_relation=141 ✓）、51 去向 35补＋13纠＋1删＋2归档=51 ✓，数字自洽。

## ① 红队攻击逐条裁决

| 编号 | 攻击点 | 裁决 | 理由 |
|---|---|---|---|
| A1 | 汇总 6 文件口径证伪：真实 10 review/2 fail，precision 下限 0.70，recall 下限 0.22 | **成立** | 磁盘 12 文件复算确认。旧汇总 §①§④ 的"5 review/1 fail、无 precision<0.78、recall 0.27~0.77"一律作废，代之以 12 文件口径 |
| A2 | recall 低至 0.22~0.32，小文件漏成筛子、无覆盖担保 | **成立（限定版）** | 5/12 文件 recall<0.35、遗漏多为考试核心概念（通解/特解/三分型、e^x、反微分）属实。但形态=omission 非捏造（低 recall 文件 precision 除 khan3-4 外全 ≥0.944），故判"小节不可直接用、须补漏"，不判"mimo 全盘造假" |
| A3 | mimo–bailian 概念 J 0.04~0.41、关系 J 0.00~0.11；"单次快照"批评 | **部分成立** | 含义界定：**跨提取器分歧 ≠ mimo 全错**。两提取器目标/粒度/提示不同，低 J 一部分是口径差（bailian 概念数多 2~4 倍：如 ch3 bailian 29 vs mimo 6），不能直接读成"mimo 错光"。但红队"单次快照"批评**成立**：单模型单次运行、无配对双跑、无第二模型全库交叉，在此状态下 mimo 不得称为"基线"，只许称"待清洗原始提取" |
| A3附 | flash-vs-max J 0.54 无盘上出处 | **成立，列禁报** | 每 base 仅单一 bailian 输出＋2 个 parsed=None，不存在配对双跑，0.54 不可复算。只许报红队实测区间（概念 J 0.04~0.41、关系 J 0.00~0.11，9/3 组抽算口径） |
| A4 | 幻觉 5/12 文件＋关系级幻觉 | **部分成立** | audit.json 标签口径下真 hallucination=**4 文件**（abitur、khan6-8、wahrscheinlichkeit、选修1.2），蓝队 D2 点名无误。红队第 5 个（lambacher Kreisfläche=πr² 超源）在 audit 中记为 dangling 而非 hallucination。裁决：登记按"4 确认＋1 疑似超源（lambacher R10）"报；"幻觉点状"旧结论降级为"4/12 确认含关系级幻觉 1 fail，系统性判定需全库第二模型交叉后才可下" |
| A5 | 方向/类型错 9/12 文件，下游中毒 | **成立** | 抽查 audit 全认（abitur 倒置、lambacher 倒置＋无效 analogy、khan3-4 反向＋误 analogy、stewart R4/R6、微分 ch3 type/overbroad、选修1.2 unsupported/overbroad）。**错边先删先纠，不许排 Future**（见④） |
| A6 | 重复关系未去重 | **成立** | lambacher 16→10、khan3-4 15→12、DAG dup_relation 24（含 lambacher 6 对最多）三方互证。665 关系总数含水分，引用须注明"去重前" |
| A7 | bailian 2/11 解析失败＋flash/max 混跑 | **成立** | parsed=None 恰为幻觉重灾区二文件，该二文件不得引用任何"交叉通过"；其余 9 文件结论暂用，须注明模型混杂（flash/max 效应未分离） |
| A8 | 51 vs 50 口径差＋悬空集中于未 audit 文件 | **成立（口径差非实质分歧）** | 50（朴素归一）vs 51（归一化＋同义）差 1 来因明确（ß→ss/同义映射），登记只许报"50~51（口径待定）"且不得隐瞒 244。56 个未 audit 文件质量未知，任何全库质量断言禁报 |

- 红队 §②"判死刑"8 条采纳：①基线降级、②precision/recall 下限更正、③幻觉分母补全、④错边先修、⑤碎图无低优先级、⑥区间更正、⑦CLI 链路主张已死（维持归档）、⑧重名 38 vs 53 口径未冻结（登记须双报备查）。

## ② 维持蓝队哪些防守

- **D1 precision 分布防守维持**：0.70~1.00、无全幻觉文件成立。"错的是漏收而非捏造"成立（khan3-4 TP=7 源文实有）。仅更正：下限引用须为 0.70，recall 下限须为 0.22（蓝队 §③ 写的 0.23 系 0.222 误舍入，不许再用）。
- **D2 点状可枚举防守维持（修正计数）**：幻觉可枚举、可修（≈6 概念＋7 关系边，删/改即消项）成立；文件数按"4 确认＋1 疑似"登记（上表 A4）。
- **D3/D4 宏观微观分层＋omission 定性维持**：244→51（193 跨文件可解 79.1%）、低 recall=omission/missing（precision 反证＋bailian 补回同方向证据）成立。但**修法优先级按④重排**：碎边（单文件碎图）与 51 同等优先，不得写"优先级低"。
- **D5 宏观分层辩护维持**：LDS-C 59/59 p<0.004（margin 0.033~0.424）不受微观边错颠覆，允许报"宏观信号在现有微观噪声下依然成立"；反向表述（宏观证微观无错）禁报。维持。
- **债务清单照单全收**：去重缺失、概念表漏收、51 真悬空、方向/类型/泛化错边、选修源缺失两项、bailian 2 raw，蓝队 §② 全部维持并转④执行。

## ③ 最终可登记口径

### 允许报
- "12 文件独立复核（Muse Spark 本体＋子智能体，归一化＋同义映射；recall/precision/rel_agree 定义与旧汇总同口径；dangling 与 hallucination 分开计数；重复条目去重后计 agree），**10 review / 2 fail**（选修1.1 源缺失、选修1.2 关系幻觉；两项待补，不入质量分母）；review precision **0.70~1.00**、recall **0.22~0.77**；全局扫描 68 文件 741 概念 665 关系（去重前），文件内悬空 244/665，全局未解 **50~51**/665（口径待定），自环 1，跨文件重名 38（正式口径）/53（朴素重算，备查）。"
- "mimo 当前状态为**待清洗原始提取**，非基线。幻觉 4 文件确认＋1 疑似（lambacher R10），可枚举约 6 概念＋7 关系边；9/12 文件有方向/类型/泛化错边；去重缺失（16→10、15→12；全库 dup 24）。"
- "mimo–bailian 第三方抽查（9 解析文件）：概念 J 0.04~0.41、关系 J 0.00~0.11（归一化口径独立抽算）；2 文件 parsed=None 未入比较；flash/max 混跑、效应未分离。"
- "宏观 LDS-C ZH-DE 59/59 在 500-perm 下 p<0.004（分辨率极限），margin 0.033~0.424；微观抽取噪声不颠覆该宏观结论，但宏观显著不得反证微观无错。"
- DAG 数字："有向图 685 节点/665 边；环 11（含自环 1＋9 节点大环 1）；prune 候选 141（删边类 1＋24、其余人工定/补纠）；51 去向 35补/13纠/1删/2归档"。

### 禁止报
1. precision 下限 0.78、recall 下限 0.27/0.23；"5 review/1 fail"；"仅 2 文件幻觉"。
2. "flash-vs-max J 0.54"（无出处）；"全局未解 51"精确值（只许 50~51）；隐瞒 244 只报 51。
3. "mimo 可用作基线/可直接冻结/零幻觉/绝对无错/全库已验证/fail 已审/51 已消除/宏观显著即微观无错/bailian raw 即交叉通过/56 未审文件质量已知"。
4. 把 6 文件区间当全库代表值；把错边/重复边列 Future。

### 旧汇总 `research/mimo_spark_audit_20260914.md` 需修订的 3 处
1. §①表＋§③-1/§④：6 文件→**12 文件全集**（5 review/1 fail→10 review/2 fail；precision 0.78→**0.70**；recall 0.27→**0.22**；khan3-4、选修1.2、lambacher 等 6 个新增行补入）。
2. §②推论1： "6 抽检仅 2 文件幻觉"→"**12 抽检 4 确认＋1 疑似**（abitur、khan6-8、wahrscheinlichkeit、选修1.2＋lambacher R10 疑似），含关系级幻觉 1 fail"。
3. §③-3/§③-4 转 pass 与优先级规则：review omission 补漏可列 Future，但**错边/幻觉边/重复边先删先纠（修数任务），244−51=193 碎边与 51 同等优先**，删除"优先级低于 51"表述。

## ④ 执行令（修数任务 vs Future，明确分类）

- **修数任务（立即执行，不得排 Future；冻结基线的前置条件）**：
  1. 删幻觉边/概念：选修1.2 的 3 条幻觉关系、abitur 超源 2 概念＋2 关系、khan6-8 interest 2 概念＋2 关系、wahrscheinlichkeit 2 概念；DAG 51 去向中**删 1**（Trennung der Variablen 噪声标签）＋自环删边 1（圆自环）。
  2. 纠错边：A5/D②-4 全清单（abitur 倒置、lambacher 倒置＋无效 analogy、khan3-4 反向＋误 analogy、stewart R4/R6、微分 ch3 type/overbroad、微分 ch4 存疑 generalization、选修1.2 unsupported/overbroad、forster R5 补 Kettenregel 分支）；DAG 51 去向中**纠 13**（别名可解异名）。
  3. 去重：全库 dup_relation **24 删边**（lambacher 6 对优先）；khan3-4 3 组重复同步去重。665 总数去重后重报。
- **Future（排期补漏，不阻塞"不冻结"结论，但阻塞"升级措辞"）**：
  1. 补概念：DAG 51 去向中**补 35**（pde/体积/向量空间/面积/周长/fläche 等高频缺目）＋各 audit omission 清单（forster 4、abitur 8、lambacher ~15、ib、khan 几何/抽样链、stewart 8、微分 ch3/ch4 核心链）；244−51=193 同文件补立目（含 forster/stewart 碎图修复，优先级与 51 持平）。
  2. 11 环中除自环外 10 环：方向/类型人工复核后纠边（9 节点大环拆解为逐边核查），列 Future 图治理项。
  3. 51 去向中**归档 2**（Exponentenrechnung、Trigonometrie）：人工判定后分流为补/纠/删，不得直接删。
  4. 选修 1.1/1.2 源补齐后重审；bailian 2 raw 解析入库后重跑交叉；56 未 audit 文件按 12 文件同方法续审（覆盖 recall/precision 全区间后方可谈冻结）。
- **冻结令**：上述修数任务清零＋重算（去重后 665、50~51 口径冻结为一）之前，mimo 不得冻结为基线，不得用于任何单文件下游图任务；verdict 冻结（任何转 pass 不得就地改 audit.json）。
