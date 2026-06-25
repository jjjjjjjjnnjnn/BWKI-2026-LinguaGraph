<p align="center">
  <a href="README.md">🇬🇧 English</a> · <a href="README_DE.md">🇩🇪 Deutsch</a> · <a href="README_ZH.md">🇨🇳 中文</a>
</p>

---

<p align="center">
  <img src="cognitive-space/web/screenshot.png" alt="LinguaGraph — Mehrsprachige Wissensstrukturanalyse" width="100%">
</p>

<h1 align="center">🧠 LinguaGraph</h1>

<p align="center">
  <b>Wie organisieren verschiedene Sprachen und Bildungssysteme dasselbe Wissen?</b>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph?style=flat-square&logo=github&color=gold" alt="Stars">
  <img src="https://img.shields.io/badge/lizenz-All%20Rights%20Reserved-blue?style=flat-square" alt="Lizenz">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/BWKI-2026-8A2BE2?style=flat-square" alt="BWKI 2026">
  <img src="https://img.shields.io/badge/Gold_Label-92-success?style=flat-square" alt="92 Gold Label">
  <img src="https://img.shields.io/badge/Konzepte-1.160%2B-informational?style=flat-square" alt="1160+ Konzepte">
  <img src="https://img.shields.io/badge/Sprachen-ZH%20%7C%20EN%20%7C%20DE-green?style=flat-square" alt="ZH/EN/DE">
  <img src="https://img.shields.io/badge/F%C3%A4cher-Mathe%20%7C%20Physik%20%7C%20Chemie-orange?style=flat-square" alt="Mathe/Physik/Chemie">
</p>

---

## 📑 Inhaltsverzeichnis

<details>
<summary><b>Zum Öffnen klicken</b></summary>

- [🔥 Warum LinguaGraph?](#-warum-linguagraph)
- [📐 Metriken](#-metriken)
- [🏆 10 Erkenntnisse (F1–F10)](#-10-erkenntnisse-f1f10)
- [📊 Datensatz](#-datensatz)
- [✅ Extraktionsqualität](#-extraktionsqualität)
- [🚀 Schnellstart](#-schnellstart)
- [📜 Literatur](#-literatur)
- [📜 Lizenz & Compliance](#-lizenz--compliance)

</details>

---

## 🔥 Warum LinguaGraph?

Mathematische Wahrheit ist universell, aber ihre Organisation in Lehrbüchern variiert stark zwischen Sprachen und Bildungssystemen. Bestehende Analysetools sind qualitativ, manuell und nicht skalierbar.

**LinguaGraph ist das erste automatisierte Framework, das:**

- 🧩 Mehrsprachige **Wissensgraphen** aus Lehrbüchern erstellt (1.160+ Konzepte, 3 Sprachen)
- 📏 **Strukturelle Unterschiede** zwischen Sprachen, Bildungssystemen und Disziplinen quantifiziert
- 🎯 Die **Lehrplanabdeckung** in 4 Bildungssystemen misst (NRW, UK, USA, China)
- ✅ Extraktionsqualität mit **92 Goldstandard-Annotationen** validiert (F1 = 0,939)

---

## 📐 Metriken

| Metrik | Formel | Bedeutung |
|--------|--------|-----------|
| **CDS** | 2\|E\|/(\|V\|·(\|V\|−1)) | Wissensdichte pro Bildungsstufe |
| **HDS** | BFS auf Voraussetzungsgraph | Maximale Kettentiefe |
| **LDS** | 1 − mean(GED, Jaccard_Node, Jaccard_Edge) | Sprachübergreifende Strukturdivergenz |
| **CS** | \|V_Lehrbuch ∩ V_Lehrplan\| / \|V_Lehrplan\| | Lehrbuch-Lehrplan-Abdeckung |

---

## 🏆 10 Erkenntnisse (F1–F10)

| # | Erkenntnis | Beleg |
|---|-----------|-------|
| **F1** | CDS-Gipfel in der **Mittelstufe** (0,271) | 3 Sprachen unabhängig, 574 Konzepte |
| **F2** | **3,7× Abfall** von Mittel- zur Oberstufe | 0,271 → 0,073 |
| **F3** | HDS ≤ **8** (Mittel 0,40); 83% sind Wurzeln | Mathematik ist ein flaches Netz |
| **F4** | **ZH–DE** Divergenz am höchsten (LDS=0,907) | ZH–EN am niedrigsten (0,802) |
| **F5** | LDS ist **themenspezifisch** | ~0,2 Variation innerhalb von Paaren |
| **F6** | **Physik**-Gipfel in der **Grundschule** (0,222) | Beide folgen "früh integrieren, spät differenzieren" |
| **F7** | Physik hat **2,1× tiefere** Ketten | HDS Mittel 0,85 vs 0,40 |
| **F8** | **Chemie**-Gipfel in der Mittelstufe (0,042) | MINT-Dichtemuster ist universell |
| **F9** | **Coverage Score** variiert stark | NRW 34%, UK 82%, US 76% |
| **F10** | Coverage-Verläufe zeigen **Systemphilosophie** | UK ↑ 53→90% (prüfungsgetrieben); NRW ↘ 50→31% (Spezialisierung) |

---

## 📊 Datensatz

| Fach | Konzepte | Beziehungen | Lehrbücher | Sprachen | Lehrplan-Coverage |
|------|:--------:|:-----------:|:----------:|:--------:|:-----------------:|
| **Mathematik** | 574 | 3.538 | 68 | ZH/EN/DE | NRW 34% · UK 82% · US 76% |
| **Physik** | 366 | 383 | 94 Ausgaben | ZH/EN/DE | NRW 38% |
| **Chemie** | 220 | 215 | 18 Ausgaben | ZH/EN/DE | NRW 36% |
| **Gesamt** | **1.160+** | **4.100+** | **180+** | **3 Sprachen** | **4 Systeme** |

---

## ✅ Extraktionsqualität

**92 Goldstandard-Annotationen** über 2 Domänen und 3 Sprachen:

| Domäne | ZH F1 | DE F1 | EN F1 | Gesamt | n |
|--------|:-----:|:-----:|:-----:|:------:|:-:|
| **Soziale Konzepte** | **0,974** | **0,949** | **0,882** | **0,939** | 72 |
| **Mathematik** | 0,857 | 0,506 | 0,711 | 0,674 | 20 |
| **Alle** | **0,974** | **0,949** | **0,882** | **0,939** | **92** |

---

## 🚀 Schnellstart

```bash
# 1. Einrichten
git clone https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph.git
cd BWKI-2026-LinguaGraph
pip install openai numpy
export BAILIAN_API_KEY="Ihr-API-Key"

# 2. Extraktion validieren
python scripts/batch_process_responses.py --gold-only
python scripts/evaluate_gold.py

# 3. Analyse durchführen
python scripts/compute_lds_from_db.py
```

---

## 📜 Literatur

- Novak & Cañas (2008) — *The theory underlying concept maps and how to construct them*
- Ausubel (1963) — *The psychology of meaningful verbal learning*
- Schmidt et al. (2001) — *Why schools matter: A cross-national comparison of curriculum and learning*
- Liang & Heckmann (2013) — Comparing German and Chinese mathematics textbooks
- Boroditsky (2001) — *Does language shape thought?*
- OECD (2023) — *Education at a Glance*

---

## 📚 Literatur

### Wissenschaftliche Publikationen

| # | Quelle | Relevanz |
|---|--------|----------|
| 1 | **Novak, J. D. & Cañas, A. J.** (2008). *The theory underlying concept maps.* | Grundlegend für die Konzeptkarten-Theorie von CDS/HDS |
| 2 | **Ausubel, D. P.** (1963). *The psychology of meaningful verbal learning.* | Assimilationstheorie — Wissen ist strukturiert, nicht aufgelistet |
| 3 | **Schmidt, W. H. et al.** (2001). *Why schools matter* (TIMSS). | Lehrplankohärenz — Inspiration für Coverage Score |
| 4 | **Liang, L. L. & Heckmann, K.** (2013). Vergleich deutscher und chinesischer Mathematiklehrbücher. ZDM, 45(6). | Methodik zum länderübergreifenden Lehrbuchvergleich |
| 5 | **Boroditsky, L.** (2001). *Does language shape thought?* Cognitive Psychology, 43(1). | Sprachliche Relativität — Kontext der Forschungsfrage |
| 6 | **Siew, C. S. Q.** (2019). *Network science in education.* Springer. | Netzwerkanalyse kognitiver/edu kativer Strukturen |
| 7 | **Ain, Q. T., Chatti, M. A., & Qussa, H.** (2025). *Automated educational KG construction.* arXiv. | EKG-Pipeline-Methodik |
| 8 | **Alatrash, R., Chatti, M. A., & Wibowo, A.** (2025). *Prerequisite inference in EKGs.* arXiv. | Voraussetzungsinferenz — unterstützt HDS-Metrik |
| 9 | **OECD.** (2023). *Education at a Glance 2023.* OECD Publishing. | Ländervergleich der Curricula |
| 10 | **IEA.** (2019). *TIMSS 2019 International Results.* | Curriculum-Coverage-Methodik |

### Open-Source-Bibliotheken

| Bibliothek | Verwendung | Lizenz |
|------------|------------|--------|
| [openai/openai-python](https://github.com/openai/openai-python) | LLM-API-Client für Konzeptextraktion | MIT |
| [networkx/networkx](https://github.com/networkx/networkx) | Graphenkonstruktion und -analyse (CDS, HDS) | BSD-3 |
| [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) | Abbildungen (Fig 3-7) | PSF |
| [numpy/numpy](https://github.com/numpy/numpy) | Numerische Berechnungen, Ähnlichkeitsmetriken | BSD-3 |
| [Three.js](https://github.com/mrdoob/three.js) | 3D-Visualisierung (CognitiveSpace) | MIT |
| [Flask](https://github.com/pallets/flask) | Workbench-Webanwendung | BSD-3 |

### Lehrpläne (Primärquellen)

| Standard | Herausgeber |
|----------|-------------|
| Kernlehrplan Mathematik/Physik/Chemie NRW (Sek I 2019, Sek II 2023) | MSB NRW |
| UK National Curriculum (Mathematik, Naturwissenschaften) | DfE England |
| US Next Generation Science Standards (NGSS) | NGSS Lead States |
| Chinese National Curriculum Standards (数学/物理/化学) | MoE China |

### Lehrbuchkorpora

Lehrbuchinhalte für die Wissensgraphenkonstruktion (akademische Forschung, Fair Use).

**ZH** (33+ Verlage): 人教版, 沪科版, 北师大版, 苏科版, 粤教版, 鲁科版, Ma Wenwei, Cheng Shouzhu, Qi Anshen, Zhao Kaihua, Wang Zhicheng, Yang Fujia, Liang Kunmiao, Guo Shuohong, Zeng Jinyan

**EN** (34+ Verlage): Khan Academy, CK-12, AP Physics, IB, IGCSE, GCSE, Halliday Resnick Walker, Serway Jewett, Young Freedman, Griffiths, Kittel, Feynman Lectures

**DE** (27+ Verlage): Duden, Lambacher Schwere, Westermann, Cornelsen, Klett, Auer, Dorn-Bader, Kern, Thieme, Tipler, Demtröder, Jackson, Papula, Fischer

### Danksagungen

- **BWKI 2026** — Wettbewerbsplattform
- **Alibaba Cloud Bailian** — Kostenloses API-Kontingent (1M Tokens pro Modell)
- **LM Studio** — Lokale Inferenz (erste Entwicklung)

---

## 📜 Zitierung

```bibtex
@misc{linguaGraph2026,
  author = {Rongjing, J.},
  title = {LinguaGraph: Cross-Lingual Knowledge Structure Analysis Framework},
  year = {2026},
  publisher = {GitHub},
  journal = {BWKI 2026},
  url = {https://github.com/jjjjjjjjnnjnn/BWKI-2026-LinguaGraph}
}
```

---

## 📜 Lizenz & Compliance

- **Lizenz**: Alle Rechte vorbehalten — BWKI 2026 Wettbewerbsprojekt
- **Fremdcode**: Alle Open-Source-Bibliotheken unter MIT-, BSD-3- oder Apache-2.0-Lizenz.
- **Lehrbuchinhalte**: Ausschnitte als Fair Use für akademische Forschung. Vollständige Quellen in den Graph-Metadaten.
- **Datenschutz**: Alle Teilnehmerdaten anonymisiert. Keine personenbezogenen Daten im Repository. Siehe [](docs/ethics/) für DSGVO-Konformität.
- **KI-Ethik**: LLM-Nutzung auf Konzeptextraktion beschränkt. Extraktionsqualität an 92 Goldstandards validiert.
- **Lehrpläne**: Amtliche Dokumente für akademischen Vergleich. Urheberrecht bei den jeweiligen Behörden.