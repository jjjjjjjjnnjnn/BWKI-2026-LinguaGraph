# LinguaGraph — 人类数据管线 / Human Data Pipeline / Datenverarbeitungspipeline für menschliche Daten

> **目的**: 标准化处理人类实验数据  
> **Purpose**: Standardized processing for human experiment data  
> **Zweck**: Standardisierte Verarbeitung menschlicher Experimentdaten  
> **设计原则**: 匿名化 → 提取 → 图谱 → LDS → 报告，每一步可审计  
> **Design principle**: Anonymize → Extract → Graph → LDS → Report, every step auditable  
> **Gestaltungsprinzip**: Anonymisieren → Extrahieren → Graph → LDS → Bericht, jeder Schritt prüfbar

---

## 目录结构 / Directory Structure / Verzeichnisstruktur

```
participant_data/
├── raw/                  ← 原始数据（包含个人信息） / Raw data (contains PII) / Rohdaten (enthält personenbezogene Daten)
│   └── pilot_mock.csv    ← 9 条模拟回答 (3 ZH, 3 DE, 3 EN) / 9 mock responses / 9 simulierte Antworten
├── anonymized/           ← 匿名化数据 / Anonymized data (PII removed) / Anonymisierte Daten (ohne personenbezogene Daten)
│   └── {batch}.jsonl
├── annotations/          ← 人工标注 / Human annotation / Manuelle Annotation
│   ├── annotator_A/
│   ├── annotator_B/
│   └── consensus/
├── graphs/               ← 个体认知图谱 (JSON) / Individual cognitive graphs / Individuelle kognitive Graphen
├── reports/              ← 分析报告 / Analysis reports / Analyseberichte
├── participant_manager.py ← 参与者生命周期管理 / Participant lifecycle management / Teilnehmerlebenszyklus-Verwaltung
└── README.md
```

## 数据流程 / Data Flow / Datenfluss

```
Google Forms / 问卷平台 / Umfrageplattform
    ↓ CSV export / CSV 导出 / CSV-Export
raw/{batch}_export.csv
    ↓ participant_manager.py import / 导入 / Import
linguaGraph.db (students + responses 表 / tables / Tabellen)
    ↓ participant_manager.py export-anonymized / 导出匿名化数据 / anonymisierte Daten exportieren
anonymized/{batch}.jsonl
    ↓ survey_pipeline/annotate.py (LLM 提取 / extraction / Extraktion)
linguaGraph.db (extractions 表 / table / Tabelle)
    ↓ survey_pipeline/run_lds.py
linguaGraph.db (cross_language_analysis 表 / table / Tabelle)
    ↓ survey_pipeline/generate_report.py
docs/survey_reports/
```

## 快速开始 / Quick Start / Schnellstart

```bash
# 1. 查看招募进度 / Check recruitment status / Rekrutierungsstatus prüfen
python participant_data/participant_manager.py status

# 2. 添加参与者 / Add a participant / Teilnehmer hinzufügen
python participant_data/participant_manager.py add --id S001 --lang zh --consent

# 3. 列出所有参与者 / List all participants / Alle Teilnehmer auflisten
python participant_data/participant_manager.py list

# 4. 从 CSV 导入 (Google Forms 导出) / Import from CSV / Aus CSV importieren
python survey_pipeline/run_all.py raw/survey_export.csv --mock

# 5. 导出匿名化数据 / Export anonymized data / Anonymisierte Daten exportieren
python participant_data/participant_manager.py export-anonymized --batch pilot_001

# 6. 运行完整管线 (导入 → 提取 → LDS → 报告) / Run full pipeline / Vollständige Pipeline ausführen
python survey_pipeline/run_all.py participant_data/raw/pilot_mock.csv --mock
```

## 参与者管理 API / Participant Manager API

```python
from participant_data.participant_manager import ParticipantManager

pm = ParticipantManager()

# CRUD 操作 / Operations / Operationen
pm.add_participant("S001", native_lang="zh", consent=True)
pm.get_participant("S001")
pm.list_participants(native_lang="zh")
pm.update_consent("S001", consent=True)
pm.delete_participant("S001")  # GDPR Art. 17 / 删除权 / Recht auf Löschung

# 状态查询 / Status / Statusabfrage
pm.get_recruitment_status()  # 30 名参与者的招募进度 / Progress toward 30 participants / Fortschritt zu 30 Teilnehmern
pm.get_response_status()     # 每位参与者的回答完成情况 / Response completion per participant / Antwortstatus pro Teilnehmer

# 匿名化 / Anonymization / Anonymisierung
pm.export_anonymized(batch_id="pilot_001")

pm.close()
```

## GDPR 合规 / GDPR Compliance / DSGVO-Konformität

| 阶段 / Stage / Stufe | 数据 / Data / Daten | 存储 / Storage / Speicherung | 保留期限 / Retention / Aufbewahrungsfrist |
|---------------------|--------------------|----------------------------|-----------------------------------------|
| raw/ | 姓名、邮箱、IP、回答 / Name, email, IP, answers / Name, E-Mail, IP, Antworten | 加密，`.gitignore` / Encrypted / Verschlüsselt | 分析后销毁 / Destroyed after analysis / Nach Analyse vernichtet |
| anonymized/ | 年龄、语言、回答 / Age, language, answers / Alter, Sprache, Antworten | 纯文本，`.gitignore` / Plain text / Klartext | 研究后归档 / Archived after study / Nach Studie archiviert |
| annotations/ | 标注结果 / Annotation results / Annotationsergebnisse | 纯文本 / Plain text / Klartext | 永久保留（研究记录） / Permanent (research record) / Dauerhaft (Forschungsunterlagen) |
| graphs/ | 匿名化认知图谱 / Anonymized cognitive graphs / Anonymisierte kognitive Graphen | 纯文本 / Plain text / Klartext | 永久保留（研究记录） / Permanent (research record) / Dauerhaft (Forschungsunterlagen) |

## 相关模块 / Related Modules / Verwandte Module

| 模块 / Module / Modul | 用途 / Purpose / Zweck |
|----------------------|--------|
| `survey_pipeline/import_csv.py` | CSV → 数据库导入 / CSV → database import / CSV → Datenbankimport |
| `survey_pipeline/annotate.py` | LLM 概念提取 / LLM concept extraction / LLM-Konzeptextraktion |
| `survey_pipeline/run_lds.py` | LDS 计算 / LDS computation / LDS-Berechnung |
| `survey_pipeline/generate_report.py` | 报告生成 / Report generation / Berichtserstellung |
| `scripts/survey_entry.py` | CLI 手动数据录入 / CLI manual data entry / CLI manuelle Dateneingabe |
| `scripts/db_utils.py` | 数据库工具 / Database utilities / Datenbank-Dienstprogramme |

---

*BWKI 2026 · LinguaGraph · 人类数据管线 / Human Data Pipeline / Datenverarbeitungspipeline für menschliche Daten*
