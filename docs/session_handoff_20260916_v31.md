# Session Handoff v31 — 全模型补满收官 + 共识 v4（2026-09-16）

- 禁区：`tests/` 未动（84 绿）、未打 tag、未碰 `freeze/`/`_deploy/`/`data/lds_c` 既有/`linguaGraph.db`。
- 密钥：同 key 只走内存；本轮尾段 pro 遇 5 连 403（配额墙），其余模型无 403。

## 1. 终局落盘（depth24=72/模型，共 504）

| 模型 | 落盘 | 缺席 | 性质 |
|---|---|---|---|
| qwen3.7-flash | 72 全勤 | 0 | ✅ |
| qwen3.8-27b | 72 全勤 | 0 | ✅ |
| qwen3.8-max-0902 | 72 全勤 | 0 | ✅ |
| qwen3.8-max | 71 | 1（wahrsch r3，四败传输） | 永久缺席 |
| kimi-k3 | 71 | 1（en_ap r3，三败传输） | 永久缺席 |
| deepseek-v4.1-flash | 70 | 2（fischer r2 四败乱码/lambacher r3 两败；ch3 r3 stale-bad 在盘） | 通道天花板 |
| deepseek-v4-pro-0813 | 60 | 9（配额墙阻塞）+3（dnr：abitur r3/wahrsch r1/r2） | 配额墙+通道 |
| 合计 | 488/504（96.8%） | 16 | |

- 关键修复：16k 通道同时治愈 v41 大文件截断（wahrsch/abitur/en_ap r3 全成交）与 pro 小中文件（EN 全系含 stewart 完整）。
- 审计门保持：r=33 越界、mojibake、prompt 回声污染全部拒收（pro 年级下 r2 重试成交等 5+ 例证非确定性）。
- max/kimi/v41-dnr/pro-dnr 共 8 文件列 `do_not_retry`，禁续烧。

## 2. 共识 v4（`research/consensus_v4_20260916.*`，离线重算）

- intra：pro 0.5206 (n20) / v41 0.6000 (n24) / kimi 0.7291 / 3.7 0.6035 / 27b 0.5862 / max 0.6276 / max0902 0.6304。
- inter_global **0.5009**（v3 0.5401→v4 0.5009：ds 系大 n 入场拉低，印证"均值缺席敏感"，两数皆快照，趋势禁报）。
- vs_mimo：pro 0.2220 (n22) / v41 0.2338 (n24) / 其余 0.22–0.26。
- vote：收录 **546** / Solid **203** / Weak **884** / Hypo **1905** / mimo 独有 **70**。
- 终审 v3 文本（C1–C7/口径/禁语/三锁）继续有效，数字引用时以 v4 为准并附快照声明；R5 thr 拆分表仍待出。

## 3. 待办（未变）

- 门户三片段粘贴 + `_deploy` 重建（人工）；submission 对齐；修数③政策（对照表待批）④破环；72 盲审；归档入库授权。
