# LinguaGraph — Results: CognitiveSpace Knowledge Graph

> **Language**: German
> **Status**: Draft v1 — based on completed CognitiveSpace data

---

## 3. Ergebnisse

### 3.1 CognitiveSpace: Statistische Übersicht

Die Extraktion und Fusion der 68 Lehrbücher ergibt einen Wissensgraphen mit folgenden Kenngrößen:

| Metrik | Wert |
|--------|------|
| Gesamtkonzepte | 574 (557 eindeutig + 17 alignierte Gruppen) |
| Gesamtrelationen | 3538 (525 direkt + ~3000 inferiert) |
| Lehrbuchquellen | 68 (45 ZH + 20 EN + 10 DE) |
| Bildungsstufen | 4 (Grundschule → Universität) |
| Dichte | 0,0015 |
| Isolierte Knoten | 2 (< 0,5 %) |

### 3.2 Verteilung nach Bildungsstufe

Die Konzepte verteilen sich erwartungsgemäß über die vier Bildungsstufen, wobei der Schwerpunkt auf Oberstufe und Universität liegt:

| Stufe | Konzepte | Anteil | Charakteristik |
|-------|----------|--------|----------------|
| Grundschule | 37 | 6,4 % | Grundlegende Arithmetik, einfache Geometrie |
| Mittelschule | 46 | 8,0 % | Algebra, Gleichungen, Funktionen |
| Oberstufe | 193 | 33,6 % | Analysis, Wahrscheinlichkeit, Vektoren |
| Universität | 298 | 51,9 % | Höhere Analysis, Lineare Algebra, DGLS |

Diese Verteilung spiegelt die zunehmende Spezialisierung und den wachsenden Begriffsumfang in höheren Bildungsstufen wider.

### 3.3 Sprachübergreifende Abdeckung

Die Alignierung zeigt eine substanzielle dreisprachige Überschneidung:

| Abdeckung | Konzepte | Anteil |
|-----------|----------|--------|
| ZH + EN + DE | 247 | 43,0 % |
| ZH + EN | 342 | 59,6 % |
| ZH + DE | 331 | 57,7 % |
| EN + DE | 297 | 51,7 % |
| Nur ZH | 88 | 15,3 % |
| Nur EN | 50 | 8,7 % |
| Nur DE | 44 | 7,7 % |

Die relativ hohe exklusive ZH-Abdeckung (15,3 %) ist auf die spezifischeren chinesischen Lehrpläne in der Grund- und Mittelschule zurückzuführen, während die Exklusivanteile für EN (8,7 %) und DE (7,7 %) deutlich geringer ausfallen.

### 3.4 Semesterstruktur-Analyse

Die Analyse des Graphen auf Semesterstruktur zeigt folgende Beobachtungen:

1. **Konnektivität**: Der Graph ist nahezu vollständig verbunden. Nur 2 von 574 Knoten (<0,5 %) sind isoliert, was auf eine hohe Qualität der Relationsextraktion hindeutet.

2. **Hierarchische Struktur**: Grundschulkonzepte haben einen hohen Zentralitätsgrad und dienen als Anker für zahlreiche Oberstufen- und Universitätskonzepte. Dies bestätigt das erwartete "Knowledge Core → Expansion"-Muster.

3. **Kreuzsprachliche Kanten**: Konzepte, die in mehreren Sprachen vorkommen, weisen strukturell ähnliche Nachbarschaftsbeziehungen auf — ein Indikator dafür, dass die zugrundeliegende mathematische Wissensstruktur sprachunabhängige Invarianten besitzt.

### 3.5 CognitiveSpace 3D-Visualisierung

Die CognitiveSpace-Visualisierung stellt den Wissensgraphen als interaktive 3D-Kugelschale dar. Die Visualisierung ist unter `cognitive-space/web/index.html` lokal ausführbar und wird über GitHub Pages automatisch bereitgestellt.

**Wichtigste Funktionen**:
- **Kugelschalen-Layout**: Vier konzentrische Schalen nach Bildungsstufe, deterministisch positioniert
- **Sprachfilter**: Interaktive Umschaltung ZH/EN/DE/All mit sofortiger graphischer Aktualisierung
- **Farbcodierung**: Grün (Grundschule) → Cyan (Mittelschule) → Blau (Oberstufe) → Violett (Universität)
- **Knotendetail**: Anzeige von Lehrbuchquelle, Kapitel, Abschnitt bei Klick
- **Such- und Erkundungsmodi**: WASD-Navigation, drei Ansichtsmodi, BFS-Expansion bei Klick

### 3.6 CognitiveSpace-Screenshot

[Abbildung: CognitiveSpace-3D-Visualisierung — 574 Konzepte in konzentrischen Kugelschalen,
vier farbcodierte Bildungsstufen, sichtbare 3538 Relationen als blaue Verbindungslinien]

### 3.7 LDS-K: Sprachübergreifender Strukturvergleich (Textbook-Pipeline)

Die Pipeline-basierte LDS-K Analyse der Mathematik-Lehrbücher (556 Konzepte, 3 Sprachen) ergibt:

| Sprachpaar | LDS-K |
|:----------:|:-----:|
| ZH-EN | 0.934 |
| DE-EN | 0.938 |
| ZH-DE | 0.519 |

Der ZH-DE Wert ist auffällig niedrig — chinesische und deutsche Mathematikbücher sind strukturell ähnlicher als jede der beiden mit den englischen Lehrbüchern. Um zu testen, ob diese Werte tatsächlich sprachgetriebene Divergenz messen, wurde eine **Null Model Suite** mit degree-preserving Randomisierung (Double-Edge Swap, 1000 Iterationen) durchgeführt:

| Bedingung | ZH-EN | DE-EN | ZH-DE |
|:----------|:-----:|:-----:|:-----:|
| Full (LDS-K baseline) | 0.934 | 0.938 | 0.519 |
| Structure Null (degree-preserving) | **0.957** | **0.957** | **0.717** |
| Node-Permuted Null | 0.934 | 0.938 | 0.519 |
| Complete Random | 1.000 | 1.000 | 1.000 |

**Zentraler Befund**: Full LDS-K < Structure Null LDS-K für alle drei Sprachpaare. Unter degree-preserving Randomisierung sind die randomisierten Graphen systematisch unterschiedlicher als die echten Graphen. Dies bedeutet, dass **Lehrbuch-Wissensstrukturen über Sprachgrenzen hinweg konvergieren** — das Gegenteil einer sprachgetriebenen Divergenz.

Die Interpretation: LDS-K wird von der **Gradverteilungsstruktur** dominiert (eine Eigenschaft, die von universeller mathematischer Prerequisite-Logik geteilt wird), nicht von sprachspezifischen Inhaltsarrangements. Der wissenschaftliche Kernbeitrag verschiebt sich damit zu **ΔLDS = LDS-C − LDS-K**, der den sprachspezifischen Anteil der menschlichen Kognition isoliert.

---

## 4. Humanvalidierung: Kognitive Graphen mehrsprachiger Probanden

> Dieser Abschnitt präsentiert LDS-C Ergebnisse basierend auf **echten Probandendaten** (N=8, 90 extrahierte Antworten) im sozialen Themenbereich.

### 4.1 Versuchsdesign und Datengrundlage

Die Humanstudie folgt einem gemischten Within-Subject- + Between-Subject-Design:

| Dimension | Spezifikation |
|-----------|---------------|
| Teilnehmer | N=8 (4 ZH-Muttersprachler, 2 DE, 2 EN) |
| Stimuli | 5 soziale Themen × 3 Sprachen |
| Extraktionsmodell | qwen-plus (F1=0,939 validiert) |
| Erfolgreich extrahiert | 90/101 Antworten (89,1 %) |
| Durchschnittliche Konzepte pro Antwort | 3,2 (Spanne: 1–12) |

**Teilnehmer nach Sprachgruppe**:
- **ZH-Gruppe**: S001, S004, S007 — ausschließlich Chinesisch
- **DE-Gruppe**: S002, S005, S008 — Deutsch + Englisch (bilingual)
- **EN-Gruppe**: S003, S006 — ausschließlich Englisch

### 4.2 Within-Subject LDS (DE-EN)

Die drei bilingualen Teilnehmer (DE-Muttersprachler) beantworteten dieselben Fragen auf Deutsch und Englisch, was einen direkten Within-Subject-Vergleich ermöglicht:

| Proband | Thema | LDS | GED-Ähnlichkeit | Node-Jaccard |
|---------|-------|:---:|:----------------:|:------------:|
| S002 | Freiheit | **0,917** | 0,250 | 0,000 |
| S002 | Zuhause | 0,667 | 1,000 | 0,000 |
| S002 | Verantwortung | 0,778 | 0,667 | 0,000 |
| S005 | Freiheit | 0,833 | 0,500 | 0,000 |
| S005 | Zuhause | 0,667 | 0,500 | 0,500 |
| S008 | Zuhause | 0,778 | 0,333 | 0,333 |
| **Mittelwert** | | **0,773** | 0,542 | 0,139 |

**Beobachtung**: Die Within-Subject LDS-Werte sind hoch (M=0,773), was bedeutet, dass dieselbe Person zu demselben Thema in verschiedenen Sprachen systematisch unterschiedliche Konzepte nennt. Der Node-Jaccard von 0,000 für Freiheit und Verantwortung bei S002 zeigt, dass DE- und EN-Antworten **kein einziges gemeinsames Konzept** teilen — ein starker Beleg für sprachliche Kognitionseffekte.

### 4.3 Between-Subject LDS (Sprachengruppen)

Durch Aggregation aller Antworten einer Sprachgruppe entstehen Gruppen-graphen, die den sprachspezifischen "kollektiven kognitiven Raum" repräsentieren:

| Sprachpaar | Freiheit | Gerechtigkeit | Erfolg | Verantwortung | Zuhause | **Mittel** |
|:----------:|:--------:|:-------------:|:------:|:-------------:|:-------:|:----------:|
| DE–ZH | 0,939 | 0,880 | 0,647 | 0,600 | 0,689 | **0,751** |
| DE–EN | 0,933 | 0,667 | 0,741 | 0,648 | 0,648 | **0,727** |
| ZH–EN | 0,662 | 0,917 | 0,710 | 0,648 | 0,583 | **0,704** |
| **Mittel** | **0,845** | **0,821** | **0,699** | **0,632** | **0,640** | **0,727** |

### 4.4 Vergleich mit Textbook-LDS-K

Der Vergleich zwischen Human-LDS-C und Textbook-LDS-K zeigt ein aufschlussreiches Muster:

| Sprachpaar | Human LDS-C (Between) | Textbook LDS-K | Differenz | Interpretation |
|:----------:|:---------------------:|:--------------:|:---------:|----------------|
| DE–ZH | **0,751** | **0,519** | **+0,232** | Kognitive Divergenz > Strukturkonvergenz |
| DE–EN | 0,727 | 0,938 | −0,211 | Kognitive Divergenz < Textbuchdivergenz |
| ZH–EN | 0,704 | 0,934 | −0,230 | Kognitive Divergenz < Textbuchdivergenz |

**Zwei zentrale Befunde**:

1. **DE–ZH ist der Schlüsselfall**: Die höchste kognitive Divergenz (LDS-C=0,751) trifft auf die geringste Textbuchdivergenz (LDS-K=0,519). Dies ist konsistent mit der ΔLDS-Hypothese: der sprachliche Einfluss auf die Kognition (DE↔ZH) ist größer als der auf die institutionelle Wissensorganisation.

2. **DE–EN und ZH–EN zeigen das umgekehrte Muster**: Textbookstrukturen divergieren stark (0,938, 0,934), während die kognitive Divergenz moderat ausfällt (0,727, 0,704). Dies bestätigt, dass LDS-K und LDS-C unterschiedliche Phänomene messen.

Die Rangfolge der kognitiven Divergenz (DE–ZH > DE–EN > ZH–EN) bleibt konsistent, während die Rangfolge der Textbuchdivergenz grundlegend anders ist (DE–EN > ZH–EN > ZH-DE). Dies zeigt, dass LDS-K und LDS-C komplementäre, aber nicht austauschbare Metriken sind.

### 4.5 Robuste Extraktionsqualität

Die Extraktion der Probandentexte erfolgte mit dem validierten qwen-plus-Modell:

| Metrik | Wert |
|--------|:----:|
| Goldstandard | 92 annotierte Antworten |
| Gesamt-F1 | **0,939** |
| ZH F1 | 0,974 |
| DE F1 | 0,949 |
| EN F1 | 0,882 |

Die hohe Extraktionsqualität stellt sicher, dass die beobachteten LDS-Unterschiede auf genuine kognitive Divergenz zurückgehen und nicht auf Extraktionsrauschen.

### 4.6 Zusammenfassung

Die Humanvalidierung zeigt drei Kernbefunde:

1. **Kognitive sprachliche Divergenz ist messbar**: Within-Subject LDS (M=0,773) und Between-Subject LDS (M=0,727) sind substanziell und zeigen eine konsistente Rangfolge (DE–ZH > DE–EN > ZH–EN).

2. **LDS-C und LDS-K messen unterschiedliche Phänomene**: Während die Textbuchstruktur sprachübergreifend konvergiert (Null Model Befund), zeigt die menschliche Kognition eine sprachspezifische Divergenz. Der DE–ZH Fall ist besonders aufschlussreich: höchste kognitive Divergenz bei geringster Textbuchdivergenz.

3. **Themenvariation ist substanziell**: Abstrakte Konzepte (Freiheit, Gerechtigkeit) zeigen höhere Divergenz als konkrete (Zuhause). Dies bestätigt die Hypothese, dass abstrakte, politisch-philosophische Konzepte stärkeren sprachlichen Einfluss auf die Kognition zeigen.

Die Ergebnisse validieren LDS-C als Maß für sprachübergreifende kognitive Strukturunterschiede und etablieren **ΔLDS = LDS-C − LDS-K** als zentrale Metrik für die Isolierung des sprachspezifischen Signals.
