# Textbook Corpus — Sources & Status (Stand 2026-09-17)

> **Status**: `data/textbook/` ist **nicht im git-Index** (95 txt per 2026-09-17 aus dem Index
> entfernt, Arbeitskopie lokal behalten; `.gitignore:56 data/textbook/ # never commit`).
> Bestandsaufnahme: `LINGUAGRAPH_DATA_INVENTORY.md` / `LINGUAGRAPH_DATA_LINEAGE.md` /
> `data/DATA_MANIFEST.md` (dort: „not committed (size, copyright)" — seit 2026-09-17 vollzogen).

## Warum ausgelagert

- Dateigröße + Urheberrecht (deutsche Materialien: UrhG §60a–§60g fair-use eng;
  interner Hinweis `_deploy/docs/review/gate_review_layer4_ethics.md:40`).
- Dateinamen tragen Quelle/Verlag (z. B. `de_lambacher_5-8.txt`, `zh_初中数学_七年级.txt`);
  pro Datei ist kein separater Lizenzkopf nötig, solange dieser Index gilt.

## Reproduzierbarkeit ohne Textbook-Blob

- Extraktionserzeugnisse **im Repo**: `data/math_extractions/merged/aligned_data.json`
  (933 KB), `config/expert_graphs/*`, `manifest.json` (SSOT 556/517/219).
- L2-Reproduktion (`reproduce_lds_binary.py`, Fig4/Fig8, `numbers_audit.py`, pytest 84)
  hängt nur von diesen Erzeugnissen ab — kein Textbook-Zugriff nötig.
- Offizielle Textbuchquelle (CN): smartedu (PEP/人教版); DE/EN: Verlagsausgaben
  s. `README.md` Textbook-Corpora-Tabelle (Publisher-Liste).

## Rechtlicher Rahmen

- Nutzung ausschließlich Forschungsanalyse (keine Weitergabe, keine Reproduktion im Paper).
- `data/consent/` + `docs/ethics/` (ZH/DE/EN + GDPR) für Human-Daten, unabhängig von diesem Korpus.
