# LinguaGraph Research Loop Runbook

**Pattern:** Sequential (research-focused)
**Mode:** safe
**Stop condition:** All 5 topics have ≥50 texts per language AND LDS computed

## Current State

| Topic | zh | en | de | LDS | Status |
|-------|----|----|-----|-----|--------|
| freedom | 42 | 36 | 41 | 0.735 | DONE |
| justice | 35 | 37 | 33 | — | ERROR (encoding) |
| responsibility | 46 | 41 | 35 | 0.707 | DONE |
| success | 0 | 0 | 0 | — | NO DATA |
| home | 0 | 0 | 0 | — | NO DATA |

## Loop Iterations

### Iteration 1: Fill Data Gaps
- [ ] Collect success topic (3 languages × 50 texts)
- [ ] Collect home topic (3 languages × 50 texts)
- [ ] Fix justice encoding issue

### Iteration 2: Full Pipeline Run
- [ ] Run research_loop.py on all 5 topics
- [ ] Verify LDS computed for all topics
- [ ] Review failure cases

### Iteration 3: Report Consolidation
- [ ] Generate final pilot study report
- [ ] Update pilot-study.md with all findings
- [ ] Create visualization data

## Commands

```bash
# Fill data gaps
python experiments/collect_fast.py

# Run full loop
python run_loop.py

# Check results
cat research/loop_summary.json
```
