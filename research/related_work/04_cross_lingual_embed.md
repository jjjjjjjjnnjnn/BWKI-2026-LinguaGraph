# Area 4: Cross-lingual Embeddings / Multilingual Semantic Spaces

## Repositories

### MUSE (Multilingual Unsupervised and Supervised Embeddings)
- **Link**: https://github.com/facebookresearch/MUSE (5700+ ⭐)
- **Domain**: ☑ NLP □ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Facebook's library for training multilingual word embeddings. Supports unsupervised alignment (no parallel data needed) and supervised alignment. Maps word vectors across 40+ languages.
- **What's similar**: Both deal with cross-lingual concept alignment. Both need to bridge language-specific representations.
- **What LinguaGraph does differently**: MUSE aligns word vectors; LinguaGraph aligns concept graphs. MUSE works at the word level; LinguaGraph works at the graph-structure level.
- **Can borrow**: Unsupervised alignment methodology, evaluation benchmarks (BLI tasks)
- **Cannot borrow**: Vector-space approach (LinguaGraph uses graph structure)
- **Cite in paper**: YES — reference for cross-lingual embedding baseline

### XLM-R (Cross-lingual Language Model)
- **Link**: https://github.com/facebookresearch/xlm (3700+ ⭐)
- **Domain**: ☑ NLP □ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Cross-lingual language model pre-trained on 100 languages. State-of-the-art for cross-lingual NLU tasks (XNLI, MLQA, etc.).
- **What's similar**: Both deal with cross-lingual representation
- **What LinguaGraph does differently**: XLM-R is a general-purpose multilingual LM; LinguaGraph is a specialized cognitive graph comparison tool
- **Can borrow**: Cross-lingual evaluation methodology
- **Cite in paper**: NO (too general)

### LASER (Language-Agnostic SEntence Representations)
- **Link**: https://github.com/facebookresearch/LASER (3300+ ⭐)
- **Domain**: ☑ NLP □ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Computes language-agnostic sentence embeddings for 90+ languages. Enables cross-lingual sentence similarity, translation ranking, etc.
- **What's similar**: Both deal with cross-lingual semantic comparison
- **Can borrow**: Sentence-level cross-lingual comparison methodology
- **Cite in paper**: NO

### WikiAlignment
- **Link**: https://github.com/facebookresearch/ccaligned (48 ⭐)
- **Domain**: ☑ NLP □ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Aligns Wikipedia articles across 97 languages. Creates massive parallel data for cross-lingual research.
- **What's similar**: Both use Wikipedia as cross-lingual data source
- **Can borrow**: Parallel data methodology
- **Cite in paper**: YES — data methodology reference

### Cross-Lingual Semantic Similarity Analysis
- **Link**: https://github.com/siddhi-bansal/linguistic-similarity-analysis-nlp
- **Domain**: ☑ NLP □ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Cross-lingual semantic similarity analysis using LASER, LaBSE, and OpenAI embeddings with heatmaps and word clouds across 61 languages.
- **What's similar**: Both measure cross-lingual semantic similarity, both produce visual outputs
- **What LinguaGraph does differently**: This project measures similarity; LinguaGraph measures structural cognitive differences
- **Can borrow**: Visualization approach (heatmaps), multi-embedding comparison methodology
- **Cite in paper**: NO

## Papers

### Conceptualizer (Liu et al., ACL 2023)
- **Title**: Conceptualizer: A Framework for Concept Alignment across 1335 Languages
- **Link**: https://arxiv.org/abs/2305.14897
- **Relevance to LinguaGraph**: 5/5
- **What it does**: Aligns concepts across 1335 languages using cross-lingual embeddings. Provides conceptual stability metrics.
- **What's similar**: Both deal with cross-lingual concept alignment and stability
- **Can borrow**: Conceptual stability metric, alignment methodology
- **Cite in paper**: YES

### Cross-Lingual Pitfalls (Xu et al., ACL 2025)
- **Title**: Cross-Lingual Pitfalls: Automatic Probing Cross-Lingual Weakness of Multilingual Large Language Models
- **Link**: https://arxiv.org/abs/2505.18673
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Identifies cross-lingual weaknesses in multilingual LLMs. Shows 50%+ accuracy drops in non-English languages.
- **What's similar**: Both study cross-lingual differences, both find that language matters
- **Can borrow**: Evaluation methodology for cross-lingual comparison
- **Cite in paper**: NO

### MUSE: Unsupervised Multilingual Embeddings (Conneau et al., ICLR 2018)
- **Title**: Unsupervised Cross-lingual Word Embedding Learning by Discriminative Training
- **Link**: https://arxiv.org/abs/1711.00043
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Learns cross-lingual word embeddings without parallel data. Uses adversarial training + refinement.
- **What's similar**: Both deal with cross-lingual alignment without parallel data
- **Can borrow**: Unsupervised alignment methodology
- **Cite in paper**: YES — reference for cross-lingual embedding alignment

### XLM-R (Conneau et al., 2020)
- **Title**: Unsupervised Cross-lingual Representation Learning at Scale
- **Link**: https://arxiv.org/abs/1911.02116
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Scales cross-lingual pre-training to 100 languages with 2.5T filtered CommonCrawl tokens.
- **What's similar**: Both deal with multilingual representation
- **Can borrow**: Scale methodology
- **Cite in paper**: NO

### LASER (Artetxe & Schwenk, 2019)
- **Title**: Language-Agnostic SEntence Representations
- **Link**: https://arxiv.org/abs/1812.10464
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Computes sentence embeddings for 90+ languages using a shared encoder.
- **What's similar**: Both deal with language-agnostic representation
- **Cite in paper**: NO
