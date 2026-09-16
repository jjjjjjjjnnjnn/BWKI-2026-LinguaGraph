# Headline 数字复现核查 20260916 / Headline-number reproduction check

- 脚本 Script: `scripts/tools/reproduce_headline.py`（独立重算，不引 numbers_audit 逻辑）
- 输出 Output: `research/reproduce_headline_20260916.json`（28 项，per-item: claim / recomputed / match）
- 运行 Run: `python scripts/tools/reproduce_headline.py` → **PASS (28/28)**
- 门控 Gate: `python scripts/tools/numbers_audit.py` → **NUMBERS_GATE PASS**

## 结果 Result: PASS，无 mismatch / no mismatches

按 stop-line 政策：mismatch 才阻塞并留待后传修复；本次零差异，无需修复项。

## 核查项 Items（claim vs recomputed，全 match）

图谱 Graph（manifest 556 / 517 / 219，233 links）:
- nodes_556 = 556（visualization_data 实际数组；manifest.graph.total_nodes 与 snapshot 一致）
- relations_517 = 517（aligned_data 数组与 total 字段；merged_relations.total；snapshot；manifest 一致）
- groups_219 = 219（aligned_data 数组与 total_aligned_groups；snapshot；manifest 一致）
- links_233 = 233（visualization_data 实际数组；manifest.graph.total_links；snapshot 一致）

Viewer（cognitive-space/web/data.js）:
- header / metadata / 实际数组均为 556 nodes / 233 links

LDS-K Tier-1（由 aligned_data.json 经 _lds_utils 独立重算，保留 3 位）:
- zh_en 0.933 / de_en 0.938 / zh_de 0.519 / spread 0.419（0.938−0.519）

复现 Replication（multi_model_replication_20260913.json；formal 集规则：n==30 且 ZH-DE p<0.05 且 margin 非 NaN）:
- 公开口径 published 59 measurements / 54 models / 177 tests（54 = 去重身份，5 dual-host）
- 文件真值 file-truth 62 / 57 / 186（含 qwen-max n=26 部分运行 + 2 稀疏小模型边界运行）
- en_ns 9/177；strata cn 48/48，west 11/11，west_ohne_luna 10/10
- dedup 54/54，margin 均值 0.137（按文件顺序首见去重）；youden 0.12（中位二分最优阈值，确定性部分）

STEAM（cognitive-space/web/data_steam.js 实际数组）:
- 1143 nodes / 834 edges；分量加总一致（math 556/233 + physics 367/386 + chemistry 220/215）

## 备注 Notes（非 headline，不计入判定）

- merge_report.txt 记 Concepts merged 557：为 prune 前合流数，渲染前去重后 556（visualization/manifest/data.js 一致）；relations 517 与 headline 一致。
- weight_vectors_sha_20260916.json 仅作参照，未触碰向量；Tier-2 未纳入 headline 核查。
