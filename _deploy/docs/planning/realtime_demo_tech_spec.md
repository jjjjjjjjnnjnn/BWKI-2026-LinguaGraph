# LinguaGraph — Real-Time Demo Technical Specification
## Live LDS Visualization for Jury Presentation
## Version 1.0 | 2026-06-25

---

## 1. Overview

**Goal**: A juror types a concept (e.g., "Freiheit") into a portal field. Within 3 seconds, the system displays the concept's cognitive graph in ZH/DE/EN side-by-side, with LDS values computed in real time.

**Success Criteria**:
- Input → visual output in < 3 seconds
- Works offline via pre-computed cache for 20+ common concepts
- Falls back gracefully to pre-recorded video if live demo fails

---

## 2. Architecture

```
┌─────────────────┐
│  User Input     │  Concept name → e.g. "Freiheit"
└────────┬────────┘
         │
    ┌────▼────┐
    │ Cache?  │──Yes──► Serve from cache (< 100ms)
    └────┬────┘
         │ No
    ┌────▼──────────────────────┐
    │ Wikipedia API (3 parallel) │
    │ ZH article | DE article | EN│
    └────┬──────────────────────┘
         │
    ┌────▼────────────────────────┐
    │ qwen-plus Extraction (3x)  │  ← Bailian API
    └────┬────────────────────────┘
         │
    ┌────▼──────────┐
    │ Build 3 Graphs │  ← networkx (browser: graphology.js)
    └────┬──────────┘
         │
    ┌────▼────────────┐
    │ Compute LDS (3)  │  ← 3 language pairs
    └────┬────────────┘
         │
    ┌────▼──────────────────────┐
    │ Visual Output             │
    │ 3-column graph + LDS table│
    └───────────────────────────┘
```

---

## 3. Pre-Computed Cache Strategy

### Why Cache

- Wikipedia API latency: 500ms-2s per article
- qwen-plus extraction latency: 500ms-2s per language
- Total worst case: ~4s — too slow for live demo
- **Cache brings response to < 100ms for known concepts**

### Cache Contents

```json
{
  "freedom": {
    "zh": {"concepts": ["自由", "权利", "选择", ...], "relations": [...]},
    "de": {"concepts": ["Freiheit", "Recht", "Selbstbestimmung", ...], "relations": [...]},
    "en": {"concepts": ["freedom", "rights", "choice", ...], "relations": [...]},
    "lds": {"zh-de": 0.519, "de-en": 0.938, "zh-en": 0.934}
  },
  ...
}
```

### Cache Population

**Phase 1 (pre-event)**: Batch extract 30 common concepts (Wikipedia articles)
**Phase 2 (event day)**: Pre-warm cache; pre-load graphs

### Cache Invalidation

Never during the demo. Cache is static for the event.

---

## 4. Frontend Implementation

### Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Graph visualization | graphology.js + sigma.js | Pure JS, no server needed |
| LDS computation | Custom JS port of `src/scoring.py` | Browser-side for speed |
| Concept extraction | Pre-computed cache (no API during demo) | Reliability |
| Fallback | Pre-recorded MP4 video | Ultimate safety net |

### UI Layout

```
┌─────────────────────────────────────────────────────┐
│  LinguaGraph — Live LDS Demo                        │
├─────────────────────────────────────────────────────┤
│  [_____________________________] [Analyze]           │  ← Input field
│  or select: [Freedom ▼] [Justice ▼] [Success ▼]     │  ← Quick-select
├──────────────────┬──────────────────┬────────────────┤
│  🇨🇳 中文 (ZH)   │  🇩🇪 Deutsch (DE) │  🇬🇧 English (EN)│
│  [graph nodes]   │  [graph nodes]   │  [graph nodes]  │
│  10 concepts     │  8 concepts      │  8 concepts     │
│  12 edges        │  10 edges        │  11 edges       │
├──────────────────┴──────────────────┴────────────────┤
│  LDS Matrix                                         │
│  ┌─────────┬─────────┬─────────┐                    │
│  │         │ DE      │ EN      │                    │
│  ├─────────┼─────────┼─────────┤                    │
│  │ ZH      │ 0.52    │ 0.93    │                    │
│  │ DE      │ —       │ 0.94    │                    │
│  └─────────┴─────────┴─────────┘                    │
├─────────────────────────────────────────────────────┤
│  ↑ Language pair convergence: ZH-DE=0.52, ZH-EN=0.93, DE-EN=0.94      │
│  ZH-EN lowest — consistent across all three levels  │
└─────────────────────────────────────────────────────┘
```

### LDS Computation (JavaScript Port)

```javascript
function computeLDS(graphA, graphB) {
  // Node Jaccard
  const nodesA = new Set(graphA.nodes.map(n => n.id));
  const nodesB = new Set(graphB.nodes.map(n => n.id));
  const intersection = new Set([...nodesA].filter(x => nodesB.has(x)));
  const union = new Set([...nodesA, ...nodesB]);
  const nodeJaccard = intersection.size / Math.max(union.size, 1);

  // Edge Jaccard
  const edgesA = new Set(graphA.edges.map(e => `${e.source}-${e.target}`));
  const edgesB = new Set(graphB.edges.map(e => `${e.source}-${e.target}`));
  const edgeIntersection = new Set([...edgesA].filter(x => edgesB.has(x)));
  const edgeUnion = new Set([...edgesA, ...edgesB]);
  const edgeJaccard = edgeIntersection.size / Math.max(edgeUnion.size, 1);

  // GED approximation (simplified for browser)
  const sizeDiff = Math.abs(graphA.nodes.length - graphB.nodes.length);
  const maxSize = Math.max(graphA.nodes.length, graphB.nodes.length);
  const gedSim = 1 - (sizeDiff + Math.abs(graphA.edges.length - graphB.edges.length)) /
                 Math.max(maxSize + Math.max(graphA.edges.length, graphB.edges.length), 1);

  const combined = (gedSim + nodeJaccard + edgeJaccard) / 3;
  return 1 - combined;
}
```

---

## 5. Fallback: Pre-Recorded Demo Video

### When to Use

- Network unavailable
- API rate-limited
- Any component fails

### Video Spec

| Parameter | Value |
|-----------|-------|
| Duration | 2 minutes |
| Format | MP4 (H.264 + AAC) |
| Resolution | 1920×1080 |
| Content | 5 concepts demo (Freedom, Justice, Success, Responsibility, Home) |
| Framerate | 30 fps (screen recording) |

### Script

```
Scene 1 (0:00-0:15): Portal homepage with Finding C (LDS heatmap)
Scene 2 (0:15-0:45): Type "Freiheit" → tri-lingual graph appears → LDS matrix populates
Scene 3 (0:45-1:15): Type "Gerechtigkeit" → same process
Scene 4 (1:15-1:45): Comparison table: 5 concepts, 3 pairs, LDS values
Scene 5 (1:45-2:00): "Language shapes knowledge — and we can measure it."
```

---

## 6. Implementation Plan

| Step | Action | Time | Dependencies |
|------|--------|------|--------------|
| 1 | Build concept cache (30 concepts) | 2 hours | qwen-plus API access |
| 2 | Port LDS to JavaScript | 1 hour | `src/scoring.py` |
| 3 | Build demo HTML page | 4 hours | graphology.js, sigma.js |
| 4 | Test with 5 concepts | 1 hour | Cache populated |
| 5 | Record fallback video | 1 hour | OBS Studio |
| 6 | Integrate into Portal | 2 hours | Existing portal HTML |
| **Total** | **~11 hours** | | |

---

## 7. Files

```
cognitive-space/portal/
├── demo/
│   ├── live.html          ← Standalone live demo page
│   ├── demo.js            ← JavaScript LDS + graph renderer
│   ├── concept_cache.json ← Pre-computed concept graphs
│   └── fallback_demo.mp4  ← Pre-recorded fallback video
```

---

## 8. Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| qwen-plus API down | Serve entirely from cache |
| Browser JS performance | Cap graph at 50 nodes; use Web Worker for LDS |
| Graph rendering too slow | Pre-layout graphs in cache; only re-color on display |
| Demo laptop dies | USB with MP4 fallback + printed slides |
