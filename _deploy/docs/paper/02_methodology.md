# LinguaGraph — Methodology

> **Language**: German
> **Status**: Final (v0.13.3)

---

## 2. Methodik

### 2.1 Überblick

LinguaGraph besteht aus zwei komplementären Analyse-Pipelines:

```
Pipeline A (Kognitive Graphen):
Probandentexte → LLM Extraktion → Konzeptgraph → LDS → Sprachenvergleich

Pipeline B (Lehrbuch-Wissensgraph):
Lehrbuchkorpus → MIMO Extraktion → Alignierung → CognitiveSpace 3D
```

Pipeline A dient der kognitiven Analyse auf individueller Ebene (Probandenstudie). Pipeline B dient der **Validierung der Extraktions- und Alignierungsmethodik im großen Maßstab** — 68 Lehrbücher, 556 Konzepte, 525 Relationen.

### 2.2 Lehrbuchkorpus (Pipeline B)

Die Grundlage des CognitiveSpace-Wissensgraphen bildet ein Korpus von **68 Lehrbüchern** aus drei Sprachräumen:

| Sprache | Anzahl | Lehrwerke | Stufen |
|---------|--------|-----------|--------|
| Chinesisch | 39 | Volksverlag (Renjiao) K-12, Tongji Analysis, Lineare Algebra, Wahrscheinlichkeit | Grundschule bis Universität |
| Englisch | 18 | Stewart Calculus, MIT OCW, Khan Academy, IGCSE, IB | K-12 bis Universität |
| Deutsch | 11 | Forster Analysis, Fischer LA, Lambacher Schweizer, Papula | Sekundarstufe bis Universität |

Die Lehrbücher decken ein breites mathematisches Spektrum ab: Arithmetik, Algebra, Geometrie, Analysis, Lineare Algebra, Differentialgleichungen, Wahrscheinlichkeitstheorie und Statistik. CN-Physik/Chemie-Ergänzung (PEP 2019, 7+4=11 Bände, s. DATA_MANIFEST): Drittspiegel (TapXWorld/ChinaTextbook) provenance unverified, nie committed, smartedu-offizielle Fassung maßgeblich.

### 2.3 Konzeptextraktion (MIMO-Verfahren)

Die Extraktion mathematischer Konzepte und ihrer Relationen erfolgte mittels eines strukturierten LLM-Prompts ("MIMO"-Verfahren):

```
[System]
Extrahiere alle mathematischen Konzepte aus dem folgenden Lehrbuchabschnitt.
Für jedes Konzept:
- id: eindeutiger Bezeichner
- name: kanonischer Name
- type: Konzepttyp (definition, theorem, method, example)

[Relationen]
Für jedes Paar verwandter Konzepte:
- source: Quellkonzept
- target: Zielkonzept
- type: Beziehungstyp (depends_on, part_of, related_to, representation, prerequisite)
- evidence: Textbeleg aus dem Lehrbuch
```

Die Extraktion wurde für jedes der 68 Lehrbücher separat durchgeführt, was **75 JSON-Extraktionsdateien** ergab (einige Lehrbücher wurden aufgrund ihres Umfangs in Kapitel aufgeteilt).

### 2.4 Graphkonstruktion und -fusion

Die Roh-Extraktionen durchlaufen einen mehrstufigen Fusionsprozess:

**Step 1 — Merging**: Alle 75 Extraktionsdateien werden eingelesen und zu einem einheitlichen Graphen zusammengeführt. Aliase und Synonyme werden anhand einer Konfigurationsdatei (`concept_taxonomy.json`) normalisiert:

```
"微分" → "Differential"
"导数" → "Ableitung" (Derivative)
"极限" → "Grenzwert" (Limit)
```

**Step 2 — Deduplizierung**: Konzepte mit identischer ID oder nachgewiesener Synonymie werden fusioniert. Nach der Deduplizierung verbleiben **556 eindeutige Konzepte**.

**Step 3 — Relationsextraktion**: Aus den extrahierten Abhängigkeiten wird ein gerichteter Graph konstruiert. Zusätzlich zu den 525 direkt extrahierten Relationen werden ~3000 transitive Inferenzen zur Sicherstellung der Konnektivität hinzugefügt.

### 2.5 Sprachübergreifende Alignierung

Die Alignierung der Konzepte über ZH/EN/DE hinweg erfolgt über ein gemeinsames ID-Schema mit **30 geteilten Konzept-IDs**:

```json
{
  "shared_id": "math_calculus_derivative",
  "zh": { "id": "math_calculus_导数", "name": "导数" },
  "en": { "id": "math_calculus_derivative", "name": "Derivative" },
  "de": { "id": "math_calculus_ableitung", "name": "Ableitung" }
}
```

Die Alignierung wird durch zwei Strategien erreicht:

1. **Explizite Abbildung**: Lehrbücher, die dasselbe mathematische Konzept behandeln, werden über Kapitelverweise gemappt (z. B. Stewart Kapitel 2 ↔ Forster Kapitel 4 ↔ Renjiao选修2-2).
2. **Semantische Inferenz**: Konzepte mit übereinstimmenden Nachbarschaftsbeziehungen im Graphen werden als äquivalent betrachtet.

Ergebnis: **219 Konzeptgruppen (39 % von 556 Konzepten) sind dreisprachig vollständig abgedeckt**, 120 sind nur im Chinesischen vorhanden (21,6 %), der Rest in zwei von drei Sprachen.

### 2.6 CognitiveSpace 3D-Visualisierung

Die Visualisierung erfolgt als **interaktiver 3D-Graph** mittels der Bibliothek `3d-force-graph` (v1.80.0).

**Layout**: Konzentrische Kugelschalen nach Bildungsstufe:

| Stufe | Konzepte | Radius |
|-------|----------|--------|
| Grundschule (小学) | 26 | r = 0–50 |
| Mittelschule (初中) | 57 | r = 60–120 |
| Oberstufe (高中) | 200 | r = 140–230 |
| Universität (大学) | 273 | r = 250–320 |

**Deterministische Positionierung**: Die Position jedes Knotens wird per deterministischer Hash-Funktion aus seiner ID berechnet:

```python
def position(knoten_id, min_r, max_r):
    h = hash(knoten_id)
    r = min_r + (h % 1001) / 1000 * (max_r - min_r)
    theta = (h % 997) / 997 * 2π
    phi = acos(2 * (((h * 13 + 7) % 1000) / 1000) - 1)
    return (r * sin(phi) * cos(theta),
            r * sin(phi) * sin(theta),
            r * cos(phi))
```

Diese deterministische Positionierung garantiert, dass jedes Konzept bei jedem Laden der Visualisierung an derselben Stelle erscheint — essentiell für die Reproduzierbarkeit in der Forschung.

**Farbcodierung**: Jeder Bildungsstufe ist eine eigene Farbe zugeordnet:
- Grundschule: Grün (#4ade80)
- Mittelschule: Cyan (#22d3ee)
- Oberstufe: Blau (#60a5fa)
- Universität: Violett (#c084fc)

**Interaktion**: Der Graph unterstützt Sprachfilterung (ZH/EN/DE), drei Ansichtsmodi (Universe, Space-Fill, Compare), Knotendetailansicht mit Lehrbuchquellen und einen BFS-Ripple-Effekt bei Klick.

### 2.7 Linguistic Divergence Score (LDS)

Der Linguistic Divergence Score quantifiziert die **strukturelle Divergenz** zwischen zwei sprachspezifischen kognitiven Graphen. Die hier verwendete **frozen v3-Formel** kombiniert Knoten- und Kantenkomponente:

```
LDS_v3(A, B) = 1 - mean( J(node_set_A, node_set_B), J(edge_set_A, edge_set_B) )
```

wobei \(J(X,Y) = \frac{|X \cap Y|}{|X \cup Y|}\) der Jaccard-Koeffizient ist und A, B zwei Sprachversionen desselben Inhalts (Textbuchkapitel, Fragebogenantwort oder Wikipedia-Artikel) bezeichnen. Ein LDS von 0 bedeutet identische Knoten- **und** Kantenstruktur; ein LDS nahe 1 maximale Divergenz. Die drei Sprachpaare ZH-EN, ZH-DE, DE-EN werden auf **drei Analyseebenen** berechnet: Konzeptebene (nur Knoten), relationale Ebene (Knoten + Kante, v3) und Kategorienebene (6-Klassen-Codebook).

**Varianten**:
- **LDS-K** (Knowledge): Strukturelle Divergenz institutionellen Wissens (Lehrbuch-Konzeptgraphen).
- **LDS-C** (Cognitive): Divergenz spontaner kognitiver Ausdrucksweise (menschliche oder LLM-Konzeptgraphen).
- **ΔLDS** = LDS-C − LDS-K: der zusätzliche, durch kognitive Ausdrucksweise eingeführte Anteil jenseits der Lehrbuchstruktur.

**Null-Modell-Rahmen**: Um Struktureffekte von Spracheffekten zu trennen, werden drei Null-Modelle eingesetzt (Details in `docs/lds_formal_definition.md` §3): (1) **Within-Language Split-Half** — Aufteilung einer Sprache in zwei Hälften → Bodenniveau der Teilnehmervariabilität; (2) **Label-Permutation** — Permutation der Sprachlabels → formales p-Wert für das getragene Sprachsignal; (3) **Cross-Source Null** — Textbuch vs. Wikipedia derselben Sprache → Trennung von Quell- und Spracheffekt. Alle LDS-Berechnungen verwenden die frozen v3-Formel; die Ergebnisse der Human- und LLM-Analyse (§4, §5) stützen sich auf denselben Rahmen.

> **Formel-Verdict (2026-09-12, vgl. `docs/BASELINE_LEDGER.md` §8)**: verifiziert — publizierte LDS-K-Werte stammen aus der 2-Komponenten-Pipeline (`scripts/figures/_lds_utils.py::lds_jaccard`; Freeze-Skript `scripts/figures/reproduce_lds_binary.py`, Log `outputs/figures/reproduce_lds_binary.log`). Die 3-Komponenten-Variante in `src/scoring.py` (exaktes GED auf 219 Knoten intractable, Fallback 0,5) reproduziert sie nicht; obiger frozen-v3-Text (2 Komponenten) ist damit die maßgebliche Definition.

### 2.8 LLM-Extraktionsqualität

Zur Validierung der Extraktionsqualität wird ein mehrsprachiger Goldstandard verwendet. Der Datensatz umfasst insgesamt **92 manuell annotierte Antworten** (36 ZH, 29 DE, 27 EN), verteilt auf zwei Domänen:

1. **Mathematische Konzepte** (20 Label): Calculus-Grundbegriffe (Grenzwert, Ableitung, Integral) — zur Validierung der domänenspezifischen Extraktionsqualität.
2. **Soziale Konzepte** (72 Label): Antworten zu Freiheit, Gerechtigkeit, Erfolg, Verantwortung und Heimat — zur Validierung im Hauptdomän der Studie.

Die Extraktion erfolgt mit **qwen-plus** (Alibaba Cloud Bailian API). Ergebnisse:

| Domäne | Sprache | F1 | Precision | Recall | n |
|--------|---------|:--:|:---------:|:------:|:-:|
| Mathematik | Chinesisch | 0,857 | 1,000 | 0,798 | 7 |
| Mathematik | Deutsch | 0,506 | 0,536 | 0,512 | 7 |
| Mathematik | Englisch | 0,711 | 0,722 | 0,722 | 6 |
| **Sozial** | **Chinesisch** | **0,974** | **1,000** | **0,950** | **29** |
| **Sozial** | **Deutsch** | **0,949** | **0,959** | **0,941** | **22** |
| **Sozial** | **Englisch** | **0,882** | **0,914** | **0,857** | **21** |
| **Gesamt (92, gewichtet)** | **Alle** | **0,881** | — | — | **92** |

> Gesamt-F1 ist das domänengewichtete Mittel ((72×0,939+20×0,674)/92≈0,881); die Kopfzahl 0,939 gilt nur für die Sozial-Subgruppe. Gesamt-Precision/Recall werden nicht aggregiert (domänenspezifisch, s. Zeilen oben).

Die Extraktionsqualität für soziale Konzepte übertrifft die mathematische Domäne deutlich: alle drei Sprachen erreichen F1 ≥ 0,88, mit chinesischen (F1=0,974) und deutschen (F1=0,949) Ergebnissen, die das Qualitätsziel (F1 ≥ 0,70) weit übertreffen. Dies bestätigt, dass die zuvor beobachtete niedrige deutsche Extraktionsqualität (F1=0,506) domänenspezifisch war und nicht die Modelleignung für die Hauptstudie widerspiegelt.

### 2.9 Model Comparison

Um zu bestimmen, ob die Extraktionsqualität durch die Pipeline oder die Modellfähigkeit begrenzt ist, vergleichen wir mehrere Modelle auf denselben Goldlabels. Die Tabelle zeigt Ergebnisse für die soziale Konzeptdomäne (72 Label) und die mathematische Domäne (20 Label):

| Model | Domäne | ZH F1 | DE F1 | EN F1 |
|-------|--------|:-----:|:-----:|:-----:|
| qwen3-8B (lokal) | Mathematik | 0,857 | 0,506 | 0,711 |
| qwen-plus (API) | Mathematik | 0,952 | 0,489 | 0,778 |
| qwen3.7-max (API) | Mathematik | 0,980 | 0,551 | 0,778 |
| **qwen-plus (API)** | **Sozial** | **0,974** | **0,949** | **0,882** |

Die Ergebnisse zeigen einen entscheidenden Befund: Die Extraktionsqualität ist **domänenabhängig**. Während qwen-plus in der mathematischen Domäne lediglich DE F1=0,489 erreicht, steigt der Wert für soziale Konzepte auf DE F1=0,949. Dies liegt vermutlich an der unterschiedlichen Konzeptstruktur: Mathematische Konzepte sind präziser und domänenspezifischer, während soziale Konzepte alltagssprachlich näher an der Trainingsdistribution der Modelle liegen. Für die Hauptstudie (soziale Konzepte) ist die Extraktionsqualität in allen drei Sprachen als hoch einzustufen.

### 2.10 Curriculum Coverage Score (CS)

Um die Beziehung zwischen Lehrbuchinhalten und offiziellen Lehrplänen zu quantifizieren, definieren wir den Coverage Score (CS):

\[
CS(G_{textbook}, G_{curriculum}) = \frac{|V_{textbook} \cap V_{curriculum}|}{|V_{curriculum}|}
\]

Der Coverage Score misst den Anteil der vom Lehrplan geforderten Konzepte, die im Lehrbuchgraph abgedeckt sind. Die Berechnung erfolgt pro Bildungsstufe und sprachspezifisch.

Aktuelle Ergebnisse für die mathematischen Lehrpläne (Stand 2026-08-08, `scripts/compute_all_coverage_v2.py`):

| Lehrplan | Gesamt-Coverage | Höchste Stufe | Niedrigste Stufe |
|----------|:--------------:|:-------------:|:----------------:|
| China (CN) | **95,4 %** | Grundstufe 1–2 (100 %) | Mittelstufe 7–9 (91,7 %) |
| England (UK) | 37,3 % | KS2 Y6 (43,9 %) | KS4 (28,3 %) |
| Vereinigte Staaten (US) | 17,2 % | alle Stufen (17,9 %) | — |
| NRW (DE) | **12,7 %** | Grundschule 1–4 (höchste) | Sekundarstufe II (niedrigste) |

Der Coverage Score zeigt erhebliche Unterschiede zwischen Bildungssystemen: Während chinesische Lehrbücher den nationalen Lehrplan nahezu vollständig abdecken (95,4 %), liegt die Abdeckung für NRW bei nur 12,7 %. Dies könnte auf die unterschiedliche Granularität der Lehrpläne oder auf eine größere methodische Lücke zwischen NRW-Lehrplan und den verwendeten Mathematiklehrbüchern hinweisen. Der Coverage Score wird als vierter Indikator neben LDS, CDS und HDS in die Analyse einbezogen.

### 2.11 Baseline-Glossar

Jeder Befund (§3–§5) wird gegen dieselben neun Referenzlinien gemessen (Portal: Methodik → Baseline-Glossar):

1. **Structure Null** — gradrandomisierte Graphen: erwartete Überlappung durch Zufall.
2. **Size-matched Bootstrap** (k = 15/25/35) — Vergleich bei gleicher Vokabelgröße.
3. **Within-language noise floor (0,97)** — sprachinterne Divergenz als Untergrenze.
4. **Wikipedia aligned control** — domänenreine soziale Konzepte (ZH/EN/DE).
5. **Human N=15 floor** — Between-Subject-Marge +0,015.
6. **LLM within-subject signal** — LDS-C 0,93–0,96, Permutation p < 0,01.
7. **Permutation test** — z. B. ZH-DE 55/55 (file-truth 56/56) bei p < 0,004 (500 perm., Auflösungsgrenze; kein exaktes p = 0,0).
8. **Heterogeneity injection (q-Scan)** — Konsistenz-Demonstration, kein Kausalbeweis.
9. **Margin threshold (≥ 0,10)** — operative Heuristik, keine validierte Grenze.

### 2.12 Technische Werkzeuge (Eigenständigkeit)

Externe Werkzeuge und Modelle (BWKI-Kriterium Eigenständigkeit — eigene Leistung: Design, LDS-Definition, alle Befund- und Falsifikationsanalysen; Hilfsmittel hier offengelegt): **Netzwerke/Graphen**: NetworkX, 3d-force-graph (CognitiveSpace-Rendering); **Figuren**: matplotlib (deterministische Skripte `scripts/figures/`); **Textextraktion**: pymupdf + RapidOCR-ONNX (DirectML-GPU, `pdf-reading`-Skill); **Semantik**: nomic-embed-v1.5 (LM Studio, Prefilter) + Muse-Spark-Adjudikation (EN-Grounding-Layer, temp-0-Protokoll in `scripts/semantic_ground_en.py`); **Konzeptextraktion (D1)**: qwen-plus via Alibaba Cloud Bailian API (als production-extraction-model gelabelt), Gold-N=92-human-annotiert (F1 sozial 0,939); **OCR/LLM-Nutzung ist in allen Ergebnisdateien als Layer getrennt gebucht** (kein Vermischen mit String-Match-Zählungen).
