# Lane-1 附录草稿：人类教材图 vs 权重向量图对比 — 新增文献支撑（2026-09-16）

> 状态：**已并入 `docs/paper/02_related_work.md`（2026-09-16，C线执行）**。并入位置：污染→§2.5 末段方法限定；几何→新 §2.6 第一段；RSA/CKA→新 §2.6 第二段；残差→§2.4 末段 + §2.7（原 §2.6 改号）Forschungslücke 第 6 点；书目 [55]–[64] 追加于文末（无 `arXiv:` 字串，CI 计数保持 18）。
> 现有编号：已确认 `[1]–[54]`（见 `docs/paper/02_related_work.md`）；本稿 `[55]–[64]` 已占号并入，无重叠、无断裂。
> 联网验证（2026-09-16，逐篇可达）：[55] ACL Anthology 2023.findings-emnlp.722 ✅；[56] arxiv.org/abs/2311.04850 ✅；[57] ACL Anthology 2024.findings-emnlp.532（页码 9113–9129 与 ACL 一致）✅；[58] PMLR v235/park24c + arxiv 2311.03658 ✅；[59] ACL Anthology 2021.conll-1.7（页 82–93）✅；[60] ACL Anthology 2024.eacl-long.3 ✅（作者按 ACL 官方记作 Clergerie, É.，候选表“de la Clergerie”已按官方修正）；[61] PMLR v97/kornblith19a ✅；[62] PMLR v285/williams24a ✅；[63] ACL Anthology 2023.findings-acl.189（页 3020–3042）✅；[64] arxiv.org/abs/2404.06228（备注 Camera-ready ACL Findings 2024）✅。10 篇零替换、零编造。

## 0. 逻辑环映射（本稿工作定义）

- **P2（方法有效性环）**：图对比方法本身是否可信（对齐标签是否为 artefact、几何度量是否恰当、RSA/CKA 是否适用）。
- **P3（结构解释环）**：权重几何与人类教材结构差异如何解释（线性表征、各向异性、跨语言残差）。
- **P4（污染/替代解释环）**：权重侧信号是否可能来自预训练污染/记忆而非真实结构知识（去污染、复述样本、推理时净化）。

## 1. 新增候选表（建议编号 [55]–[64]）

| 建议编号 | 类别 | 文献（完整引用） | 出处验证 |
|---|---|---|---|
| [55] | 污染·经典 | Sainz, O., Campos, J., García-Ferrero, I., Etxaniz, J., Lopez de Lacalle, O., & Agirre, E. (2023). NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for each Benchmark. *Findings of EMNLP 2023*, 10776–10787. DOI: 10.18653/v1/2023.findings-emnlp.722. URL: https://aclanthology.org/2023.findings-emnlp.722/ | ACL Anthology 已验证 |
| [56] | 污染·最新方法 | Yang, S., Chiang, W.-L., Zheng, L., Gonzalez, J. E., & Stoica, I. (2023). Rethinking Benchmark and Contamination for Language Models with Rephrased Samples. *arXiv:2311.04850*. URL: https://arxiv.org/abs/2311.04850 | arXiv 已验证 |
| [57] | 污染·最新净化 | Zhu, Q., Cheng, Q., Peng, R., Li, X., Peng, R., Liu, T., Qiu, X., & Huang, X. (2024). Inference-Time Decontamination: Reusing Leaked Benchmarks for Large Language Model Evaluation. *Findings of EMNLP 2024*, 9113–9129. DOI: 10.18653/v1/2024.findings-emnlp.532. URL: https://aclanthology.org/2024.findings-emnlp.532/ | ACL Anthology 已验证 |
| [58] | 权重几何·核心理论 | Park, K., Choe, Y. J., & Veitch, V. (2024). The Linear Representation Hypothesis and the Geometry of Large Language Models. *Proc. ICML 2024*, PMLR 235. *arXiv:2311.03658*. URL: https://arxiv.org/abs/2311.03658 | arXiv+PMLR 已验证 |
| [59] | 权重几何·经典探测 | Hernandez, E., & Andreas, J. (2021). The Low-Dimensional Linear Geometry of Contextualized Word Representations. *Proc. CoNLL 2021*. URL: https://aclanthology.org/2021.conll-1.7.pdf | ACL Anthology 已验证 |
| [60] | 权重几何·最新各向异性 | Godey, N., de la Clergerie, É., & Sagot, B. (2024). Anisotropy Is Inherent to Self-Attention in Transformers. *Proc. EACL 2024 (Vol.1 Long)*, 35–48. DOI: 10.18653/v1/2024.eacl-long.3. *arXiv:2401.12143*. URL: https://aclanthology.org/2024.eacl-long.3/ | ACL Anthology 已验证 |
| [61] | RSA/CKA·经典 | Kornblith, S., Norouzi, M., Lee, H., & Hinton, G. (2019). Similarity of Neural Network Representations Revisited. *Proc. ICML 2019*, PMLR 97, 3519–3529. *arXiv:1905.00414*. URL: https://proceedings.mlr.press/v97/kornblith19a.html | PMLR+arXiv 已验证 |
| [62] | RSA/CKA·最新统一 | Williams, A. H. (2024). Equivalence between representational similarity analysis, centered kernel alignment, and canonical correlations analysis. *Proc. UniReps Workshop 2024*, PMLR 285, 10–23. URL: https://proceedings.mlr.press/v285/williams24a.html | PMLR 已验证 |
| [63] | 跨语言残差·经典关联 | Gaschi, F., Cerda, P., Rastin, P., & Toussaint, Y. (2023). Exploring the Relationship between Alignment and Cross-lingual Transfer in Multilingual Transformers. *Findings of ACL 2023*, 3020–3042. URL: https://aclanthology.org/2023.findings-acl.189.pdf | ACL Anthology 已验证 |
| [64] | 跨语言残差·最新综述 | Hämmerl, K., Libovický, J., & Fraser, A. (2024). Understanding Cross-Lingual Alignment — A Survey. *Findings of ACL 2024*. *arXiv:2404.06228*. URL: https://arxiv.org/abs/2404.06228 | arXiv+ACL 已验证 |

## 2. 每篇：主张 / 可借用点 / 逻辑环 / 作证句

### [55] Sainz et al. 2023（污染·经典）
- **一句话主张**：最坏的污染是 LLM 在某 benchmark 的 test split 上训练后又在同一 benchmark 上被评估，会系统性高估性能并导致错误科学结论。
- **一句话可借用点**：为"权重向量图可能含记忆而非理解"提供污染分级与度量呼吁，可直接支撑 P4 的保守解释条款。
- **对应逻辑环**：P4。
- **作证句**：正如 Sainz et al. [55] 所警示，test-set 污染会高估模型能力，因此权重侧与人类教材图的一致性必须先排除记忆效应，方能作结构知识解释。

### [56] Yang et al. 2023（污染·复述样本）
- **一句话主张**：n-gram 重叠式去污染不足以检出 paraphrase/translation 改写的复述样本；13B 模型过拟合此类变体即可达到与 GPT-4 相当的 benchmark 分数。
- **一句话可借用点**：借用其 "LLM-based decontaminator" 思路，论证仅做字面去重不足以保证权重图干净，需语义级去污染声明。
- **对应逻辑环**：P4（主）/ P2（方法严谨性，次）。
- **作证句**：依 Yang et al. [56]，字面去重后残留的复述样本仍可驱动分数虚高，故本研究的权重—教材一致性比较须报告语义级污染检查，否则 P4 不闭合。

### [57] Zhu et al. 2024（污染·推理时净化）
- **一句话主张**：提出 Inference-Time Decontamination（ITD），在不改变难度的前提下检测并改写泄露样本，GSM8K/MMLU 上可消解约 19–23% 的记忆虚高。
- **一句话可借用点**：为权重侧评估提供"泄露 benchmark 仍可复用但须净化"的操作模板，对应本研究权重向量采样的稳健性检查。
- **对应逻辑环**：P4。
- **作证句**：Zhu et al. [57] 证明推理时改写可剥离记忆红利，这为权重向量图的净化对照实验提供了可直接套用的范式。

### [58] Park, Choe & Veitch 2024（权重几何·线性表征）
- **一句话主张**：用反事实语言形式化线性表征假设，证明 unembedding 表征连向线性探测、embedding 表征连向干预，并引入尊重语言结构的因果内积统一二者（LLaMA-2 实证）。
- **一句话可借用点**：为"从权重向量中读出概念方向并与教材图节点对比"提供理论许可证，同时警告内积选择决定 cosine/projection 结论。
- **对应逻辑环**：P3（主）/ P2（度量选择，次）。
- **作证句**：按 Park et al. [58]，概念方向的可读性依赖因果内积而非朴素欧氏几何，故权重—教材的结构对比必须声明距离度量，否则几何结论不可比。

### [59] Hernandez & Andreas 2021（权重几何·低维探测）
- **一句话主张**：ELMo/BERT 中大量句法—语义特征编码于低维线性子空间，且具层级包含关系、分布于神经元而非单神经元，并可因果操控模型行为。
- **一句话可借用点**：支撑"权重向量图的边/层级可与教材前提链做同构比较"的方法直觉，且低维性为降维对比（如 CKA 前的投影）提供依据。
- **对应逻辑环**：P3。
- **作证句**：Hernandez & Andreas [59] 表明语言特征本就占据低维因果子空间，因此权重向量与人类教材层级（HDS）的可比性不是类比，而是同类线性结构的比较。

### [60] Godey, de la Clergerie & Sagot 2024（权重几何·各向异性）
- **一句话主张**：各向异性不只源于长尾 cross-entropy，而是自注意力为形成 sharp pattern 而使 Q/K 同向漂移的内禀属性，跨模态与未训练层亦然。
- **一句话可借用点**：凡用 cosine 比较权重向量与教材嵌入者，必须先处理各向异性/均值漂移，否则相似度虚高。
- **对应逻辑环**：P2（主）/ P3（次）。
- **作证句**：依 Godey et al. [60]，各向异性是 Transformer 内禀的，权重—教材图的 cosine 对比若不做中心化/白化，其 P2 方法有效性不成立。

### [61] Kornblith et al. 2019（RSA/CKA·经典）
- **一句话主张**：CCA 类对可逆线性变换不变的指标在维度大于样本数时失效；CKA（中心化核对齐，等价 RV 系数）可可靠识别不同初始化/宽度/架构间的层对应。
- **一句话可借用点**：为"人类教材图 RDM vs 权重 RDM"的二阶比较提供标准工具 CKA（linear/RBF），替代脆弱的 CCA。
- **对应逻辑环**：P2。
- **作证句**：Kornblith et al. [61] 的 CKA 为跨表征比较提供了经检验的标准，本研究的人类图—权重图结构对比应以 linear CKA 为主指标以保 P2。

### [62] Williams 2024（RSA/CKA·统一）
- **一句话主张**：一旦对 RSA 的相异矩阵做均值中心化，RSA 与 CKA（及 CCA）在数学上大体等价，终结了二者数值分歧的争论。
- **一句话可借用点**：允许本研究在正文用 RSA 语言、在附录用 CKA 复核而不被指双重标准；统一声明即可互认。
- **对应逻辑环**：P2。
- **作证句**：Williams [62] 的等价性结果意味着 RSA 与 CKA 可互为稳健性检查，本研究以其一为主、另一为复核即满足 P2 的方法三角验证。

### [63] Gaschi et al. 2023（跨语言·对齐—迁移关联）
- **一句话主张**：多语言 Transformer 的对齐度（尤其是 strong alignment）与 zero-shot 跨语言迁移显著相关；微调与 realignment 的效果取决于任务、模型大小与语言距离（如 EN→AR POS 可 +15.8）。
- **一句话可借用点**：为"对齐后仍残留的结构分歧（LDS 式残差）具有下游意义"提供实证先例，且 distant pair 预期更大分歧。
- **对应逻辑环**：P3（主）/ P2（次）。
- **作证句**：Gaschi et al. [63] 表明对齐—迁移相关但不完全，恰为"对齐后残差"（本研究的跨语言结构分歧）留出了理论位置与实证预期（远距离语言对分歧更大）。

### [64] Hämmerl, Libovický & Fraser 2024（跨语言·综述）
- **一句话主张**：系统综述 2019–2023 对齐方法，区分 weak/strong alignment，指出强对齐以牺牲语言特异信息为代价，且生成模型须权衡语言中立与语言特异轴。
- **一句话可借用点**：为本研究的"对齐≠抹平分歧"立场提供权威综述背书，并可引用其分类法定义本研究的残差类型。
- **对应逻辑环**：P3。
- **作证句**：Hämmerl et al. [64] 的综述确认最大化对齐会损害语言特异信息，因此跨语言教材图的结构残差应被解读为预期现象而非对齐失败。

## 3. 与现有文献关系（不冲突声明）

- 与 `[16]–[19]`（MTransE/实体对齐）**不冲突**：既有文献回答"如何对齐"，新增 `[63][64]` 回答"对齐后为何仍有残差"，是互补而非替代。
- 与 `[20]–[24]`（WorldValuesBench/多语言价值）**不冲突**：既有文献测"价值选择"，新增 `[58][59][61][62]` 支撑"结构组织"的可测性，属正交维度。
- 与 `[25][26]`（跨语言 KG 迁移/文化擦除）**不冲突**：新增 `[63][64]` 强化而非削弱其结论（残差预期内）。
- 与 `[33]–[36]`（AI 文本标记）**不冲突**：新增 `[55]–[57]` 只谈 benchmark 污染与净化方法，不 претендуют AI 文本检测结论，不抢断言。
- 与 `[40][41]`（within-subject power）**不冲突**：新增 `[61][62]` 只谈表征相似度量，不涉及实验设计效力。
- 编号无冲突：现有 `[1]–[54]`（`02_related_work.md:63–171`）未收录以上 10 篇中的任何一篇（按标题/作者比对），`[55]–[64]` 为空号段，可直接并入。

## 4. 缺口核验

- 污染 2–3 篇：✅ 3 篇（[55] 经典立场 + [56] 复述污染 + [57] 推理时净化）。
- 权重几何 2–3 篇：✅ 3 篇（[58] 线性表征理论 + [59] 低维探测经典 + [60] 各向异性最新）。
- RSA-CKA 1–2 篇：✅ 2 篇（[61] CKA 经典 + [62] RSA/CKA/CCA 统一）。
- 跨语言结构残差 1–2 篇：✅ 2 篇（[63] 对齐—迁移实证 + [64] 对齐综述）。
- 合计 10 篇，**四类缺口已补齐**，可进入 §2.7/附录起草阶段；`02_related_work.md` 本体未动。

## 5. 待办（并入正文前）

- [x] 在 `02_related_work.md` 按 `[55]–[64]` 插入作证句（C线已执行：§2.4 残差段、§2.5 污染段、新 §2.6 几何+RSA、§2.7 第 6 点、文末书目）。
- [ ] 若审稿要求页数压缩，优先保留 `[55][58][60][61][63][64]`（6 篇骨干），`[56][57][59][62]` 可退附录。
- [x] 出处验证：10 篇 2026-09-16 逐篇联网验证可达（见文件头），零替换、零编造。

## 6. 红蓝对抗（C线阶段门禁，2026-09-16）

红队 5 攻 → 蓝队 5 防（均已落地）：

1. **攻：引用堆砌（citation stuffing）**——10 篇一次性并入，有为凑数而引之嫌。**防**：每篇有且仅有一个逻辑环位置（P2/P3/P4 映射见 §2），压缩预案保留 6 篇骨干；正文每段以方法限定句收尾（Preliminary、无本研究 Befund），不做装饰性引用。
2. **攻：错位引用（misplaced citation）**——污染文献塞进价值对齐 §2.5、几何文献打断 curriculum 主线。**防**：污染段明确标注“Methodische Qualifizierung … keine eigene Messung”并挂钩 P4；几何/RSA 独立成新 §2.6（Preliminary-Hintergrund），原 §2.6 顺延为 §2.7，主线未被打断；残差段落在 §2.4 对齐讨论之后，承接 LDS 残差语义。
3. **攻：编号断裂（broken numbering）**——新增 [55]–[64] 与既有 [1]–[54] 冲突或正文引用悬空。**防**：逐标题比对确认 [55]–[64] 为空号段；正文引用 [55]–[64] 与文末书目一一对应（[55][56][57]§2.5、[58][59][60][61][62]§2.6–§2.7、[63][64]§2.4+§2.7），无悬空、无跳号。
4. **攻：与 [1]–[54] 冲突**——新文献结论可能推翻既有立场（如强对齐损害特异性 vs. [16]–[19] 对齐目标；CKA 标准 vs. 既有度量）。**防**：§3 不冲突声明逐项复核：[63][64] 回答“对齐后为何仍有残差”，与 [16]–[19]“如何对齐”互补；[58][59][61][62] 支撑“结构可测性”，与 [20]–[24]“价值选择”正交；§2.6 明确 CKA 为“künftiger Vergleich”标准，不追溯否定既有 frozen-v3 度量。
5. **攻：过度主张（overclaiming）**——把背景文献写成 kebehauptete Befunde（如 ITD 百分比、+15.8 改进、anisotropy 内禀性被读作本研究结论）。**防**：所有新增段落均有 Preliminary/keine-eigene-Messung 限定；数字（−22,9 %/−19,0 %、+15.8）明确归属原作者实验条件；残差段以“kausale Attribution … ungetestet”收尾；Forschungslücke 第 6 点标注“sämtlich Preliminary-Hintergrund, keine Befunde dieser Studie”。

门禁记录：`arXiv:` 计数 = 18（与并入前一致，新增条目均用 DOI/URL 而不用 `arXiv:` 前缀）；`pytest tests/ -q` 通过（C线只动 docs + research，不碰 tests/freeze/_deploy/data/db）；`git diff --stat` 仅两文件。
