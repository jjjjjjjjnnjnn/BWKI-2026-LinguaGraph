# Deep Evidence（支持性旁证，非项目发现）— 2026-09-14

> 定位：W3 深论据补强用旁证集。只收录**开源论文 / 公开信息**对以下 5 点的**支持性旁证**。
> 红线：外部结论一律不写成项目发现；凡站不住、跨度过大的引用一律标 **“暂缓引用”**。
> SSOT 与已验证发现以 `manifest.json` / `RESEARCH_RULES.md` v0.13.2 为准；本文件不新增概念 / 指标 / 功能。

- 日期：2026-09-14
- 引用总数：15（①3 + ②3 + ③3 + ④3 + ⑤3）＋ 1 条“暂缓引用”说明
- 使用方式：答辩/论文中仅可表述为“与公开文献中的已知现象一致”，不可表述为“本项目证明了该文献结论”或反之。

---

## ① Jaccard 硬匹配：组合爆炸 / 边集敏感

项目侧含义（仅背景，不算发现）：精确图匹配代价高、硬交并比对边集扰动敏感，因此用 Jaccard (mapped) 只报告“非零相似”，不做精确等价断言。

1. 作者+年份：Riesen & Bunke (2009)
   结论一句话：精确图编辑距离（GED）计算复杂度随节点数指数增长，精确解仅对小图可行，故大图须用近似/次优匹配。
   URL: https://doi.org/10.1016/j.imavis.2008.04.004
2. 作者+年份：Limmer & Kriege (2026, arXiv:2607.18914)
   结论一句话：GED 可归约子图同构/最大公共子图等经典 NP-hard 问题，因此本身也是 NP-hard，佐证“硬匹配组合爆炸”不是实现问题而是复杂度本质。
   URL: https://arxiv.org/abs/2607.18914
3. 作者+年份：NVIDIA cuGraph 文档（Jaccard Similarity, 2023–2025 版）
   结论一句话：Jaccard 定义为交/并，计算量 O(d·n)，文档明确提示不适用于超大稀疏图与节点度差异极大的图，佐证边集/规模差异会显著影响该指标行为。
   URL: https://docs.rapids.ai/api/cugraph/stable/graph_support/algorithms/jaccard_similarity

---

## ② 图噪声底限 / 同语言高漂移合理性

项目侧含义（仅背景）：自动抽取构图必然带噪；同语言内出现可观漂移并不反常，需先设“噪声底限”再谈跨语言差异。

1. 作者+年份：Deng et al. (2023, EMNLP Findings, GOLD)
   结论一句话：无监督自动扩大的常识知识图谱会引入损害质量的 spurious noise，需要全局规则+局部结构联合去噪。
   URL: https://aclanthology.org/2023.findings-emnlp.232/
2. 作者+年份：Liu et al. (2024, AAAI, Contrastive KG Error Detection)
   结论一句话：KG 常含多类错误，且噪声三元组与语义相近的正确三元组难以区分，佐证“底噪客观存在、去噪有难度”。
   URL: https://ojs.aaai.org/index.php/AAAI/article/view/28729/29407
3. 作者+年份：Chang et al. (2023, ACL long, Linguistic Dataset Drift)
   结论一句话：提出词汇/结构/语义三维语言数据漂移并验证其可预测模型表现，佐证即使在同一语言分布内也可度量到实质性漂移。
   URL: https://aclanthology.org/2023.acl-long.498

---

## ③ 先修深度上限 / 认知阶梯

项目侧含义（仅背景）：为先修链设深度上限提供教育学旁证——认知按层级递进、工作记忆有限，深链不适合一次性教学/评估。

1. 作者+年份：Bloom et al. (1956)
   结论一句话：提出认知域六层级（记忆→理解→应用→分析→综合→评价），为“知识有层级阶梯”提供经典框架旁证。
   URL: https://teaching.cornell.edu/resource/blooms-taxonomy
2. 作者+年份：Anderson & Krathwohl et al. (2001, Bloom 修订版)
   结论一句话：修订为 Remember / Understand / Apply / Analyze / Evaluate / Create 六过程并配知识维度，佐证高阶能力建于低阶之上、需分层设计。
   URL: https://cft.vanderbilt.edu/wp-content/uploads/sites/59/BloomsTaxonomy-mary-forehand.pdf
3. 作者+年份：Sweller (1988)
   结论一句话：手段-目的分析式解题占用大量认知容量从而挤占图式习得，佐证链过深/负荷过载会损害学习，支持“设上限、分段教”的审慎做法。
   URL: https://doi.org/10.1207/s15516709cog1202_4

---

## ④ 课程标准差异（CN 高覆盖 vs DE Kompetenz 低覆盖）

> 方法声明：未找到可直接量化“CN 覆盖率高 vs DE 覆盖率低”的开源对照表；以下只分别佐证两侧的制度形态，**直接的“高 vs 低”对比结论暂缓引用**，项目内覆盖率差异仍以自有 Lama-app 语料统计为准，不借外部文献背书。

1. 作者+年份：中国教育部 MOE (2022, 义务教育课程方案和课程标准 2022 年版)
   结论一句话：2022 年修订发布 16 科义务教育课程方案与标准、九年 9522 课时并给出学业质量与“教—学—评”细化指导，佐证 CN 侧为全国统一、细粒度、高规定的课程标准形态。
   URL: http://en.moe.gov.cn/news/press_releases/202205/t20220507_625532.html
2. 作者+年份：Wang (2019, ERIC EJ1226266, Curriculum Change and Policy Redesign in China)
   结论一句话：中国课程方案与标准同时承担专业指导与行政管理功能，直接约束教材与学习材料设计，佐证其高覆盖/强约束属性的制度逻辑。
   URL: https://files.eric.ed.gov/fulltext/EJ1226266.pdf
3. 作者+年份：KMK (2003/2004, Bildungsstandards; 2022 修订版说明)
   结论一句话：德国 KMK Bildungsstandards 定义为各学段应达成的 fachbezogene Kompetenzen（能力导向的规范参照点），由各州据此制定课程与教学，佐证 DE 侧为 Kompetenz 导向、给教师与州留自由度的形态。
   URL: https://www.kmk.org/bildungsministerkonferenz/bildungsthemen/bildungsstandards.html
   辅证 URL: https://files.eric.ed.gov/fulltext/ED577138.pdf（Atmacasoy 2017：德国课程以概括方式制定、为教师留自由度）
- **暂缓引用**：Huang (2024) 的中德教育体制比较综述可作背景阅读，但其为会议综述、非课程覆盖率实证统计，不用作“CN 高覆盖 vs DE 低覆盖”的直接引证。
  URL: https://doi.org/10.54097/3be6kt31

---

## ⑤ LLM 抽取幻觉 + 多数投票去噪

项目侧含义（仅背景）：LLM 抽取会幻觉；多次采样一致性可用于检测/缓解幻觉，但一致的幻觉仍可能漏网，故多数投票只是去噪手段而非正确性保证。

1. 作者+年份：Manakul, Liusie & Gales (2023, EMNLP, SelfCheckGPT)
   结论一句话：若 LLM 掌握某概念则多次采样回答彼此一致，幻觉事实则采样间发散/矛盾，因此可用采样一致性做黑盒零资源幻觉检测。
   URL: https://aclanthology.org/2023.emnlp-main.557
2. 作者+年份：Wang et al. (2022, arXiv:2203.11171; ICLR 2023, Self-Consistency)
   结论一句话：对同一问题采样多条 CoT 推理路径再多数投票取最一致答案，可大幅提升推理准确率（如 GSM8K +17.9%），为多数投票去噪提供方法旁证。
   URL: https://arxiv.org/abs/2203.11171
3. 作者+年份：Chen et al. (2025, arXiv:2510.19507, Teaming LLMs)
   结论一句话：单模型一致性方法会在“一致性幻觉”（错误答案赢得多数票、低语义熵）上失效，需多模型 consortium voting/entropy 进一步缓解，佐证多数投票的边界。
   URL: https://arxiv.org/pdf/2510.19507

---

## 使用规范（防越界）

- 答辩口径模板：“该现象与 [作者年份] 在公开文献中报告的 [一句话结论] 方向一致；项目内数值仍以冻结数据与复现脚本为准。”
- 禁止口径：“本项目证明了 XX 文献”“XX 文献证明了本项目发现”“Sim p=0.05 可用”“§8.17 N=1 可用”（后两者已撤回/移除，见 RESEARCH_RULES）。
- 新增引用须补作者+年份+一句话+URL 四要素，否则按“暂缓引用”处理。
