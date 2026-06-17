# Area 2: WordNet / Lexical Networks / Word Sense Disambiguation

## Repositories

### English WordNet
- **Link**: https://github.com/globalwordnet/english-wordnet (809 ⭐)
- **Domain**: ☑ NLP ☑ KG □ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: The Open English WordNet — a lexical database organizing words into synsets (sets of synonyms) with hierarchical relations (hypernymy, hyponymy, meronymy).
- **What's similar to LinguaGraph**: Both represent word/concept relationships as graphs. Both organize knowledge into structured semantic networks.
- **What LinguaGraph does differently**: WordNet is hand-crafted by linguists; LinguaGraph extracts from real human responses. WordNet is language-specific; LinguaGraph is cross-lingual. WordNet captures lexical relations; LinguaGraph captures cognitive associations.
- **Can borrow**: Synset hierarchy design, evaluation metrics for lexical networks
- **Cannot borrow**: Static lexical approach (LinguaGraph needs dynamic cognitive graphs)
- **Cite in paper**: YES — foundational reference for lexical networks

### Open Multilingual WordNet (OMW)
- **Link**: https://github.com/globalwordnet/OMW (76 ⭐)
- **Domain**: ☑ NLP ☑ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Unifies WordNets for 100+ languages through a shared ontology. Enables cross-lingual lexical comparison.
- **What's similar**: Both compare concepts across languages. Both need cross-lingual concept alignment.
- **What LinguaGraph does differently**: OMW aligns at the lexical level (synset correspondence); LinguaGraph aligns at the cognitive level (how humans organize concepts). OMW uses dictionary-based alignment; LinguaGraph uses LLM extraction + graph comparison.
- **Can borrow**: Cross-lingual alignment strategy, shared ontology design, language coverage evaluation
- **Cannot borrow**: Lexicographic methodology (LinguaGraph extracts from free-form text, not dictionary entries)
- **Cite in paper**: YES — reference for cross-lingual lexical alignment

### YAGO3
- **Link**: https://github.com/yago-naga/yago3 (752 ⭐)
- **Domain**: ☑ NLP ☑ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Large semantic knowledge base derived from Wikipedia, WordNet, WikiData, and GeoNames. 50M+ facts, multilingual.
- **What's similar**: Both combine multiple knowledge sources, both are multilingual
- **What LinguaGraph does differently**: YAGO is an encyclopedic KB (entities + facts); LinguaGraph is a cognitive graph (concepts + associations). YAGO stores what exists; LinguaGraph stores how people think.
- **Can borrow**: Entity alignment methodology, multilingual graph construction
- **Cite in paper**: NO (too encyclopedic, not cognitive)

### pywsd
- **Link**: https://github.com/alvations/pywsd (748 ⭐)
- **Domain**: ☑ NLP □ KG □ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 2/5
- **What it does**: Python implementations of Word Sense Disambiguation (WSD) — determining which meaning of a word is used in context.
- **What's similar**: Both deal with concept meaning in context
- **What LinguaGraph does differently**: WSD is about disambiguating word senses; LinguaGraph is about mapping cognitive structure. Different problems.
- **Can borrow**: WSD evaluation methodology (could be useful for concept extraction quality)
- **Cite in paper**: NO

### wn (Open Multilingual Wordnet for Python)
- **Link**: https://github.com/goodmami/wn (292 ⭐)
- **Domain**: ☑ NLP ☑ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Modern interlingual WordNet interface for Python. Supports querying across multiple language WordNets.
- **What's similar**: Both provide Python API for cross-lingual concept lookup
- **What LinguaGraph does differently**: wn is a query interface; LinguaGraph is a graph construction + comparison pipeline
- **Can borrow**: Multi-language API design, interlingual mapping approach
- **Cite in paper**: NO

## Papers

### WordNet (Miller, 1995)
- **Title**: WordNet: A Lexical Database for English
- **Link**: https://dl.acm.org/doi/10.1145/219717.219748
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Introduces WordNet — organizing English words into synsets with hierarchical semantic relations. Foundational work in computational lexical semantics.
- **What's similar**: Both create graph representations of semantic knowledge
- **Can borrow**: Evaluation methodology for lexical graphs
- **Cite in paper**: YES — foundational reference

### Open Multilingual Wordnet (Bond et al., 2016)
- **Title**: Open Multilingual Wordnet
- **Link**: https://aclanthology.org/P16-1035/
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Describes the project of connecting WordNets across 100+ languages through a shared interlingual index.
- **What's similar**: Both deal with cross-lingual concept alignment
- **Can borrow**: Alignment methodology, coverage evaluation
- **Cite in paper**: YES — reference for cross-lingual lexical alignment

### EuroWordNet (Vossen, 1998)
- **Title**: EuroWordNet: A Multilingual Database with Lexical Semantic Networks
- **Link**: https://link.springer.com/chapter/10.1007/978-94-011-4826-9_11
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Multilingual lexical database with language-specific WordNets connected through an interlingual index (ILI). Covers 8 European languages.
- **What's similar**: Both compare semantic structures across languages
- **Can borrow**: Interlingual index design, cross-lingual sense alignment
- **Cite in paper**: YES — historical reference for multilingual lexical networks

### Multilingual WSD (Navigli & Ponzetto, 2012)
- **Title**: BabelNet: The Automatic Construction, Evaluation and Application of a Wide-Coverage Multilingual Semantic Network
- **Link**: https://aclanthology.org/J12-4004/
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Introduces BabelNet by combining WordNet with Wikipedia. Automatic construction of multilingual semantic network. (Covered in detail in Area 3.)
- **What's similar**: Both combine lexical + encyclopedic knowledge across languages
- **Cite in paper**: YES
