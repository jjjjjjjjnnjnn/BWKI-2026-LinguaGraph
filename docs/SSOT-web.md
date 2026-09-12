# SSOT-web — Portal/3D站数字口径 (2026-09-11, P0冻结)

> 核验方法: `manifest.json` + `release/manifest.json` + `README.md` L130-136 实读。
> 结论:两组数字都是真,属**不同scope**。重排版时加scope标注,不改任何数字。

## 双口径对照

| 数字 | 值 | Scope | 来源 | 用处 |
|---|---|---|---|---|
| Concepts (total) | 1,140+ | 全项目 Math 556 + Physics 366 + Chemistry 220 | `README.md` L131-134 | portal hero |
| Relations (total) | 1,100+ direct | 同上 (525 + 383 + 215) | `README.md` L131-134 | portal hero |
| Math nodes / relations / groups | 556 / 525 / 219 | 数学子图 (= 3D可视化数据) | `manifest.json` graph/alignment | 视频 SSOT · CognitiveSpace段 (`556 nodes · 525 relations`) |
| Textbooks | 180+ (68 math + 94 phys + 18 chem) | 全项目 | `README.md` L131-134 | portal contributions |
| Gold labels | 92 (social 72, math 20) | 全项目 | `README.md` L142 | validation |
| F1 | social 0.939 / weighted 0.881 | 全项目 | `README.md` L144+ | hero + validation |
| LLM replication | 55 Messungen / 50 Modelle | LLM-as-subject (§5) | `data/lds_c/llm_subject/` | 视频 S04, portal Finding E |
| Benchmark | 19 models (Bailian free-quota, gold 92) | 模型选型基准 | portal #validation | portal hero "19-model benchmark" |
| Human study | N=15 (6 DE + 6 ZH + 3 EN), ΔLDS≈0 | between-subject | `docs/paper/` | portal Finding E + 视频 S05 |

## 重排版执行规则

1. hero 保留 1,140+ / 1,100+,下方加一行 scope 注脚:
   `Math 556 · Physics 366 · Chemistry 220 — full project graph (README.md §dataset)`.
2. CognitiveSpace 段保留 `556 nodes · 525 relations · 219 groups`,标注 `mathematics subgraph (manifest.json)`.
3. "19-model benchmark" 旁标注 `model-selection benchmark on 92 gold labels`,与 §5 的 55/50 区分。
4. 禁止新数字;物理/化学数只用 README 已有值,不反查 legacy pipeline。

## P2b 数据修正 (2026-09-11, v0.14.2-Abgleich)

| # | Stelle | Alt | Neu | Quelle |
|---|---|---|---|---|
| 1 | trajectoryChart + Bühnen-% (50→31, 53→90) | zwei widersprüchliche Quellen (deep-Skripte vs. keyword-bridge-JSON) | **gestrichen**, nur Overalls 12.7/37.3/17.2/95.4 + paper §8.5 | paper = Schiedsrichter, kein Paper-Beleg für Trajektorien |
| 2 | Finding B Physik-Roots | 64% | **60%** (219) | `06_physics_results.md` F7 (mean 0.85 = Paper-Rundung, behalten) |
| 3 | DE contrib1 | 1.160+ / 4.100+ | **1.140+ / 1.100+** | EN/ZH + README |
| 4 | Limitations UK-Granularität | 186 | **397** (NRW 299 · US 2.124 · CN 87) | `04_discussion.md` §8 |
| 5 | Paper-Karten | 56 KB · 19+ refs | **153 KB md · 293 KB PDF · 54 refs** | gemessen (`docs/paper/`, `docs/submission/`) — Update 2026-09-11: **~161 KB md · 217 KB PDF** (deutsche Offenlegung + Strukturmarker) |
| 6 | Fig4 | alte Heatmap (6-22) | **fig4_null_model.png** (6-30), Caption unverändert | `outputs/figures/fig4_null_model_data.csv` |
| 7 | Validation | nur 19-Benchmark | **+55/50-Satz** (paper §5.10, EN/DE/ZH) | `multi_model_replication_20260910.json` |
| 8 | Kleinigkeiten | 180+ · 816 KB | **180** (68+94+18) · **956 KB** (8 PNGs) | README §Dataset · gemessen |

## P2c Modell-Roster + Academic-Honesty (2026-09-11)
- 56 complete-Aggregat = **55 (n=30) + qwen-max (n=29/30)**; 30 error + qwen-max = **31 collecting** (paper §8.15: 86 begonnen, 55 vollständig).
-西方 7 Messungen / 6 Identitäten (NVIDIA×2, Poolside×2 Hosts, OpenAI-Gewichte, Cohere, luna) — rote West-Badges, nach Margin sortiert.
- Alle 55 ZH-DE p=0.0 (<0.01), Marge 0.033–0.424 = paper +0.03…+0.42 (§5.10).
- LDS-Formel: `1 − mean(J_node, J_edge)` (README Metrics; portal vorher GED-veraltet).
- Governance-Downgrade: B = Hypothese, A (Granularität) sicherste Lesart (paper §8.6); ZH-E-Titel Falsifikations-Wording; P2-Recheck-Note an Finding C; Youden 0.13-Zeile; Paper-Sektion real (Abstract/Sections/BibTeX/PDF-Link); Footer +Schule/Autor; Figures 7→8.

## D Figure-i18n (2026-09-11, scripts/figures_i18n.py)

- fig3/fig7 DE+ZH aus Archiv-Snapshots (outputs/physics_comparison.json + chemistry_comparison.json):
  math-mid 0.2705, phys-elem 0.2222, chem-mid 0.0415 — identisch mit EN-Figuren + Portal-Text (asserts im Skript).
- fig4 DE+ZH deterministisch neu gerechnet (seeded) + assert ZH-DE 0.519; Legende/Conditions bleiben EN (Fachbegriffe).
- fig5 EN-ONLY: Recompute aus aligned_data.json ergibt 442/270/6/0.72 vs publiziert 556/459/8/0.40
  (Quellgraph superseded) — Re-Render würde Balken fälschen. Caption bleibt dreisprachig.
- Level-Mapping DE: Grundschule/Mittelstufe/Oberstufe/Hochschule; ZH: 小学/初中/高中/大学.
- Portal tauscht img-src per Sprache (fig5 bleibt EN); Coverage-Chart-Labels dreisprachig.

## D2 fig5-Archäologie: NEGATIV (2026-09-11)

4 Versuche, publizierte Werte (556 nodes / 459 roots / max 8 / mean 0.40) zu reproduzieren:
1. aligned_data.json alle Relationen, BFS: 442 / 270 / 6 / 0.72 ✗
2. merged_relations requires(+prerequisite): 196–201 / ~110 / 4 / ~0.6 ✗
3. compute_hds exakt auf merged (556 Konzepteinträge, 525 Rel): IDs inkonsistent (canonical_name vs Display-Namen) ✗
Schluss: Quellgraph der publizierten Fig5 ist superseded. fig5 bleibt EN-only + Caption;
kein Re-Render (würde Balken fälschen). Skript: scripts/figures_i18n.py (fig3/4/7 only).

## v7 Fix-Pack (2026-09-11)

- F9/F10-Paragraphen + Curriculum-Metas + Benchmark-Tooltip per data-i18n verdrahtet (EN/DE/ZH);
  F9/F10-Texte auf Governance-Downgrade synchronisiert.
- Meta-Tags -> klickbare Chips: Metric->#methodology, F9->#f9, F10->#f10,
  F1-F8/F11-F12-> eigene Finding-Sektion, Systems->#curriculum, Disciplines/Languages->#research.
- Nav-Overflow: globales box-sizing + .nav-group hidden <1100px + sticky switcher (ZH-Button wieder sichtbar).
- Benchmark-Tooltip Bugfix: parsed.y->parsed.x (horizontale Bars).
- cspace.html Mini-Portal (EN/DE/ZH, what/why/how + Launch in-iframe); Portal-Cover lädt Guide.

## v8 Debrand + Fusionschart + Cover-Revert (2026-09-11)

- Namen: 戎嘉骏→戎嘉浚，Zhenxi Lan→兰振熙 (nur ZH-Footer); EN/DE-Pinyin (Jiajun Rong · Zhenxi Lan) + CITATION.cff bereits korrekt.
- HSHL raus (Portal-Footer 3-sprachig, Root-READMEs, sync-mappings); Story-BibTeX Rongjing→Rong+Lan.
- qwen-plus Branding→neutrale Rollenbegriffe (Footer/Methodik/Flussdiagramm/Stat-Karte, Portal+Story+READMEs);
  Datenlabels bleiben (Roster-Zeile, Bench-Chart, Medaillen-Tabelle, CLI, Paper-Methoden).
- Fusionschart: 55 ZH-DE-Margen als horizontale Balken (desc, West rot) per Chart.js — Daten per Skript aus Roster-Tabelle extrahiert;
  19er-F1-Chart unverändert (andere Metrik/Achse); P1-Protokoll als Kleindruck unter dem Chart;
  55-Zeilen-Tabelle in <details>, Collecting-Tabelle separat sichtbar.
- Cover zurück auf Direkt-3D (`../web/index.html`); cspace.html geparkt für Redesign.
- Paper/docs Recruiting-Dokumente unangetastet (Methodenspezifikation + eingefrorene Preregistrierung).

## v9 Browser-Lang + Audit (2026-09-11)

- Erstbesuch folgt navigator.language (zh/de/en, sonst en); gespeicherte Wahl gewinnt; documentElement.lang wird gesetzt (portal/story/cspace).
- Audit Zahlen: keine schweren Fehler. 180+ → 180 (README-Trio + Story, SSOT P2b#8).
- p<0.01 (Portal) vs p<0.05 (Paper/README): beide wahr (perm_p=0.0); Paper-Caveat bleibt führend.
- qwen-max ohne error-Key (n=29): JSON unverändert, Zählregel dokumentiert (55×n=30 + qwen-max n=29/30).
- 0.55–0.67 vs 0.547 (story deepseek-chat): Rundung, ok.
- _deploy/LinguaGraph_BWKI2026.pdf (unreferenziert, identische Kopie) gelöscht; Mirrors 7/7 SAME; keine Konflikte/Backups; keine >10MB tracked; math_full.json (106MB) ignoriert, nicht getrackt.

## v11 3D-Neubau (2026-09-11)

- Viewer v2: porcelain hell, degree-Größen, Suche+Fokus, UI-Sprache entkoppelt, About-Panel, Modus-Captions, Space-Fill-Shell-Pinning, WASD-Toggle; 3 Bugs (all-EN, breathBase, Ripple-Farbe).
- Physik-Graph (366/383, outputs/physics_cognitivespace.json → web/data_physics.js) + Disziplin-Umschalter + ?graph-Deep-Link; LDS-Zeilen nur Mathe (Physik: Hinweis).
- Galerie cspace.html (2 Graphen + 3 Metrik-Karten + Roadmap); Story-Space-Sektion ent-hypt (556+366, 3 Modi).
- Neu: cds-terrain.html (3×4 CDS, fig7-Quelle), margin-galaxy.html (55 Modelle, 12 Familien), coverage-towers.html (4 Systeme × Stages, coverage_all_curricula.json).

## v12 404-Fix + Suche + Einstiege (2026-09-11)

- 404-Ursache: _deploy/index.html war stale v2-Viewer; relativer ../portal-Pfad lief ins Leere. Fix: scripts/mirror_root.py (portal→Root mit ../-Flattening, fail-loud bei Rest-../).
- UI-Sprache in Topbar neben Research-Portal (+rel=noopener); Browser-Auto beibehalten; Detail-Stufenname übersetzt (lc.l-Bug).
- Suche: Dropdown-Panel, Match-Sprach-Badges, ↑↓/Enter/Esc, +N more, Click-outside-schließt.
- Einstiege: Portal-CS-Sektion 6 View-Buttons (EN/DE/ZH), Story-Space 4 Kleinlinks; Story-CTA-Ziel unverändert.

## v13 Labels + 2D-Satelliten (2026-09-11)

- Label-Lücken Mathe (556): 197 Triple (31 EN-/138 DE-Platzhalter) + 145 EN-only + 120 ZH-only + 94 DE-only. Handübersetzung (~887 Strings, Standardterminologie), Physik (366) war komplett.
- Patchliste: scripts/label_patch_{zh_a,zh_d1,zh_d2,de,en_a,en_b}.json + scripts/apply_label_patch.py (idempotent, nur Missing/Platzhalter, 13 benign Plural-Varianten allowlist). Ergebnis: 556/556 Triple, 0 Platzhalter. Bei release.py-Regeneration: Skript erneut laufen lassen.
- Suche zeigt UI-Sprach-Label + Name (nodeLabel-Fallback); Nachbarliste lokalisiert; Detail-dl weiter dreisprachig.
- Satelliten 3D→2D (null CDN-Abhängigkeit): cds-terrain (Gruppenbalken + Peak-★ + Chemie-0-Rahmen, Klick #finding-a), margin-galaxy (Dot-Strips 12 Familien, rot=westlich, Klick #validation), coverage-towers (Gruppenbalken + Overall-★, Klick #curriculum). T-Wörterbücher + Ziele unverändert; Haupt-Force-Graph bleibt 3D.

## v14 Modi + Margin Proof + Methoden + Quellen (2026-09-11)

- Viewer-Modi neu: universe = freie Force-Lage mit Anker-Reset (Drift-Bugfix, stationär range<1); spacefill = auto-fit Schalen aus Live-Levelverteilung; compare = 1 fixierte Kugel pro Stufe (Tetraeder). sizeVal-Sprachbonus gelöscht (post-v13 alle Knoten trilingual). switchGraph ruft assignAnchors (Physik hatte keine Anker → NaN-Distanz).
- Margin Proof (margin-galaxy.html rewrite): 55 Balken降序, Familienfarben, West-rot-Kontur, Headline 55/55 positiv · +0.03…+0.42 · all p<0.01; Portal/cspace Buttons umbenannt (Margin Proof/Beleg/实证).
- Methoden-<details> überall: 3 Satelliten (T-m_*), Viewer-About (Modi-Zeile), Portal (mm_fig37/fig8/cover/bench/margin), Story (story_mm_*). Keine neuen Zahlen.
- Portal #sources: 73 Titel aus source_references (Mathe 32 / Physik 23 / Chemie 18) + Nav-Link; Refs = Zitatzählung.
- docs/physics_sourcing.md: Lückenliste P0 (Physik ZH 必修三 + 选必1/2/3), P1 (Chemie 选必1-3 + 大学有机/物化; Mathe 必修1/2), P2 Dubletten (Duden/Tipler). Freeze: kein Merge pre-9/13.

## v15 Display-Sprache + Portal + Hero-Video (2026-09-11/12)

- Viewer Sprachfilter → Anzeigesprache (v15): presence-Filter war post-v13 vakant (alle Knoten trilingual → identische Counts). `setLang` lädt nichts mehr nach (kein graphData-Reload, keine Kamera-Bewegung); `nodeLabel` liest `dispLang()` (explizit ZH/EN/DE oder 'all' = UI-Sprache); HUD `hud.display` zeigt Sprache (`display DE`), Counts konstant per Design. Tooltip-Accessor `.nodeLabel()` gesetzt (evaluiert pro Hover → UI-Wechsel folgt automatisch). Kartentitel `:635` nutzt `nodeLabel` (vorher rohes `n.name` = immer ZH).
- Hot-Switch (B): UI-Handler rendert offene Karte (`lastNode`) + Suchdropdown neu; `All` + UI-ZH ⇒ ZH-Titel. Playwright-verifiziert (556/366 konstant, 0 pageerrors).
- Portal (D): `Open Full Screen` → `../web/index.html` (war `../index.html` = Portal-Selbstreferenz live); Galerie-Button in Hauptzeile solid (`Interactive Gallery`/`Interaktive Galerie`/交互展厅); `cognitivespace_hint` Filter→Display-Wording (3-sprachig).
- Hero-Doppelspalte: `#pitch` in `.hero-inner` (Text links, Video rechts; ≤1024px gestapelt); Stats/Scope darunter vollbreit; keine neuen Refs (Regeln `../portal/` greifen positionsunabhängig).
- C Länderfilter GESCHLOSSEN (Entscheidung A): Vorwärts-Mapping (offizielle Methodik) liefert keine per-node Flags (Viewer-Hits NRW 16 / UK 19 / US 20 / CN 5 von 556); Rückwärts-Substrings invertieren die publizierten Totalen (CN 13,5 % statt 95,4 % — grobe Lehrpläne vs. feine Topics sind verschiedene Fragen). Kein Filter, keine Explorationsebene — Anzeige-Sprache ist die Antwort auf #1.
- physics_sourcing-Freeze AUFGEHOBEN (User-Entscheidung v15-Planung): Chemie/Physik-Merge nach Sammel-Signal (E), nicht mehr 9/13-Datum.

## v16 Chemie-Viewer + Quellen 144 (2026-09-12)

- AgentA Daten (ein Durchgang, keine erfundenen Quellen): `expand_chemistry_graph.py` `[:2]`-Cut entfernt → Voll-PUBS; `chem_水/chem_化学` Backfill (218+2=220 Baseline gehalten, 0 dangling); P1 fünf Titel jetzt zitiert (选必1/2/3 je 51 = alle high, 邢其毅/傅献彩 je 123 = alle college); Buchquellen-Texte fehlen noch → `chapter/section` weiter leer, keine Halluzination. Stand: 220 concepts / 215 relations, labels 100 % trilingual, middle 46 / high 51 / college 123 / elementary 0, 89 Publisher-Titel.
- AgentB Konverter + Wiring: `chemistry_pipeline.py` +`graph_to_cognitivespace`/`export_cognitivespace` (idempotent, sha-stabil) → `outputs/chemistry_cognitivespace.json` (gitignored wie physics) → `web/data_chemistry.js` (`var data_chemistry`). Viewer: script-Tag, `GRAPHS.chemistry`, Disziplin-Button + `disc.chemistry`, Deep-Link-Whitelist, `about.body_chemistry`, LDS-Zweig = physics-Wording (mathematics-only), `graph.profile`-Count generisch (`ND.length` statt 556). cspace: soon-Karte → Chemie-Karte (`?graph=chemistry`), `r_disc`/scope/loadnote (`~180–450 KB`) + Filter→UI-Wording (math_d/r_lang) nach v16-Display-Regel.
- Portal `#sources`: Chemie 18 → 89 Titel, Gesamt 73 → 144 (Math 32 / Physik 23 verifiziert unverändert; Portal-Tabelle per Skript gegen `source_references` geprüft = 89/89 deckungsgleich). Hero `1,140+` unverändert (Konzeptzahl gleich).
- Playwright: Chemie 220/215 init, spacefill/compare pinned drift 0, universe settled 0 (= math baseline; 99 direkt nach Mode-Wechsel = Einschwingen, kein Drift), Titel EN/DE/ZH schalten, math-back 556, 0 pageerrors.
