# LinguaGraph — BWKI 2026 Ideenanmeldung

> **Deadline**: 28. Juni 2026
> **Einreichung**: Über das BWKI-Portal (idee.bw-ki.de)
> **Team**: Jiajun Rong (Einzelteilnahme)

---

## 1. Projektname (max. 60 Zeichen)

```
LinguaGraph — Wie Sprache das Denken formt
```

> Zeichen: 44/60 ✅

---

## 2. Beschreibung eurer Projektidee (max. 1000 Zeichen)

```
Sprache prägt, wie wir die Welt organisieren — aber lässt sich dieser Effekt
messen? LinguaGraph ist ein KI-Projekt, das untersucht, ob verschiedene
Sprachen (Chinesisch, Deutsch, Englisch) zu unterschiedlichen kognitiven
Strukturen führen.

Kerninnovation: Der Language Drift Score (LDS) — ein Metrik, der kognitive
Graphen aus mehrsprachigen Antworten vergleicht. Anders als herkömmliche
Ansätze analysiert LDS die Struktur von Konzeptnetzwerken.

Ablauf:
1. Probanden beantworten Fragen zu sozialen Themen (Freiheit,
   Gerechtigkeit, Verantwortung, Erfolg, Familie) in ihrer Muttersprache
2. Eine KI extrahiert Konzepte und Beziehungen aus Antworten
3. Daraus werden kognitive Graphen konstruiert
4. LDS vergleicht die Graphen über Sprachgrenzen hinweg
5. Eine 3D-Visualisierung macht Unterschiede sichtbar

Erste Ergebnisse mit Wikipedia-Korpora zeigen systematische Unterschiede:
Chinesisch betont kollektive Werte, Deutsch formale Strukturen,
Englisch individualistische Analyse.
```

> Zeichen: ~970/1000 ✅

---

## 3. Woher bekommt ihr eure Daten? (max. 1000 Zeichen)

```
Die Studie verwendet drei Datenquellen:

1. KORPUS-DATEN (bereits vorhanden):
   - Wikipedia-Artikel zu Freiheit, Gerechtigkeit, Verantwortung, Erfolg
     und Familie in Chinesisch, Deutsch und Englisch (CC-BY-SA 4.0)
   - 15 Lehrbuchtexte aus dem deutschen Bildungssystem

2. SIMULATIONSDATEN (bereits vorhanden):
   - 300 KI-generierte Antworten mit Persona-Prompts (GPT-4.1-mini),
     die verschiedene kulturelle Perspektiven simulieren
   - Gekennzeichnet als "Computational Baseline" (nicht menschlich)

3. MENSCHLICHE DATEN (in Planung):
   - 60+ Probanden (20 Chinesisch, 20 Deutsch, 20 Englisch)
   - Rekrutierung über Schulen und Online-Plattformen
   - 15 offene Fragen zu sozialen Themen
   - Vollständig anonymisiert (kein Name, keine E-Mail, keine IP)
   - DSGVO-konform mit Einwilligungsformularen in drei Sprachen
```

> Zeichen: ~970/1000 ✅

---

## 4. Datei Anhang (Optional, max 10MB)

| Datei | Größe | Beschreibung |
|------|-------|-------------|
| `submission/idea/Cognitive_City_Screenshot.png` | ⬜ | 3D Cognitive City Screenshot (Three.js) |
| `submission/idea/LDS_Diagramm.png` | ⬜ | Pipeline-Übersichtsdiagramm |

---

## 5. BWKI Bewertungskriterien — Check

| Kriterium | Adressiert in |
|-----------|---------------|
| **Praktische Relevanz & Innovationskraft** | LDS ist der erste Metrik, der kognitive Strukturen auf Grafik-Ebene über Sprachen vergleicht. |
| **Eingesetzte Methode des ML** | LLM-gestützte Konzeptextraktion (GPT-4.1-mini / Qwen3-8B), Graph-Algorithmen (NetworkX) |
| **Ergebnis & Eigenleistung** | Komplette Pipeline selbst entwickelt (GitHub: 1145+ commits, 44 Python-Module) |
| **Kritische Reflexion** | Gate Review mit 5 Audit-Layern durchgeführt. Limitationen dokumentiert. |
| **Präsentation (Video Pitch)** | ⬜ Wird separat vorbereitet |

---

## 6. Nächste Schritte

- [ ] Screenshot der Cognitive City erstellen
- [ ] Pipeline-Übersichtsdiagramm erstellen
- [ ] Finale Textprüfung (Rechtschreibung, Grammatik)
- [ ] **Einreichung bis 28.06.2026**
- [ ] Vollständige Projekt-Einreichung bis 20.09.2026
