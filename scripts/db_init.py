"""
LinguaGraph Database Initialization
====================================
Creates SQLite database with all tables for the BWKI 2026 project.

Usage:
    python db_init.py              # Create database (safe, only adds new tables)
    python db_init.py --fresh      # Drop and recreate all tables
    python db_init.py --stats      # Print table statistics

Table Schema:
    - students:          Participant information
    - questionnaires:    Survey definitions (ZH/DE/EN)
    - responses:         Multi-language student answers
    - extractions:       LLM concept/relation extraction results
    - graphs:            NetworkX knowledge graphs (serialized)
    - gold_labels:       Human annotations (ground truth)
    - cross_language_analysis: Cross-language comparison results
    - evaluation_results: LLM extraction quality metrics
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# === Database Path ===
DB_DIR = Path(__file__).parent.parent  # project root (scripts/../)
DB_PATH = DB_DIR / "linguaGraph.db"


def get_connection() -> sqlite3.Connection:
    """Get a database connection with Row factory enabled."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # Better concurrent read performance
    conn.execute("PRAGMA foreign_keys=ON")    # Enforce referential integrity
    return conn


# ===== Schema Definition =====
# Each table gets its own CREATE statement for clarity.
# All tables use TEXT primary keys with human-readable IDs.

SCHEMA_SQL = """
-- Students: participant demographic & consent info
CREATE TABLE IF NOT EXISTS students (
    student_id      TEXT PRIMARY KEY,           -- "S001", "S002"...
    age_group       TEXT,                       -- "13-15", "16-18"
    native_lang     TEXT NOT NULL,              -- "zh" (native language)
    school_lang     TEXT NOT NULL,              -- "de" (school language)
    other_langs     TEXT,                       -- comma-sep, e.g. "en,fr"
    years_in_germany INTEGER,                   -- years lived in Germany
    consent         INTEGER DEFAULT 0,          -- 0/1 informed consent
    notes           TEXT,                       -- free-form researcher notes
    created_at      TEXT DEFAULT (datetime('now'))
);

-- Questionnaires: survey instruments per language
CREATE TABLE IF NOT EXISTS questionnaires (
    questionnaire_id TEXT PRIMARY KEY,          -- "social_issues_v1"
    title           TEXT NOT NULL,
    language        TEXT NOT NULL,              -- "zh", "de", "en"
    questions       TEXT NOT NULL,              -- JSON array of question objects
    version         TEXT DEFAULT '1.0',
    created_at      TEXT DEFAULT (datetime('now'))
);

-- Responses: the core multi-language student answers
CREATE TABLE IF NOT EXISTS responses (
    response_id     TEXT PRIMARY KEY,           -- "R001_zh_q1"
    student_id      TEXT NOT NULL REFERENCES students(student_id),
    questionnaire_id TEXT NOT NULL REFERENCES questionnaires(questionnaire_id),
    language        TEXT NOT NULL,              -- "zh", "de", "en"
    question_id     TEXT NOT NULL,              -- "q1", "q2", "q3", "q4"
    answer_text     TEXT NOT NULL,
    word_count      INTEGER,                    -- word/token count
    source          TEXT DEFAULT 'survey',      -- "survey", "interview", "manual"
    quality_flag    TEXT DEFAULT 'ok',           -- "ok", "short", "empty", "review"
    created_at      TEXT DEFAULT (datetime('now')),
    UNIQUE(student_id, language, question_id)
);

-- Extractions: LLM concept/relation extraction results
CREATE TABLE IF NOT EXISTS extractions (
    extraction_id    TEXT PRIMARY KEY,          -- "E_20260617_001"
    response_id      TEXT NOT NULL REFERENCES responses(response_id),
    model_used       TEXT NOT NULL,             -- "gpt-4.1-mini", "qwen3-8b", "mock"
    concepts         TEXT NOT NULL,             -- JSON array of concept strings
    relations        TEXT NOT NULL,             -- JSON array of relation objects
    missing_hints    TEXT,                      -- JSON array of missing link hints
    raw_response     TEXT,                      -- LLM original output text
    extraction_time_ms INTEGER,                 -- milliseconds
    confidence       REAL DEFAULT 1.0,          -- extraction confidence 0-1
    created_at       TEXT DEFAULT (datetime('now'))
);

-- Graphs: networkx knowledge graphs built from extractions
CREATE TABLE IF NOT EXISTS graphs (
    graph_id        TEXT PRIMARY KEY,           -- "G_20260617_001"
    extraction_id   TEXT NOT NULL REFERENCES extractions(extraction_id),
    language        TEXT NOT NULL,
    domain          TEXT DEFAULT 'social_issues',
    node_count      INTEGER,
    edge_count      INTEGER,
    density         REAL,
    graph_json      TEXT NOT NULL,              -- NetworkX DiGraph serialized
    created_at      TEXT DEFAULT (datetime('now'))
);

-- Gold Labels: human annotations (ground truth)
CREATE TABLE IF NOT EXISTS gold_labels (
    label_id        TEXT PRIMARY KEY,            -- "L_20260617_001"
    response_id     TEXT NOT NULL REFERENCES responses(response_id),
    annotator       TEXT NOT NULL,               -- "annotator_1", "partner_name"
    concepts        TEXT NOT NULL,               -- JSON array of concept strings
    relations       TEXT NOT NULL,               -- JSON array of relation objects
    missing_hints   TEXT,                        -- JSON array of missing link hints
    difficulty      TEXT DEFAULT 'medium',        -- "easy", "medium", "hard"
    created_at      TEXT DEFAULT (datetime('now'))
);

-- Cross-Language Analysis: LDS & CDI results per student per language pair
CREATE TABLE IF NOT EXISTS cross_language_analysis (
    analysis_id      TEXT PRIMARY KEY,           -- "A_20260617_001"
    student_id       TEXT NOT NULL REFERENCES students(student_id),
    lang_pair        TEXT NOT NULL,              -- "zh-de", "zh-en", "de-en"
    topic            TEXT NOT NULL,              -- "freedom", "justice", "success", "family"
    lcd_score        REAL,                       -- Language Cognitive Drift
    graph_similarity REAL,
    concept_shift_count INTEGER,
    relation_shift_count INTEGER,
    shared_concepts   INTEGER,
    unique_l1_concepts INTEGER,
    unique_l2_concepts INTEGER,
    details_json     TEXT,                       -- Full analysis details
    created_at       TEXT DEFAULT (datetime('now'))
);

-- Evaluation Results: LLM extraction accuracy vs gold labels
CREATE TABLE IF NOT EXISTS evaluation_results (
    eval_id          TEXT PRIMARY KEY,           -- "EV_20260617_001"
    extraction_id    TEXT NOT NULL REFERENCES extractions(extraction_id),
    label_id         TEXT NOT NULL REFERENCES gold_labels(label_id),
    concept_precision REAL,
    concept_recall    REAL,
    concept_f1        REAL,
    relation_precision REAL,
    relation_recall    REAL,
    relation_f1        REAL,
    mcl_precision     REAL,
    mcl_recall        REAL,
    mcl_f1            REAL,
    coverage          REAL,
    details_json     TEXT,
    created_at       TEXT DEFAULT (datetime('now'))
);

-- Indices for common query patterns
CREATE INDEX IF NOT EXISTS idx_responses_student
    ON responses(student_id);
CREATE INDEX IF NOT EXISTS idx_responses_language
    ON responses(language);
CREATE INDEX IF NOT EXISTS idx_responses_question
    ON responses(question_id);
CREATE INDEX IF NOT EXISTS idx_extractions_response
    ON extractions(response_id);
CREATE INDEX IF NOT EXISTS idx_extractions_model
    ON extractions(model_used);
CREATE INDEX IF NOT EXISTS idx_graphs_language
    ON graphs(language);
CREATE INDEX IF NOT EXISTS idx_cross_lang_student
    ON cross_language_analysis(student_id);
CREATE INDEX IF NOT EXISTS idx_cross_lang_pair
    ON cross_language_analysis(lang_pair);
CREATE INDEX IF NOT EXISTS idx_gold_labels_response
    ON gold_labels(response_id);
CREATE INDEX IF NOT EXISTS idx_eval_extraction
    ON evaluation_results(extraction_id);
"""


# ===== Initialization =====

def create_database(drop_first: bool = False) -> sqlite3.Connection:
    """Create or recreate the database with all tables."""
    if drop_first and DB_PATH.exists():
        DB_PATH.unlink()
        print(f"  [DROP] Removed existing database: {DB_PATH.name}")

    conn = get_connection()

    # Execute schema
    conn.executescript(SCHEMA_SQL)
    conn.commit()

    print(f"  [OK] Database ready: {DB_PATH.name}")
    print(f"  [OK] {len([s for s in SCHEMA_SQL.split('CREATE TABLE') if s.strip()])} tables created")
    return conn


# ===== Statistics =====

def print_stats(conn: sqlite3.Connection) -> None:
    """Print row counts for every table."""
    tables = [
        "students", "questionnaires", "responses",
        "extractions", "graphs", "gold_labels",
        "cross_language_analysis", "evaluation_results"
    ]
    print(f"\n{'='*50}")
    print(f"  Database: {DB_PATH.name}")
    print(f"{'='*50}")
    total = 0
    for table in tables:
        count = conn.execute(f"SELECT COUNT(*) as c FROM {table}").fetchone()["c"]
        status = "✅" if count > 0 else "  "
        print(f"  {status} {table:<30s} {count:>4d} rows")
        total += count
    print(f"{'─'*50}")
    print(f"     {'TOTAL':<30s} {total:>4d} rows")
    print(f"{'='*50}\n")


# ===== CLI Entry =====

def main():
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph Database Initialization")
    parser.add_argument("--fresh", action="store_true", help="Drop and recreate database")
    parser.add_argument("--stats", action="store_true", help="Print table statistics")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  LinguaGraph DB Initialization")
    print(f"{'='*50}")

    if args.stats:
        conn = get_connection()
        print_stats(conn)
        conn.close()
        return

    conn = create_database(drop_first=args.fresh)
    print_stats(conn)
    conn.close()

    print("  [DONE] Database initialized successfully.\n")


if __name__ == "__main__":
    main()
