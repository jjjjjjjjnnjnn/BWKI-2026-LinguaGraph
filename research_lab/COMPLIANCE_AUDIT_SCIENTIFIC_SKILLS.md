# 合规审计: K-Dense-AI/scientific-agent-skills

> **审计日期**: 2026-06-17
> **目标**: 评估该 140-Skill 科研工具集是否适合集成至 LinguaGraph 或建立独立研究沙盒
> **审计维度**: License, 数据流向, 内容合规, BWKI 独立性, 主项目影响

---

## 1. 基本信息

| 项目 | 值 |
|------|----|
| 名称 | scientific-agent-skills |
| 作者 | K-Dense-AI (Organization) |
| 版本 | v2.52.0 (2026-06-12) |
| Stars | 28,522 |
| Forks | 2,918 |
| License | **MIT** |
| 兼容平台 | Claude Code, Cursor, Codex, Pi, Antigravity |

---

## 2. License 兼容性评估

| 检查项 | 结果 | 说明 |
|--------|:----:|------|
| License 类型 | ✅ | **MIT License** — 最宽松的开源许可证 |
| 商用允许 | ✅ | MIT 允许商用、修改、再发布 |
| 版权要求 | ✅ | 仅需保留原始版权声明 |
| GPL "传染性" | ✅ | **无** — MIT 不要求衍生作品使用相同许可证 |
| 与 LinguaGraph 兼容 | ✅ | LinguaGraph 为 All Rights Reserved，MIT 组件不会影响主项目版权 |

**结论**: ✅ License 无风险。MIT 是科研项目最常用的许可证。

---

## 3. 内容分类 (140 Skills)

审计发现 140 个 Skill，可分为 4 大类：

### A类 — 直接有助于 LinguaGraph (15 Skills)

| Skill | 用途 | 对 LinguaGraph 价值 |
|-------|------|---------------------|
| `statistical-power` | 统计功效分析 | ⭐⭐⭐ 直接解决 Gate Review C3 |
| `statistical-analysis` | t-test, ANOVA, Bootstrap | ⭐⭐⭐ 分析管道 |
| `experimental-design` | 实验设计咨询 | ⭐⭐ 验证当前方案 |
| `paper-lookup` | 论文检索 | ⭐⭐⭐ Related Work |
| `literature-review` | 文献综述 | ⭐⭐⭐ |
| `citation-management` | 引用管理 | ⭐⭐ |
| `scientific-writing` | 论文写作 | ⭐⭐⭐ BWKI 论文 |
| `scientific-visualization` | 科学可视化 | ⭐⭐ 图表 |
| `markdown-mermaid-writing` | Mermaid 图表 | ⭐⭐ 论文图 |
| `hypothesis-generation` | 假设生成 | ⭐⭐ Phase 3 |
| `research-lookup` | 研究检索 | ⭐⭐ |
| `latex-posters` | 海报生成 | ⭐ BWKI 展示 |
| `infographics` | 信息图 | ⭐ 演示 |
| `networkx` | 图算法 | ⭐ 已使用，可参考 |
| `statsmodels` | 统计建模 | ⭐ 已使用 |

### B类 — 可能有用但非核心 (20 Skills)

| Skill | 说明 |
|-------|------|
| `seaborn`, `matplotlib` | 绘图 — 已使用 |
| `scikit-learn`, `shap`, `umap-learn` | ML 工具 |
| `polars`, `dask`, `vaex` | 数据处理 |
| `sympy` | 符号数学 — 论文公式 |
| `pdf`, `pptx`, `docx`, `xlsx` | 文档处理 |
| `scientific-schematics`, `scientific-slides` | 演示材料 |
| `peer-review` | 论文审阅模拟 |
| `scientific-brainstorming` | 头脑风暴 |
| `scientific-critical-thinking` | 批判性思维分析 |
| `venue-templates` | 论文投稿模板 |
| `open-notebook` | 开放科学笔记 |

### C类 — 领域不相关 (100+ Skills)

生物信息学/化学信息学/药物发现/量子计算/材料科学等:
`biopython`, `rdkit`, `deepchem`, `scanpy`, `pymatgen`, `qiskit`, `cirq`,
`pyhealth`, `torchdrug`, `diffdock`, `molecular-dynamics`, 等

**对 LinguaGraph 无直接价值**，但不会造成危害。

### D类 — 需谨慎评估 (5 Skills)

| Skill | 风险 | 说明 |
|-------|------|------|
| `exa-search` | 🟡 **数据外流** | 调用外部 API 搜索，不发送本地数据则安全 |
| `peer-review` | 🟢 安全 | 只分析文本 |
| `research-grants` | 🟢 安全 | 资助信息查询 |
| `clinical-decision-support` | 🟢 不适用 | 医疗领域 |
| `treatment-plans` | 🟢 不适用 | 医疗领域 |

---

## 4. 数据流向评估

| 风险 | 评估 | 说明 |
|------|:----:|------|
| 是否自动上传本地数据 | ❌ 否 | Skill 是本地运行的 CLI/MCP 工具，不上传数据 |
| 是否调用外部 API | ✅ 是 (部分) | `exa-search`, `paper-lookup` 等需要 API Key |
| API Key 管理 | ✅ 安全 | 使用环境变量，不硬编码 |
| 是否发送用户数据给第三方 | ⚠️ 仅明确授权时 | Skill 只发送你指定让它发送的内容 |
| 是否符合 GDPR | ✅ | 本地运行，不自动收集参与者数据 |

---

## 5. 对 BWKI "独立完成" 要求的影响

| 检查项 | 结果 |
|--------|:----:|
| 使用开源工具是否允许 | ✅ 允许 |
| 是否需要注明工具来源 | ✅ 应在 CONTRIBUTORS.md 中说明 |
| 是否影响原创性 | ❌ **不会** — 工具辅助，核心方法(LDS/问卷/实验设计)是原创的 |

---

## 6. 审计结论

### 总体评分: ✅ 安全

```
License:     ✅ MIT — 无风险
数据安全:    ✅ 本地运行，无自动上传
内容合规:    ✅ 无侵权/违规内容
BWKI 合规:   ✅ 不影响独立性
主项目影响:  ✅ 不影响已冻结的 LDS/问卷/方法
```

### A/B/C 分类

| 分类 | 定义 | Skill 数 | 操作 |
|------|------|:---------:|------|
| **A类 — 立即可用** | 对 Human Validation 阶段直接有帮助 | 15 | ✅ 安装到 research_lab |
| **B类 — 以后使用** | 对论文/展示有用，非当前瓶颈 | 20 | ✅ 安装但暂不接入 |
| **C类 — 不相关** | 生物/化学/量子等不相关领域 | 100+ | ✅ 安装但不使用 |
| **D类 — 需谨慎** | 涉及外部 API 调用 | 5 | ⚠️ 审查后再用 |

---

## 7. 推荐安装方案

```
LinguaGraph (主仓库)
└── 不直接安装 — 保持冻结

research_lab/ (沙盒仓库 / 独立目录)
    └── scientific-agent-skills ✅
        ├── A类: 立即使用 (15)
        ├── B类: 论文辅助 (20)
        ├── C类: 不接触 (100+)
        └── D类: 合规使用 (5)
```

**MIT License 要求**: 使用后必须在项目中包含版权声明:

```
K-Dense-AI/scientific-agent-skills — MIT License
Copyright (c) 2026 K-Dense-AI
```
