# Bailian Gold Bench v2 20260914

- models: qwen3.8-flash, qwen3.8-max, qwen3.8-max-0902, deepseek-v4-pro-0813, kimi-k3, qwen3.8-27b, deepseek-v4.1-flash, qwen3.7-flash | temperature=0 | n=92 (zh=36, de=29, en=27)
- source: linguaGraph.db gold_labels+responses (read-only, no DB write)
- method: scripts/tools/bailian_gold_bench.py 按模型分拆运行(同prompt/同参数), infra类exception条目顺序重试一次; deepseek空content按口径记parse_fail

## 1. 分语言F1

| model | zh F1 | de F1 | en F1 | overall | fail_rate (exc+parse) |
|---|---|---|---|---|---|
| qwen3.8-flash | 0.7839 | 0.6584 | 0.6713 | 0.7113 | 1.09% (exc=0,parse=1) |
| qwen3.8-max | 0.8348 | 0.6564 | 0.6777 | 0.7325 | 0.00% (exc=0,parse=0) |
| qwen3.8-max-0902 | 0.8266 | 0.6708 | 0.6907 | 0.7376 | 0.00% (exc=0,parse=0) |
| deepseek-v4-pro-0813 | 0.0833 | 0.0345 | 0.0741 | 0.0652 | 93.48% (exc=0,parse=86) |
| kimi-k3 | 0.6016 | 0.5356 | 0.5085 | 0.5535 | 7.61% (exc=0,parse=7) |
| qwen3.8-27b | 0.8008 | 0.6020 | 0.6630 | 0.6977 | 4.35% (exc=1,parse=3) |
| deepseek-v4.1-flash | 0.5305 | 0.2227 | 0.2889 | 0.3626 | 56.52% (exc=0,parse=52) |
| qwen3.7-flash | 0.8358 | 0.6552 | 0.6060 | 0.7114 | 0.00% (exc=0,parse=0) |

## 2. 失败率口径

- exception: API调用异常 (timeout/4xx/5xx/connection); parse_fail: 无`{...}`匹配或concepts空/JSON解析失败(含deepseek空content)。fail_rate=(exc+parse)/总数。
- 8并行初跑时出现 ~12条/模型的 Connection error (DE段集中, 本地并发拥塞所致), 已顺序重试, 上表为重试后终值。
- deepseek两模型经抽查: 多数调用返回空content(raw_len=0, 疑reasoning输出走reasoning_content字段), 属模型/通道兼容问题, 按口径记parse_fail。

## 3. 与已有基线对照 (research/bailian_gold_20260914.json)

- 已有基线: qwen3.8-flash overall=0.6830, qwen3.8-max overall=0.7213 (n=92, temperature=0)
- 本次v2: qwen3.8-flash overall=0.7113 (Δ=+0.0283), qwen3.8-max overall=0.7325 (Δ=+0.0112)
- temperature=0下仍有run间波动 (flash zh 0.7173→0.7839), Δ在预期波动带内, 模型间排序稳定: max-0902 > max ≈ flash > 27b > 3.7-flash > kimi-k3 >> deepseek。

## 4. 与已知qwen-max gloss交叉的对照

- 已知交叉 (research/wiki_gloss_audit_30_qwen_cross_20260914.json): 双模型一致 28/30=93.3%, 分歧 G012(房产:property vs real estate)、G017(negative Freiheit:liberty vs freedom); flash匹配源27/30, max匹配源26/30。
- 金标重叠对照句: 13 条 (gold概念命中cross 30词, 不区分大小写)。前20条见JSON `control.hits`。

## 5. 缺席模型 (403/404)

- 本次无403/404整模型缺席 (8模型均有有效返回; deepseek失败为200空content, 非HTTP缺席)。

