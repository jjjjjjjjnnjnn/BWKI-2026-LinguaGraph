# W6 LM Studio 恢复操作方案 (LM_RESTORE_OPS)

> 依据：
> - `research/tier2_smoke_20260914.log`：2026-09-14 探测 `127.0.0.1:1234/v1` DEAD（`Invoke-WebRequest` + `curl.exe -m 3` 均 refused），`--test` 未执行，OUT 未覆盖。
> - `scripts/semantic_ground_en.py` docstring + 常量（L18-22）：`LM=http://127.0.0.1:1234/v1`，`EMB_MODEL=text-embedding-nomic-embed-text-v1.5`，`CHAT_MODEL=phi-4-mini-instruct`，`--test` = 5 节点冒烟，`--full` = 全部 ungrounded，`OUT=config/expert_graphs/text_grounding_en_semantic_20260912.json`（resume-safe）。
> 本文件只给用户操作步骤，不执行下载。

## 0. 前提 / 禁区（先读）

- 基准：`base=C:\Users\rongj\Desktop\学校\BWKI-2026-备战`，所有命令在此目录执行。
- 禁区不动：`data/lds_c/llm_subject`、`linguaGraph.db`、`tests/*断言`；不删缓存、不全量重嵌、不覆盖 OUT。
- 保护对象（恢复前先确认未被改）：
  - `C:/Users/rongj/AppData/Local/Temp/opencode/sem_emb_cache.json`：约 10615 entries，dim=768（只读计数即可，不要删）。
  - `config/expert_graphs/text_grounding_en_semantic_20260912.json`：约 Length=106766，LastWriteTime=2026/9/12 18:28:56，results=407。

## 1. 下载 / 安装 LM Studio

1. 官网 `https://lmstudio.ai/` 下载 Windows 安装包（2026-09-14 时期最新 stable 0.3.x 即可，无需指定旧版；只要支持 OpenAI-compatible `GET /v1/models`、`POST /v1/embeddings`、`POST /v1/chat/completions`）。
2. 安装后首次启动，跳过不必要的插件，保持默认本地服务端即可。

## 2. 下载两个模型（名字必须精确）

在 LM Studio → Discover / Search 页分别搜索并 Download：

1. Embedding（prefilter 用）：
   - `text-embedding-nomic-embed-text-v1.5`
   - 即脚本 `EMB_MODEL`（`scripts/semantic_ground_en.py:19`）。不要下 `nomic-embed-v1.5` 的其他变体（GGUF 后缀不同会换 model id，导致 404）。
2. 判官（adjudication 用）：
   - `phi-4-mini-instruct`
   - 即脚本 `CHAT_MODEL`（`scripts/semantic_ground_en.py:20`），`temperature=0, max_tokens=5` 由脚本传入，无需在 UI 改。

下载完成后在 My Models 确认两者都 Present。

## 3. 启动本地服务（必须 127.0.0.1:1234）

1. LM Studio 左栏 → Developer（`</>`）→ Status / Server：
   - Enable `Serve on Local Network` 可关（本机即可）；
   - Port 必须 `1234`，Host `127.0.0.1`（脚本硬编码 `LM="http://127.0.0.1:1234/v1"`，改端口必挂）。
2. 分两次 Load（或一次全 Load，内存够即可）：
   - Load `text-embedding-nomic-embed-text-v1.5`（Embeddings 开启）；
   - Load `phi-4-mini-instruct`（temp 0 由请求控制，UI 可留默认）。
3. 点 `Start Server`，状态变绿 `Running on http://127.0.0.1:1234`。

## 4. 存活探测（2 选 1，3 秒超时）

PowerShell（base 目录）：

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:1234/v1/models" -TimeoutSec 3 -UseBasicParsing
```

或：

```powershell
curl.exe -m 3 -s http://127.0.0.1:1234/v1/models
```

- 成功：返回 JSON 含上述两个 model id → 进 §5。
- 失败（`无法连接到远程服务器` / exit 7）：仍为 DEAD，停手，不要跑 `--test/--full`（硬跑必挂在 `post("/embeddings")` / `post("/chat/completions")`）。

## 5. 恢复后顺序：--test → --full

```powershell
python scripts/semantic_ground_en.py --test
python scripts/semantic_ground_en.py --full
```

- 必须先 `--test`（5 节点冒烟），通过后再 `--full`。
- 两者都是 resume-safe：读 OUT 已有 results 按 `name` 跳过（126-131 行逻辑），逐条追加写 OUT，安全断点续跑；Ctrl+C 后重跑即可。

## 6. 预期输出（对照 tier2_smoke log §5）

`--test` 正常时应看到（数字必须对上，否则停手检查）：

```text
ungrounded EN nodes: 407
corpus sentences: <与上次一致>
cache hit: 10615 vecs
embedding 0 new sentences...
resuming: 407 done
semantic hits: ...  # --test 只跳过 done，不新增
```

关键断言：

- `407 resuming`：`text_grounding_20260912.json` 待做 `243+164=407` 与 OUT `results=407` 对齐。
- `零新 embed`：`missing = 0`，即 `CACHE` 10615 vecs 全命中，不调用 `/embeddings` 增量；`--test` 的 5 节点因 `name in done` 全部跳过，`--full` 同理零新增。
- 若出现 `embedding N new sentences (N>0)` 或 `resuming < 407`：说明 CACHE/OUT 被动过，先停手核对 §0 的 Length/时间戳。

## 7. 失败回退：只用 shards 改判（无 LM 调用）

若 LM 仍 DEAD 或 `--test` 挂在 `post()`：

1. 不重试 `--full`，不删 CACHE，不覆盖 OUT。
2. 只用已落盘离线数据做判官一致率（`research/tier2_smoke_20260914.log §3` 口径）：
   - 源：`C:/Users/rongj/AppData/Local/Temp/opencode/sem_shards/manifest.json` + `shard_XX.json` + `verdict_*.json`
   - 口径：`10 shards = 9x41 + 1x38 = 407 nodes`（与 `merge_sem_verdicts.py assert 407` 一致），`verdicts 10 files, total 407, unique 407, dup 0`，`union_keys=en,evidence,graph,name,semantic_hit`。
   - 已知基线：总命中 `165/407=40.5%`（physics 104/243，chemistry 61/164），`verdicts vs OUT mismatch 0/407 → 100%一致`。
3. 回退动作仅限：重算命中率 / 按 shard 分布 / 与 OUT 对齐检查（只读 `json.load`），新增文件只允许 `research/*.log|*.md`。

## 附录：常量速查

| 项 | 值 |
|---|---|
| LM endpoint | `http://127.0.0.1:1234/v1` |
| EMB_MODEL | `text-embedding-nomic-embed-text-v1.5` |
| CHAT_MODEL | `phi-4-mini-instruct` (temp 0) |
| CACHE | `C:/Users/rongj/AppData/Local/Temp/opencode/sem_emb_cache.json` |
| OUT | `config/expert_graphs/text_grounding_en_semantic_20260912.json` |
| 基座 | `config/expert_graphs/text_grounding_20260912.json` |
| 命令 | `python scripts/semantic_ground_en.py --test` → `--full` |
