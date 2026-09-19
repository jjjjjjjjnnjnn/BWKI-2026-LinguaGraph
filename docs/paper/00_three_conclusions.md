# LinguaGraph — 3 Kernschlussfolgerungen (Poster/Pitch-fähig)

> Komprimierung der 12 Forschungsbefunde (F1–F12) auf 3 Hauptschlussfolgerungen
> Geeignet für: Poster, 3-Minuten-Vortrag, Abstract, Begutachtungsunterlagen

---

## Schlussfolgerung 1: Die Wissensdichte ist nicht-monoton und disziplinabhängig

**Was wir fanden**:
> Die Wissensdichte erreicht ihren Höhepunkt früh in beiden Disziplinen — Mathematik in der **Mittelstufe** (CDS=0,271), Physik in der **Grundschule** (CDS=0,222) — und fällt danach monoton ab.

**Warum es relevant ist**:
> Die Annahme, dass „fortgeschritteneres Wissen dichter vernetzt ist", ist für **beide Disziplinen falsch**. Beide folgen einem **Gipfel-und-Abfall**-Muster, wobei die maximale strukturelle Integration auf der Einführungsstufe auftritt. Diese Übereinstimmung (Preliminary, nur Mathe/Physik-Lehrbuchgraphen, CDS-Ebene) deutet auf ein sample-begrenztes Muster hin — keine universelle Eigenschaft; Replikation in weiteren Fächern/Sprachen ausstehend.: Curricula sind darauf ausgelegt, die Verbindungsdichte in den Grundlagenphasen zu maximieren, bevor sie in die Spezialisierung divergieren.

**Evidenz**:
| Disziplin | Spitzenniveau | Spitzen-CDS | Verlaufsform |
|-----------|-----------|---------|-------|
| Mathematik | Mittelstufe | 0,271 | ↑ Gipfel ↓ stetiger Abfall |
| Physik | Grundschule | 0,222 | ↑ Gipfel ↓ rascher Abfall |

**◆ Robustheit (Preliminary, STEM-Lehrbuchgraphen, kein Universalitäts-Anspruch)**: Muster in ZH, EN, DE beobachtet — Replikation ausstehend (Chemie: CDS 0,042 @ Mittelstufe, s. §6/akademische Version)

---

## Schlussfolgerung 2 (Preliminary, frozen sample): Beobachtete Tiefenobergrenze HDS ≤ 8 (Mathe max 8 / Physik max 6; frozen June-dense, nicht rekonstruierbar — s. 06_physics/forensic notes)

**Was wir fanden**:
> Die maximale Tiefe der Voraussetzungsketten ist auf **HDS ≤ 8** beschränkt, unabhängig von der Disziplin. Die mittlere Tiefe unterscheidet sich je nach Disziplin (Mathe: 0,40, Physik: 0,84).

**Warum es relevant ist**:
> Pädagogisches Wissen scheint einer natürlichen Tiefengrenze für Voraussetzungsstrukturen zu unterliegen. Beide Disziplinen teilen dieselbe Obergrenze. Physik weist eine **2,1-fach höhere sequenzielle Tiefe** auf als Mathematik (64 % Wurzeln in Physik, 233/367, vs. 83 % in Mathe), jedoch nicht die zuvor mit einer kleineren Stichprobe geschätzten 2,8-fache.

**Evidenz**:
| Metrik | Mathe | Physik |
|--------|:----:|:-------:|
| Max. HDS | 8 | 6 |
| Mittlere HDS | 0,40 | 0,84 |
| Wurzelkonzepte | 83 % | 64 % (233/367; frozen June-dense 219, s. 06_physics) |
| Strukturtyp | Flaches Netz | Tiefere Kette |

---

## Schlussfolgerung 3: Scheinbare ZH-DE-Ähnlichkeit (LDS-K 0,519) — T1-falsifiziert als Label-Artefakt (0,52→0,99, Abb. 10); ΔLDS isoliert … (Ebenen-getrennt, Preliminary)

**Was wir fanden**:
> Die lehrbuchbasierten LDS-K-Werte reichen von **0,519 (ZH-DE) bis 0,938 (DE-EN)**, doch eine **Nullmodell-Kritik** zeigt, dass diese Werte vollständig von der Gradverteilungsstruktur dominiert werden — nicht von der Sprache. Unter gradbewahrender Randomisierung (Structure Null, frozen v3, Full vs. Structure Null) sind die realen Graphen deskriptiv **ähnlicher** als randomisierte Graphen (ZH-EN Snapshot 0,934 < 0,957; DE-EN: 0,938 < 0,957; ZH-DE: 0,519 < 0,717). Lesart T1-falsifiziert: ZH-DE 0,519 kollabiert nach Entfernen CJK-kontaminierter de-Labels (167/219) auf 0,990 (J_node 0,556→0,020); kein Beleg inhaltlicher Konvergenz. Dies falsifiziert die Hypothese, dass LDS-K sprachbedingte Divergenz misst.

**Warum es relevant ist**:
> Mathematische Wahrheit beansprucht universelle Geltung — doch lehrbuchwissenschaftliche Wissensstrukturen erscheinen über Sprachen hinweg oberflächlich ähnlicher als gradrandomisierte Graphen (T1-falsifiziert, s. §8.14; Sample-begrenzung s. §9.3) — Dies ist mit geteilter Gradstruktur vereinbar (Preliminary), kein Dominanz-Beweis. **Einschränkung**: Die Mathematik-Knoten sind teils Alignierungs-Labels (P2-Recheck: `de`-Feld teils chinesisch, Size-Matching kehrt das Muster um) — die ZH-DE-„Konvergenz" ist damit indikativ, kein unabhängiger Beleg. Der zentrale wissenschaftliche Beitrag verschiebt sich von LDS-K (Lehrbuchdivergenz) zu **ΔLDS = LDS-C − LDS-K** (kognitive Divergenz jenseits der Wissensstruktur, Konzeptebene; Relationsebene nicht vergleichbar). Die N=15-Humanvalidierung falsifiziert ΔLDS > 0 unter Between-Subject-Bedingungen — und präzisiert damit die Bedingungen (Within-Subject, N≥30), unter denen ein sprachspezifischer Anteil menschlichen Wissensausdrucks nachweisbar wäre.

**Evidenz (Nullmodell-Suite)**:
| Bedingung | ZH-EN | DE-EN | ZH-DE |
|:----------|:-----:|:-----:|:-----:|
| Voll (LDS-K-Basislinie) | 0,934 | 0,938 | 0,519 |
| Structure Null (gradbewahrend) | **0,957** | **0,957** | **0,715** (Punkt; 5-seed-Mittel 0,717) |
| Node-Permuted Null (retired — Shuffle-then-set = Identität, keine Power, s. LEDGER §2.1) | 0,934 | 0,938 | 0,519 |
| Complete Random | 1,000 | 1,000 | 1,000 |
| **Interpretation** | Struktur dominiert | Struktur dominiert | Real ÄHNLICHER als Zufall |

> Snapshot-Hinweis: Voll-Zeile = Freeze-Stand 2026-09-12 (ZH-EN 0,934); aktueller Re-Freeze (SSOT 2026-09-16) ZH-EN 0,933 — δ im Rundungsband, kein Befundwechsel.

**Humanvalidierung (N=15, erweitert)**: Die konzeptuelle LDS-C liegt bei 0,93–0,96 — **nicht unterscheidbar vom Within-Language-Split-Half-Boden (0,92–0,96) und von Label-Permutation (0,94)**. ΔLDS ≈ 0 (−0,05 bis +0,05). Die früheren N=8-Werte (0,70–0,75) werden nicht repliziert.

**LLM-as-Subject (Within-Subject, §5)**: Dasselbe LLM (deepseek-v4-flash) antwortet in ZH/DE/EN → LDS-C 0,93–0,96 **≫ Split-Half-Boden 0,85–0,87** → **Sprachsignal ist unter Within-Subject-Bedingungen klar nachweisbar**. LMM: Sprachcode ist der dominante Organisator (same_lang +0,038, LMM-Wald-p<0,001; Permutation p=0,000, Cell-Cluster-Bootstrap p<0,01; N=50 Dyaden aus 5 Zellen, single-model), kultureller Rahmen sekundär (same_frame +0,001, p=0,90/0,937/0,82); ZH-DE trägt eine strukturelle Ebene jenseits der Assoziationsstatistik. **Zentrale Lehre: Der Human-Negativebefund ist mit der Heterogenitäts-/Design-Artefakt-Hypothese vereinbar (Exklusion + Konsistenz-Demonstration, q=0,30; mechanismus-konsistente q-Werte kollabieren die Marge nicht vollständig — keine quantitative Kausalzuordnung), kein Beleg für das Fehlen sprachlicher Kognitionseffekte.**

---

## Einheitliche Narration (30-Sekunden-Pitch, AI-Audit-Framing)

> **Mehrsprachige KI-Systeme werden überwiegend mit englischen Daten trainiert — ob sie wertbeladene Konzepte (Gerechtigkeit, Freiheit, Verantwortung, Heimat, Erfolg) sprachübergreifend konsistent verstehen, ist ein blinder Fleck gängiger KI-Evaluation. LinguaGraph macht dieses Modellverhalten prüfbar: Das LLM-as-Subject-Experiment (Within-Subject) weist ein statistisch signifikantes, kulturell gemustertes Sprachsignal nach (LDS-C 0,93–0,96 ≫ Boden 0,85–0,87, Permutationstest p<0,01; DE: Autonomie/Regeln, ZH: Raum/Anspruch). Der Domänen-Vergleich (soziale Konzepte divergieren stärker als institutionelle Labels) ist hierfür **indikativ**, aber wegen der Alignierungsabhängigkeit der Mathematik-Knoten nicht als eigenständiger Beweis zu werten (P2-Recheck; Details: `docs/p2_methodology_rechecks.md`). Der Output ist ein interpretierbarer Divergenzbericht pro Modell und Sprachpaar — für Entwickler (Vorabprüfung), Regulierer (Transparenz, z. B. im Kontext von Dokumentationspflichten wie dem EU AI Act) und Forscher (kulturelle Werte in KI). Die operative Schwelle (Marge ≥ 0,10) ist heuristisch, keine validierte Grenze — modell-/paarabhängig (9 englisch-haltige Paare n.s.) — kein fertiges Audit-Instrument.**

> LinguaGraph macht unsichtbare sprachliche Strukturmuster in KI-Systemen sichtbar, messbar und vergleichbar.

## Akademische Version (für Begutachtungsunterlagen)

> **Mathematik, Physik und Chemie folgen unterschiedlichen Dichtetrajektorien, zeigen im frozen sample HDS ≤ 8 und eine scheinbare Lehrbuch-Ähnlichkeit (T1-falsifiziert als Alignierungs-/Größen-Artefakt, P2-Recheck; Details `docs/p2_methodology_rechecks.md`). Auf menschlicher Ebene (N=15) ist in einem Between-Subject-Design kein separierbares Sprachsignal nachweisbar. Ein LLM-as-Subject-Experiment (Within-Subject) weist das Sprachsignal dagegen klar nach: Sprachcode dominiert, kultureller Rahmen ist sekundärer Modulator. Damit ist der Human-Negativebefund mit der Design-Artefakt-Hypothese vereinbar (gestützt, nicht quantitativ kausal zugeordnet) — kein Beleg für das Fehlen sprachlicher Kognitionseffekte.**

## Theorie → Evidenz-Kette

| Schlussfolgerung | Theorie | Evidenzquelle | Unterstützt |
|-----------|--------|----------------|----------|
| C1 | Ausubel (1963) — Wissensintegration vor Spezialisierung | CDS nach Niveau (Mathe + Physik + Chemie) | Curriculumentwicklung |
| C2 | Novak & Cañas (2008) — Concept Maps als propositionale Netzwerke | HDS-Verteilung (Mathe + Physik) | Lernprogression |
| C3 | Nullmodell (gradbewahrendes Rewiring) | LDS-K vs. Structure Null (Voll < Null) | **Falsifikation** — LDS-K misst KEINE Sprachdivergenz |
| ΔLDS-Hypothese | Linguistische Relativität [49][50] | LDS-C vs. LDS-K: Human (N=15, Between) + LLM (Within) | **Human: falsifiziert (Between-Subject); LLM Within-Subject: Sprachsignal nachweisbar** — Code dominiert, Rahmen sekundär |
