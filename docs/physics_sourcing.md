# Physik-Sourcing: Beschaffungsliste + Lücken (Chemie/Mathe-Anhang)

Stand: 2026-09-12 · Inventar aus `source_references` (Physik 23 Titel, Chemie **89**, Mathe 32 — siehe Portal #sources, gesamt 144).
**Freeze aufgehoben (User-Entscheidung v16):** Merge nach Sammel-Signal, kein 9/13-Datum mehr.

## Physik-Bestand (23 Titel)

| Lang | Vorhanden | Lücke |
|------|-----------|-------|
| ZH (8) | 初中物理八年级上下、小学科学三/四上、高中必修一/二、大学物理×2 | **必修第三册、选择性必修 1/2/3** |
| EN (7) | AP 1/2, CK-12 MS, Feynman (nur 1 Ref), Halliday, Khan ×2 | optional: IGCSE Physics 0625 |
| DE (8) | Cornelsen entdecken, Dorn-Bader, Duden ×2 Einträge, Lambacher Schwere, Tipler ×2 Einträge, Westermann OS | Doppel-Einträge bereinigen (s.u.) |

## Download-Liste (Priorität)

**P0 — Physik ZH (v15-kritisch):**
1. 人教版高中物理必修第三册（全）
2. 人教版高中物理选择性必修第一册（动量/振动波/光）
3. 人教版高中物理选择性必修第二册（电磁感应/交变电流/传感）
4. 人教版高中物理选择性必修第三册（热/气体/原子物理）

**P1 — Chemie (v16 ERLEDIGT als Refs, ohne Buchtexte):**
5. 人教版高中化学选择性必修1（反应原理）—— zitiert (51×), chapter/section noch leer
6. 人教版高中化学选择性必修2（物质结构）—— zitiert (51×), chapter/section noch leer
7. 人教版高中化学选择性必修3（有机）—— zitiert (51×), chapter/section noch leer
8. 邢其毅《基础有机化学》上/下（大学）—— zitiert (123×), chapter/section noch leer
9. 傅献彩《物理化学》上/下（大学）—— zitiert (123×), chapter/section noch leer

**P1 — Mathe (Auffüllung):**
10. 人教A版高中数学必修第一册 / 必修第二册（2019）

**P2 — Pipeline-Cleanup (kein Sampling):**
- `physics_full.json`: Dubletten zusammenführen — "Duden Physik Kompakt" vs "Duden: Physik Kompakt",
  "Tipler Physik" (n=1) vs "Tipler: Physik" (n=252). Skript: Titel normalisieren (Doppelpunkt-Variante → eine Form).

## Ablage-Konvention (`data/textbook/`)

- Dateiname: `{lang}_{kurztitel}_ch{a}[-{b}]_sec{x}[.y].txt`, z.B.
  `zh_物理必修3_ch1_sec1.1-1.7.txt`, `zh_选择性必修1_ch2_sec2.1-2.5.txt`
- PDFs/TXTs der Downloads **bleiben liegen** (nicht löschen); reine Text-Extrakte daneben.
- Nach Ablage: in `data/DATA_MANIFEST.md` eintragen (Titel · Sprache · Kapitel · Stand).
- Verarbeitung: `scripts/physics_pipeline.py` / Chemie-/Mathe-Pendant → `source_references`
  pro Konzept (Lehrbuch · Sprache · Kapitel · Abschnitt) → Portal #sources + Node-Card Top-3.
- Neue Termini brauchen Labels (ZH/EN/DE): `scripts/apply_label_patch.py`-Patchliste erweitern.

## Aufwand-Schätzung

- P0 (4 Bücher): Download (du) + Ablage/Extrakt/Pipeline (ich, ~1 Turn) + Merge erst post-9/13.
- P1/P2: Folgeturns nach Freigabe.
