## 2. Verwandte Arbeiten

Dieser Abschnitt verortet LinguaGraph in vier Forschungssträngen: pädagogische Wissensgraphen, Curriculumanalyse und -vergleich, Concept Mapping und kognitive Struktur sowie sprachübergreifende Wissensintegration.

### 2.1 Pädagogische Wissensgraphen

Die Konstruktion von Wissensgraphen aus Bildungsressourcen hat in den letzten Jahren bedeutende Fortschritte erfahren. Yao et al. (2019) schlugen Joint Embedding Learning für pädagogische Wissensgraphen vor und zeigten, dass Konzeptbeziehungen automatisch aus Curriculumsdokumenten abgeleitet werden können [1]. Zhao, Sun und Xu (2022) entwickelten EDUKG, einen heterogenen K-12-Bildungswissensgraphen, der mehrere Fächer umfasst, und demonstrierten die Machbarkeit einer groß angelegten Wissensorganisation auf Curriculumniveau [2].

Am relevantesten für LinguaGraph ist die Arbeit von Ain, Chatti und Qussa (2025), die eine optimierte Pipeline zur automatischen Konstruktion pädagogischer Wissensgraphen entwickelten [3]. Ihr Ansatz verwendet Large Language Models zur Konzeptextraktion, ähnlich unserer MIMO-Prompt-Methodik. Eine Folgestudie verglich Top-Down- und Bottom-Up-Konstruktionsansätze und stellte fest, dass die Bottom-Up-Extraktion aus Lehrbuchinhalten eine vollständigere Konzeptabdeckung liefert [4]. LinguaGraph übernimmt einen Bottom-Up-Ansatz, erweitert ihn jedoch um sprachübergreifende Ausrichtung — eine Dimension, die in bestehenden EKG-Pipelines fehlt.

Alatrash, Chatti und Wibowo (2025) befassten sich speziell mit der Inferenz von Voraussetzungsbeziehungen in pädagogischen Wissensgraphen und schlugen einen multikriteriellen Ansatz vor, der textuelle, strukturelle und taxonomische Signale berücksichtigt [5]. Ihre Methode fließt unmittelbar in die HDS-Metrik unseres Frameworks ein, die die Tiefe von Voraussetzungsketten als Proxy für die Wissenshierarchie misst.

### 2.2 Curriculumanalyse und -vergleich

Der länderübergreifende Curriculumsvergleich ist ein Eckpfeiler der internationalen Bildungsforschung. Das TIMSS-Rahmenwerk (Trends in International Mathematics and Science Study) bietet eine systematische Methodik zum Vergleich von Curricula über Länder hinweg, einschließlich der Dimensionen Curriculumintention, -implementierung und -ergebnis [6]. Die OECD-PISA-Studien analysieren in ähnlicher Weise, wie Curriculumsstrukturen Lernergebnisse beeinflussen [7].

Spezifische Vergleiche zwischen deutschen und chinesischen Mathematikcurricula wurden von Liang und Heckmann (2013) durchgeführt, die Lehrbuchaufgaben analysierten und systematische Unterschiede in Aufgabenkomplexität und Darstellungsstil feststellten [8]. Fan, Zhu und Miao (2013) erweiterten dies auf einen breiteren länderübergreifenden Vergleich von Lehrbuchaufgaben [9]. Während diese Studien sich auf Aufgaben- oder Inhaltsebene konzentrieren, führt LinguaGraph einen Graphenvergleich ein — den Language Drift Score (LDS) — der strukturelle Unterschiede erfasst, die eine oberflächliche Inhaltsanalyse übersieht.

Der kürzlich veröffentlichte Kernlehrplan NRW (2019, 2023) für das deutsche Gymnasium im Fach Mathematik bietet eine formale kompetenzbasierte Curriculumsstruktur [10]. Das chinesische Pendant, der *Yiwu Jiaoyu Shuxue Kecheng Biaozhun* (2022) und der *Putong Gaozhong Shuxue Kecheng Biaozhun* (2017), definieren in ähnlicher Weise Lernprogressionen und Inhaltsstandards [11]. LinguaGraph ist nach unserem Kenntnisstand das erste System, das diese Curriculumsstandards in strukturierte Wissensgraphen für den direkten sprachübergreifenden Vergleich überführt.

Zur institutionellen Einordnung stützen wir uns auf öffentlich dokumentierte Governance-Unterschiede (als Kontext, nicht als getestete Ursache): Das deutsche System ist föderal organisiert — primäre Zuständigkeit der Länder, koordiniert über die KMK, Bundesrolle via BMBF [28]; das chinesische System ist hochzentralisiert unter dem MoE mit nationaler Lehrbuchzulassung und Prüfungskopplung (Gaokao) [29]. Die TIMSS-2023-Enzyklopädie dokumentiert länderspezifische Curriculumspolitiken systematisch [30]; die TIMSS-2023-Insights-Reihe untersucht explizit, inwieweit curriculare Vorgaben im Unterricht umgesetzt werden und wie dies mit Leistung zusammenhängt [31]; OECD *Education at a Glance 2025* liefert vergleichbare Systemkennzahlen (u. a. Deutschland: 4,4 % des BIP für Bildung) [32]. Diese Quellen stützen die Governance-Hypothese (F10) als institutionellen Kontext; die Unterrichts-Implementierungskette bleibt ungetestet.

### 2.3 Concept Mapping und Wissensorganisation

Die theoretische Grundlage der Wissensstrukturanalyse geht auf Ausubels Assimilationstheorie des sinnvollen Lernens (1963) zurück, die argumentiert, dass Wissen hierarchisch und nicht als isolierte Fakten organisiert ist [12]. Novak und Cañas (2008) operationalisierten diese Theorie durch Concept Mapping und zeigten, dass Wissensstrukturen als propositionale Netzwerke externalisiert werden können [13]. Ihr Rahmenwerk liegt den CDS- und HDS-Metriken in LinguaGraph zugrunde: Der Concept Density Score erfasst die Vernetztheit von Konzepten innerhalb einer Wissensdomäne, während der Hierarchy Depth Score die Tiefe der Voraussetzungsketten misst.

Jüngste Fortschritte haben die automatische Generierung von Concept Maps ermöglicht. Schwach überwachte Ansätze mittels Graphtranslation (2021) [14] und generative LLM-basierte Methoden (2025) [15] haben groß angelegtes Concept Mapping praktikabel gemacht. LinguaGraph unterscheidet sich von diesen Ansätzen durch seine mehrsprachige Ausrichtung: Anstatt Concept Maps für eine einzelne Sprache zu generieren, konstruieren wir parallele Wissensgraphen für Chinesisch, Deutsch und Englisch und ermöglichen so einen sprachübergreifenden Strukturvergleich.

### 2.4 Sprachübergreifende Wissensgraph-Ausrichtung

Die sprachübergreifende Wissensgraph-Ausrichtung zielt darauf ab, äquivalente Entitäten und Relationen sprachübergreifend zu identifizieren. Frühe Arbeiten von McGillivray et al. (2016) schlugen multilinguale Wissensgraph-Embeddings für die sprachübergreifende Ausrichtung vor [16]. Nachfolgende Forschung entwickelte Methoden zur Entitätsausrichtung mittels adversarialem Training [17], Subgraph-Netzwerken [18] und Co-Training mit Entitätsbeschreibungen [19].

Diese ausrichtungsfokussierten Ansätze unterscheiden sich grundlegend von LinguaGraphs Zielsetzung. Die Ausrichtungsforschung fragt: *Wie lassen sich äquivalente Konzepte sprachübergreifend abgleichen?* LinguaGraph fragt: *Welche strukturellen Unterschiede verbleiben bei gegebenen abgeglichenen Konzepten zwischen sprachspezifischen Wissensorganisationen?* Die LDS-Metrik erfasst diese verbleibenden strukturellen Unterschiede — die nach der Konzeptausrichtung fortbestehende Divergenz — die von der bestehenden sprachübergreifenden KG-Forschung nicht systematisch quantifiziert wurde.

Die systematische Übersichtsarbeit von Chen et al. (2026) zu cross-lingualem Transfer für Knowledge-Graph-Akquisition bestätigt, dass sprachbias-bedingte Alignierungsschwierigkeiten und geringe Transfereffizienz fortbestehende Kernherausforderungen sind — trotz mehrsprachiger Embeddings und LLMs [25]. Dies verortet unsere P2-Recheck-Einschränkung (Alignierungs-Labels als partielle Artefaktquelle, s. §8.14.5) als bekanntes Domänenproblem, nicht als Einzelfall. Han et al. (unter Begutachtung) schlagen komplementär eine Transfer-Lokalisierungs-Ebene vor: Universelles Wissen *soll* konvergieren, kulturell situiertes Wissen *soll* divergieren — hohe Transferleistung um den Preis kultureller Auslöschung („cultural erasure") ist die unerwünschte Quadrant [26]. Diese Unterscheidung rahmt unseren Zentralbefund (institutionelle Konvergenz vs. kulturelle Divergenz) als erwartbares Muster statt als Anomalie. Dass Mehrsprachigkeit nicht Multikulturalität impliziert, zeigen Wang et al. (2025) empirisch über WVS-Opinionverteilungen in vier Sprachen [27].

### 2.5 Multilinguale Wertausrichtung von LLMs

Ein wachsender Forschungsstrang untersucht, ob Large Language Models (LLMs) menschliche Werte sprachübergreifend konsistent vertreten. WorldValuesBench (Zhao et al., 2024) etablierte eine groß angelegte Benchmark zur Vorhersage kultureller Wertantworten aus dem World Values Survey [20]. Xu et al. (2024) zeigten, dass Wertkonzepte in LLMs über 16 Sprachen hinweg als lineare Richtungen im Repräsentationsraum darstellbar sind [21]. Agarwal et al. (2024) wiesen nach, dass die moralische Bewertung von LLMs von der Prompt-Sprache abhängt [22]. Farid et al. (2025) deckten über die Übersetzung zweier Moral-Benchmarks in fünf Sprachen systematische kreuzlinguistische Fehlausrichtungen auf [23]; Lee et al. (2026) schlugen mit MET ein theoriebasiertes, kulturbewusstes mehrsprachiges Moral-Entscheidungsbenchmark vor [24].

Gemeinsam messen diese Arbeiten die **Auswahl** von Werten über Sprachen hinweg — durch Vorhersage, Klassifikation oder Rating. LinguaGraph ergänzt diese Perspektive um ein **strukturelles** Maß: Während bestehende multilinguale Wert- und Moral-Benchmarks (WorldValuesBench, 2024; One Model, Many Morals, 2025; MET, 2026) die *Auswahl* von Werten über Sprachen hinweg messen, erfasst LinguaGraph mit dem LDS die *strukturelle Organisation* von Wertkonzepten (Knoten + Kanten) — ein komplementäres, bisher ungemessenes Maß. Das LLM-as-Subject-Design (Within-Subject, §5) isoliert dabei die Sprache als einzige Variable; die Replikation über 51 Messungen (§5.10) zeigt, dass die strukturelle Divergenz von Wertkonzepten über Sprachpaare hinweg breit reproduzierbar und kulturell gerichtet ist (DE Autonomie/Regeln vs. ZH Raum/Anspruch). Keine der bestehenden Arbeiten misst diese strukturelle Divergenz systematisch.

Als Hintergrund — nicht als Evidenz dieser Studie — ist dokumentiert, dass KI-generierte Texte messbare linguistische Marker tragen: Fu und Yang (2025) vergleichen maschinell identifizierte vs. menschlich inferierte Prädiktoren [33]; RoBERTa-basierte Detektion erreicht 96,1 % Genauigkeit mit interpretierbaren stilistischen Unterschieden (LIME/SHAP) [34]; eine Großstudie über 27 LLMs × 10 Domänen systematisiert 284 interpretierbare Merkmale und deren domänenübergreifende Generalisierung [35]; ein Survey synthetisiert die verstreuten Befunde zu AIGT-vs-HWT-Merkmalen [36]. Diese Literatur stützt die allgemeine Beobachtung, dass KI-Texte systematische Stilmerkmale aufweisen — sie ersetzt keine eigene Messung im Chinesischen und wird hier nicht als Befund beansprucht.

### 2.6 Forschungslücke

Während jeder dieser Forschungsstränge unabhängig Aspekte der Wissensstrukturanalyse untersucht hat, integriert keine bestehende Arbeit:

1. **Automatische Wissensgraphkonstruktion** aus mehrsprachigen Lehrbuchinhalten
2. **Systematischer Vergleich** von Wissensstrukturen über Sprachen hinweg
3. **Quantitative Metriken** (LDS, CDS, HDS) für den Strukturvergleich
4. **Curriculumsbezogene Analyse**, die Lehrbuchwissensgraphen mit offiziellen Curriculumsstandards vergleicht
5. **Strukturelle (statt auswahlbasierte) Messung der Wertdivergenz mehrsprachiger LLMs** — die Trennung von Konzeptauswahl und Konzeptorganisation über Sprachen hinweg

LinguaGraph schließt diese Lücke durch eine integrierte Pipeline von der Lehrbuchextraktion bis zur sprachübergreifenden Strukturanalyse, mit validierten Metriken, die Unterschiede in der Wissensorganisation auf mehreren Ebenen erfassen — über Sprachen (LDS), Bildungsstufen (CDS) und hierarchische Tiefe (HDS) hinweg.

---

## Literaturverzeichnis

[1] Yao, S., Wang, R., & Sun, S. (2019). Joint Embedding Learning of Educational Knowledge Graphs. arXiv:1911.08776.

[2] Zhao, B., Sun, J., & Xu, B. (2022). EDUKG: a Heterogeneous Sustainable K-12 Educational Knowledge Graph. arXiv:2210.12228.

[3] Ain, Q. U., Chatti, M. A., & Qussa, J. (2025). An Optimized Pipeline for Automatic Educational Knowledge Graph Construction. arXiv:2509.05392.

[4] Ain, Q. U., Chatti, M. A., & Shakhshir, A. (2025). Top-Down vs. Bottom-Up Approaches for Automatic EKG Construction. arXiv:2505.10069.

[5] Alatrash, R., Chatti, M. A., & Wibowo, N. (2025). Inferring Prerequisite Knowledge Concepts in EKGs. arXiv:2509.05393.

[6] IEA. (1995–2023). Trends in International Mathematics and Science Study (TIMSS). International Association for the Evaluation of Educational Achievement.

[7] OECD. (Various). PISA Curriculum Analysis and Education at a Glance. OECD Publishing.

[8] Liang, S., & Heckmann, K. (2013). A comparison of German and Chinese mathematics textbooks. ZDM, 45(5), 743–756.

[9] Fan, L., Zhu, Y., & Miao, Z. (2013). A comparative study on mathematics textbook problems across countries. ICMT.

[10] MSB NRW. (2019). Kernlehrplan Mathematik für das Gymnasium (Sek I). Ministerium für Schule und Bildung NRW.

[11] MoE China. (2022). Yiwu Jiaoyu Shuxue Kecheng Biaozhun [Compulsory Education Mathematics Curriculum Standards]. Ministry of Education, PRC.

[12] Ausubel, D. P. (1963). The Psychology of Meaningful Verbal Learning. Grune & Stratton.

[13] Novak, J. D., & Cañas, A. J. (2008). The Theory Underlying Concept Maps. IHMC.

[14] Weakly Supervised Concept Map Generation through Task-Guided Graph Translation. (2021). AAAI.

[15] Generative Large Language Models for Knowledge Representation: A Systematic Review of Concept Map Generation. (2025). arXiv.

[16] McGillivray, B., et al. (2016). Multilingual Knowledge Graph Embeddings for Cross-lingual Knowledge Alignment. IJCAI.

[17] Cross-lingual Entity Alignment with Adversarial Kernel Embedding. (2021). AAAI.

[18] SubGraph Networks based Entity Alignment for Cross-lingual Knowledge Graph. (2022). arXiv.

[19] Co-training Embeddings of Knowledge Graphs and Entity Descriptions for Cross-lingual Entity Alignment. (2018). arXiv.

[20] Zhao, W., Mondal, D., Tandon, N., et al. (2024). WorldValuesBench: A Large-Scale Benchmark Dataset for Multi-Cultural Value Awareness of Language Models. arXiv:2404.16308.

[21] Xu, S., Dong, W., Guo, Z., et al. (2024). Exploring Multilingual Concepts of Human Value in Large Language Models: Is Value Alignment Consistent, Transferable and Controllable across Languages? arXiv:2402.18120.

[22] Agarwal, U., Tanmay, K., Khandelwal, A., et al. (2024). Ethical Reasoning and Moral Value Alignment of LLMs Depend on the Language we Prompt them in. arXiv:2404.18460.

[23] Farid, S., Lin, J., Chen, Z., et al. (2025). One Model, Many Morals: Uncovering Cross-Linguistic Misalignments in Computational Moral Reasoning. arXiv:2509.21443.

[24] Lee, A., Kwon, R., Zhang, Y., et al. (2026). MET: Theory-Grounded and Culture-Aware Multilingual Moral Reasoning. arXiv:2607.11736.

[25] Chen, W.-L., Zhou, K.-Q., Sarkheyli-Hägele, A., et al. (2026). Cross-lingual transfer learning for knowledge graph acquisition: Paradigms, resources and challenges. Expert Systems with Applications, 303, 130434. https://doi.org/10.1016/j.eswa.2025.130434.

[26] Han, H., Agrawal, S., & Briakou, E. (unter Begutachtung). Rethinking Cross-lingual Alignment: Balancing Transfer and Cultural Erasure in Multilingual LLMs. arXiv:2510.26024.

[27] Wang, Y., et al. (2025). Multilingual != Multicultural: Evaluating Gaps Between Multilingual Capabilities and Cultural Alignment in LLMs. arXiv:2502.16534.

[28] KMK. Ständige Konferenz der Kultusminister der Länder; BMBF-Rahmenrolle. https://www.kmk.org/en/index.html; Eurydice Germany.

[29] Ministry of Education of the PRC. Nationale Lehrbuchzulassung und Gaokao-Kopplung. http://en.moe.gov.cn/.

[30] IEA. (2023). TIMSS 2023 Encyclopedia: Education Policy and Curriculum in Mathematics and Science. https://timss2023.org/encyclopedia/.

[31] TIMSS & PIRLS International Study Center. TIMSS 2023 Insights: Curriculum Alignment report (curricular specifications → classroom implementation → achievement). https://timss.bc.edu/latest-news/timss-2023-insights-curriculum-alignment.html.

[32] OECD. (2025). Education at a Glance 2025 (Germany profile: 4.4% of GDP). OECD Publishing. https://www.oecd.org/en/publications/education-at-a-glance-2025_1a3543e2-en/germany_fa91d155-en.html.

[33] Fu, K., & Yang, X. (2025). Linguistic Markers of AI-Generated Text: A Comparative Analysis of Machine-Identified and Human-Inferred Predictors. AMCIS 2025 TREOs. https://aisel.aisnet.org/treos_amcis2025/1.

[34] Classifying human vs. AI text with machine learning and explainable transformer models. (2025). Scientific Reports. https://www.nature.com/articles/s41598-025-27377-z.

[35] A Systematic Analysis of Linguistic Features in AI-Generated Text (27 LLMs × 10 domains, 284 features). (2026). arXiv:2606.04177.

[36] Linguistic Characteristics of AI-Generated Text: A Survey. (2025). arXiv:2510.05136.

[37] Markus, H. R., & Kitayama, S. (1991). Culture and the self: Implications for cognition, emotion, and motivation. Psychological Review, 98(2), 224–253.

[38] Hofstede, G. (2001). Culture's Consequences: Comparing Values, Behaviors, Institutions and Organizations Across Nations (2nd ed.). Sage. (Original work published 1980.)

[39] Nisbett, R. E. (2003). The Geography of Thought: How Asians and Westerners Think Differently … and Why. Free Press.
