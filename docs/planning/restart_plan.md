# LinguaGraph — 研究重启计划（Research Restart Plan）

> 更新日期: 2026-08-07 | 提交截止: **2026-09-20/21**（约 6 周）
> 前置文档: [three_month_roadmap.md](three_month_roadmap.md) · [lds_formal_definition.md](../lds_formal_definition.md) · [recruitment_plan.md](../recruitment_plan.md)
> 方向定位：**研究优先、纵深分析**（"竖式研究"）；非研究内容（论文排版、视频、演示）后置。

---

## 1. 为什么重启 / 现状速览

项目停摆约一个月后重启。扫描确认：**工程与语料侧已基本完成，但核心科学主张尚未兑现**——论文真正的主见 `ΔLDS = LDS_C − LDS_K > 0`（语言驱动的认知分歧）依赖的 LDS-C **从未在合格数据上计算过**（[lds_formal_definition.md](../lds_formal_definition.md) 原文 "❌ Not yet computed"）。

### 1.1 三大数据流现状

| 数据流 | 计划/承诺 | 当前实际 | 状态 |
|--------|-----------|----------|------|
| 语料 LDS-K | Wikipedia 5 主题 × 3 语言 + 教材图 | 教材图已算（ZH-EN 0.934 / DE-EN 0.938 / ZH-DE 0.519） | ✅ 完成（可深化） |
| 模拟基线 | 300 SIM 对照 | 已算，但数值有出入（论文 0.647 vs 文件 0.667） | ⚠️ 需调和 |
| **人类 LDS-C** | 预注册 N=30 / idea N=60+ | **N=11 合格（6 DE + 5 ZH + 0 EN）**，从未跑 LDS-C | ❌ 核心缺口 |

### 1.2 人类数据质量（SSOT: `../../freeze/freeze_survey_20260703/`）

| 指标 | 数值 |
|------|------|
| 提交 / 合格 | 18 → 11（6 DE + 5 ZH + **0 EN**） |
| 完全干净 / 带标记 | 3 / 8（15 项短答标记，min_length 通过率 16.7%） |
| 排除率 | 38.9%（阈值 <25%）→ WARN |
| 主题顺序 | eligible.csv 实际：q1 Freiheit, q2 Gerechtigkeit, q3 Verantwortung, q4 Zuhause/Heimat, q5 Erfolg |

### 1.3 论文数字 vs manifest.json（口径不一致，需对齐）

| 指标 | manifest.json（SSOT） | 论文 03_results | 状态 |
|------|----------------------|-----------------|------|
| 节点数 | 556 | 557 唯一 (+17 组 = 574) | ❌ 差 ~18 |
| 三语对齐组 | 219 | 247 (43.0%) | ❌ 不一致 |
| 层级分布 | 和=219（仅对齐组） | 和=574（全图） | ⚠️ 同名不同子集 |
| 直接关系数 | 525 | 525 | ✅ 一致 |
| LDS/CDS/HDS/F1/N | **不含** | 有 | ❌ SSOT 不覆盖核心指标 |

### 1.4 未提交的关键数据（有丢失风险，W1 必须先 commit）

`freeze/` · `data/raw/` · `scripts/qc_checks.py` · `scripts/qc_pipeline.py` · `docs/reddit_reply.md`

---

## 2. 研究问题与主张（Part A）

复用 [lds_formal_definition.md](../lds_formal_definition.md) §5 断言链，不重写定义。

| RQ | 研究问题 | 状态 |
|----|----------|------|
| RQ1 | LDS 能否量化跨语言知识图结构差异？（方法验证） | 部分完成（F1 0.939：ZH 0.974 / DE 0.949 / EN 0.882；19 模型 benchmark） |
| RQ2 | ZH/EN/DE 制度性知识图是否系统性不同？（语料） | ✅ 已答：**结构性趋同**；ZH-DE 0.519 远低于噪声底 |
| **RQ3** | **人类自发认知表达是否比制度知识更分歧？（ΔLDS > 0）** | **❌ 未算——核心** |
| RQ4 | 哪些概念/关系驱动跨语言分歧？（可解释性） | 未做 |
| RQ5 | 结论对模型 / 对齐 / 方向 / 阈值稳健吗？ | 部分（敏感性计划 §7.4 未完成） |

### 2.1 核心科学定位（必须诚实面对）

LDS-K 空模型已**自我证伪**"LDS-K 衡量语言分歧"的假设：

- 结构空模型 > 真实 LDS（真实图比度序列随机图**更趋同**）
- 组内噪声底 0.96–0.97；ZH-DE LDS-K = 0.52 **远低于噪声底** → 制度性知识**强烈趋同**，尤其 ZH-DE
- 全部科学价值悬于 **RQ3：LDS-C 是否显著高于 LDS-K（ΔLDS > 0）**

**这意味着**：不能把 LDS-K 当"语言分歧证据"写进论文；它只能作为 ΔLDS 的**基线**。唯一能支撑"语言塑造认知表达"的证据链是 LDS-C > LDS-K。

---

## 3. 关键研究设计决策（Part B）

| 决策 | 内容 | 理由 / 风险 |
|------|------|-------------|
| **D1 招募定位** | 人类侧焦点比较 = **ZH-DE**（6 vs 5 人）；三语人类主张放弃，三语证据由语料 LDS-K + Wikipedia 负对照承担 | EN 大概率保持 0；ZH-DE 语料信号最强（0.52）。可选后台低成本 EN 补量（Reddit 重投 + university pool），若 EN ≥ 2-3 再加 EN-ZH/EN-DE 探索对 |
| **D2 提取模型** | 优先序：研究 provider `gpt-4.1-mini`（若 `OPENAI_API_KEY` 可用）→ Ollama `qwen3:8b` → 本地 `qwen2.5-0.5b-q4_k_m.gguf`。**门控：F1 vs gold labels 达标后才进 LDS-C** | 0.5B GGUF 对 ZH/DE/EN 概念提取质量风险高；提取质量决定 LDS-C 可信度 |
| **D3 主题映射** | 核对 questionnaire JSON / form_structure.csv / eligible.csv / config.yaml / 语料 **五处** q1-q5 映射，建立规范映射表 | 已发现 config.yaml（q3=Erfolg, q4=Familie, q5=Verantwortung）与 eligible.csv 实际（q3=Verantwortung, q4=Zuhause, q5=Erfolg）**不一致**；按主题分析前必须先解决 |
| **D4 分析单元** | LDS-C 在**语言聚合图**（DE 组图 vs ZH 组图）上计算（每主题 + 合并），个体级 LDS 作次要 | 单语言个体只有单图，组内无法跨语言；聚合图是可行的比较单元 |
| **D5 纵深优先** | 少量、深挖：ΔLDS 主线 + 语料深化，不做广度铺陈 | 用户方向；6 周时间窗限制 |

---

## 4. 分析任务（Part C）

### A0 — 数据治理与血缘（先决条件，W1）

- **commit** `freeze/`、`data/raw/`、`scripts/qc_*.py`、`docs/reddit_reply.md`（唯一人类数据 SSOT，防丢失）
- 核对 manifest（556/219）vs 论文（557/247）计数口径；决定扩展 manifest.json 或另立**指标 SSOT**（P1 原则要求论文数字有唯一来源）
- 文档化每条 LDS-K 的 **语料 × 主题 × 语言 × 模型** 血缘（解决 pilot_corpus 主题名 knowledge/language_thought/bilingualism 与论文 5 大主题不一致的问题）
- 落地 D3 主题映射
- 复用：`../../scripts/qc_checks.py` · `../../scripts/qc_pipeline.py` · `release.py` · `LINGUAGRAPH_DATA_LINEAGE.md`

### A1 — 提取 + 建图（核心前置，W2）

- 对 11 份合格回答跑概念/关系提取（按 D2 模型）；构建 DE / ZH 语言聚合图
- 提取 QC：概念数、refusal、去重、质量报告
- 复用：`../../scripts/run_pipeline.py`（重构后统一入口）· `../../scripts/qc_pipeline.py`

### A2 — LDS-C 计算（核心，W2–W3）

- 用**冻结 LDS v3 全公式**（节点 Jaccard + 边 Jaccard，基于对齐组）
  - ⚠️ 现有 `../../scripts/compute_lds_from_db.py` 是**简化版**（仅概念 Jaccard），需升级为 v3 全公式——否则数字不可用于论文
- Bootstrap CI（1000 次，模板见 lds_formal_definition §7.1）
- 空模型：组内 split-half 噪声底、标签置换（威胁解释，见 §6）
- 复用：`../../scripts/figures/_lds_utils.py`

### A3 — ΔLDS 核心分析（核心，W3）

- `ΔLDS = LDS_C − LDS_K`（ZH-DE 焦点；若 D1 补量成功再加 EN 对）
- Bootstrap CI、Cohen's d、功效估算；**诚实试点定位**（小样本、EN 缺口如实报告）
- 产出主图：ΔLDS 对比图

### A4 — LDS-K 深化（语料侧完整证据，W4）

- 5 主题按主题分解；节点 vs 边分量；驱动概念/关系
- 敏感性：阈值 0.85、模型、对齐松紧（synonym vs exact）、有向 vs 无向
- 跨源空模型：教材 vs Wikipedia 同语言（检验 LDS 是"语言"指标还是"来源"指标）
- 复用：`../../scripts/figures/fig1_lds_k_heatmap.py` · `fig4_null_model.py` · `fig_cross_source_null.py` · `fig_wikipedia_lds.py`

### A5 — 可解释性驱动分析（W5）

- 用图证据**验证/证伪**"ZH 集体 / DE 理性 / EN 个体"叙事（idea 提交时的假设）
- 每语言对 top 分歧概念/关系（基于对齐组差分）

### A6 — 模拟基线整合（W5）

- 调和 0.647 vs 0.667 出入（重算或说明）；明确"LLM 默认"对照角色
- 复用：`../../scripts/simulate_baseline.py`

### A7 — 核心图表（W5–W6）

ΔLDS 图 · 主题热图 · 空模型对比 · 驱动网络 · Wikipedia 负对照 · 覆盖图（复用 `../../scripts/figures/`）

---

## 5. 六周里程碑（Part D）

| 周 | 日期 | 任务 | 交付 |
|----|------|------|------|
| W1 | Aug 10–16 | **A0** 治理+血缘+commit；**D3** 映射确认；**D2** 模型 F1 门控 | 数据安全 + 映射表 + 模型选择 |
| W2 | Aug 17–23 | **A1** 提取+QC；**A2** LDS-C 首轮（v3 全公式） | 语言图 + LDS-C 初值 |
| W3 | Aug 24–30 | **A2** 空模型+Bootstrap；**A3** ΔLDS 核心分析+主图 | ΔLDS 结果 + 主图 |
| W4 | Aug 31–Sep 6 | **A4** LDS-K 深化+敏感性+跨源空模型 | 语料侧完整证据 |
| W5 | Sep 7–13 | **A5** 可解释性 + **A6** 基线整合 + **A7** 图表；结果灌入 `../paper/03_results.md` / `04_discussion.md` | 论文可复用结果 |
| W6 | Sep 14–20 | 数字与指标 SSOT 对齐；诚实性审查（试点/小样本标注）；提交组装 | 提交就绪 |

---

## 6. 治理与合规（Part E）

- 遵守三条原则：**SSOT（manifest）· Immutable Release · Validated Pipeline**（[../../.claude/CLAUDE.md](../../.claude/CLAUDE.md) §1）
- **不改任何冻结项**：LDS v3 定义、30 概念共享映射、问卷结构、管线架构、实验方案
- 11 份人类记录 GDPR 合规（已匿名、知情同意，见 `../ethics/`）
- **诚实报告**：小样本、EN 缺口、试点定位、空模型威胁——沿用 [lds_formal_definition.md](../lds_formal_definition.md) §6 已建的反证框架
- 提取质量门控（D2）不达标则**降级为方法演示**，不写成因果证据

---

## 7. 风险（Part F）

| 风险 | 缓解 |
|------|------|
| 弱模型提取质量（0.5B GGUF） | D2 门控：F1 vs gold labels（0.939 目标） |
| 小 N 功效不足（组间比较） | Bootstrap CI + Cohen's d + 试点框架；主检验聚焦 ZH-DE 聚合图 |
| EN=0 三语人类缺口 | D1：ZH-DE 焦点 + 后台低成本 EN 补量（不阻塞主线） |
| 主题映射歧义 | D3/A0 先解决，否则任何按主题分析无效 |
| 语料血缘混乱（多套主题名） | A0 建立规范血缘表 |
| 时间（6 周） | 严格周里程碑；研究优先，非必要包装后置 |

---

## 8. 参考与前置

- [three_month_roadmap.md](three_month_roadmap.md) — 双板块认知模型与 Month 2 计划
- [lds_formal_definition.md](../lds_formal_definition.md) — LDS v3 定义、空模型、统计附录（权威）
- [experiment-design.md](../experiment-design.md) — ⚠️ 已过时（旧 5 主题设计）；以 config.yaml 注释为准
- [recruitment_plan.md](../recruitment_plan.md) — 含 8/16/11 数字矛盾，A0 待修
- [../../release/manifest.json](../../release/manifest.json) — 图结构 SSOT（556 节点 / 219 三语组）
- [../../freeze/freeze_survey_20260703/](../../freeze/freeze_survey_20260703/) — 人类数据唯一 SSOT（未提交）
- [../../scripts/compute_lds_from_db.py](../../scripts/compute_lds_from_db.py) — ⚠️ 需升级为 v3 全公式
- [../../scripts/figures/](../../scripts/figures/) — 现有分析图脚本
