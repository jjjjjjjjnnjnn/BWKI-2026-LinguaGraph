# LinguaGraph — 完整项目状态交接文档（v1.0）

> **生成时间**: 2026-08-10 | **版本**: v1.0（v0.9 + AI 审计叙事 + 51 模型复制 + 多提供商基建）
> **上一交接**: `docs/session_handoff_20260808.md`（v0.9，已被 v1.0 取代）
> **新 AI 加载顺序**: ① 本文件 → ② `docs/submission/einreichung_checkliste.md`（提交清单）→ ③ `.claude/CLAUDE.md`（治理）
> **BWKI 截止**: 2026-09-20/21（约 6 周）

---

## 1. 当前阶段与核心状态

**阶段**: Month 2「理论 + 分析」（8 月）。研究主线已完整；**当前焦点 = 多模型复制（已 51 模型）+ 提交工程（AI 审计叙事）**。

**研究主线（三层完整证据链 + 51 模型复制）**:

> **"多语言 AI 是否在语言之间漂移地理解价值概念？"——是，51/51 模型显著；文化方向（DE 自主 vs ZH 空间）跨中西方极度稳健。人类组间阴性已被证明是设计伪影（信号幅度与 LLM 相同，差异在底噪）。**

| 层 | 结果 | 一句话 |
|----|------|--------|
| 人类 N=15 组间 | 阴性（LDS-C ≈ 噪声底） | 组间设计测不出 → **设计伪影** |
| LLM 组内（D1） | 阳性（LDS-C ≫ 底） | 同一模型三语 → **语言信号真实存在** |
| 设计效应证明（A3） | 人类/LLM 信号幅度相同，底噪不同 | 人类阴性 = 组内个体异质性（异质性注入直接因果证明，q=0.30 精确复刻） |
| 语料深化（A4） | 社会 Wikipedia ZH-DE 0.82 vs 数学 0.52 | 制度知识抹平语言，文化概念暴露语言 |
| **51 模型复制（🆕 2026-08-10）** | **51/51 模型全部 LDS-C ≫ floor、p<0.05；ZH-DE 余量 +0.033~+0.286；1179 方向一致概念；Heimat:safety/physical space 41/41 全票** | **跨语言价值观分歧 = 多语言 LLM 普遍属性（中西方皆然）** |

**三大不可违反原则**（.claude/CLAUDE.md §1）: SSOT=manifest.json · Immutable Release · Validated Pipeline。

---

## 2. 🆕 AI 审计叙事（提交定位，2026-08-09 决策）

**场景 A（选定）**: LinguaGraph = **多语言 AI 价值观一致性审计工具**——测量模型是否在语言间漂移地理解价值负载概念，并定位分歧组件。

- **用户担忧已回应**：项目不"不实用/不直观"——是"用 AI 研究 AI 本身"（LLM-as-Subject = 被测对象），AI 审计是前沿且实用
- 叙事材料已重写（`docs/video_script.md` v2、`docs/pitch_3min.md`、`docs/pitch_30s.md`）
- 提交清单：`docs/submission/einreichung_checkliste.md`（平台问答草稿、代码提交指南、PDF 工具链决策）

---

## 3. 🆕 多模型复制（51 模型，核心新成果，勿重跑）

### 3.1 结果（`docs/multimodel_replication_20260809.md` + `data/lds_c/llm_subject/multi_model_replication_20260810.json`）

| 指标 | 值 |
|------|-----|
| 完整模型 | **51**（8 zen/OpenRouter + 42 DashScope + gpt-oss 部分） |
| 信号 | **51/51 LDS-C ≫ floor，所有语言对 p<0.05** |
| ZH-DE 余量 | **+0.033（deepseek-r1-0528）~ +0.286（deepseek-v3.1）**，全为正 |
| 方向一致性 | **1179 概念**（≥3/51），Heimat:safety（DE）与 physical space（ZH）**41/41 全票**，equal opportunity/freedom limit 39 票 DE |
| 漂移排名 | 余量跨模型差 ~9 倍 → 审计"按模型排名"操作性输出 |

### 3.2 模型来源（跨中西方）
- **zen 免费**（8）：deepseek-v4-flash/pro、glm-5.2、kimi-k2.6、mimo、laguna、longcat、**nemotron-3-ultra-free（NVIDIA 美国）**
- **DashScope（42）**：deepseek-v3/v3.1/v3.2/v4/r1 族、glm-4.5~5.2、kimi-k2.x、MiniMax、qwen3.x 家族

### 3.3 基建（API/配额，⚠️ 重要）
| 提供商 | 端点 | key 在 `.env` | 配额 | 状态 |
|--------|------|-------------|------|------|
| opencode zen/go | `https://opencode.ai/zen/go/v1` | `OPENAI_API_KEY` | 付费 | ✅ 已用 |
| opencode zen/v1 | `https://opencode.ai/zen/v1` | 同上 | 免费（日限） | ✅ 已用 |
| OpenRouter | `https://openrouter.ai/api/v1` | `OPENROUTER_API_KEY` + `OPENROUTER_API_KEY2` | 免费（日限 ~50-100 次，~08:30 重置） | 🔄 gpt-oss 17/30 跨日累积 |
| **DashScope/千问** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `DASHSCOPE_API_KEY` | **137 模型各 1M 免费 token** | ✅ 已用 42 |

**⚠️ 教训（欠费事件）**: 2026-08-10 曾因用非免费额度模型导致 DashScope 账号欠费封锁。**此后只用用户确认的 137 免费清单模型**（`scripts/run_dashscope_batch.py` 已过滤）。**DashScope 免费清单 = 用户 2026-08-10 提供的 137 个模型列表**，勿用清单外模型。

---

## 4. 数据状态

### 4.1 已提交数据（勿重跑）
- 人类 SSOT：`freeze/freeze_survey_20260703|0712/`（15 合格，6DE+6ZH+3EN 双语试点）
- D1 原始：`data/lds_c/llm_subject/llm_subject_20260808.json`（220 units）
- **多模型 subject 文件**：`data/lds_c/llm_subject/llm_subject_{provider}_{model}_{date}.json`（各 30 units）
- **复制结果**：`data/lds_c/llm_subject/multi_model_replication_20260810.json`

### 4.2 关键脚本（新增/修改）
| 脚本 | 功能 |
|------|------|
| `lds_c_multi_model.py` | 多模型复制 harness（复用冻结纯函数，方向一致性投票） |
| `lds_c_llm_subject.py` | 支持 `--model`/`--api-url`/`--api-key-env`/`--provider`；跨日 resume（合并好单元）；`LDS_ABORT_AFTER=3` 连续失败中止 |
| `run_dashscope_batch.py` | DashScope 并行批（6 worker，**仅免费清单模型**） |
| `run_openrouter_batch.py` | OpenRouter 配额轮询 + 顺序批 |
| `build_divergence_map.py` | 交互式 demo 生成器（普通人可视化） |

**API keys**: `.env`（gitignored）含 `OPENAI_API_KEY`（zen）、`OPENROUTER_API_KEY`/`OPENROUTER_API_KEY2`（OpenRouter 两账号）、`DASHSCOPE_API_KEY`（千问）。

---

## 5. 提交工程状态（9/20 截止，见 `docs/submission/einreichung_checkliste.md`）

| 提交物 | 状态 |
|--------|------|
| 平台问答草稿 | ✅ `docs/submission/plattform_antworten.md`（德文 8 节） |
| 代码提交指南 | ✅ `docs/submission/code_einreichung.md` |
| 视频脚本 v2（AI 审计） | ✅ `docs/video_script.md`（**未录制**） |
| 论文 PDF | ⏳ 待工具链决策（pandoc+MiKTeX 推荐） |
| 支持披露 | ✅ `docs/declaration_of_support.md` + `CONTRIBUTORS.md` |

---

## 6. 下一步（建议优先级）

1. **文献扎根**（任务 8）：51 模型的 DE-自主/ZH-空间 模式 ↔ Markus & Kitayama / Hofstede → 论文可解释小节
2. **OpenRouter 西方模型**（gpt-oss 17/30 等）：跨日累积完成（需 ~2-3 天）
3. **论文数字一致性**：`04_discussion.md` §4.15 已是 51 模型版；`03_results.md` 结果章待同步 51 模型引用
4. **提交工程**：视频录制（最大剩余项）、PDF 组装
5. **任务清单**：#5 PDF（pending）、#8 文献扎根（pending）、其余完成

---

## 7. 风险

| 风险 | 缓解 |
|------|------|
| DashScope 账号再欠费 | 只用 137 免费清单模型（已过滤） |
| OpenRouter 免费配额太小（单日无法完成一模型） | 跨日 resume（`--provider` 隔离 + 好单元合并） |
| 视频未录制（最大提交风险） | 脚本 v2 已就绪，8/14-28 录制窗口 |
| 51 模型数据量大 | 已提交，git 保护 |

## 8. 🆕 对抗性审查 + 修复状态（2026-08-10，P0-P3 全部完成）

**审查**: `docs/review/full_project_adversarial_review_20260810.md`（4 agent 并行：模型QA/现实检验/代码审查/critic）。发现 9 CRITICAL，核心是"声明与随代码数据不符"。

**P0（数据说真话 + 合规）✅**:
- C1: "51/51 全部 p<0.05" 修正 → 实际 **51/51 ZH-DE 显著，8/153 英语对不显著**；p=0.0 → p<0.004 说明
- C2: 方向一致性加**空模型**（≥10 票 **204 vs 129±4，p<0.001**——观测非噪声）；弃用双计数的 1179
- C3/C7: 诚实分母（41/51=80%、physical space 1 反票）、47 唯一/88% 中方
- C6: 披露重写（三提供方 + 欠费 + F1 修正）
- C9: ratio 解读反转修复 + loader 内容校验 + 提交全部输入文件

**P1（一致性 + 评分）✅**:
- C4: SSOT 对账——论文统一到 **556/525/219/68 教材（39+18+11）**（旧 574/3538/247 是硬编码残留）
- C5: 结果章加 §5.10 复制章节；结论/提交/视频同步定位 C
- H1: 启发式阈值（ZH-DE 余量 ≥0.10 = 高分歧）
- H4: judge_qa.md 重写为实际设计

**P2（方法学深修）✅**: `docs/p2_methodology_rechecks.md`
- C8: size-match 领域对照**反转**（k=15-35 wiki J_node 高于数学）→ "制度趋同/文化分歧"不能作内容证据，已降级
- H2: 异质性注入降级为"一致性演示"（target_q 未坍缩）
- H3: 交叉提取保留 ZH-DE 76%/DE-EN 79%（非纯自提取伪影），EN 对敏感

**P3（收尾）✅**: release.py 验证通过；69 pytest 全过（+loader/空模型/ratio/提取提示词回归测试）；工作树干净。

**⚠️ 遗留（提交前仍须处理）**:
- **结果章引用 §3.8 领域不对称处**需与 P2-1 降级一致（已加 caveat，但 §3.8 主文本仍用 0.444/0.800 作"内容驱动"证据——需同步措辞或标注）
- manifest 与 release/ 一致性已由 release.py 保证
- 视频录制（8/14-28）

---

*交接版本: v1.0 | 2026-08-10 | 数据血缘见 §4 + `LINGUAGRAPH_DATA_LINEAGE.md`*
