# Weight Phase 4 — 人类侧升级记账（2026-09-16，人类门控）

> Phase 1–3 已闭环（测量 EXECUTED / 解释 Hypothesis）。本 Phase 须人类到场，agent 不可执行。

## Ph1（已闭环）

- E1b/E3 比特级可复现（rerun 零 diff）；aligned_data.json SHA a663c2c0…✓；
  vectors 双 SHA ✓（与 snapshot 一致）；Release 已传
  `data-weight-vectors-20260916`，LEDGER 已回填 URL。

## Ph2（已闭环）

- N=200 repeats：k=5 ρ 0.74±0.24（[0.5,1.0]）、k=10 0.76±0.24、k=15 0.70±0.28（[-1,1]）；
  EN 对序 ~50/50 翻转，zh-de 首位稳定。结论：**单次 draw ρ 值无解读价值**（含 E3 报告的 k=15 ρ=0.866），
  只许分布陈述。threshold 对照已产出（见 `research/weight_e3_repeats_20260916.json`）。
- 末行重算＋密度 adjudication：记账待 E3-full 独立复核（E3 报告既有 MISMATCH 声明维持）。

## Ph3（已闭环）

- 线性 CKA（shared gid n=199）：zh-de 0.4251 ＞ zh-en 0.3057 ＞ de-en 0.2831——与 LDS-K 序同向（独立方法分布级收敛，描述性）。
- RSA（embedding 距离 vs 教科书图距离，19701 对）：zh 0.17 / en 0.02 / de 0.07——几乎不跟踪，支持 Two-Tier"测不同东西"。
- 去污对照：T1 剥离已在 E1b gid 层执行；改写/频次 PENDING 维持。

## Ph4（待人类）

1. N=30 问卷（86% power）＋72 盲审二评闭环后，人类图重算 LDS-C，与向量图再比；
2. 在此之前人类侧维持 pilot＋Developing；向量侧解释维持 Hypothesis/PENDING，不升 Developing。
