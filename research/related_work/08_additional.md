# Area 8: Additional Relevant Work

## Additional Repositories

### Graph Edit Distance
- **Link**: NetworkX (built-in)
- **Domain**: □ NLP ☑ KG □ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 4/5
- **What it does**: NetworkX provides graph_edit_distance() — exact algorithm for computing the minimum edit distance between two graphs. O(n³) worst case.
- **What's similar**: LinguaGraph uses GED as a core component of LDS
- **Can borrow**: Already using it — this is a verification that the approach is standard
- **Cite in paper**: YES — NetworkX is the implementation reference

### NetworkX
- **Link**: https://github.com/networkx/networkx (14000+ ⭐)
- **Domain**: □ NLP ☑ KG □ Cross-lingual ☑ Visualization □ Annotation
- **Relevance to LinguaGraph**: 5/5
- **What it does**: Standard Python library for graph analysis. Provides algorithms for centrality, community detection, shortest paths, graph edit distance, etc.
- **What's similar**: LinguaGraph's entire graph pipeline is built on NetworkX
- **Can borrow**: Already using it — citation reference
- **Cite in paper**: YES — core dependency

### spaCy
- **Link**: https://github.com/explosion/spaCy (30000+ ⭐)
- **Domain**: ☑ NLP □ KG □ Cross-lingual □ Visualization ☑ Annotation
- **Relevance to LinguaGraph**: 2/5
- **What it does**: Industrial-strength NLP library. Used by CoCo-Ex for concept extraction pipeline.
- **Can borrow**: NER and dependency parsing for pre-processing
- **Cite in paper**: NO (LinguaGraph uses LLM extraction, not spaCy)

### Ollama
- **Link**: https://github.com/ollama/ollama (120000+ ⭐)
- **Domain**: ☑ NLP □ KG □ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Local LLM inference. LinguaGraph supports Ollama as a provider for Qwen3-8B.
- **What's similar**: Both use local LLMs for NLP tasks
- **Can borrow**: Already using it
- **Cite in paper**: YES — infrastructure reference

## Additional Papers

### Graph Edit Distance (Bunke & Shearer, 1998)
- **Title**: A Graph Distance Metric Based on the Maximal Common Subgraph
- **Link**: https://doi.org/10.1023/A:1008238806256
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Foundational work on graph edit distance — the minimum number of edit operations to transform one graph into another.
- **What's similar**: LinguaGraph uses GED as a core metric
- **Cite in paper**: YES — algorithmic foundation

### Jaccard Similarity (Jaccard, 1912)
- **Title**: The Distribution of the Flora in the Alpine Zone
- **Link**: Classic reference
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Jaccard index = |A ∩ B| / |A ∪ B|. Used for set similarity. LinguaGraph applies it to node sets and edge sets.
- **What's similar**: LinguaGraph uses Jaccard as a core metric
- **Cite in paper**: YES — mathematical foundation

### Knowledge Graph Survey (Hogan et al., 2021)
- **Title**: Knowledge Graphs
- **Link**: https://dl.acm.org/doi/10.1145/3459637
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Comprehensive survey of knowledge graphs: construction, storage, retrieval, quality, and applications.
- **Can borrow**: Taxonomy of KG quality metrics, construction methods
- **Cite in paper**: YES — survey reference

### Graph Neural Networks for KG (Wang et al., 2020)
- **Title**: A Comprehensive Survey of Graph Neural Networks
- **Link**: https://arxiv.org/abs/2009.01329
- **Relevance to LinguaGraph**: 2/5
- **What it does**: Survey of GNNs for graph-structured data. Covers message passing, attention, pooling.
- **What LinguaGraph does differently**: LinguaGraph uses classical graph algorithms, not GNNs
- **Cite in paper**: NO (LinguaGraph doesn't use deep learning on graphs)

### LLM as NLP Pipeline (Mialon et al., 2023)
- **Title**: Augmented Language Models: a Survey
- **Link**: https://arxiv.org/abs/2302.07842
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Survey of LLMs used as NLP pipelines — replacing traditional multi-stage NLP with single LLM calls.
- **What's similar**: LinguaGraph uses LLMs for concept extraction (replacing traditional NER + relation extraction)
- **Can borrow**: Evaluation methodology for LLM-as-pipeline
- **Cite in paper**: YES — reference for LLM-based extraction approach
