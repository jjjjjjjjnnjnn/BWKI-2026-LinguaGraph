# 支持披露声明 — Declaration of Support — Erklärung der Unterstützung

> **版本**: 1.0 | **日期**: 2026-08-08
> **依据**: BWKI 2026 Teilnahmebedingungen「Eigenständigkeit」条款（Stand 28.04.2023）
> **作用**: 本文件按竞赛规则透明、完整披露本项目使用的全部外部支持来源。**此文件必须随书面文档提交。**

---

## 0. 总声明（Zusicherung）

本项目（LinguaGraph）由参赛学生独立完成核心科学工作：研究问题提出、实验设计、LDS 指标定义、数据收集方案、结果解释与结论。下述支持来源均已透明披露，未隐瞒任何形式的协助。

All core scientific work — research questions, experimental design, the LDS metric definition, data collection protocol, result interpretation, and conclusions — was carried out independently by the student participant. All forms of support are transparently disclosed below.

---

## 1. AI 模型使用（Nutzung von KI-Modellen）

| 用途 | 模型 | 提供方/端点 | 说明 |
|------|------|-------------|------|
| 概念/关系提取（人类问卷 → 知识图） | deepseek-v4-flash | opencode GO（OpenAI 兼容端点，`https://opencode.ai/zen/go/v1`） | 将 15 份人类问卷回答按主题提取概念与关系，附英文 gloss |
| LLM-as-Subject 组内实验（D1） | deepseek-v4-flash | 同上 | **作为受控认知被试**：同一模型分别用 ZH/DE/EN 回答 5 个社会主题——语言是唯一变化量 |
| 自由联想英文化（P3） | deepseek-v4-flash | 同上 | 285 个联想词英文化，保证跨语言对齐 |
| Wikipedia 概念英文化 | deepseek-v4-flash | 同上 | 96 个 ZH+DE 概念英文化，修复对齐伪影 |

**关键说明**: LLM 在本项目中有**两种**不同角色——(1) 作为**提取工具**（把文本转为概念图）；(2) 作为**实验被试**（LLM-as-Subject 组内设计）。第二种是本研究的**核心科学方法**，不是隐藏的辅助：论文 §5 明确将其作为受控被试，检验"语言驱动认知结构分歧"假说。这符合 Binz & Schulz (2023, *PNAS*) 确立的 LLM-as-Subject 范式。

### 提取质量门控
- 概念提取 F1 达 0.939（19 模型 benchmark，`scripts/`）
- 全部空结果显式重试，0 空单元（220/220）
- deepseek 推理爆炸问题（`finish=length`）已记录于 `docs/session_handoff_20260808.md` §5

---

## 2. AI 辅助工具使用（Nutzung KI-basierter Hilfsmittel）

| 工具 | 用途 | 参与程度 |
|------|------|---------|
| **Claude Code**（Anthropic） | 辅助编程、数据分析脚本编写、文档撰写、代码审查 | 核心代码/分析脚本由 Claude Code 协助生成与调试；研究设计与结论由参赛学生主导 |

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

## 5. 算力与基础设施（Rechenleistung und Infrastruktur）

| 项目 | 说明 |
|------|------|
| 计算资源 | **本地 CPU**（Python 分析脚本）+ **第三方 LLM API**（opencode GO，按量付费） |
| GPU | **未使用**外部 GPU 算力 |
| 其他 | 无云集群、无外部提供的训练基础设施 |

---

## 6. 版权与音乐（Urheberrecht / 视频素材）

- 提交视频将仅使用项目自制画面与系统生成内容。
- 若视频中引用任何有版权音乐或影像，将在视频描述中**列出作者/权利方及链接**（按规则要求）。
- 本项目 LDS 定义、问卷、实验设计均为原创（论文中引用相关文献）。

---

## 7. 自查与合规确认（Compliance Check）

| 规则要求 | 状态 |
|---------|------|
| AI 模型使用披露 | ✅ 本文件 §1 |
| AI 辅助工具披露 | ✅ 本文件 §2 |
| 数据集来源披露 | ✅ 本文件 §3 |
| 人员/机构披露 | ✅ 本文件 §4 |
| 算力/基础设施披露 | ✅ 本文件 §5 |
| 视频版权素材署名 | ⏳ 录制时执行 |
| EU AI Act 合规 | ✅ LLM 用于研究分析，无受限用途（禁止深度伪造等） |
| 无歧视/反民主/军事内容 | ✅ 不适用 |

---

*本文件随书面文档提交。任何遗漏的辅助来源将于提交前补充更新。*
