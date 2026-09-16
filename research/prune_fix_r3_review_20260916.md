# 修数③对照表：13 条 dangling 纠目标（2026-09-16，执行结论更新）

> ## ⚠️ 2026-09-16 验证结论（覆盖下文初版建议）
>
> 逐文件实测：13 条的 `suggest` 值**无一是所在文件的既有概念**（`similar figures` 除外，系自查 fuzzy 命中）。
> 把端点改成 suggest = 制造新的悬空边，违反"不新增悬空"底线。执行器守卫已拒收全部 8 条初版 ✅。
> 因此：初版 8 条 ✅ 全部作废；唯一可执行的是 #6→`similar figures`（已执行，备份 `prune_backup_20260916_endpoint/`）。
> 其余 12 条 HOLD，转全局别名/规范化政策（=⑤补充概念域，需新增概念或对齐表映射，超出边修复 scope）。
>
> 原对照表保留如下供审计：

> 来源：`research/prune_candidates_20260914.json`（复扫后 115 项中的 13 纠；`reason=别名/模糊可解`）。
> 规则：逐条勾选 ✅执行 / ⏸hold 后，方可按 `file+edge_index` 改 `source/target` 为 `suggest`（不新增概念）。
> 全 13 条 `freq_global=1`（单次出现，改动无连带）。

| # | 文件 | 端 | 原端点 | → 建议标准名 | 关系 | edge | 风险评级 | 建议 |
|---|---|---|---|---|---|---|---|---|
| 1 | de_forster_analysis1_ch5_sec5.1.json | target | Zusammensetzung | 复合函数 | applies_to | 6 | 🟢 trivial（德→中标准译名） | ✅ |
| 2 | de_lambacher_5-8_erweitert.json | target | Volumen | volume | representation | 6 | 🟢 trivial（德→英同义词） | ✅ |
| 3 | en_ib_math_aa_sl.json | target | quadratic function | 二次函数 | requires | 5 | 🟢 trivial（英→中标准译名） | ✅ |
| 4 | en_igcse_math_0580.json | target | triangle | dreieck | applies_to | 2 | 🟡 方向争议（EN 文件内端点改德名；全库以何语为准未冻结） | ⏸ |
| 5 | en_khan_academy_6-8.json | target | right triangle | 直角三角形 | applies_to | 15 | 🟢 trivial（英→中标准译名） | ✅ |
| 6 | en_khan_academy_6-8.json | target | similar triangles | ähnliche dreiecke | representation | 18 | 🟡 方向争议（EN 文件改德名；与 #4 同类，须统一规范） | ⏸ |
| 7 | en_ode_pde_ch8-10.json | target | ODE | 常微分方程 | representation | 11 | 🟢 trivial（缩写展开） | ✅ |
| 8 | en_probability_ch1-8.json | target | likelihood function | 似然函数 | requires | 13 | 🟢 trivial（英→中标准译名） | ✅ |
| 9 | zh_初中数学_七年级.json | source | 百分数 | prozentrechnung | analogy | 17 | 🟡 方向争议（中→德；analogy 跨语言例，改后该边成德内边，语义是否保留待定） | ⏸ |
| 10 | zh_初中数学_八年级.json | source | 比例 | proportion | requires | 13 | 🟢 trivial（中→英同义词） | ✅ |
| 11 | zh_初中数学_八年级.json | target | 相似 | similarity | requires | 13 | 🟢 trivial（中→英同义词） | ✅ |
| 12 | zh_微分方程_ch4_sec4.1-4.3.json | target | 二阶线性微分方程 | lineare dgl 2. ordnung | representation | 0 | 🟡 方向争议（中→德混合名；且为 edge 0 首边，改动显眼） | ⏸ |
| 13 | zh_选修2-2_ch9_sec9.1-9.2.json | source | 矩阵指数 | matrixexponential | requires | 10 | 🟢 trivial（中→英/德同义词，无空格德式拼写与库内 `matrixexponential` 是否存在须复核） | ✅（复核拼写后） |

## 待你决策

- ✅ 建议执行 8 条（1,2,3,5,7,8,10,11；13 待拼写复核）：trivial 跨语言同义/译名/缩写展开，零规范争议。
- ⏸ 建议 hold 5 条（4,6,9,12 + 13拼写）：涉及**全库规范名以何语为准**（#4/#6 英文件德名化、#12 中文件德名化、#9 analogy 跨语言例改德内边）。
- 核心问题：跨语言 requires/representation 边的规范端点语言政策未冻结——定一条（例："端点语言跟随所在文件语言，跨语言对齐只走对齐表"），则 #4/#6/#9/#12 全改写为文件语言名；维持 suggest 原案则接受混合语言图谱。定政策后 13 条可一次执行。
- ④破 10 环与 65+2 人工定不在本表，须上游③政策定后再逐环定案。
