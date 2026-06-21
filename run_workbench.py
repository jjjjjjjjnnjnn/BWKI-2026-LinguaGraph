#!/usr/bin/env python3
"""
LinguaGraph Research Workbench — Launch Script

Starts the Flask development server.
Open http://localhost:5000 in your browser.

Usage:
    python run_workbench.py
"""

import sys, os
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

from workbench.app import app

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════╗")
    print("║  LinguaGraph Research Workbench              ║")
    print("║  Open: http://localhost:5000                 ║")
    print("║                                                ║")
    print("║  Pages:                                       ║")
    print("║  /              Overview + corpus stats       ║")
    print("║  /results       Graph analysis + LDS          ║")
    print("║  /cognitivespace 3D visualization             ║")
    print("║  /report        Structural analysis report    ║")
    print("╚══════════════════════════════════════════════╝")
    app.run(debug=False, port=5000)
