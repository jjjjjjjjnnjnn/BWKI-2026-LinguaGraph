# LinguaCore Runtime — Technical Architecture & Implementation Plan

> **目标**: 一个极小的"语义变换器（Semantic Transformer）"，模型只负责语言层，所有逻辑由程序端完成。
> **核心原则**: 更强的游戏系统 → 更弱的模型 → 更好的整体体验

---

## 1. 核心架构

```
Input (游戏/研究数据)
    ↓
┌─────────────────────────────────────┐
│        程序状态机 (100% 逻辑)         │
│                                     │
│  WorldManager  → 世界状态管理         │
│  MemorySystem  → NPC记忆检索          │
│  QuestSystem   → 任务状态跟踪          │
│  FactionSystem → 势力关系计算          │
│  EconomySystem → 资源管理              │
│  CombatSystem  → 战斗逻辑              │
│  GraphBuilder  → 知识图谱构建 (BWKI)   │
│  LDSEngine     → LDS计算 (BWKI)       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│        Prompt Builder                │
│  构建结构化输入 (状态 → JSON)         │
│  "模型只看得到这个"                   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│    [ LinguaCore-0.5B ]               │
│    Qwen2.5-0.5B GGUF Q4_K_M        │
│    ~350-400 MB on disk              │
│    ~800 MB RAM at runtime           │
│    ~15+ tok/s on mobile             │
│                                      │
│  模型只输出:                          │
│  { "reply": "一句话" }               │
│  { "concepts": [...], "relations": } │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│        Parser + Validator            │
│  JSON解析 → 类型检查 → 字段验证       │
│  失败时降级为规则回复                   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│        Post-Processor                │
│  可读化处理 → 缓存 → UI 更新          │
│  (程序端，不需要模型)                  │
└─────────────────────────────────────┘
    ↓
Output (屏幕 / 程序逻辑)
```

## 2. 推理预算

### 一次交互 = 1 次推理（严禁链式推理）

```
❌ 错误:
  玩家输入 → 模型推理 → 意图识别
                                               ← 1
  NPC回复  → 模型推理 → 生成回复
                                               ← 2
  更新记忆 → 模型推理 → 记忆摘要
                                               ← 3  ← 手机发热

✅ 正确:
  玩家输入 → 程序意图检测 → 状态机更新 → Prompt Builder
  → [模型推理 × 1] → 一句话回复 → Parser → UI
                                               ← 1  ← 玩家无感
```

### 推理频率

| 场景 | 推理次数 | 说明 |
|------|:--------:|------|
| NPC 日常对话 | 0 | 规则系统覆盖 80% |
| NPC 关键对话 | 1 | 仅生成回复文本 |
| NPC 记忆触发 | 1 | 仅生成记忆相关回复 |
| Concept Extraction (BWKI) | 1 | 输入文本 → JSON |
| Translation (BWKI) | 1 | 输入文本 → 翻译文本 |

**目标: 90%+ 交互零推理**

## 3. 模型规格

### 当前选择：Qwen2.5-0.5B GGUF Q4_K_M

| 指标 | 数值 |
|------|------|
| 模型大小 | ~350-400 MB (on disk) |
| 运行时内存 | ~800 MB RAM |
| 推理速度 (手机) | 15+ tok/s |
| 推理速度 (桌面) | 118+ tok/s |
| 量化格式 | GGUF Q4_K_M |
| 格式兼容 | llama.cpp, mml_client.gd |

### 长期目标：LinguaCore-0.3B

| 指标 | 数值 |
|------|------|
| 模型大小 | ~150-250 MB |
| 运行时内存 | ~500 MB RAM |
| 方式 | Qwen0.5B 裁剪 / SmolLM / TinyLlama |

## 4. 共享协议

两个项目共用同一套 TaskRequest/TaskResponse 协议：

```python
# 输入
request = TaskRequest(
    task=TaskType.NPC_DIALOGUE,       # 任务类型
    text="你好",                       # 输入文本
    system_prompt="你是客栈老板...",    # 上下文
    max_tokens=64,                    # 限制输出长度
    temperature=0.3,                  # 低温度 = 稳定
)

# 输出
response = provider.generate(request)
# response.raw_text = '{"reply":"住店还是打尖？","action":"greet"}'

# 程序端处理
output = json.loads(response.raw_text)
npc_say(output["reply"])
```

## 5. 实施计划

### Phase 1: 架构对齐（现在）

| 任务 | 状态 |
|------|------|
| TaskRequest/TaskResponse 协议 | ✅ BWKI 已实现 |
| Provider + Router + Fallback | ✅ 已实现 |
| LocalProvider (GGUF) | ✅ 已实现 |
| MockProvider (测试) | ✅ 已实现 |
| Aftermask NPC 规则系统 | ✅ 已实现（350行） |
| Aftermask 转生引擎 | ✅ 已实现（320行） |

### Phase 2: 集成与测试（现在）

| 任务 | 状态 |
|------|------|
| Aftermask → LocalProvider 连接 | 📋 待实现 |
| NPC 对话端到端测试 | 📋 待实现 |
| BWKI pipeline 完整验证 | ✅ 45/45 |

### Phase 3: 移动端部署

| 任务 | 预计 |
|------|------|
| Android NDK 编译 llama.cpp | BWKI 数据到齐后 |
| mml_client.gd 异步改造 | BWKI 数据到齐后 |
| 手机端测试 | BWKI 数据到齐后 |

## 6. 验证指标

| 指标 | 当前 | 目标 |
|------|:----:|:----:|
| 模型体积 | 463 MB | <400 MB |
| 运行时内存 | ~1.2 GB | <1 GB |
| 手机推理速度 | 未测试 | >15 tok/s |
| 零推理交互占比 | 未测量 | >90% |
| NPC 规则覆盖率 | ~80% | >80% |
| 端到端延迟 (桌面) | ~118 tok/s | >50 tok/s |
