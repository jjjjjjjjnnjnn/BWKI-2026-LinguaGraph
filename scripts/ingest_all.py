"""
Ingest All Data — Batch Import
=================================
Run all ingestion scripts in order.

Usage:
    python ingest_all.py            # Import all available data
    python ingest_all.py --fresh    # Re-import (clear existing)
    python ingest_all.py --dry-run  # Preview only
"""

import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
SCRIPTS = [
    ("ingest_questionnaires.py", "Questionnaires"),
    ("ingest_student_data.py",   "Student Data"),
    ("ingest_gold_labels.py",    "Gold Labels"),
    ("ingest_expert_graphs.py",  "Expert Graphs"),
]


def run_script(name: str, label: str, fresh: bool = False, dry_run: bool = False) -> bool:
    """Run a single ingestion script. Returns True on success."""
    script_path = SCRIPTS_DIR / name
    if not script_path.exists():
        print(f"\n  [SKIP] {name} not found")
        return True

    print(f"\n{'='*50}")
    print(f"  Step: {label}")
    print(f"{'='*50}")

    cmd = [sys.executable, str(script_path)]
    if fresh:
        cmd.append("--fresh")
    if dry_run:
        cmd.append("--dry-run")

    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Batch import all data into linguaGraph DB")
    parser.add_argument("--fresh", action="store_true", help="Re-import (clear existing)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without importing")
    parser.add_argument("--skip-validation", action="store_true", help="Skip validation step")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  LinguaGraph — Batch Data Import")
    print(f"  {'(DRY RUN)' if args.dry_run else '(LIVE)'}")
    print(f"{'='*50}\n")

    all_ok = True
    for script_name, label in SCRIPTS:
        ok = run_script(script_name, label, fresh=args.fresh, dry_run=args.dry_run)
        if not ok:
            print(f"  [FAILED] {label}")
            all_ok = False

    # Run validation at the end
    if not args.dry_run and not args.skip_validation:
        print(f"\n{'='*50}")
        print(f"  Final: Data Validation")
        print(f"{'='*50}")
        subprocess.run([sys.executable, str(SCRIPTS_DIR / "validate_data.py")])

    # Show db summary
    if not args.dry_run:
        print(f"\n{'='*50}")
        print(f"  Final Summary")
        print(f"{'='*50}")
        subprocess.run([sys.executable, str(SCRIPTS_DIR / "db_utils.py"), "--summary"])

    if all_ok:
        print(f"\n  [PASS] All imports completed successfully!\n")
    else:
        print(f"\n  [WARN] Some imports had issues. Check output above.\n")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
