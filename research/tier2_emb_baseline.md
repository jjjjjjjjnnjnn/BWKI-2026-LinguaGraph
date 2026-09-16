# Tier-2 Embedding Baseline（A路线 · 只读复用验证）

> 日期：2026-09-14 · 任务T4 · 只读验证，不重算、不写盘（除本md）
> 验证方式：`json.load` 计数 + 头注释核对，未执行 `--test/--full`

## 1. 复用链（Tier-2 A路线）

```
config/expert_graphs/text_grounding_20260912.json   # substr基座：physics/chemistry items + en_grounded
  → scripts/semantic_ground_en.py                   # A路线单机：nomic预筛 top-5 + phi-4-mini 判官，resume-safe 写 OUT
  → C:/Users/rongj/AppData/Local/Temp/opencode/sem_emb_cache.json  # 语料句向量缓存
  → scripts/sem_shards.py [--n 10]                  # 读缓存（仅label补embed），写 sem_shards/shard_XX.json + manifest
  → 10路并行 Spark 判官 → sem_shards/verdict_*.json
  → scripts/merge_sem_verdicts.py                   # assert 407 + 按名回查，写 OUT + 打印rates
  → config/expert_graphs/text_grounding_en_semantic_20260912.json  # 407 results
```

脚本头注释要点：

- `semantic_ground_en.py:1-9`：EN语义grounding，LM Studio预筛+phi-4-mini裁决，与substring层分离；`--test` 5节点冒烟，`--full` 全量未ground EN节点；写 `text_grounding_en_semantic_20260912.json`（resume-safe）。
- `sem_shards.py:1-6`：P1 prep，embedding预筛top-5，为并行Spark判官写分片；读 `Temp/sem_emb_cache.json`（快，无新embedding除label）；写 `Temp/sem_shards/shard_XX.json + manifest`。
- `merge_sem_verdicts.py:1,16-18`：合并10分片verdicts；`assert len(results)==407` 防静默丢片；`results`即OUT的407条。

## 2. 验证数字（只读 `json.load`，2026-09-14实测）

| 工件 | 预期 | 实测 | 结论 |
|---|---|---|---|
| `sem_emb_cache.json` 条数×维度 | 10615×768？ | **10615 entries，首向量 dim=768** | ✅ 对上 |
| `text_grounding_en_semantic_20260912.json` results/hits | 407/165？ | **results=407，hits=165** | ✅ 对上 |
| 按(graph,hit)分布 | — | physics True 104 / False 139；chemistry True 61 / False 103 | ✅ 合计407/165 |
| `sem_shards/manifest.json` | 10 shards | **10 shards：9×41 + 1×38 = 407；verdict_*.json=10** | ✅ 对上 |
| 基座 `text_grounding_20260912.json` | — | physics 367（已ground 124 / 待做243）；chemistry 220（56 / 164）；待做合计 **243+164=407** | ✅ 与语义results等长，复用口径一致 |

派生覆盖率（与 `merge_sem_verdicts.py:30-37` 同口径：substr + semantic）：

- physics：substr 124/367 + semantic 104 → EN 228/367 = 62.1%
- chemistry：substr 56/220 + semantic 61 → EN 117/220 = 53.2%
- semantic命中率：165/407 = 40.5%

复用命令（本次仅展示，**未执行**）：

```powershell
python3 -c "import json; d=json.load(open('C:/Users/rongj/AppData/Local/Temp/opencode/sem_emb_cache.json',encoding='utf-8')); print(len(d), len(next(iter(d.values()))))"
python3 -c "import json; d=json.load(open('config/expert_graphs/text_grounding_en_semantic_20260912.json',encoding='utf-8')); r=d['results']; print(len(r), sum(1 for x in r if x.get('semantic_hit')))"
```

## 3. 模型卡

- **Embedding**：`text-embedding-nomic-embed-text-v1.5`（`semantic_ground_en.py:19 / sem_shards.py:16`），经 LM Studio `http://127.0.0.1:1234/v1`，维度 **768**，余弦相似度（`cos()`），batch=32。
- **语料**：`data/textbook/open/en_openstax_*sec*.txt + data/textbook/en_mit801_notes_ch*.txt`，分句规则 `40<=len<=500` 去重（`sentences()`），缓存键=句子文本。
- **预筛**：label向量 vs 全语料余弦，取 **top-5**（`sorted(...)[:5]`，两脚本一致）。
- **判官**：
  - A路线单机：`phi-4-mini-instruct`，temperature=0，max_tokens=5，system“physics/chemistry textbook grounding judge”，输出单个数字0-5（0=无匹配）。
  - 实际合并件标注：`muse-spark-1.3-contributor adjudication, 10 parallel judges; substantive-description rule, passing mentions rejected`（OUT `method`字段 + `merge`脚本OUT写入）。
- **Resume/幂等**：`semantic_ground_en.py:126-131` 读OUT已有results按name跳过；`CACHE.write_text` 增量持久化；`merge`用 `assert 407 + name in by_name` 守卫。

## 4. 下一步（--test → --full resume，未执行）

```powershell
# 1) 冒烟（5节点，需 LM Studio 1234 在线：nomic-embed + phi-4-mini）
python scripts/semantic_ground_en.py --test
# 2) 全量 resume（跳过 OUT 已有 name，断点续跑安全）
python scripts/semantic_ground_en.py --full
```

预期：`ungrounded EN nodes: 407`，`resuming: <已做> done`，`corpus sentences ≈ 10615`，`cache hit: 10615 vecs`（命中则零新embed），OUT逐条追加写。

> 禁区未动：仅新增本 `research/tier2_emb_baseline.md`；缓存/配置/分片均只读。
