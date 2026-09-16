# Enforcement — 按 debate_verdict_20260914 6裁决执行归档守卫（2026-09-14）

> 基地：`C:\Users\rongj\Desktop\学校\BWKI-2026-备战`
> 裁决源：`research/debate_verdict_20260914.md`（§议题1-6 + L126-135一览）· 冻结源：`research/checkpoint_20260914.md` §3/§4 · `research/baseline_board.md` A/B · `research/gold_freeze_2026-09-14.md` · `research/gold_deconfound_2026-09-14.md:103-111` · `research/tier2_emb_baseline.md` · `research/rsa_bridge.md` · `docs/fig3_cds_forensic.md` · `docs/fig5_hds_forensic.md` · `docs/BASELINE_LEDGER.md` · `docs/evidence_register.md`
> 执行范围：只新增本文件；无必要edit则零改动；禁区不动（`tests/ data/lds_c/llm_subject/ linguaGraph.db freeze/ _deploy/ _archive/ sync_readmes.py` + PII/API-Key/版权教材原文）；不打tag（`v1.0-bwki-submission`按checkpoint §6待平台录入后）。

## 守卫动作1 · 0.519/PEP归档项：裸收敛句核查

- 命令：`rg -n "konvergiert erheblich" --glob '!_deploy/**' --glob '!.git/**'` → **0命中（NOTFOUND）**。
- 结论：正文已无 `ZH-DE konvergiert erheblich` 裸句，无需改限定。
- 残留限定式措辞（均带证伪句同段，不触发edit）：
  - `README_DE.md:185` F4 `ZH-DE (0,519) konvergiert … aber Nullmodell (F5) falsifiziert … Alignierungs-Artefakte` + `README_DE.md:195` T1 `167/219 → 0,52→0,99 falsifiziert` + `README_DE.md:70` T1同段。
  - `README.md:82` T1 `167/219 → 0.52→0.99 label artefact` + `README.md:101-102` Fig8 frozen `0.9336/0.9382/0.5188`。
  - `cognitive-space/portal/index.html:783-784` Finding C `look more convergent … collapses to 0.990 once 167/219 removed: label artifact`（`_deploy`镜像同文，禁区不动）。
  - `cognitive-space/web/story/index.html:1028` Abb4 `ZH–DE konvergiert (0,519) … T1-Dekontamination falsifiziert (0,52→0,99)`——缺size-match句，按裁决不得升为headline，仅附录反例位。
- `narrative_fix_skipped.md`：本次新增0条（仍 `0/33`，见该文件L9-11）；ARCHIVE_POLICY类C（L48-50）要求跟踪文件不手改，缺size三件套处只登记不补。

## 守卫动作2 · 0.939暂缓项：hero核查

- Hero实现PASS：`cognitive-space/portal/index.html:347` hero stat = `0.881 Overall F1 (weighted)`，无单写0.939 hero。
- 并列合规：
  - `cognitive-space/portal/index.html:386` contrib1 `DB-path 0.939† + harness ~0.65 + weighted 0.881`；`:417` GL `F1 0.939† Developing social 0.881 overall`；`:1038-1040` 社会行`0.939† Developing (DB-path; harness ~0.65)` + 加权行`0.881`；`:1055` †注。
  - `README.md:81` + `:98`（`0.939† n=72 Developing + 0.674 n=20 + 0.881 + harness ~0.65 vs DB 0.939`）；`README_DE.md:92` + `:109`同式；`docs/evidence_register.md:22` C9b Developing。
- 文档瑕疵只登记不改：`cognitive-space/portal/README.md:13` Hero描述仍写 `(1,143 concepts, F1=0.939† Developing social)`，与实现0.881不一致。按`research/ARCHIVE_POLICY.md:48-55`类C只登记不补，本次不edit，待源重镜时同批修。

## 6裁决执行表

| # | 议题 | 裁决 | 平台是否可登记 | 证据行号 |
|---|---|---|---|---|
| 1 | 0.519 收敛 | **归档** | 否（headline/hero/结论禁入；仅方法附录/P2-Recheck反例警示，三件套并列时可注） | verdict L22-25,L130；checkpoint L35,L45-49；baseline L17,L20；evidence C3:15+C16:29；README_DE:185,195；README:82,101-102；portal:783-784 |
| 2 | 0.939 headline | **暂缓** | headline只许`0.881`；社会须`0.939†(n=72,Developing,blind pending,DB-path特值)+harness ~0.65`同页并列；G2前禁Mature/hero单写/绝对值选型 | verdict L41-44,L131；checkpoint L36-37,L51-55；baseline L35-38；gold_freeze L8-9,L16-17；deconfound L105-111；portal:347,386,417,1038-1040,1055；README:81,98；C9b:22 |
| 3 | HDS≤8 | **可写（限定）** | 是（描述性+冻结注；禁universal law/定论；因果归F10假设） | verdict L60-63；fig5 L3 claim `max8/mean0.40/459roots83%`，L37-40 frozen+footnote；evidence C2:14+C20:33；checkpoint L38 |
| 4 | 学段切分CDS | **可写（描述性限定）** | 是（描述性+无CI注；化学`consistent with, not confirming Δ=0.012`；禁因果/治理外推+frozen注） | verdict L79-82；fig3 L34-36 `46/280→0.271,175/1113→0.073`，L51-53 Option1已实施；evidence C1:13+C20:33；README_DE:182-183,188 |
| 5 | PEP镜像 | **归档+暂缓** | 镜像永不进仓/不出处栏（指smartedu官方）；CS治理归因仅假设（Q2假设句+粒度混杂注可登）；Q1/Q3缺口注可登；官方本重采列Future | verdict L98-102；DATA_MANIFEST L57 `永不进仓·以smartedu官方本为准·7mapped+4stubs`+L58 link-only；paper02:34 `Drittspiegel provenance unverified nie committed`，02:214+04:70+05:26,52粒度+假设；portal:349 scope `1 pending sensor`，811-812假设句，949粒度`CN87/US2124/NRW299`；checkpoint L74-81 |
| 6 | Tier2否决权 | **可写（守卫）** | 守卫规则本身可登方法（§8.10-8.16+rsa_bridge）；触发否决结论`offen`归档不可登结论/平台；Tier2基线仅复用基线，`--full`前不升主证据 | verdict L118-122；rsa_bridge L59 `<50 unresolved`，L52 `perm≥1000`，L65-66 size反转否决，L71 `CLOSED三合一否则offen`；tier2 L29 `407/165`，L36-37 `62.1%/53.2%`；baseline B L30-33 blocked+L35-38；checkpoint §4 R3-R5 |

## 平台口径（一句话）

- Q headline：`0.881`；社会行：`0.939† Developing n=72 blind pending DB-path（harness ~0.65）`；收敛句：不填；HDS/CDS：填限定版+冻结/无CI注；CS 12.7%-95.4%：填`测量强、治理归因仅假设+粒度混杂CN87/US2124/NRW299`；出处栏：第三方PEP镜像不填，填smartedu官方渠道+`7 mapped+4 stubs / 1 pending sensor`缺口注；Tier2：填守卫规则，不填被否决绝对值。

*执行人：归档守卫 · 2026-09-14 · 本次写盘仅本文件；grep/hero证据如上；未动禁区，未打tag。*
