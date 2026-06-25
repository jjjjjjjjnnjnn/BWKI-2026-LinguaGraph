#!/usr/bin/env python3
"""
sync_readmes.py — Trilingual README sync

Rewrites of English source README.md into README_DE.md (German) and README_ZH.md (Chinese)
using comprehensive section-level and phrase-level translation maps.

Strategy:
  1. Read source README.md
  2. Apply DE/ZH heading translations (regex on ## headings)
  3. Apply DE/ZH body phrase translations (longest-first substring replacement)
  4. Write output files
  5. Verify completeness by scanning for known English keywords
  6. Also fix portal footer links
"""

import re
import sys

def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path: str, content: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def translate_heading(line: str, lang: str) -> str:
    """Translate a ## or ### heading if it's in English."""
    heading_map = {
        'en': {},  # identity
        'de': {
            'Table of Contents': 'Inhaltsverzeichnis',
            'Why LinguaGraph?': 'Warum LinguaGraph?',
            'Metrics at a Glance': 'Metriken im Überblick',
            '12 Findings (F1–F12)': '12 Erkenntnisse (F1–F12)',
            'Dataset': 'Datensatz',
            'Extraction & Human Validation': 'Extraktion und Humanvalidierung',
            'Quick Start': 'Schnellstart',
            'Deploy Your Own': 'Selbst hosten',
            'Model Benchmark': 'Modellvergleich',
            'Project Structure': 'Projektstruktur',
            'References': 'Literaturverzeichnis',
            'Key References': 'Literaturverzeichnis',
            'Citation': 'Zitationshinweis',
            'License & Compliance': 'Lizenz & Compliance',
            'Contact': 'Kontakt',
            'Academic Papers': 'Wissenschaftliche Publikationen',
            'Open Source Libraries': 'Open-Source-Bibliotheken',
            'Curriculum Standards (Primary Sources)': 'Lehrplanstandards (Primärquellen)',
            'Textbook Corpora': 'Lehrbuchkorpora',
            'Acknowledgments': 'Danksagungen',
        },
        'zh': {
            'Table of Contents': '目录',
            'Why LinguaGraph?': '为什么需要 LinguaGraph?',
            'Metrics at a Glance': '核心指标一览',
            '12 Findings (F1–F12)': '12 项发现 (F1–F12)',
            'Dataset': '数据集',
            'Extraction & Human Validation': '提取与人类验证',
            'Quick Start': '快速开始',
            'Deploy Your Own': '自行部署',
            'Model Benchmark': '模型基准测试',
            'Project Structure': '项目结构',
            'References': '参考文献',
            'Key References': '参考文献',
            'Citation': '引用说明',
            'License & Compliance': '许可与合规',
            'Contact': '联系方式',
            'Academic Papers': '学术论文',
            'Open Source Libraries': '开源库',
            'Curriculum Standards (Primary Sources)': '课程标准（原始来源）',
            'Textbook Corpora': '教材语料库',
            'Acknowledgments': '致谢',
        },
    }
    # Match headings starting with optional emoji, then English title (may start with digit)
    m = re.match(r'^(#{1,4}\s+(?:[^\w\d\s][ -￿]?\s*)?)([A-Za-z0-9][A-Za-z0-9\s&–—,;:\'!?()/-]+)$', line)
    if m:
        prefix, en_title = m.groups()
        en_title = en_title.strip()
        if en_title in heading_map.get(lang, {}):
            return prefix.rstrip() + ' ' + heading_map[lang][en_title]
    return line


def build_body_map(lang: str) -> dict:
    """Build a comprehensive English→DE/ZH body translation map."""
    maps = {
        'de': {
            # ===== Why LinguaGraph? =====
            'Mathematical truth is universal, but the way it is organized in textbooks varies dramatically across languages and educational systems. Existing curriculum analysis tools are qualitative, manual, and cannot scale across multiple languages or disciplines.':
                'Mathematische Wahrheit ist universell, aber die Art und Weise, wie sie in Lehrbüchern organisiert ist, variiert erheblich zwischen Sprachen und Bildungssystemen. Bestehende Lehrplananalysewerkzeuge sind qualitativ, manuell und können nicht über mehrere Sprachen oder Disziplinen hinweg skaliert werden.',
            '**LinguaGraph is the first automated framework that:**':
                '**LinguaGraph ist das erste automatisierte Framework, das:**',
            '🧩 Constructs **multilingual knowledge graphs** from textbooks at scale (1,160+ concepts, 3 languages)':
                '🧩 **Mehrsprachige Wissensgraphen** aus Lehrbüchern in großem Maßstab erstellt (1.160+ Konzepte, 3 Sprachen)',
            '📏 Quantifies **structural differences** between languages, education systems, and disciplines':
                '📏 **Strukturelle Unterschiede** zwischen Sprachen, Bildungssystemen und Disziplinen quantifiziert',
            '🎯 Measures **textbook-curriculum alignment** across 4 educational systems (Germany, UK, US, China)':
                '🎯 **Lehrbuch-Lehrplan-Abgleich** über 4 Bildungssysteme hinweg misst (Deutschland, Großbritannien, USA, China)',
            '✅ Validates extraction quality with **92 gold-standard annotations** (F1 = 0.939)':
                '✅ Extraktionsqualität mit **92 Goldstandard-Annotationen** validiert (F1 = 0,939)',
            '> **It turns the invisible structure of knowledge into visible, measurable metrics.**':
                '> **Es verwandelt die unsichtbare Struktur von Wissen in sichtbare, messbare Metriken.**',

            # ===== Metrics at a Glance - What It Reveals column =====
            'Knowledge interconnection density per education level':
                'Vernetzungsdichte des Wissens pro Bildungsstufe',
            'Maximum prerequisite chain length':
                'Maximale Länge der Voraussetzungskette',
            'Cross-language structural divergence':
                'Sprachübergreifende strukturelle Divergenz',
            'Textbook-curriculum alignment':
                'Lehrbuch-Lehrplan-Abgleich',

            # ===== Dataset table headers =====
            '| Subject | Concepts | Relations | Textbooks | Languages | Curriculum Coverage |':
                '| Fach | Konzepte | Beziehungen | Lehrbucher | Sprachen | Lehrplanabdeckung |',

            # ===== Badge alt text =====
            'alt="92 Gold Labels"':
                'alt="92 Gold-Standard"',
            'alt="1160+ Concepts"':
                'alt="1160+ Konzepte"',

            # ===== Table headers (DE) =====
            '| Metric | Full Name | Formula | What It Reveals |':
                '| Metrik | Bezeichnung | Formel | Bedeutung |',
            '| # | Finding | Evidence | Impact |':
                '| # | Erkenntnis | Beleg | Auswirkung |',
            '| Domain | ZH F1 | DE F1 | EN F1 | Overall | n |':
                '| Bereich | ZH F1 | DE F1 | EN F1 | Gesamt | n |',

            # ===== Reference table headers (DE) =====
            '| Library | Usage | License |':
                '| Bibliothek | Verwendung | Lizenz |',
            '| Standard | Publisher |':
                '| Standard | Herausgeber |',

            # ===== ToC entries =====
            '- [🔥 Why LinguaGraph?](#-why-linguagraph)':
                '- [🔥 Warum LinguaGraph?](#-warum-linguagraph)',
            '- [📐 Metrics at a Glance](#-metrics-at-a-glance)':
                '- [📐 Metriken im Uberblick](#-metriken-im-uberblick)',
            '- [📊 Dataset](#-dataset)':
                '- [📊 Datensatz](#-datensatz)',
            '- [✅ Extraction & Human Validation](#-extraction--human-validation)':
                '- [✅ Extraktion und Humanvalidierung](#-extraktion-und-humanvalidierung)',
            '- [🚀 Quick Start](#-quick-start)':
                '- [🚀 Schnellstart](#-schnellstart)',
            '- [🧪 Model Benchmark](#-model-benchmark)':
                '- [🧪 Modellvergleich](#-modellvergleich)',
            '- [📁 Project Structure](#-project-structure)':
                '- [📁 Projektstruktur](#-projektstruktur)',
            '- [📚 Key References](#-key-references)':
                '- [📚 Literaturverzeichnis](#-literaturverzeichnis)',
            '- [📜 Citation](#-citation)':
                '- [📜 Zitationshinweis](#-zitationshinweis)',
            '- [📜 License & Compliance](#-license--compliance)':
                '- [📜 Lizenz & Compliance](#-lizenz--compliance)',
            '- [🤝 Contact](#-contact)':
                '- [🤝 Kontakt](#-kontakt)',
            '- [🏆 12 Findings (F1–F12)](#-12-findings-f1f12)':
                '- [🏆 12 Erkenntnisse (F1–F12)](#-12-erkenntnisse-f1f12)',
            '- [🚀 Deploy Your Own](#-deploy-your-own)':
                '- [🚀 Selbst hosten](#-selbst-hosten)',

            # ===== Portal button text =====
            '🧠 Research Portal →':
                '🧠 Forschungsportal →',
            '🧠 LinguaGraph Research Portal →':
                '🧠 LinguaGraph Forschungsportal →',

            # ===== Reference entry =====
            'TIMSS 2019 International Results in Mathematics and Science':
                'TIMSS 2019 International Results in Mathematik und Science',
            'UK National Curriculum (Mathematics, Science)':
                'UK National Curriculum (Mathematik, Science)',

            # ===== 12 Findings - Evidence column =====
            'Confirmed independently in ZH, EN, DE':
                'Unabhängig bestätigt in ZH, EN, DE',
            '0.271 → 0.073; concept count 4.2×':
                '0,271 → 0,073; Konzeptanzahl 4,2×',
            'BFS on 3,538 prerequisite relations':
                'BFS auf 3.538 Voraussetzungsrelationen',
            'Wikipedia corpus, 5 social topics':
                'Wikipedia-Korpus, 5 soziale Themen',
            '~0.2 variation within pairs':
                '~0,2 Variation innerhalb der Paare',
            '366 physics concepts, 3 languages':
                '366 Physikkonzepte, 3 Sprachen',
            'HDS mean 0.85 vs 0.40':
                'HDS-Mittelwert 0,85 vs. 0,40',
            '220 chemistry concepts':
                '220 Chemiekonzepte',
            'NRW 34%, UK 82%, US 76%, China 8%':
                'NRW 34%, Großbritannien 82%, USA 76%, China 8%',
            "UK ↑ 53→90% (exam-driven); NRW ↘ 50→31% (specialization)":
                "Großbritannien ↑ 53→90% (prüfungsgetrieben); NRW ↘ 50→31% (Spezialisierung)",
            'N=8 participants, 90 responses, 3 levels':
                'N=8 Probanden, 90 Antworten, 3 Ebenen',
            '300 simulated responses, mock extraction':
                '300 simulierte Antworten, Mock-Extraktion',

            # ===== 12 Findings - Impact column =====
            'Challenges "knowledge gets denser with level" assumption':
                'Stellt die Annahme "Wissen wird mit der Stufe dichter" in Frage',
            'Curriculum diversification after integration hub':
                'Lehrplandiversifizierung nach Integrationsknotenpunkt',
            'Mathematics is a shallow web, not a deep tree':
                'Mathematik ist ein flaches Netz, kein tiefer Baum',
            'Counterintuitive: European languages not structurally closer':
                'Gegenintuitiv: Europäische Sprachen sind strukturell nicht näher',
            'Cross-language divergence varies by knowledge domain':
                'Sprachübergreifende Divergenz variiert nach Wissensdomäne',
            'Both follow "integrate-early, diverge-late" pattern':
                'Beide folgen dem Muster "früh integrieren, spät divergieren"',
            'Physics knowledge is more cumulative and sequential':
                'Physikwissen ist kumulativer und sequenzieller',
            'STEM density pattern is universal across subjects':
                'STEM-Dichtemuster ist fächerübergreifend universell',
            'Educational system design fundamentally affects textbook alignment':
                'Die Gestaltung des Bildungssystems beeinflusst grundlegend den Lehrbuchabgleich',
            'Assessment structure shapes curriculum-textbook relationship':
                'Prüfungsstruktur prägt die Lehrplan-Lehrbuch-Beziehung',
            'Cross-level consistency: individual → textbook → curriculum':
                'Ebenenübergreifende Konsistenz: Individuum → Lehrbuch → Lehrplan',
            'Divergence is genuine, not random variation':
                'Divergenz ist echt, keine zufällige Variation',

            # ===== 12 Findings - Finding column (DE) =====
            'CDS peaks at **Middle school** (0.271), not Elementary':
                'CDS erreicht Höhepunkt in **Mittelstufe** (0,271), nicht in Grundschule',
            '**3.7× density drop** from Middle to High school':
                '**3,7× Dichteabfall** von Mittel- zur Oberstufe',
            'HDS ≤ **8** (mean 0.40); 83% of concepts are roots':
                'HDS ≤ **8** (Mittel 0,40); 83% der Konzepte sind Wurzeln',
            '**ZH–DE** divergence highest (LDS=0.907), ZH–EN lowest (0.802)':
                '**ZH–DE** Divergenz am höchsten (LDS=0,907), ZH–EN am niedrigsten (0,802)',
            'LDS is **topic-dependent**':
                'LDS ist **themenabhängig**',
            '**Physics** peaks at **Elementary** (0.222), Math at Middle (0.271)':
                '**Physik** erreicht Höhepunkt in **Grundschule** (0,222), Mathe in Mittelstufe (0,271)',
            'Physics has **2.1× deeper** prerequisite chains':
                'Physik hat **2,1× tiefere** Voraussetzungsketten',
            '**Chemistry** peaks at Middle (0.042), 6.5× lower than Math':
                '**Chemie** erreicht Höhepunkt in Mittelstufe (0,042), 6,5× niedriger als Mathe',
            '**Coverage Score** varies dramatically across systems':
                '**Coverage Score** variiert dramatisch zwischen Systemen',
            'Coverage trajectories reveal **system design philosophy**':
                'Coverage-Verläufe offenbaren **Systemdesignphilosophie**',
            '**Human LDS** rank order matches Wikipedia corpus ✅':
                '**Humanes LDS** Rangfolge stimmt mit Wikipedia-Korpus überein ✅',
            'Human LDS (**0.727**) exceeds simulation baseline (**0.647**, p=0.05)':
                'Humanes LDS (**0,727**) übertrifft Simulationsbasislinie (**0,647**, p=0,05)',
            'Human LDS (**0.727**) exceeds simulation baseline (**0.647**, p=0.05)':
                'Humanes LDS (**0,727**) übertrifft Simulationsbasislinie (**0,647**, p=0,05)',

            # ===== Dataset table =====
            '| **Mathematics** | 574 | 3,538 | 68 | ZH/EN/DE |':
                '| **Mathematik** | 574 | 3.538 | 68 | ZH/EN/DE |',
            '| **Physics** | 366 | 383 | 94 editions | ZH/EN/DE |':
                '| **Physik** | 366 | 383 | 94 Ausgaben | ZH/EN/DE |',
            '| **Chemistry** | 220 | 215 | 18 editions | ZH/EN/DE |':
                '| **Chemie** | 220 | 215 | 18 Ausgaben | ZH/EN/DE |',
            '| **Total** | **1,160+** | **4,100+** | **180+** | **3 languages** | **4 educational systems** |':
                '| **Gesamt** | **1.160+** | **4.100+** | **180+** | **3 Sprachen** | **4 Bildungssysteme** |',

            # ===== Extraction & Human Validation =====
            '**92 gold-standard annotations** across 2 domains and 3 languages (qwen-plus, Bailian API):':
                '**92 Goldstandard-Annotationen** über 2 Domänen und 3 Sprachen (qwen-plus, Bailian API):',
            '| **Social concepts** | **0.974** | **0.949** | **0.882** | **0.939** | 72 |':
                '| **Soziale Konzepte** | **0,974** | **0,949** | **0,882** | **0,939** | 72 |',
            '| **Mathematics** | 0.857 | 0.506 | 0.711 | 0.674 | 20 |':
                '| **Mathematik** | 0,857 | 0,506 | 0,711 | 0,674 | 20 |',
            '| **All** | **0.974** | **0.949** | **0.882** | **0.939** | **92** |':
                '| **Alle** | **0,974** | **0,949** | **0,882** | **0,939** | **92** |',

            '> Error analysis: 29% of errors are from very short responses (1-2 words); 40% from partial omissions. No systematic misdirection.':
                '> Fehleranalyse: 29% der Fehler stammen von sehr kurzen Antworten (1-2 Wörter); 40% von teilweisen Auslassungen. Keine systematische Fehlleitung.',

            '**🧑 Human Validation Study (N=8)**':
                '**🧑 Humanvalidierungsstudie (N=8)**',
            '- 101 responses from ZH/DE/EN native speakers across 5 social topics':
                '- 101 Antworten von ZH/DE/EN-Muttersprachlern zu 5 sozialen Themen',
            '- Within-subject DE-EN LDS: **0.773** (same person, different language, different concepts)':
                '- Innerhalb der Versuchspersonen DE-EN LDS: **0,773** (gleiche Person, andere Sprache, andere Konzepte)',
            '- Between-subject LDS rank order: **DE–ZH (0.751) > DE–EN (0.727) > ZH–EN (0.704)**':
                '- Zwischen den Gruppen LDS-Rangfolge: **DE–ZH (0,751) > DE–EN (0,727) > ZH–EN (0,704)**',
            '- ✅ **Identical rank order** to Wikipedia corpus — cross-level validation':
                '- ✅ **Identische Rangfolge** mit Wikipedia-Korpus — ebenenübergreifende Validierung',

            '**🤖 Simulation Baseline (300 responses)**':
                '**🤖 Simulationsbasislinie (300 Antworten)**',
            '- Mean simulated LDS: **0.647** (SD=0.086)':
                '- Mittleres simuliertes LDS: **0,647** (SD=0,086)',
            '- **Human LDS (0.727) > Simulation LDS (0.647)**, p=0.05':
                '- **Humanes LDS (0,727) > Simulations-LDS (0,647)**, p=0,05',
            '- Confirms cross-language divergence exceeds random expectation':
                '- Bestätigt, dass sprachübergreifende Divergenz über zufällige Erwartung hinausgeht',

            '> See [`docs/paper/02_methodology.md`](docs/paper/02_methodology.md) for full methodology, [`scripts/analyze_human_pilot.py`](scripts/analyze_human_pilot.py) for human analysis, and [`scripts/analyze_sim_baseline.py`](scripts/analyze_sim_baseline.py) for simulation.':
                '> Siehe [`docs/paper/02_methodology.md`](docs/paper/02_methodology.md) für die vollständige Methodik, [`scripts/analyze_human_pilot.py`](scripts/analyze_human_pilot.py) für die Humananalyse und [`scripts/analyze_sim_baseline.py`](scripts/analyze_sim_baseline.py) für die Simulation.',

            # ===== Deploy Your Own =====
            'The Research Portal is a **zero-build static site**. Deploy anywhere:':
                'Das Forschungsportal ist eine **Zero-Build-Statikseite**. Überall bereitstellen:',
            '| Platform | Publish Directory |':
                '| Plattform | Verzeichnis |',
            '| **GitHub Pages** | Deployment bundle contents:':
                '| **GitHub Pages** | Bereitstellungsbundle-Inhalt:',

            # ===== Quick Start =====
            '### Test any model':
                '### Beliebiges Modell testen',
            '# 1. Install & configure':
                '# 1. Installieren & konfigurieren',
            '# 2. Validate extraction quality (5 min)':
                '# 2. Extraktionsqualität validieren (5 Min.)',
            '# 3. Generate 300-response simulation baseline':
                '# 3. 300-Antworten-Simulationsbasislinie generieren',
            '# 4. Full analysis pipeline':
                '# 4. Vollständige Analyse-Pipeline',

            # ===== Model Benchmark =====
            '20 models tested on identical 20 gold labels (20 social + 20 math) via [Alibaba Cloud Bailian](https://bailian.console.aliyun.com/):':
                '20 Modelle getestet auf identischen 20 Goldlabels (20 sozial + 20 Mathe) über [Alibaba Cloud Bailian](https://bailian.console.aliyun.com/):',
            '| Model | Domain | ZH F1 | DE F1 | EN F1 | Speed |':
                '| Modell | Bereich | ZH F1 | DE F1 | EN F1 | Geschwindigkeit |',
            'Full results: [`research/findings/bailian_benchmark_complete.json`](research/findings/bailian_benchmark_complete.json)':
                'Vollständige Ergebnisse: [`research/findings/bailian_benchmark_complete.json`](research/findings/bailian_benchmark_complete.json)',

            # ===== Project Structure =====
            '# Analysis pipelines (batch extraction, evaluation, benchmark)':
                '# Analyse-Pipelines (Batch-Extraktion, Evaluation, Benchmark)',
            '# Full research paper (abstract → conclusion)':
                '# Vollständiges Forschungspapier (Abstract → Fazit)',
            '# Quality audits & critical assessments':
                '# Qualitätsaudits & kritische Bewertungen',
            '# GDPR compliance & consent forms':
                '# DSGVO-Compliance & Einwilligungsformulare',
            '# BWKI competition submission':
                '# BWKI-Wettbewerbseinreichung',
            '# Knowledge graphs (JSON) — Math, Physics, Chemistry, Curricula':
                '# Wissensgraphen (JSON) — Mathematik, Physik, Chemie, Lehrpläne',
            '# 174 cross-lingual concept alignments':
                '# 174 sprachübergreifende Konzeptzuordnungen',
            '# 3D knowledge graph visualization (Three.js)':
                '# 3D-Wissensgraph-Visualisierung (Three.js)',
            '# Benchmark outputs, evaluation reports':
                '# Benchmark-Ergebnisse, Evaluationsberichte',
            '# API keys, DB, PII excluded':
                '# API-Schlüssel, DB, PII ausgeschlossen',

            # ===== License & Compliance =====
            '- **License**: All Rights Reserved — BWKI 2026 competition project':
                '- **Lizenz**: Alle Rechte vorbehalten — BWKI 2026 Wettbewerbsprojekt',
            '- **Privacy**: Participant data fully anonymized. No PII in repository. See [`docs/ethics/`](docs/ethics/) for GDPR compliance.':
                '- **Datenschutz**: Teilnehmerdaten vollständig anonymisiert. Keine PII im Repository. Siehe [`docs/ethics/`](docs/ethics/) für DSGVO-Compliance.',
            '- **AI Ethics**: LLM usage limited to concept extraction from textbook text. No synthetic data presented as human data.':
                '- **KI-Ethik**: LLM-Nutzung beschränkt auf Konzeptextraktion aus Lehrbuchtexten. Keine synthetischen Daten als menschliche Daten dargestellt.',
            '- **Data Sources**: Textbook excerpts used for academic research under fair use principles.':
                '- **Datenquellen**: Lehrbuchauszüge für akademische Forschung unter Fair-Use-Grundsätzen verwendet.',

            # ===== Contact =====
            '- **Competition**: [BWKI 2026](https://www.bw-ki.de/)':
                '- **Wettbewerb**: [BWKI 2026](https://www.bw-ki.de/)',
            '- **Author**: Rongjing J. — bilingual researcher (ZH/DE), passionate about AI & education':
                '- **Autor**: Rongjing J. — zweisprachiger Forscher (ZH/DE), leidenschaftlich für KI & Bildung',
            # author in contact section
            'bilingual researcher (ZH/DE), passionate about AI & education':
                'zweisprachiger Forscher (ZH/DE), leidenschaftlich für KI & Bildung interessiert',

            # ===== Acknowledgments (DE) =====
            '- **BWKI 2026** — Competition platform':
                '- **BWKI 2026** — Wettbewerbsplattform',
            '- **Alibaba Cloud Bailian** — Free API quota (1M tokens per model)':
                '- **Alibaba Cloud Bailian** — Kostenloses API-Kontingent (1M Tokens pro Modell)',
            '- **LM Studio** — Local inference (initial development)':
                '- **LM Studio** — Lokale Inferenz (erste Entwicklung)',
            '- **OpenRouter** — Model routing (tested)':
                '- **OpenRouter** — Modell-Routing (getestet)',

            # ===== Footer =====
            '<sub>Built with ❤️ for BWKI 2026 — because knowledge should be understood, not just taught.</sub>':
                '<sub>Mit ❤️ für BWKI 2026 — denn Wissen sollte verstanden, nicht nur gelehrt werden.</sub>',
            'Research Questions · Findings · Interactive 3D · Validation · Paper':
                'Forschungsfragen · Erkenntnisse · Interaktives 3D · Validierung · Paper',

            # Numbers formatting
            '1,160+': '1.160+',
            '4,100+': '4.100+',
            '0.271': '0,271',
            '0.271 → 0.073': '0,271 → 0,073',
            '0.073': '0,073',
            '0.939': '0,939',
            '0.974': '0,974',
            '0.949': '0,949',
            '0.882': '0,882',
            '0.857': '0,857',
            '0.711': '0,711',
            '0.674': '0,674',
            '0.506': '0,506',
            '0.773': '0,773',
            '0.751': '0,751',
            '0.727': '0,727',
            '0.704': '0,704',
            '0.647': '0,647',
            '0.907': '0,907',
            '0.802': '0,802',
            '0.042': '0,042',
            '0.222': '0,222',
            '0.40': '0,40',
            '0.85': '0,85',
            '2.1×': '2,1×',
            '3.7×': '3,7×',
            '4.2×': '4,2×',
            '6.5×': '6,5×',
            '2-3s': '2-3s',  # unchanged
            '10-20s': '10-20s',  # unchanged
        },

        'zh': {
            # ===== Why LinguaGraph? =====
            'Mathematical truth is universal, but the way it is organized in textbooks varies dramatically across languages and educational systems. Existing curriculum analysis tools are qualitative, manual, and cannot scale across multiple languages or disciplines.':
                '数学真理是普遍的，但它在教材中的组织方式在不同语言和教育体系之间差异巨大。现有的课程分析工具是定性的、手动的，无法跨多种语言或学科扩展。',
            '**LinguaGraph is the first automated framework that:**':
                '**LinguaGraph 是首个实现以下功能的自动化框架：**',
            '🧩 Constructs **multilingual knowledge graphs** from textbooks at scale (1,160+ concepts, 3 languages)':
                '🧩 从教材中大规模构建**多语言知识图谱**（1,160+ 概念，3 种语言）',
            '📏 Quantifies **structural differences** between languages, education systems, and disciplines':
                '📏 量化语言、教育体系和学科之间的**结构差异**',
            '🎯 Measures **textbook-curriculum alignment** across 4 educational systems (Germany, UK, US, China)':
                '🎯 衡量跨4个教育体系（德国、英国、美国、中国）的**教材-课程对齐度**',
            '✅ Validates extraction quality with **92 gold-standard annotations** (F1 = 0.939)':
                '✅ 使用 **92 个黄金标准标注**验证提取质量（F1 = 0.939）',
            '> **It turns the invisible structure of knowledge into visible, measurable metrics.**':
                '> **它将知识的无形结构转化为可见、可衡量的指标。**',

            # ===== Metrics at a Glance - What It Reveals column =====
            'Knowledge interconnection density per education level':
                '每教育阶段的知识互联密度',
            'Maximum prerequisite chain length':
                '最大前提知识链长度',
            'Cross-language structural divergence':
                '跨语言结构差异度',
            'Textbook-curriculum alignment':
                '教材与课程对齐度',

            # ===== Dataset table headers =====
            '| Subject | Concepts | Relations | Textbooks | Languages | Curriculum Coverage |':
                '| 学科 | 概念 | 关系 | 教材 | 语言 | 课程覆盖率 |',

            # ===== Badge alt text =====
            'alt="92 Gold Labels"':
                'alt="92 黄金标注"',
            'alt="1160+ Concepts"':
                'alt="1160+ 概念"',

            # ===== Table headers (ZH) =====
            '| Metric | Full Name | Formula | What It Reveals |':
                '| 指标 | 全称 | 公式 | 含义 |',
            '| # | Finding | Evidence | Impact |':
                '| # | 发现 | 证据 | 影响 |',
            '| Domain | ZH F1 | DE F1 | EN F1 | Overall | n |':
                '| 领域 | 中文 F1 | 德文 F1 | 英文 F1 | 总体 | n |',

            # ===== Reference table headers (ZH) =====
            '| Library | Usage | License |':
                '| 库 | 用途 | 许可 |',
            '| Standard | Publisher |':
                '| 标准 | 发布者 |',

            # ===== ToC entries =====
            '- [🔥 Why LinguaGraph?](#-why-linguagraph)':
                '- [🔥 为什么需要 LinguaGraph?](#-为什么需要-linguagraph)',
            '- [📐 Metrics at a Glance](#-metrics-at-a-glance)':
                '- [📐 核心指标一览](#-核心指标一览)',
            '- [📊 Dataset](#-dataset)':
                '- [📊 数据集](#-数据集)',
            '- [✅ Extraction & Human Validation](#-extraction--human-validation)':
                '- [✅ 提取与人类验证](#-提取与人类验证)',
            '- [🚀 Quick Start](#-quick-start)':
                '- [🚀 快速开始](#-快速开始)',
            '- [🧪 Model Benchmark](#-model-benchmark)':
                '- [🧪 模型基准测试](#-模型基准测试)',
            '- [📁 Project Structure](#-project-structure)':
                '- [📁 项目结构](#-项目结构)',
            '- [📚 Key References](#-key-references)':
                '- [📚 参考文献](#-参考文献)',
            '- [📜 Citation](#-citation)':
                '- [📜 引用说明](#-引用说明)',
            '- [📜 License & Compliance](#-license--compliance)':
                '- [📜 许可与合规](#-许可与合规)',
            '- [🤝 Contact](#-contact)':
                '- [🤝 联系方式](#-联系方式)',
            '- [🏆 12 Findings (F1–F12)](#-12-findings-f1f12)':
                '- [🏆 12 项发现 (F1–F12)](#-12-项发现-f1f12)',
            '- [🚀 Deploy Your Own](#-deploy-your-own)':
                '- [🚀 自行部署](#-自行部署)',

            # ===== Portal button text =====
            '🧠 Research Portal →':
                '🧠 研究门户 →',
            '🧠 LinguaGraph Research Portal →':
                '🧠 LinguaGraph 研究门户 →',

            # ===== Reference entry =====
            'TIMSS 2019 International Results in Mathematics and Science':
                'TIMSS 2019 International Results in 数学和 Science',

            # ===== 12 Findings - Evidence column =====
            'Confirmed independently in ZH, EN, DE':
                '在中文、英文、德文中独立确认',
            '0.271 → 0.073; concept count 4.2×':
                '0.271 → 0.073；概念数量 4.2 倍',
            'BFS on 3,538 prerequisite relations':
                '对 3,538 条前提关系进行 BFS',
            'Wikipedia corpus, 5 social topics':
                '维基百科语料，5 个社会话题',
            '~0.2 variation within pairs':
                '语对内部差异约 0.2',
            '366 physics concepts, 3 languages':
                '366 个物理概念，3 种语言',
            'HDS mean 0.85 vs 0.40':
                'HDS 均值 0.85 对比 0.40',
            '220 chemistry concepts':
                '220 个化学概念',
            'NRW 34%, UK 82%, US 76%, China 8%':
                '北威州 34%，英国 82%，美国 76%，中国 8%',
            "UK ↑ 53→90% (exam-driven); NRW ↘ 50→31% (specialization)":
                "英国 ↑ 53→90%（考试驱动）；北威州 ↘ 50→31%（专业化）",
            'N=8 participants, 90 responses, 3 levels':
                'N=8 参与者，90 份回答，3 个层次',
            '300 simulated responses, mock extraction':
                '300 条模拟回答，模拟提取',

            # ===== 12 Findings - Impact column =====
            'Challenges "knowledge gets denser with level" assumption':
                '挑战"知识随阶段增长而变密"的假设',
            'Curriculum diversification after integration hub':
                '整合枢纽后的课程多样化',
            'Mathematics is a shallow web, not a deep tree':
                '数学是一个浅层网络，而非深层树状结构',
            'Counterintuitive: European languages not structurally closer':
                '反直觉：欧洲语言在结构上并不更接近',
            'Cross-language divergence varies by knowledge domain':
                '跨语言差异因知识领域而异',
            'Both follow "integrate-early, diverge-late" pattern':
                '两者都遵循"早期整合，后期分化"的模式',
            'Physics knowledge is more cumulative and sequential':
                '物理知识更具累积性和顺序性',
            'STEM density pattern is universal across subjects':
                'STEM 密度模式跨学科具有普遍性',
            'Educational system design fundamentally affects textbook alignment':
                '教育体系设计从根本上影响教材对齐度',
            'Assessment structure shapes curriculum-textbook relationship':
                '考试结构塑造了课程与教材的关系',
            'Cross-level consistency: individual → textbook → curriculum':
                '跨层次一致性：个体 → 教材 → 课程',
            'Divergence is genuine, not random variation':
                '差异是真实存在的，而非随机波动',

            # ===== 12 Findings - Finding column (ZH) =====
            'CDS peaks at **Middle school** (0.271), not Elementary':
                'CDS 在**初中**达到峰值（0.271），而非小学',
            '**3.7× density drop** from Middle to High school':
                '**密度下降 3.7 倍**从初中到高中',
            'HDS ≤ **8** (mean 0.40); 83% of concepts are roots':
                'HDS ≤ **8**（均值 0.40）；83% 的概念是根节点',
            '**ZH–DE** divergence highest (LDS=0.907), ZH–EN lowest (0.802)':
                '**中文-德语**差异最大（LDS=0.907），中文-英语最小（0.802）',
            'LDS is **topic-dependent**':
                'LDS **依赖于话题**',
            '**Physics** peaks at **Elementary** (0.222), Math at Middle (0.271)':
                '**物理**在**小学**达到峰值（0.222），数学在初中（0.271）',
            'Physics has **2.1× deeper** prerequisite chains':
                '物理的前提知识链**深 2.1 倍**',
            '**Chemistry** peaks at Middle (0.042), 6.5× lower than Math':
                '**化学**在初中达到峰值（0.042），比数学低 6.5 倍',
            '**Coverage Score** varies dramatically across systems':
                '**覆盖率**在不同教育体系中差异巨大',
            'Coverage trajectories reveal **system design philosophy**':
                '覆盖率轨迹揭示了**体系设计理念**',
            '**Human LDS** rank order matches Wikipedia corpus ✅':
                '**人类 LDS** 排序与维基百科语料一致 ✅',
            'Human LDS (**0.727**) exceeds simulation baseline (**0.647**, p=0.05)':
                '人类 LDS (**0.727**) 超过模拟基线 (**0.647**, p=0.05)',

            # ===== Dataset table =====
            '| **Mathematics** | 574 | 3,538 | 68 | ZH/EN/DE |':
                '| **数学** | 574 | 3,538 | 68 | ZH/EN/DE |',
            '| **Physics** | 366 | 383 | 94 editions | ZH/EN/DE |':
                '| **物理** | 366 | 383 | 94 个版本 | ZH/EN/DE |',
            '| **Chemistry** | 220 | 215 | 18 editions | ZH/EN/DE |':
                '| **化学** | 220 | 215 | 18 个版本 | ZH/EN/DE |',
            '| **Total** | **1,160+** | **4,100+** | **180+** | **3 languages** | **4 educational systems** |':
                '| **总计** | **1,160+** | **4,100+** | **180+** | **3 种语言** | **4 个教育体系** |',

            # ===== Extraction & Human Validation =====
            '**92 gold-standard annotations** across 2 domains and 3 languages (qwen-plus, Bailian API):':
                '**92 个黄金标准标注**覆盖 2 个领域和 3 种语言（qwen-plus，百联 API）：',
            '| **Social concepts** | **0.974** | **0.949** | **0.882** | **0.939** | 72 |':
                '| **社会概念** | **0.974** | **0.949** | **0.882** | **0.939** | 72 |',
            '| **Mathematics** | 0.857 | 0.506 | 0.711 | 0.674 | 20 |':
                '| **数学** | 0.857 | 0.506 | 0.711 | 0.674 | 20 |',
            '| **All** | **0.974** | **0.949** | **0.882** | **0.939** | **92** |':
                '| **全部** | **0.974** | **0.949** | **0.882** | **0.939** | **92** |',

            '> Error analysis: 29% of errors are from very short responses (1-2 words); 40% from partial omissions. No systematic misdirection.':
                '> 误差分析：29% 的错误来自极短的回答（1-2 个词）；40% 来自部分遗漏。没有系统性的误导。',

            '**🧑 Human Validation Study (N=8)**':
                '**🧑 人类验证研究（N=8）**',
            '- 101 responses from ZH/DE/EN native speakers across 5 social topics':
                '- 来自中文/德文/英文母语者的 101 份回答，覆盖 5 个社会话题',
            '- Within-subject DE-EN LDS: **0.773** (same person, different language, different concepts)':
                '- 被试内 DE-EN LDS：**0.773**（同一人，不同语言，不同概念）',
            '- Between-subject LDS rank order: **DE–ZH (0.751) > DE–EN (0.727) > ZH–EN (0.704)**':
                '- 被试间 LDS 排序：**DE–ZH (0.751) > DE–EN (0.727) > ZH–EN (0.704)**',
            '- ✅ **Identical rank order** to Wikipedia corpus — cross-level validation':
                '- ✅ **与维基百科语料排序一致**——跨层次验证',

            '**🤖 Simulation Baseline (300 responses)**':
                '**🤖 模拟基线（300 条回答）**',
            '- Mean simulated LDS: **0.647** (SD=0.086)':
                '- 模拟 LDS 均值：**0.647**（标准差=0.086）',
            '- **Human LDS (0.727) > Simulation LDS (0.647)**, p=0.05':
                '- **人类 LDS (0.727) > 模拟 LDS (0.647)**，p=0.05',
            '- Confirms cross-language divergence exceeds random expectation':
                '- 确认跨语言差异超出了随机预期',

            '> See [`docs/paper/02_methodology.md`](docs/paper/02_methodology.md) for full methodology, [`scripts/analyze_human_pilot.py`](scripts/analyze_human_pilot.py) for human analysis, and [`scripts/analyze_sim_baseline.py`](scripts/analyze_sim_baseline.py) for simulation.':
                '> 完整方法论参见 [`docs/paper/02_methodology.md`](docs/paper/02_methodology.md)，人类分析脚本参见 [`scripts/analyze_human_pilot.py`](scripts/analyze_human_pilot.py)，模拟基线脚本参见 [`scripts/analyze_sim_baseline.py`](scripts/analyze_sim_baseline.py)。',

            # ===== Deploy Your Own =====
            'The Research Portal is a **zero-build static site**. Deploy anywhere:':
                '研究门户是一个**零构建静态网站**。可部署到任何地方：',
            '| Platform | Publish Directory |':
                '| 平台 | 发布目录 |',
            '| **GitHub Pages** | Deployment bundle contents:':
                '| **GitHub Pages** | 部署包内容：',

            # ===== Quick Start =====
            '### Test any model':
                '### 测试任意模型',
            '# 1. Install & configure':
                '# 1. 安装与配置',
            '# 2. Validate extraction quality (5 min)':
                '# 2. 验证提取质量（5 分钟）',
            '# 3. Generate 300-response simulation baseline':
                '# 3. 生成 300 条回答的模拟基线',
            '# 4. Full analysis pipeline':
                '# 4. 完整分析流程',

            # ===== Model Benchmark =====
            '20 models tested on identical 20 gold labels (20 social + 20 math) via [Alibaba Cloud Bailian](https://bailian.console.aliyun.com/):':
                '在相同的 20 个黄金标签（20 个社会 + 20 个数学）上测试了 20 个模型，通过[阿里云百联平台](https://bailian.console.aliyun.com/)：',
            '| Model | Domain | ZH F1 | DE F1 | EN F1 | Speed |':
                '| 模型 | 领域 | 中文 F1 | 德文 F1 | 英文 F1 | 速度 |',
            'Full results: [`research/findings/bailian_benchmark_complete.json`](research/findings/bailian_benchmark_complete.json)':
                '完整结果：[`research/findings/bailian_benchmark_complete.json`](research/findings/bailian_benchmark_complete.json)',

            # ===== Project Structure =====
            '# Analysis pipelines (batch extraction, evaluation, benchmark)':
                '# 分析流程（批量提取、评估、基准测试）',
            '# Full research paper (abstract → conclusion)':
                '# 完整研究论文（摘要 → 结论）',
            '# Quality audits & critical assessments':
                '# 质量审计与批判性评估',
            '# GDPR compliance & consent forms':
                '# GDPR 合规与知情同意书',
            '# BWKI competition submission':
                '# BWKI 竞赛提交材料',
            '# Knowledge graphs (JSON) — Math, Physics, Chemistry, Curricula':
                '# 知识图谱（JSON）——数学、物理、化学、课程',
            '# 174 cross-lingual concept alignments':
                '# 174 个跨语言概念对齐',
            '# 3D knowledge graph visualization (Three.js)':
                '# 3D 知识图谱可视化（Three.js）',
            '# Benchmark outputs, evaluation reports':
                '# 基准测试输出、评估报告',
            '# API keys, DB, PII excluded':
                '# 排除 API 密钥、数据库、个人隐私信息',

            # ===== License & Compliance =====
            '- **License**: All Rights Reserved — BWKI 2026 competition project':
                '- **许可**：保留所有权利 — BWKI 2026 竞赛项目',
            '- **Privacy**: Participant data fully anonymized. No PII in repository. See [`docs/ethics/`](docs/ethics/) for GDPR compliance.':
                '- **隐私**：参与者数据完全匿名化。仓库中不包含个人身份信息。GDPR 合规详情参见 [`docs/ethics/`](docs/ethics/)。',
            '- **AI Ethics**: LLM usage limited to concept extraction from textbook text. No synthetic data presented as human data.':
                '- **AI 伦理**：LLM 使用仅限于从教材文本中提取概念。没有将合成数据呈现为人类数据。',
            '- **Data Sources**: Textbook excerpts used for academic research under fair use principles.':
                '- **数据来源**：教材摘录在合理使用原则下用于学术研究。',

            # ===== Contact =====
            '- **Competition**: [BWKI 2026](https://www.bw-ki.de/)':
                '- **竞赛**：[BWKI 2026](https://www.bw-ki.de/)',
            '- **Author**: Rongjing J. — bilingual researcher (ZH/DE), passionate about AI & education':
                '- **作者**：Rongjing J. — 双语研究者（中/德），对 AI 与教育充满热情',
            'bilingual researcher (ZH/DE), passionate about AI & education':
                '双语研究者（中/德），对 AI 与教育充满热情',

            # ===== Acknowledgments (ZH) =====
            '- **BWKI 2026** — Competition platform':
                '- **BWKI 2026** — 竞赛平台',
            '- **Alibaba Cloud Bailian** — Free API quota (1M tokens per model)':
                '- **阿里云百联** — 免费 API 额度（每个模型 100 万 token）',
            '- **OpenRouter** — Model routing (tested)':
                '- **OpenRouter** — 模型路由（已测试）',
            '- **LM Studio** — Local inference (initial development)':
                '- **LM Studio** — 本地推理（初期开发）',

            # ===== Footer =====
            '<sub>Built with ❤️ for BWKI 2026 — because knowledge should be understood, not just taught.</sub>':
                '<sub>用 ❤️ 为 BWKI 2026 打造——因为知识应该被理解，而不仅仅是被告知。</sub>',
            'Research Questions · Findings · Interactive 3D · Validation · Paper':
                '研究问题 · 发现 · 交互式 3D · 验证 · 论文',
        },
    }
    return maps.get(lang, {})


def verify_translation(text: str, lang: str) -> list:
    """Check for remaining English keywords that should have been translated."""
    # These are words that should NOT remain in English in DE/ZH
    check_words = {
        'de': [
            'Concepts', 'Relations', 'Disciplines', 'Gold Labels', 'Overall F1',
            'Research Questions', 'Interactive 3D', 'Research Portal',
            'Social concepts', 'Mathematics', 'Model Benchmark',
            'Project Structure', 'Quick Start', 'Extraction Validation',
            'Table of Contents', 'Why LinguaGraph', 'Dataset',
            'References', 'License', 'Compliance', 'Contact',
            'Citation', 'Key References',
        ],
        'zh': [
            'Concepts', 'Relations', 'Disciplines', 'Gold Labels', 'Overall F1',
            'Research Questions', 'Interactive 3D', 'Research Portal',
            'Social concepts', 'Mathematics', 'Model Benchmark',
            'Project Structure', 'Quick Start', 'Extraction Validation',
            'Table of Contents', 'Why LinguaGraph', 'Dataset',
            'References', 'License', 'Compliance', 'Contact',
            'Citation', 'Key References',
        ],
    }
    remaining = [w for w in check_words.get(lang, []) if w in text]
    return remaining


def translate_readme(source_text: str, lang: str) -> str:
    """Translate README content from English to target language."""
    text = source_text

    # Pre-process: ensure all ## headings start on their own line
    text = re.sub(r'([^\n])(\n?## )', r'\1\n\2', text)

    # Step 1: Translate ## headings
    lines = text.split('\n')
    translated_lines = []
    for line in lines:
        if line.startswith('## '):
            translated_lines.append(translate_heading(line, lang))
        else:
            translated_lines.append(line)
    text = '\n'.join(translated_lines)

    # Step 2: Translate body phrases (longest first to avoid partial matches)
    body_map = build_body_map(lang)
    for old in sorted(body_map.keys(), key=len, reverse=True):
        text = text.replace(old, body_map[old])

    return text


def fix_portal_links() -> None:
    """Fix portal footer links to use GitHub URLs."""
    portal_path = 'cognitive-space/portal/index.html'
    html = read_file(portal_path)

    html = html.replace(
        'href="../README.md"',
        'href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph"'
    )
    html = html.replace(
        'href="../README_DE.md"',
        'href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/blob/master/README_DE.md"'
    )
    html = html.replace(
        'href="../README_ZH.md"',
        'href="https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph/blob/master/README_ZH.md"'
    )

    write_file(portal_path, html)
    print('  Portal footer links fixed to GitHub URLs')


def main():
    # Read source EN README
    en = read_file('README.md')

    for lang_code, output_file in [('de', 'README_DE.md'), ('zh', 'README_ZH.md')]:
        # Translate
        translated = translate_readme(en, lang_code)

        # Write
        write_file(output_file, translated)

        # Verify
        t = read_file(output_file)
        remaining = verify_translation(t, lang_code)
        sections = [l.strip() for l in t.split('\n') if l.strip().startswith('## ') and not l.strip().startswith('### ')]

        print(f'{output_file}: {len(t)} chars, {len(sections)} sections')
        if remaining:
            print(f'  [WARN] Remaining English ({len(remaining)}): {remaining}')
        else:
            print(f'  [OK] All text translated!')

        # Check for any English paragraph text (heuristic: lines with >20 chars of mostly ASCII)
        ascii_paragraphs = 0
        for line in t.split('\n'):
            stripped = line.strip()
            if len(stripped) > 40:
                ascii_count = sum(1 for c in stripped if c.isascii() and c.isalpha())
                if ascii_count > len(stripped) * 0.7 and stripped.startswith(('Mathematical', 'Existing', 'LinguaGraph', 'It turns', 'Error', '101 responses', 'Mean simulated', '20 models', 'The Research')):
                    ascii_paragraphs += 1
                    if ascii_paragraphs <= 2:
                        print(f'  ⚠️  Possible English paragraph: "{stripped[:80]}..."')

        if ascii_paragraphs > 0:
            print(f'  [WARN] {ascii_paragraphs} possible English paragraphs detected')
        else:
            print(f'  [OK] No English paragraphs detected')

    # Fix portal links
    fix_portal_links()

    print('\nDone! All files updated.')


if __name__ == '__main__':
    main()
