# Session Handoff v29 — 补跑收官 + 表决v3（2026-09-15）

- 基地：`C:\Users\rongj\Desktop\学校\BWKI-2026-备战`；前序 v28。
- 禁区守住：未改 `tests/`（只读跑门禁）、未打 tag、未碰 `freeze/`/`_deploy/`/`data/lds_c/llm_subject/` 既有文件/`linguaGraph.db`（无写）；`pytest 84 passed`（本轮实跑 31.75s 全绿）。
- 密钥：新 key（对话内 `sk-ws-H.…`，本文件不记全文）只走 `$env:BAILIAN_API_KEY` 内存；本轮全程无 403（配额充足），禁写文件/日志/git 遵守。
- 口径冻结延续：`556 / 238-of-525 / 219`；`59/54/177 vs 62/57/186`；`F1≈0.881 / 0.939† / harness~0.65`。

## 1. 本轮战果（新 key，temperature=0，mimo-schema 统一 prompt）

- P0：7 模型轻探针全 OK（ds 系回 reasoning 风格，属已知 harness 行为）。
- P1 ds-pro：16000/32000 双通道实证失败——16k 截断（brace 26/25，JSON 半截），32k 超时；判定 extraction 通道不可靠，bulk 停止，ds-pro 维持 harness 不兼容（C4 不变），depth 落盘 12/72 作探索存档。
- P2 kimi：`en_probability` 回收（c40r30）；`en_ap r2/r3` 在 7.9KB 大文件上 2× 传输失败 → 缺席确认（r1 仍在）。kimi depth 70/72。
- P3 v41：尺寸天花板实证——625B 小文件 OK，~1000B+ DE 系统性 mojibake（`?t`）+ 截断；对账回收 15 + 新跑 4（含 ch3 r2 重试成功）；fischer r2（4败）/lambacher r3（2败）列 `do_not_retry`，bulk 止损。v41 done 50（depth 落盘约 35+2 review）。
- 全模型对账（零成本回收 16+29：v41 15 + ds-pro 1 + max breadth 17 + v41 breadth 12），并揪出 manifest 落后于落盘的系统性问题。
- P4 qwen 广度+depth 残余：0902 depth **72/72 完成**；3.7 depth 72/72（早满）；max 71/72（wahrsch r3 2× 传输失败→缺席）；27b 71/72（abitur r3 2× 超时→缺席）；广度 qwen 四模型 bmiss 清零（3.7/max/0902/27b done 113/112/113/112，失败仅上述 depth 缺席项）。
- 并发：2→12 工人实测，10 工人 10/10 最稳；12 工人现 1 超时即回落；同 base 禁并行（stage 文件共享，已用全局 distinct-bases + 同模型 manifest 父进程单线程更新解决）。
- 质量门：审计（15–40概念/10–30关系/引用闭合/无占位/无`?�`乱码）+ 调用失败禁入库（fresh-stage 守卫，拦截 1 起 r1/r2 复本污染并回滚）+ 失败重试1次记缺席；不严谨项只放探索区。

## 2. 表决 v3（`research/consensus_v3_20260915.json/.md`，离线重算）

- intra：pro 0.6029(n5) / v41 0.6393(n14) / kimi 0.7347 / 3.7-flash 0.6035 / 27b 0.5928(n24) / max 0.6276(n24) / max0902 0.6304(n24)。
- inter_global **0.5401**（v2 0.4629 为配额截断值，v3 以 qwen 全 depth 为准；ds 行仍小样本）。
- vs_mimo 0.22–0.26；vote：收录 **540** / Solid **191** / Weak **739** / Hypo **1710** / mimo 独有 **74**（v2：491/145/506/1554/76）。
- 以上仍为快照口径（ds 列小样本 + 4 个单文件缺席），禁报完成品；verdict 文本 v3 未写。

## 3. 脚本变更（`scripts/tools/`，3 文件）

- `bailian_reextract.py`：`BAILIAN_MAX_TOKENS` 环境覆盖 + `reasoning_content` 回退 + ASCII 安全打印。
- `ensemble_refill_one.py`（新）：单发抽取→审计→入库→manifest 更新；stale-stage 守卫；`--auto-depth/--auto-breadth/--do_not_retry`。
- `ensemble_refill_batch.py`（新）：多进程批跑，父进程统一更新 manifest，403 停调度。

## 4. 下轮（P5，全部离线零成本）

1. 终审 v3 文本（C1–C7 行号不变，v3 数追记；inter 0.46→0.54 口径变更必须显式声明原因）。
2. Two-Tier/Limitations 追加非确定性实证 + v41 通道天花板。
3. 门户补丁仍按 `portal_patch_20260914.md` 人工三片段粘贴（未贴）。
4. 修数任务（删幻觉边/纠错边/去重24/破11环），清零前不得冻结、不得打 tag。
5. 可选：4 个单文件缺席（max wahrsch r3 / 27b abitur r3 / kimi en_ap r2r3） deferred 单重试一次。
