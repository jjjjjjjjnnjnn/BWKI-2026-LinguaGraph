# Weight-vs-Human 逻辑脊收口：P1–P5 五环 + 证据编号 + 降级规则（Lane-4，2026-09-16）

> Lane-4 目标：P1–P5 逻辑脊收口，不新增数据/语料/指标/功能（`RESEARCH_RULES.md` 禁令）。
> 口径冻结：F1 social 0.939 仍为 Developing/PILOT（C9b）；N=8 不报显著；已撤回 Sim p=0.05 与 §8.17 N=1 **不引用、不入证据链**。
> 上游输入：`RESEARCH_RULES.md`（三问+禁令）、`docs/paper/00_three_conclusions.md`、
> `research/human_vs_machine_20260914.md`（话术卡）、`research/limitations_20260914.md`（L1–L5）。

---

## 0. 证据编号总表（Lane-1 / Lane-2 / Lane-3 / 冻结值）

| 编号 | 内容 | 归属 | 链接 |
|---|---|---|---|
| L1-1 | Ausubel（1963）知识整合先于分化；Novak & Cañas（2008）概念图命题网络；语言相对论 [49][50] 仅作 ΔLDS 动机，不作证实源 | Lane-1 文献/理论 | `docs/paper/00_three_conclusions.md §理论→证据链` |
| L1-2 | Boroditsky（2000）时间隐喻仅作 LPA 探索动机（C12–C15 Exploratory，不进入主脊） | Lane-1 文献 | `docs/evidence_register.md C12–C15` |
| L2-1 | SSOT：manifest.json 556 Konzepte / 525 Relationen / 219 Gruppen；68 抽取文件；30 shared IDs frozen | Lane-2 provenance | `RESEARCH_RULES.md v0.13.2`；`LINGUAGRAPH_DATA_LINEAGE.md §5/§8`；`manifest.json` |
| L2-2 | LDS-K 冻结值：ZH-EN 0.934 / DE-EN 0.938 / ZH-DE 0.519（精确 0.9336/0.9382/0.5188） | Lane-2 冻结值 | `scripts/analyze_human_lds.py:23-28 LDS_K`；`scripts/figures_i18n_wave2.py:269`；`outputs/figures/reproduce_lds_binary.log` |
| L2-3 | Gold 92 条：Batch A 数学 n=20 手标干净（C9a Mature）；Batch B 社会 n=72 机器预提+人工接受（C9b Developing，盲审待补）；目标 100→实得 92（8 empty dropped） | Lane-2 provenance | `data/gold/gold_dataset.json`；`docs/evidence_register.md C9a/C9b` |
| L2-4 | 人类 pilot N=8 社会话题 LDS-C 占位：zh-en 0.704 / de-en 0.727 / zh-de 0.751（demo implant，仅形态登记） | Lane-2 provenance | `scripts/analyze_human_lds.py:258-268 demo()`；`research/human_vs_machine_20260914.md §1` |
| L2-5 | 向量实测：nomic-embed-text-v1.5 dim=768，934 词条；主对 434（zh-de 65 / zh-en 184 / de-en 185）；均值 zh-de 0.4804 / zh-en 0.5249 / de-en 0.4888 | Lane-2 provenance | `research/two_tier_benchmark_20260914.md §1–§2`；`scripts/tools/openweight_embed_audit.py` |
| L2-6 | 人类 N=15 Between 主值：LDS-C ≈ 0.93–0.96 ≈ split-half 底 0.92–0.96；permutation p=0.08/1.0/1.0（fragile）；LLM Within：LDS-C 0.93–0.96 ≫ 底 0.85–0.87，p<0.01；LMM same_lang +0.038 p<0.001 | Lane-2 provenance | `docs/paper/00_three_conclusions.md C3`；`docs/evidence_register.md C17/C18` |
| L3-1 | T1 去污染：167/219 de-label 含 CJK；J_node 0.556→0.020；ZH-DE LDS 0.52→0.990（Fig.8）；C16 SUPERSEDES C3 趋同读法 | Lane-3 audit | `docs/evidence_register.md C16`；`docs/p2_methodology_rechecks.md` |
| L3-2 | Null-suite：Full < Structure Null（ZH-EN 0.934<0.957；DE-EN 0.938<0.957；ZH-DE 0.519<0.717）；Complete Random 1.000 | Lane-3 audit | `docs/paper/00_three_conclusions.md C3 证据表` |
| L3-3 | G3 去亲缘双值：DB 路径社会 0.939 vs 独立 harness 社会 ~0.65（qwen-plus 0.6497 / qwen-max 0.6483；干净数学 0.7244/0.7068，gap +0.0176 同号）；0.939 为 DB+seed 同源特值，不可作 harness F1 引用 | Lane-3 audit | `research/gold_deconfound_2026-09-14.md §1–§5`；`research/gold_deconfound_2026-09-14.json` |
| L3-4 | 蓝队防守：12 文件 10 review / 2 fail；precision 0.70–1.00；文件内悬空 244/665→全局未解 51/665；幻觉点状 6 概念+7 边；宏观 59/59 p<0.004（500-perm 分辨率极限）与微观噪声分层，不互证 | Lane-3 audit | `research/blue_defense_20260914.md D1–D5`；`docs/evidence_register.md C19` |
| L3-5 | 共识快照不稳定性：intra 0.59–0.73；inter v2 0.4629→v3 0.5401 系 qwen 补满分母 artefact，不可比、趋势禁报；v41/ds-pro 冻结，三锁 L1/L2/L3 | Lane-3 audit | `research/consensus_v3_20260915.md`；`research/limitations_20260914.md L5` |
| L3-6 | 口径债务：chunk 节级保守偏（L1）、硬匹配惩罚（L2，zh-de 有效对仅 65，std 0.1274 最宽）、N=8+覆盖率 37.9%（L3）、temperature=0 非确定 intra 0.59–0.73（L4） | Lane-3 audit | `research/limitations_20260914.md L1–L4`；`research/two_tier_benchmark_20260914.md §1` |
| F-1 | 冻结引用：LDS-K 0.934/0.938/0.519；CDS 峰值数学 0.271/物理 0.222；HDS ≤8（数学 max 8/物理 max 6）；within-split-half 底教材线 ~0.97 / 人类 0.92–0.96 / LLM 0.85–0.87 | 冻结值 | `docs/paper/00_three_conclusions.md C1–C3`；`docs/evidence_register.md C1/C2/C4/C20` |

不引用清单（硬禁）：Sim p=0.05（已撤回，Skalendrift，`RESEARCH_RULES.md` ❌）；
§8.17 N=1（已移除 → `_archive/20260908_qitian_removal/`，❌）。本文件零引用；若他页引用即判该页违规。

---

## 1. P1 定义环（Definition）

**形式化表述：**
`LDS-K = 1 − mean(GED_sim, J_node, J_edge)`（教材图谱，课程结构）；
`LDS-C = 1 − Jaccard(人类/LLM 作答概念集)`（行为层，问卷 implant 口径按 `analyze_human_between.py` / `analyze_sim_baseline.py` 分话题切片）；
`ΔLDS = LDS-C − LDS-K`（概念层；关系层不可比）；
`drift_vec = 1 − cos_sim(开权重嵌入同义对)`（分布邻近度，`two_tier` 口径）。

**前提：** 四量各测各的；LDS-K 以 L2-2 冻结值为唯一输入；LDS-C 正式值以 N≥30 管线为准，当前人类列仅 L2-4 占位。

**证据：** L1-1（动机）+ L2-1 + L2-2 + F-1 + L3-2（LDS-K 非语言发散的定义域限定）。

**断环即降级：** 若混用任一定义（如用 drift_vec 代 LDS-K、用关系层 ΔLDS）→ C3/C5/C6 由 Mature 降为 Developing；若用错冻结值 → 相关 claim 降为 Hypothesis，Fig.8/Fig.3 重审。

**三问检查：** (1)增证据？是——锁定四量口径，防事后调参（L3-6 软匹配阈值须预注册）。(2)验假设？是——ΔLDS 可证伪性依赖定义分离（C6/C17/C18）。(3)助提交？是——方法章/图注可直接引用本节，答辩防“哪个对”诘问（话术卡 Q2）。

---

## 2. P2 污染环（Contamination）

**形式化表述：**
`∀e ∈ ZH-DE: CJK(de_label(e)) → exclude(e)` 后 `LDS-K(ZH-DE): 0.519 → 0.990`（T1）；
`seed(qwen-plus, temp 0.3) ∩ eval(qwen-plus) → F1_social = 0.939† 为同源特值`（G3）；
`labels.zh == labels.de（表面全同，32/219 组）→ 从向量主对剔除`（L2-5）。

**前提：** 污染主张只认审计数（167/219；J 0.556→0.020；harness ~0.65 vs DB 0.939），不认叙事；`research/gold_review/` 缺席为已登记 gap，不得默许通过。

**证据：** L3-1 + L3-3 + L2-3 + L2-5 + L3-6（L2 硬匹配对 zh-de 降权）。

**断环即降级：** 若引用 ZH-DE 0.519 作“趋同”证据而不并列 0.990 → C3 趋同读法复活，整脊降为 Hypothesis，打回重写；若引用 0.939 作通用 F1（不标 †/Developing/DB-path）→ C9b 由 Developing 降为 Hypothesis，portal/hero 图注冻结解禁前禁进 headline；若向量 zh-de 0.4804 不标 n=65/std 0.1274 → Tier-2 结论降为 Hypothesis。

**三问检查：** (1)增证据？是——T1/G3 均为反向证据（证伪 skolemnictwo 趋同、证伪通用 0.939）。(2)验假设？是——C16 替代 C3（SUPERSEDED 登记）。(3)助提交？是——Limitations 定稿口径与禁语清单的执行点（`limitations_20260914.md §配套禁语`）。

---

## 3. P3 方法环（Method）

**形式化表述：**
Two-Tier 判定：`range(LDS-K)=0.419 ≫ range(drift_vec)=0.0445（≈9.4×）∧ 序结构不一致 → 两层互补且不可互换`；
口径三锁：chunk=节（对称施加，偏差同向）；归一=小写+去空格/连字符/下划线+ß→ss+同义映射（硬匹配）；判官 temperature=0/max_tokens=5（嵌入无采样随机，但 run 间非确定 L3-5/L4 快照论）。
显著性三锁：N=8 禁报显著；500-perm p<0.004 为分辨率极限（1/500），59/59 全过+margin 下限 0.033 为正方可报“宏观成立”；C17 permutation p（200 iter）为 fragile，报 null 时须标 needs_review。

**前提：** 方法变更（chunk 改章级、软匹配阈值、模型版本更换）须重跑+重登记版本号与日期（`limitations_20260914.md §可复现性`）；缓存只写 `%TEMP%/opencode/`，Repo 零写入。

**证据：** L2-5 + L3-4（D1–D5 分层辩护）+ L3-5 + L3-6（L1/L2/L4）+ `research/human_vs_machine_20260914.md §2–§3`。

**断环即降级：** 若改任一锁无重跑（如换模沿用旧数）→ 相关 Tier/Macro claim 由 Mature 降为 Developing；若 N=8 报 p/显著/探针通过 → 当页判违规，C7/C8 由 Developing 降为 Hypothesis；若反向表述“宏观显著证明微观无错”→ 蓝队禁语触发，整脊降级。

**三问检查：** (1)增证据？是——向量窄带 vs 图谱结构化为已验对照（预期成立，`two_tier §0/§5`）。(2)验假设？是——Tier-2 作证伪探针（效应课程特异 vs 通用语义的分离器）。(3)助提交？是——可复现命令与版本号登记即答辩 Q5/Q6 标准答。

---

## 4. P4 分叉环（Fork：Between vs Within）

**形式化表述：**
`Human Between (N=15): LDS-C ≈ floor ∧ ΔLDS ≈ 0 (−0.05..+0.05) → C17（Developing）：Between 条件下无可分语言信号（falsifiziert, Between-Subject）`；
`LLM Within (same-model deepseek-v4-flash; 59-model replication ZH-DE 59/59 p<0.004): LDS-C ≫ floor (+0.08–0.09) → C18/C19（Mature）：Within 条件下语言码信号清晰，code 主导（+0.038, p<0.001），frame 次要（+0.001, p=0.90）`；
`Fork 解释：Human-Negative 与 Design-Artefakt-Hypothese 相容（Exklusion + Konsistenz, q=0.30；机制一致 q 不完全坍缩 marge——无定量因果归属），非“无语言认知效应”之证`。

**前提：** 两分支检验对象不同（Between-human vs Within-LLM），任何“一方证伪另一方”属违规外推；人文子集探针为单向不对称证伪（通过→课程特异；报警→降级为跨域共有并追查通用因子；永不单独证实数学结论）；N=8 pilot 符号翻转（Δ +0.232/−0.230/−0.211）仅为 pilot 级观察，正式检验待 N=30（bootstrap CI+Cohen's d+Bonferroni）。

**证据：** L2-6 + L2-4 + `docs/paper/00_three_conclusions.md C3 + §Humanvalidierung/LLM-as-Subject` + `docs/evidence_register.md C7/C8/C17/C18/C19` + `research/human_vs_machine_20260914.md §3–§4`。

**断环即降级：** 若用 N=8 报 C7/C8 而不并列 C17 → C7/C8 由 Developing 降为 Hypothesis；若报“人类证实/证伪 LLM”（跨分支证伪）→ 相关 ΔLDS claim 降为 Hypothesis；若人文探针报警仍坚持“课程特异”无降级 → C-链降为 Hypothesis 并触发蓝队 D5 分层复审。

**三问检查：** (1)增证据？是——N=15 null + Within 正信号共同精确化“何种条件下可检出”（N≥30 Within 设计）。(2)验假设？是——Between falsifiziert + Within nachgewiesen 的分叉即 ΔLDS 假设的边界条件。(3)助提交？是——30 秒 pitch / 学术版双口径的合法措辞来源（`00_three_conclusions.md §统一叙事/学术版`）。

---

## 5. P5 诚实环（Honesty：封顶与禁比）

**形式化表述：**
升级禁令：`F1_social 0.939 ≡ Developing/PILOT（C9b）∧ harness ~0.65 并列；任何单值引用 0.939 即违规`；
样本禁令：`N=8 → 仅形态登记（均匀带 0.70–0.75 vs 向量 0.48–0.52 vs 图谱结构化），禁显著、禁探针通过/报警、禁互证`；
引用禁令：`Sim p=0.05 = ∅；§8.17 N=1 = ∅`；
EN 上限规则（见 §6）与跨量纲禁比（见 §7）为本环子句，违反即触发 P5 断环。

**前提：** `research/gold_review/` 缺席、v41/ds-pro 冻结、三锁 L1/L2/L3 未解前，headline 禁用 0.5401/540/194 及任何“趋势”表述；宏观 LDS-C 引用须带 margin 下限与 perm 分辨率声明。

**证据：** L3-3 + L2-4 + L3-4 禁语清单 + L3-5 + L3-6 + `research/human_vs_machine_20260914.md §5 禁语` + `research/limitations_20260914.md §配套禁语/§500-perm 话术`。

**断环即降级：** 任一禁语出现（“证实/互证/探针通过(N=8)/全库已验证/零幻觉/宏观即微观无错”等）→ 当页 Mature→Developing→Hypothesis 连降两级，打回重写；F1 升级引用 → C9b 降为 Hypothesis 且 portal hero 标注 † 义务触发。

**三问检查：** (1)增证据？否（诚实环不增新数）——但保住既有证据的可信度，等价于增“负证据保险”。(2)验假设？是——防假阳性即假设检验的一部分。(3)助提交？是——评审信任的唯一来源；三问任一“是”即保留本环（`RESEARCH_RULES.md` 停止规则的逆否：助提交=“是”→继续执行）。

---

## 6. EN 上限与 ZH-DE 采信规则

**EN 上限规则（cap rule）：**
涉英两对 LDS-K（0.934/0.938）贴语内噪声底（教材线 ~0.97；人类底 0.92–0.96）——只许报“近底/不可分”，不许报“英语发散最大/英语特异”，不许做 0.934 vs 0.938 的序差断言（差 0.004 在 chunk/归一口径差量级内，L3-6）。
LLM Within 9 EN n.s.（C19）并列登记：ZH-DE 可分 ≠ EN 可分。

**ZH-DE 采信规则（adoption rule）：**
原始 0.519 **禁作趋同证据**；唯一合法引用形为二值并列：`raw 0.519（污染态）→ decontaminated 0.990（T1）` + 定性句“T1-falsifiziert als Label-Artefakt”（C16）。
向量 zh-de 0.4804 与 LDS-K 0.519 的数值接近（Δ −0.0386）**禁作互证**（话术卡 Q3 照读）；人文/向量任一“均匀带”只许报形态相似，不许报数值验证。
ΔLDS zh-de pilot +0.232（L2-4 − L2-2）为 pilot 级符号观察，正式采用待 N=30；当前 ΔLDS 正式口径以 N=15（≈0）+ LLM Within（+0.08–0.09，floor 分离）为准。

---

## 7. 跨量纲禁比声明（Binding）

`drift_vec（余弦距离）≁ LDS-K（1 − mean(GED_sim, J_node, J_edge)）≁ LDS-C（1 − Jaccard 作答集）`：
数值直比、差值排序（§3 表“差 −0.0386/−0.4091/−0.4492”仅作量纲差异展示，不作效应量）、
“两源数值接近即互证/一方证伪另一方”均属违规外推（`human_vs_machine §2.3`）。
唯一合法比较：**序结构比较**（向量窄带 0.0445 vs 图谱极差 0.419；LDS-K 序 zh-en≈de-en≫zh-de 在向量层未复现）与**测量本质陈述**（课程结构 vs 分布邻近度 vs 问卷行为）。
本声明覆盖既往所有三源表（含 `human_vs_machine §1` 与 `two_tier §3` 对照表）的解读层；数字层维持，解读层以本声明为准。

---

## 8. 闭环判定 + 降级触发点清单

### 闭环判定

| 环 | 是否闭环 | 依据 |
|---|---|---|
| P1 定义 | ✅ 闭环 | 四量定义+冻结值+关系层不可比已锁定；L3-2 限定定义域 |
| P2 污染 | ✅ 闭环 | T1（0.519→0.990）+ G3（0.939† vs ~0.65）+ 表面全同剔除三污染子句齐备；C16 SUPERSEDES 登记 |
| P3 方法 | ✅ 闭环 | Two-Tier 预期已验（0.0445 vs 0.419）+ 三锁口径 + 三锁显著性；重跑/版本号规则齐备 |
| P4 分叉 | ✅ 闭环 | Between-null（C17 Developing）+ Within-正（C18/C19 Mature）+ 设计伪影相容解释 + 单向探针逻辑；N=30 待办已注册为 PENDING 而非缺环 |
| P5 诚实 | ✅ 闭环 | 三禁令+EN/ZH-DE 子句+禁比声明+禁语清单齐备；Sim p=0.05 / §8.17 N=1 零引用已执行 |
| **全脊** | **✅ P1–P5 闭环（Developing 封顶 humaine 侧；Mature 仅限已登记项 C16/C18/C19）** | 无新升级；N=30/盲审/三锁解冻为已注册 PENDING，不破环 |

### 降级触发点清单（断环即降级：Mature→Developing→Hypothesis）

| # | 触发点 | 跌落 |
|---|---|---|
| T-P1-1 | 混用定义（drift/LDS 互代；关系层 ΔLDS）或错引冻结值 | 相关 claim →Developing；错冻结值 →Hypothesis |
| T-P2-1 | 引 0.519 作趋同不并列 0.990 | 整脊 →Hypothesis |
| T-P2-2 | 引 0.939 不标 †/Developing/DB-path 或作 harness F1 | C9b →Hypothesis |
| T-P2-3 | 向量 zh-de 不标 n=65/std 0.1274 或做单对断言 | Tier-2 →Hypothesis |
| T-P3-1 | 换模/改口径无重跑重登记 | 相关 claim →Developing |
| T-P3-2 | N=8 报显著/探针通过/报警 | 当页违规；C7/C8 →Hypothesis |
| T-P3-3 | “宏观显著证明微观无错”反向表述 | 整脊降级 |
| T-P4-1 | N=8 报 C7/C8 不并列 C17 | C7/C8 →Hypothesis |
| T-P4-2 | 跨分支证伪（人类⇄LLM 互否） | ΔLDS claim →Hypothesis |
| T-P4-3 | 探针报警仍坚持课程特异无降级 | C-链 →Hypothesis + D5 复审 |
| T-P5-1 | 任一禁语（证实/互证/全库已验证/零幻觉等） | 当页连降两级 |
| T-P5-2 | 引用 Sim p=0.05 或 §8.17 N=1 | 当页判违规 →Hypothesis |
| T-P5-3 | EN 序差断言（0.934 vs 0.938）或数值互证（0.48≈0.52） | 相关结论 →Hypothesis |
| T-P5-4 | headline 用 0.5401/540/194 或报趋势（三锁未解前） | headline 下架，相关 claim →Developing |

---

## 9. 三问总检（Lane-4 本文件）

1. 是否增加科学证据？**是**——新增为“逻辑证据”（五环形式化+证据编号+降级规则），零新数但增可证伪性（T-清单 14 项可执行）。
2. 是否帮助验证研究假设？**是**——ΔLDS 边界条件（Between-null / Within-正）与 T1/G3 双证伪的可引用收口。
3. 是否帮助完成 BWKI 提交？**是**——方法章措辞、Limitations 定稿、话术卡 Q1–Q6 照读句、headline 封顶规则均可直接粘贴。
三问 ≥1 是 → 依 `RESEARCH_RULES.md` 执行成立；且未触四禁（无新语料/概念/功能/指标）。

*严谨尾记：本文件未升级任何结论；C9b 维持 Developing；C7/C8 维持 Developing 且注明被 C17 superseded，引用时须并列 C17；C17 本身 fragile（200 iter）标 needs_review；C19 headline 用 59/54/177 公开口径，文件真值 62/57/186 并列。*
