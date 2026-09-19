# PROJECT SEAL — 封盘 (2026-09-19)

HEAD: `b7b17f3` (seal commit;封盘基线 `4f95ed3` + 本文件). 远端同步 (含 tag `seal-2026-09-19` → `b7b17f3`). 门禁: numbers PASS / cdn PASS / pytest 84/84.
本文件 + `docs/session_handoff_20260919_v47.md` 为最终状态说明. **封盘≠发布**: 无 GitHub Release.

## 一、完成 (证据链闭合)
- v1 seed-fremd 复制 (6 臂, T1 11 + T2 92) + v2 因子实验 (P1/P2/P3/P3b × 3 锚 + big-pickle 描述性) + E2 ROBUST.
- 判定: F1 CARD confirmed / F2 LANG model-side failure / P3 (deepseek validated, glm drift-caveat, 6.8 marginal miss) / panel MAINTAIN (echte Gold-vs-Rater-Divergenz: Rater-Jaccard 0.44–0.77, vs-gold 0.389; D-V9 Bugfix) + 11/72 一致 reject.
- Claims: C21 v2-partial-repro / C23 gehärtet / C24 neu (Hypothese) / C9b Developing (不动).
- 门户改写式更新 (三语) + Fig v2-cells + _deploy 同步 (1A09 fork 已消除).
- 论文 §2.8/§2.9b/05 定量补齐; 分母纪律 (A2 vs valid-only) 全仓诚实标注.

## 二、Parked (Owner 明确不做, 非待办)
1. R4 panel 21 条: R4 保持 56 records (51 judged). 共识结论基于 partial-R4; 11 一致 reject 含 R4 票, 不受影响.
2. 人工 12 条 spot-check: 未做. Panel 维持"弱证据 maintain".
3. 人类外部盲审: 未做. Panel 永不能替代人类盲审 (A-Judge J7).
4. Key 轮换: **未做 — 唯一遗留风险**. 4 串 key (zen/OpenCode, MiniMax, r4, sensenova + OpenRouter 免费) 仍有效,
   散见于本机聊天记录; 仓库内零入库 (已验证, 仅变量名). 若未来任何 key 异常扣费 → 第一动作: 进对应控制台 revoke.
   新 key 永远只写本地 `.env`, 不经聊天.
5. nach 仓 (46 paths): deadline 后单独收敛, 主仓 pitch 自包含.
6. stash@{0} (WIP on 0bcae32): 封盘时已 drop (早被后续提交 supersede, 留着是雷).

## 三、已知 caveats (读数时必须同时读)
- glm P3 0.544 带 serving-drift caveat (+0.32 P0cal); deepseek/6.8 drift≈0.
- 6.8 P3 0.395 marginal miss (0.40 线下, 未四舍五入).
- R2 (glm) 作 judge 超严 (36 rejects, 14 solo) = rater 噪声, 已 dissent 分析.
- big-pickle 全系描述性 (P0 partial-46, CORE 外, E1-gate 无 claim).
- ZH-EN 显示 0.933 (SSOT Re-Freeze 0.9330, 2026-09-16); Fig8-Snapshot (2026-09-12) zeigt 0.9336 — δ im Rundungsband, s. D-V10.

## 四、重启条件 (任一满足, 按 v44–v47 接回)
R4 配额恢复 / 有 30 分钟人力 (spot-check) / 有三语人力 (盲审) / 做 key 轮换.
入口: 本文件 → v47 → REPORT §7/§8 → PANEL_SCREEN.md.

## 五、Post-seal Errata (Tiefenaudit 2026-09-19, D-V9/D-V10)
- D-V9 (`panel_consensus.py` Typo): alte Jaccard-Tabelle 0.06–0.28 falsch; neu 0.44–0.77.
  Deutung „Rater-Rauschen → weak-evidence maintain" ersetzt durch „echte Gold-Divergenz".
  MAINTAIN-Verdikt unberührt (kam aus IMPORT-Gates, nicht aus Jaccard).
- D-V10 (ZH-EN Flip-Flop): v46 schrieb 0.934 (alte Freeze-Basis 0.9336); korrekt per SSOT-Re-Freeze ist
  0.933 (Basis 0.9330). Portal/Labs/Evidence-C3/Paper-Prosa revertiert; Snapshot-Tabellen/Captions
  behalten 0.934 mit Snapshot-Label + Re-Freeze-Hinweis.
- Historische Handoffs (v43–v46) bleiben timestamped Snapshots; obige Errata + v43 A2-Korrekturen (v45),
  v44 P3-EN-deepseek 0.22→0.21, §2.9b Sozial-A2-Portion sind die maßgeblichen Korrekturen.
- Tag `seal-2026-09-19` zeigt auf `b7b17f3` (Seal-Zustand); Errata-Commits folgen nach (ohne neuen Tag).
- Post-seal Portal-Fixes (Tiefenaudit Portal 2026-09-19): `_deploy/favicon.svg` nachgereicht (Root-断链);
  `figKeys`-Index-Mapping entfernt (7 `.fig-label` laufen über `data-i18n`, 12 tote Caption-Zeilen raus);
  en-`finding_c_sub` entdeutscht; 15 Orphan-i18n-Zeilen raus; Methodology-`<h2>` mit `data-i18n`.
- Post-seal Portal-Runde 2: L7-Provenance-Card (UNVERIFIED/Restrisiken-Draft) entfernt → Carousel 3 Slides
  (Dots/Count auto, g4-Hash geclampt); `method_prov_note` formal (19-Modell-Benchmark, qwen-plus);
  Mermaid-EXT (MIMO→19-model benchmarked, 3-sprachig); Carousel-minHeight folgt aktivem Slide
  (+Resize-Dispatch bei Sprachwechsel); 24 Orphan-i18n-Zeilen raus.
