#!/usr/bin/env python3
"""
WRAPPER — delegates to canonical scripts/math_graph_pipeline/

Canonical source: scripts/math_graph_pipeline/
This file is auto-generated — edit the canonical version, not this wrapper.
"""

import sys
from pathlib import Path

_canonical = str(Path(__file__).resolve().parents[3] / "scripts")
if _canonical not in sys.path:
    sys.path.insert(0, _canonical)

from math_graph_pipeline.export_graph import main as _main

if __name__ == "__main__":
    _main()
