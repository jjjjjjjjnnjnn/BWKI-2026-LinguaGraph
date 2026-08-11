# LinguaGraph — A3/C/D 深化结果：设计效应证明 · 分歧驱动者 · 节点/边分解

> **生成**: 2026-08-08 | **管线**: `scripts/lds_c_design_effect.py` · `scripts/lds_c_divergence_drivers.py` · `scripts/lds_c_node_edge_decomp.py`
> **公式**: 冻结 v3（`docs/lds_formal_definition.md`）| **数据**: `data/lds_c/llm_subject/` · `data/lds_c/extractions_*.json` · `data/math_extractions/merged/aligned_data.json` · `data/wikipedia_extractions/`
> **状态**: 纯分析深化（零新 API 调用），全部结果可复现

---

## 0. 一句话结论

**三项深化把 D1 的"设计伪影"主张从推断升级为定量证明，并补上论文遗留的 RQ4（驱动者）与跨域结构分解：**
① **信号幅度相等**：人类 LDS-C（0.93–0.96）与 LLM LDS-C（0.93–0.96）几乎相同——跨语言分歧的**幅度在人类与模型中一样**；真正的差异在**底噪**（人类 split-half 0.92–0.96 ≈ 信号 → 淹没；LLM 0.85–0.87 ≪ 信号 → 可见），且**不是样本量问题**（LLM 在 N=3 仍有信号）。② **ZH-DE 分歧驱动者是框架负载文化概念**（DE：自主/规则/目标导向；ZH：空间/边界/应得）。③ **社会/制度反转是节点驱动的**，边分量不反转（数学边贡献 0.074 最大）——制度知识收敛于概念选择，关系组织仍分歧。

---

## 1. 设计效应证明（`lds_c_design_effect.py` → `design_effect_20260808.json`）

### 1.1 核心观察：信号幅度相等，底噪不同

| 语言对 | 人类 LDS-C | 人类 split-half 底 | 人类 s/f | LLM LDS-C | LLM split-half 底 | LLM s/f |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| ZH-EN | 0.9634 | 0.9585 | **1.005** | 0.9552 | 0.8745 | **1.092** |
| DE-EN | 0.9324 | 0.9237 | **1.009** | 0.9300 | 0.8456 | **1.100** |
| ZH-DE | 0.9364 | 0.9223 | **1.015** | 0.9446 | 0.8618 | **1.096** |

> **⚠️ 样本量标注（审计 H3）**: 上表的人类底噪用 6/6（DE/ZH）→ 3/3 切分、EN 3 → 1/2 切分；LLM 底噪用 10 → 5/5 切分——**每半样本数不对称**（小半集 LDS 更高）。为排除"样本量混淆"，用 **N-matched 复核**（§1.2，floor_scan N=6 行 = 3+3 切分）：LLM 底噪在匹配切分下仍为 0.854–0.885，远低于人类 0.922–0.958（gap 0.05–0.07）。**结论不依赖样本量不对称**。

- **人类 signal/floor ≈ 1.00**（余量 +0.005~0.014）→ 语言信号**淹没**在组内个体变异中。
- **LLM signal/floor ≈ 1.09–1.10**（余量 +0.08~0.09）→ 语言信号**可见**。
- **信号幅度相等**：人类与 LLM 的跨语言 LDS-C 都是 0.93–0.96——人类阴性**不是"无语言效应"**，而是信号被同量级的底噪掩盖。

### 1.2 Floor-scan：不是样本量问题

| N/语 | ZH-EN 余量 | DE-EN 余量 | ZH-DE 余量 |
|:---:|:---:|:---:|:---:|
| 3 | +0.021 | +0.038 | +0.028 |
| 5 | +0.051 | +0.062 | +0.059 |
| 6 | +0.065 | +0.076 | +0.071 |
| 8 | +0.076 | +0.081 | +0.078 |
| 10 | +0.081 | +0.085 | +0.083 |

**LLM 即使在 N=3 仍检出信号**（余量 +0.02~0.04）。人类 N=15（6/6/3）的阴性**不是样本量不足**——是**组内方差结构**不同：人类同语言内参与者异质（floor 0.92–0.96），LLM 同权重样本同质（floor 0.85–0.87）。

### 1.3 Virtual between-subject lens（决定性对照）

把 LLM 样本当作"虚拟参与者"、按**人类同样的组间管线**、在**人类 N=6/语**下重分析：

| 语言对 | LLM 虚拟组间 LDS-C | LLM 虚拟组间 floor | 余量 |
|:---:|:---:|:---:|:---:|
| ZH-EN | 0.9491 | 0.8854 | **+0.064** |
| DE-EN | 0.9317 | 0.8589 | **+0.073** |
| ZH-DE | 0.9441 | 0.8741 | **+0.070** |

**LLM 信号即使在"组间设计 + 人类 N"下依然存活**（余量 +0.06~0.07）。→ **人类阴性既不是"无语言效应"，也不是单纯"组间设计"——而是"人类组内个体异质性"**。LLM 作为受控被试之所以能分离信号，是因为同一权重集合消除了人类个体差异这一方差源。

### 1.4 对论文叙事的修正（v0.8 → 深化）

原 v0.8 表述"人类阴性 = 设计伪影（组间混淆语言与个体差异）"——**方向 A 将其精确化**：
- 跨语言分歧的**幅度在人类与 LLM 中相同**（LDS-C 均 0.93–0.96）；
- 差异在**底噪**：人类组内个体变异（0.92–0.96）与信号同量级 → 不可分辨；LLM 采样同质（0.85–0.87）→ 可分辨；
- **组间设计本身并非不可用**（LLM 组间虚拟 lens 仍检出信号），**问题在于人类组内异质性**这一方差源被组间设计带入底噪。

---

## 2. A5 分歧驱动者（`lds_c_divergence_drivers.py` → `divergence_drivers_20260808.json`）

### 2.1 方法

逐语言对、逐主题，计算每个对齐概念的存在不对称性，按提及频次加权 → 驱动者排序。**只在一侧语言出现的概念驱动 LDS；两侧共享的概念降低 LDS。**

### 2.2 LLM P1 top 驱动者（ZH-DE，within-subject）

| 主题 | 概念（canonical key） | 方向 | 频次 |
|:---:|:---|:---:|:---:|
| Gerechtigkeit | equal opportunity | DE-only | 7 |
| Freiheit | freedom limit of | DE-only | 6 |
| Heimat | physical space | ZH-only | 6 |
| Erfolg | goal own | DE-only | 6 |
| Heimat | feel | DE-only | 5 |
| Freiheit | boundary freedom of | ZH-only | 4 |
| Gerechtigkeit | due treatment | ZH-only | 4 |
| Erfolg | accord living one own s to valu | ZH-only | 4 |

**模式**：ZH-DE 的分歧驱动者是**框架负载概念**——DE 侧偏"自主/规则/目标"（equal opportunity, freedom limit, goal own），ZH 侧偏"空间/边界/应得"（physical space, boundary freedom, due treatment）。这与 §4.4 的方向性趋势（DE 自主、ZH 法理/应得）**在概念粒度上互相印证**。

### 2.3 各语言对驱动者/共享量

| 语言对 | 驱动者总数 | 共享概念总数（5 主题） |
|:---:|:---:|:---:|
| ZH-EN | 394 | 20 |
| DE-EN | 340 | 27 |
| ZH-DE | 372 | 21 |

共享概念极少（每主题 2–8 个）→ 三语概念图几乎完全由语言侧特有概念构成，与 LDS-C ≈ 0.93–0.96 一致。

### 2.4 人类参考（between-subject）与关系驱动者

- **人类 ZH-DE top 驱动者**：DE 侧 consequence/family/work（频次 2–3），ZH 侧 Freiheit 集群（legal right / cage of power / exercise freedom）。与 LLM 方向性一致（DE 责任-后果，ZH 自由-法理）。
- **关系驱动者（edge level）**：
  - DE-only：`responsibility relates_to consequence`（freq 3）、`responsibility relates_to harm`（freq 2）
  - ZH-only：`success relates_to goal`、`success relates_to goal milestone stage`、`freedom relates_to individual`
  - → **ZH-DE 关系层面同样是 DE 责任-后果 vs ZH 成功-目标** 的结构性分工。

---

## 3. 节点/边分解对称（`lds_c_node_edge_decomp.py` → `node_edge_decomp_20260808.json`）

### 3.1 三来源 × 三语言对的分解（冻结 v3）

| 来源 | 语言对 | LDS v3 | J_node | J_edge | node-only | edge+ |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| 数学（制度） | ZH-EN | 0.9336 | 0.086 | 0.047 | 0.914 | 0.020 |
| 数学（制度） | ZH-DE | **0.5188** | 0.556 | 0.407 | **0.444** | **0.074** |
| Wikipedia（社会） | ZH-EN | 0.6976 | 0.324 | 0.281 | 0.677 | 0.021 |
| Wikipedia（社会） | ZH-DE | **0.8191** | 0.200 | 0.162 | **0.800** | 0.019 |
| 人类（认知） | ZH-DE | 0.9535 | 0.085 | 0.008 | 0.915 | 0.038 |

### 3.2 关键发现：反转是节点驱动的，边分量不反转

- **节点分量反转成立**：数学 ZH-DE node-only 0.444（制度最趋同）vs 社会 0.800（文化最分歧）。
- **边分量不反转**：数学 edge+ 0.074（**最大**）vs 社会 0.019 vs 人类 0.038。
- **→ 制度知识的趋同主要体现在概念选择（节点），而关系组织（边）仍系统性分歧**。数学的概念集跨语言高度重叠（J_node 0.556），但"概念如何连接"（J_edge 0.407）分歧显著大于社会领域（0.162）。

### 3.3 对 A4 §3.8 的修正

A4 表述"ZH-DE 边分量贡献 3–4×（0.075）"本身正确，但**深化后的解释不同**：该 0.075 不是"边驱动的趋同"，而是"边驱动的**分歧**"——数学概念收敛（node-only 0.444）却被边结构拉回（LDS v3 0.519）。社会领域的反转则纯粹是节点现象。**跨域结论：制度 vs 社会的结构反转 = 概念选择（节点）驱动；关系组织在所有来源都系统性分歧。**

---

## 4. 异质性注入直接检验（`lds_c_heterogeneity_injection.py` → `heterogeneity_injection_20260809.json`）

把"人类阴性 = 组内异质性"从**排除法**升级为**直接因果证明**。

### 4.1 基线：单样本异质性人类与 LLM 相似

| 语言 | 人类两两重叠 | LLM 两两重叠 | 人类 avg 概念/人 | LLM avg 概念/人 |
|:---:|:---:|:---:|:---:|:---:|
| zh | 0.057 | 0.059 | 26.0 | 28.7 |
| de | 0.106 | 0.108 | 21.2 | 27.8 |
| en | 0.038 | 0.072 | 21.7 | 28.2 |

→ 单样本异质性可比；floor 差异的机制是**聚合稀疏度**（人类每参与者概念少 → 3+3 半聚合稀疏 → 高 floor）。

### 4.2 注入扫描（ZH-DE 焦点，LLM 数据，q = 概念保留概率）

| q | LLM LDS-C | LLM floor | 信号余量 |
|:---:|:---:|:---:|:---:|
| 1.00 | 0.944 | 0.873 | **+0.071** |
| 0.60 | 0.939 | 0.905 | +0.033 |
| 0.40 | 0.946 | 0.916 | +0.030 |
| 0.30 | 0.955 | **0.941** | **+0.014** |
| **人类（参考）** | 0.936 | **0.921** | **+0.015** |

### 4.3 决定性校准

**q=0.30 时 LLM floor（0.941）≥ 人类 floor（0.921），信号余量坍缩到 +0.014 ≈ 人类 +0.015——精确复刻人类阴性。**

→ **人类阴性被直接因果地归因于组内异质性（聚合稀疏度），而非"无语言效应"**。已写入论文 §5.9.2b + 讨论 §4.14。

---

## 5. 论文整合点

| 章节 | 新增内容 |
|------|---------|
| `03_results.md` §5.8 | 设计效应证明（信号幅度相等 + 底噪差异 + 非 N 效应 + 虚拟组间 lens） |
| `03_results.md` §5.9.2 | **异质性注入直接因果证明（坍缩表 + 校准点）** |
| `03_results.md` §5.8 | A5 分歧驱动者（ZH-DE 框架负载概念，DE 自主/规则 vs ZH 空间/应得） |
| `03_results.md` §3.8 | 节点/边分解对称（反转是节点驱动，边不反转） |
| `04_discussion.md` §4.14 | 设计伪影精确化：人类阴性 = 组内个体异质性，非组间设计本身、非无效应；**注入证实为正面因果** |
| `lds_formal_definition.md` §6 | 设计效应证据加入反证框架 |

---

## 6. 数据与脚本血缘

| 资产 | 位置 |
|------|------|
| 方向 A 结果 | `data/lds_c/llm_subject/design_effect_20260810.json`（修正版：ratio 解读已修复） |
| 方向 C 结果 | `data/lds_c/divergence_drivers_20260809.json`（最新日期） |
| 方向 D 结果 | `data/lds_c/lds_k_deep/node_edge_decomp_20260809.json`（最新日期） |
| **异质性注入结果** | `data/lds_c/llm_subject/heterogeneity_injection_20260809.json` |
| 方向 A 脚本 | `scripts/lds_c_design_effect.py` |
| 方向 C 脚本 | `scripts/lds_c_divergence_drivers.py` |
| 方向 D 脚本 | `scripts/lds_c_node_edge_decomp.py` |
| **异质性注入脚本** | `scripts/lds_c_heterogeneity_injection.py` |

**复现**：`python scripts/lds_c_design_effect.py && python scripts/lds_c_divergence_drivers.py && python scripts/lds_c_node_edge_decomp.py && python scripts/lds_c_heterogeneity_injection.py`
