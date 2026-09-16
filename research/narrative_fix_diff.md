# T1 narrative_fix_diff — 只读扫描，不改原文

> 基地 `C:\Users\rongj\Desktop\学校\BWKI-2026-备战` · T1 只写本文件，不改原文，不碰 `tests/data/lds_c/llm_subject/linguaGraph.db`，不打 tag。
> 扫描范围：`docs/paper/00_three_conclusions.md, 03_results.md, 04_discussion.md, 02_related_work.md, 02_methodology.md, cognitive-space/portal/index.html, cognitive-space/web/story/index.html`
> 目标类型：裸 `0.519` / `converge|konverg` / `proves|beweist|Beweis` / `first|erste` / `universal|universell|universally` / `validated|validiert` / 裸 `0.939` / `GED三元` / `融合|Fusion`
> 替换措辞受控词表：`T1-falsifiziert` / `Preliminary` / `Developing四件套(machine-seeded/human-accepted + same-source + harness~0.65 + Blind-Review ausstehend)` / `frozen v3 (2-Komponenten-Jaccard, `scripts/figures/_lds_utils.py::lds_jaccard`, Fig4-Freeze ZH-EN 0.9336/DE-EN 0.9382/ZH-DE 0.5188)`
> 判定：`删` = 整句删除；`加限定` = 保留主句+强制限定从句；`降级` = 强词换弱词 (proves→shows/suggests, universal→sample-limited pattern, validated→checked/Preliminary)。
> `GED三元` 说明：7 文件内唯一 GED 提及是 `02_methodology.md:151` 自带 frozen-限定（3-Komponenten-Variante intractable/Fallback 0.5，不复现已发表值，2-Komponenten frozen v3 为准）——已合规，不计入条数，不另开条。

格式：`文件:行号｜原文摘｜判定｜替换措辞`

---

## N01 — docs/paper/00_three_conclusions.md:14｜universal + Konvergenz｜降级+加限定
- 原文摘：`Diese Konvergenz deutet auf eine universelle Eigenschaft der pädagogischen Wissensorganisation hin`
- 判定：降级 + 加限定
- 替换措辞：`Diese Übereinstimmung (Preliminary, nur Mathe/Physik-Lehrbuchgraphen, CDS-Ebene) deutet auf ein sample-begrenztes Muster hin — keine universelle Eigenschaft; Replikation in weiteren Fächern/Sprachen ausstehend.`

## N02 — docs/paper/00_three_conclusions.md:26｜universal heading｜降级
- 原文摘：`## Schlussfolgerung 2: Die Wissenstiefe hat eine universelle Obergrenze`
- 判定：降级
- 替换措辞：`## Schlussfolgerung 2 (Preliminary, frozen sample): Beobachtete Tiefenobergrenze HDS ≤ 8 (Mathe max 8 / Physik max 6)`

## N03 — docs/paper/00_three_conclusions.md:44｜konvergieren heading (T1-falsifiziert fehlt)｜加限定
- 原文摘：`## Schlussfolgerung 3: Lehrbuchwissenschaftliche Strukturen konvergieren sprachübergreifend`
- 判定：加限定
- 替换措辞：`## Schlussfolgerung 3: Scheinbare ZH-DE-Ähnlichkeit (LDS-K 0.519) — T1-falsifiziert als Label-Artefakt (0.52→0.99, Fig. 8); ΔLDS isoliert … (Ebenen-getrennt, Preliminary)`

## N04 — docs/paper/00_three_conclusions.md:47｜裸0.519 + systematisch ähnlicher｜加限定
- 原文摘：`ZH-EN: 0,934 < 0,957; DE-EN: 0,938 < 0,957; ZH-DE: 0,519 < 0,717 … systematisch ähnlicher als randomisierte Graphen`
- 判定：加限定
- 替换措辞：`… (frozen v3, Full vs. Structure Null) — Lesart T1-falsifiziert: ZH-DE 0.519 kollabiert nach Entfernen CJK-kontaminierter de-Labels (167/219) auf 0.990 (J_node 0.556→0.020); kein Beleg inhaltlicher Konvergenz.`

## N05 — docs/paper/00_three_conclusions.md:50｜bemerkenswert ähnlich + Konvergenz deutet｜降级+加限定
- 原文摘：`sind … bemerkenswert ähnlich … Diese Konvergenz deutet darauf hin, dass die mathematische Voraussetzungslogik … dominiert`
- 判定：降级 + 加限定
- 替换措辞：`erscheinen … oberflächlich ähnlicher als gradrandomisierte Graphen (T1-falsifiziert, s. N04) … Dies ist mit geteilter Gradstruktur vereinbar (Preliminary), kein Dominanz-Beweis.`

## N06 — docs/paper/00_three_conclusions.md:75｜universal + bemerkenswerte Konvergenz｜降级+加限定
- 原文摘：`respektieren eine universelle Tiefengrenze und zeigen … bemerkenswerte strukturelle Konvergenz über Sprachen hinweg auf Lehrbuchebene`
- 判定：降级 + 加限定
- 替换措辞：`zeigen im frozen sample HDS ≤ 8 und eine scheinbare Lehrbuch-Ähnlichkeit (T1-falsifiziert als Alignierungs-/Größen-Artefakt, P2-Recheck; Details `docs/p2_methodology_rechecks.md`).`

## N07 — docs/paper/03_results.md:60｜sprachunabhängige Invarianten｜降级
- 原文摘：`dass die zugrundeliegende mathematische Wissensstruktur sprachunabhängige Invarianten besitzt`
- 判定：降级
- 替换措辞：`dass Nachbarschaften über Sprachen hinweg teilweise überlappen (deskriptiv, Preliminary) — kein Invarianz-Beweis; Alignierungsabhängigkeit (P2) vorbehalten.`

## N08 — docs/paper/03_results.md:97｜konvergieren (nackt)｜加限定
- 原文摘：`Dies bedeutet, dass Lehrbuch-Wissensstrukturen über Sprachgrenzen hinweg konvergieren`
- 判定：加限定
- 替换措辞：`Full < Structure Null (frozen v3) — Lesart T1-falsifiziert: scheinbare ZH-DE-Ähnlichkeit 0.519→0.990 nach Dekontamination; kein Konvergenz-Beleg.`

## N09 — docs/paper/03_results.md:99｜universell + isoliert｜降级
- 原文摘：`von universeller mathematischer Prerequisite-Logik geteilt … der den sprachspezifischen Anteil … isoliert`
- 判定：降级
- 替换措辞：`von geteilter Gradstruktur (Preliminary) … ΔLDS = LDS-C − LDS-K zielt auf den kognitiven Anteil jenseits der Lehrbuchstruktur (Ebenen-getrennt, Preliminary, keine kausale Isolation).`

## N10 — docs/paper/03_results.md:105｜systematisch/kein Artefakt/Relationenstruktur｜加限定
- 原文摘：`Die ZH-DE-Konvergenz (0.52 im Pool) ist systematisch über alle vier Bildungsebenen … Sie ist kein Artefakt … zeigt sich auch in der Relationenstruktur`
- 判定：加限定
- 替换措辞：`Die nominelle ZH-DE-Zahl (0.52, frozen v3) liegt in allen vier Ebenen unter den EN-Paaren — T1-falsifiziert: nach CJK-Dekontamination + Size-Matching (k=15–35) kehrt sich der Wiki-Vergleich um; kein Konvergenz-Beleg (Fig. 8).`

## N11 — docs/paper/03_results.md:200｜strukturell konvergenten Lehrbuchgraphen｜加限定
- 原文摘：`Artefakt des Vergleichs zwischen spärlichen Menschengraphen und dichten, strukturell konvergenten Lehrbuchgraphen`
- 判定：加限定
- 替换措辞：`Artefakt des Vergleichs spärlicher Menschengraphen mit dichten Lehrbuch-Alignierungs-Labels (deren nominelle ZH-DE-Ähnlichkeit T1-falsifiziert ist, 0.52→0.99).`

## N12 — docs/paper/03_results.md:320 + :324｜Design-Effekt-Beweis (Beweis)｜降级
- 原文摘：`### 5.9 Design-Effekt-Beweis …` / `**5.9.1 Design-Effekt-Beweis: gleiche Signalamplitude …**`
- 判定：降级
- 替换措辞：`### 5.9 Design-Effekt-Vergleich (Konsistenz-Demonstration, kein Kausalbeweis) …` / `**5.9.1 Design-Effekt-Vergleich (Preliminary): gleiche Signalamplitude …**`

## N13 — docs/paper/03_results.md:381｜Institutionelles Wissen konvergiert｜加限定
- 原文摘：`Institutionelles Wissen konvergiert primär in der Konzeptwahl (Knoten)`
- 判定：加限定
- 替换措辞：`Alignierungs-Labels stimmen nominell stärker überein (node-only 0.444, frozen v3) — P2/T1: kein belastbarer inhaltlicher Befund (de-Feld teils chinesisch; Size-Matching kehrt Muster um).`

## N14 — docs/paper/04_discussion.md:28｜universelle Eigenschaft｜降级
- 原文摘：`könnte es eine universelle Eigenschaft der mathematischen Lehrplangestaltung widerspiegeln`
- 判定：降级
- 替换措辞：`könnte es ein Muster der untersuchten STEM-Lehrbuchgraphen (ZH/EN/DE, Preliminary) widerspiegeln — kein Universalitäts-Anspruch.`

## N15 — docs/paper/04_discussion.md:43｜stärker konvergieren als Zufall｜加限定
- 原文摘：`sind die randomisierten Graphen systematisch unterschiedlicher … Lehrbuchwissensstrukturen stärker konvergieren, als der Zufall vorhersagen würde`
- 判定：加限定
- 替换措辞：`Full < Structure Null (frozen v3, deskriptiv) — Lesart T1-falsifiziert (0.52→0.99); kein Konvergenz-Beleg.`

## N16 — docs/paper/04_discussion.md:45｜universell ist｜降级
- 原文摘：`weil mathematische Voraussetzungslogik universell ist`
- 判定：降级
- 替换措辞：`weil die Gradstruktur in den untersuchten Lehrbuchgraphen geteilt ist (Preliminary, frozen sample).`

## N17 — docs/paper/04_discussion.md:47｜bedeutsam + bemerkenswert konvergent + unabhängig｜加限定+降级
- 原文摘：`ist der hier erzielte Befund stärker — auch die organisatorischen Strukturen … sind … bemerkenswert konvergent. Drei … produzieren unabhängig voneinander …`
- 判定：降级 + 加限定
- 替换措辞：`deskriptiv: nominelle ZH-DE-Ähnlichkeit unter Structure-Null-Erwartung (frozen v3) — T1-falsifiziert als Label-/Größen-Artefakt; kein Stärkebeweis, keine Unabhängigkeits-Aussage über Bildungstraditionen.`

## N18 — docs/paper/04_discussion.md:49｜universell + genuines Sprachsignal isolieren｜降级
- 原文摘：`von der universellen Logik … Um ein genuines Sprachsignal zu isolieren, müssen wir …`
- 判定：降级
- 替换措辞：`von geteilter Gradstruktur (Preliminary) … Um einen kognitiven Anteil jenseits der Lehrbuchstruktur zu schätzen (ΔLDS, Ebenen-getrennt, Preliminary) …`

## N19 — docs/paper/04_discussion.md:168｜裸0.519 partielle Konvergenz｜加限定
- 原文摘：`ZH-DE (0,519) liegt im Bereich der „partiellen Konvergenz" — deutlich unter den Nullenwartungen`
- 判定：加限定
- 替换措辞：`ZH-DE nominell 0.519 (frozen v3) — T1-falsifiziert (dekontaminiert 0.990; Size-Matching kehrt Wiki-Vergleich um); nicht als Konvergenz-Evidenz werten (Fig. 8).`

## N20 — docs/paper/04_discussion.md:198｜konvergieren erheblich｜加限定
- 原文摘：`einige Sprachpaare konvergieren erheblich (ZH-DE), während andere auf Rauschniveau liegen`
- 判定：加限定
- 替换措辞：`nominelle ZH-DE-Ähnlichkeit (0.519, T1-falsifiziert als Label-Artefakt), EN-Paare auf Rauschniveau (0.934/0.938 ≈ Boden).`

## N21 — docs/paper/04_discussion.md:210｜Design-Effekt-Beweis (Beweis)｜降级
- 原文摘：`Präzisierung des Design-Artefakts (Design-Effekt-Beweis, §5.9.1–5.9.2)`
- 判定：降级
- 替换措辞：`Präzisierung des Design-Artefakts (Design-Effekt-Vergleich: Exklusion + Konsistenz-Demonstration q=0.30, keine quantitative Kausalzuordnung, §5.9.1–5.9.2)`

## N22 — docs/paper/02_related_work.md:19｜first/erste｜降级
- 原文摘：`LinguaGraph ist nach unserem Kenntnisstand das erste System, das diese Curriculumsstandards in strukturierte Wissensgraphen … überführt`
- 判定：降级
- 替换措辞：`LinguaGraph überführt … (Preliminary, Stand Sept. 2026, ohne systematischen Prior-Art-Vergleich — kein First-Nachweis).`

## N23 — docs/paper/02_related_work.md:41｜55 Messungen/breit reproduzierbar (Zahl+Stärke nackt)｜加限定
- 原文摘：`die Replikation über 55 Messungen (§5.10) zeigt, dass die strukturelle Divergenz … breit reproduzierbar und kulturell gerichtet ist`
- 判定：加限定
- 替换措辞：`die Replikation (59 Messungen / 54 Identitäten, §5.10, Verfügbarkeitsstichprobe, keine Mehrfachtest-Korrektur) zeigt: ZH-DE 59/59 signifikant, 9/177 EN-Tests n.s. (R1/Distill) — Richtung Preliminary, modell-/paarabhängig.`

## N24 — docs/paper/02_related_work.md:59｜validierten Metriken｜降级
- 原文摘：`mit validierten Metriken, die Unterschiede … erfassen`
- 判定：降级
- 替换措辞：`mit frozen-v3-Metriken (Preliminary; Gold Developing C9b, s. §2.8/§8.7), die … schätzen`

## N25 — docs/paper/02_methodology.md:60-62 + docs/paper/03_results.md:12｜Fusion/Fusionsprozess (融合 nackt)｜加限定
- 原文摘：`### 2.4 Graphkonstruktion und -fusion` / `Die Roh-Extraktionen durchlaufen einen mehrstufigen Fusionsprozess` / `Die Extraktion und Fusion der 68 Lehrbücher ergibt …`
- 判定：加限定
- 替换措辞：`### 2.4 Graphkonstruktion und -zusammenführung (Alignierungs-Labels, P2-vorbehalten)` / `… mehrstufige Zusammenführung (Dedup + Alignierung; Mathe-Knoten = Alignierungs-Labels, de-Feld teils CJK-kontaminiert, T1-falsifiziert) …`

## N26 — docs/paper/02_methodology.md:180｜F1 ≥ 0,88/weit übertreffen/hoch einzustufen (validiert-Ton, harness fehlt)｜降级
- 原文摘：`alle drei Sprachen erreichen F1 ≥ 0,88 … die das Qualitätsziel … weit übertreffen … als hoch einzustufen`
- 判定：降级
- 替换措辞：`DB-Pfad nominell F1 ≥ 0,88 (Developing C9b; Developing四件套; harness-reberechnet ~0,65) — Preliminary, kein Validierungs-Beleg; bis Blind-Review nur als Arbeitshypothese.`

## N27 — cognitive-space/portal/index.html:360 (+ i18n :1515/:1889/:2015)｜bare 0.519 converge｜加限定
- 原文摘：`LDS-K reveals heterogeneous …: ZH-DE (0.519) textbooks converge substantially`
- 判定：加限定
- 替换措辞：`LDS-K nominell ZH-DE 0.519 (frozen v3) — T1-falsifiziert als Label-Artefakt (0.52→0.99, Fig. 8); EN-Paare ≈ noise floor. Core signal: ΔLDS (Preliminary, Ebenen-getrennt).`

## N28 — cognitive-space/portal/index.html:386/:417/:1528 (+ story :313)｜validated + 裸0.939｜降级
- 原文摘：`validated against 92 gold-standard annotations (social F1 = 0.939† Developing …)` / `GL[92 Gold Labels<br/>F1 0.939† social 0.881 overall]`
- 判定：降级
- 替换措辞：`checked against Preliminary gold (92: 20 hand C9a + 72 machine-seeded/human-accepted C9b Developing; DB-path 0.939†, harness ~0.65, blind audit pending; weighted 0.881) — no validation claim.`

## N29 — cognitive-space/portal/index.html:401/:1705 + :761｜density universals + universal upper bound｜降级
- 原文摘：`12 findings spanning density universals (F1–F3, F6–F8)` / `Educational knowledge has a universal upper bound … regardless of discipline`
- 判定：降级
- 替换措辞：`12 findings spanning density patterns in the STEM sample (Preliminary, frozen graphs) …` / `In the frozen sample, prerequisite depth is bounded (math ≤ 8, physics ≤ 6, Preliminary) — no universal claim.`

## N30 — cognitive-space/portal/index.html:783/:794 + i18n :1539/:1913/:2039｜shows convergence + proves/beweist/证明｜降级+加限定
- 原文摘：`Textbook LDS-K shows convergence (ZH-DE 0.519 …)` / `Textbook structures converge more than random expectation` / `A Null Model proves Full < Structure Null` / `Ein Null-Modell beweist …` / `Null Model 证明 …`
- 判定：降级 + 加限定
- 替换措辞：`Textbook LDS-K nominell ZH-DE 0.519 (frozen v3) — T1-falsifiziert (0.52→0.99 label artifact)` / `Full < Structure Null, deskriptiv (Preliminary)` / `A Null Model shows Full < Structure Null (descriptive, Preliminary, T1-falsified reading)` (+ DE/ZH 同步降级 `zeigt`/`显示为描述性差异`).

## N31 — cognitive-space/portal/index.html:1033/:1038/:1055 + story :515/:527｜Human-annotated + Validated + 表格裸0.939｜降级
- 原文摘：`Human-annotated gold standard … Validated against production-model extraction` / 表格 `Social Concepts … 0.939 … 72`（表内无 Developing/harness）
- 判定：降级
- 替换措辞：`Mixed-provenance gold (20 hand C9a + 72 machine-seeded/human-accepted C9b, Developing; harness ~0.65) checked against extraction (Preliminary)`；表格 `0.939` 改为 `0.939† Developing (DB-path; harness ~0.65)` 并链 `research/gold_deconfound_2026-09-14.md`。

## N32 — cognitive-space/web/story/index.html:435/:732｜Validated (against curricula / core hypothesis)｜降级
- 原文摘：`Validated against 4 national curricula` / `Validated the core hypothesis that cross-language knowledge structures measurably differ`
- 判定：降级
- 替换措辞：`Compared against 4 national curricula (coverage: keyword bridge + 2-overlap, Preliminary)` / `Explored whether cross-language structures differ (pilot, Preliminary — no validation claim).`

## N33 — cognitive-space/web/story/index.html:637/:686/:747 (+ i18n :955/:1031)｜universal / holds universally / Confirmed universal｜降级
- 原文摘：`STEM density pattern is universal` / `The … pattern holds universally` / `Confirmed universal STEM density pattern (F8)`
- 判定：降级
- 替换措辞：`STEM density pattern in the 3-subject sample (Preliminary, frozen graphs)` / `… holds in the frozen 3-subject sample (Preliminary, no universal claim)` / `F8 pattern observed in the sample (Preliminary).`
