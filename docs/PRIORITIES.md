# LinguaGraph — Prioritäten & Roadmap

> **Stand:** 2026-06-18 · Nächster Meilenstein: BWKI Ideenanmeldung (28. Juni)

---

## 🥇 Aktuelle Prioritäten

### Stufe 1: BWKI Ideenanmeldung (Deadline 28. Juni)

| Aufgabe | Status | Wer |
|---------|--------|-----|
| Beschreibungstext (960/1000) | ✅ Fertig | — |
| Datenquellen (820/1000) | ✅ Fertig | — |
| Pipeline-Diagramm (SVG) | ✅ Fertig | — |
| **Einreichen auf idee.bw-ki.de** | ❌ **Nicht geschehen** | **DU** |

→ **Priority #1:** Formular öffnen, Texte kopieren, Datei anhängen, absenden.

### Stufe 2: Human Data Pipeline (Juli–August)

```text
Probanden rekrutieren (20 ZH / 20 DE / 20 EN)
        ↓
Pilot (3+3+3) → Analyse → Adjust
        ↓
Hauptstudie (60 Probanden)
        ↓
Ergebnisse → LDS Vergleiche → Charts
```

### Stufe 3: Results Dashboard

```text
Automatisierte Pipeline:
Raw Data → Extraction → Graph → LDS → CI → Charts → Report
```

### Stufe 4: Finale Submission (Deadline 21. September)

```text
Paper schreiben (IMRaD)
Three.js Cognitive City finalisieren
Poster / Präsentation vorbereiten
```

---

## 📊 Ressourcenverteilung (Empfohlen)

```text
Nächste 2 Wochen:

40%  Pilot-Datenerhebung (3+3+3 Probanden)
25%  Results-Pipeline automatisieren
20%  Three.js / UI / Visualisierung
10%  Paper-Charts & Diagramme
 5%  Lokales Modell evaluieren (nur Benchmark)
```

---

## 🔮 Future Work (Phase 2 — nach BWKI)

- **Model Merging & Fine-Tuning** — Qwen2.5-1.5B + LoRA + TIES + GGUF
  - Vollständig dokumentiert in `docs/model_strategy.md`
  - Training Pipeline in `docs/training_pipeline.md`
  - Konfiguration in `config/training/`
  - Muss NICHT vor BWKI gemacht werden
- Multi-Agent Orchestrierung
- Knowledge Base (RAG) Integration

---

## ⛔ Was wir NICHT tun (jetzt)

- ❌ Model trainieren / fusionieren
- ❌ Neue Metriken erfinden (LDS ist frozen)
- ❌ Pipeline umbauen
- ❌ Concept Mapping erweitern

---

## 📋 Nächste konkrete Schritte

```
Sofort (heute):
1. Ideenanmeldung absenden (idee.bw-ki.de)

Nach Anmeldung:
2. Probanden-Rekrutierung planen (WhatsApp / Schule / WeChat)
3. 3 Pilot-Probanden finden (1 ZH, 1 DE, 1 EN)
4. Ethics Package drucken + Einverständnis einholen
5. Pilot-Durchlauf: Umfrage → Extraction → LDS → Report
6. Results Dashboard bauen
7. Three.js Stadt für Pilot-Daten rendern
```
