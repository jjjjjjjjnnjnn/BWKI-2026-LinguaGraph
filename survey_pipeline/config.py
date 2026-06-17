"""
LinguaGraph Survey Pipeline — Configuration
=============================================
Central config for the pilot/main survey analysis pipeline.
"""

from pathlib import Path

# === Paths ===
PROJECT_DIR = Path(__file__).parent.parent
DB_PATH = PROJECT_DIR / "linguaGraph.db"
DATA_DIR = PROJECT_DIR / "data"
QUESTIONNAIRE_DIR = DATA_DIR / "questionnaires"
OUTPUT_DIR = PROJECT_DIR / "survey_pipeline" / "output"
REPORT_DIR = PROJECT_DIR / "docs" / "survey_reports"

# === LLM Config (LM Studio local) ===
LLM_BASE_URL = "http://127.0.0.1:1234/v1"
LLM_MODEL = "qwen3-8b"
LLM_TEMPERATURE = 0.3
LLM_MAX_TOKENS = 2000

# === Topic Mapping ===
# Maps Google Form question numbers to topic IDs
QUESTION_TOPIC_MAP = {
    4: "success",
    5: "success",
    6: "success",
    7: "responsibility",
    8: "responsibility",
    9: "responsibility",
    10: "freedom",
    11: "freedom",
    12: "freedom",
    13: "home",
    14: "home",
    15: "home",
    16: "justice",
    17: "justice",
    18: "justice",
    19: "meta",
    20: "meta",
}

# Maps question numbers to question IDs for DB
QUESTION_ID_MAP = {
    4: "q_success_def",
    5: "q_success_words",
    6: "q_success_scenario",
    7: "q_resp_relation",
    8: "q_resp_words",
    9: "q_resp_scenario",
    10: "q_freedom_boundary",
    11: "q_freedom_words",
    12: "q_freedom_scenario",
    13: "q_home_diff",
    14: "q_home_words",
    15: "q_home_scenario",
    16: "q_justice_def",
    17: "q_justice_words",
    18: "q_justice_scenario",
    19: "q_meta_language",
    20: "q_meta_switch",
}

# Concept word questions (free association, one word per line)
WORD_QUESTIONS = {5, 8, 11, 14, 17}

# === Language Detection ===
NATIVE_LANG_MAP = {
    "Chinese": "zh",
    "English": "en",
    "German": "de",
}

# === Quality Thresholds ===
MIN_WORD_COUNT = 10
MIN_ANSWER_LENGTH = 20

# === Pipeline Settings ===
USE_MOCK_EXTRACTION = False  # Set True to skip LLM calls (for testing)
ANNOTATION_BATCH_SIZE = 5
