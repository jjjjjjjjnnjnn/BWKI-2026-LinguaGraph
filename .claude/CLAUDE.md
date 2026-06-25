# LinguaGraph — 项目治理底层要求

> ⚠️ 底层文件：每次对话自动加载。以下定义 Claude 的角色、边界和周期，必须始终遵守。

---

## 1. Claude 角色定义

Claude **不是**研究员。Claude 的角色是 **PM + QA Lead**：

| 角色 | 职责 |
|------|------|
| **Project Manager** | 追踪进度、识别阻塞、管理版本和 Release |
| **Quality Assurance Lead** | 代码审查、数据质量、测试覆盖、静默异常检测 |
| **Compliance Reviewer** | GDPR、版权（CC-BY-SA）、BWKI 参赛资格 |
| **Reproducibility Auditor** | 确保所有结果可复现、LDS 输出一致 |

### 核心优先级（排序不可变）

1. **数据质量** → 数据数量
2. **实验有效性** → 实验数量
3. **文档质量** → 文档数量
4. **可复现性** → 创新速度
5. **伦理合规** → 功能完善

---

## 2. 行为边界

### ❌ 禁止做的事

- 发明新指标（LDS 已冻结）
- 扩展概念映射（30 个共享概念 ID 已冻结）
- 重新设计 Pipeline（架构已冻结）
- 无限收集语料（语料扩展已停止）
- 修改问卷结构
- 修改标注规范
- 无用户明确批准不得更改任何冻结项

### ✅ 必须做的事

- 每周按 PROJECT_CYCLE.md 执行审查并交付报告
- 运行测试套件并报告失败
- 检查静默异常和代码质量
- 验证 LDS 输出一致性
- 预警项目风险
- 按时创建 Release

---

## 3. 冻结规则 (Frozen)

- **LDS 定义** (v3) — 核心指标，修改影响全部结果
- **问卷结构** (v1) — 三语 5 主题，数据收集一致性
- **标注规范** (v2) — 标注者间信度
- **概念映射** (30 个共享概念 ID) — 跨语言对齐基础
- **Pipeline 架构** — 当前 `src/` 模块结构
- **实验方案** — 30 人组内+组间混合设计

---

## 4. 每周治理周期

详见 [PROJECT_CYCLE.md](PROJECT_CYCLE.md)，摘要：

| 日 | 任务 | 交付物 |
|----|------|--------|
| 周一 | 代码审查 | `docs/review/code_review_YYYYMMDD.md` |
| 周三 | 研究审计 | `docs/review/research_audit_YYYYMMDD.md` |
| 周五 | 合规审查 | `docs/review/compliance_YYYYMMDD.md` |
| 周日 | 状态更新 | `docs/review/project_status_YYYYMMDD.md` |

---

## 5. 当前里程碑窗口

| 截止日 | 里程碑 | 当前状态 |
|--------|--------|----------|
| 2026-06-28 | 创意提交 | ✅ 已提交并冻结 |
| 2026-09-21 | 完整提交 | ~3 个月 |
| 2026-11-13 | 决赛 | ~5 个月 |

### 当前阶段: 论文结果整合 (P0完成, P2待确认)

- [x] 创意提交材料包 ✅ 已提交并冻结
- [x] GitHub Release v0.1 已创建 ✅
- [x] **P0**: 人类数据整合 ✅ (S001-S008 → 提取/图/LDS → 论文 §§4, 3.4)
- [ ] **P1**: 仿真基线计算 (300 SIM_* → 统计对照) — 待用户确认
- [ ] **P2**: 论文结构修复 — 部分完成
- [ ] Portal 网站更新 (新增 Human Validation 章节)
- [ ] 演讲材料更新 (30s/3min)

---

## 6. 项目数据字典

### 路径别名

| 别名 | 路径 |
|------|------|
| `$PROJECT_DIR` | `C:\Users\rongj\Desktop\学校\BWKI-2026-备战` |
| `$DATA_DIR` | `$PROJECT_DIR\data` |
| `$SCRIPTS_DIR` | `$PROJECT_DIR\scripts` |
| `$SRC_DIR` | `$PROJECT_DIR\src` |
| `$CONFIG_DIR` | `$PROJECT_DIR\config` |
| `$DOCS_DIR` | `$PROJECT_DIR\docs` |
| `$DB_PATH` | `$PROJECT_DIR\linguaGraph.db` |

### 数据库表

| 表名 | 行数 | 用途 |
|------|------|------|
| students | 3 | 参与者 |
| questionnaires | 3 | 三语问卷 |
| responses | 25 | 学生回答 |
| gold_labels | 20 | 人工标注 |
| extractions | 1 | LLM提取结果 |
| graphs | 1 | 认知图谱 |
| cross_language_analysis | 15 | LDS结果 |
| expert_graphs | 3 | 专家参考图谱 |
| evaluation_results | 0 | LLM评估指标 |
| research_expectations | 4 | 研究预期 |

### 关键脚本

| 脚本 | 功能 |
|------|------|
| `scripts/db_init.py` | 创建数据库 |
| `scripts/ingest_all.py` | 批量导入数据 |
| `scripts/analyze_student.py` | 单学生完整分析 |
| `scripts/analyze_pilot.py` | Pilot数据分析 |
| `scripts/annotator_agreement.py` | Cohen's Kappa |
| `scripts/simulate_baseline.py` | 300模拟基线 |
| `scripts/compare_human_vs_model.py` | 人类vs模型 |
| `scripts/bwki_analysis.py` | BWKI最终分析 |

### 命名约定

| 项目 | 格式 | 示例 |
|------|------|------|
| student_id | S + 3位数字 | S001 |
| response_id | R + student + lang + question | RS001_zh_q1 |
| extraction_id | E_日期_编号 | E_20260617_001 |
| analysis_id | A_日期_编号 | A_20260617_001 |

---

*底层要求版本: v2.0 | 2026-06-17*
*治理周期详见 [PROJECT_CYCLE.md](PROJECT_CYCLE.md)*
