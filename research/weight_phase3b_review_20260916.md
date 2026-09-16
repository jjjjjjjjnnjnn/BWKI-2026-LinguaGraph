# Phase-3b 脏树冻结 + 提交同步 + 终审（2026-09-16）

> 范围：实际脏树 1 modified + 89 untracked（与任务描述 18 modified / ~105 untracked 不符，以实测为准，不编造）。
> 红线：未 commit / 未 push / 未打 tag（仅备好待提交清单）；未改 `tests/` 断言；未改 `submission/idea` 历史；未编造 177 口径。
> 状态：测量沿用上游报告；本文件只做冻结裁决 + 提交同步 + 门禁 + 红队，不新增数据/语料/指标。

## 1. 回滚 / 登记决策（脏树裁决）

- 实测（`git status -uall`）：`M cognitive-space/portal/index.html`（+23/-0，4 处 honesty/provenance 注记 + 5 新键 × EN/DE/ZH 15 字典项）1 文件；untracked 89 = `bailian_audit` 68 + `mimo_spark_audit` 13 + weight 线 6（`weight_lmstudio_models`、`weight_vs_human_E3`、`weight_vectors` ×2、`weight_phase3a_review`、附录 W 归 paper 侧）+ `scripts/tools/weight_graph_E1b.py`、`weight_graph_E3.py` + `docs/paper/08_appendixW_weight_vs_human.md`。
- 任务描述的“data 11 + paper 5 + portal 2 = 18 modified”在实测中**不存在**：`git diff --stat` 跟踪改动仅 portal 1 文件；`data/`、`docs/paper/`（已跟踪部分）零改动。因此**不执行 `git checkout` 回滚**（无回滚对象；盲目 checkout 只会丢弃有意的 honesty 注记），也不需要 `_archive/` 备份（无丢工作风险）。书面记录在此。
- Portal 改动逐 hunk review：4 hunks（method_prov 注 / F12 注 / limitations 模型来源卡 / validation 设计执行拆分 + 三语字典）均为 Phase-3a 已评审口径（附录 W 残余风险①–⑥、设计 phi vs 执行 Spark、Two-Tier nomic-only 不受影响），无结论升级、无数字改动 → 裁决**有意基线，予以暂存**（staged，未 commit）。
- 瞬态记录：本轮初 `git status` 曾见 `index.html.bak-20260916` + `session_handoff_20260916_v33.md`，终检时已不在盘（并发进程产物，与 Phase-3a 记录的 `wiki_gloss_audit_30*` 瞬态同类）；未对其执行任何 archive/delete。

## 2. add / archive 清单（已执行，未 commit）

- `git add`（staged，10 文件，+1211/-2）：portal `index.html`（M）、`docs/paper/08_appendixW_weight_vs_human.md`、`research/weight_vs_human_E3_20260916.md`、`research/weight_lmstudio_models_20260916.json`、`scripts/tools/weight_graph_E1b.py`、`scripts/tools/weight_graph_E3.py`、`research/weight_phase3a_review_20260916.md`（引用清单：附录 W 逐字引用的上游 6 报告中 E3 正文此前 untracked，本轮补齐；E1b/E3 脚本补齐其 JSON 产物的生成端，消除“产物已入库、脚本悬空”）、`submission/final/README.md`、`code_einreichung.md`、`declaration_of_support.md`（§3 同步改动）。
- 刻意**未 add**：`weight_vectors_934x768_20260916.json` + `.term2vec.json`（各 ~15.8 MB，无 LFS，按 HEAD 附言作 release-attachment 处理，保持 untracked）；`research/bailian_audit/` 68 + `research/mimo_spark_audit/` 13（共 81，约 1.48 MB，批量入库前需先登记 manifest/ledger，保守 hold，不动）。
- Archive：本轮无可归档对象（`bailian_gold*/consensus*/prune_backup*` 在盘不存在；`data/lds_c` 0913/0914 已在 `34756ec`/`b64b807` 入库，无 untracked 残留；bak/handoff 瞬态已自消失）。未动 `submission/idea` 历史。

## 3. 提交物更新 diff（未 commit，staged）

- `submission/final/README.md`：Stand 行加 Phase-3b 附注（附录 W exploratory 且不在 PDF、设计执行拆分指针、177 未验证不采用）；F12 行保留 59/54 + file truth 62/57/186 并注明 177 不采用；新增 W 附录行；Zahlen 节加 manifest guard 实测行；PDF 行注明 ORDER 仅核心章、附录 W 未入。
- `submission/final/code_einreichung.md`：新增 Schritt 5（weight 线复现：`weight_graph_audit/E1b/E3.py` + numpy-only 真实登记——任务提示的 torch/transformers 在此三脚本不适用，已书面纠正；LM Studio nomic 端点 + UNVERIFIED；向量 untracked 非 LFS；输出清单 + Hypothesis/PENDING 封顶）。
- `submission/final/declaration_of_support.md`：§1 追加设计态/执行态判官拆分段（设计 phi-4-mini-instruct 开源快照 vs 执行 muse-spark-1.3-contributor 闭源 10 判官 407 结果；Two-Tier nomic-only 不受影响；引 §2.12 + App. W）。
- 附录 W 与 PDF：`scripts/build_paper_pdf.py` ORDER 为 9 核心章 + declaration 附录，**不含** `08_appendixW_weight_vs_human.md` → 未入 PDF 的原因是“exploratory appendix-only 按设计排除”，非遗漏；本轮未改 ORDER（冻结构建）。

## 4. 门禁结果（2026-09-16 实测）

- `python -m pytest tests/ -q`：**84 passed**（39.12s，复核）。
- `docs/paper` 内 `arXiv:` = **18**（与基线一致；附录 W + 提交物新增零引入）。
- `manifest.json` guard：**556 / 525 / 219**（total_nodes / total_relations / aligned_groups，与 SSOT 一致）。
- 禁语扫描（变更范围 8 文件：3 提交物 + 附录 W + E3 + lmstudio JSON + E1b/E3 脚本）：**零命中**（portal 全文件既有命中为本轮之前 `finding_c/limitations/val` 旧键，不触碰）。
- forbidden-numbers guard：README 内裸 `177` 仅 2 处且均为守卫措辞（“unverifiziert — nicht übernommen”）；附录 W 内 `177` 为 SHA `177ca4b8…` 前缀，非计数断言；59/54 + file-truth 62/57/186 口径未动；556/525/219、0.519/0.934/0.938 未改。

## 5. 红队 5 攻 5 防（攻击 → 防御 → 修复，均已落地）

| # | 红队攻击 | 防御 / 证据 | 修复 | 裁决 |
|---|---|---|---|---|
| B1 | 冻结完整性：E1b/E3 JSON 已入库但生成脚本悬空（untracked），复现链断裂 | `git ls-files` 显示 JSON 在库、脚本不在库；附录 W/E3 引用脚本路径悬空于 git 视角 | 本轮 `git add` 两脚本（staged），产物-脚本配对恢复 | 防御成立 |
| B2 | 提交一致性：README 59/54 与 file truth 62/57/186 打架，或 177 被扶正为事实 | README 三数并列且 F12 行明示 file truth；177 仅以“未验证不采用”出现，code/declaration 无 177 | 措辞已按守卫口径书写，无事实化 177 | 防御成立 |
| B3 | 回滚风险：误把有意 honesty 注记当“未冻结重跑”checkout，导致丢工作 | `git diff` 逐 hunk 证明 4 处均为 provenance/design-split 注记，无 data/paper 重跑痕迹；data 零改动 | 不执行 checkout，不备份（无丢风险），书面记录 | 防御成立 |
| B4 | 引用悬空：附录 W 引 E3 正文 / 快照 / §2.12，提交物引附录 W，链中任一不存在 | 附录 W 引用的 6 上游报告 + 快照 + §2.12 行均存在；E3 正文此前 untracked 本轮已 staged；`build_paper_pdf` ORDER 不含 W 已在 README/declaration 注明原因 | E3 正文 staged；PDF 排除原因书面化，无悬空 | 防御成立 |
| B5 | 禁令渗入 + 体积炸弹：新增措辞命中禁语，或 31 MB 向量 / 81 审计 JSON 被顺手入库 | 变更范围禁语零命中；向量 2×15.8 MB 明确排除（release-attachment）；81 审计 JSON hold（需先登记 manifest/ledger） | 未入库体积物；审计批量入库降为 P1 待办 | 防御成立 |

## 6. 待用户下令事项（本轮均未执行）

1. `git commit`（staged 10 文件 + 本文件待 add）：提交信息与是否合并且无 audit 向量由用户定。2. `git push` / tag：禁止擅动，等明确指令。3. 81 审计 JSON（bailian 68 + mimo_spark 13）是否入库：需先补 manifest 登记 + BASELINE_LEDGER 条目再定。4. 向量 2 文件是否发 release-attachment：需用户确认渠道。5. `177` 口径如有新证据需转正：先验 file-truth 62/57/186 差值来源再改 README。6. PDF 是否需要附录 W 版 ORDER：当前冻结为不含 W；如需出附录版 PDF 则另起构建指令。
