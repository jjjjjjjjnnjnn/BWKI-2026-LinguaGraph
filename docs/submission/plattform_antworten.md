# LinguaGraph — Antworten zur Projektdokumentation (BWKI 2026)

> **Status**: Entwurf v1 (2026-08-09) | **Sprache**: Deutsch (BWKI-Einreichsprache)
> **Zweck**: Antwortentwürfe für die Fragen in der Einreicheplattform (Idee, Methoden, Umsetzung, Ergebnisse, Fehlerquellen, kritische Einschätzung)
> **Digitale Quelle**: Alle Zahlen stammen aus `data/lds_c/` (verifiziert, Stand 2026-08-09) und der Arbeit `docs/paper/`.
> **Vollständige Unterstützungs-Offenlegung**: `docs/declaration_of_support.md`

---

## 1. Idee — Worum geht es?

Mehrsprachige KI-Systeme werden heute für Milliarden von Menschen in Dutzenden Sprachen bereitgestellt, werden aber überwiegend mit englischen Daten trainiert. Bislang ist ungeklärt, ob solche Systeme abstrakte, wertbeladene Konzepte — Gerechtigkeit, Freiheit, Verantwortung, Heimat, Erfolg — sprachübergreifend **konsistent** verstehen. Gängige KI-Evaluation misst nur die Aufgabenerfüllung, nicht die Konzeptstruktur des Modells.

Die Idee von LinguaGraph: **das KI-Modell selbst zum Versuchsprobanden machen** und messen, ob und wo es wertbeladene Konzepte sprachabhängig strukturiert. Der Output ist ein interpretierbarer Divergenzbericht pro Modell und Sprachpaar — ein neues Werkzeug für Entwickler (Vorabprüfung), Regulierer (Transparenz, EU AI Act) und Forscher (kulturelle Werte in KI).

## 2. Methoden — Wie ist es umgesetzt?

**LLM-as-Subject (Within-Subject-Design)**: Dasselbe Modell (deepseek-v4-flash) wird auf Deutsch, Chinesisch und Englisch zu denselben fünf Themen befragt. Da es dasselbe Modell ist, ist die Sprache die einzige Variable — anders als bei Menschen, bei denen Sprache mit individueller Variabilität konfundiert ist (eine Person spricht eine Sprache).

**Kognitive Graphen**: Aus den Antworten werden pro Sprache Konzeptgraphen extrahiert (Konzepte = Knoten, Relationen = Kanten; 30 geteilte Konzept-IDs, sprachübergreifend aligniert).

**Neue Metrik — Linguistic Divergence Score (LDS)**: `LDS = 1 − mean(J_node, J_edge)`, wobei J_node und J_edge die Jaccard-Ähnlichkeit der Knotenmengen bzw. Kantenmengen zwischen zwei Sprachen sind.

**Statistik**: Label-Permutations-Nulltest (formaler p-Wert), Split-Half-Boden zur Rauschreferenz, Zell-Cluster-Bootstrap für die gemischten Modelle (LMM), Domänen-Kontrollvergleich (institutionelles vs. kulturelles Wissen), Sensitivitätsanalyse über Alignierungs- und Extraktionsparameter.

## 3. Umsetzung — Wie wurde es technisch realisiert?

- **Extraktions-Pipeline**: LLM-basierte Konzept-/Relationsextraktion aus Probandentexten und Wikipedia-Korpora (soziale Konzepte) bzw. Mathematik-Lehrbüchern (institutionelle Kontroll-Domäne).
- **Analyse-Pipeline**: `scripts/lds_c_*.py` — modulare, typisierte, dokumentierte Skripte mit reproduzierbarer Reihenfolge (§6 `docs/lds_formal_definition.md`).
- **Reproduzierbarkeit**: Fixe Seeds, `--seed`-CLI, datierte JSON-Ergebnisse mit Nachvollziehbarkeitsblock (Eingabedateien, Modell, Parameter).
- **Validierung**: 60+ pytest-Tests (Kernmetrik, Nullmodelle, LMM-Robustheit, leere-Menge-Konvention), leere-Menge-Konvention verhindert stille LDS=1.0-Artefakte.
- **Konsistenz**: LDS-Formel v3 ist als Projekt-Source-of-Truth eingefroren; alle Zahlen stammen aus `manifest.json` / `data/lds_c/`.

## 4. Ergebnisse — Was wurde gefunden?

| Befund | Evidenz |
|--------|---------|
| **Das Sprachsignal ist real** | LLM-as-Subject: LDS-C 0.93–0.96, klar über dem Within-Language-Boden 0.85–0.87; Permutationstest p<0.01 (alle Sprachpaare) |
| **Es ist kulturell gemustert, nicht zufällig** | ZH-DE-Divergenztreiber: DE betont Autonomie/Regeln/eigene Ziele, ZH Raum/Grenzen/Anspruch |
| **Domänen-Asymmetrie (Kontrollbefund)** | Institutionelles Wissen (Mathematik) konvergiert sprachübergreifend (node-only 0.44); kulturelle Konzepte divergieren (0.80) → das Signal ist kultureller Natur, kein Messartefakt |
| **Struktur, nicht nur Wortwahl** | Auch die Beziehungen zwischen Konzepten organisieren sich sprachspezifisch (Kanten-Komponente divergiert systematisch) |
| **Warum Menschen dafür ungeeignet sind** | N=15 (6 DE · 6 ZH · 3 EN), Between-Subject: LDS-C 0.93–0.96 ≈ Split-Half-Boden 0.92–0.96 → negatives Ergebnis ist ein Design-Artefakt. Der direkte Nachweis: Heterogenitäts-Injektion in die LLM-Stichprobe (Konzept-Dropout q=0.30) reproduziert exakt das menschliche Negativergebnis (Signal-Marge +0.014 ≈ menschlich +0.015) |

## 5. Fehlerquellen — Was hat nicht funktioniert und warum?

1. **Menschliches Between-Subject-Design** (das wichtigste "Nicht-Ergebnis"): Das erste Human-Experiment (N=15) zeigte kein Sprachsignal. Erst die Design-Effekt-Analyse zeigte: Die Signalamplitude ist bei Menschen und LLMs gleich groß — der Unterschied liegt im Rauschen (menschliche individuelle Variabilität vs. homogene LLM-Stichprobe). Durch Heterogenitäts-Injektion wurde die Negativität **direkt kausal** auf die aggregationsbedingte Sparsity zurückgeführt.
2. **Alignment-Artefakt**: Chinesische Konzepte ohne lateinische Tokens (canonical_key) erzeugten leere Schlüssel → falsche Divergenz. Fix: Glossierung chinesischer Konzepte ins Englische vor der Alignierung, mit expliziter Fehlermeldung bei fehlenden Glosses.
3. **Wikipedia-LDS=1.0-Artefakt**: Leere Mengen erzeugten still die maximale Divergenz. Fix: leere-Menge-Konvention (∅=∅ identisch; ∅ vs. nicht-leer = NaN, kein stilles Maximum) + Testabdeckung.
4. **Modellabhängige Extraktionsqualität**: Die Extraktionsqualität variiert nach Domäne (soziale Konzepte F1≈0.94, deutsche Mathematik F1≈0.51). Dies betrifft die Lehrbuch-Kontrolldomäne, nicht das LLM-as-Subject-Kernexperiment.

## 6. Kritische Einschätzung — Grenzen und nächste Schritte

**Ehrliche Grenzen**:
- **Proof-of-Concept an einem Modell** (deepseek-v4-flash): Eine produktive Anwendung als Audit-Instrument erfordert die Erweiterung auf weitere Modelle.
- **5 Konzepte, 3 Sprachen**: Die Breite der Wertekonzepte ist begrenzt; weitere Konzepte und Sprachen (z. B. Französisch, Japanisch) stehen aus.
- **Kein Schwellenwert** für "kritische" Divergenz definiert — was ein Audit als Handlungsempfehlung bräuchte.
- **Interpretation der Richtung**: Die Divergenztreiber (DE: Autonomie; ZH: Raum/Anspruch) sind deskriptiv; ihre kulturelle Deutung ist Hypothese, keine kausale Erklärung.

**Nächste Schritte**: Modell-Matrix (mehrere LLMs), Konzept- und Spracherweiterung, Schwellenwert-Definition, Interpretation mit Kulturwissenschaft.

## 7. Projektentwicklung — Wie hat sich die Idee entwickelt?

Start (Juni 2026): **Sprachübergreifende Wissensstruktur in Bildungstexten** (Mathematik-Lehrbücher, ZH/EN/DE). Zwischenbefund: Lehrbuchwissen konvergiert strukturell, Nullmodelle falsifizieren eine sprachgetriebene Lehrbuchdivergenz.

Drehung (Juli 2026): Der Fokus verschob sich von der Wissensstruktur zur **kognitiven Konzeptstruktur** und — durch das LLM-as-Subject-Design — zur **Prüfung des KI-Systems selbst**. Die Lehrbuch-Analyse blieb als Domänen-Kontrollbefund erhalten (institutionelles Wissen konvergiert → das kulturelle Signal ist kein Artefakt).

Dieser Wandel ist ausdrücklich erlaubt und dokumentiert ("Idee darf sich im Laufe der Bearbeitung verändern"): Das Projekt begann als Textbuch-Analyse und wurde zu einem Werkzeug zur KI-Validierung.

## 8. Daten, Modelle, Unterstützung — Offenlegung

Vollständige Offenlegung in `docs/declaration_of_support.md`:

| Kategorie | Angabe |
|-----------|--------|
| KI-Modell (Analyse/Proband) | deepseek-v4-flash @ opencode GO (Konzept-/Relationsextraktion, LLM-as-Subject) |
| KI-Assistenz (Entwicklung/Text) | Claude Code (Programmierunterstützung, Datenanalyse, Textdokumentation) |
| Datensätze | Wikipedia (CC-BY-SA, soziale Konzepte), menschliche Fragebögen (GDPR-Einwilligung, anonymisiert), Mathematik-Lehrbücher (institutionelle Kontrolldomäne) |
| Personen/Institutionen | keine externen Kooperationen; Eigenarbeit |
| Rechenleistung | keine externe GPU; reine API + lokale CPU |
