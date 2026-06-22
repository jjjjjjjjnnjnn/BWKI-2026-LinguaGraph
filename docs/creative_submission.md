# LinguaGraph — BWKI 2026 Creative Submission Package

> Deadline: 2026-06-28
> Language: German (BWKI official language)

---

## 1. 150-Word Abstract (Kurzbeschreibung)

**Titel**: LinguaGraph — Wie Sprache das Denken formt: Eine KI-basierte Analyse kognitiver Strukturen in Chinesisch, Deutsch und Englisch

**Abstract**:
Spricht man verschiedene Sprachen, denkt man vielleicht auch unterschiedlich. In diesem Projekt untersuche ich, ob Chinesisch, Deutsch und Englisch die Art und Weise beeinflussen, wie Menschen über abstrakte Konzepte wie Freiheit, Gerechtigkeit und Erfolg denken.

Mithilfe von KI (Large Language Models) extrahiere ich aus Antworten von Probanden kognitive Konzepte und deren Beziehungen, erstelle daraus Wissensgraphen und vergleiche diese über Sprachen hinweg. Ein neu entwickelter Metrik, der Language Drift Score (LDS), quantifiziert, wie stark sich die kognitiven Strukturen zwischen Sprachen unterscheiden.

Ergebnisse einer Pilotstudie mit Wikipedia-Texten zeigen: Das Konzept "Erfolg" weist mit LDS=0.97 die größten sprachabhängigen Unterschiede auf, während "Freiheit" mit LDS=0.81 vergleichsweise ähnlicher strukturiert ist. Diese Arbeit verbindet KI-Methoden mit kognitiver Linguistik und eröffnet neue Wege, den Einfluss von Sprache auf das Denken messbar zu machen.

---

## 2. 500-Word Abstract (Ausführliche Beschreibung)

**Titel**: LinguaGraph — Mapping How Language Shapes Thinking: Eine KI-gestützte Analyse sprachabhängiger kognitiver Strukturen

### Einleitung

Die Frage, ob Sprache das Denken beeinflusst (Sapir-Whorf-Hypothese), beschäftigt die Wissenschaft seit Jahrzehnten. Während Studien zu Farbwahrnehmung, Raumkognition und Zeitverständnis sprachliche Einflüsse nachweisen konnten, blieben abstrakte soziale Konzepte weitgehend unerforscht. Gleichzeitig haben Large Language Models (LLMs) neue Möglichkeiten eröffnet, kognitive Strukturen aus Texten zu extrahieren.

Als in Deutschland lebender chinesischer Schüler erlebe ich täglich, wie sich meine Gedankengänge zwischen Chinesisch, Deutsch und Englisch unterscheiden. Diese persönliche Erfahrung ist der Ausgangspunkt für LinguaGraph.

### Forschungsfrage

Beeinflusst die Sprache, in der eine Frage gestellt wird, die kognitive Struktur der Antwort? Kann Künstliche Intelligenz diesen Einfluss messbar machen?

### Methode

Der LinguaGraph-Pipeline besteht aus vier Schritten:

1. **Datenerhebung**: Probanden beantworten offene Fragen zu sozialen Konzepten (Freiheit, Gerechtigkeit, Erfolg, Verantwortung, Heimat) in Chinesisch, Deutsch und Englisch.

2. **KI-Extraktion**: Ein LLM extrahiert aus jeder Antwort kognitive Konzepte und deren Beziehungen. Die Extraktion erfolgt sprachspezifisch.

3. **Graphkonstruktion**: Aus den extrahierten Konzepten und Relationen werden gerichtete Wissensgraphen erstellt. Knoten repräsentieren Konzepte, Kanten repräsentieren Beziehungen (z.B. "impliziert", "ist Teil von", "steht im Gegensatz zu").

4. **Sprachvergleich**: Ein neu entwickeltes Concept-Mapping-System gleicht sprachspezifische Konzepte auf eine gemeinsame Bedeutungsebene ab (z.B. "Freiheit", "自由" und "freedom" → CONCEPT_FREEDOM). Anschließend werden drei Metriken berechnet:
   - **Language Drift Score (LDS)**: Ähnlichkeit der Graphstrukturen
   - **Concept Shift**: Unterschiede in den verwendeten Konzeptmengen
   - **Relation Shift**: Unterschiede in den Beziehungsmustern

### Pilotstudie

In einer Pilotstudie mit Wikipedia-Artikeln zu fünf Konzepten in drei Sprachen (15 Texte) wurde der Pipeline getestet:

| Konzept | LDS (Mittel) | Höchste Drift |
|---------|-------------|---------------|
| Erfolg | 0.972 | ZH: Familie + Anstrengung; DE: Karriere + Kompetenz; EN: Opportunity |
| Verantwortung | 0.831 | ZH: Pflicht + Gesellschaft; DE: Kausalität + Gesetz |
| Gerechtigkeit | 0.822 | ZH: soziale Harmonie; DE: Verfahren + Recht |
| Freiheit | 0.812 | ZH: Verantwortung + Gesellschaft; DE: positive/negative Freiheit |

Die Rangfolge der Konzepte (Success > Responsibility > Justice > Freedom) erwies sich als stabil über mehrere Methodenversionen hinweg.

### Geplante Humanstudie

In der nächsten Phase werden 30 Probanden (10 chinesische, 10 deutsche, 10 englische Muttersprachler) rekrutiert. Jeder Proband beantwortet 5 Fragen in allen drei Sprachen (within-subject Design). Die Ergebnisse werden mit einem Zweitannotator validiert (Cohen's Kappa ≥ 0.70).

### Bedeutung

LinguaGraph ist das erste Projekt, das KI-extrahierte kognitive Graphen für den systematischen Vergleich abstrakter sozialer Konzepte über drei Sprachen hinweg nutzt. Es bietet nicht nur eine neuartige Methode zur Quantifizierung sprachlicher Einflüsse auf das Denken, sondern auch praktische Anwendungen für bilinguale Bildung und interkulturelle Kommunikation.

---

## 3. 3-Minute Speech Script

> Für Video-Pitch oder Kurzpräsentation

```
[0:00-0:15] — Hook
Stell dir vor, jemand fragt dich: "Was ist Freiheit?"
Würdest du anders antworten, wenn die Frage auf Chinesisch,
Deutsch oder Englisch gestellt wird?

[0:15-0:45] — Persönliche Motivation
Ich bin in China aufgewachsen und lebe jetzt in Deutschland.
Jeden Tag merke ich: Wenn ich auf Chinesisch denke, kommen
mir andere Zusammenhänge in den Sinn als auf Deutsch oder Englisch.
"Freiheit" auf Chinesisch — das hat viel mit Familie und
Verantwortung zu tun. "Freiheit" auf Deutsch — da denke ich
an Selbstbestimmung und Recht.
Ist das nur mein Eindruck — oder steckt mehr dahinter?

[0:45-1:30] — Die Methode
Ich habe eine Methode entwickelt, die diese Frage
wissenschaftlich untersucht:
1. Probanden beantworten Fragen in drei Sprachen
2. KI extrahiert aus jeder Antwort die verwendeten Konzepte
3. Diese Konzepte werden als Graph dargestellt
4. Die Graphen werden sprachübergreifend verglichen

Das Besondere: Ich bilde verschiedene sprachliche Konzepte
auf eine gemeinsame Bedeutungsebene ab. "Freiheit", "自由"
und "freedom" werden als dasselbe Konzept erkannt — erst
dann wird der Vergleich fair.

[1:30-2:15] — Erste Ergebnisse
In einer Pilotstudie mit Wikipedia-Artikeln habe ich fünf
Konzepte getestet. Das Ergebnis:
"Erfolg" zeigt die größten Unterschiede zwischen den
Sprachen. Auf Chinesisch steht Erfolg im Zusammenhang mit
Familie und Anstrengung. Auf Deutsch mit Karriere und
Kompetenz. Auf Englisch mit Opportunity und Choice.

Ein neu entwickelter Wert, der Language Drift Score,
macht diesen Unterschied messbar: von 0,81 bei "Freiheit"
bis 0,97 bei "Erfolg".

[2:15-2:45] — Nächste Schritte
Jetzt beginnt der wichtigste Teil: Echte Probanden.
30 Menschen werden die Fragen in allen drei Sprachen
beantworten. Ein Zweitannotator wird die Ergebnisse
unabhängig überprüfen.

Gleichzeitig entsteht eine 3D-Visualisierung — die
"Cognitive City" — die die Gedankenwelt jeder Sprache
als eigene Stadt darstellt.

[2:45-3:00] — Abschluss
LinguaGraph zeigt: Sprache formt nicht nur, wie wir
sprechen, sondern wie wir denken. Und KI kann diesen
Unterschied sichtbar machen.
```

---

## 4. 5-Minute Speech Script

> Für ausführliche Präsentation oder Jurymitglieder

```
[0:00-0:20] — Hook mit Beispiel
Drei Freunde, drei Sprachen, eine Frage: "Was ist Erfolg?"
Der chinesische Freund sagt: "Erfolg bedeutet,
dass meine Familie stolz auf mich ist."
Der deutsche Freund: "Erfolg ist, wenn ich meine
beruflichen Ziele erreiche."
Der englische Freund: "Success means seizing
opportunities and achieving your potential."

Gleiches Konzept — aber völlig unterschiedliche
Antworten. Ist das Zufall? Oder formt die Sprache,
wie wir denken?

[0:20-1:00] — Persönliche Geschichte
Ich bin Rongjing, 15 Jahre alt, komme aus China
und lebe seit einiger Zeit in Deutschland.
Jeden Tag erlebe ich: Wenn ich auf Chinesisch über
ein Thema nachdenke, kommen mir andere Ideen als
auf Deutsch oder Englisch.

"Freiheit" auf Chinesisch — ich denke an Verantwortung
gegenüber der Familie.
"Freiheit" auf Deutsch — ich denke an Selbstbestimmung
und individuelle Rechte.
"Freiheit" auf Englisch — ich denke an politische Freiheiten
und free will.

Diese Beobachtung hat mich neugierig gemacht.
Kann man diesen Unterschied wissenschaftlich messen?

[1:00-2:00] — Wissenschaftlicher Hintergrund
Die Idee, dass Sprache das Denken beeinflusst, ist nicht neu.
Die Sapir-Whorf-Hypothese besagt, dass Sprache unsere
Wahrnehmung der Welt formt. Forscher wie Lera Boroditsky
haben gezeigt, dass Sprache Farbwahrnehmung, Zeitverständnis
und räumliches Denken beeinflusst.

Aber: Abstrakte soziale Konzepte wie Freiheit, Gerechtigkeit
oder Erfolg wurden bisher kaum in diesem Zusammenhang untersucht.
Genau hier setzt LinguaGraph an.

[2:00-3:30] — Technische Methode
LinguaGraph besteht aus vier Schritten:

Schritt 1 — Datenerhebung:
Probanden beantworten 5 offene Fragen in Chinesisch,
Deutsch und Englisch. Die Fragen sind einfach: "Was ist
Freiheit?", "Was ist Erfolg?", "Was bedeutet Heimat für dich?"

Schritt 2 — KI-Extraktion:
Ein Large Language Model analysiert jede Antwort und
extrahiert die verwendeten kognitiven Konzepte und deren
Beziehungen. Zum Beispiel:
"Freiheit bedeutet, eigene Entscheidungen zu treffen"
→ Konzepte: Freiheit, Entscheidung
→ Beziehung: Freiheit ermöglicht Entscheidung

Schritt 3 — Graphkonstruktion:
Aus den extrahierten Konzepten und Beziehungen wird
ein Wissensgraph erstellt — eine Art Landkarte des Denkens.

Schritt 4 — Sprachvergleich:
Das Herzstück ist ein Concept-Mapping-System. Es gleicht
sprachspezifische Konzepte auf eine gemeinsame Bedeutungsebene ab.
"Freiheit", "自由" und "freedom" werden als dasselbe Konzept
erkannt — erst dann wird der Vergleich fair und aussagekräftig.
Mit dem Language Drift Score (LDS) wird die Ähnlichkeit der
Graphstrukturen quantifiziert.

[3:30-4:15] — Ergebnisse der Pilotstudie
In einer Pilotstudie habe ich 15 Wikipedia-Artikel zu
fünf Konzepten in drei Sprachen analysiert:

| Konzept | LDS | Wichtigster Unterschied |
|---------|-----|------------------------|
| Erfolg | 0.97 | ZH: Familie; DE: Karriere; EN: Opportunity |
| Verantwortung | 0.83 | ZH: Pflicht; DE: Kausalität |
| Gerechtigkeit | 0.82 | ZH: soziale Harmonie; DE: Verfahren |
| Freiheit | 0.81 | ZH: Verantwortung; DE: Selbstbestimmung |
| Heimat | TBD | Noch nicht abgeschlossen |

Die Rangfolge blieb stabil, als ich die Methode veränderte —
ein Zeichen dafür, dass der LDS ein verlässliches Maß ist.

[4:15-4:45] — Geplante Humanstudie
Jetzt beginnt der wichtigste Teil:
30 Probanden — 10 chinesische, 10 deutsche und 10 englische
Muttersprachler — werden die Fragen beantworten.
Ein Zweitannotator wird die KI-Ergebnisse überprüfen.
Das Ziel: Nachweisen, dass die sprachabhängigen Unterschiede
nicht nur in Wikipedia-Texten, sondern auch im Denken
realer Menschen existieren.

[4:45-5:00] — Vision und Abschluss
Stellen Sie sich vor, Sie könnten die Gedankenwelt eines
Menschen als Stadt sehen — Gebäude sind Konzepte, Straßen
sind Verbindungen. LinguaGraph macht diese Vision möglich
mit der "Cognitive City", einer 3D-Visualisierung, die
Sprachunterschiede auf einen Blick zeigt.

Ich glaube, dass dieses Projekt nicht nur wissenschaftlich
relevant ist, sondern auch praktisch: Es kann helfen,
bilinguale Bildung zu verbessern und interkulturelle
Kommunikation zu fördern.

Weil Sprache nicht nur ist, wie wir sprechen.
Sprache ist, wie wir denken.
```

---

## 5. Poster Structure

> Für mögliche Posterpräsentation im Finale

```
┌─────────────────────────────────────────────────────┐
│  LinguaGraph: How Language Shapes Thinking           │
│  Eine KI-basierte Analyse kognitiver Strukturen      │
├──────────┬──────────────────────────────────────────┤
│ TITEL    │ LinguaGraph — Mapping How Language        │
│ BEREICH  │ Shapes Thinking                           │
├──────────┼──────────────────────────────────────────┤
│ LINKS    │ RECHTS: Forschungsergebnisse               │
│          │                                           │
│ Problem  │ Top Drift Ranking:                        │
│ Sprache  │ ┌──────────┬──────┬──────────────────┐   │
│ formt    │ │ Konzept  │ LDS  │ Haupterkenntnis   │   │
│ Denken?  │ ├──────────┼──────┼──────────────────┤   │
│          │ │ Erfolg   │ 0.97 │ Familie vs. Kar. │   │
│ Bisher:  │ │ Verantw. │ 0.83 │ Pflicht vs. Ges. │   │
│ Farben,  │ │ Gerecht  │ 0.82 │ Harmonie vs. Ver.│   │
│ Raum     │ │ Freiheit │ 0.81 │ Verantw. vs. Sel.│   │
│          │ └──────────┴──────┴──────────────────┘   │
│ Jetzt:   │                                           │
│ Soziale  │ Geplante Humanstudie:                     │
│ Konzepte │ 30 Probanden (10 ZH, 10 DE, 10 EN)        │
│          │ Within-subject Design                     │
│          │ Zweitannotator (κ ≥ 0.70)                 │
├──────────┼──────────────────────────────────────────┤
│ METHODE  │ VISUALISIERUNG                            │
│          │                                           │
│ 1. Probandenantwort (ZH/DE/EN) │ ZH City │ DE City │
│ 2. KI-Extraktion (LLM)        │  🏙️     │  🏙️     │
│ 3. Wissensgraph (NetworkX)    │  ~~~~~  │  ~~~~~  │
│ 4. Concept Mapping            │ EN City │          │
│ 5. LDS Berechnung             │  🏙️     │ ← LDS   │
│                              │         │          │
├──────────┴──────────────────────────────────────────┤
│ KONTAKT / INFO                                      │
│ GitHub: LinguaGraph | BWKI 2026                        │
└─────────────────────────────────────────────────────┘
```

---

## 6. Video Script (3-Minuten Pitch)

> Direkt für die Video-Einreichung

### Szene 1: Persönlich (0:00-0:30)

**Visual**: Du sitzt an einem Tisch, vor dir drei Flaggen (China, Deutschland, UK/USA). Du sprichst in die Kamera.

**Audio**:
"Hallo, ich bin Rongjing. Ich bin in China geboren und lebe jetzt in Deutschland. Jeden Tag erlebe ich etwas Faszinierendes: Wenn ich auf Chinesisch über ein Thema nachdenke, kommen mir andere Ideen als auf Deutsch. 'Freiheit' auf Chinesisch bedeutet für mich Verantwortung. 'Freiheit' auf Deutsch bedeutet Selbstbestimmung. Ist das nur mein Gefühl — oder steckt Wissenschaft dahinter?"

### Szene 2: Das Problem (0:30-1:00)

**Visual**: Drei Sprechblasen mit gleicher Frage "Was ist Freiheit?" in ZH/DE/EN. Unterschiedliche Wörter tauchen auf.

**Audio**:
"Genau diese Frage untersuche ich in meinem BWKI-Projekt LinguaGraph. Die Idee, dass Sprache das Denken beeinflusst — der sogenannte Sapir-Whorf-Effekt — ist bekannt für Farben und Raum. Aber gilt er auch für abstrakte Konzepte wie Freiheit, Gerechtigkeit oder Erfolg? Und kann KI diesen Einfluss messbar machen?"

### Szene 3: Die Methode (1:00-1:50)

**Visual**: Animierter Pipeline-Durchlauf: Text → Zahnrad (KI) → Punkte mit Linien (Graph) → Zahlen.

**Audio**:
"Meine Methode arbeitet in vier Schritten:
Erstens: Probanden beantworten einfache Fragen in drei Sprachen.
Zweitens: Eine KI extrahiert aus jeder Antwort die verwendeten Konzepte und deren Beziehungen.
Drittens: Diese werden als Wissensgraph dargestellt — eine Landkarte des Denkens.
Viertens: Ich vergleiche diese Landkarten über Sprachen hinweg.

Der Schlüssel ist ein Concept-Mapping-System: Es stellt sicher, dass 'Freiheit', '自由' und 'freedom' als dasselbe Konzept erkannt werden. Erst dann ist der Vergleich fair."

### Szene 4: Erste Ergebnisse (1:50-2:20)

**Visual**: Balkendiagramm: LDS-Werte für 4 Konzepte. Dann drei Mini-Cities nebeneinander.

**Audio**:
"Meine Pilotstudie mit Wikipedia-Texten zeigt klare Unterschiede: 'Erfolg' hat den höchsten Language Drift Score — 0,97. Im Chinesischen ist Erfolg mit Familie verbunden, im Deutschen mit Karriere, im Englischen mit Opportunity. 'Freiheit' liegt bei 0,81 — ähnlicher, aber immer noch deutlich unterschiedlich strukturiert."

### Szene 5: Ausblick (2:20-2:50)

**Visual**: Aufbau einer 3D-City aus dem Graph. Drei Cities nebeneinander mit Brücken dazwischen.

**Audio**:
"Der nächste Schritt ist entscheidend: 30 echte Probanden werden die Fragen beantworten. Gleichzeitig entsteht eine 3D-Visualisierung — die Cognitive City — die die Gedankenwelt jeder Sprache als eigene Stadt darstellt. Chinesisch, Deutsch und Englisch — drei Städte, eine Karte."

### Szene 6: Abschluss (2:50-3:00)

**Visual**: Du wieder im Bild, lächelnd.

**Audio**:
"LinguaGraph zeigt: Sprache formt, wie wir denken. Und KI kann diesen Unterschied sichtbar machen. Danke für Ihre Aufmerksamkeit."

---

## 7. Timeline für kreative Einreichung

| Datum | Aufgabe | Status |
|-------|---------|--------|
| 2026-06-28 | Ideeneinreichung (150 Wörter) | ⏳ MUSS |
| 2026-07-15 | Video-Skript fertig | ⏳ |
| 2026-08-01 | Rohvideo aufnehmen | ⏳ |
| 2026-08-15 | Cognitiv City Video-Clip fertig | ⏳ |
| 2026-09-01 | Endgültige Einreichung | ⏳ |
| 2026-09-21 | Abgabefrist | ⛔ |
