# Contributors

## LinguaGraph Team

- **Project Lead**: Student researcher (Chinese-German bilingual)
- **Institution**: German high school (9-13年级)

## AI Models Used (Disclosure per BWKI Eigenständigkeit)

| Model | Provider / Endpoint | Purpose |
|-------|---------------------|---------|
| deepseek-v4-flash | opencode GO (`https://opencode.ai/zen/go/v1`) | Concept/relation extraction; **LLM-as-Subject** within-subject experiment (P1/P2/P3/P5); Wikipedia + association glossing |

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
