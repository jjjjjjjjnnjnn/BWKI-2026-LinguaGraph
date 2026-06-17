# Area 7: Linguistic Relativity / Computational Sapir-Whorf

## Repositories

### Cross-Lingual-Pitfalls
- **Link**: https://github.com/xzx34/Cross-Lingual-Pitfalls
- **Domain**: ☑ NLP □ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Automatic probing of cross-lingual weaknesses in multilingual LLMs. Generates bilingual question pairs that expose performance discrepancies. 6000+ pairs across 16 languages.
- **What's similar to LinguaGraph**: Both study how language affects representation/processing. Both compare performance across languages.
- **What LinguaGraph does differently**: Cross-Lingual-Pitfalls studies LM weaknesses; LinguaGraph studies human cognitive differences. Different subjects, same underlying question.
- **Can borrow**: Bilingual pair generation methodology, evaluation framework
- **Cite in paper**: YES — related computational approach to linguistic relativity

### NLP-Color-Evolution
- **Link**: (multiple repos studying color terms cross-lingually)
- **Domain**: ☑ NLP □ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Studies how color naming differs across languages — classic Sapir-Whorf test case. Uses computational methods to measure color boundary differences.
- **What's similar**: Both study linguistic relativity computationally
- **Can borrow**: Evaluation methodology for linguistic relativity testing
- **Cite in paper**: YES — classic test case reference

### Color Naming Cross-Lingual
- **Link**: Various repos on color naming across languages
- **Domain**: ☑ NLP □ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Multiple projects study how languages carve up the color spectrum differently. Berlin & Kay (1969) established that color terms follow universal patterns with language-specific variation.
- **What's similar**: Both study how language categorizes experience
- **Can borrow**: Experimental design patterns, evaluation metrics
- **Cite in paper**: YES — foundational linguistic relativity reference

### WordNet-Based Semantic Drift
- **Link**: Various repos studying semantic shift across languages
- **Domain**: ☑ NLP □ KG ☑ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Studies how word meanings shift across languages and time. Uses WordNet + distributional semantics.
- **What's similar**: Both measure semantic/cognitive differences across languages
- **Can borrow**: Semantic drift measurement methodology
- **Cite in paper**: NO

## Papers

### Separating Tongue from Thought (ACL 2025)
- **Title**: Separating Tongue from Thought: Activation Patching Reveals Language-Independent Thought in Multilingual LMs
- **Link**: https://arxiv.org/abs/2502.05602 (referenced in methodology.md)
- **Relevance to LinguaGraph**: 5/5
- **What it does**: Uses activation patching in multilingual LMs to show that some conceptual operations are language-independent while others are language-dependent. Directly tests Sapir-Whorf computationally.
- **What's similar**: Both address "does language shape thought?" Both use computational methods.
- **What LinguaGraph does differently**: This paper uses LM internals; LinguaGraph uses human response graphs. Different methods, same question.
- **Can borrow**: Experimental design for testing linguistic relativity, classification of language-dependent vs independent concepts
- **Cite in paper**: YES — directly comparable work

### The Sapir-Whorf Hypothesis (Whorf, 1956)
- **Title**: Language, Thought, and Reality
- **Link**: Classic reference
- **Relevance to LinguaGraph**: 5/5
- **What it does**: Original formulation: language determines (strong version) or influences (weak version) thought and cognitive categories.
- **What's similar**: LinguaGraph IS a computational test of Sapir-Whorf
- **Cite in paper**: YES — foundational reference

### Color Naming and Categorization (Berlin & Kay, 1969)
- **Title**: Basic Color Terms: Their Universality and Evolution
- **Link**: Classic reference
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Foundational study showing that color terms follow universal patterns across languages, with language-specific variation at the boundaries.
- **What's similar**: Both study how language categorizes experience
- **Cite in paper**: YES — classic test case

### Thinking for Speaking (Slobin, 1996)
- **Title**: From "Thought and Language" to "Thinking for Speaking"
- **Link**: https://doi.org/10.1017/CBO9781139173437.007
- **Relevance to LinguaGraph**: 5/5
- **What it does**: Proposes "thinking for speaking" — the idea that language forces speakers to attend to certain aspects of experience during speech production. Refines Sapir-Whorf.
- **What's similar**: LinguaGraph measures exactly this — how different languages lead to different conceptual structures in free-form responses
- **Cite in paper**: YES — theoretical foundation

### The We思维 (Boroditsky, 2001)
- **Title**: Does Language Shape Thought? Mandarin and English Speakers' Conceptions of Time
- **Link**: https://doi.org/10.1037/0033-2909.127.1.62
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Empirical study showing that Mandarin speakers (vertical time) and English speakers (horizontal time) think about time differently. Classic evidence for linguistic relativity.
- **What's similar**: Both study how language-specific structures affect cognition
- **Cite in paper**: YES — empirical evidence for linguistic relativity

### L1 Influence on L2 (Jarvis & Pavlenko, 2008)
- **Title**: Crosslinguistic Influence in Language and Cognition
- **Link**: https://doi.org/10.4324/9780203946893
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Comprehensive review of crosslinguistic influence — how L1 affects L2 processing. Covers conceptual transfer, lexical transfer, and structural transfer.
- **What's similar**: Both deal with cross-lingual cognitive differences
- **Cite in paper**: YES — reference for cross-lingual cognition

### Cultural Relativity (Nisbett, 2003)
- **Title**: The Geography of Thought: How Asians and Westerners Think Differently...and Why
- **Link**: https://doi.org/10.1037/10895-000
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Argues that cultural differences in thought (holistic vs analytic) are real and measurable. Uses language as one explanatory variable.
- **What's similar**: Both study cross-cultural cognitive differences
- **Cite in paper**: YES — cultural psychology reference
