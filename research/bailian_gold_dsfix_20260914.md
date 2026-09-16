# Bailian Gold Bench 20260914

- models: deepseek-v4-pro-0813, deepseek-v4.1-flash | temperature=0 | n=92 (zh=36, de=29, en=27)
- source: linguaGraph.db gold_labels+responses (read-only, no DB write)

## 1. 分语言F1

| model | zh F1 | de F1 | en F1 | overall | fail_rate (exc+parse) |
|---|---|---|---|---|---|
| deepseek-v4-pro-0813 | 0.1757 | 0.0517 | 0.1852 | 0.1394 | 76.09% (exc=0,parse=70) |
| deepseek-v4.1-flash | 0.5842 | 0.2778 | 0.2222 | 0.3814 | 53.26% (exc=0,parse=49) |

## 2. 失败率口径

- exception: API调用异常 (timeout/4xx/5xx); parse_fail: 无`{...}`匹配或concepts空/JSON解析失败。fail_rate=(exc+parse)/总数。

## 3. 与已知qwen-max gloss交叉的对照

- 已知交叉 (research/wiki_gloss_audit_30_qwen_cross_20260914.json): 双模型一致 28/30=93.3%, 分歧 G012(房产:property vs real estate)、G017(negative Freiheit:liberty vs freedom); flash匹配源27/30, max匹配源26/30。
- 金标重叠对照句: 13 条 (gold概念命中cross 30词, 不区分大小写)。前20条见JSON `control.hits`, 下表示例(最多10条):

| resp_id | lang | hit_concepts | qwen-max gloss |
|---|---|---|---|
| RS001_zh_q_freedom_words | zh | 责任 | 责任=>responsibility |
| RS001_zh_q_home_scenario | zh | 家庭 | 家庭=>family |
| RS001_zh_q_home_words | zh | 责任 | 责任=>responsibility |
| RS001_zh_q_justice_words | zh | 责任 | 责任=>responsibility |
| RS001_zh_q_resp_words | zh | 责任 | 责任=>responsibility |
| RS001_zh_q_success_def | zh | 家庭 | 家庭=>family |
| RS001_zh_q_success_scenario | zh | 家庭 | 家庭=>family |
| RS004_zh_q_freedom_words | zh | 责任 | 责任=>responsibility |
| RS004_zh_q_home_diff | zh | 责任 | 责任=>responsibility |
| RS004_zh_q_justice_words | zh | 责任 | 责任=>responsibility |

