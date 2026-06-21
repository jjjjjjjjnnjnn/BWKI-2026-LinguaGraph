# Data Manifest

## Overview

This directory contains the source data used by the LinguaGraph research pipeline. Raw textbook content and LLM extraction outputs are **referenced but not versioned** in this repository to maintain a focused, lightweight research codebase.

## Collections

| Collection | Files | Status | Description |
|-----------|-------|--------|-------------|
| `textbook/` | 75+ text files | 📦 Referenced only | Raw textbook sections (ZH/EN/DE), sourced from CC-BY-SA and fair-use educational materials |
| `math_extractions/` | 63 JSON files | 📦 Referenced only | MIMO LLM extraction outputs — concept/relation JSON from each textbook section |
| `questionnaires/` | 3 JSON + 2 PDF | ✅ Tracked | BWKI survey instruments in ZH/EN/DE |
| `gold/` | 1 JSON | ✅ Tracked | Gold-standard human annotations |
| `baseline/` | 1 JSON | ✅ Tracked | Computational baseline results |
| `corpus/` | 12+ text files | ✅ Tracked | Wikipedia pilot corpus (ZH/EN/DE, 5 topics) |
| `evidence/` | 6 files | ✅ Tracked | Research evidence and analysis summaries |

## Raw Data Policy

The following are **not committed** to this repository:

- `data/textbook/` — Raw textbook text (size, copyright considerations)
- `data/math_extractions/` — LLM extraction outputs (derived, reproducible from pipeline)

These assets are regenerable by running the pipeline:

```bash
# Regenerate extractions from textbook text (requires MIMO LLM)
# Then run the knowledge graph pipeline:
python scripts/math_graph_pipeline/run_pipeline.py
```

For BWKI review, the complete dataset including raw text and extractions is available upon request or can be regenerated using the pipeline scripts in `cognitive-space/scripts/math_graph_pipeline/`.

## Provenance

All textbook sources are documented in `cognitive-space/README.md` with full attribution (publisher, edition, chapter references). Extraction methodology is documented in `docs/mimo_prompt.md`.
