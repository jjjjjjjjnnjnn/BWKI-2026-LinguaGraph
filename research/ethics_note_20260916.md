# Human-Data Ethics Note — LinguaGraph BWKI 2026

Date: 2026-09-16 | Scope: repo-evidence only (`tests/`, `participant_data/`, `docs/ethics/`, survey/pilot files, paper claims). No new data collected.

## 1. 是否涉及人类被试 — YES

- Pilot N=8: P001-P008, zh-only, 80/80 responses (10 each), `docs/pilot_quality_report.md` 2026-06-19 snapshot pilot_v1.
- Formal human arm N=15 (6 DE / 6 ZH / 3 EN), Between-Subject, per `docs/paper/01_abstract_introduction.md`, README Kernbefunde F11, `plattform_antworten.md` S4/S5.
- Design target per `participant_data/participant_manager.py`: 30 total (10 per zh/de/en); recruitment status machine tracks registered/consented. Formal N=15 < target 30.
- Analysis path: `scripts/analyze_human_pilot.py` (S* extractions via qwen-plus batch) + `tests/evaluate_survey.py` (per-question LLM extraction Q01-Q10, Q08 structured).

## 2. 何种数据 (data categories)

- Collected: written answers to open tasks — Wortassoziationen, Begriffserklaerungen (e.g. Xiao/Fernweh/Privacy), Bildbeschreibungen, Uebersetzungen, soziale Themen (Freiheit, Gerechtigkeit, Erfolg, Verantwortung, Heimat). See `data/questionnaires/survey_analysis.md`, consent texts.
- Metadata fields in code/DB: student_id, native_lang, school_lang, other_langs, age_group, years_in_germany, notes, language/question_id/answer_text/word_count, consent flag. See `participant_manager.add_participant`, `survey_entry.py`.
- Explicitly NOT collected per consent/GDPR pack: Namen, Adressen, IP-Adressen, Geburtsdatum. Extraction/analysis keeps language/question/answer text only.
- Live stores in repo boundary: `linguaGraph.db`, `participant_data/`, `data/raw/survey_*.jsonl`, `data/raw/test_survey_data.jsonl`, pilot responses in DB (`source='pilot'`). Submission excludes PII: anonymized aggregates in `freeze/` + `data/lds_c/` only (per `code_einreichung.md` S3, README).

## 3. 知情同意方式 (consent)

- Basis stated: GDPR/DSGVO Art. 6(1)(a) Einwilligung. Trilingual templates present: `docs/ethics/consent_de.md`, `consent_en.md`, `consent_zh.md` (+ `gdpr_package.md` Docs 4-7).
- Content: purpose, 10 tasks x3 languages ~45 min, anonymized storage + AI analysis, controller via school supervisor, rights (access/rectification/erasure/withdrawal/complaint), voluntary, exit deletes data immediately, paper signature lines (Teilnehmer-ID/Datum/Unterschrift).
- Machine enforcement: `consent` boolean on add/update; `update_consent()`; status reports consented counts; `delete_participant()` for Art. 17 erasure; deletion-request template in GDPR pack (Art. 17, 30-day confirm per policy; breach notice 72h per Art. 33/34).
- Consent status verdict: TEMPLATE-LEVEL complete; SIGNED-FORM EVIDENCE missing (no signed forms or consent log found in repo — record as OPEN gap, not as confirmed obtained).

## 4. 匿名化 (anonymization)

- Implemented in `participant_manager.anonymize_response()`: student_id -> sha256 12-char anonymous_id, drops timestamp/created_at/updated_at; keeps language/answer. `export_anonymized(batch)` writes JSONL to `participant_data/anonymized/`.
- Policy: random ID (S001...), name-ID mapping stored separately password-protected, deleted at completion; paper consent forms shredded after retention; analysis results indefinite only as aggregates without PII.
- Test coverage: `tests/test_participant_manager.py::TestAnonymization` asserts id/timestamp removal.
- Verdict: MECHANISM present and tested; operational proof (mapping file location, password control, export actually used for submission) NOT evidenced — OPEN gap.

## 5. 保存期限 (retention)

- Stated uniformly: max 12 Monate nach Projektende, dann endgueltige Loeschung (consent forms paper+digital, anonymized responses via permanent DB deletion, name-ID mapping via secure shredding). Analysis aggregates indefinite.
- Deletion procedure: locate by ID in mapping, delete responses/extractions/analysis rows, confirm within 30 days.
- Gaps (OPEN): "Projektende" date undefined so clock start unclear; mapping-deletion certificate absent; no evidence retention schedule was executed.

## 6. 未成年人说明 (minors)

- Templates cover <16: parental/guardian co-signature required, citing Art. 8 DSGVO + DDG S4 (`gdpr_package.md` Doc 7, `consent_de.md` footer, `consent_zh.md` footer). Target group per consent_zh header: 13-18 Jahre.
- Pilot conflict: `pilot_quality_report.md` S6 notes age range 10-55 spanning 4 decades. This includes <16 (and <13) without evidenced parental consents in repo. Formal N=15 age distribution not found in read materials.
- Verdict: RULE present; PILOT SCOPE (10-55) vs TARGET (13-18) mismatch + missing parental-consent proof = OPEN deviation.

## 7. 缺口 = OPEN 偏离 + 补救建议

1. OPEN: signed consent / parental consent log absent (templates only). Fix: file signed-form count per cohort (pilot N=8, formal N=15) + parental forms for <16; do not submit until reconciled.
2. OPEN: Google Forms vs "lokal verschluesselt, kein Cloud-Upload" tension (`gdpr_package.md` retention policy says collected via Google Forms then local SQLite). Fix: name the actual collection channel, data-processing agreement if Google used, or correct the policy sentence.
3. OPEN: name-ID mapping protection/location unverified; DB (`linguaGraph.db`) and `participant_data/` live in workspace. Fix: confirm mapping file path + access control, confirm PII never pushed to `submission/final/` or public remote, shred mapping at completion with record.
4. OPEN: retention clock undefined + no deletion log. Fix: define Projektende date, compute deletion deadline, log deletions.
5. OPEN: pilot age 10-55 out of declared 13-18 scope; short/language-mixed answers and carryover issues noted but no ethics re-review. Fix: restrict future cohorts to declared range or amend protocol + obtain retrospective parental-consent confirmation for pilot minors; exclude unconsented records.
6. OPEN: survey content risk low but Q-bank includes value-laden topics for minors; no distress/withdrawal log found. Fix: add 1-line withdrawal/distress log (even if zero events).

ETHICS VERDICT: human data YES (pilot 8 + formal 15); consent TEMPLATE ok / SIGNED proof OPEN; anonymization MECHANISM ok / OPERATIONAL proof OPEN; retention 12-month rule stated / EXECUTION open; minors RULE ok / PILOT age-scope + parental-proof OPEN. Do not claim "fully consented/anonymized/deleted" until gaps 1-5 closed.
