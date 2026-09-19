# Session Handoff v44 — Harness v2 + Agent-Panel 收官 (2026-09-19)

状态: `master` clean, 远端已同步 (ahead 0, 10 commits: 522964a…f083eef 全上 `origin/master`)。
门禁: numbers-gate PASS / cdn-gate PASS / pytest 84/84 (终验 09-19)。
工作树: 干净 (仅 `.env` ignored + `_log_*` ignored)。 key 零入库 (4 串只在聊天记录, 轮换待 Owner)。

## 一、本轮完成 (v43 之后)
- **Harness v2 CORE** (prereg v1.2 A11–A18, 首 call 前冻结; P0–P3 四 cell SHA 冻结, 驱动=`--cell` 单源 `_v2_cells.json`):
  P1 (CARD-only) / P2 (LANG-only EN+DE+zh10) / P3 (BOTH) × glm-r4 / deepseek-r4 / 6.8-sn (+ big-pickle western P3)。
  minimax EXCLUDED (Owner: 不可用), F5/qwen CUT (Owner)。
- **v2 结论** (REPORT §7 + `V2_MATRIX.json`, A2 fails=0/92, B=1000/seed 20260918):
  F1 CARD **CONFIRMED** (paired dF1 +0.27/+0.41/+0.34; glm 帯 drift-caveat 见下);
  F2 LANG **MODEL-SIDE FAILURE** (EN-CJK 5–56%→0.0% 全员服从, EN-F1 仍 0.02/0.14/0.00);
  P3: deepseek **V2-validated** (soc 0.544), glm caveated (0.544), 6.8 **marginal miss** (0.395<0.40, 未四舍五入),
  big-pickle 描述性 0.608 (EN 0.377 最高, partial-46 对照)。
  P1-EN≈P3-EN → EN lift 来自基数, 与语言句无关。pred_n 12–17→~2.2。
- **glm P0cal drift +0.32** (同 prompt 同传输隔夜漂移, en_001 在 P0 下拿 1.0): glm lift 全标 caveat; deepseek/6.8 drift≈0 干净。
  附带: WindowsApps-`python3` stub + 重定向 = 假死 (改真 python 路径 + `python*` 监控)。
- **E2 P3b** (A18, glm n=30, SHAs f91a3dad/8058b210): |P3b−P3| +0.024 → **ROBUST** (P3 非措辞脆弱)。
- **Agent-Panel** (A-Judge J1–J7, falsify-only 永不转正): R1 deepseek / R2 glm / R3 6.8 / R4 cohere-openrouter (51/72, daily-429 熔断停车) / R5 big-pickle。
  共识 `--import`: rejects 15, agr 0.389, qwen-F1 0.419 → **MAINTAIN** (弱证据 maintain, Jaccard ~0.1 噪声大)。
  **11/72 五家一致 reject** (A005/A006/A014/A018/A020/A022/A027/A028/A032/A035/A041, 含 Western R4/R5) = falsify-grade gold 质量 caveat (~15%)。
  R2 (36 rejects, 14 solo) = rater 噪声。详见 `research/gold_review_v2/PANEL_SCREEN.md`。
- **Claims**: C21 定量改写 (v2-partial-repro), C23 harden (Mature 候选), **C24 新增** (Western EN), C9b 纹丝不动 Developing (+panel caveat)。
- **治理**: D-V1–D-V5 (filter/resume 覆盖丢数据×2、stage 教训、sandbox 污染、 stub、 freeze 记录) 全 CLOSED; D-S1 bounds-CLOSED。
  prereg: v1.1 (A1–A10) + v1.2 (A11–A18) + A-Judge (J1–J7)。
- **提交动作**: push×2 (8+2 commits); textbook 95 `rm --cached` (工作拷贝保留); sn 碎臂按 partial 提交; `_log_*` + panel_prompts 入 ignore。
- **审核纪律**: 每 cell 独立复算 (SHA/配对/分母三查); scorer 两个 order-bug 现场抓获; 6.8 P3 soc 0.395 不凑 0.40; R2 噪声不藏。

## 二、关键数字 (A2, paired)
- v1 social: 0.10–0.15 (6 臂); v2 P3 social: glm 0.544 / deepseek 0.544 / 6.8 0.395 / big-pickle 0.580。
- P1−P0: +0.34/+0.41/+0.27; P3−P0: +0.40/+0.41/+0.30; P2−P0 ≈ 0 (overall)。
- EN: v1 ~0 → v2-P3 0.31/0.22/0.04/0.38 (glm/ds/6.8/bp); P2-EN ≈ 0 全员。
- Panel: κ=0.56, exact-5 20/72, 11 一致 reject, R4 待 21 条。

## 三、待 Owner (按优先级)
1. **R4 resume** (21 条, daily reset 后; 同 ns resume 即可) → 重跑 consensus → 若变更新 screen。
2. **人工 12 条** (~30min): A005/A006/A014/A018/A020/A022/A027/A028/A032/A035/A041 + A065。
3. **E3 温度** (glm P3 同 30 IDs, 60 calls, 随时可插; zc-free 不可测, 仅 direct)。
4. **人类盲审** (外部三语人 3–4h; panel 永不能替代)。
5. **key 轮换** (提交后; 清单: 四控制台 revoke → 新 key 只写本地 `.env` → 旧 key 验 401; r4 可先行)。
6. nach 仓 (46 paths, deadline 后单独收敛; 主仓 pitch 自包含已验)。

## 四、禁区重申
不改 tests/ 逻辑; freeze/ 只读; 禁 add -A; key 永不打印/入库; paper 本轮零动 (v2 只进 REPORT+evidence, 不混 instrument);
`research/mimo_spark_audit/` 不动; 8 月 LDS 历史不动; 新 conversation 先读本文件 + REPORT §7 + PANEL_SCREEN.md。
