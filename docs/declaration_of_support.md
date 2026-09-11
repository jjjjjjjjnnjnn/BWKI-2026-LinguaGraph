# Erklärung der Unterstützung — Declaration of Support

> **Version**: 2.0 | **Stand**: 2026-09-11 (vor Einreichung final geprüft)
> **Grundlage**: BWKI 2026 Teilnahmebedingungen, Klausel „Eigenständigkeit" (Stand 28.04.2023)
> **Zweck**: Dieses Dokument legt alle externen Unterstützungsquellen des Projekts transparent und vollständig offen. **Es ist mit der schriftlichen Ausarbeitung einzureichen.**
> **v1.0 → v2.0 Änderungen**: alle KI-Anbieter ergänzt (opencode zen / OpenRouter / DashScope / NIM / Cohere / Kilo), 55-Modell-Replikation, Methodenentscheidung Extraktionsmodell = Versuchsmodell, ein Drittanbieter-API-Abrechnungsvorfall; F1-Zahlen-Zuordnung korrigiert.

---

## 0. Zusicherung

Das Projekt (LinguaGraph) wurde in seiner wissenschaftlichen Kernarbeit — Fragestellung, Versuchsdesign, Definition der LDS-Metrik, Datenerhebungsplan, Ergebnisinterpretation und Schlussfolgerungen — von den teilnehmenden Schülern eigenständig erbracht. Alle unten genannten Unterstützungsquellen sind transparent offengelegt; keine Form der Hilfe wurde verschwiegen.

---

## 1. Nutzung von KI-Modellen

Das Projekt nutzt große Sprachmodelle (LLMs) in **zwei klar getrennten Rollen**:

**(1) Als Extraktionswerkzeug** (Text → Konzeptgraph): für Konzept-/Relationsextraktion aus Human-Fragebögen und Wikipedia-Korpora.

**(2) Als Versuchspersonen (LLM-as-Subject, Within-Subject-Design)**: Dies ist die **wissenschaftliche Kernmethode** der Arbeit — dasselbe (bzw. verschiedene) Modelle beantworten 5 Gesellschaftsthemen auf ZH/DE/EN, um die Hypothese „Sprache treibt kognitive Strukturdivergenz" zu prüfen. Dies folgt dem durch Binz & Schulz (2023, *PNAS*) etablierten LLM-as-Subject-Paradigma. **Antworten und Extraktionen der Versuchsmodelle werden im Papier als kontrollierte Experimente berichtet, nicht als verborgene Hilfestellung.**

### 1.1 Verwendete Modelle und Anbieter (alle)

| Anbieter/Endpunkt | Modelle | Verwendung |
|------|------|------|
| **opencode GO** (`https://opencode.ai/zen/go/v1`) | deepseek-v4-flash | Baseline-Versuchsmodell (D1-Hauptexperiment) · Konzept-/Relationsextraktion · Glossar-Anglisierung |
| **opencode zen/v1** (`https://opencode.ai/zen/v1`) | u. a. deepseek-v4-flash, nemotron-3-ultra-free (NVIDIA), mimo-v2.5-free, laguna-s-2.1-free, longcat-2.0-free | Replikations-Versuchsmodelle |
| **OpenRouter** (`https://openrouter.ai/api/v1`, kostenlose Stufe) | u. a. gpt-oss-20b:free (teilweise laufend), nemotron-/laguna-/gemma-Modelle | Replikations-Versuchsmodelle (teilweise unvollständig) |
| **Alibaba Cloud DashScope/Qwen** (`https://dashscope.aliyuncs.com/compatible-mode/v1`) | deepseek-v3/v3.1/v3.2/v4/r1-Familie, GLM-4.5–5.2, Kimi, MiniMax, Qwen3.x u. a., **42 Modelle** | Replikations-Versuchsmodelle |
| **NVIDIA NIM** | gpt-oss-20b | West-Erweiterung (vollständig) |
| **Cohere** | command-a-03-2025 | West-Erweiterung (vollständig) |
| **Kilo** | laguna-s-2.1, nemotron-3-super-120b-a12b | West-Erweiterung (vollständig) |
| **opencode-Terminal** | gpt-5.6-luna (Herkunft ungeklärt) | West-Erweiterung (vollständig) |

**Mehrmodell-Replikation (55 vollständige Messungen / 50 eindeutige Modelle + 31 laufende)**: 2026-08-09/10 wurden 42 DashScope-Modelle + 7 zen/OpenRouter-Modelle + D1-Baseline unter identischem P1-Protokoll (3 Sprachen × k=10) als LLM-as-Subject vermessen. **West-Erweiterung 2026-09-09/10 (gleiches Protokoll, alle vollständig)**: gpt-oss-20b (NVIDIA NIM), command-a-03-2025 (Cohere), laguna-s-2.1 + nemotron-3-super (Kilo), gpt-5.6-luna (opencode-Terminal) → **55 vollständige Messungen / 50 eindeutige Modelle**, alle ZH-DE-Paare signifikant. **Alle Modelle wurden als kontrollierte Versuchsmodelle vermessen**; ihre Antworten und Extraktionen bilden den Datenkörper des Papiers (`data/lds_c/llm_subject/`). Dies sind Forschungsdaten, keine „Hilfe bei der Anfertigung".

### 1.2 Extraktionsqualität und F1-Zahlen (v1-Verwechslung korrigiert)

- **Human-validierte F1 (Extraktion sozialer Konzepte)**: ZH 0,974 / DE 0,949 / EN 0,882, sozial gesamt **0,939** (72 soziale Gold-Annotationen), gewichtet über Domänen **0,881** (n=92) — dies validiert, ob der Extraktor humane Konzeptannotationen wiederherstellt.
- **19-Modell-Extraktionsbenchmark**: F1-Spanne **0,55–0,67** über Modellfamilien (`data/model_comparison/`) — zur Modellauswahl, kein berichteter Projektwert.
- **v1-Fehler**: v1 vermischte beides zu einem einzigen „0,939 (19-Modell-Benchmark)" — korrigiert. Papier §8.7/§8.9 entsprechen den beiden obigen Zahlengruppen.

### 1.3 offengelegte Methodenentscheidung: Extraktionsmodell = Versuchsmodell

In der Mehrmodell-Replikation **extrahiert jedes Versuchsmodell die Konzepte aus seinen eigenen Antworten selbst** (`lds_c_llm_subject.py`, zwei Stufen: Antworten → Extraktion durch dasselbe Modell). Dies hält die „Konzeptstruktur desselben Modells" konsistent, bedeutet aber auch, dass die gemessene sprachübergreifende Divergenz Extraktionverhaltensunterschiede je Sprache enthält. Papier §5 legt diese Konfundierung offen; Extraktionsdichte und Divergenzmarge sind unkorreliert (corr −0,23), und die Domänenkontrolle (institutionelle Konvergenz vs. kulturelle Divergenz) mildert sie teilweise.

### 1.4 Leerergebnisse und Wiederholungen

- Leerergebnisse werden explizit wiederholt (max. 3 Versuche je Nachricht); nach 3 aufeinanderfolgenden Fehlereinheiten wird das Modell automatisch verworfen (`LDS_ABORT_AFTER`)
- Baseline-D1-Experiment: 220/220 Einheiten vollständig; Mehrmodell-Sammlung mit Checkpoint-Fortsetzung je Einheit

---

## 2. Nutzung KI-basierter Hilfsmittel

| Werkzeug | Verwendung | Umfang |
|------|------|---------|
| **Claude Code** (Anthropic) | unterstütztes Programmieren, Schreiben von Datenanalyseskripten, Dokumentation, Code-Review, **dieser Review-/Reparaturprozess** | Kerncode/Analyseskripte wurden mit Claude Code generiert und debuggt; Forschungsdesign und Schlussfolgerungen wurden von den teilnehmenden Schülern geleitet |

**Hinweis**: Claude Code wirkte als KI-Programmierassistent bei Skriptentwicklung, Datenanalyse und Dokumentenlayout mit. **Wissenschaftliche Urteile, Versuchsdesign-Entscheidungen und Ergebnisinterpretation wurden von den teilnehmenden Schülern eigenständig erbracht** und werden gemäß Wettbewerbsregeln transparent offengelegt.

---

## 3. Datensatzquellen

| Datensatz | Quelle | Lizenz | Verwendung |
|--------|------|------|------|
| Human-Fragebogenantworten (N=15) | eigene Erhebung (Online-Fragebogen, 2026-07) | eigene Daten der Teilnehmenden; Einwilligungserklärungen (`docs/ethics/consent_{de,en,zh}.md`), DSGVO-konform | Analyse kognitiver Äußerungen (Between-Subject-Design) |
| Wikipedia-Artikel (ZH/EN/DE, 5 Gesellschaftsthemen) | Wikipedia | **CC-BY-SA** (Namensnennung erforderlich) | soziokulturelle Wissenskontrolle (Negativkontrolle/Vertiefung) |
| Mathematik-Lehrbuch-Wissensstruktur | CN/DE/EN-Lehrpläne und -Lehrbücher | Konzeptgraphen sind Strukturbeschreibungen, keine Textkopien | institutionelle Wissenskontrolle (LDS-K) |

### Wikipedia-Namensnennung (CC-BY-SA-Konformität)
Das Projekt extrahierte dreisprachige Konzeptstrukturen zu 5 Gesellschaftsthemen (Freiheit/Gerechtigkeit/Verantwortung/Heimat/Erfolg). Gemäß CC-BY-SA werden die Quellartikel hier genannt:
- Jede Extraktionsdatei `data/wikipedia_extractions/{topic}_{lang}.json` enthält ein `source_url`-Feld mit dem konkreten Artikellink.
- **Bei Einreichung**: Das Literaturverzeichnis des Papiers listet je Datei die Wikipedia-Artikel mit Extraktionsdatum (2026-08-08) auf.

---

## 4. Personen und Institutionen

| Beteiligte | Rolle | Anmerkung |
|--------|------|------|
| Teilnehmende Schüler | Projektleitung, Forschung | Forschungsdesign, Datenerhebung und Ergebnisinterpretation eigenständig erbracht |
| Schule (deutsches Gymnasium) | stellt Rahmen | keine inhaltlich-wissenschaftliche Einwirkung |
| Weitere Teams/Institutionen | keine | keine externe Forschungskooperation |

---

## 5. Rechenleistung, Infrastruktur und Drittanbieter-API-Abrechnung

| Posten | Angabe |
|------|------|
| Rechenressourcen | **lokale CPU** (Python-Analyseskripte) + **Drittanbieter-LLM-APIs** |
| GPU | **keine** externe GPU-Leistung genutzt |
| Drittanbieter-API-Abrechnung | opencode GO (nutzungsbasiert), DashScope (Freibetrag + ein Sperrvorfall), OpenRouter (kostenlose Stufe), opencode zen/v1 (kostenlose Stufe) |

### 5.1 Drittanbieter-API-Abrechnungsvorfall (ehrliche Offenlegung)

Am 2026-08-10 führte bei einer DashScope-Batch-Sammlung die **versehentliche Nutzung eines nicht kostenfreien Modells zu einer kurzen Kontosperrung wegen Zahlungsrückstands**. Das Problem wurde am selben Tag erkannt: Nach Umstellung auf **ausschließlich Freibetrags-Modelle** wurde die Sammlung fortgesetzt und nach Begleichung wieder aufgenommen. Der Vorfall ist im internen Übergabedokument (`docs/session_handoff_20260810.md` §3.3) festgehalten. **Er beeinträchtigt die Validität der Forschungsdaten nicht** (erhobene Daten wurden verifiziert), wird aber der Vollständigkeit halber offengelegt.

---

## 6. Urheberrecht und Musik (Videomaterial)

- Das Einreichungsvideo verwendet ausschließlich selbst erstellte Bilder und systemgenerierte Inhalte.
- Falls im Video urheberrechtlich geschütztes Material verwendet wird, werden in der Videobeschreibung **Autor/Rechteinhaber und Link genannt** (gemäß Regelwerk).
- LDS-Definition, Fragebogen und Versuchsdesign der Arbeit sind originär (einschlägige Literatur im Papier zitiert).

---

## 7. Selbstprüfung und Compliance-Bestätigung

| Regelanforderung | Status |
|---------|------|
| Offenlegung der KI-Modellnutzung | ✅ diese Datei §1 (alle Anbieter + 55-Modell-Replikation + Extraktions-=Versuchsmodell-Entscheidung) |
| Offenlegung KI-basierter Hilfsmittel | ✅ diese Datei §2 |
| Offenlegung der Datensatzquellen | ✅ diese Datei §3 |
| Offenlegung Personen/Institutionen | ✅ diese Datei §4 |
| Offenlegung Rechenleistung/Infrastruktur | ✅ diese Datei §5 (inkl. API-Abrechnungsvorfall) |
| Namensnennung von Video-Copyright-Material | ⏳ bei Aufnahme auszuführen |
| EU-AI-Act-Konformität | ✅ LLM-Nutzung für Forschungsanalyse, keine beschränkten Zwecke (keine Deepfakes u. Ä.) |
| Keine diskriminierenden/antidemokratischen/militärischen Inhalte | ✅ nicht zutreffend |

---

*Dieses Dokument wird mit der schriftlichen Ausarbeitung eingereicht. Übersehene Hilfsquellen werden vor Einreichung nachgetragen.*

---

## 8. Unterschrift (bei Einreichung ausfüllen)

| Feld | Angabe |
|------|--------|
| Ort, Datum | __________, 2026-09-__ |
| Name (Druckschrift) | __________ |
| Unterschrift | __________ |

*Erklärung: Die obige Offenlegung ist vollständig und wahrheitsgemäß; alle KI-/Werkzeug-/Datenquellen der Arbeit sind in §§1–5 genannt.*
