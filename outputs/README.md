# LinguaGraph — 结果目录 / Outputs Directory / Ergebnisverzeichnis

> **用途**: 存放论文级别的结果数据、图表和统计报告  
> **Purpose**: Store publication-grade result data, figures, and statistical reports  
> **Zweck**: Aufbewahrung von ergebnisrelevanten Daten, Abbildungen und statistischen Berichten auf Publikationsniveau  
> **状态**: ⏳ 等待人类实验数据  
> **Status**: ⏳ Awaiting human experiment data  
> **Status**: ⏳ Warte auf menschliche Experimentdaten

---

## 目录结构 / Directory Structure / Verzeichnisstruktur

| 路径 / Path | 内容 / Content / Inhalt | 状态 / Status |
|-------------|------------------------|--------------|
| `figure_templates.md` | 5 张论文图表的规格说明 / Specs for 5 publication figures / Spezifikationen für 5 Publikationsabbildungen | ✅ 已准备 / Ready / Bereit |
| `paper_results_template.md` | 结果表格模板 / Result table templates (Table 1-4, Figure 1-5) / Vorlagen für Ergebnistabellen | ✅ 已准备 / Ready / Bereit |
| `hypothesis_results_template.md` | 假设检验框架 (H1-H5) / Hypothesis testing framework (H1-H5) / Hypothesentest-Rahmenwerk (H1-H5) | ✅ 已准备 / Ready / Bereit |
| `findings/` | 语料分析发现 (Pilot 阶段) / Corpus analysis findings (Pilot phase) / Korpusanalyse-Erkenntnisse (Pilotphase) | ✅ 已有 / Available / Vorhanden |

## 数据来后的处理流程 / Data Processing Pipeline / Datenverarbeitungspipeline

```bash
# 1. 导入数据 / Import data / Daten importieren
python participant_data/import.py --input raw/survey_export.csv

# 2. 匿名化 / Anonymize / Anonymisieren
python participant_data/anonymize.py --batch pilot_001

# 3. 批量运行 Pipeline / Batch run pipeline / Pipeline im Batch ausführen
python scripts/analyze_student.py --all

# 4. 生成论文图表 / Generate publication figures / Publikationsabbildungen generieren
python scripts/bwki_analysis.py --all-figures

# 5. 概念提取评估 / Concept extraction evaluation / Konzeptextraktion evaluieren
python evaluation/extractor_benchmark.py --all

# 6. 标注一致性 / Annotator agreement / Annotator-Übereinstimmung
python scripts/annotator_agreement.py
```

## 输出产物 / Output Artifacts / Ausgabeerzeugnisse

### 图表 / Figures / Abbildungen

| 编号 / ID | 内容 / Content / Inhalt | 格式 / Format |
|-----------|------------------------|--------------|
| Figure 1 | LDS 跨语言分布 / Cross-lingual LDS distribution / Sprachübergreifende LDS-Verteilung | PNG |
| Figure 2 | CDS 学段对比 / CDS across education levels / CDS über Bildungsstufen | PNG |
| Figure 3 | 概念重叠图 / Concept overlap Venn diagram / Konzeptüberschneidungs-Venn-Diagramm | PNG |
| Figure 4 | 认知图谱对比 / Cognitive graph comparison / Kognitiver Graphenvergleich | PNG |
| Figure 5 | CognitiveSpace 全景 / CognitiveSpace overview / CognitiveSpace-Übersicht | PNG |

### 表格 / Tables / Tabellen

| 编号 / ID | 内容 / Content / Inhalt |
|-----------|------------------------|
| Table 1 | 参与者人口统计 / Participant demographics / Teilnehmerdemografie |
| Table 2 | LDS 语言配对结果 / LDS by language pair / LDS nach Sprachpaar |
| Table 3 | CDS/HDS 学段分析 / CDS/HDS by level / CDS/HDS nach Bildungsstufe |
| Table 4 | 假设检验结果 / Hypothesis test results / Hypothesentestergebnisse |

---

*最后更新 / Last updated / Letzte Aktualisierung: 2026-06-21*
