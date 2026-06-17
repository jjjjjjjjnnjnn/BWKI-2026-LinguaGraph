# LinguaGraph Research Loop

## 目标

建立多语言认知差异证据库，持续产出研究发现。

## 核心原则

1. **100 篇可比较的平行语料 > 5000 篇杂乱文本**
2. **每个循环必须回答一个研究问题**
3. **失败案例比成功案例更有价值**

## 循环结构

```
Phase A: Data Discovery    — 寻找平行文本
Phase B: Data Audit        — 审核质量
Phase C: Pipeline Validation — 提取+比较
Phase D: Error Mining      — 发现失败案例
Phase E: Report            — 输出发现
```

## 主题优先级

1. Freedom / 自由 / Freiheit
2. Responsibility / 责任 / Verantwortung
3. Success / 成功 / Erfolg
4. Fairness / 公平 / Gerechtigkeit
5. Home / 家 / Heimat

## 终止条件

- 每主题 ≥ 50 篇平行文本
- 总文本数 ≥ 250
- 发现 ≥ 20 个高价值案例
- Concept F1 > 85%

## 文件结构

```
research/
├── loop_config.json        # 循环配置
├── findings/               # 发现记录
│   ├── topic_freedom.md
│   ├── topic_justice.md
│   └── ...
├── failure_cases/          # 失败案例
├── notable_cases/          # 高价值案例
├── gold_dataset/           # 标注数据
└── reports/                # 研究报告
    └── pilot_study_final.md
```
