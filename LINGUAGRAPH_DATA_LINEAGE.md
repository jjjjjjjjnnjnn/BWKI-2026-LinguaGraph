# LinguaGraph — Data Lineage & Impact Analysis

> 生成: 2026-06-29 | 版本: 2.0 (从数据清单升级为数据依赖地图)
> 用途: 每次数据更新时查阅，确认影响范围并按 SOP 执行

---

## 三条原则（驱动本文件所有设计）

```
P1 — SSOT:           manifest.json 是唯一数字来源
P2 — Immutable:      release/ 目录是不可修改的快照
P3 — Validated:      所有结果必须通过 release.py 验证
```

本文件中的 Data Lineage、Impact Analysis、SOP 都是这三条的实现细节。

---

## 1. 架构红线

### 单源真理 (Single Source of Truth)

| 资产 | 唯一源 | 副本处理 |
|------|--------|----------|
| Pipeline 脚本 | `scripts/math_graph_pipeline/` | `cognitive-space/scripts/math_graph_pipeline/` = **import wrapper** (2026-06-29 已消除双目录) |
| Level 推断 | `merge_extractions.py` (LEVEL_RULES 字典) | 通过 `align_languages.py` 前向传播，export 严禁二次推断 |
| CROSS_LANG_MAP | `align_languages.py` (~150 条) | `config/cross_language_mapping.json` 为辅助映射文件 |
| **Manifest** (数字来源) | `manifest.json` | 由 `generate_manifest.py` 自动生成，`release.py` 流程最后一步 |
| Schema 版本 | `data_schema_version = "2.1.0"` | 内嵌于 `manifest.json` + `visualization_data.json` + `aligned_data.json` |

### Pipeline 调用图

```
project root
  python scripts/release.py                         ← 统一入口
    ├── run_pipeline.py (merge → align → export → validate)
    ├── quality_report.py (metrics + gates + diff)
    ├── gate check (PASS → continue, FAIL → stop)
    ├── export data.js + deploy
    ├── generate_manifest.py (manifest.json)
    └── assemble release/ bundle

  python scripts/math_graph_pipeline/run_pipeline.py
    ├── merge_extractions.py   (canonical)
    ├── align_languages.py     (canonical)
    ├── export_graph.py        (canonical)
    └── validate_pipeline.py   (canonical)

cognitive-space 目录
  python cognitive-space/scripts/math_graph_pipeline/*.py
    └── import wrappers → 全部委托到 canonical

质量报告
  python scripts/quality_report.py     ← 独立于 pipeline, 读取已生成的数据
  python scripts/generate_manifest.py  ← 读取所有数据, 生成 manifest.json
```

---

## 2. 数据流 (Data Lineage)

### 2.1 Raw Data (原始输入)

```
data/textbook/ (93 files)
  └── zh/ 小学数学_*.txt, 初中数学_*.txt, 必修*.txt, 选修*.txt, 线性代数*.txt, ...
  └── en/ ap_calculus_ab_bc.txt, ib_math_aa_sl.txt, stewart_ch*.txt, ...
  └── de/ westermann_9-10.txt, lambacher_5-8*.txt, fischer_lineare_algebra*.txt, ...

data/gold/gold_dataset.json (92 条)
data/questionnaires/ (已冻结)
data/evidence/ (研究证据)
linguaGraph.db (SQLite, 438K)
```

**更新触发器**: 添加新教材、修改教材提取文本、更新 Gold 标注
**影响范围**: pipeline 全流程（merge → align → export → validate）

---

### 2.2 Intermediate (中间数据)

```
merge_extractions.py ──→ merged_concepts.json  (557 concepts)
                       ──→ merged_relations.json (525 relations)
                       ──→ merge_report.txt

align_languages.py ────→ aligned_data.json
                          ├── aligned_groups (219, trilingual)
                          ├── unmatched_concepts (359)
                          └── relations
```

**更新触发器**: 运行 pipeline（Step 1-2）
**影响范围**: 所有下游产出

---

### 2.3 Artifacts (输出数据)

```
export_graph.py ──────→ visualization_data.json   (556 nodes, 238 links)
                      ──→ config/expert_graphs/*.json (per-domain + math_full)
                      ──→ cognitive-space/web/data.js (380 KB, JS wrapper)

validate_pipeline.py ──→ pipeline_snapshot.json

scripts/quality_report.py ──→ data/quality_history/quality_report_*.json
                            ──→ data/quality_history/quality_report_latest.json
```

**更新触发器**: 运行 pipeline（Step 3-4）
**影响范围**: 可视化、门户、部署

---

### 2.4 Visualization (可视化消费端)

```
cognitive-space/web/data.js        ← 从 visualization_data.json 转换
cognitive-space/web/index.html      ← 3D 查看器
cognitive-space/web/i18n.js         ← 三语翻译
cognitive-space/portal/index.html   ← 研究门户
cognitive-space/web/story/index.html ← 叙事页面
```

**更新触发器**: pipeline 运行后 + data.js 重新生成
**影响范围**: 所有面向用户的可视化

---

### 2.5 Deployment (发布)

```
_deploy/data.js             ← mirror of cognitive-space/web/data.js
_deploy/index.html          ← mirror of cognitive-space/web/index.html
_deploy/portal/index.html   ← mirror of cognitive-space/portal/index.html
_deploy/story/index.html    ← mirror of cognitive-space/web/story/index.html
_deploy/docs/               ← mirror of docs/
_deploy/figures/            ← mirror of figures/
```

**更新触发器**: 所有修改后
**验证**: MD5 一致性检查 (`scripts/quality_report.py` 自动比较)

---

### 2.6 Derived Analytics (派生分析)

```
outputs/structures-complete-level-*.json   ← 若 graph 数据更新则需重算
research/findings/coverage_findings.json    ← 若覆盖度重算
evaluation/reports/extractor_comparison.json ← 若提取器更新
```

**注意**: `outputs/human_pilot_*.json`, `research/findings/gold_evaluation.json`,
`research/findings/bailian_benchmark*.json` 等项目**独立于数学图管线**，不受 pipeline 更新影响。

---

## 3. Impact Analysis (影响分析)

### 3.1 变更 → 必重新运行

| 修改内容 | 必须重新运行 | 可以跳过 |
|----------|-------------|----------|
| 修改教材摘录文本 | merge → align → export → validate → data.js → deploy | 分析/论文结果不直接变（仅 graph 数据变） |
| 添加新课标/新提取文件 | merge → align → export → validate → data.js → deploy → quality_report | 同上 |
| 修改 ALIAS_GROUPS | merge → align → export → validate → data.js → deploy | 不需要重新抓取原始教材 |
| 修改 CROSS_LANG_MAP | align → export → validate → data.js → deploy | merge 可跳过（concept 未变） |
| 修改 LEVEL_RULES | merge → export → validate → data.js → deploy | align 可跳过（若 concept 未变） |
| 修改 export_graph.py 格式 | export → validate → data.js → deploy | merge → align 完全不需要 |
| 修改 validate_pipeline.py 门控 | validate → 更新 snapshot | 数据全部不变 |
| 修改 quality_report.py 指标 | quality_report | 数据全部不变 |
| 修改 3D Viewer (index.html) | deploy + UI 测试 | 数据分析全部跳过 |
| 修改颜色/样式 | deploy + UI 验证 | 统计/管线全部跳过 |
| 修改分析算法 (scoring.py) | findings / evaluation / figures | merge/align/export 不需要 |
| 修改 portal 文字/翻译 | deploy | 数据全部不变 |

### 3.2 阈值 — 超阈值需人工复核

| 指标 | 周阈值 | 月阈值 |
|------|--------|--------|
| 节点数变化 | >3 或 >10% | — |
| 链接数变化 | >3 或 >10% | — |
| 对齐组数变化 | >3 或 >10% | — |
| 级别分布变化 (单级) | >5 或 >15% | — |
| data.js MD5 变化 | 任何变化 | — |
| 图密度变化 | >0.0005 | — |
| 度=0 节点数变化 | >5% | — |
| P95 度变化 | >2 | — |
| 三语覆盖率下降 | >0% | >0% |

---

## 4. 标准操作流程 (SOP)

### 完整发布流程（推荐）

```bash
# 推荐：一条命令完成全流程
python scripts/release.py
# 内部执行链：pipeline → quality_report → gates → export → deploy → manifest → bundle

# 跳过 pipeline（已有数据，仅重新检查和部署）
python scripts/release.py --skip-pipeline

# 预览模式（不写文件）
python scripts/release.py --dry-run --skip-pipeline

# 分步执行（用于调试）
python scripts/math_graph_pipeline/run_pipeline.py
python scripts/quality_report.py --check-quality-gates
python scripts/generate_manifest.py
```

### 质量报告解读
# 方案 C: 仅修改了 level 规则 (LEVEL_RULES)
#   → 部分流程 (merge → export → validate, 跳过 align)
#
# 方案 D: 仅修改了导出格式 (export_graph.py)
#   → 最小流程 (export → validate, 跳过 merge → align)

# === Step 1: 运行 pipeline ===
python scripts/math_graph_pipeline/run_pipeline.py

# === Step 2: 更新 data.js (3D 查看器数据) ===
python -c "
import json, pathlib
vis = json.loads(pathlib.Path('data/math_extractions/merged/visualization_data.json').read_text(encoding='utf-8'))
js = '// CognitiveSpace - 3D Knowledge Graph Data\n'
js += 'var data = ' + json.dumps(vis, ensure_ascii=False, indent=2) + ';\n'
pathlib.Path('cognitive-space/web/data.js').write_text(js, encoding='utf-8')
"

# === Step 3: 更新 deploy 镜像 ===
cp cognitive-space/web/data.js _deploy/data.js

# === Step 4: 生成质量报告 ===
python scripts/quality_report.py --check-quality-gates

# === Step 5: 检查分析结果 ===
# 如果 quality report 显示超过阈值的变化，检查相关分析文件
# 如果节点数/链接数变化 >10%，重新生成论文图表
# python scripts/generate_paper_figures.py  # 按需
```

### 质量报告解读

每次运行 `python scripts/quality_report.py` 或 `python scripts/release.py` 后：

1. **Gate 1-4 全部 PASS** → 数据完整性 OK
2. **diff 为空** → 与上一版无显著变化
3. **diff 出现 WARN** → 人工审查变化来源
4. **degree_zeros 变化 >5%** → 大量节点脱链，检查 export 逻辑
5. **graph_density 剧烈变化** → 节点/链接比例失调
6. **MD5 变化但指标不变** → 输出格式/顺序变化，无害

---

## 5. Manifest (数字单源真理)

`manifest.json` 是项目所有聚合数字的唯一来源。

| 消费者 | 读取路径 |
|--------|----------|
| Portal | `manifest.json` 中的 graph/alignment 数字 |
| Paper | `manifest.json` 确保论文数字与代码一致 |
| Release | `release/manifest.json` 随发布包分发 |
| README | 可引用 `manifest.json` 的数字 |

### 字段表

```
schema_version         = "1.0.0"       ← manifest 自身 schema
data_schema_version    = "2.1.0"       ← 数据输出 schema
provenance.git_commit  = "60b3020"     ← 生成时的 git commit
provenance.build_time  = "2026-06-29T10:54:28"
graph.total_nodes      = 556           ← 论文/门户一致
alignment.trilingual   = 219 (100%)
checksums.data.js      = "9b0480..."
```

### Schema 版本策略

| 文件 | schema 字段 | 当前版本 | 何时加号 |
|------|-----------|---------|---------|
| `visualization_data.json` | `schema_version` | `2.1.0` | 字段增删 |
| `aligned_data.json` | `schema_version` | `2.1.0` | 字段增删 |
| `manifest.json` | `schema_version` | `1.0.0` | 结构变化 |
| `data.js` | 继承自 `visualization_data.json` | 同源 | 无需单独版本 |

---

## 6. Release Bundle

每次 `python scripts/release.py` 生成 `release/` 目录：

```
release/
├── manifest.json                (1.2 KB, 单源真理)
├── data.js                      (380 KB, 3D 查看器)
├── data/
│   ├── visualization_data.json  (429 KB)
│   └── aligned_data.json        (936 KB)
├── report/
│   ├── release_report.md        (1 KB, 人类可读)
│   └── quality_report.json      (2 KB, 结构化指标)
└── checksums.txt                (6 条目, MD5)
```

任何人都可以在一次 `git clone` + `release/` 后获得与研究一致的精确数据。

---

## 7. 质量门控标准 (Quality Gates)

| 门控 | 条件 | 失败时应检查 |
|------|------|-------------|
| Gate 1 (唯一性) | 所有节点 ID 唯一 | export_graph.py 的 dedup guard |
| Gate 2 (Level 一致性) | 所有 align group 携带 level | align_languages.py 的 level 前向传播 |
| Gate 3 (三语完整性) | 所有 align group 有 zh/en/de | CROSS_LANG_MAP 和 align 逻辑 |
| Gate 4 (快照漂移) | 节点/链接/级别变化 < 10% 或 < 3 | 审查 pipeline 变动来源 |

---

## 8. 当前基线 (2026-06-29)

| 指标 | 值 |
|------|-----|
| Nodes | 556 |
| Unique IDs | 556 |
| Duplicate IDs | 0 |
| Links | 238 |
| Graph Density | 0.001543 |
| Avg Degree | 0.856 |
| Median Degree | 0 |
| P95 Degree | 5 |
| Max Degree | 20 |
| Degree=0 | 381 (68.5%) |
| Connected components | 388 |
| Largest component | 121 |
| Aligned groups | 219 |
| Trilingual groups | 219 (100%) |
| Unmatched concepts | 359 |
| Total relations | 525 |
| Elementary (level 1) | 26 |
| Middle (level 2) | 57 |
| High (level 3) | 200 |
| College (level 4) | 273 |
| data.js MD5 | `9b0480c1859ced0f377c2c5962223b64` |

---

## 9. 项目级技术债状态

| 债务 | 状态 | 备注 |
|------|------|------|
| 双目录同步 | ✅ 已修复 (2026-06-29) | `cognitive-space/` 内改为 import wrapper |
| Manifest 生成 | ✅ 已实现 | `scripts/generate_manifest.py`, schema v1.0.0 |
| Release Bundle | ✅ 已实现 | `release/` 目录由 release.py 自动生成 |
| Schema 版本 | ✅ 已实现 | `data_schema_version = "2.1.0"` |
| .pyc 缓存 | ⚠️ subprocess 方式 | 清空 `__pycache__` 即可解决 |
| Windows GBK 编码 | ⚠️ 部分脚本 | `quality_report.py` 已全 ASCII |

---

## 10. 注意事项

1. **单源真理**: 所有 pipeline 代码编辑 `scripts/math_graph_pipeline/`，不要修改 `cognitive-space/scripts/math_graph_pipeline/`（那里只有 import wrapper）
2. **Level SSOT**: level 在 `merge_extractions.py` 的 LEVEL_RULES 中推断，经 `align_languages.py` 前向传播到 `export_graph.py`。**绝对不要在 export 中做二次 level 推断**
3. **data.js 格式**: 这是 JS 变量赋值文件 (`var data = {...}`)，不是纯 JSON，更新时注意
4. **quality_history 目录**: 所有历史质量报告存储在 `data/quality_history/`，最新版是 `quality_report_latest.json`
5. **WM 相关文件**: `research/findings/` 和 `outputs/` 中的大部分文件独立于数学图管线，只有 `coverage_*` 系列受影响
