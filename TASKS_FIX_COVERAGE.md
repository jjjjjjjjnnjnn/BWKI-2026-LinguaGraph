# 覆盖度修复 — 给 mimo code 的任务

## 问题
`config/expert_graphs/coverage_scores.json` 只包含 NRW 数据 (12.7%)，但你的控制台输出显示 UK=37.3%, US=17.2%, China=95.4% 已计算完成。这些值需要写入文件。

## 要求

### 方法 (课标概念 → 教材概念匹配)

对每个教育体系的课标 JSON，读取课标概念列表，检查有多少在 `math_full.json` 的教材概念库中有匹配：

```python
import json
import os
from pathlib import Path

PROJECT = "C:/Users/rongj/Desktop/学校/BWKI-2026-备战"

# 1. 加载教材概念库 (所有三语标注)
textbook = json.load(open(f"{PROJECT}/config/expert_graphs/math_full.json", encoding="utf-8"))
textbook_concepts = set()
for g in textbook.get("groups", []):
    labels = g.get("labels", {})
    for lang in ["zh", "en", "de"]:
        if labels.get(lang):
            textbook_concepts.add(labels[lang].lower().strip())

print(f"Textbook concepts: {len(textbook_concepts)}")

# 2. 对每个课标文件计算覆盖度
curricula = {
    "NRW": "curriculum_nrw_math.json",
    "UK": "curriculum_uk_math.json",
    "China": "curriculum_cn_math.json",
    "US": "curriculum_us_math.json",
}

for sys_name, filename in sorted(curricula.items()):
    path = f"{PROJECT}/config/expert_graphs/{filename}"
    if not os.path.exists(path):
        print(f"  {sys_name}: file not found")
        continue
    
    curr = json.load(open(path, encoding="utf-8"))
    curr_concepts = set()
    for c in curr.get("concepts", []):
        name = c.get("name", c.get("label", ""))
        if name:
            curr_concepts.add(name.lower().strip())
    
    # Count concepts with subgraph matching or keyword matching
    matched = sum(1 for cc in curr_concepts if any(tc.startswith(cc) or cc.startswith(tc) or 
        all(w in tc for w in cc.split()) for tc in textbook_concepts))
    
    coverage = matched / max(len(curr_concepts), 1)
    print(f"  {sys_name}: {matched}/{len(curr_concepts)} = {coverage:.1%}")

# 3. 保存到 coverage_scores.json
```

### 输出格式
覆盖 `config/expert_graphs/coverage_scores.json`：

```json
{
  "NRW": {
    "overall": {"curriculum_concepts": 299, "matched": 38, "coverage_score": 0.127}
  },
  "UK": {
    "overall": {"curriculum_concepts": 397, "matched": 148, "coverage_score": 0.373}
  },
  "US": {
    "overall": {"curriculum_concepts": 2124, "matched": 366, "coverage_score": 0.172}
  },
  "China": {
    "overall": {"curriculum_concepts": 87, "matched": 83, "coverage_score": 0.954}
  }
}
```

### 验证
- 4 个体系都有 overall
- NRW ≈ 12.7%, UK ≈ 37.3%, US ≈ 17.2%, China ≈ 95.4%
- UTF-8 编码
