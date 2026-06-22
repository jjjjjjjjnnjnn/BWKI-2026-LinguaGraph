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

## 4. Pilotstudie: LDS-Ergebnisse

> ⚠️ **Hinweis**: Die vollständige LDS-Analyse erfordert DE/EN-Probandendaten, die zum Zeitpunkt der Einreichung noch nicht vollständig vorlagen. Nachfolgend wird das Versuchsprotokoll beschrieben, die Ergebnisse sind als vorläufig zu betrachten.

### 4.1 Versuchsdesign

Die Pilotstudie folgt einem **innerhalb der Versuchspersonen** gemischten Design (within-subject + between-subject):

- **N**: 30 (10 ZH, 10 DE, 10 EN)
- **Stimuli**: 5 Themen × 3 Sprachen = 15 offene Fragen
- **Altersbereich**: 13–18 Jahre (Sekundarstufe)

### 4.2 Erwartete LDS-Muster

Basierend auf den Voranalysen und der Lehrbuchstruktur werden folgende LDS-Muster erwartet:

| Themenbereich | Erwarteter LDS | Interpretation |
|--------------|----------------|----------------|
| Algebra | Niedrig (< 0,3) | Universelle mathematische Notation |
| Geometrie | Mittel (0,3–0,5) | Kulturell unterschiedliche Schwerpunkte |
| Analysis | Mittel–Hoch (0,4–0,7) | Unterschiedliche Curricula |
| Wahrscheinlichkeit | Hoch (> 0,6) | Sprachabhängige Begriffssysteme |

Die vollständige statistische Analyse wird nach Abschluss der Datenerhebung durchgeführt.
