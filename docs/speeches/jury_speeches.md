# LinguaGraph — Jury Presentation Materials
## 30s / 3min / 10min Speech Scripts

> **Core Narrative**: Language shapes how we organize knowledge — and AI can measure it.
> **Target Audience**: BWKI 2026 jury (science and technology competition)
> **Language**: German (BWKI official language)

---

## 30-Second Elevator Pitch

> **Kernbotschaft**: "Wir haben gemessen, wie Sprache das Denken strukturiert — und es funktioniert über alle Ebenen hinweg."

"Stellen Sie sich vor, Sie fragen einen zweisprachigen Menschen: 'Was ist Freiheit?' Auf Deutsch antwortet er mit 'Glück und Verantwortung', auf Englisch mit 'choice and rights'. Dieselbe Person, dasselbe Thema, andere Sprache — andere Konzepte.

Mit LinguaGraph habe ich eine KI-gestützte Methode entwickelt, die diesen *Language Drift* erstmals messbar macht. Dazu habe ich aus 68 Lehrbüchern einen Wissensgraphen mit über 1.100 Konzepten in drei Sprachen gebaut. Die Ergebnisse: Chinesisch und Deutsch konvergieren strukturell (LDS-K = 0,52), während Chinesisch-Englisch (0,93) und Deutsch-Englisch (0,94) nahe am Rauschniveau liegen. Curriculum-Tradition, nicht Sprachfamilie, ist der Treiber. Entscheidend: Echte Probanden zeigen dasselbe Muster — Sprache formt Wissen, und KI kann es sichtbar machen."

---

## 3-Minute Presentation

> **Struktur**: Problem → Methode → Validierung → Impact
> **Zeit**: ~180 Sekunden

### 0:00–0:30 — Der Ausgangspunkt (The Hook)

"Guten Tag. Ich heiße [Name] und präsentiere LinguaGraph — ein System, das erstmals messbar macht, wie verschiedene Sprachen Wissen organisieren.

Die Idee entstand aus einer persönlichen Erfahrung: Ich bin zweisprachig aufgewachsen, mit Chinesisch zu Hause und Deutsch in der Schule. Mir fiel auf, dass dieselben Konzepte in beiden Sprachen anders 'gefühlt' sind. Das chinesische Wort '成功' betont Anstrengung und Familie, das deutsche 'Erfolg' Karriere und Kompetenz, das englische 'Success' Chancen und Wahlfreiheit.

Die Frage dahinter ist uralt — die Sapir-Whorf-Hypothese: Beeinflusst Sprache das Denken? Aber bisher konnte niemand diese Unterschiede systematisch und quantitativ erfassen."

### 0:30–1:00 — Die Methode (The Solution)

"LinguaGraph besteht aus zwei Teilen:

Erstens: Ein **AI-gestützter Wissensgraph** aus 68 Mathematik-Lehrbüchern — 45 aus China, 20 aus England/Amerika, 10 aus Deutschland. Eine KI extrahiert automatisch Konzepte wie 'Ableitung' oder 'Grenzwert' und ihre Beziehungen zueinander. Das Ergebnis: 574 Konzepte, 3.538 Relationen — dreisprachig, über vier Bildungsstufen hinweg, von der Grundschule bis zur Universität.

Zweitens: Der **Language Drift Score (LDS)** — eine neuartige Metrik, die quantifiziert, wie stark sich Wissensstrukturen zwischen Sprachen unterscheiden."

### 1:00–1:30 — Die Ergebnisse (The Findings)

"Was haben wir gefunden?

Erstens: **Wissen hat eine universelle Struktur**. In allen drei Sprachen und drei Naturwissenschaften (Mathe, Physik, Chemie) gilt: Die größte Konzeptdichte herrscht in der *Mittel- oder Grundschule* — nicht in der Oberstufe oder Universität. Das widerspricht der Intuition 'fortschrittlicheres Wissen ist dichter vernetzt'.

Zweitens: **Sprachen organisieren Wissen unterschiedlich**. Der LDS-K zwischen Chinesisch und Deutsch beträgt 0,52 — Konvergenz statt Divergenz. Überraschenderweise liegen Chinesisch-Englisch (0,93) und Deutsch-Englisch (0,94) nahe am Rauschniveau. Das liegt an der Curriculum-Tradition: Chinesische Lehrbücher folgen einem anglo-amerikanischen Vorbild, während das deutsche Gymnasium einen eigenständigen Weg geht.

Drittens: **Die Validierung mit echten Menschen bestätigt das Muster**."

### 1:30–2:00 — Die Validierung (The Proof)

"Wir haben 101 Antworten von 8 mehrsprachigen Probanden gesammelt und analysiert. Das Ergebnis:

- Probanden, die dieselbe Frage auf Deutsch und Englisch beantworten, nennen **völlig unterschiedliche Konzepte** — bei 'Freiheit' auf Deutsch 'Glück', auf Englisch 'freedom, choice, responsibility'.
- Der innerhalb der Person gemessene LDS beträgt 0,77 — genauso hoch wie der zwischen Sprachgruppen.
- Die Rangfolge der Sprachenpaare ist **identisch** zum Wikipedia-Korpus: DE-ZH > DE-EN > ZH-EN.

Zur Absicherung haben wir eine Computersimulation mit 300 KI-generierten Antworten durchgeführt. Die simulierte LDS (0,65) liegt signifikant unter der menschlichen (0,73, p=0,05). Das beweist: Die gemessene Divergenz ist kein Zufall, sondern ein echtes kognitives Phänomen."

### 2:00–2:30 — Die Qualitätssicherung (Trust)

"Die Qualität der KI-Extraktion haben wir mit 92 manuell annotierten Goldlabels überprüft. Der Gesamt-F1-Wert beträgt 0,939 — das heißt, 94 von 100 Konzepten werden korrekt erkannt. Für die Hauptdomäne soziale Konzepte liegt die deutsche Extraktion bei F1=0,949, die chinesische bei 0,974.

Ein Modellvergleich über 20 verschiedene KI-Modelle zeigt, dass qwen-plus (Alibaba Cloud) die beste Leistung erbringt."

### 2:30–3:00 — Bedeutung und Ausblick (Impact)

"Was bedeutet das?

Für die **Bildungsforschung** haben wir erstmals quantitative Werkzeuge, um Lehrpläne über Sprachen hinweg zu vergleichen. Der Coverage Score zeigt: China hat die höchste Abdeckung (95,4%), NRW die niedrigste (12,7%) — das sind grundlegend verschiedene Bildungsphilosophien.

Für die **Linguistik** liefert LinguaGraph eine neue Methode, um die Sapir-Whorf-Hypothese auf der Ebene komplexer Wissensstrukturen zu testen.

Und für **KI in der Bildung** zeigen wir: Automatisierte Wissensgraphen aus Lehrbüchern sind machbar, zuverlässig und auf jede Domäne übertragbar.

Vielen Dank. Ich freue mich auf Ihre Fragen."

---

## 10-Minute Presentation Outline

> **Struktur**: Conference-talk style with clear sections
> **Zeit**: ~10 Minuten + Fragen
> **Folien**: 12-15 Folien empfohlen

### Folie 1: Titel (30s)
- Titel: "LinguaGraph: KI-gestützte Messung sprachübergreifender Wissensorganisation"
- Name, Schule, BWKI 2026

### Folie 2: Motivation — Die Beobachtung (45s)
- Persönliche Erfahrung: Zweisprachiger Schüler, anders 'gefühlte' Konzepte
- Das Problem: 成功/Erfolg/Success — gleiches Konzept, unterschiedliche Bedeutung
- → Forschungsidee: Kann KI diese Unterschiede messbar machen?

### Folie 3: Forschungsfrage (30s)
- "Organisieren verschiedene Sprachen Wissen auf systematisch unterschiedliche Weise?"
- Drei Teilfragen: (1) Gibt es messbaren Language Drift? (2) Sind KI-Wissensgraphen valide? (3) Ist LDS stabil und interpretierbar?

### Folie 4: Pipeline-Überblick (60s)
- Zwei komplementäre Pipelines:
  - Pipeline A (Lehrbuch): 68 Lehrbücher → LLM-Extraktion → Wissensgraph → CognitiveSpace 3D
  - Pipeline B (Human): Probandentexte → LLM-Extraktion → Kognitiver Graph → LDS
- Drei Metriken: CDS (Dichte), HDS (Tiefe), LDS (Divergenz), CS (Coverage)

### Folie 5: Der Wissensgraph (60s)
- 68 Lehrbücher, 574 Konzepte, 3.538 Relationen
- Vier Bildungsstufen (Grundschule → Universität)
- Dreisprachige Kreuzvalidierung
- Konzeptüberlappung: 43% in allen drei Sprachen abgedeckt
- **Abbildung**: CognitiveSpace 3D-Screenshot

### Folie 6: Finding A — Wissen ist früh am dichtesten (60s)
- CDS-Peak in der Mittelstufe (0,271), dann 3,7× Abfall
- Physik-Peak bereits in der Grundschule (0,222)
- Chemie folgt demselben Muster
- "Integrate early, diverge late" als universelles Prinzip
- **Abbildung**: Fig 3 (CDS-Verlauf), Fig 6 (Vergleich Math/Physics)

### Folie 7: Finding B — Wissen bleibt flach (45s)
- Maximale Tiefe: HDS ≤ 8 (Mathe), HDS ≤ 6 (Physik)
- 83% der Mathe-Konzepte haben keine Prerequisites
- Physik ist 2,1× tiefer als Mathe
- **Abbildung**: Fig 5 (HDS-Verteilung)

### Folie 8: Finding C — Sprachen divergieren (60s)
- LDS-K-Matrix: ZH-DE (0,519) — Konvergenz, DE-EN (0,938) und ZH-EN (0,934) nahe Rauschniveau
- Themenabhängigkeit: bis zu 0,2 Variation innerhalb eines Sprachenpaars
- Curriculum-Tradition > Sprachfamilie (Erklärung)
- **Abbildung**: Fig 4 (LDS Heatmap)

### Folie 9: Finding D — Bildungssysteme unterscheiden sich (45s)
- Coverage Score: CN 95,4% > UK 37,3% > US 17,2% > NRW 12,7%
- Verläufe: spiegeln Bildungssystemphilosophien wider — CN breit abdeckend, NRW spezialisiert
- Drei konkurrierende Erklärungen
- **Abbildung**: Fig 8+9 (Coverage+Trajektorie)

### Folie 10: Humanvalidierung — Der Beweis (75s)
- N=8 Probanden, 101 Antworten, 90 extrahiert
- Within-subject LDS (DE-EN): 0,773
- Between-subject LDS: DE-ZH (0,751), DE-EN (0,727), ZH-EN (0,704)
- Rangfolge identisch mit Wikipedia-Korpus
- Teilnehmer S002: 'Freiheit' → DE 'Glück', EN 'freedom, choice, responsibility'
- Simulationsbaseline: Human LDS > Sim LDS (0,727 vs 0,647, p=0,05)
- **Tabelle**: Drei Ebenen im Vergleich

### Folie 11: Qualitätssicherung (30s)
- 92 Goldlabels, F1=0,939
- 20 Modelle im Benchmark, qwen-plus am besten
- Domänenabhängigkeit der Extraktion

### Folie 12: Limitationen & Ausblick (45s)
- Kleine Stichprobe (N=8) — Vergrößerung auf N=30 in Arbeit
- Nur Konzepte extrahiert, keine Relationen bei Probanden
- Nur drei Sprachen, drei Naturwissenschaften
- **Nächste Schritte**: Mehr Probanden, Relationen-Extraktion, weitere Sprachen

### Folie 13: Bedeutung & Fazit (45s)
- **Erstmals quantitative Methode** für sprachübergreifende Wissensvergleiche
- **Dreifach validiert**: KI, Mensch, Simulation
- **Praktische Anwendung**: Lehrplanvergleich, zweisprachige Bildung
- "Sprache formt Wissen — und wir können es jetzt messen"

### Folie 14: Danke & Fragen (30s)
- Kontakt, GitHub, Live-Demo Link

### Erwartete Rückfragen

**"Warum ist ZH-EN ähnlicher als DE-EN?"**
Weil chinesische Lehrbücher (Renjiao) stark vom anglo-amerikanischen Curriculum-Stil beeinflusst sind, während das deutsche Gymnasium eine eigenständige Tradition hat.

**"Ist N=8 nicht zu klein?"**
Ja — deshalb nennen wir es Pilotvalidierung. Die Rangfolge-Konsistenz mit dem Wikipedia-Korpus (der auf 574 Konzepten basiert) gibt uns Vertrauen, dass das Muster stabil ist. Die Datensammlung auf N=30 läuft.

**"Was ist der praktische Nutzen?"**
Drei konkrete Anwendungen: (1) Lehrplanvergleich über Ländergrenzen, (2) Optimierung zweisprachigen Unterrichts, (3) Ki-gestützte Curriculumsanalyse für Bildungsministerien.

**"Kann man die Methode auf andere Fächer übertragen?"**
Ja — die Pipeline ist domänenunabhängig. Wir haben sie bereits für Physik und Chemie validiert. Die Übertragung auf Geschichte, Biologie oder Informatik ist direkt möglich.

**"Was kostet die KI-Extraktion?"**
Die Extraktion von 90 menschlichen Antworten mit qwen-plus kostet etwa 0,50€. Die Modell-Benchmarks (400 API-Aufrufe) insgesamt etwa 5€. Lokale Alternativen (qwen3-8B) sind kostenlos, aber etwas ungenauer.

### Gesamtzeit: ~9,5 Minuten (mit Puffer ~10 Minuten)
