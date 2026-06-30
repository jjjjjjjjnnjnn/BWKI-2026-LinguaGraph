# LinguaGraph — 3-Month Strategic Roadmap v2
## Target: BWKI 2026 Full Submission (Deadline: 2026-09-21)

> 更新日期: 2026-06-29 | 旧版已归档: `docs/planning/archive/three_month_roadmap_v1.md`

---

## 当前状态: 工程基础设施完成，进入科研产出阶段

| 维度 | 状态 | 差距 |
|------|------|------|
| Pipeline + 质量门控 | ✅ SSOT + Quality Gates + Release | 无 |
| Manifest + Provenance | ✅ 单源真理 + Git 追踪 + 校验和 | 无 |
| 3 条不可违反原则 | ✅ SSOT / Immutable / Validated | 无 |
| 教材知识图谱 | 556 节点, 238 边, 219 三语组 | **需扩大覆盖** |
| 提取验证 | 92 gold, 20-model benchmark | 无 |
| 人类验证 | N=8 pilot, within + between LDS | **N 太小** |
| LDS 理论 | 3-component metric | **需 formal definition + LDS-K/LDS-C 分离** |
| 跨学科 | Math(556), Physics(366), Chemistry(220) | 化学覆盖度低 |
| 论文 | 9 sections (DE) | 需与 manifest.json 对齐 |
| Portal | 5 findings + 3D CognitiveSpace | 基本完成 |
| 演讲 | 无 | 需 30s/3min/10min |

---

## 科学框架更新: 双板块认知模型

根据最新分析，项目已经自然形成了**双数据源结构**，需要将 LDS 分为两个版本来反映这种差异：

```
                    ┌───────────────────┐
                    │   教材语料流      │
                    │ (structured)      │
                    │                   │
                    │  → LDS-K          │
                    │  (Knowledge LDS)  │
                    └────────┬──────────┘
                             │
                  结构差异对比
                             │
                    ┌────────Ⅴ──────────┐
                    │  LDS 多语言差异   │
                    └────────▲──────────┘
                             │
                  认知表达对比
                             │
                    ┌────────┴──────────┐
                    │   人类问卷流      │
                    │ (spontaneous)     │
                    │                   │
                    │  → LDS-C          │
                    │  (Cognitive LDS)  │
                    └───────────────────┘
```

**关键科研问题**: `ΔLDS = LDS_C - LDS_K` — 语言对"认知 vs 知识结构"的影响差异。

---

## Month 1: 双板块基线 + LDS 形式化 (7月1日 – 7月31日)

### 核心行动

| 周 | 行动 | 交付物 | 优先级 |
|----|------|--------|--------|
| W1 (Jul 1-7) | **LDS formal definition** — 写出 LDS-K 和 LDS-C 的数学定义 + 公理性质（非负性/对称性/有界性 ≤1） | `docs/lds_formal_definition.md` | **P0** |
| W1 | 最终确定实验方案 + 伦理 | Protocol doc, consent forms | P0 |
| W1 | 在 OSF 注册分析计划 | OSF preregistration | P0 |
| W2 | LDS 消融实验：去语言 / 去教材 / 纯 Wikipedia / 纯模拟 | 4 组 LDS 对比表 | **P0** |
| W2-3 | 招募 22+ 双语被试 | 22 signed consents | P0 |
| W3-4 | 数据收集 + 通过 pipeline 提取 | 30 × 5 topics × 2-3 languages | P0 |
| W4 | 运行完整 pipeline + quality report + release | `release/v1.0/` | P0 |

### 实验设计（与现有协议一致）

**双语翻译-控制协议**: 每位被试在两种最强语言中回答相同的 5 个社会主题。

| 效应 | 对照 |
|------|------|
| 语言效应 (Language) | 组内，同一主题，不同语言 |
| 个体效应 (Individual) | 组间，同一语言，不同人 |
| 主题效应 (Topic) | 组内，同一语言，不同主题 |

### 预注册假设

```
H1 (Language effect):         Within-subject LDS > simulation baseline LDS
H2 (Language pair diff):      DE-ZH LDS > ZH-EN LDS  
H3 (Level consistency):       Rank order preserved across individual/corpus/curriculum
H4 (Topic effect):            Abstract concepts (Freedom, Justice) > concrete (Home)
```

### LDS 消融实验计划

| 消融条件 | 预期 | 验证方法 |
|----------|------|----------|
| 去掉语言标签 | LDS ≈ 0（若 LDS 真正测的是语言差异） | 随机混洗语言标签 |
| 只用 Wikipedia | LDS 与教材 LDS 趋势一致 | Spearman 相关 |
| 只用 Simulation | LDS < 人类 LDS（控制基线） | t 检验 |
| 随机图基线 | LDS 显著低于真实图 | 随机化边分布 |

---

## Month 2: 理论 + 分析 (8月1日 – 8月31日)

| 周 | 行动 | 交付物 |
|----|------|--------|
| W5-6 | 在新数据上运行 pipeline | 30 名被试的 LDS 值 |
| W6-7 | 统计分析 | 所有假设检验 + 图表 |
| W6-7 | **论文数字与 manifest.json 对齐** | 论文所有数字来自同一发布版本 |
| W7-8 | LDS 理论性质证明 | 正式数学附录 |
| W8 | ΔLGS 分析 = LDS_C - LDS_K | 核心科学图 |

### LDS 理论包

1. **公理性质**: 证明非负性、对称性、有界性 (0 ≤ LDS ≤ 1)
2. **敏感性分析**: LDS 如何响应节点增删
3. **与替代指标的比较**: Jaccard-only, GED-only, Wasserstein
4. **置信区间**: Bootstrap CI 方法论正式化

---

## Month 3: 演示 + 交付 (9月1日 – 9月21日)

| 周 | 行动 | 交付物 |
|----|------|--------|
| W9-10 | 最终论文审查 + 润色 | 完整 DE 论文 |
| W10-11 | 实时演示 | 带有 LDS 实时计算的 Portal |
| W11-12 | 演讲润色 + 排练 | 3 个最终演讲 |
| W12 | 最终材料组装 | 所有提交材料 |
| W12 | **创建 GitHub Release v1.0** | 包含 release/ 目录的发布包 |

---

## 附录: 工程基础设施状态（已完成）

以下所有项目在上一次迭代中完成，不再需要额外投入：

| 完成项 | 对应文件 |
|--------|----------|
| Pipeline SSOT | `scripts/math_graph_pipeline/` (唯一源码) |
| Quality Gates | `scripts/quality_report.py` |
| Manifest | `scripts/generate_manifest.py` |
| Release Pipeline | `scripts/release.py` |
| Data Lineage | `LINGUAGRAPH_DATA_LINEAGE.md` |
| 3 Principles | `.claire/workflows/principles.md` |
| Agent Collaboration | `.claire/workflows/agent-collaboration.md` |

---

## 风险登记

| 风险 | 概率 | 影响 | 缓解 |
|------|:----:|:----:|------|
| 无法及时招募 22 名双语者 | 中 | 高 | 回退到方案 C（10 双语 + 20 单语） |
| LDS 消融实验显示 LDS ≈ 语言无关 | 低 | 高 | 报告真实结果，仍是有效科研 |
| N=30 仍不显著 | 低 | 中 | 预先计算 power analysis |
| 实时演示在评审时失败 | 低 | 高 | 预录视频备份 |

---

## 决策日志

| # | 决策 | 理由 | 日期 |
|---|------|------|------|
| D1 | 不增加新学科/语言 | 现有 3×3 矩阵足够 | 2026-06-25 |
| D2 | API/REST 层不部署 | GitHub Pages 已满足提交需要 | 2026-06-25 |
| D3 | 代码开源 | 已满足；支持可复现性 | 2026-06-25 |
| D4 | 双语翻译-控制协议 | 最强调的 causal inference | 2026-06-25 |
| D5 | LDS 分为 LDS-K / LDS-C | 双数据源自然形成 | 2026-06-29 |
| D6 | 工程基础设施冻结 | 管线/质量/发布已稳定 | 2026-06-29 |
