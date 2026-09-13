# LinguaGraph — 3-Minute Pitch (v2, AI-Audit-Framing)

> For project presentations, lab meetings, short talks
> **Stand:** 2026-08-09 | ersetzt v1 (Textbuch-Rahmen, überholt)
> **Narrativer Kern:** LinguaGraph ist ein Audit-Werkzeug für mehrsprachige KI — es misst, ob ein Modell wertbeladene Konzepte sprachübergreifend konsistent versteht, und wo genau nicht.

---

## 1. The Problem (30s)

AI systems are deployed to billions of people in dozens of languages — but they are trained mostly on English data. Does a model's understanding of value-laden concepts — justice, freedom, responsibility — stay consistent across languages?

Standard AI evaluation measures **task performance**, not conceptual consistency. If a model in a loan-decision or content-moderation system frames "fairness" differently in German than in Chinese, users get inconsistent treatment depending on language. **That blind spot is unmeasured.**

## 2. The Method (45s)

How do you measure something invisible like a model's concept structure? **Ask the AI itself.**

LinguaGraph makes the LLM a controlled experimental subject (**LLM-as-Subject**, within-subject design): the same model, the same five concepts (justice, freedom, responsibility, home, success), prompted in Chinese, German, and English. Because it is the same model, **language is the only variable.**

We extract a concept graph per language and measure divergence with our new metric, the **Linguistic Divergence Score (LDS)** — over shared concepts and relations. And we go beyond a single number: we name **which concept components** diverge, in **which domains**, and whether the divergence lives in concept choice or in the relations between concepts.

## 3. The Findings (60s)

On a state-of-the-art multilingual model the language signal is **real and significant** (permutation test p<0.01):

| What | Result |
|------|--------|
| LDS-C (signal) | 0.93–0.96 |
| Within-language floor | 0.85–0.87 → signal clearly above noise |
| German framing | freedom → autonomy, rules, one's own goals |
| Chinese framing | freedom → space, boundaries, what one deserves |

The decisive **control**: institutional knowledge (e.g. mathematics) *converges* across languages, while cultural concepts *diverge*. The instrument finds convergence where convergence is expected and divergence where divergence is expected — so the cultural signal is not a measurement artifact. Even the **relations** between concepts organize language-specifically.

**Why humans couldn't give us this:** in human between-subject data, language is confounded with individual differences — one person speaks one language. The AI removes that noise source, which is exactly what an audit needs.

## 4. The Application (45s)

LinguaGraph is a **new kind of AI audit**. The output is an interpretable **divergence report** per model and language pair:

- **Developers** — pre-deployment check: does my multilingual model drift on value-laden terms, and where? → targeted calibration.
- **Regulators** — transparency evidence (EU AI Act) for cross-lingual model behavior.
- **Researchers** — a quantitative, interpretable way to study cultural values in AI.

## 5. Next Steps

- Extend the audit to more models, concepts, and languages
- Define a threshold for "critical" divergence
- Open the divergence-report as a reusable evaluation tool

---

*Read the paper at `docs/paper/` · Evidence at `data/lds_c/` · Disclosure at `docs/declaration_of_support.md`*
