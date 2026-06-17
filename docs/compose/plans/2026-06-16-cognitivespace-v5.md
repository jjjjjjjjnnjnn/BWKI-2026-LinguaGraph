# CognitiveSpace v5.0 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 验证 MCL（Missing Cognitive Links）能准确发现学习者的认知断裂，并以跨语言场景作为验证案例，用 3D Knowledge City 直观展示。

**Architecture:** LLM 作为可插拔组件（本地优先），核心算法是 MCL 检测（确定性），LCD 作为 MCL 的跨语言应用案例，3D Knowledge City 用 3d-force-graph 实时渲染。

**Tech Stack:** Python 3.12, NetworkX, 3d-force-graph (JS), LM Studio (本地 LLM), Flask (可选)

---

## 项目定位（最终版）

| 层级 | 内容 |
|------|------|
| **研究项目名** | CognitiveSpace |
| **产品/Demo 名** | LinguaGraph |
| **核心贡献 1** | MCL Detection — 缺失认知连接检测 |
| **核心贡献 2** | Cognitive Graph Estimation — 用 LLM 估计认知图谱 |
| **展示方式** | 3D Knowledge City — 认知空间可视化 |
| **验证场景** | 跨语言对比（LCD 作为 MCL 的应用，不是独立贡献） |

## BWKI 7 项评分目标

| 标准 | 目标 | 关键证据 |
|------|------|---------|
| 1. 独立完成度 | 8/10 | 代码有测试，文档清晰 |
| 2. 原创性 | 9/10 | MCL 是新概念，LCD 是新指标 |
| 3. 难度 | 7/10 | 跨语言映射 + 图算法 |
| 4. 科学方法 | 8/10 | Gold Dataset + Precision/Recall/F1 |
| 5. 洞见 | 8/10 | MCL 能解释"为什么学不会" |
| 6. 实际价值 | 8/10 | 教育诊断应用明确 |
| 7. 代码可读性 | 7/10 | 有测试，模块清晰 |

---

## 文件结构

```
BWKI-2026-备战/02-项目规划/
├── config/
│   ├── config.yaml                    # MODIFY: 本地优先
│   ├── prompts/
│   │   ├── extract.md                 # EXISTING
│   │   └── explain.md                 # EXISTING
│   ├── expert_graphs/
│   │   ├── calculus.json              # EXISTING
│   │   └── social_issues.json         # CREATE: 社会议题专家图
│   └── normalization_map.json         # CREATE: 概念归一化
├── src/
│   ├── __init__.py                    # EXISTING
│   ├── models.py                      # EXISTING
│   ├── extract.py                     # MODIFY: 支持 LM Studio
│   ├── graph.py                       # EXISTING
│   ├── compare.py                     # EXISTING (MCL 核心)
│   ├── cross_language.py              # EXISTING (LCD 应用)
│   ├── explain.py                     # EXISTING
│   └── main.py                        # MODIFY: 本地模式
├── data/
│   ├── gold/
│   │   └── gold_dataset.json          # MODIFY: 扩展到 30 条
│   ├── students/
│   │   └── student_001.json           # EXISTING (mock)
│   ├── questionnaires/
│   │   ├── questionnaire_zh.json      # EXISTING
│   │   ├── questionnaire_de.json      # EXISTING
│   │   └── questionnaire_en.json      # EXISTING
│   └── concept_mapping.json           # CREATE: 跨语言概念映射
├── tests/
│   ├── test_extract.py                # CREATE
│   ├── test_compare.py                # CREATE
│   ├── test_cross_language.py         # CREATE
│   └── test_integration.py            # CREATE
├── web/
│   ├── index.html                     # MODIFY: 改名 CognitiveSpace
│   ├── server.py                      # MODIFY: 连接真实 pipeline
│   └── static/
│       └── graph-data.json            # CREATE: 3D 渲染数据
├── output/                            # 运行时生成
├── docs/
│   ├── mcl_definition.md              # EXISTING
│   ├── cognitivespace-v5-design.md    # CREATE: 本文件
│   └── validation-report.md           # CREATE: 验证报告
└── requirements.txt                   # CREATE
```

---

## 原则：Evidence First

> **Every claim must have evidence.**

| 声称 | 证据 |
|------|------|
| LLM 能提取概念 | Sprint 0: Concept Precision/Recall |
| MCL 有效 | Sprint 2: 与教师标注一致性 (F1) |
| LCD 有意义 | Sprint 3: Graph Edit Distance 实验 |
| 3D 有帮助 | Sprint 4: Demo + 用户反馈 |

## 数学定义

### MCL (Missing Cognitive Links)

```
MCL = E_expert \ E_learner

其中：
- E_expert = 专家知识图谱边集合
- E_learner = 学习者估计图谱边集合
- \ = 集合差

MCL Score = |MCL| / |E_expert| × 100%
```

加权版本（考虑边的重要性）：

```
Weighted MCL = Σ w_i × (1 - c_i)

其中：
- w_i = 边 i 的重要性权重
- c_i = LLM 对该边的置信度
```

### LCD (Language Cognitive Drift)

```
LCD = GED(G_L1, G_L2) / max(|E_L1|, |E_L2|)

其中：
- GED = Graph Edit Distance（图编辑距离）
- G_L1 = 语言 1 下的认知图谱
- G_L2 = 语言 2 下的认知图谱
- |E| = 边数
```

LCD ∈ [0, 1]：
- 0 = 两种语言下认知结构完全相同
- 1 = 完全不同

---

## Sprint 0：Extraction Validation（6/16-6/17）

> **验证 LLM 提取是否可靠。如果这一关过不了，后面所有验证都会失真。**

### Task 0.1: 设计 10 条标准测试输入

**Files:**
- Create: `data/extraction_test.json`

- [ ] **Step 1: 创建测试数据**

```json
[
  {
    "id": "ext_001",
    "language": "zh",
    "input": "我知道导数表示变化率，但不知道为什么需要极限。",
    "human_labels": {
      "concepts": ["导数", "变化率", "极限"],
      "relations": [
        {"from": "导数", "to": "变化率", "type": "represents", "confidence": 1.0}
      ]
    }
  },
  {
    "id": "ext_002",
    "language": "zh",
    "input": "积分是导数的逆运算，可以用来计算面积。",
    "human_labels": {
      "concepts": ["积分", "导数", "面积"],
      "relations": [
        {"from": "积分", "to": "导数", "type": "inverse_of", "confidence": 1.0},
        {"from": "积分", "to": "面积", "type": "represents", "confidence": 1.0}
      ]
    }
  },
  {
    "id": "ext_003",
    "language": "de",
    "input": "Ableitung ist die Änderungsrate einer Funktion an einem Punkt.",
    "human_labels": {
      "concepts": ["Ableitung", "Änderungsrate", "Funktion"],
      "relations": [
        {"from": "Ableitung", "to": "Änderungsrate", "type": "represents", "confidence": 1.0},
        {"from": "Ableitung", "to": "Funktion", "type": "is_part_of", "confidence": 1.0}
      ]
    }
  },
  {
    "id": "ext_004",
    "language": "de",
    "input": "Integral ist das Gegenteil von Ableitung und kann Flächen berechnen.",
    "human_labels": {
      "concepts": ["Integral", "Ableitung", "Fläche"],
      "relations": [
        {"from": "Integral", "to": "Ableitung", "type": "inverse_of", "confidence": 1.0},
        {"from": "Integral", "to": "Fläche", "type": "represents", "confidence": 1.0}
      ]
    }
  },
  {
    "id": "ext_005",
    "language": "en",
    "input": "The derivative represents the rate of change of a function.",
    "human_labels": {
      "concepts": ["derivative", "rate of change", "function"],
      "relations": [
        {"from": "derivative", "to": "rate of change", "type": "represents", "confidence": 1.0},
        {"from": "derivative", "to": "function", "type": "is_part_of", "confidence": 1.0}
      ]
    }
  },
  {
    "id": "ext_006",
    "language": "en",
    "input": "Integration is the reverse of differentiation and calculates area under curves.",
    "human_labels": {
      "concepts": ["integration", "differentiation", "area"],
      "relations": [
        {"from": "integration", "to": "differentiation", "type": "inverse_of", "confidence": 1.0},
        {"from": "integration", "to": "area", "type": "represents", "confidence": 1.0}
      ]
    }
  },
  {
    "id": "ext_007",
    "language": "zh",
    "input": "极限是微积分的基础，导数定义需要用到极限。",
    "human_labels": {
      "concepts": ["极限", "微积分", "导数"],
      "relations": [
        {"from": "导数", "to": "极限", "type": "requires", "confidence": 1.0},
        {"from": "极限", "to": "微积分", "type": "is_part_of", "confidence": 1.0}
      ]
    }
  },
  {
    "id": "ext_008",
    "language": "de",
    "input": "Grenzwerte sind die Grundlage der Analysis. Die Definition der Ableitung benötigt Grenzwerte.",
    "human_labels": {
      "concepts": ["Grenzwert", "Analysis", "Ableitung"],
      "relations": [
        {"from": "Ableitung", "to": "Grenzwert", "type": "requires", "confidence": 1.0},
        {"from": "Grenzwert", "to": "Analysis", "type": "is_part_of", "confidence": 1.0}
      ]
    }
  },
  {
    "id": "ext_009",
    "language": "en",
    "input": "Limits are the foundation of calculus. The definition of derivative requires limits.",
    "human_labels": {
      "concepts": ["limits", "calculus", "derivative"],
      "relations": [
        {"from": "derivative", "to": "limits", "type": "requires", "confidence": 1.0},
        {"from": "limits", "to": "calculus", "type": "is_part_of", "confidence": 1.0}
      ]
    }
  },
  {
    "id": "ext_010",
    "language": "zh",
    "input": "函数的导数就是斜率，积分就是求面积。 chain rule 用于复合函数。",
    "human_labels": {
      "concepts": ["导数", "斜率", "积分", "面积", "chain rule", "复合函数"],
      "relations": [
        {"from": "导数", "to": "斜率", "type": "represents", "confidence": 1.0},
        {"from": "积分", "to": "面积", "type": "represents", "confidence": 1.0},
        {"from": "chain rule", "to": "复合函数", "type": "is_part_of", "confidence": 1.0}
      ]
    }
  }
]
```

---

### Task 0.2: 写 Extraction 测试脚本

**Files:**
- Create: `tests/test_extraction_validation.py`

- [ ] **Step 1: 写验证脚本**

```python
"""Validate LLM extraction accuracy against human labels."""
import json
from pathlib import Path
from src.extract import extract_concepts

DATA_DIR = Path(__file__).parent.parent / "data"
TEST_FILE = DATA_DIR / "extraction_test.json"


def load_test_data():
    with open(TEST_FILE, encoding="utf-8") as f:
        return json.load(f)


def evaluate_extraction():
    """Evaluate extraction accuracy on 10 test samples."""
    test_data = load_test_data()
    
    concept_tp = 0
    concept_fp = 0
    concept_fn = 0
    relation_tp = 0
    relation_fp = 0
    relation_fn = 0
    json_errors = 0
    total = len(test_data)
    
    for sample in test_data:
        try:
            result = extract_concepts(
                sample["input"],
                language=sample["language"],
                use_mock=False  # 使用真实 LLM
            )
        except Exception as e:
            json_errors += 1
            print(f"[ERROR] {sample['id']}: {e}")
            continue
        
        # 概念对比
        extracted_concepts = set(result["concepts"])
        human_concepts = set(sample["human_labels"]["concepts"])
        
        concept_tp += len(extracted_concepts & human_concepts)
        concept_fp += len(extracted_concepts - human_concepts)
        concept_fn += len(human_concepts - extracted_concepts)
        
        # 关系对比（简化：只比较 source-target 对）
        extracted_relations = {(r["source"], r["target"]) for r in result["relations"]}
        human_relations = {(r["from"], r["to"]) for r in sample["human_labels"]["relations"]}
        
        relation_tp += len(extracted_relations & human_relations)
        relation_fp += len(extracted_relations - human_relations)
        relation_fn += len(human_relations - extracted_relations)
    
    # 计算指标
    concept_precision = concept_tp / max(concept_tp + concept_fp, 1)
    concept_recall = concept_tp / max(concept_tp + concept_fn, 1)
    concept_f1 = 2 * concept_precision * concept_recall / max(concept_precision + concept_recall, 1e-6)
    
    relation_precision = relation_tp / max(relation_tp + relation_fp, 1)
    relation_recall = relation_tp / max(relation_tp + relation_fn, 1)
    relation_f1 = 2 * relation_precision * relation_recall / max(relation_precision + relation_recall, 1e-6)
    
    json_success_rate = (total - json_errors) / total
    
    print("=" * 50)
    print("Extraction Validation Results")
    print("=" * 50)
    print(f"Samples: {total}")
    print(f"JSON Success Rate: {json_success_rate:.0%}")
    print()
    print("Concept Extraction:")
    print(f"  Precision: {concept_precision:.2%}")
    print(f"  Recall:    {concept_recall:.2%}")
    print(f"  F1:        {concept_f1:.2%}")
    print()
    print("Relation Extraction:")
    print(f"  Precision: {relation_precision:.2%}")
    print(f"  Recall:    {relation_recall:.2%}")
    print(f"  F1:        {relation_f1:.2%}")
    print("=" * 50)
    
    # 通过标准
    passed = (
        json_success_rate >= 0.9 and
        concept_f1 >= 0.5 and
        relation_f1 >= 0.4
    )
    
    if passed:
        print("[PASS] Extraction is reliable enough for MCL validation.")
    else:
        print("[FAIL] Extraction needs improvement before proceeding.")
    
    return {
        "json_success_rate": json_success_rate,
        "concept_f1": concept_f1,
        "relation_f1": relation_f1,
        "passed": passed
    }


if __name__ == "__main__":
    evaluate_extraction()
```

- [ ] **Step 2: 运行验证**

```bash
cd "C:\Users\rongj\Desktop\学校\BWKI-2026-备战\02-项目规划"
python -m tests.test_extraction_validation
```

Expected: 输出 Precision/Recall/F1，以及是否通过

---

### Task 0.3: 分析失败案例

- [ ] **Step 1: 记录失败模式**

| 失败类型 | 示例 | 解决方案 |
|---------|------|---------|
| 概念遗漏 | 未提取"极限" | 调整 prompt |
| 概念多余 | 提取了"计算" | 添加过滤规则 |
| 关系错误 | "积分→面积"标为 "is_part_of" | 明确关系类型定义 |
| JSON 格式错误 | 响应不是合法 JSON | 重试机制 |

- [ ] **Step 2: 如果通过率 < 80%，调整 prompt**

修改 `config/prompts/extract.md`，增加：
- 更明确的概念定义
- 关系类型枚举
- 输出格式示例

---

## Sprint 1：连接 LLM + 最小 3D Demo（6/18-6/22）

### Task 1.1: 更新 config.yaml 为本地优先

**Files:**
- Modify: `config/config.yaml`

- [ ] **Step 1: 修改 LLM 配置**

```yaml
# === LLM Configuration ===
llm:
  # Provider: local (LM Studio) or openai
  provider: local

  # 本地模型设置 (LM Studio)
  local:
    base_url: http://127.0.0.1:1234/v1
    model: qwen3-8b  # 或你加载的模型名

  # OpenAI 备用
  openai:
    api_key: ${OPENAI_API_KEY}
    model: gpt-4.1-mini
```

- [ ] **Step 2: 测试配置加载**

```bash
cd "C:\Users\rongj\Desktop\学校\BWKI-2026-备战\02-项目规划"
python -c "import yaml; c=yaml.safe_load(open('config/config.yaml')); print(c['llm']['provider'])"
```

Expected: `local`

---

### Task 1.2: 修改 extract.py 支持 LM Studio

**Files:**
- Modify: `src/extract.py:31-107`

- [ ] **Step 1: 添加 config 加载和本地模式**

在 `extract_concepts` 函数开头添加 config 加载逻辑：

```python
def extract_concepts(
    student_answer: str,
    language: str = "zh",
    model: str = None,
    api_key: str = None,
    base_url: str = None,
    use_mock: bool = False
) -> dict:
    """
    Extract concepts and relations from student answer using LLM.
    """
    # 加载 config
    import yaml
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)
    else:
        config = {}

    llm_config = config.get("llm", {})
    provider = llm_config.get("provider", "local")

    # Mock 模式
    if use_mock:
        return _mock_extract(student_answer, language)

    # 本地模式 (LM Studio)
    if provider == "local":
        local_config = llm_config.get("local", {})
        base_url = base_url or local_config.get("base_url", "http://127.0.0.1:1234/v1")
        model = model or local_config.get("model", "qwen3-8b")
        api_key = "not-needed"  # LM Studio 不需要 API key
    else:
        # OpenAI 模式
        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return _mock_extract(student_answer, language)
        model = model or llm_config.get("openai", {}).get("model", "gpt-4.1-mini")
        base_url = base_url or llm_config.get("openai", {}).get("base_url")

    from openai import OpenAI

    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url

    client = OpenAI(**client_kwargs)

    # ... 后续代码不变 ...
```

- [ ] **Step 2: 测试本地连接**

确保 LM Studio 运行，然后：

```bash
cd "C:\Users\rongj\Desktop\学校\BWKI-2026-备战\02-项目规划"
python -c "
from src.extract import extract_concepts
result = extract_concepts('导数是变化率的极限', language='zh')
print('Concepts:', result['concepts'])
print('Model:', result['model'])
"
```

Expected: 返回真实 LLM 提取的概念列表，model 显示为实际模型名。

---

### Task 1.3: 测试 LLM 提取准确性

**Files:**
- Create: `tests/test_extract.py`

- [ ] **Step 1: 写测试用例**

```python
"""Tests for LLM concept extraction."""
import pytest
from src.extract import extract_concepts, normalize_concepts


class TestNormalizeConcepts:
    """测试概念归一化"""

    def test_chinese_synonyms(self):
        """同义词应该被归一化"""
        concepts = ["微分", "求导", "导数"]
        result = normalize_concepts(concepts)
        # 至少应该减少重复
        assert len(result) <= len(concepts)

    def test_empty_input(self):
        """空输入应该返回空列表"""
        result = normalize_concepts([])
        assert result == []


class TestExtractConcepts:
    """测试 LLM 概念提取"""

    def test_mock_mode(self):
        """Mock 模式应该返回预定义结果"""
        result = extract_concepts("导数是变化率", language="zh", use_mock=True)
        assert "concepts" in result
        assert "relations" in result
        assert result["model"] == "mock"

    def test_chinese_input(self):
        """中文输入应该提取中文概念"""
        result = extract_concepts(
            "导数表示函数的变化率，积分是导数的逆运算",
            language="zh",
            use_mock=True
        )
        assert len(result["concepts"]) > 0

    def test_german_input(self):
        """德语输入应该提取德语概念"""
        result = extract_concepts(
            "Ableitung ist die Änderungsrate einer Funktion",
            language="de",
            use_mock=True
        )
        assert len(result["concepts"]) > 0

    def test_english_input(self):
        """英语输入应该提取英语概念"""
        result = extract_concepts(
            "Derivative represents the rate of change",
            language="en",
            use_mock=True
        )
        assert len(result["concepts"]) > 0

    def test_result_structure(self):
        """返回结果应该包含必要字段"""
        result = extract_concepts("test", use_mock=True)
        assert "concepts" in result
        assert "relations" in result
        assert "raw_response" in result
        assert "language" in result
        assert "model" in result
```

- [ ] **Step 2: 运行测试**

```bash
cd "C:\Users\rongj\Desktop\学校\BWKI-2026-备战\02-项目规划"
python -m pytest tests/test_extract.py -v
```

Expected: All tests PASS

---

### Task 1.4: 构建最小 3D Knowledge City

**Files:**
- Create: `web/graph-data.json`
- Modify: `web/index.html` (修改渲染逻辑)

- [ ] **Step 1: 创建 graph-data.json**

```json
{
  "nodes": [
    {"id": "导数", "label": "导数", "group": "expert", "size": 8},
    {"id": "变化率", "label": "变化率", "group": "expert", "size": 6},
    {"id": "极限", "label": "极限", "group": "expert", "size": 6},
    {"id": "函数", "label": "函数", "group": "expert", "size": 6},
    {"id": "积分", "label": "积分", "group": "expert", "size": 6}
  ],
  "links": [
    {"source": "导数", "target": "变化率", "type": "represents"},
    {"source": "导数", "target": "极限", "type": "requires"},
    {"source": "积分", "target": "导数", "type": "inverse_of"},
    {"source": "导数", "target": "函数", "type": "is_part_of"}
  ],
  "missing_links": [
    {"source": "极限", "target": "导数", "type": "prerequisite", "severity": "high"}
  ]
}
```

- [ ] **Step 2: 修改 index.html 的 3D 渲染**

找到 3d-force-graph 初始化代码，确保它能读取 graph-data.json：

```javascript
// 3D Knowledge City 渲染
const Graph = ForceGraph3D()(document.getElementById('3d-graph'))
  .graphData(graphData)
  .nodeLabel('label')
  .nodeColor(node => {
    if (node.group === 'expert') return '#4a7dff';
    if (node.group === 'student') return '#ff6b6b';
    return '#888';
  })
  .linkDirectionalArrowLength(6)
  .linkDirectionalArrowRelPos(1)
  .linkColor(link => {
    if (link.type === 'prerequisite') return '#ff4444';
    return '#666';
  });
```

- [ ] **Step 3: 测试 3D 渲染**

在浏览器中打开 `web/index.html`，应该看到：
- 5 个蓝色节点（专家图谱）
- 4 条连线
- 1 条红色虚线（缺失连接）

---

### Task 1.5: 端到端测试

- [ ] **Step 1: 运行完整 pipeline**

```bash
cd "C:\Users\rongj\Desktop\学校\BWKI-2026-备战\02-项目规划"
python -m src.main --input "导数是变化率的极限" --language zh
```

Expected: 输出包含 concepts, relations, missing_links

- [ ] **Step 2: 验证 3D 输出**

检查 `output/` 目录生成了 graph-data.json

---

## Sprint 2：MCL 验证（6/23-6/29）

### Task 2.1: 设计标注协议

**Files:**
- Create: `docs/annotation-protocol.md`

- [ ] **Step 1: 编写标注规范**

```markdown
# 标注协议 v1.0

## 标注任务

给定一段学生回答和一个问题，标注：

1. **概念列表**：学生提到了哪些概念？
2. **关系列表**：概念之间有什么关系？
3. **缺失连接**：哪些专家认为重要的连接学生没有提到？

## 概念标注规则

- 概念用中文命名（德语/英语回答也标注中文）
- 概念应该是领域术语，不是普通词汇
- 示例："导数"是概念，"计算"不是概念

## 关系标注规则

关系类型：
- `prerequisite`: A 是 B 的前提（必须先学 A 才能学 B）
- `is_part_of`: A 是 B 的一部分
- `represents`: A 代表 B
- `inverse_of`: A 是 B 的逆运算
- `relates_to`: A 与 B 相关（弱关系）

## 缺失连接标注

- 只标注"专家认为重要但学生没有提到"的连接
- 不标注"学生提到但不准确"的内容
- 每个缺失连接需要说明理由
```

---

### Task 2.2: 标注 30 条 Gold Dataset

**Files:**
- Modify: `data/gold/gold_dataset.json`

- [ ] **Step 1: 准备标注材料**

从 questionnaires 中选取 10 个问题，每个问题收集 3 个不同水平的回答（强/中/弱），共 30 条。

- [ ] **Step 2: 标注（你和伙伴分工）**

每条数据标注：
```json
{
  "sample_id": "zh_001",
  "language": "zh",
  "question": "什么是导数？",
  "text": "...",
  "human_labels": {
    "concepts": ["导数", "变化率", "极限", "函数"],
    "relations": [
      {"from": "导数", "to": "变化率", "type": "represents"},
      {"from": "导数", "to": "极限", "type": "requires"}
    ],
    "missing_hints": [
      {"from": "积分", "to": "导数", "reason": "学生未提到积分与导数的关系"}
    ]
  },
  "annotator": "annotator_1",
  "difficulty": "medium"
}
```

- [ ] **Step 3: 一致性检查**

两人各标注 10 条，比较一致率。目标：Cohen's Kappa > 0.7

---

### Task 2.3: 运行 MCL 检测

**Files:**
- Create: `tests/test_compare.py`

- [ ] **Step 1: 写 MCL 测试**

```python
"""Tests for MCL detection."""
import pytest
import networkx as nx
from src.compare import detect_missing_links, calculate_graph_similarity


class TestDetectMissingLinks:
    """测试缺失连接检测"""

    def test_identical_graphs(self):
        """相同图应该没有缺失连接"""
        g1 = nx.DiGraph()
        g1.add_edges_from([("A", "B"), ("B", "C")])
        g2 = nx.DiGraph()
        g2.add_edges_from([("A", "B"), ("B", "C")])
        
        missing = detect_missing_links(g1, g2)
        assert len(missing) == 0

    def test_missing_concept(self):
        """缺少概念应该被检测到"""
        expert = nx.DiGraph()
        expert.add_edges_from([("A", "B"), ("B", "C"), ("C", "D")])
        student = nx.DiGraph()
        student.add_edges_from([("A", "B")])
        
        missing = detect_missing_links(student, expert)
        # 应该检测到缺少 C, D 以及 B->C, C->D
        assert len(missing) > 0

    def test_missing_relation(self):
        """缺少关系应该被检测到"""
        expert = nx.DiGraph()
        expert.add_edges_from([("A", "B"), ("A", "C")])
        student = nx.DiGraph()
        student.add_edges_from([("A", "B")])
        
        missing = detect_missing_links(student, expert)
        # 应该检测到缺少 A->C
        assert any(m["type"] == "missing_relation" for m in missing)

    def test_severity_levels(self):
        """缺失连接应该有严重程度分级"""
        expert = nx.DiGraph()
        expert.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")])
        student = nx.DiGraph()
        student.add_edges_from([("A", "B")])
        
        missing = detect_missing_links(student, expert)
        severities = [m["severity"] for m in missing]
        assert "high" in severities or "medium" in severities


class TestGraphSimilarity:
    """测试图相似度计算"""

    def test_identical_graphs(self):
        """相同图相似度应为 1.0"""
        g1 = nx.DiGraph()
        g1.add_edges_from([("A", "B")])
        g2 = nx.DiGraph()
        g2.add_edges_from([("A", "B")])
        
        sim = calculate_graph_similarity(g1, g2)
        assert sim == 1.0

    def test_empty_graphs(self):
        """空图相似度应为 1.0（无差异）"""
        g1 = nx.DiGraph()
        g2 = nx.DiGraph()
        
        sim = calculate_graph_similarity(g1, g2)
        assert sim == 1.0
```

- [ ] **Step 2: 运行测试**

```bash
python -m pytest tests/test_compare.py -v
```

Expected: All tests PASS

---

### Task 2.4: 计算 MCL vs 教师标注的一致率

**Files:**
- Create: `tests/test_validation.py`

- [ ] **Step 1: 写验证脚本**

```python
"""Validate MCL detection against teacher annotations."""
import json
from pathlib import Path
from src.extract import extract_concepts
from src.graph import build_graph
from src.compare import detect_missing_links

DATA_DIR = Path(__file__).parent.parent / "data"
GOLD_FILE = DATA_DIR / "gold" / "gold_dataset.json"
EXPERT_DIR = DATA_DIR.parent / "config" / "expert_graphs"


def load_gold_dataset():
    """加载 Gold Dataset"""
    with open(GOLD_FILE, encoding="utf-8") as f:
        return json.load(f)


def evaluate_mcl():
    """评估 MCL 检测准确率"""
    gold = load_gold_dataset()
    
    tp = 0  # True Positive: 系统检测到 & 教师标注了
    fp = 0  # False Positive: 系统检测到 & 教师没标注
    fn = 0  # False Negative: 系统没检测到 & 教师标注了
    
    for sample in gold:
        # 1. LLM 提取
        result = extract_concepts(sample["text"], language=sample["language"], use_mock=True)
        student_graph = build_graph(result)
        
        # 2. 加载专家图
        expert_graph = load_expert_graph(sample["language"])
        
        # 3. MCL 检测
        detected = detect_missing_links(student_graph, expert_graph)
        detected_set = {(m.get("source"), m.get("target")) for m in detected}
        
        # 4. 教师标注
        human_set = {(h["from"], h["to"]) for h in sample["human_labels"].get("missing_hints", [])}
        
        # 5. 计算
        tp += len(detected_set & human_set)
        fp += len(detected_set - human_set)
        fn += len(human_set - detected_set)
    
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-6)
    
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    print(f"F1: {f1:.2%}")
    print(f"Samples: {len(gold)}")
    
    return {"precision": precision, "recall": recall, "f1": f1}


if __name__ == "__main__":
    evaluate_mcl()
```

- [ ] **Step 2: 运行验证**

```bash
python -m tests.test_validation
```

Expected: 输出 Precision, Recall, F1 分数

---

### Task 2.5: 写验证报告

**Files:**
- Create: `docs/validation-report.md`

- [ ] **Step 1: 报告模板**

```markdown
# MCL 验证报告

## 实验设置

- Gold Dataset: 30 条标注样本
- LLM: Qwen3-8b (本地)
- 标注者: 2 人
- Cohen's Kappa: X.XX

## 结果

| 指标 | 值 |
|------|-----|
| Precision | XX% |
| Recall | XX% |
| F1 | XX% |

## 分析

### 成功案例
- ...

### 失败案例
- ...

## 结论

MCL 检测与教师标注的一致率达到 [X]%，证明系统能够有效发现学习者的认知断裂。
```

---

## Sprint 3：LCD 作为验证案例（6/30-7/6）

### Task 3.1: 收集 15+ 学生三语数据

**目标：** 每个学生用中/德/英三种语言回答 4 个问题

**问卷问题（社会议题）：**
1. 什么是公平？
2. 什么是成功？
3. 什么是自由？
4. 什么是责任？

**收集方式：** 在线问卷（Google Forms / Typeform）

---

### Task 3.2: 运行 MCL 检测

- [ ] **Step 1: 批量处理**

```python
# 对每个学生的每种语言运行 MCL
for student in students:
    for lang in ["zh", "de", "en"]:
        graph = extract_and_build(student.answers[lang])
        mcl = detect_missing_links(graph, expert_graph)
        save_result(student.id, lang, mcl)
```

---

### Task 3.3: 计算 LCD 指标

- [ ] **Step 1: LCD 计算逻辑**

```python
def calculate_lcd(graph_l1, graph_l2, concept_mapping):
    """
    LCD = 1 - Graph_Similarity(graph_l1, graph_l2)
    
    其中 graph_l1 和 graph_l2 是同一学生在不同语言下的认知图谱
    concept_mapping 是跨语言概念映射
    """
    # 将 L1 概念映射到 L2
    mapped_l1 = apply_mapping(graph_l1, concept_mapping)
    
    # 计算图相似度
    similarity = calculate_graph_similarity(mapped_l1, graph_l2)
    
    # LCD = 1 - similarity
    lcd = 1 - similarity
    
    return lcd
```

- [ ] **Step 2: 批量计算**

```python
lcd_scores = []
for student in students:
    for lang_pair in [("zh", "de"), ("zh", "en"), ("de", "en")]:
        g1 = load_graph(student, lang_pair[0])
        g2 = load_graph(student, lang_pair[1])
        lcd = calculate_lcd(g1, g2, concept_mapping)
        lcd_scores.append({
            "student": student.id,
            "pair": lang_pair,
            "lcd": lcd
        })
```

---

### Task 3.4: 分析漂移模式

- [ ] **Step 1: 统计分析**

```python
import statistics

# 平均 LCD
avg_lcd = statistics.mean([s["lcd"] for s in lcd_scores])

# 按语言对分组
by_pair = {}
for s in lcd_scores:
    pair = s["pair"]
    by_pair.setdefault(pair, []).append(s["lcd"])

# 输出
for pair, scores in by_pair.items():
    print(f"{pair[0]}→{pair[1]}: avg LCD = {statistics.mean(scores):.2%}")
```

---

### Task 3.5: 可视化双城对比

- [ ] **Step 1: 创建 Dual City 页面**

在 `web/index.html` 中添加双面板视图：
- 左面板：中文认知图谱
- 右面板：德语认知图谱
- 中间：LCD 分数和差异高亮

---

## Sprint 4：Demo + BWKI 提交（7/7-7/13）

### Task 4.1: 打磨 3D Knowledge City

- [ ] 添加 Building Height（概念重要性）
- [ ] 添加 Missing Bridge（缺失连接可视化）
- [ ] 添加动画效果

### Task 4.2: 录制 Demo 视频

- [ ] 30 秒快速演示
- [ ] 3-5 分钟完整 Pitch

### Task 4.3: 写 BWKI 创意大纲

```markdown
# CognitiveSpace: Estimating Learner Cognitive Graphs with LLMs

## 研究问题
如何用 AI 发现学习者"哪里没学会"？

## 方法
1. 用 LLM 从学生回答中提取概念和关系
2. 构建认知图谱
3. 与专家图谱对比，检测缺失连接 (MCL)
4. 跨语言对比，量化认知漂移 (LCD)

## 创新点
1. MCL: 新概念，定义"认知断裂"
2. LCD: 新指标，量化语言对认知的影响
3. 3D Knowledge City: 直观展示认知空间

## 验证
- Gold Dataset: 30 条标注样本
- MCL vs 教师标注: Precision/Recall/F1
- LCD 跨语言验证: 15+ 学生三语数据
```

### Task 4.4: 最终代码清理

- [ ] 添加 docstrings
- [ ] 运行所有测试
- [ ] 更新 README

---

## 成功标准

### Sprint 1 完成标准
- [ ] extract.py 能连接 LM Studio
- [ ] 最小 3D Demo 能显示 5 个节点
- [ ] 所有测试通过

### Sprint 2 完成标准
- [ ] 30 条 Gold Dataset 标注完成
- [ ] MCL Precision > 60%
- [ ] MCL Recall > 50%
- [ ] 验证报告完成

### Sprint 3 完成标准
- [ ] 15+ 学生三语数据收集完成
- [ ] LCD 分数可计算
- [ ] 跨语言漂移模式可观察

### Sprint 4 完成标准
- [ ] Demo 可运行
- [ ] BWKI 创意大纲提交
- [ ] 3-5 分钟视频完成
