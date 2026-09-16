# 脏树合规台账（2026-09-16）

## 处置结论

| 项 | 归属 | 处置 |
|---|---|---|
| `submission/final/code_einreichung.md` +10（Weight Step5） | 并行组 | 留置不碰，待其自提交 |
| `submission/final/declaration_of_support.md` +2（Design-vs-Exec Richter） | 并行组 | 留置不碰，待其自提交 |
| vectors 2×15.8MB＋bailian 68＋mimo 13 | 本线 HELD 策略 | `.gitignore` 已加规则（L69–72），`add -A` 误收机制性消除 |
| `.env` | 本地密钥 | 未跟踪＋已忽略（L9），密钥形状全仓零命中（`sk-[A-Za-z0-9]{16,}` 0，其它 provider 形状 0；23 旧 `sk-` 均为 task-/desk- 类误命中） |

## 规则（常设）

1. 禁 `add -A` / `add .` / `commit -a`（并行活跃期）；逐路径 add＋`diff --cached --name-only` 核对归属；
2. push 只认 HEAD，不认工作区；脏树留置须在每次 handoff 登记；
3. 新大文件（>1MB）入库前评估 LFS/Release；密钥只走内存 env，禁落盘。
