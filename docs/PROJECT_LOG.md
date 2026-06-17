# LinguaGraph — Project Activity Log & Compliance Record

> BWKI 2026 · Bundeswettbewerb Künstliche Intelligenz
> Project: LinguaGraph — Mapping How Language Shapes Thinking
> Student: [Name], [School], [Grade]
> Log started: 2026-06-15 · Last updated: 2026-06-17

---

## 1. Project Identity

| Field | Value |
|-------|-------|
| Project Name | LinguaGraph |
| BWKI Phase | Idea Submission (deadline 2026-06-28) |
| Full Submission | 2026-09-21 |
| Finals | 2026-11-13 (Tübingen) |
| Repository | `C:\Users\rongj\Desktop\学校\BWKI-2026-备战\02-项目规划` |
| Team | 1 student + 1 partner (linguistics) + 3 advisors |

---

## 2. Development Timeline

### Phase 0: Project Foundation (2026-06-15)

| Date | Action | Artifact | Status |
|------|--------|----------|--------|
| 06-15 | Project directory created | `BWKI-2026-备战/` with README | ✅ |
| 06-15 | 6 subdirectories created | 01-比赛信息 through 06-代码模板 | ✅ |
| 06-15 | LinguaGraph v4.0 planning | `LinguaGraph-项目计划-v4.0.md` | ✅ |
| 06-15 | Workflow v4 defined | `workflow-v4.md` | ✅ |
| 06-15 | Partner task list v4 | `伙伴任务清单-v4.md` | ✅ |
| 06-15 | Social issues graph created | `expert_graph/social_issues_graph.json` (17 concepts) | ✅ |
| 06-15 | Trilingual questionnaires created | `data/questionnaires/` (ZH/DE/EN) | ✅ |

### Phase 1: Core Pipeline (2026-06-15 to 06-16)

| Date | Action | Artifact | Status |
|------|--------|----------|--------|
| 06-15 | Source modules created | `src/extract.py`, `graph.py`, `compare.py` | ✅ |
| 06-16 | Cross-language module | `src/cross_language.py` (4 gap types) | ✅ |
| 06-16 | Scoring functions | `src/scoring.py` (MCL, LCD, F1) | ✅ |
| 06-16 | Explanation module | `src/explain.py` | ✅ |
| 06-16 | Gold dataset (21 entries) | `data/gold/gold_dataset.json` | ✅ |
| 06-16 | Schema validation | `schema_v1.json`, `validate_schema.py` | ✅ |
| 06-16 | Full pipeline v1 | `pipeline_v1.py` | ✅ |
| 06-16 | Prompt v2 designed | `prompt_v2.py`, `prompt_v2_guide.md` | ✅ |
| 06-16 | Project structure doc | `项目结构-v4.md` | ✅ |
| 06-16 | Change log started | `docs/CHANGELOG.md` | ✅ |
| 06-16 | Web frontend (Three.js) | `web/index.html` (541 lines, 3D graph vis) | ✅ |
| 06-16 | Evaluation framework | `evaluation.py` (Concept F1, Relation F1) | ✅ |
| 06-16 | Provider abstraction | `src/providers/base.py`, `ollama.py`, `openai.py` | ✅ |

### Phase 2: Audit & Fix Cycle (2026-06-17, Session 1)

| Time | Action | Artifact | Classification |
|------|--------|----------|---------------|
| 08:00 | 3D audit report generated | Code + Science + Readiness audit | Audit |
| 08:30 | Fix C2: explain.py bypassing Provider | `src/explain.py` rewritten | 🔴 CRITICAL |
| 09:00 | Fix C3: CORS wildcard | `web/server.py:129` restricted to localhost | 🔴 CRITICAL |
| 09:15 | Fix H1: add pytest (21 tests) | `tests/test_scoring.py`, `test_compare.py` | 🟡 HIGH |
| 09:30 | Fix H3: create normalization_map.json | `config/normalization_map.json` | 🟡 HIGH |
| 09:45 | Fix H5: Relation F1 ignore type | `src/scoring.py:153-180` triple comparison | 🟡 HIGH |
| 10:00 | Fix C5+C6: concept mapping | `config/concept_mapping.json` created | 🔴 CRITICAL |

### Phase 3: Database & Data Pipeline (2026-06-17, Session 2)

| Time | Action | Artifact | Status |
|------|--------|----------|--------|
| 10:30 | Agent collaboration infra | `.claude/CLAUDE.md`, settings.json, 3 memory files | ✅ |
| 11:00 | SQLite database | `db_init.py` (9 tables, 11 indices) | ✅ |
| 11:15 | DB utilities | `db_utils.py` (query, insert, export) | ✅ |
| 11:30 | Questionnaires import | `ingest_questionnaires.py` (3 questionnaires) | ✅ |
| 11:45 | Student data import | `ingest_student_data.py` (1 student) | ✅ |
| 12:00 | Gold labels import | `ingest_gold_labels.py` (20 labels) | ✅ |
| 12:15 | Expert graphs import | `ingest_expert_graphs.py` (3 graphs) | ✅ |
| 12:30 | Survey entry CLI | `survey_entry.py` (4 subcommands) | ✅ |
| 12:45 | Data validation | `validate_data.py` (6 check types) | ✅ |
| 13:00 | Batch import | `ingest_all.py` (one-click) | ✅ |

### Phase 4: Config Migration & Analysis Pipeline (2026-06-17, Session 3)

| Time | Action | Artifact | Status |
|------|--------|----------|--------|
| 13:15 | Config: social_issues domain | `config.yaml` updated | ✅ |
| 13:20 | Concept mapping expanded | `config/concept_mapping.json` (30+ social concepts) | ✅ |
| 13:25 | Extract prompt updated | `config/prompts/extract.md` (social issues) | ✅ |
| 13:30 | Student analysis pipeline | `analyze_student.py` (DB→extract→graph→compare→save) | ✅ |
| 13:35 | Evaluation pipeline | `evaluate_pipeline.py` (F1 extraction quality) | ✅ |

### Phase 5: Pilot Study (2026-06-17, Session 4)

| Time | Action | Artifact | Status |
|------|--------|----------|--------|
| 14:00 | Freedom corpus (ZH/DE/EN) | `data/pilot_corpus/freedom/` | ✅ |
| 14:10 | Concept analysis script v1 | `research/analyze_freedom.py` | ❌ Replaced |
| 14:20 | Cross-language mapping v1 | `config/cross_language_mapping.json` (created) | ✅ |
| 14:30 | Freedom v1 results | LCD=1.00 (artifact) | ❌ Fixed |
| 14:40 | Cross-language mapping fixed | `config/cross_language_mapping.json` (Gerechtigkeit fix) | ✅ |
| 14:45 | v2: fixed concept mapping | `research/analyze_freedom_v2.py` | ✅ |
| 14:50 | v2 results (corrected) | Freedom LCD: zh-en=0.614, zh-de=0.821, de-en=0.872 | ✅ |
| 15:00 | Justice corpus + analysis | `data/pilot_corpus/justice/` + analysis | ✅ |
| 15:10 | Responsibility corpus + analysis | Same structure | ✅ |
| 15:15 | Success corpus + analysis | Same structure | ✅ |

### Audit 2: Code Review & Research Audit (2026-06-17, Session 5)

| Issue | Finding | Severity | Fix |
|-------|---------|----------|-----|
| C1 | Substring matching: "Freiheit" in "Willensfreiheit" | 🔴 CRITICAL | Word-boundary regex for DE/EN |
| C2 | LCD redundant for complete graphs | 🔴 CRITICAL | Co-occurrence-based graphs |
| C3 | Gerechtigkeit collision (equality AND justice) | 🔴 CRITICAL | Removed from equality |
| H1 | validate_data.py indentation bug | 🟡 HIGH | Fixed loop indentation |
| H2 | quality flag "empty" unreachable | 🟡 HIGH | Reversed condition order |
| H3 | English "right" keyword too generic | 🟡 MEDIUM | Removed bare "right" |
| H4 | load_article pattern too permissive | 🟡 MEDIUM | Tightened to {lang}_*.txt |
| H5 | Duplicate "权力" in power mapping | 🟡 MEDIUM | Removed duplicate |

### Phase 6: Experiment Design & Ethics (2026-06-17, Session 6)

| Time | Action | Artifact | Status |
|------|--------|----------|--------|
| 15:30 | Experiment design | `research/experiment_design.md` | ✅ |
| 15:35 | Research rules | `research/RESEARCH_RULES.md` | ✅ |
| 15:40 | Top Drift Ranking | `research/findings/top_drift_concepts.md` | ✅ |
| 15:45 | LDS Stability Report | `research/findings/lds_stability_report.md` | ✅ |
| 15:50 | Cognitive City data (v2) | `research/visualization/cognitive_cities_v2.json` | ✅ |
| 16:00 | Questionnaire validation | `docs/questionnaire_validation.md` | ✅ |
| 16:10 | Project audit | `docs/project_audit.md` | ✅ |
| 16:15 | Annotation Guideline v2 | `docs/annotation_guideline_v2.md` (20 examples, κ workflow) | ✅ |
| 16:20 | BWKI Paper Outline | `docs/bwki_paper_outline.md` (10 sections, ~55% complete) | ✅ |
| 16:25 | Ethics Package (7 docs) | `docs/ethics/consent_zh/de/en.md`, `gdpr_package.md` | ✅ |
| 16:30 | Creative submission materials | `docs/creative_submission.md` | ✅ |
| 16:35 | Pilot analysis template | `scripts/analyze_pilot.py` | ✅ |
| 16:40 | Annotator agreement analysis | `scripts/annotator_agreement.py` | ✅ |
| 16:45 | Simulation protocol | `docs/simulation_protocol.md` | ✅ |
| 16:50 | Simulation pipeline | `scripts/simulate_baseline.py` | ✅ |
| 16:55 | Human vs Model comparison | `scripts/compare_human_vs_model.py` | ✅ |

---

## 3. Source Compliance Record

### 3.1 Wikipedia Corpus Attribution Status

| File | Source | Attribution | License | Compliance |
|------|--------|-------------|---------|------------|
| `data/pilot_corpus/*/zh_*.txt` | zh.wikipedia.org | ❌ Missing | CC-BY-SA 4.0 | ❌ FAIL |
| `data/pilot_corpus/*/de_*.txt` | de.wikipedia.org | ❌ Missing | CC-BY-SA 4.0 | ❌ FAIL |
| `data/pilot_corpus/*/en_*.txt` | en.wikipedia.org | ❌ Missing | CC-BY-SA 4.0 | ❌ FAIL |
| `data/gold/gold_dataset.json` | Manually annotated | ✅ N/A | Original | ✅ PASS |
| `data/questionnaires/*.json` | Original design | ✅ N/A | Original | ✅ PASS |
| `data/evidence/*.md` | KB synthesis | ⚠️ Informal refs | Internal | ⚠️ WARN |
| `expert_graph/*.json` | Original construction | ✅ N/A | Original | ✅ PASS |

**Action Required**: Add CC-BY-SA header to all 12 Wikipedia corpus files before BWKI submission.

### 3.2 Ethics & Data Privacy Compliance

| Requirement | Status | Document |
|-------------|--------|----------|
| GDPR Art. 13: Information obligation | ✅ Complete | `docs/ethics/gdpr_package.md` |
| GDPR Art. 7: Consent | ✅ ZH/DE/EN available | `docs/ethics/consent_*.md` |
| GDPR Art. 17: Right to erasure | ✅ Template ready | `docs/ethics/gdpr_package.md` |
| GDPR Art. 8: Minor consent (<16) | ✅ Parental consent form | `docs/ethics/gdpr_package.md` |
| DSGVO §4: Aufklärungspflicht | ✅ DE version available | `docs/ethics/consent_de.md` |
| Data retention policy | ✅ Defined (12 months) | `docs/ethics/gdpr_package.md` |
| Breach notification procedure | ✅ Defined (72h) | `docs/ethics/gdpr_package.md` |

**Note**: All [Name] and [Email] placeholders must be filled before participant recruitment.

---

## 4. Code Repository Status

### 4.1 Code Inventory

| Directory | Python Files | Lines of Code | Coverage |
|-----------|-------------|---------------|----------|
| `src/` | 11 | ~3,100 | Core pipeline |
| Root scripts | 20 | ~50,000 | Pipeline + tools |
| `research/` | 4 | ~36,000 | Analysis scripts |
| `tests/` | 6 | ~28,000 | pytest tests |
| `scripts/` | 3 | ~19,000 | New tooling |
| **Total** | **~44** | **~136,000** | |

### 4.2 Git Status

| Aspect | Status | Action Needed |
|--------|--------|---------------|
| Repository initialized | ❌ Not done | `git init` before human data collection |
| .gitignore | ✅ Exists | `02-项目规划/.gitignore` |
| First commit | ❌ Not done | After ethics package is filled in |

---

## 5. Key Metrics Over Time

| Metric | 06-15 | 06-16 | 06-17 | Target |
|--------|-------|-------|-------|--------|
| Python files | ~15 | ~35 | ~44 | — |
| Test count | 0 | 21 | 21 | 30+ |
| Database tables | 0 | 0 | 9 | 9 |
| Gold labels | 0 | 21 | 21 | 100+ |
| Cross-lang analysis records | 0 | 0 | 15 | 90+ |
| Wiki corpus (files) | 0 | 0 | 12 | 12 (frozen) |
| Concepts analyzed | 0 | 0 | 4 | 4 (frozen) |
| Ethics documents | 0 | 0 | 7 | 7 |
| Experiment design docs | 0 | 0 | 15+ | — |

---

## 6. Current Lock Status

As of 2026-06-17, the following are **FROZEN** per project rules:

- [🔒] Corpus expansion — no more Wikipedia/textbook scraping
- [🔒] New concept analysis — no more topics beyond the 5 selected
- [🔒] LDS/LCD algorithm changes — no metric modifications
- [🔒] Pipeline refactoring — no architecture changes
- [🔒] New analysis module development

The following are **ACTIVE**:

- [✅] Human participant recruitment
- [✅] Pilot data collection (9 people)
- [✅] Second annotator recruitment
- [✅] Creative submission (due 06-28)
- [✅] Three.js Cognitive City demo

---

## 7. Data Flow Diagram

```
Wikipedia Articles (12 files, 4 topics × 3 languages)
    │
    ├──→ Keyword Extraction (with mapping layer)
    │       │
    │       └──→ Co-occurrence Graph → LDS → Ranking
    │
    ├──→ (Pilot corpus, stored in data/pilot_corpus/)
    │
    ├──→ Gold Labels (21 responses, manually annotated)
    │       │
    │       └──→ F1 Evaluation of LLM extraction
    │
    ├──→ Questionnaires (5 topics × 3 languages)
    │       │
    │       ├──→ Human responses (when collected) → Analysis
    │       └──→ Simulation responses (LLM persona) → Baseline
    │
    └──→ Cognitive City JSON (for Three.js visualization)
```

---

## 8. Compliance Checklist (For BWKI Submission)

- [ ] All Wikipedia corpus files have CC-BY-SA attribution headers
- [ ] Consent forms have [Name] and [Email] filled in
- [ ] Git repository initialized with first commit
- [ ] Hardcoded paths in archived scripts replaced
- [ ] Full bibliography formatted (Tier 1-3 papers)
- [ ] Pipeline diagram created for paper
- [ ] Three.js Cognitive City demo runnable
- [ ] 9-person pilot completed
- [ ] Second annotator trained (κ ≥ 0.70)
- [ ] Creative submission uploaded by 06-28

---

## 9. Agent Collaboration Log

| Date | Agent | Role | Outcome |
|------|-------|------|---------|
| 06-16 | Claude Code | Pipeline development | extract/graph/compare/scoring built |
| 06-17 | Claude Code | Database infrastructure | SQLite + 6 ingestion scripts |
| 06-17 | Claude Code | Pilot study | 4 concepts analyzed, LDS ranking |
| 06-17 | Claude Code | Code review | 8 issues identified and fixed |
| 06-17 | Claude Code | Experiment design | Full protocol + ethics package |
| 06-17 | Claude Code | Submission materials | Abstracts, scripts, outlines |
| — | opencode | Frontend (pending) | Cognitive City Three.js |
| — | mimo code | Backend/vis (pending) | Simulation + visualization |

---

*This log is maintained as a compliance record for BWKI 2026 submission requirements.*
*Last updated: 2026-06-17 18:00 UTC+8*

---

## 10. Simulation Baseline Status

| Component | Status | Detail |
|-----------|--------|--------|
| Template (300 slots) | ✅ Ready | `data/pilot_corpus/simulation/simulation_template.json` |
| Batch 1 (success + freedom) | ⏳ Unfilled | 120 responses → `--batch 1` |
| Batch 2 (responsibility + justice) | ⏳ Unfilled | 120 responses → `--batch 2` |
| Batch 3 (home) | ⏳ Unfilled | 60 responses → `--batch 3` |
| DB isolation | ✅ Designed | `source='simulation'`, `student_id='SIMULATION'` |
| Persona prompts | ✅ Documented | `docs/simulation_protocol.md` |
| Comparison analysis | ✅ Ready | `scripts/compare_human_vs_model.py` → Spearman ρ |

### Run Order (when ready)
```bash
python scripts/simulate_baseline.py --batch 1   # 120 responses
python scripts/simulate_baseline.py --batch 2   # 120 responses
python scripts/simulate_baseline.py --batch 3   # 60 responses
python scripts/simulate_baseline.py --pipeline  # Run analysis
python scripts/compare_human_vs_model.py --report  # Compare with human data (when available)
```
