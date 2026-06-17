# LinguaGraph — 数据收集管道 (Human Data)

> **用途**: 人类实验数据的标准化处理流程
> **设计原则**: 匿名化 → 标注 → 分析 → 报告，每一步可审计

---

## 目录结构

```
participant_data/
├── raw/              ← 原始数据 (来自问卷平台，含身份信息)
│   └── (gitignored)
├── anonymized/       ← 匿名化数据 (PII 已移除，用于分析)
│   └── participants.jsonl
├── annotations/      ← 人工标注
│   ├── annotator_A/
│   ├── annotator_B/
│   └── consensus/
├── graphs/           ← 个体认知图谱 (JSON)
├── reports/          ← 分析报告
└── logs/             ← 处理日志
```

---

## 数据流

```
Google Form / 问卷平台
    ↓ CSV 导出
raw/{batch}_export.csv
    ↓ anonymize.py (移除姓名、邮箱、IP)
anonymized/{batch}.jsonl
    ↓ annotate.py (两位标注员独立标注)
annotations/annotator_A/{batch}.json
annotations/annotator_B/{batch}.json
    ↓ consensus.py (合并标注)
annotations/consensus/{batch}.json
    ↓ 
graph.py (构建认知图)
graphs/{participant}.json
    ↓
analyze.py (计算 LDS + Bootstrap CI)
reports/{batch}_analysis.json
    ↓
结果表格 + 图表
results/
```

---

## 使用说明

```bash
# 1. 导入原始 CSV
python participant_data/import.py --input raw/survey_export.csv --batch pilot_001

# 2. 匿名化
python participant_data/anonymize.py --batch pilot_001

# 3. 生成标注任务
python participant_data/prep_annotation.py --batch pilot_001

# 4. 分析 (标注完成后)
python scripts/analyze_student.py --all

# 5. 生成报告
python participant_data/generate_report.py --batch pilot_001
```

---

## GDPR 合规

| 阶段 | 数据内容 | 存储 | 期限 |
|------|----------|------|------|
| raw/ | 姓名, 邮箱, IP, 回答 | 加密, `.gitignore` | 分析完成后销毁 |
| anonymized/ | 年龄, 语言, 回答 | 明文, `.gitignore` | 研究结束后归档 |
| annotations/ | 标注结果 | 明文 | 永久 (研究记录) |
| graphs/ | 匿名化认知图 | 明文 | 永久 (研究记录) |
