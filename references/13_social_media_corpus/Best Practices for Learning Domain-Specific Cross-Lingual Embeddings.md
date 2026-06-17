---
type: social_media
topic: bilingualism
language: en
platform: academic_paper
source_domain: 06_cross_lingual_kg
source_file: Best Practices for Learning Domain-Specific Cross-Lingual Embeddings.md
crawled_at: "2026-06-17T11:12:57.697058+00:00"
content_hash: "d958e2c027ee"
quality: B
status: unverified
tags:
  - bilingualism
  - en
  - academic
  - crawled
---

# Best Practices for Learning Domain-Specific Cross-Lingual Embeddings

**Source:** 06_cross_lingual_kg/Best Practices for Learning Domain-Specific Cross-Lingual Embeddings.md
**Language:** en
**Topic:** bilingualism
**Crawled:** 2026-06-17T11:12:57.697058+00:00

## Content

# Best Practices for Learning Domain-Specific Cross-Lingual Embeddings

**Source:** http://arxiv.org/abs/1907.03112v1
**Crawled:** 2026-06-17
**Authors:** Lena Shakurova, Beata Nyari, Chao Li, Mihai Rotaru

Cross-lingual embeddings aim to represent words in multiple languages in a shared vector space by capturing semantic similarities across languages. They are a crucial component for scaling tasks to multiple languages by transferring knowledge from languages with rich resources to low-resource languages. A common approach to learning cross-lingual embeddings is to train monolingual embeddings separately for each language and learn a linear projection from the monolingual spaces into a shared space, where the mapping relies on a small seed dictionary. While there are high-quality generic seed dictionaries and pre-trained cross-lingual embeddings available for many language pairs, there is little research on how they perform on specialised tasks. In this paper, we investigate the best practices for constructing the seed dictionary for a specific domain. We evaluate the embeddings on the sequence labelling task of Curriculum Vitae parsing and show that the size of a bilingual dictionary, the frequency of the dictionary words in the domain corpora and the source of data (task-specific vs generic) influence the performance. We also show that the less training data is available in the low-resource language, the more the construction of the bilingual dictionary matters, and demonstrate that some of the choices are crucial in the zero-shot transfer learning case.
