# LinguaGraph — 评审驱动执行计划

> 来源: Chief Research Advisor 评审 (2026-06-30)
> 目标: 把项目从"优秀工程平台"推向"优秀科研成果"

---

## 评审关键意见总结

| # | 问题 | 严重程度 |
|---|------|:--------:|
| 1 | Null Model 不够 adversarial：目前都在尝试证明 LDS，而非反驳它 | **高** |
| 2 | N=8 是整个项目的 Critical Path | **阻止级** |
| 3 | 缺少统计报告框架（效应量、CI、多重比较校正） | **高** |
| 4 | Portal 正在反向变成数据源，而非 manifest.json 的消费者 | **中** |
| 5 | 论文剩余章节需要同步更新 | **中** |

---

## 执行顺序

### Phase 1: Critical Path — Infrastructure for Human Data (P0)

1. **更多 adversarial Null Model** 加入 fig4_null_model.py
2. **Human recruitment infrastructure**: 在线问卷设计 + 质量检查
3. **Statistical framework document**: 提前写分析计划

### Phase 2: Theory & Validation (P1)

4. LDS formal definition 完善（统计性质、CI、bootstrap）
5. 剩余论文章节同步 (01, 02)

### Phase 3: Paper & Portal (P2)

6. Portal 改为 manifest.json 驱动
7. Figure polishing

---

## 具体任务分解

| # | 任务 | 复杂度 | 依赖 |
|---|------|:------:|:----:|
| 1 | **Adversarial Null Models**: 加入 within-language baseline + cross-discipline LDS | M | fig4_null_model.py |
| 2 | **LDS Statistical Appendix**: Bootstrap CI, effect size, power analysis | M | lds_formal_definition.md |
| 3 | **Human Recruitment Plan**: Survey tech spec, quality checks, recruitment pipeline | H | — |
| 4 | **Paper: 01_abstract_introduction.md update** | L | 00_three_conclusions.md |
| 5 | **Paper: 02_related_work.md update** | M | New findings |
| 6 | **Portal → manifest.json as source** | M | manifest.json |

---

## 执行

### 立即执行 (本轮会话):

1. ✅ Adversarial Null Models — 更新 fig4_null_model.py + 文档
2. ✅ LDS Statistical Appendix — 写入 lds_formal_definition.md
3. ✅ Human recruitment infrastructure — 创建问卷设计文档
4. ✅ Paper 01 + 02 更新

### 下一轮建议:

5. Portal manifest.json 重构
6. 开始招募被试
7. 论文最终润色
