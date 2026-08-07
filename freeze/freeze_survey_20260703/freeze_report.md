# Dataset Freeze: survey_20260703

**Freeze date**: 2026-07-04
**Pipeline version**: 1.0

## Summary

| Metric | Value |
|--------|-------|
| Total submitted | 18 |
| Eligible (final) | 11 |
|   Clean pass | 3 |
|   With flags (manual review) | 8 |
| Excluded | 7 |

### Language distribution

| Language | N |
|----------|---|
| de | 6 |
| zh | 5 |

### Duration statistics (eligible, seconds)

| Metric | Value |
|--------|-------|
| Median | 424 |
| Mean | 537.2 |
| Range | 140 -- 1305 |

## QC Check Pass Rates

| Check | Pass | Flag (review) | Failed | Pass rate |
|-------|:----:|:-------------:|:------:|:---------:|
| completeness | 18 | 0 | 0 | 100.0% |
| duplicate | 18 | 0 | 0 | 100.0% |
| duration | 14 | 4 | 0 | 77.8% |
| language | 18 | 0 | 0 | 100.0% |
| metadata | 11 | 0 | 7 | 61.1% |
| min_length | 3 | 15 | 0 | 16.7% |
| refusal | 17 | 0 | 1 | 94.4% |

## Exclusion Reasons

- [de] TEST_002: metadata: No consent recorded
- [de] DIAG_001: metadata: No consent recorded
- [zh] DIAG_002: refusal: 'Freiheit' gibberish: '��ϲ���'; Overall response appears to be spam/gibberish; metadata: No consent recorded
- [de] JSON_TEST: metadata: No consent recorded
- [zh] WORKER_JSON_TEST: metadata: No consent recorded
- [zh] NOCORS_TEST: metadata: No consent recorded
- [en] FINAL_TEST: metadata: No consent recorded

## Items Flagged for Manual Review

- [de] TEST_002 (min_length): min_length: Only 2/5 meet paragraph length (50 chars)
- [de] TEST_002 (duration): duration: Fast completion: 15s (threshold: 60s)
- [de] R20260701_DE_EKJHH6 (min_length): min_length: 'Q1' too short (48 < 50 chars)
- [de] R20260701_DE_TFF14F (min_length): min_length: 'Q5' too short (42 < 50 chars)
- [zh] R20260702_ZH_JHZK4J (min_length): min_length: 'Q2' too short (33 < 50 chars); 'Q3' too short (36 < 50 chars); 'Q4' too short (30 < 50 chars); 'Q5' too sho
- [zh] R20260702_ZH_YP7IMU (min_length): min_length: 'Q1' too short (34 < 50 chars); 'Q2' too short (36 < 50 chars); 'Q4' too short (40 < 50 chars); 'Q5' too sho
- [de] R20260702_DE_HMH36H (min_length): min_length: 'Q4' too short (40 < 50 chars)
- [de] R20260702_DE_CWJRV8 (min_length): min_length: 'Q1' too short (49 < 50 chars); 'Q4' too short (45 < 50 chars); 'Q5' too short (47 < 50 chars); Only 2/5 mee
- [zh] R20260702_ZH_XBTVBA (min_length): min_length: 'Q2' too short (40 < 50 chars); 'Q3' too short (40 < 50 chars); 'Q4' too short (48 < 50 chars); 'Q5' too sho
- [de] DIAG_001 (min_length): min_length: 'Freiheit' too short (10 < 50 chars); Only 0/5 meet paragraph length (50 chars)
- [de] DIAG_001 (duration): duration: Fast completion: 15s (threshold: 60s)
- [zh] DIAG_002 (min_length): min_length: 'Freiheit' too short (6 < 50 chars); Only 0/5 meet paragraph length (50 chars)
- [de] JSON_TEST (min_length): min_length: 'Freiheit' too short (31 < 50 chars); Only 0/5 meet paragraph length (50 chars)
- [de] JSON_TEST (duration): duration: Fast completion: 10s (threshold: 60s)
- [zh] WORKER_JSON_TEST (min_length): min_length: '����' too short (22 < 50 chars); Only 0/5 meet paragraph length (50 chars)
- [zh] WORKER_JSON_TEST (duration): duration: Fast completion: 20s (threshold: 60s)
- [zh] NOCORS_TEST (min_length): min_length: '����' too short (10 < 50 chars); Only 0/5 meet paragraph length (50 chars)
- [en] FINAL_TEST (min_length): min_length: 'Freedom' too short (21 < 50 chars); Only 0/5 meet paragraph length (50 chars)
- [zh] R20260703_ZH_SR1JIR (min_length): min_length: 'Q4' too short (31 < 50 chars); 'Q5' too short (32 < 50 chars)
