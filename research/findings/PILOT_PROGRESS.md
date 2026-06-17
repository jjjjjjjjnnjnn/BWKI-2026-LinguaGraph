# LinguaGraph Pilot Study — Cross-Language Analysis Progress

## Method
- **v2**: Cross-language concept mapping applied (see `config/cross_language_mapping.json`)
- Prevents LCD false positives by mapping `权利/Recht/right` → shared ID `rights`
- Source: Wikipedia articles per language

## Completed (4/20 concepts)

### Concept 1: Freedom / 自由 / Freiheit ✅
| Pair | LCD | Shared | Chinese-unique | German-unique | English-unique |
|------|-----|--------|---------------|--------------|---------------|
| zh-de | 0.8209 | 9 | individual, liberation, socialism, family | reason, security, equality | — |
| zh-en | 0.6140 | 12 | liberation, socialism, family, society | — | (none) |
| de-en | 0.8718 | 6 | — | reason, security, equality, economy | domination, free will, democracy |
**Universal core**: freedom, rights, autonomy, speech, religion, philosophy

### Concept 2: Justice / 公平 / Gerechtigkeit ✅
| Pair | LCD | Shared | Chinese-unique | German-unique | English-unique |
|------|-----|--------|---------------|--------------|---------------|
| zh-de | 0.8913 | 5 | education, family, domination, economy | reason, progress, religion | — |
| zh-en | 0.6989 | 8 | education, family, security, domination | — | history, power, religion |
| de-en | 0.8765 | 5 | — | reason, progress, security, success | economy, history, power, law |
**Universal core**: equality, justice, philosophy, society

### Concept 3: Responsibility / 责任 / Verantwortung ✅
| Pair | LCD | Shared | Unique insights |
|------|-----|--------|----------------|
| zh-de | 0.8810 | 5 | ZH moral/legal lens (justice, law, rights); DE institutional (education, choice, history) |
| zh-en | 0.7727 | 6 | ZH adds family, equality; EN narrower (free will, law, society) |
| de-en | 0.8378 | 4 | DE choice/education/history; EN free will/law |
**Universal core**: freedom, philosophy, responsibility, society

### Concept 4: Success / 成功 / Erfolg ✅
| Pair | LCD | Shared | Unique insights |
|------|-----|--------|----------------|
| zh-de | 1.0000 | 1 | ZH broad (family, education, society, history, progress); DE business-only frame |
| zh-en | 0.9167 | 3 | ZH broad (economy, family, history, society); EN moderate (education, individual) |
| de-en | 1.0000 | 1 | DE purely financial/business; EN educational/individual |
**Key insight**: German "Erfolg" is semantically narrow (business result); Chinese 成功 is socially embedded; English success straddles both.

## Global Patterns (across all 4 concepts)
- **zh-en consistently lowest LCD** (0.61–0.92): Chinese-English share more conceptual overlap
- **zh-de and de-en consistently higher LCD** (0.82–1.00): German conceptual structure is more distinct
- **Chinese consistently adds**: family, society, education — social embeddedness dimension
- **German consistently adds**: reason, economy, security — systematic/institutional dimension
- **English consistently adds**: individual rights, free will — liberal political dimension

## Remaining concepts (next session)
5. **Democracy / 民主 / Demokratie**
6. **Equality / 平等 / Gleichheit**
7. **Family / 家庭 / Familie**
8. **Education / 教育 / Bildung**
9. **Identity / 身份 / Identität**
10. **Power / 权力 / Macht**
11. **Progress / 进步 / Fortschritt**
12. **History / 历史 / Geschichte**
13–20: To be selected based on initial findings

## Questionnaire suggestions (accumulated)
1. "Is freedom more about individual rights or social responsibility?"
2. "Can freedom conflict with security? How would you resolve this?"
3. "Does economic freedom contradict social equality?"
4. "How important are education and family to your understanding of justice?"
5. "Is success defined by personal achievement or social contribution?"
6. "Does true responsibility require free will, or can it exist without it?"
7. "Is equality of opportunity more important than equality of outcome?"
8. "What does democracy mean to you — voting rights or daily participation?"

## Database
- `cross_language_analysis` table: 12 rows (4 concepts × 3 language pairs)
- Source corpus: `data/pilot_corpus/{freedom,justice,responsibility,success}/`
- Analyzer: `research/analyze_concept.py`
- Concept mapping: `config/cross_language_mapping.json`
