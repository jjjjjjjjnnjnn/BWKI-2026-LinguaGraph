# LinguaGraph — Project Consolidation Report

> Date: 2026-06-17
> Action: Merged 3 directories → 1 unified project

---

## 1. Source Directories

| # | Directory | Size | Status |
|---|-----------|------|--------|
| A | `C:\Users\rongj\Desktop\linguagraph` | ~50 files | ✅ Merged into main project |
| B | `C:\Users\rongj\Desktop\学校\BWKI-2026-备战` | ~200 files | ✅ Main project (kept) |
| C | `C:\Users\rongj\Desktop\本地知识库\知识库内容\BWKI` | ~600+ files | 📚 Reference library (kept as-is) |

---

## 2. Conflict Analysis

### 2.1 Conflicting Files (same name, different content)

| File | linguagraph version | 02-项目规划 version | Decision |
|------|-------------------|-------------------|----------|
| `src/compare.py` | 315 lines, Jun 17 | 204 lines, Jun 15 | **Keep main version** — tested with DB pipeline |
| `src/cross_language.py` | 323 lines, Jun 17 | 280 lines, Jun 15 | **Keep main version** — tested with DB pipeline |
| `src/extract.py` | `extract_v2.py` (9453 bytes) | `extract.py` (8558 bytes) | **Keep both** — v2 archived for reference |
| `pipeline.py` | 119 lines, different approach | v1 + mock versions | **Archived** main version is DB-integrated |
| `requirements.txt` | 64 bytes | 82 bytes | **Merge** (union of both) |

### 2.2 New Files Added from linguagraph

| Source | Destination | Description |
|--------|-------------|-------------|
| `linguagraph/experiments/*.py` (9 files) | `02-项目规划/experiments/` | Data collection scripts (Wikipedia, education, social media, baseline) |
| `linguagraph/visualization/` | `02-项目规划/web/threejs/` | New Three.js Cognitive City version |
| `linguagraph/questionnaire/` | `02-项目规划/data/questionnaires/` | PDF forms, survey analysis, form structure |
| `linguagraph/research/` (6 files) | `02-项目规划/research/` | concept_mapping, validate_method, research_loop, hypotheses |
| `linguagraph/docs/` (9 files) | `02-项目规划/docs/linguagraph_*` | audit-report, compliance-review, error-analysis, etc. |

### 2.3 Files Unique to 02-项目规划 (not in linguagraph)

These are the core of the project and were missing from linguagraph:

| Category | Files |
|----------|-------|
| **Database** | `db_init.py`, `db_utils.py`, `linguaGraph.db`, `ingest_*.py` (5 files) |
| **Pipeline** | `analyze_student.py`, `evaluate_pipeline.py`, `survey_entry.py`, `validate_data.py` |
| **Human Study** | `scripts/analyze_pilot.py`, `scripts/annotator_agreement.py`, `scripts/compare_human_vs_model.py`, `scripts/simulate_baseline.py` |
| **Documentation** | `annotation_guideline_v2.md`, `experiment_design.md`, `questionnaire_validation.md`, `project_audit.md`, `bwki_paper_outline.md`, `creative_submission.md`, `simulation_protocol.md` |
| **Ethics** | `docs/ethics/` (7 documents: consent forms, GDPR package) |
| **Config** | `config/cross_language_mapping.json`, `config/concept_mapping.json`, `config/prompts/` |
| **Research** | `research/analyze_concept.py`, `research/generate_city_data.py`, `research/findings/*` (8 files) |
| **Data** | `data/pilot_corpus/` (4 concepts × 3 languages), `data/evidence/` (6 files) |
| **Frontend** | `web/index.html` (original), `web/server.py` |

---

## 3. Final Project Structure (After Merge)

```
02-项目规划/
├── src/                      # Core library (tested, annotated)
│   ├── extract.py            # LLM extraction
│   ├── graph.py              # Graph construction
│   ├── compare.py            # Missing link detection
│   ├── cross_language.py     # Cross-language gap analysis
│   ├── scoring.py            # MCL, LCD, F1 scoring
│   ├── explain.py            # Explanation generation
│   ├── models.py             # Data models
│   ├── schema_utils.py       # Schema validation
│   ├── review_workflow.py    # Review automation
│   ├── providers/            # LLM provider abstraction
│   │   ├── base.py
│   │   ├── ollama.py
│   │   └── openai.py
│   └── archive/              # From linguagraph (reference)
│       ├── compare_mimo.py
│       ├── cross_language_mimo.py
│       ├── extract_v2.py
│       ├── pipeline_mimo.py
│       └── run_loop.py
│
├── scripts/                  # Human study tools
│   ├── analyze_pilot.py
│   ├── annotator_agreement.py
│   ├── compare_human_vs_model.py
│   ├── simulate_baseline.py
│   └── bwki_analysis.py
│
├── experiments/              # Data collection (from linguagraph)
│   ├── collect_wikipedia.py
│   ├── collect_education.py
│   ├── collect_social.py
│   ├── collect_fast.py
│   ├── generate_baseline.py
│   ├── pilot_corpus_analysis.py
│   ├── reorganize_corpus.py
│   ├── social_media_scraper.py
│   └── textbook_comparison.py
│
├── data/
│   ├── questionnaires/       # ZH/DE/EN surveys + from linguagraph
│   ├── pilot_corpus/         # Wikipedia articles (4 topics × 3 langs)
│   ├── gold/                 # 21 gold labels
│   ├── evidence/             # Research foundation docs
│   └── (simulation/)         # Simulation data (to be generated)
│
├── config/
│   ├── config.yaml
│   ├── concept_mapping.json
│   ├── cross_language_mapping.json
│   ├── normalization_map.json
│   └── prompts/extract.md
│
├── docs/
│   ├── annotation_guideline_v2.md
│   ├── bwki_paper_outline.md
│   ├── questionnaire_validation.md
│   ├── question_audit.md
│   ├── creative_submission.md
│   ├── experiment_design.md
│   ├── experiment_conductor.md
│   ├── project_audit.md
│   ├── simulation_protocol.md
│   ├── PROJECT_LOG.md
│   ├── CHANGELOG.md
│   ├── linguagraph_*          # From linguagraph (prefixed)
│   └── ethics/                # 7 GDPR/consent documents
│
├── research/
│   ├── analyze_concept.py     # Cross-language analysis pipeline
│   ├── generate_city_data.py  # Cognitive City JSON export
│   ├── (from linguagraph: concept_mapping.py, validate_method.py, etc.)
│   └── findings/              # LDS results, rankings, reports
│
├── web/
│   ├── index.html             # Original Three.js demo
│   ├── server.py
│   └── threejs/               # New Cognitive City (from linguagraph)
│       ├── index.html
│       └── main.js
│
├── tests/                     # 21 pytest tests
├── db_init.py                 # Database schema
├── db_utils.py                # Database utilities
├── linguaGraph.db             # SQLite database
├── *.py                       # Pipeline scripts (root level)
└── 归档/                       # v3 archives
```

---

## 4. Knowledge Base (Reference Library)

`C:\Users\rongj\Desktop\本地知识库\知识库内容\BWKI\` remains **unchanged** — it serves as the research reference library with:

| Directory | Content | File Count |
|-----------|---------|------------|
| 00_overview | BWKI guides, scoring, strategy | 6 |
| 01_cognitive_science | Paper summaries | ~80+ |
| 02_linguistics | Cross-linguistic research | ~30 |
| 03_education | Education research | ~20 |
| 04_ai_education | AI in education | ~15 |
| 05_graph_theory | Graph theory papers | ~15 |
| 06_cross_lingual_kg | Multilingual knowledge graphs | ~10 |
| 07_cultural_psychology | Cultural psychology | ~10 |
| 08_visualization | Visualization references | ~10 |
| 09_research_database | Paper tracker (P001-P088) | ~10 |
| 10_methodology | Research methods | ~10 |
| 11_prototype | Existing tools analysis | ~10 |
| 12_experts | Expert interviews | ~5 |
| 13_social_media_corpus | Social media data | ~5 |
| **Total** | | **~250+ files** |

---

## 5. Consolidation Stats

| Metric | Before | After |
|--------|--------|-------|
| Python files | ~35 (main) + ~12 (linguagraph) | ~47 (unified) |
| Documentation | ~15 (main) + ~9 (linguagraph) | ~24 (merged) |
| Experiment scripts | ~0 | ~9 (from linguagraph) |
| Research findings | ~8 | ~15 (merged) |
| Visualization | 1 page (web/) | 2 versions (web/ + web/threejs/) |
| Knowledge base | → kept separate | ~250 files (unchanged) |

---

## 6. What to Clean Up

| Item | Action |
|------|--------|
| `C:\Users\rongj\Desktop\linguagraph` | ✅ Can delete after verification |
| `02-项目规划/encoding_test.txt` | ✅ Test artifact, safe to delete |
| `02-项目规划/encoding_test_raw.txt` | ✅ Test artifact, safe to delete |
| `02-项目规划/src/archive/` | Keep for reference until pipeline is stable |
| `02-项目规划/root *.py` | Consider moving to subdirectories (scripts/, experiments/) |
| Knowledge base | Keep as-is, reference only |

---

## 7. Verification

- ✅ All existing tests pass (21 pytest)
- ✅ Database schema intact (9 tables)
- ✅ All analysis scripts import correctly
- ✅ No duplicate file names in core directories
- ✅ Ethical documents consolidated (7 files in docs/ethics/)
- ✅ Both Three.js versions preserved (web/ + web/threejs/)
- ✅ linguagraph docs archived with `linguagraph_` prefix
