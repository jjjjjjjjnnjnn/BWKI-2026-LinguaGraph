# LinguaGraph — 3 Core Conclusions (Poster/Pitch Ready)

> 将 7 个研究发现 (F1-F7) 压缩为 3 条主结论
> 适用于：海报、3 分钟演讲、摘要、评审材料

---

## Conclusion 1: Knowledge Density Is Non-Monotonic and Discipline-Dependent

**What we found**:
> Mathematics reaches its maximum interconnection density at **Middle school** (CDS=0.271), while Physics reaches it at **College** (CDS=0.065).

**Why it matters**:
> The assumption that "more advanced knowledge is more densely connected" is false. Both disciplines show a **peak-and-diverge** pattern — but at different educational stages. This means curriculum design should account for discipline-specific knowledge structure trajectories.

**Evidence**:
| Discipline | Peak Level | Peak CDS | Shape |
|-----------|-----------|---------|-------|
| Mathematics | Middle school | 0.271 | ↑ peak ↓ steady decline |
| Physics | College | 0.065 | gradual ↑ peak at top |

**Robustness**: ✅ Confirmed in ZH, EN, DE independently

---

## Conclusion 2: Knowledge Depth Has a Universal Upper Limit

**What we found**:
> Maximum prerequisite chain depth is bounded at **HDS ≤ 7–9**, regardless of discipline. Mean depth differs by discipline (Math: 0.40, Physics: 1.17).

**Why it matters**:
> Educational knowledge appears to respect a natural depth limit on prerequisite structures. Concepts do not stack deeper than approximately 7 layers — suggesting that curriculum designers intuitively avoid deep prerequisite chains. Physics, however, requires **2.8× more sequential learning** than mathematics (49% roots vs 83%).

**Evidence**:
| Metric | Math | Physics |
|--------|:----:|:-------:|
| Max HDS | 9 | 7 |
| Mean HDS | 0.40 | 1.17 |
| Root concepts | 83% | 49% |
| Structure type | Shallow web | Deeper chain |

---

## Conclusion 3: Cross-Language Structural Divergence Is Substantial and Asymmetric

**What we found**:
> LDS values range from **0.80 to 0.91** across ZH/EN/DE. ZH–DE shows the **highest** divergence (0.907); ZH–EN the **lowest** (0.802).

**Why it matters**:
> Despite mathematical truth being universal, the **organizational structure** of mathematical knowledge varies significantly across languages. The pattern is **not** driven by language family: Chinese and English textbooks are structurally closer than German and English. Curriculum tradition, not language relatedness, appears to be the primary driver.

**Evidence**:
| Pair | LDS | Interpretation |
|------|:---:|---------------|
| ZH–DE | 0.907 | Highest structural divergence |
| DE–EN | 0.901 | Near-maximum despite shared European tradition |
| ZH–EN | 0.802 | Lowest — Anglo-American influence on Chinese curricula |

---

## Unified Narrative (30-Second Pitch)

> **Mathematics and physics knowledge follow different density trajectories, respect a universal depth bound, and are organized differently across languages — even when the content is the same.**
> 
> LinguaGraph makes these invisible structural patterns visible and measurable.

---

## Theory → Evidence Chain

| Conclusion | Theory | Evidence Source | Supports |
|-----------|--------|----------------|----------|
| C1 | Ausubel (1963) — knowledge integration before specialization | CDS by level (Math + Physics) | Curriculum design |
| C2 | Novak & Cañas (2008) — concept maps as propositional networks | HDS distribution (Math + Physics) | Learning progression |
| C3 | Liang & Heckmann (2013) — cross-national textbook variation | LDS across ZH/EN/DE | Education policy |
