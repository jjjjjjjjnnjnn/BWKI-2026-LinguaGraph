# LinguaGraph 全项目严谨性审查（2026-08-08）

> **审查范围**: 论文 7 章 + 7 个核心脚本 + 数据血缘 + 治理口径
> **审查方式**: 主代理逐行核验统计核心 + 2 个子代理并行审查（论文逻辑 / 代码库）
> **状态**: 审查报告（未修改文件）。发现按严重度排序，附修复建议与深入方向。

---

## CRITICAL（必须修复）

### C1. 论文方法论章 §2.7 的 LDS 公式仍是 v1（概念集 Jaccard），与全文使用的冻结 v3 冲突
- **位置**: `docs/paper/02_methodology.md` §2.7
- **问题**: 方法章公式 `LDS(A,B) = 1 − |∩|/|∪|`（纯概念集）。但结果章 §4.5/§5.9.4 用 v3 `1 − mean(J_node, J_edge)`。方法章**完全没有**定义 LDS-K / LDS-C / ΔLDS 三变体、节点/边双分量、以及空模型套件。评审人逐章核对公式时第一处撞墙。
- **修复**: §2.7 替换为 v3 冻结公式 + 三变体定义 + 空模型方法（引用 `docs/lds_formal_definition.md`）。

### C2. 核心度量 `jaccard` 对空集约定错误：J(∅,∅)=0 → LDS=1.0（静默最大分歧）
- **位置**: `scripts/lds_c_compute.py:171-194`、`scripts/lds_k_deepen.py:61-75`
- **问题**: 两个空集 union=0 → 返回 0.0 → LDS=1.0。语义上应 J=1（恒等）。更危险：空 vs 非空也 LDS=1.0，与"完全无重叠"无法区分。任何 gloss 缺失/阈值过滤/子样本为空的分支都会静默报最大分歧——**与项目已知的 Wikipedia LDS=1.0 伪影同类**。当前人类/LLM 集非空故潜伏，但这是计时炸弹。
- **修复**: `if not a and not b: return 1.0`；空 vs 非空返回 NaN 并在聚合层显式报错。

### C3. ΔLDS 口径全篇混乱：概念级 vs v3 关系级两套数字并存
- **位置**: `03_results.md` §4.2（概念级）vs §4.5（v3 级）vs §5.9.4
- **问题**: 概念级 ΔLDS 约 −0.02~+0.05；v3 级 ΔLDS 约 +0.03~+0.45（ZH-DE）。论文主要用概念级，把 +0.445 标为伪影，但 +0.03/+0.04 也被吞进"ΔLDS≈0"叙述。标题区间"−0.02 bis +0.05"（00/01/04/05 四处）与 §4.2 表内 DE-EN=−0.044 矛盾（−0.044 在声称区间外）。
- **修复**: 统一 ΔLDS 计算基准（只用规范 v3 LDS-K），文中明确两口径差异。

### C4. Coverage Score 数字方法章与讨论章不一致
- **位置**: `02_methodology.md` §2.10（NRW 34.1%、UK 85.5%、US 55.6%）vs `04_discussion.md` §4.5（CN 95.4%、UK 37.3%、US 17.2%、NRW 12.7%）
- **问题**: 两套数字互相矛盾，方法章无 China 值。评审无法确定哪组是当前真相。
- **修复**: 以一条数据为准贯穿全文。

---

## HIGH（应修复）

### H1. LMM 推断依据不稳健：dyad 非独立 + 自由度偏宽 + Hessian 无正定性检查
- **位置**: `scripts/lds_c_llm_lmm.py:78-100,104-181,184-195`
- **问题**: (a) 5 cell × C(5,2)=10 dyad/topic，同一 cell 出现在 4 条 dyad 中共享聚合集 → 非独立，模型只有 (1|topic) 未刻画 → SE 系统性偏小、same_lang p=9e-5 可能夸大；(b) t 检验用 n−3=47 df，有效自由度远小于此；(c) `approx_hess` 无正定性检查，负方差会静默 clip 成 ~1e-6 SE 与天文 t。
- **修复**: cell 级随机效应（5 cell×5 topic）或 cluster-robust SE；Hessian 正定检查；df 用 Kenward-Roger 近似并明示小样本局限。**论文 §5.6/§4.14 引用 same_lang p<0.001 时需注明此推断局限**。

### H2. 硬编码日期文件路径：跨脚本可复现性断裂 + gloss 缺失时静默退化
- **位置**: `scripts/lds_k_deepen.py:358,361,324,431` 等
- **问题**: `lds_k_deepen` 硬编码 `wiki_gloss_20260808.json`，而 `lds_c_node_edge_decomp` glob 最新——同 gloss 表可能加载不同文件产生不一致数字；gloss 文件缺失 → `gloss={}` → 中文概念被丢弃 → wiki LDS 退化为 C2 伪影（正是本脚本声称修复的 bug）；`sensitivity_threshold_wiki` 缺失 `llm_subject` 文件时**静默跳过**无警告。
- **修复**: glob 取最新并记录实际路径；gloss 缺失显式报错退出；阈值块缺失打印 WARN。

### H3. design_effect 结论为硬编码文本 + human/LLM floor 比较存在样本量混淆
- **位置**: `scripts/lds_c_design_effect.py:261-269,88-117`
- **问题**: (a) `conclusion` 字段是静态字符串（硬编码 0.93-0.96/0.85-0.87），非程序化推导，数据重算不更新；(b) human floor 用 6/6→3/3、EN 3→1/2 切分，LLM floor 用 10→5/5——**每半样本数不对称**，小半集 LDS 更高。实测 N-matched（N=6：3+3）复核后 LLM floor 仍 0.854-0.885 远低于 human 0.922-0.958（gap 0.05-0.07），**结论成立**，但 headline 表用不匹配 N 的数字且未披露此混淆。
- **修复**: conclusion 程序化生成；floor 表标注 half-size；输出记录 N per language。

### H4. P3 联想 gloss 缺失时守卫失效 → 中文概念静默清空 → assoc LDS=1.0
- **位置**: `scripts/lds_c_llm_analyze.py:323-330`
- **问题**: 警告条件是 `if p3_records and gloss:`，`gloss` 为空 dict 时为 falsy → 警告块整体跳过。此时 `canonical_key("自由")` 无拉丁 token → 空 key → ZH 联想集空 → assoc LDS=1.0 静默进入结果。
- **修复**: `if p3_records and not gloss:` 显式报错；校验每语言概念集非空。

### H5. 人类 LDS-C / v3 数值在两个表之间漂移
- **位置**: `03_results.md` §4.2/§4.5 vs §5.9.1/§5.9.4
- **问题**: 同批人类数据，§4.2 概念级 0.961/0.933/0.934，§5.9.1 却 0.963/0.932/0.936；人类 ZH-DE v3 §4.5 0.964 vs §5.9.4 0.954。同一数量两组值无说明（pooled vs 分组口径差异）。
- **修复**: 统一为一组并互引。

---

## MEDIUM（应改进）

| # | 问题 | 位置 |
|---|------|------|
| M1 | 控制台表把 \|ΔLDS\| 标成 "d"，Cohen's d 从未实现（函数存在但未调用） | `lds_c_compute.py:339,392-413` |
| M2 | 标签置换零模型只输出均值/SD，**从不计算观测 LDS 的 p 值** | `lds_c_compute.py:311-336` |
| M3 | `--seed` CLI 参数被忽略（死参数，`random.seed(RANDOM_SEED)` 硬编码） | `lds_c_compute.py:423,431` |
| M4 | 模型标签硬编码 `"deepseek-v4-flash@opencode"`，不读提取文件 model 字段 | `lds_c_compute.py:377` |
| M5 | bootstrap CI 百分位索引 off-by-one（约定性） | `lds_c_compute.py:261-262` |
| M6 | "LDS-K" 同名两种定义：concept-level node-only vs v3 含边，跨脚本混用风险 | `lds_c_compute.py:210-230` vs `lds_k_deepen.py:61-75` |
| M7 | human 边元组含 type、wiki/math 边不含 → 跨源 edge 分量不可横向比较 | `lds_c_node_edge_decomp.py:119` |
| M8 | 数学跨层边只归 source 层；无 labels 的 group 边静默丢弃 | `lds_k_deepen.py:141-151` |
| M9 | 输出目录双份拷贝（outputs/ 与 data/lds_c/ 内容相同），非 compute 脚本不记录输入路径/模型/seed | 多处 |
| M10 | TOPICS/PAIRS 常量多脚本重复定义，加主题会静默失配 | 5 处 |
| M11 | `signal_to_floor_ratio` 除零无保护 | `lds_c_design_effect.py:110` |
| M12 | 各脚本"glob 最新文件"装载数据，可能静默换源 | 5 处 loader |
| M13 | strict/loose 对齐敏感性同时改变边方向性（混淆变量） | `lds_k_deepen.py:243-295` |
| M14 | NaN 写入 JSON（allow_nan 默认 True），下游标准解析器会失败 | `lds_c_llm_analyze.py:262` |
| M15 | divergence_drivers 主题标签严格匹配 vs LDS-C 容错 → 同一数据两套数字 | `lds_c_divergence_drivers.py:55` |
| M16 | LDS-C 仅按 presence 计（union 去重）丢弃频率，论文未说明 | 设计选择 |

---

## 验证已确认健康的点（正面）

- **LMM 似然实现**：复合对称 log|V| 与二次型公式逐行核验**正确**（`(m-1)logσ² + log(σ²+mτ²)`；`ss/σ² − τ²/(σ²·s2_block)·(Σr)²`）。
- **方向 D 与 A4 完全一致**：node_edge_decomp 的 math/wiki LDS、J_node、J_edge 与 lds_k_deepen_20260808.json **逐位相同**。
- **设计效应数字**：human floor（design_effect n_iter=200）与 canonical（n_iter=1000）差异 <0.001；LDS-C CI 人类 vs LLM **全部重叠**（支持"信号幅度相同"主张）。
- **N-matched 复核**：把 LLM floor 改用与人类匹配的 3+3 切分，floor 仍 0.854-0.885 远低于 human 0.922-0.958 → 设计效应结论**不依赖样本量混淆**，成立。
- **53 个 pytest 全部通过**（含本会话新增 8 个深化脚本冒烟测试）。

---

## 深入方向（基于审查发现，按优先级）

### 方向 1（最高）：统计推断完备化 —— 空模型正式 p 值 + LMM 推断加固
- 补 M2：标签置换算出 `p = mean(perm ≥ obs)`，人类与 LLM 的"信号 vs 底噪"从目测升级为正式检验。
- 修 H1：LMM 加 cell 级随机效应（或 cluster-robust SE by cell），重跑 D1 机制结论，看 same_lang 显著性是否存活——**若存活则 M2 主导结论更稳，若不存活则必须诚实降级**。
- 价值：审稿人问"你凭什么说代码层主导"时，给的是稳健推断而非近似推断。

### 方向 2：C2 空集守卫 + 全覆盖空模型测试
- 修 C2（核心度量空集约定），并为 `jaccard`/`lds_v3`/`canonical_key` 空集分支补测试（当前测试恰好没测空集）。
- 价值：杜绝任何子样本/阈值/gloss 分支静默产出 LDS=1.0 伪影——这是评审会深挖的诚实性点。

### 方向 3：论文方法学章补全（C1）
- §2.7 补 v3 公式 + LDS-K/C/ΔLDS 变体 + 空模型套件方法。
- 价值：评审逐章核对的第一处撞墙，修复后论文自洽。

### 方向 4：设计效应从"排除法"升级为"直接检验"
- 目前"人类阴性 = 组内个体异质性"是排除法（LLM 数据在组间 lens 下存活 → 非组间设计本身）。
- 直接检验：对人类数据做**不同聚合水平的 floor 扫**（N=2/3/4/5/6），证明 floor 随人类样本数下降而下降（而非异质性本身）——或用现有 3 名双语者做真人类组内 pilot（B 方向，需真人）。
- 价值：把"设计伪影"主张从排除法变成直接测量。

### 方向 5：数字口径统一（C3/C4 + manifest 遗留）
- ΔLDS 统一 v3 基准；coverage 数字选一组贯穿；manifest 556/557、219/247 对齐。
- 价值：评审最常抓"数字不自洽"，统一后一劳永逸。

---

## 建议执行顺序

```
P0 合规（已完成：支持披露+审计文档）→
P1 论文自洽（C1 方法章 v3 + C3 ΔLDS + C4 coverage）→
P2 统计完备（方向1：置换 p 值 + LMM 加固；方向2：空集守卫）→
P3 血缘（H2 路径 + M4 模型透传 + M9 lineage）→
P4 深入（方向4 设计效应直接检验）
```
