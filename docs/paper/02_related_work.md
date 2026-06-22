## 2. Related Work

This section situates LinguaGraph within four research strands: educational knowledge graphs, curriculum analysis and comparison, concept mapping and cognitive structure, and cross-lingual knowledge integration.

### 2.1 Educational Knowledge Graphs

The construction of knowledge graphs from educational resources has seen significant advances in recent years. Yao et al. (2019) proposed joint embedding learning for educational knowledge graphs, demonstrating that concept relationships can be automatically inferred from curriculum documents [1]. Zhao, Sun, and Xu (2022) developed EDUKG, a heterogeneous K-12 educational knowledge graph spanning multiple subjects, showing the feasibility of large-scale curriculum-level knowledge organization [2].

Most relevant to LinguaGraph is the work of Ain, Chatti, and Qussa (2025), who developed an optimized pipeline for automatic educational knowledge graph construction [3]. Their approach uses large language models for concept extraction, similar to our MIMO prompt methodology. A follow-up study compared top-down and bottom-up construction approaches, finding that bottom-up extraction from textbook content yields more complete concept coverage [4]. LinguaGraph adopts a bottom-up approach but extends it by incorporating cross-language alignment — a dimension absent from existing EKG pipelines.

Alatrash, Chatti, and Wibowo (2025) specifically addressed prerequisite inference in educational knowledge graphs, proposing a multi-criteria approach that considers textual, structural, and taxonomic signals [5]. Their method directly informs the HDS metric in our framework, which measures the depth of prerequisite chains as a proxy for knowledge hierarchy.

### 2.2 Curriculum Analysis and Comparison

Cross-national curriculum comparison has been a cornerstone of international education research. The TIMSS (Trends in International Mathematics and Science Study) framework provides systematic methodology for comparing curricula across countries, including curriculum intention, implementation, and attainment dimensions [6]. The OECD PISA studies similarly analyze how curriculum structures affect learning outcomes [7].

Specific comparisons between German and Chinese mathematics curricula have been conducted by Liang and Heckmann (2013), who analyzed textbook problems and found systematic differences in problem complexity and representation style [8]. Fan, Zhu, and Miao (2013) extended this to a broader cross-national comparison of textbook problems [9]. While these studies focus on problem-level or content-level comparison, LinguaGraph introduces a graph-level comparison — the Language Drift Score (LDS) — which captures structural differences that surface-level content analysis misses.

The recently published Kernlehrplan NRW (2019, 2023) for German Gymnasium mathematics provides a formal competency-based curriculum structure [10]. The Chinese equivalent, the *Yiwu Jiaoyu Shuxue Kecheng Biaozhun* (2022) and the *Putong Gaozhong Shuxue Kecheng Biaozhun* (2017), similarly define learning progressions and content standards [11]. LinguaGraph is the first system to our knowledge that converts these curriculum standards into structured knowledge graphs for direct cross-language comparison.

### 2.3 Concept Mapping and Knowledge Organization

The theoretical foundation of knowledge structure analysis traces to Ausubel's assimilation theory of meaningful learning (1963), which argues that knowledge is organized hierarchically rather than as isolated facts [12]. Novak and Cañas (2008) operationalized this theory through concept mapping, demonstrating that knowledge structures can be externalized as propositional networks [13]. Their framework underlies the CDS and HDS metrics in LinguaGraph: Concept Density Score captures the connectedness of concepts within a knowledge domain, while Hierarchy Depth Score measures prerequisite chain depth.

Recent advances have automated concept map generation. Weakly supervised approaches using graph translation (2021) [14] and generative LLM-based methods (2025) [15] have made large-scale concept mapping feasible. LinguaGraph differs from these approaches in its multilingual orientation: rather than generating concept maps for a single language, we construct parallel knowledge graphs across Chinese, German, and English, enabling cross-linguistic structural comparison.

### 2.4 Cross-lingual Knowledge Graph Alignment

Cross-lingual knowledge graph alignment aims to identify equivalent entities and relations across languages. Early work by McGillivray et al. (2016) proposed multilingual knowledge graph embeddings for cross-lingual alignment [16]. Subsequent research developed entity alignment methods using adversarial training [17], subgraph networks [18], and co-training with entity descriptions [19].

These alignment-focused approaches differ fundamentally from LinguaGraph's goal. Alignment research asks: *How do we match equivalent concepts across languages?* LinguaGraph asks: *Given matched concepts, what structural differences remain between language-specific knowledge organizations?* The LDS metric captures these residual structural differences — the divergence that persists after concept alignment — which existing cross-lingual KG research has not systematically quantified.

### 2.5 Research Gap

While each of these research strands has independently explored aspects of knowledge structure analysis, no existing work integrates:

1. **Automatic knowledge graph construction** from multilingual textbook content
2. **Systematic comparison** of knowledge structures across languages
3. **Quantitative metrics** (LDS, CDS, HDS) for structural comparison
4. **Curriculum-level analysis** comparing textbook knowledge graphs to official curriculum standards

LinguaGraph addresses this gap by providing an integrated pipeline from textbook extraction through cross-language structural analysis, with validated metrics that capture knowledge organization differences at multiple levels — across languages (LDS), education levels (CDS), and hierarchical depth (HDS).

---

## References

[1] Yao, S., Wang, R., & Sun, S. (2019). Joint Embedding Learning of Educational Knowledge Graphs. arXiv:1911.08776.

[2] Zhao, B., Sun, J., & Xu, B. (2022). EDUKG: a Heterogeneous Sustainable K-12 Educational Knowledge Graph. arXiv:2210.12228.

[3] Ain, Q. U., Chatti, M. A., & Qussa, J. (2025). An Optimized Pipeline for Automatic Educational Knowledge Graph Construction. arXiv:2509.05392.

[4] Ain, Q. U., Chatti, M. A., & Shakhshir, A. (2025). Top-Down vs. Bottom-Up Approaches for Automatic EKG Construction. arXiv:2505.10069.

[5] Alatrash, R., Chatti, M. A., & Wibowo, N. (2025). Inferring Prerequisite Knowledge Concepts in EKGs. arXiv:2509.05393.

[6] IEA. (1995–2023). Trends in International Mathematics and Science Study (TIMSS). International Association for the Evaluation of Educational Achievement.

[7] OECD. (Various). PISA Curriculum Analysis and Education at a Glance. OECD Publishing.

[8] Liang, S., & Heckmann, K. (2013). A comparison of German and Chinese mathematics textbooks. ZDM, 45(5), 743–756.

[9] Fan, L., Zhu, Y., & Miao, Z. (2013). A comparative study on mathematics textbook problems across countries. ICMT.

[10] MSB NRW. (2019). Kernlehrplan Mathematik für das Gymnasium (Sek I). Ministerium für Schule und Bildung NRW.

[11] MoE China. (2022). Yiwu Jiaoyu Shuxue Kecheng Biaozhun [Compulsory Education Mathematics Curriculum Standards]. Ministry of Education, PRC.

[12] Ausubel, D. P. (1963). The Psychology of Meaningful Verbal Learning. Grune & Stratton.

[13] Novak, J. D., & Cañas, A. J. (2008). The Theory Underlying Concept Maps. IHMC.

[14] Weakly Supervised Concept Map Generation through Task-Guided Graph Translation. (2021). AAAI.

[15] Generative Large Language Models for Knowledge Representation: A Systematic Review of Concept Map Generation. (2025). arXiv.

[16] McGillivray, B., et al. (2016). Multilingual Knowledge Graph Embeddings for Cross-lingual Knowledge Alignment. IJCAI.

[17] Cross-lingual Entity Alignment with Adversarial Kernel Embedding. (2021). AAAI.

[18] SubGraph Networks based Entity Alignment for Cross-lingual Knowledge Graph. (2022). arXiv.

[19] Co-training Embeddings of Knowledge Graphs and Entity Descriptions for Cross-lingual Entity Alignment. (2018). arXiv.
