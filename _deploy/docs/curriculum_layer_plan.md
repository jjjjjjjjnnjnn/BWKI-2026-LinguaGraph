# LinguaGraph — Curriculum Layer Integration Plan

> 将 Kernlehrplan 作为"课程标准层"加入 LinguaGraph
> 目标：比较教材 → 课程标准的知识结构对齐程度

---

## 1. 核心理念

当前系统：
```
教材 → 概念图谱 → LDS/CDS/HDS
```

新增层：
```
课程标准 → 概念图谱 → Coverage Score
                              ↓
教材     → 概念图谱 → Curriculum-LDS
```

三个新问题可以回答：

| 问题 | 指标 | 价值 |
|------|------|------|
| 教材覆盖了课程标准的多少概念？ | **Coverage Score** | 教育质量评估 |
| 教材结构与课程标准的结构差异多大？ | **Curriculum-LDS** | 课程设计质量 |
| 不同教育体系的课程标准结构差异多大？ | **Curriculum LDS** | 跨体系比较 |

---

## 2. 数据源

### 德国：NRW Kernlehrplan Mathematik

| 学段 | 版本 | 下载链接 | 大小 |
|------|------|---------|------|
| Sek I (5-10) | 2019 | [PDF](https://lehrplannavigator.nrw.de/system/files/media/document/file/g9_m_klp_3401_2019_06_23_0.pdf) | 293 KB |
| Sek II (11-13) | 2023 | [PDF](https://lehrplannavigator.nrw.de/system/files/media/document/file/gost_klp_m_2023_06_07.pdf) | ~300 KB |

### 中国：义务教育数学课程标准 + 高中数学课程标准

| 学段 | 来源 | 查找方式 |
|------|------|---------|
| 1-9 年级 | 教育部《义务教育数学课程标准（2022）》 | 搜索 "义务教育数学课程标准 2022 PDF" |
| 10-12 年级 | 教育部《普通高中数学课程标准（2017修订）》 | 搜索 "普通高中数学课程标准 2017 PDF" |

### 英国/国际：National Curriculum + Common Core

| 来源 | 学段 | 查找方式 |
|------|------|---------|
| England National Curriculum | KS1-5 (5-18岁) | `gov.uk/national-curriculum` |
| US Common Core State Standards | K-12 | `corestandards.org/Math` |

> **初期建议**：先只做 NRW Kernlehrplan（一个 PDF），验证管线通不通。通了之后再加中国/英国课标。

---

## 3. 操作步骤

### Step 1: 下载 Kernlehrplan PDF

```bash
# 从 Sek I (5-10年级)
curl -o data/curricula/nrw_seki_mathematik_2019.pdf \
  "https://lehrplannavigator.nrw.de/system/files/media/document/file/g9_m_klp_3401_2019_06_23_0.pdf"

# 从 Sek II (11-13年级)
curl -o data/curricula/nrw_sekii_mathematik_2023.pdf \
  "https://lehrplannavigator.nrw.de/system/files/media/document/file/gost_klp_m_2023_06_07.pdf"
```

### Step 2: 解析 PDF → 结构化概念

Kernlehrplan 的结构通常如下：

```
Inhaltsfeld (内容领域)
  └── Schwerpunkt (重点)
       └── Kompetenz (能力目标)
            └── Konkretisierung (具体化)
```

你需要写一个解析脚本 `scripts/parse_curriculum.py`：

```python
# 策略 A：直接文本提取（快速，但需要清理 OCR/PDF 噪声）
import PyPDF2  # 或 pdfplumber

# 策略 B：将 PDF 文本分段后，用 LLM 提取概念和关系
# （复用 src/extract.py 的 Prompt）
```

**输出格式**（与现有 expert_graph 格式统一）：
```json
{
  "version": "2.0",
  "domain": "curriculum_nrw_math",
  "languages": ["de"],
  "concepts": [
    {
      "name": "curriculum_nrw_arith_natuerliche_zahlen",
      "display_name": "Natürliche Zahlen",
      "level": "middle",
      "labels": {"de": "Natürliche Zahlen", "zh": "自然数", "en": "Natural Numbers"},
      "source": "Kernlehrplan Mathematik NRW 2019",
      "inhaltsfeld": "Arithmetik/Algebra"
    }
  ],
  "relations": [
    {"source": "...", "target": "...", "type": "prerequisite"}
  ]
}
```

### Step 3: 概念对齐（Curriculum ↔ Textbook）

已有的教材概念和新的课程标准概念之间需要对齐。

对齐策略：
```
教材概念 "Natürliche Zahlen"
    ↔
课程标准概念 "Natürliche Zahlen"
    ↔
中文概念 "自然数"
```

复用 `config/concept_mapping.json` 中已有的跨语言映射，新增 `curriculum` 命名空间。

### Step 4: 计算新指标

**Coverage Score**：
```
Coverage(L) = |教材概念_L ∩ 课标概念_L| / |课标概念_L|
```

**Curriculum-LDS**（重用现有 LDS 公式）：
```
Curriculum-LDS(教材, 课标) = 1 - mean(GED_sim, Jaccard_node, Jaccard_edge)
```
将教材图谱和课程标准图谱分别作为 LDS 的两个输入。

### Step 5: 生成对比图

```
Figure 7: Curriculum Coverage by Level
  X 轴: Elementary → Middle → High → College
  Y 轴: Coverage Score
  解读: 哪个学段的教材最贴近课程标准？

Figure 8: Curriculum-LDS by Level
  X 轴: Elementary → Middle → High → College
  Y 轴: Curriculum-LDS
  解读: 教材结构在哪个学段偏离课程标准最多？
```

---

## 4. 项目结构更新

```
data/curricula/                           ← 新课标目录
├── nrw_seki_mathematik_2019.pdf          ← 下载的 Kernlehrplan
├── nrw_sekii_mathematik_2023.pdf
├── curriculum_nrw_math.json              ← 解析后的概念图谱
└── alignment_textbook_curriculum.json    ← 教材↔课标对齐映射

scripts/
├── parse_curriculum.py                   ← 新课标解析脚本
└── generate_paper_figures.py             ← 更新：增加 Fig 7/8

config/
├── expert_graphs/
│   ├── math_full.json                    ← 已有：教材图谱
│   └── curriculum_nrw_math.json          ← 新增：课标图谱
└── concept_mapping.json                  ← 更新：加入课标命名空间

docs/
├── cognitive_metrics_framework.md        ← 更新：加入 Coverage Score
└── handoff_multi_subject.md
```

---

## 5. 时间估计

| 步骤 | 内容 | 工期 |
|------|------|------|
| Step 1 | 下载 2 份 Kernlehrplan PDFs | 30 分钟 |
| Step 2 | 解析 PDF → 结构化概念图谱（50-80 概念） | 1-2 天 |
| Step 3 | 概念对齐（Curriculum ↔ Textbook） | 1 天 |
| Step 4 | Coverage Score 实现 + 计算 | 0.5 天 |
| Step 5 | Curriculum-LDS 计算 + 对比图 | 1 天 |
| **总计** | **首次跑通** | **~4 天** |

---

## 6. 已知风险

| 风险 | 概率 | 缓解 |
|------|------|------|
| PDF 解析困难（表格/页眉干扰） | 中 | 先用 pdfplumber 提取纯文本；复杂部分手动整理 |
| 课标概念粒度 vs 教材概念粒度不匹配 | 中 | 课标概念更抽象（"数感"），教材更具体（"自然数加法"），需要多对一映射 |
| 中国课标（中文）不在手边 | 低 | 可以从教育部官网下载 |

---

## 7. 启动命令（给下个 AI 会话）

按顺序执行：

```bash
# 1. 进入项目
cd C:/Users/rongj/Desktop/学校/BWKI-2026-备战

# 2. 读取项目上下文和本计划
cat docs/handoff_multi_subject.md
cat docs/curriculum_layer_plan.md

# 3. 下载 Kernlehrplan
mkdir -p data/curricula
curl -o data/curricula/nrw_seki_mathematik_2019.pdf \
  "https://lehrplannavigator.nrw.de/system/files/media/document/file/g9_m_klp_3401_2019_06_23_0.pdf"
curl -o data/curricula/nrw_sekii_mathematik_2023.pdf \
  "https://lehrplannavigator.nrw.de/system/files/media/document/file/gost_klp_m_2023_06_07.pdf"

# 4. 阅读现有图谱格式
cat config/expert_graphs/math_full.json | head -80

# 5. 开始 Step 2：写 parse_curriculum.py
```
