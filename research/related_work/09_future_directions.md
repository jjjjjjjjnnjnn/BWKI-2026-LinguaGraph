# Supplementary: Future Directions & Inspiration (BWKI Phase 2-3)

> **Source**: User research compilation, 2026-06-17
> **Purpose**: Future-phase inspiration. NOT for current BWKI submission.
> **Status**: Reference only — no code changes to LinguaGraph.

---

## Filter Criteria

| Relevance | Action |
|-----------|--------|
| ☑ Directly useful for LinguaGraph BWKI | Add to main related_work/ |
| ◐ Useful for future Phase 2-3 expansion | Add here (this file) |
| ✗ Out of scope (TCM, ancient docs, AGI) | Noted but not added |

---

## Tier 1: Directly Useful for LinguaGraph (Add to main database)

### Concordia (Google DeepMind)
- **Link**: https://github.com/google-deepmind/concordia
- **License**: Apache 2.0
- **Relevance to LinguaGraph**: 4/5
- **What it does**: Generative agent simulation library. Agents have memory, personality, and social behavior. Uses a "Game Master" architecture for environment simulation.
- **What's similar**: Multi-agent social simulation with city/neighborhood metaphor
- **Future use**: Phase 3 — "Chinese Agent City / German Agent City / English Agent City" where agents of different linguistic backgrounds discuss the same topics. Compare agent LDS vs human LDS.
- **Can borrow**: Agent memory architecture, social simulation patterns, city-based visualization
- **Cannot borrow**: Game Master architecture (too complex for BWKI scope)
- **Cite in paper**: NO (future direction, not current work)

### AI Town (a16z)
- **Link**: https://github.com/a16z-infra/ai-town
- **License**: MIT
- **Relevance to LinguaGraph**: 3/5
- **What it does**: 2D town simulation with autonomous agents. Agents have memory, reflection, planning, movement, and对话. Browser-based visualization.
- **What's similar**: City metaphor for knowledge organization, agent-based social simulation
- **Future use**: Inspiration for Cognitive City visualization — agents moving between concept buildings, visualizing how different language communities navigate the same conceptual space
- **Can borrow**: 2D/3D city visualization patterns, agent movement animation
- **Cannot borrow**: Full agent lifecycle (too complex)
- **Cite in paper**: NO (visualization inspiration)

### MetaMind
- **Link**: https://github.com/MetaMindResearch/MetaMind (verify availability)
- **Relevance to LinguaGraph**: 3/5
- **What it does**: Multi-agent framework based on Theory of Mind (ToM). Three协作 phases: ToM agent → moral agent → response agent. First LLM to reach human-level on ToM tasks.
- **What's similar**: Theory of Mind = understanding others' mental states. Cross-cultural cognition = understanding how different cultures conceptualize the same ideas. These overlap.
- **Future use**: Phase 3 — test whether LLMs can predict cross-cultural cognitive differences
- **Can borrow**: ToM evaluation methodology
- **Cannot borrow**: Full framework
- **Cite in paper**: NO (future direction)

---

## Tier 2: Useful Pipeline Patterns (Reference only)

### Graphify
- **Link**: https://github.com/anthropics/graphify (verify)
- **Relevance to LinguaGraph**: 2/5
- **What it does**: Zero-config knowledge graph construction from any file type. No vector DB needed — uses graph algorithms for clustering. Saves 71.5x token cost.
- **What's similar**: Knowledge graph construction from documents
- **What LinguaGraph does differently**: LinguaGraph extracts from human responses, not documents
- **Can borrow**: Lightweight graph construction pattern (no vector DB)
- **Cite in paper**: NO

### he-wiki-rag
- **Link**: https://github.com/anthropics/he-wiki-rag (verify)
- **Relevance to LinguaGraph**: 2/5
- **What it does**: Chapter-tree indexing for RAG. BGE-M3 + BM25 + Rerank three-stage hybrid retrieval.
- **What's similar**: Document structure preservation
- **What LinguaGraph does differently**: LinguaGraph doesn't do RAG — it does extraction + comparison
- **Can borrow**: Chapter-tree indexing concept (useful for reference management)
- **Cite in paper**: NO

### shiji-kb (Ancient Text → Knowledge Graph)
- **Link**: https://github.com/anthropics/shiji-kb (verify)
- **Relevance to LinguaGraph**: 2/5
- **What it does**: Converts 《史记》(577K characters) into structured knowledge graph. 15,190 entities, 3,198 events extracted.
- **What's similar**: Text → KG pipeline, entity extraction, relation extraction
- **What LinguaGraph does different**: shiji-kb is for historical texts; LinguaGraph is for cognitive responses
- **Can borrow**: Pipeline architecture (extract → normalize → graph → compare)
- **Cite in paper**: NO

### AncientDoc (ByteDance)
- **Link**: https://github.com/bytedance/AncientDoc (verify)
- **Relevance to LinguaGraph**: 1/5
- **What it does**: Benchmark for evaluating VLMs on Chinese ancient documents. 100+ books, 3000+ pages from Warring States to Qing Dynasty.
- **What's similar**: VLM evaluation methodology
- **What LinguaGraph does different**: Different domain entirely
- **Can borrow**: Evaluation methodology pattern
- **Cite in paper**: NO

---

## Tier 3: Out of Scope (Noted but NOT added)

These projects are interesting but do NOT serve LinguaGraph's current goals:

| Project | Why excluded |
|---------|-------------|
| MaxKB | Enterprise RAG system — not relevant to cognitive graph comparison |
| BetterRAG | Multimodal RAG — LinguaGraph is text-only |
| FrankSherlock | Image search engine — wrong domain |
| Photon | Image processing pipeline — wrong domain |
| OpenTCM / TCMChat | Traditional Chinese Medicine — completely different field |
| nihaisha-nishi-tcm | TCM course notes — completely different field |
| Sibelium | Artificial consciousness — too speculative |
| WalnutiQ | Brain simulation — too low-level |
| Emergent-Cognition-Framework | Theoretical AGI — no practical value |
| Brain-constrained neural model | Neuroscience simulation — wrong level |
| DisRNN | Interpretable RNNs — wrong paradigm |
| cogniarch | Generic cognitive architecture — too broad |
| Cognito Simulation Engine | AGI toolkit — wrong scope |
| cognitive-kit | MCP server — wrong tool type |
| HugAgent | Individual reasoning benchmark — tangential |
| Theory of Mind AI Library | ToM for chatbots — tangential |
| PyETR | Reasoning theory — too theoretical |
| Microsoft Anthropomorphic Intelligence | AI persona evaluation — tangential |
| Aura Research | Document wiki compiler — not relevant |
| LLM Wiki | Document to wiki — not relevant |

---

## Phase 3 Roadmap (AI Simulation Baseline)

If LinguaGraph completes the BWKI submission successfully, the natural next step is:

```
Phase 1 (current): Human LDS
  ↓
Phase 2: Human experiment (30 participants)
  ↓
Phase 3: AI LDS
  - GPT-4.1 playing "Chinese person"
  - GPT-4.1 playing "German person"
  - GPT-4.1 playing "American person"
  - Same questionnaire, same pipeline
  ↓
Phase 4: Human LDS vs AI LDS comparison
  - Research question: Do LLMs capture cross-cultural cognitive differences?
  - This is a publishable paper on its own
```

Concordia and AI Town provide architectural inspiration for Phase 3.

---

## Copyright & Attribution

| Project | License | Attribution Required |
|---------|---------|---------------------|
| Concordia | Apache 2.0 | Yes — include LICENSE notice |
| AI Town | MIT | Yes — include copyright notice |
| MetaMind | Verify license | Check before use |
| Graphify | Verify license | Check before use |
| he-wiki-rag | Verify license | Check before use |
| shiji-kb | Verify license | Check before use |
| AncientDoc | Verify license | Check before use |

All projects are open-source. No proprietary code is being copied. This document is for research reference only.
