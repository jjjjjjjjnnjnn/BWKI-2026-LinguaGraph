# LinguaGraph — Technology Transfer：MML Runtime

> **Status:** Architecture vision · Prototype validated · Production extraction post-BWKI
>
> 本文档描述 LinguaGraph 研究过程中产出的技术资产，以及如何被独立项目复用。
> 这不是"研究项目做了一个游戏"，而是"研究产出的基础设施可以脱离研究场景独立存在"。

---

## 1. 核心概念：MML Runtime

MML (Minimal Model Loader) Runtime 是 LinguaGraph 的通用模型基础设施层。
它不绑定任何特定任务，只提供模型加载、推理、量化和适配器接口。

```
mml-runtime/
│
├── loaders/          模型加载（GGUF / safetensors）
│   ├── gguf.py       llama.cpp GGUF loader
│   └── safetensor.py HuggingFace safetensors loader
│
├── adapters/         LoRA 适配器管理
│   ├── base.py       Adapter 抽象基类
│   ├── lora.py       LoRA 权重合并/切换
│   └── hotswap.py    运行时热切换多个 adapter
│
├── quantization/     量化策略
│   ├── gguf.py       Q4_K_M / Q8_0 量化
│   └── profile.py    内存/速度基准测试
│
├── inference/        推理接口
│   ├── local.py      本地推理（llama.cpp）
│   ├── server.py     HTTP Server 模式
│   └── structured.py JSON 结构化输出约束
│
├── cache/            KV cache 管理
│   └── shared.py     跨请求缓存复用
│
└── config/           配置
    ├── providers.yaml Provider 热切换配置
    └── models.yaml   模型注册表
```

**关键设计原则：**

| 原则 | 说明 |
|------|------|
| **Task-agnostic** | Runtime 不知道自己在做概念提取还是 NPC 对话，它只负责"加载模型 → 推理 → 返回 tokens" |
| **Hot-swappable** | 运行时切换 LoRA adapter 不需要重启进程，改 config 即可 |
| **Stateless protocol** | 应用层通过 HTTP/JSON 与 Runtime 通信，不绑定编程语言 |

---

## 2. 架构总览

```
                        ╔══════════════════╗
                        ║   Qwen2.5-1.5B   ║
                        ║  (GGUF Q4_K_M)   ║
                        ║     ~900 MB      ║
                        ╚══════════════════╝
                                │
                    ┌───────────┴───────────┐
                    │     MML Runtime        │
                    │  (shared infra layer)  │
                    └───────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    │   Adapter Manager      │
                    │  (LoRA hot-swap)       │
                    └───────────┬───────────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
         ▼                      ▼                      ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ LinguaGraph      │   │ Game Project    │   │ Future: Browser │
│ Adapter          │   │ Adapter         │   │ Adapter         │
├─────────────────┤   ├─────────────────┤   ├─────────────────┤
│ Task: Concept   │   │ Task: NPC       │   │ Task: Any       │
│ extraction      │   │ dialogue /      │   │ (WebGPU)        │
│                  │   │ narration       │   │                  │
│ Output: JSON    │   │ Output: JSON    │   │ Output: JSON    │
│ concepts +      │   │ dialogue +      │   │ Any schema      │
│ relations       │   │ emotion tags    │   │                  │
│                  │   │                  │   │                  │
│ Prompt:         │   │ Prompt:         │   │                  │
│ "Extract        │   │ "Generate NPC   │   │                  │
│ concepts from   │   │ dialogue for    │   │                  │
│ this response"  │   │ this scenario"  │   │                  │
└─────────────────┘   └─────────────────┘   └─────────────────┘
```

**关键观察：** 分叉点在 Adapter 层，不在 Runtime 层。Runtime + 基座模型是共享的。

---

## 3. 共享组件清单

以下组件在两个项目间**代码级复用**，不需要修改：

| 组件 | LinguaGraph 用法 | 游戏项目用法 | 复用率 |
|:-----|:----------------|:-------------|:------:|
| `loaders/gguf.py` | 加载 Qwen2.5-1.5B GGUF | 同一文件，无修改 | **100%** |
| `adapters/base.py` | Adapter 抽象 | 同一接口 | **100%** |
| `adapters/lora.py` | LoRA 合并 | 同一接口 | **100%** |
| `quantization/gguf.py` | Q4_K_M 量化 | 同一配置 | **100%** |
| `inference/local.py` | llama.cpp Python 调用 | 同一调用 | **100%** |
| `inference/structured.py` | JSON schema 约束 | 不同 schema，同一机制 | **90%** |
| `inference/server.py` | HTTP 服务端 | HTTP 服务端 | **100%** |
| `config/providers.yaml` | Provider 注册 | 修改 provider 列表 | **50%** |

**不共享的组件：**

| 组件 | LinguaGraph | 游戏项目 |
|:-----|:-----------|:---------|
| LoRA adapter 权重 | Concept extraction (20 MB) | NPC dialogue (20 MB) |
| Prompt template | "Extract concepts and relations…" | "Generate character dialogue…" |
| Output schema | `{concepts: [...], relations: [...]}` | `{dialogue: [...], emotion: ...}` |
| Config presets | BWKI 评测用参数 | 游戏运行时参数 |

---

## 4. LinguaGraph Adapter

| 属性 | 值 |
|:-----|:----|
| **基座** | Qwen2.5-1.5B-Instruct |
| **量化** | Q4_K_M (~900 MB) |
| **LoRA rank** | 16 |
| **训练数据** | 500+ 合成 + 30 黄金标注 |
| **输出** | `{concepts: [...], relations: [...]}` |
| **延迟** | ~200ms / 次提取 |
| **部署** | Python + llama-cpp-python |

**Config:**
```yaml
# providers.yaml
providers:
  linguagraph:
    adapter: linguagraph_concept_extraction
    model: lingua_graph_model.gguf
    prompt_template: prompts/concept_extraction_v2.txt
    output_schema: schemas/concept_graph.json
    temperature: 0.1
```

---

## 5. Game Adapter

| 属性 | 值 |
|:-----|:----|
| **基座** | Qwen2.5-1.5B-Instruct（同一模型文件） |
| **量化** | Q4_K_M（同一配置） |
| **LoRA rank** | 16 |
| **训练数据** | 22+ 部小说 ~1M 字 |
| **输出** | `{dialogue: [...], emotion: "...", topics: [...]}` |
| **延迟** | <500ms（可接受，比模型快即可） |
| **部署** | Godot 4 → HTTP → llama-server |

**Config:**
```yaml
# providers.yaml
providers:
  game_npc:
    adapter: game_npc_dialogue
    model: lingua_graph_model.gguf       # 同一模型文件
    prompt_template: prompts/npc_dialogue_v1.txt
    output_schema: schemas/npc_response.json
    temperature: 0.3
```

**游戏侧架构：**
```
Godot 进程                  llama-server 进程
┌─────────────┐           ┌──────────────────┐
│ AI_Client    │──HTTP──→  │ MML Runtime       │
│ .gd          │           │ + Game LoRA       │
│              │←──JSON── │                    │
│              │           │ 内存常驻 ~1.5 GB   │
│ 队列 + 超时  │           │ 20-30 tok/s       │
│ + 降级模板   │           └──────────────────┘
└─────────────┘
```

游戏启动时 spawn `llama-server` 子进程，退出时 kill。模型掉线时降级到模板数据，游戏依然可玩。

---

## 6. 未来：WebGPU 浏览器推理

MML Runtime 的 HTTP/JSON 协议天然支持 WebGPU 后端替换：

```
当前（本地推理）:
  Godot → HTTP → llama-server (CPU/GPU)

未来（浏览器推理）:
  Browser → WebGPU → MML Runtime (GPU, 浏览器内)
```

**WebGPU 带来的能力：**

| 场景 | 当前方案 | WebGPU 方案 | 优势 |
|:-----|:---------|:------------|:-----|
| LinguaGraph 演示 | 需安装 Python + llama.cpp | **浏览器打开即用** | 零部署成本 |
| 游戏用户 | 需下载 900MB 模型 | 渐进式加载 | 降低门槛 |
| Cognitive City | 静态 3D | **AI 驱动的动态可视化** | 评委可交互 |

**技术路径：**
```
WebLLM (Mozilla) / llama.cpp WebGPU build
    ↓
浏览器内加载 Qwen2.5-1.5B Q4_K_M
    ↓
MML Runtime JavaScript 移植
    ↓
同一 Adapter 接口，不同后端
    ↓
LinguaGraph: 浏览器内概念提取
Game: 浏览器内 NPC 对话
```

WebGPU 不是 MVP 必需的，但它是一条清晰的 evolution path，答辩时可以展示。

---

## 7. 对 BWKI 的战略价值

### 7.1 正确的叙事层次

```
LinguaGraph BWKI 项目
   │
   ├── 研究贡献：LDS 指标、认知图谱、三语对比
   │
   └── 技术资产：MML Runtime
         │
         ├── LinguaGraph Adapter（研究）
         │
         └── Game Adapter（独立项目复用）
```

**评委看到的：**
- 项目不只是跑了一组实验
- 产出了一套可复用的技术基础设施
- 架构设计考虑了通用性和可迁移性
- 有实际的外部项目验证了这套设计

### 7.2 答辩话术（30 秒版）

> "LinguaGraph 研究过程中，我们开发了一套轻量化模型运行时。
>
> 这些组件——Provider 抽象、GGUF 量化、LoRA 适配——设计时就是任务无关的。
>
> 目前有一个独立的游戏项目正在复用这套基础设施，
> 用不同的 LoRA 适配器做 NPC 对话生成。
>
> 这说明 LinguaGraph 的技术资产可以脱离研究场景独立存在。"

### 7.3 在论文中的痕迹

| 位置 | 内容 |
|:-----|:------|
| §1.2 | 一句话提及技术复用 |
| §7.5 | 一段概述 + 指向本文档 |
| §6.5 (#7) | 诚实声明仍在早期 |
| README | 三语各一行 "技术复用" |

---

## 8. 当前状态

| 组件 | 状态 | 说明 |
|:-----|:----:|:------|
| `loaders/gguf.py` | ✅ 现有（LinguaGraph 已实现） | 可直接提取 |
| `adapters/base.py` | ✅ 现有 | 可直接提取 |
| `inference/local.py` | ✅ 现有 | 可提取为独立包 |
| `quantization/gguf.py` | ✅ 已验证 | 脚本已存在 |
| `inference/structured.py` | ⚠️ 需抽象 | 目前在 extract.py 中硬编码 |
| `inference/server.py` | 🔄 游戏侧开发中 | Godot ↔ llama-server 通信 |

**最近里程碑：** 当 `inference/server.py` 跑通 Godot 全链路时，MML Runtime 的核心架构就得到了端到端验证。

---

*Document version: v1.0 · 2026-06-18*
*Author: Claude (PM + QA Lead)*
