# LinguaGraph — 数据扩展任务书

> **目标**：大规模增加采样样本，覆盖更多学科/课标/语言，使研究发现具有统计显著性
> 
> 在下个 AI 会话中执行。加载本文件后直接开始工作。

---

## 1. 项目状态（30 秒速览）

| 维度 | 当前数据量 | 扩展目标 |
|------|-----------|---------|
| 数学教材图谱 | 574 concepts, 3538 relations | ✅ 已冻结（足以支撑分析） |
| **物理教材图谱** | **87 concepts, 104 relations** | **⬆️ 需扩展至 200+** |
| **NRW 课标图谱** | **41 concepts, 147 relations** | **⬆️ 需完成（Sek I + Sek II）** |
| 中国课标 | ❌ 不存在 | **需新建（～100 concepts）** |
| 生物教材 | ❌ 不存在 | 第三学科候选 |
| LDS 数据 | 15 条 (Wikipedia 5 topics × 3 pairs) | 需补充更多语料对 |

---

## 2. 优先任务排序

### P0：物理图谱扩展（87 → 200+ concepts）

物理图谱当前只有 87 个概念。为了与数学（574 concepts）做有意义的对比，物理应该扩展到至少 200 概念。

**操作步骤**：

```bash
# 1. 打开物理图谱
cat config/expert_graphs/physics_full.json
```

**需要补充的内容**：

| 缺失领域 | 当前状态 | 目标状态 |
|---------|---------|---------|
| 力学 | 已有（力、加速度、牛顿定律） | 补充：动量、冲量、角动量、简谐振动 |
| 热学 | 已有少量 | 补充：温度、内能、熵、热机 |
| 电磁学 | 已有少量 | 补充：电场、电势、高斯定理、安培定律、法拉第定律 |
| 光学 | 缺失 | 新建：反射、折射、干涉、衍射、偏振 |
| 近代物理 | 缺失 | 新建：量子论基础、原子模型、核物理基础 |
| 实验方法 | 缺失 | 新建：测量、误差、数据分析 |

**格式参考**（必须保持与 math_full.json 完全一致）：
```json
{
  "name": "physics_thermo_entropy",
  "display_name": "熵",
  "level": "high",
  "labels": {"zh": "熵", "en": "Entropy", "de": "Entropie"},
  "source_references": [
    {"textbook": "人教版高中物理选择性必修3", "language": "zh", "chapter": "热力学定律", "section": "熵"}
  ]
}
```

**关系补充**（每新增一个概念，至少添加 1-2 条关系）：
```json
{
  "source": "physics_thermo_entropy",
  "target": "physics_thermo_热力学第二定律",
  "type": "prerequisite",
  "relation": "prerequisite"
}
```

**验证**：
```bash
python scripts/physics_pipeline.py   # 重新计算 CDS/HDS
python scripts/generate_paper_figures.py --fig 6  # 重新生成对比图
```

---

### P1：NRW 课程标准图谱完成（41 → 150+ concepts）

**下载链接**：
```bash
# Sek I (5-10 年级) - 核心课程
curl -o data/curricula/nrw_seki_mathematik_2019.pdf \
  "https://lehrplannavigator.nrw.de/system/files/media/document/file/g9_m_klp_3401_2019_06_23_0.pdf"

# Sek II (11-13 年级) - 高级课程
curl -o data/curricula/nrw_sekii_mathematik_2023.pdf \
  "https://lehrplannavigator.nrw.de/system/files/media/document/file/gost_klp_m_2023_06_07.pdf"
```

**操作步骤**：

```bash
# 1. 先看当前的课标图谱
cat config/expert_graphs/curriculum_nrw_math.json | head -80

# 2. 了解 parse_curriculum.py
cat scripts/parse_curriculum.py

# 3. 运行解析脚本扩展
python scripts/parse_curriculum.py --sek1 data/curricula/nrw_seki_mathematik_2019.pdf
python scripts/parse_curriculum.py --sek2 data/curricula/nrw_sekii_mathematik_2023.pdf

# 4. 验证
python -c "
import json
with open('config/expert_graphs/curriculum_nrw_math.json') as f:
    data = json.load(f)
lvls = {}
for c in data['concepts']:
    l = c.get('level','?')
    lvls[l] = lvls.get(l,0)+1
print('By level:', lvls)
print('Total:', len(data['concepts']))
"
```

**Kernlehrplan 的结构**（典型内容领域）：

| 内容领域 (Inhaltsfeld) | 学段 | 概念数（估计） |
|----------------------|------|-------------|
| Arithmetik/Algebra | 5-10 | 25-30 |
| Funktionen | 5-10 | 15-20 |
| Geometrie | 5-10 | 20-25 |
| Stochastik | 5-10 | 10-15 |
| Analysis (Sek II) | 11-13 | 20-25 |
| Analytische Geometrie (Sek II) | 11-13 | 15-20 |
| Stochastik (Sek II) | 11-13 | 10-15 |

**策略**：如果 PDF 解析困难，可以直接在 JSON 中手动补全概念。41 个基础概念已存在，需扩展至覆盖上述全部内容领域。

---

### P2：中国课程标准导入

**来源**：教育部《义务教育数学课程标准（2022）》+《普通高中数学课程标准（2017修订）》

**搜索方式**：
```bash
# 用 curl 从教育部网站获取，或用搜索找到 PDF
# 文件名通常为 "义务教育数学课程标准2022.pdf"
```

**输出格式**：与 `curriculum_nrw_math.json` 完全一致，但 `labels` 需包含：
```json
{
  "domain": "curriculum_cn_math",
  "languages": ["zh", "en"],
  "concepts": [
    {
      "name": "curriculum_cn_arith_natural_number",
      "display_name": "自然数",
      "level": "elementary",
      "labels": {"zh": "自然数", "en": "Natural Numbers"},
      "source": "义务教育数学课程标准 2022"
    }
  ]
}
```

**提示**：中国课标的结构与德国不同。中国的写法是：
```
数与代数 → 图形与几何 → 统计与概率 → 综合与实践
```
每个领域下分学段（1-3 年级、4-6 年级、7-9 年级、高中）。

---

### P3：中等优先级 — 生物教材图谱

**只在 P0/P1 完成后才开始**。

目标：50-100 概念，覆盖初中到大学生物学，验证第三学科的 CDS/HDS 模式。

参考框架：
```
生物学
├── 分子与细胞（高中/大学）
├── 遗传与进化（高中/大学）
├── 稳态与环境（高中/大学）
├── 生物技术（高中/大学）
└── 人体生理（初中）
```

---

## 3. 数据格式标准（必须严格遵守）

### 概念格式

```json
{
  "name": "domain_subdomain_concept_id",    // 唯一 ID，全小写 + 下划线
  "display_name": "显示名",                  // 简短名称
  "category": "concept",                    // 固定为 "concept"
  "level": "middle",                        // elementary | middle | high | college
  "labels": {                               // 三语/双语标签
    "zh": "中文名",
    "en": "English Name",
    "de": "Deutscher Name"                  // 如果无德语翻译可省略
  },
  "source_references": [                    // 至少一个来源引用
    {
      "textbook": "教材名称",
      "language": "zh",
      "chapter": "章节名",
      "section": "节名"
    }
  ]
}
```

### 关系格式

```json
{
  "source": "physics_thermo_entropy",       // 必须匹配概念的 name
  "target": "physics_thermo_热力学第二定律", // 必须匹配概念的 name
  "type": "prerequisite",                   // 推荐：prerequisite | requires | part_of | generalization | specialization | representation | applies_to | analogy
  "relation": "prerequisite"                // 与 type 一致
}
```

---

## 4. 绝对禁止

- ❌ **不要修改** `src/extract.py`、`src/scoring.py`、`src/graph.py`
- ❌ **不要修改** LDS/CDS/HDS 定义（已冻结 v1.0）
- ❌ **不要训练任何模型**
- ❌ **不要同时扩 3 个以上方向**
- ❌ **不要删除现有数据**（math_full.json、已有物理数据）

---

## 5. 验证流程

每次增补数据后运行：

```bash
# 1. 物理管线
python scripts/physics_pipeline.py

# 2. 论文图
python scripts/generate_paper_figures.py --fig 6

# 3. 统计
python -c "
import json
# 检查所有 expert_graph
from pathlib import Path
import os, sys
for f in sorted(Path('config/expert_graphs').glob('*.json')):
    with open(f) as fh:
        data = json.load(fh)
    concepts = data.get('concepts', []) if isinstance(data, dict) else []
    relations = data.get('relations', []) if isinstance(data, dict) else []
    lvls = {}
    for c in concepts:
        l = c.get('level','?')
        lvls[l] = lvls.get(l,0)+1
    print(f'{f.stem:35s}: {len(concepts):4d} concepts, {len(relations):4d} relations | levels: {lvls}')
"
```

---

## 6. 第一次会话的启动命令

```bash
# 1. 进入项目
cd C:/Users/rongj/Desktop/学校/BWKI-2026-备战

# 2. 阅读核心上下文
cat docs/handoff_multi_subject.md           # 项目全貌
cat docs/data_expansion_task.md              # 本任务书（当前文件）

# 3. 阅读已有的数据格式
cat config/expert_graphs/math_full.json | head -100
cat config/expert_graphs/physics_full.json | head -100
cat config/expert_graphs/curriculum_nrw_math.json

# 4. 开始 P0
# 编辑 config/expert_graphs/physics_full.json
```

---

## 7. 估计工期

| 任务 | 工作量 | 并行度 |
|------|--------|--------|
| P0：物理 87→200+ | 2-3 天 | 可独立 |
| P1：课标 41→150+ | 2-3 天 | 可与 P0 并行 |
| P2：中国课标 | 1-2 天 | 需找到 PDF |
| P3：生物 | 2-3 天 | P0/P1 之后 |
