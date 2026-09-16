# MIMO–Spark 独立复核汇总审计（2026-09-14）

- 基地：`C:\Users\rongj\Desktop\学校\BWKI-2026-备战`
- 输入：`research/mimo_spark_audit/*.audit.json`（12 个）＋全局结构扫描（68 文件 / 741 概念 / 665 关系，去重前）
- 复核执行：Muse Spark 本体＋子智能体（CLI 链路见 §0）
- 本文件为唯一新产出，不改动既有 audit.json。

## §0 CLI 链路结论（归档口径）

- `opencode run agentic`：空回退，已归档（不作为复核通道）。
- 直连 zen / go：401（未授权），已归档。
- 本轮 6 文件复核由 Muse Spark 本体＋子智能体独立执行，`model` 字段记为 `muse-spark-1.3-contributor (independent re-audit)` / `opencode-go/muse-spark-1.3-contributor`。
- 后续任何"无错"主张不得引用 CLI 自动链路，只能引用本文件 §④ 的抽检口径。

## ① 每文件表

recall=|mimo∩spark|/|spark|（归一化＋同义映射后），precision=|mimo∩spark|/|mimo|，rel_agree=有序端点对一致数（不计 type 差异，差异另见 flags）。

| 文件 | mimo_c/mimo_r | spark_c/spark_r | recall | precision | rel_agree | flags 摘要 | verdict |
|---|---|---|---|---|---|---|---|
| de_abitur_lk | 28/21 | 34/21 | 0.765 | 0.929 | 18 | hallucination×2（Partielle Integration、Substitutionsregel 超源增殖＋配公式）；dangling×3（→Produktregel、→Kettenregel 为悬空＋幻觉，→bedingte Wahrscheinlichkeit 为概念表漏收）；direction_error×1（Permutationen→Kombinationen generalization 倒置）；omission 8 项（Stetigkeit、LGS、Komplexe Zahlen/Gauss-Ebene、 Bedingte W.、Binomial-/Normalverteilung、Erwartungswert、Varianz） | review |
| de_forster_ch5_sec5.1 | 11/8 | 15/12 | 0.733 | 1.000 | 8 | dangling：8 条关系端点 Ableitung/Grenzwert/Zusammensetzung 源文有据但 mimo 概念表未收（补 3 概念可解）；omission 4（Ableitung/Differentiation、Grenzwert/-satz、Zusammengesetzte Funktion、Differenzierbarkeit）；incomplete×1（R5 Quotientenregel→Produktregel 遗漏 Kettenregel 分支）；hallucination 0 | review |
| en_khan_6-8 | 37/22 | 39/18 | 0.744 | 0.784 | 10 | hallucination：compound/simple interest 2 概念＋2 关系源文无依据；dangling 5 目标（factor、multiple、fraction、multiplication、right triangle）；direction×1（similar figures 应为 similar triangles，L84 斜率论证）；implicit（mimo-only 但文本可辩：integer、y-intercept、line of best fit、MAD、IQR，不计 TP 亦非幻觉）；missing（equivalent ratios、absolute value、cube root、equivalent expressions、scale drawings/circle/volume 链、random sampling/inference） | review |
| en_stewart_ch3_sec3.1 | 7/6 | 22/16 | 0.318 | 1.000 | 2 | dangling：6 关系中 5 条目标 Derivative 不在 mimo 概念表；direction×2（R4 rate of change→Derivative 反向；R6 FTC→Derivative inverse_of 误配，正确边为 Differentiation inverse_of Antidifferentiation/Integration）；missing 8（e^x、a^x、velocity、acceleration、second derivative、marginal cost、antidifferentiation/integration、limit definition of e）。注：严格精确匹配 TP=6 时 recall 0.273/precision 0.857；lenient 计 Sum and Difference Rules 覆盖 sum+difference 得上表值。无幻觉概念，低 recall=不完备非捏造 | review |
| zh_微分方程_ch3_sec3.2-3.4 | 6/5 | 22/16 | 0.273 | 1.000 | 3 | coverage_low（缺通解/特解/线性无关/特征根三分型等）；dangling（常微分方程：源文、概念表双缺）；type_error（非齐次—齐次 inverse_of 应为 derived_from/related）；overbroad（特征方程/待定系数法/参数变易法 target 泛化为高阶线性微分方程，应指向常系数齐次/非齐次子类型） | review |
| zh_选修2-2_ch1_sec1.1 | 4/2 | 18/12 | 0.222 | 1.000 | 2 | source_txt_missing（data/textbook 下无对应源 txt，无法逐行核验）；unverifiable_audit（spark 清单基于课标 1.1 常规推定，非源文独立提取）；coverage_low（缺平均/瞬时/变化率、割线、导函数、几何意义等）；concept_generic（函数过泛） | **fail（源缺失）** |
| de_lambacher_5-8 | 15/16 | 30/20 | 0.500 | 1.000 | 7 | duplication×6组（16 条→去重后 10 组独立端点对）；dangling×1（R10 Kreis→Fläche：目标 Fläche 不在概念表＋公式 Kreisfläche=πr²源文未出现，记 dangling，疑似超源）；direction_error×2（Brüche→Grundrechenarten generalization 倒置；Wahrscheinlichkeit→Durchschnitt analogy 无效）；omission ~15（Stellenwert、Würfel/Quader、Symmetrie、Diagramme、Median/Modalwert、Terme/Funktionenbegriff、Zufallsexperimente 等） | review |
| de_wahrscheinlichkeit_ch1-8 | 24/15 | 36/24 | 0.611 | 0.917 | 15 | hallucination×2（Fehler 1. Art、Fehler 2. Art 源文无字样，超源增殖）；omission 14（Ereignisraum/Axiome/klassisches Modell、Unabhängigkeit、Bernoulli/Uniform/Exponential、Dichte/Verteilungsfunktion、Korrelation、H0/H1/Z-/χ²-Test 等）；关系端点均落概念表内，无悬空 | review |
| en_ib_math_aa_sl | 18/14 | 38/20 | 0.447 | 0.944 | 13 | dangling 5/14（quadratic function、derivative、function、probability 未立目但语义正确）；implicit×1（inverse function 源文无字面依据，不计 TP 非幻觉）；missing（指数/对数、弧度/三角恒等式、极限/微分法则、积分/FTC、条件概率/Bayes/期望、无穷几何级数、3D 直线平面等） | review |
| en_khan_academy_3-4 | 10/15 | 31/16 | 0.226 | 0.700 | 6 | duplicate 3 组（15 行→12 独立：fraction→division、equivalent fractions→fraction、factor→multiplication 各×2）；dangling 9/15（division/multiplication/addition/length/area）；direction×2（angle→perpendicular 反向；area→perimeter 误 analogy）；implicit 3（numerator/denominator/multiple 文本可辩，不计 TP 非幻觉）；missing（四则/位值/数轴/时间/体积质量/缩放图/等积划分/多步应用题/同分母加法/面积/小数等） | review |
| zh_微分方程_ch4_sec4.1-4.3 | 7/7 | 24/17 | 0.292 | 1.000 | 2 | coverage_low（缺受迫振动/LR-RC-LRC 电路方程/衰变/Malthus/一阶方程组/矩阵指数/特征值动力学等，recall 仅 0.29）；dangling 3（二阶线性/常/微分方程 target 未立目）；overbroad 3（弹簧振动/逻辑斯蒂/SIR target 泛化为二阶线性/微分方程/方程组）；direction 存疑 1（方程组 generalization 常微分方程） | review |
| zh_选修2-2_ch1_sec1.2 | 9/12 | 22/16 | 0.409 | 1.000 | 1 | hallucinated×3（微分方程的阶→微分方程 / 微分的几何意义→微分 / 无穷级数→收敛，源文无据）；dangling 6＋1（target=导数×6、极限×1 未立目）；unsupported×1（商法则 requires 积法则源文未提）；overbroad×6（specialization 泛化到裸导数，应指向初等函数公式/四则运算法则子类型） | **fail（关系幻觉）** |

通过率（按 verdict 计）：10/12 review，2/12 fail（选修1.1 源缺失、选修1.2 关系幻觉；两项待补，不入质量分母）；review precision **0.70~1.00**、recall **0.22~0.77**（下限 khan3-4 precision 0.70 / 选修1.1 recall 0.222）。
旧口径"5/6 review（83.3%）、1/6 fail、无 precision<0.78、recall 0.27~0.77"一律**作废**，代之以本表 12 文件全集口径（终审 `research/multi_model_verdict_20260914.md` A1）。

## ② 全局错误界

扫描基数：68 文件，741 概念，665 关系。

- 悬空（文件内）：244/665（36.7%）——端点不在**同文件** mimo 概念表内。
- 全局未解：51/665（7.7%）——端点不在**全库概念并集**内（归一化＋同义口径）。
- 自环：1（个案修，不影响界）。
- 跨文件重名：38（候选同义/切分差异，非直接错误）。
- 推论 1（幻觉可枚举、非零星两文件）：12 抽检中 **4 文件确认含真 hallucination＋1 文件疑似超源**：de_abitur_lk（2 概念＋2 关系超源增殖）、en_khan_6-8（interest 2 概念＋2 关系主题漂移）、de_wahrscheinlichkeit（Fehler 1./2. Art 源文无字样×2）、zh_选修2-2_ch1_sec1.2（3 条关系幻觉＋6 条裸导数泛化，判 fail）；lambacher R10 Kreis→Fläche（Kreisfläche=πr²源文未出现）在 audit 中记 dangling，列**疑似超源**。旧结论"6 抽检仅 2 文件幻觉""幻觉点状"降级为"4/12 确认含关系级幻觉 1 fail"，系统性判定需全库第二模型交叉后才可下（终审 A4）。
- 推论 2（悬空多为跨文件设计）：文件内 244 → 全局 51，约 79% 在跨文件并集内可解。典型如 Ableitung/Grenzwert、Derivative、bedingte Wahrscheinlichkeit：源文有据，仅是"关系引用了未在同文件立目的概念"。修法是**补概念条目**而非删关系。
- 推论 3（覆盖缺口在小文件）：recall < 0.35 的五项（选修1.1 0.222、khan3-4 0.226、微分方程ch3 0.273、微分方程ch4 0.292、stewart 0.318）恰为 mimo_c ≤ 10 的小提取；大文件（abitur 28、khan6-8 37）recall ≥ 0.74。缺口形态=漏收（omission/missing），非错收（低 recall 文件 precision 除 khan3-4 0.70 外全 ≥0.944；小节不可直接用、须补漏，见终审 A2）。
- 复计数注：以朴素归一（小写＋去空白/连字符/下划线、无同义表）独立重算得文件内悬空 244（一致）、全局未解 50、跨文件重名 53、自环 1。与 официально 采用的 51/38 差 1～15，差值来自 ß→ss、同义映射（Bayes-Formel≈Satz von Bayes 等）与重名计数口径（归一化后 vs 原名）。本文件 §③④ 采用扫描口径 **51/38** 为准，此注仅备查。

## ③ 裁决

1. **mimo 当前为待清洗原始提取，非基线**：review precision 高（0.70～1.00）、recall 0.22～0.77；幻觉 4 确认＋1 疑似可枚举，主要债务是 omission（小文件漏收）＋ dangling（同文件未立目）＋方向/类型/泛化错边＋重复未去重。任何"零错/可直接冻结/可用作基线"结论均不成立（终审 A1—A3）。旧"precision 0.78～1.0、hallucination 点状、可作基线"表述作废。
2. **fail 项归档**：zh_选修2-2_ch1_sec1.1 因源 txt 缺失判 fail（unverifiable），zh_选修2-2_ch1_sec1.2 因 3 条关系幻觉＋6 条裸导数泛化判 fail；两项待补，不进入通过率分母的质量论证，仅记源缺失/幻觉待修。源补齐＋删/纠边后重审，verdict 冻结（不得就地改 audit.json）。
3. **review omission 补漏列 Future，错边/幻觉边/重复边先删先纠（修数任务）**：10 个 review 的 omission/missing（abitur 8 项、forster 4 项、khan 几何/抽样链、stewart 8 项、微分方程ch3 通解/特解/三分型、微分方程ch4 受迫振动/电路方程/矩阵方法链、lambacher ~15 项、ib 指数/三角/微积分链、khan3-4 四则/位值/面积小数链、wahrscheinlichkeit 14 项）列为补漏概念清单，转入 pass 列 Future 任务，不得就地改 verdict；但方向/类型/泛化错边、幻觉边、重复边不得排 Future，须按终审④修数任务先删先纠（删：选修1.2 3 条幻觉关系、abitur 超源 2 概念＋2 关系、khan6-8 interest 2 概念＋2 关系、wahrscheinlichkeit 2 概念；纠：A5 全清单倒置/误配/overbroad；去重：全库 dup_relation 24 删边＋khan3-4 3 组＋lambacher 6 对优先）。
4. **51 全局悬空＋193 碎边同等优先列修复候选**：51/665 为真正的跨文件未解端点，按 `research/dag_validation_20260914.md` §3 去向执行——补 35 / 纠 13 / 删 1（Trennung der Variablen 噪声标签）/ 归档 2（Exponentenrechnung、Trigonometrie）；prune 141＝1 自环删边＋65 bad_length 人工定＋51 dangling 见去向＋24 dup_relation 删边。244−51=193 为文件内悬空但全局可解（含 forster/stewart 碎图修复），修法是同文件补立概念条目，**与 51 同等优先**。旧"优先级低于 51"表述删除作废。

## ④ 平台／论文可登记口径（只许这样报）

- 允许报："12 文件独立复核（Muse Spark 本体＋子智能体，归一化＋同义映射；recall/precision/rel_agree 定义与旧口径同口径；dangling 与 hallucination 分开计数；重复条目去重后计 agree），10 review / 2 fail（选修1.1 源缺失、选修1.2 关系幻觉；两项待补，不入质量分母）；review precision 0.70～1.00、recall 0.22～0.77；全局扫描 68 文件 741 概念 665 关系（去重前），文件内悬空 244/665，全局未解 50~51/665（口径待定），自环 1，跨文件重名 38（正式口径）/53（朴素重算，备查）。"
- 允许报："mimo 当前为待清洗原始提取，非基线。幻觉 4 文件确认＋1 疑似（abitur、khan6-8、wahrscheinlichkeit、选修1.2＋lambacher R10 疑似），可枚举约 6 概念＋7 关系边；9/12 文件有方向/类型/泛化错边；去重缺失（lambacher 16→10、khan3-4 15→12；全库 dup_relation 24）。"
- 允许报 DAG："有向图 685 节点/665 边；环 11（含自环 1＋9 节点大环 1）；prune 候选 141（删边类 1＋24、其余人工定/补纠）；51 去向 35补/13纠/1删/2归档"（出处 `research/dag_validation_20260914.md`）。
- 允许报方法：recall/precision/rel_agree 定义、同义表、dangling 与 hallucination 分开计数、小文件覆盖缺口结论（小节不可直接用、须补漏）。
- **不许报**："绝对无错""零幻觉""可用作基线/可直接冻结""全库已验证"。fail 项不得说成"已审"。51 未解消除前不得升级措辞。旧数字"5 review/1 fail、precision 下限 0.78、recall 下限 0.27/0.23、仅 2 文件幻觉、全局未解 51 精确值、flash-vs-max J 0.54"一律禁报；只许报 50~51 且不得隐瞒 244；不得把 6 文件区间当全库代表值；错边/重复边不得列 Future。
