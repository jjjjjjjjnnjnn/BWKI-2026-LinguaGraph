# Phase-3a 集成红队评审（2026-09-16）

> 范围：`docs/paper/02_methodology.md` §2.12 三句、新建 `docs/paper/08_appendixW_weight_vs_human.md`、
> `cognitive-space/portal/index.html` 四处（methodology 脚注 / F12 注 / limitations 模型来源卡 / validation 设计执行拆分）
> + EN/DE/ZH i18n 键（5 新键 × 3 语言）、本文件。
> 红线：未动 `tests/`、`freeze/`、`_deploy/`、db、data 既有、`submission/` 历史。

## 1. 五攻五防（攻击 → 防御 → 修复，均已落地）

| # | 红队攻击 | 防御 / 证据 | 修复 | 裁决 |
|---|---|---|---|---|
| A1 | 结论升级：附录 W 或 Portal 新增表述被读作第 4 结论，或把 Hypothesis 抬到 Developing | 全文件头注 appendix-only + Hypothesis 封顶；W.6 显式声明 `00_three_conclusions.md` 结论数保持 3；Portal 新增均为 honesty/provenance 注记，不带结论动词 | W 头注 + W.6 + Portal 注记措辞已按封顶口径书写，无升级句残留 | 防御成立 |
| A2 | 三语不同步：HTML `data-i18n` 无字典对应，或某语言缺键导致回退英文 | 5 新键 × EN/DE/ZH = 15 字典项；含 4 处 HTML 共 20 行全命中（`method_prov_note`/`f12_prov_note`/`limit7_prov_title`/`limit7_prov_desc`/`valid_design_exec`）；`setLanguage` 的 `data-i18n` 通用回退已覆盖新增键 | 15 字典项一次补齐，三语逐行复核 | 防御成立 |
| A3 | 数字口径 SSOT 冲突：新增数字与冻结源不一致（556/525/219、0.0445/0.419、0.519/0.934/0.938、238 边、SHA 截断、n=3、6 风险） | 逐数回查：Two-Tier §2–§3、E1 §2、E1b §2、E3 §2、快照 JSON（SHA 全值在 JSON 内，正文仅截断显示）；密度 7.8×/平均度 2.8× 与 E3 JSON 一致 | 核对一致，未改任何数字 | 防御成立 |
| A4 | 引用失效：新增引用指向不存在的快照/附录/章节/报告 | 逐链验证可达：`research/weight_snapshot_20260916.json` 存在；附录 W 本轮新建存在；§2.12（行 232）存在；上游六报告（audit/E1/E1b/E3/logic/provenance）存在 | 全链可达，零悬空引用 | 防御成立 |
| A5 | 禁语渗入 + 文献计数破坏：新增措辞命中禁语表 5 项，或新增文献标记破坏 `arXiv:` 计数 | 新增范围扫描：Portal 20 行逐行 Clean；附录 W 零命中；§2.12 三句零命中；`docs/paper` 内文献标记计数 = 18（与基线一致，docs/paper 新增条目零引入该标记） | 相关表述已改写规避（如以“标签过滤/未锁定版本/残余风险”措辞替代），无需二次修复 | 防御成立 |
| A6 | 红线触碰：改动波及 `tests/freeze/_deploy/db/data` 或 `submission/` 历史 | `git diff --stat` 跟踪改动仅 Portal 1 文件（+23 行）；新建仅附录 W + 本文件；`git status` 无红线目录改动记录 | 无修复事项 | 防御成立 |

## 2. 门禁结果（2026-09-16 实测）

- `python3 -m pytest tests/ -q`：**84 passed**（151.37s）。
- 文献标记计数：`docs/paper` 内 `arXiv:` = **18** 处（全部位于 `02_related_work.md` 既有条目；附录 W 与 Portal 新增零引入）。
- `git diff --stat`（跟踪文件）：`cognitive-space/portal/index.html | 23 +++++++++++++++++++++++`（1 文件 +23 行）；另有 2 个新建文件（附录 W、本文件）位于 untracked；其余 untracked 均为本轮之前已存在的 Lane 产物与数据文件，非本轮写入。
- 禁语扫描（新增范围：§2.12 三句 + 附录 W 全文 + Portal 新增 20 行 + 本文件）：**零命中**（断言成立；Portal 全文件既有 8 处命中均为本轮之前既有键 `finding_c_*`/`val_*`/`small_qwen`/`curr_nrw_desc`，不在本轮范围，不触碰）。
- `00_three_conclusions.md`：未修改，结论数保持 3。

## 3. 特殊记录

- §2.12 三句（HF 今日头非实验 pin + served UNVERIFIED + 社区量化不可对 hash，引 `weight_snapshot_20260916.json`）经核查在 HEAD（`f21cebb` 系谱）已存在，本轮复核内容一致，未重复插入、无重复文本。
- Portal 新增 4 处 i18n 键在 EN/DE/ZH 三字典均已同步；`index.html.bak-20260916` 为本轮之前已存在的备份文件，未触碰。
- 瞬态记录：门禁期间曾观察到 `research/wiki_gloss_audit_30*.json` 短时出现在 `git status` 改动列表（09:57，并发进程写入，非本轮操作）；终检时 `git diff --numstat` 已确认跟踪改动仅剩 Portal 1 文件（+23/−0），该瞬态改动未残留、本轮未写入该二文件。
- 本文件所有新统计口径沿用上游报告，不新增数据/语料/指标；引用附录 W 残余风险 ①–⑥ 时须附带全文。
