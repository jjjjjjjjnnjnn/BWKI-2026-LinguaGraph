# LinguaGraph — Code-Einreichung (Lauffähiger Code, BWKI 2026)

> **Stand**: 2026-09-08 (v0.13.2) | **Sprache**: Deutsch/Englisch | **Pipeline**: `scripts/lds_c_*.py` (+ kanonisch `scripts/math_graph_pipeline/`)
> **Hinweis**: Der Code ist die reproduzierbare Analyse-Pipeline des LLM-as-Subject-Kernexperiments. Alle Ergebnisse in `data/lds_c/` sind durch diese Skripte erzeugbar.

---

## 1. Ausführen (Reproduktion)

Voraussetzung: Python 3.10+, `pip install -r requirements.txt`.

**Schritt 0 — Tests (Kernvalidierung):**
```bash
python -m pytest tests/ -v        # 84 Tests: Kernmetrik, Nullmodelle, LMM, leere-Menge-Konvention
```

**Schritt 1 — LLM-as-Subject-Daten erzeugen** (Netzwerk/API erforderlich; alternativ liegen die Ausgaben bereits unter `data/lds_c/`):
```bash
python scripts/lds_c_llm_subject.py        # LLM antwortet in ZH/DE/EN auf 5 Themen
python scripts/lds_c_llm_analyze.py        # Konzept-/Relations-Extraktion + Alignment
```

**Schritt 2 — Analyse (vollständig offline reproduzierbar):**
```bash
python scripts/lds_c_compute.py            # Kernberechnung: LDS-C, Bootstrap-CI, Permutations-Nulltest
python scripts/lds_c_llm_lmm.py            # Gemischte Modelle (LMM) + Zell-Cluster-Bootstrap
python scripts/lds_c_llm_per_topic.py      # Themenbezogene LDS-C
python scripts/lds_c_llm_gloss_assoc.py    # Assoziations-Analyse (P1)
python scripts/lds_c_thematic.py           # Thematische Richtungstendenzen
```

**Schritt 3 — Vertiefungsanalysen (2026-08-08, Design-Effekt/Driver/Struktur):**
```bash
python scripts/lds_c_design_effect.py          # Design-Effekt-Beweis (Signal vs. Boden, N-matched)
python scripts/lds_c_divergence_drivers.py     # Divergenztreiber (welche Konzeptbestandteile)
python scripts/lds_c_node_edge_decomp.py       # Knoten/Kanten-Zerlegung der LDS v3
python scripts/lds_c_heterogeneity_injection.py  # Direkter Kausalnachweis (Dropout-Injektion)
```

**Schritt 4 — Kontroll-Domäne (Lehrbuch-Wissen, Domänen-Asymmetrie):**
```bash
python scripts/lds_k_deepen.py               # LDS-K, Knoten-/Kanten-Aufschlüsselung, Sensitivität
```

Alle Skripte schreiben datierte JSON-Ausgaben nach `data/lds_c/` inkl. Nachvollziehbarkeitsblock (Eingabedateien, Modell, Parameter, Seed).

---

## 2. Skriptrollen (Übersicht)

| Skript | Rolle |
|--------|-------|
| `lds_c_llm_subject.py` | LLM-as-Subject-Befragung (ZH/DE/EN, 5 Themen) |
| `lds_c_llm_analyze.py` | Konzept-/Relations-Extraktion, P3-Gloss-Guard |
| `lds_c_compute.py` | LDS-C-Kernberechnung, Bootstrap-CI, Permutations-p |
| `lds_c_llm_lmm.py` | LMM + Zell-Cluster-Bootstrap-SE + Hessian-PSD-Check |
| `lds_c_design_effect.py` | Design-Effekt-Beweis (Signal-Amplitude gleich, Boden verschieden) |
| `lds_c_divergence_drivers.py` | Divergenztreiber je Sprachpaar (Konzept-Ebene) |
| `lds_c_node_edge_decomp.py` | LDS v3 = 1 − mean(J_node, J_edge) Zerlegung |
| `lds_c_heterogeneity_injection.py` | Direkter Kausalnachweis der Design-Artefakt-Hypothese |
| `lds_k_deepen.py` | LDS-K Lehrbuch-Kontrolldomäne + leere-Menge-Konvention |

## 3. Verwendete Datensätze, Modelle, Frameworks (Offenlegung)

| Kategorie | Verwendung | Quelle/Dokumentation |
|-----------|------------|----------------------|
| **KI-Modell** | deepseek-v4-flash @ opencode GO — LLM-as-Subject-Proband + Konzept-/Relationsextraktion | `docs/declaration_of_support.md` |
| **Datensatz: Wikipedia** | Soziale Konzepte (ZH/DE/EN), CC-BY-SA | `data/wikipedia_extractions/` |
| **Datensatz: Menschliche Fragebögen** | N=15 (6 DE · 6 ZH · 3 EN), GDPR-Einwilligung, anonymisiert | `freeze/` (SSOT), `participant_data/` (PII, nicht eingereicht) |
| **Datensatz: Mathematik-Lehrbücher** | Institutionelle Kontrolldomäne | `data/corpus/` |
| **Bibliotheken** | numpy, scipy, statsmodels, pytest | `requirements.txt` |
| **Rechenleistung** | Keine externe GPU; reine API + lokale CPU | — |

**Lizenzhinweis**: Wikipedia-Daten unterliegen CC-BY-SA; Quellen in `data/wikipedia_extractions/` dokumentiert. Lehrbuch-Korpus: urheberrechtlich geschützt, nur für die Analyse verwendet, nicht weitergegeben.

## 4. Projektstruktur (für die Begutachtung)

```
scripts/lds_c_*.py    # Kern-Analyse-Pipeline (LLM-as-Subject + LDS)
scripts/lds_k_*.py    # Kontroll-Domäne (Lehrbuch-Wissen)
data/lds_c/           # Alle Ergebnisse (datierte JSON, reproduzierbar)
data/lds_c/llm_subject/  # LLM-as-Subject-Einzel- und Aggregatdaten
docs/paper/           # Wissenschaftliche Arbeit (DE)
docs/submission/      # Einreichungs-Unterlagen (dieses Dokument + Checkliste)
tests/                # 84 pytest-Tests
```

**Wichtig für die Einreichung**: `participant_data/` (PII) und API-Schlüssel sind nicht Teil des Einreichungs-Codes. Die Einreichung enthält die anonymisierten Aggregate in `freeze/` und `data/lds_c/`.
