# Area 6: Human Annotation Agreement / Inter-Annotator Reliability

## Repositories

### nltk (Natural Language Toolkit)
- **Link**: https://github.com/nltk/nltk (13000+ ⭐)
- **Domain**: ☑ NLP □ KG □ Cross-lingual □ Visualization ☑ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Standard Python NLP library with annotation agreement tools (Cohen's Kappa, Kappa agreement, etc.)
- **What's similar**: Both need inter-annotator agreement measurement
- **Can borrow**: Kappa computation, annotation workflow patterns
- **Cite in paper**: YES — standard NLP toolkit reference

### scikit-learn
- **Link**: https://github.com/scikit-learn/scikit-learn (61000+ ⭐)
- **Domain**: ☑ NLP □ KG □ Cross-lingual □ Visualization ☑ Annotation
- **Relevance to LinguaGraph**: 2/5
- **What it does**: Standard ML library with cohen_kappa_score, classification reports, confusion matrices.
- **What's similar**: Both need statistical evaluation tools
- **Can borrow**: kappa_score, classification_report
- **Cite in paper**: NO (too general)

### jiwer
- **Link**: https://github.com/jitsi/jiwer (1800+ ⭐)
- **Domain**: ☑ NLP □ KG □ Cross-lingual □ Visualization ☑ Annotation
- **Relevance to LinguaGraph**: 2/5
- **What it does**: Word Error Rate (WER) and Character Error Rate (CER) computation. Used for transcript evaluation.
- **What's similar**: Both deal with text similarity measurement
- **What LinguaGraph does differently**: jiwer measures surface-level text similarity; LinguaGraph measures semantic/cognitive similarity
- **Cite in paper**: NO

### Dawid-Skene
- **Link**: https://github.com/dawid-skene/dawid-skene-python (50+ ⭐)
- **Domain**: □ NLP □ KG □ Cross-lingual □ Visualization ☑ Annotation
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Implements Dawid-Skene model for aggregating noisy crowd annotations. Estimates true labels from multiple imperfect annotators.
- **What's similar**: Both deal with annotation quality and aggregation
- **Can borrow**: Annotation aggregation methodology
- **Cite in paper**: NO

### AnnotationStudio
- **Link**: https://github.com/annotation-studio/annotation-studio (200+ ⭐)
- **Domain**: □ NLP □ KG □ Cross-lingual □ Visualization ☑ Annotation
- **Relevance to LinguaGraph**: 2/5
- **What it does**: Web-based text annotation tool with collaborative features, NER, sentiment, relation annotation.
- **What's similar**: Both need annotation infrastructure
- **Can borrow**: Annotation UI patterns, inter-annotator agreement reporting
- **Cite in paper**: NO

## Papers

### Cohen's Kappa (Cohen, 1960)
- **Title**: A Coefficient of Agreement for Nominal Scales
- **Link**: https://psycnet.apa.org/record/1960-04681-001
- **Relevance to LinguaGraph**: 5/5
- **What it does**: Introduces Cohen's Kappa — the standard metric for inter-annotator agreement on categorical labels. Corrects for chance agreement.
- **What's similar**: LinguaGraph needs to measure agreement on concept extraction (are two annotators extracting the same concepts?)
- **Can borrow**: Kappa computation, interpretation guidelines (0.61-0.80 = substantial, 0.81-1.00 = almost perfect)
- **Cite in paper**: YES — essential for annotation evaluation

### Krippendorff's Alpha (Krippendorff, 2004)
- **Title**: Content Analysis: An Introduction to Its Methodology
- **Link**: https://doi.org/10.4324/9781315803241
- **Relevance to LinguaGraph**: 5/5
- **What it does**: Generalizes Cohen's Kappa to handle: (1) multiple annotators, (2) missing data, (3) different data types. The gold standard for content analysis reliability.
- **What's similar**: LinguaGraph may have multiple annotators per response; alpha handles this better than kappa
- **Can borrow**: Alpha computation, handling of missing annotations
- **Cite in paper**: YES — preferred over Cohen's Kappa for multi-annotator settings

### Fleiss' Kappa (Fleiss, 1971)
- **Title**: Measuring Nominal Scale Agreement Among Many Raters
- **Link**: https://doi.org/10.1037/h0031619
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Extends Cohen's Kappa to more than 2 annotators. Measures agreement on nominal scales with multiple raters.
- **What's similar**: LinguaGraph may have 3+ annotators per concept extraction task
- **Can borrow**: Multi-rater kappa computation
- **Cite in paper**: YES — if 3+ annotators per item

### Measuring Agreement on Item-by-Item Basis (Gwet, 2014)
- **Title**: Handbook of Inter-Rater Reliability (4th ed.)
- **Link**: https://www.gwet.net/
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Comprehensive handbook covering kappa, alpha, and other agreement coefficients. Discusses edge cases and alternatives.
- **Can borrow**: Decision framework for choosing the right agreement metric
- **Cite in paper**: NO (reference book, not primary source)

### Annotation Guidelines for Knowledge Extraction (Pustejovsky & Stubbs, 2012)
- **Title**: Natural Language Annotation for Machine Learning
- **Link**: https://dl.acm.org/doi/10.1093/acprof:oso/9780195362626.001.0001
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Textbook on annotation methodology for NLP. Covers schema design, annotation workflow, reliability measurement, and guidelines writing.
- **What's similar**: LinguaGraph needs annotation guidelines for concept extraction (currently in docs/annotation_guideline_v2.md)
- **Can borrow**: Annotation schema design, guideline writing methodology, quality control workflow
- **Cite in paper**: YES — methodological reference for annotation design
