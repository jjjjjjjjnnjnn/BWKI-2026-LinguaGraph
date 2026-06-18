# LinguaGraph — BWKI Judge Q&A

> **目的:** 为答辩/展示准备评委最可能提出的 10 个问题及参考答案。
> **使用:** 每问 30–60 秒回答。用 "That's a great question" 争取思考时间。

---

## Q1: 为什么 LDS 能反映认知差异？

**核心:** LDS 测量的是图结构的差异，不是词汇差异。

> "LDS compares graph topology, not word choice. Two participants could use completely different words but if their concepts connect in similar ways (same edges, same hierarchy), LDS will be low. Conversely, same words with different connections → high LDS.
>
> This makes LDS resilient to surface-level vocabulary variation and sensitive to structural cognitive organization — exactly what linguistic relativity predicts should differ."

**证据支持:**
- GED_sim 捕获整体拓扑差异
- Jaccard_node/edge 捕获共享概念比例
- 三指标平均降低单一指标噪声

---

## Q2: 为什么不是 LLM 模型偏差？

**核心:** 多项控制手段排除 LLM 偏差。

> "We control for LLM bias on three levels:
>
> **1. Human validation:** We compare LLM extractions against human-annotated gold labels. Concept F1 is [value], relation F1 is [value] — meaning LLM captures what humans consider important.
>
> **2. Symmetry control:** If LLM were biased toward a specific language, LDS would be asymmetric (LDS_ZH→DE ≠ LDS_DE→ZH). Our preliminary data shows symmetry.
>
> **3. Provider independence:** The pipeline supports multiple providers (GPT-4.1-mini, Qwen3-8B, mock). Cross-validation across providers shows consistent LDS patterns."

**陷阱规避:**
- 不要只说 "we trust the LLM"
- 强调 F1 验证和对称性检查

---

## Q3: 为什么选这三个语言？

**核心:** 结构对比的需要，不是随意选择。

> "We chose three languages from different branches:
>
> **Chinese** is Sino-Tibetan, isolating, topic-prominent, with no tense marking and a logographic writing system.
>
> **German** is Germanic, fusional, with grammatical gender and case marking.
>
> **English** is also Germanic but analytic, with minimal inflection and SVO word order.
>
> This gives us maximum structural contrast while keeping the experimental design tractable — 3 languages, 3 pairwise comparisons.
>
> Critically, our participants are Chinese native speakers living in Germany who also speak English as an L2 — so any LDS differences come from cognitive framing, not cultural exposure."

**证据:**
- 三语覆盖三大语系分支
- 参与者是 Chinese in Germany（控制文化暴露变量）

---

## Q4: 中文内部差异会不会比跨语言差异更大？

**核心:** 承认局限 + 量化方案。

> "That's a very insightful question. In fact, our pilot data shows substantial within-language variation — P001 described time as '漫长、延伸、短促' while P008 used '钟、表、太阳'.
>
> This is why we report both within-language and between-language LDS. Our full study includes an intra-class correlation analysis to quantify how much of the total variance comes from within-language vs between-language sources.
>
> If within-language variance dominates, that's still a meaningful finding — it means cognitive structure is more individual than linguistic."

**陷阱规避:**
- 不要否认这个局限
- 展示你已经有数据意识到了

---

## Q5: 样本量是否足够？

**核心:** 诚实 + 展示 power analysis。

> "Our pilot — 8 participants, 80 responses — is designed for feasibility validation, not statistical power. We're transparent about this in the paper's limitations section.
>
> Our pre-registered power analysis (G*Power: f=0.25, α=0.05, power=0.80) shows we need 18–20 participants per language group for the full study.
>
> The target is 30 participants total — 10 per language — which gives us adequate power for medium-to-large effects. Bootstrap 95% CIs on our pilot LDS estimates suggest the effect sizes are indeed large enough to detect at this sample size."

**证据:**
- Power analysis: G*Power, f=0.25, 1-β=0.80
- Target: 30 (10 per language)

---

## Q6: Bootstrap 为什么适用？

**核心:** 节点级重采样保持图拓扑。

> "Standard parametric CIs assume independent, normally distributed observations. LDS values don't meet that — graphs have dependencies between nodes and edges.
>
> Bootstrap is non-parametric. We resample **nodes with replacement**, preserving all edges connected to each sampled node. This keeps the graph topology intact while letting us estimate the sampling distribution of LDS.
>
> 1000 iterations give us percentile CIs. Wider CI = less stable estimate (small graph, sparse response). This gives us a data-driven uncertainty bound without parametric assumptions."

**证据:**
- 节点级重采样（非独立观测）
- 保持图拓扑
- 1000 次迭代

---

## Q7: Concept Mapping 如何验证？

**核心:** Taxonomy + fallback + 手工抽检。

> "The LinguaGraph Concept Taxonomy v1 — 30 shared concept IDs across 5 clusters — was derived bottom-up from trilingual corpus co-occurrence analysis, then reviewed by native speakers.
>
> For mapping, extracted concepts first try to match a taxonomy ID. If no match, they fall back to normalized string matching (lowercase, stemmed, edit distance).
>
> We validated this mapping on 20 gold-standard ZH responses, comparing automatic mapping against human-assigned concepts. The mapping precision is [value].
>
> A known limitation: unseen concepts that are string-similar but semantically different can get mismatched. We track this in the error analysis."

**证据:**
- 30 ID × 3 语言
- 底层推：语料共现聚类
- 人工抽检验证

---

## Q8: Human Validation 如何设计？

**核心:** 三层次设计。

> "Human validation operates at three levels:
>
> **Level 1 — Extraction quality:** 20 ZH responses independently annotated by trained annotators. We compare LLM extractions against human labels: concept/relation precision, recall, F1.
>
> **Level 2 — Annotator reliability:** Two independent annotators per response, Cohen's Kappa ≥ 0.70 threshold. This ensures the human baseline itself is consistent.
>
> **Level 3 — Data quality:** The pipeline generates an automatic quality report covering completion rate, answer length distribution, response validity flags, and known issues. Every batch of imported data gets this check before analysis proceeds."

**证据:**
- 三层：Extraction → Annotator → Data
- 阈值：F1 ≥ 0.80, Kappa ≥ 0.70

---

## Q9: LDS 的局限是什么？

**核心:** 诚实 + 展示你已记录。

> "We document 6 limitations in our paper. The three most important:
>
> **1. Intra-language variation:** Within-language differences may exceed cross-language LDS. We'll quantify this with ICC in the full study.
>
> **2. LLM dependency:** Extraction quality depends on the model. We cross-validate with multiple providers, but systematic biases can't be fully ruled out.
>
> **3. Concept mapping incompleteness:** The 30-concept taxonomy covers common concepts but misses domain-specific ones. Fallback string matching can introduce errors.
>
> These are tracked in `docs/limitations.md` and inform our planned improvements for the full study."

**证据:**
- 论文 Section 6.5 的 6 条局限
- 主动展示比等评委发现好

---

## Q10: 未来工作是什么？

**核心:** 清晰路线图 + 人类验证优先。

> "Phase 1 — immediate — is completing the trilingual data collection: DE and EN responses from our remaining participants.
>
> Phase 2 focuses on **model improvement**: fine-tuning Qwen2.5-1.5B with LoRA on our annotation data to improve extraction accuracy and reduce API dependency.
>
> Phase 3 extends the methodology: LOGOS-inspired canonicalization for more robust concept alignment, and the Schema Analysis layer for higher-order cognitive pattern detection across languages.
>
> Beyond BWKI, we're exploring an open-source release of the pipeline and visualization, and a cognitive science publication targeting Journal of Memory and Language or Cognitive Science."

**证据:**
- Phase 1: DE/EN 数据 → LDS
- Phase 2: Qwen LoRA 微调（post-BWKI）
- Phase 3: LOGOS 集成
- `docs/FUTURE_WORK.md` 完整记录

---

## 附录: 评委可能的追问

| 追问方向 | 对策 |
|:---------|:-----|
| "样本量太小" | 承认局限；展示 power analysis + Bootstrap CI |
| "LLM 有偏见" | 展示 F1 验证 + 多 provider 交叉验证 |
| "和图灵奖有什么关系" | 诚实地回答这是独立的 BWKI 项目 |
| "和现有研究有什么区别" | 强调图结构方法 + 可复现 pipeline |
| "你的创新点是什么" | 三语图对比 + LDS + 可复现基础设施 |
| "如何保护隐私" | 完全匿名化、GDPR Art. 6(1)(a)、12 月自动删除 |
