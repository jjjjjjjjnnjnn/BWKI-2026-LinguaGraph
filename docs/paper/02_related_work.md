## 2. Verwandte Arbeiten

Dieser Abschnitt verortet LinguaGraph in vier Forschungssträngen: pädagogische Wissensgraphen, Curriculumanalyse und -vergleich, Concept Mapping und kognitive Struktur sowie sprachübergreifende Wissensintegration.

### 2.1 Pädagogische Wissensgraphen

Die Konstruktion von Wissensgraphen aus Bildungsressourcen hat in den letzten Jahren bedeutende Fortschritte erfahren. Yao et al. (2019) schlugen Joint Embedding Learning für pädagogische Wissensgraphen vor und zeigten, dass Konzeptbeziehungen automatisch aus Curriculumsdokumenten abgeleitet werden können [1]. Zhao, Sun und Xu (2022) entwickelten EDUKG, einen heterogenen K-12-Bildungswissensgraphen, der mehrere Fächer umfasst, und demonstrierten die Machbarkeit einer groß angelegten Wissensorganisation auf Curriculumniveau [2].

Am relevantesten für LinguaGraph ist die Arbeit von Ain, Chatti und Qussa (2025), die eine optimierte Pipeline zur automatischen Konstruktion pädagogischer Wissensgraphen entwickelten [3]. Ihr Ansatz verwendet Large Language Models zur Konzeptextraktion, ähnlich unserer MIMO-Prompt-Methodik. Eine Folgestudie verglich Top-Down- und Bottom-Up-Konstruktionsansätze und stellte fest, dass die Bottom-Up-Extraktion aus Lehrbuchinhalten eine vollständigere Konzeptabdeckung liefert [4]. LinguaGraph übernimmt einen Bottom-Up-Ansatz, erweitert ihn jedoch um sprachübergreifende Ausrichtung — eine Dimension, die in bestehenden EKG-Pipelines fehlt.

Alatrash, Chatti und Wibowo (2025) befassten sich speziell mit der Inferenz von Voraussetzungsbeziehungen in pädagogischen Wissensgraphen und schlugen einen multikriteriellen Ansatz vor, der textuelle, strukturelle und taxonomische Signale berücksichtigt [5]. Ihre Methode fließt unmittelbar in die HDS-Metrik unseres Frameworks ein, die die Tiefe von Voraussetzungsketten als Proxy für die Wissenshierarchie misst.

### 2.2 Curriculumanalyse und -vergleich

Der länderübergreifende Curriculumsvergleich ist ein Eckpfeiler der internationalen Bildungsforschung. Das TIMSS-Rahmenwerk (Trends in International Mathematics and Science Study) bietet eine systematische Methodik zum Vergleich von Curricula über Länder hinweg, einschließlich der Dimensionen Curriculumintention, -implementierung und -ergebnis [6]. Die OECD-PISA-Studien analysieren in ähnlicher Weise, wie Curriculumsstrukturen Lernergebnisse beeinflussen [7].

Spezifische Vergleiche zwischen deutschen und chinesischen Mathematikcurricula wurden von Liang und Heckmann (2013) durchgeführt, die Lehrbuchaufgaben analysierten und systematische Unterschiede in Aufgabenkomplexität und Darstellungsstil feststellten [8]. Fan, Zhu und Miao (2013) erweiterten dies auf einen breiteren länderübergreifenden Vergleich von Lehrbuchaufgaben [9]. Während diese Studien sich auf Aufgaben- oder Inhaltsebene konzentrieren, führt LinguaGraph einen Graphenvergleich ein — den Language Drift Score (LDS) — der strukturelle Unterschiede erfasst, die eine oberflächliche Inhaltsanalyse übersieht.

Der kürzlich veröffentlichte Kernlehrplan NRW (2019, 2023) für das deutsche Gymnasium im Fach Mathematik bietet eine formale kompetenzbasierte Curriculumsstruktur [10]. Das chinesische Pendant, der *Yiwu Jiaoyu Shuxue Kecheng Biaozhun* (2022) und der *Putong Gaozhong Shuxue Kecheng Biaozhun* (2017), definieren in ähnlicher Weise Lernprogressionen und Inhaltsstandards [11]. LinguaGraph überführt diese Curriculumsstandards in strukturierte Wissensgraphen für den direkten sprachübergreifenden Vergleich (Preliminary, Stand Sept. 2026, ohne systematischen Prior-Art-Vergleich — kein First-Nachweis).

Zur institutionellen Einordnung stützen wir uns auf öffentlich dokumentierte Governance-Unterschiede (als Kontext, nicht als getestete Ursache): Das deutsche System ist föderal organisiert — primäre Zuständigkeit der Länder, koordiniert über die KMK, Bundesrolle via BMBF [28]; das chinesische System ist hochzentralisiert unter dem MoE mit nationaler Lehrbuchzulassung und Prüfungskopplung (Gaokao) [29]. Die TIMSS-2023-Enzyklopädie dokumentiert länderspezifische Curriculumspolitiken systematisch [30]; die TIMSS-2023-Insights-Reihe untersucht explizit, inwieweit curriculare Vorgaben im Unterricht umgesetzt werden und wie dies mit Leistung zusammenhängt [31]; OECD *Education at a Glance 2025* liefert vergleichbare Systemkennzahlen (u. a. Deutschland: 4,4 % des BIP für Bildung) [32]. Diese Quellen stützen die Governance-Hypothese (F10) als institutionellen Kontext; die Unterrichts-Implementierungskette bleibt ungetestet.

### 2.3 Concept Mapping und Wissensorganisation

Die theoretische Grundlage der Wissensstrukturanalyse geht auf Ausubels Assimilationstheorie des sinnvollen Lernens (1963) zurück, die argumentiert, dass Wissen hierarchisch und nicht als isolierte Fakten organisiert ist [12]. Novak und Cañas (2008) operationalisierten diese Theorie durch Concept Mapping und zeigten, dass Wissensstrukturen als propositionale Netzwerke externalisiert werden können [13]. Ihr Rahmenwerk liegt den CDS- und HDS-Metriken in LinguaGraph zugrunde: Der Concept Density Score erfasst die Vernetztheit von Konzepten innerhalb einer Wissensdomäne, während der Hierarchy Depth Score die Tiefe der Voraussetzungsketten misst.

Jüngste Fortschritte haben die automatische Generierung von Concept Maps ermöglicht. Schwach überwachte Ansätze mittels Graphtranslation (2021) [14] und generative LLM-basierte Methoden (2025) [15] haben groß angelegtes Concept Mapping praktikabel gemacht. LinguaGraph unterscheidet sich von diesen Ansätzen durch seine mehrsprachige Ausrichtung: Anstatt Concept Maps für eine einzelne Sprache zu generieren, konstruieren wir parallele Wissensgraphen für Chinesisch, Deutsch und Englisch und ermöglichen so einen sprachübergreifenden Strukturvergleich.

### 2.4 Sprachübergreifende Wissensgraph-Ausrichtung

Die sprachübergreifende Wissensgraph-Ausrichtung zielt darauf ab, äquivalente Entitäten und Relationen sprachübergreifend zu identifizieren. Frühe Arbeiten von McGillivray et al. (2016) schlugen multilinguale Wissensgraph-Embeddings für die sprachübergreifende Ausrichtung vor [16]. Nachfolgende Forschung entwickelte Methoden zur Entitätsausrichtung mittels adversarialem Training [17], Subgraph-Netzwerken [18] und Co-Training mit Entitätsbeschreibungen [19].

Diese ausrichtungsfokussierten Ansätze unterscheiden sich grundlegend von LinguaGraphs Zielsetzung. Die Ausrichtungsforschung fragt: *Wie lassen sich äquivalente Konzepte sprachübergreifend abgleichen?* LinguaGraph fragt: *Welche strukturellen Unterschiede verbleiben bei gegebenen abgeglichenen Konzepten zwischen sprachspezifischen Wissensorganisationen?* Die LDS-Metrik erfasst diese verbleibenden strukturellen Unterschiede — die nach der Konzeptausrichtung fortbestehende Divergenz — die von der bestehenden sprachübergreifenden KG-Forschung nicht systematisch quantifiziert wurde.

Die systematische Übersichtsarbeit von Chen et al. (2026) zu cross-lingualem Transfer für Knowledge-Graph-Akquisition bestätigt, dass sprachbias-bedingte Alignierungsschwierigkeiten und geringe Transfereffizienz fortbestehende Kernherausforderungen sind — trotz mehrsprachiger Embeddings und LLMs [25]. Dies verortet unsere P2-Recheck-Einschränkung (Alignierungs-Labels als partielle Artefaktquelle, s. §8.14.5) als bekanntes Domänenproblem, nicht als Einzelfall. Han et al. (unter Begutachtung) schlagen komplementär eine Transfer-Lokalisierungs-Ebene vor: Universelles Wissen *soll* konvergieren, kulturell situiertes Wissen *soll* divergieren — hohe Transferleistung um den Preis kultureller Auslöschung („cultural erasure") ist die unerwünschte Quadrant [26]. Diese Unterscheidung rahmt unseren Zentralbefund (institutionelle Konvergenz vs. kulturelle Divergenz) als erwartbares Muster statt als Anomalie. Dass Mehrsprachigkeit nicht Multikulturalität impliziert, zeigen Wang et al. (2025) empirisch über WVS-Opinionverteilungen in vier Sprachen [27].

Für die Interpretation von Restdivergenzen nach der Ausrichtung ist relevant, dass Ausrichtung und Transfer nur korreliert, nicht identisch sind: Gaschi et al. (2023) zeigen über Sprachen, Modelle und Seeds, dass der Alignierungsgrad mit cross-lingualem Transfer signifikant zusammenhängt, Realignment aber nur unter Bedingungen (u. a. ferne Sprachpaare, kleinere Modelle) verlässlich hilft [63]. Hämmerl et al. (2024) systematisieren weak vs. strong alignment und argumentieren, dass maximale Ausrichtung sprachspezifische Information kostet — ein Trade-off zwischen sprachneutralen und sprachspezifischen Anteilen ist demnach konstitutiv [64]. Für LinguaGraph stützt dies die Lesart des LDS als erwartbare Residualgröße (Preliminary): Verbleibende Strukturdivergenz nach Konzeptabgleich ist kein Ausrichtungsversagen, sondern theoretisch vorhergesagter Rest — die kausale Attribution (institutionell vs. kulturell) bleibt dabei ungetestet.

### 2.5 Multilinguale Wertausrichtung von LLMs

Ein wachsender Forschungsstrang untersucht, ob Large Language Models (LLMs) menschliche Werte sprachübergreifend konsistent vertreten. WorldValuesBench (Zhao et al., 2024) etablierte eine groß angelegte Benchmark zur Vorhersage kultureller Wertantworten aus dem World Values Survey [20]. Xu et al. (2024) zeigten, dass Wertkonzepte in LLMs über 16 Sprachen hinweg als lineare Richtungen im Repräsentationsraum darstellbar sind [21]. Agarwal et al. (2024) wiesen nach, dass die moralische Bewertung von LLMs von der Prompt-Sprache abhängt [22]. Farid et al. (2025) deckten über die Übersetzung zweier Moral-Benchmarks in fünf Sprachen systematische kreuzlinguistische Fehlausrichtungen auf [23]; Lee et al. (2026) schlugen mit MET ein theoriebasiertes, kulturbewusstes mehrsprachiges Moral-Entscheidungsbenchmark vor [24].

Gemeinsam messen diese Arbeiten die **Auswahl** von Werten über Sprachen hinweg — durch Vorhersage, Klassifikation oder Rating. LinguaGraph ergänzt diese Perspektive um ein **strukturelles** Maß: Während bestehende multilinguale Wert- und Moral-Benchmarks (WorldValuesBench, 2024; One Model, Many Morals, 2025; MET, 2026) die *Auswahl* von Werten über Sprachen hinweg messen, erfasst LinguaGraph mit dem LDS die *strukturelle Organisation* von Wertkonzepten (Knoten + Kanten) — ein komplementäres, bisher ungemessenes Maß. Das LLM-as-Subject-Design (Within-Subject, §5) isoliert dabei die Sprache als einzige Variable; die Replikation (59 Messungen / 54 Identitäten, §5.10, Verfügbarkeitsstichprobe, keine Mehrfachtest-Korrektur) zeigt: ZH-DE 59/59 signifikant, 9/177 EN-Tests n.s. (R1/Distill) — Richtung Preliminary, modell-/paarabhängig. Keine der bestehenden Arbeiten misst diese strukturelle Divergenz systematisch.

Dass englisch-haltige Paare schwächere Signale tragen (§5.10: alle 9 nicht-signifikanten Tests betreffen ZH-EN/DE-EN), ist mit der Englisch-Zentriertheit aktueller Modelle konsistent: MEXA evaluiert gezielt englisch-zentrierte LLMs über cross-linguale Alignierung [43]; im EN↔ZH-Transfer überwiegt negativer Transfer vom Englischen aufs Chinesische [44]; cross-linguale faktische Inkonsistenz ist ein dokumentierter Mechanismus multilingualer Modelle [45]. Englisch wirkt als Trainings-Hub mit generalisierteren, weniger differenzierten Konzeptrepräsentationen — schwächere EN-Paardivergenz ist damit theoretisch erwartbar, kein Gegenbefund.

Zur Designfrage (Between- vs. Within-Subject, §4 vs. §5): Within-Subject-Designs erreichen bei gleicher Effektstärke mit deutlich kleineren Stichproben diagnostische Power als Between-Subject-Designs [40][41] — die menschliche N=15-Null unter Between-Subject ist daher auch power-analytisch erwartbar (s. §8.10), kein Beleg für Abwesenheit.

Als Hintergrund — nicht als Evidenz dieser Studie — ist dokumentiert, dass KI-generierte Texte messbare linguistische Marker tragen: Fu und Yang (2025) vergleichen maschinell identifizierte vs. menschlich inferierte Prädiktoren [33]; RoBERTa-basierte Detektion erreicht 96,1 % Genauigkeit mit interpretierbaren stilistischen Unterschieden (LIME/SHAP) [34]; eine Großstudie über 27 LLMs × 10 Domänen systematisiert 284 interpretierbare Merkmale und deren domänenübergreifende Generalisierung [35]; ein Survey synthetisiert die verstreuten Befunde zu AIGT-vs-HWT-Merkmalen [36]. Diese Literatur stützt die allgemeine Beobachtung, dass KI-Texte systematische Stilmerkmale aufweisen — sie ersetzt keine eigene Messung im Chinesischen und wird hier nicht als Befund beansprucht.

Methodische Qualifizierung — Kontamination (Preliminary-Hintergrund, keine eigene Messung): Befunde aus Gewichtsvektoren dürfen nicht ohne Kontaminationsvorbehalt als Strukturwissen interpretiert werden. Sainz et al. (2023) definieren Kontaminationsgrade und zeigen, dass Test-Split-Training zu systematischer Leistungsüberschätzung und Fehlschlüssen führt [55]. Yang et al. (2023) weisen nach, dass n-Gramm-Dedup paraphrasierte und übersetzte Wiederholungen nicht erkennt und ein 13B-Modell mit solchen Varianten Benchmark-Werte auf GPT-4-Niveau erreichen kann [56]. Zhu et al. (2024) schlagen mit Inference-Time Decontamination eine operativ nutzbare Gegenmaßnahme vor (GSM8K −22,9 %, MMLU −19,0 % Inflationsreduktion) [57]. Für einen künftigen Gewichts-vs.-Lehrbuch-Vergleich folgt daraus: Ohne semantische Dekontaminationskontrolle bleibt jede Erklärung auf der Gewichtsseite (P4) vorläufig.

### 2.6 Repräsentationsgeometrie und Ähnlichkeitsmaße

Die Lesbarkeit von Konzepten aus Gewichtsvektoren setzt eine Geometrieannahme voraus (Preliminary-Hintergrund, keine eigene Messung). Park et al. (2024) formalisieren die Linear-Representation-Hypothese kontrafaktisch und zeigen an LLaMA-2, dass Konzeptrichtungen als lineare Sonden bzw. Steuervektoren fungieren — wobei die Wahl des inneren Produkts (kausales vs. euklidisches) über Cosine- und Projektionsbefunde entscheidet [58]. Hernandez und Andreas (2021) belegen für ELMo/BERT, dass syntaktisch-semantische Merkmale in niedrigdimensionalen, hierarchisch verschachtelten und kausal manipulierbaren Unterräumen kodiert sind [59]. Godey et al. (2024) weisen nach, dass Anisotropie eine intrinsische Eigenschaft von Self-Attention ist — auch jenseits von Long-Tail-Cross-Entropy — sodass Cosine-Vergleiche ohne Zentrierung oder Whitening systematisch überhöht sind [60]. Jede künftige Gewichts-vs.-Lehrbuch-Geometrie muss daher die Metrik (inneres Produkt, Zentrierung) vorab deklarieren.

Für den Strukturvergleich zweier Repräsentationsräume (z. B. RDM Mensch-Lehrbuch vs. RDM Gewichtsraum) ist Centered Kernel Alignment der geprüfte Standard: Kornblith et al. (2019) zeigen, dass CCA bei Dimension größer Stichprobe versagt und CKA demgegenüber Schichtkorrespondenzen über Initialisierungen hinweg robust identifiziert [61]. Williams (2024) beweist, dass RSA über Dissimilaritätsmatrizen nach Mittelwertzentrierung mit CKA (und CCA) weitgehend äquivalent ist — RSA und CKA können daher als wechselseitige Robustheitsprüfungen dienen [62]. Für LinguaGraph bedeutet dies: Ein künftiger Gewichts-vs.-Human-Vergleich sollte lineares CKA als Hauptmaß mit RSA als Replikation berichten (P2-Triangulation).

### 2.7 Forschungslücke

Während jeder dieser Forschungsstränge unabhängig Aspekte der Wissensstrukturanalyse untersucht hat, integriert keine bestehende Arbeit:

1. **Automatische Wissensgraphkonstruktion** aus mehrsprachigen Lehrbuchinhalten
2. **Systematischer Vergleich** von Wissensstrukturen über Sprachen hinweg
3. **Quantitative Metriken** (LDS, CDS, HDS) für den Strukturvergleich
4. **Curriculumsbezogene Analyse**, die Lehrbuchwissensgraphen mit offiziellen Curriculumsstandards vergleicht
5. **Strukturelle (statt auswahlbasierte) Messung der Wertdivergenz mehrsprachiger LLMs** — die Trennung von Konzeptauswahl und Konzeptorganisation über Sprachen hinweg
6. **Geometrisch triangulierter Gewichts-vs.-Lehrbuch-Vergleich** — lineare Konzeptgeometrie mit deklarierter Metrik [58][59][60], CKA/RSA-Triangulation [61][62], Kontaminationskontrolle [55][56][57] und Residualdeutung nach Ausrichtung [63][64] (sämtlich Preliminary-Hintergrund, keine Befunde dieser Studie)

LinguaGraph schließt diese Lücke durch eine integrierte Pipeline von der Lehrbuchextraktion bis zur sprachübergreifenden Strukturanalyse, mit frozen-v3-Metriken (Preliminary; Gold Developing C9b, s. §2.8/§8.7), die Unterschiede in der Wissensorganisation auf mehreren Ebenen schätzen — über Sprachen (LDS), Bildungsstufen (CDS) und hierarchische Tiefe (HDS) hinweg.

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

[10] MSB NRW. (2019; Neufassung 2023). Kernlehrplan Mathematik für das Gymnasium (Sek I). Ministerium für Schule und Bildung NRW.

[11] MoE China. (2017; 2022). Putong Gaozhong Shuxue Kecheng Biaozhun (2017) / Yiwu Jiaoyu Shuxue Kecheng Biaozhun (2022) [Senior High / Compulsory Education Mathematics Curriculum Standards]. Ministry of Education, PRC.

[12] Ausubel, D. P. (1963). The Psychology of Meaningful Verbal Learning. Grune & Stratton.

[13] Novak, J. D., & Cañas, A. J. (2008). The Theory Underlying Concept Maps. IHMC.

[14] Lu, J., Dong, X., & Yang, C. (2023). Weakly Supervised Concept Map Generation through Task-Guided Graph Translation (GT-D2G). IEEE Transactions on Knowledge and Data Engineering, 35(10), 10871–10883. https://doi.org/10.1109/tkde.2023.3252588.

[15] Zhai, X. (2025). Generative Large Language Models for Knowledge Representation: A Systematic Review of Concept Map Generation. arXiv:2509.14554.

[16] Chen, M., Tian, Y., Yang, M., & Zaniolo, C. (2017). Multilingual Knowledge Graph Embeddings for Cross-lingual Knowledge Alignment (MTransE). Proc. IJCAI 2017, 1511–1517. https://doi.org/10.24963/ijcai.2017/209.

[17] Trisedya, B. D., Qi, J., & Zhang, R. (2019). Entity Alignment between Knowledge Graphs Using Attribute Embeddings. Proc. AAAI 2019, 33(01), 297–304.

[18] Yu, S., Zhang, S., Zhang, J., Zhou, J., Xuan, Q., Li, B., & Hu, X. (2022). SubGraph Networks based Entity Alignment for Cross-lingual Knowledge Graph. arXiv:2205.03557.

[19] Chen, M., Tian, Y., Chang, K.-W., Skiena, S., & Zaniolo, C. (2018). Co-training Embeddings of Knowledge Graphs and Entity Descriptions for Cross-lingual Entity Alignment. Proc. IJCAI 2018, 3998–4004. arXiv:1806.06478.

[20] Zhao, W., Mondal, D., Tandon, N., et al. (2024). WorldValuesBench: A Large-Scale Benchmark Dataset for Multi-Cultural Value Awareness of Language Models. arXiv:2404.16308.

[21] Xu, S., Dong, W., Guo, Z., et al. (2024). Exploring Multilingual Concepts of Human Value in Large Language Models: Is Value Alignment Consistent, Transferable and Controllable across Languages? arXiv:2402.18120.

[22] Agarwal, U., Tanmay, K., Khandelwal, A., et al. (2024). Ethical Reasoning and Moral Value Alignment of LLMs Depend on the Language we Prompt them in. arXiv:2404.18460.

[23] Farid, S., Lin, J., Chen, Z., et al. (2025). One Model, Many Morals: Uncovering Cross-Linguistic Misalignments in Computational Moral Reasoning. arXiv:2509.21443.

[24] Lee, A., Kwon, R., Zhang, Y., et al. (2026). MET: Theory-Grounded and Culture-Aware Multilingual Moral Reasoning. arXiv:2607.11736.

[25] Chen, W.-L., Zhou, K.-Q., Sarkheyli-Hägele, A., et al. (2026). Cross-lingual transfer learning for knowledge graph acquisition: Paradigms, resources and challenges. Expert Systems with Applications, 303, 130434. https://doi.org/10.1016/j.eswa.2025.130434.

[26] Han, H., Agrawal, S., & Briakou, E. (unter Begutachtung). Rethinking Cross-lingual Alignment: Balancing Transfer and Cultural Erasure in Multilingual LLMs. arXiv:2510.26024.

[27] Wang, Y., et al. (2025). Multilingual != Multicultural: Evaluating Gaps Between Multilingual Capabilities and Cultural Alignment in LLMs. arXiv:2502.16534.

[28] KMK / BMBF. (o. J.). Ständige Konferenz der Kultusminister der Länder; Rahmenrolle des BMBF. https://www.kmk.org/en/index.html; Eurydice Germany. (Zugriff Sept. 2026.)

[29] Ministry of Education of the PRC. (o. J.). Nationale Lehrbuchzulassung und Gaokao-Kopplung. http://en.moe.gov.cn/. (Zugriff Sept. 2026.)

[30] IEA. (2023). TIMSS 2023 Encyclopedia: Education Policy and Curriculum in Mathematics and Science. https://timss2023.org/encyclopedia/.

[31] TIMSS & PIRLS International Study Center. (2024). TIMSS 2023 Insights: Curriculum Alignment report (curricular specifications → classroom implementation → achievement). https://timss.bc.edu/latest-news/timss-2023-insights-curriculum-alignment.html. (Zugriff Sept. 2026.)

[32] OECD. (2025). Education at a Glance 2025 (Germany profile: 4.4% of GDP). OECD Publishing. https://www.oecd.org/en/publications/education-at-a-glance-2025_1a3543e2-en/germany_fa91d155-en.html.

[33] Fu, K., & Yang, X. (2025). Linguistic Markers of AI-Generated Text: A Comparative Analysis of Machine-Identified and Human-Inferred Predictors. AMCIS 2025 TREOs. https://aisel.aisnet.org/treos_amcis2025/1.

[34] Masih, A., Afzal, B., et al. (2025). Classifying human vs. AI text with machine learning and explainable transformer models. Scientific Reports, 15, 43310. https://www.nature.com/articles/s41598-025-27377-z.

[35] El Attar, Y., Dönmez, E., Maurer, M., & Falenska, A. (2026). A Systematic Analysis of Linguistic Features in AI-Generated Text Detection Across Domains and Models (27 LLMs × 10 domains, 284 features). arXiv:2606.04177.

[36] Terčon, L., & Dobrovoljc, K. (2025). Linguistic Characteristics of AI-Generated Text: A Survey. arXiv:2510.05136.

[37] Markus, H. R., & Kitayama, S. (1991). Culture and the self: Implications for cognition, emotion, and motivation. Psychological Review, 98(2), 224–253.

[38] Hofstede, G. (2001). Culture's Consequences: Comparing Values, Behaviors, Institutions and Organizations Across Nations (2nd ed.). Sage. (Original work published 1980.)

[39] Nisbett, R. E. (2003). The Geography of Thought: How Asians and Westerners Think Differently … and Why. Free Press.

[40] Bellemare, C., Bissonnette, L., & Kröger, S. (2014). Statistical power of within- and between-subjects designs in economic experiments. IZA Discussion Paper No. 8583. https://docs.iza.org/dp8583.pdf.

[41] Seltman, H. J. (2018). Experimental Design and Analysis, Chapter 14: Within-Subjects Designs. Carnegie Mellon University. https://www.stat.cmu.edu/~hseltman/309/Book/chapter14.pdf.

[42] Sukiennik, N., Gao, C., Xu, F., & Li, Y. (2025). An Evaluation of Cultural Value Alignment in LLM. arXiv:2504.08863.

[43] Kargaran, A. H., Modarressi, A., Nikeghbal, N., Diesner, J., Yvon, F., & Schuetze, H. (2025). MEXA: Multilingual Evaluation of English-Centric LLMs via Cross-Lingual Alignment. Findings of ACL 2025, 27001–27023. https://aclanthology.org/2025.findings-acl.1385/.

[44] Zhou, Y., & Matusevych, Y. (2025). Curse of bilinguality: Evaluating monolingual and bilingual language models on Chinese linguistic benchmarks. Proc. GEM 2025. https://aclanthology.org/2025.gem-1.58/.

[45] Wang, M., Adel, H., Lange, L., Liu, Y., Nie, E., Strötgen, J., & Schuetze, H. (2025). Lost in Multilinguality: Dissecting Cross-lingual Factual Inconsistency in Transformer Language Models. Proc. ACL 2025, 5075–5094. https://aclanthology.org/2025.acl-long.253/.

[46] Fluss, R., Faraggi, D., & Reiser, B. (2005). Estimation of the Youden Index and its Associated Cutoff Point. Biometrical Journal, 47(4), 458–472. https://doi.org/10.1002/bimj.200410135.

[47] Binz, M., & Schulz, E. (2023). Using cognitive psychology to understand GPT-3. PNAS, 120(6), e2218523120. https://doi.org/10.1073/pnas.2218523120.

[48] Hagendorff, T., Fabi, S., & Kosinski, M. (2023). Human-like intuitive behavior and reasoning biases emerged in large language models but disappeared in ChatGPT. Nature Machine Intelligence, 5, 1163–1176. https://doi.org/10.1038/s42256-023-00740-0.

[49] Whorf, B. L. (1956). Language, Thought, and Reality. MIT Press.

[50] Lucy, J. A. (1997). Linguistic relativity. Annual Review of Anthropology, 26, 291–312.

[51] Winawer, J., Witthoft, N., Frank, M. C., Wu, L., Wade, A. R., & Boroditsky, L. (2007). Russian blues reveal effects of language on color discrimination. PNAS, 104(19), 7780–7785.

[52] Levinson, S. C. (1996). Language and space. Annual Review of Anthropology, 25, 353–382.

[53] Boroditsky, L. (2001). Does language shape thought? Mandarin and English speakers' conceptions of time. Cognitive Psychology, 43(2), 1–22.

[54] Schmidt, W. H., et al. (2001). Why Schools Matter: A Cross-National Comparison of Curriculum and Learning. Jossey-Bass.

[55] Sainz, O., Campos, J., García-Ferrero, I., Etxaniz, J., Lopez de Lacalle, O., & Agirre, E. (2023). NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for each Benchmark. Findings of EMNLP 2023, 10776–10787. https://doi.org/10.18653/v1/2023.findings-emnlp.722.

[56] Yang, S., Chiang, W.-L., Zheng, L., Gonzalez, J. E., & Stoica, I. (2023). Rethinking Benchmark and Contamination for Language Models with Rephrased Samples. Preprint. https://arxiv.org/abs/2311.04850.

[57] Zhu, Q., Cheng, Q., Peng, R., Li, X., Peng, R., Liu, T., Qiu, X., & Huang, X. (2024). Inference-Time Decontamination: Reusing Leaked Benchmarks for Large Language Model Evaluation. Findings of EMNLP 2024, 9113–9129. https://doi.org/10.18653/v1/2024.findings-emnlp.532.

[58] Park, K., Choe, Y. J., & Veitch, V. (2024). The Linear Representation Hypothesis and the Geometry of Large Language Models. Proc. ICML 2024, PMLR 235, 39643–39666. https://proceedings.mlr.press/v235/park24c.html.

[59] Hernandez, E., & Andreas, J. (2021). The Low-Dimensional Linear Geometry of Contextualized Word Representations. Proc. CoNLL 2021, 82–93. https://doi.org/10.18653/v1/2021.conll-1.7.

[60] Godey, N., Clergerie, É., & Sagot, B. (2024). Anisotropy Is Inherent to Self-Attention in Transformers. Proc. EACL 2024 (Vol. 1, Long Papers), 35–48. https://doi.org/10.18653/v1/2024.eacl-long.3.

[61] Kornblith, S., Norouzi, M., Lee, H., & Hinton, G. (2019). Similarity of Neural Network Representations Revisited. Proc. ICML 2019, PMLR 97, 3519–3529. https://proceedings.mlr.press/v97/kornblith19a.html.

[62] Williams, A. H. (2024). Equivalence between representational similarity analysis, centered kernel alignment, and canonical correlations analysis. Proc. UniReps Workshop 2024, PMLR 285, 10–23. https://proceedings.mlr.press/v285/williams24a.html.

[63] Gaschi, F., Cerda, P., Rastin, P., & Toussaint, Y. (2023). Exploring the Relationship between Alignment and Cross-lingual Transfer in Multilingual Transformers. Findings of ACL 2023, 3020–3042. https://doi.org/10.18653/v1/2023.findings-acl.189.

[64] Hämmerl, K., Libovický, J., & Fraser, A. (2024). Understanding Cross-Lingual Alignment — A Survey. Findings of ACL 2024. Preprint. https://arxiv.org/abs/2404.06228.
