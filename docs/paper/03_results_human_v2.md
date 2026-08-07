# LinguaGraph — Humanvalidierung (Revision v2, N=15)

> **Sprache**: Deutsch | **Status**: Entwurf zur Überarbeitung von §4 in 03_results.md
> **Datum**: 2026-08-08 | **Ersetzt**: bisherige N=8-Zahlen (andere Pipeline-Ära, inkonsistent)

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
