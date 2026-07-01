## 5. Schlussfolgerung

### 5.1 Zusammenfassung der Beobachtungen

Diese Studie stellt LinguaGraph vor, ein wissensgraphbasiertes Framework zur Messung, wie Wissen über Sprachen (Chinesisch, Deutsch, Englisch), Disziplinen (Mathematik, Physik, Chemie) und Bildungssysteme (NRW, UK, US, China) organisiert ist. Das konsistente strukturelle Muster über alle drei Disziplinen hinweg ist:

> **Die Organisation von Bildungswissen folgt einem universellen „früh integrieren, spät divergieren"-Muster: Die maximale Verbindungsdichte tritt in den grundlegenden Stufen (Grundschule/Mittelstufe) auf — über alle Disziplinen und alle drei Sprachen hinweg — und nimmt dann mit zunehmender Spezialisierung monoton ab.**

Die sprachübergreifende LDS-Analyse zeigt ein differenzierteres Bild. Anstelle eines einheitlichen „Spracheffekts" beobachten wir **heterogene sprachübergreifende Strukturbeziehungen**:

| Sprachpaar | LDS-K (Lehrbuch) | Interpretation |
|:----------:|:----------------:|---------------|
| ZH–DE | 0,519 | **Wesentliche Konvergenz** — weit unterhalb der sprachinternen Rauschschwelle (0,97) |
| ZH–EN | 0,934 | **Nahe der Rauschschwelle** — nicht von sprachinterner Variation unterscheidbar |
| DE–EN | 0,938 | **Nahe der Rauschschwelle** — nicht von sprachinterner Variation unterscheidbar |

Die entscheidende Erkenntnis ist nicht, dass „Sprache die Wissensstruktur beeinflusst", sondern dass **verschiedene Sprachpaare systematisch unterschiedliche Grade struktureller Konvergenz aufweisen**, wobei ZH-DE ein Muster zeigt, das Standard-Nullmodelle (grad-erhaltende Randomisierung, sprachinterne Split-Half) nicht erklären können. Diese Heterogenität — nicht Uniformität — ist die primäre Beobachtung, die unser Framework ermöglicht.

### 5.2 Drei Dimensionen der Struktur

| Dimension | Erkenntnis | Grenze |
|-----------|-----------|--------|
| **Dichte (CDS)** | ALLE Disziplinen erreichen Höhepunkt in frühen Stufen, dann Abfall | Mathe: 0,271 @ Mittelstufe; Physik: 0,222 @ Grundschule; Chemie: 0,042 @ Mittelstufe |
| **Tiefe (HDS)** | Voraussetzungsketten sind universell begrenzt | Max 8 (Mathe am tiefsten bei 8, Physik bei 6) |
| **Divergenz (LDS-K)** | Heterogen: ZH-DE konvergiert (0,52); ZH-EN und DE-EN auf Rauschniveau (0,93–0,94) | Sprachinterne Rauschschwelle: ~0,97 |
| **Abdeckung (CS)** | Lehrbuch-Lehrplan-Abgleich variiert nach Governance-Modell | NRW 12,7%, UK 37,3%, US 17,2%, CN 95,4% |

### 5.3 Wissenschaftlicher Kernbeitrag: Ein Framework zur Messung sprachübergreifender Strukturheterogenität

Der Kernbeitrag dieser Studie ist **keine** universelle Erkenntnis über Sprache und Kognition, sondern vielmehr ein **methodologisches Framework**, das heterogene sprachübergreifende Strukturbeziehungen sichtbar und quantifizierbar macht. Im Einzelnen:

1. **LDS allein ist unzureichend** — die Nullmodell-Suite zeigt, dass LDS-K-Werte gegen mehrere Basislinien interpretiert werden müssen (Struktur-Null, sprachinterne Rauschschwelle, kompletter Zufall)
2. **LDS-K zeigt strukturelle Konvergenz, nicht Divergenz** — alle drei Sprachpaare zeigen LDS-K-Werte auf oder unterhalb ihrer sprachinternen Rauschschwellen
3. **ΔLDS = LDS-C − LDS-K wird als interpretierbares Sprachsignal vorgeschlagen**, erfordert aber N ≥ 30 menschliche Daten für statistische Validierung
4. **Pilotdaten (N=8) zeigen heterogenes ΔLDS**: nur DE-ZH (+0,232) unterstützt die ΔLDS > 0-Hypothese; ZH-EN (−0,230) und DE-EN (−0,211) tun dies nicht. Die Erklärung für dieses Muster ist noch nicht bekannt und erfordert weitere Untersuchung.

Der 19-Modell-Benchmark (F1-Bereich 0,55–0,67) und die Wikipedia-Negativkontrolle (LDS=1,0) bestätigen, dass diese Beobachtungen keine Artefakte der Extraktionsmethodik sind.

### 5.4 Beiträge

Wir stellen LinguaGraph vor, ein Framework, das:

1. **Automatisch mehrsprachige Bildungswissensgraphen** aus Lehrbüchern über ZH/EN/DE erstellt
2. **Strukturelle Muster** mittels vier graphbasierter Metriken (CDS, HDS, LDS, CS) quantifiziert
3. **Eine Nullmodell-Grundlage** zur Interpretation von LDS bereitstellt, die heterogene sprachübergreifende Strukturbeziehungen statt eines uniformen Spracheffekts aufdeckt
4. **Über drei MINT-Disziplinen** (Mathematik, Physik, Chemie) kreuzvalidiert
5. **Lehrplanabgleich** über vier Bildungssysteme integriert (NRW 12,7%, UK 37,3%, US 17,2%, CN 95,4%)
6. **19 mehrsprachige LLMs** für Konzeptextraktion benchmarkt (F1-Bereich 0,55–0,67) und so die modellübergreifende Robustheit bestätigt

### 5.5 Einschränkungen

Die Studie hat fünf wesentliche Einschränkungen:

1. **Extraktionsqualität variiert nach Domäne**: Soziale Konzeptextraktion erreicht ZH F1=0,974, DE F1=0,949, EN F1=0,882 (72 Goldlabels im sozialen Bereich; 92 insgesamt inkl. Mathematik). Die mathematische Domänenextraktion ist niedriger (DE F1=0,506, 20 Goldlabels), was domänenspezifische Variation bestätigt.
2. **Stichprobengröße der menschlichen Validierung**: Die Humanstudie (N=8) zeigt konsistenzübergreifende Muster, erfordert aber größere Stichproben für populationsbezogene Schlussfolgerungen. Die ΔLDS-Berechnung wartet auf N ≥ 30.
3. **Umfang des Nullmodells**: Das graderhaltende Nullmodell ist konservativ — es testet Kantenanordnung jenseits der Gradstruktur, aber nicht, ob die Gradstruktur selbst sprachbeeinflusst ist.
4. **Lehrplanvergleich**: Der Coverage Score verwendet keyword-basiertes Matching; zukünftige Versionen sollten semantische Alignierung integrieren.
5. **Golddatensatzgröße**: Aktuelle 92 Goldlabels insgesamt liefern zuverlässige Schätzungen über Domänen hinweg. Eine Erweiterung auf 200+ würde die statistische Aussagekraft für Untergruppenanalysen weiter stärken.

### 5.6 Zukünftige Arbeit

- **Mehrsprachig feinabgestimmte Modelle** für sprachübergreifende Konzeptextraktion mit höherem F1
- **ΔLDS-Berechnung** mit N ≥ 30 menschlichen Daten zur Isolierung des Sprachsignals
- **Zusätzliche Disziplinen** (Biologie, Geschichte) zur Testung der „früh integrieren, spät divergieren"-Hypothese über Wissenstypen hinweg
- **Semantischer Coverage Score** mittels embedding-basierten Konzeptabgleichs
- **Hierarchische Nullmodelle** zur Trennung von Gradstruktureffekten von Kantenanordnungseffekten
- **CognitiveSpace-Visualisierung** zur interaktiven Erkundung sprachübergreifender Strukturunterschiede

### Abschlusserklärung

> **Wissen in der Bildung folgt einer nichtlinearen strukturellen Organisation, die in ihrer frühzeitigen Integration universell und in ihrer Divergenzrate disziplinabhängig ist. Sprachübergreifende Strukturbeziehungen sind heterogen: Lehrbuchstrukturen konvergieren in unterschiedlichem Maße über Sprachpaare hinweg, wobei ZH-DE wesentlich stärkere Konvergenz zeigt als ZH-EN oder DE-EN relativ zu sprachinternen Basislinien. Das LinguaGraph-Framework macht diese unsichtbaren strukturellen Muster sichtbar, messbar und vergleichbar — und bietet eine methodologische Grundlage zur Untersuchung, wann, warum und in welchem Ausmaß sprachspezifische Wissensorganisation existiert. Die Frage, ob ein echtes Sprachsignal im kognitiven Ausdruck existiert, bleibt offen und erwartet die Erhebung und Analyse von N ≥ 30 menschlichen Antworten.**
