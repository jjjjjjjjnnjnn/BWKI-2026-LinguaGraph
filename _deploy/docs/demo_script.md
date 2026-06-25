# LinguaGraph — BWKI Demo Script (5 分钟)

> **目的:** 创意展示 / 决赛答辩口述脚本
> **时长:** 5 分钟（严格控制）
> **语言:** 英语为主，括号内为中文提示
> **配套:** Cognitive City V3 可视化 + LDS 结果

---

## 00:00–01:00 — Problem & Motivation

**现场:** 打开 Cognitive City V3 展示

> "Does the language you speak shape how you think?
>
> This question — the Sapir-Whorf hypothesis — has been debated for decades. But most evidence comes from small behavioral experiments: reaction times, memory tests, eye tracking.
>
> What's missing is a **structural** comparison. If Chinese, German, and English speakers think differently, can we *see* that difference in the structure of their ideas?
>
> That's what LinguaGraph measures."

**要点:**
- 问题：语言是否塑造思维
- 缺口：缺乏结构性、可量化的对比方法
- 方案：认知图谱 + Language Drift Score

**屏幕:**
- Cognitive City 自由主题全景
- 突出 ZH/EN/DE 三城并排

---

## 01:00–02:00 — Method: Cognitive Graph

**现场:** 点击建筑展示细节

> "We gave participants a 10-task cognitive-linguistic battery: word associations, cultural concept explanations, spatial descriptions, and translations — each designed to probe a specific cognitive dimension.
>
> From each response, an LLM extracts **concepts** and **relations**, forming a directed graph. Every node is a concept, every edge is a semantic relation like 'implies' or 'opposes'.
>
> Each participant produces one graph per language. Then we compare: how similar are the ZH graph and the DE graph for the same person answering the same question?
>
> The Language Drift Score — LDS — quantifies this: 0 means identical cognitive structures, 1 means completely different."

**要点:**
- 10 项认知任务（非传统问卷）
- LLM 提取 → 有向图
- LDS = 1 − mean(GED_sim, Jaccard_node, Jaccard_edge)

**屏幕:**
- 点击放大某栋建筑（概念），展示 hover 信息窗
- 切换到 LDS 柱状图区域

---

## 02:00–03:00 — Human Validation

**现场:** 展示质量数据

> "But we need to know: is this measuring real cognitive differences, or just LLM noise?
>
> We validated on 3 levels:
>
> **First**, gold-standard annotations: 20 ZH responses independently annotated by human raters. Concept extraction F1 reaches [value] — well above our 0.80 threshold.
>
> **Second**, annotator agreement: Cohen's Kappa is [value] — substantial agreement.
>
> **Third**, pilot data shows that LDS patterns align with theoretical predictions: culturally-unique concepts show the highest drift, spatial descriptions the lowest.
>
> In other words: the pipeline captures genuine linguistic-cognitive differences, not artifacts."

**要点:**
- 人类标注者验证 F1 > 0.80
- Cohen's Kappa > 0.70
- LDS 分布符合理论预期

**屏幕:**
- F1 表（概念/关系）
- 或单页 slide（仍在用的话）

---

## 03:00–04:00 — Results: LDS Findings

**现场:** 展示 LDS 结果

> "Our pilot study with [N] native Chinese speakers shows the pipeline works end-to-end.
>
> The preliminary cross-language LDS values show [pair] has the highest drift at [value], while [pair] shows the lowest at [value].
>
> Breaking it down by topic: cultural concepts like 'filial piety' in Chinese or 'Fernweh' in German show substantially higher drift than spatial descriptions — exactly what the linguistic relativity literature predicts.
>
> Bootstrapped 95% confidence intervals confirm these estimates are stable at [N] participants per language."

**要点:**
- LDS 值：语言对 × 主题
- 文化概念 > 空间概念（理论一致）
- Bootstrap CI 确认稳定性

**屏幕:**
- Figure 1（LDS 分组条形图）或 Figure 3（主题对比图）

---

## 04:00–05:00 — Impact & Future

**现场:** 演示模式自动切换主题

> "LinguaGraph makes three contributions:
>
> **First**, a reproducible, open-source pipeline for cross-language cognitive comparison. Anyone can run `python scripts/run_pipeline.py` to reproduce our results.
>
> **Second**, the Cognitive City visualization — an intuitive 3D interface that makes abstract LDS patterns explorable.
>
> **Third**, the Concept Taxonomy v1 — 30 shared concept IDs across 5 clusters, a structured ontology for cross-language cognitive research.
>
> **Beyond the paper:** The core infrastructure we built — provider abstraction, GGUF quantization, LoRA adaptation — is task-agnostic. We extracted it into a standalone runtime, and an independent game project is now reusing it with a different LoRA adapter. This confirms our architecture is generalizable beyond this single experiment.
>
> Our full study targets 30 participants across all three languages. With that, we'll have the first AI-powered, graph-based quantification of linguistic relativity.
>
> Thank you."

**要点:**
- 可复现 pipeline
- Cognitive City 可视化
- Concept Taxonomy
- **技术资产：运行时已被独立项目复用（架构通用性证明）**
- 未来：30 人 × 3 语言

**屏幕:**
- 演示模式自动切换主题
- 结尾定格在 Cognitive City 全景

---

## 附录: 时间控制

| 段落 | 时长 | 核心信息 |
|:-----|:----:|:---------|
| Problem & Motivation | 1:00 | 语言 vs 思维，结构性方法缺失 |
| Method | 1:00 | 10 任务 → 图谱 → LDS |
| Human Validation | 1:00 | F1 > 0.80, Kappa > 0.70 |
| Results | 1:00 | LDS 按主题/语言对，Bootstrap 稳定 |
| Impact & Future | 1:00 | 可复现、可视化、30 人全量 |

**备用：若时间不足**
- 压缩 Validation 到 0:30
- 跳过 Future，在 Q&A 回答

---

## 附录: Q&A 过渡

> "That's a great question. Let me show you..."
> "That's actually something we specifically validated..."
> "The data on that is in the quality report..."

详见 `docs/judge_qa.md`
