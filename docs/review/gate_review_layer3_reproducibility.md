# Gate Review Layer 3: Reproducibility Audit

**Date**: 2026-06-17
**Auditor**: Reproducibility Auditor
**Scope**: Full reproducibility audit of LinguaGraph project
**Target**: BWKI 2026 contest submission readiness

---

## Summary

| Metric | Score | Status |
|--------|-------|--------|
| Hardcoded paths in code | 0 | PASS |
| Hardcoded paths in docs | 12+ | WARN |
| Dependency completeness | 4 phantom deps | FAIL |
| API-free demo mode | Partial | WARN |
| DB schema versioning | None | FAIL |
| Test suite (pytest) | 2 files, 19 tests | WARN |
| Can third-party reproduce? | Not without guidance | FAIL |

---

## 1. Hardcoded Paths

### Finding 1.1: Zero hardcoded paths in executable code

- **Risk**: Hardcoded absolute paths blocking cross-machine runs
- **Severity**: LOW (no issue, but verify negative finding)
- **Evidence**: Grep of `src/`, `scripts/`, `tests/`, `config/` — zero matches for `C:\Users\rongj`
- **Impact**: The Python source code uses `Path(__file__).parent.parent` consistently, which resolves relative to file location. This IS portable.
- **Fix cost**: None required
- **Fix suggestion**: Maintain this pattern.

### Finding 1.2: Hardcoded paths in documentation (acceptable but fragile)

- **Risk**: Documentation drift — if the parent directory structure changes, docs become wrong
- **Severity**: LOW
- **Evidence**: 12+ occurrences across 6 files:
  - `.claude/CLAUDE.md`: line 99 (`$PROJECT_DIR` definition)
  - `docs/corpus-status.md`: lines 82, 85, 88
  - `docs/CONSOLIDATION_REPORT.md`: lines 12-14, 155, 194
  - `docs/PROJECT_LOG.md`: line 18
  - `docs/compose/plans/2026-06-16-cognitivespace-v5.md`: lines 400, 457, 532, 624, 697
  - `docs/video_script.md`: line 110
- **Impact**: BWKI judges will not read project-local `.claude/` or internal `docs/compose/` files. The hardcoded paths in `corpus-status.md` point to a separate knowledge base (`C:\Users\rongj\Desktop\本地知识库\`) that is NOT in the repository, so the corpus status is unreproducible.
- **Fix cost**: Low
- **Fix suggestion**: Replace hardcoded absolute paths with `$PROJECT_DIR` alias or relative paths in user-facing docs only. The `corpus-status.md` paths referencing the local knowledge base should be either reconciled as reproducible corpus data or clearly documented as external.

---

## 2. Dependency Completeness

### Finding 2.1: Phantom dependencies in requirements.txt

- **Risk**: Unused dependencies create confusion and bloat
- **Severity**: MEDIUM
- **Evidence**: `requirements.txt` lists 9 packages. The following 4 are NOT imported by any file under `src/`:
  - `requests>=2.28` — not imported anywhere in src/
  - `scipy>=1.10` — not imported anywhere in src/
  - `beautifulsoup4>=4.11` (bs4) — not imported anywhere in src/
  - `scikit-learn>=1.2` (sklearn) — not imported anywhere in src/
- **Impact**: A judge running `pip install -r requirements.txt` will install 4 unnecessary packages. This does not break reproducibility but signals sloppy dependency management.
- **Fix cost**: Low
- **Fix suggestion**: Remove `requests`, `scipy`, `beautifulsoup4`, `scikit-learn` unless needed by scripts outside `src/`. Audit `scripts/` separately.

### Finding 2.2: Version pins are too loose

- **Risk**: Upstream breaking changes between now and Sept 2026 submission
- **Severity**: MEDIUM
- **Evidence**: Every dependency uses `>=` with no upper bound:
  ```
  openai>=1.0.0
  networkx>=3.0
  pyyaml>=6.0
  ```
  The `openai` SDK is volatile (frequent breaking changes between minor versions). NetworkX may introduce breaking changes in v4.x.
- **Impact**: A judge cloning in September 2026 and running `pip install -r requirements.txt` could get different package versions that produce different results (especially in the `openai` client library API and NetworkX graph serialization).
- **Fix cost**: Low
- **Fix suggestion**: Add upper bounds: `openai>=1.0.0,<2.0.0`, `networkx>=3.0,<4.0`, etc. Better: generate a `requirements.txt` with exact pinned versions via `pip freeze > requirements.lock` and commit both files.

### Finding 2.3: No Python version constraint

- **Risk**: Judge uses incompatible Python version
- **Severity**: HIGH
- **Evidence**: No `.python-version` file, no `python_requires` in setup.py (no setup.py exists), no Python version mentioned in `requirements.txt` or README.md
  - The code uses `dataclasses` and typed `dict[str, Concept]` (Python 3.9+ syntax)
  - `str | None` type hints (Python 3.10+ syntax)
  - These require Python >= 3.10
- **Impact**: A judge on Python 3.8 or 3.9 will get SyntaxError at import time. Cannot reproduce anything.
- **Fix cost**: Low
- **Fix suggestion**: Add a `.python-version` file with `3.12` (or current tested version). Add to README: "Requires Python >= 3.10". Consider adding `python_requires=">=3.10"` to a `setup.py` or `pyproject.toml`.

---

## 3. API Key Dependency

### Finding 3.1: Working mock/demo mode exists but is poorly surfaced

- **Risk**: Reviewer cannot test pipeline without paid API
- **Severity**: HIGH
- **Evidence**:
  - `src/extract.py` line 34: `use_mock: bool = False` parameter
  - `src/extract.py` lines 88-164: `_mock_extract()` function exists with keyword-based extraction
  - Mock mode is accessible via `extract_concepts(answer, language, use_mock=True)`
  - `tests/test_extraction_validation.py` exposes `--mock` CLI flag (line 142-145)
  - HOWEVER `src/main.py`'s `run_pipeline()` function (lines 17-80) has NO `use_mock` parameter. It always calls the live provider via `extract_concepts(answer, language)`.
  - The default config.yaml sets `provider: ollama` with `base_url: http://127.0.0.1:1234/v1` (LM Studio port, not standard Ollama port 11434)
  - OllamaProvider (ollama.py line 27) hardcodes `api_key="ollama"` — no real key needed.
- **Impact**: A BWKI judge trying `python src/main.py` as shown in README will get a `ConnectionError` because LM Studio/Ollama is not running on 127.0.0.1:1234. They cannot run the pipeline without either (a) setting up Ollama, (b) paying for OpenAI, or (c) finding the hidden mock mode. The mock mode is not mentioned in README.
- **Fix cost**: Low
- **Fix suggestion**: (a) Add `use_mock=True` parameter to `run_pipeline()` in `src/main.py`. (b) Add `python src/main.py --mock` CLI argument. (c) Add a clear "Running without API key" section in README showing `--mock` usage.

### Finding 3.2: OPENAI_API_KEY raises hard error with no fallback

- **Risk**: Pipeline crashes entirely without Ollama or OpenAI key
- **Severity**: HIGH
- **Evidence**: `src/providers/openai.py` lines 25-29:
  ```python
  if not self.api_key:
      raise ValueError(
          "OpenAI API key required. Set OPENAI_API_KEY env var "
          "or llm.openai.api_key in config.yaml"
      )
  ```
  This is correct behavior for the OpenAI provider. But the default config (ollama with LM Studio) will crash if LM Studio is not running because `OllamaProvider.extract()` will throw a `ConnectionError` from the OpenAI SDK — no graceful fallback to mock mode.
- **Impact**: First-run experience is a crash or connection refused. No `.env.example` or `.env` file exists. No documentation tells the judge what to do.
- **Fix cost**: Low
- **Fix suggestion**: (a) Create `.env.example` with `OPENAI_API_KEY=your-key-here` commented out. (b) In README, add a "Configuration" section explaining the two options (Ollama vs OpenAI). (c) Consider catching `ConnectionError` in `get_provider()` and falling back to mock with a warning.

---

## 4. Database Initialization

### Finding 4.1: Schema is NOT versioned

- **Risk**: Cannot migrate schema forward; schema changes destroy data
- **Severity**: CRITICAL
- **Evidence**: Grep for `schema_version`, `SCHEMA_VERSION`, `migration` — zero matches in entire project. No version table in the SQL schema (`db_init.py` lines 47-183). The `CREATE TABLE IF NOT EXISTS` statements have no version tracking. The `--fresh` flag (line 232) drops the entire database.
- **Impact**: If the schema changes between now and September (new tables, new columns), there is no migration path. The only option is `--fresh` which destroys all data. For a competition submission where a judge needs to verify data integrity, this is unacceptable. Any data collected before a schema change would be lost.
- **Fix cost**: Medium
- **Fix suggestion**: Add a `schema_version` table to the database:
  ```sql
  CREATE TABLE IF NOT EXISTS schema_version (
      version INTEGER PRIMARY KEY,
      applied_at TEXT DEFAULT (datetime('now')),
      description TEXT
  );
  ```
  Implement a simple version check in `create_database()`: if DB exists and version < expected, run migration scripts. Maintain atomic migration files in a `migrations/` directory.

### Finding 4.2: linguaGraph.db CAN be recreated from scratch

- **Risk**: Low (positive finding)
- **Severity**: LOW (good)
- **Evidence**: `scripts/db_init.py` line 187-201: `create_database(drop_first=True)` drops and recreates all tables. `get_connection()` uses `DB_PATH = Path(__file__).parent.parent / "linguaGraph.db"` which is relative.
- **Impact**: A judge can recreate the database. However, there is no seed data — the tables are created empty. Running `python scripts/db_init.py` then `python src/main.py` produces empty results because no data has been ingested.
- **Fix cost**: Low
- **Fix suggestion**: Add a `db_init.py --seed` flag that populates tables with demo/test data (the gold dataset and sample students) so a judge can immediately verify results.

---

## 5. Test Suite Completeness

### Finding 5.1: Only 2 of 6 "test" files are real pytest tests

- **Risk**: False sense of test coverage
- **Severity**: HIGH
- **Evidence**: Tests directory listing:
  - `tests/test_scoring.py` — ACTUAL pytest test (4 classes, 13 test methods)
  - `tests/test_compare.py` — ACTUAL pytest test (2 classes, 8 test methods)
  - `tests/test_extraction_validation.py` — NOT pytest; CLI script with `if __name__ == "__main__"`
  - `tests/test_v3_pipeline.py` — NOT pytest; references non-existent `data/survey/v3/example_zh.json`
  - `tests/analyze_results.py` — NOT a test; analysis script
  - `tests/evaluate_survey.py` — NOT a test; survey evaluation script

  Running `python -m pytest tests/ -v` will only discover 2 files with ~19 tests.

- **Impact**: (a) A judge running the prescribed test command sees ~19 tests pass and may assume comprehensive coverage. (b) The non-pytest files look like tests but won't be run by pytest — they are "dead tests." (c) `test_v3_pipeline.py` will crash because it loads a file that does not exist.
- **Fix cost**: Medium
- **Fix suggestion**: (a) Rename non-test scripts or move them out of `tests/`. (b) Add pytest markers: `@pytest.mark.unit`, `@pytest.mark.integration`. (c) Add real pytest tests for: extraction normalization, database operations, cross-language analysis, provider system, end-to-end pipeline with mock.

### Finding 5.2: What IS tested

| Feature | File | Test methods | Coverage |
|---------|------|-------------|----------|
| MCL Score | test_scoring.py | 5 | Identical graphs, all missing, partial, empty expert |
| LCD Score | test_scoring.py | 3 | Identical, different, with cross-language mapping |
| Concept F1 | test_scoring.py | 3 | Perfect, partial, no match |
| Relation F1 | test_scoring.py | 3 | Perfect, wrong type, empty |
| Missing link detection | test_compare.py | 5 | Identical, missing concept, missing relation, isolated node, threshold |
| Graph similarity | test_compare.py | 3 | Identical, empty, no overlap |

### Finding 5.3: What is NOT tested

- **LLM extraction** — `extract.py` normalization functions have zero tests
- **Graph building** — `graph.py` `build_graph()` and `load_expert_graph()` have zero tests
- **Explanation generation** — `explain.py` logic has zero tests
- **Cross-language analysis** — `cross_language.py` has zero tests
- **Database operations** — `db_init.py` and `db_utils.py` have zero tests
- **Provider system** — `providers/__init__.py` factory has zero tests
- **End-to-end pipeline** — `main.py` has zero tests
- **Data integrity** — no validation that data files conform to expected schemas
- **LDS consistency** — no regression tests for the frozen LDS metric
- **Schema migration** — no tests for database versioning

### Finding 5.4: Test data dependencies are broken

- **Risk**: Tests crash on clean checkout
- **Severity**: HIGH
- **Evidence**:
  - `tests/test_v3_pipeline.py` line 7: `with open('data/survey/v3/example_zh.json')` — this file does NOT exist
  - `tests/test_extraction_validation.py` line 16: `DATA_DIR / "extraction_test.json"` — this file does NOT exist
- **Impact**: These files will crash at import/runtime. A judge cloning the repo will get `FileNotFoundError`.
- **Fix cost**: Low
- **Fix suggestion**: Either create the missing test data files, or add guard clauses that skip tests gracefully with `pytest.skip("test data not found")`.

---

## 6. Documentation for Reproduction

### Finding 6.1: Missing critical setup steps in README

- **Risk**: BWKI judge cannot reproduce results
- **Severity**: CRITICAL
- **Evidence**: README.md "Quick Start" section:
  ```bash
  pip install -r requirements.txt
  python src/main.py
  python scripts/db_init.py
  python -m pytest tests/ -v
  ```
  Missing from this sequence:
  1. **Python version requirement**: Not stated anywhere. Code uses 3.10+ syntax.
  2. **Virtual environment**: Not mentioned.
  3. **Configuration**: No mention of editing `config/config.yaml` or setting environment variables.
  4. **API setup**: No mention of OPENAI_API_KEY, Ollama installation, or mock mode.
  5. **`.env` file**: No `.env.example` exists. No instructions to create one.
  6. **Database initialization order**: `db_init.py` is shown AFTER `src/main.py`, but `main.py` does not use the database. The implication is confusing.
  7. **Data ingestion**: No instruction to run `scripts/ingest_all.py` or populate the database. Running the README commands as shown yields empty results.
  8. **Test expectations**: No information on what passing/failing tests mean or expected count (19 tests, all passing).
  9. **Output interpretation**: No explanation of what `src/main.py` output means or where results are saved.
  10. **Expert graphs**: `src/graph.py` line 69 references `config/expert_graphs/{domain}.json` — this directory does not exist. The `load_expert_graph("calculus")` call will raise `FileNotFoundError` on a clean checkout.

- **Fix cost**: Medium
- **Fix suggestion**: Restructure README "Quick Start" as a numbered, ordered reproduction protocol:

  ```markdown
  ## Reproduction Protocol (for BWKI judges)

  ### Prerequisites
  - Python >= 3.10
  - pip

  ### Step 1: Setup
  git clone <repo>
  cd BWKI-2026-LinguaGraph
  python -m venv .venv
  source .venv/bin/activate  # or .venv\Scripts\activate on Windows
  pip install -r requirements.txt

  ### Step 2: Configure LLM
  # Option A: Free local mode (recommended for review)
  # Install Ollama from https://ollama.com, then:
  #   ollama pull qwen3:8b
  # Edit config.yaml: set provider: ollama, base_url: http://127.0.0.1:11434/v1

  # Option B: Mock mode (no API needed)
  # Edit src/main.py to pass use_mock=True, or run:
  python scripts/demo_mock.py

  # Option C: OpenAI (requires billing)
  # Set OPENAI_API_KEY in .env file

  ### Step 3: Initialize database
  python scripts/db_init.py

  ### Step 4: Ingest demo data
  python scripts/ingest_all.py --demo

  ### Step 5: Run pipeline
  python src/main.py --mock   # mock mode, no API needed

  ### Step 6: Run tests
  python -m pytest tests/ -v
  # Expected: 19 tests pass

  ### Step 7: Verify results
  # Output is saved to output/ directory
  # Database state: python scripts/db_init.py --stats
  ```

### Finding 6.2: Unlisted external data dependencies

- **Risk**: Functionality that references files not in the repo
- **Severity**: HIGH
- **Evidence**:
  - `data/corpus/` (Wikipedia corpus) is listed in project structure but does not exist (empty directory or missing)
  - `data/baseline/` (300 computational baselines) listed but not confirmed
  - `data/questionnaires/` listed but might not be complete
  - `config/expert_graphs/` directory does not exist — `src/graph.py:load_expert_graph()` will fail
  - `config/prompts/extract.md` and `config/prompts/explain.md` exist (good)
  - `data/survey/v3/example_zh.json` is referenced by tests but does not exist
  - `data/extraction_test.json` is referenced by tests but does not exist
- **Impact**: Several code paths crash on clean checkout due to missing data/assets.
- **Fix cost**: Medium
- **Fix suggestion**: (a) Audit every file path referenced in source code and create stubs or fallbacks for missing directories. (b) Add a `scripts/verify_assets.py` that checks all expected files exist and reports status. (c) Document which data files are expected and where they come from.

---

## Overall Reproducibility Score

| Category | Grade | Rationale |
|----------|-------|-----------|
| Path portability | A | Source code is portable (relative paths throughout) |
| Dependency management | C- | Phantom deps, no Python version pin, loose version bounds |
| API independence | D | Mock mode exists but hidden; no graceful fallback |
| Database versioning | F | No schema versioning, no migration path |
| Test suite | D | 19 tests for 15 source files; 4 "test" scripts are not tests; broken test data |
| Documentation | D- | Missing prerequisites, setup steps, data dependencies, config guidance |
| **Overall** | **D** | **Cannot be reproduced by a third party without significant guidance** |

## Action Items (Priority Order)

| Priority | Item | Issue | Est. Cost |
|----------|------|-------|-----------|
| P0 | Fix `config/expert_graphs/` directory | `load_expert_graph()` crashes on line 72 of `graph.py` | 30 min |
| P0 | Fix missing test data files | `test_v3_pipeline.py` and `test_extraction_validation.py` crash | 30 min |
| P0 | Add mock mode to `src/main.py` CMD | `run_pipeline()` has no `--mock` flag | 15 min |
| P1 | Add `.python-version` and Python version to README | Judges on Python 3.8/3.9 crash at import | 5 min |
| P1 | Clean `requirements.txt` of phantom deps | Reduces confusion, 4 unnecessary packages | 10 min |
| P1 | Create `.env.example` | No guidance on API key setup | 5 min |
| P1 | Add DB seed data (`db_init.py --seed`) | Judge runs pipeline, gets empty results | 1 hr |
| P1 | Rename/move non-test scripts out of `tests/` | 4/6 files in tests/ are not tests | 15 min |
| P2 | Add schema version table and migration system | Schema changes between now and Sept destroy data | 2 hr |
| P2 | Rewrite README "Quick Start" as reproduction protocol | Critical for BWKI judging | 1 hr |
| P2 | Add `requirements.lock` with exact versions | Ensures deterministic installs | 10 min |
| P3 | Fallback to mock on ConnectionError in get_provider() | Better first-run experience | 30 min |
| P3 | Add `scripts/verify_assets.py` | Checks all expected files exist | 30 min |
