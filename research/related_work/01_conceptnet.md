# Area 1: ConceptNet / Concept Graphs / Text Semantic Networks

## Repositories

### ConceptNet5
- **Link**: https://github.com/commonsense/conceptnet5 (2943 ⭐)
- **Domain**: □ NLP ☑ KG □ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 4/5
- **What it does**: The canonical commonsense knowledge graph. 21M+ nodes, 35M+ edges across 50 languages. Nodes are concepts (words/phrases), edges are relations (IsA, HasProperty, UsedFor, etc.).
- **What's similar to LinguaGraph**: Both use concept-as-node, relation-as-edge graph structures. Both aim to represent how concepts relate to each other.
- **What LinguaGraph does differently**: ConceptNet is a static, crowdsourced KB. LinguaGraph extracts dynamic cognitive graphs from individual human responses. ConceptNet says "what humans know"; LinguaGraph says "how a specific language community organizes concepts."
- **Can borrow**: Relation taxonomy (IsA, HasProperty, etc.), concept normalization methods, multilingual concept alignment
- **Cannot borrow**: crowdsourcing methodology (LinguaGraph uses LLM extraction + human annotation), evaluation framework (ConceptNet evaluates KB quality, not cognitive differences)
- **Cite in paper**: YES — foundational reference

### ConceptNet Numberbatch
- **Link**: https://github.com/commonsense/conceptnet-numberbatch (1322 ⭐)
- **Domain**: ☑ NLP ☑ KG □ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Pre-trained ConceptNet embeddings (word vectors). State-of-the-art word vectors that combine ConceptNet with WordNet, Wiktionary, and distributional statistics. 50+ languages.
- **What's similar to LinguaGraph**: Both use multilingual concept representations. Numberbatch provides vector-based cross-lingual concept similarity.
- **What LinguaGraph does differently**: Numberbatch computes static similarity; LinguaGraph computes structural/graph-level differences. Numberbatch answers "how close are these words?" LinguaGraph answers "how differently are these concepts organized in different minds?"
- **Can borrow**: Cross-lingual concept alignment method, evaluation metrics for semantic similarity
- **Cannot borrow**: Embedding-based approach (LinguaGraph uses graph structure, not vectors)
- **Cite in paper**: YES — for cross-lingual concept alignment baseline

### CoCo-Ex
- **Link**: https://github.com/Heidelberg-NLP/CoCo-Ex (59 ⭐)
- **Domain**: ☑ NLP ☑ KG □ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 5/5
- **What it does**: Extracts meaningful concepts from natural language text and maps them to ConceptNet nodes. Uses contextualized embeddings for concept extraction.
- **What's similar to LinguaGraph**: Both extract concepts from text and map to knowledge graph nodes. Both bridge raw text → structured concept representation.
- **What LinguaGraph does differently**: CoCo-Ex maps to a pre-existing KB; LinguaGraph builds its own graphs from scratch. CoCo-Ex is a concept extraction tool; LinguaGraph is a comparison framework.
- **Can borrow**: Concept extraction pipeline, ConceptNet mapping strategy, evaluation methodology
- **Cannot borrow**: Single-language focus (LinguaGraph needs multilingual extraction)
- **Cite in paper**: YES — methodological reference for concept extraction

### ConceptNet Lite
- **Link**: https://github.com/ldtoolkit/conceptnet-lite (73 ⭐)
- **Domain**: □ NLP ☑ KG □ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 2/5
- **What it does**: Lightweight Python wrapper for offline ConceptNet access without PostgreSQL. Enables local graph traversal.
- **What's similar to LinguaGraph**: Both use graph-based concept representation with Python.
- **What LinguaGraph does differently**: LinguaGraph builds its own graphs; ConceptNet-Lite queries an existing KB.
- **Can borrow**: Local graph traversal patterns
- **Cannot borrow**: Architecture (LinguaGraph doesn't use ConceptNet as backend)
- **Cite in paper**: NO

### CauseNet
- **Link**: https://github.com/causenet-org/CIKM-20 (77 ⭐)
- **Domain**: ☑ NLP ☑ KG □ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Extracts causal relations from web text to build a causality graph. Focuses on cause-effect structure.
- **What's similar to LinguaGraph**: Both extract relational structure from text to build graphs. Both go beyond bag-of-words to capture meaning structure.
- **What LinguaGraph does differently**: CauseNet focuses on causality only; LinguaGraph captures diverse relation types. CauseNet is English-only; LinguaGraph is trilingual.
- **Can borrow**: Web-scale extraction methodology, relation validation techniques
- **Cannot borrow**: Single-relation focus
- **Cite in paper**: NO

## Papers

### ConceptNet5 (Havasi et al., 2017)
- **Title**: ConceptNet 5.5: A Multilingual Graph of Common Sense
- **Link**: https://arxiv.org/abs/1612.03975
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Describes ConceptNet 5.5 with 21M nodes and 35M edges across 50 languages. Evaluated on word similarity and analogy tasks.
- **What's similar**: Both deal with multilingual concept representation
- **Can borrow**: Evaluation methodology (MEN, RW, SimLex benchmarks), multilingual alignment approach
- **Cite in paper**: YES

### ATOMIC (Sap et al., 2019)
- **Title**: ATOMIC: An Atlas of Machine Commonsense for If-Then Reasoning
- **Link**: https://arxiv.org/abs/1908.06165
- **Relevance to LinguaGraph**: 3/5
- **What it does**: 880K if-then commonsense tuples across 23 relation types (xIntent, xEffect, xAttr, etc.). Focuses on social commonsense.
- **What's similar**: Both capture relational structure between concepts, both use typed edges
- **Can borrow**: Relation taxonomy design, graph construction methodology
- **Cite in paper**: YES — as comparison for relation design

### A Data-Driven Study of Commonsense Knowledge (Shen & Kejriwal, 2020)
- **Title**: A Data-Driven Study of Commonsense Knowledge using the ConceptNet Knowledge Base
- **Link**: https://arxiv.org/abs/2011.14084
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Systematic structural analysis of ConceptNet using unsupervised graph representation learning and clustering. Reveals substructures in commonsense relations.
- **What's similar**: Both analyze graph structure of commonsense knowledge, both use graph-level metrics
- **Can borrow**: Analysis methodology (embedding + clustering for graph structure analysis)
- **Cite in paper**: YES — methodological reference for graph analysis

### Understanding Substructures in Commonsense Relations (Shen & Kejriwal, 2022)
- **Title**: Understanding Substructures in Commonsense Relations in ConceptNet
- **Link**: https://arxiv.org/abs/2210.01263
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Reveals that "official" ConceptNet relations (HasContext, FormOf, SymbolOf) have hidden substructures that could be refined.
- **What's similar**: Both challenge simple relation taxonomies, both look deeper into how concepts are connected
- **Can borrow**: Subdivision methodology, visualization of graph substructures
- **Cite in paper**: NO (niche)

### Conceptualizer (Liu et al., ACL 2023)
- **Title**: Conceptualizer: A Framework for Concept Alignment across 1335 Languages
- **Link**: Referenced in methodology.md
- **Relevance to LinguaGraph**: 5/5
- **What it does**: Aligns concepts across 1335 languages using cross-lingual embeddings. Provides a framework for measuring conceptual overlap.
- **What's similar**: Both deal with cross-lingual concept alignment, both want to measure how concepts differ across languages
- **What LinguaGraph does differently**: Conceptualizer uses embedding similarity; LinguaGraph uses graph structure comparison. Conceptualizer is large-scale automated; LinguaGraph is deep cognitive analysis.
- **Can borrow**: Cross-lingual alignment methodology, evaluation framework
- **Cannot borrow**: Embedding-based approach (LinguaGraph uses graph-level comparison)
- **Cite in paper**: YES — core methodological reference
