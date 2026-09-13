# LinguaGraph Methodology

## Linguistic Divergence Score (LDS)

### Definition

The Linguistic Divergence Score quantifies how differently two languages organize the same conceptual space. It is defined as:

```
LDS(L1, L2) = 1 - mean(GED_sim, Jaccard_node, Jaccard_edge)
```

Where:
- `GED_sim` = normalized Graph Edit Distance similarity ∈ [0, 1]
- `Jaccard_node` = node set Jaccard similarity ∈ [0, 1]
- `Jaccard_edge` = edge set Jaccard similarity ∈ [0, 1]

### Interpretation

| LDS Value | Interpretation |
|-----------|---------------|
| 0.0 | Identical cognitive structures |
| 0.0 - 0.3 | Low drift — similar thinking patterns |
| 0.3 - 0.7 | Moderate drift — notable structural differences |
| 0.7 - 1.0 | High drift — fundamentally different organizations |

### Algorithm

1. **Concept Extraction**: Extract concepts from text responses using LLM or keyword matching
2. **Graph Construction**: Build directed graphs where nodes = concepts, edges = relations
3. **Pairwise Comparison**: For each language pair (zh↔de, zh↔en, de↔en):
   - Compute GED similarity
   - Compute node Jaccard
   - Compute edge Jaccard
   - Average → combined similarity
4. **LDS Calculation**: LDS = 1 - combined_similarity

### Complexity

- Graph Edit Distance: O(n³) worst case (NP-hard in general, but NetworkX uses exact algorithm for small graphs)
- Jaccard: O(n) where n = number of nodes/edges
- Overall: O(n³) dominated by GED

### Limitations

1. GED computation is exact but slow for graphs >15 nodes
2. Node matching is string-exact (no semantic similarity)
3. Edge matching considers only relation type, not strength
4. Assumes concepts are independently extracted per language
5. **GED fallback**: Graph Edit Distance is NP-hard; when computation fails on large graphs, the fallback value is `GED_sim = 0.5` (see `src/scoring.py:166`)

## Conceptual Stability

Based on the Conceptualizer methodology (Liu et al., ACL 2023), conceptual stability measures how consistently a concept is represented across languages.

```
stability(concept) = mean(concreteness_proxy, cross_lingual_overlap)
```

Where:
- `concreteness_proxy` = 1/(1 + variance_in_word_lengths)
- `cross_lingual_overlap` = average character overlap across language pairs

## References

1. Conceptualizer: 1335-language concept alignment (ACL 2023)
2. CCKG: Cultural Commonsense Knowledge Graph (EACL 2026)
3. RISE: Riemannian geometry for cross-lingual semantics (ICLR 2026)
4. Separating Tongue from Thought: activation patching (ACL 2025)
