# Portal Audit — 论文级连贯改版（2026-09-16）

## 1. Rubric 打分

| 维度 | 标准 | 结果 |
|---|---|---|
| 连贯 | paper 章节↔门户区 1:1（章级）：Motivation→hero / Methodik→methodology+Lab1 / Ergebnisse→findings+Lab2 / Einschränkungen→limitations+Lab3 / Kernbeitrag→paper区 | GO（注：H3 级 1:1 故意不做——门户是摘要层，细节点 PDF；story 删除后 F1–F12 明细仅 PDF 承载，已在 paper 区明示） |
| 可懂 | 三实验室 JS 零错＋i18n 128/128/128 同步＋5 分钟走完 | 机审 GO；5 分钟人工体验待用户走一遍 |
| 严谨 | B≤8 反转修复、DE 0.934→0.933×4、roster 26 含 qwen 注、m5 去算术化、ZH:127 英文残留修；numbers-gate PASS；banned 全仓 0（labs 新文件已扫） | GO |
| 简洁 | index 656≤900 行；labs 50/78/73≤130；字典 117→128 键（+11≤35）；删除 9 文件（3 展厅＋story＋5 deploy 镜像＋1 空目录） | GO |

## 2. 删除清单（3D 主图保留）

`web/cds-terrain.html, coverage-towers.html, margin-galaxy.html, web/story/index.html`＋`_deploy` 对应 5 件。历史引用保留（v1 归档/CHANGELOG/SSOT-web/forensic/submission 冻结件）；live 引用全改（cspace 三卡→三 labs，portal README 镜像表，根 README 三语 portal 行 F1–F12/margin galaxy→A–E/mini labs）。

## 3. 附带修补（机审发现）

- cspace.html 漏网 stale：STEAM 839→834、math 525/238→517/233（含 scope×2、body 默认文本×2），三语。
- 根 README 三语 portal 行：F1–F12→A–E、margin galaxy→mini labs。

## 4. 残余项

- 5 分钟人工走查（用户）。
- H1/H3 人类项不受影响；v1.0 仍 block（原判不变）。
