# LinguaGraph — Human Recruitment Infrastructure

> Status: P0 — Critical Path for ΔLDS
> Target: N = 30 (10 ZH, 10 DE, 10 EN)
> Current: N = 8
> Gap: 22 participants

---

## 1. Participant Requirements

| Criteria | Specification |
|----------|---------------|
| Language group ZH | Native Mandarin speaker, educated in Chinese system |
| Language group DE | Native German speaker, educated in German system |
| Language group EN | Native English speaker, educated in English system |
| Bilingual (DE-EN) | DE group only: proficient in English (self-reported B2+) |
| Exclusion | Formal linguistics training, translation studies, cognitive science |
| Age range | 18–35 |
| Education | Currently enrolled in or completed university |

## 2. Survey Architecture

### 2.1 Frontend (Static HTML, hostable on GitHub Pages)

```
human-survey/
├── index.html          # Consent form + language selection
├── survey.html         # Main questionnaire (5 topics)
├── debrief.html        # Debriefing page
├── i18n.js             # ZH/EN/DE translations
├── style.css
└── data.js             # Responses stored as JSON in localStorage
```

### 2.2 Data Flow

```
Participant opens index.html
        │
        ▼
Language selection → stored in localStorage
        │
        ▼
Consent form → "I agree" checkbox required
        │
        ▼
Questionnaire: 5 open-ended prompts
  Each prompt: "Please describe what [TOPIC] means to you..."
  Input: textarea (minimum 30 characters)
  Order: randomized per participant (Latin square)
        │
        ▼
Debrief → thank you + explanation
        │
        ▼
Data export: JSON blob via download button
  (or researcher-administered collection via manual copy)
```

### 2.3 Topic Prompts

| # | Topic | Prompt (EN) |
|---|-------|-------------|
| 1 | Freedom | "Please describe what freedom means to you. What concepts or ideas are most important for understanding freedom?" |
| 2 | Justice | "Please describe what justice means to you. What concepts or ideas are most important for understanding justice?" |
| 3 | Responsibility | "Please describe what responsibility means to you. What concepts or ideas are most important for understanding responsibility?" |
| 4 | Home | "Please describe what home means to you. What concepts or ideas are most important for understanding home?" |
| 5 | Success | "Please describe what success means to you. What concepts or ideas are most important for understanding success?" |

Each available in ZH/EN/DE. Order randomized per participant.

## 3. Data Quality Checks

### 3.1 Automatic (Client-Side)

| Check | Threshold | Action |
|-------|-----------|--------|
| Minimum length | ≥ 30 characters per response | Prevent submit, show warning |
| Copy-paste detection | Levenshtein ratio between responses | Flag for review |
| Empty concept extraction | LLM extracts 0 concepts | Mark as invalid |
| Completion time | < 60 seconds for 5 questions | Flag as rushed |

### 3.2 Manual (Post-Collection)

| Check | Criterion |
|-------|-----------|
| Response relevance | Does the response address the topic? |
| Language proficiency | Is the response in the correct language? |
| Extraction quality | Does LLM extraction produce valid concepts? |
| Within-subject consistency | Do bilingual responses show reasonable variation? |

### 3.3 Exclusion Criteria

Exclude participant if:
- Any automatic check triggers twice (2+ short responses)
- Language mismatch (ZH participant writing in EN)
- All 5 responses fail extraction (LLM returns empty for all)
- Response appears LLM-generated (checked by researcher)
- Bilingual participant fails >1 shared concept check

## 4. Recruitment Pipeline

### 4.1 Channels

| Channel | Target Group | Expected Yield | Cost |
|---------|-------------|:--------------:|:----:|
| University mailing lists | ZH, EN | 5-10 | Free |
| Social media (ZH: WeChat, DE: Discord, EN: Reddit) | All | 5-8 | Free |
| Personal networks | All | 3-5 | Free |
| University participant pools (SONA, Prolific) | EN | 10-15 | €100-200 |

### 4.2 Recruitment Materials

Each channel needs:
1. **Call for participation** (1 paragraph + link)
2. **Informed consent form** (ZH/EN/DE) — already exists in `docs/ethics/`
3. **Debriefing document** (ZH/EN/DE)

### 4.3 Timeline

| Week | Action | Milestone |
|:----:|--------|:---------:|
| 1 | Deploy survey; start ZH recruitment via WeChat | N=10 |
| 2 | Start DE recruitment via Discord/university | N=15 |
| 3 | Start EN recruitment via SONA/Prolific | N=20 |
| 4 | Follow-up; check data quality | N=25 |
| 5 | Final push | **N=30** |

## 5. ΔLDS Analysis Plan (After N ≥ 30)

### 5.1 Primary Analysis

```python
# 1. Compute LDS-C for each language pair
lds_c = {
    "ZH-EN": compute_lds(human_data, "zh", "en"),
    "DE-EN": compute_lds(human_data, "de", "en"),
    "ZH-DE": compute_lds(human_data, "zh", "de"),
}

# 2. Compute ΔLDS = LDS-C - LDS-K
delta_lds = {
    pair: lds_c[pair] - lds_k[pair]
    for pair in lds_c
}

# 3. Test H2: LDS-C > LDS-K (one-tailed paired t-test)
t_stat, p_value = paired_ttest(
    list(lds_c.values()),
    list(lds_k.values()),
    alternative="greater"
)

# 4. Test H3: ΔLDS > 0 (one-sample t-test)
t_stat, p_value = one_sample_ttest(
    list(delta_lds.values()),
    mu=0,
    alternative="greater"
)
```

### 5.2 Bootstrap CI

Compute 95% CI for each ΔLDS via bootstrapping participants with replacement.

### 5.3 Effect Size

Report Cohen's d for ΔLDS, and interpret against thresholds (small/medium/large).

### 5.4 Sensitivity Checks

- Exclude participants with rushed responses
- Exclude participants with failed extraction (partial)
- Compare qwen-plus vs best alternative model (hy3-preview)
- Relax node alignment threshold

---

## 6. Current Status

| Item | Status | Owner |
|------|--------|-------|
| Informed consent (ZH/EN/DE) | ✅ Done | Ethics review |
| Survey prompts (ZH/EN/DE) | ✅ Done | Prior experiment |
| Survey frontend | ❌ Not built | — |
| Data quality checks | ⚠️ Partial (post-hoc) | Need automated |
| Recruitment materials | ❌ Not written | — |
| Recruitment channels | ❌ Not contacted | — |
| ΔLDS analysis code | ❌ Not written | — |

## 7. Immediate Next Steps

1. Build survey frontend (single HTML file, no server needed)
2. Write recruitment call in ZH/EN/DE
3. Deploy via GitHub Pages
4. Begin recruitment
5. Collect until N ≥ 30
6. Run ΔLDS analysis
