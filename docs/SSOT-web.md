# SSOT-web — Portal/3D站数字口径 (2026-09-11, P0冻结)

> 核验方法: `manifest.json` + `release/manifest.json` + `README.md` L130-136 实读。
> 结论:两组数字都是真,属**不同scope**。重排版时加scope标注,不改任何数字。

## 双口径对照

| 数字 | 值 | Scope | 来源 | 用处 |
|---|---|---|---|---|
| Concepts (total) | 1,140+ | 全项目 Math 556 + Physics 366 + Chemistry 220 | `README.md` L131-134 | portal hero |
| Relations (total) | 1,100+ direct | 同上 (525 + 383 + 215) | `README.md` L131-134 | portal hero |
| Math nodes / relations / groups | 556 / 525 / 219 | 数学子图 (= 3D可视化数据) | `manifest.json` graph/alignment | 视频 SSOT · CognitiveSpace段 (`556 nodes · 525 relations`) |
| Textbooks | 180+ (68 math + 94 phys + 18 chem) | 全项目 | `README.md` L131-134 | portal contributions |
| Gold labels | 92 (social 72, math 20) | 全项目 | `README.md` L142 | validation |
| F1 | social 0.939 / weighted 0.881 | 全项目 | `README.md` L144+ | hero + validation |
| LLM replication | 55 Messungen / 50 Modelle | LLM-as-subject (§5) | `data/lds_c/llm_subject/` | 视频 S04, portal Finding E |
| Benchmark | 19 models (Bailian free-quota, gold 92) | 模型选型基准 | portal #validation | portal hero "19-model benchmark" |
| Human study | N=15 (6 DE + 6 ZH + 3 EN), ΔLDS≈0 | between-subject | `docs/paper/` | portal Finding E + 视频 S05 |

## 重排版执行规则

1. hero 保留 1,140+ / 1,100+,下方加一行 scope 注脚:
   `Math 556 · Physics 366 · Chemistry 220 — full project graph (README.md §dataset)`.
2. CognitiveSpace 段保留 `556 nodes · 525 relations · 219 groups`,标注 `mathematics subgraph (manifest.json)`.
3. "19-model benchmark" 旁标注 `model-selection benchmark on 92 gold labels`,与 §5 的 55/50 区分。
4. 禁止新数字;物理/化学数只用 README 已有值,不反查 legacy pipeline。
