# LinguaGraph — Research Lab Skills Index

> **目的**: 精选高质量开源 AI 编程/审查/项目管理 Skills 索引
> **审计标准**: License, Stars, 活跃度, 与 LinguaGraph 相关性
> **原则**: 只下载 MIT/Apache-2.0, 保留原始 LICENSE

---

## 已安装 (Installed)

| # | 项目 | 用途 | ⭐ | License | 大小 | 目录 |
|---|------|------|----|---------|:----:|:----:|
| 1 | [scientific-agent-skills](scientific-agent-skills/) | 140 科研 Skills | 28.5k | MIT | — | `research_lab/` |
| 2 | [agent-skills](skills/agent-skills/) | 生产级工程 Skills (Google) | 62k | MIT | 1.1M | `skills/` |
| 3 | [pm-skills](skills/pm-skills/) | 项目管理 Skills (100+) | 19k | MIT | 12M | `skills/` |
| 4 | [planning-with-files](skills/planning-with-files/) | 崩溃回弹计划系统 | 23k | MIT | 23M | `skills/` |
| 5 | [cognee](skills/cognee/) | AI 记忆 + 知识图谱引擎 | 17.8k | Apache 2.0 | 113M | `skills/` |
| 6 | [claude-skills](skills/claude-skills/) | 337 Claude Code Skills | 18.3k | MIT | 48M | `skills/` |

---

## 精选评估

| 项目 | License | 相关性 | 说明 |
|------|:-------:|:------:|------|
| **agent-skills** | MIT | ⭐⭐⭐ | Google 工程 Skills。代码审查、测试、性能优化 |
| **pm-skills** | MIT | ⭐⭐⭐ | PM 工作流：roadmap, 任务分解, sprint 管理 |
| **planning-with-files** | MIT | ⭐⭐⭐ | 崩溃安全计划系统。适合长期 Agent 任务 |
| **cognee** | Apache 2.0 | ⭐⭐⭐ | 知识图谱内存引擎。LinguaGraph 可借鉴图谱架构 |
| **claude-skills** | MIT | ⭐⭐⭐ | 337 Skills：工程/产品/合规/研究/业务 |

---

## 未安装（审查后排除）

| 项目 | 原因 |
|------|------|
| anthropics/skills | ❌ 仓库无 LICENSE 文件，默认 All Rights Reserved，不可用 |
| awesome-claude-skills | ❌ 纯列表（README），不是可克隆的代码库 |
| ponytail | ▶ 有趣但不必须（"最懒工程师"哲学） |
| cherry-studio | ▶ 桌面应用，非 CLI Skills 集 |

---

## 审核后再决定

| 项目 | 风险 | 说明 |
|------|------|------|
| ponytail | 🟢 安全 | "最懒高级工程师"哲学——有趣但不必须 |
| cherry-studio | 🟢 安全 | 桌面应用，非 CLI Skills |
| googleworkspace/cli | 🟢 安全 | Google 工具接口，不直接相关 |

---

## 使用规则

1. ✅ 可用于辅助代码审查、项目管理、论文写作
2. ✅ 保留原始 LICENSE 文件
3. ❌ 不用于修改 LinguaGraph 核心 Pipeline
4. ❌ 不用于修改 LDS / 问卷 / 概念映射
5. ❌ 不用于自动生成新实验假设

*最后更新: 2026-06-17*
