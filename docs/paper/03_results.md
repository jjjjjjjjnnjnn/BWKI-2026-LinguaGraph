# LinguaGraph — Results: CognitiveSpace Knowledge Graph

> **Language**: German
> **Status**: Draft v2 — §4 (Humanvalidierung) überarbeitet auf N=15 (ersetzt N=8; siehe `03_results_human_v2.md`)

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

> Dieser Abschnitt präsentiert LDS-C Ergebnisse auf Basis der **erweiterten, QC-geprüften Stichprobe (N=15: 6 DE · 6 ZH · 3 EN)**, extrahiert mit `deepseek-v4-flash` (opencode GO). Alle Ergebnisse sind reproduzierbar (Skripte `scripts/lds_c_extract.py`, `lds_c_compute.py`, `lds_c_thematic.py`).

### 4.1 Versuchsdesign und Datengrundlage

| Dimension | Spezifikation |
|-----------|---------------|
| Teilnehmer | N=15 (6 DE, 6 ZH, 3 EN bilingual-ZH) |
| Stimuli | 5 soziale Themen (Freiheit, Gerechtigkeit, Verantwortung, Heimat, Erfolg) |
| Datenquelle | Freeze-SSOT `freeze_survey_20260703` + `freeze_survey_20260712` (QC-geprüft, 4/4 in zweitem Batch) |
| Extraktionsmodell | deepseek-v4-flash (opencode GO), Temperatur 0.3 |
| Extrahierte Antworten | 15/15 (100 %), pro Antwort 5–6 Konzepte je Thema mit engl. Gloss |
| Konzept-Alignierung | Englischer Gloss → kanonischer Schlüssel (Synonym-Karte + Stemmer) |

### 4.2 Konzeptebene LDS-C (zwischen den Sprachgruppen)

Aggregierte Konzeptmengen pro Sprachgruppe, LDS = 1 − Jaccard(kanonische Schlüssel).

| Sprachpaar | LDS-C (gepoolt) | 95 %-CI (Bootstrap) | LDS-K (Konzept) | ΔLDS |
|:----------:|:---------------:|:-------------------:|:---------------:|:----:|
| ZH-EN | 0.961 | [0.936, 0.985] | 0.977 | −0.016 |
| DE-EN | 0.933 | [0.899, 0.986] | 0.977 | −0.044 |
| ZH-DE | 0.934 | [0.908, 0.960] | 0.887 | +0.047 |

**Wichtig**: Alle drei Sprachpaare zeigen LDS-C ≈ 0.93–0.96. Die Werte liegen **nahe der Zufallsverteilung** (siehe 4.3) und deutlich höher als die früheren N=8-Schätzungen (0.70–0.75), die mit einer älteren Pipeline berechnet wurden.

### 4.3 Null-Modell-Prüfung: Kein separierbares Sprachsignal

Zwei Null-Modelle testen, ob die beobachtete LDS-C auf Sprache zurückgeht oder auf Teilnehmervariabilität:

| Sprachpaar | LDS-C (beobachtet) | Within-Lang Split-Half (Boden) | Label-Permutation |
|:----------:|:------------------:|:------------------------------:|:-----------------:|
| ZH-EN | 0.961 | 0.958 | 0.940 |
| DE-EN | 0.933 | 0.923 | 0.938 |
| ZH-DE | 0.934 | 0.922 | 0.935 |

**Zentraler Befund**:
1. **Within-Language-Split-Half** (Teilnehmervariabilität innerhalb einer Sprache): 0.92–0.96 ≈ beobachtete LDS-C. Die Variabilität **innerhalb** einer Sprachgruppe ist genauso groß wie die Divergenz **zwischen** den Gruppen.
2. **Label-Permutation** (Permutation der Sprachlabels): 0.94–0.94 ≈ beobachtete LDS-C. Das Vertauschen der Sprachzugehörigkeit ändert die LDS-C nicht — **die Sprachlabels tragen kein messbares Signal**.

**Interpretation**: Auf Konzeptebene ist die LDS-C von Teilnehmervariabilität dominiert. Das Between-Subject-Design (jede Person antwortet nur in einer Sprache) vermischt sprachgetriebene Divergenz mit individueller Variabilität. Bei N=15 (6/6/3) dominiert die letztere. **Die Hypothese ΔLDS > 0 wird auf Konzeptebene nicht bestätigt.**

### 4.4 Thematische Analyse (6-Kategorien-Codebook)

Eine grobkörnige Codierung (Codebook v1: Legal/Institutional, Individual/Autonomy, Material/Concrete, Social/Relational, Moral/Abstract, Emotional/Affective; LLM-Klassifikation, n=335 Konzepte) vergleicht die Verteilungen der Themenkategorien:

| Kategorie | DE | EN | ZH |
|-----------|:--:|:--:|:--:|
| Legal/Institutional | 0.05 | 0.10 | **0.12** |
| Individual/Autonomy | **0.27** | 0.21 | 0.25 |
| Material/Concrete | 0.11 | 0.12 | 0.09 |
| Social/Relational | 0.15 | **0.21** | 0.15 |
| Moral/Abstract | 0.17 | 0.15 | **0.24** |
| Emotional/Affective | **0.14** | 0.10 | 0.11 |

| Test | Ergebnis |
|------|----------|
| Chi-Quadrat | χ²=9.14, p=0.519 (n.s.), Cramér's V=0.117 |
| Permutationstest | p=0.354 (5000 Iterationen) |
| Shannon-Entropie | DE 2.68 · EN 2.74 · ZH 2.64 |

**Befund**: Die Kategorienverteilungen unterscheiden sich **nicht signifikant** zwischen den Sprachen. Es zeigen sich jedoch **konsistente Richtungstendenzen**, die mit einer kulturellen Rahmungshypothese übereinstimmen: ZH rahmt Freiheit häufiger rechtlich-institutionell (Freiheit: 0.24 vs. DE 0.09 / EN 0.07), ZH stärker moralisch-abstrakt (0.24), DE stärker individuell-autonom (0.27) und affektiv (0.14). Diese Tendenzen sind bei N=15 nicht statistisch bestätigbar.

### 4.5 Relationale Ebene (v3-Knoten+Kante)

Zusätzlich zur Konzeptebene wurden explizite Relationen zwischen den extrahierten Konzepten erfasst (7 Relationstypen, pro Thema). Insgesamt 162 Kanten (DE 59, ZH 67, EN 36). Die v3-LDS kombiniert Knoten- und Kanten-Jaccard (frozen Formel):

| Sprachpaar | LDS v3 | 95 %-CI | Node-Jaccard | Edge-Jaccard | LDS-K (v3) | ΔLDS | Split-Half-Boden |
|:----------:|:------:|:-------:|:------------:|:------------:|:----------:|:----:|:----------------:|
| ZH-EN | 0.977 | [0.962, 0.992] | 0.037 | 0.010 | 0.934 | +0.043 | 0.979 |
| DE-EN | 0.966 | [0.949, 0.993] | 0.068 | **0.000** | 0.938 | +0.028 | 0.959 |
| ZH-DE | 0.964 | [0.948, 0.980] | 0.064 | 0.008 | 0.519 | +0.445 | 0.958 |

**Zentraler Befund**: Die Kantenstrukturen überlappen sprachübergreifend kaum (Edge-Jaccard ≈ 0, DE-EN exakt 0.000). Der Split-Half-Boden (0.958–0.979) entspricht der beobachteten v3-LDS (0.964–0.977) — auch auf relationaler Ebene ist die Divergenz vollständig durch Teilnehmervariabilität erklärbar. Der scheinbar große ΔLDS-Wert für ZH-DE (+0.445) ist ein Artefakt des Vergleichs zwischen spärlichen Menschengraphen und dichten, strukturell konvergenten Lehrbuchgraphen — nicht ein Beleg für sprachgetriebene Divergenz (der Split-Half-Boden von 0.958 für ZH-DE widerlegt dies).

**Fazit relationale Ebene**: Die relationale Struktur bestätigt die Konzept- und Themenebene. Unter Between-Subject-Bedingungen (N=15) ist kein separierbares Sprachsignal nachweisbar — weder auf Knoten-, Kanten-, noch Kategorienebene.

### 4.6 Zusammenfassung und methodologische Reflexion

Die erweiterte Humanvalidierung (N=15) liefert über **drei Analyseebenen** hinweg ein konsistentes, ehrliches negatives Ergebnis:

1. **Konzeptebene**: LDS-C 0.93–0.96, nicht von Teilnehmervariabilität unterscheidbar (Split-Half-Boden 0.92–0.96; Label-Permutation 0.94).

2. **Themenebene**: Kategorienverteilungen nicht signifikant verschieden (χ² p=0.52, Permutation p=0.35), aber konsistente Richtungstendenzen (ZH rechtlich/moralisch, DE autonom/affektiv, EN sozial).

3. **Relationale Ebene (v3)**: LDS-C 0.96–0.98, Edge-Jaccard ≈ 0, Split-Half-Boden ≈ beobachtet → ebenfalls kein separierbares Sprachsignal.

4. **Die früheren N=8-Befunde (LDS-C 0.70–0.75, ΔLDS>0) werden nicht repliziert**: Sie stammen aus einer älteren Pipeline und sind mit dem erweiterten, QC-geprüften Datensatz und der standardisierten Extraktion nicht vereinbar.

5. **Methodologische Lehre (Kernbeitrag dieser Revision)**: Ein Between-Subject-Design kann sprachgetriebene Divergenz nicht von individueller Variabilität trennen, wenn die Stichprobe klein ist. Dies gilt unabhängig von der Analyseebene (Konzept, Kategorie, Relation). Zukünftige Studien benötigen (a) ein Within-Subject-Design, (b) größere Stichproben pro Sprachgruppe, oder (c) Metriken, die gegen individuelle Konzeptwahl robust sind.

**Dieser negative Befund ist wissenschaftlich wertvoll**: Er falsifiziert die einfache Hypothese "Sprache → unterschiedliche Konzeptgraphen" auf allen drei Ebenen und präzisiert die Bedingungen, unter denen sprachliche Kognitionseffekte nachweisbar wären.

---

## 5. LLM-as-Subject: Sprachsignal im Within-Subject-Design

> Der negative Humanbefund (§4) wirft die entscheidende methodologische Frage auf: Ist die fehlende Trennbarkeit ein Artefakt des Between-Subject-Designs (Teilnehmervariabilität überlagert die Sprache) oder ein echtes Nichtvorhandensein sprachlicher Kognitionseffekte? Um diese zu beantworten, wurde ein **kontrolliertes Within-Subject-Experiment** mit einem Large Language Model als standardisiertem kognitivem Subjekt durchgeführt: **dasselbe Modell** (deepseek-v4-flash, opencode GO) antwortet in ZH/DE/EN auf dieselben 5 Themen. Da die Gewichte identisch sind, ist die Sprache die einzige Variation — das Within-Subject-Design gilt konstruktionsbedingt. Reproduzierbar via `scripts/lds_c_llm_subject.py`, `lds_c_llm_analyze.py`, `lds_c_llm_per_topic.py`, `lds_c_llm_lmm.py`.

### 5.1 Versuchsdesign

| Dimension | Spezifikation |
|-----------|---------------|
| Subjekt | deepseek-v4-flash (opencode GO), Temperatur 0.3, k=10 unabhängige Sessions pro Bedingung |
| Stimuli | 5 soziale Themen (Freiheit, Gerechtigkeit, Verantwortung, Heimat, Erfolg) |
| Sonden | P1 Sprach-Haupteffekt · P2 Rahmen-Code-Entkopplung · P3 Freie Assoziation · P5 Antwort- vs. Promptsprache |
| Hygiene | jede Session unabhängig (keine Kontextakkumulation), themenweise Beantwortung, konterbalancierte Reihenfolge |
| Umfang | 220 Einheiten / ~570 API-Aufrufe, 0 leere Extraktionen |

### 5.2 Sprach-Haupteffekt (P1): Signal ist nachweisbar

| Sprachpaar | LDS-C (gepoolt) | 95 %-CI | Split-Half-Boden | Label-Permutation |
|:----------:|:---------------:|:-------:|:----------------:|:-----------------:|
| ZH-EN | **0.955** | [0.935, 0.966] | 0.875 | 0.879 |
| DE-EN | **0.930** | [0.912, 0.955] | 0.846 | 0.880 |
| ZH-DE | **0.945** | [0.932, 0.961] | 0.862 | 0.879 |

**Zentraler Befund**: Die beobachtete LDS-C übersteigt den Split-Half-Boden um **+0.08 bis +0.09** und die Label-Permutation um **+0.05 bis +0.08**. Anders als bei den menschlichen Daten (N=15, Between-Subject: LDS-C ≈ Boden ≈ Permutation) trägt das Sprachlabel hier **messbares Signal**.

> **Dies ist der zentrale Kontrast der Arbeit**: Derselbe Messrahmen (LDS-C + Nullmodelle), nur das Design von Between-Subject (Menschen) auf Within-Subject (LLM) umgestellt, verwandelt ein nicht-trennbares Signal in ein trennbares. Der menschliche Negativebefund ist damit als **Design-Artefakt** charakterisiert — nicht als Beleg für das Fehlen sprachlicher Kognitionseffekte.

### 5.3 Rahmen-Code-Entkopplung (P2): Rahmen wirkt innerhalb, nicht über Codes

| Code | Bedingung | LDS | 95 %-CI |
|:----:|:----------:|:---:|:-------:|
| ZH | ZH-natürlich vs. ZH-Code+DE-Rahmen | 0.916 | [0.905, 0.943] |
| DE | DE-natürlich vs. DE-Code+ZH-Rahmen | 0.914 | [0.901, 0.937] |

Die reine Rahmenmanipulation (gleicher Code, anderer kultureller Rahmen) erzeugt LDS ≈ 0.91–0.92 — oberhalb des Split-Half-Bodens. **Die Rahmeninstruktion verändert also die Konzeptwahl innerhalb eines Codes.** Der scheinbare Vergleich mit der sprachübergreifenden LDS-C (0.93–0.96) ist jedoch **nicht äquivalent**: Er vergleicht innerhalb desselben Code-Orbits, nicht zwischen Orbits (siehe LMM, §5.6).

### 5.4 Freie Assoziation (P3): statistische Basis der Konzeptdivergenz

| Sprachpaar | Assoziations-LDS | Konzept-LDS (P1) | Δ |
|:----------:|:----------------:|:----------------:|:---:|
| ZH-EN | 0.933 | 0.955 | −0.022 |
| DE-EN | 0.920 | 0.930 | −0.011 |
| ZH-DE | **0.736** | 0.945 | **−0.209** |

Die freien Assoziationen desselben Modells (englisch glossiert in denselben kanonischen Schlüsselraum) erklären die Konzeptdivergenz für **EN-Paare nahezu vollständig** (Δ≈−0.01 bis −0.02) — die Konzeptdivergenz ist hier ein statistisches Nebenprodukt der Assoziationsverteilung. Für **ZH-DE** dagegen liegt die Assoziationsdivergenz (0.736) weit unter der Konzeptdivergenz (0.945): **Es existiert eine strukturelle Ebene jenseits der Assoziationsstatistik** — konsistent mit der Rahmen-Wirkung auf das kulturell entfernteste Paar.

### 5.5 Antwort- vs. Promptsprache (P5): Promptsprache ohne eigenen Effekt

| Kontrast | LDS | 95 %-CI | Innerhalb-Bedingung-Boden |
|:--------:|:---:|:-------:|:-------------------------:|
| DE-Frage/DE-Antwort vs. ZH-Frage/DE-Antwort | 0.815 | [0.800, 0.884] | 0.827 / 0.843 |

Bei fixierter Antwortsprache (DE) erzeugt die Variation der Fragesprache (DE vs. ZH) **keine über dem Boden liegende** Divergenz. Die Frage-/Promptsprache trägt kein eigenständiges Signal — die Antwortsprache (Produktionssprache) dominiert.

### 5.6 LMM: Sprachcode ist der dominante Organisator (Mechanismus-Kern)

Um die marginalen Beiträge von Sprachcode und kulturellem Rahmen zu trennen, wurde ein gemischtes Modell über 50 dyadische Zellpaare (5 Zellen × 5 Themen, Response = Jaccard-Similarität) geschätzt:

`Similarität ~ same_lang + same_frame + (1|topic)`

| Effekt | Koeffizient (Jaccard) | SE | t | p | Permutation p |
|:------:|:---------------------:|:--:|:--:|:---:|:-------------:|
| Intercept | +0.050 | 0.011 | 4.60 | <0.001 | — |
| **same_lang** | **+0.038** | 0.009 | 4.28 | **<0.001** | **0.000** |
| **same_frame** | **+0.001** | 0.009 | 0.13 | **0.90** | **0.779** |

**Marginalbeitrag**: Das Teilen des Sprachcodes erhöht die Konzeptähnlichkeit signifikant (+0.038); das Teilen des kulturellen Rahmens hat **keinen** signifikanten marginalen Beitrag (+0.001). Die Permutationsprüfung (blockweise, 1000 Iterationen) bestätigt die Robustheit.

**Harmonisierung mit P2 (Zwei-Boden-Konzept)**:
- Boden 1 = Split-Half innerhalb einer Bedingung: J≈0.12 (gleicher Code + Rahmen)
- Boden 2 = vollständig verschiedene Zellen: J≈0.05 (verschiedener Code + Rahmen)
- Rahmenwechsel (gleicher Code): J≈0.088 → **zwischen den Böden**: bewegt Konzepte innerhalb des Code-Orbits (0.12→0.088), erreicht aber keine codeübergreifende Divergenz (0.088 ≫ 0.05).

**→ Der Sprachcode ist die dominante Organisationsebene (lexikalisch-statistisch); der kulturelle Rahmen ist ein sekundärer, code-interner Modulator.**

### 5.7 Themenbezogene Decomposition

| Thema | Ø Sprachsignal (P1−Boden) | Ø Rahmen-Effekt (P2) |
|:------|:---:|:---:|
| Freiheit | 0.045 | 0.89 |
| Gerechtigkeit | **0.114** | **0.96** |
| Verantwortung | 0.058 | 0.87 |
| Heimat | 0.082 | 0.86 |
| Erfolg | **0.115** | **0.98** |

Das Sprachsignal und der Rahmen-Effekt sind bei **abstrakten, moralisch konnotierten Themen (Erfolg, Gerechtigkeit) am stärksten** — konsistent mit der Hypothese, dass abstrakte Konzepte sprach- und kulturabhängiger sind als konkrete.

### 5.8 Zusammenfassung und Einordnung

1. **Sprachsignal existiert** im Within-Subject-Design (P1: LDS-C ≫ Boden) — der menschliche Negativebefund ist ein Between-Subject-Artefakt.
2. **Dominanter Mechanismus**: Sprachcode (M2, lexikalisch-assoziativ) — signifikanter marginaler Beitrag im LMM.
3. **Sekundärer Mechanismus**: kultureller Rahmen (M3) — wirkt innerhalb des Codes, überbrückt Codes nicht.
4. **ZH-DE trägt eine strukturelle Ebene** jenseits der Assoziationsstatistik (P3: Δ=−0.209) — am stärksten beim kulturell entferntesten Paar.
5. **Promptsprache (M5) ist ohne eigenen Effekt** (P5 falsifiziert).

Die Ergebnisse validieren die zentrale Methodenlehre aus §4.6: **ein Within-Subject-Design ist erforderlich, um sprachgetriebene Divergenz zu trennen** — und bieten zugleich eine testbare Blaupause für zukünftige Humanstudien mit Within-Subject-Design.
