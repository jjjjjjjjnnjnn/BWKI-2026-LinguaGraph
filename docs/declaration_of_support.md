# 支持披露声明 — Declaration of Support — Erklärung der Unterstützung

> **版本**: 2.0 | **最后更新**: 2026-08-10（提交前将复核重定日期）
> **依据**: BWKI 2026 Teilnahmebedingungen「Eigenständigkeit」条款（Stand 28.04.2023）
> **作用**: 本文件按竞赛规则透明、完整披露本项目使用的全部外部支持来源。**此文件必须随书面文档提交。**
> **v1.0 → v2.0 变更**: 补全全部 AI 提供方（opencode zen / OpenRouter / DashScope）、55 模型复制实验、提取=被试模型的方法学选择、一次第三方 API 欠费事件；修正提取 F1 数字归属。

---

## 0. 总声明（Zusicherung）

本项目（LinguaGraph）由参赛学生独立完成核心科学工作：研究问题提出、实验设计、LDS 指标定义、数据收集方案、结果解释与结论。下述支持来源均已透明披露，未隐瞒任何形式的协助。

All core scientific work — research questions, experimental design, the LDS metric definition, data collection protocol, result interpretation, and conclusions — was carried out independently by the student participant. All forms of support are transparently disclosed below.

---

## 1. AI 模型使用（Nutzung von KI-Modellen）

本项目使用大语言模型（LLM）承担**两种明确区分的角色**：

**(1) 作为提取工具**（把文本转为概念图）：用于人类问卷、Wikipedia 语料的概念/关系提取。

**(2) 作为实验被试（LLM-as-Subject 组内设计）**：这是本研究的**核心科学方法**——同一（或不同）模型分别用 ZH/DE/EN 回答 5 个社会主题，检验"语言驱动认知结构分歧"假说。这符合 Binz & Schulz (2023, *PNAS*) 确立的 LLM-as-Subject 范式。**被试模型的回答与提取均在论文中作为受控实验呈现，非隐藏辅助。**

### 1.1 使用的模型与提供方（全部）

| 提供方/端点 | 模型 | 用途 |
|------|------|------|
| **opencode GO**（`https://opencode.ai/zen/go/v1`） | deepseek-v4-flash | 基线被试（D1 主实验）· 概念/关系提取 · gloss 英文化 |
| **opencode zen/v1**（`https://opencode.ai/zen/v1`） | deepseek-v4-flash、nemotron-3-ultra-free（NVIDIA）、mimo-v2.5-free、laguna-s-2.1-free、longcat-2.0-free 等 | 多模型复制被试 |
| **OpenRouter**（`https://openrouter.ai/api/v1`，免费层） | gpt-oss-20b:free（部分收集）、nemotron/laguna/gemma 等免费模型 | 多模型复制被试（部分未完成） |
| **阿里云 DashScope/千问**（`https://dashscope.aliyuncs.com/compatible-mode/v1`） | deepseek-v3/v3.1/v3.2/v4/r1 族、GLM-4.5~5.2、Kimi、MiniMax、Qwen3.x 等 **42 个模型** | 多模型复制被试 |

**多模型复制实验（51 个条目：50 完整 + qwen-max 部分）**: 2026-08-09/10，在完全相同的 P1 协议（3 语言 × k=10）下，对 42 个 DashScope 模型 + 7 个 zen/OpenRouter 模型 + D1 基线运行 LLM-as-Subject。**2026-09-09/10 西方扩展（同协议，全完整）**: gpt-oss-20b（NVIDIA NIM）、command-a-03-2025（Cohere）、laguna-s-2.1 + nemotron-3-super（Kilo）、gpt-5.6-luna（opencode 终端）→ **55 个完整测量 / 50 个唯一模型**，全部 ZH-DE 显著。**所有模型均作为受控被试被测量**，其回答与提取构成了论文的数据主体（`data/lds_c/llm_subject/`）。这是研究数据，不是"辅助完成工作"。

### 1.2 提取质量与 F1 数字（修正 v1 混用）

- **人工标注验证 F1（社会概念提取）**: ZH 0.974 / DE 0.949 / EN 0.882，总体约 **0.94**（72 个社会概念黄金标注）——这是"提取器能否恢复人工标注概念"的验证。
- **19 模型提取基准**: 多模型概念提取 F1 范围 **0.55–0.67**（`data/model_comparison/`）——用于模型选择，非论文声称值。
- **v1 错误**: v1 将两者混为单一"0.939（19 模型 benchmark）"，已修正。论文 §8.7/§8.9 分别对应上述两组数字。

### 1.3 方法学选择披露：提取模型 = 被试模型

多模型复制中，**每个被试模型自行提取其回答中的概念**（`lds_c_llm_subject.py` 两阶段：回答 → 同模型提取）。这是刻意保持"同一模型的概念结构"一致性的选择，但也意味着"测得的跨语言分歧"包含模型各语言下的提取行为差异。论文 §4.x 已披露此混淆；提取密度与分歧余量无相关（corr −0.23），且领域对照（制度趋同/文化分歧）提供部分缓解。

### 1.4 空结果与重试

- 空结果显式重试（每消息最多 3 次）；连续 3 个失败单元自动弃用该模型（`LDS_ABORT_AFTER`）
- 基线 D1 实验 220/220 单元完整；多模型收集按单元断点续跑

---

## 2. AI 辅助工具使用（Nutzung KI-basierter Hilfsmittel）

| 工具 | 用途 | 参与程度 |
|------|------|---------|
| **Claude Code**（Anthropic） | 辅助编程、数据分析脚本编写、文档撰写、代码审查、**本审查/修复过程** | 核心代码/分析脚本由 Claude Code 协助生成与调试；研究设计与结论由参赛学生主导 |

**说明**: Claude Code 作为 AI 编程助手参与了脚本开发、数据分析和文档排版。**科学判断、实验设计决策、结论解释由参赛学生独立完成**。按竞赛规则透明披露。

---

## 3. 数据集来源（Datensatzquellen）

| 数据集 | 来源 | 许可 | 用途 |
|--------|------|------|------|
| 人类问卷回答（N=15） | 自行收集（2026-07 在线问卷） | 参赛者自有数据；参与者知情同意（`docs/ethics/consent_{de,en,zh}.md`），GDPR 合规 | 人类认知表达分析（组间设计） |
| Wikipedia 文章（ZH/EN/DE，5 社会主题） | Wikipedia | **CC-BY-SA**（须署名） | 社会文化知识对照（负对照/语料深化） |
| 数学教材知识结构 | 中/德/英课程教材 | 概念图为其结构描述，非原文复制 | 制度知识对照（LDS-K） |

### Wikipedia 署名（CC-BY-SA 合规）
本项目从 Wikipedia 提取了 5 个社会主题（Freiheit/Gerechtigkeit/Verantwortung/Heimat/Erfolg）的三语概念结构。按 CC-BY-SA 要求，此处列出来源文章：
- 每个主题的提取文件 `data/wikipedia_extractions/{topic}_{lang}.json` 含 `source_url` 字段，记录了具体文章链接。
- **提交时**：论文参考文献需按各文件 `source_url` 列出对应 Wikipedia 文章及提取日期（2026-08-08）。

---

## 4. 人员与机构（Personen und Institutionen）

| 参与方 | 角色 | 说明 |
|--------|------|------|
| 参赛学生 | 项目负责人、研究者 | 独立完成研究设计、数据收集、结果解释 |
| 学校（德国高中） | 提供环境 | 无科研内容介入 |
| 其他团队/机构 | 无 | 无外部科研合作机构 |

---

## 5. 算力、基础设施与第三方 API 计费（Rechenleistung und Infrastruktur）

| 项目 | 说明 |
|------|------|
| 计算资源 | **本地 CPU**（Python 分析脚本）+ **第三方 LLM API** |
| GPU | **未使用**外部 GPU 算力 |
| 第三方 API 计费 | opencode GO（按量付费）、DashScope（免费额度 + 一次欠费）、OpenRouter（免费层）、opencode zen/v1（免费层） |

### 5.1 第三方 API 计费事件（诚实披露）

2026-08-10，在一次 DashScope 批量收集中，**因误用非免费额度模型导致账号短暂欠费并触发账户封锁**。问题当天发现：改用**仅免费额度模型**后继续收集，并在结清欠费后恢复。此事已如实记录于本项目内部交接文档（`docs/session_handoff_20260810.md` §3.3）。**此事件不影响研究数据有效性**（已收集数据经校验），但为完整透明，特此披露。

---

## 6. 版权与音乐（Urheberrecht / 视频素材）

- 提交视频将仅使用项目自制画面与系统生成内容。
- 若视频中引用任何有版权音乐或影像，将在视频描述中**列出作者/权利方及链接**（按规则要求）。
- 本项目 LDS 定义、问卷、实验设计均为原创（论文中引用相关文献）。

---

## 7. 自查与合规确认（Compliance Check）

| 规则要求 | 状态 |
|---------|------|
| AI 模型使用披露 | ✅ 本文件 §1（含全部提供方 + 55 模型复制 + 提取=被试选择） |
| AI 辅助工具披露 | ✅ 本文件 §2 |
| 数据集来源披露 | ✅ 本文件 §3 |
| 人员/机构披露 | ✅ 本文件 §4 |
| 算力/基础设施披露 | ✅ 本文件 §5（含 API 计费事件） |
| 视频版权素材署名 | ⏳ 录制时执行 |
| EU AI Act 合规 | ✅ LLM 用于研究分析，无受限用途（禁止深度伪造等） |
| 无歧视/反民主/军事内容 | ✅ 不适用 |

---

*本文件随书面文档提交。任何遗漏的辅助来源将于提交前补充更新。*
