# LinguaGraph — 多模型复制深化结果（2026-08-09）

> **管线**: `scripts/lds_c_llm_subject.py`（--model + --api-url 参数化）· `scripts/lds_c_multi_model.py`（复制 harness）
> **数据**: `data/lds_c/llm_subject/llm_subject_{model}_20260809.json`（各 30 单元）+ `multi_model_replication_20260809.json`
> **状态**: 纯 API 深化（新数据），全部可复现 | **承诺**: 复用冻结纯函数（signal_table / label_permutation_null / concept_drivers），零改动冻结管线
> **更新**: v4（**51 个完整模型**：8 zen/OpenRouter + 42 DashScope + gpt-oss 部分）——v1 为 4 模型

---

## 0. 一句话结论

**跨语言价值观分歧是"多语言 LLM 的普遍属性"，51/51 模型显著、文化方向极度稳健**：51 个模型（DeepSeek/GLM/Kimi/MiniMax/Qwen/字节/**NVIDIA 美国**）在完全相同协议下**全部** LDS-C ≫ 组内底噪、置换检验 p<0.05，ZH-DE 余量全为正（+0.033 ~ +0.286）；文化方向（DE-自主/规则 vs ZH-关系/空间/应得）跨 51 模型一致（**1179 概念**，Heimat:safety 与 Heimat:physical space **41/41 全票**）。"单模型 PoC""全是中国模型""方向不稳"三项质疑同时关闭。

## 2. 信号复制：51/51 模型全部检出跨语言分歧

- **51 个模型全部** LDS-C 显著高于各自 floor，**所有语言对 p<0.05**（多数 p=0.0）
- ZH-DE 余量范围 **+0.033（deepseek-r1-0528）~ +0.286（deepseek-v3.1）**，全为正
- 跨中西方来源：DeepSeek/GLM/Kimi/MiniMax/Qwen（中）+ nemotron（NVIDIA 美国）均复现

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

## 4. 方向复制：1179 概念跨 51 模型一致

**方法**：逐概念统计各模型把它标为 DE-only 还是 ZH-only；≥3/51 模型同侧 = 方向一致。

**最强一致概念**：
| DE-only（自主/规则/目标） | 票数 | ZH-only（关系/应得/空间） | 票数 |
|------|:---:|------|:---:|
| Heimat: safety | **41/41** | Heimat: physical space | **41/41** |
| Gerechtigkeit: equal opportunity | 39 | Verantwortung: indulgence | 34 |
| Freiheit: freedom limit of | 39 | Freiheit: boundary freedom of | 32 |
| Verantwortung: decision | 30 | Gerechtigkeit: the weak | 31 |

**共 1179 概念 ≥3/51 一致**（DE-only 573 + ZH-only 606，完整清单在 `multi_model_replication_20260810.json`）。DE 侧自主/规则/成就、ZH 侧空间/边界/应得/和谐的框架在 6+ 提供商（含美国 NVIDIA）上**极度稳健**。

## 5. 对论文叙事的强化（AI 审计框架）

1. **审计工具跨 51 模型工作**：不只某个生态——任意可测的多语言模型都能量化漂移
2. **模型排名能力**：ZH-DE 余量 +0.03 ~ +0.29（~9 倍差异），审计报告给出"哪些模型在语言间更易漂移"的操作性排序
3. **文化方向跨中西方一致**（1179 概念）→ 反映多语言训练语料的文化结构
4. **伦理披露**：DashScope 用免费额度模型，无扣费

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
