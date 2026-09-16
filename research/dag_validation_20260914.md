# DAG 验证报告（2026-09-14）

对象：`data/math_extractions/` 顶层 68 个 json（排除 `merged/` 子目录）。
方法：networkx 有向图，节点=概念名，边=relations，归一化=去首尾空白+小写。
全局图：685 节点 / 665 边。只读 data，未改任何数据。

## 1. 环检测：11 个（成员去重后）

| # | 成员 |
|---|------|
| 1 | 圆（自环，`zh_初中数学_九年级.json`，另见 R1） |
| 2 | counting \| place value |
| 3 | erwartungswert \| varianz |
| 4 | expression \| variable |
| 5 | 克 \| 千克 |
| 6 | 全等三角形 \| 相似三角形 |
| 7 | 方向导数 \| 梯度 |
| 8 | 正方形 \| 长方形 |
| 9 | area \| length \| perimeter |
| 10 | equation \| expression \| variable |
| 11 | 三角函数 \| 偏微分方程 \| 傅里叶级数 \| 分离变量法 \| 切线 \| 圆 \| 导数 \| 常微分方程 \| 微分方程（9 节点大环） |

去重方式：`simple_cycles` 结果按成员集合（frozenset）去重后 11 个（去重前后一致，无旋转重复）。

## 2. prune 统计：共 141 条（`research/prune_candidates_20260914.json`）

| kind | 计数 | action |
|------|------|--------|
| self_loop（自环，`圆`） | 1 | 删边 1 |
| bad_length（实体<2或>20字符：单字 8 / 超长 57） | 65 | 人工定 65（CJK 单字多合法、超长多为短语需拆分/改名） |
| dangling（全局悬空端点出现次数） | 51 | 见 §3 去向表 |
| dup_relation（文件内重复关系对） | 24 | 删边 24（去冗余，`de_lambacher_5-8.json` 6 对最多） |

规则脚本：`scripts/tools/rule_prune_candidates.py`（只读 data、只写 research/）。
悬空规则：(a)字符数<2或>20→删边；(b)全局频次≥2→补概念；(c)别名/模糊（difflib≥0.85）可解→纠目标；(d)其余→人工定。

## 3. 51 悬空端点去向表

| 去向 | 计数 | 说明举例 |
|------|------|----------|
| 补（补概念） | 35 | pde×6、体积×5、向量空间×5、面积×3、周长×3、fläche×3 等系统性缺概念；含无别名但频次≥2 的 symmetrie×2、三角函数×2 |
| 纠（纠目标） | 13 | 别名可解的一次性笔误/异名，如 likelihood function→似然函数、vektorraum→vector space、trennung der variablen→separation of variables |
| 删（删边） | 1 | Trennung der Variablen（22 字符噪声标签） |
| 归档（人工定） | 2 | Exponentenrechnung、Trigonometrie（无别名、单次出现，待人工判定） |
| 合计 | 51 | 35+13+1+2=51 ✓ |

注：悬空 51 为“端点出现次数”（50 条边涉及，其中 1 条边双端悬空）；去重后独立端点 27 个。
别名跨语言可解是主体（纠 13 + 补中别名可解的高频项），说明抽取端点多用了异名而非标准概念名。

## 4. 新增文件清单（仅 3 个，未改数据、未碰禁区）

1. `scripts/tools/rule_prune_candidates.py`
2. `research/prune_candidates_20260914.json`
3. `research/dag_validation_20260914.md`（本文件）
