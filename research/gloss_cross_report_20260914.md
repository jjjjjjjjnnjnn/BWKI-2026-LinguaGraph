# Gloss Cross Report 20260914 — qwen3.8-flash vs max (30词)

- 输入:
  - `research/wiki_gloss_audit_30.json` (seed=20260914, n=30, population=96, 源模型 deepseek-v4-flash)
  - `research/wiki_gloss_audit_30_qwen_cross_20260914.json` (models=[qwen3.8-flash, qwen3.8-max], n=30)
- 日期: 2026-09-14

## 1. 双模型交叉一致率

- 一致: **28/30 = 93.3%**
- 分歧: **2/30 = 6.7%** (G012, G017)

## 2. 与源 gloss_en 匹配率 (`match_source` 字段)

- 匹配: **27/30 = 90.0%**
- 不匹配: **3/30 = 10.0%** (G001, G014, G017)
- 按模型拆分(精确字符串相等 vs `gloss_en`):
  - flash 匹配源: 27/30 = 90.0% (仅 G001/G014/G017 不等)
  - max 匹配源: 26/30 = 86.7% (G001/G012/G014 不等, G017 相等)

## 3. 分歧2条明细

| audit_id | zh | 源 gloss_en | flash | max | match_source |
|---|---|---|---|---|---|
| G012 | 房产 | property | property | real estate | true (flash侧命中) |
| G017 | negative Freiheit | negative freedom | negative liberty | negative freedom | false (max侧命中, flash侧 liberty/freedom 变体) |

备注(一致但与源不匹配, 非分歧, 供复核):
- G001 住所: 源 dwelling vs 双模型一致 residence
- G014 无家可归: 源 homeless vs 双模型一致 homelessness (词性/单复数变体)

## 4. 结论

- 第二模型交叉已闭环一半: qwen3.8-flash vs max 双跑完成, 一致率 28/30, 源匹配率 27/30; 剩余一半(人工裁决)未闭环。
- `research/wiki_gloss_audit_30.json` 中 `accept/notes/qwen_cross_gloss` 仍全空, 缺人工 accept/notes。
- 故 §7 维持 `needs_review`, 不得标 verified。
