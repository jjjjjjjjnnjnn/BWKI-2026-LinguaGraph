# LinguaGraph — Agent Collaboration Framework

> 定义 Codex（方向/架构/审查）与 Claude Code（实现/调试/验证）的协作边界、手写格式和阶段门控。

---

## 1. 角色边界

### Codex（项目主管）

| 职责 | 产出物 | 门控 |
|------|--------|------|
| 研究问题分解 | Research Question → 可执行子任务 | 子任务必须有明确通过标准 |
| 架构决策 | ADR 或架构变更说明 | 变更必须标注影响范围 |
| 任务拆分 | 结构化任务说明（见 §2 格式） | 任务必须包含：输入、输出、验证方法 |
| 质量审查 | Review 报告 | 不通过则退回 Claude Code 修改 |

### Claude Code（执行工程师）

| 职责 | 产出物 | 门控 |
|------|--------|------|
| 编码实现 | 符合任务说明的代码 | 通过 `release.py --dry-run` |
| 调试修复 | 根因分析 + 修复 | 通过现有 Quality Gates |
| 数据更新 | 重新运行 pipeline | 通过 `scripts/quality_report.py` |
| 文档同步 | README / Portal 更新 | 三语同步（`sync_readmes.py`） |

### 共享义务

双方都必须遵守：

1. **Pipeline 唯一源码** = `scripts/math_graph_pipeline/`（技术债表 §9）
2. **所有修改必须通过 release.py** 验证（除非明确注明"跳过管线"）
3. **冻结规则不可违反**（见 CLAUDE.md §3）

---

## 2. 任务手写格式

Codex 向 Claude Code 交代任务时，使用以下结构：

```yaml
---
phase: "实现"                    # 研究周期阶段
task_id: "T-2026-07-01-001"      # 唯一 ID
priority: "P0"                   # P0=阻塞, P1=重要, P2=优化
estimated_effort: "30min"        # 预估时间
depends_on: []                   # 前置任务 ID
---

## 目标
[一句话说明要完成什么]

## 上下文
[为什么需要这个任务，相关的背景信息]

## 输入
- 数据依赖：[必须存在的数据文件或状态]
- 代码基线：[git commit 或分支]

## 要求
1. [具体要求，可验证]
2. [具体要求，可验证]

## 验证方法
- [如何确认任务完成，例如 "运行 X 脚本，确认 Y 指标"]
- [门控条件，例如 "quality_report.py Gate 1-4 必须 PASS"]

## 不包含（明确排除）
- [不需要做的事，避免 scope creep]
```

---

## 3. 研究周期 × 阶段门控

```
┌─────────────────────────────────────────────────────────────┐
│                     Codex 主导阶段                           │
├─────────────────────────────────────────────────────────────┤
│  Ideation → Specification → Task Breakdown                  │
│     │              │               │                        │
│     └── Gate 0 ────┘               │                        │
│         RQ 明确,                                    │
│         假设可验证                                │
│                                    │                        │
│                                    └── Gate 1 ──────────── │
│                                       任务说明完整,          │
│                                       依赖已满足              │
├─────────────────────────────────────────────────────────────┤
│                     Claude Code 主导阶段                      │
├─────────────────────────────────────────────────────────────┤
│  Implementation → Testing → Validation                      │
│       │              │              │                       │
│       └── Gate 2 ────┘              │                       │
│          Code complete,              │                       │
│          tests pass                  │                       │
│                                      └── Gate 3 ─────────── │
│                                          Quality Gates PASS, │
│                                          release.py run      │
├─────────────────────────────────────────────────────────────┤
│                     Codex 主导阶段                           │
├─────────────────────────────────────────────────────────────┤
│  Review → Integration → Paper/Release                       │
│    │            │               │                            │
│    └── Gate 4 ──┘               │                            │
│       审查通过,                    │                            │
│       无回归                     │                            │
│                                  └── Gate 5 ─────────────── │
│                                      Release 发布,            │
│                                      manifest.json 更新      │
└─────────────────────────────────────────────────────────────┘
```

### 门控定义

| 门控 | 名称 | 条件 | 裁判 |
|------|------|------|------|
| Gate 0 | 问题就绪 | RQ 已精炼、假设可验证、相关数据已确认存在 | Codex |
| Gate 1 | 任务就绪 | 任务说明完整、依赖已标注、验证方法已定义 | Codex |
| Gate 2 | 实现就绪 | 代码通过 lint/test、无静默异常 | Claude Code + CI |
| Gate 3 | 数据就绪 | `release.py` 全流程通过、Quality Gates PASS | `scripts/release.py` |
| Gate 4 | 审查就绪 | 审查无 CRITICAL 问题、回归检查通过 | Codex |
| Gate 5 | 发布就绪 | manifest.json 已更新、Release 已创建 | Codex |

---

## 4. 与现有工程基础设施的集成

所有代码修改最终都必须通过同一套验证管线：

```
Claude Code 修改代码
        │
        ▼
python scripts/release.py --skip-pipeline --dry-run
        │
        ▼
Quality Report → Gate 1-4 PASS?
        │              │
       YES             NO
        │              │
        ▼              ▼
  可提交         退回修改
```

### 特殊情况的处理

**情况 A：Claude Code 发现任务说明不完整**
→ 暂停实现，回复 Codex 补充任务说明。

**情况 B：Codex 指定了方向但数据不支持**
→ Claude Code 运行 `quality_report.py`，附上证据说明数据不支持。

**情况 C：Gate 3 失败（release.py 未通过）**
→ Claude Code 必须修复，不可绕过。

**情况 D：需要在冻结规则之外操作**
→ Codex 必须明确解除冻结（标注影响范围），不可由 Claude Code 自行决定。

---

## 5. 论文与数据版本的一致性承诺

论文中出现的所有数字必须来自同一个 `manifest.json`：

```text
论文中的数字
        │
        ▼
manifest.json
        │
        ▼
release/v{N}.x/
   ├── data.js
   ├── data/visualization_data.json
   ├── report/quality_report.json
   └── checksums.txt
```

提交论文时，对应的 `release/` 目录必须存在且可复现。

---

## 6. 快速参考：一张表

| 场景 | 谁主导 | 使用什么 | 通过条件 |
|------|--------|----------|----------|
| 提出新 RQ | Codex | 任务说明模板 | Gate 0 |
| 拆任务 | Codex | 手写格式 §2 | Gate 1 |
| 写代码 | Claude Code | `scripts/` | Gate 2 |
| 更新管线 | Claude Code | `release.py` | Gate 3 |
| 审查质量 | Codex | Quality Report | Gate 4 |
| 发布 | Codex | `release.py` + Git | Gate 5 |

---

*版本: 1.0 | 2026-06-29*
