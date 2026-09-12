# LinguaGraph 鈥?BWKI 2026 Ideenanmeldung

> **Deadline**: 28. Juni 2026
> **Einreichung**: 脺ber das BWKI-Portal (idee.bw-ki.de)
> **Team**: Jiajun Rong (lead research & implementation) · Zhenxi Lan (funding & advisory)

---

## 1. Projektname (max. 60 Zeichen)

```
LinguaGraph 鈥?Wie Sprache das Denken formt
```

> Zeichen: 42/60 鉁?
---

## 2. Beschreibung eurer Projektidee (max. 1000 Zeichen)

```
Sprache pr盲gt, wie wir die Welt organisieren 鈥?aber l盲sst sich dieser
Effekt messen? LinguaGraph ist ein KI-Projekt, das untersucht, ob
verschiedene Sprachen zu unterschiedlichen kognitiven Strukturen f眉hren.

Kerninnovation ist der Language Drift Score (LDS), ein graphbasierter
脛hnlichkeitsindikator zur Quantifizierung sprach眉bergreifender
Unterschiede in Konzeptnetzwerken.

Ablauf:
1. Probanden beantworten Fragen zu sozialen Themen (Freiheit,
   Gerechtigkeit, Verantwortung, Erfolg, Familie)
2. Eine KI extrahiert Konzepte und Beziehungen aus Antworten
3. Daraus werden kognitive Graphen konstruiert
4. LDS vergleicht die Graphen 眉ber Sprachgrenzen hinweg
5. Eine 3D-Visualisierung macht Unterschiede sichtbar

Erste Analysen mit Wikipedia-Korpora deuten auf m枚gliche Unterschiede
hin: Chinesisch betont kollektive Werte, Deutsch formale Strukturen,
Englisch individualistische Analyse. Diese Hypothesen sollen in
einer geplanten Humanstudie 眉berpr眉ft werden.
```

> Zeichen: ~970/1000 鉁?
---

## 3. Woher bekommt ihr eure Daten? (max. 1000 Zeichen)

```
Die Studie verwendet drei Datenquellen:

1. KORPUS-DATEN (bereits vorhanden):
   - Wikipedia-Artikel zu Freiheit, Gerechtigkeit, Verantwortung, Erfolg
     und Familie in Chinesisch, Deutsch und Englisch (CC-BY-SA 4.0)
   - 15 analysierte Bildungstexte aus dem deutschen Schulsystem (nur fuer Forschungszwecke verwendet)

2. SIMULATIONSDATEN (bereits vorhanden):
   - Computational Baseline Dataset (300 simulierte Antworten) zur
     Methodenevaluation und als Vergleichsbasis f眉r sp盲tere
     Humanstudien 鈥?klar gekennzeichnet als KI-generiert

3. MENSCHLICHE DATEN (in Planung):
   - 60+ Probanden (20 Chinesisch, 20 Deutsch, 20 Englisch)
   - Rekrutierung 眉ber Schulen und Online-Plattformen
   - 15 offene Fragen zu sozialen Themen
   - Vollst盲ndig anonymisiert (kein Name, keine E-Mail, keine IP)
   - Datenerhebung gemaess DSGVO-Richtlinien mit informierter
     Einwilligung und anonymisierter Speicherung
```

> Zeichen: ~970/1000 鉁?
---

## 4. Datei Anhang (Optional, max 10MB)

| Datei | Gr枚脽e | Beschreibung |
|------|-------|-------------|
| `submission/idea/Cognitive_City_Screenshot.png` | 猬?| 3D Cognitive City Screenshot (Three.js) |
| `submission/idea/LDS_Diagramm.png` | 猬?| Pipeline-脺bersichtsdiagramm |

---

## 5. BWKI Bewertungskriterien 鈥?Check

| Kriterium | Adressiert in |
|-----------|---------------|
| **Praktische Relevanz & Innovationskraft** | LDS ist der erste Metrik, der kognitive Strukturen auf Grafik-Ebene 眉ber Sprachen vergleicht. |
| **Eingesetzte Methode des ML** | LLM-gest眉tzte Konzeptextraktion (GPT-4.1-mini / Qwen3-8B), Graph-Algorithmen (NetworkX) |
| **Ergebnis & Eigenleistung** | Komplette Pipeline selbst entwickelt (GitHub: 1145+ commits, 44 Python-Module) |
| **Kritische Reflexion** | Gate Review mit 5 Audit-Layern durchgef眉hrt. Limitationen dokumentiert. |
| **Pr盲sentation (Video Pitch)** | 猬?Wird separat vorbereitet |

---

## 6. N盲chste Schritte

- [ ] Screenshot der Cognitive City erstellen
- [ ] Pipeline-脺bersichtsdiagramm erstellen
- [ ] Finale Textpr眉fung (Rechtschreibung, Grammatik)
- [ ] **Einreichung bis 28.06.2026**
- [ ] Vollst盲ndige Projekt-Einreichung bis 20.09.2026


