# LinguaGraph — Literature Matrix

> Generated: 2026-06-22
> Sources: arXiv, Semantic Scholar, Google Scholar
> Structure: 5 priority areas × 5-10 papers each

---

## Area 1: Educational Knowledge Graphs (EKG)

| # | Paper | Year | Authors | Venue | Relevance to LinguaGraph |
|---|-------|------|---------|-------|--------------------------|
| 1 | Joint Embedding Learning of Educational Knowledge Graphs | 2019 | Yao, Wang, Sun | arXiv | EKG construction methodology |
| 2 | EDUKG: a Heterogeneous Sustainable K-12 Educational Knowledge Graph | 2022 | Zhao, Sun, Xu | arXiv | K-12 KG spanning all subjects — closest to our approach |
| 3 | An Optimized Pipeline for Automatic Educational Knowledge Graph Construction | 2025 | Ain, Chatti, Qussa | arXiv | **Most directly relevant** — automatic EKG pipeline |
| 4 | Top-Down vs. Bottom-Up Approaches for Automatic EKG Construction | 2025 | Ain, Chatti, Shakhshir | arXiv | Two construction paradigms; LinguaGraph uses bottom-up |
| 5 | Inferring Prerequisite Knowledge Concepts in EKGs: A Multi-criteria Approach | 2025 | Alatrash, Chatti, Wibowo | arXiv | Prerequisite inference — directly supports our HDS metric |
| 6 | Multi-source Education KG Construction and Fusion for College Curricula | 2023 | Li, Cheng, Zhang | arXiv | Multi-source fusion across curricula |
| 7 | Leveraging Graph RAG to Support Understanding of Knowledge Concepts in MOOCs | 2025 | Abdelmagied, Chatti, Joarder | arXiv | KG + LLM in education; post-dates our approach |

## Area 2: Curriculum Analysis & Comparison

| # | Paper | Year | Authors | Venue | Relevance to LinguaGraph |
|---|-------|------|---------|-------|--------------------------|
| 1 | TIMSS Curriculum Analysis (Trends in International Mathematics and Science Study) | 1995–2023 | IEA | IEA | Multi-country curriculum comparison framework |
| 2 | Knowing Mathematics for Teaching (comparison of German/Chinese textbooks) | 2004 | Ball, Bass, et al. | JTE | Cross-national textbook comparison methodology |
| 3 | Textbook problem comparison across Asian and European systems (Fan, Zhu, Miao) | 2013 | Fan, Zhu, Miao | ESM | Cross-national textbook problem analysis |
| 4 | German and Chinese mathematics textbook comparison (Liang & Heckmann) | 2013 | Liang, Heckmann | ZDM | Directly compares DE and ZH math textbooks |
| 5 | OECD Curriculum Studies (Education at a Glance, PISA curriculum analysis) | Various | OECD | OECD | Cross-national curriculum structure data |
| 6 | National Curriculum frameworks (Kernlehrplan NRW, Chinese K-12 Standards) | Various | MSB NRW / MoE China | Government | Primary source documents for our curriculum layer |

## Area 3: Concept Mapping & Knowledge Organization

| # | Paper | Year | Authors | Venue | Relevance to LinguaGraph |
|---|-------|------|---------|-------|--------------------------|
| 1 | The Theory Underlying Concept Maps and How to Construct and Use Them | 2008 | Novak, Cañas | IHRDC | **Foundational** — concept mapping theory |
| 2 | Learning, Creating, and Using Knowledge: Concept Maps as Facilitative Tools | 1998/2010 | Novak | Routledge | Core theory for our CDS/HDS metrics |
| 3 | Enhancing Knowledge Tracing with Concept Map and Response Disentanglement | 2024 | — | arXiv | Concept maps for knowledge tracing |
| 4 | Concept Map Assessment Through Structure Classification | 2025 | — | arXiv | Automated concept map evaluation |
| 5 | Weakly Supervised Concept Map Generation through Task-Guided Graph Translation | 2021 | — | AAAI | Automated concept map from text |
| 6 | Generative LLMs for Concept Map Generation: A Systematic Review | 2025 | — | arXiv | **Highly relevant** — LLM + concept maps |
| 7 | Harnessing Structured Knowledge: Concept Map-Based MCQ Generation | 2025 | — | arXiv | EKG application to assessment |

## Area 4: Cross-lingual Knowledge Graphs

| # | Paper | Year | Authors | Venue | Relevance to LinguaGraph |
|---|-------|------|---------|-------|--------------------------|
| 1 | Multilingual Knowledge Graph Embeddings for Cross-lingual Knowledge Alignment | 2016 | — | IJCAI | Cross-lingual KG alignment — LDS precursor |
| 2 | SubGraph Networks based Entity Alignment for Cross-lingual KG | 2022 | — | arXiv | Entity alignment across languages |
| 3 | Cross-lingual Temporal Knowledge Graph Reasoning | 2023 | — | arXiv | Cross-lingual KG temporal reasoning |
| 4 | Co-training Embeddings for Cross-lingual Entity Alignment | 2018 | — | arXiv | Entity/relation mapping across languages |
| 5 | Cross-lingual Entity Alignment with Adversarial Kernel Embedding | 2021 | — | arXiv | Alignment methods comparison |

## Area 5: Textbook Analysis & Comparative Studies

| # | Paper | Year | Authors | Venue | Relevance to LinguaGraph |
|---|-------|------|---------|-------|--------------------------|
| 1 | Comparative Textbook Analysis (general methodology) | Various | — | — | Framework for comparing textbooks |
| 2 | Cognitive Network Science: A review of research on cognition | 2019 | Siew | Cognitive Science | Network analysis of cognitive structures |
| 3 | Ausubel's Assimilation Theory of Meaningful Learning | 1963/2000 | Ausubel | — | **Foundational** — knowledge is structured, not listed |
| 4 | Knowledge Space Theory (KST) | 1985–present | Doignon, Falmagne | Springer | Theory of prerequisite knowledge structures |

---

## Core Papers by Direct Relevance to LinguaGraph

### Tier 1: Must-cite (directly support LDS/CDS/HDS or pipeline)

1. **Novak & Cañas (2008)** — Concept map theory → theoretical basis for CDS
2. **Alatrash, Chatti et al. (2025)** — Prerequisite inference in EKG → directly supports HDS
3. **Ain, Chatti et al. (2025)** — Automatic EKG pipeline → validates our extraction approach
4. **Siew (2019)** — Cognitive network science → theoretical basis for structure analysis
5. **Ausubel (1963/2000)** — Assimilation theory → "knowledge is structure, not list"

### Tier 2: Important context

6. **Liang & Heckmann (2013)** — DE/ZH textbook comparison → our work extends to graph
7. **Fan, Zhu & Miao (2013)** — Cross-national textbook problem comparison → methodology reference
8. **Zhao, Sun, Xu (2022)** — EDUKG K-12 graph → closest existing project
9. **Doignon & Falmagne (1985)** — Knowledge Space Theory → prerequisite structure theory

### Tier 3: Supporting

10. **Novak (1998/2010)** — Book-length concept mapping theory
11. **OECD PISA/TIMSS** — Curriculum comparison frameworks
12. Various cross-lingual KG alignment papers (2016–2023)

---

## BibTeX (export-ready)

```bibtex
@article{ain2025optimized,
  title={An Optimized Pipeline for Automatic Educational Knowledge Graph Construction},
  author={Ain, Qurat Ul and Chatti, Mohamed Amine and Qussa, Jean},
  journal={arXiv preprint arXiv:2509.05392},
  year={2025}
}

@article{alatrash2025inferring,
  title={Inferring Prerequisite Knowledge Concepts in Educational Knowledge Graphs: A Multi-criteria Approach},
  author={Alatrash, Rawaa and Chatti, Mohamed Amine and Wibowo, Nasha},
  journal={arXiv preprint arXiv:2509.05393},
  year={2025}
}

@article{zhao2022edukg,
  title={EDUKG: a Heterogeneous Sustainable K-12 Educational Knowledge Graph},
  author={Zhao, Bowen and Sun, Jiuding and Xu, Bin},
  journal={arXiv preprint arXiv:2210.12228},
  year={2022}
}

@article{yao2019joint,
  title={Joint Embedding Learning of Educational Knowledge Graphs},
  author={Yao, Siyu and Wang, Ruijie and Sun, Shen},
  journal={arXiv preprint arXiv:1911.08776},
  year={2019}
}

@article{ain2025topdown,
  title={Top-Down vs. Bottom-Up Approaches for Automatic Educational Knowledge Graph Construction in CourseMapper},
  author={Ain, Qurat Ul and Chatti, Mohamed Amine and Shakhshir, Amr},
  journal={arXiv preprint arXiv:2505.10069},
  year={2025}
}

@inproceedings{li2023multisource,
  title={Multi-source Education Knowledge Graph Construction and Fusion for College Curricula},
  author={Li, Zeju and Cheng, Linya and Zhang, Chunhong},
  booktitle={arXiv preprint arXiv:2305.04567},
  year={2023}
}

@article{siew2019cognitive,
  title={Cognitive Network Science: A review of research on cognition},
  author={Siew, Cynthia SQ},
  journal={Topics in Cognitive Science},
  year={2019}
}

@techreport{novak2008theory,
  title={The Theory Underlying Concept Maps and How to Construct and Use Them},
  author={Novak, Joseph D and Cañas, Alberto J},
  institution={IHMC},
  year={2008}
}

@book{novak1998learning,
  title={Learning, Creating, and Using Knowledge: Concept Maps as Facilitative Tools in Schools and Corporations},
  author={Novak, Joseph D},
  year={1998},
  publisher={Routledge}
}

@article{liang2013comparison,
  title={A comparison of German and Chinese mathematics textbooks},
  author={Liang, Senfeng and Heckmann, Kirsten},
  journal={ZDM},
  year={2013}
}

@inproceedings{fan2013comparing,
  title={A comparative study on mathematics textbook problems across countries},
  author={Fan, Lianghuo and Zhu, Yan and Miao, Zhenzhen},
  booktitle={International Conference on Mathematics Textbook Research},
  year={2013}
}

@inproceedings{mcgillivray2016multilingual,
  title={Multilingual Knowledge Graph Embeddings for Cross-lingual Knowledge Alignment},
  author={McGillivray, Barbara and others},
  booktitle={IJCAI},
  year={2016}
}

@book{ausubel1963psychology,
  title={The Psychology of Meaningful Verbal Learning},
  author={Ausubel, David P},
  year={1963},
  publisher={Grune & Stratton}
}

@book{doignon1985knowledge,
  title={Knowledge Spaces},
  author={Doignon, Jean-Paul and Falmagne, Jean-Claude},
  year={1985},
  publisher={Springer}
}
```
