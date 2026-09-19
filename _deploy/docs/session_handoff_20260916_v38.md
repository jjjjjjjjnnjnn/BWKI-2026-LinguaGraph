# Session Handoff v38 — weight 线收官（2026-09-16）

门禁：pytest 84 / numbers-gate PASS。

## 归档（9＋2）

- E3 报告＋E1b/E3 脚本＋附录 W＋phase3a/b＋lmstudio models＋E1b/E3 图更新已入库（评审：Hypothesis 封顶＋红线声明）。

## 实验 Ph1–Ph3（全量）

- Ph1：E1b/E3 比特级可复现；aligned SHA✓；vectors 双 SHA✓。
- Ph2：N=200 repeats——单次 draw ρ 无解读价值（EN 序 ~50/50 翻转，k=15 甚至出现 -1.0）；
  threshold 对照已产出。E3 报告 k=15 ρ=0.866 降为 draw 伪影，禁引用。
- Ph3：线性 CKA zh-de 0.4251＞zh-en 0.3057＞de-en 0.2831（与 LDS-K 同向，独立方法收敛，描述性）；
  RSA 0.17/0.02/0.07（几乎不跟踪，支持 Two-Tier 分层）。
- 解释维持 Hypothesis/PENDING，不升 Developing。

## Release＋Ph4

- vectors 已传 Release `data-weight-vectors-20260916`（仓库内保持 HELD），URL 回填 LEDGER。
- Ph4 人类门控记账（`research/weight_phase4_ledger_20260916.md`）：N=30＋72 二评闭环后重算。
