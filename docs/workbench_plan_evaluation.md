# LinguaGraph Workbench — Project Plan Evaluation

> **Date**: 2026-06-21
> **Purpose**: Evaluate the "LinguaGraph Workbench" product vision against existing project plans and constraints

---

## 1. Current State Assessment

### What we have (built and working)

| Component | Status | Notes |
|-----------|--------|-------|
| Textbook corpus (68) | ✅ Complete | 45 ZH + 20 EN + 10 DE |
| Concept extraction | ✅ Complete | MIMO pipeline, 75 JSON files |
| Knowledge graph (CognitiveSpace) | ✅ Complete | 574 nodes, 3538 edges |
| Cross-language alignment | ✅ Complete | 247 trilingual, 30 shared IDs |
| CognitiveSpace 3D viz | ✅ Complete | Deployable, frozen |
| Gold Dataset schema | ✅ Complete | A + C task families defined |
| LDS metric | ✅ Frozen (defined) | Needs human data |
| GitHub repo | ✅ Clean | Research-ready structure |

### What's missing (before submission)

| Item | Dependency | Timeline |
|------|-----------|----------|
| DE/EN human data | External (recruitment) | Jul–Aug |
| LDS results | Human data | After data |
| Complete paper draft | All of the above | Aug |
| Application demos | Pipeline complete | Now–Jul |

### Frozen items (not to be changed)

| Item | Reason |
|------|--------|
| LDS definition | Would invalidate all prior analysis |
| Pipeline architecture | Would break reproducibility |
| Concept mapping (30 IDs) | Would break cross-language alignment |
| Corpus expansion | Scope control |

---

## 2. The "LinguaGraph Workbench" Proposal — Evaluation

### What it is

A web-based interface that wraps the existing pipeline into a usable product:

```
Upload textbook (PDF/txt)
    ↓
Select language (ZH/EN/DE)
    ↓
[System runs: extraction → graph → alignment → LDS]
    ↓
View: Knowledge Graph + CognitiveSpace 3D + Analysis Report
```

### Compatibility with frozen items

| Workbench Feature | Conflicts with frozen items? |
|------------------|------------------------------|
| File upload | No (new UI layer) |
| Extraction trigger | No (uses existing pipeline) |
| Graph construction | No (uses existing code) |
| LDS computation | No (uses existing metric) |
| 3D visualization | No (uses CognitiveSpace) |
| Analysis report | No (new output format) |

**Verdict**: The Workbench uses existing components. It does NOT change any frozen item.

### Effort estimate

| Feature | Effort | Reuses |
|---------|--------|--------|
| Simple web UI (upload + trigger) | 2–3 days | Flask/FastAPI |
| Pipeline integration (call existing scripts) | 1 day | `scripts/run_pipeline.py` |
| Report generation (PDF summary) | 2 days | `outputs/export_pipeline.py` |
| CognitiveSpace embedding | 0.5 day | `cognitive-space/web/` |
| **Total MVP** | **~6 days** | |

### Risk analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| Distraction from paper writing | Medium | Build MVP in 1 week, then freeze |
| Web deployment complexity | Low | Flask + localhost sufficient for demo |
| Pipeline integration bugs | Low | All components already tested |
| User authentication/security | None | Local-only tool, no PII processing |

---

## 3. Comparison: Existing Plan vs Workbench Addition

### Existing plan (from PRIORITIES.md, Jun 18)

```
Next 2 weeks:
40%  Pilot data collection
25%  Results pipeline automation
20%  Three.js / UI / visualization
10%  Paper charts & diagrams
 5%  Local model evaluation
```

### Proposed updated plan (with Workbench)

```
Next 2 weeks:
35%  Pilot data collection          (unchanged, -5%)
20%  Results pipeline automation     (unchanged, -5%)
10%  LinguaGraph Workbench MVP       (NEW)
20%  CognitiveSpace polish + cases   (unchanged)
10%  Paper charts & diagrams         (unchanged)
 5%  Local model evaluation          (unchanged)
```

The Workbench takes 10% from the least critical items. The core research path (data collection + paper) stays at 55%.

---

## 4. Recommendation

### ✅ Adopt, but with strict boundaries

The Workbench is a **presentation layer** for the existing system. It does not change frozen items and directly addresses the "who would use this?" question from reviewers.

### Adoption rules

1. **Scope**: Web UI that wraps existing pipeline scripts. No new extraction, graph, or LDS code.
2. **Timeline**: 1 week MVP, then freeze. No feature creep.
3. **Architecture**: Keep it simple — Flask (or even static HTML + JS calling a backend). CognitiveSpace already works standalone.
4. **Deliverable**: A runnable demo that shows "upload → analyze → visualize" in under 30 seconds.

### Not included in MVP

| Feature | Reason |
|---------|--------|
| User accounts | Overkill for demo |
| Cloud deployment | Local demo sufficient |
| Real-time processing | Pipeline already fast enough |
| Multi-language document support | Focus on ZH/EN/DE only |
| PDF parsing | Focus on plain text input |

---

## 5. Updated Project Roadmap (Jun 21 → Sep 21)

```
Phase A (Jun 21–28): Foundation
  ✅ CognitiveSpace frozen
  ✅ Paper outline + abstract + methodology written
  ✅ GitHub repo cleaned and pushed
  ▶ Workbench design (this document)
  ⏳ Gold Dataset schema finalized

Phase B (Jul 1–31): Data + Pipeline
  ⏳ DE/EN pilot data collection (3+3+3)
  ⏳ LinguaGraph Workbench MVP
  ⏳ Application cases A + B documented
  ⏳ Gold Dataset generation scripts

Phase C (Aug 1–31): Results + Paper
  ⏳ Full LDS results from human data
  ⏳ Paper figures + tables
  ⏳ Complete paper draft
  ⏳ Gold Dataset v1 release

Phase D (Sep 1–21): Final Polish
  ⏳ Paper review + revisions
  ⏳ Demo video (2-3 min)
  ⏳ Poster preparation
  ⏳ Final submission package
```

---

## 6. Verdict

**Adopt the Workbench vision**, constrained to a 1-week MVP, because:

1. ✅ It addresses the reviewer question: "who would use this?"
2. ✅ It uses existing frozen components (no new research risk)
3. ✅ It bridges theory (LDS) to practice (usable tool)
4. ✅ It makes CognitiveSpace feel like part of a product, not a standalone viz
5. ⚠️ Must NOT expand beyond 1 week or change frozen items

The Workbench is the right answer to the question:

> "My findings — how does it become something others can use, understand, and benefit from?"
