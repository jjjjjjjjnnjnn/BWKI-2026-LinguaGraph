# ④破环定案表（2026-09-16，只定案不执行）

> 溯源：每环成员/文件/边/证据见 subagent 溯源（行号 L11–L303 各文件）。原则：只断证据最弱的一条；
> 悬空端点边优先删；跨文件互定义保留定义方向。执行前须另行备份＋复扫＋pytest。

| 环 | 断边提案 | 理由 | 风险 |
|---|---|---|---|
| #2 counting\|place value（k-2同文件） | 断 `counting -> place value` requires（L156） | 位值制建立在数数上，反向无证据（"Place value builds on counting"） | 低 |
| #3 Varianz\|Erwartungswert（跨文件） | 断 `Erwartungswert -> Varianz` requires（westermann L51） | 方差经期望定义（wahrsch L41 ✓）；期望不需方差，"berechnet"系计算提及非前置 | 低中 |
| #4+#10 expression/variable/equation（5-6同文件） | 断 `variable -> equation` requires（L216） | "often contain"弱证据；保留 equation->expression->variable 链为 DAG | 中（#4/#10 同断一条，共用边 L160/L209 保留） |
| #5 克\|千克 | 删二年级上 L143 `克 -> 千克`（悬空端点边，该文件无此二概念） | 悬空边；保留 `千克 -> 克`（1kg=1000g 定义方向） | 低 |
| #6 全等\|相似 | 断 `相似三角形 -> 全等三角形` generalization（九年级 L215） | 全等是相似比1特例，方向只能是全等→相似 | 低中 |
| #7 方向导数\|梯度（ch9_sec9.1同文件） | 断 `方向导数 -> 梯度` representation（L98） | 同一公式倒写；保留 `梯度 -> 方向导数`（点积定义方向） | 低 |
| #8 正方形\|长方形 | 删二年级上 L150 `长方形 -> 正方形`（悬空端点边） | 悬空边；保留 `正方形 -> 长方形` specialization（正方形是特殊的长方形） | 低 |
| #9 area\|length\|perimeter | 断 `area -> perimeter` analogy（3-4 L166） | "Both measure properties"类比非前置，三条中唯一非 requires | 低 |
| #11 九节点大环 | 改 `偏微分方程 -> 常微分方程` generalization（ch9_sec9.5 L49）为反向 `常微分方程 -> 偏微分方程` | "PDE 是 ODE 的推广"被建成 PDE generalizes ODE，方向反了；ODE→PDE 才符合"推广"语义，断环 | 中（改向非删边，需复扫确认环消失且无新环） |

- 待执行：10 次断/改边（#4 与 #10 共用一断，实 9 个动作），前置③政策A Phase 2（#5/#8 的悬空边删除与⑤悬空治理相关，但环断边独立可先行）。
- #11 改向后若产生新环，回滚并升级为人工逐边会审。
