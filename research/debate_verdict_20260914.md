# W4 红蓝博弈裁决书 — 2026-09-14

> 基地：`C:\Users\rongj\Desktop\学校\BWKI-2026-备战` · 只新增本文件
> 裁判原则：**站不住 → 归档 / Future，不进论文正文 / 平台 headline**；限定版才可写，且必须带约束注。
> 裁决三态：**可写（限定版）/ 暂缓（条件未满足前不写）/ 归档（不进论文+平台，仅附录反例或 Future）**
> 依据冻结：`research/checkpoint_20260914.md` §3/§4 · `research/baseline_board.md` A/B · `research/gold_freeze_2026-09-14.md` · `research/gold_deconfound_2026-09-14.md` · `research/tier2_emb_baseline.md` · `research/rsa_bridge.md` · `docs/fig3_cds_forensic.md` · `docs/fig5_hds_forensic.md` · `docs/BASELINE_LEDGER.md`

---

## 议题1 · 0.519 收敛（ZH-DE LDS math 0.5188）

**红方（质疑站不住）：**
- R1红问：0.5188 能否证明"中文与德文知识组织更接近"？全尺寸 math 0.519 vs wiki 0.819 的差距是否内容证据？
- R2红问：T1 去污 167/219 德标签含 CJK、剔除后 ZH-DE J_node 0.556→0.020（LDS 0.52→0.99），这不是直接证伪吗？
- R3红问：size-match k=15/25/35 gap 全负（−0.023/−0.053/−0.080，wiki>math），全尺寸结论反转，凭什么还留 headline？

**蓝方（辩护限定版）：**
- R1蓝答：不主张语言收敛因果，只主张"对齐标签一致性"的指示性描述，且 final README 已降级 C1 为 indikativ。
- R2蓝答：承认 T1 污染是致命伤，但主张保留为"伪影警示案例"，引用时强制并列证伪句。
- R3蓝答：承认全尺寸不可作内容证据，主张冻结值只用于方法对照（Fig4/Fig8），不作收敛 headline。

**裁决：归档**
- 0.519 不得作为"语言收敛 / 制度趋同"证据进论文正文、结论、平台任何 headline/hero。
- 仅允许在方法附录/P2-Recheck 作**反例警示**（artefact note），引用时必须三件套并列：`0.5188 + T1去污崩塌句（167/219→0.99）+ size-match反转句`。
- Future：对齐标签重洗 + 独立提取后才可重审；此前提暂缓转正申请。

---

## 议题2 · 0.939 headline（社会 F1）

**红方：**
- R1红问：门户 hero 单写 F1=0.939 是否 over-claim？72 项全是 auto_accepted/machine-seeded，无二评。
- R2红问：独立 harness 社会 F1 仅 ~0.65（qwen-plus 0.6497 / qwen-max 0.6483），0.939 与 harness 差 0.29，怎能同名引用？
- R3红问：盲审门（F1≥0.85 ∧ Agr≥0.8 ∧ 每语≥0.7）未过，G2 verdict pending，凭什么称 Mature？

**蓝方：**
- R1蓝答：0.939 是 DB-path + seed 同源特值（paper value），不是 harness 值；主 README/portal 已加 † 与 harness 注。
- R2蓝答：辩护"双数字记账"：headline 用加权 0.881=(72×0.939+20×0.674)/92，社会子集只写 0.939†。
- R3蓝答：承认 gold 仍 PILOT（freeze note），主张社会子集标注 Developing + blind pending 可保留。

**裁决：暂缓（限定可写，G2通过前不升级）**
- 平台/论文 headline 只许写**加权 0.881**；社会 0.939 必须写 `0.939†（社会子集 n=72, Developing, blind pending, DB-path特值）`，且同页/同段并列 harness ~0.65。
- Hero/摘要禁止单写 0.939；G2 三门全过前不得写 Mature、不得作模型选型绝对值证据（只保 qwen-plus>qwen-max 排名）。
- 出处：`gold_freeze_2026-09-14.md` + `gold_deconfound_2026-09-14.md §5` + `baseline_board.md B-Gold`。

---

## 议题3 · HDS≤8（数学 max 8 / 均值 0.40，83% 根概念）

**红方：**
- R1红问：HDS"当前存档不可重算"（pipeline 丢失，六月稠密图冻结），不可复算的值凭什么进 F3 headline？
- R2红问：max=8 是否单点离群？均值才 0.40，用 max 立"普遍上界"是否夸大？
- R3红问：物理 HDS≤6 / 均值 0.85 与数学差异大，universell 上界是否站不住？

**蓝方：**
- R1蓝答：有取证链：aligned 219 / 556-238 快照 / math_full 3833 三源穷举 + portal 三语冻结注，可引用但降级强度。
- R2蓝答：不只报 max，并报均值 0.40 + 83% 根 + 物理对照，主张结论是"浅网、非深树"而非"8 即定律"。
- R3蓝答：承认学科差异，限定措辞为"样本内上界（observed max）"，物理 0.85 反而佐证"浅网方向一致"。

**裁决：可写（限定版，必须带冻结注）**
- 可写 F3 描述性结论，措辞限定为：`观测上界 max 8（数学）/ 6（物理），均值 0.40/0.85，83% 根概念——浅网结构`。
- 强制脚注：`冻结自 2026-06 稠密图，当前存档不可重算，见 fig5 forensic；重算链重建前不得升级为普遍认知定律`。
- 禁止写法：universal law / 认知约束定论；因果外推归 F10 假设。

---

## 议题4 · 学段切分（CDS 中段峰值 0.271→高段 0.073，3.7× 稀释）

**红方：**
- R1红问：F1–F3 全是描述性、无 CI，是否样本巧合？阈值 0.90/0.50 也是描述性。
- R2红问：化学中段峰值差绝对值仅 0.012，小到可忽略，还称"三科一致"吗？
- R3红问：CDS 同样冻结自六月稠密图、不可重算，学段故事是否只是 frozen 快照讲故事？

**蓝方：**
- R1蓝答：中段峰值在 ZH/EN/DE 三语独立复现（0.271→0.073），跨语言同峰比单点 CI 更有说服力。
- R2蓝答：化学已诚实降级为 "consistent with, not confirming"，不隐瞒小效应。
- R3蓝答：fig3 forensic 有 CDS middle 46/280→0.271、high 175/1113→0.073 分子分母，可审计方向；主张描述性成立、因果禁止。

**裁决：可写（描述性限定版）**
- 可写：`CDS 中段峰值 0.271（小学 0.216 → 中段 0.271 → 高段 0.073 → 大学 0.042），三语独立同峰；数学/物理方向一致`。
- 强制约束：① 标注描述性、无 CI；② 化学写 "consistent with, not confirming（Δ=0.012）"；③ 因果/治理外推禁止，归 F10 假设；④ 带 frozen 注（见 fig3 forensic）。
- 出处：`docs/cognitive_metrics_framework.md §CDS` + `docs/fig3_cds_forensic.md` + `docs/evidence_register.md C1/C20`。

---

## 议题5 · PEP 镜像（CN 物理化学 PEP 2019，11 册）

**红方：**
- R1红问：第三方镜像（TapXWorld/ChinaTextbook）provenance unverified，版权教材扫描件能否进仓/引用？
- R2红问：CS 12.7%–95.4%（CN 87 vs US 2124 vs NRW 299 课程概念粒度混杂）能否归因"集权 vs 联邦"治理？
- R3红问：物理"1 pending sensor node"、11 册中 4 stubs 是否瞒报缺口？

**蓝方：**
- R1蓝答：仓内无扫描件原文，仅映射 JSON + gitignored OCR 事实级 txt；`DATA_MANIFEST.md` 明示"本地研究专用·永不进仓·以 smartedu 官方本为准"。
- R2蓝答：F9 测量强、F10 治理归因仅假设，不作结论；论文已注粒度混杂 + 课堂实施链未测。
- R3蓝答：缺口已公开：portal scope-note + cn_mapping 注记 + physics_sourcing P0-3（7 mapped + 4 stubs），非瞒报。

**裁决：归档（镜像）+ 暂缓（官方本重采列 Future）**
- 第三方 PEP 镜像**归档**：永不进仓、不引用、不进平台填报出处栏；评审索要原文一律指向 smartedu 官方渠道。
- CS 治理归因（集权 vs 联邦）**归档为假设**：F10措辞，不得写进结论/平台因果栏；平台填报 Q2 必须写假设句 + 粒度混杂注。
- Q1/Q3 缺口注**可写**：允许写数据来源注（7 mapped + 4 stubs / sensor 缺口），不得隐瞒。
- Future：以官方本重采/补齐后才可重审转正。

---

## 议题6 · Tier2 否决权（LLM-Within / RSA 关环守卫）

**红方：**
- R1红问：Tier2（LLM-as-Subject Within，典型 floor 0.70–0.87，command-a ~0.49）提取密度差异大，跨模型 marge 绝对值比较是否伪影？
- R2红问：小模型链断在提取（qwen2.5-0.5b zh 36 概念 → floor NaN；hy-mt2 空集；gemma 不遵 schema），Tier2 凭什么否决/放行 Tier1 结论？
- R3红问：perm=500 不足辨 Bonferroni（0.05/177≈0.0003），§2.3/§3 blocked（perm/floor≥1000 未跑），RSA 关环是否 premature？

**蓝方：**
- R1蓝答：否决权正是为此存在：跨提取器只报方向不报绝对差（Ledger §8.8 尺度漂移），marge 与 ratio（LDS-C/floor）并报。
- R2蓝答：密度守卫 `<50 概念/语言 → unresolved，不进 RSA`（phi-4-mini ~140 通过线），NaN 不插值，直接触发否决。
- R3蓝答：RSA 协议只定义、不跑数；关环判据 `CLOSED ≡ (ρCI>0) ∧ (vote超额) ∧ (M2一致)`，任一不满足即 `offen`；blocked 未解前一律 offen。

**裁决：可写（守卫规则本身可写；被否决的结论归档）**
- Tier2 否决权/RSA 守卫**可写进方法**（§8.10–8.16 + `rsa_bridge.md`）：密度守卫 50、perm≥1000 + bootstrap CI、size-k 反转否决、CLOSED 三合一。
- 触发否决时对应实质结论**归档**：`offen`，不进正文结论/平台；Tier1 数学 cell（J_node 0.556 含对齐/尺寸伪影）不得单独关环。
- Tier2 基线（nomic-embed 768 + top-5 + phi-4-mini/muse-spark 判官，407 results/hits 165，物理 62.1%/化学 53.2%）只作**复用基线可写**，`--full` 未跑前不得升级为主证据。
- 出处：`research/rsa_bridge.md §3–§6` + `research/tier2_emb_baseline.md` + `baseline_board.md B（§2.3/§3 blocked）`。

---

## 6 裁决一览

| # | 议题 | 裁决 | 一句话 |
|---|---|---|---|
| 1 | 0.519 收敛 | **归档** | T1去污崩塌 + size反转，禁作收敛证据，仅附录伪影警示 |
| 2 | 0.939 headline | **暂缓** | 只许 0.881 + 0.939† + 0.65 并列，G2过门前禁 Mature/hero单写 |
| 3 | HDS≤8 | **可写（限定）** | 观测上界 + 浅网描述，必须带六月冻结注，禁升级定律 |
| 4 | 学段切分 | **可写（描述性限定）** | 三语同峰可写，化学降级，禁因果/治理外推 |
| 5 | PEP 镜像 | **归档 + 暂缓** | 第三方镜像归档永不引用；治理归因归档为假设；官方本重采列 Future |
| 6 | Tier2 否决权 | **可写（守卫）** | 守卫规则本身可写；被否决结论一律 offen 归档 |

*裁判签名：W4 Roberto · 2026-09-14 · 下一步：按本裁决修论文措辞 + 平台填报口径，blocked/pending 项列 Future，不提前转正。*
