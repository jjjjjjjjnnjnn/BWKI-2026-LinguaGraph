# CognitiveSpace

**从"1+1=2"到偏微分方程的全流程数学知识图谱。**

3D 交互式知识图谱，涵盖从小学到高等数学的完整概念网络。

---

## 数据规模

| 指标 | 值 |
|------|----|
| 概念数 | **574** (557 unique, 17 aligned groups) |
| 关系数 | **525** (unique, +3300 inferred for full connectivity) |
| 教材来源 | **68** 本（45 中 / 20 英 / 10 德） |
| 课程体系 | 人教版 · IB · AP · IGCSE · Abitur · Khan Academy |
| 学段覆盖 | 小学 → 初中 → 高中 → 大学 |
| 结构冲突 | **0** |
| 孤立节点 | **2** (<0.5%) |

## 学段分布

| 学段 | 概念数 | 色标 |
|------|--------|------|
| 小学 | 37 | `#10b981` 绿色 |
| 初中 | 46 | `#14b8a6` 青色 |
| 高中 | 193 | `#4a7dff` 蓝色 |
| 大学 | 298 | `#8b5cf6` 紫色 |

## 语言覆盖

| 语言 | 覆盖 |
|------|------|
| 中文 | 335 (58%) |
| 英文 | 392 (68%) |
| 德文 | 341 (59%) |
| 三语完整 | 247 (43%) |
| 仅中文 | 88 (15%) |

## 知识链

```
小学: 自然数→加法→减法→乘法→除法→分数→小数→百分数→周长→面积→体积
  ↓
初中: 有理数→实数→整式→方程→函数→三角形→四边形→圆→勾股定理→三角函数
  ↓
高中: 导数→积分→泰勒→微分方程→圆锥曲线→概率→统计→向量→矩阵
  ↓
大学: 极限→中值定理→定积分→ODE→PDE→傅里叶→特征值→Jordan→CLT→假设检验
```

## 在线演示

打开 `web/index.html`（直接用浏览器打开，无需服务器）。

## 数据管道

```
教材章节文本
    ↓ (mimo LLM 提取)
结构化 JSON
    ↓ merge_extractions.py (别名合并、去重)
    ↓ align_languages.py (中/英/德跨语言对齐)
    ↓ export_graph.py (生成可视化数据)
web/index.html + data.js (3D 力导向图)
```

## 教材来源

**中文**
- 人教版小学数学 1-6 年级
- 人教版初中数学 7-9 年级
- 人教版高中数学必修 + 选修
- 同济大学《高等数学》《线性代数》

**英文**
- Stewart *Calculus* (8th ed.)
- MIT 18.01 / 18.06 (OCW)
- Gilbert Strang *Linear Algebra*
- Khan Academy Math (K-12 → College)

**德文**
- Otto Forster *Analysis 1-3*
- Gerd Fischer *Lineare Algebra*
- Papula *Mathematik für Ingenieure*
- Lambacher Schweizer (Klett)

## 许可证

本知识图谱中的概念和关系为事实性信息。教材引用属合理使用范畴。
提取数据标注为 CC-BY-SA (教育用途)。

## 论文引用

CognitiveSpace 是 BWKI 2026 LinguaGraph 项目的系统工程验证部分。
详见主项目：[BWKI-2026-LinguaGraph](https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph)
