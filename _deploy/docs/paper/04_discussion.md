## 8. Diskussion

### 8.1 Zusammenfassung der Ergebnisse

Diese Studie führte LinguaGraph ein, ein wissensgraphbasiertes Rahmenwerk zur Analyse, wie mathematisches Wissen über Sprachen (Chinesisch, Deutsch, Englisch), Bildungsstufen (Grundschule bis Universität) und zuletzt auch Disziplinen (Mathematik vs. Physik) hinweg organisiert ist. Zwölf zentrale Befunde ergaben sich (F11 und F12 wurden auf Basis der erweiterten N=15-Humanvalidierung revidiert):

| # | Befund | Evidenz |
|---|--------|----------|
| F1 | CDS erreicht Spitze in der Mittelstufe (0,271), nicht in der Grundschule | Nicht-monotonisches Dichtemuster |
| F2 | 3,7-facher Dichteabfall von der Mittel- zur Oberstufe | CDS 0,271 → 0,073; Konzeptanzahl 4,2-facher Anstieg |
| F3 | HDS ≤ 8 (Mittelwert 0,40); 83 % der Konzepte sind Wurzeln | Mathematik ist ein flaches Netz, kein tiefer Baum |
| F4 | Lehrbuch-LDS-K variiert stark (0,519 ZH-DE bis 0,938 DE-EN) | Strukturdominiert, nicht sprachgetrieben |
| F5 | Nullmodell falsifiziert LDS-K als Sprachmetrik: Voll < Struktur-Null | Gradverteilung dominiert; ΔLDS ist zentral |
| F6 | Verschiedene Disziplinen zeigen verschiedene CDS-Muster | Mathematik Spitze in Mittelstufe; Physik Spitze in Grundschule |
| F7 | Physik weist tiefere Voraussetzungsketten auf (HDS-Mittel 0,85 vs. 0,40) | Physikalisches Wissen ist stärker kumulativ |
| F8 | Chemie-CDS erreicht ebenfalls Spitze in der Mittelstufe (0,042) | Konsistent mit „Integriere früh, trenne spät“-Muster |
| F9 | Coverage-Scores variieren drastisch zwischen Bildungssystemen (12,7–95,4 %) | Lehrplandesign-Philosophie treibt Unterschiede |
| F10 | China zeigt nahezu perfekte Übereinstimmung (95,4 %); NRW am niedrigsten (12,7 %) | Zentralisiertes vs. föderales Systemmerkmal |
| **F11** | **Falsifiziert (N=15):** LDS-C auf Konzeptebene (0.93–0.96) ist nicht von Teilnehmervariabilität unterscheidbar (Split-Half-Boden 0.92–0.96; Label-Permutation 0.94). Keine konsistente sprachspezifische Rangordnung. | Nullmodell-Suite (Within-Lang Split-Half, Label-Permutation) |
| **F12** | **Überarbeitet (N=15):** Der Unterschied zur Simulationsbasislinie (0.647) ist ein Artefakt der Extraktions-/Alignierungsmethode (höhere LDS-Skala), nicht ein Beleg für sprachliche Kognition. LDS-C ≈ Within-Language-Null → **kein** über Zufall hinausgehendes Sprachsignal. | LDS-C ≈ Split-Half-Boden; ΔLDS ≈ 0 (−0.05 bis +0.05) |

### 8.2 Interpretation des CDS-Gipfels

Der Befund, dass der Concept Density Score seinen Höhepunkt in der Mittelstufe erreicht (F1) und nicht in der Grund- oder Hochschule, bedarf einer sorgfältigen Interpretation. Eine naive Erwartung könnte lauten, dass „höher entwickeltes Wissen dichter vernetzt ist.“ Die Daten widersprechen dem: Der Mathematiklehrplan der Mittelstufe fungiert als **Wissensdichteknotenpunkt**, an dem grundlegende Arithmetik, einfache Algebra, Geometrie und Wahrscheinlichkeitskonzepte eng miteinander verbunden sind. Dieses Muster ist konsistent mit Ausubels Assimilationstheorie [12], die vorhersagt, dass Wissensstrukturen in Phasen der Konsolidierung vor der Aufspaltung in Spezialisierungen eine maximale Integration erreichen.

Der anschließende 3,7-fache Abfall von der Mittel- zur Oberstufe (F2) fällt mit einer 4,2-fachen Ausweitung der Konzeptanzahl zusammen, was darauf hindeutet, dass der Mathematiklehrplan an diesem Übergang bewusst diversifiziert wird. Dies könnte ein pädagogisches Gestaltungsprinzip widerspiegeln: Die Mittelstufe vermittelt eine integrierte Grundlage; die Oberstufe führt spezialisierte Teilbereiche ein (Analysis, Vektorgeometrie, Statistik), die in relativer Isolation gelehrt werden, bevor eine mögliche Reintegration auf universitärem Niveau erfolgt.

Die Robustheit dieses Befundes über drei Sprachen hinweg (ZH, EN, DE) deutet darauf hin, dass es sich nicht um ein Artefakt einer bestimmten Lehrbuchtradition handelt. Vielmehr könnte es eine universelle Eigenschaft der mathematischen Lehrplangestaltung widerspiegeln — oder zumindest eine Konvergenz über drei unterschiedliche Bildungssysteme hinweg.

### 8.3 Sprachübergreifende strukturelle Divergenz: Eine Nullmodell-Kritik

Die LDS-K-Ergebnisse (F4) zeigen eine erhebliche Variation zwischen den Sprachpaaren: ZH-EN=0,934, DE-EN=0,938, ZH-DE=0,519. Der ZH-DE-Wert sticht hervor — chinesische und deutsche Lehrbuchwissensstrukturen sind beträchtlich ähnlicher (niedrigerer LDS-K) als jede von beiden im Vergleich zum Englischen. Dies stellt unmittelbar die naive Erwartung in Frage, dass typologisch entfernte Sprachen (ZH-DE) die größte Divergenz aufweisen würden.

Um zu bestimmen, ob diese Werte echte sprachgetriebene strukturelle Unterschiede darstellen, wandten wir eine **Nullmodell-Suite** mit vier Bedingungen an:

| Bedingung | Beschreibung | ZH-EN | DE-EN | ZH-DE |
|:----------|-------------|:-----:|:-----:|:-----:|
| Voll (LDS-K-Baseline) | Realer Graphenvergleich | 0,934 | 0,938 | 0,519 |
| Struktur-Null | Grad-erhaltende Kantenumordnung (×1000) | **0,957** | **0,957** | **0,717** |
| Knotenpermutations-Null | Zufällige Neuzuweisung von Knotenbezeichnungen | 0,934 | 0,938 | 0,519 |
| Vollständig zufällig | Erdős–Rényi-Graph | 1,000 | 1,000 | 1,000 |

Der entscheidende Befund: **Vollständiges LDS-K < Struktur-Null-LDS-K für alle drei Sprachpaare.** Unter grad-erhaltender Randomisierung (Doppelkantentausch, 1000 Iterationen) sind die randomisierten Graphen systematisch *unterschiedlicher* voneinander als die realen Graphen. Dies bedeutet, dass Lehrbuchwissensstrukturen *stärker* konvergieren, als der Zufall vorhersagen würde — das Gegenteil dessen, was eine sprachgetriebene Divergenzhypothese erwarten würde.

Dieses Ergebnis falsifiziert die Interpretation, dass LDS-K sprachgetriebene kognitive Divergenz misst. Stattdessen werden die hohen LDS-K-Werte von der **Gradverteilungsstruktur** dominiert — einer Eigenschaft, die sprachübergreifend geteilt wird, weil mathematische Voraussetzungslogik universell ist. Wenn die Gradverteilungen erhalten bleiben (Struktur-Null), sinkt die strukturelle Ähnlichkeit, was zeigt, dass das, was Lehrbuchgraphen „ähnlich“ macht, ihre gemeinsame Gradstruktur ist, nicht die sprachspezifische Inhaltsanordnung.

Die theoretische Implikation ist bedeutsam: Während mathematische Wahrheit universell ist, ist der hier erzielte Befund stärker — auch die *organisatorischen Strukturen* von Lehrbüchern sind sprachübergreifend bemerkenswert konvergent. Drei unterschiedliche Bildungstraditionen (Chinesisch, Deutsch, Englisch) produzieren unabhängig voneinander Lehrbuchwissensgraphen, deren strukturelle Eigenschaften (Gradverteilungen, Dichteprofile) einander ähnlicher sind als vergleichbare Graphen mit derselben Gradsequenz.

Dies bedeutet, dass der Korpusanalyse-Ansatz (LDS-K) per se keine sprachrelativistischen Effekte auf die Wissensorganisation messen kann. Er misst in erster Linie **strukturelle Konvergenz**, die von der universellen Logik mathematischer Voraussetzungen angetrieben wird. Um ein genuines Sprachsignal zu isolieren, müssen wir zur kognitiven Ebene übergehen — dem Vergleich, wie Menschen ihr Wissen in ihrer Muttersprache ausdrücken — erfasst durch ΔLDS = LDS-C − LDS-K.

Die erweiterte Humanvalidierung (N=15, F11) liefert jedoch ein negatives Ergebnis für diese Verschiebung: Die menschlichen LDS-C-Werte (Konzeptebene ZH-EN=0,963, DE-EN=0,932, ZH-DE=0,936) liegen **nahe der Within-Language-Null** (Split-Half-Boden 0,92–0,96) und sind von Label-Permutation nicht unterscheidbar (0,94). ΔLDS ≈ 0 (−0,05 bis +0,05), nicht > 0. Damit wird die naive Hypothese „Sprache → unterschiedliche Konzeptgraphen" auf allen drei Analyseebenen (Konzept, Kategorie, Relation) falsifiziert.

### 8.4 Disziplinübergreifende Validierung

Die Hinzunahme der Physik (F6, F7) bestätigt, dass die CDS- und HDS-Metriken echte strukturelle Eigenschaften der Wissensorganisation erfassen und nicht lediglich Artefakte des Mathematik-Korpus darstellen. Die kontrastierenden Muster — Mathematik gipfelt in der Mittelstufe, Physik in der Grundschule — zeigen, dass **Wissensorganisation disziplinabhängig ist**, wobei beide demselben „Integriere früh, trenne spät“-Muster folgen, jedoch auf unterschiedlichen Bildungsstufen.

Dieser Befund hat Implikationen für die Lehrplangestaltung. Wenn Mathematik- und Physikstudierende grundlegend unterschiedliche Wissensdichtetrajektorien durchlaufen, dann sind pädagogische Strategien, die für eine Disziplin wirken, möglicherweise nicht auf die andere übertragbar. Der Mathematikunterricht könnte frühe Integration betonen; der Physikunterricht könnte akzeptieren, dass Integration auf fortgeschrittenem Niveau ein natürlicher Bestandteil des Lernverlaufs ist.

### 8.5 Die Lehrplanebene

Die Integration von Lehrplanstandards (Kernlehrplan NRW, UK National Curriculum, US NGSS/CCSS) in das Wissensgraphen-Rahmenwerk offenbart einen systematischen Befund: **Die Übereinstimmung zwischen Lehrbuch und Lehrplan variiert dramatisch zwischen den Bildungssystemen**:

| System | Coverage-Score | Muster |
|--------|:-------------:|--------|
| China (CN) | 95,4 % | Nahezu perfekte Ausrichtung (zentraler Lehrplan) |
| England (UK) | 37,3 % | Mäßig; am höchsten in der Sekundarstufe II |
| Vereinigte Staaten (US) | 17,2 % | Niedrig (breite Richtlinien, lokale Variation) |
| NRW Deutschland | 12,7 % | Niedrigste (detaillierte, studiengangspezifische Vorgaben) |

Der Coverage-Score misst die **Lehrplan-→Lehrbuch-**Übereinstimmung: Findet sich zu jedem Lehrplankonzept ein entsprechendes Konzept im Lehrbuchgraph? Die dramatische Spanne — von 12,7 % (NRW) bis 95,4 % (CN) — spiegelt grundlegende Unterschiede in der Bildungsgovernance wider: Zentrale Systeme erzeugen enge Ausrichtung; föderale Systeme mit studiengangspezifischen Vorgaben erzeugen von Natur aus niedrigere messbare Übereinstimmung.

### 8.6 Warum erzeugen Bildungssysteme unterschiedliche Wissensstrukturen?

Die erhebliche systemübergreifende Variation der Coverage-Scores (12,7–95,4 %) wirft eine über die Messung hinausgehende Frage auf: **Was erklärt diese Unterschiede?** Wir betrachten drei konkurrierende Erklärungsansätze.

#### Erklärungsansatz A: Granularität des Lehrplans (am besten gestützt)

Die sparsamste Erklärung ist, dass sich Lehrpläne in ihrer Granularität unterscheiden. Der NRW-Kernlehrplan spezifiziert 299 Mathematikkonzepte über 6 Stufen, während der UK National Curriculum ähnliche Inhalte mit 397 breiteren Deskriptoren abdeckt. Wenn ein Lehrplan Konzepte in feinerer Granularität definiert, kann jedes Lehrbuchkonzept definitionsgemäß weniger Lehrplankonzepte abdecken — was niedrigere Coverage-Scores unabhängig von der tatsächlichen Übereinstimmung der Inhalte erzeugt.

Dies wird durch das NRW-stufenweise Muster gestützt: Die Abdeckung erreicht ihren Höhepunkt in der Sek I (Klassen 7–8), wo sich der Lehrplan auf gemeinsame Kerninhalte konzentriert, und fällt in der Sek II (Klassen 11–13) ab, wo der Lehrplan spezialisierte Kurse (Grundkurse, Leistungskurse) mit feinkörnigeren Kompetenzerwartungen einführt.

#### Erklärungsansatz B: Bildungsphilosophie und Prüfungsstruktur (höherer Interpretationswert)

Das britische Muster (37,3 %) und das US-Muster (17,2 %) spiegeln unterschiedliche Bildungsphilosophien wider. Der UK National Curriculum bietet einen mäßig vorschreibenden Rahmen, an dem sich Lehrbücher auf Sekundarstufenebene orientieren. Die USA zeigen eine geringere Ausrichtung (17,2 %), was mit breiten, nicht vorschreibenden Richtlinien (NGSS/CCSS) konsistent ist, die lokale Anpassungen ermöglichen. Chinas nahezu perfekte Ausrichtung (95,4 %) ist konsistent mit einem zentralisierten Lehrplansystem, in dem Lehrbücher nach expliziten nationalen Standards verfasst werden.

Diese Interpretation deckt sich mit der vergleichenden Bildungsforschung: Schmidt et al. (2001) fanden, dass die Kohärenz von Lehrplänen zwischen TIMSS-Ländern erheblich variiert, wobei China eine hohe Übereinstimmung zwischen intendierten und implementierten Lehrplänen aufweist. In jüngerer Zeit dokumentiert die OECD-Veröffentlichung „Education at a Glance“ (2023), dass föderale Strukturen eine stärker variierende Lehrplanumsetzung hervorbringen als zentrale Systeme.

#### Erklärungsansatz C: Arbeitsteilung zwischen Lehrplan und Lehrbuch (am differenziertesten)

Eine dritte Möglichkeit ist, dass sich die Beziehung zwischen Lehrbuch und Lehrplan in den verschiedenen Systemen grundlegend unterscheidet. In der deutschen Tradition legen Lehrpläne minimale Kompetenzstandards fest, während Lehrbücher erhebliche Autonomie in der Wissensorganisation ausüben. Im chinesischen System werden Lehrbücher direkt aus dem nationalen Lehrplan entwickelt, was eine nahezu perfekte Ausrichtung (95,4 %) erzeugt.

Nach dieser Interpretation ist der niedrige Coverage-Score NRWs (12,7 %) kein Mangel, sondern ein Merkmal: Deutsche Lehrbücher sind darauf ausgelegt, alternative organisatorische Strukturen anzubieten, die den Lehrplan ergänzen statt zu duplizieren. Dies würde vorhersagen, dass NRW-Lehrbücher eine HÖHERE interne strukturelle Diversität (mehr Variation zwischen Verlagen) aufweisen als chinesische Lehrbücher — eine testbare Hypothese für zukünftige Arbeiten.

#### Synthese

Die drei Erklärungen schließen sich nicht gegenseitig aus. Die Lehrplangranularität (A) ist die sicherste Interpretation, die Bildungsphilosophie (B) bietet die reichhaltigste Erzählung und die Arbeitsteilung zwischen Lehrplan und Lehrbuch (C) eröffnet die interessantesten Forschungsfragen. Unsere Daten sind mit allen drei konsistent, aber ihre Beurteilung erfordert zusätzliche Evidenz — insbesondere systemübergreifende Analysen der Lehrplankonzept-Granularität und der inhaltlichen Diversität von Lehrbüchern.

Diese Herausforderung — die Trennung von Messungseffekten und echten strukturellen Unterschieden — ist selbst ein Beitrag: Sie zeigt, dass systemübergreifende Bildungsvergleiche eine sorgfältige Beachtung der Struktur des Referenzstandards erfordern, nicht nur des Lehrbuchgraphen.

### 8.7 Extraktionszuverlässigkeit und Fehleranalyse

Ein potenzielles Bedenken bei jeder LLM-basierten Analyse ist, ob Messfehler die berichteten Ergebnisse verursachen könnten. Unsere Extraktionsvalidierung anhand von 92 Goldstandard-Annotationen (ZH F1=0,974, DE F1=0,949, EN F1=0,882) deutet darauf hin, dass die Extraktionsqualität des früheren primären Extraktionsmodells (qwen-plus) insgesamt hoch ist. Die Fehleranalyse zeigt, dass 29 % der Extraktionsfehler bei sehr kurzen Antworten (1–2 Wörter) auftreten, bei denen eine leere Extraktion tatsächlich angemessen ist. Bei den verbleibenden Fehlern handelt es sich überwiegend um partielle Auslassungen — 1–2 Konzepte aus einer Liste von 3–4 fehlen — und nicht um systematische Fehlleitungen.

**Hinweis zur N=15-Erweiterung**: Die erweiterte Humanvalidierung (§4) wurde mit `deepseek-v4-flash` (opencode GO) extrahiert; eine erneute F1-Validierung gegen die Goldstandards steht aus. Der 19-Modell-Benchmark (§8.9) zeigt jedoch, dass Konzeptextraktionsqualität über Modellfamilien hinweg eine Eigenschaft der Aufgabe ist (F1-Bereich 0,55–0,67), sodass eine modellinduzierte Skalenverschiebung der LDS-C zwar möglich, eine systematische Verzerrung der Null-Relation (beobachtet ≈ Split-Half) aber unwahrscheinlich ist.

Diese Fehlerverteilung bedeutet, dass die strukturellen Metriken (CDS, HDS, LDS, Coverage-Score) robust gegenüber Extraktionsrauschen sind: Partielle Auslassungen reduzieren die Konzeptanzahlen leicht, verzerren jedoch nicht systematisch die Graphentopologie oder die sprachübergreifenden Vergleiche. Wir halten es daher für unwahrscheinlich, dass die berichteten Befunde Artefakte der Extraktionsmethodik sind.

### 8.8 Robustheitsprüfung: Rechnerische Basislinie — methodisch revidiert

Zur Kontrolle, ob die beobachteten LDS-Werte echte strukturelle Unterschiede und nicht zufällige Konzeptvariation widerspiegeln, wurde ursprünglich eine **rechnerische Basislinie** aus 300 simulierten Antworten (20 pro Bedingung × 5 Themen × 3 Sprachen) berechnet. Die frühere Version dieser Analyse (N=8, qwen-plus-Extraktion) ergab einen scheinbaren Unterschied zwischen menschlichem LDS (0,727) und Simulation (0,647, p=0,05).

**Diese Vergleich ist mit der N=15-Erweiterung nicht mehr haltbar**, aus zwei Gründen:

1. **Skalenverschiebung**: Die neue, standardisierte Extraktion (deepseek-v4-flash) verschiebt LDS-C auf eine andere Skala (0,93–0,96); ein direkter Vergleich mit der alten Simulationsverteilung mischt zwei unterschiedliche Messverfahren.
2. **Null-Test-Ergebnis**: Die korrekte Kontrolle ist nicht der Vergleich zweier Absolutwerte, sondern die Lage der beobachteten LDS-C relativ zur Within-Language-Null (Split-Half 0,92–0,96; Label-Permutation 0,94). Beobachtete LDS-C liegt **auf** diesem Boden → vollständig durch Teilnehmervariabilität erklärbar.

Ein aussagekräftiger Mensch-vs-Simulation-Vergleich erfordert **dieselbe Extraktions-/Alignierungsmethode** für beide Bedingungen. Dies ist eine Aufgabe für zukünftige Arbeit (nicht mehr eine Stütze der ΔLDS > 0-Hypothese).

### 8.9 Robustheitsprüfung: Modellübergreifende Extraktionskonsistenz

Um zu überprüfen, ob die LDS-Ergebnisse nicht von einem einzelnen Extraktionsmodell getrieben werden, führten wir einen **19-Modell-Benchmark** über drei API-Plattformen durch (DashScope, DeepSeek API, OpenCode GO). Alle Modelle extrahierten Konzepte aus denselben N≥50 Goldstandard-Items:

| Rang | Modell | F1 | N | Quelle |
|:----:|-------|:--:|:-:|--------|
| 1 | hy3-preview | 0,6741 | 57 | OpenCode GO |
| 2 | mimo-v2.5-pro | 0,6735 | 75 | OpenCode GO |
| 3 | **qwen-plus** | **0,6659** | 92 | DashScope |
| 4 | **qwen-max** | **0,6610** | 92 | DashScope |
| 5–10 | Gemischte Modelle | 0,59–0,63 | 79–92 | Gemischt |
| 11–19 | Untere Stufe | 0,55–0,59 | 89–92 | Gemischt |

**Zentrale Ergebnisse**: (1) Alle 19 Modelle erreichen F1 > 0,55, was bestätigt, dass die Konzeptextraktion modellfamilienübergreifend robust ist. (2) Qwen-plus (das primäre Extraktionsmodell) belegt Rang 3 mit F1=0,666 und liegt damit innerhalb des oberen Clusters. (3) DeepSeek-Modelle (v4-pro mit 0,593, v4-flash mit 0,608) sind wettbewerbsfähig. (4) Der enge F1-Bereich (0,55–0,67) über verschiedene Architekturen hinweg (Qwen, DeepSeek, GLM, MinMax, Kimi, Mimo) deutet darauf hin, dass die Extraktionsqualität eine Eigenschaft der Aufgabe ist, nicht eines bestimmten Modells.

Ein sekundärer Befund: 186 zusätzliche DashScope-Modelle (Text, Vision, Sprache) erzeugten alle F1=0,0, was bestätigt, dass diese andere Prompting-Strategien erfordern. GPT-4o und GPT-4o-mini waren aufgrund von Guthabenbeschränkungen während des Benchmarks nicht mehr verfügbar.

### 8.10 Threats to Validity

Wir identifizieren sechs Hauptbedrohungen für die Validität der berichteten Ergebnisse.

**Abhängigkeit vom Extraktionsmodell**. Alle LDS-Berechnungen hängen von der Konzeptextraktion mittels qwen-plus ab. Während der 19-Modell-Benchmark die modellübergreifende Konsistenz bestätigt (F1-Bereich 0,55–0,67), könnte eine andere Extraktionsarchitektur systematisch andere Konzeptmengen erzeugen und möglicherweise die LDS-Werte verändern. Diese Bedrohung wird durch den engen F1-Bereich über verschiedene Modellfamilien hinweg teilweise abgemildert.

**Repräsentativität des Korpus**. Der Mathematik-Korpus (68 Lehrbücher) ist umfassend, jedoch verzerrt: Chinesische Lehrbücher stammen überwiegend von einem einzigen Verlag (Renjiao), deutsche Lehrbücher sind in Richtung universitärer Materialien verschoben und der englische Korpus ist auf IGCSE-/IB-Rahmenwerke beschränkt. Die sprachinterne Split-Half-Null (LDS≈0,97) quantifiziert diese Bedrohung.

**Übersetzungsasymmetrie bei der Konzeptausrichtung**. Die sprachübergreifende Konzeptausrichtung hängt von Expertenurteilen ab. Fehlausrichtungen erhöhen den LDS, indem sie zur Vereinigungsmenge beitragen, ohne die Schnittmenge zu erhöhen. Diese Bedrohung wird durch die Struktur der aligned_groups teilweise kontrolliert, aber die asymmetrische Abdeckung bleibt eine Quelle von Messfehlern.

**Auswahlverzerrung der Lehrpläne**. Lehrplandokumente variieren in ihrer Granularität (NRW: 299 Konzepte, UK: 397, US: 2.124, CN: 87). Höhere Granularität senkt mechanisch die Coverage-Scores. Unsere stufenweise Analyse kontrolliert dies teilweise.

**Begrenzte Stichprobengröße und Between-Subject-Design (Pilot-Menschendaten)**. Die ΔLDS-Analyse beruht auf N=15 Teilnehmenden (6 DE, 6 ZH, 3 EN) in einem Between-Subject-Design. Die Nullmodell-Suite zeigt, dass bei dieser Stichprobengröße die Teilnehmervariabilität die Sprachgruppe dominiert: sprachgetriebene Divergenz kann nicht von individueller Variabilität getrennt werden. Eine Post-hoc-Power-Rechnung (`scripts/sw_fix_analyses.py`, t-Test-Approximation) bestätigt dies: Bei kleinen bis mittleren Effekten (d=0,2–0,5) hat ein 6-gegen-6-Between-Vergleich nur Power 0,06–0,12, ein gepaarter Within-Vergleich mit N=15 dagegen 0,11–0,44 (N=30: 0,19–0,75). Die menschliche Null ist damit auch power-analytisch erwartbar — kein Beleg für Abwesenheit, sondern eine Grenze des Designs selbst. Die registrierte Folgeuntersuchung (R1) nutzt folgerichtig Within-Subject mit N≥30 pro Arm.

**Reichweite des Nullmodells**. Die grad-erhaltende Struktur-Null testet die Kantenanordnung über die Gradstruktur hinaus, jedoch nicht, ob die Gradstruktur selbst sprachbeeinflusst ist. Ein zukünftiges hierarchisches Nullmodell könnte diese Frage angehen.

### 8.11 LDS-Interpretationsrahmen

Anstatt willkürliche Schwellenwerte für LDS-Werte festzulegen, verankern wir die Interpretation an der Nullmodell-Suite:

| LDS-Bereich | Interpretation | Anker |
|:---------:|---------------|--------|
| > 0,97 | Vollständige Divergenz | Über dem sprachinternen Rauschboden |
| 0,90–0,97 | Typische sprachübergreifende Divergenz | Nahe am Rauschboden |
| 0,50–0,90 | Partielle Konvergenz | Unterhalb des Rauschbodens, oberhalb der Struktur-Null |
| 0,00–0,50 | Erhebliche Konvergenz | Deutlich unter allen Nullenwartungen |

In diesem Rahmen:
- **Sprachinterner Rauschboden** ≈ 0,97 (Split-Half) → Obergrenze für aussagekräftigen Vergleich
- **Struktur-Null** ≈ 0,96 (graderhaltend) → strukturelle Basislinie
- **Vollständig zufällig** = 1,00 → Plausibilitätsprüfung

ZH-DE (0,519) liegt im Bereich der „partiellen Konvergenz“ — deutlich unter den Nullenwartungen. ZH-EN (0,934) und DE-EN (0,938) liegen im Bereich „nahe am Rauschboden“ — nicht unterscheidbar von zwei zufälligen Hälften desselben sprachlichen Lehrbuchgraphen. Hierbei handelt es sich in erster Linie um Beobachtungen und nicht um Erklärungen; der Mechanismus, der die Heterogenität zwischen den Paaren antreibt, erfordert weitere Untersuchungen.

### 8.12 Einschränkungen

Mehrere Einschränkungen sollten anerkannt werden:

**Umfang der Daten**. Der Mathematik-Korpus (68 Lehrbücher, 556 Konzepte) ist umfassend. Der Physik-Korpus (366 Konzepte) und der Chemie-Korpus (220 Konzepte) ermöglichen eine disziplinübergreifende Validierung, bleiben aber kleiner. Die Lehrplangraphen decken zwar vier Systeme ab (NRW, UK, US, China), verwenden jedoch unterschiedliche Abgleichsmethoden, die die Vergleichbarkeit beeinträchtigen können.

**Extraktionsmethodik**. Während unsere Goldstandard-Validierung eine insgesamt hohe Qualität belegt (F1=0,939), wurden die sozialwissenschaftlichen Golddaten mittels halbautomatischen Schlüsselwortabgleichs mit anschließender manueller Überprüfung validiert. Im Goldstandard selbst könnten einige Fehler verbleiben.

**Stichprobengröße und Design der menschlichen Validierung**. Die erweiterte Humanstudie (N=15, 6 DE · 6 ZH · 3 EN) bestätigt die frühere Einschränkung und verschärft sie: Bei N=15 in einem **Between-Subject-Design** dominiert Teilnehmervariabilität die messbare LDS-C vollständig (Split-Half-Boden ≈ beobachtete LDS-C ≈ Label-Permutation). Dies ist kein Stichprobenfehler, sondern eine **strukturelle Grenze des Designs**: Da jede Person nur in einer Sprache antwortet, können sprachgetriebene Divergenz und individuelle Variabilität nicht getrennt werden. Die zentrale methodologische Lehre: Zukünftige Studien benötigen (a) ein Within-Subject-Design, (b) größere Stichproben pro Sprachgruppe (N≥30), oder (c) Metriken, die gegen individuelle Konzeptwahl robust sind. Die thematischen Richtungstendenzen (ZH rechtlich/moralisch, DE autonom/affektiv, EN sozial) bieten eine testbare Hypothese für ein Within-Subject-Design.

**Interpretation des Nullmodells**. Während die graderhaltende Struktur-Null zeigt, dass LDS-K von strukturellen Faktoren und nicht von der Sprache dominiert wird, bewahrt der Doppelkantentausch-Algorithmus die exakte Gradsequenz jedes Graphen. Dies ist eine konservative Null: Sie testet, ob sprachspezifische Kantenanordnungen über die Gradstruktur hinaus Informationen hinzufügen, testet jedoch nicht, ob die Gradstruktur selbst sprachbeeinflusst sein könnte. Ein zukünftiges hierarchisches Nullmodell könnte diese geschichtete Frage angehen.

**Kantenfreie Graphen in früheren menschlichen Daten**. Die frühere qwen-plus-Extraktion erzeugte eine rein konzeptbasierte Ausgabe (keine Relationen) für menschliche Antworten. In der N=15-Erweiterung wurde dies behoben: Eine Relationsextraktion (7 Typen, `scripts/lds_c_extract_relations.py`) lieferte 162 Kanten (DE 59, ZH 67, EN 36), sodass die vollständige v3-LDS-Formel (Node- + Edge-Jaccard) angewendet werden konnte. Das Ergebnis bestätigt die Konzeptebene: Edge-Jaccard ≈ 0 und Split-Half-Boden ≈ beobachtete v3-LDS — kein separierbares Sprachsignal. Die Kantenzahl pro Antwort bleibt jedoch spärlich, sodass Kantenaussagen auf Gruppenebene robust, auf individueller Ebene aber eingeschränkt interpretierbar sind.

**Kausalität**. Unsere Analyse ist korrelativ. Wir messen strukturelle Unterschiede zwischen Systemen, können diese jedoch nicht unabhängig voneinander auf Lehrplangestaltung, Lehrbuchtradition oder Bildungsphilosophie zurückführen.

**Generalisierbarkeit**. Mathematik, Physik und Chemie könnten strukturelle Eigenschaften teilen, die in geistes- oder sozialwissenschaftlichen Disziplinen nicht vorhanden sind. Die Erweiterung auf zusätzliche Domänen ist eine Priorität.

**LDS-Interpretation**. Der LDS-Interpretationsrahmen (Abschnitt 8.11) verankert numerische Werte an Nullmodell-Baselines, jedoch sind die Schwellenwerte (0,90, 0,50) deskriptiv statt inferenziell. Mit zunehmenden menschlichen Daten sollten Bootstrap-Konfidenzintervalle diese deskriptiven Schwellenwerte für Hypothesentests ersetzen.

### 8.13 Implikationen

Trotz dieser Einschränkungen haben die vorliegenden Ergebnisse Implikationen für drei Fachgemeinschaften:

**Für die Bildungsforschung**: Die CDS- und HDS-Metriken bieten quantitative Werkzeuge für die Lehrplananalyse, die bestehende qualitative Rahmenwerke (TIMSS, PISA) ergänzen. Eine Lehrplangestalterin könnte CDS verwenden, um Dichteengpässe zu identifizieren, und HDS, um übermäßig lange Voraussetzungsketten zu erkennen.

**Für KI in der Bildung**: Die automatisierte Pipeline zeigt, dass die groß angelegte, sprachübergreifende Konstruktion von Wissensgraphen aus Lehrbüchern mit aktuellen LLMs machbar ist. Dies eröffnet die Möglichkeit einer Lehrplanebenen-Wissensanalyse in einem Umfang, den die manuelle Inhaltsanalyse nicht erreichen kann.

**Für die Erforschung des linguistischen Relativitätsprinzips**: Unsere Daten stützen keine einheitliche „Sprache formt Wissen“-Behauptung. Stattdessen zeigen sie, dass sprachübergreifende strukturelle Beziehungen heterogen sind — einige Sprachpaare konvergieren erheblich (ZH-DE), während andere auf Rauschniveau liegen (ZH-EN, DE-EN). Die erweiterte Humanvalidierung (N=15) erlaubt eine präzise Antwort auf der Ebene menschlicher Konzeptäußerungen: In einem Between-Subject-Design ist bei dieser Stichprobe **kein separierbares Sprachsignal** nachweisbar. Das LLM-as-Subject-Experiment (§5) zeigt jedoch, dass dies ein **Design-Artefakt** ist: Unter Within-Subject-Bedingungen ist das Sprachsignal klar nachweisbar (LDS-C 0.93–0.96 ≫ Boden 0.85–0.87), mit dem Sprachcode als dominanter Organisationsebene. Dies falsifiziert die einfache Hypothese „Sprache → unterschiedliche Konzeptgraphen" nur für das Between-Subject-Design, nicht für die Existenz sprachlicher Kognitionseffekte überhaupt. Die Richtungstendenzen (ZH rechtlich/moralisch, DE autonom/affektiv, EN sozial) bleiben als testbare Hypothesen für Within-Subject-Studien erhalten.

### 8.14 LLM-as-Subject: Methodologische Einordnung des Within-Subject-Befunds

Das LLM-as-Subject-Experiment (§5) liefert den methodologischen Schlüssel zur Interpretation des negativen Humanbefunds:

1. **Design über Signal**: Derselbe Messrahmen (LDS-C + Nullmodelle) produziert unter Between-Subject (Menschen) kein trennbares Signal, unter Within-Subject (LLM) ein deutliches (LDS-C übersteigt den Boden um +0.08 bis +0.09). Die Sprachlabels tragen unter Within-Subject-Bedingungen messbare Information.

2. **Mechanismus**: Das lineare gemischte Modell trennt die marginalen Beiträge — der Sprachcode dominiert (same_lang +0.038, p<0.001), der kulturelle Rahmen hat keinen signifikanten codeübergreifenden Beitrag (same_frame +0.001, p=0.90). Der Rahmen wirkt als code-interner Modulator; die codeübergreifende Divergenz wird von der lexikalisch-assoziativen Ebene getragen. Die freien Assoziationen desselben Modells erklären die Konzeptdivergenz für EN-Paare (M2), nicht aber für ZH-DE, wo eine strukturelle Ebene jenseits der Assoziationsstatistik existiert.

3. **Validität des LLM als Subjekt**: Die Verwendung eines LLM als kontrolliertem kognitivem Subjekt folgt etablierten Paradigmen (Binz & Schulz, 2023; Hagendorff, 2023) und beantwortet eine Frage, die mit menschlichen Between-Subject-Daten prinzipiell nicht beantwortbar ist. Das Modell ist kein Ersatz für menschliche Kognition, sondern ein Werkzeug zur Isolation der Sprachvariable bei konstantem „Gewichtssatz". Diese Grenze ist zu betonen: Die Ergebnisse zeigen, dass Sprachcode und Rahmen die Konzeptwahl eines LLM verändern — sie extrapolieren nicht direkt auf menschliche Kognition, liefern aber eine testbare Blaupause (Within-Subject-Design, erwartete Effektrichtung) für zukünftige Humanstudien.

4. **Präzisierung des Design-Artefakts (Design-Effekt-Beweis, §5.9.1–5.9.2)**: Der Vergleich auf identischem Messrahmen zeigt eine **gleiche Signalamplitude** bei Mensch und LLM (LDS-C jeweils 0.93–0.96); die menschliche Null ist **nicht** auf "keine Sprachwirkung" und **nicht** auf "Between-Subject-Design an sich" zurückzuführen (eine virtuelle Between-Subject-Analyse der LLM-Daten bei menschlicher N überlebt das Signal). Entscheidend ist die **individuelle Heterogenität innerhalb einer Sprachgruppe**: Sie hebt die Bodenlinie (0.92–0.96) auf das Signalniveau. Die Heterogenitäts-Injektion (§5.9.2b) zeigt als **Konsistenz-Demonstration**, dass eine ausreichende Aggregationssparsität die menschliche Null reproduzieren kann (q=0.30 → Marge +0.014 vs. menschlich +0.015) — wobei der mechanismus-konsistente Zielwert (q≈0.76–0.91) die Marge **nicht** vollständig kollabiert (P2-Recheck). Die heterogenitätsbedingte Erklärung ist damit gestützt (Exklusion + Konsistenz), aber nicht als quantitative Kausalzuordnung zu werten. Dies hat eine direkte Designimplikation — Between-Subject-Studien zum Sprachrelativismus benötigen entweder ausreichende N pro Gruppe, um die Heterogenität zu schlagen, oder ein Within-Subject-Design, das die Varianzquelle eliminiert.

5. **Strukturelle vs. lexikalische Divergenz (Knoten/Kanten, §5.9.4)**: Die soziale/institutionelle Umkehr ist **knotengetrieben** (Konzeptwahl), der Kantenbeitrag in der Mathematik am größten (0.074). Institutionelles Wissen konvergiert im *Was* (Konzepte), nicht im *Wie* (Beziehungen) — die relationale Organisation bleibt über alle Quellen systemisch divergent. Dies trennt den Mechanismus "Konzeptwahl" von "Beziehungsstruktur" und stützt die M2-Dominanz (§5.6) auf der Korpusseite: die Divergenz entsteht primär auf der assoziativ-lexikalischen Ebene, nicht auf der relationalen. **Einschränkung (P2-Recheck)**: Die Mathematik-Knoten sind Alignierungs-Labels (nicht unabhängig extrahierte Konzepte), das `de`-Label-Feld enthält teils chinesische Texte, und ein Size-Matching auf die Wikipedia-Größe kehrt das Muster um (bei k=15–35 ist der Wikipedia-J_node höher) — der mathematische J_node (0.556) ist damit teilweise ein Darstellungs-/Größen-Artefakt, nicht ein Beleg unabhängiger sprachübergreifender Konvergenz (Details: `docs/p2_methodology_rechecks.md`).

### 8.15 Modellübergreifende Replikation: Die Divergenz ist eine breit replizierbare, modellabhängige Eigenschaft

Ein zentraler Vorbehalt gegen den Within-Subject-Befund war dessen Beschränkung auf ein einzelnes Modell (deepseek-v4-flash). Eine Replikation des identischen P1-Protokolls (3 Sprachen × k=10, gleicher Messrahmen LDS-C/Floor/Nullmodelle) auf **54 weiteren Modellen** (50 eindeutige Modell-Identitäten; 42 über DashScope, 7 über zen/OpenRouter plus D1-Baseline, 2 über Kilo, je 1 über Cohere/NIM/opencode-go) — DeepSeek-, GLM-, Kimi-, MiniMax- und Qwen-Familien sowie nemotron-3-ultra + nemotron-3-super (NVIDIA, **US-Ursprung**), laguna-s-2.1 (Poolside, **US-Ursprung**, auf zwei Hosts), **gpt-oss-20b (OpenAI-Gewichte, US-Ursprung)**, **command-a (Cohere, CA-Ursprung)** und gpt-5.6-luna (Herkunft ungeklärt, offengelegt) — erweitert die Evidenz:

**Befund 1 — Signale replizieren breit, aber nicht ausnahmslos**: **Alle 55 Messungen zeigen LDS-C über dem jeweiligen Within-Language-Boden, und alle 55 ZH-DE-Paare sind signifikant** (p<0.05; die meisten p<0.01). Von den 165 Sprachpaar-Tests insgesamt sind **8 nicht signifikant** (p≥0.05) — **alle acht betreffen englisch-haltige Paare** (ZH-EN oder DE-EN), überwiegend bei DeepSeek-R1/Distill-Modellen (deepseek-r1-0528 DE-EN p=0.672). Die sprachübergreifende Wertedivergenz ist damit **eine breit replizierbare Eigenschaft mehrsprachiger LLMs**, aber mit modell- und sprachpaar-spezifischer Stärke — insbesondere ist die englisch-bezogene Divergenz in einigen Modellen statistisch nicht von der sprachinternen Varianz trennbar.

**Befund 2 — Divergenzmagnitude variiert modellabhängig (Rangordnung)**: Die ZH-DE-Marge reicht von +0.03 (deepseek-r1-0528) bis +0.42 (command-a-03-2025) — ein Faktor ~13 zwischen den extremsten Modellen. Für die Anwendung als KI-Validierungswerkzeug bedeutet dies eine **quantifizierbare Rangordnung der sprachübergreifenden Drift-Sensitivität** über Modelle hinweg. Hinweis: Absolute Margen sind über Modelle mit sehr unterschiedlicher Extraktionsdichte (z. B. command-a: Floor ~0,49 vs. typisch 0,70–0,87) nicht direkt vergleichbar; Signifikanz und Kulturrichtung sind es.

**Befund 3 — Die Kulturrichtung übersteigt das Zufallsniveau, am stärksten bei hoher Übereinstimmung**: Eine Voten-Analyse der ZH-DE-Divergenztreiber (wie viele Modelle markieren ein Konzept als nur-in-DE bzw. nur-in-ZH) wird gegen ein **frequenz-angepasstes Zufalls-Nullmodell** getestet (beobachtete Gesamthäufigkeit jedes Konzepts fixiert, Richtung jeder Stimme zufällig mit p=0.5). Die beobachtete Zahl richtungskonsistenter Konzepte (max(DE,ZH)-Stimmen ≥ t) übersteigt das Nullmodell bei **allen** Schwellen (p<0.001), am stärksten bei hoher Übereinstimmung: ≥10 Stimmen 218 vs. 147±4; ≥20 Stimmen 61 vs. 12±2. Die stärksten Konzepte (Heimat:safety 46 Stimmen DE; Heimat:physical space 44 ZH-Stimmen; equal opportunity 42) stützen die DE-Autonomie/ZH-Raum-Orientierung. Wichtig: Die Stärke ist begrenzt — z. B. produzierten nur 46 von 56 Modellen Heimat:safety überhaupt als einseitigen Treiber, und 5 Modelle wurden auf zwei Hosts gemessen (Redundanz).

**Ehrliche Abgrenzung**: Die Replikation umfasst 50 eindeutige Modell-Identitäten; 5 Modelle wurden auf zwei Hosts gemessen (zen + DashScope ×4, laguna zen + Kilo), was die Effektivität der "55" verringert; **~87 % der Messungen stammen von chinesischen Anbietern** — der westliche Anteil umfasst sieben Messungen (NVIDIA nemotron-3-ultra + nemotron-3-super, Poolside laguna-s-2.1 auf zwei Hosts, OpenAI-Gewichte gpt-oss-20b, Cohere command-a, gpt-5.6-luna/Herkunft ungeklärt). Eine Anbieter-Stratifizierung der 55 vollständigen Messungen (`scripts/sw_fix_analyses.py`): CN-Stratum 48/48 ZH-DE-Paare signifikant (mittlere Marge 0,130), West-Stratum 7/7 signifikant (mittlere Marge 0,182) — richtungskonsistent, aber als Anbieter-*Vergleich* weiter unterpowert, daher Transparenzbericht. Dass Modelle herkunftsunabhängig stärker mit US-Werten alignieren, ist als Branchenmuster dokumentiert [42]; die Herstellererweiterung (Modell-Matrix) bleibt registrierte Folgearbeit. Die Divergenz ist als **Messgröße** (nicht als normatives "Problem") zu interpretieren: Ein Modell, das Wertkonzepte in der Zielsprache kulturadäquat rahmt, ist nicht notwendigerweise fehlerhaft. Als **Vorschlag für einen operativen Schwellenwert** ("hohe sprachübergreifende Divergenz") dient die ZH-DE-Marge (LDS-C − Boden) ≥ 0.10 — bezogen auf die beobachtete Spanne von +0.03 bis +0.42 über 55 Messungen trennt dieser Wert die hoch-divergenten Modelle (command-a, kimi-k2.6, deepseek-v3.x, nemotron) von den niedrig-divergenten (deepseek-v4-flash/pro, r1-Distill). Dies ist eine **heuristische** Festlegung für die Anwendung, keine validierte Validitätsgrenze; eine kalibrierte Schwelle bleibt zukünftiger Arbeit überlassen. Eine Youden-Kalibrierung [46] auf den 55 vollständigen ZH-DE-Margen (Median-Split-Klassen, Bootstrap-CI über Modelle; `scripts/sw_fix_analyses.py`) stützt die Größenordnung: balancierte Trennung bei 0,13 (95 %-CI 0,13–0,14); die Heuristik 0,10 liegt knapp unterhalb des CI und wirkt damit sensitiv-inklusiv — quantifiziert, aber weiterhin keine validierte Grenze. Ehrlichkeitshinweis: Die Klassen stammen aus einem Median-Split derselben 55 Margen, sodass die Trennung (J=1,0) teilweise tautologisch ist; die Kalibrierung ist eine Konsistenzprüfung, keine unabhängige Validierung.

**Robustheit der Replikationsaussage (Sensitivitäten)**: Vier vorausgenommene Einwände wurden quantitativ geprüft. (a) *Multiples Testen*: Bei 165 Tests ohne Korrektur wären unter der globalen Null ~8 falsch-positive Treffer zu erwarten; die Permutationsauflösung (500 Iterationen) kann ein Bonferroni-Niveau (0,05/165≈0,0003) formal nicht auflösen. Entscheidend ist die Meta-Betrachtung: Alle 55 ZH-DE-Paare überschreiten sämtliche 500 Permutationen (p<0,002 einseitig je Test); unter der globalen Null wären 55×0,002≈0,11 solcher Treffer erwartet — beobachtet wurden 55. (b) *Doppelzählung*: Dedupliziert auf 50 eindeutige Identitäten (je Dual-Host eine Messung) bleiben 50/50 ZH-DE-Paare signifikant; mittlere Marge 0,140 (vs. 0,136 über 55), Spanne unverändert +0,03…+0,42. Der Voten-Bias durch Doppelstimmen ist auf ≤10 Stimmen begrenzt und ändert keine Schwellen-Aussage (≥10: 218 vs. 147±4; ≥20: 61 vs. 12±2). (c) *luna-Provenienz*: Ohne das Herkunft-ungeklärte luna-Modell bleiben 6/6 West-Messungen signifikant (mittlere Marge 0,176 vs. 0,182 mit luna). (d) *Selektionsbias*: Von 86 begonnenen Messungen sind 55 vollständig (je 10/10/10); 31 blieben unvollständig (API-Limits, Kosten-Stopp, Modell-EOL) — der Ausfall korreliert mit westlichen/ratelimitierten Kanälen und ist in `docs/session_handoff_20260910.md` dokumentiert. Die Complete-Case-Analyse bleibt damit eine Verfügbarkeitsstichprobe, kein präregistriertes Design. (e) *Floor-Normierung*: Die Rangordnungs-Aussage (Befund 2) wurde zusätzlich floor-normiert geprüft (Ratio = LDS-C/Boden, je Modell in den Replikationsdaten vorhanden): Die Rangkorrelation zwischen Marge und Ratio beträgt Spearman 0,997, die Top-5 sind identisch, command-a bleibt auch normiert Rang 1 (Ratio 1,87); West-Ratio im Mittel 1,284 vs. CN 1,169. Die Rangordnung wird daher nicht vom Floor-Niveau getrieben — der Kollaps-Hinweis zu command-a (Boden ~0,49) betrifft die absolute Deutung, nicht die Ordnung. (f) *Familie×Sprachpaar*: Die 8 nicht-signifikanten EN-Tests konzentrieren sich auf die R1/Distill-Familie — 6/10 EN-Tests bei 5 R1/Distill-Modellen vs. 2/100 bei allen übrigen 50 Modellen; der mittlere EN-Boden liegt bei R1/Distill höher (0,844 vs. 0,784). Die Konfundierung Sprache×Modellfamilie ist damit benannt und quantifiziert: Die EN-Hub-Deutung bleibt Hypothese, die Alternative „Reasoning-Verbosität hebt den Boden und schluckt das EN-Signal" ist nicht ausgeschlossen.

### 8.16 Kulturell-psychologische Einordnung der Divergenzrichtung

Die beobachtete Divergenzrichtung — DE-seitig Autonomie/Regeln/Ziel (equal opportunity, freedom limit, decision, goal, safety), ZH-seitig Raum/Boundary/Anspruch/Harmonie (physical space, boundary, deserved treatment, the weak, indulgence) — ist **konsistent mit etablierten kulturell-psychologischen Rahmen**:

1. **Selbstkonstruktion (Markus & Kitayama, 1991)** [37]: Die Theorie unterscheidet eine **unabhängige** (independent) von einer **interdependenten** Selbstkonstruktion. Individuell-orientierte Kulturen (typisch westlich) rahmen Werte über persönliche Autonomie, Leistung und regelbasierte Gerechtigkeit — deckungsgleich mit der DE-seitigen Treiberstruktur (Autonomie, eigene Ziele, Chancengleichheit). Interdependent-orientierte Kulturen (typisch ostasiatisch) rahmen Werte über relationale Grenzen, Harmonie und Fürsorge für die Gruppe — deckungsgleich mit der ZH-seitigen Struktur (Raum, Grenzen, Anspruch, Schutz der Schwachen, Nachsicht).

2. **Individualismus/Kollektivismus (Hofstede, 1980, 2001)** [38]: Deutschland weist einen hohen Individualismus-Index auf (≈67), China einen deutlich niedrigeren (≈20). Dies sagt vorher, dass deutsche Rahmungen Wertkonzepte individualistisch (Autonomie, Leistung) und chinesische kollektivistisch (Beziehung, Harmonie, Gruppenpflicht) organisieren.

3. **Konfuzianischer Beziehungsraum**: Die ZH-seitige Betonung von "Raum/Grenze/Anspruch" (物理空间, 边界, 应得) ist mit dem konfuzianisch geprägten relationalen Selbst vereinbar, das soziale Grenzen und den eigenen "Platz" in der Beziehungsordnung betont (vgl. Nisbett, 2003: holistische vs. analytische Kognition) [39].

**Ehrliche Einordnung**: Diese Übereinstimmung ist eine **interpretative Hypothese** (die Richtung ist mit den Rahmen konsistent), kein Test der Theorien. Die Richtung ist modell- und trainingsdatenspezifisch und wird als **beschreibend** berichtet; eine kausale Zuordnung (Sprache → Kulturrahmen) ist nicht beansprucht.
