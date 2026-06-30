# LinguaGraph — Research Task Lifecycle

> 一个研究任务从提出到关闭的完整生命周期。

---

## 任务状态

```text
DRAFT     → Codex 起草任务说明
REFINED   → Codex + Claude Code 确认任务范围
IN_PROGRESS → Claude Code 执行
REVIEW     → Codex 审查产出
GATE_FAIL  → 退回 IN_PROGRESS
DONE       → Gate 3/4/5 通过
CLOSED     → 任务关闭，Release 发布
```

## 任务模板（用于 Codex → Claude Code 手写）

```yaml
---
task_id: "T-2026-06-29-001"
phase: "实现/审查/发布"
priority: "P0"
status: "DRAFT"
depends_on: []
---

## 目标

## 背景

## 输入依赖

## 执行要求

## 验证标准

## 排除范围
```

## 记录

```
data/task_log/
├── YYYY/
│   ├── T-YYYY-MM-DD-NNN.md
│   └── ...
└── index.json
```
