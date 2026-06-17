# Area 3: BabelNet / Multilingual Knowledge Graphs

## Repositories

### BabelNet API (Python)
- **Link**: https://github.com/jackee777/babelnetpy (33 ⭐)
- **Domain**: ☑ NLP ☑ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Python interface to BabelNet — a multilingual semantic network combining WordNet + Wikipedia. 150+ languages, 15M+ concepts, 350M+ edges.
- **What's similar to LinguaGraph**: Both deal with cross-lingual concept representation. Both use graph structure.
- **What LinguaGraph does differently**: BabelNet is a pre-built multilingual KB; LinguaGraph extracts cognitive graphs from individual responses. BabelNet is encyclopedic; LinguaGraph is cognitive.
- **Can borrow**: Cross-lingual concept alignment, multilingual graph structure
- **Cannot borrow**: BabelNet's crowdsourced + Wikipedia approach
- **Cite in paper**: YES — key comparison for multilingual KGs

### BabelNet-Sememe-Prediction
- **Link**: https://github.com/thunlp/BabelNet-Sememe-Prediction (20 ⭐)
- **Domain**: ☑ NLP ☑ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Predicts sememes (minimal semantic units) for BabelNet synsets. Builds a multilingual sememe knowledge base.
- **What's similar**: Both deal with fine-grained semantic analysis across languages
- **Can borrow**: Sememe-based concept decomposition, multilingual evaluation
- **Cite in paper**: NO

### Framester
- **Link**: https://github.com/alammehwish/framester (11 ⭐)
- **Domain**: ☑ NLP ☑ KG □ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 2/5
- **What it does**: Hub connecting FrameNet, WordNet, VerbNet, BabelNet, DBpedia, YAGO, DOLCE. Formal frame semantics with OWL querying.
- **What's similar**: Both combine multiple knowledge resources
- **What LinguaGraph does differently**: Framester is about ontology integration; LinguaGraph is about cognitive graph comparison
- **Cite in paper**: NO

### Language-Agnostic Ontology Extension Framework
- **Link**: https://github.com/revabharara/Language-Agnostic-Ontology-Extension-Framework (existing reference)
- **Domain**: ☑ NLP ☑ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Integrates ontologies with knowledge graphs for structured knowledge organization and semantic analysis. Language-agnostic approach.
- **What's similar**: Both aim for language-independent semantic analysis
- **Can borrow**: Ontology-KG integration pattern
- **Cite in paper**: NO

### CCAligned
- **Link**: https://github.com/facebookresearch/ccaligned (48 ⭐)
- **Domain**: ☑ NLP □ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Massive parallel corpus of 100M+ sentence pairs from Wikipedia across 97 languages. Enables cross-lingual NLP research.
- **What's similar**: Both need cross-lingual data; CCAligned provides aligned text pairs
- **Can borrow**: Parallel corpus methodology, cross-lingual evaluation approach
- **Cannot borrow**: Corpus-level approach (LinguaGraph works at the individual response level)
- **Cite in paper**: YES — reference for cross-lingual data methodology

## Papers

### BabelNet (Navigli & Ponzetto, 2012)
- **Title**: BabelNet: The Automatic Construction, Evaluation and Application of a Wide-Coverage Multilingual Semantic Network
- **Link**: https://aclanthology.org/J12-4004/
- **Relevance to LinguaGraph**: 5/5
- **What it does**: Automatically constructs a multilingual semantic network from Wikipedia + WordNet. 150+ languages. Evaluates on word similarity, translation, and WSD tasks.
- **What's similar**: Both create multilingual semantic graphs. Both need cross-lingual concept alignment.
- **What LinguaGraph does differently**: BabelNet is a universal KB; LinguaGraph extracts per-person cognitive graphs. BabelNet measures semantic similarity; LinguaGraph measures cognitive structural difference.
- **Can borrow**: Evaluation methodology, cross-lingual alignment approach
- **Cite in paper**: YES — key comparison

### CCKG: Cultural Commonsense Knowledge Graph (EACL 2026)
- **Title**: CCKG: A Cultural Commonsense Knowledge Graph
- **Link**: Referenced in methodology.md
- **Relevance to LinguaGraph**: 5/5
- **What it does**: Builds culturally-specific commonsense knowledge graphs for different cultures. Shows that commonsense knowledge varies across cultural contexts.
- **What's similar**: Both argue that knowledge is culturally situated. Both build culture-specific knowledge representations.
- **What LinguaGraph does differently**: CCKG is static cultural KB; LinguaGraph extracts from individual cognitive responses. CCKG focuses on cultural commonsense; LinguaGraph focuses on linguistic-cognitive structure.
- **Can borrow**: Cultural annotation methodology, cross-cultural evaluation metrics
- **Cite in paper**: YES — very close conceptual alignment

### RISE: Riemannian Geometry for Cross-Lingual Semantics (ICLR 2026)
- **Title**: RISE: Riemannian Isometry for Cross-Lingual Semantic Embeddings
- **Link**: Referenced in methodology.md
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Uses Riemannian geometry to model cross-lingual semantic differences. Proposes a geometric framework for understanding how meaning changes across languages.
- **What's similar**: Both model cross-lingual semantic differences quantitatively
- **What LinguaGraph does differently**: RISE uses geometric embeddings; LinguaGraph uses graph-level comparison. RISE is purely mathematical; LinguaGraph includes visualization.
- **Can borrow**: Mathematical framework for measuring semantic drift
- **Cite in paper**: YES — methodological comparison

### Separating Tongue from Thought (ACL 2025)
- **Title**: Separating Tongue from Thought: Activation Patching Reveals Language-Independent Thought in Multilingual LMs
- **Link**: Referenced in methodology.md
- **Relevance to LinguaGraph**: 5/5
- **What it does**: Uses activation patching in multilingual LMs to show that some concepts are language-independent while others are language-dependent. Directly tests Sapir-Whorf computationally.
- **What's similar**: Both address whether language shapes thought. Both use computational methods to test linguistic relativity.
- **What LinguaGraph does differently**: This paper uses mechanistic interpretability on LMs; LinguaGraph uses graph comparison of human responses. Different methods, same question.
- **Can borrow**: Experimental design for testing linguistic relativity, evaluation framework
- **Cite in paper**: YES — directly comparable work

### Multilingual Knowledge Graph Completion (Sun et al., 2019)
- **Title**: Cross-lingual Knowledge Graph Alignment and Completion
- **Link**: https://aclanthology.org/P19-1519/
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Proposes methods for aligning and completing knowledge graphs across languages using multilingual embeddings.
- **What's similar**: Both deal with cross-lingual KG alignment
- **Can borrow**: Alignment evaluation metrics
- **Cite in paper**: NO
