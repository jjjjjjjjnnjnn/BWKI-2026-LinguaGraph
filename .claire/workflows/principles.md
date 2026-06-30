# LinguaGraph — 三条不可违反原则

> 整个项目的治理层可以压缩为三条原则。一切 Gate、流程、检查都是这三条的实现细节，而非独立规则。

---

## PRINCIPLE 1 — Single Source of Truth

**manifest.json 是项目所有聚合数字的唯一来源。**

任何地方（论文、Portal、README、图表）出现的以下数字必须与 `manifest.json` 一致：

- 节点数、边数、对齐组数
- 级别分布、三语覆盖率
- data.js MD5

**违反示例：** 论文写 "556 nodes" 但 `manifest.json` 显示 557。

---

## PRINCIPLE 2 — Immutable Release

**每次 `release.py` 生成的 `release/` 目录是不可修改的研究快照。**

快照包含：

- 当时的数据文件（visualization_data.json, aligned_data.json）
- 当时的质量报告（quality_report.json）
- 当时的校验和（checksums.txt）

**违反示例：** 修改 release 目录中的文件而不重新运行 `release.py`。

---

## PRINCIPLE 3 — Validated Pipeline

**所有结果必须通过 `release.py` 验证才能被视为有效。**

`release.py` 内部执行：

```
pipeline → quality_report → gates → manifest → bundle
```

**违反示例：** 手动修改 data.js 但不运行 `release.py` 验证。

---

## 这些原则在 CLAUDE.md 中的对应

| CLAUDE.md § | 对应的原则 | 实现方式 |
|-------------|-----------|----------|
| §1 优先级排序 | — | 约束工程不压倒研究 |
| §2 行为边界（冻结规则） | P1, P3 | 冻结项不可在管线外修改 |
| §3 三语同步 | P1 | manifest.json 包含 checksums |
| §4 Agent 协作 | P1, P2, P3 | 双方都受 release.py 约束 |
| §5 Pipeline 源码 | P3 | 唯一源码 = scripts/math_graph_pipeline/ |
| §6 发布流程 | P2 | release.py → immutable bundle |

---

## 为什么是三条，不是十二条

Gates (1-6)、Task Lifecycle (DRAFT→CLOSED)、Schema Version、检查清单——这些都是**实现手段**，不是**不可违反原则**。

如果以后需要加一个新 Gate，不需要修改这三条。如果以后需要改手写格式，也不需要改这三条。

这三条只回答一个问题：

> **"这个项目里什么绝对不能违反？"**
