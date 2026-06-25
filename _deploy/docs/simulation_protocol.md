# LinguaGraph — Computational Control Model (Zero-shot Cognitive Baseline)

## Positioning

> **This is NOT a replacement for human data.**
> This is a **computational baseline** — a "zero-shot cognitive simulator" that serves as the control group against which human cognition is compared.

```
Human Data (Ground Truth)          ← Core evidence for BWKI
  vs.
Model Simulation (Baseline)        ← Computational control condition
```

---

## Why This Works

| Argument | Why It's Strong |
|----------|----------------|
| "LLMs encode human cultural knowledge" | Pre-training data includes ZH/DE/EN cultural content |
| "Model predictions can serve as a null model" | If model shows no LDS → human LDS is culturally real |
| "We can test whether linguistic cognition is model-reproducible" | This is the frontier question in computational cognitive science |

---

## Prompt Design Principles

### Principle 1: Persona-driven, NOT language-switching

```
❌ WRONG: "Answer this question in German"
    → Measures translation ability, not cognitive framing

✅ CORRECT: "You are a German native speaker...
    Explain what freedom means to you."
    → Measures cultural-linguistic cognitive framing
```

### Principle 2: Include life context, not just language label

| Language | Persona Elements |
|----------|-----------------|
| ZH | Native Chinese speaker, born and raised in China, school in Chinese, daily life in Chinese |
| DE | Native German speaker, born and raised in Germany, school in German, daily life in German |
| EN | Native English speaker (US/UK), born and raised in English-speaking country |

### Principle 3: Avoid priming specific concepts

```
❌ WRONG: "As a Chinese person, what does freedom mean (think about family, society)?"
    → This injects the hypothesis

✅ CORRECT: "What does freedom mean to you? Explain in your own words."
    → Neural prompt, lets the persona do the work
```

---

## ZH Persona Prompt

```
You are a Chinese native speaker. You were born and raised in China.
You attended school in Chinese. Your daily life and thinking are in Chinese.
You have NOT lived abroad for extended periods.

Please answer the following question naturally, as if you were responding
to a survey. Write 3-5 sentences. There are no right or wrong answers.

Question: 什么是自由? 请用自己的话解释。
```

## DE Persona Prompt

```
You are a German native speaker. You were born and raised in Germany.
You attended school in German. Your daily life and thinking are in German.
You have NOT lived abroad for extended periods.

Please answer the following question naturally, as if you were responding
to a survey. Write 3-5 sentences. There are no right or wrong answers.

Frage: Was ist Freiheit? Erklären Sie in eigenen Worten.
```

## EN Persona Prompt

```
You are an English native speaker from the United States.
You were born and raised in the US. You attended school in English.
Your daily life and thinking are in English.
You have NOT lived abroad for extended periods.

Please answer the following question naturally, as if you were responding
to a survey. Write 3-5 sentences. There are no right or wrong answers.

Question: What is freedom? Explain in your own words.
```

---

## Full Prompt Set (5 Concepts × 3 Languages = 15 Prompts)

| Topic | ZH Prompt | DE Prompt | EN Prompt |
|-------|-----------|-----------|-----------|
| Freedom | 什么是自由? | Was ist Freiheit? | What is freedom? |
| Justice | 什么是公平? | Was ist Gerechtigkeit? | What is justice/fairness? |
| Success | 你的人生目标是什么？ | Was macht ein gutes Leben aus? | What makes a good life? |
| Responsibility | 责任是什么？ | Was bedeutet Verantwortung? | What does responsibility mean? |
| Home | 家对你意味着什么？ | Was bedeutet Heimat? | What does home mean? |

Each uses the same persona prefix:
```
[Persona: {ZH/DE/EN} native speaker, born and raised in {China/Germany/US},
 schooled in {Chinese/German/English}, not lived abroad]

Question: {translated question}

Answer naturally, 3-5 sentences.
```

---

## Data Isolation Protocol

All simulated data MUST be clearly separated from human data.

### Database Separation

All simulation records use:
- `student_id = "SIMULATION"` (not a human participant ID)
- `source = "simulation"` in responses table
- `model_used = "gpt-4.1-mini-simulation"` in extractions table
- A dedicated `simulations` metadata table tracks prompt templates used

### Table: simulation_metadata

```sql
CREATE TABLE IF NOT EXISTS simulation_metadata (
    simulation_id   TEXT PRIMARY KEY,
    model           TEXT NOT NULL,
    persona_lang    TEXT NOT NULL,
    persona_prompt  TEXT NOT NULL,
    temperature     REAL DEFAULT 0.7,
    topic           TEXT NOT NULL,
    num_responses   INTEGER,
    created_at      TEXT DEFAULT (datetime('now'))
);
```

### Directory Separation

```
data/pilot_corpus/
├── freedom/           ← Wikipedia corpus (existing)
├── simulation/
│   ├── prompts/       ← All persona prompts stored here
│   └── responses/     ← LLM-generated responses (JSON)
```

---

## Validation Checks

Before running comparisons, verify:

| Check | What to Test | Pass Criteria |
|-------|-------------|---------------|
| Language match | Does the model actually respond in the target language? | 100% correct language |
| Length match | Are simulation responses similar length to human? | ±20% of human avg |
| Concept diversity | Does simulation produce varied responses across runs? | < 70% identical concept sets |
| No hypothesis leakage | Does the prompt avoid biasing concepts? | Independent audit |

---

## Known Limitations (Document Transparently)

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Model training data includes internet text from all languages | ZH persona may still reflect Western cultural content | Use distinct persona prompts, test for "cultural contamination" |
| LLMs may default to "safe" culturally neutral answers | May underestimate real LDS | Compare distribution width |
| Single model (GPT-4.1) may not generalize | Model-specific results | Note as limitation |
| Prompt sensitivity | Different prompts → different results | Freeze prompt; document exactly |
