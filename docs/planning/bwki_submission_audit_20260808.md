# BWKI 2026 参赛要求记录 + 与 LinguaGraph 项目现状比对

> **生成**: 2026-08-08 | **依据**: BWKI 官方 Teilnahmebedingungen（Tübingen AI Center，Stand 28.04.2023）+ 当前项目研究状态
> **目标**: 把官方评分标准与项目逐条对照，识别提交前必须补齐的合规缺口
> **旧版文档**: `docs/bwki-compliance-review.md`（2026-06-17，创意提交阶段，研究完成度 15%——**已被本版取代**）
> **提交截止**: 2026-09-20/21（约 6 周）

---

## 0.0 官方提醒邮件处理（2026-08-09）

**邮件类型**: 项目阶段标准提醒（非个别反馈）。

| 要点 | 含义 | 行动 |
|------|------|------|
| 截止 20.09.26 重申 | 剩 ~6 周 | 倒排计划 |
| **文档直接在提交平台填写**（idea/方法/实现/结果/错误源/批判自评） | 交付物 = 平台问答草稿 | **新增 P0**：`docs/submission/plattform_antworten.md` 草稿 |
| "**Idee darf sich verändern**" | 项目从"教材课程分析"→"认知概念分歧+LLM-as-Subject"的演进**官方允许**，评委欣赏演进叙事 | 文档中主动讲演进路径 |
| 记录"**was nicht funktioniert hat**" | 已有完整失败档案（deepseek 深坑、canonical_key 伪影、Wiki LDS=1.0 伪影、人类阴性） | 满足"错误源分析"评分项，直接复用 |
| 支持透明披露重申 | `declaration_of_support.md` ✅ | 已达标 |

---

## 0. 官方要求速览（从参赛条件提取）

### 提交物（三项）
| 提交物 | 官方要求 | 本项目对应 |
|--------|---------|-----------|
| **1. Schriftliche Dokumentation**（书面文档） | 项目文档 | `docs/paper/`（德文，分节） |
| **2. Lauffähiger Code**（可运行代码） | 机器学习方法 | `scripts/` + `src/`（已验证可复现） |
| **3. Video-Pitch**（2–4 分钟） | 非专家能懂 + 专家能评估复杂度 | `docs/video_script.md`（脚本有，视频未录） |

### 七项评分标准（Dokumentation 决定）
| # | 标准 | 一句话 |
|---|------|--------|
| 1 | **Eigenständigkeit**（独立性） | 自有贡献可辨识、支持来源完全披露 |
| 2 | **Originalität, Kreativität, Ideenreichtum** | 原创方法/新视角 |
| 3 | **Schwierigkeitsgrad und Aufwand** | 难度与工作量 |
| 4 | **Wissenschaftliches Arbeiten** | 错误源分析、嵌入前沿、自评批判 |
| 5 | **Ausblick, Neuheit, Erkenntnisgewinn** | 展望、新颖、知识增益 |
| 6 | **Praktische Relevanz** | 实际意义 |
| 7 | **Lesbarkeit und Struktur des Codes** | 代码可读与结构 |

### Eigenständigkeit 披露要求（本版重点，官方原文摘录）
> "Sämtliche Formen der Unterstützung sind dabei transparent und vollständig offenzulegen. Dies umfasst **insbesondere die Nutzung von KI-Modellen oder Frameworks**, die Mitwirkung beteiligter Personen, Institutionen oder Unternehmen sowie die Verwendung von Datensätzen, die bereitgestellt oder von Plattformen heruntergeladen wurden. Ebenso ist anzugeben, wenn **GPU-Rechenleistung oder technische Infrastruktur** zur Verfügung gestellt wurde."

→ **AI 模型/框架、数据集来源、人员/机构、算力基础设施，全部必须披露。** 违规可被取消资格。

### 其他合规红线
- **EU AI Act** 遵守（"geltenden politischen Vorgaben und Regularien wie dem EU AI Act"）
- 语言：**德文或英文**均可
- 决赛：最多 10 队进 11 月决赛，需到场（面授或视频）才计奖
- 禁止：歧视、反民主、军事/武器、暴力美化

---

## 1. 七项评分标准逐条比对

### 1.1 Eigenständigkeit（独立性）— 🟡 需补支持披露文档（**最大缺口**）

| 官方要求 | 现状 | 证据 | 缺口 |
|---------|------|------|------|
| 自有贡献可辨识 | ✅ | LDS 原创指标、LLM-as-Subject 组内设计、设计效应证明 | — |
| 核心代码自行编写 | ✅ | `scripts/lds_c_*.py` 原创 | — |
| **AI 模型使用披露** | ❌ **缺失** | 用了 deepseek-v4-flash @ opencode GO 提取 + 分析 | **需在文档+提交中明确** |
| **AI 辅助工具披露** | ❌ **缺失** | 开发/分析用了 Claude Code | **需在文档中明确** |
| **数据集来源披露** | ⚠️ 部分 | Wikipedia（CC-BY-SA）、人类问卷（GDPR 知情同意）、数学教材 | **需汇总成清单** |
| 人员/机构披露 | ⚠️ 部分 | `docs/CONTRIBUTORS.md` 有工具清单 | **需更新至最新（含 API 端点）** |
| GPU/算力披露 | ✅ | 无外部算力（纯 API + 本地） | 写明即可 |

**结论**: `docs/CONTRIBUTORS.md` 列了开源工具，但**未披露 API 模型使用**。必须新增正式的支持披露章节——这直接关系到参赛资格。

### 1.2 Originalität（原创性）— ⭐ 9/10（最强项）

| 要求 | 现状 | 证据 |
|------|------|------|
| 原创指标 | ✅ | **LDS v3**（冻结，节点+边 Jaccard） |
| 原创设计 | ✅ | **LLM-as-Subject 组内设计**（同一权重集三语 → 语言是唯一变量） |
| 原创深化 | ✅ | **设计效应证明**（人类/LLM 信号幅度相同、底噪不同） |
| 填补空白 | ✅ | 13 篇 Crossref 验证文献确认空白（`research_directions_20260808.md`） |

**评委视角**: "语言驱动认知结构分歧"——用一个**受控被试**把不可检验的假说变成可检验的，这是方法学新意。

### 1.3 Schwierigkeitsgrad（难度）— 🟢 8/10（较 6/17 的 5/10 大幅提升）

| 维度 | 现状 |
|------|------|
| 真实数据 | ✅ N=15 人类（6DE+6ZH+3EN 双语）+ 220 LLM units + Wikipedia 96 词英文化 |
| 统计检验 | ✅ Bootstrap CI、split-half、标签置换、χ²、**LMM 混合效应**、置换检验 |
| 机制分解 | ✅ 五探针（P1/P2/P3/P5）+ LMM 代码层主导 |
| 交叉验证 | ✅ 语料侧（数学 vs 社会）+ 跨源空模型 + 敏感性全维度 |

**较旧版**: 从"无真实数据、无 p 值"到"完整证据链 + 设计效应证明"——难度维度已实质兑现。

### 1.4 Wissenschaftliches Arbeiten（科学方法论）— 🟢 8/10

| 要求 | 现状 | 证据 |
|------|------|------|
| 错误源分析 | ✅ | deepseek 推理爆炸踩坑、canonical_key 对齐伪影、Wikipedia LDS=1.0 伪影修复 |
| 嵌入前沿 | ✅ | 13 篇 Crossref 验证 DOI（Binz & Schulz 2023、Arora 2024 等） |
| 自评批判 | ✅ | **诚实阴性**（人类组间三层）、空模型反证框架、局限性章节 |
| 基线/对照 | ✅ | LDS-K vs LDS-C、Wikipedia 负对照、跨源空模型、设计效应 lens |

**较旧版**: 从"无实验结果可分析"到"阴性→阳性→机制→深化"完整科学流程。

### 1.5 Ausblick, Neuheit, Erkenntnisgewinn（展望/新颖/知识增益）— 🟢 8/10

| 要求 | 现状 |
|------|------|
| 知识增益 | ✅ **人类阴性是设计伪影**（信号幅度=LLM）；**代码层主导机制**；**制度抹平语言/文化暴露语言** |
| 方法学贡献 | ✅ 组间/组内对同一假说检测力差异（可发表） |
| 展望 | ✅ 人类组内设计蓝图（方向 A 提供必要性证据） |

### 1.6 Praktische Relevanz（实践相关性）— 🟢 7/10

| 应用 | 说明 |
|------|------|
| 多语言 AI 文化偏置 | LLM 三语输出概念结构分歧 → 多语 LLM 对齐/评测可测 |
| 跨文化教育 | 数学趋同/社会分歧 → 双语教学、教材比较 |
| 双语认知 | 双语者语言切换时的概念地图差异 |

**较旧版**: 从"定位未验证"到"多语 LLM 偏置评测"这一当下热点的具体落点。

### 1.7 Lesbarkeit und Struktur des Codes（代码质量）— 🟢 8/10

| 要求 | 现状 |
|------|------|
| 模块化 | ✅ `scripts/lds_c_*.py` 一脚本一功能 |
| 类型提示 | ✅ 全部有 type hints |
| 文档字符串 | ✅ 每脚本有 docstring |
| 可复现 | ✅ 交接 §4 有复现顺序，本轮 3 脚本已验证 |
| 测试 | ⚠️ `tests/` 有 pytest（test_v3_pipeline 等），但新脚本未覆盖 |

**建议**: 提交前跑 `pytest`，确认测试通过；为新脚本加冒烟测试。

---

## 2. 提交材料清单（三项 vs 现状）

| 材料 | 官方要求 | 当前状态 | 缺口 | 优先级 |
|------|---------|---------|------|--------|
| **文档（德文 PDF）** | 完整研究报告 | ✅ 分节齐备（00–07） | **❌ 未组装成 PDF**、无标题页/目录/参考文献/支持披露 | 🔴 P0 |
| **代码** | 可运行、方法=ML | ✅ 已验证可复现 | 需提交清单 + README 运行说明 | 🟡 P1 |
| **视频 2–4 分钟** | 非专家懂+专家评复杂度 | ⚠️ `video_script.md` 脚本过时 | **❌ 未录制**；脚本需更新至 LLM-as-Subject 新成果 | 🔴 P0 |

**视频脚本过时确认**: `docs/video_script.md` 不含 LLM-as-Subject 组内设计、设计效应证明——**必须重写后录制**。

---

## 3. Eigenständigkeit 支持披露（新规则硬性要求，**最紧迫合规项**）

根据官方条款，以下支持**必须**在文档中透明披露，否则取消资格：

| 支持类型 | 是否使用 | 披露内容 | 状态 |
|---------|---------|---------|------|
| **AI 模型（提取/分析）** | ✅ deepseek-v4-flash @ opencode GO | 模型名、端点、用途（概念/关系提取、Wikipedia 英文化、LLM-as-Subject 被试） | ❌ 未披露 |
| **AI 辅助工具（开发/写作）** | ✅ Claude Code | AI 辅助编码、数据分析、文档撰写 | ❌ 未披露 |
| 数据集来源 | ✅ 三源 | Wikipedia（CC-BY-SA）、人类问卷（GDPR 知情同意）、数学教材（版权注意） | ⚠️ 部分 |
| 人员/机构 | — | 无外部合作机构；自研究 | ✅ |
| 算力/GPU | ❌ | 纯 API + 本地 CPU（无外部算力） | ✅ 写明即可 |
| 视频音乐/素材 | ⏳ | 录制时若用授权音乐需署名 | 未开始 |

**必须新建**: `docs/declaration_of_support.md`（或并入论文附录），列出上述全部支持来源。

---

## 4. 与 2026-06-17 旧合规审查的差异（进步幅度）

| 维度 | 6/17（创意阶段） | 现在（8/8） | 变化 |
|------|:---:|:---:|:---:|
| 真实实验数据 | ❌ 0 名被试 | ✅ N=15 + 220 LLM units | 🔥 填平 |
| 统计检验 | ❌ 无 | ✅ LMM + Bootstrap + 置换 | 🔥 填平 |
| 错误分析 | ❌ 无 | ✅ 3 类伪影 + 深坑记录 | 🔥 填平 |
| 研究完成度 | 15% | ~90% | 🔥 |
| 支持披露 | ❌ 缺 | ❌ **仍缺** | ⚠️ 唯一未动项 |
| 视频 | ❌ | ⚠️ 脚本有但过时 | 🔧 |
| 文档 PDF | ❌ | ❌ | 🔧 |

**结论**: 科学研究维度已从 15% → 90% 全面兑现；**剩下的工作集中在"提交工程"**（披露文档、PDF 组装、视频录制）而非研究本身。

---

## 5. 剩余工作清单（按优先级，9/20 截止）

### P0 — 合规与提交（红线）
- [x] **新建 `docs/declaration_of_support.md`**：披露 AI 模型（deepseek）、AI 辅助工具（Claude Code）、数据集来源、人员、算力 → 并入论文附录（2026-08-08 ✅）
- [x] **更新 `docs/CONTRIBUTORS.md`**：补 API 模型与辅助工具（2026-08-08 ✅）
- [ ] **论文组装 PDF**：标题页 + 目录 + 参考文献 + 支持披露附录（德文）— ⚠️ 工具链决策待定（见 `docs/submission/einreichung_checkliste.md`）
- [x] **重写视频脚本**（2026-08-09 v2，AI-Audit-Framing：LLM-as-Subject + 设计效应证明 + 应用场景）→ **录制 2–4 分钟（未录）**

### P1 — 代码与数据
- [ ] 运行 `pytest`，修复失败，为新脚本加冒烟测试
- [ ] 提交代码清单 + README 运行说明（复现顺序）
- [ ] manifest 数字口径对齐（556/557、219/247）——A0 遗留

### P2 — 内容收尾
- [ ] 论文格式审查（字数、图表、参考文献一致性）
- [ ] A6 模拟基线调和（§4.8 已标注方法上不再成立，可标注为历史）

---

## 6. 提交叙事（2026-08-09 定版：AI-Audit-Framing）

> **决策记录（2026-08-09）**: 针对"项目不实用/不直观/缺应用场景"的担忧，经三方案评估（A 多语言 AI 价值观审计 / B 跨文化本地化 / C 纯学术）选定 **A**。理由：证据支撑最强（LLM 信号 + 分歧驱动者 + 领域不对称全支撑）、实用性强（AI 对齐/监管审计）、直观（一句话讲懂）。对外叙事统一为 AI-Audit-Framing；学术严谨性保留在方法/结果章。

**一句话（评委视角）**: "LinguaGraph 是给多语言 AI 做价值观一致性审计的工具：它测量一个模型是否在语言之间漂移地理解公平、自由、责任等概念——并精确定位分歧发生在哪个概念组件。用 LLM 本身做受控被试。"

**三层展开**:
1. **问题**: 多语言 AI 主要用英语训练 → 跨语言价值一致性无人测量（评价盲区，EU AI Act 透明度需求）
2. **方法 + 证据**: LLM-as-Subject 组内设计（LDS-C 0.93–0.96 ≫ 底噪 0.85–0.87，p<0.01）→ 文化性（DE 自主/规则 vs ZH 空间/应得）→ 领域对照（制度趋同/文化暴露 = 非伪影）→ 异质性注入直接因果证明
3. **应用**: 可解释的分歧报告（LDS-C + 分歧组件 + 领域）→ 开发者/监管者/研究者；诚实边界 = 单模型 PoC

**学术版（Begutachtungsunterlagen）**: 保留在 `00_three_conclusions.md`「学术版」与论文正文。

---

## 7. 数据血缘

| 资产 | 位置 |
|------|------|
| 论文分节（德文） | `docs/paper/00`–`07` |
| 视频脚本（过时） | `docs/video_script.md` |
| 支持工具清单（需更新） | `docs/CONTRIBUTORS.md` |
| 旧合规审查（已过时） | `docs/bwki-compliance-review.md` |
| 交接（研究状态） | `docs/session_handoff_20260808.md`（v0.9） |
