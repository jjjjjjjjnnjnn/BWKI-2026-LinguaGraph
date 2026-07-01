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

### 2.3 Concept Mapping und Wissensorganisation

Die theoretische Grundlage der Wissensstrukturanalyse geht auf Ausubels Assimilationstheorie des sinnvollen Lernens (1963) zurück, die argumentiert, dass Wissen hierarchisch und nicht als isolierte Fakten organisiert ist [12]. Novak und Cañas (2008) operationalisierten diese Theorie durch Concept Mapping und zeigten, dass Wissensstrukturen als propositionale Netzwerke externalisiert werden können [13]. Ihr Rahmenwerk liegt den CDS- und HDS-Metriken in LinguaGraph zugrunde: Der Concept Density Score erfasst die Vernetztheit von Konzepten innerhalb einer Wissensdomäne, während der Hierarchy Depth Score die Tiefe der Voraussetzungsketten misst.

Jüngste Fortschritte haben die automatische Generierung von Concept Maps ermöglicht. Schwach überwachte Ansätze mittels Graphtranslation (2021) [14] und generative LLM-basierte Methoden (2025) [15] haben groß angelegtes Concept Mapping praktikabel gemacht. LinguaGraph unterscheidet sich von diesen Ansätzen durch seine mehrsprachige Ausrichtung: Anstatt Concept Maps für eine einzelne Sprache zu generieren, konstruieren wir parallele Wissensgraphen für Chinesisch, Deutsch und Englisch und ermöglichen so einen sprachübergreifenden Strukturvergleich.

### 2.4 Sprachübergreifende Wissensgraph-Ausrichtung

Die sprachübergreifende Wissensgraph-Ausrichtung zielt darauf ab, äquivalente Entitäten und Relationen sprachübergreifend zu identifizieren. Frühe Arbeiten von McGillivray et al. (2016) schlugen multilinguale Wissensgraph-Embeddings für die sprachübergreifende Ausrichtung vor [16]. Nachfolgende Forschung entwickelte Methoden zur Entitätsausrichtung mittels adversarialem Training [17], Subgraph-Netzwerken [18] und Co-Training mit Entitätsbeschreibungen [19].

Diese ausrichtungsfokussierten Ansätze unterscheiden sich grundlegend von LinguaGraphs Zielsetzung. Die Ausrichtungsforschung fragt: *Wie lassen sich äquivalente Konzepte sprachübergreifend abgleichen?* LinguaGraph fragt: *Welche strukturellen Unterschiede verbleiben bei gegebenen abgeglichenen Konzepten zwischen sprachspezifischen Wissensorganisationen?* Die LDS-Metrik erfasst diese verbleibenden strukturellen Unterschiede — die nach der Konzeptausrichtung fortbestehende Divergenz — die von der bestehenden sprachübergreifenden KG-Forschung nicht systematisch quantifiziert wurde.

### 2.5 Forschungslücke

Während jeder dieser Forschungsstränge unabhängig Aspekte der Wissensstrukturanalyse untersucht hat, integriert keine bestehende Arbeit:

1. **Automatische Wissensgraphkonstruktion** aus mehrsprachigen Lehrbuchinhalten
2. **Systematischer Vergleich** von Wissensstrukturen über Sprachen hinweg
3. **Quantitative Metriken** (LDS, CDS, HDS) für den Strukturvergleich
4. **Curriculumsbezogene Analyse**, die Lehrbuchwissensgraphen mit offiziellen Curriculumsstandards vergleicht

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
