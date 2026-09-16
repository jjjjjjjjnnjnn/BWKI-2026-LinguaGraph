# Weight vs Human Provenance 附表：nomic-embed-text-v1.5 + phi-4-mini-instruct 开源可证性（2026-09-16）

> Lane-2 产物 · 只新增本文件，不改 `data/`、`freeze/`、`_deploy/`、`db`、`tests/`。
> 原则：查不到写 UNVERIFIED，不编造 hash / 日期。本地 LM Studio 当时离线（`GET /v1/models` 连接拒绝），以脚本记录 + 磁盘快照为准。

## 0. 设计态 vs 执行态（一句话）

- **设计态（A路线单机）**：nomic 预筛 top-5 + `phi-4-mini-instruct` 判官（`scripts/semantic_ground_en.py:18-20`，`research/tier2_emb_baseline.md §3`）。
- **执行态（实际合并件）**：nomic 预筛 top-5 + `muse-spark-1.3-contributor` 10 并行判官（`scripts/merge_sem_verdicts.py:22-26` OUT `method` 字段实测确认，见 §3）。
- **Two-Tier 向量报告**（`research/two_tier_benchmark_20260914.md`）只用 nomic 嵌入（768 维，934 词条，434 主对），**不受判官替换影响**。

## 1. 模型卡表

| # | 名称（脚本内名） | HF URL | revision / sha（HF API 当前 `main` 头） | license | cutoff / 训练期 / 发布 | 参数 / 维度 | 训练数据披露 | 本地快照（2026-09-16 实测） |
|---|---|---|---|---|---|---|---|---|
| E1 | `text-embedding-nomic-embed-text-v1.5`（`openweight_embed_audit.py:46`，`semantic_ground_en.py:19`） | https://huggingface.co/nomic-ai/nomic-embed-text-v1.5 | `e9b6763023c676ca8431644204f50c2b100d9aab`（`https://huggingface.co/api/models/nomic-ai/nomic-embed-text-v1.5` 之 `sha`；`lastModified 2026-04-07T14:17:02Z`，`createdAt 2024-02-10T06:32:35Z`） | `apache-2.0`（HF 页面 + API 一致） | cutoff：**UNVERIFIED**（模型卡未声明 cutoff；为嵌入模型，不适用 LM cutoff 口径） | 137M（0.1B，F32；API `safetensors.parameters.F32=136731648`；HF 标注 0.1B）/ 本项目实测 `dim=768` | 技术报告 `2402.01613`（Nomic Embed）+ MRL `2205.13147`；训练数据**已披露**：`contrastors` 全量开源（https://github.com/nomic-ai/contrastors）+ Atlas 5M 样本可视化；两阶段管线（nomic-bert-2048 → 无监督对比 → 高质量微调） | LM Studio 服务名（脚本记录）：`text-embedding-nomic-embed-text-v1.5 @ http://127.0.0.1:1234/v1`；**磁盘未找到对应 GGUF**（`C:\Users\rongj\.lmstudio\models` 递归搜 `*nomic*` / `*embed*` 零命中；`hub/models` 仅 qwen 条目）；本地 hash：**待补（无本地文件可算）**；2026-09-16 实测 LM Studio 离线，`GET /v1/models` 连接拒绝 → 在线模型名** UNVERIFIED（以脚本记录为准）** |
| J1-设计 | `phi-4-mini-instruct`（`semantic_ground_en.py:20`，`temperature=0, max_tokens=5`） | https://huggingface.co/microsoft/Phi-4-mini-instruct | `cfbefacb99257ffa30c83adab238a50856ac3083`（`https://huggingface.co/api/models/microsoft/Phi-4-mini-instruct` 之 `sha`；`lastModified 2025-12-10T20:24:40Z`，`createdAt 2025-02-19T01:00:58Z`） | `mit`（HF 页面 + API 一致，LICENSE 在仓内） | **cutoff June 2024**（模型卡 Training/Model 节原文 "cutoff date of June 2024 for publicly available data"）；训练期 Nov–Dec 2024；发布 Feb 2025（与 `createdAt 2025-02-19` 一致）；上下文 128K | 3.8B（API `BF16=3836021760`；HF 标注 4B）/ dense decoder-only Transformer（phi3 架构，200K 词表，GQA，共享输入输出 embedding） | 技术报告 `2503.01743`（Phi-4-Mini Technical Report）；训练数据 5T tokens：过滤公开文档 + 高质量教育/代码 + 新造合成 textbook-like + 高质量 chat SFT；去污染流程有声明（n-gram 比对 + 污染报告）；细节见 `data_summary_card.md`（仓内） | `C:\Users\rongj\.lmstudio\models\MaziyarPanahi\Phi-4-mini-instruct-GGUF\Phi-4-mini-instruct.Q4_K_S.gguf`，**2337733952 bytes**，`LastWriteTime 2026-09-12 11:52:45`；sha256：**待补**（2.3GB 本次未算，禁编造）；社区量化版（MaziyarPanahi，非官方 Microsoft 仓）→ 与官方 safetensors 不可直接对 hash；2026-09-16 LM Studio 离线，在线加载态 UNVERIFIED |
| J1-执行 | `muse-spark-1.3-contributor`（实际判官，非开源权重） | UNVERIFIED（无 HF 页面；为 API 模型） | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | 证据：`config/expert_graphs/text_grounding_en_semantic_20260912.json` 之 `method = "nomic-embed-v1.5 prefilter (top-5) + muse-spark-1.3-contributor adjudication, 10 parallel judges; …"`（2026-09-16 实测复读）；`merge_sem_verdicts.py:22-26` 写入；`results=407` |

### 1.1 可作证项（本 Lane 能签字的）

1. **nomic-embed-text-v1.5 开源可证**：HF URL + 当前 `main` sha `e9b67630…` + `apache-2.0` + 技术报告 `2402.01613` + 训练数据 `contrastors` 全量披露。可作证"开权重嵌入对照基线"的模型身份；**不可作证本地 served 权重 hash**（磁盘无文件 + 服务离线）。
2. **phi-4-mini-instruct 开源可证（设计态）**：HF URL + 当前 `main` sha `cfbefacb…` + `mit` + **cutoff June 2024** + 发布 Feb 2025 + 技术报告 `2503.01743` + 5T 数据构成声明。可作证"设计态判官"的模型身份；**不可作证本地 GGUF 与官方权重一致**（社区量化版，hash 待补），且**执行态实际未使用 phi**（见 §3）。

## 2. 本地快照（2026-09-16 实测，不编造）

| 位置 | 内容 | 大小 / 时间 | sha256 | 说明 |
|---|---|---|---|---|
| `models/qwen2.5-0.5b-q4_k_m.gguf`（repo 内唯一 GGUF） | qwen2.5-0.5b | **491400032 bytes**，`2026-06-19 07:06:16` | 待补（本次未算，大文件禁编造） | 与 Tier-2 无关（Tier-2 用 LM Studio 侧 nomic+phi/Spark），仅记录以防混淆 |
| `C:\Users\rongj\.lmstudio\models\MaziyarPanahi\Phi-4-mini-instruct-GGUF\Phi-4-mini-instruct.Q4_K_S.gguf` | phi-4-mini 社区量化 | **2337733952 bytes**，`2026-09-12 11:52:45`（+ 同目录 `config.json`） | 待补（2.3GB 本次未算） | 设计态判官的本地候选；执行态未使用 |
| `C:\Users\rongj\.lmstudio\models` 递归搜 `*nomic*` / `*embed*` | 零命中 | — | — | nomic 本地权重不可定位；`hub/models` 仅 qwen 条目 |
| `llama/llama-cli.exe` + 3×`ggml-*.dll` | 本地 llama 侧车 | `llama-cli.exe` **9216 bytes**，`2026-06-19 03:34:38`；`--version` 无输出；`VersionInfo` 全空 | — | 版本 **UNVERIFIED**（9216 字节疑为 shim/stub，非完整 llama.cpp 二进制；dll：`ggml-base 763904` / `alderlake 1157120` / `haswell 1161728`） |
| LM Studio `GET /v1/models` | 离线 | `ConnectionRefused 127.0.0.1:1234`（2026-09-16） | — | 在线模型名、served revision 均 UNVERIFIED；脚本记录值见 §1 |

## 3. 设计态 vs 执行态证据链

- 设计态判官 = phi：`semantic_ground_en.py:18-20`（`EMB_MODEL` / `CHAT_MODEL`）、`sem_shards.py:2,16`（"parallel Spark judges" 分片注释与 embedding 预筛一致）、`tier2_emb_baseline.md §1/§3`（"A路线单机：nomic预筛 top-5 + phi-4-mini 判官"）。
- 执行态判官 = Spark：`merge_sem_verdicts.py:22-26` 写死 `method` 含 `muse-spark-1.3-contributor adjudication, 10 parallel judges`；OUT 文件 `config/expert_graphs/text_grounding_en_semantic_20260912.json` 实测 `method` 同文（2026-09-16 复读），`results=407`，`assert 407` 守卫无静默丢片。
- 影响面：`tier2_emb_baseline.md §2` 的计数验证（10615×768 / 407 / 165 hits / 10 shards）复用的是**已合并 Spark 件**，数字本身不受"设计态写法"影响；但**判官可证性口径必须写 Spark（闭源 API），不能写 phi（开权重）**。`two_tier_benchmark_20260914.md` 的向量窄带结论（极差 0.0445 vs 图谱 0.419）仅依赖 nomic 嵌入，不受影响。

## 4. 版本不可复现缺口清单（诚实版）

1. **HF `main` 头已漂移**：nomic `lastModified 2026-04-07`、phi `lastModified 2025-12-10` 均晚于实验（2026-09-12/14）。本表 sha 是**今日 API 头**，不是实验当日 pinned revision → 实验权重版本 UNVERIFIED，需写死 revision 才能复现。
2. **本地 served 权重无 hash**：nomic 磁盘无文件；phi 本地为社区 GGUF 且 sha256 待补；LM Studio 离线无法取 `GET /v1/models`。→ "跑的是哪个字节"不可证。
3. **LM Studio 转换层未知**：即使 HF sha 已知，LM Studio 侧的量化/归一化/`trust_remote_code` 行为无记录（nomic 要求 task-prefix；本项目概念词未加 `search_query:`/`clustering:` 前缀——口径如实，但与官方推荐用法差异需声明）。
4. **判官替换未在 baseline 报告正文声明**：`tier2_emb_baseline.md §3` 仍写 phi 为判官，执行态 Spark 只出现在 OUT `method` + `merge` 脚本 → 读者按文档会误以为开权重闭环。需在引用处加注（本表 §3 即该注）。
5. **llama 侧车版本未知**：`llama-cli.exe` 无版本输出，`models/*.gguf` 与 Tier-2 无关但同名易混（qwen2.5-0.5b）。
6. **nomic 无 cutoff 口径**：嵌入模型不声明知识截止；"cutoff"一栏只能写 UNVERIFIED/NA，不能借 phi 的 June 2024 冒充。

## 5. 补齐动作 checklist

- [ ] 启动 LM Studio 后记录 `GET /v1/models` 全文（含 served 模型名 + 后端版本），附到本表附录。
- [ ] 定位 nomic 本地权重文件（LM Studio 缓存路径），记录文件名 + bytes + `sha256`（`Get-FileHash -Algorithm SHA256`；大文件分块算，禁手填）。
- [ ] 对 `Phi-4-mini-instruct.Q4_K_S.gguf`（2337733952 bytes）补 `sha256` + 上游来源链接（MaziyarPanahi 具体 revision）。
- [ ] 在 HF 上为两个模型 pin 实验 revision（`?rev=<sha>` 可访问确认），把"实验 revision"与"今日 main 头"拆成两列；若旧 revision 已不可取，明确写 UNVERIFIED。
- [ ] 在 `tier2_emb_baseline.md` 引用处加注执行态判官为 Spark（**新文件注记，不改旧文件数字**；或在下游报告引用时声明）。
- [ ] `llama/llama-cli.exe` 确认是否为 stub；如是，记录真实 llama.cpp 版本来源（另行安装路径 + `llama-cli --version` 输出）。
- [ ] nomic 调用是否加 task-prefix（`clustering:`/`search_document:`）做一次敏感性说明（新实验，不动旧数）。

## 6. 复核命令（只读，不写盘）

```powershell
$env:PYTHONIOENCODING='utf-8'
python3 -c "import json; d=json.load(open('config/expert_graphs/text_grounding_en_semantic_20260912.json',encoding='utf-8')); print(d.get('method')); print(len(d['results']))"
Get-Item 'C:\Users\rongj\.lmstudio\models\MaziyarPanahi\Phi-4-mini-instruct-GGUF\Phi-4-mini-instruct.Q4_K_S.gguf' | Select-Object Name, Length, LastWriteTime
Get-ChildItem 'C:\Users\rongj\.lmstudio\models' -Recurse -Filter '*nomic*' | Select-Object FullName, Length
# sha（大文件，超时则标待补，不许编造）：
# Get-FileHash 'C:\Users\rongj\.lmstudio\models\MaziyarPanahi\Phi-4-mini-instruct-GGUF\Phi-4-mini-instruct.Q4_K_S.gguf' -Algorithm SHA256
```

## 7. 来源

- HF nomic 页（license apache-2.0、技术报告 2402.01613、contrastors、MRL 2205.13147）：https://huggingface.co/nomic-ai/nomic-embed-text-v1.5（2026-09-16 webfetch 实测）。
- HF phi 页（license mit、cutoff June 2024、训练 Nov–Dec 2024、发布 Feb 2025、技术报告 2503.01743）：https://huggingface.co/microsoft/Phi-4-mini-instruct（2026-09-16 webfetch 实测）。
- HF API（sha/时间戳）：`https://huggingface.co/api/models/nomic-ai/nomic-embed-text-v1.5`、`https://huggingface.co/api/models/microsoft/Phi-4-mini-instruct`（2026-09-16 实测）。
- 项目内：`research/two_tier_benchmark_20260914.md`、`research/tier2_emb_baseline.md`、`scripts/tools/openweight_embed_audit.py`、`scripts/semantic_ground_en.py`、`scripts/merge_sem_verdicts.py`、`scripts/sem_shards.py`。
- 机器可读快照：`research/weight_snapshot_20260916.json`（`checked_at 2026-09-16T06:58:00Z`；含本地sha256 + 在线模型列表 + 线上pin）。

## 8. §6 快照表（B线 2026-09-16 补测，不改上文数字）

> 设计态判官 = `phi-4-mini-instruct`（开源权重，本节快照对象）；执行态判官 = `muse-spark-1.3-contributor`（闭源 API，非本节对象，不混称）。

### 8.1 本地文件 sha256（流式实测）

| 文件 | 字节数 | mtime | sha256 | 说明 |
|---|---|---|---|---|
| `models/qwen2.5-0.5b-q4_k_m.gguf` | 491400032 | 2026-06-19 07:06:16 | `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db` | repo内唯一GGUF；与Tier-2无关，仅防混淆 |
| `C:\Users\rongj\.lmstudio\models\MaziyarPanahi\Phi-4-mini-instruct-GGUF\Phi-4-mini-instruct.Q4_K_S.gguf` | 2337733952 | 2026-09-12 11:52:45 | `5482cf4a772b948d8852d0b4d8541c5a07557e6b68d980c388f3f92bfddbc389` | 设计态判官本地候选；社区量化版，与官方safetensors不可直接对hash；执行态未用phi |
| `…\Phi-4-mini-instruct-GGUF\config.json` | 31 | 2026-09-12 11:36:19 | UNVERIFIED（未算，非权重） | 上游：https://huggingface.co/MaziyarPanahi/Phi-4-mini-instruct-GGUF |
| LM Studio其余7个GGUF（sauerkrautlm-8b/Qwen3-8B/Qwen3.5-9B×2/qwen2.5-0.5b/Hy-MT2-1.8B/gemma-3-270m） | 见json | 见json | UNVERIFIED（非Tier-2相关，未计算，不编造） | 详见 `weight_snapshot_20260916.json`之`lmstudio_models_other` |
| `C:\Users\rongj\.lmstudio\models`递归搜`*nomic*`/`*embed*` | 零命中 | — | — | nomic磁盘权重不可定位；`hub/models`仅qwen条目 |
| `llama/llama-cli.exe` | 9216 | 2026-06-19 03:34:38 | —（非权重hash对象） | `--version`无输出、退出码-1073741515、`VersionInfo`全空 → 版本UNVERIFIED；9216字节疑为shim/stub |

### 8.2 在线模型列表（本次在线，含时间戳）

- `GET http://127.0.0.1:1234/v1/models` 于 **2026-09-16T06:54:52Z** 成功（此前同日早前记录为离线，现状以本次为准）。
- `data[].id` = `text-embedding-nomic-embed-text-v1.5`、`phi-4-mini-instruct`、`hy-mt2-1.8b`、`gemma-3-270m-it`、`llama-3-sauerkrautlm-8b-instruct`、`qwen2.5-0.5b-instruct`、`qwen/qwen3-8b`、`qwen/qwen3.5-9b`（共8个）。
- `/v1/models`只给名不给revision → served revision仍UNVERIFIED（诚实声明）。

### 8.3 线上 pin（访问日期 2026-09-16，今日main头非实验pin）

| 模型 | main sha | license | 技术报告 | cutoff |
|---|---|---|---|---|
| nomic-ai/nomic-embed-text-v1.5 | `e9b6763023c676ca8431644204f50c2b100d9aab`（`lastModified 2026-04-07`） | apache-2.0 | 2402.01613 + MRL 2205.13147 | UNVERIFIED（嵌入模型无cutoff口径；模型卡未声明，不借phi冒充） |
| microsoft/Phi-4-mini-instruct | `cfbefacb99257ffa30c83adab238a50856ac3083`（`lastModified 2025-12-10`） | mit | 2503.01743 | **June 2024**（模型卡原文；训练Nov–Dec 2024；发布Feb 2025） |
| MaziyarPanahi/Phi-4-mini-instruct-GGUF（社区量化上游） | `177ca4b8b568a3f865c34e21e914aeb553da19cc`（`lastModified 2025-03-01`） | 上游页声明quantized_by MaziyarPanahi，base microsoft/Phi-4-mini-instruct | — | 继承官方June 2024，不独立声明 |
| contrastors（nomic训练数据/代码仓） | HEAD `613ddfd37309e538cceadb05b1e6423e7b09f603`（2025-02-18，GitHub API实测） | apache-2.0 | — | 今日HEAD非实验pin；实验revision UNVERIFIED |

## 9. §红蓝：阶段门禁 + 红队 ≥5 攻（2026-09-16）

门禁结论：**有条件通过** —— 设计态phi与执行态Spark已拆列（§0/§3），两模型线上pin+本地sha已落盘（§8+json），但残余风险R1–R5仍有效，引用本表时必须同时引用残余风险清单。

| # | 红队攻击 | 防御 / 证据 | 裁决 |
|---|---|---|---|
| R1 | 今日main sha ≠ 实验当日sha（nomic lastModified 2026-04-07、phi 2025-12-10均晚于实验09-12/14）→ 用今日sha冒充实验版本即不可复现 | 承认漂移：§4.1 + §8.3明确标"今日main头非实验pin"；实验revision列写UNVERIFIED；json拆`hf_sha_main`与实验pin字段 | 防御成立，转残余风险① |
| R2 | 本地phi为MaziyarPanahi社区量化Q4_K_S，非官方safetensors → hash无法与官方sha对上，"开权重可证"偷换 | 已拆：本地sha `5482cf4a…`只证"磁盘该字节"，官方sha `cfbefacb…`只证"模型身份"；§1/§8明写不可直接对hash；上游pin `177ca4b8…`单独记录 | 防御成立，转残余风险② |
| R3 | `/v1/models`只有名无revision/hash → "在线即实验权重"不可证；且早前离线、现在在线，时间不一致 | 全文记录矛盾：早前离线（§2）+本次在线时间戳（§8.2）；served revision写UNVERIFIED；nomic以在线名+脚本记录为准，不谎称字节一致 | 防御成立，转残余风险③ |
| R4 | nomic本地文件零命中 → "跑的是哪个字节"无验证；离线时更全无验证 | 如实写零命中（§2/§8.1）；本地hash UNVERIFIED；Two-Tier向量结论只 claim"该服务输出的768维行为"，不claim"某字节权重" | 防御成立，转残余风险④ |
| R5 | `llama/llama-cli.exe` 9216字节无版本输出 → 侧车工具链不可证，且`models/*.gguf`易与Tier-2混淆 | 版本标UNVERIFIED（退出码-1073741515实测）；qwen GGUF hash已算但声明与Tier-2无关（§8.1）；Tier-2路径为LM Studio侧nomic+phi/Spark非llama侧车 | 防御成立，转残余风险⑤ |
| R6 | contrastors HEAD（2025-02-18）≠ 实验数据快照 → "训练数据已披露"不等于"数据版本已pin" | HEAD sha如实记录并标"非实验pin"（§8.3）；可证性只到"披露存在+repo可达"，不到"实验数据版本" | 防御成立，转残余风险⑥ |

**残余风险清单（引用时必须附带）：**
- ① 实验权重revision未pin：两模型的实验当日sha均UNVERIFIED，今日sha仅供身份对照，不可用于复现。
- ② 社区量化断裂：本地phi GGUF（`5482cf4a…`）与官方权重无hash可比性；nomic本地字节完全缺失。
- ③ served态未知：LM Studio在线名已确认（8模型，2026-09-16T06:54:52Z），但served revision/hash未知；早前离线记录与本次在线并存，时间敏感。
- ④ 工具链stub：llama侧车版本UNVERIFIED，与Tier-2无关但同目录易混。
- ⑤ 执行态不可开权重：实际判官Spark为闭源API（§3证据链），"开权重闭环"仅设计态成立，引用baseline必须加注。
- ⑥ 数据版本未pin：contrastors仅HEAD可查，实验数据版本UNVERIFIED。

## 10. Phase-1③ sha pin收尾（2026-09-16，只追加，不改§0–§9数字）

> 范围：provenance §5 checklist 三项 + E3蓝队缺口6 + pip freeze。只新增/追加 research 文件；未动 `tests/`、`freeze/`、`_deploy/`、`linguaGraph.db`、`data/` 既有。查不到写 UNVERIFIED，禁编造。

### 10.1 三项裁决

| # | 项 | 裁决 | 证据落盘 |
|---|---|---|---|
| 1 | nomic本地文件定位（全盘/LM Studio `%USERPROFILE%/.lmstudio`） | **UNVERIFIED**（非PASS：无文件可算hash） | `C:\Users\rongj\.lmstudio\models` 递归 9 文件（8×GGUF+1×config.json），`*nomic*`/`*embed*`（大小写不敏感）零命中；`hub/models` 仅 qwen qwen3-8b/qwen3.5-9b manifest/yaml/README/thumbnail；`%USERPROFILE%/.cache/huggingface` 无目录、无命中。结论：nomic 磁盘字节不可定位，sha256 UNVERIFIED。明细见 `research/weight_snapshot_20260916.json:phase1c3_20260916.item1_nomic_local` |
| 2 | GET /v1/models 全文附录 | **PASS**（全文+时间戳已存；served revision 仍 UNVERIFIED） | `GET http://127.0.0.1:1234/v1/models` 200 在线；8 个 id：`text-embedding-nomic-embed-text-v1.5`、`phi-4-mini-instruct`、`hy-mt2-1.8b`、`gemma-3-270m-it`、`llama-3-sauerkrautlm-8b-instruct`、`qwen2.5-0.5b-instruct`、`qwen/qwen3-8b`、`qwen/qwen3.5-9b`。全文见 **`research/weight_lmstudio_models_20260916.json`**（含 fetched_at_utc + raw）。`/v1/models` 只给名不给 revision/hash → served revision UNVERIFIED（延续§8.2口径） |
| 3 | HF ?rev= pin确认 + contrastors HEAD | **PASS**（今日main/HEAD确认；实验当日pin仍UNVERIFIED） | 访问日期 2026-09-16：nomic `e9b6763023c676ca8431644204f50c2b100d9aab`（lastModified 2026-04-07）与预期一致，`.../resolve/e9b67630.../config.json` 200 可达；phi `cfbefacb99257ffa30c83adab238a50856ac3083`（lastModified 2025-12-10）与预期一致，`.../resolve/cfbefacb.../config.json` 200 可达；MaziyarPanahi GGUF `177ca4b8b568a3f865c34e21e914aeb553da19cc`（2025-03-01）；contrastors HEAD `613ddfd37309e538cceadb05b1e6423e7b09f603`（2025-02-18T19:26:54Z，GitHub API实测）。今日头均晚于实验09-12/14 → 实验 revision 列维持 UNVERIFIED。明细见 snapshot `phase1c3_20260916.item3_hf_rev_confirm` |

### 10.2 E3蓝队缺口6补齐（输入hash，只读不改data）

| 文件 | 字节 | sha256 | 说明 |
|---|---|---|---|
| `data/math_extractions/merged/aligned_data.json` | 936045 | `a663c2c0630c2327e81ef3d15d35311297c1bf7adb9d76f8082a06a604034615` | E3输入219行；只读hash，未改data |
| `research/weight_vectors_934x768_20260916.term2vec.json` | 15873620 | `6a4f8cb93eae60dae3c500c111537d246e44847e50fc1804457ed38eae9b12d8` | 934×768 |
| `research/weight_vectors_934x768_20260916.json` | 15890895 | `cca943eb75b502338b10ee6da1ff275e2a3db819da1133352623527c29896984` | 全量对照 |

### 10.3 运行时（pip freeze）

- `python 3.12.8`（`C:\Users\rongj\AppData\Local\Programs\Python\Python312\python.exe`），`numpy 2.3.5`（import实测）。
- `python3 -m pip freeze` 共 324 行；子集：`numpy==2.3.5`、`torch==2.12.0`、`transformers==5.10.2`、`safetensors==0.8.0`、`sentence-transformers==5.5.1`、`openai==2.41.0`、`scikit-learn==1.9.0`、`scipy==1.17.1`。全文存 snapshot `phase1c3_20260916.runtime.pip_freeze_full`。
- 注：hermes `pip` 显示 `numpy==2.4.3` 系另一环境，与本仓 `sys.executable` 不一致；本快照以 `python3 -m pip`（system 3.12.8）为准，另一环境记分歧不采信。

### 10.4 snapshot路径

- 主快照（追加段）：**`research/weight_snapshot_20260916.json:phase1c3_20260916`**（含 item1/item2/item3 + e3_gap6 + runtime + pip_freeze_full）。
- 在线附录：**`research/weight_lmstudio_models_20260916.json`**（GET /v1/models 全文 + fetched_at_utc `2026-09-16T07:43:25Z` 左右，文件内时间戳为准）。
- 本报告§10即书面 UNVERIFIED/PASS 记录；§0–§9数字未动。

### 10.5 残余风险（Phase-1③后仍有效，引用须附带）

- ① 实验权重revision未pin：今日sha仅身份对照，不可复现；served字节未知（nomic无文件，phi为社区量化）。
- ② `/v1/models` 无 revision/hash；在线名≠字节一致；早前离线与本次在线并存，时间敏感。
- ③ E3输入hash仅证“现盘字节”，不证实验当日字节（当时未落盘）；跨机/跨版本不保证一致（numpy/python已锁定现值，但实验时版本未记录）。
- ④ 执行态判官 Spark 闭源（§3），开权重闭环仅设计态成立。
