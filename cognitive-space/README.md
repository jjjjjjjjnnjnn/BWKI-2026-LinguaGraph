# CognitiveSpace

> **跨语言数学知识图谱 — 从小学数学到偏微分方程。**
> **Cross-lingual mathematics knowledge graph — from elementary arithmetic to partial differential equations.**  
> **Mehrsprachiger Mathematik-Wissensgraph — von der Grundschule bis zu partiellen Differentialgleichungen.**

3D interactive knowledge graph covering the complete mathematics concept network.  
3D-interaktiver Wissensgraph, der das gesamte mathematische Konzeptnetz abdeckt.

---

## 数据 / Data / Daten

| 指标 / Metric | 值 / Value |
|--------|-------|
| 概念 / Concepts / Konzepte | **574** (557 unique, 17 aligned) |
| 关系 / Relations / Beziehungen | **525** (known) + **~3000** (inferred) |
| 教材 / Textbooks / Lehrbücher | **68** (45 ZH / 20 EN / 10 DE) |
| 课程体系 / Curricula / Lehrpläne | 人教版 · IB · AP · IGCSE · Abitur · Khan Academy |
| 学段 / Levels / Stufen | 小学 → 大学 / Elementary → University |
| 结构冲突 / Structural conflicts | **0** |
| 孤立节点 / Isolated nodes | **2** (<0.5%) |

## 学段 / Levels / Bildungsstufen

| 学段 / Level | 概念数 / Concepts | 颜色 / Color |
|-------|----------|-------|
| 小学 / Elementary / Grundschule | 37 | `#10b981` 绿色 / Green |
| 初中 / Middle / Mittelschule | 46 | `#14b8a6` 青色 / Teal |
| 高中 / High / Oberstufe | 193 | `#4a7dff` 蓝色 / Blue |
| 大学 / College / Universität | 298 | `#8b5cf6` 紫色 / Purple |

## 语言覆盖 / Language Coverage / Sprachabdeckung

| 语言 / Language | 覆盖率 / Coverage |
|----------|----------|
| 中文 / Chinese / Chinesisch | 335 (58%) |
| 英语 / English / Englisch | 392 (68%) |
| 德语 / German / Deutsch | 341 (59%) |
| 三语完整 / Trilingual / Dreisprachig | 247 (43%) |

## 快速开始 / Quick Start

在浏览器中打开 `web/index.html` — 无需服务器。  
Open `web/index.html` in any browser — no server required.  
`web/index.html` in einem Browser öffnen — kein Server erforderlich.

## 数据管线 / Pipeline

```
教材文本 / Textbook text / Lehrbuchtext
    ↓ (MIMO LLM 提取 / Extraction / Extraktion)
结构化 JSON / Structured JSON
    ↓ merge_extractions.py (合并 + 去重 / merge + deduplicate / Zusammenführen + Deduplizieren)
    ↓ align_languages.py (ZH/EN/DE 对齐 / alignment / Abgleich)
    ↓ export_graph.py (可视化数据 / visualization data / Visualisierungsdaten)
web/index.html + data.js
```

## 教材来源 / Textbook Sources / Lehrbuchquellen

**中文**: 人教版 K-12, 同济大学（微积分、线性代数）  
**英语**: Stewart *Calculus*, MIT OCW, Strang *Linear Algebra*, Khan Academy  
**德语**: Forster *Analysis*, Fischer *Lineare Algebra*, Papula, Lambacher Schweizer

## 许可协议 / License / Lizenz

提取数据: CC-BY-SA（教育用途）。教材引用: 合理使用。  
Extracted data: CC-BY-SA (educational use). Textbook citations: fair use.  
Extrahierte Daten: CC-BY-SA (Bildungszwecke). Lehrbuchzitate: Fair Use.

## 引用 / Citation

BWKI 2026 LinguaGraph 项目的一部分。  
Part of the BWKI 2026 LinguaGraph project.  
Hauptrepository: [BWKI-2026-LinguaGraph](https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph)
