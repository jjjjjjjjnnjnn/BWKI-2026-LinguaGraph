# LinguaGraph — Pilot Quality Report

**Generated:** 2026-06-19 11:44

**Snapshot:** pilot_v1 (frozen)

## 1. Completion

| Metric | Value |
|--------|:-----:|
| Participants | 8 |
| Expected responses | 80 |
| Actual responses | 80 |
| Completion rate | 100.0% |
| Missing answers | 0 |

## 2. Per-Participant

| ID | Lang | Got | Expected | Complete |
|----|:----:|:---:|:--------:|:--------:|
| P001 | zh | 10 | 10 | ✅ |
| P002 | zh | 10 | 10 | ✅ |
| P003 | zh | 10 | 10 | ✅ |
| P004 | zh | 10 | 10 | ✅ |
| P005 | zh | 10 | 10 | ✅ |
| P006 | zh | 10 | 10 | ✅ |
| P007 | zh | 10 | 10 | ✅ |
| P008 | zh | 10 | 10 | ✅ |

## 3. Language Distribution

| Language | Responses |
|:--------:|:---------:|
| zh | 80 (100%) ████████████████████ |

## 4. Response Quality

| Metric | Value |
|--------|:-----:|
| Average word count | 16.3 |
| Min word count | 2 |
| Max word count | 57 |
| Short answers (<5 chars) | 8 (10.0%) |
| Language-mixed answers | 7 (8.8%) |

### Short Answers:

- P001 q10_emotion_reaction: "口误🤓"
- P003 q17_robot_description: "智能护士"
- P004 q17_robot_description: "医疗助手"
- P006 q15_picture_exchange: "书拿去"
- P006 q17_robot_description: "护工"

## 5. Known Issues

- P006 q12: Residual characters from previous question ('杯子zai')
- P003 q12: Incomplete translation (missing 'through living room')
- P003 q16: Metaphorical interpretation deviating from source
- q14: 'brought forward' systematically misunderstood by 4/8 participants

## 6. Lessons Learned

- Question order matters: P006 q12 contamination suggests spacing/attention issues
- Translation difficulty varies: 'brought forward' widely misinterpreted
- Age range matters: 10-55 spanning 4 decades enables generational analysis
- Instruction clarity: q3 (12_year_old) translation was uniquely creative

## 7. Planned Improvements

- Separate screens per question (prevent carryover contamination)
- Add example translations for tricky phrases (e.g., 'brought forward')
- Standardize age format before collection
- Collect response time metadata if platform allows