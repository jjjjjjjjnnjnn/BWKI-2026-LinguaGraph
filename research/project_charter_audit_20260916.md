# Project Charter Audit (retrospective) — LinguaGraph BWKI 2026

Date: 2026-09-16 | Scope: retrospective against frozen submission materials only, no new claims
Sources: `docs/submission/README.md`, `submission/final/README.md`, `docs/submission/plattform_antworten.md`, `submission/final/plattform_antworten.md`, `docs/submission/einreichung_checkliste.md`, `docs/submission/feld_mapping.md`, `docs/submission/declaration_of_support.md`, `docs/submission/code_einreichung.md`, `docs/submission/BASELINE_LEDGER.md`, `docs/paper/01_abstract_introduction.md`, `CONTRIBUTORS.md`, `research/numbers_ssot_20260916.json`, quota evidence in `research/red_attack_v2_20260914.md`, `research/blue_defense_v2_20260914.md`, `docs/session_handoff_20260915_v28.md`, `docs/session_handoff_20260916_v36.md`

## 1. 资格 (Eligibility — only as stated in materials)

- Wettbewerb: Bundeswettbewerb Kuenstliche Intelligenz 2026 (BWKI 2026). Einreichsprache Deutsch. Frist 20.09.2026.
- Teamform (per `declaration_of_support.md` S0/S4, `CONTRIBUTORS.md`, README header): 2 Schueler — Jiajun Rong (Lead: Forschung, Implementierung, alle Analysen); Zhenxi Lan (Supporting: Finanzierung & Beratung). Keine externen Forschungskooperationen; Schule (deutsches Gymnasium) stellt nur Rahmen, keine inhaltliche Einwirkung.
-赛道细分缺项声明: materials state "BWKI 2026" but do NOT name a track/sub-category (e.g. Einzel vs Gruppe) nor age-class proof. Record as MISSING formal item; team size = 2 per above, do not infer track name.
- Eigenstaendigkeit: core (Fragestellung, Design, LDS-Definition, Erhebung, Interpretation) per S0 as Schueler-Eigenleistung; all assistance disclosed in declaration S1-S5.

## 2. 预算 (Budget — zero/external-funding statement)

- Per declaration S5 + code guide S3: lokale CPU + Drittanbieter-LLM-APIs; keine externe GPU.
- Abrechnungslage per declaration S5/S5.1: opencode GO nutzungsbasiert; DashScope Freibetrag (+ ein Sperrvorfall 2026-08-10: versehentlich nicht-kostenfreies Modell, Kontosperrung wegen Zahlungsrueckstand, same-day fix auf Freibetrag-Modelle, Daten verifiziert, Validitaet nicht beeintraechtigt); OpenRouter kostenlose Stufe; opencode zen/v1 kostenlose Stufe. Rolle "Finanzierung" bei Zhenxi Lan (no amount stated).
-声明: no separate budget sheet found in submission materials; interpreted as zero-budget/self-funded + free-tier. Formal budget table with amounts: MISSING (declared as such, amounts not invented).

## 3. 团队能力 (Capacity as evidenced)

- Lead covers full pipeline: `scripts/lds_c_*.py`, `scripts/lds_k_*`, figures, LMM, null models; Supporting covers funding & advisory.
- Tooling disclosed (declaration S2, CONTRIBUTORS): Claude Code (coding/analysis/docs), NetworkX, 3d-force-graph, matplotlib, pymupdf+RapidOCR, nomic-embed-v1.5 + Muse-Spark adjudication, qwen-plus extraction (Gold N=92).
- Quality gates: 84 pytest (mocked, no API keys), fixed seeds, dated JSON with provenance block, SSOT `manifest.json` 556/517/219, PDF rebuilt via `scripts/build_paper_pdf.py`.
- Limit honestly stated: Extraktionsqualitaet domaenenabhaengig (sozial F1 0.939 Developing C9b, Mathe-DE ~0.51); Kleinstmodell-Kette bricht bei Extraktion.

## 4. 风险预案 (Risks + instantiated quota-wall downgrade path)

| Risk | Mitigation / Status |
|---|---|
| Video groesster Restposten | Skript+Storyboard fertig; 4K-Master+subs vorhanden 09-12; Narrativ-Abgleich vs v26 offen |
| Plattform-Felder weichen ab | Feld-Mapping <=1700 Zeichen; Abgleich bis 9/13 offen |
| API-Quota West-Replikation | Geloest (v0.14.0 NIM+Cohere+Kilo+Terminal, 59 Messungen) aber neue Quota-Wand 2026-09-15/16 dokumentiert, siehe unten |
| DashScope Sperrvorfall | Offengelegt S5.1, auf Freibetrag umgestellt |

Quota-wall downgrade path (already instantiated, not hypothetical):
- ds-pro: `ensemble_v2/deepseek-v4-pro-0813/_manifest.json` calls=100, done 3, missing 60, failed 49; quota_note: FREE_QUOTA_EXHAUSTED_403 AllocationQuota.FreeTierOnly verified by direct probe 2026-09-15; all 49 HTTPError consecutive after first OK; genuine_failed_hint=[]. v36 handoff 2026-09-16: P0-a ds-pro single-probe still 403, 53 items HOLD, zero calls.
- v41flash: Chinese block missing (66), breadth probes 9/9 403; kimi-k3 tail 8 quota + 3 genuine; max/max-0902 cap100 truncation.
- mimo/bailian absence: consensus v2/v3/v4 — mimo depth 24/24 in-scope but bailian `*.bailian.json` 0 (v2) to 62 absent (missing not scored); absence never scored as 0.
- Enforced downgrade language (red/blue verdicts): "residual matrix / quota-truncated snapshot" only; ds-pro F1 0.065 ruled harness-incompatible (86/92 empty content, reasoning_content not wired) = unmeasurable, not capability; no model ranking across harness confounds; no canonical-set claims before P1-P3 closure. This is the live fallback: report survivors descriptively, keep missing/failed split, ban headline use.

## 5. 假设/样本/主要结局三行锁定 (pre-registration lite)

- H (Annahme): ZH/EN/DE organisieren Wissen systematisch unterschiedlich; LLM-extrahierte Graphen + LDS koennen das messen (Leitfrage README + Paper S1.2, drei Teilfragen Drift/Validitaet/Stabilitaet).
- S (Sample, frozen): Human Between-Subject N=15 (6 DE / 6 ZH / 3 EN) + Pilot N=8 (zh-only, superseded, nicht repliziert) + LLM-as-Subject within-subject 59 Messungen / 54 Modelle (publiziert; file truth 62/57/186 inkl. qwen-max n=26/30 parked). Target 30 (10/Sprache) per ParticipantManager not reached for human arm.
- E (Primary endpoint): Delta-LDS = LDS-C minus LDS-K > 0. Frozen read: F11 human between falsifiziert Delta-LDS > 0 (LDS-C 0.93-0.96 ~= Split-Half-Boden 0.92-0.96); F12 LLM-within signal +0.08-0.09 ueber Boden (0.85-0.87), alle ZH-DE p<0.05 (p=0.0 als p<0.004), 9 EN-Paare n.s.; LDS-K ZH-DE 0.519 (frozen binary). Margin >=0.10 / Youden 0.12 heuristic only, nicht validiert (LEDGER S9 needs_review).

## 6. 形式审查checklist (per einreichung_checkliste.md Stand 2026-09-16 v21)

Dokumentation:
- [x] `submission/final/plattform_antworten.md` final drafts
- [ ] Plattform-Felderabgleich + Anpassung bis 9/13 — OPEN
- [x] declaration_of_support.md v2.0
- [x] CONTRIBUTORS aktualisiert

Code:
- [x] Pipeline reproduzierbar (84 pytest, code guide)
- [x] Datasets/Modelle/Frameworks offengelegt
- [x] PII/API-Keys ausgeschlossen (vermerkt)
- [x] README BWKI-Reproduktionspfad
- [x] requirements deps-import-ok + pytest 84 green 2026-09-16; frische Venv-Installation ausstehend (optional)
- [ ] CI-Erstrun GitHub Actions — OPEN (workflow vorhanden, laeuft erst bei Push; origin/master 15 commits behind, Push-Entscheidung beim User)

Video-Pitch:
- [x] script v2 + storyboard + Fakten-Check
- [x] Aufnahme 09-12 4K-Master + EN/ZH subs + DE/EN srt (ftyp-verifiziert)
- [x] Schnitt 2-4min 1080p H.264 (Master vorhanden)
- [ ] Narrativ-Abgleich vs v26-Paper — OPEN
- [x] Musik/Assets-Lizenz — DONE 2026-09-18: Small Signs of Change – Sascha Ende (ende.app, CC BY 4.0)
- [ ] `submission/pitch/assets/` — OPEN

Supporting Paper/PDF:
- [x] Narrative reframed (AI-Audit)
- [x] PDF assembliert fpdf2, drei Orte bytes-identisch, Stand 2026-09-16: 243313B inkl. 517-Re-Freeze
- [ ] Formatpruefung (Zahlen/Diagramme/Referenzen) bis 9/13 — OPEN
- [x] Manifest 556/517/219 abgeglichen; _deploy-Spiegel synchron

Content leftovers:
- [ ] `04_discussion.md` so-what check — optional/OPEN
- [x] SW-Fixforschung Step 4 (SW1/SW2+West/SW3/SW4) done
- [x] pitch_10min/demo_script LEGACY mark done

Signature/Copyright:
- [ ] Unterschrift Ort/Datum/Name (declaration S8 blank) — OPEN at submission signing
- [ ] Video-Copyright-Nennung bei Aufnahme — PENDING (declaration S7)

CHECKLIST RESULT: NOT all-checked. Open items: Plattform-Abgleich, CI-Erstrun (+Push-Entscheidung), Video-Narrativabgleich, Musik/Assets-Lizenz, pitch assets, PDF-Formatpruefung, Unterschrift, Budget-Betragstabelle, Track-Benennung. No commits made by this audit.
