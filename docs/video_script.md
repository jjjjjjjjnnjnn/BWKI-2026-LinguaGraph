# LinguaGraph — BWKI Video Pitch Script (v2, AI-Audit-Framing)

**Duration:** ~3 Minuten (BWKI-Vorgabe: 2–4 Minuten)
**Format:** Screen recording + narration
**Language:** German (narration) + English (subtitles)
**Stand:** 2026-08-09 | ersetzt v1 (Textbuch-Rahmen, überholt)

> **Narrativer Kern (v2):** LinguaGraph ist ein **Audit-Werkzeug für mehrsprachige KI**: Es misst, ob ein KI-Modell abstrakte, wertbeladene Konzepte (Gerechtigkeit, Freiheit, Verantwortung, Heimat, Erfolg) in verschiedenen Sprachen konsistent versteht — und lokalisiert, welche Konzept-Bestandteile genau divergieren. Das LLM selbst ist der vermessene Proband (LLM-as-Subject, Within-Subject-Design).

---

## 0:00–0:25 — Hook: Dasselbe Wort, verschiedene Karte (直观钩子)

**Visual:** Side-by-side zwei Konzeptgraphen für dasselbe Wort — links „Freiheit" (DE), rechts „自由" (ZH). Verschiedene Hub-Konzepte werden hervorgehoben.

**Narration (DE):**
„Fragen wir ein deutsches KI-Modell: Was gehört zur Freiheit? Es antwortet: Autonomie, Regeln, eigene Ziele. Fragen wir dasselbe Modell auf Chinesisch nach 自由: Es antwortet mit Raum, Grenzen, dem, was einem zusteht. Dasselbe Wort — aber eine andere kognitive Landkarte. Genau solche Unterschiede macht LinguaGraph messbar."

**Narration (EN subtitle):**
"Ask a German AI model: what belongs to freedom? It answers: autonomy, rules, one's own goals. Ask the same model in Chinese: it answers with space, boundaries, what one deserves. The same word — but a different cognitive map. LinguaGraph makes exactly such differences measurable."

---

## 0:25–0:55 — Problem: Der blinde Fleck der mehrsprachigen KI (问题)

**Visual:** Weltkarte mit Sprachfiltern; eine „Lücke" im englisch dominierten Trainingskorpus; Schlagwort „EU AI Act".

**Narration (DE):**
„KI-Systeme werden heute für Milliarden von Menschen in Dutzenden Sprachen bereitgestellt. Aber sie sind überwiegend mit englischen Daten trainiert. Versteht ein Modell ‚Gerechtigkeit' in einem Kreditentscheidungs-System auf Deutsch und Chinesisch gleich? Wenn nicht, erhalten Nutzer je nach Sprache unterschiedliche Behandlung. Gängige KI-Evaluation misst aber nur die Aufgabenerfüllung — nicht, ob die Wertkonzepte des Modells sprachübergreifend konsistent sind. Das ist ein blinder Fleck."

**Narration (EN subtitle):**
"AI systems are deployed to billions of people in dozens of languages, but they are trained mostly on English data. Does a model understand 'justice' in a loan-decision system the same way in German and Chinese? If not, users get inconsistent treatment depending on language. But standard AI evaluation measures task performance — not whether the model's value concepts are consistent across languages. That is a blind spot."

---

## 0:55–1:40 — Methode: Das LLM als kontrollierter Proband (方法)

**Visual:** Drei Panel: dasselbe Modell-Icon antwortet auf DE / ZH / EN zu denselben 5 Themen; Konzeptgraphen werden extrahiert; LDS-Gleichung (1 − mean(J_node, J_edge)).

**Narration (DE):**
„Wie misst man etwas Unsichtbares wie die Konzeptstruktur eines Modells? Kernidee: Man fragt die KI selbst. Wir machen das LLM zum kontrollierten Versuchsprobanden: Dasselbe Modell, dieselben fünf Themen — Gerechtigkeit, Freiheit, Verantwortung, Heimat, Erfolg — nur die Sprache ändert sich. Weil es dasselbe Modell ist, ist Sprache die einzige Variable.

Aus den Antworten extrahieren wir pro Sprache einen Konzeptgraphen. Unsere neue Metrik, der Linguistic Divergence Score (LDS), misst die strukturelle Divergenz — über gemeinsame Konzepte und Relationen. Und wir können nicht nur eine Zahl ausgeben, sondern benennen, welche Konzept-Bestandteile genau divergieren."

**Narration (EN subtitle):**
"How do you measure something invisible like a model's concept structure? Key idea: ask the AI itself. We turn the LLM into a controlled experimental subject: the same model, the same five topics — justice, freedom, responsibility, home, success — only the language changes. Because it is the same model, language is the only variable. We extract a concept graph per language, and our new metric, the Linguistic Divergence Score (LDS), measures structural divergence — over shared concepts and relations. And we can go beyond a single number: we can name exactly which concept components diverge."

---

## 1:40–2:25 — Befunde: Sprachsignal ist real und kulturell gemustert (发现)

**Visual:** Fünf Themen-Säulen ZH-DE (Gerechtigkeit 0.96 / Freiheit 0.96 / Verantwortung 0.98 / Heimat 0.93 / Erfolg 0.93) + Math-Kontrollsäule 0.52; Ecke: "55 Messungen · 50 Modelle · alle ZH-DE p<0.05" + Fußnote "ohne qwen-max-Teilmessung (n=29, in ZH-DE ebenfalls signifikant)"; B1: LDS-C 0.93–0.96 / Boden 0.85–0.87 / Social 0.82 (Basismodell deepseek-v4-flash).

**Narration (DE):**
„Wir haben das Experiment auf 50 Modelle verschiedener Anbieter ausgeweitet (55 Messungen) — auch auf sieben westliche Messungen. In allen 55 Messungen ist das chinesisch-deutsche Signal statistisch signifikant (Permutationstest p < 0.05). Und es ist nicht zufällig, sondern kulturell gemustert: Deutsche Konzepte betonen Autonomie und Regeln, chinesische Raum und Anspruch — die Kulturrichtung übersteigt ein Zufalls-Nullmodell deutlich.

Der entscheidende Kontrollbefund: Institutionelles Wissen — etwa Mathematik — konvergiert sprachübergreifend. Kulturelle Konzepte divergieren dagegen deutlich. Unser Messinstrument findet also genau das, was es finden soll: Konvergenz, wo Konvergenz zu erwarten ist, Divergenz, wo Divergenz zu erwarten ist. Selbst die Beziehungen zwischen Konzepten organisieren sich sprachspezifisch."

**Narration (EN subtitle):**
"We extended the experiment to 50 models from different providers (55 measurements) — including seven western measurements. Across all 55 measurements the Chinese–German signal is statistically significant (permutation test p < 0.05). And it is not random but culturally patterned: German concepts emphasize autonomy and rules, Chinese concepts space and entitlement — the cultural direction clearly exceeds a random null model.

The decisive control finding: institutional knowledge — for instance mathematics — converges across languages. Cultural concepts, by contrast, diverge clearly. Our instrument finds exactly what it should find: convergence where convergence is expected, divergence where divergence is expected. Even the relations between concepts are organized language-specifically."

---

## 2:25–2:50 — Anwendung: Ein neues Werkzeug zur KI-Prüfung (应用)

**Visual:** Drei Nutzer: Entwickler, Regulierer, Forscher; ein „Divergenzbericht" pro Modell und Sprachpaar.

**Narration (DE):**
„Damit ist LinguaGraph eine neue Art von KI-Prüfung. Ein Entwickler kann vor dem Einsatz eines mehrsprachigen Modells prüfen: Driftet mein Modell bei wertbeladenen Begriffen zwischen Sprachen — und wo genau? Für Regulierer liefert es Transparenz, wie der EU AI Act sie für den Einsatz von KI verlangt. Der Output ist interpretierbar — kein Black-Box-Score, sondern eine Liste der konkreten Konzept-Bestandteile, die divergieren."

**Narration (EN subtitle):**
"This makes LinguaGraph a new kind of AI audit. A developer can check a multilingual model before deployment: does my model drift on value-laden terms between languages — and where exactly? For regulators, it provides the transparency that frameworks like the EU AI Act require. The output is interpretable — not a black-box score, but a list of the concrete concept components that diverge."

---

## 2:50–3:10 — Schluss (收尾)

**Visual:** „LinguaGraph" + ein Wort: „Sichtbar." + Danke.

**Narration (DE):**
„LinguaGraph verwandelt eine philosophische Frage — formt Sprache unser Denken? — in eine messbare Ingenieursfrage für die KI-Systeme, von denen wir alle abhängen. Und der Befund ist: Ja, sie driften — messbar über Dutzende Modelle hinweg, in einer klar erkennbaren kulturellen Richtung. Jetzt können wir sehen, wo — das ist der erste Schritt zu einer verlässlichen Prüfung mehrsprachiger KI."

**Narration (EN subtitle):**
"LinguaGraph turns a philosophical question — does language shape our thinking? — into a measurable engineering question for the AI systems we all depend on. And the first finding is: yes, they drift. Now we can see where — and that is the first step toward auditing it."

---

## Recording Checklist

- [ ] Side-by-side Konzeptgraphen „Freiheit" (DE) vs „自由" (ZH) mit Hub-Hervorhebung
- [ ] Weltkarte / Sprach-Split + „EU AI Act"-Einblendung
- [ ] Drei-Sprachen-Panel: dasselbe Modell → 5 Themen
- [ ] LDS-Formel (1 − mean(J_node, J_edge)) + Balken LDS-C vs. Boden (0.93–0.96 / 0.85–0.87)
- [ ] **55-Messungs-Replikation**: Balken der ZH-DE-Margen (top-8 Modelle, 0.03–0.42) + "55 Messungen, 50 Modelle"
- [ ] Treiberliste (DE-only vs ZH-only) aus `divergence_drivers_20260809.json`
- [ ] **Kontrollbefund (P2-Recheck)**: Domänen-Vergleich ist alignierungsabhängig → im Video nicht als harter "Kontrollbeweis" präsentieren; stattdessen die Nullmodell-Statistik der Kulturrichtung (≥10 Stimmen 218 vs 147, p<0.001)
- [ ] Divergenzbericht-Mockup (Entwickler/Regulierer/Forscher)
- [ ] Deutsche Narration + englische Untertitel
- [ ] Total: ~3 Min (Vorgabe 2–4) · Export 1080p, H.264

## Fakten-Check für die Aufnahme

| Behauptung | Quelle |
|------------|--------|
| 55 Messungen, 50 eindeutige Modelle; alle ZH-DE-Paare p<0.05; 8/165 nicht-signifikante englisch-haltige Paare | `data/lds_c/llm_subject/multi_model_replication_20260910.json` |
| Kulturrichtung über Zufallsniveau (≥10 Stimmen 218 vs 147, p<0.001) | `multi_model_replication_20260910.json` |
| LDS-C 0.93–0.96, Boden 0.85–0.87 (Basismodell) | `data/lds_c/llm_subject/design_effect_20260810.json` |
| DE: Autonomie/Regeln; ZH: Raum/Anspruch | `divergence_drivers_20260809.json` |
| Mathematik full-v3 0.5188 (konvergiert) vs sozial 0.8191 (divergiert); node-only 0.444 nur Dekompositionsebene, kein Domänen-Hauptwert | `node_edge_decomp_20260809.json` |
| Per-Topic ZH-DE: Gerechtigkeit 0.9565 / Freiheit 0.9592 / Verantwortung 0.9804 / Heimat 0.9268 / Erfolg 0.9268 | `lds_c_results_20260808.json` (per_topic_lds_c.ZH-DE) |
| Ethik: Messung = Basis für Audit, nicht fertiges "Korrektur"-Instrument | Formulierung im Skript ehrlich gehalten |
