# Session Handoff v48 — Post-Seal Portal Rounds (2026-09-19, supersedes v47 as entry)

HEAD: `b4f17c7`, ahead 0, clean. Tag `seal-2026-09-19` → `b7b17f3` (Seal-Zustand);
post-seal commits: `908f01d` (audit) + `b03ae88` (sync) + `093993a` + `1438324` + `a8469df` + `b4f17c7` (portal).
Gates (last full): numbers PASS / cdn PASS / pytest 84/84. JS: node --check 4 inline blocks OK.

## 一、Post-seal 修正链 (v47 之后)
- **D-V9** (`panel_consensus.py` Typo `judged[b]`→`judged[b][i]`): Jaccard-Tabelle 0.06–0.28 falsch → **0.44–0.77**
  (R1–R3 0.77). Deutung: echte Gold-vs-Rater-Divergenz, kein Rauschen. MAINTAIN unberührt (IMPORT-Gates).
  Nur md-Tabelle diff, JSON unverändert. Downstream (SCREEN/REPORT/evidence/§2.8) korrigiert.
- **D-V10** (ZH-EN): v46 fälschlich 0.934; SSOT-Re-Freeze = **0.933** (Basis 0.9330). Portal/Labs/C3/Prosa
  revertiert; Snapshot-Tabellen/Captions/Methodbox mit Snapshot-Label + Dualnote.
- F5 post-hoc-Label; **J3 leak-grep 0 Hits (NEGATIVE)** in SCREEN vermerkt;
  §2.9b Sozial-A2 korrigiert (6.8 zh 0.163/de 0.118, glm zh 0.216/de 0.167);
  v44-Errata (ds P3-EN 0.22→0.21); `.gitignore` + `*key*/*token*`; SEAL HEAD + Errata §五.
- **Portal-Runde 1** (`093993a`): `_deploy/favicon.svg` nachgereicht; `figKeys`-Mapping entfernt
  (7 Labels → `data-i18n`); en-`finding_c_sub` entdeutscht; 27 Orphan-Zeilen raus; Methodology-h2 i18n.
- **Portal-Runde 2** (`1438324`): L7-Provenance-Draft-Card entfernt (Carousel 3 Slides, g4-Hash-Clamp);
  `method_prov_note` formal (19-Modell-Benchmark, qwen-plus); MIMO→EXT (19-model benchmarked, 3-sprachig);
  Carousel-minHeight = aktiver Slide (+Resize-Dispatch); 24 Orphan-Zeilen raus.
- **Show-all-Bug** (`a8469df`): Inline-`translateX` schlug `.all`-CSS (leere Ansicht ab Seite 2) → `paint()`
  löscht Transform im All-Modus; 收起 scrollt zu Section-Start; Button Show all↔Show less (3-sprachig,
  i18n-sicher via `window.limAllLabel`); Nav/Keys/Swipe im All-Modus aus (gedimmt); Count-Init 1/3.
- **Fig-Legenden-Bug** (`b4f17c7`): Farbe=Cell + Schraffur=Anker, Doppel-Legende je Panel (verifiziert per
  Bild-Read en+zh); Portal-Caption + Farbschlüssel (3-sprachig). 9 PNGs (3 Bilder × 3 Dirs) hash-identisch.

## 二、Deploy invariant (jedes Mal verifiziert)
- `_deploy/portal/index.html` == Quelle (byte-identical); `_deploy/index.html` == Quelle minus `../`
  (19 Refs, CRLF-erhaltend); labs ×3 identisch; evidence + favicon + figures gespiegelt.

## 三、Parked (unverändert, Owner-seitig)
R4 21 条 / 人工 12 条 / 人类盲审 / key 轮换 (einziges Risiko, s. SEAL §二) / nach 仓.
Browser-Realcheck offen (Show-all 3 Klicks + Sprachwechsel, s. Commit-Nachricht `a8469df`).

## 四、Einstieg (v47-Tabelle gilt weiter; Neuheiten hier)
- Portal-Audit-Trail: dieser §一. Methodik-Figur: EXT-Label. Limitations: 3 Slides, aktuelle minHeight-Logik.
- Aktuelle Zahlen: REPORT §7/§8, PANEL_SCREEN.md (Jaccard 0.44–0.77), evidence C9b/C21–C24, SSOT ZH-EN 0.933.
