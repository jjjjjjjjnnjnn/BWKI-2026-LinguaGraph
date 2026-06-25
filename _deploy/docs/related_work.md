# LinguaGraph — 相关工作定位报告

> **版本**: v1.0 | 2026-06-17
> **目的**: 将外部开源项目定位为 LinguaGraph 的引用、基线和验证层，而非替换核心 Pipeline
> **原则**: 先引用 → 再验证 → 最后集成

---

## 1. Related Work Matrix

| 系统 | 多语言 | 概念图 | 关系分类 | 人类实验 | 跨语言比较 | LDS |
|------|:------:|:------:|:--------:|:--------:|:----------:|:---:|
| **ConceptNet5** | ✅ 50+ | ✅ 21M 节点 | ✅ 30+ 类型 | ❌ | ⚠️ 词汇级 | ❌ |
| **CoCo-Ex** | ⚠️ 单一 | ❌ 提取 | ❌ | ✅ 人工标注 | ❌ | ❌ |
| **Concordia** | ✅ | ⚠️ Agent 记忆 | ❌ | ❌ | ❌ | ❌ |
| **LinguaGraph** | ✅ ZH/DE/EN | ✅ 个体认知图 | ✅ 6 类型 | ✅ 计划 60人 | ✅ 图结构级 | ✅ 首创 |

### 关键发现

**To the best of our knowledge, LinguaGraph is the first system to simultaneously combine**:
1. 多语言概念图比较 (ZH/DE/EN)
2. 人类实验验证 (n=60 设计)
3. 图结构级跨语言比较指标 (LDS)
4. 个体级认知分析（非群体级）

We are not aware of existing systems that combine these four dimensions in a single framework.

---

## 2. 项目定位详述

### 2.1 ConceptNet5

**角色**: 关系分类法参考 + 评估基线

| 维度 | ConceptNet5 | LinguaGraph |
|------|-------------|-------------|
| 数据来源 | 众包 + 游戏 | LLM 提取 + 人工标注 |
| 节点粒度 | 词汇/短语 | 认知概念 |
| 图类型 | 静态知识库 | 个体动态认知图 |
| 比较维度 | — | 跨语言图结构 (LDS) |

**可引用部分**:
- 关系分类法: `IsA`, `PartOf`, `Causes`, `UsedFor`, `CapableOf`
- 评估基准: MEN, RW, SimLex 数据集
- 多语言对齐方法: 跨语言概念映射策略

**论文引用价值**: ✅ Must-cite — 常识知识图谱领域的鼻祖

**集成路线** (Phase 2):
```
ConceptNet relation taxonomy
    ↓
LinguaGraph 关系类型扩展
    ↓
src/graph.py + config/relation_types.json
    ↓
评估: LLM 提取 vs ConceptNet 关系的 F1
```

---

### 2.2 CoCo-Ex (Heidelberg-NLP)

**角色**: 概念提取基线 (Baseline A)

| 维度 | CoCo-Ex | LinguaGraph |
|------|---------|-------------|
| 方法 | 传统 NLP (Constituency Parse + Embedding) | LLM (GPT-4.1-mini / Qwen3) |
| 目标 | 提取概念 → 映射 ConceptNet | 提取概念+关系 → 构建个体认知图 |
| 语言 | 英语 | 中文 + 德语 + 英语 |
| 评估 | 人工标注 F1 | 人工标注 F1 |
| 输出 | 概念列表 | 概念 + 关系 + 图谱 |

**作为 Baseline 的价值**:
```
提取器              F1 (预期)
─────────────────────────────
Keyword 匹配        0.30-0.40
CoCo-Ex             0.50-0.65   ← 传统 NLP 基线
LLM (GPT-4.1-mini)  0.70-0.85   ← LinguaGraph 当前
LLM + CoCo-Ex 融合   0.75-0.90   ← 未来方向
```

**论文引用价值**: ✅ Should-cite — 概念提取方法论参考

**集成路线** (Phase 2):
```
CoCo-Ex 提取管道
    ↓
封装为 LinguaGraph Provider (extractors/coco_ex.py)
    ↓
在 evaluate_pipeline.py 中加入对比
    ↓
报告: "Comparison of LLM vs Traditional Concept Extraction"
```

---

### 2.3 Concordia (Google DeepMind)

**角色**: 未来扩展方向 (Phase 3)

| 维度 | Concordia | LinguaGraph |
|------|-----------|-------------|
| 核心 | 多 Agent 社会模拟 | 跨语言认知比较 |
| Agent | 生成式 Agent (记忆+个性) | 语言社区认知表征 |
| 比较 | Agent vs Agent 行为 | 语言 vs 语言 图结构 |
| 可视化 | 2D 小镇 | 3D Cognitive City |

**当前状态**: ❌ Phase 3 之前不动

**未来应用场景** (BWKI 后):
```
LinguaGraph 2.0:
  ┌─────────────────────────────┐
  │ Chinese Agent City          │ → 中文认知图
  │  (Agent 讨论"自由/成功/责任") │
  ├─────────────────────────────┤
  │ German Agent City           │ → 德语认知图
  │  (Agent diskutiert Freiheit) │
  ├─────────────────────────────┤
  │ English Agent City          │ → 英语认知图
  │  (Agent discusses freedom)  │
  ├─────────────────────────────┤
  │ Human Participant Data      │ → 真实认知图
  └─────────────────────────────┘
        ↓
  Human LDS vs Agent LDS 比较
        ↓
  研究问题: "LLM 是否模拟了人类跨语言认知差异？"
```

**论文引用价值**: ❌ NOT for BWKI — 未来 Phase

---

## 3. 外部项目使用策略

```
当前 (BWKI 提交):
  ConceptNet → 论文引用关系分类法
  CoCo-Ex    → 论文引用为 Baseline 对比
  Concordia  → 仅在 Future Work 中提及

Phase 2 (BWKI 后):
  ConceptNet → 关系类型扩展
  CoCo-Ex    → 封装为第二个 Provider
  Concordia  → 研究性原型

Phase 3 (论文扩展):
  Concordia  → 多语言 Agent 城市模拟
  CoCo-Ex    → LLM + 传统 NLP 混合提取
```

### 不变原则

- ❌ 不修改 LDS 定义
- ❌ 不替换问卷结构
- ❌ 不重构核心 Pipeline
- ✅ 只作为引用、基线、未来方向
- ✅ 保留完整版权和许可证声明

---

## 4. 论文/答辩定位

### LinguaGraph 的独特价值

在论文 Related Work 中可以写：

> To the best of our knowledge, no existing system combines:
1. LLM-based concept extraction from individual responses
2. Individual-level cognitive graph construction
3. Cross-lingual graph comparison using structure metrics (LDS)
4. 3D Cognitive City visualization

Existing work typically covers only one or two of these dimensions.

### 未来对比方向

```
LinguaGraph
  vs ConceptNet (静态知识库)
  vs CoCo-Ex (传统 NLP 提取)
  vs Concordia (Agent 模拟)
  = 唯一能回答"语言是否改变认知结构"的系统
```

---

## 5. 许可证声明

```
external/CoCo-Ex/           MIT License        — Copyright Heidelberg-NLP
external/conceptnet5/       Apache 2.0         — Copyright Commonsense Computing
external/concordia/         Apache 2.0         — Copyright Google DeepMind
```

所有项目保留原始许可证和版权声明。LinguaGraph 使用这些项目作为研究引用和方法论参考。
详细许可证见各子目录的 LICENSE / NOTICE 文件。
