# LinguaGraph — 完整项目状态交接文档（研究重启后）

> **生成时间**: 2026-08-08 | **版本**: v0.7 (研究重启)
> **上一交接**: `docs/session_handoff_20260702.md`（v0.6.2，已被本文件取代）
> **新 AI 加载顺序**: ① 本文件 → ② `docs/planning/restart_plan.md` → ③ `.claude/CLAUDE.md`（治理）

---

## 1. 当前阶段与核心状态

**阶段**: Month 2「理论 + 分析」（8 月），研究重启后。BWKI 提交截止 **2026-09-20/21**（约 6 周）。

**研究主线（重启计划 RQ3，核心）**: ΔLDS = LDS-C − LDS-K > 0（语言驱动的认知分歧）。**已系统检验并诚实证伪（阴性结果）**——见 §3。

**三大不可违反原则**（.claude/CLAUDE.md §1）: SSOT=manifest.json · Immutable Release · Validated Pipeline。

---

## 2. 数据状态（人类数据 SSOT）

| 批次 | 语言分布 | 状态 |
|------|---------|------|
| `freeze/freeze_survey_20260703/` | 6 DE + 5 ZH | ✅ 已提交 (57257ac) |
| `freeze/freeze_survey_20260712/` | 1 ZH + 3 EN | ✅ 已提交 (4317bd8) |
| **合计** | **15 合格（6 DE + 6 ZH + 3 EN）** | 3 EN 为双语 ZH 母语者，作试点 |

**LDS-C 分析数据**（`data/lds_c/`）：
- `extractions_20260807.json` — 15/15 回答概念提取（deepseek-v4-flash，含英文 gloss）
- `relations_20260808.json` — 15/15 回答关系提取（162 边）
- `thematic_classification_20260807.json` — 269/284 gloss 主题分类
- `lds_c_results_20260807.json` / `lds_c_thematic_20260807.json` / `lds_c_v3_results_20260808.json` — 三层分析结果

**API key**: `.env`（gitignored）存 `OPENAI_API_KEY`（opencode GO，deepseek-v4-flash）。**⚠️ key 曾出现在对话中，建议轮换**。端点 `https://opencode.ai/zen/go/v1`（注意带 `/v1`）。

---

## 3. 核心科研发现（三层一致阴性结果，N=15）

### 3.1 概念级 LDS-C
| Pair | LDS-C | 95% CI | 组内 split-half 底 | 标签置换空模型 | ΔLDS vs LDS-K(概念) |
|------|-------|--------|-------------------|---------------|--------------------|
| ZH-EN | 0.961 | [0.936, 0.985] | 0.958 | 0.940 | −0.016 |
| DE-EN | 0.933 | [0.899, 0.986] | 0.923 | 0.938 | −0.044 |
| ZH-DE | 0.934 | [0.908, 0.960] | 0.922 | 0.935 | +0.047 |

### 3.2 主题级（6 类 Codebook v1）
- χ²=9.14, **p=0.519**；置换 p=0.354；Cramér's V=0.117 — **不显著**
- 方向性模式（未达显著）: ZH 高法理(0.12)/道德(0.24)，DE 高自主(0.27)/情感(0.14)，EN 高社会(0.21)
- 最强方向信号: Freiheit 主题 Legal/Institutional 比例 **ZH 0.24 vs DE 0.09 / EN 0.07**

### 3.3 关系级 v3（节点+边）
- LDS v3: ZH-EN 0.977 / DE-EN 0.966 / ZH-DE 0.964
- **Edge-Jaccard ≈ 0**（DE-EN 0.000）；split-half 底 0.958-0.979 ≈ 观测 → **无语言信号**
- ZH-DE ΔLDS=+0.445 是稀疏人类图 vs 密集教材图的结构假象，非语言驱动

### 3.4 统一结论
**在三层分析（概念/主题/关系）上，N=15 组间设计下均无可分离的语言信号**：
1. 观测 LDS-C ≈ 组内 split-half 底 ≈ 标签置换空模型 → **组间参与者变异性主导**
2. **旧论文 N=8 主张（LDS-C 0.70-0.75, ΔLDS>0）不被复制**——旧管线时代产物
3. 核心方法学教训: **组间设计无法分离语言效应与个体差异**；需组内设计 / 更大 N / 结构稳健指标
4. 方向性文化框架差异（ZH 法理·DE 自主·EN 具体）是**可测假设**，留给未来组内设计研究

---

## 4. 已构建的脚本（全部可复现）

| 脚本 | 功能 | 关键点 |
|------|------|--------|
| `scripts/lds_c_extract.py` | 概念提取 | deepseek-v4-flash，按主题，英文 gloss，整卷→按主题回退→修复三重机制，合并保存 |
| `scripts/lds_c_compute.py` | 概念级 LDS-C | 词干+同义词对齐(canonical_key)、Bootstrap、split-half、标签置换、ΔLDS vs LDS-K 概念级重算 |
| `scripts/lds_c_thematic.py` | 主题级分析 | 6 类 Codebook，LLM 分类(BATCH≤15)，χ²+置换+Cramér's V+熵+Wilson CI |
| `scripts/lds_c_extract_relations.py` | 关系提取 | 7 关系类型，按主题，映射到规范 key，8192 token |
| `scripts/lds_c_compute_v3.py` | v3 节点+边 LDS | 冻结公式，Bootstrap，split-half，ΔLDS vs 冻结 LDS-K |
| `scripts/lds_c_canonicalize.py` | LLM 语义规范化 | **模型限制不可行**（deepseek 聚类推理爆炸），保留备将来换模型 |
| `scripts/qc_pipeline.py` / `qc_checks.py` | 数据 QC/freeze | 既有 |

**数据接入流程**（重复使用）: 问卷星导出 xlsx → 解析转换（D3 主题映射规范顺序 [Freiheit, Gerechtigkeit, Verantwortung, Heimat, Erfolg]）→ `data/raw/survey_*.jsonl` → `qc_pipeline.py --freeze` → `freeze_survey_*`。

---

## 5. ⚠️ 关键踩坑（新 AI 必读）

1. **deepseek-v4-flash 推理爆炸**: 对多词聚类/关系任务，模型把全部 token 预算耗在 chain-of-thought（`finish=length, reasoning=8192, content=''`），系统提示无法抑制。
   - **对策**: 分类用 BATCH≤15 + 8192 token；关系/概念按主题小调用；空结果必须重试（`classify_batch` 返回空 dict 不抛异常，需显式检查）；失败 chunk 靠续跑补齐。
   - **不可行任务**: LLM 聚类规范化（deepseek 对聚类彻底失控）——对齐用词干+同义词，或用非推理模型。
2. **`.env` 中 OPENAI_API_KEY 曾入对话** → 建议轮换。
3. **GitHub 当前不可连接** → 只用本地 git 提交（数据已多次提交保护）。
4. **对齐是瓶颈的误判**: 词汇级对齐改进只合并 5% gloss、LDS 几乎不变 → 证明高 LDS 非对齐噪音，而是组间参与者变异性。
5. **输出目录 `outputs/` 被 gitignore** → 计算结果需另存 `data/lds_c/` 才入库。

---

## 6. 论文状态

| 文件 | 状态 |
|------|------|
| `docs/paper/03_results.md` | 现有结果章节（含**过时的 N=8 主张**，与 N=15 分析矛盾） |
| `docs/paper/03_results_human_v2.md` | **新修订 §4**（N=15 三层分析 + 诚实阴性 + 方法学反思）✅ 待合并 |
| `docs/paper/04_discussion.md` | 现有讨论（F11/F12 等需修订） |
| `docs/paper/04_discussion_revision.md` | **修订指引**（F11/F12 + 受影响小节的新措辞）✅ 待应用 |
| 其余章节 (00,01,02,05,06,07) | 未受本轮影响 |

---

## 7. 待办事项（按优先级）

### P0 — 论文整合（提交必需）✅ 已完成 (c2ba9dc)
- [x] 将 `03_results_human_v2.md` 合并进 `03_results.md`（替换旧 §4）
- [x] 按 `04_discussion_revision.md` 修订 `04_discussion.md`（F11/F12、§4.8、§4.12）
- [x] 更新 `00_three_conclusions.md` / `01_abstract` / `05_conclusion`（N=15 一致）
- [ ] 检查 manifest/数字口径对齐（A0 遗留: 556/557、219/247）

### P0.5 — 研究方向决策（✅ 已出文档 + D1 已完成，待论文整合）
- [x] `docs/planning/research_directions_20260808.md`：**D1 LLM-as-Subject 组内设计**（主推）
- [x] **D1 机制实验完成**（`docs/d1_mechanism_results.md`）：
  - **核心结果**：LLM 组内设计语言信号真实（LDS-C 0.93–0.96 ≫ 底 0.85–0.87）→ 人类 N=15 阴性是设计伪影
  - **LMM 机制判定**：`same_lang +0.038 (p<0.001)`, `same_frame +0.001 (p=0.90)` → **代码层主导（M2），框架次级（M3）**——早期 P2 表述已纠正
  - 按主题：Erfolg & Gerechtigkeit 最强；ZH-DE 有结构层
- [ ] **论文整合**：D1 结果 → 论文 §4/§5（LLM-as-subject 范式 + 机制分解 + 组间/组内对照）

### P1 — 研究深化（重启计划剩余）
- [ ] **A4**: LDS-K 深化（按主题分解、敏感性、跨源空模型）— 复用 `scripts/figures/*`
- [ ] **A5**: 可解释性驱动分析（top 分歧概念/关系）
- [ ] **A6**: 模拟基线调和（0.647 vs 0.667）
- [ ] **A7**: 核心图表（ΔLDS、主题热图、空模型对比）

### P2 — 未来研究（讨论部分作为 Future Work）
- [ ] 组内设计新数据（分离语言效应）——**已被 D1（LLM 组内）部分解决**
- [ ] EN 补量至 10 / 或换非推理模型重跑语义规范化

### P3 — 提交组装（9 月中旬）
- [ ] 视频演讲（BWKI 评分项，按研究优先可后置）
- [ ] 最终 Release 打包

---

## 8. 关键链接与参考

| 资源 | 位置 |
|------|------|
| 研究重启计划 | `docs/planning/restart_plan.md` |
| LDS 正式定义/空模型 | `docs/lds_formal_definition.md` |
| 项目治理 | `.claude/CLAUDE.md` |
| 三语问卷/招募 | `docs/recruitment_plan.md`（含数字待核对标注） |
| 人类数据 SSOT | `freeze/freeze_survey_20260703/` + `freeze_survey_20260712/` |
| 分析数据 | `data/lds_c/` |
| LDS-C 计算工具 | `scripts/figures/_lds_utils.py` |
| GitHub | `github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph`（当前不可达） |

---

## 9. Git 状态

最近 13 个提交（本次会话）: SSOT 数据 → 清理归档 → 新数据批次 → LDS-C 提取/计算 → 对齐改进 → 主题分析 → 关系提取/v3 → 论文修订。工作树干净（仅 `.wrangler/` 缓存未跟踪）。

**未提交**: 无（`.wrangler/` 为 Cloudflare 缓存，可忽略）。
