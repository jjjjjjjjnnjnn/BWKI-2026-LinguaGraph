# LinguaGraph — 研究层批判性审查与未来方向（2026-08-11）

> **依据**: 用户要求"不进入呈现部分，继续研究"——本审查聚焦**研究层**（方法学 + 证据强度 + 可复现性），非项目管理维度（后者见 `docs/review/rnd_project_review_20260811.md`）。
> **方法**: 对已提交数据与脚本逐项重验（非重复运行管线，仅核验已提交 JSON/代码），全部发现可追溯到 `data/lds_c/llm_subject/` 与 `scripts/`。
> **验证基线**: `multi_model_replication_20260810.json`（51 测量/47 唯一）· `lmm_20260809.json`（n=50）· `per_topic_20260808.json` · 69/84 pytest 通过。
> **执行进度（2026-08-11）**: R2 / R7 / R3 ✅ 已执行并出结果（`docs/research_forward_findings_20260811.md`）；R1 待启动（需招募）；R4 待用户批准；R5 机会性；R6 待执行。

---

## 0. 一句话结论

**研究主线的证据质量在本轮逐项重验中成立**——51/51 ZH-DE 显著、8/153 英文对非显著、方向一致性 ≥10 票 204 vs 129±4（均与提交数据一致）；但发现 **1 处数据文件内部自相矛盾、3 处计数/口径小错、4 类研究层薄弱点**，并识别出 **7 条可执行的未来研究方向**（其中 3 条零成本、1 条是最高科学价值的闭环实验）。

---

## 1. 本轮逐项重验的事实基线（✅ 均与提交数据一致）

| 声明 | 重验结果 |
|------|---------|
| 51 测量 / 47 唯一模型 | ✅ 51 有效条目 = 43 DashScope + 8 zen；`split(":")[-1]` 去重得 47（4 对双 host） |
| 51/51 ZH-DE 显著 | ✅ 153 对中非显著仅 8（p≥0.05），ZH-DE 0 个非显著 |
| 8/153 非显著全为英文对 | ✅ 2 ZH-EN + 6 DE-EN；其中 6/8 为 DeepSeek-R1/Distill 族 |
| 方向一致性 ≥10 票 204 vs 129±4 | ✅ 空模型固定频次+随机方向；≥3 票 1056 vs 823±9.5 亦显著（24 SD） |
| Heimat:safety 41/51（80%）DE | ✅ de_only_strong[0] = [41, 0] |
| LMM: same_lang +0.038 (p<0.001) / same_frame +0.001 (p=0.90) | ✅ n=50 dyads，5 cells，n_same_lang=10，n_same_frame=10 |
| 主题级（基线模型）ZH-DE 全主题有信号 | ✅ Freiheit +0.070 / Gerechtigkeit +0.086 / Verantwortung +0.062 / Heimat +0.103 / Erfolg +0.094 |

---

## 2. 确认的 bug / 不一致（需修，按严重度）

### 🔴 B1 — 数据文件内部自相矛盾（最严重，P1 SSOT 直接违反）
`data/lds_c/llm_subject/multi_model_replication_20260810.json` 的 `direction_consistency.readme` 声称：

> "the >=3 count lies inside that noise band (audit C2)"

但**同一文件的** `observed_vs_null["3"]` 显示：observed **1056** vs null 823±9.5，p_null_ge_observed = **0.0**（~24 SD 超出空模型）。**≥3 明显显著**，与论文 §5.10、§8.15、handoff、对抗审查更正横幅（"权威数字 204 vs 129 / 1056 vs 823"）全部一致。

**结论**：readme 措辞是审计 C2 修正前（"1179 双计数"时代）的**过期残留**，与其自身数据矛盾。数据 JSON 为不可变证据（P2，不 in-place 改），修复方式：
- 在 `docs/multimodel_replication_20260809.md` 或 handoff 加一条显式注记：`multi_model_replication_20260810.json readme 的 "≥3 lies inside noise band" 为过期措辞，以 observed_vs_null 数据 + 论文 §5.10 为准（≥3 显著）`；或
- 下次重新生成 replication 时修正 readme 字符串（同时保留旧文件）。

### 🟠 B2 — 论文计数小错（2 处）
1. `docs/paper/03_results.md` §5.10 写 "**42** DashScope- und 8 zen/OpenRouter-Modelle → 51" — 实测 **43** DashScope（+8 zen = 51）。
2. `docs/paper/04_discussion.md` §8.15 写 "westlicher Anteil auf **ein** NVIDIA-Modell begrenzt" — 实际西方来源模型 **2 个**：`nemotron-3-ultra`（NVIDIA，美国）+ `laguna-s-2.1`（**Poolside，美国实验室**）。laguna 未计入西方披露。论文 §5.10 的 "~88 % chinesische Anbieter" 实际应为 ~94–96%（51 中 2–3 西方），"88%" 偏保守但披露意图诚实。

### 🟠 B3 — handoff 数据过期
`docs/session_handoff_20260810.md` §7 写 "gpt-oss 17/30"。实测：`llm_subject_openai_gpt-oss-20b_free_20260809.json`（1 zh）+ `_20260810.json`（zh 10 + de 10）≈ **21 唯一 P1 单元，en 全缺**。故该模型报 "incomplete"（`MIN_UNITS_PER_LANG=5` 且 en=0）是正确的，但数字应刷新为 21/30、en 缺口。

### 🟡 B4 — 潜在数据韧性缺陷（当前未触发）
`scripts/lds_c_multi_model.py` 的 `discover_models()` **每模型只取最新日期文件、不跨日合并 GOOD 单元**，与 `lds_c_llm_subject.collect_good_units()`（按 unit_id 合并）语义不一致。当前数据未触发（provider 前缀保证 model key 分离 + 新文件更完整），但若未来出现"旧文件完整 + 新文件部分"（如重跑中断），复制分析会**静默丢弃完整单元**。建议：`discover_models` 对齐为 `collect_good_units` 语义（按 unit_id 去重合并），并加一条回归测试（API 鲁棒性测试套件已在 `tests/test_api_robustness.py`，但复制分析路径未覆盖）。

---

## 3. 研究层空缺与薄弱点

### G1 — 西方模型覆盖 ≈ 2/51（最大外效空缺）
51 有效测量中：43 DashScope（中国）+ 6 中国模型经 zen + **2 西方**（nemotron-ultra, laguna）。尝试过的西方前沿（gpt-oss 21/30 缺 en、gemma-4-31b 3/30、laguna 部分、nemotron-ultra-OpenRouter 3/30）**全部因配额未完成**（handoff 已诚实披露，但未量化"实际只有 2 个西方模型"）。
- **影响**：方向一致性（DE-自主/ZH-空间）实质由 49 个中国模型建立，西方证据仅 2 模型。**handoff 措辞"跨中西方极度稳健"过强**；论文 §8.15 相对诚实。命题应表述为"跨中西方（2/51 西方）"而非"跨文明"。
- **机会性解法**：gpt-oss 仅缺 10 个 en 单元，OpenRouter 配额恢复时 1 次运行即可纳入（51→52）。

### G2 — 英文空结果无机制解释（✅ 已闭环 → 转为发现）
8/153 非显著全为英文对（2 ZH-EN + 6 DE-EN），且 **6/8 是 DeepSeek-R1/Distill 族**。论文 §5.10/§8.15 只报告事实，无机制。三个可测假设：
1. **EN 高 floor**：模型英语语料最丰富 → EN 概念集更大/更稳定 → 语内 Jaccard 高 → 信噪比低；
2. **EN 桥接**：DE/ZH 概念空间都向英语训练分布对齐 → EN 与两者都相似 → DE↔EN、ZH↔EN 信号弱；
3. **R1 推理模式伪影**：R1/Distill 的 CoT 解码同质化跨语言概念产出。

**若 (2) 成立，本身是强结论**："英语作为模型内部通用语，平滑了 DE/ZH 价值概念分歧"——对接 value-alignment 文献（WorldValuesBench 等均以英语评测，有直接审计含义）。

**✅ 已执行（R2，2026-08-11）**: 机制 = 信号梯度（ZH-DE > ZH-EN > DE-EN）× 模型 floor 抬升（NS 模型全部语言 +0.05~0.07，概念 ~15% 更多）；R1 族 5/5 NS（Fisher p=9e-6）。EN 空是模型级弱信号尾部，非 EN 特有缺陷（详见 `docs/research_forward_findings_20260811.md` §2）。

### G3 — LMM frame 效应识别弱（设计强度问题）
LMM 仅 5 cells（3 natural + 2 crossed），`same_frame` 由 **2 个 dyads/主题**（10/50 行）识别；cluster bootstrap 在 **5 个 cell** 上重采样退化（近确定性）。因此 "same_frame +0.001, p=0.90 → frame negligible (M3)" 实为**低功效的"未检出"**，而非"效应为零"。P2 probe（§5.3：frame 在 code 内移动概念，LDS≈0.91）是 frame 效应的更干净证据，但 **code 间 frame 效应的真正估计需要完整 3×3 交叉设计**。

### G4 — 主题×模型粒度缺失（✅ 已闭环）
复制仅报告 pair 级聚合；**51×3×5 的主题×模型 margin 表不存在**。无法回答"ZH-DE 信号是否每个主题在所有模型成立，还是 1–2 主题驱动"。基线模型的主题级分析（5 主题全有信号）**不能外推到 51 模型**。

**✅ 已执行（R7，2026-08-11）**: 50/51 模型 5/5 主题 ZH-DE margin 为正 → 信号跨主题成立（`docs/research_forward_findings_20260811.md` §1）。

### G5 — k 敏感性未测（✅ 部分闭环）
协议固定 k=10，未扫 k∈{5,8,10,15}。LDS 作为审计工具，其对提取深度（k）的稳定性是核心鲁棒性问题，未验证。

**✅ 已执行（R3-A）**: 实测概念/主题为 5–6，k'∈{3,5,6} 下 ZH-DE margin **100% 正**（k 鲁棒）；但**语言对排序不稳定**（≈50/50）→ 论文避免排序声明。

### G6 — 概念对齐方法脆弱性（✅ 部分闭环）
`canonical_key` 字符串对齐 + 词表映射仅合并 ~5%；对齐方式（嵌入对齐、LLM 判定同义）变化会系统影响 LDS。未做对齐敏感性分析。

**✅ 已执行（R3-B）**: 模糊 token-overlap 对齐下，**ZH-DE 保持最分歧 + DE 侧方向存活**（严格 +23 → 模糊 +11）；EN 对内部排序敏感（不可声明）。注：模糊代理非 LLM 判定同义，后者留作未来。

### G7 — 多重比较未校正（已披露，无碍主结论）
153 对 perm 检验无 FDR；因 0/51 ZH-DE 失败，主结论不受影响，但 "8/153" 与 per-pair p 应注明未经校正。perm p 粒度为 p<0.004（n_iter=500），已披露。

### G8 — ΔLDS 的"语言成分"未分解
within-subject 消除了模型异质性，但"语言"仍混淆 (i) prompt 语义内容、(ii) 训练分布、(iii) 翻译伪影。P5（answer vs prompt 语言）探针在基线存在，但**未在 51 模型上执行**。

---

## 4. 未来研究方向（按优先级，标注成本与价值）

| # | 方向 | 成本 | 价值 | 说明 |
|---|------|------|------|------|
| **R1** | **人类组内直接检验**（within-subject 双语者） | 1–2 周，需招募 6–10 名 DE/ZH/EN 平衡双语者各用 L1+L2 答 5 主题 | **最高**——直接闭环"人类阴性=组内异质性" | ✅ **协议定稿 + 分析脚本就绪**（`docs/planning/r1_within_subject_protocol.md` + `scripts/lds_c_r1_within_subject.py`）。**补完预注册组内臂**（OSF §2.1/§4.2），非新实验。**待用户启动招募**（3 轮：L1/L2/L1 重测） |
| **R2** | **英文空结果机制分解**（G2 三假设） | 零成本，2–3 天 | 高——把 caveat 转为发现 | ✅ **已执行**（`docs/research_forward_findings_20260811.md`）：EN 空 = 信号梯度尾部 × R1 族 floor 抬升（Fisher p=9e-6），非 EN 特有缺陷 |
| **R3** | **LDS 度量鲁棒性套件**（k 扫描 + 对齐敏感性） | 零成本，2–3 天 | 高——LDS 作为审计工具的证据 | ✅ **已执行**：k∈{3,5,6} ZH-DE 100% 正（鲁棒）；模糊对齐下 ZH-DE 最分歧 + DE 方向存活；**EN 对排序不稳定**——避免排序声明 |
| **R4** | **完整交叉 frame 设计**（3×3，5 模型子集） | ~2 天，DashScope 免费额度内（~675k tokens/模型） | 中高——为 M2/M3 核心结论提供充分统计 | 9 cells = 36 dyads/主题 → same_lang/same_frame 识别充分。⚠️ 属新实验，超出现冻结 30 人实验方案，需用户批准 |
| **R5** | **机会性完成 gpt-oss**（补 10 en 单元） | OpenRouter 配额恢复时 1 次运行 | 中——西方前沿覆盖 2→3/52 | 不自动重启编排器（handoff 明确） |
| **R6** | **方向向量 × 文化理论定量校准** | 1 天（~50 概念 × 5 人规范） | 中高——升级 §8.16 解释性假设 | 51 模型 per-concept DE/ZH 投票向量与概念级文化标注（抽象性/关系性/情感效价）相关；显著则讨论落点最强 |
| **R7** | **主题×模型全表**（51×3×5 margin 表） | 零成本，数小时 | 中——检验主题一致性 | ✅ **已执行**：50/51 模型 5/5 主题 ZH-DE 正——信号跨主题成立，非主题驱动；附带发现"最可靠显著 ≠ 幅度最大" |

### 建议执行顺序（2026-08-11 更新）
1. **✅ 已完成（零成本，纯计算）**：R7 → R2 → R3（`docs/research_forward_findings_20260811.md`）——G2/G4 闭环、G5/G6 部分闭环；
2. **并行启动最长路径**：R1 招募（尽早）；
3. **预算内**：R4（若时间允许，需用户批准扩展）；
4. **机会性**：R5；
5. **必做小修**：B1 注记 ✅、B2 计数修正（论文，待用户）、B3 刷新 ✅。

---

## 5. 保留不动（审慎判断）

- **数据 JSON 不可变**：B1 只加注记，不改 `observed_vs_null` 数字（数字正确，措辞过期）。
- **不自动重启 OpenRouter 编排器**：配额未恢复，重启浪费轮询（handoff 明确）。
- **不碰冻结项**：R3 是对齐敏感性分析（非修改冻结映射）；R4 需用户明确批准后作为新实验开展。

---

*版本: v1.0 | 2026-08-11 | 与 `rnd_project_review_20260811.md`（六维度）+ `full_project_adversarial_review_20260810.md`（对抗审查）构成三层审查体系*
