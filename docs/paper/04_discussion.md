## 4. Diskussion

### 4.1 Zusammenfassung der Ergebnisse

Diese Studie führte LinguaGraph ein, ein wissensgraphbasiertes Rahmenwerk zur Analyse, wie mathematisches Wissen über Sprachen (Chinesisch, Deutsch, Englisch), Bildungsstufen (Grundschule bis Universität) und zuletzt auch Disziplinen (Mathematik vs. Physik) hinweg organisiert ist. Elf zentrale Befunde ergaben sich (F11 und F12 wurden auf Basis der erweiterten N=15-Humanvalidierung revidiert):

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
| **F12** | **Überarbeitet (N=15):** Der Unterschied zur Simulationsbasislinie (0.647) ist ein Artefakt der Extraktions-/Alignierungsmethode (höhere LDS-Skala), nicht ein Beleg für sprachliche Kognition. LDS-C ≈ Within-Language-Null → **kein** über Zufall hinausgehendes Sprachsignal. | LDS-C ≈ Split-Half-Boden; ΔLDS ≈ 0 (−0.02 bis +0.05) |

### 4.2 Interpretation des CDS-Gipfels

Der Befund, dass der Concept Density Score seinen Höhepunkt in der Mittelstufe erreicht (F1) und nicht in der Grund- oder Hochschule, bedarf einer sorgfältigen Interpretation. Eine naive Erwartung könnte lauten, dass „höher entwickeltes Wissen dichter vernetzt ist.“ Die Daten widersprechen dem: Der Mathematiklehrplan der Mittelstufe fungiert als **Wissensdichteknotenpunkt**, an dem grundlegende Arithmetik, einfache Algebra, Geometrie und Wahrscheinlichkeitskonzepte eng miteinander verbunden sind. Dieses Muster ist konsistent mit Ausubels Assimilationstheorie [12], die vorhersagt, dass Wissensstrukturen in Phasen der Konsolidierung vor der Aufspaltung in Spezialisierungen eine maximale Integration erreichen.

Der anschließende 3,7-fache Abfall von der Mittel- zur Oberstufe (F2) fällt mit einer 4,2-fachen Ausweitung der Konzeptanzahl zusammen, was darauf hindeutet, dass der Mathematiklehrplan an diesem Übergang bewusst diversifiziert wird. Dies könnte ein pädagogisches Gestaltungsprinzip widerspiegeln: Die Mittelstufe vermittelt eine integrierte Grundlage; die Oberstufe führt spezialisierte Teilbereiche ein (Analysis, Vektorgeometrie, Statistik), die in relativer Isolation gelehrt werden, bevor eine mögliche Reintegration auf universitärem Niveau erfolgt.

Die Robustheit dieses Befundes über drei Sprachen hinweg (ZH, EN, DE) deutet darauf hin, dass es sich nicht um ein Artefakt einer bestimmten Lehrbuchtradition handelt. Vielmehr könnte es eine universelle Eigenschaft der mathematischen Lehrplangestaltung widerspiegeln — oder zumindest eine Konvergenz über drei unterschiedliche Bildungssysteme hinweg.

### 4.3 Sprachübergreifende strukturelle Divergenz: Eine Nullmodell-Kritik

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

Die erweiterte Humanvalidierung (N=15, F11) liefert jedoch ein negatives Ergebnis für diese Verschiebung: Die menschlichen LDS-C-Werte (Konzeptebene ZH-EN=0,961, DE-EN=0,933, ZH-DE=0,934) liegen **nahe der Within-Language-Null** (Split-Half-Boden 0,92–0,96) und sind von Label-Permutation nicht unterscheidbar (0,94). ΔLDS ≈ 0 (−0,02 bis +0,05), nicht > 0. Damit wird die naive Hypothese „Sprache → unterschiedliche Konzeptgraphen" auf allen drei Analyseebenen (Konzept, Kategorie, Relation) falsifiziert.

### 4.4 Disziplinübergreifende Validierung

Die Hinzunahme der Physik (F6, F7) bestätigt, dass die CDS- und HDS-Metriken echte strukturelle Eigenschaften der Wissensorganisation erfassen und nicht lediglich Artefakte des Mathematik-Korpus darstellen. Die kontrastierenden Muster — Mathematik gipfelt in der Mittelstufe, Physik in der Grundschule — zeigen, dass **Wissensorganisation disziplinabhängig ist**, wobei beide demselben „Integriere früh, trenne spät“-Muster folgen, jedoch auf unterschiedlichen Bildungsstufen.

Dieser Befund hat Implikationen für die Lehrplangestaltung. Wenn Mathematik- und Physikstudierende grundlegend unterschiedliche Wissensdichtetrajektorien durchlaufen, dann sind pädagogische Strategien, die für eine Disziplin wirken, möglicherweise nicht auf die andere übertragbar. Der Mathematikunterricht könnte frühe Integration betonen; der Physikunterricht könnte akzeptieren, dass Integration auf fortgeschrittenem Niveau ein natürlicher Bestandteil des Lernverlaufs ist.

### 4.5 Die Lehrplanebene

Die Integration von Lehrplanstandards (Kernlehrplan NRW, UK National Curriculum, US NGSS/CCSS) in das Wissensgraphen-Rahmenwerk offenbart einen systematischen Befund: **Die Übereinstimmung zwischen Lehrbuch und Lehrplan variiert dramatisch zwischen den Bildungssystemen**:

| System | Coverage-Score | Muster |
|--------|:-------------:|--------|
| China (CN) | 95,4 % | Nahezu perfekte Ausrichtung (zentraler Lehrplan) |
| England (UK) | 37,3 % | Mäßig; am höchsten in der Sekundarstufe II |
| Vereinigte Staaten (US) | 17,2 % | Niedrig (breite Richtlinien, lokale Variation) |
| NRW Deutschland | 12,7 % | Niedrigste (detaillierte, studiengangspezifische Vorgaben) |

Der Coverage-Score misst die **Lehrplan-→Lehrbuch-**Übereinstimmung: Findet sich zu jedem Lehrplankonzept ein entsprechendes Konzept im Lehrbuchgraph? Die dramatische Spanne — von 12,7 % (NRW) bis 95,4 % (CN) — spiegelt grundlegende Unterschiede in der Bildungsgovernance wider: Zentrale Systeme erzeugen enge Ausrichtung; föderale Systeme mit studiengangspezifischen Vorgaben erzeugen von Natur aus niedrigere messbare Übereinstimmung.

### 4.6 Warum erzeugen Bildungssysteme unterschiedliche Wissensstrukturen?

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

### 4.7 Extraktionszuverlässigkeit und Fehleranalyse

Ein potenzielles Bedenken bei jeder LLM-basierten Analyse ist, ob Messfehler die berichteten Ergebnisse verursachen könnten. Unsere Extraktionsvalidierung anhand von 92 Goldstandard-Annotationen (ZH F1=0,974, DE F1=0,949, EN F1=0,882) deutet darauf hin, dass die Extraktionsqualität des früheren primären Extraktionsmodells (qwen-plus) insgesamt hoch ist. Die Fehleranalyse zeigt, dass 29 % der Extraktionsfehler bei sehr kurzen Antworten (1–2 Wörter) auftreten, bei denen eine leere Extraktion tatsächlich angemessen ist. Bei den verbleibenden Fehlern handelt es sich überwiegend um partielle Auslassungen — 1–2 Konzepte aus einer Liste von 3–4 fehlen — und nicht um systematische Fehlleitungen.

**Hinweis zur N=15-Erweiterung**: Die erweiterte Humanvalidierung (§4) wurde mit `deepseek-v4-flash` (opencode GO) extrahiert; eine erneute F1-Validierung gegen die Goldstandards steht aus. Der 19-Modell-Benchmark (§4.9) zeigt jedoch, dass Konzeptextraktionsqualität über Modellfamilien hinweg eine Eigenschaft der Aufgabe ist (F1-Bereich 0,55–0,67), sodass eine modellinduzierte Skalenverschiebung der LDS-C zwar möglich, eine systematische Verzerrung der Null-Relation (beobachtet ≈ Split-Half) aber unwahrscheinlich ist.

Diese Fehlerverteilung bedeutet, dass die strukturellen Metriken (CDS, HDS, LDS, Coverage-Score) robust gegenüber Extraktionsrauschen sind: Partielle Auslassungen reduzieren die Konzeptanzahlen leicht, verzerren jedoch nicht systematisch die Graphentopologie oder die sprachübergreifenden Vergleiche. Wir halten es daher für unwahrscheinlich, dass die berichteten Befunde Artefakte der Extraktionsmethodik sind.

### 4.8 Robustheitsprüfung: Rechnerische Basislinie — methodisch revidiert

Zur Kontrolle, ob die beobachteten LDS-Werte echte strukturelle Unterschiede und nicht zufällige Konzeptvariation widerspiegeln, wurde ursprünglich eine **rechnerische Basislinie** aus 300 simulierten Antworten (20 pro Bedingung × 5 Themen × 3 Sprachen) berechnet. Die frühere Version dieser Analyse (N=8, qwen-plus-Extraktion) ergab einen scheinbaren Unterschied zwischen menschlichem LDS (0,727) und Simulation (0,647, p=0,05).

**Diese Vergleich ist mit der N=15-Erweiterung nicht mehr haltbar**, aus zwei Gründen:

1. **Skalenverschiebung**: Die neue, standardisierte Extraktion (deepseek-v4-flash) verschiebt LDS-C auf eine andere Skala (0,93–0,96); ein direkter Vergleich mit der alten Simulationsverteilung mischt zwei unterschiedliche Messverfahren.
2. **Null-Test-Ergebnis**: Die korrekte Kontrolle ist nicht der Vergleich zweier Absolutwerte, sondern die Lage der beobachteten LDS-C relativ zur Within-Language-Null (Split-Half 0,92–0,96; Label-Permutation 0,94). Beobachtete LDS-C liegt **auf** diesem Boden → vollständig durch Teilnehmervariabilität erklärbar.

Ein aussagekräftiger Mensch-vs-Simulation-Vergleich erfordert **dieselbe Extraktions-/Alignierungsmethode** für beide Bedingungen. Dies ist eine Aufgabe für zukünftige Arbeit (nicht mehr eine Stütze der ΔLDS > 0-Hypothese).

### 4.9 Robustheitsprüfung: Modellübergreifende Extraktionskonsistenz

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

### 4.10 Threats to Validity

Wir identifizieren sechs Hauptbedrohungen für die Validität der berichteten Ergebnisse.

**Abhängigkeit vom Extraktionsmodell**. Alle LDS-Berechnungen hängen von der Konzeptextraktion mittels qwen-plus ab. Während der 19-Modell-Benchmark die modellübergreifende Konsistenz bestätigt (F1-Bereich 0,55–0,67), könnte eine andere Extraktionsarchitektur systematisch andere Konzeptmengen erzeugen und möglicherweise die LDS-Werte verändern. Diese Bedrohung wird durch den engen F1-Bereich über verschiedene Modellfamilien hinweg teilweise abgemildert.

**Repräsentativität des Korpus**. Der Mathematik-Korpus (68 Lehrbücher) ist umfassend, jedoch verzerrt: Chinesische Lehrbücher stammen überwiegend von einem einzigen Verlag (Renjiao), deutsche Lehrbücher sind in Richtung universitärer Materialien verschoben und der englische Korpus ist auf IGCSE-/IB-Rahmenwerke beschränkt. Die sprachinterne Split-Half-Null (LDS≈0,97) quantifiziert diese Bedrohung.

**Übersetzungsasymmetrie bei der Konzeptausrichtung**. Die sprachübergreifende Konzeptausrichtung hängt von Expertenurteilen ab. Fehlausrichtungen erhöhen den LDS, indem sie zur Vereinigungsmenge beitragen, ohne die Schnittmenge zu erhöhen. Diese Bedrohung wird durch die Struktur der aligned_groups teilweise kontrolliert, aber die asymmetrische Abdeckung bleibt eine Quelle von Messfehlern.

**Auswahlverzerrung der Lehrpläne**. Lehrplandokumente variieren in ihrer Granularität (NRW: 299 Konzepte, UK: 397, US: 2.124, CN: 87). Höhere Granularität senkt mechanisch die Coverage-Scores. Unsere stufenweise Analyse kontrolliert dies teilweise.

**Begrenzte Stichprobengröße und Between-Subject-Design (Pilot-Menschendaten)**. Die ΔLDS-Analyse beruht auf N=15 Teilnehmenden (6 DE, 6 ZH, 3 EN) in einem Between-Subject-Design. Die Nullmodell-Suite zeigt, dass bei dieser Stichprobengröße die Teilnehmervariabilität die Sprachgruppe dominiert: sprachgetriebene Divergenz kann nicht von individueller Variabilität getrennt werden. Dies ist die zentrale methodologische Lehre — nicht ein temporärer Mangel, sondern eine Grenze des Designs selbst.

**Reichweite des Nullmodells**. Die grad-erhaltende Struktur-Null testet die Kantenanordnung über die Gradstruktur hinaus, jedoch nicht, ob die Gradstruktur selbst sprachbeeinflusst ist. Ein zukünftiges hierarchisches Nullmodell könnte diese Frage angehen.

### 4.11 LDS-Interpretationsrahmen

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

### 4.12 Einschränkungen

Mehrere Einschränkungen sollten anerkannt werden:

**Umfang der Daten**. Der Mathematik-Korpus (68 Lehrbücher, 574 Konzepte) ist umfassend. Der Physik-Korpus (366 Konzepte) und der Chemie-Korpus (220 Konzepte) ermöglichen eine disziplinübergreifende Validierung, bleiben aber kleiner. Die Lehrplangraphen decken zwar vier Systeme ab (NRW, UK, US, China), verwenden jedoch unterschiedliche Abgleichsmethoden, die die Vergleichbarkeit beeinträchtigen können.

**Extraktionsmethodik**. Während unsere Goldstandard-Validierung eine insgesamt hohe Qualität belegt (F1=0,939), wurden die sozialwissenschaftlichen Golddaten mittels halbautomatischen Schlüsselwortabgleichs mit anschließender manueller Überprüfung validiert. Im Goldstandard selbst könnten einige Fehler verbleiben.

**Stichprobengröße und Design der menschlichen Validierung**. Die erweiterte Humanstudie (N=15, 6 DE · 6 ZH · 3 EN) bestätigt die frühere Einschränkung und verschärft sie: Bei N=15 in einem **Between-Subject-Design** dominiert Teilnehmervariabilität die messbare LDS-C vollständig (Split-Half-Boden ≈ beobachtete LDS-C ≈ Label-Permutation). Dies ist kein Stichprobenfehler, sondern eine **strukturelle Grenze des Designs**: Da jede Person nur in einer Sprache antwortet, können sprachgetriebene Divergenz und individuelle Variabilität nicht getrennt werden. Die zentrale methodologische Lehre: Zukünftige Studien benötigen (a) ein Within-Subject-Design, (b) größere Stichproben pro Sprachgruppe (N≥30), oder (c) Metriken, die gegen individuelle Konzeptwahl robust sind. Die thematischen Richtungstendenzen (ZH rechtlich/moralisch, DE autonom/affektiv, EN sozial) bieten eine testbare Hypothese für ein Within-Subject-Design.

**Interpretation des Nullmodells**. Während die graderhaltende Struktur-Null zeigt, dass LDS-K von strukturellen Faktoren und nicht von der Sprache dominiert wird, bewahrt der Doppelkantentausch-Algorithmus die exakte Gradsequenz jedes Graphen. Dies ist eine konservative Null: Sie testet, ob sprachspezifische Kantenanordnungen über die Gradstruktur hinaus Informationen hinzufügen, testet jedoch nicht, ob die Gradstruktur selbst sprachbeeinflusst sein könnte. Ein zukünftiges hierarchisches Nullmodell könnte diese geschichtete Frage angehen.

**Kantenfreie Graphen in früheren menschlichen Daten**. Die frühere qwen-plus-Extraktion erzeugte eine rein konzeptbasierte Ausgabe (keine Relationen) für menschliche Antworten. In der N=15-Erweiterung wurde dies behoben: Eine Relationsextraktion (7 Typen, `scripts/lds_c_extract_relations.py`) lieferte 162 Kanten (DE 59, ZH 67, EN 36), sodass die vollständige v3-LDS-Formel (Node- + Edge-Jaccard) angewendet werden konnte. Das Ergebnis bestätigt die Konzeptebene: Edge-Jaccard ≈ 0 und Split-Half-Boden ≈ beobachtete v3-LDS — kein separierbares Sprachsignal. Die Kantenzahl pro Antwort bleibt jedoch spärlich, sodass Kantenaussagen auf Gruppenebene robust, auf individueller Ebene aber eingeschränkt interpretierbar sind.

**Kausalität**. Unsere Analyse ist korrelativ. Wir messen strukturelle Unterschiede zwischen Systemen, können diese jedoch nicht unabhängig voneinander auf Lehrplangestaltung, Lehrbuchtradition oder Bildungsphilosophie zurückführen.

**Generalisierbarkeit**. Mathematik, Physik und Chemie könnten strukturelle Eigenschaften teilen, die in geistes- oder sozialwissenschaftlichen Disziplinen nicht vorhanden sind. Die Erweiterung auf zusätzliche Domänen ist eine Priorität.

**LDS-Interpretation**. Der LDS-Interpretationsrahmen (Abschnitt 4.11) verankert numerische Werte an Nullmodell-Baselines, jedoch sind die Schwellenwerte (0,90, 0,50) deskriptiv statt inferenziell. Mit zunehmenden menschlichen Daten sollten Bootstrap-Konfidenzintervalle diese deskriptiven Schwellenwerte für Hypothesentests ersetzen.

### 4.13 Implikationen

Trotz dieser Einschränkungen haben die vorliegenden Ergebnisse Implikationen für drei Fachgemeinschaften:

**Für die Bildungsforschung**: Die CDS- und HDS-Metriken bieten quantitative Werkzeuge für die Lehrplananalyse, die bestehende qualitative Rahmenwerke (TIMSS, PISA) ergänzen. Eine Lehrplangestalterin könnte CDS verwenden, um Dichteengpässe zu identifizieren, und HDS, um übermäßig lange Voraussetzungsketten zu erkennen.

**Für KI in der Bildung**: Die automatisierte Pipeline zeigt, dass die groß angelegte, sprachübergreifende Konstruktion von Wissensgraphen aus Lehrbüchern mit aktuellen LLMs machbar ist. Dies eröffnet die Möglichkeit einer Lehrplanebenen-Wissensanalyse in einem Umfang, den die manuelle Inhaltsanalyse nicht erreichen kann.

**Für die Erforschung des linguistischen Relativitätsprinzips**: Unsere Daten stützen keine einheitliche „Sprache formt Wissen“-Behauptung. Stattdessen zeigen sie, dass sprachübergreifende strukturelle Beziehungen heterogen sind — einige Sprachpaare konvergieren erheblich (ZH-DE), während andere auf Rauschniveau liegen (ZH-EN, DE-EN). Die erweiterte Humanvalidierung (N=15) erlaubt nun eine präzisere Antwort: Auf der Ebene menschlicher Konzeptäußerungen ist bei dieser Stichprobe **kein separierbares Sprachsignal** nachweisbar — LDS-C liegt auf dem Split-Half-Boden und ist von Label-Permutation ununterscheidbar. Dies falsifiziert die einfache Hypothese „Sprache → unterschiedliche Konzeptgraphen" und präzisiert zugleich, unter welchen Bedingungen ein Sprachsignal nachweisbar wäre (Within-Subject-Design, N≥30, strukturrobuste Metriken). Das LinguaGraph-Rahmenwerk stellt die Werkzeuge bereit, um diese Heterogenität zu messen; die Richtungstendenzen (ZH rechtlich/moralisch, DE autonom/affektiv, EN sozial) bleiben als testbare Hypothesen für zukünftige Studien erhalten.
