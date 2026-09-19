# Session Handoff v46 — Portal + Paper v2/Panel Update (2026-09-19)

基线: portal 源码 C71D4FFD…C9EF8 (2026-09-18); 同步后源码=_deploy/portal 7B60E8ED…BA6B;
_deploy/index.html 旧 fork (1A09, 内容 180-textbook 旧版) 已重建为源码去 `../` 版 7B66F7… (19 引用 1:1 验证, CRLF 保留)。
门禁: numbers PASS / cdn PASS / pytest 84/84。

## 一、门户改写式更新 (cognitive-space/portal/index.html + labs, 三语 i18n 全镜像)
- contrib1/bench-note/gold-row/gold-desc/limitations: `harness ~0.65 / blind pending` →
  harness-v2 P3 0.40–0.58 (CARD-confirmed, LANG model-side) + panel MAINTAIN (11/72 一致 reject, 人工待补)。
- ZH-EN 0.933→**0.934** 全仓显示位 (portal 主+i18n×3+labs×3; 精确 0.9336/0,9336 原样保留)。
- labs/limits L6 三语 + reproduce/counterex 冻结三元组同步。
- 新增 Fig v2-cells 引用块 (gold 卡后) + figBases 注册 (三语 caption 键 method_figv2)。

## 二、新图 (零 API, 读 V2_MATRIX.json)
- `scripts/figures/fig_v2_cells.py` (YaHei 修 tofu, 惯例同 fig8) →
  `outputs/figures/fig_v2_cells{,_de,_zh}.png` → 镜像 cognitive-space/figures + web/figures + _deploy/figures。
  内容: (a) social-F1 P0/P1/P2/P3 ×3 锚 + big-pickle P3*; (b) EN-F1 同布局; caption 含 A2/drift-caveat/来源。

## 三、论文 (docs/paper, 只加不改旧结论)
- 02_methodology §2.8 †: panel 定量 (15/72, 0.389, κ0.56, 11 一致) + harness-v2 区间替代 ~0.65。
- 新 §2.9b Harness v2 (F1/F2/P3/E2/分母纪律/Claims C21-C24/C9b 不动/新图引用)。
- 05_conclusion 金标局限句补 panel 定量。
- 溯源: social-EN 16/21 + 21/21 由 gold+run 文件复算 belegt; Sozial-only 表加 valid-only/A2 注。

## 四、发布同步
- _deploy/portal/index.html + labs×3 = 源码 byte-identical; _deploy/index.html = 去 `../` 派生;
  _deploy/docs/evidence_register.md = docs 版; 新图三处镜像。
- 旧 1A09 fork 差异根因: 内容旧 (180 vs 204) + 路径适配; 现已消除, 以源码为准。

## 五、parked (不变)
R4 21 条 / 人工 12 条 / 人类盲审 / key 轮换 / stash@{0} / nach 仓。
