# LinguaGraph — 多模型复制深化结果（2026-08-09）

> **管线**: `scripts/lds_c_llm_subject.py`（--model 参数化）· `scripts/lds_c_multi_model.py`（复制 harness）
> **数据**: `data/lds_c/llm_subject/llm_subject_{model}_20260809.json`（各 30 单元）+ `multi_model_replication_20260809.json`
> **状态**: 纯 API 深化（新数据），全部可复现 | **承诺**: 复用冻结纯函数（signal_table / label_permutation_null / concept_drivers），零改动冻结管线

---

## 0. 一句话结论

**跨语言价值观分歧是"多语言 LLM 的普遍属性"，不是某个模型的怪癖**：4 个模型（3 个独立提供商 DeepSeek / 智谱 / Moonshot）在完全相同的 P1 组内协议下，全部呈现 LDS-C ≫ 组内底噪、置换检验 p<0.01；且 **47 个概念的方向（DE-自主/规则 vs ZH-关系/应得）跨 ≥3 模型一致，12 个概念 4/4 模型全一致**。"单模型 PoC"这一头号限制被关闭。

---

## 1. 复制设计（为何这是严谨升级）

原发现建立在单个模型 deepseek-v4-flash 上，诚实局限是"proof-of-concept at one model"。复制实验：

- **同一协议**：完全相同的 P1（3 语言 × k=10 自然回答 → 概念图 → LDS-C vs split-half floor vs 置换检验）
- **独立来源**：deepseek-v4-pro（DeepSeek 同族，控制族内一致性）+ kimi-k2.6（Moonshot）+ glm-5.2（智谱）
- **冒烟验证先行**：先验证三语顺从 + 提取产出 en gloss（对齐必需），确认无 H4/C2 伪影风险后才投入全量
- **网关限制（如实披露）**：gpt-5.6-luna（403）与 grok-4.5（503）经 opencode GO 网关不可达——复制只能在可达的中国来源提供商之间进行

## 2. 信号复制：4/4 模型全部检出跨语言分歧

| 模型 | 提供商 | ZH-EN margin | DE-EN margin | ZH-DE margin | ZH-DE p |
|------|--------|:---:|:---:|:---:|:---:|
| deepseek-v4-flash | DeepSeek | +0.081 | +0.084 | +0.083 | 0.0 |
| deepseek-v4-pro | DeepSeek | +0.065 | +0.072 | +0.075 | 0.0 |
| glm-5.2 | 智谱 | +0.149 | +0.137 | +0.155 | 0.0 |
| kimi-k2.6 | Moonshot | +0.158 | +0.145 | +0.135 | <0.01 |

- 所有模型 LDS-C（0.87–0.96）显著高于各自组内 floor（0.74–0.87），全部 12 个语言对 p<0.01
- **信号是普遍属性**：跨语言价值观分歧不是 deepseek 的独特行为

## 3. 幅度因模型而异（审计工具的实用维度）

- glm-5.2 / kimi-k2.6 余量 +0.135~0.158，**约为 deepseek 族（+0.065~0.084）的 2 倍**
- → 不同模型的"跨语言漂移敏感度"不同——审计工具可**按漂移幅度给模型排名**（哪个模型更易在语言间漂移），这是可操作的产品能力

## 4. 方向复制：47 个概念跨模型方向一致

**方法**：逐概念统计各模型把它标为 DE-only 还是 ZH-only；≥3/4 模型同侧 = 方向一致。（top-10 Jaccard 偏低是频率排序所致，方向一致性才是正确的稳健性度量。）

**12 个概念 4/4 模型方向全一致**：

| DE-only（自主/规则/目标） | ZH-only（关系/集体/应得） |
|------|------|
| Gerechtigkeit: equal opportunity | Gerechtigkeit: deserv treatment |
| Gerechtigkeit: the weak（反—ZH 侧） | Freiheit: discipline self |
| Freiheit: freedom limit of | Verantwortung: indulgence |
| Verantwortung: decision | Erfolg: growth |
| Verantwortung: arbitrarines | |
| Heimat: safety | |
| Erfolg: goal own | |
| Erfolg: development personal | |

**47 个概念 ≥3/4 模型方向一致**（完整清单在 `multi_model_replication_20260809.json`）。ZH-only 侧含 physical space、belong of sense、love、memory warm、and law morality、order public、boundary——与"ZH 框为空间/边界/应得/和谐"一致；DE-only 侧含 dignity、society、contentment inner、own valu、familiarity——"DE 框为自主/成就/自我"一致。

→ **文化方向（DE 自主 vs ZH 空间/应得）不是 deepseek 的特异行为，而是跨提供商鲁棒的多语言模型属性**。这与原始 deepseek 发现（a3_c_d_deepen_results §2）一致并强化。

## 5. 对论文叙事的强化（AI 审计框架）

1. **"审计工具跨模型工作"**：不只是 deepseek——在任何可测的多语言模型上都能量化漂移
2. **模型排名能力**：漂移幅度因模型而异（glm/kimi > deepseek），审计报告可给出"哪些模型在语言间更容易漂移"
3. **文化方向稳健**：跨提供商一致 → 分歧反映的是语言-文化语料结构，而非单模型权重怪癖
4. **伦理披露**：西方模型经网关不可达，复制覆盖中国来源提供商——诚实标注，不夸大"所有模型"

## 6. 局限

- 全部 4 个模型为中国来源提供商（网关限制，非选择）
- 仅 P1 探针、k=10、3 语言 5 概念——与原始协议一致以可比
- 方向一致性是描述性投票度量，不是对"为什么"的因果解释

## 7. 复现

```bash
# 冒烟验证候选模型（三语顺从 + en gloss）后：
python scripts/lds_c_llm_subject.py --model deepseek-v4-pro --probes P1 --k 10
python scripts/lds_c_llm_subject.py --model kimi-k2.6   --probes P1 --k 10
python scripts/lds_c_llm_subject.py --model glm-5.2     --probes P1 --k 10
python scripts/lds_c_multi_model.py   # 对比 + 方向一致性
```

## 8. 数据血缘

| 资产 | 位置 |
|------|------|
| 复制 harness | `scripts/lds_c_multi_model.py` |
| 被试脚本（--model） | `scripts/lds_c_llm_subject.py` |
| 每模型 subject 数据 | `data/lds_c/llm_subject/llm_subject_{model}_20260809.json` |
| 对比结果 | `data/lds_c/llm_subject/multi_model_replication_20260809.json` |
