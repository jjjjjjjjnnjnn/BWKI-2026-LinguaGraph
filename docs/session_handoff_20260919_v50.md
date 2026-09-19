# Session Handoff v50 — Paper Overhaul + Signed Final (2026-09-19, supersedes v49 as entry)

HEAD: `d403ced` + 3 commits (`ab98503` decl v3.0, `ed203c2` P1, `b2f69e4` dual-signer,
`d403ced` figures) — ahead 0 after final push, clean. Tag `seal-2026-09-19` → `b7b17f3` (unverändert).
Gates: numbers PASS / cdn PASS / pytest 84/84 / CI 3 workflows grün (letzter Push).
Frist BWKI-Plattform: 20.09.2026. Owner-Rest: Plattform-Upload (SIGNED-PDF!), Video-Sichtung, Konsolen-Check.

## 一、Paper-Overhaul P0 (Text + Kette, PDF v1 `A1B672B7…` 260571B/40p)
- **A**: §8.9 archiviert (REMOVED-Banner, Tabelle behalten); §9.3/§9.4 Developing-Portrait;
  04:109/05:63/TRACE + E2-Vollsätze; 19-Modell 6 Stellen umgeschrieben; universell×3 raus;
  Harness-Verdikt-Block in §9.3; 01:28 + Gliederung (2A/2B-Doku, F5-Notiz).
- **B**: [16]→Chen 2017; LDS Linguistic; §2A/§2B-Header; §8.14.4/5→§8.14, N04→§8.14, Story RQ1 raus;
  fig6-Pfad; P3 SSOT-Namen (glm-4.7-flash/qwen3-6.8b + Harness-Aliase); P3b 4-stellig;
  Zahlen-Batch (struct 0,715+Punkt/Mittel-Trennung, Node-Perm retired, Floor/Perm-Zeilen,
  ΔLDS-Quellen, 62/57/186, wiki retired-Tag, J_node-Freeze, Physik 17×/0,84/frozen-Labels/Belege,
  LPA-Pointer, AppW 0,933); p<0,001-Klauseln ×5; Kausal-Soften ×3; AI-Act-Zeile; garantiert;
  Wikipedia-CC-BY-SA-Fußnote (§3.8); Decl §4 Realnamen+Schule; LDS-VEC-Glossar.
- **Dezimal-Skript** (683 Stellen → Komma): 2 Pannen, beide repariert — Header `### 1,1`
  (Fix-Skript), Modellnamen `glm-4,7` (12 Stellen, Fix-Skript). Regel: Prosa Komma,
  Code/frozen-4-stellig/§-Refs/IDs geschützt. Skripte gelöscht (TEMP).
- **C**: Declaration 3 Kopien synchron (Video EINGEREICHT-Namen); `_deploy`-Baum resync
  (paper frisch + AppW lesbar + forensic-Pfade + fig_v2-Spiegel); Menu-PDF-Größen 248KB.

## 二、P1-Reaudit (6 lokal, 0 API-Kosten, PDF v2 `01984D5F…` 260797B/40p)
- Reproduziert: Kanten 162 (59/67/36), P1-perm 0/500, per-topic 5/5, Coverage Δ=0, Titel 83/89.
- **Geändert**: LMM same_frame 0,779→**0,937** (alt ohne Code; neu within-topic 1000 Iter,
  Skript persistiert `scripts/tools/lmm_blockperm_reaudit_20260919.py` + JSON, Re-Run ≡);
  Physik „94 Belege"→10091 Einträge; LPA-D1-Klammer korrigiert (9=Skript/10=Codebook).
- p=0,08-Tausend-Perm geskippt (Schreibverbot `data/lds_c/`, limitationiert). P2 parked.

## 三、Figuren (PDF v3 `3FC0510D…` 2532228B/47p, 15/15 Abb. 1–15 inline DE)
- Mapping: 02: v2_cells, coverage; 03: fig3/fig5/screenshot/fig1/fig4/a7_5/wiki/fig8/a7_2/a7_1/a7_4;
  06: fig6/fig7. a7_3 EXCLUDED (0,72/0,92 veraltet vs. 0,715/0,9615).
- Refs Fig4/Fig8/Abbildung 6→Abb. 7/10/14 (alle Stellen). a7_2-Insert ging 1× verloren → neu + verifiziert.
- **Build-Fix**: `html_clean`-Regex fraß `<img>` (`<i`-Präfix) → `(?!mg)`-Guard; Pfad-Rewrite
  `../../outputs|../../cognitive-space`→absolut. Layout per Render-Proof geprüft (2 Seiten).
- Portal: „2,4 MB PDF" (3 Kopien). Graphen innen Punkt-Dezimalen (frozen snapshots, bekannt).

## 四、Declaration v3.0 + Signatur (PDF v4 `71374717…` 261046B/40p → SIGNED Desktop)
- Header 2.0/09-11→**3.0/2026-09-19** (beide Quellen; v2→v3-Changelog); Phase-3b-Absatz nach
  Echtheitsprüfung (AppW 08:28 + Snapshot) in `docs/`-Quelle gemergt; §8 Dual-Signer
  (Druckschrift vorausgefüllt) in allen 3 Kopien.
- **Desktop-Artefakte (NICHT in git)**: `LinguaGraph_Declaration_of_Support_SIGN.pdf` (5 S.),
  `LinguaGraph_BWKI2026_Paper_SIGNED.pdf` (40 S., alte Fassung), **`LinguaGraph_BWKI2026_FINAL_SIGNED.pdf`
  (47 S., FINAL: Abb-PDF + Hamm/2026-09-19 elektronisch + beide Stift-Signaturen)** — Render-proofed.
  Komposit-Panne (40p-Koordinaten auf 47p-Seite) → mit vermessenen Koordinaten neu; Repo unberührt.
- Signatur-PNGs (`sig_jiajun/zhenxi.png`) liegen auf Desktop (Quelle); TEMP-Skripte gelöscht.

## 五、Einstieg (nächste Session)
v49 (Historie) → dieses v50 → `docs/submission/einreichung_checkliste.md` (Frist-Arbeit:
**FINAL_SIGNED-PDF hochladen**, Video-Sichtung, Konsolen-Check). Zahlen-Anker/Disziplin s. v48 §二/§四.
Bekannte Schönheitsfehler: Graph-Dezimalpunkte (EN) vs. Text (DE); a7-Legenden-Overlap (Originale).
