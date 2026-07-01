# Evidence Milestones — 证据生产路线图

> 最后更新: 2026-07-01 | 详见 `docs/osf_preregistration.md`（正式的实验方案）

---

## E1–E3: 已完成 ✅

| 里程碑 | 状态 | 内容 |
|--------|:----:|------|
| E1: 教材知识图谱对比 | ✅ | 微积分跨课程对比（10 概念 + 10 关系 × 2） |
| E2: 不可译概念分析 | ✅ | 6 个不可译概念（孝/Schadenfreude/Heimat 等） |
| E3: Wikipedia 跨语言对比 | ✅ | 导数/积分/极限 中德英对比（转入 LDS 论文叙事） |

---

## E4: Gold Dataset → 92 条 ✅

**状态**：✅ **已完成**（远超原目标 50 条）
**产出**：`data/gold/gold_dataset.json` (92 labels)
| 领域 | 数量 |
|------|:----:|
| 社会概念 | 72 |
| 数学概念 | 20 |
| qwen-plus F1 | 0.939 (社会), 0.674 (数学) |

---

## E5: 人类验证（当前 N=8 → 目标 N=30）

**状态**：🔶 **进行中** — 8/30 参与者
**产出**：`data/students/` — 101 回答, 89% 提取覆盖率
- 4 ZH-native, 2 DE-native, 2 EN-native
- 通过 ChatGPT 和 WeChat 招募
- **下一步**：编写招募材料 → 启动正式招募

---

## E6: LLM vs Human 对比 ✅

**状态**：✅ **部分完成**（有 N=8 数据）
**产出**：
- `scripts/compare_human_vs_model.py`
- `scripts/analyze_human_lds.py` — ΔLDS 计算（demo mode with N=8）
- 19 模型基准测试 (F1 0.55–0.67)

---

## E7: 失败案例库

**状态**：🔶 部分完成（5 案例，目标 15-20）
**产出**：`data/failure_cases/README.md`

---

## 关键指标（BWKI 提交时）

| 指标 | 目标值 | 当前值 | 状态 |
|------|--------|:------:|:----:|
| Gold Dataset | 92 条 ✅ | **92** | ✅ |
| 人类参与者 | 30 人 | **8** | 🔶 CP |
| Cohen's Kappa | > 0.7 | **0.81** (social) | ✅ |
| Concept F1 | > 0.80 | **0.939** (social) | ✅ |
| 19 模型基准 | — | **F1 0.55–0.67** | ✅ |
| 失败案例 | 15+ 个 | **5** | 🔶 |
| LDS 正式定义 | v3 | **v3** | ✅ |
| OSF 预注册 | 完成 | **完成** | ✅ |
