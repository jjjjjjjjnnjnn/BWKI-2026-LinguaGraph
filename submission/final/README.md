# LinguaGraph — BWKI 2026 Final Submission (bis 20.09.)

> Stand: 2026-09-08 (v0.13.2) | Phase-3b-Anhangnotiz 2026-09-16 (committed 2026-09-16): Appendix W (`docs/paper/08_appendixW_weight_vs_human.md`) ist exploratory appendix-only und NICHT im assemblierten PDF (`scripts/build_paper_pdf.py` ORDER = Kernkapitel only); Design-vs-Execution-Richtertrennung siehe `declaration_of_support.md` §1 + Paper §2.12; Zahlenstand unten unverändert (177er口径 unverifiziert, nicht übernommen).
> Historie: `submission/idea/` (Ideenanmeldung 28.06., historisch — Teamnamen/Rauschzeichen dort nicht mehr anfassen).

## Forschungsfrage

> Unterscheiden sich ZH/EN/DE systematisch darin, wie sie Wissen organisieren — und können LLM-extrahierte Wissensgraphen diese Unterschiede messen?

## Kernbefunde (Kurzfassung, mit Einschränkungen)

| # | Befund | Einschränkung |
|---|--------|---------------|
| F1–F3 | CDS-Gipfel Mittelstufe (0,271); HDS ≤ 8; flaches Netz | Deskriptiv, ohne CI |
| F5 | Nullmodell: Full < Structure (alle Paare) — LDS-K misst **keine** Sprachdivergenz | Stärkste, ehrlichste Evidenz |
| F11 | N=15 falsifiziert ΔLDS > 0 between-subject | Pilot N=8 nicht repliziert |
| F12 | LLM-within-subject Signal +0,08–0,09 (59 Messungen, 54 Modelle; file truth 62/57/186 incl. qwen-max n=26/30) | ~81 % CN-Anbieter; 9 EN-Paare n. s.; 177er-Maßzahl unverifiziert — nicht übernommen |
| C1 | ZH-DE-Konvergenz (0,519) | **Indikativ** (P2-Recheck: Alignierungs-Labels) |
| F9/F10 | CS 12,7 %–95,4 % | Messung stark, Governance nur Hypothese |
| W (App.) | Weight-Vektor-Kontrollebene exploratory appendix-only (Two-Tier; E1/E1b/E3 Hypothesis/PENDING) | Keine Haupt-Schlussfolgerung; nicht im PDF (ORDER Kernkapitel only); Design phi-4-mini-instruct vs. Ausführung muse-spark-1.3-contributor (Two-Tier nomic-only, unberührt) |

## Zahlen (SSOT `manifest.json`, Build 2026-09-08)

- 556 Konzepte / 525 direkte Relationen (+~3000 transitiv) / 219 trilinguale Gruppen (39,4 %)
- Guard 2026-09-16 verifiziert: `manifest.json` = 556 / 525 / 219 (graph.total_nodes / alignment.total_relations / alignment.aligned_groups); pytest 84 grün; `docs/paper` arXiv-Marker = 18.
- Physik 367 / Chemie 220 (Legacy-Pipelines) → gesamt 1.140+ Konzepte
- Gold: 92 (sozial F1 0,939; gewichtet gesamt 0,881)
- Human: N=15 (Between, Δ≈0) + LLM-within (Signal)
- 59 Messungen: 42 DashScope + 8 zen/OpenRouter + 2 Kilo + 1 Cohere + 1 NIM + 1 Cloudflare + 1 LM-Studio + 3 opencode-go (54 Modelle)lo + 1 Cohere + 1 NIM + 1 opencode-go; alle ZH-DE p<0,05 (p=0,0 als p<0,004 lesen)
- Westlich (7 Messungen): nemotron-3-ultra + laguna-s-2.1 (zen), gpt-oss-20b (NIM), command-a (Cohere), laguna-s-2.1 + nemotron-3-super (Kilo), gpt-5.6-luna (Herkunft ungeklärt)

## Dateien

| Datei | Inhalt |
|-------|--------|
| `LinguaGraph_BWKI2026.pdf` | Paper (assembliert via `scripts/build_paper_pdf.py`, fpdf2; ORDER = Kernkapitel only — Appendix W NICHT enthalten, Grund: exploratory appendix-only) |
| `plattform_antworten.md` | Dokumentations-Antworten (Entwurf) |
| `declaration_of_support.md` | Unterstützungs-Offenlegung (Anhang) |
| `code_einreichung.md` | Reproduktions-Guide |

## Reproduktion

```bash
git clone https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph.git
cd BWKI-2026-LinguaGraph
pip install -r requirements.txt   # prüfen, siehe Checkliste
python -m pytest tests/ -q        # 84 tests (alle gemockt, keine API-Keys nötig)
python scripts/release.py --dry-run
python scripts/build_paper_pdf.py # PDF neu assemblieren
```

PII/API-Keys sind von der Einreichung ausgeschlossen (siehe `code_einreichung.md`).
Offenlegung: Extraktions- vs. Beobachter-Rolle von LLMs siehe `declaration_of_support.md`.
