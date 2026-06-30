# LinguaGraph — Research Release Checklist

> 每次从研究阶段推进到发布时执行。确保论文数字、代码数据、portal 显示三者一致。

---

## Step 1: 运行完整的工程检查

```bash
# 全流程验证
python scripts/release.py

# 确认输出
cat data/quality_history/release_report.md
```

**必须 PASS：** Gate 1-4 ✓, release.py exit 0

---

## Step 2: 确认数字一致性

```bash
# 读取 manifest
python -c "import json; m=json.load(open('manifest.json')); print('Nodes:', m['graph']['total_nodes']); print('Groups:', m['alignment']['aligned_groups']); print('Trilingual:', m['alignment']['trilingual_groups'])"
```

| 检查项 | 命令 |
|--------|------|
| 论文节点数 vs manifest | `manifest.json.graph.total_nodes` |
| 论文边数 vs manifest | `manifest.json.graph.total_links` |
| Portal 显示的数字 | 必须与 manifest.json 一致 |
| 图表引用的数字 | 必须与 manifest.json 一致 |
| data.js MD5 | `manifest.json.checksums['data.js']` |

---

## Step 3: 版本锁定

```bash
# 记录当前 release
git tag "research/v$(cat manifest.json | python -c "import sys,json; print(json.load(sys.stdin)['build_time'][:10])")"

# 确认 tag 存在
git tag -l "research/*"
```

---

## Step 4: 论文引用格式

论文 Method 或 Appendix 中包含以下信息：

```
Data version:        manifest.json 的 build_time + git_commit
Pipeline version:    manifest.json 的 pipeline_version
Schema version:      manifest.json 的 data_schema_version
Number of textbooks: 93 (data/textbook/)
Gold labels:         92 (data/gold/gold_dataset.json)
```

---

## 快速验证

```bash
python -c "
import json
m = json.load(open('manifest.json'))
print('=== Release Readiness ===')
print(f'  Git commit:    {m[\"provenance\"][\"git_commit\"]}')
print(f'  Build time:    {m[\"build_time\"]}')
print(f'  Nodes:         {m[\"graph\"][\"total_nodes\"]}')
print(f'  Links:         {m[\"graph\"][\"total_links\"]}')
print(f'  Groups:        {m[\"alignment\"][\"aligned_groups\"]}')
print(f'  Trilingual:    {m[\"alignment\"][\"trilingual_groups\"]}')
print(f'  data.js MD5:   {m[\"checksums\"][\"data.js\"]}')
print()
print('Status: READY' if m['checksums']['data.js'] else 'Status: NOT READY')
"
```
