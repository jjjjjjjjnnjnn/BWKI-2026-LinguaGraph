#!/usr/bin/env python3
"""
CognitiveSpace — One-Command Pipeline

Runs the full math graph pipeline in sequence:
  merge → align → export

Usage:
    python scripts/math_graph_pipeline/run_pipeline.py [--input-dir data/math_extractions]

Equivalent to running merge_extractions.py, align_languages.py, and export_graph.py
in sequence with default arguments.
"""

import subprocess
import sys
from pathlib import Path


def run_step(script_name: str, description: str, input_dir: str | None = None) -> bool:
    """Run a pipeline step and return True if successful."""
    script_path = Path(__file__).parent / script_name
    cmd = [sys.executable, str(script_path)]
    if input_dir:
        cmd.extend(["--input-dir", input_dir])

    print(f"\n{'='*60}")
    print(f"  Step: {description}")
    print(f"{'='*60}\n")

    result = subprocess.run(cmd, cwd=str(Path(__file__).parent.parent.parent))
    return result.returncode == 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run the full CognitiveSpace math graph pipeline")
    parser.add_argument("--input-dir", type=str, default=None,
                        help="Input directory for extraction files (default: data/math_extractions)")
    args = parser.parse_args()

    input_dir = args.input_dir

    steps = [
        ("merge_extractions.py", "Merge extractions"),
        ("align_languages.py", "Align languages"),
        ("export_graph.py", "Export graphs"),
        ("validate_pipeline.py", "Quality gates"),
    ]

    print("CognitiveSpace — Full Pipeline")
    print(f"Python: {sys.executable}")
    if input_dir:
        print(f"Input dir: {input_dir}")

    for script, desc in steps:
        if not run_step(script, desc, input_dir):
            print(f"\n[FAIL] Pipeline stopped at: {desc}")
            sys.exit(1)

    print(f"\n{'='*60}")
    print("  Pipeline complete!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
