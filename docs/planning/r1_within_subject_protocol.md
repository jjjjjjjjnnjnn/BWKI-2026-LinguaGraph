# LinguaGraph — R1 人类组内直接检验协议（Within-Subject 双语臂）

> **状态**: 设计定稿，待启动（招募 = 用户物理动作）
> **依据**: `docs/review/research_forward_review_20260811.md` R1（最高价值方向）+ `docs/osf_preregistration.md` §2.1/§4.2
> **性质**: **补完预注册的 within-subject 人类臂，非新实验**——OSF 预注册已承诺"Bilingual participants (DE-EN) answer identical questions in both languages → within-subject LDS"。冻结项（问卷 5 主题、qwen-plus 提取、LDS v3、概念映射）全部不变；仅新增一种**作答方式**（同一人双语作答）。

---

## 0. 为什么这是决定性检验

A3 设计效应证明目前是**间接的**：人类阴性被归因于"组内个体异质性"（异质性注入在 q=0.30 精确复刻，但该 q 比真实人类稀疏度极端 3×，且 P2 复核降级为"一致性演示"而非"直接因果"）。

**R1 提供直接检验**：让同一批人用两种语言回答相同 5 主题。若人类组内显示语言信号（margin > 0 且 ≈ LLM 组内 margin 0.08–0.09），则"人类阴性 = 组内异质性"从推断升级为直接证实，论文叙事闭环。若人类组内 margin ≈ 0，则诚实否定"信号幅度相等"，把 LLM-as-Subject 重定位为"LLM 属性而非人类属性"——**两个方向都有科学价值，这正是预注册的意义**。

---

## 1. 设计

### 1.1 被试

| 语言对 | 目标 N | 最低 N | 招募渠道 | 备注 |
|--------|:---:|:---:|---------|------|
| **ZH-EN** | 8 | 6 | 微信/小红书/知乎（现有渠道） | 中文母语 + 英语流利（中国留学生最易招） |
| **DE-EN** | 8 | 6 | 学校 Schloss Heessen / 国际班 | **预注册指定的 DE-EN 对** |
| ZH-DE | 3–5 | 2 | 困难（双语者稀少） | 可选；直接匹配 LLM 最强对 |

平衡双语者定义：L1 母语 + L2 达到可自由写作水平（自评 ≥ 8/10 或 C1+）。排除标准沿用预注册 §4.4：跨语言概念重叠 < 50% 视为理解障碍。

### 1.2 作答轮次（每人 3 轮 × 5 主题）

| 轮 | 语言 | 用途 | 间隔 |
|----|------|------|------|
| R1 | L1 | 主数据 | — |
| R2 | **L2** | 跨语言信号（LDS_cross） | ≥ 24–48h 洗脱 |
| R3 | **L1 重测** | 组内语内 floor（LDS_retest） | ≥ 3 天（避免记忆/近因） |

**每人 15 份回答**（约 40 分钟写作，分散一周）。R3 重测**必需**——它是组内语内 floor 的唯一干净来源（见 §1.3）。

### 1.3 为什么 R3 重测必需

LLM 组内 floor（split-half 0.85–0.87）度量"同一模型两次作答的差异"。人类对应物 = 同一人同语言两次作答（重测）。若无重测，唯一可用 floor 是**组间 floor（0.92–0.96）**——它由组间异质性主导，恰是组内设计要消除的，作对比是稻草人。正确对比：
- **信号** = LDS(L1_set, L2_set)（同一人跨语言）
- **floor** = LDS(L1_set, L1_retest_set)（同一人同语言）
- **margin = 信号 − floor**；若 margin > 0，语言比个人作答漂移带来更多概念分歧。

### 1.4 链接（跨轮次配对）

问卷当前匿名单次作答。需为每位参与者分配**编码**（P01…），三轮均填写。最小改动方案：在 `cognitive-space/survey/index.html` 加一个可选的"参与者编码"输入框，随提交写入后端（不收集任何其他身份信息，仍匿名）。这是数据完整性必需，**非呈现改动**。

---

## 2. 分析管线（脚本待数据到达后运行，可先备好）

### 2.1 复用（冻结，零改动）
- 提取：qwen-plus（F1=0.939 验证）
- 概念规范化：`canonical_key`
- LDS：冻结 v3（`lds_concept` / `lds_c_compute.py`）

### 2.2 新增分析（`scripts/lds_c_r1_within_subject.py`，占位）
```
对每位参与者 P：
  S_L1    = canonical keys(P.R1)          # 5 主题概念集
  S_L2    = canonical keys(P.R2)
  S_L1r   = canonical keys(P.R3)
  LDS_cross  = lds_concept(S_L1, S_L2)
  LDS_retest = lds_concept(S_L1, S_L1r)
  margin     = LDS_cross − LDS_retest

聚合（每语言对）：
  mean/median margin；单样本检验 margin > 0
  bootstrap CI（参与者为重采样单元）
  vs 对照：LLM 组内 margin（基线 0.08–0.09；面板 0.03–0.29）
```

### 2.3 判定
| 结果 | 解释 |
|------|------|
| margin > 0 且 ≈ LLM | **直接证实**：人类组内语言信号存在，"人类阴性=组内异质性"闭环 |
| margin ≈ 0 | 诚实否定 A3"信号幅度相等"——LLM 信号是人类没有的模型属性，重定位叙事 |
| margin < 0 | 反直觉但有趣：个人 L2 概念组织比 L1 重测更稳定（需解释，可能是 L2 更抽象/模板化） |

---

## 3. 招募文案（双语者定向，基于 handbook 改造）

### 3.1 ZH-EN（微信/小红书）
```
【求助】AI 竞赛研究项目，需要「中文母语 + 英语流利」的同学帮忙 🧠
我的研究想了解：同一个人用中文和用英语想事情，会不会不一样？
需要你分三次（每次 10-15 分钟，间隔几天）用中/英/中回答相同的 5 个开放式问题。
全程匿名，不收集任何个人信息，可随时退出。
能帮忙的同学请私信我拿问卷链接 + 你的参与编号～提前谢谢！🙏
```

### 3.2 DE-EN（学校/邮件）
```
📢 Umfrage für mein BWKI 2026 Projekt — bilingual (DE/EN) gesucht
Ich untersuche, ob dieselbe Person auf Deutsch und Englisch unterschiedlich über
Werte (Freiheit, Gerechtigkeit, ...) denkt. Drei kurze Runden (je 10-15 Min, mit
Tagen Abstand), anonym, jederzeit abbrechbar. Link + Teilnehmercode per PN. Danke!🙏
```

### 3.3 招募口径
- 明确"3 轮、间隔、同一编号"以管理预期；
- 告知匿名 + 可退出（延续现有同意书，重测在自愿参与范围内）；
- 目标：2 周内收齐 ZH-EN 8 + DE-EN 8。

---

## 4. 分工与时间线

| 事项 | 谁 | 时间 |
|------|-----|------|
| 批准协议 + 启动招募 | 用户 | 今起 |
| 分发问卷 + 分配编号 + 协调 3 轮 | 用户 | 2 周 |
| 问卷加"参与者编码"字段（可选，数据完整性） | 用户批准后执行 | 0.5 天 |
| 提取 + LDS + 分析脚本（`lds_c_r1_within_subject.py`） | 我（可立即备好） | 1 天 |
| 数据收集完成 → 运行分析 → 集成论文 | 我 | 2–3 天 |

**截止兼容**：招募 2 周 + 收集 2 周 + 分析 3 天 ≈ 5 周，**2026-09-20 前完成**。

---

## 5. 风险

| 风险 | 缓解 |
|------|------|
| 双语者招募不足（尤其 ZH-DE） | 以 ZH-EN/DE-EN 为主（预注册指定 DE-EN）；ZH-DE 为增强项 |
| 3 轮流失 | 明确 3 轮预期 + 编号跟踪 + 小额答谢 |
| 重测污染（记忆） | R3 与 R2 ≥ 3 天间隔；必要时换题序 |
| 匿名 vs 链接冲突 | 仅编码 + 时间戳，无身份信息；编码由研究者分配，不落问卷 |
| 冻结项边界 | 不改问卷内容/概念映射/指标/提取——只新增作答轮次与编号字段 |

---

*版本: v1.0 | 2026-08-11 | 预注册依据: `docs/osf_preregistration.md` §2.1/§4.2 · 前置审查: `docs/review/research_forward_review_20260811.md` R1*
