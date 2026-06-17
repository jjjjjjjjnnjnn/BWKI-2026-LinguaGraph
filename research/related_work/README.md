# LinguaGraph Related Work Database

## Purpose

Structured database of related GitHub repositories and academic papers for positioning LinguaGraph in the research landscape.

## Search Methodology

1. **Integration first**: Scanned existing `references/` (140+ entries) and `web_research_summary.md` for overlaps
2. **Gap-filling**: Only searched for genuinely missing entries across 5 core areas
3. **Standardized format**: Every entry uses the same template for easy comparison
4. **Relevance scoring**: 1-5 scale based on methodological similarity to LinguaGraph

## Coverage

| Area | Repos | Papers | File |
|------|-------|--------|------|
| ConceptNet / Concept Graphs | 5+ | 5+ | `01_conceptnet.md` |
| WordNet / Lexical Networks | 4+ | 4+ | `02_wordnet.md` |
| BabelNet / Multilingual KG | 5+ | 5+ | `03_babelnet.md` |
| Cross-lingual Embeddings | 4+ | 4+ | `04_cross_lingual_embed.md` |
| KG Visualization | 5+ | 3+ | `05_kg_visualization.md` |
| Human Annotation Agreement | 3+ | 3+ | `06_human_annotation.md` |
| Linguistic Relativity (Computational) | 4+ | 5+ | `07_linguistic_relativity.md` |
| Additional Relevant Work | 3+ | 3+ | `08_additional.md` |
| Future Directions (Phase 2-3) | 3+ | 0 | `09_future_directions.md` |

## Entry Template

```markdown
## [Name]
- **Link**: URL
- **Domain**: □ NLP □ KG □ Cross-lingual □ Visualization □ Annotation
- **Relevance to LinguaGraph**: X/5
- **What it does**: 1-2 sentences
- **What's similar to LinguaGraph**: 
- **What LinguaGraph does differently**: 
- **Can borrow**: 
- **Cannot borrow**: 
- **Cite in paper**: YES/NO
```

## Summary

See `summary.md` for gap analysis and positioning.
