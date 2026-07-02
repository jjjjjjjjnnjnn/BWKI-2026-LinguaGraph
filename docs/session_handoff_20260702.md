# LinguaGraph — 完整项目状态交接文档

> **生成时间**: 2026-07-02 | **版本**: v0.6.2
> **下一会话加载**: 读取此文件 + `linguagraph-research-contract.md`

---

## 研究契约（已固化，不可变）

### Research Question
> Do different languages exhibit systematically different cognitive structures, and under what conditions are these differences observed?

### Principles (P1–P5)
P1: Evidence before explanation · P2: Null models precede interpretation
P3: Human data overrides corpus · P4: Measure, don't prove · P5: Negative results are scientific results

### 三层证据架构
```
LDS-K (教材知识结构)  → Mature     → 假设生成
LDS-C (人类概念结构)  → Developing → 主要确认性证据（瓶颈）
LPA (语言产出分析)    → Exploratory → 补充性质性证据
```

---

## 当前阶段：Phase 2→3（证据收集 → 证据验证）

### 数据状态

| 数据源 | 有效 N | 状态 |
|--------|:------:|:----:|
| LDS-C pilot (前期) | 8 (4ZH+2DE+2EN) | ✅ 已存档 |
| LDS-C 后端自动收集 | 8 (2ZH+6DE) | ✅ Google Sheets 运行中 |
| LDS-C 中国用户 | 0 | ❌ GFW 屏蔽，改用问卷星 |
| LPA DE (语言学问卷) | 6 | ✅ 已编码分析 |
| LPA ZH (语言学问卷) | 13 | 🆕 刚收到，未处理 |
| LDS-C 总有效 | **16** | 🔶 ZH=6, DE=8, EN=2 |

### 关键缺口
- **EN**: 仅 2 份（严重不足）
- **ZH**: 问卷星替代方案刚启动

---

## 已完成的治理/方法文档

| 文档 | 位置 | 说明 |
|------|------|------|
| Research Contract | 项目记忆 | RQ + 5 Principles + 证据架构 |
| Research Lifecycle | plan 文件 | 6 阶段 + KR + 优先级矩阵 |
| LPA Framework | `docs/lpa_framework.md` | 4 维度、编码方案、IRR 协议 |
| LPA Codebook v0.3 | `docs/lpa_codebook.md` | 20+ 准则、包含/排除规则、Decision Log |
| LPA References | `docs/lpa_references.md` | 22 条学术引用 |
| Evidence Register | `docs/evidence_register.md` | 15 条 Claims + 置信度 |
| OSF Preregistration | `docs/osf_preregistration.md` | 完整实验方案 |
| Recruitment Plan | `docs/recruitment_plan.md` | 渠道追踪 + 阶段性目标 |
| LPA 分析管线 | `scripts/analyze_lpa.py` | 自动编码 + IRR 计算 |

### 已完成的工程设施
- Pipeline / Manifest / SSOT / Quality Gates / Release
- Portal (12-section, trilingual) — 已部署
- Survey 前端 — 三语，Google Sheets 后端，Cloudflare Worker 中转
- 论文 — 8 章节全部德文，≈80% 草稿

---

## LPA IRR 基线（N=6, 30 二进制准则）

| 指标 | 值 |
|------|:---:|
| 平均 κ | 0.782 ✅ 超过 0.70 阈值 |
| Accept (≥0.80) | 19/30 (63%) |
| Revise (0.60-0.69) | 2/30 |
| Exclude (<0.60) | 9/30 (需 Codebook 修订) |

主要分歧：拒绝回答编码（"Kann kein Englisch" 应标 T- 而非 T?）

---

## 技术架构

```
Survey (GitHub Pages)
  ├── 直连 → Google Apps Script → Google Sheets (海外用户)
  ├── → Cloudflare Worker → Google Apps Script → Sheets (中国用户，已被墙)
  └── **新方案: 问卷星** (中国用户替代方案)
```

Cloudflare Worker: `https://linguagraph-relay.rongjiajun2025.workers.dev`
Google Apps Script: 已部署可运行
问卷星: 待创建

---

## 待办事项（按优先级）

### P0 — 数据收集（关键路径）
- [ ] **ZH**: 在问卷星创建 5 题调查 → 发微信
- [ ] **EN**: 发 Reddit r/linguistics 或 r/cogsci
- [ ] **DE**: 学校渠道分发

### P1 — 方法验证（可并行）
- [ ] **LPA ZH 13 份**：通过 Codebook 编码，与 DE 6 份做跨语言对比
- [ ] **LPA IRR 第二轮**：修订 Codebook 后重算 κ
- [ ] **LDS-C 质量检查**：到达 N≈20 时做一次中期评估

### P2 — 论文
- [ ] Introduction / Related Work / Methods 润色
- [ ] 不提前写 Results / Discussion

### P3 — 工程维护
- [ ] 保持 Pipeline / Release 正常运行

---

## 关键链接

| 资源 | URL |
|------|-----|
| GitHub 仓库 | https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph |
| Research Portal | https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/portal/ |
| 3D 知识图谱 | https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/ |
| 调查问卷 | https://jjjjjjjjnnjnn.github.io/BWKI-2026-LinguaGraph/survey/ |
| LPA ZH 问卷 | `cognitive-space/survey/lpa_zh.html` |
| LPA EN 问卷 | `cognitive-space/survey/lpa_en.html` |

---

## 新会话加载顺序

1. 读取项目记忆 `linguagraph-research-contract.md`（研究契约）
2. 读取此文件（状态交接）
3. 读取 plan 文件（Research Lifecycle + 当前优先级）
4. 继续推进 P0 数据收集 + P1 方法验证
