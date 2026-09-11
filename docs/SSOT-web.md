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
| 5 | Paper-Karten | 56 KB · 19+ refs | **153 KB md · 293 KB PDF · 54 refs** | gemessen (`docs/paper/`, `docs/submission/`) |
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
