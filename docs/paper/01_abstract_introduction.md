# LinguaGraph — BWKI 2026: Abstract and Introduction

> **Language**: German (BWKI submission language)
> **Status**: Draft v1

---

## Abstract

> Sprichst du eine andere Sprache, denkst du eine andere Welt?

Diese Arbeit stellt die Frage, ob Sprache nicht nur die Kommunikation, sondern die **strukturelle Organisation von Wissen** beeinflusst. Dazu wurde LinguaGraph entwickelt — ein System, das mithilfe von Large Language Models (LLMs) kognitive Graphen aus Texten extrahiert und **sprachübergreifend vergleicht**.

Die Methodik basiert auf zwei komplementären Pipelines:

1. **LinguaGraph Pipeline**: Extraktion von Konzepten aus Probandentexten (ZH/DE/EN), Konstruktion kognitiver Graphen und Berechnung des *Language Drift Score* (LDS) — eines neuartigen metrischen Maßes für strukturelle Divergenz zwischen Sprachen.

2. **CognitiveSpace Pipeline**: Automatisierte Extraktion eines mathematischen Wissensgraphen aus 68 Lehrbüchern (45 CH, 20 EN, 10 DE) mit **574 Konzepten und 3538 Relationen** über vier Bildungsstufen (Grundschule bis Universität). Die sprachübergreifende Alignierung erzielt 247 dreisprachig abgedeckte Konzepte (43 %) bei null strukturellen Konflikten.

Der CognitiveSpace-Graph wird als **3D-Kugelschalenvisualisierung** dargestellt, die die Wissensexpansion von der Kernmathematik zur Hochschulmathematik sichtbar macht — mit interaktiven Sprachfiltern (ZH/EN/DE).

**Zentrale Beiträge**:
- Language Drift Score (LDS) als neuartige Metrik für sprachübergreifende kognitive Divergenz
- Erster systematischer Vergleich mathematischer Wissensstrukturen über ZH/EN/DE hinweg
- CognitiveSpace: skalierbare 3D-Visualisierung mit 574 Konzepten aus 68 Lehrbüchern
- Vollständige Pipeline: Textextraktion → Graphkonstruktion → Alignierung → Analyse → Visualisierung

Die Arbeit demonstriert, dass LLM-gestützte Graphanalyse ein vielversprechendes Werkzeug zur Untersuchung sprachlicher Einflüsse auf die Wissensorganisation darstellt — mit Implikationen für die bilinguale Bildung und die KI-Forschung. Eine Humanstudie zur Validierung des LDS ist in Vorbereitung.

---

## 1. Einleitung

### 1.1 Motivation

Als zweisprachiger Schüler — aufgewachsen mit Chinesisch als Muttersprache, unterrichtet auf Deutsch und wissenschaftlich geprägt durch Englisch — ist mir immer wieder aufgefallen, dass dieselben Konzepte in verschiedenen Sprachen **anders "gefühlte" Bedeutungskerne** haben. Das chinesische Wort 「成功」(Chénggōng) betont Leistung durch Anstrengung und familiäre Erwartungen. Das deutsche "Erfolg" ist stärker karriere- und kompetenzorientiert. Das englische "Success" assoziiert Chancen und individuelle Wahlfreiheit.

Diese subjektive Beobachtung wirft eine tiefere Frage auf: **Unterscheiden sich Sprachen nicht nur in Wörtern, sondern in der Art, wie sie Wissen organisieren?**

Die *linguistische Relativitätstheorie* (Sapir-Whorf-Hypothese) postuliert genau das: Sprache beeinflusst das Denken. In den letzten zwei Jahrzehnten wurde dies empirisch für Farbwahrnehmung (Winawer et al., 2007), Raumkonzepte (Levinson, 1996) und Zeitwahrnehmung (Boroditsky, 2001) belegt. Doch für **abstrakte, komplexe Wissensdomänen** wie Mathematik blieb diese Frage weitgehend unerforscht.

Hier setzt LinguaGraph an.

### 1.2 Forschungsfrage

Die übergeordnete Forschungsfrage lautet:

> **Organisieren verschiedene Sprachen Wissen auf systematisch unterschiedliche Weise — und kann Künstliche Intelligenz diese Unterschiede messbar machen?**

Daraus leiten sich drei Teilfragen ab:

1. **Existiert ein messbarer "Language Drift"** zwischen kognitiven Graphen aus ZH-, EN- und DE-Texten?
2. **Sind LLM-extrahierte Wissensgraphen ein valides Instrument**, um sprachübergreifende Strukturunterschiede zu erfassen?
3. **Ist der Language Drift Score (LDS) stabil und interpretierbar** über verschiedene Themen und Sprachen hinweg?

### 1.3 Beiträge

Diese Arbeit leistet folgende Beiträge:

1. **Language Drift Score (LDS)** — Eine neuartige graphentheoretische Metrik, die die strukturelle Divergenz zwischen sprachspezifischen Wissensgraphen quantifiziert. LDS = 1 — GraphSimilarity, wobei Ähnlichkeit über gemeinsame Konzepte und Relationen gemessen wird.

2. **Erster systematischer Vergleich mathematischer Wissensstrukturen** über ZH/EN/DE hinweg — basierend auf 68 Lehrbüchern, 574 extrahierten Konzepten und 3538 Relationen.

3. **CognitiveSpace** — Eine skalierbare 3D-Visualisierung, die Wissensstrukturen als konzentrische Kugelschalen darstellt. Vier Bildungsstufen (Grundschule bis Universität) sind farblich codiert und interaktiv filterbar nach Sprache.

4. **End-to-End-Pipeline** — Ein vollständiges System von der Lehrbuchtextextraktion über die sprachübergreifende Konzeptalignierung bis zur Graphanalyse und 3D-Visualisierung. Die Pipeline ist reproduzierbar und auf beliebige Wissensdomänen übertragbar.

### 1.4 Gliederung

Die Arbeit ist wie folgt aufgebaut. Kapitel 2 gibt einen Überblick über verwandte Arbeiten aus Linguistik, KI-Forschung und Wissensgraphen. Kapitel 3 beschreibt die Methodik beider Pipelines. Kapitel 4 präsentiert die Ergebnisse des CognitiveSpace-Wissensgraphen. Kapitel 5 skizziert das geplante Humanstudienprotokoll. Kapitel 6 diskutiert die Ergebnisse und Limitationen. Kapitel 7 fasst die Arbeit zusammen.
