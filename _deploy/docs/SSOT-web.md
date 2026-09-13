# SSOT-web — Portal/3D站数字口径 (2026-09-11, P0冻结)

> 核验方法: `manifest.json` + `release/manifest.json` + `README.md` L130-136 实读。
> 结论:两组数字都是真,属**不同scope**。重排版时加scope标注,不改任何数字。

## 口径冻结 (2026-09-12, frozen — 三学科对照, 不改历史行只定当前值)

| 学科 | 口径 | 值 | 说明 |
|---|---|---|---|
| Math | 输入语料 / 原始库题名 / 入图引用 | **68 / 72 / 32** | 68册输入语料(75 JSON, 含章节拆分)；72原始库题名(含版次重复, 清洗前)；32入图引用(`source_references`, 唯一可引用层) |
| Physics | concepts / relations | **367 / 386** | 含Sensor节点`physics_em_传感器`+3 requires-边；Video baked 366冻结不改 |
| Chemistry | concepts / relations | **220 / 215** | Backfill后基线(218+2, 0 dangling) |
| Titles总量 | Math + Phys + Chem | **204 = 32 + 83 + 89** | Portal `#sources`实测三数之和；README Total以此为准(旧240退役) |

## 双口径对照

| 数字 | 值 | Scope | 来源 | 用处 |
|---|---|---|---|---|
| Concepts (total) | 1,140+ | 全项目 Math 556 + Physics 367 + Chemistry 220 | `README.md` L131-134 | portal hero |
| Relations (total) | 1,100+ direct | 同上 (525 + 386 + 215) | `README.md` L131-134 | portal hero |
| Math nodes / relations / groups | 556 / 525 / 219 | 数学子图 (= 3D可视化数据) | `manifest.json` graph/alignment | 视频 SSOT · CognitiveSpace段 (`556 nodes · 525 relations`) |
| Textbooks | 204 titles (32 math in-graph + 83 phys + 89 chem) | 全项目 Titel-Summe, Portal `#sources` | `02_methodology.md` 计数口径 (68/72/32) | portal contributions |
| Gold labels | 92 (social 72, math 20) | 全项目 | `README.md` L142 | validation |
| F1 | social 0.939 / weighted 0.881 | 全项目 | `README.md` L144+ | hero + validation |
| LLM replication | 58 Messungen / 53 Modelle (174 Tests; file-truth 59/54/177) | LLM-as-subject (§5) | `data/lds_c/llm_subject/` | 视频 S04, portal Finding E |
| Benchmark | 19 models (Bailian free-quota, gold 92) | 模型选型基准 | portal #validation | portal hero "19-model benchmark" |
| Human study | N=15 (6 DE + 6 ZH + 3 EN), ΔLDS≈0 | between-subject | `docs/paper/` | portal Finding E + 视频 S05 |

## 重排版执行规则

1. hero 保留 1,140+ / 1,100+,下方加一行 scope 注脚:
   `Math 556 · Physics 367 · Chemistry 220 — full project graph (README.md §dataset)`.
2. CognitiveSpace 段保留 `556 nodes · 525 relations · 219 groups`,标注 `mathematics subgraph (manifest.json)`.
3. "19-model benchmark" 旁标注 `model-selection benchmark on 92 gold labels`,与 §5 的 58/53 区分。
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
| 7 | Validation | nur 19-Benchmark | **+58/53-Satz** (paper §5.10, EN/DE/ZH) | `multi_model_replication_20260913.json` |
| 8 | Kleinigkeiten | 180+ · 816 KB | **204 Titel-Summe (32+83+89, P2b#8 alt 180 = 68+94+18 Volumen-Mix, retired)** · **956 KB** (8 PNGs) | README §Dataset · gemessen |

## P2c Modell-Roster + Academic-Honesty (2026-09-11)
- 59 complete-Aggregat = **58 (n=30) + qwen-max (n=26/30)**; 22 error + qwen-max + phi-4-mini (n=25, ZH-DE-Voter) = **24 collecting** (paper §8.15: 81 begonnen, 58+1 vollständig).
-西方 10 Messungen / 9 Identitäten (NVIDIA×2, Poolside×2 Hosts, OpenAI-Gewichte, Cohere, Meta-Gewichte, xAI, luna, spark) — rote West-Badges, nach Margin sortiert.
- Alle 58 ZH-DE p<0.004 (<0.01; 500-perm. resolution limit), Marge 0.033–0.424 = paper +0.03…+0.42 (§5.10).
- LDS-Formel: `1 − mean(J_node, J_edge)` (README Metrics; portal vorher GED-veraltet).
- Governance-Downgrade: B = Hypothese, A (Granularität) sicherste Lesart (paper §8.6); ZH-E-Titel Falsifikations-Wording; P2-Recheck-Note an Finding C; Youden 0.12-Zeile (58 Margen, CI 0.12–0.13); Paper-Sektion real (Abstract/Sections/BibTeX/PDF-Link); Footer +Schule/Autor; Figures 7→8.

## v23f Replication-58 (2026-09-13, 09-13-Replikation löst 09-10 ab)
- Quelle: `multi_model_replication_20260913.json` (10:01) — 81 Keys (6 Dubletten bereinigt: mistral-/nvidia-nim-/gemma-Prefixe), **58 n=30 (53 Identitäten, 5 Dual-Host)** + qwen-max n=26/30 (3 Quota-Leerläufe gestrippt, LDS stabil) + phi-4-mini n=25 (ZH-DE-Voter, min-units=5).
- Promoviert: grok-4.6 (+0.09), llama-3.3-70b (+0.12, Meta-Gewichte = Western), muse-spark (+0.12). Datei-Wahrheit **59/54/177**; publiziert **58/53/174**.
- Strata (Skript `sw_fix_analyses.py`, WESTERN_MARKERS +llama): CN 48/48 mean 0.130 — West 10/10 mean 0.162 (ohne luna 9/9 mean 0.155); CN-Anteil ~83 %.
- Votes (`direction_consistency`, 60 Voter): ≥3: 1179 vs 919±11; ≥10: 236 vs 156±4; ≥20: 72 vs 14±2 (alle p_null_ge=0.0). Heimat:safety 48 DE; physical space 45 ZH; equal opportunity 45. Paper-Zähler „48 von 59 [inkl. qwen-max n=26/30; publiziert 58/53]".
- Youden (58 Margen): Optimum 0.12, CI 0.12–0.13, J=1.0 (Median-Split-Tautologie wie bisher); Heuristik 0.10 **unterhalb** CI → sensitiv-inklusiv formulieren (keine validierte Grenze, unverändert).
- Dedup: 53/53 sig, mean 0.138 (vs 0.135 über 58). EN n.s. weiter 8/174, alle EN-haltig (R1/Distill 6/10 EN-Tests vs 2/106 übrige; R1-EN-Boden 0.844 vs 0.775).

## D Figure-i18n (2026-09-11, scripts/figures_i18n.py; Wave 2 2026-09-12 scripts/figures_i18n_wave2.py)

> Freshness-Note (2026-09-13 verifiziert): CSV neuer als EN-PNG (wiki/heatmap/figure1/figure3, CSV 09-12 vs PNG 06-19/06-22) ist **kein Drift** — Wave-2-Skript schreibt fehlende CSVs aus frozen EN-Werten (EN-PNGs sind die Quelle, nie überschrieben) + EN-Pixel-Gate (MAE=0.000, `--check` 2026-09-13 ALL OK). EN-PNGs bleiben maßgeblich; _de/_zh sind Chrome-Übersetzungen identischer Balken.

- fig3/fig7 DE+ZH aus Archiv-Snapshots (outputs/physics_comparison.json + chemistry_comparison.json):
  math-mid 0.2705, phys-elem 0.2222, chem-mid 0.0415 — identisch mit EN-Figuren + Portal-Text (asserts im Skript).
- fig4 DE+ZH deterministisch neu gerechnet (seeded) + assert ZH-DE 0.519; Legende/Conditions bleiben EN (Fachbegriffe).
- fig5 EN/DE/ZH alle live (B7 2026-09-13 in figBases aktiviert): publizierte Balken frozen, Quellgraph superseded — kein Re-Render, Disclosure via docs/fig5_hds_forensic.md (Portal-Caption trägt den Hinweis dreisprachig).
- fig_wikipedia_lds DE+ZH ebenfalls aktiviert (Dateien vorhanden), aber methodische Kontrolle only (Gloss ohne Human-Spot-Check, Ledger §7 needs_review) — nie als formaler Beleg.
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
- Fusionschart: 58 ZH-DE-Margen als horizontale Balken (desc, West rot) per Chart.js — Daten per Skript aus Roster-Tabelle extrahiert;
  19er-F1-Chart unverändert (andere Metrik/Achse); P1-Protokoll als Kleindruck unter dem Chart;
  55-Zeilen-Tabelle in <details>, Collecting-Tabelle separat sichtbar.
- Cover zurück auf Direkt-3D (`../web/index.html`); cspace.html geparkt für Redesign.
- Paper/docs Recruiting-Dokumente unangetastet (Methodenspezifikation + eingefrorene Preregistrierung).

## v9 Browser-Lang + Audit (2026-09-11)

- Erstbesuch folgt navigator.language (zh/de/en, sonst en); gespeicherte Wahl gewinnt; documentElement.lang wird gesetzt (portal/story/cspace).
- Audit Zahlen: keine schweren Fehler. 180+ → 180 (README-Trio + Story, SSOT P2b#8).
- p<0.01 (Portal) vs p<0.05 (Paper/README): beide wahr (perm_p<0.004); Paper-Caveat bleibt führend.
- qwen-max ohne error-Key (n=26, zh10/de10/en6, 3 Quota-Leerläufe gestrippt): JSON unverändert, Zählregel dokumentiert (58×n=30 + qwen-max n=26/30).
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

## v17 Doppelbilanz 55/56 + Wortlaut-Fixes (2026-09-12)

- Datei-Wahrheit (`multi_model_replication_20260910.json`, per Skript verifiziert): 56 ok Modelle (55×n=30 + qwen-max n=29, de10/en9/zh10), 51 Identitäten (`n_models_unique=51`), 168 Paare (56×3), ZH-DE 56/56 signifikant (perm_p alle 0.0), 8 n.s. alle EN (DE-EN×6 inkl. r1-0528 p=0.672, ZH-EN×2). Western 7 Messungen / 6 Identitäten (laguna×2 eine Familie). Q6-Definitionen: 218 = `n_consistent_at_report_threshold`, 147.1±4.2 = permutation null mean±SD (`direction_consistency`, L7776–7952), n=56 = votierende Modelle (nicht 1679 Messungen).
- Publik-Konvention (User-Entscheidung): 55/50/165 + Fußnote „ohne qwen-max-Teilmessung (in ZH-DE ebenfalls signifikant)". SSOT führt beide Bücher; Portal-Proof-Headline, Video-Skript, judge_qa tragen die Fußnote; `paper/` unangetastet (Autoren-Domäne).
- Wortlaut-Fixes (audit-only-Linie): DE `US-amerikanische` → `sieben westliche Messungen` (Skripte + DE-srt); `toward correcting it` → `toward auditing it` (Skripte + EN-srt cue15; DE-Schluss hat keinen correcting-Anspruch). srt als Draft committet (Timing geschätzt). CHANGELOG v0.14.2 verifiziert (F1=0,881 in 04_discussion:176, 238 Links in 03_results:56 — kein Over-claim).
- Physik-94-Versions-Caveat: nur narrativ (story/pitch_10min), `outputs/` ohne Beleg, cross_refs nur 23 Titel-Strings → W1-Verifizierung oder Wording auf Titel zurückstufen (Autoren-Option).

## v17-phys P0-Refs + 81 Titel (2026-09-12, same batch)

- W1b: `data/textbook/` null Physik (nur Mathe) → Branch 3: `expand_physics_graph.py:1018`-Cut (`level_pubs[:2]`) bestätigt, dry-run refs 2127→10088 bei identischen 366/383 (Relationen bit-identisch verifiziert). P0 544 refs = 136 high-Knoten × 4 Bücher (je 100 % high-Abdeckung), Katalog-Ebene 0 neue Topics, einzige Lücke Sensor/Sensorik (1 Kandidat, nicht gebaut — 366-Headline geschützt).
- Merge: Draft → `physics_full.json` (names identisch), `physics_pipeline.py`-Reexport → `data_physics.js` (366/383, labels 100 %), Draft gelöscht, Mapping als `physics_p0_mapping.json` behalten. Portal `#sources` Physik 23→81, gesamt 202 (32+81+89); Tabelle per Skript 81/81 deckungsgleich. Story/README/pitch_10min: „94 versions/editions" → „81 titles (94 refs)" (94 = Planungskatalog 33+34+27 inkl. Doppelzählung, real distinct 81, Triples 94). `paper/06` („94 Verlagsausgaben", Chemie „6 Verlage") als Autoren-Sign-off offen gelassen.
- Playwright: Physik 366/383 HUD, Karte öffnet, 0 pageerrors. Duden/Tipler-Dubletten in den Daten natürlich mergiert (103/254); P2-Normalisierung weiter offen, separat.

## v18 T-Falsifikation + Sensor-367 + Fig8 (2026-09-12)

- T1/T2/T3 (nur vorhandene Daten, Kette zuerst gegen 0.556/0.407→0.519 validiert <0.001): T1 FilterA (167/219 CJK-de raus, 52 behalten) ZH-DE J_node 0.5556→0.0196, LDS 0.52→0.99 = FALSIFIZIERT; T2 k=15/25/35 gaps −0.038/−0.050/−0.079 (full-size +0.356 überlebt nicht); T3 EN-Brücke falsifiziert (allein 79.3 % des Inters, aber auf kontaminiertem Set). Tendenz: Artefakt (76.3 % Kontamination ↔ Kollaps).
- Fig8 (`scripts/figures/fig8_lds_decontamination.py`, EN/DE/ZH + CSV, deterministische Snapshot-Werte mit Quellenkommentar): Full vs Structure Null vs Dekontaminiert, ZH-DE-Pfeil +0.47; in `outputs/figures/` + `web/figures/` gespiegelt, portal finding_c eingebettet (figBases-Eintrag), Paper-§3.8-Satz angehängt.
- finding_c umgeschrieben ( statemen→Falsifikation, 3-sprachig) + honesty=T1-Verdict; story RQ1/Fig4-Captions/Tabelle (EN/DE/ZH) + P2→T1; paper/06 Autoren-Sign-offs (94→81 Titel/94 Belege, 6 Verlage→89 Titel, 366/383→367/386 Tabelle+Intro).
- Sensor-Knoten (User-Entscheidung, live außer Video): `physics_em_传感器` (high, ZH/EN/DE, refs NPTEL-syllabus + LEIFI-Induktion + PEP-选必2-Ch5-Katalog, 待核验) + 3 requires-Links → 367/386. Portal `#sources` Physik 81→83 (NPTEL/LEIFI je 1), gesamt 204; cspace/about/story/README/pitch_10min 367/386 bzw. 83-Titel nachgezogen; Hero `1,140+` bleibt (1143, video-konsistent); Video baked 366 eingefroren (SSOT-Vermerk).
- R-Mappings staging (0 €, keine Texte kopiert): `cn_textbook_mapping.json` (7 Bücher × 125 §§, 100 % Node-Hits, 8.8 % uncertain, Lücken: Sensor-3§§/LC-Schwingung/Ölfilm/Korrosion), `open_source_mapping.json` (72/72 Kapitel, Lizenzen 100 %, 17 URLs + 15 Manifest-Zeilen + 3 Exzerpte in Temp), Download-Listen für den User in Temp (`cn_download_list.md`, `en_download_list.md`).
- Compliance-Leitplanke: Ausdruck vs. Fakten-Trennung (nur Fakten extrahieren), kein smartedu-F12-Graubereich, kein LEIFI-Volltext (§44b), Voll-PDFs nie ins Repo, `via/license/note/evidence`-Felder, Eigenständigkeits-Werkzeugkapitel fürs Paper fällig. Chemie-15 + v17-Katalog-Refs bleiben staging bis Textnachweis (keine Wiederholung des Verzeichnis-Fehlers).

## v18b R-Downloads + Backfill (2026-09-12)

- 89 Dateien in `data/textbook/open/` (gitignored): 72 OpenStax-Sektionen Volltext (Chem2e 36: Ch6/7/8/16/17/20/21; UnivPhys2 29: Ch10/13/14/15/16; UnivPhys3 7: Ch10.1-10.7), 2 Voll-PDFs (Phys2 63.8MB verifiziert Faraday/Lenz, Phys3 53.5MB), 8.01-F16-Bundle (64MB/712pp — URL heißt TableOfContents, liefert Full-Notes), 5 MIT-Syllabi/Homepages, 7 Chem-Intros, 2 CN-Klausur-Syllabi (USTC621/UCAS, admin-öffentlich).
- Vol3-Slugs korrigiert (10.4 Nuclear Reactions / 10.5 Fission / 10.6 Nuclear Fusion / 10.7 Medical statt geratenen Titeln); Chem2e-Voll-PDF (218MB) bewusst geskipt → Sektionen; LEIFI/NPTEL link-only; OpenStax-LLM-Training-Vorbehalt in Manifest vermerkt (nur lokales Mapping).
- Backfill: `open_source_mapping.json` + `local_evidence` pro Entry (9/9, 0 missing) + `local_arrivals_20260912`; `data/DATA_MANIFEST.md` 8-Felder-Zeilen; Portal `#sources` + `src_local`-Badge (3-sprachig); CN-PEP-Texte weiter pending (smartedu-Login, User-Aktion).
- Skripte: `fetch_open_texts.py` / `fetch_openstax_sections.py` (mit Marker-Validierung) / `extract_vol3_ch10.py` (superseded, dokumentiert) / `update_mapping_local_evidence.py`.

## v18c CN-PEP-Mirror (2026-09-12, User-Fund)

- Quelle auf User-Hinweis: `github.com/TapXWorld/ChinaTextbook` (Dritt-Mirror, 43GB, provenance unverified; offiziell: smartedu). 7/7 Bedarf-Bücher als "普通高中教科书" (2019) vorhanden, via raw.githubusercontent geladen: Phys 必修3 21.6MB/143pp, 选必1 10.4/130, 选必2 14.3/122, 选必3 12.3/143; Chem 选必1 12.3/139, 选必2 10.5/115, 选必3 15.0/163 (Größen = API-Bytes, vollständig).
- Format: **Scans ohne Textlayer** (264 Bild-XObjects, 0 ToUnicode, 48 Fonts) → OCR pending (keine lokale Engine); Cover + TOC-Seiten visuell verifiziert (2019-Prüfsiegel + PEP-Imprint, 2 Covers vom Modell gelesen).
- Ablage `data/textbook/cn_mirror/` (gitignored, nie committed); Manifest-8-Felder + `cn_textbook_mapping` + `local_evidence` 7/7 (`text_available` bleibt False bis OCR); Portal-`src_local` aktualisiert (3-sprachig).
- Skripte: `fetch_cn_pep_mirror.py` (URL-Encoding-Fix dokumentiert) / `render_cn_covers.py` / `update_cn_mapping_local_evidence.py`.

## v18d GPU-OCR-Vollmenge (2026-09-12, pdf-reading-Skill + DirectML)

- Skill global: `~/.config/opencode/skills/pdf-reading/` (SKILL.md + scripts/pdf_extract.py + pdf_qc.py + QC-CHECKLIST.md + gpu_config.yaml). Engine: RapidOCR ONNX; CUDA-EP scheitert (cublasLt64_13.dll fehlt) → DirectML (flat flags det_use_dml!; nested dicts werden still ignoriert), warm ~0.5s/Seite (CPU 5s), RTX 5060 ~52%.
- 9 Subagents parallel: 7+4=11 CN-Bücher (见DM; 31 Kapitel-txts ~1.55MB, mean conf 0.95-0.985, Census je Buch OK, Front/Back-Matter an Kapiteln vermerkt), MIT-Bundle 712pp (Probe 0.9585, full 0.9512, 0 flagged; Bonus Ch27-29 extrahiert), OpenStax-Re-Verify (Vol2 781pp/1.75M chars, Vol3 597pp/1.39M, alle Keywords hit; USTC/UCAS text_layer OK).
- Scan-Korrektur: Chemie-选必1 hat kein §1.3 — 化学反应的方向 = §2.3 (Mapping repariert, Alter-Eintrag gelöscht). QC-Reports: Temp/opencode/qc_*.md (9x). Offene Reste: resumed pages ohne conf-Werte, 5%-Samples tlw. ungeeyeballt, section-fact-Extraktion → source_references noch fällig.

## v18e R-Grounding (2026-09-12)

- `scripts/ground_refs.py` + `text_grounding_20260912.json` (545KB, tracked): substring-grounding ZH→51 CN-Kapitel, EN→101 OpenStax/MIT-Files. Physik 367: ZH 66.5 % / EN 33.8 %; Chemie 220: ZH 65.9 % / EN 25.5 %; DE = unavailable (LEIFI link-only, ehrlich).
- Lücken-Audit → 4 Bücher nachgeladen (Phys/Chem 必修1/2, +526pp, GPU-OCR 0.95-0.98, 4 Subagents):斜抛/开普勒/宇宙速度 jetzt grounded; Rest = College-Knoten (83, erwartet) + OCR-Varianten + EN-Phrasen-Recall.
- Mapping 7→11 Bücher (4 stubs,节 pending); Manifest + Portal-`src_local` (grounding-Raten, 3-sprachig); Skripte: `ground_refs.py` / `extend_mapping_bx.py` / `fetch_cn_pep_mirror.py` (+4 Jobs).

## v19 P1 EN-Semantik (2026-09-12, Spark statt phi-4)

- Pipeline: `semantic_ground_en.py` (nomic-embed-v1.5 Prefilter top-5, 11.147 Sätze, Cache) smoke 5/5 → `sem_shards.py` (10 Shards à ~40) → 10 parallele Spark-Judges (substantive-description-Regel, passing-mention rejected) → `merge_sem_verdicts.py`.
- Ergebnis `text_grounding_en_semantic_20260912.json` (107KB, 165/407 = 40.5 % strict): Physik-EN 33.8 % → **62.1 %**, Chemie-EN 25.5 % → **53.2 %**; Layer getrennt gebucht (kein Mix mit Substring; reverse: substring 33.8/25.5 vs semantic 62.1/53.2); temp 0, Shards+Verdicts in Temp/sem_shards (reproduzierbar).
- Lokaler phi-4-Pfad verworfen (zu langsam); LM-Studio-Server lief (phi-4-mini + nomic-embed verifiziert), Embeddings wiederverwendet. Portal-`src_local` EN-Raten (3-sprachig); Manifest + Technische-Werkzeuge-Registrierung fällig in P4 (Eigenständigkeit).

## v22-pdf (2026-09-12, 红蓝对抗)
- PDF全量重出：227898B/35页（旧222388B备份_archive）；红方独立提取核对0,934/0,938/0,519、367/386、T1-falsifiziert×17、frozen/forensic同句、LEDGER引用；混用逗号/缺字形记备注不拦路。
- CLOSED 2026-09-12: author roles fixed to dual-team (Rong Lead / Lan Supporting funding+advisory).

## v22-maint (2026-09-12, 红蓝对抗)
- 归档5脚本（-f进仓保provenance）+旧CSV deprecated + manifest三合一（备份→重跑→零漂移，commit=84fb483）+ deploy图补齐20件 + workflow paths + submission 3快照 + 407注释。pre-grounding大备份留磁盘（2.8MB，不进仓）。
- CLOSED 2026-09-12: author roles fixed to dual-team (Rong Lead / Lan Supporting funding+advisory).

## v22-p1 (2026-09-12, 红蓝对抗12/12)
- 366→367六处、89 titles、pitch 556/525、hero=1143、floor三线、人/机后缀、双账脚注、EN层标签、CN 7+4=11、p口径、paper frozen句、§2.2镜像句、MANIFEST 7行+数字修正。红方全过。
- CLOSED 2026-09-12: author roles fixed to dual-team (Rong Lead / Lan Supporting funding+advisory).

## v21-p0b (2026-09-12, 红蓝对抗)
- 接地回写：merge_grounding_back.py→verification 367/367+220/220（有证据302/180，空65/40确为空）；CN 11/11 0 stubs（+60节）；24 zero页verified_blank（重提0成功，空白版权/尾页）。红方全过。
- CLOSED 2026-09-12: author roles fixed to dual-team (Rong Lead / Lan Supporting funding+advisory).

## v21-p0a (2026-09-12, 红蓝对抗)
- 工具披露同步（declaration+code_einreichung+新建CONTRIBUTORS）；submission/README旧数清零；证伪措辞三处+返工（video BAKED-FREEZE声明不改台词、plattform 219、p<0.004记法、§2.2来源）。
- CLOSED 2026-09-12: author roles fixed to dual-team (Rong Lead / Lan Supporting funding+advisory).

## v21-wave2 (2026-09-12, 红蓝对抗)
- scope_note三语367+pending标注；05_conclusion T1收敛5处（L13/L17/L25/9.2 frozen注/L35/L92返工）；evidence C16-C20 + C3/C7/C8降级 + 表头更新；新建compliance_review_response.md（7条：3✅2🟡…R3 teilweise）；chat/emb垃圾确认不存在（红方Test-Path False）。

## v20 基线台账+公式裁决 (2026-09-12, 红蓝对抗)
- 对抗机制：蓝方举证 → 红方9组质询(7致命) → 蓝方作答(8认罚) → 红方复验 → 裁决人终审。红方3"不通过"中2误伤(只搜JSON未查CSV，已纠正)，1成立(6.2逻辑跳跃，已收窄)。
- `docs/BASELINE_LEDGER.md`：8基线四列台账；verified仅§4人机同幅+§8a二元；2a drop；其余needs_review+补实验清单(P0/P1/P2)；精度政策3位+CI；容差三档。
- 公式终审：二元精确复现发表值(裁决人亲跑 `reproduce_lds_binary.py`，log冻结)；三元收窄为as-implemented；`src/scoring.py`加VERDICT注(行为不动)；Fig2重画二元+三语脚注；portal公式卡改回二元；paper §2.7改为Verdict注。
- 附带：`outputs/physics_{comparison,cognitivespace}.json` v18漏提交的367/386本次收齐(physics_full.json实测367概念/386关系)；portal ZH字典区历史mojibake(HEAD既有)记P1，不在本轮修。
- Fig3破案 CLOSED (Wave 2 W2.1, 原因找到→不删除)：middle 46/280→0.271、high 175/1113→0.073（无向密度唯一命中）；源头 eeca788/2ffd963/763b836（2026-06-21/22）；稠密管线已丢失（574→556/3375），16+96穷举无命中；Option 1落地（portal三语+story+assert信息）。
- Fig5立案 CLOSED (Wave 2 W2.2, 同政策→不删除)：`docs/fig5_hds_forensic.md`新建；4阶段拼合史（eeca788定义/2ffd963 max7+mean0.40/8ad379a 459/897f04e max8+0.4029+3538/0962982 556分母）；丢失556/525一致ID图（merged-557+6悬空边为残骸，最接近460/7/0.27）；`6f1d5b2`事故覆盖math节（发表JSON仅存于6f1d5b2^）；脚注portal finding_b三语+story F7/fig5_caption三语；story stale 64%→60%顺手修复；paper表为发表态，披露由取证注承担。

## v19 P2/P3/P4-Abschluss (2026-09-12，续)
- P2 QC-closure: `--pages`-Modus in skill-`pdf_extract.py` (+ Manifest-Merge, `pdf_qc.py` ignoriert skipped/-1) → `conf_backfill.py`: 101 Seiten nachgeholt, **-1 = 0, 1481 Seiten, 27 flagged (alle belegt blank/cover), mean conf 0.9665**; Visual-Closure: 2 Seiten vom Modell gegengeprüft (xb2-p60 Sinus-Wechselstrom, bx1-p28 Redox — Schlüsselterme im OCR verifiziert); `render_qc_sample.py`.
- P3 chem-15: `status = staging-confirmed-2026-09-12` + deutsches Verdict (kein zweiter Verzeichnis-Fehler); physics-10-Elementar-Refs als Konvention vermerkt.
- P4a Glossar-9: Portal Methodik-`<details>` (EN/DE/ZH, 11 keys × 3) + Paper §2.11 + §2.12 Technische Werkzeuge (Eigenständigkeit-Fix: NetworkX/3d-force-graph/matplotlib/RapidOCR/nomic/Spark-Adjudikation/qwen-plus offengelegt).
- P4b Fig2: `fig2_lds_flow.py` (Subagent, scoring.py-L119-treu: 3 Komponenten, LCD = Alias) EN/DE/ZH + web-Spiegel + `figBases`-Eintrag + Portal-Einbettung; LDS-Formelkarte korrigiert (2→3 Komponenten).
- P4c Fig3-Forensik: `fig3_forensic.py` + CSV (16 Zeilen): 0.271/0.073 unter keinem Archiv-Setup reproduzierbar (Snapshot 0.0038/0.0025; requires 0.0328/0.0180) → frozen + `docs/fig3_cds_forensic.md` mit 3 Optionen (User-Entscheidung fällig, keine stille Claim-Änderung).
- Inkonsistenz gefunden & dokumentiert (statt vertuscht): Paper §2.7 frozen-v3 (2 Komponenten) vs Code+methodology.md (3) → Paper-Fußnote in §2.7.
