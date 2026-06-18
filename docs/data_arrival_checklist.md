# LinguaGraph — DE/EN Data Arrival Checklist

> **用途:** DE/EN 数据到达后逐项核对，确保导入质量。
> **流程:** 数据到达 → mimo 处理 → 本清单核查 → `python scripts/run_pipeline.py`

---

## 1. 文件完整性检查

*数据文件准备阶段（mimo 处理前）*

- [ ] 原始数据格式已知（CSV / JSON / XLSX / Google Forms 导出）
- [ ] 文件编码为 UTF-8（非 GBK / GB2312 / Latin-1）
- [ ] 文件名命名规范：`responses_{lang}_{date}.csv`
- [ ] 每文件包含 response_id, student_id, language, question_id, answer_text 列

---

## 2. 参与者数据验证

*导入前确认*

| 检查项 | 命令 / 方法 | 通过条件 |
|:-------|:------------|:--------:|
| participant_id 不重复 | `SELECT student_id, COUNT(*) FROM students GROUP BY student_id HAVING COUNT(*) > 1` | 0 行 |
| native_lang 正确标记 | `SELECT DISTINCT native_lang FROM students` | `de`, `en` 存在 |
| age_group 格式一致 | `SELECT DISTINCT age_group FROM students` | 统一格式（如 "10-15"） |
| consent 字段 | `SELECT student_id FROM students WHERE consent = 0` | 0 行 |
| years_in_germany 合理 | `SELECT student_id, years_in_germany FROM students` | 无负值 / 远超年龄的值 |

**快速检查脚本:**
```python
from db_utils import get_connection, query
conn = get_connection()
dupes = query(conn, "SELECT student_id, COUNT(*) FROM students GROUP BY student_id HAVING COUNT(*) > 1")
print(f"Duplicates: {len(dupes)}")
print(f"Languages: {query(conn, 'SELECT DISTINCT native_lang, COUNT(*) FROM students GROUP BY native_lang')}")
conn.close()
```

---

## 3. 回答数据验证

*导入后立即检查*

| 检查项 | 命令 / 方法 | 通过条件 |
|:-------|:------------|:--------:|
| 总回答数匹配 | `SELECT COUNT(*) FROM responses` | 已知预期值 |
| 语言分布正确 | `SELECT language, COUNT(*) FROM responses GROUP BY language` | 每语言 ≥ 预期数 |
| 题目编号齐全 | `SELECT DISTINCT question_id FROM responses` | 10 个 ID（q8–q17） |
| 每人回答数正确 | `SELECT student_id, COUNT(*) FROM responses GROUP BY student_id` | 每人 10 条 |
| 无乱码 / 编码错误 | `SELECT response_id FROM responses WHERE answer_text LIKE '%�%'` | 0 行 |
| 无空回答 | `SELECT response_id FROM responses WHERE answer_text IS NULL OR TRIM(answer_text) = ''` | 0 行 |

**常见问题与处理:**

| 问题 | 处理方式 |
|:-----|:---------|
| participant_id 重复 | 确认是否为重填；保留一份，删除重复 |
| language 标签错误 | 查找源数据，手工修正再重导入 |
| question_id 不匹配 | 与问卷模板对照，修正后重导 |
| 编码错误（�） | 重新以 UTF-8 编码保存源文件 |
| 空回答 | 联系参与者确认；标记为缺失（quality_flag = 'missing'） |

---

## 4. 回答质量检查

*导入后质量评估*

| 检查项 | 阈值 | 命令 |
|:-------|:----:|:-----|
| Completion rate | ≥ 90% | `SELECT 1.0 * COUNT(*) / (students * 10) AS rate FROM responses` |
| Short answers (<5 chars) | < 15% | `SELECT COUNT(*) FROM responses WHERE LENGTH(TRIM(answer_text)) < 5` |
| Language mixing detected | < 20% | `pilot_pipeline.py` 自动报告 |
| Average word count | ≥ 8 | `SELECT AVG(LENGTH(answer_text)) FROM responses` |
| 每题回答人数 | 每人各 1 条 | `SELECT question_id, COUNT(DISTINCT student_id) FROM responses GROUP BY question_id` |

**若质量未达标:**
- Completion < 90% → 核查是否系统性地缺了某些题目或参与者
- Short answers > 15% → 检查是否有题目被系统性忽略（如翻译题）
- 语言混合 > 20% → 确认参与者是否按要求使用目标语言回答

---

## 5. 管道运行验证

*数据导入并确认质量后*

```bash
# 全量运行
python scripts/run_pipeline.py

# 确认输出
ls results/tables/
ls results/figures/
ls docs/pilot_quality_report.md
```

**预期输出:**

| 产出 | 路径 | 验证方式 |
|:-----|:-----|:---------|
| 参与者摘要 | `results/tables/participant_summary.csv` | 确认含 DE/EN 行 |
| 质量报告 | `docs/pilot_quality_report.md` | Completion > 90%, 已知问题更新 |
| Table 1 人口学 | `results/tables/table1_demographics.md` | 3 语言列均有数据 |
| Table 2 LDS | `results/tables/table2_lds_by_topic.md` | 有实际 LDS 值，不是 `—` |
| Figure 1 | `results/figures/figure1_lds_distribution.png` | 3 组条形图可见 |
| Figure 3 | `results/figures/figure3_topic_comparison.png` | 水平条形图可见 |

**若某环节失败:**
```bash
# 1. 确认 DB 连接正常
python -c "from db_utils import get_connection; c = get_connection(); print('OK')"

# 2. 确认有 DE/EN 数据
python -c "from db_utils import get_connection, query; c = get_connection(); print(query(c, 'SELECT language, COUNT(*) FROM responses GROUP BY language'))"

# 3. 确认 cross_language_analysis 有数据
python -c "from db_utils import get_connection, query_value; c = get_connection(); print(f'LDS analyses: {query_value(c, \"SELECT COUNT(*) FROM cross_language_analysis\")}')"
```

---

## 6. LDS 结果验收

*跨语言分析完成后*

- [ ] LDS 值在合理范围内（0.0–1.0）
- [ ] Bootstrap CI 非 NaN
- [ ] 至少一个语言对显示出显著差异（CI 不重叠）
- [ ] LDS 值按预期排序（文化概念 > 空间描述 > 专业描述）

**已知预期（来自 validation_rationale.md）:**
- q9（文化概念 · 孝/Fernweh/Privacy）→ LDS 最高
- q13（空间描述）→ LDS 最低–中
- q14（时间翻译）→ LDS 中–高

---

## 7. 签署确认

```markdown
- [ ] 文件完整性检查通过
- [ ] 参与者数据验证通过
- [ ] 回答数据验证通过
- [ ] 回答质量检查通过（或已知问题已记录）
- [ ] Pipeline 全量运行成功
- [ ] LDS 结果合理
- [ ] 以上有异常项已在 `docs/pilot_quality_report.md` 中记录

检查人: ________________
日期: ________________
```
