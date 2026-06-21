# CognitiveSpace

> **Cross-lingual mathematics knowledge graph — from elementary arithmetic to partial differential equations.**  
> **Mehrsprachiger Mathematik-Wissensgraph — von der Grundschule bis zu partiellen Differentialgleichungen.**

3D interactive knowledge graph covering the complete mathematics concept network.  
3D-interaktiver Wissensgraph, der das gesamte mathematische Konzeptnetz abdeckt.

---

## Data / Daten

| Metric | Value |
|--------|-------|
| Concepts / Konzepte | **574** (557 unique, 17 aligned) |
| Relations / Beziehungen | **525** (known) + **~3000** (inferred) |
| Textbooks / Lehrbücher | **68** (45 ZH / 20 EN / 10 DE) |
| Curricula / Lehrpläne | Renjiao · IB · AP · IGCSE · Abitur · Khan Academy |
| Levels / Stufen | Elementary → University |
| Structural conflicts | **0** |
| Isolated nodes | **2** (<0.5%) |

## Levels / Bildungsstufen

| Level | Concepts | Color |
|-------|----------|-------|
| Elementary / Grundschule | 37 | `#10b981` Green |
| Middle / Mittelschule | 46 | `#14b8a6` Teal |
| High / Oberstufe | 193 | `#4a7dff` Blue |
| College / Universität | 298 | `#8b5cf6` Purple |

## Language Coverage / Sprachabdeckung

| Language | Coverage |
|----------|----------|
| Chinese / Chinesisch | 335 (58%) |
| English / Englisch | 392 (68%) |
| German / Deutsch | 341 (59%) |
| Trilingual / Dreisprachig | 247 (43%) |

## Quick Start

Open `web/index.html` in any browser — no server required.  
`web/index.html` in einem Browser öffnen — kein Server erforderlich.

## Pipeline

```
Textbook text / Lehrbuchtext
    ↓ (MIMO LLM Extraction / Extraktion)
Structured JSON
    ↓ merge_extractions.py (merge + deduplicate / Zusammenführen + Deduplizieren)
    ↓ align_languages.py (ZH/EN/DE alignment / Abgleich)
    ↓ export_graph.py (visualization data / Visualisierungsdaten)
web/index.html + data.js
```

## Textbook Sources / Lehrbuchquellen

**Chinese / Chinesisch**: Renjiao K-12, Tongji University (Calculus, Linear Algebra)  
**English / Englisch**: Stewart *Calculus*, MIT OCW, Strang *Linear Algebra*, Khan Academy  
**German / Deutsch**: Forster *Analysis*, Fischer *Lineare Algebra*, Papula, Lambacher Schweizer

## License / Lizenz

Extracted data: CC-BY-SA (educational use). Textbook citations: fair use.  
Extrahierte Daten: CC-BY-SA (Bildungszwecke). Lehrbuchzitate: Fair Use.

## Citation

Part of the BWKI 2026 LinguaGraph project.  
Main repository: [BWKI-2026-LinguaGraph](https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph)
