# Data Manifest

## Overview

This directory contains the source data used by the LinguaGraph research pipeline. Raw textbook content and LLM extraction outputs are **referenced but not versioned** in this repository to maintain a focused, lightweight research codebase.

## Collections

| Collection | Files | Status | Description |
|-----------|-------|--------|-------------|
| `textbook/` | 75+ text files | 📦 Referenced only | Raw textbook sections (ZH/EN/DE), sourced from CC-BY-SA and fair-use educational materials |
| `math_extractions/` | 63 JSON files | 📦 Referenced only | MIMO LLM extraction outputs — concept/relation JSON from each textbook section |
| `questionnaires/` | 3 JSON + 2 PDF | ✅ Tracked | BWKI survey instruments in ZH/EN/DE |
| `gold/` | 1 JSON | ✅ Tracked | Gold-standard human annotations |
| `baseline/` | 1 JSON | ✅ Tracked | Computational baseline results |
| `corpus/` | 12+ text files | ✅ Tracked | Wikipedia pilot corpus (ZH/EN/DE, 5 topics) |
| `evidence/` | 6 files | ✅ Tracked | Research evidence and analysis summaries |

## Raw Data Policy

The following are **not committed** to this repository:

- `data/textbook/` — Raw textbook text (size, copyright considerations)
- `data/math_extractions/` — LLM extraction outputs (derived, reproducible from pipeline)

These assets are regenerable by running the pipeline:

```bash
# Regenerate extractions from textbook text (requires MIMO LLM)
# Then run the knowledge graph pipeline:
python scripts/math_graph_pipeline/run_pipeline.py
```

For BWKI review, the complete dataset including raw text and extractions is available upon request or can be regenerated using the pipeline scripts in `cognitive-space/scripts/math_graph_pipeline/`.

## Provenance

All textbook sources are documented in `cognitive-space/README.md` with full attribution (publisher, edition, chapter references). Extraction methodology is documented in `docs/mimo_prompt.md`.

## Open-textbook arrivals 2026-09-12 (`data/textbook/open/`, local only, not committed)

> 8-field rows: 题名 / 作者 / 版次 / 出版社 / 年份 / 章节 / 语言 / 许可+URL. Fetch scripts: `scripts/fetch_open_texts.py` (intros+syllabi), `scripts/fetch_openstax_sections.py` (72 sections), `scripts/extract_vol3_ch10.py` (attempted PDF slice, superseded by correct web slugs).

- `题名:University Physics Volume 2 | 作者:Ling/Sanny/Moebs | 版次:2016 | 出版社:OpenStax/Rice | 年份:2016 | 章节:Ch10/13/14/15/16 (29 sections full text + full-book PDF 63.8MB) | 语言:en | 许可+URL:CC BY-NC-SA 4.0 · openstax.org/details/books/university-physics-volume-2 | 到货:2026-09-12`
- `题名:University Physics Volume 3 | 作者:Ling/Sanny/Moebs | 版次:2016 | 出版社:OpenStax/Rice | 年份:2016 | 章节:Ch10.1-10.7 (7 sections full text + full-book PDF 53.5MB; slugs corrected: 10.4 Nuclear Reactions / 10.5 Fission / 10.6 Nuclear Fusion / 10.7 Medical) | 语言:en | 许可+URL:CC BY-NC-SA 4.0 · openstax.org/details/books/university-physics-volume-3 | 到货:2026-09-12`
- `题名:Chemistry 2e | 作者:Flowers/Theopold/Langley/Robinson | 版次:2e | 出版社:OpenStax/Rice | 年份:2019 | 章节:Ch6/7/8/16/17/20/21 (36 sections full text + 7 intros; full-book PDF 218MB skipped — sections instead) | 语言:en | 许可+URL:CC BY-NC-SA 4.0 · openstax.org/details/books/chemistry-2e | 到货:2026-09-12`
- `题名:MIT OCW 5.60/5.12/5.13/8.01SC/8.02 syllabi+notes | 作者:MIT Faculty | 版次:2005-2016 terms | 出版社:MIT OCW | 年份:2005-2016 | 章节:syllabus metadata (5) + 8.01 F16 course-notes bundle (64MB, source URL named TableOfContents) | 语言:en | 许可+URL:CC BY-NC-SA 4.0 · ocw.mit.edu/pages/privacy-and-terms-of-use | 到货:2026-09-12`
- `题名:USTC 621《物理化学》考试大纲 | 作者:中国科学技术大学 | 版次:当年版 | 出版社:USTC研招 | 年份:当年版 | 章节:模块划分依据(傅献彩第六版对应) | 语言:zh | 许可+URL:公开行政文件(unverified)·本地研究使用 | 到货:2026-09-12`
- `题名:UCAS《有机化学》考试大纲 | 作者:中国科学院大学 | 版次:2016-06-22 | 出版社:UCAS研招 | 年份:2016 | 章节:模块划分依据(邢其毅第三版对应) | 语言:zh | 许可+URL:公开行政文件(unverified)·本地研究使用 | 到货:2026-09-12`
- `题名:普通高中教科书·物理/化学7册 (PEP 2019) | 作者:人教社课材所 | 版次:2019(第1版) | 出版社:人民教育出版社 | 年份:2019 | 章节:物理必修3(143pp)/选必1(130pp)/选必2(122pp)/选必3(143pp)/化学选必1(139pp)/选必2(115pp)/选必3(163pp) | 语言:zh | 许可+URL:版权教材·第三方镜像(TapXWorld/ChinaTextbook, provenance unverified)·本地研究专用·永不进仓·以smartedu官方本为准 | 到货:2026-09-12 | 格式:扫描版无文本层(OCR pending,本地无OCR引擎) | 封面已目验(2019审定章+人教社印)`
- LEIFI/NPTEL: link-only, no local copy (LEIFI §44b / NPTEL license-version unverified) — mapping rows carry URLs only.
- OpenStax LLM-training reservation noted (book footer): local research mapping use only; no redistribution, no model training.
