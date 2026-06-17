"""
Survey Pipeline — One-Click Runner
====================================
Run the complete survey analysis pipeline from CSV to report.

Usage:
    python run_all.py <csv_file>           # Full pipeline
    python run_all.py <csv_file> --mock    # Skip LLM calls
    python run_all.py <csv_file> --dry-run # Preview only
"""

import sys
import time
from pathlib import Path

from import_csv import import_csv
from clean_data import run_cleaning
from annotate import annotate_all
from run_lds import run_lds
from generate_report import generate_report


def run_pipeline(csv_file: str, use_mock: bool = False, dry_run: bool = False):
    """Run the complete pipeline."""
    print(f"\n{'#'*60}")
    print(f"  LinguaGraph Survey Pipeline")
    print(f"  Input: {csv_file}")
    print(f"  Mode: {'DRY RUN' if dry_run else ('MOCK' if use_mock else 'FULL')}")
    print(f"{'#'*60}\n")

    start_time = time.time()

    # Step 1: Import CSV
    print("=" * 60)
    print("  STEP 1/5: Import CSV")
    print("=" * 60)
    import_result = import_csv(csv_file, dry_run=dry_run)
    if dry_run:
        print("  [DRY RUN] Stopping after import preview.")
        return
    if "error" in import_result:
        print(f"  [ERROR] Import failed: {import_result['error']}")
        return

    # Step 2: Clean Data
    print("\n" + "=" * 60)
    print("  STEP 2/5: Clean Data")
    print("=" * 60)
    clean_stats = run_cleaning()

    # Step 3: Annotate (LLM extraction)
    print("\n" + "=" * 60)
    print("  STEP 3/5: Annotate (LLM)")
    print("=" * 60)
    annotate_all(use_mock=use_mock)

    # Step 4: Compute LDS
    print("\n" + "=" * 60)
    print("  STEP 4/5: Compute LDS")
    print("=" * 60)
    run_lds()

    # Step 5: Generate Report
    print("\n" + "=" * 60)
    print("  STEP 5/5: Generate Report")
    print("=" * 60)
    generate_report()

    elapsed = time.time() - start_time
    print(f"\n{'#'*60}")
    print(f"  Pipeline complete!")
    print(f"  Time: {elapsed:.1f}s")
    print(f"  Output: docs/survey_reports/")
    print(f"{'#'*60}\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run full survey pipeline")
    parser.add_argument("csv_file", help="Path to Google Forms CSV export")
    parser.add_argument("--mock", action="store_true", help="Use mock extraction (no LLM)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without importing")
    args = parser.parse_args()

    run_pipeline(args.csv_file, use_mock=args.mock, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
