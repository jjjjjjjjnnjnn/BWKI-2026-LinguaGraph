## 6. Cross-Disciplinary Validation: Physics

To test whether our findings generalize beyond mathematics, we constructed a parallel Physics knowledge graph spanning elementary through university level, covering mechanics, thermodynamics, electromagnetism, optics, modern physics, fluid mechanics, and nuclear/particle physics. The Physics graph contains **366 concepts** and **383 relations** across ZH/EN/DE textbooks with 94 publisher editions.

### 6.1 Concept Density Structure (CDS)

| Level | Physics CDS | Math CDS | Ratio |
|-------|:-----------:|:--------:|:-----:|
| Elementary | **0.222** | 0.216 | 1.03 |
| Middle | 0.029 | **0.271** | 0.11 |
| High | 0.013 | 0.073 | 0.17 |
| College | 0.011 | 0.042 | 0.26 |

**Finding F6**: Physics CDS **peaks at Elementary** (0.222), while Math CDS peaks at Middle school (0.271). Both disciplines show early-stage density peaks, but at different levels:

- **Physics**: Elementary-level mechanics concepts (force, mass, velocity, density, pressure) are highly interconnected — nearly every concept relates to force or motion. This reflects the foundational nature of classical mechanics.
- **Mathematics**: Middle school marks the integration of arithmetic, algebra, geometry, and probability into a cohesive network before dispersing into specialized subfields.

The 3.7× drop from Physics Elementary (0.222) to High (0.013) reflects rapid curricular expansion: physics education broadens from ~10 core mechanics concepts to 136 high-school concepts spanning thermodynamics, electromagnetism, optics, and modern physics.

### 6.2 Hierarchy Depth Structure (HDS)

| Metric | Physics | Math |
|--------|:-------:|:----:|
| Maximum depth | **6** | 8 |
| Mean depth | **0.85** | 0.40 |
| Root concepts | 219 (64%) | 459 (83%) |

**Finding F7**: Physics exhibits **deeper prerequisite chains** (mean HDS 0.85 vs Math 0.40). This reflects the cumulative nature of physics knowledge: understanding electromagnetic induction requires first mastering electric charge → current → magnetic field → Faraday's law — a chain of 4+ concepts. Mathematics, by contrast, has more independent entry points (83% roots).

### 6.3 Publisher Coverage

| Language | Publishers | Education Levels |
|----------|:----------:|:----------------:|
| Chinese (ZH) | 33 | Elementary → University |
| English (EN) | 34 | Elementary → University |
| German (DE) | 27 | Elementary → University |

Key publishers include:
- **ZH**: 人教版, 沪科版, 北师大版, 苏科版, 粤教版, 鲁科版, 马文蔚, 程守洙, 漆安慎, 赵凯华, 汪志诚, 杨福家, 梁昆淼, 郭硕鸿, 曾谨言
- **EN**: Khan Academy, CK-12, AP Physics 1/2/C, IB, IGCSE, GCSE, Halliday Resnick Walker, Serway Jewett, Young Freedman, Griffiths, Kittel, Feynman Lectures
- **DE**: Duden, Lambacher Schwere, Westermann, Cornelsen, Klett, Auer, Dorn-Bader, Kern, Thieme, Tipler, Demtröder, Jackson, Arfken, Schiff, Greiner

### 6.4 Interpretation

The contrasting CDS patterns across disciplines suggest that **knowledge organization is discipline-dependent**, not universal:

- **Physics** follows a **convergent-then-diverge** pattern: tightly interconnected foundational concepts (elementary mechanics) before dispersing into independent subfields (thermodynamics, E&M, optics, modern physics).
- **Mathematics** follows a **build-then-disperse** pattern: foundational arithmetic integrates at middle school, then branches into specialized domains.

This pattern is consistent with the pedagogical structure of physics education, where mechanics provides the conceptual foundation that unifies all later subfields through force analysis and energy conservation.

### 6.5 Figures

- Figure 6: CDS Comparison — Math vs Physics by Education Level (outputs/figures/fig6_cds_comparison.png)

### 6.6 Data Assets

| Asset | Concepts | Relations | Status |
|-------|:--------:|:---------:|:------:|
| Math knowledge graph | 574 | 3,538 | Complete |
| Physics knowledge graph | 366 | 383 | Complete |
| NRW curriculum graph | 41 | 147 | In progress |
| Chinese curriculum graph | 0 | 0 | Pending |
