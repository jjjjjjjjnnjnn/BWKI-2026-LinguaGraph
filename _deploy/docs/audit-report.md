# LinguaGraph 全流程审查报告

**审查时间:** 2026-06-17
**审查范围:** 全部代码 + BWKI 竞赛对齐 + 可视化就绪度
**审查文件:** 7 个核心文件

---

## 一、总览评分

| 维度 | 得分 | 说明 |
|------|------|------|
| **代码质量** | 6/10 | 核心算法正确，但有重复代码和硬编码 |
| **架构设计** | 7/10 | Pipeline 清晰，模块分离合理 |
| **研究对齐** | 5/10 | 概念提取未接真实 LLM，数据为硬编码 |
| **可视化** | 7/10 | Cognitive City 设计好，但数据为 demo |
| **竞赛就绪** | 4/10 | 缺少真实数据、真实 LLM、完整实验 |
| **总体** | **5.8/10** | 框架完成，内容为空壳 |

---

## 二、逐文件审查

### 2.1 `src/compare.py` (165行)

**Bug / 问题:**

| # | 行号 | 问题 | 严重度 |
|---|------|------|--------|
| 1 | 31-34 | `nx.graph_edit_distance` 对大图（>10节点）极慢，无超时保护 | 中 |
| 2 | 36 | `edit_cost is None` 时设为 `max_nodes`，但 `max_cost` 包含边数，归一化不准 | 低 |
| 3 | 57-58 | `min(a,b), max(a,b)` 假设节点名可比较，中文/德文混合排序可能异常 | 低 |
| 4 | 83-92 | `cosine_similarity_embeddings` 已实现但未被调用（compare_graphs 未使用嵌入） | 中 |
| 5 | 102 | LDS 计算 `1 - mean(GED, Jaccard, EdgeJaccard)` — 当 GED=1.0, Jaccard=0 时 LDS=0.67，但这不代表"语言漂移" | **高** |

**关键发现:** LDS 的数学含义需要重新审视。当前 LDS = 1 - mean(GED, Jaccard, EdgeJaccard)，但 GED 归一化方向反了（高 GED = 高相似度），导致 LDS 在示例数据上输出 0.667 而非预期的低值。

**修复建议:**
- GED 归一化应为 `edit_cost / max_cost`（不是 `1 - edit_cost/max_cost`）
- 或重新定义 LDS 为 `1 - node_jaccard`（更直观）

---

### 2.2 `src/cross_language.py` (229行)

**Bug / 问题:**

| # | 行号 | 问题 | 严重度 |
|---|------|------|--------|
| 1 | 10-28 | `CORE_83_CONCEPTS` 有重复项：justice 出现2次, freedom 出现2次, truth 出现2次, beauty 出现2次 | 中 |
| 2 | 61 | `translations` dict 中 `"freedom"` 重复定义（行34和行61），后者覆盖前者（值相同但浪费） | 低 |
| 3 | 70-82 | `conceptual_similarity` 只做字符串匹配，不做语义匹配（"自由" vs "liberty" 无法匹配） | 中 |
| 4 | 176 | `consistency` 计算除以 `max(avg_pos.values())`，若最大值为0则除零 | 中 |
| 5 | 186 | `from compare import build_graph, compare_graphs` — 相对导入在 `__main__` 中可工作，但作为模块导入会失败 | **高** |

**关键发现:** `compute_lds_from_concepts` 中的 `from compare import ...` 是相对导入，当从 `pipeline.py` 或 `server.py` 导入时会 `ModuleNotFoundError`。

---

### 2.3 `src/extract_v2.py` (243行)

**Bug / 问题:**

| # | 行号 | 问题 | 严重度 |
|---|------|------|--------|
| 1 | 14 | `LM_MODEL` 硬编码为 `qwen3.5-9b-uncensored-hauhaucs-aggressive`，其他人运行会失败 | 中 |
| 2 | 105 | `<think>` 标签清理只匹配 ````，不匹配 ````（闭合标签） | 低 |
| 3 | 125 | `json.loads` 处理 LLM 输出时，若 LLM 输出 ```json 代码块会失败 | 中 |
| 4 | 140-173 | `fallback_extract` 的关键词表硬编码，覆盖面有限 | 中 |
| 5 | 187-189 | 后备提取的关系全是 `co_occurs`，无语义区分 | 中 |

**关键发现:** 提取模块在 fallback 模式下只能做关键词匹配，无法提取真正的语义关系。LLM 模式依赖本地 LM Studio 运行。

---

### 2.4 `web/server.py` (221行)

**Bug / 问题:**

| # | 行号 | 问题 | 严重度 |
|---|------|------|--------|
| 1 | 10-12 | `from compare import ...` — 当从 `web/` 目录运行时，`sys.path` 指向 `src/`，但如果 `src/` 有 `__init__.py` 可能冲突 | 低 |
| 2 | 20-62 | `DISTRICT_MAP` 和 `CONCEPT_IMPORTANCE` 硬编码了三语概念映射（200+行），维护成本高 | 中 |
| 3 | 75-103 | `build_city_data` 每次请求都重建图，无缓存 | 低 |
| 4 | 142-169 | `build_default_city` 的边是固定的，不随问题变化 | **高** |
| 5 | 221 | `debug=True` 在生产环境不安全 | 低 |

**关键发现:** 问题输入框（`btn-ask`）点击后只是刷新默认数据，没有真正根据问题生成新城市。这是最大的功能缺口。

---

### 2.5 `web/index.html` (432行)

**Bug / 问题:**

| # | 行号 | 问题 | 严重度 |
|---|------|------|--------|
| 1 | 199 | `const T3 = window.THREE;` — 若 3d-force-graph 加载失败，T3 为 undefined | 中 |
| 2 | 200-231 | `createBuilding` 无错误处理，T3 缺失时整页崩溃 | 中 |
| 3 | 311 | demo 数据中 `source:'自我', target:'身份'` 但 `身份` 未在 zhNodes 中定义 | **高** |
| 4 | 363-373 | `lang-tab` 事件监听器无问题，但 `filterByLang` 调用 `Graph.graphData()` 可能触发重建（性能问题） | 低 |
| 5 | 394-398 | `btn-ask` 只更新标题文字，不触发新数据加载 | **高** |

**关键发现:** `generateDemoData()` 中引用了 `身份` 节点但未定义（行311 `target:'身份'`），会导致链接指向不存在的节点。

---

### 2.6 `pipeline.py` (103行)

**Bug / 问题:**

| # | 行号 | 问题 | 严重度 |
|---|------|------|--------|
| 1 | 67-87 | `build_default_graph` 与 `web/server.py` 的 `build_default_city` 重复定义 | 中 |
| 2 | 25-38 | 无 `try/except` 保护，任一步失败整个 pipeline 崩溃 | 低 |

**发现:** pipeline 只是 demo 运行器，不连接真实数据。

---

### 2.7 `data/gold/gold_dataset.json`

**问题:** 只有 7 条样本，不足以验证提取质量。BWKI 提交需要 ≥20 条。

---

## 三、BWKI 竞赛对齐审查

### 3.1 评分维度评估

| BWKI 维度 | 权重 | 当前得分 | 差距 |
|-----------|------|---------|------|
| **创新性** | ⭐⭐⭐⭐⭐ | 5/10 | LDS 定义需修正；Cognitive City 设计好但未展示真实数据 |
| **技术实现** | ⭐⭐⭐⭐ | 4/10 | 概念提取未接真实 LLM；可视化用 demo 数据；pipeline 未端到端 |
| **研究方法** | ⭐⭐⭐⭐ | 3/10 | 无真实被试数据；无统计检验；无对照组 |
| **展示效果** | ⭐⭐⭐ | 7/10 | Cognitive City 设计优秀；LDS 面板直观 |
| **社会影响** | ⭐⭐⭐ | 5/10 | 跨语言教育应用有潜力，但未论证 |

### 3.2 Top 5 关键差距

| # | 差距 | 影响 | 修复难度 |
|---|------|------|---------|
| 1 | **无真实被试数据** | 无法证明任何假设 | 中（需招募15人） |
| 2 | **LDS 数学定义有误** | 核心指标不可信 | 低（修正归一化） |
| 3 | **概念提取未接真实 LLM** | pipeline 是空壳 | 低（接 LM Studio） |
| 4 | **可视化用硬编码数据** | Demo 不代表真实结果 | 中（需接 pipeline 输出） |
| 5 | **问题输入不触发新数据** | 交互是假的 | 中（需实现 /api/generate） |

---

## 四、JavaScript 错误清单

浏览器控制台会报以下错误/警告：

| # | 错误 | 原因 | 修复 |
|---|------|------|------|
| 1 | `THREE.MeshPhongMaterial` 可能警告 | 3d-force-graph 内部已加载 Three.js | 可忽略 |
| 2 | `身份` 节点不存在 | demo 数据引用未定义节点 | 删除该链接或添加节点 |
| 3 | `filterByLang` 后 stats 可能不准 | `updateStats` 只更新计数，不更新 LDS | 添加 LDS 更新 |

---

## 五、修复优先级

### P0 — 立即修复（影响演示）

1. **修正 LDS 计算** — `compare.py` 行 102，GED 归一化方向反了
2. **修复 demo 数据** — `index.html` 行 311，`身份` 节点未定义
3. **接真实 LLM** — `extract_v2.py` 接 LM Studio，跑一次真实提取
4. **接 pipeline 输出** — `server.py` 读取 `data/output/graph_*.json` 而非硬编码

### P1 — 本周完成

5. **实现 /api/generate** — 根据问题动态生成城市数据
6. **补充 Gold Dataset** — 扩展到 20+ 条
7. **修正 CORE_83_CONCEPTS** — 去重
8. **修正 cross_language.py 导入** — 改为绝对导入

### P2 — 竞赛提交前

9. **招募 15 名学生** — 三语问卷
10. **运行完整 pipeline** — 真实数据 → 真实 LDS
11. **撰写论文** — 方法论 + 结果 + 创新点
12. **录制 Demo 视频** — 3D 城市动画

---

## 六、总结

**现状:** 框架完整，内容空壳。代码结构清晰，Cognitive City 设计优秀，但所有数据都是硬编码 demo，没有真实研究支撑。

**关键风险:**
- LDS 数学定义可能有误（需验证）
- 无真实数据 = 无研究结论
- 6/28 截止日仅剩 11 天

**建议:** 先修 P0 的 4 个 bug，再集中精力招募学生收集真实数据。没有真实数据，再好的可视化也只是 demo。
