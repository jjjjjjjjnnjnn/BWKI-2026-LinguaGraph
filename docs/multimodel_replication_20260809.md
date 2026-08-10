# LinguaGraph — 多模型复制深化结果（2026-08-09）

> **管线**: `scripts/lds_c_llm_subject.py`（--model + --api-url 参数化）· `scripts/lds_c_multi_model.py`（复制 harness）
> **数据**: `data/lds_c/llm_subject/llm_subject_{model}_20260809.json`（各 30 单元）+ `multi_model_replication_20260809.json`
> **状态**: 纯 API 深化（新数据），全部可复现 | **承诺**: 复用冻结纯函数（signal_table / label_permutation_null / concept_drivers），零改动冻结管线
> **更新**: v4（**51 个完整模型**：8 zen/OpenRouter + 42 DashScope + gpt-oss 部分）——v1 为 4 模型

---

## 0. 一句话结论

**跨语言价值观分歧是"多语言 LLM 的普遍属性"（ZH-DE 51/51 显著），但强度与方向是模型特异的**：51 个测量（47 个唯一模型，88% 中国提供方 + 1 个 NVIDIA 美国）在相同协议下，**全部 ZH-DE 对显著**（p<0.05），但 **8/153 个语言对（全含英语）不显著**（主要 DeepSeek R1 族）；文化方向（DE 自主/规则 vs ZH 空间/应得）在 **≥10 票阈值超过随机空模型**（207 vs 181，p<0.001），但 ≥3 票的 1179 落在噪声带内。这是**测量方法论 + 广度证据**，不是"所有模型所有语言对都强烈分歧"的普遍定律。

## 2. 信号复制：51 测量，ZH-DE 全显著，英语对部分不显著

- **51/51 的 ZH-DE 对显著**（p<0.05，多数 p=0.0）
- **8/153 个语言对非显著**（p≥0.05），**全部含英语**：deepseek-r1 DE-EN 0.444、r1-0528 DE-EN **0.672**、r1-distill-qwen-7b ZH-EN 0.476/DE-EN 0.052、r1-distill-qwen-14b ZH-EN 0.384、r1-distill-qwen-32b DE-EN 0.224、glm-4.6 DE-EN 0.472、qwen3-235b-a22b DE-EN 0.060
- ZH-DE 余量范围 **+0.033（deepseek-r1-0528）~ +0.286（deepseek-v3.1）**，全为正
- **p 值报告**: 置换检验在 n_iter=500 下观测值高于全部置换样本时报告 p=0.0，严格应报 **p<0.004**（双侧）；153 次检验未做多重比较校正

## 1. 复制设计（为何这是严谨升级）

- **同一协议**：完全相同的 P1（3 语言 × k=10 自然回答 → 概念图 → LDS-C vs split-half floor vs 置换检验）
- **跨来源**：付费端点（deepseek-flash/pro、glm、kimi）+ zen/v1 免费（nemotron-3-ultra-free【NVIDIA 美国】、mimo-v2.5-free、laguna-s-2.1-free）+ OpenRouter 免费（配额受限，待重试）
- **冒烟验证先行**：验证三语顺从 + 提取产出 en gloss，无 H4/C2 伪影风险
- **重试规则**：单条消息内 3× 重试（脚本内置）；连续 3 个 EMPTY 单元自动弃用该模型（`LDS_ABORT_AFTER`）；配额失败 ≠ 模型不可用，清空待重试

## 2. 信号复制：8/8 模型全部检出跨语言分歧

| 模型 | 来源 | ZH-EN | DE-EN | ZH-DE | ZH-DE p |
|------|------|:---:|:---:|:---:|:---:|
| deepseek-v4-flash | DeepSeek（中） | +0.081 | +0.084 | +0.083 | 0.0 |
| deepseek-v4-pro | DeepSeek（中） | +0.065 | +0.072 | +0.075 | 0.0 |
| glm-5.2 | 智谱（中） | +0.149 | +0.137 | +0.155 | 0.0 |
| kimi-k2.6 | Moonshot（中） | +0.158 | +0.145 | +0.135 | <0.01 |
| mimo-v2.5-free | 字节（中） | +0.094 | +0.054 | +0.081 | 0.0 |
| laguna-s-2.1-free | poolside | +0.130 | +0.111 | +0.100 | 0.0 |
| longcat-2.0-free | — | +0.136 | +0.172 | +0.135 | 0.0 |
| **nemotron-3-ultra-free** | **NVIDIA（美）** | +0.102 | +0.109 | **+0.155** | 0.0 |

- 所有 24 个语言对 LDS-C（0.84–0.96）显著高于各自 floor（0.72–0.87），p<0.05（多数 p=0.0）
- **跨中西方来源复现**：NVIDIA（美国）模型显示与 glm/kimi 同量级（甚至更高）的 ZH-DE 分歧 → 非中国模型的独立确认

## 3. 幅度因模型而异（审计工具的实用维度）

- glm/kimi/nemotron/longcat 余量 +0.135~0.172，约为 deepseek 族（+0.065~0.084）的 2 倍
- → 不同模型的"跨语言漂移敏感度"不同——审计报告可按漂移幅度给模型排名

## 4. 方向一致性：显著高于随机，最强在高票（空模型对照）

**方法**：逐概念统计各模型把它标为 DE-only 还是 ZH-only；一个概念在阈值 t "方向一致" = max(DE票, ZH票) ≥ t。**对照空模型**：固定每个概念的实际出现频次，方向随机（p=0.5），检验"多少概念随机就能凑到 t 票同侧"。

| 阈值 t | 观测一致概念 | 空模型期望±SD | p（观测≥空） |
|:---:|:---:|:---:|:---:|
| ≥3 | 1056 | 823±10 | <0.001 |
| ≥5 | 558 | 375±8 | <0.001 |
| **≥10** | **204** | **129±4** | **<0.001** |
| ≥20 | 50 | 8±2 | <0.001 |

→ **方向一致性在全部阈值显著高于随机**，最强在高票（≥20 票 50 vs 8，6 倍）。**注意**：早期"1179 概念"是未对照空模型的 ≥3 双计数，已废弃；空模型对照使主张可复现。

**最强一致概念**（≥10 票，真实覆盖率）：
| DE-only（自主/规则/目标） | (DE,ZH)票 | ZH-only（关系/应得/空间） | (DE,ZH)票 |
|------|:---:|------|:---:|
| Heimat: safety | (41, 0) | Heimat: physical space | **(1, 41)** |
| Gerechtigkeit: equal opportunity | (39, 0) | Verantwortung: indulgence | (0, 34) |
| Freiheit: freedom limit of | (39, 0) | Freiheit: boundary freedom of | (0, 32) |
| Verantwortung: decision | (38, 0) | Gerechtigkeit: the weak | (0, 31) |

**诚实分母**：safety 41 票 = 41/51（80%，10 个模型未产出该概念，非"全票"）；physical space 有 1 个真实反票（dashscope:qwen-plus 标 DE-only）。

## 5. 对论文叙事的强化（AI 审计框架）

1. **测量方法论跨 51 模型工作**：任意可测的多语言模型都能量化跨语言分歧（不是"工具已完成审计"，而是"基础测量已铺开"）
2. **模型排名能力**：ZH-DE 余量 +0.03 ~ +0.29（~9 倍差异），可排序"哪些模型在语言间分歧更大"
3. **文化方向显著高于随机**（空模型对照）→ 支持"多语言训练语料的文化结构"解释
4. **诚实局限**：47 唯一模型、88% 中国提供方、1 个 NVIDIA 美国模型；OpenRouter 西方模型未完成；无审计阈值（未来工作）；2026-08-10 一次 API 欠费事件已披露于 `declaration_of_support.md` §5.1

## 6. 局限与待办

- **OpenRouter 免费配额不足以完成完整 P1**（实测）：`free-models-per-day` 每日约 50–100 次请求（每日 ~08:30 重置），完整 P1 需 180 次 → 单日连一个模型都完成不了。gpt-oss 两天累计 9 good zh 单元（跨日 resume 约 3–4 天/模型）。**结论**：OpenRouter 免费层适合**跨日累积**或用**付费/credits**跑完整 P1；单日免费无法支撑全量复制。
- **已清理**：所有 OpenRouter 文件的空单元已清除（保留 good），跨日 resume 逻辑就绪
- ling-tiny-free 仅 12/30（zh10+de2）——已清理待重试
- 方向一致性是描述性投票度量，非因果解释

## 7. 复现

```bash
# 冒烟验证候选模型（三语顺从 + en gloss）后：
python scripts/lds_c_llm_subject.py --model <model> --probes P1 --k 10 \
    [--api-url https://opencode.ai/zen/v1]  # 或 --api-url https://openrouter.ai/api/v1
python scripts/lds_c_multi_model.py   # 对比 + 方向一致性
```

## 8. 数据血缘

| 资产 | 位置 |
|------|------|
| 复制 harness | `scripts/lds_c_multi_model.py` |
| 被试脚本（--model/--api-url/abort） | `scripts/lds_c_llm_subject.py` |
| 每模型 subject 数据 | `data/lds_c/llm_subject/llm_subject_{model}_20260809.json` |
| 对比结果 | `data/lds_c/llm_subject/multi_model_replication_20260809.json` |
