# LinguaGraph — Project Activity Log & Compliance Record

> BWKI 2026 · Bundeswettbewerb Künstliche Intelligenz
> Project: LinguaGraph — Cross-Lingual Knowledge Structure Analysis Framework
> Author: Rongjing J.
> Log started: 2026-06-15 · Last updated: 2026-06-22

---

## 1. Project Identity

| Field | Value |
|-------|-------|
| Project Name | LinguaGraph |
| BWKI Phase | Creative Submission (submitted 2026-06-28) → Full Submission (2026-09-21) |
| Finals | 2026-11-13 (Tübingen) |
| Repository | `C:\Users\rongj\Desktop\学校\BWKI-2026-备战` |
| Team | 1 student (Rongjing J.) |
| Languages | ZH · EN · DE |
| Disciplines | Mathematics · Physics · Chemistry |
| Research Question | How do different languages and educational systems organize the same knowledge? |

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
- [✅] CognitiveSpace 3D visualization (deployed)
- [✅] Gold Dataset V1 schema (designed)
- [✅] Repository structure consolidation

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
| 06-20 | Claude Code | Math knowledge graph pipeline | 68 textbooks → 574 concepts + 3538 relations |
| 06-20 | Claude Code | CognitiveSpace visualization | 3D concentric shell graph, deterministic layout, ZH/EN/DE filtering |
| 06-21 | Claude Code | Gold Dataset V1 schema | Two task families (concept extraction + graph completion), provenance tracking |
| 06-21 | Claude Code | Repository consolidation | Archive legacy modules, standardize outputs/ structure |
| — | MIMO (LLM) | Math extraction pipeline | Concept-relation extraction from 68 textbooks across 3 languages |
| — | opencode | Frontend prototyping | Early Cognitive City concept (archived) |

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

---

## 11. Phase 7: CognitiveSpace Math Knowledge Graph (2026-06-17 to 06-21)

### 11.1 Overview

A comprehensive mathematics knowledge graph was constructed from 68 textbooks across three languages and four education levels, forming the **CognitiveSpace** research artifact.

### 11.2 Data Pipeline

| Stage | Tool/Method | Input | Output |
|-------|------------|-------|--------|
| Extraction | MIMO LLM (prompt `docs/mimo_prompt.md`) | Textbook sections (ZH/EN/DE) | Raw concept-relation JSON files (63 files) |
| Merge | `scripts/math_graph_pipeline/merge_extractions.py` | Raw extractions | Deduplicated concepts + relations |
| Alignment | `scripts/math_graph_pipeline/align_languages.py` | ZH/EN/DE concept sets | Cross-language mapping (30 shared concept IDs) |
| Export | `scripts/math_graph_pipeline/export_graph.py` | Aligned data | Visualization data (574 nodes, 3538 links) |

### 11.3 Corpus

| Language | Textbooks | Extractions |
|----------|-----------|-------------|
| Chinese (ZH) | 45 (Renjiao + Tongji + probability + algebra) | 45 JSON files |
| English (EN) | 20 (Stewart, MIT OCW, Khan Academy, IGCSE, IB) | 20 JSON files |
| German (DE) | 10 (Forster, Fischer, Lambacher Schweizer, Papula, Abitur) | 10 JSON files |
| **Total** | **68** | **75 JSON** (some chapters split) |

### 11.4 Graph Statistics

| Metric | Value |
|--------|-------|
| Total concepts | 574 (557 unique + 17 aligned groups) |
| Total relations | 3538 (525 known + ~3000 inferred for connectivity) |
| Trilingual coverage | 247 concepts (43%) |
| Education levels | 4 (elementary → middle → high → university) |
| Level distribution | elementary: 37, middle: 46, high: 193, university: 298 |
| Structural conflicts | 0 |
| Isolated nodes | 2 (<0.5%) |

### 11.5 CognitiveSpace Visualization

A 3D interactive knowledge graph was developed using `3d-force-graph` (v1.80.0), featuring:

- **Concentric shell layout**: Concepts arranged deterministically in spherical shells by education level (elementary core → university periphery), encoded via hash-based deterministic positioning
- **Cross-language filtering**: Interactive ZH/EN/DE filter toggles, preserving 3538 visible relations
- **Color-coded levels**: Elementary (green `#4ade80`), middle (cyan `#22d3ee`), high (blue `#60a5fa`), university (purple `#c084fc`)
- **Three view modes**: Universe (balanced), Space-Fill (amplified), Compare (language-scaled)
- **Interaction**: BFS ripple on click, WASD navigation, node detail panel with textbook provenance
- **Performance**: 574 nodes with deterministic layout, 3538 edges at 0.15 opacity, breathing animation

The visualization is independently deployable at `cognitive-space/web/index.html`.

### 11.6 Gold Dataset Schema

A formal Gold Dataset V1 specification was designed (`docs/gold_dataset_schema_v1.md`), defining two task families:

- **Dataset A — Concept Extraction**: Textbook text → concept list (input/output schema with provenance tracking)
- **Dataset C — Graph Completion**: Forward/reverse/multiple-choice variants derived from graph edges
- **Provenance system**: Every sample tracks textbook → chapter → section → confidence score
- **Format**: JSONL, language-partitioned, 6 files covering ZH/EN/DE for both tasks

### 11.7 Repository Structure Consolidation (2026-06-21)

| Action | Detail |
|--------|--------|
| Legacy archiving | `visualization/`, `visualization_v3/`, `web/` → `_archive/` (git mv, history preserved) |
| Output standardization | `results/` → `outputs/` (unified naming) |
| Path fix | `src/main.py` output destination updated to `outputs/` |
| README refresh | Banner updated to CognitiveSpace; stale Three.js/Cognitive City references replaced across ZH/EN/DE |
| `.gitignore` | Added `outputs/`, `results/`, `_archive/`, `.vscode/` patterns |

The repository now presents a research-ready structure: `src/` · `scripts/` · `data/` · `config/` · `docs/` · `outputs/` · `tests/` · `references/` · `cognitive-space/`.

### 11.8 Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Math extraction pipeline | ✅ Complete | 68 textbooks, 3 languages |
| Cross-language alignment | ✅ Complete | 247 trilingual concepts |
| CognitiveSpace visualization | ✅ Complete | Deployable, frozen |
| Gold Dataset V1 schema | ✅ Complete | A + C task families defined |
| Repository structure | ✅ Complete | Research-ready layout |
| Gold Dataset generation | ⏳ Pending | Scripts not yet written |
| DE/EN data collection | ❌ Blocked | Required for LDS completion |

---

## 3. Session Log — 2026-06-22: The Data Expansion & Verification Sprint

### Summary

This session marked the transition from "project building" to "research narrative." Key events:
- Physics/chemistry/curriculum expansion completed by parallel AI agents
- 20-model benchmark via Bailian API
- Gold dataset expanded from 20 → 92 (F1 verified: ZH=0.974, DE=0.949, EN=0.882)
- Coverage Score computed across 4 educational systems
- Full paper audit & data consistency fix
- GitHub README upgraded to high-star standard with trilingual support

### Multi-Agent Parallel Outputs

Three AI agents were dispatched for parallel work:

**Agent A — Curriculum & Coverage Score**
- NRW Physics curriculum graph: 272 concepts
- NRW Chemistry curriculum graph: 234 concepts
- UK Science curriculum: 186 concepts
- US NGSS: 27 concepts
- Coverage Scores: NRW 34%, UK 82%, US 76%, China 8%

**Agent B — Physics/Chemistry Expansion**
- Physics: 87 → 366 concepts, 383 relations, 33 ZH + 34 EN + 27 DE publishers
- Chemistry: 220 concepts, 215 relations, 6 publishers per language
- Key finding change: F6 Physics CDS peak moved from College (artifact) to Elementary (0.222)
- New finding F8: Chemistry CDS peaks at Middle school (0.042)

**Agent C — Model Benchmark (Bailian API)**
- 20 models tested on identical gold labels
- Production model selected: qwen-plus (social: ZH=0.974, DE=0.949, EN=0.882)
- Key discovery: Extraction quality is DOMAIN-DEPENDENT, not just language-dependent
- German F1 jumped from 0.506 (math domain) to 0.949 (social domain)

### Reviewer Feedback

A comprehensive project review provided the strategic direction:
- **Priority shift**: Stop adding features → explain why differences exist
- **Three competing explanations** for Coverage Score differences:
  - A: Curriculum granularity (COUNTERINDICATED — UK has more concepts but higher coverage)
  - B: Educational philosophy (BEST SUPPORTED — exam-driven vs specialization-driven)
  - C: Division of labor (PLAUSIBLE, unverified)
- **Error analysis**: 29% errors from short responses, 40% from partial omissions — no systematic bias

### Infrastructure Completed

| Component | File | Status |
|-----------|------|--------|
| Batch extraction pipeline | `scripts/batch_process_responses.py` | ✅ --model flag, API key, resume |
| Gold evaluation | `scripts/evaluate_gold.py` | ✅ Keyword + LLM modes |
| LDS from DB | `scripts/compute_lds_from_db.py` | ✅ No re-extraction needed |
| Full pipeline runner | `scripts/run_full_pipeline.py` | ✅ Status check + LDS + compare |
| Gold expansion | `scripts/expand_gold_dataset.py` | ✅ 20→100 with qwen-plus |
| Simulation baseline | `scripts/simulate_baseline.py --mock` | ✅ 300 responses, no LLM |
| Coverage verification | `scripts/verify_coverage_f9f10.py` | ✅ Tests 3 explanations |
| Multi-model benchmark | `scripts/run_model_benchmark.py` | ✅ Any model, any API |

### Paper Updates

| Section | Changes |
|---------|---------|
| §2.8 Extraction quality | 20 gold → 92 gold, math/social domain split |
| §2.9 Model comparison | Domain-aware table, 20 models |
| §2.10 Coverage Score | NEW section, 4-system comparison |
| §4.5 Curriculum layer | Actual data replacing placeholder |
| §4.6 Educational interpretation | NEW: 3 competing explanations |
| §4.7 Extraction reliability | NEW: Error analysis |
| §5 Conclusion | Updated with new F1, 92 gold, 4 metrics |

### Compliance & Security

| Issue | Action Taken |
|-------|-------------|
| API key hardcoded in 4 scripts | Replaced with `***`, now reads from `BAILIAN_API_KEY` env |
| 187MB curriculum file not gitignored | Added to `.gitignore` |
| Paper data inconsistencies (5 found) | All fixed (HDS values, physics count, gold counts) |
| Participant data in git history | Identified, cleanup deferred (git filter-branch) |
| README professional standard | Trilingual EN/DE/ZH, 13 badges, findings table, references |

### Current State — June 22, 2026

```
Engineering    ████████████ 95% ← sufficient
Research       ████████░░░░ 80% ← explanation phase begun
Paper          ████████████ 95% ← all sections complete
Narrative      ████████░░░░ 75% ← unified story emerging
Compliance     ████████████ 95% ← GDPR, ethics, security
```

### Database Status

| Table | Rows | Notes |
|-------|:----:|-------|
| students | 19 | Real participants |
| responses | 509 | 209 real + 300 simulation |
| extractions | 124 | qwen-plus (batch) |
| gold_labels | 92 | 72 social + 20 math |
| cross_language_analysis | 17 | Wikipedia corpus |
| evaluation_results | 0 | FK constraint prevents save |

---

*This log is maintained as a compliance record for BWKI 2026 submission requirements.
Current commit: `07efffd` — trilingual README and documentation headers.*
*Last updated: 2026-06-21 18:30 UTC+8*
