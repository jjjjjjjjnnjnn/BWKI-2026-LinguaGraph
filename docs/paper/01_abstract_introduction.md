# LinguaGraph — BWKI 2026: Abstract and Introduction

> **Language**: German (BWKI submission language)
> **Status**: Final (v0.13.3)

---

## Abstract

> Sprichst du eine andere Sprache, denkst du eine andere Welt?

Diese Arbeit stellt die Frage, ob Sprache nicht nur die Kommunikation, sondern die **strukturelle Organisation von Wissen** beeinflusst. Dazu wurde LinguaGraph entwickelt — ein System, das mithilfe von Large Language Models (LLMs) kognitive Graphen aus Texten extrahiert und **sprachübergreifend vergleicht**.

Die Methodik basiert auf zwei komplementären Pipelines:

1. **LinguaGraph Pipeline**: Extraktion von Konzepten aus Probandentexten (ZH/DE/EN), Konstruktion kognitiver Graphen und Berechnung des *Linguistic Divergence Score* (LDS) — eines neuartigen metrischen Maßes für strukturelle Divergenz zwischen Sprachen.

2. **CognitiveSpace Pipeline**: Automatisierte Extraktion eines mathematischen Wissensgraphen aus 68 Lehrbüchern (39 ZH, 18 EN, 11 DE) mit **556 Konzepten und 525 Relationen** über vier Bildungsstufen (Grundschule bis Universität). Die sprachübergreifende Alignierung erzielt 219 dreisprachig abgedeckte Konzeptgruppen (39 %) bei null strukturellen Konflikten.

Der CognitiveSpace-Graph wird als **3D-Kugelschalenvisualisierung** dargestellt, die die Wissensexpansion von der Kernmathematik zur Hochschulmathematik sichtbar macht — mit interaktiven Sprachfiltern (ZH/EN/DE).

**Anwendungsszenario — Prüfung mehrsprachiger KI-Systeme**: Da LLMs überwiegend mit englischen Daten trainiert werden, ist bislang unklar, ob ihre Wertkonzepte (Gerechtigkeit, Freiheit, Verantwortung, Heimat, Erfolg) sprachübergreifend konsistent sind — ein blinder Fleck gängiger KI-Evaluation, die nur Aufgabenerfüllung misst. LinguaGraph macht genau dieses Modellverhalten prüfbar: Das LLM-as-Subject-Experiment (Within-Subject) quantifiziert, **ob und wo** ein mehrsprachiges Modell wertbeladene Konzepte sprachabhängig strukturiert, und benennt die konkret divergierenden Konzept-Bestandteile. Der Output ist ein interpretierbarer Divergenzbericht pro Modell und Sprachpaar.

**Zentrale Beiträge**:
- Linguistic Divergence Score (LDS) als neuartige Metrik für sprachübergreifende Strukturanalyse — inklusive **LDS-K (Wissen)** , **LDS-C (Kognition)** und **ΔLDS = LDS-C − LDS-K**
- **Null Model Suite**: Falsifikation der Annahme, dass LDS-K sprachgetriebene Divergenz misst — tatsächlich dominieren Gradverteilungsstrukturen, und Lehrbuchwissen konvergiert sprachübergreifend
- Kernbeitrag verschiebt sich zu **ΔLDS** (menschliche Kognition minus Lehrbuchstruktur), der den sprachspezifischen Anteil isoliert — die N=15-Analyse zeigt ΔLDS ≈ 0 unter Between-Subject-Bedingungen und spezifiziert, wann ΔLDS > 0 nachweisbar wäre
- Erster systematischer Vergleich mathematischer Wissensstrukturen über ZH/EN/DE hinweg (556 Konzepte, 4 Nullmodelle, 19-Modell-Benchmark)
- CognitiveSpace: skalierbare 3D-Visualisierung mit 556 Konzepten aus 68 Lehrbüchern
- Vollständige Pipeline: Textextraktion → Graphkonstruktion → Alignierung → Analyse → Visualisierung
- **Humanvalidierung**: Erweiterte, QC-geprüfte LDS-C-Analyse an N=15 Probanden (6 DE · 6 ZH · 3 EN) über drei Ebenen (Konzept, Kategorie, Relation) — **ehrliches negatives Ergebnis unter Between-Subject**: LDS-C (0.93–0.96) ist von Teilnehmervariabilität nicht unterscheidbar (Split-Half-Boden 0.92–0.96; Label-Permutation 0.94); die früheren N=8-Befunde (0.70–0.75) werden nicht repliziert
- **LLM-as-Subject (Within-Subject)**: Dasselbe LLM antwortet in ZH/DE/EN auf dieselben 5 Themen → **Sprachsignal ist nachweisbar** (LDS-C 0.93–0.96 ≫ Boden 0.85–0.87); LMM identifiziert den **Sprachcode als dominanten Organisator** (same_lang +0.038, p<0.001; same_frame +0.001, p=0.90); ZH-DE trägt eine strukturelle Ebene jenseits der Assoziationsstatistik; eine **modellübergreifende Replikation** (47 eindeutige Modelle, überwiegend chinesische Anbieter plus ein US-Modell) zeigt: alle 51 ZH-DE-Sprachpaare signifikant (p<0.05), aber 8/153 Sprachpaaren (alle englisch-bezogen) nicht; die Kulturrichtung (DE Autonomie/Regeln vs. ZH Raum/Anspruch) übersteigt ein frequenz-angepasstes Zufalls-Nullmodell bei allen Schwellen (p<0.001), am stärksten bei hoher Übereinstimmung (204 Konzepte mit ≥10 Stimmen vs. 129 zufällig erwartet)
- **Anwendungsfall — KI-Validierung**: Divergenzbericht pro Modell und Sprachpaar (LDS-C + konkret divergierende Konzeptbestandteile + Domänen-Asymmetrie) — für Entwickler (Vorabprüfung mehrsprachiger Modelle), Regulierer (Transparenz gemäß EU AI Act) und Forscher (kulturelle Werte in KI)

Die Arbeit demonstriert, dass LLM-gestützte Graphanalyse ein vielversprechendes Werkzeug zur Untersuchung sprachlicher Einflüsse auf die Wissensorganisation darstellt — mit Implikationen für die bilinguale Bildung und die KI-Forschung. Eine Null Model Suite falsifiziert die Annahme sprachgetriebener Lehrbuchdivergenz und etabliert ΔLDS als Kernmetrik. Die erweiterte Humanvalidierung (N=15) falsifiziert ΔLDS > 0 unter Between-Subject-Bedingungen; ein LLM-as-Subject-Experiment (Within-Subject) weist das Sprachsignal dagegen klar nach und klassifiziert den Human-Negativebefund als **Design-Artefakt** — mit dem Sprachcode als dominanter Organisationsebene und dem kulturellen Rahmen als sekundärem, code-internem Modulator.

---

## 1. Einleitung

### 1.1 Motivation

Als zweisprachiger Schüler — aufgewachsen mit Chinesisch als Muttersprache, unterrichtet auf Deutsch und wissenschaftlich geprägt durch Englisch — ist mir immer wieder aufgefallen, dass dieselben Konzepte in verschiedenen Sprachen **anders "gefühlte" Bedeutungskerne** haben. Das chinesische Wort 「成功」(Chénggōng) betont Leistung durch Anstrengung und familiäre Erwartungen. Das deutsche "Erfolg" ist stärker karriere- und kompetenzorientiert. Das englische "Success" assoziiert Chancen und individuelle Wahlfreiheit.

Diese subjektive Beobachtung wirft eine tiefere Frage auf: **Unterscheiden sich Sprachen nicht nur in Wörtern, sondern in der Art, wie sie Wissen organisieren?**

Die *linguistische Relativitätstheorie* (Sapir-Whorf-Hypothese) postuliert genau das: Sprache beeinflusst das Denken. In den letzten zwei Jahrzehnten wurde dies empirisch für Farbwahrnehmung (Winawer et al., 2007), Raumkonzepte (Levinson, 1996) und Zeitwahrnehmung (Boroditsky, 2001) belegt. Doch für **abstrakte, komplexe Wissensdomänen** wie Mathematik blieb diese Frage weitgehend unerforscht.

Hier setzt LinguaGraph an.

Die Relevanz dieser Frage reicht heute über die Sprachwissenschaft hinaus: Moderne KI-Systeme werden in Dutzenden Sprachen eingesetzt, aber überwiegend mit englischen Daten trainiert. Wenn ein Modell „Gerechtigkeit" in einem Kreditentscheidungs-System sprachabhängig anders strukturiert, erhalten Nutzer je nach Sprache inkonsistente Behandlung. Die Prüfung dieser sprachübergreifenden Konsistenz ist ein offenes Problem der KI-Validierung — gängige Evaluation misst Aufgabenerfüllung, nicht die Konzeptstruktur des Modells. Genau dafür stellt LinguaGraph ein quantitatives Werkzeug bereit.

### 1.2 Forschungsfrage

Die übergeordnete Forschungsfrage lautet:

> **Organisieren verschiedene Sprachen Wissen auf systematisch unterschiedliche Weise — und kann Künstliche Intelligenz diese Unterschiede messbar machen?**

Daraus leiten sich drei Teilfragen ab:

1. **Existiert ein messbarer "Linguistic Drift"** zwischen kognitiven Graphen aus ZH-, EN- und DE-Texten?
2. **Sind LLM-extrahierte Wissensgraphen ein valides Instrument**, um sprachübergreifende Strukturunterschiede zu erfassen?
3. **Ist der Linguistic Divergence Score (LDS) stabil und interpretierbar** über verschiedene Themen und Sprachen hinweg?

### 1.3 Beiträge

Diese Arbeit leistet folgende Beiträge:

1. **Linguistic Divergence Score (LDS)** — Eine neuartige graphentheoretische Metrik, die die strukturelle Divergenz zwischen sprachspezifischen Wissensgraphen quantifiziert. LDS = 1 — GraphSimilarity, wobei Ähnlichkeit über gemeinsame Konzepte und Relationen gemessen wird.

2. **Erster systematischer Vergleich mathematischer Wissensstrukturen** über ZH/EN/DE hinweg — basierend auf 68 Lehrbüchern, 556 extrahierten Konzepten und 525 Relationen.

3. **CognitiveSpace** — Eine skalierbare 3D-Visualisierung, die Wissensstrukturen als konzentrische Kugelschalen darstellt. Vier Bildungsstufen (Grundschule bis Universität) sind farblich codiert und interaktiv filterbar nach Sprache.

4. **End-to-End-Pipeline** — Ein vollständiges System von der Lehrbuchtextextraktion über die sprachübergreifende Konzeptalignierung bis zur Graphanalyse und 3D-Visualisierung. Die Pipeline ist reproduzierbar und auf beliebige Wissensdomänen übertragbar.

5. **KI-Validierungsinstrument** — Anwendung des Frameworks als Audit-Werkzeug für mehrsprachige KI: Quantifizierung, ob und wo ein Modell wertbeladene Konzepte sprachabhängig strukturiert, mit interpretierbarem Divergenzbericht (LDS-C, divergierende Konzeptbestandteile, Domänen-Asymmetrie) für Entwickler, Regulierer und Forscher.

### 1.4 Gliederung

Die Arbeit ist wie folgt aufgebaut. Kapitel 2 gibt einen Überblick über verwandte Arbeiten aus Linguistik, KI-Forschung und Wissensgraphen. Kapitel 3 beschreibt die Methodik beider Pipelines. Kapitel 4 präsentiert die Ergebnisse — vom CognitiveSpace-Wissensgraphen über die LDS-Analyse bis zur Humanvalidierung (F1–F12). Kapitel 5 weist das Sprachsignal im LLM-as-Subject-Within-Subject-Design nach, Kapitel 6 validiert fächerübergreifend (Physik, Chemie) und exploriert die Sprachproduktion (LPA). Kapitel 8 diskutiert Ergebnisse, Limitationen und die methodologische Einordnung; Kapitel 9 fasst zusammen und formuliert die Audit-Anwendung.
