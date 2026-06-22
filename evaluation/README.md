# LinguaGraph — 评估框架 / Evaluation Framework / Evaluierungsrahmen

> **目的**: 对比不同概念提取方法的 F1，建立标准化评测基准  
> **Purpose**: Compare F1 scores of different concept extraction methods, establish standardized evaluation benchmarks  
> **Zweck**: F1-Werte verschiedener Konzeptextraktionsmethoden vergleichen, standardisierte Evaluierungsbenchmarks erstellen  
> **原则**: 不修改核心 Pipeline，只做外部对比评估  
> **Principle**: Do not modify core pipeline, only perform external comparative evaluation  
> **Prinzip**: Kern-Pipeline nicht verändern, nur externe Vergleichsevaluierung durchführen  
> **基于**: ConceptNet 关系分类法 + CoCo-Ex 提取基线  
> **Based on**: ConceptNet relation taxonomy + CoCo-Ex extraction baseline  
> **Basiert auf**: ConceptNet-Beziehungstaxonomie + CoCo-Ex-Extraktionsbaseline

---

## 评测目标 / Evaluation Goals / Evaluierungsziele

| 维度 / Dimension | Keyword | CoCo-Ex | LLM (LinguaGraph) |
|------------------|:-------:|:-------:|:-----------------:|
| 概念提取 F1 / Concept Extraction F1 | ⬜ | ⬜ | ⬜ |
| 关系提取 F1 / Relation Extraction F1 | — | — | ⬜ |
| 多语言支持 / Multilingual Support | ✅ | ❌ EN only | ✅ ZH/DE/EN |
| 速度 / Speed | ✅ Fast | 🟡 Medium | ❌ API required |
| 可离线 / Offline Capable | ✅ | ✅ | ❌ |

## 使用方法 / Usage / Verwendung

```bash
# 对比所有提取器 / Compare all extractors / Alle Extraktoren vergleichen
python evaluation/extractor_benchmark.py

# 只跑 LLM 提取器 / Run only LLM extractor / Nur LLM-Extraktor ausführen
python evaluation/extractor_benchmark.py --extractor llm

# 只跑 CoCo-Ex 基线 / Run only CoCo-Ex baseline / Nur CoCo-Ex-Baseline ausführen
python evaluation/extractor_benchmark.py --extractor cocoex

# 指定语言 / Specify language / Sprache angeben
python evaluation/extractor_benchmark.py --lang zh
```

## 数据集 / Dataset / Datensatz

使用 `data/gold/gold_dataset.json` 中的 20 条人工标注数据作为 Ground Truth。  
Uses 20 human-annotated entries from `data/gold/gold_dataset.json` as ground truth.  
Verwendet 20 manuell annotierte Einträge aus `data/gold/gold_dataset.json` als Ground Truth.

## 指标说明 / Metrics / Metriken

| 指标 / Metric | 说明 / Description / Beschreibung |
|-------------|------|
| **Precision** | 提取的概念中正确比例 / Proportion of correctly extracted concepts / Anteil korrekt extrahierter Konzepte |
| **Recall** | 应提取概念中被正确提取的比例 / Proportion of expected concepts that were extracted / Anteil der erwarteten Konzepte, die extrahiert wurden |
| **F1** | Precision 与 Recall 的调和平均 / Harmonic mean of Precision and Recall / Harmonisches Mittel aus Precision und Recall |
| **Relation F1** | 关系提取的 F1 分数 / F1 score for relation extraction / F1-Wert für Relationsextraktion |

---

*BWKI 2026 · LinguaGraph · Evaluierungsrahmen*
