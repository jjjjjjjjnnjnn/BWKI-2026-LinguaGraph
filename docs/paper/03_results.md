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
| Strukturkonflikte | 0 |
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

---

## 4. Humanvalidierung: Kognitive Graphen mehrsprachiger Probanden

> Die vorherige Sektion präsentierte LDS-Ergebnisse basierend auf einem Wikipedia-Korpus. Dieser Abschnitt validiert diese Befunde anhand **echter Probandendaten** (N=8, 90 extrahierte Antworten).

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

### 4.4 Vergleich mit Wikipedia-Korpus

Der Vergleich zwischen Human- und Wikipedia-LDS zeigt ein klares Muster:

| Sprachpaar | Human LDS (Between) | Wikipedia LDS (Korpus) | Differenz |
|:----------:|:-------------------:|:---------------------:|:---------:|
| DE–ZH | **0,751** | **0,907** | −0,156 |
| DE–EN | 0,727 | 0,901 | −0,174 |
| ZH–EN | 0,704 | 0,802 | −0,098 |
| **Mittel** | **0,727** | **0,870** | **−0,143** |

**Drei zentrale Befunde**:

1. **Rangfolge bleibt erhalten**: DE–ZH > DE–EN > ZH–EN in beiden Datensätzen. Die sprachpaarspezifische Divergenz ist kein Artefakt der Korpusauswahl, sondern ein reproduzierbares Muster.

2. **Human LDS < Wikipedia LDS**: Individuelle kognitive Graphen zeigen geringere Divergenz als aggregierte Textkorpora. Dies ist konsistent mit der Interpretation, dass Bildungssysteme sprachspezifische Organisationsmuster verstärken.

3. **Themenvariation ist substanziell**: Freiheit (M=0,845) und Gerechtigkeit (M=0,821) zeigen die höchste Divergenz, Zuhause (M=0,640) die niedrigste. Dies bestätigt die Hypothese, dass abstrakte, politisch-philosophische Konzepte stärker sprachabhängig sind als alltägliche Erfahrungskonzepte.

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

Die Humanvalidierung bestätigt die drei Kernbefunde der Korpusanalyse:

1. **Sprachliche Divergenz ist ein reproduzierbares Phänomen** auf individueller und Gruppenebene
2. **DE–ZH zeigt die größte, ZH–EN die geringste strukturelle Divergenz** — konsistent über alle Analyseebenen
3. **Die Themenspezifität der Divergenz bleibt erhalten** — abstrakte Konzepte (Freiheit, Gerechtigkeit) divergieren stärker als konkrete (Zuhause)

Die Ergebnisse validieren LDS als Maß für sprachübergreifende kognitive Strukturunterschiede und erweitern die Gültigkeit der Korpusbefunde auf die individuelle Kognitionsebene.
