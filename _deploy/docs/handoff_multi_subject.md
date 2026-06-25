# LinguaGraph — Multi-Subject Expansion Handoff

> 本文件用于向新的 AI 会话交接：多学科验证（Physics/Biology）的完整任务、上下文和执行步骤。
> 
> 场景：你的电脑上运行另一个 Claude Code 会话，加载此文件后直接开始工作。

---

## 1. 项目背景（30 秒速览）

**LinguaGraph** 是一个 BWKI 2026 研究项目，核心研究问题是：

> **不同语言教材中的知识组织方式是否存在可量化的结构差异？**

当前进展：

| 维度 | 当前状态 |
|------|---------|
| 学科 | 仅数学（68 本教材，574 概念，3538 关系） |
| 语言 | ZH / EN / DE（三语平行） |
| 指标 | LDS / CDS / HDS（已冻结 v1.0） |
| 图表 | Fig3 CDS by Level, Fig4 LDS Heatmap, Fig5 HDS Distribution |
| 发现 | F1-F5（见下文） |
| 代码库 | `github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph` |

---

## 2. 核心发现（当前数学教材）

这些已经验证的发现是你的起点：

| # | 发现 | 证据 |
|---|------|------|
| F1 | **CDS 在初中达到峰值**（0.271），非单调递减 | 三语独立验证通过 |
| F2 | 初中→高中 **3.7× 骤降**（概念数 4.2× 增长） | CDS 0.271→0.073 |
| F3 | **HDS ≤ 7**，均值 0.40，66% 概念零先修链 | 数学是网状结构 |
| F4 | **ZH–DE 结构差异最大**（LDS=0.907） | ZH–EN 最小（0.802） |
| F5 | 跨语言差异因主题而异（同语言对内变幅 ~0.2） | topic-dependent |

---

## 3. 你要做的事情

**核心任务**：将 LinguaGraph Pipeline 扩展到第二个学科（Physics 优先），验证：

1. **CDS 峰值**在 Physics 中出现在哪个学段？
2. **HDS 分布**在不同学科中是否不同？
3. **LDS 模式**在 Physics 中是否与 Math 一致？

**为什么是 Physics？**

> 如果 Math 的 CDS 峰值在初中，而 Physics 的 CDS 峰值在高中，这就构成了一个**跨学科发现**——不同学科的知识成长模式不同。这个发现比单纯增加数据量更有研究价值。

---

## 4. 怎么做（详细步骤）

### Step 1: 了解现有管线

```bash
# 项目根目录
cd /path/to/BWKI-2026-LinguaGraph

# 先理解现有的提取管线
less src/extract.py        # 概念提取（MIMO prompt + 规则回退）
less src/graph.py          # 知识图谱构建
less src/scoring.py        # LDS/CDS/HDS 计算
less scripts/generate_paper_figures.py  # 图表生成器
less workbench/process.py  # 文本→分析→3D 的规则提取器

# 看数据格式
less config/expert_graphs/math_full.json  # 参考：完整数学图谱格式
```

### Step 2: 寻找物理教材（ZH/EN/DE）

你需要为每个语言找到 **2-3 本覆盖全学段的物理教材**。

**中文物理教材**：
- 人教版初中物理（八年级、九年级）
- 人教版高中物理（必修 1-3，选修系列）
- 大学物理（如《普通物理学》《力学》《电磁学》）

**英文物理教材**：
- AP Physics 1 & 2（代数基础）
- AP Physics C（微积分基础）
- Halliday Resnick Walker *Fundamentals of Physics*
- Khan Academy Physics

**德语物理教材**：
- Duden Physik（5-10 年级）
- Gymnasium Physik（Oberstufe）
- Tipler *Physik*（大学）
- University Physics German edition

教材以 **章节文本** 格式存储，每个文件 ≈ 一节。
参考现有格式：`data/textbook/zh_人教版高中数学选修2-2_ch1_sec1.1.txt`

### Step 3: 生成物理图谱

有两种策略可选：

**策略 A：用 workbench/process.py 的规则提取器**
```python
# process.py 包含 200+ 数学术语的字典
# 对于物理，你需要增加物理术语字典
```

**策略 B：直接构建专家图谱 JSON**
参考 `config/expert_graphs/` 中的格式，手动或半自动构建物理概念网络。

推荐从策略 B 开始——先构建一个 50-100 概念的物理核心图谱，验证管线通不通。

参考 `config/expert_graphs/math_full.json` 格式：
```json
{
  "version": "2.0",
  "domain": "physics",
  "languages": ["zh", "en", "de"],
  "concepts": [
    {
      "name": "physics_mechanics_force",
      "display_name": "力",
      "category": "concept",
      "level": "middle",
      "labels": {
        "zh": "力",
        "en": "Force",
        "de": "Kraft"
      },
      "source_references": [
        {"textbook": "...", "language": "zh", "chapter": "...", "section": "..."}
      ]
    }
  ],
  "relations": [
    {
      "source": "physics_mechanics_力",
      "target": "physics_mechanics_加速度",
      "type": "prerequisite",
      "relation": "prerequisite"
    }
  ],
  "metadata": {
    "total_concepts": 0,
    "total_relations": 0,
    "created": ""
  }
}
```

### Step 4: 将物理图谱导入 CognitiveSpace

编辑 `cognitive-space/web/data.js`，将物理概念和关系追加到 `COGNITIVE_DATA_EXT`。

需添加：
- `level` 字段（elementary / middle / high / college）
- `labels` 字段（zh / en / de 翻译）
- `group` 字段设为 `"physics"`（用于区分数学和物理）

### Step 5: 计算指标

```bash
# 用 generate_paper_figures.py 扩展版
# 你需要：
# 1. 修改 load_cognitive_data() 使其能按 group 过滤
# 2. 修改 compute_cds() 使其能按 subject + level 分组
# 3. 新增对比图的生成函数

python scripts/generate_paper_figures.py --fig 6  # 新增：学科对比
```

### Step 6: 生成学科对比图

关键图表示例：
```
Figure 6: CDS Comparison — Math vs Physics
  X 轴: Education Level (Elementary → College)
  Y 轴: CDS
  两组柱: Math / Physics

预期发现假设：
  如果 Math 的 CDS 峰值在初中，
  而 Physics 的 CDS 峰值在高中，
  这就是一个跨学科发现。
```

---

## 5. 指标定义（已冻结，禁止修改）

### CDS（概念密度分）
```
CDS(G) = 2|E| / (|V| × (|V|-1))
```
### HDS（层级深度分）
```
HDS(G) = max_{v∈V} depth(v)
```
### LDS（语言漂移分）
```
LDS(A,B) = 1 - mean(GED_sim, Jaccard_node, Jaccard_edge)
```
详见 `docs/cognitive_metrics_framework.md`

---

## 6. 现有文件结构（关键路径）

```
cognitive-space/web/data.js          # 全部 574 概念 + 3538 关系数据
config/expert_graphs/math_full.json  # 数学完整图谱（197 concepts, 195 rels）
src/extract.py                        # LLM + 规则概念提取
src/graph.py                          # 图谱构建 + NetworkX
src/scoring.py                        # LDS/CDS/HDS 计算
scripts/generate_paper_figures.py     # 论文图表生成器
workbench/process.py                  # 文本→分析的规则管线（200+ 术语字典）
docs/cognitive_metrics_framework.md   # 指标定义（v1.0 FREEZE）
docs/paper/03_results_text.md         # 已有发现文档
outputs/figures/                      # 已生成的图表
data/textbook/                        # 现有教材文本
```

---

## 7. 工作节奏建议

| 阶段 | 内容 | 预计时间 |
|------|------|---------|
| Step 1-2 | 理解管线 + 收集物理教材 | 2-3 天 |
| Step 3 | 构建物理概念图谱（50-100 概念） | 2-3 天 |
| Step 4 | 导入 CognitiveSpace | 0.5 天 |
| Step 5 | 计算指标 + 校验 | 1 天 |
| Step 6 | 生成对比图 + 文档 | 1 天 |
| 总计 | Physics 完整一轮 | ~7-10 天 |

尽量**避免**：
- 收集过多教材（每种语言 2-3 本已经足够）
- 构建超过 200 概念的物理图谱（第一轮 50-100 概念就够）
- 训练任何模型
- 更改 LDS/CDS/HDS 定义

---

## 8. 交接检查清单

启动新会话时，请先确认以下信息：

- [ ] 项目路径正确
- [ ] 已读 `cognitive-space/web/data.js` 的数据格式
- [ ] 已读 `config/expert_graphs/math_full.json` 的数据格式
- [ ] 已读 `docs/cognitive_metrics_framework.md`
- [ ] 已读 `scripts/generate_paper_figures.py`
- [ ] 已读 `docs/paper/03_results_text.md`
- [ ] 三语物理教材已下载到 `data/textbook/`
- [ ] 第一个物理概念 JSON 已开始构建
