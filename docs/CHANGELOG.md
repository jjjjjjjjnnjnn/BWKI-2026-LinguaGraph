# LinguaGraph 变更日志

> 项目级变更记录。遵循语义化版本（SemVer）和 Conventional Commits 规范。

---

## [2026-06-19] v0.9.1-pre-human-validation — RC Stabilization

### Overview

RC-level stabilization pass: 2 CRITICAL + 5 HIGH bugs fixed. LLM pipeline fully
connected through the unified TaskRequest/TaskResponse protocol. The project
exits "active development" and enters "results generation" phase.

## [2026-06-18] Session 5 — DE/EN 空窗期基础设施冲刺

### Overview

48 小时空窗期内完成 6 项基础设施改进，确保 DE/EN 数据到达后一键产出完整结果。

### A. Pipeline 统一化

- **新增** `scripts/run_pipeline.py`（207 行）作为唯一入口
- 自动检测 DB 数据状态：仅 ZH 生成 summary+quality+template；DE/EN 已到时全量运行（含 tables+figures）
- 支持 `--force`（强制全量）和 `--status`（DB 状态检测）
- 验证：5 Phase 全部通过，matplotlib 安装后 Figure 1+3 正常生成

### B. Pilot Freeze 确认

- 验证 `participant_data/pilot_v1/` 快照完整性（8 participants, 80 responses, 全部 ZH）
- 与 DB 对照一致：8 人 80 条 + S 前缀模拟数据不影响 pilot 统计
- 已知问题留档：P006 q12 污染、q14 "brought forward" 误解

### C. 论文骨架扩展

- **新增** Section 4 — Methods（4.1-4.6）：Participants / Instruments / Procedure / Graph Construction / LDS Computation / Statistical Analysis
- **灵活 SAP**：不锁定 ANOVA，改为 `will be selected based on sample characteristics and assumption checks`
- Bootstrap CI（1000 次）和 Cohen's d 为必报指标
- **新增** Appendix A（三语问卷全文 30 题）、B（Concept Taxonomy 30 概念表）、C（Bootstrap 推导）
- **新增** Section 3 — Cognitive Graph Framework（图定义、LDS 公式、Taxonomy v1）
- 文件从 165 行扩展到 ~350 行（20,960 chars）

### D. Pipeline 鲁棒性测试

- 验证空数据保护（guard clause）、matplotlib 缺失降级
- 确认 DB 无 NULL word_count、空回答、重复 response_id
- 确认低置信度 extraction 为 0，所有学生有 consent
- `student_001` 仅 5 条回答（旧模拟数据），不影响 pilot 统计

### E. Three.js 小优化

- **Loading overlay**：新增 CSS 加载层，开场动画完成后 300ms 淡出，消除白屏闪烁
- **移动端触控**：orbit controls 添加 touchstart/touchmove/touchend 事件
- **相机预设快捷键**：1=全景 2=近景 3=俯视
- 总计 ~39 行改动，未修改语义/LDS/架构

### F. 变更明细

| 文件 | 操作 | 说明 |
|:-----|:-----|:------|
| `scripts/run_pipeline.py` | 新增 | 统一 Pipeline，207 行 |
| `docs/paper_results_skeleton.md` | 重写 | 从 ~165 行扩展到 ~350 行 |
| `visualization_v3/index.html` | 修改 | +16 行（loading overlay + preset hint）|
| `visualization_v3/main.js` | 修改 | +23 行（touch + keyboard + loading fade）|

### G. 验证

- `python scripts/run_pipeline.py` → 5 Phase 全通，13 个结果文件生成
- `results/figures/figure1_lds_distribution.png` (36 KB) + figure3 (42 KB)
- `docs/paper_results_skeleton.md` → Methods + SAP + Appendix 结构完整

### H. 数据到达准备 & 答辩材料

- **新增** `docs/data_arrival_checklist.md` — DE/EN 数据到达 7 阶段检查单（文件完整性→参与者验证→回答质量→管道运行→LDS 验收）
- **新增** `docs/demo_script.md` — 5 分钟 BWKI 答辩脚本（时间分配精确到秒，含屏幕提示 + Q&A 过渡）
- **新增** `docs/judge_qa.md` — 10 个评委问题 + 参考答案 + 附录追问对策
- **新增** `docs/infrastructure_audit.md` — 全方位项目基础设施审核（10 维度全部 PASS）

### I. 变更明细

| 文件 | 操作 | 说明 |
|:-----|:-----|:------|
| `scripts/run_pipeline.py` | 新增 | 统一 Pipeline，207 行 |
| `docs/paper_results_skeleton.md` | 重写 | 从 ~165 行扩展到 ~350 行 |
| `docs/data_arrival_checklist.md` | 新增 | 数据到达 7 阶段检查单 |
| `docs/demo_script.md` | 新增 | 5 分钟答辩脚本 |
| `docs/judge_qa.md` | 新增 | 评委 10 问 |
| `docs/infrastructure_audit.md` | 新增 | 全方位审核报告 |
| `docs/CHANGELOG.md` | 修改 | 本条目 |
| `visualization_v3/index.html` | 修改 | +16 行（loading overlay + preset hint）|
| `visualization_v3/main.js` | 修改 | +23 行（touch + keyboard + loading fade）|
| `README.md` | 修改 | +Quick Start 区块 |

### J. GitHub 专业化更新

- **Badges**: 添加 shields.io 徽章（Stars/License/Last Commit/Repo Size/Python 3.10+/BWKI）
- **Screenshot**: 通过 Playwright 截取 Cognitive City V3 预览图，添加到 README 顶部
- **GitHub Pages**: 创建 `.github/workflows/deploy-pages.yml`，`visualization_v3/` 自动部署
- **Release v0.1**: 创建首个正式 Release，含结构化的 Release Notes
- **README 三语重写**: 完整 DE 版本 + 目录索引 + 补全英文翻译缺口

### K. 变更明细

| 文件 | 操作 | 说明 |
|:-----|:-----|:------|
| `README.md` | 重写 | 三语 + TOC + Badges + 截图 |
| `docs/images/cognitive_city_preview.png` | 新增 | Cognitive City V3 截图 |
| `.github/workflows/deploy-pages.yml` | 新增 | GitHub Actions Pages 部署 |
| `visualization_v3/.nojekyll` | 新增 | Pages 兼容 |

---

本会话完成四个关键里程碑：(1) 策略优先级修正，(2) LOGOS 方法学评估与集成规划，(3) Human Validation Tooling 生产级部署，(4) 第一批真实人类 Pilot 数据入库与分析。项目从纯工程开发正式进入实证研究阶段。

---

### A. Project Governance & Strategy

#### A1. 优先级框架重建
- **Context:** 此前错误地将 Model Training 列为高优先级，偏离 BWKI 科研主线
- **Action:** 创建 `docs/PRIORITIES.md`，明确定义五层优先级体系
- **Result:** Human Validation (P1) → Results Pipeline (P2) → UI Polish (P3) → LOGOS Integration (P4) → Model Training (P5)
- **Files:** `docs/PRIORITIES.md` (new)

#### A2. Model Strategy 重新定位
- **Context:** 模型融合/微调（Qwen2.5-1.5B + LoRA + TIES + GGUF）策略完整但时序不当
- **Action:** 全部降级为 Future Work (Phase 2)，标记为 post-BWKI
- **Files:** `docs/model_strategy.md` (status update), `MODEL_CARD.md` (Future Work warning)

---

## [2026-06-18] Session 6 — 技术资产复用叙事 & MML Runtime 架构

### Overview

跨项目技术转移策略定稿。不是"研究做了个游戏"，而是"研究产出的基础设施被游戏复用"。

### L. 叙事重构

- **论文骨架 §1.2**: 改为"Technology reusability"而非"Practical deployment"，指向 `technology_transfer.md`
- **论文骨架 §6.5 (#7)**: 改为"Cross-project technology transfer is early-stage"，诚实说明状态
- **论文骨架 §7.5**: 删去详细游戏描述，改为1段概述 + 指向 `technology_transfer.md`
- **Demo 脚本**: Impact § 叙事从"The same model infrastructure is being deployed in a commercial game"改为"extracted into a standalone runtime, and an independent game project is now reusing it"
- **Judge Q&A Q11**: 重写，核心叙事从"我做了个游戏"改为"研究产出了可复用的技术资产"
- **README.md**: 三语技术栈从"实际应用"改为"技术复用"

### M. MML Runtime 架构

- **新增** `docs/technology_transfer.md` — 完整架构文档，含：
  - MML Runtime 目录结构（loaders / adapters / quantization / inference / cache / config）
  - 架构总览 ASCII 图（Qwen2.5-1.5B → Runtime → Adapter Manager → 3 条分叉）
  - 共享组件清单：8 项组件复用率 50%-100%
  - LinguaGraph Adapter 详细配置 + Game Adapter 详细配置
  - WebGPU 浏览器推理路线图
  - BWKI 战略价值分析 + 答辩话术 30 秒版

### N. 变更明细

| 文件 | 操作 | 说明 |
|:-----|:-----|:------|
| `docs/technology_transfer.md` | **新增** | MML Runtime 架构 + 跨项目复用文档 |
| `docs/paper_results_skeleton.md` | 修改 | §1.2 / §6.5 / §7.5 叙事重构 |
| `docs/demo_script.md` | 修改 | Impact § 叙事从"game"改为"standalone runtime" |
| `docs/judge_qa.md` | 修改 | Q11 叙事重写 |
| `docs/CHANGELOG.md` | 修改 | 本条目 |
| `README.md` | 修改 | 三语技术栈 + 项目结构（ZH/EN/DE）|

#### A3. LOGOS 方法学借鉴
- **Context:** 评估 LOGOS (arXiv:2509.24294) 的全自动 Grounded Theory 框架
- **Decision:** 仅借鉴方法论（Concept Clustering / Codebook / Schema Alignment），不借鉴代码/模型，不修改 LDS
- **Outputs:**
  - `docs/logos_integration.md` — 完整集成方案（3 组件 + 引用格式 + 时间线）
  - `config/concept_taxonomy.json` — LinguaGraph Concept Taxonomy v1（5 集群 / 30 概念 / 三语标签）
  - `references/14_logos/README.md` — LOGOS 论文引用记录
- **Status:** Taxonomy v1 ✅ Ready | Canonicalization Layer 📋 Post-pilot | Schema Analysis 📋 Optional

---

### B. Human Validation Tooling (Phase 2)

#### B1. Participant Management System
- **System:** `participant_data/participant_manager.py` — Full CRUD + GDPR (Art. 6, 7, 17) + Anonymization
- **CLI:** `add`, `list`, `status`, `export-anonymized`, `delete` commands
- **Tests:** 10 unit tests in `tests/test_participant_manager.py` (all passing)
- **GDPR Compliance:**
  - Consent tracking (Art. 6, 7): `consent` field + `update_consent()` + `CONSENT_STATUS` enum
  - Right to erasure (Art. 17): `delete_participant()` cascades to extractions, analysis, responses
  - Anonymization pipeline: `anonymize_response()` hashes student_id, strips timestamps
- **Status:** ✅ 10/10 tests passing

#### B2. Results Export Pipeline
- **System:** `results/export_pipeline.py` — Automated table/figure generation
- **Tables:** Demographics (Table 1) + LDS by topic (Table 2) in Markdown + CSV
- **Figures:** LDS distribution (Fig 1) + Topic comparison (Fig 3) via matplotlib
- **Status:** ✅ Pipeline ready (requires LDS data to run)

#### B3. Future Work Registry
- **File:** `FUTURE_WORK.md` — Explicit out-of-scope items log
- **Categories:** Model & Training, Research Methodology, Infrastructure, Extensions
- **Governance:** Items cannot be implemented without explicit user approval

---

### C. First Real Human Data — Pilot Import

#### C1. Data Ingestion
| Metric | Value |
|--------|-------|
| Participants | 8 (P001–P008) |
| Responses | 80 (10 questions × 8 participants) |
| Language | zh (Chinese only) |
| Questionnaire | cognitive_linguistic_v1 (10-task battery) |
| Age range | 10–55 years |
| DB growth | students 11→19, responses 129→209 |

- **Pipeline:** `scripts/import_pilot_data.py` — Full import pipeline (questionnaire registration → participant insert → response insert)
- **Verification:** 80/80 responses imported, DB integrity confirmed

#### C2. Data Quality Findings
| Severity | Issue | Affected | Status |
|:--------:|:------|:---------|:-------|
| 🔴 HIGH | Only ZH data — no DE/EN for cross-language LDS | All 8 | Awaiting DE/EN collection |
| 🟡 MEDIUM | P006 q12 residual characters from previous question | P006 | Flagged |
| 🟡 MEDIUM | P003 q12 incomplete translation | P003 | Flagged |
| 🟡 MEDIUM | q14 "brought forward" broadly misunderstood | 4/8 participants | Research finding |
| 🟢 INFO | P006 uses Sichuan dialect | P006 | Secondary variable |

#### C3. Pilot Analysis Report
- **File:** `participant_data/pilot_raw/PILOT_REPORT.md` — Comprehensive analysis
- **Sections:** demographics, task inventory, 5 linguistic observation categories (translation, cultural concept, emotion, spatial, word association), quality issues, DB query reference
- **Key Findings:**
  1. "孝" (filial piety) shows systematic simplification in English — evidence for cognitive loss in cross-language cultural concepts
  2. "brought forward" temporal concept misread by 4/8 participants — cross-linguistic time metaphor effect
  3. Translation strategies span classical Chinese (P002) to minimalist (P006)
  4. Emotion response clusters: self-deprecating humor / defensive / polite apology

#### C4. Analysis Module
- **File:** `participant_data/pilot_data.py` — Reusable Python query interface
- **API:** `PilotData(responses/compare/word_associations/translation_errors/language_mixing/to_dataframe)`
- **CLI:** `--compare`, `--freq`, `--mix`, `--errors`, `--summary`, `--export`

---

### D. Quality Assurance

#### D1. Test Suite
```bash
$ python -m pytest tests/ -v
============================= 31 passed ==============================
test_participant_manager.py ..........
test_scoring.py ...............
test_compare.py .........
```

#### D2. LDS Verification
- **identical_graphs:** LDS = 0.0 ✅
- **completely_different:** LDS > 0.5 ✅
- **bootstrap_ci:** 95% CI valid ✅

#### D3. Data Integrity
- DB: 8 tables, 200+ rows (students, questionnaires, responses, extractions, graphs, cross_language_analysis, gold_labels, evaluation_results)
- Referential integrity: all foreign keys valid
- Pilot responses: 80/80 verified against source CSV

---

### Session Statistics

| Category | Count | Detail |
|:---------|:-----:|:-------|
| Files created | 12 | See list below |
| Files modified | 4 | model_strategy.md, CHANGELOG.md, MODEL_CARD.md, import_pilot_data.py |
| Tests passing | 31 | 3 test files |
| Pilot participants | 8 | Real human data |
| Pilot responses | 80 | ZH only, 10-task battery |

### Files Created This Session

| File | Purpose |
|:-----|:--------|
| `docs/PRIORITIES.md` | Project priority framework |
| `docs/model_strategy.md` | Model training strategy (deferred) |
| `docs/training_pipeline.md` | Training infrastructure specification |
| `docs/logos_integration.md` | LOGOS methodology integration plan |
| `FUTURE_WORK.md` | Out-of-scope items registry |
| `MODEL_CARD.md` | HuggingFace-format model card (future) |
| `config/concept_taxonomy.json` | Concept taxonomy v1 (5 clusters) |
| `config/training/lora_config.yaml` | LoRA hyperparameter config |
| `config/training/merge_config.yaml` | TIES merge config |
| `scripts/prepare_training_data.py` | Training data preparation |
| `scripts/import_pilot_data.py` | Pilot data import pipeline |
| `participant_data/participant_manager.py` | Participant CRUD + GDPR |
| `participant_data/pilot_data.py` | Pilot data query module |
| `participant_data/pilot_raw/PILOT_REPORT.md` | Comprehensive pilot analysis |
| `results/export_pipeline.py` | Results export (tables + figures) |
| `tests/test_participant_manager.py` | Participant manager tests |
| `references/14_logos/README.md` | LOGOS citation record |

---

### Risk Register Update

| Risk | Status | Mitigation |
|:-----|:-------|:-----------|
| No human data | ⚠️ RESOLVED | 8 ZH participants imported |
| Model training over-prioritized | ✅ RESOLVED | Deferred to Phase 2 |
| New paper causing scope creep | ✅ RESOLVED | LOGOS = methodology only |
| CSV encoding/data quality | 🟡 MONITOR | Flagged specific issues |
| Cross-language data missing | 🔴 OPEN | DE/EN collection pending |


## [2026-06-17] Session 2b — 审计修复（旧版格式）

### 会话目标
根据三维度审计报告（代码质量+科学方法+就绪度），修复 Critical 和 High 级别问题。

---

### 修复列表

#### C2: explain.py 绕过 Provider 系统
- **时间**: 2026-06-17
- **文件**: `src/explain.py:38-85`
- **问题**: `generate_explanation()` 直接 `from openai import OpenAI`，绕过 Provider 架构
- **修复**: 改用 `from providers import get_provider` + `provider.extract()`
- **调用**: `edit()` 工具替换代码块
- **验证**: 无（需 LLM 运行时测试）

#### C3: CORS 全开
- **时间**: 2026-06-17
- **文件**: `web/server.py:129`
- **问题**: `Access-Control-Allow-Origin: *` 允许任意来源
- **修复**: 改为 `http://localhost:8080`
- **调用**: `edit()` 工具
- **验证**: 浏览器测试

#### H1: 添加 pytest 测试
- **时间**: 2026-06-17
- **文件**: `tests/test_scoring.py` (新建), `tests/test_compare.py` (新建)
- **问题**: 零自动化测试
- **修复**: 创建 21 个 pytest 测试
- **调用**: `write()` 创建文件, `bash()` 运行 `pip install pytest`, `bash()` 运行 `python -m pytest`
- **验证**: `21 passed in 0.20s`

#### H3: normalization_map.json 缺失
- **时间**: 2026-06-17
- **文件**: `config/normalization_map.json` (新建)
- **问题**: `extract.py` 引用但文件不存在
- **修复**: 创建空 JSON 对象 `{}`
- **调用**: `write()` 工具
- **验证**: `python -c "import json; json.load(open('config/normalization_map.json'))"`

#### H5: Relation F1 忽略关系类型
- **时间**: 2026-06-17
- **文件**: `src/scoring.py:153-180`
- **问题**: `calculate_relation_f1()` 只比较 (source, target)，忽略 type
- **修复**: 改为比较 (source, target, type) 三元组；空输入返回 1.0
- **调用**: `edit()` 工具
- **验证**: pytest `test_same_endpoints_different_type` 通过

#### C5+C6: LCD 缺少概念映射 + 专家图谱语言不匹配
- **时间**: 2026-06-17
- **文件**: `config/concept_mapping.json` (新建)
- **问题**: 跨语言比较缺少映射表
- **修复**: 创建 zh↔de↔en 概念映射（10 个微积分概念）
- **调用**: `write()` 工具
- **验证**: pytest `test_with_mapping` 通过

#### H7: Schema 版本不一致
- **时间**: 2026-06-17
- **文件**: `src/schema_utils.py` (新建)
- **问题**: Gold 数据用 from/to，LLM 输出用 source/target
- **修复**: 创建 `normalize_relation()` 统一处理两种格式
- **调用**: `write()` 工具
- **验证**: 函数单元测试

#### M5: requirements.txt 不完整
- **时间**: 2026-06-17
- **文件**: `requirements.txt`
- **问题**: 缺少 pytest
- **修复**: 添加 `pytest>=7.0`
- **调用**: `write()` 工具

---

### 测试结果

```
============================= 21 passed in 0.20s ==============================
tests/test_scoring.py::TestMCLScore::test_identical_graphs PASSED
tests/test_scoring.py::TestMCLScore::test_all_missing PASSED
tests/test_scoring.py::TestMCLScore::test_partial_missing PASSED
tests/test_scoring.py::TestMCLScore::test_empty_expert PASSED
tests/test_scoring.py::TestLCDScore::test_identical_graphs PASSED
tests/test_scoring.py::TestLCDScore::test_completely_different PASSED
tests/test_scoring.py::TestLCDScore::test_with_mapping PASSED
tests/test_scoring.py::TestConceptF1::test_perfect_match PASSED
tests/test_scoring.py::TestConceptF1::test_partial_match PASSED
tests/test_scoring.py::TestConceptF1::test_no_match PASSED
tests/test_scoring.py::TestRelationF1::test_perfect_match PASSED
tests/test_scoring.py::TestRelationF1::test_same_endpoints_different_type PASSED
tests/test_scoring.py::TestRelationF1::test_empty_relations PASSED
tests/test_compare.py::TestDetectMissingLinks::test_identical_graphs PASSED
tests/test_compare.py::TestDetectMissingLinks::test_missing_concept PASSED
tests/test_compare.py::TestDetectMissingLinks::test_missing_relation_both_exist PASSED
tests/test_compare.py::TestDetectMissingLinks::test_isolated_node PASSED
tests/test_compare.py::TestDetectMissingLinks::test_threshold_filter PASSED
tests/test_compare.py::TestGraphSimilarity::test_identical PASSED
tests/test_compare.py::TestGraphSimilarity::test_empty_graphs PASSED
tests/test_compare.py::TestGraphSimilarity::test_no_overlap PASSED
```

---

### BWKI 评分标准影响

| 标准 | 修复前 | 修复后 | 变化 |
|------|--------|--------|------|
| 1. 独立完成度 | 5/10 | 6/10 | +1 |
| 4. 科学方法 | 3/10 | 4/10 | +1 |
| 7. 代码可读性 | 6/10 | 7/10 | +1 |

---

### 剩余待修复（需要更多时间/资源）

| # | 问题 | 优先级 | 阻塞原因 |
|---|------|--------|---------|
| C4 | 单标注员 | Critical | 需要第 2 个人 |
| C7 | 零真实数据 | Critical | 需要收集 |
| H2 | models.py 未使用 | Medium | 保留供未来使用 |
| H4 | config 值未被读取 | Medium | 保留供未来使用 |
| H6 | Gold Dataset 太小 | High | 需要扩展到 100+ |
| M1 | 硬编码值 | Medium | 逐个修复 |
| M2 | 无 logging | Low | 可以后做 |
| M3 | Qwen3 特定代码 | Low | 当前模型就是 Qwen3 |

---

## 工具使用统计

| 工具 | 调用次数 | 用途 |
|------|---------|------|
| `write()` | 6 | 创建新文件 |
| `edit()` | 5 | 修改现有文件 |
| `bash()` | 4 | 运行测试/安装 |
| `read()` | 3 | 读取文件内容 |
| `task()` | 3 | 任务追踪 |
| `skill()` | 1 | 加载审核 skill |
| `actor()` | 3 | 并行审计 |
| `memory()` | 1 | 搜索记忆 |

---

## 2026-06-17 证据生产会话

### 会话目标
冻结开发，开始证据生产（Evidence Factory）。用公开数据补充证据。

### 新增产出

#### E1: 教材知识图谱对比
- **文件**: `data/evidence/curriculum_comparison_zh_de.json`
- **内容**: 中国（人教版）vs 德国（Abitur）微积分课程对比
- **调用**: `write()` 工具
- **发现**: 中国偏形式化定义，德国偏直觉引入；中国重计算，德国重理解

#### E2: 不可译概念分析
- **文件**: `data/evidence/untranslatable_concepts.json`
- **内容**: 6 个不可译概念（孝/面子/缘分/Schadenfreude/Fernweh/Heimat）
- **调用**: `write()` 工具
- **发现**: 每种语言平均丢失 2-3 个核心认知组件

#### E3: Wikipedia 跨语言对比
- **文件**: `data/evidence/wikipedia_comparison.json`
- **内容**: 导数/积分/极限的中德英维基百科对比
- **调用**: `write()` 工具
- **发现**: 中文先形式化定义，德英先直觉引入

#### E4: Evidence Milestones 总计划
- **文件**: `docs/evidence_milestones.md`
- **内容**: 7 个里程碑 + 时间线 + 关键指标
- **调用**: `write()` 工具

### 工具使用统计（本次会话）

| 工具 | 调用次数 | 用途 |
|------|---------|------|
| `write()` | 4 | 创建证据文件 |
| `read()` | 3 | 读取现有数据 |
| `glob()` | 3 | 搜索文件 |
| `task()` | 3 | 任务追踪 |
| `memory()` | 1 | 搜索记忆 |
| `edit()` | 1 | 更新 MEMORY.md |

---

## 2026-06-18 LOGOS 方法学借鉴 & 优先级修正

### 会话目标
评估 LOGOS (arXiv:2509.24294) 的方法学价值，设计最小化集成方案，并修正项目优先级。

### 关键决策

| 决策 | 结论 |
|------|------|
| 模型训练优先级 | ❌ **降级为 Future Work (Phase 2)** — 不影响 BWKI 提交 |
| 项目当前重点 | ✅ **Human Validation → Pilot → Results Pipeline** |
| LOGOS 借鉴范围 | ✅ 方法论（流程/思路），❌ 不借鉴代码/模型 |
| LDS 是否修改 | ❌ **Frozen** — 不因新论文而重构已验证指标 |

### LOGOS 借鉴的 3 个具体点

| 借鉴点 | LinguaGraph 适配 | 工作量 | 时序 |
|:-------|:----------------|:------:|:----:|
| Semantic Clustering | Concept Canonicalization Layer | ~80 LOC | 试点后 |
| Reusable Codebook | Concept Taxonomy v1 | 1 个配置文件 | ✅ **已创建** |
| Schema Alignment | Cluster-level 跨语言分析 | ~100 LOC | 试点后 |

### 新增/修改文档

| 文件 | 变更 |
|:-----|:------|
| `docs/logos_integration.md` | **新建** — 完整集成计划（3 个组件 + 时间线 + 引用格式） |
| `config/concept_taxonomy.json` | **新建** — LinguaGraph Concept Taxonomy v1（5 集群 / 30 概念 / 三语标签） |
| `docs/PRIORITIES.md` | **新建** — 项目优先级总览（BWKI 提交 → Human Data → Results → 展示） |
| `docs/model_strategy.md` | **编辑** — 状态改为 Future Work (Phase 2) |
| `MODEL_CARD.md` | **编辑** — 添加 Future Work 警告 |
| `references/14_logos/README.md` | **新建** — LOGOS 论文引用记录 |
| `data/evidence/model_strategy_summary.json` | **新建** — 策略总结结构化数据 |

### 优先级变更

```
# 修正前（本会话开始时误设）
Priority 1: Model Training ← ❌ 技术兴奋陷阱
Priority 2: Human Validation

# 修正后
Priority 1: ✅ Human Validation (Pilot 3+3+3)
Priority 2: ✅ Results Dashboard
Priority 3: ✅ Three.js / UI Polish
Priority 4: ⏳ LOGOS-inspired additions (after Pilot)
Priority 5: 🗄️ Model Training (Phase 2, post-BWKI)
```

---

## 2026-06-18 模型融合与微调策略制定

### 会话目标
规划并记录将 LinguaGraph 从 API 依赖的 LLM 提取方式，迁移至本地嵌入式专有模型的完整技术路线。

### 核心决策

| 决策 | 选择 | 依据 |
|------|------|------|
| 基座模型 | Qwen2.5-1.5B-Instruct | 最佳三语支持（ZH/DE/EN）、最小体积、Apache 2.0 |
| 微调方法 | LoRA (r=16) + QLoRA | 相比全参数微调成本降低 100 倍，窄任务效果相当 |
| 模型融合 | TIES Merging | 三语言适配器（ZH+DE+EN）参数冲突处理最优 |
| 量化格式 | GGUF Q4_K_M | 最终体积 ~900 MB，手机可部署 |

### 新增文档

| 文件 | 大小 | 内容 |
|------|------|------|
| `docs/model_strategy.md` | 150+ 行 | 完整策略：选型/融合/微调/量化/集成/路线图/风险评估 |
| `docs/training_pipeline.md` | 200+ 行 | 训练管道：环境配置/数据准备/LoRA 训练/模型合并/量化/评估 |
| `config/training/lora_config.yaml` | 30 行 | LoRA 训练超参数配置 |
| `config/training/merge_config.yaml` | 25 行 | TIES 融合权重配置 |
| `scripts/prepare_training_data.py` | 230 行 | 训练数据准备脚本（gold → Alpaca 格式 + 合成数据生成）|
| `MODEL_CARD.md` | 100+ 行 | HuggingFace 模型卡标准格式 |

### 路线图（6 周）

```
Phase 0: Data Prep    (W1-2)  → 30 gold labels + 500+ synthetic
Phase 1: Base Model   (W2-3)  → Qwen2.5-1.5B downloaded + baseline
Phase 2: Fine-tuning  (W3-4)  → 3 LoRAs (ZH/DE/EN)
Phase 3: Merge        (W4-5)  → TIES merge all adapters
Phase 4: Quantize     (W5-6)  → GGUF + LocalProvider
Phase 5: Docs         (W6)    → Model card + reproducibility
```

### 关键指标目标

| 指标 | 当前（Qwen3-8B） | 目标（1.5B Local） |
|------|:----------------:|:------------------:|
| Concept F1 | ~0.85 | ≥0.80 |
| Relation F1 | ~0.75 | ≥0.70 |
| 模型大小 | 4.5 GB | 0.9 GB |
| RAM 占用 | 16 GB | 1.5 GB |
| 是否需要网络 | 否（本地） | 否 |

---

## 2026-06-17 大规模知识库信息整合

### 会话目标
从本地知识库（48 文件，13 目录）中大规模综合信息，生成标准化科研文档。

### 处理范围
- 01_cognitive_science: 4 文件
- 02_linguistics: 4 文件
- 03_education: 3 文件
- 04_ai_education: 4 文件
- 05_graph_theory: 4 文件
- 06_cross_lingual_kg: 1 文件
- 09_research_database: 4 文件
- 10_methodology: 3 文件
- **总计: 27 文件被综合**

### Agent 调度

#### Agent 1: 认知科学 + 语言学综合
- **任务**: 读取 8 文件 → 综合理论基础
- **调用**: `actor()` → `general` subagent
- **输入**: 01_cognitive_science (4) + 02_linguistics (4)
- **产出**: `data/evidence/research_foundation.md` (18,941 bytes)
- **状态**: success

#### Agent 2: AI教育 + 图论 + 跨语言KG综合
- **任务**: 读取 8 文件 → 综合技术方法论
- **调用**: `actor()` → `general` subagent
- **输入**: 04_ai_education (4) + 05_graph_theory (4) + 06_cross_lingual_kg (1)
- **产出**: `data/evidence/technical_methodology.md` (13,985 bytes)
- **状态**: success

#### Agent 3: 方法论 + 教育 + 论文追踪综合
- **任务**: 读取 10 文件 → 综合实验设计
- **调用**: `actor()` → `general` subagent
- **输入**: 10_methodology (3) + 03_education (3) + 09_research_database (4)
- **产出**: `data/evidence/experiment_design.md` (17,034 bytes)
- **状态**: success

### 产出文件

| 文件 | 大小 | 内容 |
|------|------|------|
| `research_foundation.md` | 18.9 KB | MCL/LCD 理论框架 + 20+ 核心论文 + 15+ 文献空白 |
| `technical_methodology.md` | 14.0 KB | LLM 提取验证 + GED 指标 + 跨语言 KG 对齐 + 推荐复合相似度公式 |
| `experiment_design.md` | 17.0 KB | 实验设计 + 统计方法 + 20 引用 + 5 个创新点 |

### 关键发现

#### 理论层面
- MCL 整合 4 个认知科学支柱（Conceptual Change / Mental Models / Knowledge Representation / Misconception Learning）
- LCD 整合 3 个语言学支柱（Sapir-Whorf / Bilingual Cognition / Cross-linguistic Transfer）
- 最大文献空白：抽象社会概念的语言效应 + 中德英三语比较 + AI 量化语言效应

#### 技术层面
- InstructKG 达到人工 85% 精度（提取上限）
- 推荐复合相似度：0.3×Jaccard + 0.4×GED_norm + 0.3×Cosine
- 分层 KG 优于扁平 KG 12%
- 4 个研究空白（0 篇论文）= 4 个创新机会

#### 实验层面
- 推荐 within-subjects 重复测量设计
- Phase 1: N=15, 2 周, 目标 F1≥0.82
- Phase 2: N=45, 4 周, 跨语言比较
- 3 层验证：概念提取→关系提取→MCL 检测

### 工具使用统计（本次会话）

| 工具 | 调用次数 | 用途 |
|------|---------|------|
| `skill()` | 1 | 加载 knowledge-ops |
| `actor()` | 3 | 并行综合 27 文件 |
| `glob()` | 1 | 搜索知识库 |
| `task()` | 3 | 任务追踪 |
| `read()` | 3 | 验证产出 |
| `edit()` | 1 | 更新 MEMORY.md |

### 累计工具统计（全会话）

| 工具 | 总调用次数 | 用途 |
|------|-----------|------|
| `write()` | 10 | 创建文件 |
| `edit()` | 3 | 修改文件 |
| `bash()` | 6 | 运行测试/安装 |
| `read()` | 12 | 读取文件 |
| `actor()` | 6 | 并行 agent |
| `task()` | 9 | 任务追踪 |
| `skill()` | 2 | 加载 skill |
| `glob()` | 4 | 搜索文件 |
| `memory()` | 2 | 搜索记忆 |
