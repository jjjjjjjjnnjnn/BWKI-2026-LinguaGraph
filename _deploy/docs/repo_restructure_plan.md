# BWKI 仓库重构计划

> **状态**: 提案 | **风险**: 中（会改变 Git 历史、移动文件引用）
> **目标**: 将仓库从"快速原型结构"升级为"科研项目结构"

---

## 现有问题

### 1. 边界模糊

```
BWKI-2026-备战/        ← 既是 BWKI 研究仓库
├── cognitive-space/   ← 又是 CognitiveSpace 可视化
├── research/          ← 又是实验记录
├── research_lab/      ← 又是工具集合
├── survey_pipeline/   ← 又是分析管道
├── participant_data/  ← 又是数据管理
├── evaluation/        ← 又是评估脚本
├── experiments/       ← 又是实验脚本
├── external/          ← 又是外部库
├── references/        ← 又是文献库
```

### 2. 结构重复

| 根目录 | CognitiveSpace 内 | 问题 |
|--------|------------------|------|
| `config/expert_graphs/` (9文件) | `cognitive-space/config/expert_graphs/` (math_full.json) | 半重复 |
| `data/math_extractions/` (53文件) | `cognitive-space/data/math_extractions/merged/` | 影子 |
| `web/` | `cognitive-space/web/` | 旧版未删除 |

### 3. 历史残留

| 目录 | 状态 |
|------|------|
| `visualization/` | 废弃（被 cognitive-space/web 取代） |
| `visualization_v3/` | 废弃（被 cognitive-space/web 取代） |
| `web/` | 废弃（被 cognitive-space/web 取代） |
| `web/threejs/` | 废弃（THREE 方案已放弃） |
| `output/` | 遗留（仅 zh_001.json） |

---

## 重构方案

### 第一步：删除废弃目录（零风险）

```
rm -rf visualization/
rm -rf visualization_v3/
rm -rf web/                # 不包括 cognitive-space/web
rm -rf output/             # 或移到 outputs/legacy/
rm -rf .pytest_cache/
```

### 第二步：剥离 CognitiveSpace（低风险）

CognitiveSpace 应完全独立。现有 `cognitive-space/` 子目录结构已经很好。

但根目录引用了它的数据：
- `data/math_extractions/` → 大多数数学提取数据 **仅用于 CognitiveSpace**
- `config/expert_graphs/` → 部分文件用于 CognitiveSpace 管道

**方案**：将所有数学提取数据和专家图谱移到 `cognitive-space/data/` 下，根目录不再保留数学数据副本。

### 第三步：对齐目标结构

**目标**：
```
BWKI-2026-LinguaGraph/
├── README.md
├── CLAUDE.md
├── LICENSE
├── src/              # 核心模块（已有）
├── scripts/          # 分析管道（已有）
├── config/           # 配置文件（已有）
├── data/             # 结构化数据
├── docs/             # 文档
├── tests/            # 测试
├── outputs/          # 输出 + 结果
├── external/         # 外部引用（已有）
└── references/       # 文献（已有）
```

**具体变更**：

#### `data/` 重组

```
data/                              data/
├── baseline/             →         ├── baseline/
├── corpus/                        ├── corpus/
├── evidence/                      ├── evidence/
├── gold/              (新建)       ├── gold/
│   ├── schema_v1.md               │   ├── schema_v1.md
│   ├── concept_extraction/        │   ├── concept_extraction/
│   └── graph_completion/          │   └── graph_completion/
├── math_extractions/    → 已移到     cognitive-space/data/math_extractions/
├── questionnaires/                ├── questionnaires/
├── pilot_dataset/                 ├── pilot_dataset/
├── textbook/            → 可选移到   cognitive-space/data/textbook/
├── output/              → 删        outputs/
└── consent_form.md                └── (保留)
```

#### `outputs/` 新建

```
outputs/
├── figures/
├── reports/
├── lds/
├── tables/
└── README.md
```

合并 `results/` → `outputs/`：
```
results/figures/         →  outputs/figures/
results/tables/          →  outputs/tables/
results/paper_results_template.md  →  outputs/
```

#### `research/` 合并

`research/findings/` → `outputs/reports/`
`research/visualization/` → `outputs/figures/`
`research/` 中的分析脚本 → 按功能拆入 `scripts/` 或 `outputs/`

### 第四步：Gold Dataset 预留目录

```
data/gold/
├── dataset_schema_v1.md   ← 已存在的 schema 文档
├── concept_extraction/
│   ├── ce_zh.jsonl
│   ├── ce_en.jsonl
│   └── ce_de.jsonl
├── graph_completion/
│   ├── gc_zh.jsonl
│   ├── gc_en.jsonl
│   └── gc_de.jsonl
└── metadata.json
```

### 第五步：根目录清理

| 项目 | 处理 |
|------|------|
| `linguaGraph.db` | 移到 `data/` 或 `outputs/` |
| `models/qwen2.5-0.5b-q4_k_m.gguf` | 保留（独占 650MB，不影响结构） |
| `llama/` | 保留（推理工具） |
| `.pytest_cache/` | 删除 |
| `.github/workflows/deploy-pages.yml` | 移到 cognitive-space/（如果服务于它） |

---

## 风险控制

| 风险 | 缓解 |
|------|------|
| Git 历史中移动文件导致丢失 | 用 `git mv`，不删重写 |
| 脚本路径引用被破坏 | 迁移后统一更新 `scripts/` 中的路径 |
| `cognitive-space/scripts/math_graph_pipeline/` 引用 `../../data/math_extractions/` | 相对路径保持兼容 |
| `CLAUDE.md` 中的路径别名 | 需要更新 `$DATA_DIR` 等映射 |

## 执行顺序

```
Round 1（5分钟）
删除废弃目录: visualization visualization_v3 web output

Round 2（10分钟）
合并 results/ → outputs/
创建 gold/ 目录结构

Round 3（15分钟）
移动数学数据到 cognitive-space/
删除根目录重复数据

Round 4（5分钟）
更新路径引用
更新 CLAUDE.md

Round 5（可选）
更新 .gitignore
创建 outputs/README.md
```
