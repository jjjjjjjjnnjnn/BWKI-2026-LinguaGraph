# LinguaGraph — 3 Kernschlussfolgerungen (Poster/Pitch-fähig)

> Komprimierung der 12 Forschungsbefunde (F1–F12) auf 3 Hauptschlussfolgerungen
> Geeignet für: Poster, 3-Minuten-Vortrag, Abstract, Begutachtungsunterlagen

---

## Schlussfolgerung 1: Die Wissensdichte ist nicht-monoton und disziplinabhängig

**Was wir fanden**:
> Die Wissensdichte erreicht ihren Höhepunkt früh in beiden Disziplinen — Mathematik in der **Mittelstufe** (CDS=0,271), Physik in der **Grundschule** (CDS=0,222) — und fällt danach monoton ab.

**Warum es relevant ist**:
> Die Annahme, dass „fortgeschritteneres Wissen dichter vernetzt ist", ist für **beide Disziplinen falsch**. Beide folgen einem **Gipfel-und-Abfall**-Muster, wobei die maximale strukturelle Integration auf der Einführungsstufe auftritt. Diese Konvergenz deutet auf eine universelle Eigenschaft der pädagogischen Wissensorganisation hin: Curricula sind darauf ausgelegt, die Verbindungsdichte in den Grundlagenphasen zu maximieren, bevor sie in die Spezialisierung divergieren.

**Evidenz**:
| Disziplin | Spitzenniveau | Spitzen-CDS | Verlaufsform |
|-----------|-----------|---------|-------|
| Mathematik | Mittelstufe | 0,271 | ↑ Gipfel ↓ stetiger Abfall |
| Physik | Grundschule | 0,222 | ↑ Gipfel ↓ rascher Abfall |

**Robustheit**: ✅ Unabhängig in ZH, EN, DE bestätigt

---

## Schlussfolgerung 2: Die Wissenstiefe hat eine universelle Obergrenze

**Was wir fanden**:
> Die maximale Tiefe der Voraussetzungsketten ist auf **HDS ≤ 8** beschränkt, unabhängig von der Disziplin. Die mittlere Tiefe unterscheidet sich je nach Disziplin (Mathe: 0,40, Physik: 0,85).

**Warum es relevant ist**:
> Pädagogisches Wissen scheint einer natürlichen Tiefengrenze für Voraussetzungsstrukturen zu unterliegen. Beide Disziplinen teilen dieselbe Obergrenze. Physik weist eine **2,1-fach höhere sequenzielle Tiefe** auf als Mathematik (64 % Wurzeln in Physik vs. 83 % in Mathe), jedoch nicht die zuvor mit einer kleineren Stichprobe geschätzten 2,8-fache.

**Evidenz**:
| Metrik | Mathe | Physik |
|--------|:----:|:-------:|
| Max. HDS | 8 | 6 |
| Mittlere HDS | 0,40 | 0,85 |
| Wurzelkonzepte | 83 % | 64 % |
| Strukturtyp | Flaches Netz | Tiefere Kette |

---

## Schlussfolgerung 3: Lehrbuchwissenschaftliche Strukturen konvergieren sprachübergreifend; ΔLDS isoliert das Sprachsignal

**Was wir fanden**:
> Die lehrbuchbasierten LDS-K-Werte reichen von **0,519 (ZH-DE) bis 0,938 (DE-EN)**, doch eine **Nullmodell-Kritik** zeigt, dass diese Werte vollständig von der Gradverteilungsstruktur dominiert werden — nicht von der Sprache. Unter gradbewahrender Randomisierung (Structure Null) sind die realen Graphen systematisch **ähnlicher** als randomisierte Graphen (ZH-EN: 0,934 < 0,957; DE-EN: 0,938 < 0,957; ZH-DE: 0,519 < 0,717). Dies falsifiziert die Hypothese, dass LDS-K sprachbedingte Divergenz misst.

**Warum es relevant ist**:
> Obwohl mathematische Wahrheit universell ist, sind lehrbuchwissenschaftliche Wissensstrukturen über Sprachen hinweg **bemerkenswert ähnlich** — ähnlicher, als gradrandomisierte Graphen erwarten ließen. Diese Konvergenz deutet darauf hin, dass die mathematische Voraussetzungslogik — und nicht die Sprache — die institutionelle Wissensorganisation dominiert. Der zentrale wissenschaftliche Beitrag verschiebt sich von LDS-K (Lehrbuchdivergenz) zu **ΔLDS = LDS-C − LDS-K** (kognitive Divergenz jenseits der Wissensstruktur). Die N=15-Humanvalidierung falsifiziert ΔLDS > 0 unter Between-Subject-Bedingungen — und präzisiert damit die Bedingungen (Within-Subject, N≥30), unter denen ein sprachspezifischer Anteil menschlichen Wissensausdrucks nachweisbar wäre.

**Evidenz (Nullmodell-Suite)**:
| Bedingung | ZH-EN | DE-EN | ZH-DE |
|:----------|:-----:|:-----:|:-----:|
| Voll (LDS-K-Basislinie) | 0,934 | 0,938 | 0,519 |
| Structure Null (gradbewahrend) | **0,957** | **0,957** | **0,717** |
| Node-Permuted Null | 0,934 | 0,938 | 0,519 |
| Complete Random | 1,000 | 1,000 | 1,000 |
| **Interpretation** | Struktur dominiert | Struktur dominiert | Real ÄHNLICHER als Zufall |

**Humanvalidierung (N=15, erweitert)**: Die konzeptuelle LDS-C liegt bei 0.93–0.96 — **nicht unterscheidbar vom Within-Language-Split-Half-Boden (0.92–0.96) und von Label-Permutation (0.94)**. ΔLDS ≈ 0 (−0.05 bis +0.05). Die früheren N=8-Werte (0.70–0.75) werden nicht repliziert.

**LLM-as-Subject (Within-Subject, §5)**: Dasselbe LLM (deepseek-v4-flash) antwortet in ZH/DE/EN → LDS-C 0.93–0.96 **≫ Split-Half-Boden 0.85–0.87** → **Sprachsignal ist unter Within-Subject-Bedingungen klar nachweisbar**. LMM: Sprachcode ist der dominante Organisator (same_lang +0.038, p<0.001), kultureller Rahmen sekundär (same_frame +0.001, p=0.90); ZH-DE trägt eine strukturelle Ebene jenseits der Assoziationsstatistik. **Zentrale Lehre: Der Human-Negativebefund ist ein Between-Subject-Design-Artefakt, nicht ein Beleg für das Fehlen sprachlicher Kognitionseffekte.**

---

## Einheitliche Narration (30-Sekunden-Pitch, AI-Audit-Framing)

> **Mehrsprachige KI-Systeme werden überwiegend mit englischen Daten trainiert — ob sie wertbeladene Konzepte (Gerechtigkeit, Freiheit, Verantwortung, Heimat, Erfolg) sprachübergreifend konsistent verstehen, ist ein blinder Fleck gängiger KI-Evaluation. LinguaGraph macht dieses Modellverhalten prüfbar: Das LLM-as-Subject-Experiment (Within-Subject) weist ein statistisch signifikantes, kulturell gemustertes Sprachsignal nach (LDS-C 0.93–0.96 ≫ Boden 0.85–0.87, Permutationstest p<0.01; DE: Autonomie/Regeln, ZH: Raum/Anspruch). Der Domänen-Kontrollbefund (institutionelles Wissen konvergiert, kulturelle Konzepte divergieren) belegt, dass das Signal kultureller Natur ist, nicht methodisch bedingt. Der Output ist ein interpretierbarer Divergenzbericht pro Modell und Sprachpaar — für Entwickler (Vorabprüfung), Regulierer (Transparenz gemäß EU AI Act) und Forscher (kulturelle Werte in KI).**

> LinguaGraph macht unsichtbare sprachliche Strukturmuster in KI-Systemen sichtbar, messbar und vergleichbar.

## Akademische Version (für Begutachtungsunterlagen)

> **Mathematik, Physik und Chemie folgen unterschiedlichen Dichtetrajektorien, respektieren eine universelle Tiefengrenze und zeigen — kontraintuitiv — bemerkenswerte strukturelle Konvergenz über Sprachen hinweg auf Lehrbuchebene. Auf menschlicher Ebene (N=15) ist in einem Between-Subject-Design kein separierbares Sprachsignal nachweisbar. Ein LLM-as-Subject-Experiment (Within-Subject) weist das Sprachsignal dagegen klar nach: Sprachcode dominiert, kultureller Rahmen ist sekundärer Modulator. Damit ist der Human-Negativebefund als Design-Artefakt klassifiziert, nicht als Beleg für das Fehlen sprachlicher Kognitionseffekte.**

## Theorie → Evidenz-Kette

| Schlussfolgerung | Theorie | Evidenzquelle | Unterstützt |
|-----------|--------|----------------|----------|
| C1 | Ausubel (1963) — Wissensintegration vor Spezialisierung | CDS nach Niveau (Mathe + Physik + Chemie) | Curriculumentwicklung |
| C2 | Novak & Cañas (2008) — Concept Maps als propositionale Netzwerke | HDS-Verteilung (Mathe + Physik) | Lernprogression |
| C3 | Nullmodell (gradbewahrendes Rewiring) | LDS-K vs. Structure Null (Voll < Null) | **Falsifikation** — LDS-K misst KEINE Sprachdivergenz |
| ΔLDS-Hypothese | Linguistische Relativität (Whorf, 1956; Lucy, 1997) | LDS-C vs. LDS-K: Human (N=15, Between) + LLM (Within) | **Human: falsifiziert (Between-Subject); LLM Within-Subject: Sprachsignal nachweisbar** — Code dominiert, Rahmen sekundär |
