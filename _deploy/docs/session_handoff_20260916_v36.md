# Session Handoff v36 — 失败重跑轮（2026-09-16）

pytest 84 绿。Key：`.env` 未跟踪（DASHSCOPE_API_KEY→BAILIAN_API_KEY 内存映射，无落盘）。

## Phase 0 探针

- P0-a ds-pro：单发最小文件 → **403 配额墙仍在**，53 项全 HOLD。
- P0-b v41：单发 zh 小文件 → **FILED**（c=22 r=25），通道开 → Phase 2 放行。
- P0-c dnr3：盘内无 runner log；manifest 自证（genuine_failed_hint=[]＋quota_note 明记窗口失败系配额拒收）
  → 判 quota 误标，转 Phase 1 池（待配额恢复；维持 dnr 标记不动，解冻须配额恢复后）。

## Phase 1 ds-pro：HOLD（403），零调用零改动。

## Phase 2 v41：batch breadth 28 → filed 15＋audit-fail 13＋quota-STOP 1（en_probability 未尝试）

- 落盘 16（含探针 1）：done 81→97；13 audit-fail（mojibake `???`/`?�`＋refs 未闭合）回 missing（各剩 1 次重试，待配额恢复）；
  dnr3（fischer r2/lambacher r3/ch3 r3）未动。
- 事故：首 commit 误卷并行组已暂存文件（28 files）→ 已 `reset --soft + reset` 抢救，
  重提纯 v41 17 文件（`a49a424`）；并行组文件 zero-touch 退回工作区。
- 教训：以后每次 commit 前 `git diff --cached --name-only` 核对归属（并行组活跃期）。

## Phase 3 双姝：max wahrsch.r3＋kimi en_ap.r3 各单发 600s → 均 403

- 结论：维持 permanent absent（死因由传输转配额确认）；manifest 零触碰（stale 守卫拒写已验）。
- 口径统一：引用 manifest（max 4x / kimi 2x）；verdict 旧注（3败/2败）加脚注待改。

## 当前钥匙状态

- 本轮 v41 batch 约 30 calls 后 key 级配额耗尽（v41 尾＋max＋kimi 连续 403）；
  下一轮（13 重试＋en_probability＋ds 53）须等配额恢复或注资。
