# Contributors

## LinguaGraph Team

- **Project Lead**: Student researcher (Chinese-German bilingual)
- **Institution**: German high school (9-13年级)

## AI Models Used (Disclosure per BWKI Eigenständigkeit)

> SSOT: `../submission/final/declaration_of_support.md` §1 (alle Anbieter + 59-Modell-Replikation 59/54/177). Diese Tabelle ist eine spiegelte Kurzfassung (Stand 2026-09-17).

| Model(s) | Provider / Endpoint | Purpose |
|-------|---------------------|---------|
| deepseek-v4-flash | opencode GO (`https://opencode.ai/zen/go/v1`) | Concept/relation extraction; **LLM-as-Subject** within-subject experiment (P1/P2/P3/P5); Wikipedia + association glossing |
| deepseek-v4-flash, nemotron-3-ultra-free (NVIDIA), mimo-v2.5-free, laguna-s-2.1-free, longcat-2.0-free u. a. | opencode zen/v1 | Replication subject models |
| gpt-oss-20b:free, nemotron-/laguna-/gemma-Modelle u. a. | OpenRouter (free tier) | Replication subject models (partly incomplete) |
| deepseek-v3/v3.1/v3.2/v4/r1 families, GLM-4.5–5.2, Kimi, MiniMax, Qwen3.x u. a. (**42 Modelle**) | Alibaba Cloud DashScope/Qwen | Replication subject models |
| gpt-oss-20b | NVIDIA NIM | West-Erweiterung (vollständig) |
| command-a-03-2025 | Cohere | West-Erweiterung (vollständig) |
| laguna-s-2.1, nemotron-3-super-120b-a12b | Kilo | West-Erweiterung (vollständig) |
| gpt-5.6-luna (Herkunft ungeklärt) + grok-4.6 + muse-spark | opencode-Terminal | West-Erweiterung (vollständig) |
| llama-3.3-70b | Cloudflare | West-Erweiterung (vollständig) |
| phi-4-mini-instruct (lokal) | LM Studio | 59. Messung (Kleinstmodell-Grenze, s. Paper §8.15) |
| qwen-plus | Alibaba Cloud Bailian API | D1 production extraction model (Gold-N=92, sozial F1 0,939† Developing C9b) |

## AI-Assisted Development Tools (Disclosure per BWKI Eigenständigkeit)

| Tool | Provider | Purpose |
|------|----------|---------|
| Claude Code | Anthropic | Assisted code development, data analysis scripting, documentation |

> Full disclosure: see `docs/declaration_of_support.md`.

## External Tools and Libraries

This project uses the following open-source tools:

| Tool | License | Purpose |
|------|---------|---------|
| [NetworkX](https://networkx.org/) | BSD-3-Clause | Graph algorithms |
| [NumPy](https://numpy.org/) | BSD-3-Clause | Numerical computation |
| [SciPy](https://scipy.org/) | BSD-3-Clause | LMM mixed-effects model (closed-form ML) |
| [Flask](https://flask.palletsprojects.com/) | BSD-3-Clause | Web framework |
| [3d-force-graph](https://github.com/vasturiano/3d-force-graph) | MIT | 3D graph visualization |
| [Three.js](https://threejs.org/) | MIT | 3D rendering |

## Datasets

| Dataset | Source | License |
|---------|--------|---------|
| Human questionnaire responses (N=15) | Self-collected (2026-07) | Participant-consented, GDPR-compliant |
| Wikipedia articles (ZH/EN/DE, 5 social topics) | Wikipedia | CC-BY-SA (attribution in paper references) |
| Math textbook concept structures | ZH/DE/EN curricula | Structural description, not verbatim reproduction |

## Research References

This project builds on the following research:

1. Conceptualizer (ACL 2023) — 1335-language concept alignment
2. CCKG (EACL 2026) — Cultural Commonsense Knowledge Graph
3. RISE (ICLR 2026) — Riemannian geometry for cross-lingual semantics
4. Separating Tongue from Thought (ACL 2025) — Activation patching
5. Binz & Schulz (2023, PNAS) — LLM as cognitive subject (within-subject paradigm)
6. Arora et al. (2024, PNAS Nexus) — cultural bias and alignment of LLMs

## Acknowledgments

- BWKI (Bundeswettbewerb Künstliche Intelligenz) for the competition framework
- Plattform Lernende Systeme / acatech for organizing the competition
