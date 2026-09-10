# LinguaGraph Research Rules

> Stand: v0.13.2 (2026-09-08) | SSOT: manifest.json (556 Konzepte / 525 Relationen / 219 Gruppen)

## 当前阶段: Submission Finalization (Frist 20.09.2026)

## 禁止

- 无限扩展语料
- 新增概念超过20个
- 新增功能
- 新增指标

## 优先级

| 优先级 | 任务 |
|--------|------|
| P0 | 真实被试实验 |
| P0 | 问卷设计 |
| P0 | 方法验证 |
| P1 | Cognitive City 可视化 |
| P2 | 额外语料 |

## 决策检查

所有新增工作必须回答：

1. 是否增加科学证据？
2. 是否帮助验证研究假设？
3. 是否帮助完成 BWKI 提交？

如果三个问题都是"否" → 停止执行。

## 已验证发现 (v0.13.2)

| 指标 | 值 | 状态 |
|------|-----|------|
| LDS 排序 | N=15: kein Signal (Between); LLM-within: Signal +0.08–0.09 | ✅ revidiert (Pilot N=8 nicht repliziert) |
| Jaccard (mapped) | 0.35-0.43 | ✅ 非零 |
| 数据量 | 556 Konzepte / 525 Relationen / 68 Bücher (39/18/11) | ✅ SSOT manifest.json |
| 概念映射 | 30 shared IDs (eingefroren) / 219 trilinguale Gruppen | ✅ 有效 |
| F1 | Sozial 0.939; gewichtet gesamt 0.881 (n=92) | ✅ korrigiert |
| 55-Modell-Replikation | 42 DashScope + 7 zen/OR + D1 + 2 Kilo + 1 Cohere + 1 NIM + 1 go (50 Identitäten); alle ZH-DE p<0.05 | ✅ |
| Sim-Vergleich p=0.05 | **Zurückgezogen** (Skalendrift) | ❌ nicht verwenden |
| §8.17 N=1 | **Entfernt** (→ _archive/20260908_qitian_removal/) | ❌ nicht verwenden |

## 下一步 (P0)

1. LLM Extraction — 替代 fallback 关键词匹配
2. Top 20 Drift Concepts 排名
3. 问卷最终版
4. 招募 15 名学生
