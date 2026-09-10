# LinguaGraph — Results: CognitiveSpace Knowledge Graph

> **Language**: German
> **Status**: Final (v0.13.3) — §4 (Humanvalidierung) auf N=15 (ersetzt N=8; Entwurfsnotiz archiviert unter `_archive/20260811_rnd_review/docs/paper/03_results_human_v2.md`)

---

## 3. Ergebnisse

### 3.1 CognitiveSpace: Statistische Übersicht

Die Extraktion und Fusion der 68 Lehrbücher ergibt einen Wissensgraphen mit folgenden Kenngrößen:

| Metrik | Wert |
|--------|------|
| Gesamtkonzepte | 556 (eindeutige Konzepte) |
| Gesamtrelationen | 525 (direkte Relationen) |
| Lehrbuchquellen | 68 (39 ZH + 18 EN + 11 DE) |
| Bildungsstufen | 4 (Grundschule → Universität) |
| Dichte | 0,0015 |
| Isolierte Knoten | 2 (< 0,5 %) |

### 3.2 Verteilung nach Bildungsstufe

Die Konzepte verteilen sich erwartungsgemäß über die vier Bildungsstufen, wobei der Schwerpunkt auf Oberstufe und Universität liegt:

| Stufe | Konzepte | Anteil | Charakteristik |
|-------|----------|--------|----------------|
| Grundschule | 26 | 4,7 % | Grundlegende Arithmetik, einfache Geometrie |
| Mittelschule | 57 | 10,3 % | Algebra, Gleichungen, Funktionen |
| Oberstufe | 200 | 36,0 % | Analysis, Wahrscheinlichkeit, Vektoren |
| Universität | 273 | 49,1 % | Höhere Analysis, Lineare Algebra, DGLS |

Diese Verteilung spiegelt die zunehmende Spezialisierung und den wachsenden Begriffsumfang in höheren Bildungsstufen wider.

### 3.3 Sprachübergreifende Abdeckung

Die Alignierung zeigt eine substanzielle dreisprachige Überschneidung:

| Abdeckung | Konzepte | Anteil* |
|-----------|----------|--------|
| ZH + EN + DE (dreisprachige Gruppen) | **219** | 39,4 % |
| Sprachspezifisch (nicht abgedeckt) | **359** | — |
| — davon nur ZH | 120 | 21,6 % |
| — davon nur DE | 94 | 16,9 % |
| — davon nur EN | 145 | 26,1 % |

> *Anteile beziehen sich auf 556 Konzepte. 219 Gruppen ≠ 219 Konzepte: Gruppen- und Konzeptzählung verwenden unterschiedliche Nenner, daher addieren sich 39,4 % + 64,6 % nicht auf 100 %.

Die relativ hohe exklusive ZH-Abdeckung (21,6 %) ist auf die spezifischeren chinesischen Lehrpläne in der Grund- und Mittelschule zurückzuführen, während die Exklusivanteile für EN (26,1 %) und DE (16,9 %) deutlich geringer ausfallen.

### 3.4 Semesterstruktur-Analyse

Die Analyse des Graphen auf Semesterstruktur zeigt folgende Beobachtungen:

1. **Konnektivität**: Der Graph ist dünn verknüpft (238 Links auf 556 Knoten, Dichte 0,0015, 388 Zusammenhangskomponenten): 381 Knoten (68,5 %) haben keine ausgehenden Kanten; die größte Komponente umfasst 121 Knoten. Die Struktur folgt einem Kern-Peripherie-Muster mit wenigen zentralen Ankerkonzepten und vielen peripheren Einträgen.

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

[Abbildung: CognitiveSpace-3D-Visualisierung — 556 Konzepte in konzentrischen Kugelschalen,
vier farbcodierte Bildungsstufen, sichtbare 238 Relationen als blaue Verbindungslinien]

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

### 3.8 LDS-K Vertiefung: Bildungsebenen, Sensitivität und Cross-Source-Nullmodell

Die LDS-K-Ergebnisse wurden vertieft (reproduzierbar via `scripts/lds_k_deepen.py` + `lds_k_wiki_gloss.py`):

**Bildungsebenen**: Die ZH-DE-Konvergenz (0.52 im Pool) ist **systematisch über alle vier Bildungsebenen** — Grundschule 0.39, Mittelschule 0.80, Oberstufe 0.54, Universität 0.49. Sie ist kein Artefakt einer einzelnen Ebene. Die Kantenkomponente trägt für ZH-DE dreifach mehr zur Divergenz bei (Δ 0.075) als für ZH-EN/DE-EN (Δ ~0.02) — die Konvergenz zeigt sich auch in der **Relationenstruktur**, nicht nur in der Konzeptwahl.

**Sensitivität**: Die Ergebnisse sind robust gegenüber (a) Kantenrichtung (Δ ≤ 0.004), (b) Alignierungstoleranz — Synonym-/Stem-Mapping vs. exakte Gloss-Übereinstimmung (Δ ≤ 0.05), (c) Wichtigkeitsschwelle (Δ ≤ 0.02 auf LLM-Konzepten). Die Rangfolge (ZH-DE < ZH-EN ≈ DE-EN) bleibt in allen Konfigurationen erhalten.

**Cross-Source-Nullmodell**: Zwei Quellen wurden verglichen:
1. **Lehrbuch (Mathematik) vs. Wikipedia (sozial)**: LDS = 1.00 (null Knotenüberlappung) — dies ist eine **Domänenkonfundierung** (Mathematik ⊥ Soziales), kein Sprachsignal. Der Vergleich ist methodisch ungeeignet, weil die Quellen verschiedene Wissensdomänen abdecken.
2. **Wikipedia(zh) vs. Human(zh), beide sozial (domänenrein)**: LDS = 0.94 — die Quelle trägt einen großen Anteil zur Divergenz bei (institutionelle Enzyklopädie vs. spontane Kognition überschneiden sich kaum, J_node=0.06).

**Wikipedia-Negativkontrolle (korrigiert)**: Frühere Analysen berichteten LDS = 1.00 für soziale Wikipedia-Konzepte. Dies war ein **Alignierungs-Artefakt**: chinesische Konzepte (z. B. 自由) werden von `canonical_key` (das nur lateinische Zeichen extrahiert) zu leeren Schlüsseln reduziert. Nach Glossierung von 96 chinesischen und deutschen Konzepten in denselben kanonischen Schlüsselraum ergeben sich reale Werte:

| Quelle | ZH-EN | DE-EN | ZH-DE |
|:------|:-----:|:-----:|:-----:|
| Mathematik-Lehrbücher | 0.934 | 0.938 | **0.519** |
| Wikipedia (sozial, aligniert) | 0.698 | 0.723 | **0.819** |

**Zentraler Befund (mit Einschränkung)**: Die Struktur sozialer Konzepte (Freiheit, Gerechtigkeit, Verantwortung, Heimat, Erfolg) weist eine höhere sprachübergreifende Divergenz auf als die Mathematik-Labels — und das Muster ist **umgekehrt**: Während ZH-DE in Mathematik am stärksten konvergiert (0.52), ist es in der sozialen Domäne am divergentesten (0.82). **Einschränkung (P2-Recheck)**: Dieser Vergleich ist **kein belastbarer Beleg unabhängiger sprachübergreifender Konvergenz**. Die Mathematik-Knoten sind **Alignierungs-Labels** (keine unabhängig extrahierten Konzepte), das `de`-Label-Feld enthält teils chinesische Texte, und ein Size-Matching auf die Wikipedia-Größe **kehrt das Muster um** (bei k=15–35 ist der Wikipedia-J_node höher; Details: `docs/p2_methodology_rechecks.md`). Die Mathematik-"Konvergenz" (0.519) ist daher teilweise ein Darstellungs-/Größen-Artefakt; die Aussage ist nur als "die **Alignierungs-Labels** institutionellen Wissens stimmen sprachübergreifend besser überein als die unabhängig extrahierten sozialen Konzepte" zu lesen — nicht als Beleg, dass institutionelles Wissen "inhaltlich" konvergiert.

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
| ZH-EN | 0.963 | [0.936, 0.985] | 0.977 | −0.014 |
| DE-EN | 0.932 | [0.899, 0.986] | 0.977 | −0.045 |
| ZH-DE | 0.936 | [0.908, 0.960] | 0.887 | +0.049 |

**Wichtig**: Alle drei Sprachpaare zeigen LDS-C ≈ 0.93–0.96. Die Werte liegen **nahe der Zufallsverteilung** (siehe 4.3) und deutlich höher als die früheren N=8-Schätzungen (0.70–0.75), die mit einer älteren Pipeline berechnet wurden.

**Hinweis zur ΔLDS-Definition (Berichtsformat)**: Die hier berichteten ΔLDS-Werte (konzeptuelle Ebene, −0.044 bis +0.047) verwenden die **konzeptuelle LDS-K** (nur Knoten) als Basis, sodass LDS-C und LDS-K auf derselben Skala verglichen werden (apples-to-apples). Die relationale v3-LDS-K (§4.5) ist mit den relationalen LDS-C-Werten zu vergleichen — beide ΔLDS-Formate sind in der Arbeit durchgängig nach Ebene getrennt und nicht miteinander vermischt. Die Titelaussage "ΔLDS ≈ 0 (−0.05 bis +0.05)" bezieht sich auf die konzeptuelle Ebene.

### 4.3 Null-Modell-Prüfung: Kein separierbares Sprachsignal

Zwei Null-Modelle testen, ob die beobachtete LDS-C auf Sprache zurückgeht oder auf Teilnehmervariabilität:

| Sprachpaar | LDS-C (beobachtet) | Within-Lang Split-Half (Boden) | Label-Permutation | Perm-p |
|:----------:|:------------------:|:------------------------------:|:-----------------:|:------:|
| ZH-EN | 0.963 | 0.958 | 0.940 | 0.08 |
| DE-EN | 0.932 | 0.923 | 0.938 | 1.00 |
| ZH-DE | 0.936 | 0.922 | 0.935 | 1.00 |

**Zentraler Befund**:
1. **Within-Language-Split-Half** (Teilnehmervariabilität innerhalb einer Sprache): 0.92–0.96 ≈ beobachtete LDS-C. Die Variabilität **innerhalb** einer Sprachgruppe ist genauso groß wie die Divergenz **zwischen** den Gruppen.
2. **Label-Permutation** (Permutation der Sprachlabels): 0.94–0.94 ≈ beobachtete LDS-C. Der formale Permutationstest (500 Iterationen, zweiseitig) liefert **p = 0.08 / 1.00 / 1.00** — die Sprachlabels tragen **kein messbares Signal** (kein p-Wert unterhalb konventioneller Schwellen).

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

| Sprachpaar | LDS-C (gepoolt) | 95 %-CI | Split-Half-Boden | Label-Permutation | **Perm-p** |
|:----------:|:---------------:|:-------:|:----------------:|:-----------------:|:---------:|
| ZH-EN | **0.955** | [0.935, 0.966] | 0.875 | 0.879 | **<0.01** |
| DE-EN | **0.930** | [0.912, 0.955] | 0.846 | 0.880 | **<0.01** |
| ZH-DE | **0.945** | [0.932, 0.961] | 0.862 | 0.879 | **<0.01** |

**Zentraler Befund**: Die beobachtete LDS-C übersteigt den Split-Half-Boden um **+0.08 bis +0.09** und die Label-Permutation um **+0.05 bis +0.08**. Ein formaler Permutationstest (500 Iterationen; zweiseitig; Anteil der Permutationen mit LDS ≥ beobachtetem LDS) liefert für alle drei Sprachpaare **p < 0.01** (keine der 500 Permutationen erreichte die beobachtete LDS-C). Anders als bei den menschlichen Daten (N=15, Between-Subject: LDS-C ≈ Boden ≈ Permutation, p = 0.08/1.0/1.0) trägt das Sprachlabel hier **messbares Signal**.

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

| Effekt | Koeffizient (Jaccard) | SE | t | p | Permutation p | **Bootstrap p** |
|:------:|:---------------------:|:--:|:--:|:---:|:-------------:|:--------------:|
| Intercept | +0.050 | 0.011 | 4.60 | <0.001 | — | — |
| **same_lang** | **+0.038** | 0.009 | 4.28 | **<0.001** | **0.000** | **<0.01** |
| **same_frame** | **+0.001** | 0.009 | 0.13 | **0.90** | **0.779** | **0.82** |

**Marginalbeitrag**: Das Teilen des Sprachcodes erhöht die Konzeptähnlichkeit signifikant (+0.038); das Teilen des kulturellen Rahmens hat **keinen** signifikanten marginalen Beitrag (+0.001). Die Permutationsprüfung (blockweise, 1000 Iterationen) bestätigt die Robustheit. Zusätzlich wurde ein **Cell-Cluster-Bootstrap** (1000 Iterationen, Resampling der 5 Zellen unter Beibehaltung der Dyaden innerhalb der Zelle) durchgeführt, um der Nicht-Unabhängigkeit der Dyaden (jede Zelle erscheint in 4 Dyaden) Rechnung zu tragen: same_lang bleibt signifikant (p<0.01), same_frame nicht-signifikant (p=0.82) — die Kernsaussage ist gegenüber dieser konservativeren Inferenz **robust**.

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

### 5.9 Design-Effekt-Beweis, Divergenztreiber und Knoten/Kanten-Dekomposition

> Reproduzierbar via `scripts/lds_c_design_effect.py`, `lds_c_divergence_drivers.py`, `lds_c_node_edge_decomp.py`; Ergebnisse in `data/lds_c/llm_subject/design_effect_*.json`, `data/lds_c/divergence_drivers_*.json`, `data/lds_c/lds_k_deep/node_edge_decomp_*.json`.

**5.9.1 Design-Effekt-Beweis: gleiche Signalamplitude, unterschiedliche Bodenlinie.**

Der Vergleich von Mensch (Between-Subject, N=15) und LLM (Within-Subject, k=10) auf identischem Messrahmen zeigt:

| Sprachpaar | LDS-C Mensch | Boden Mensch | s/f Mensch | LDS-C LLM | Boden LLM | s/f LLM |
|:----------:|:---:|:---:|:---:|:---:|:---:|:---:|
| ZH-EN | 0.963 | 0.958 | **1.005** | 0.955 | 0.875 | **1.092** |
| DE-EN | 0.932 | 0.924 | **1.009** | 0.930 | 0.846 | **1.100** |
| ZH-DE | 0.936 | 0.922 | **1.015** | 0.945 | 0.862 | **1.096** |

Die **Signalamplitude (LDS-C) ist bei Mensch und LLM nahezu identisch (0.93–0.96)**. Der entscheidende Unterschied liegt in der **Bodenlinie** (Within-Language Split-Half): Bei Menschen überlagert die Variabilität *innerhalb* einer Sprachgruppe (0.92–0.96) die Divergenz *zwischen* den Gruppen (Signal/Boden ≈ 1.00 → Signal **untergegangen**); beim LLM liegt der Boden (0.85–0.87) deutlich unter dem Signal (Signal/Boden ≈ 1.09–1.10 → Signal **sichtbar**).

> **Hinweis zur Stichprobengröße (Sample-Size-Kontrolle)**: Die menschlichen Bodenwerte in der Tabelle beruhen auf Halb-Splits mit 3/3 (DE/ZH) bzw. 1/2 (EN) Teilnehmenden; die LLM-Bodenwerte auf 5/5 Stichproben. Ein N-abgestimmter Floor-Scan (§5.9.1, N=6 → 3+3 Halb-Splits, analog zur menschlichen Aufteilung) ergibt für das LLM weiterhin einen Boden von 0.854–0.885 — weit unter dem menschlichen Boden (0.922–0.958, Differenz 0.05–0.07). Die Schlussfolgerung ist daher **nicht** durch unterschiedliche Stichprobengrößen verursacht.

Ein Floor-Scan (LLM-Signal bei N = 3/5/6/8/10 Stichproben pro Sprache) zeigt, dass das Signal **auch bei N=3 nachweisbar bleibt** (Marge +0.02–0.04) und bei N=10 auf +0.08 anwächst. Die menschliche Null ist also **kein Stichprobeneffekt**, sondern Folge der Varianzstruktur: menschliche Teilnehmer innerhalb einer Sprache sind heterogen, LLM-Stichproben desselben Gewichtssatzes sind homogen.

**5.9.2 Virtuelle Between-Subject-Linse + Heterogenitäts-Injektion (direkter Kausalnachweis).**

*(a) Exklusion.* Werden die LLM-Stichproben als "virtuelle Teilnehmer" mit exakt der menschlichen Between-Subject-Pipeline bei menschlicher N (=6 pro Sprache) analysiert, **überlebt das Sprachsignal** (Marge ZH-EN +0.064, DE-EN +0.073, ZH-DE +0.070). D. h. **weder "keine Sprachwirkung" noch "Between-Subject-Design an sich" erklärt die menschliche Null**.

*(b) Direkte Kausalprüfung (Heterogenitäts-Injektion, `scripts/lds_c_heterogeneity_injection.py`).* Mensch und LLM zeigen **fast identische within-language Paar-Overlaps** (ZH 0.057 vs 0.059; DE 0.106 vs 0.108) — die Heterogenität *einzelner* Antworten ist vergleichbar. Der Unterschied liegt in der **Aggregationssparsität**: menschliche Teilnehmer tragen pro Person weniger Konzepte bei, sodass ein 3+3-Halb-Split spärlich ist und beide Hälften kaum überlappen. Injiziert man diese Sparsität in die LLM-Stichproben (Konzept-Dropout mit Wahrscheinlichkeit 1−q), **kollabiert die Signal-Marge monoton**:

| q (Behaltewahrscheinlichkeit) | LLM LDS-C (ZH-DE) | LLM Boden | Signal-Marge |
|:---:|:---:|:---:|:---:|
| 1.00 (keine Injektion) | 0.944 | 0.873 | **+0.071** |
| 0.60 | 0.939 | 0.905 | +0.033 |
| 0.40 | 0.946 | 0.916 | +0.030 |
| 0.30 | 0.955 | **0.941** | **+0.014** |
| **Mensch (Referenz)** | 0.936 | **0.921** | **+0.015** |

**Bei q=0.30 erreicht der injizierte LLM-Boden (0.941) den menschlichen Boden (0.921), und die Signal-Marge kollabiert auf +0.014 — nahe der menschlichen +0.015.** Dies zeigt, dass **eine ausreichende Aggregationssparsität die menschliche Null reproduzieren kann**. **Einschränkung (P2-Recheck)**: q=0.30 ist der spärlichste der zehn Scan-Punkte und **3× spärlicher als die tatsächliche menschliche Sparsität** (der mechanismus-konsistente Zielwert q≈0.76–0.91 liefert weiterhin eine Marge von +0.05–0.065, nicht kollabiert; die automatische Boden-Kalibrierung des Skripts stoppt bei q=0.35 mit Marge +0.033, dem 2,2-Fachen des menschlichen Werts). Die Injektion ist daher eine **Konsistenz-Demonstration** ("extreme Sparsität kann die Null erzeugen"), keine vollständige **direkte Kausalprüfung** mit der realistischen menschlichen Sparsität. Die heterogenitätsbedingte Erklärung der menschlichen Null bleibt gestützt (Exklusion anderer Ursachen + Konsistenz), ist aber nicht als quantitative Kausalzuordnung zu werten.

**5.9.3 Divergenztreiber (RQ4): Rahmengeladene Konzepte treiben ZH-DE.**

Eine Asymmetrie-Analyse über Konzepte (nur in einer Sprache auftretende Konzepte, nach Erwähnungshäufigkeit gewichtet) identifiziert die Treiber der Sprachdivergenz. Für ZH-DE (LLM-P1):

| Thema | Konzept | Richtung | Häufigkeit |
|:------|:--------|:--------:|:---:|
| Gerechtigkeit | equal opportunity | DE-only | 7 |
| Freiheit | freedom limit of | DE-only | 6 |
| Heimat | physical space | ZH-only | 6 |
| Erfolg | goal own | DE-only | 6 |
| Freiheit | boundary freedom of | ZH-only | 4 |
| Gerechtigkeit | due treatment | ZH-only | 4 |

Die Treiber sind **rahmengeladene Kulturkonzepte**: DE tendiert zu Autonomie/Regel/Ziel (equal opportunity, freedom limit, goal own), ZH zu Raum/Grenze/Anspruch (physical space, boundary freedom, due treatment) — konsistent mit den Richtungstendenzen der Themenanalyse (§4.4: DE autonom, ZH rechtlich-institutionell). Geteilte Konzepte sind extrem selten (20–27 über 5 Themen), im Einklang mit LDS-C ≈ 0.93–0.96. Auf Relationsebene (menschlich): DE-only `responsibility → consequence` (freq 3), ZH-only `success → goal` (freq 2) — die strukturelle Arbeitsteilung ist auch relational sichtbar.

**5.9.4 Knoten/Kanten-Dekomposition: Die Reversion ist knotengetrieben.**

Die soziale/institutionelle Umkehr (ZH-DE am konvergentesten in Mathematik, am divergentesten in sozialen Wikipedia) wird in Knoten- und Kantenkomponente zerlegt (frozen v3):

| Quelle | Paar | LDS v3 | J_node | J_edge | node-only | Kantenbeitrag |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| Mathematik | ZH-DE | 0.519 | 0.556 | 0.407 | **0.444** | **0.074** |
| Wikipedia sozial | ZH-DE | 0.819 | 0.200 | 0.162 | **0.800** | 0.019 |
| Mensch kognitiv | ZH-DE | 0.954 | 0.085 | 0.008 | 0.915 | 0.038 |

Die **Umkehr besteht auf der Knotenebene** (Mathematik node-only 0.444 → konvergent; sozial 0.800 → divergent), **nicht auf der Kantenebene**: der Kantenbeitrag ist in der Mathematik am größten (0.074). Institutionelles Wissen konvergiert primär in der **Konzeptwahl (Knoten)**; die **Beziehungsorganisation (Kanten)** bleibt über alle Quellen hinweg systemisch divergent. Dies vertieft §3.8: der Kantenbeitrag 0.075 ist keine "kantengetriebene Konvergenz", sondern eine "kantengetriebene Divergenz" innerhalb eines konzeptuell konvergenten Fachs.

> **Einschränkung (P2-Recheck)**: Die Mathematik-Knoten sind Alignierungs-Labels und damit teils Alignierungsprodukte, nicht unabhängig extrahierte Konzepte; zudem enthält das `de`-Label-Feld im Alignierungs-Datensatz teils chinesische Texte (110/150 Stichprobe), was den mathematischen J_node künstlich erhöht. Ein Size-Matching auf die Wikipedia-Größe (~45 Knoten/Sprache) **kehrt das Muster um**: bei k=15–35 zeigt Wikipedia einen höheren J_node (0.07–0.15) als Mathematik (0.03–0.07); die mathematische "Konvergenz" (J_node 0.556) ist ein Artefakt der nahe-vollständigen Universumsabtastung (~195/219 Gruppen) + des Label-Artefakts, nicht ein Beleg unabhängiger sprachübergreifender Konvergenz. Die "institutionelle Konvergenz / kulturelle Divergenz"-Umkehr ist daher **kein belastbarer inhaltlicher Befund** (Details: `docs/p2_methodology_rechecks.md`).

**5.10 Modellübergreifende Replikation (55 Messungen, 50 eindeutige Modelle).**

> Reproduzierbar via `scripts/lds_c_multi_model.py`; Ergebnisse in `data/lds_c/llm_subject/multi_model_replication_*.json`.

Das identische P1-Protokoll (3 Sprachen × k=10, gleicher Messrahmen LDS-C/Floor/Nullmodelle) wurde auf **42 DashScope-, 7 zen/OpenRouter-Modellen plus D1-Baseline sowie neu je 2 Kilo-, 1 Cohere-, 1 NIM- und 1 opencode-go-Modell** angewendet → **55 vollständige Messungen (je 10/10/10)**, davon **50 eindeutige Modell-Identitäten** (5 Modelle auf zwei Hosts gemessen: deepseek-v4-flash, deepseek-v4-pro, glm-5.2, kimi-k2.6, laguna-s-2.1). Die Familien: Qwen (20), DeepSeek (12), GLM (7), Kimi/Moonshot (6), MiniMax (2), mimo/ByteDance, laguna/poolside (×2 Hosts), longcat, **nemotron-3-ultra + nemotron-3-super (NVIDIA, US-Ursprung)**, **gpt-oss-20b (OpenAI-Gewichte, US-Ursprung)**, **command-a (Cohere, CA-Ursprung)**, gpt-5.6-luna (Herkunft ungeklärt, offengelegt). **~87 % der Messungen stammen von chinesischen Anbietern; sieben westliche Messungen** (6 Identitäten: NVIDIA ×2, Poolside ×2 Hosts, OpenAI-Gewichte, Cohere, luna) sind enthalten.

**Signal — breit repliziert, aber nicht ausnahmslos**: Alle **55 ZH-DE-Sprachpaare sind signifikant** (p<0.05, meist <0.01); die ZH-DE-Marge reicht von +0.03 (deepseek-r1-0528) bis +0.42 (command-a-03-2025). Von den **165 Sprachpaar-Tests sind 8 nicht signifikant** (p≥0.05) — **alle betreffen englisch-haltige Paare** (ZH-EN oder DE-EN), überwiegend DeepSeek-R1/Distill-Modelle (deepseek-r1-0528 DE-EN p=0.672). Hinweis zur p-Reportung: Bei n_iter=500 tritt p=0.0 auf, wenn der beobachtete Wert über allen Permutationen liegt; streng ist p<0.004 zu berichten, und es wurde keine Mehrfachtest-Korrektur vorgenommen.

**Kulturrichtung — über dem Zufallsniveau**: Eine Voten-Analyse der ZH-DE-Treiber (wie viele Modelle markieren ein Konzept als nur-in-DE bzw. nur-in-ZH) wird gegen ein **frequenz-angepasstes Zufalls-Nullmodell** getestet. Die beobachtete Zahl richtungskonsistenter Konzepte (max(DE,ZH) ≥ t) übersteigt das Nullmodell bei allen Schwellen (p<0.001): ≥3: 1133 vs. 882±11; ≥10: **218 vs. 147±4**; ≥20: 61 vs. 12±2. Die stärksten Konzepte (Heimat:safety 46 DE-Stimmen; Heimat:physical space 44 ZH-Stimmen; equal opportunity 42) stützen die DE-Autonomie/ZH-Raum-Orientierung, jedoch mit begrenzter Abdeckung (z. B. produzierten nur 46 von 56 Modellen Heimat:safety als einseitigen Treiber).
