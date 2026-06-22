#!/usr/bin/env python3
"""
LinguaGraph — Unified Pipeline
===============================
Single entry point for all pipeline operations.
Auto-detects DB state and runs the right combination of scripts.

Usage:
    python scripts/run_pipeline.py              # Full pipeline (auto-detect mode)
    python scripts/run_pipeline.py --force     # Force export pipeline even without DE/EN
    python scripts/run_pipeline.py --status    # Only print DB status, no pipeline run
"""

import importlib.util
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

import numpy as np

# Ensure we can import from scripts/
SCRIPTS_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from db_utils import get_connection, query, query_value


def detect_db_status() -> Dict[str, Any]:
    """Detect what data is available in the database."""
    conn = get_connection()

    # Count responses by language
    lang_counts = query(conn, """
        SELECT language, COUNT(*) as c
        FROM responses
        GROUP BY language
        ORDER BY language
    """)

    # Count participants by native language
    native_counts = query(conn, """
        SELECT native_lang, COUNT(*) as c
        FROM students
        GROUP BY native_lang
        ORDER BY native_lang
    """)

    # Check cross_language_analysis for existing LDS results
    lds_count = query_value(conn, "SELECT COUNT(*) FROM cross_language_analysis")

    # Check extractions
    extraction_count = query_value(conn, "SELECT COUNT(*) FROM extractions")

    # Check gold_labels
    gold_count = query_value(conn, "SELECT COUNT(*) FROM gold_labels")

    conn.close()

    langs = {r["language"]: r["c"] for r in lang_counts}
    natives = {r["native_lang"]: r["c"] for r in native_counts}

    has_zh = langs.get("zh", 0) > 0
    has_de = langs.get("de", 0) > 0
    has_en = langs.get("en", 0) > 0

    total_responses = sum(langs.values())

    return {
        "has_zh": has_zh,
        "has_de": has_de,
        "has_en": has_en,
        "languages_present": sorted(langs.keys()),
        "responses_by_language": langs,
        "participants_by_native": natives,
        "total_responses": total_responses,
        "lds_analyses": lds_count,
        "extractions": extraction_count,
        "gold_labels": gold_count,
        "has_cross_language_data": lds_count > 0,
    }


def print_status(status: Dict[str, Any]):
    """Print human-readable DB status."""
    print(f"\n{'='*60}")
    print(f"  LinguaGraph — DB Status Report")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    print("  Responses by language:")
    for lang, count in sorted(status["responses_by_language"].items()):
        print(f"    {lang}: {count}")
    print(f"    Total: {status['total_responses']}")

    print(f"\n  Participants by native language:")
    for lang, count in sorted(status["participants_by_native"].items()):
        print(f"    {lang}: {count}")

    print(f"\n  Extractions: {status['extractions']}")
    print(f"  Gold labels: {status['gold_labels']}")
    print(f"  LDS analyses: {status['lds_analyses']}")

    print(f"\n  Pipeline mode: ", end="")
    if status["has_de"] or status["has_en"]:
        print("FULL (DE/EN data present → all outputs)")
    else:
        print("ZH-ONLY (summary + quality + LDS template)")

    print(f"\n{'='*60}\n")


def run_script(module_name: str, func_name: str, label: str):
    """Import a script module and call a function by name."""
    script_path = SCRIPTS_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        print(f"  [FAIL] Cannot load {script_path}")
        return False

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, func_name):
        print(f"  [FAIL] {module_name}.py has no function '{func_name}'")
        return False

    print(f"\n  [{label}] Running {module_name}.{func_name}()...")
    getattr(module, func_name)()
    return True


def main():
    random.seed(42)
    np.random.seed(42)
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph Unified Pipeline")
    parser.add_argument("--force", action="store_true",
                        help="Force full pipeline even without DE/EN data")
    parser.add_argument("--status", action="store_true",
                        help="Print DB status and exit")
    args = parser.parse_args()

    # 1. Detect state
    status = detect_db_status()

    if args.status:
        print_status(status)
        return

    print(f"\n{'='*60}")
    print(f"  LinguaGraph — Unified Pipeline")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    print_status(status)

    # 2. Decide pipeline mode
    has_de_or_en = status["has_de"] or status["has_en"]
    run_full = has_de_or_en or args.force

    # 3. Always run pilot_pipeline components (importable functions)
    from pilot_pipeline import (
        ensure_dirs,
        export_participant_summary,
        export_participant_summary_md,
        export_quality_report,
        export_lds_template,
        export_results_summary,
    )

    ensure_dirs()

    print("  Phase 1: Participant Summary...")
    export_participant_summary()
    export_participant_summary_md()

    print("\n  Phase 2: Quality Report...")
    export_quality_report()

    print("\n  Phase 3: LDS Report...")
    export_lds_template()

    # 4. Full pipeline (tables + figures) only when DE/EN data or --force
    if run_full:
        print("\n  Phase 4: Tables & Figures (DE/EN data available)...")
        sys.path.insert(0, str(PROJECT_DIR / "results"))
        from export_pipeline import (
            export_demographics,
            export_lds_table,
            generate_figures,
        )
        export_demographics()
        export_lds_table()
        generate_figures()
        print()
    else:
        print("\n  Phase 4: Skipped (no DE/EN data).")

    print("\n  Phase 5: Results Summary...")
    export_results_summary()

    print(f"\n{'='*60}")
    print(f"  Pipeline Complete.")
    print(f"  Mode: {'FULL' if run_full else 'ZH-ONLY (use --force for full)'}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    main()
