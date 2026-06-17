# External Projects — LinguaGraph 融合集成

> **创建日期**: 2026-06-17
> **目的**: 将现有开源项目集成至 LinguaGraph，增强概念提取、知识图谱和未来 Agent 模拟能力
> **原则**: 不重构核心 Pipeline，不修改 LDS，不替换问卷

---

## 目录

| 项目 | 兼容度 | License | 集成模块 | 状态 |
|------|--------|---------|----------|------|
| [CoCo-Ex](#1-coco-ex) | 5/5 | Apache 2.0 | 概念提取 | ✅ 已克隆 |
| [ConceptNet5](#2-conceptnet5) | 4/5 | Apache 2.0 | 关系分类法、评估基准 | ✅ 已克隆 |
| [Concordia](#3-concordia) | 4/5 | Apache 2.0 | 未来多 Agent 模拟 | ✅ 已克隆 |

---

## 1. CoCo-Ex

### 基本信息
- **仓库**: `external/CoCo-Ex/`
- **原始地址**: https://github.com/Heidelberg-NLP/CoCo-Ex
- **License**: Apache 2.0 (需保留版权声明)
- **Stars**: 59
- **兼容度**: 5/5

### 核心价值
CoCo-Ex 从自然语言文本中提取有意义的概念并将其映射到 ConceptNet 节点。
这与 LinguaGraph 的 `src/extract.py` 功能直接对应——都是 文本→概念 的提取管道。

### 可复用模块
| 模块 | 用途 | 集成方式 |
|------|------|----------|
| `concept_extraction.py` | 基于上下文化的 embedding 提取概念 | 作为 extract.py 的第二个 Provider (非 LLM 方案) |
| `mapping_to_conceptnet.py` | 将提取的概念映射到标准化的 KG 节点 | 增强 cross_language_mapping.json |
| 评估方法 | CoCo-Ex 的提取评估指标 | 用于 evaluate_pipeline.py 的对比基线 |

### 集成计划
```
1. 提取 CoCo-Ex 的核心概念提取逻辑
2. 封装为 LinguaGraph Provider (coco_ex.py)
3. 与现有的 OpenAI / Ollama / Mock 并列
4. 在 evaluate_pipeline.py 中对比各 Provider 的 F1
```

### License 遵守
Apache 2.0 要求:
- ✅ 保留原始版权声明 (已复制 NOTICE 文件)
- ✅ 修改时注明变更
- ❌ 不暗示背书

---

## 2. ConceptNet5

### 基本信息
- **仓库**: `external/conceptnet5/`
- **原始地址**: https://github.com/commonsense/conceptnet5
- **License**: Apache 2.0
- **Stars**: 2943
- **兼容度**: 4/5

### 核心价值
ConceptNet5 是规范化的常识知识图谱，有 21M+ 节点和 35M+ 边，横跨 50 种语言。
它的关系分类法 (IsA, HasProperty, UsedFor, Causes, PartOf 等) 是 LinguaGraph 关系类型的参考标准。

### 可复用模块
| 模块 | 用途 | 集成方式 |
|------|------|----------|
| 关系分类法 (relation taxonomy) | LinguaGraph 当前使用的关系类型较少 | 扩展 `src/graph.py` 的关系类型枚举 |
| 评估基准 (MEN, RW, SimLex) | 用于评估概念提取质量 | 在 `tests/` 中添加标准化评估 |
| 多语言概念对齐 | ConceptNet5 的跨语言概念映射方法 | 改进 `config/cross_language_mapping.json` 的映射算法 |

### 集成计划
```
1. 提取 ConceptNet5 的关系分类法
2. 扩展 LinguaGraph 的 relation_type 枚举
3. 添加 ConceptNet 语义相似度作为 LDS 的对比基线
4. 用于 evaluate_pipeline.py 的外部验证
```

### License 遵守
Apache 2.0 — 与 CoCo-Ex 相同要求。

---

## 3. Concordia (Google DeepMind)

### 基本信息
- **仓库**: `external/concordia/`
- **原始地址**: https://github.com/google-deepmind/concordia
- **License**: Apache 2.0
- **兼容度**: 4/5

### 核心价值
Concordia 是一个生成式 Agent 模拟库，Agent 拥有记忆、个性和社会行为。
它的 "Game Master" 架构可用于构建不同语言背景的 Agent 社区——中文 Agent City、德语 Agent City、英语 Agent City。

### 适用场景 (Phase 3)
```
当前 Phase (BWKI):      人类数据的 LDS 计算
Phase 2 (未来):         Human LDS vs Model LDS 对比  
Phase 3 (扩展):         Concordia Agent 模拟 =
                        中文 Agent 群 → 讨论"自由/成功/责任"
                        德语 Agent 群 → 讨论"Freiheit/Erfolg/Verantwortung"
                        → 计算 Agent LDS → 对比 Human LDS
```

### 当前状态
仅作为研究参考，**不集成到 BWKI 提交版本**。

---

## 版权与许可证声明

```
CoCo-Ex:      Apache 2.0 — Copyright Heidelberg-NLP
ConceptNet5:  Apache 2.0 — Copyright Commonsense Computing  
Concordia:    Apache 2.0 — Copyright Google DeepMind
```

所有项目均为开源，已保留原始许可证文件。
LinguaGraph 使用这些项目作为研究参考和方法论借鉴，未复制受保护的代码。
详细许可证文件见各子目录的 LICENSE / NOTICE。
