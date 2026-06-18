# LinguaGraph — Human Validation Data Pipeline

> **Purpose**: Standardized processing for human experiment data
> **Design principle**: Anonymize → Extract → Graph → LDS → Report, every step auditable

---

## Directory Structure

```
participant_data/
├── raw/                  ← Raw data (from survey platform, contains PII)
│   └── pilot_mock.csv    ← 9 mock responses (3 ZH, 3 DE, 3 EN)
├── anonymized/           ← Anonymized data (PII removed, for analysis)
│   └── {batch}.jsonl
├── annotations/          ← Human annotation
│   ├── annotator_A/
│   ├── annotator_B/
│   └── consensus/
├── graphs/               ← Individual cognitive graphs (JSON)
├── reports/              ← Analysis reports
├── participant_manager.py ← Participant lifecycle management
└── README.md
```

---

## Data Flow

```
Google Forms / Survey Platform
    ↓ CSV export
raw/{batch}_export.csv
    ↓ participant_manager.py import (or survey_pipeline/import_csv.py)
linguaGraph.db (students + responses tables)
    ↓ participant_manager.py export-anonymized
anonymized/{batch}.jsonl
    ↓ survey_pipeline/annotate.py (LLM extraction)
linguaGraph.db (extractions table)
    ↓ survey_pipeline/run_lds.py
linguaGraph.db (cross_language_analysis table)
    ↓ survey_pipeline/generate_report.py
docs/survey_reports/
```

---

## Quick Start

```bash
# 1. Check recruitment status
python participant_data/participant_manager.py status

# 2. Add a participant
python participant_data/participant_manager.py add --id S001 --lang zh --consent

# 3. List all participants
python participant_data/participant_manager.py list

# 4. Import from CSV (Google Forms export)
python survey_pipeline/run_all.py raw/survey_export.csv --mock

# 5. Export anonymized data
python participant_data/participant_manager.py export-anonymized --batch pilot_001

# 6. Run full pipeline (import → extract → LDS → report)
python survey_pipeline/run_all.py participant_data/raw/pilot_mock.csv --mock
```

---

## Participant Manager API

```python
from participant_data.participant_manager import ParticipantManager

pm = ParticipantManager()

# CRUD
pm.add_participant("S001", native_lang="zh", consent=True)
pm.get_participant("S001")
pm.list_participants(native_lang="zh")
pm.update_consent("S001", consent=True)
pm.delete_participant("S001")  # GDPR Art. 17

# Status
pm.get_recruitment_status()  # Progress toward 30 participants
pm.get_response_status()     # Response completion per participant

# Anonymization
pm.export_anonymized(batch_id="pilot_001")

pm.close()
```

---

## GDPR Compliance

| Stage | Data | Storage | Retention |
|-------|------|---------|-----------|
| raw/ | Name, email, IP, answers | Encrypted, `.gitignore` | Destroyed after analysis |
| anonymized/ | Age, language, answers | Plain text, `.gitignore` | Archived after study |
| annotations/ | Annotation results | Plain text | Permanent (research record) |
| graphs/ | Anonymized cognitive graphs | Plain text | Permanent (research record) |

---

## Related Modules

| Module | Purpose |
|--------|---------|
| `survey_pipeline/import_csv.py` | CSV → database import |
| `survey_pipeline/annotate.py` | LLM concept extraction |
| `survey_pipeline/run_lds.py` | LDS computation |
| `survey_pipeline/generate_report.py` | Report generation |
| `scripts/survey_entry.py` | CLI manual data entry |
| `scripts/db_utils.py` | Database utilities |
