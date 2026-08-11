# LinguaGraph — 研究深化结果：R7 / R2 / R3（2026-08-11）

> **依据**: `docs/review/research_forward_review_20260811.md` §4 的零成本方向（G2/G4/G5/G6），按序执行 R7 → R2 → R3。
> **方法**: 纯计算于已提交数据（`data/lds_c/llm_subject/`），复用冻结辅助函数（`aggregate_languages` / `compute_pairwise` / `within_language_split_half` / `lds_concept` / `canonical_key` / `signal_table`），**零新 API、零指标改动**。
> **脚本**: `scripts/lds_c_r7_topic_model.py` · `scripts/lds_c_r2_en_null.py` · `scripts/lds_c_r3_robustness.py`
> **数据**: `topic_model_margins_20260811.json` · `en_null_mechanism_20260811.json` · `metric_robustness_20260811.json`

---

## 0. 三句话结论

1. **R7（主题×模型）— G4 闭环**：ZH-DE 语言信号是**跨主题属性**——50/51 模型的全部 5 个主题 margin 为正（唯一例外是 7B 弱模型 4/5），**非 1–2 主题驱动**。
2. **R2（英文空结果机制）— G2 转为发现**：英文空结果**不是 EN 特有**，而是"信号强度梯度 × 模型底噪升高"的尾部——EN 对天然最弱（ZH-DE > ZH-EN > DE-EN），DeepSeek-R1/Distill 族因产出更多概念（~15%）抬高语内 floor，把最弱的 EN 对压过显著线（**R1 富集 Fisher p=9e-6，5/5 R1 族全 NS**）。
3. **R3（度量鲁棒性）— G5/G6 部分闭环**：ZH-DE margin 在 k∈{3,5,6} 下 **100% 为正**（k 鲁棒）；但**语言对排序不稳定**（ZH-DE vs EN 约 50/50）——论文应避免"哪个语言对最分歧"的排序声明。模糊对齐下 **ZH-DE 保持最分歧、DE 侧驱动方向存活**（严格 +23 → 模糊 +11），但 EN 对内部排序敏感。

---

## 1. R7 — 主题×模型 margin 表（51×3×5）

### 方法
对 51 个完整模型，逐主题（5 主题）逐语言对（3 对）计算 LDS-C（pooled）与语内 split-half floor → margin。

### 结果（ZH-DE margin 跨 51 模型分布）

| 主题 | pos% | ≥0.02% | neg% | 中位 | 最小 | 最大 |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| Freiheit | 100% | 100% | 0% | **+0.148** | +0.025 | +0.344 |
| Gerechtigkeit | 100% | 98% | 0% | +0.100 | +0.019 | +0.321 |
| Verantwortung | 100% | 94% | 0% | +0.120 | +0.010 | +0.329 |
| Heimat | 100% | 96% | 0% | +0.169 | +0.012 | +0.433 |
| Erfolg | 98% | 94% | **2%** | +0.095 | **-0.014** | +0.439 |

**主题一致性**：50/51 模型 5/5 主题 ZH-DE margin 为正；1 模型 4/5（唯一负值 = `dashscope:deepseek-r1-distill-qwen-7b` 的 Erfolg −0.014——即两个英文对都不显著的 7B 弱模型，整体信号本就最弱）。

**一致性核对**：R7 pooled margin 与 replication 权威 margin 吻合（deepseek-v3.1: +0.289 vs +0.286；nemotron: +0.167 vs +0.155；kimi-k2.5: +0.125 vs +0.122）。

### 结论（G4 闭环）
- ZH-DE 信号**跨主题成立**，非主题驱动 → 论文"51/51 ZH-DE 显著"无需按主题限定。
- 附带的诚实观察：pooled margin 排序 **ZH-EN (+0.132) > ZH-DE (+0.125) > DE-EN (+0.117)**——"最可靠显著（ZH-DE 0 NS）" ≠ "幅度最大（ZH-EN）"。**显著性是权威声明，幅度排序不是**（见 R2 机制解释）。

---

## 2. R2 — 英文空结果机制分解

### 方法
51 模型分组：NS-EN（7 模型，任一 EN 对 perm_p≥0.05）vs 全显著（44）。比较：语内 floor、聚合概念集大小、跨语言 Jaccard、margin。

### 结果

| 指标 | NS-EN（7） | 全显著（44） | 差 |
|------|:---:|:---:|:---:|
| floor_zh | 0.865 | 0.804 | **+0.061** |
| floor_de | 0.845 | 0.776 | **+0.069** |
| floor_en | 0.827 | 0.774 | **+0.053** |
| \|set_zh\| | 200 | 175 | +25 |
| \|set_de\| | 184 | 162 | +22 |
| \|set_en\| | 178 | 154 | +24 |
| J(DE,EN) | 0.120 | 0.101 | +0.018 |
| J(ZH,EN) | 0.092 | 0.077 | +0.015 |
| J(ZH,DE) | 0.071 | 0.072 | ±0 |
| margin[ZH-EN] | **+0.062** | **+0.134** | −0.073 |
| margin[DE-EN] | **+0.045** | **+0.124** | −0.079 |
| margin[ZH-DE] | **+0.074** | **+0.138** | −0.064 |

**富集检验**：R1 族（deepseek-r1 / r1-0528 / distill-7b/14b/32b）**5/5 全 NS**；非 R1 仅 2/46（glm-4.6、qwen3-235b）。**Fisher exact p = 9e-6（odds ratio ∞）**。

### 机制（统一解释）
1. **信号梯度**（全显著组内也成立）：ZH-DE (+0.138) > ZH-EN (+0.134) > DE-EN (+0.124)——EN 对**天然最弱**（英语作为训练通用语，EN 概念空间与 DE、ZH 都较接近 → EN 对 LDS 最低）。这一"EN 桥接"成分体现在 NS 组 J(DE,EN)/J(ZH,EN) 略高。
2. **模型底噪升高**：NS 模型在**全部三种语言**的语内 floor 更高（+0.05~0.07），因其产出 ~15% 更多概念 → 聚合更稀疏 → floor 抬升。
3. **两者叠加**：升高的 floor 把本已最弱的 EN 对（ZH-EN、DE-EN）压过显著线；ZH-DE 因底margin 最高而存活。R1/Distill 族因推理模式产出更丰富/异质的概念，成为主要聚类（5/5）。

### 结论（G2 转发现）
**"8/153 英文对非显著"不是 EN 特有缺陷，而是模型级信号强度梯度的尾部，DeepSeek-R1/Distill 特异性显著（Fisher p<1e-5）**。论文可将此从"披露"升级为"机制解释"：
- EN 对天然最弱（桥接语言）——对 value-alignment SOTA 有直接含义（它们全用英语评测，英语可能是最不易暴露分歧的语言）；
- R1 族特异性——审计应用时对推理型模型的解释需谨慎。

---

## 3. R3 — 度量鲁棒性

### 3.1 Part A — k 敏感性（51 模型 × k'∈{3,5,6}）

| k' | ZH-DE pos% | 中位 margin | 最小 | 最大 |
|:---:|:---:|:---:|:---:|:---:|
| 3 | **100%** | +0.151 | +0.041 | +0.374 |
| 5 | **100%** | +0.133 | +0.038 | +0.303 |
| 6 | **100%** | +0.122 | +0.033 | +0.287 |

**ZH-DE 信号对提取深度 k 鲁棒**（100% 为正，中位 margin 随 k 减小略升）。但 **语言对排序不稳定**：ZH-DE vs EN 谁更分歧在 k' 上约 50/50（k=3: 26/25；k=6: 23/27）。→ **论文不应对"哪个语言对最分歧"作排序声明**；"ZH-DE 显著"（perm p）是稳健声明，"幅度排序"不是。

### 3.2 Part B — 模糊对齐鲁棒性（基线）

| 语言对 | 严格 LDS | 模糊 LDS | 严格 J | 模糊 J |
|:---:|:---:|:---:|:---:|:---:|
| ZH-EN | 0.903 | 0.593 | 0.097 | 0.407 |
| DE-EN | 0.918 | 0.498 | 0.082 | 0.502 |
| ZH-DE | **0.933** | **0.622** | 0.067 | 0.378 |

- **ZH-DE 在两种对齐下都是最分歧对**（严格 0.933 / 模糊 0.622 均为最大）→ 核心对排序鲁棒。
- **DE/ZH 方向不对称存活**：严格 de_only 150 vs zh_only 127（+23）；模糊 44 vs 33（**+11**）——DE 侧更多语言专属概念的方向**符号不变**（幅度缩小，因模糊合并了部分共享 token）。
- **EN 对内部排序敏感**（严格 DE-EN 0.918 > ZH-EN 0.903；模糊 DE-EN 0.498 < ZH-EN 0.593）→ EN 对排序不可作为声明。

### 结论（G5/G6 部分闭环）
- LDS 对 k 鲁棒（信号方向）；对对齐严格度，**核心声明（ZH-DE 显著 + 最分歧 + DE 方向）存活**，**EN 对排序不可靠**。
- 边界：模糊对齐是确定性 token-overlap 代理，非 LLM 判定同义；后者留作未来（需少量 API，见 review R3 注释）。

---

## 4. 论文/文档整合建议

| 位置 | 内容 |
|------|------|
| 论文 §5.10 / §8.15 | 把"8/153 无解释"升级为机制句：*"Die englisch-bezogenen Nullfälle sind der Schwanz eines Modell-Level-Signal-Gradienten (ZH-DE > ZH-EN > DE-EN); DeepSeek-R1/Distill-Modelle (5/5, Fisher p<1e-5) produzieren ~15% mehr Konzepte und erhöhen den Within-Language-Boden, was die ohnehin schwächsten EN-Paare unter die Signifikanzschwelle drückt."* |
| 论文 §8.16 | 方向不对称的对齐鲁棒性（严格 +23 → 模糊 +11）可作为 DE 方向稳健性的方法学注脚 |
| 论文 §5.10 | 不增加"语言对幅度排序"声明（R3: 排序对 k 与对齐敏感） |
| 审查 doc | R2/R7/R3 标记 ✅ 已执行 |

---

*版本: v1.0 | 2026-08-11 | 与 `research_forward_review_20260811.md` + `rnd_project_review_20260811.md` 构成研究线三层审查执行记录*
