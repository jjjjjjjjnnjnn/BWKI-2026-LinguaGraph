# mimo 基线可用性·蓝队防守书（2026-09-14）

- 立场：蓝队（防守方）。任务是为 mimo 基线**可用性辩护＝界定可用边界**，不是洗白。凡红队已锤实的错误，本文件全部认领为债务；防守只针对"全盘不可用／系统性捏造"这类扩大化指控。
- 输入（已全读）：
  - `research/mimo_spark_audit/*.audit.json` 12 个（下表 §附）。
  - `research/mimo_spark_audit_20260914.md`（6 文件子集汇总，§0–④）。
  - `research/bailian_audit/*.bailian.json` 11 个（第三方抽取通道 qwen3.8-flash/max，9 个已解析概念 22–40 / 关系 23–30，2 个 parsed=NULL 仅 raw：de_abitur_lk、de_wahrscheinlichkeit_ch1-8）。
- 方法口径（与汇总审计一致）：归一化＝小写＋去空格/连字符/下划线（＋ß→ss，个别 χ²→chi-quadrat）＋同义映射；recall＝|mimo∩spark|/|spark|，precision＝|mimo∩spark|/|mimo|；rel_agree＝有序端点对一致数（不计 type 差异，差异另见 flags）；dangling＝端点不在**同文件** mimo 概念表内（即使源文有据，也与 hallucination 分开计数）；hallucination＝源文无依据的增殖。
- 与旧汇总的关系：`mimo_spark_audit_20260914.md` 只覆盖 6 文件（5 review / 1 fail）；本文件按磁盘现有 **12 文件全集重 tally：10 review / 2 fail（83.3% / 16.7%）**，不改动任何既有 audit.json verdict，旧 §③④ 结论在本文件 §③ 中按 12 文件口径更新引用。

## ① 防守证据（5 条，每条都可被 audit.json 证伪）

**D1. precision 全线 0.70–1.00，无"全幻觉文件"。**
12 文件 precision：de_abitur 0.929、forster 1.0、lambacher 1.0、wahrscheinlichkeit 0.917、ib 0.944、khan_3-4 0.70（全集最低）、khan_6-8 0.784、stewart 1.0（含 leniency；严格精确匹配 0.857）、微分 ch3 1.0、微分 ch4 1.0、选修 1.1 1.0（但 fail 源缺失，见债务）、选修 1.2 1.0（概念 precision；关系另有 3 条幻觉边，见 D2）。最低 0.70 的 khan_3-4 其 TP=7 仍是源文实有（fraction/equivalent fractions/factor/perimeter/angle/parallel/perpendicular），"错"的是漏收而非捏造。指控"mimo 系统性编造"与此分布矛盾：若是系统性捏造，应出现 precision 塌陷文件，实际一个都没有。

**D2. 幻觉是点状、可枚举、可修的，不是弥散噪声。**
12 文件中出现真 hallucination 判定的仅 4 文件，且每条都已点名：
- de_abitur：2 概念＋2 关系（Partielle Integration、Substitutionsregel 超源增殖＋配公式；→Produktregel、→Kettenregel 悬空＋幻觉）。
- khan_6-8：2 概念＋2 关系（compound/simple interest 源文无依据）。
- wahrscheinlichkeit：2 概念（Fehler 1./2. Art；Kap.8 仅列 H0/H1/Teststatistik/α 及 Z-/t-/χ²-/F-Test，从未出现该字样）。
- 选修 1.2：3 条关系幻觉（微分方程的阶→微分方程、微分的几何意义→微分、无穷级数→收敛，端点均不在源文）。
其余：forster / lambacher / stewart / 微分 ch3 / 微分 ch4 hallucination_count=0；ib 的 inverse function、khan_3-4 的 numerator/denominator/multiple、khan_6-8 的 integer/y-intercept/line of best fit/MAD/IQR 均判为 implicit（文本可辩，不计 TP 亦非幻觉）。即可修复量上限 ≈ 6 概念＋7 关系边，删/改即消项，不影响基线整体成立。

**D3. 244 悬空中有 79% 是"跨文件可解"，修法是补概念不是删关系。**
全局扫描口径（68 文件 / 741 概念 / 665 关系）：文件内悬空 244/665（36.7%）→ 全局未解 51/665（7.7%）；244−51=193（79.1%）在跨文件并集内可解。典型：forster 的 Ableitung/Grenzwert/Zusammensetzung（8 条关系端点源文有据，补 3 概念可解）、stewart 的 Derivative（6 关系中 5 条目标源文实有 L5 起贯穿）、abitur 的 bedingte Wahrscheinlichkeit（源文有 Bedingte Wahrscheinlichkeit 一节，仅 mimo 概念表漏收）、ib 的 quadratic function/derivative/function/probability（语义正确，仅未在同文件立目）。朴素归一重算（无同义表）得文件内悬空 244 一致、全局未解 50、自环 1，与正式口径 51 差 1 来自 ß→ss/同义映射（Bayes-Formel≈Satz von Bayes 等），属口径差非实质分歧。结论：悬空的主形态是"关系引用了未在同文件立目的概念"，债务在概念表完备性，不在关系捏造。

**D4. 低 recall 全是"小文件漏收"，形态＝omission/missing，非错收。**
recall<0.5 的 6 文件恰为 mimo_c≤18 的小提取：khan_3-4 0.226（mimo_c 10）、微分 ch3 0.273（6）、微分 ch4 0.292（7）、stewart 0.318（7）、选修 1.2 0.409（9）、ib 0.447（18）；而大文件 abitur（28）0.765、khan_6-8（37）0.744、forster（11）0.733、wahrscheinlichkeit（24）0.611。低 recall 文件的 precision 反而全线 ≥0.94（除 khan_3-4 0.70 外均为 1.0/0.944），stewart audit 明记"低 recall=不完备非捏造"。bailian 第三方通道佐证同一方向：bailian ch3 29 概念 / ch4 28 概念恰好补回 mimo 漏收的通解/特解/线性无关/受迫振动/LR-RC-LRC/放射性衰变/马尔萨斯等，说明缺口是"没收到"，不是"收错了"。补漏即可提升 recall，不需推翻基线。

**D5. 宏观置换检验 p<0.004 不受上述微观噪声颠覆（分层辩护）。**
宏观层（语言可分性 LDS-C）：`docs/evidence_register.md:C19` 登记 ZH-DE 59/59 formal at p<0.004（500 perm 分辨率极限），`docs/SSOT-web.md:66` 同记"Alle 59 ZH-DE p<0.004，Marge 0.033–0.424"；微观层（本文件 D1–D4）是概念/关系抽取噪声（direction/type/overbroad/dangling）。二者不在同一检验对象上：宏观零模型是 label permutation 下的 margin 分布，微观的边方向倒置（如 Permutationen→Kombinationen、Brüche→Grundrechenarten、FTC→Derivative）与 target 泛化（如特征方程→高阶线性微分方程裸上位）不改变"跨语言距离显著大于零模型"的结论量级（margin 下限 0.033 仍为正，且 59/59 全过）。因此允许的表述是"宏观信号在现有微观噪声下依然成立"，不许反向表述为"宏观显著证明微观无错"。

## ② 承认的债务清单（红队已锤实，蓝队照单全收）

1. **去重缺失（pipeline 缺 dedup）**：lambacher 16 条中 6 组端点对完全重复（[0]=[6]、[1]≈[7]、[2]=[8]、[3]=[12]、[4]=[13]、[5]=[15]），去重后独立端点对仅 10 组；khan_3-4 15 rows=12 unique（fraction→division、equivalent fractions→fraction、factor→multiplication 各 ×2）。rel_agree 已按去重后计数（lambacher 7、khan_3-4 6），债务在提取流水线，不在审计口径。
2. **概念表漏收（dangling 主因）**：forster（Ableitung/Grenzwert/Zusammengesetzte Funktion/Differenzierbarkeit）、abitur 8 项（Stetigkeit、LGS、Komplexe Zahlen/Gauss-Ebene、Bedingte W.、Binomial-/Normalverteilung、Erwartungswert、Varianz）、lambacher 约 15 项（Stellenwertsystem、Würfel/Quader、Symmetrie、Größen/Maße、Diagramme、Median/Modalwert、Ganze/Rationale Zahlen、Terme、Funktionenbegriff、Zufallsexperimente）、ib（exponent laws/logarithms、quadratic/vertex、radian/sector、trig identities、limits/continuity、FTC、expected value 等）、khan 几何/抽样链（scale drawings、circle/volume、random sampling/inference）、stewart 8 项（e^x、a^x、velocity/acceleration、second derivative、marginal cost、antidifferentiation/integration、limit definition of e）、微分 ch3（通解/特解/线性无关/特征根三分型）、微分 ch4（受迫振动/LR-RC-LRC/衰变/马尔萨斯/方程组/矩阵指数等）。修法：Future 补漏概念清单，不得就地改 verdict。
3. **51 真悬空（跨文件未解 51/665＝7.7%）**：244−51=193 为同文件补立目即可解（优先级低）；51 为真正的全局未解端点（含 D2 的幻觉边＋选修 1.2 的裸导数/极限泛化边＋个别超源公式边如 Kreisfläche=πr²），需逐条修（补概念 / 纠目标 / 删幻觉边）。51 未消除前不得升级措辞。
4. **方向/类型/泛化错边（逐条认）**：direction（abitur Permutationen→Kombinationen 倒置、khan_6-8 similar figures 应为 similar triangles、stewart R4 rate→Derivative 反向＋R6 FTC→Derivative 误配、khan_3-4 angle→perpendicular 反向＋area→perimeter 误 analogy、lambacher Brüche→Grundrechenarten 倒置＋Wahrscheinlichkeit→Durchschnitt analogy 无效、微分 ch4 方程组 generalization 方向存疑）、type（微分 ch3 非齐次—齐次 inverse_of 应为 derived_from/related）、overbroad（微分 ch3/ch4、选修 1.2 的裸上位 target，应指向常系数齐次/非齐次子类型、物理/生物应用、一阶方程组、基本初等公式/四则运算法则子类型）、unsupported（选修 1.2 商法则 requires 积法则源文未提）、incomplete（forster R5 遗漏 Kettenregel 分支）。均不计入 precision 攻防，计入关系质量债务。
5. **选修源缺失（fail 两项，不进入质量分母）**：选修 1.1 `source_txt_missing`（data/textbook 下无源 txt，spark 清单系课标推定，unverifiable，coverage_low＋函数过泛）判 fail；选修 1.2 虽概念 precision=1.0 但关系含 3 条幻觉边＋6 条裸导数泛化边判 fail。两项只记"源缺失/待补"，源补齐后重审，不得说成"已审"。
6. **bailian 通道 2 个 parsed=NULL**：de_abitur_lk（qwen3.8-max，raw 13434）、de_wahrscheinlichkeit（qwen3.8-flash，raw 11805）尚未解析入库，跨模型交叉结论暂以其余 9 解析文件为准，2 个 raw 不得引用为"交叉通过"。

## ③ 可登记口径（只许这样报）

- **允许报（方法＋通过率）**："12 文件独立复核（Muse Spark 本体＋子智能体，归一化＋同义映射；recall/precision/rel_agree 定义见 §头；dangling 与 hallucination 分开计数；重复条目去重后计 agree），10 review / 2 fail（源缺失/幻觉边，不计入质量否决的分母质量论证，仅记待补）；review precision 0.70–1.00、recall 0.23–0.77；全局扫描 68 文件 741 概念 665 关系，文件内悬空 244/665，全局未解 51/665，自环 1，跨文件重名 38（朴素重算 53，差值来自归一化 vs 原名口径，备查）。"
- **允许报（宏观分层）**："宏观 LDS-C ZH-DE 59/59 在 500-perm 下 p<0.004（分辨率极限），margin 0.033–0.424；微观抽取噪声（D1–D4）不颠覆该宏观结论，但宏观显著不得反证微观无错。"
- **禁语清单（出现即判违规）**："绝对无错""零幻觉""可直接冻结""全库已验证""fail 项已审""51 未解已消除""宏观显著即微观无错""bailian raw 即交叉通过"。其中"零幻觉"特禁：D2 已点名 4 文件幻觉，任何全称否定与 audit.json 矛盾。
- **转 pass 规则**：5→10 个 review 的 omission/missing 列补漏概念清单转 pass 列 Future；51 逐条修；选修两项源补齐后重审。在此之前 verdict 冻结。

## 附·12 文件速查表

| 文件 | mimo_c/mimo_r | spark_c/spark_r | recall | precision | rel_agree | verdict | 一句话 |
|---|---|---|---|---|---|---|---|
| de_abitur_lk | 28/21 | 34/21 | 0.765 | 0.929 | 18 | review | 唯二真幻觉之一（积分方法细分超源）＋8 漏收 |
| de_forster_ch5_sec5.1 | 11/8 | 15/12 | 0.733 | 1.000 | 8 | review | 0 幻觉；8 关系悬空系概念表漏收 3 词 |
| de_lambacher_5-8 | 15/16 | 30/20 | 0.500 | 1.000 | 7 | review | 0 幻觉；去重缺失（16→10）＋15 漏收 |
| de_wahrscheinlichkeit_ch1-8 | 24/15 | 36/24 | 0.611 | 0.917 | 15 | review | 2 幻觉概念（Fehler 1./2. Art）＋14 漏收；关系无悬空 |
| en_ib_math_aa_sl | 18/14 | 38/20 | 0.447 | 0.944 | 13 | review | 0 幻觉；5/14 关系悬空＋大面积 missing |
| en_khan_3-4 | 10/15 | 31/16 | 0.226 | 0.700 | 6 | review | 全集最低 precision 但仍非捏造；3 重复＋9/15 悬空 |
| en_khan_6-8 | 37/22 | 39/18 | 0.744 | 0.784 | 10 | review | 唯二真幻觉之二（interest 漂移）＋几何/抽样漏收 |
| en_stewart_ch3_sec3.1 | 7/6 | 22/16 | 0.318 | 1.000 | 2 | review | 0 幻觉；小文件漏收＋Derivative 悬空＋FTC 误配 |
| zh_微分方程_ch3_sec3.2-3.4 | 6/5 | 22/16 | 0.273 | 1.000 | 3 | review | 0 幻觉；缺通解/特解/三分型＋type/overbroad |
| zh_微分方程_ch4_sec4.1-4.3 | 7/7 | 24/17 | 0.292 | 1.000 | 2 | review | 0 幻觉；缺受迫振动/电路/衰变/方程组链 |
| zh_选修2-2_ch1_sec1.1 | 4/2 | 18/12 | 0.222 | 1.000 | 2 | **fail（源缺失）** | 无源 txt，unverifiable，不入质量分母 |
| zh_选修2-2_ch1_sec1.2 | 9/12 | 22/16 | 0.409 | 1.000 | 1 | **fail** | 3 幻觉关系＋裸导数泛化，待源补齐重审 |
