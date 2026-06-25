# LinguaGraph BWKI Demo Video Script

**Duration:** 3-5 minutes
**Format:** Screen recording + narration
**Language:** German (BWKI requirement)

---

## 0:00-0:30 — Personal Story (Personalismo)

**Visual:** Student sitting at desk, bilingual books visible

**Narration (DE):**
"Ich bin chinesischer Schüler in Deutschland. Jeden Tag erlebe ich, wie meine beiden Sprachen — Chinesisch und Deutsch — mein Denken beeinflussen. Wenn ich auf Chinesisch über 'Erfolg' nachdenke, denke ich an 'Familie' und 'Anstrengung'. Wenn ich auf Deutsch darüber nachdenke, denke ich an 'Leistung' und 'Karriere'. Das hat mich gefragt: Verändert Sprache tatsächlich unsere kognitive Struktur?"

**Narration (EN subtitle):**
"I am a Chinese student in Germany. Every day I experience how my two languages — Chinese and German — influence my thinking. When I think about 'success' in Chinese, I think of 'family' and 'effort'. When I think in German, I think of 'performance' and 'career'. This made me ask: Does language actually change our cognitive structure?"

---

## 0:30-1:00 — Research Question

**Visual:** Animated text: "Does language shape how we think?"

**Narration (DE):**
"Mein Forschungsprojekt LinguaGraph untersucht genau diese Frage. Wir verwenden KI, um kognitive Landkarten in drei Sprachen zu erstellen — Chinesisch, Englisch und Deutsch — und messen die strukturellen Unterschiede mit einem neuen Metric: dem Language Drift Score."

**Narration (EN subtitle):**
"My research project LinguaGraph investigates exactly this question. We use AI to create cognitive maps in three languages — Chinese, English, and German — and measure structural differences with a new metric: the Language Drift Score."

---

## 1:00-2:00 — Method + Demo

**Visual:** Cognitive City 3D visualization running

**Narration (DE):**
"Sehen Sie sich diese drei Städte an. Jede Stadt repräsentiert eine Sprache. Die Gebäude sind Konzepte — je höher, desto zentraler. Die Straßen sind Beziehungen zwischen Konzepten. Die Brücken verbinden äquivalente Konzepte über Sprachgrenzen hinweg.

Wenn wir 'Erfolg' betrachten:
- Die chinesische Stadt betont 'Anstrengung' und 'Familie'
- Die englische Stadt betont 'Achievement' und 'Opportunity'  
- Die deutsche Stadt betont 'Leistung' und 'Karriere'

Der Language Drift Score misst, wie unterschiedlich diese Strukturen sind. Für 'Erfolg' liegt er bei 0.27 — die höchste Differenz aller getesteten Konzepte."

**Visual:** Zoom into each city, highlight different buildings

---

## 2:00-3:00 — Results

**Visual:** LDS comparison chart + concept ranking

**Narration (DE):**
"Unsere Vorstudie analysierte 813 Texte in drei Sprachen. Das Ergebnis:

| Konzept | LDS |
|---------|-----|
| Erfolg | 0.27 |
| Verantwortung | 0.26 |
| Freiheit | 0.23 |
| Zuhause | 0.24 |

'Erfolg' zeigt die höchste sprachliche Differenz. Das bedeutet: Chinesen, Engländer und Deutsche haben strukturell unterschiedliche Vorstellungen von Erfolg.

Interessanterweise zeigt 'Zuhause' die niedrigste Differenz — ein universelles Konzept."

---

## 3:00-3:30 — Implications

**Visual:** Application scenarios

**Narration (DE):**
"Die Implikationen sind vielfältig:
1. Bildung: Zweisprachige Schüler könnten verschiedene kognitive Frameworks nutzen
2. Internationale Kommunikation: 'Erfolg' bedeutet nicht dasselbe in jeder Kultur
3. KI-Entwicklung: Sprachmodelle sollten kulturelle Unterschiede berücksichtigen"

---

## 3:30-4:00 — Future Work + Closing

**Visual:** Questionnaire preview + future roadmap

**Narration (DE):**
"Als nächstes führen wir eine experimentelle Studie mit 30 Muttersprachlern durch, um zu validieren, dass unsere KI-Messungen echte kognitive Unterschiede widerspiegeln.

Mein Ziel ist es zu zeigen: Sprache ist nicht nur ein Werkzeug zum Kommunizieren — sie formt tatsächlich unsere Denkweise."

**Visual:** LinguaGraph logo + "Thank you"

---

## Recording Checklist

- [ ] Screen recording of Cognitive City (localhost:8080)
- [ ] Zoom into each city (ZH/EN/DE)
- [ ] Show LDS bars updating
- [ ] Show concept ranking chart
- [ ] Narration in German (with English subtitles)
- [ ] Total duration: 3-5 minutes
- [ ] Export: 1080p, H.264

## Technical Setup

```bash
# Start visualization
cd C:\Users\rongj\Desktop\linguagraph
python -m http.server 8080 --directory visualization

# Open browser
# http://localhost:8080

# Record with OBS or similar
# Window capture: Chrome/Firefox
# Audio: Microphone for narration
```
