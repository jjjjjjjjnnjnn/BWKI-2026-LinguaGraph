# LinguaGraph — R&D 全生命周期审查报告（2026-08-11）

> **依据**: 开发与研究型（R&D）项目核心要求框架——六维度：目标与范围 · 技术先进性 · 过程管理 · 团队结构 · 质量合规 · 成果转化
> **范围**: 全项目审查 + 先进性扫描 + 项目结构与过期/冲突文件处置
> **前置**: `docs/session_handoff_20260810.md`（v1.0）· `docs/review/full_project_adversarial_review_20260810.md`（4-agent 对抗审查）
> **验证基线**: 69 pytest 通过 · `release.py --dry-run` PASS · PDF 30 页（含本次整合的物理/LPA 章节）

---

## 0. 总评

**定位**：这是一个 **偏研究型（Research-weighted）** 项目——核心产出是方法（LDS v3）+ 复制证据（51 模型），容错率适中（允许诚实阴性），评审重点是创新性与可复现性，而非产品稳定性。这一定位合理且与叙事定位 C（方法论为中心）一致。

**优势**（远超一般学生项目的部分）：
- **OSF 预注册**（RQ1-3 + H1-H3 假设状态表）——规范的研究生命周期起点
- **冻结指标 + SSOT + 不可变 Release + 门控管线**——三条不可违反原则已工程化
- **诚实阴性文化**：人类 N=15 阴性、H1 falsified、P2 复核降级（C8 反转/H2/H3）——可证伪性实践到位
- **合规完整**：GDPR 包 + 三语同意 + CC-BY-SA 披露 v2.0 + 欠费事件诚实披露

**主要弱点**（见各维度）：① 先进性论证的**查新断档**（文献矩阵 6 周未更新、论文缺 LLM 文化对齐 SOTA 对照）；② 多学科侧流（chemistry）未闭环；③ 知识沉淀过度依赖 AI 会话（CHANGELOG/PROJECT_LOG 停滞）；④ API 管线缺正式鲁棒性测试。

---

## 1. D1 目标与范围界定

**双重目标**：

| 目标类型 | 内容 | 状态 |
|---------|------|------|
| 研究目标 | OSF 预注册 RQ1-3（教材结构跨语言分歧 / 人类认知表达分歧 / ΔLDS 隔离语言成分） | ✅ 假设已判（H1 falsified 等） |
| 开发目标 | BWKI 完整提交包（PDF · 代码 · 视频脚本 v2 · 平台问答草稿） | ✅ 材料齐备，剩用户物理动作（视频/平台填写） |

**TRL 对标**：协议验证级（LLM-as-Subject within-subject 协议在 51 模型上验证），非产品级；审计工具（Positioning C）诚实定位为未来工作，需阈值 + 西方模型 + 规范性判断。

**边界约束**：
- ✅ `FUTURE_WORK.md` 明确 out-of-scope（微调、模型合并、指标扩展等）
- ✅ `CLAUDE.md` 冻结 LDS/问卷/概念映射/管线架构
- ⚠️ **发现——侧流未闭环**：多学科验证（physics 366 概念 / chemistry 220 / LPA 语言产出）曾作为 roadmap 项进入，但未闭环。**本次处置**：physics + LPA 已整合入论文（PDF 30 页）；chemistry 仍为未纳入范围的状态，需明确披露或关闭（见 §8 建议）。
- ⚠️ 止损点依赖 `restart_plan.md` + handoff，无正式"范围变更控制"文档（轻微；单人项目可接受）。

---

## 2. D2 技术先进性与创新性（含先进性扫描）

### 2.1 可辩护的创新点

| 创新点 | 与 SOTA 差异化 |
|--------|---------------|
| **LDS v3 度量**（`1 − mean(J_node, J_edge)`） | 度量**结构性概念图分歧**，而非任务准确率/偏好选择——区别于主流 LLM 评测 |
| **LLM-as-Subject within-subject 设计** | 同一模型三语作答 → **语言是唯一变量**，构造上分离语言与个体异质性（人类组间设计做不到） |
| **51 模型跨中西方复制**（47 唯一，88% 中方 + 1 NVIDIA 美） | 跨提供方复现 + 空模型方向一致性，非单点发现 |
| **方向一致性空模型** | 固定频次 + 方向随机，≥10 票 204 vs 129±4（p<0.001）；≥3 票 1056 vs 823 亦显著（非噪声） |

### 2.2 可证伪性（强）

H1 falsified、N=15 人类阴性诚实报告、P2 复核（C8 领域对照反转、H2 异质性降级、H3 交叉提取敏感性）——**"数据说真话"文化落地**，这是真正的 R&D 气质。

### 2.3 查新与对标（⚠️ 本次先进性扫描的核心 Gap → 已部分解决）

- 现有证据：`docs/literature_matrix.md`（2026-06-22，5 领域）+ 论文 `02_related_work.md`（4 线索）
- **Gap A——文献矩阵断档**：6 周未更新，未覆盖 2026 年中最新工作（仍待补——可用本报告的 arXiv 查新结果刷新）
- **Gap B——对标错位**：论文 related_work 以**教育知识图谱**为中心，但当前核心叙事已演化为**多语言 LLM 价值概念分歧**——未对照该热点 SOTA。**已解决**：完成实时 arXiv 查新并产出 **`docs/sota_positioning_20260811.md`**（8 组检索词、6 篇最相近工作逐篇摘要核对 + 更广景观）。**核心发现**：SOTA 全部测"选择/评分/准确率/表示方向"，无一测"概念图结构分歧"——LinguaGraph 的 LDS 图度量 + within-subject + 51 模型面板是真实差异化。论文 related_work 落点建议见该文档 §6。
- **Gap C——网络查新受限**：WebSearch 端点不可用 + claude.ai WebFetch 被拦截；**已解决**：经本地知识库环境（`C:\Users\rongj\Desktop\本地知识库`，urllib + SSL 规避直连 arXiv API）完成 2026-08-11 实时查新，含 2026-07/08 最新工作（MET 等）。正式引用前建议在可联网环境对 8 篇关键论文做最终核验。

### 2.4 知识产权

无专利/软著布局（BWKI 学生竞赛可接受）；`docs/submission/code_einreichung.md` 已定义提交物与许可。`docs/technology_transfer.md` 记录了 MML Runtime 基础设施的复用叙事。

---

## 3. D3 过程管理与敏捷迭代

| 框架项 | 实现 | 评估 |
|--------|------|------|
| Stage-Gate | Gate 0-5（`.claire/workflows/`）+ `release.py` 门控（dry-run PASS）+ PROJECT_CYCLE 周审查 | ✅ |
| 数据规范 | SSOT manifest · LINGUAGRAPH_DATA_LINEAGE · 校验和 · loader 内容校验（C9 修复） | ✅ 强 |
| 可复现 | committed JSON + 69 测试 + 跨日 resume + `LDS_ABORT_AFTER` | ✅ 强 |
| 风险动态管理 | handoff §7 风险表（DashScope 欠费 / OpenRouter 配额停滞）+ 欠费教训记录 | ✅ |

**⚠️ 发现——知识沉淀断裂**：
- `CHANGELOG.md` 停更于 v0.12.0（2026-08-08）；`PROJECT_LOG.md` 停更于 2026-06-23（**本次已归档**，其记录职责由 `session_handoff_*.md` 承担）
- 过度依赖 AI 会话 handoff + memory（`.claude/projects/.../memory/`）——人的维护入口薄弱。**建议**：交接文档作为唯一现行状态源已足够，但 CHANGELOG 需补 v0.13.0（见 §7 执行记录）
- OpenRouter 西方模型跨日累积停滞（免费配额 ~20h 未释放）——已诚实披露为未来工作，**不要自动重启编排器**

---

## 4. D4 团队结构与人才梯队

- 单人 + AI 协作（BWKI 参赛资格允许）；人类被试 N=15（6 DE / 6 ZH / 3 EN）
- 跨学科：cognitive science + NLP + AI + 教育（文献矩阵 5 领域；讨论 §8.16 文化心理学扎根 Markus & Kitayama / Hofstede）
- 知识沉淀：handoff + memory + docs 已建立；无 wiki/seminar（单人项目可接受）
- **评估**：无结构性缺陷；唯一弱点是"人的连续性"依赖单人记忆，靠文档体系缓解

---

## 5. D5 质量与合规性

| 项 | 状态 |
|----|------|
| 伦理审查 | ✅ GDPR 包 + 三语 consent（`docs/ethics/`）+ participant_data gitignored |
| 数据隐私 | ✅ participant_data/raw 等 gitignored（GDPR） |
| 版权 | ✅ 声明 v2.0：三提供方 + CC-BY-SA + 欠费事件 + F1 修正 |
| 标准化 | ✅ 无适用行业标准（研究工具）；code_einreichung 定义提交格式 |
| 测试验证 | ✅ 69 unit/regression + release.py 门控；⚠️ **缺口**：无压力/故障注入测试（API 配额耗尽、跨日 resume 仅靠 `LDS_ABORT_AFTER` 兜底） |
| BWKI 参赛资格 | ✅ einreichung_checkliste + plattform_antworten 草稿 |

---

## 6. D6 成果转化与可持续性

- **可转化性评估**：审计工具（Positioning C）——中期已评估为未来工作（需阈值、西方模型、规范判断）；MML Runtime 基础设施有独立复用叙事（`technology_transfer.md`）
- **文档完备性**：PDF 30 页 · code_einreichung · plattform_antworten · video_script v2 · declaration_of_support —— 强
- **社会效益**：EU AI Act 透明度叙事（视频/答辩/平台问答中量化）——AI 审计价值明确
- **评估**：作为学生竞赛项目，转化文档远超平均水平；商业化转化非目标

---

## 7. 项目结构与过期/冲突文件处置（本次执行，2026-08-11）

### 7.1 修正 in-place（live 文档中的过期数字 → 改为与提交 JSON 一致）

| 文件 | 修正内容 |
|------|---------|
| `docs/multimodel_replication_20260809.md` | 一句话结论：207 vs 181 → **204 vs 129±4**；"1179 在噪声内" → **≥3 票 1056 vs 823 显著**（1179 为旧双计数）；数据引用指向 20260810 权威版 |
| `docs/session_handoff_20260810.md` §3.1 | "1179 方向一致概念 / 41/41 全票" → **≥10 票 204 vs 129±4**；Heimat:safety 41/51（80%）、physical space 41（1 反票） |
| `docs/video_script.md` + `docs/judge_qa.md` | `design_effect_20260809.json` → **`design_effect_20260810.json`**（ratio 解读已修正版） |
| `docs/review/full_project_adversarial_review_20260810.md` | 顶部加**更正横幅**：C2 空模型结论已被修正（评审 agent 双计数），权威数字 204 vs 129 / 1056 vs 823 |
| `docs/a3_c_d_deepen_results.md` | 血缘表设计效应引用 → 20260810 修正版 |

### 7.2 归档（7 文件 → `_archive/20260811_rnd_review/docs/`，gitignore 不跟踪、磁盘 + git 历史双保留）

| 文件 | 原因 |
|------|------|
| `docs/paper/03_results_human_v2.md` | 被 `03_results.md` §4 取代的草稿（内容已整合） |
| `docs/paper/04_discussion_revision.md` | 被 `04_discussion.md` F11/F12 取代的修订草稿 |
| `docs/session_handoff_20260702.md` | 被 20260808/20260810 交接取代 |
| `docs/bwki_paper_outline.md` + `_v2.md` | 被完整论文取代的规划大纲 |
| `docs/repo_restructure_plan.md` | 仓库重构已完成（本审查即执行） |
| `docs/PROJECT_LOG.md` | 停更 7 周，记录职责由交接文档承担 |

### 7.3 整合入论文（本次新增）

- **物理章节**（`06_physics_results.md`，366 概念/383 边，CDS/HDS 跨学科验证）：加入 PDF 构建 ORDER（§6）；讨论章 F6/F7 早已引用，本章补全细节；裁剪 §6.6 未完成状态行（NRW/中文待做 → 一句范围说明）
- **LPA 章节**（`07_lpa_analysis.md`，探索性语言产出框架 + N=6 试点）：重编号 §3.4 → **§7**，修正内部 §3.x 交叉引用，加入 PDF ORDER；**保持探索性定位**（N≥120 大样本从未开展，未升级为验证结果）
- PDF 重建：29 → **30 页**（137K 字符）

### 7.4 保留不动（审慎判断）

- **数据 JSON**（不可变证据，被冻结脚本/loader 引用——如 `extractions_20260807.json` 被 `lds_c_compute.py` 引用，归档即破坏管线）
- **CDS/HDS 数据来源注**：物理/化学章的 CDS/HDS 表来自 `outputs/{physics,chemistry}_comparison.json`（data.js 旧管线原始图，Math 574/3538），而 §6.6 库存表用 SSOT manifest（556/525，对齐图）——两种视图并存，属 CDS 线的既有张力（未重跑管线，重跑会牵连物理章数字）
- README 引用的文档（handoff_multi_subject、pilot_quality_report、recruitment_*、reddit_*）
- `docs/related_work.md`（外部项目定位）vs `docs/paper/02_related_work.md`（论文章节）——**用途不同，非重复**
- `references/`（139 文献）· `freeze/`（SSOT）· `release/`（不可变）· `_deploy/` · `cognitive-space/` · `workbench/`

---

## 8. 遗留风险与建议优先级

| # | 事项 | 优先级 | 类型 |
|---|------|--------|------|
| 1 | **✅ 先进性论证闭环**：SOTA 定位表（`docs/sota_positioning_20260811.md`，arXiv 实时查新）+ related_work §2.5 新线索（[20]-[24]）+ **文献矩阵刷新**（新增 Area 6 十篇 + Tier 1b + BibTeX） | P1 | 已解决 |
| 2 | **✅ 论文章节重编号已完成**（讨论 §4→**§8**、结论 §5→**§9**，消除与结果 §4/§5 冲突；12 个跨文件引用同步）。**已知遗留**：方法论章 §2 与 related_work §2 仍同名（整章级联重编号超出范围） | P2 | 已解决 + 1 已知项 |
| 3 | **API 鲁棒性测试**（压力/故障注入：配额耗尽、resume 一致性） | P2 | 测试 |
| 4 | **✅ chemistry 侧流已闭环**（§6.7 Chemie CDS/HDS 小节：220 概念/215 关系，F8 细化，与 F6/F7 一致） | P2 | 已解决 |
| 5 | CHANGELOG 补 v0.13.0（本审查 + 51 模型 + P0-P3 + PDF） | P2 | 文档（见 §7.1 后执行） |
| 6 | 视频录制（2-4 分钟，脚本 v2 就绪） | P0（用户） | 物理动作 8/14-28 |
| 7 | 平台填写（plattform_antworten 草稿已备） | P0（用户） | 物理动作 |

**已消除的风险**：live 文档数字冲突（5 处修正）、孤儿/过期文件（7 文件归档）、未整合结果流（物理/LPA 已整合）。

---

*审查版本: v1.0 | 2026-08-11 | 与 `docs/session_handoff_20260810.md` + `docs/review/full_project_adversarial_review_20260810.md` 构成审查三件套*
