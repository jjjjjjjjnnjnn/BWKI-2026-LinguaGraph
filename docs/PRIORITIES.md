# LinguaGraph — Prioritäten & Roadmap

> **Stand:** 2026-07-01 · Nächster Meilenstein: Vollständige Einreichung (21. September)

---

## 🥇 Aktuelle Prioritäten

### Stufe 1: Paper + Experimente (Jul–Aug)

| Aufgabe | Status | Anmerkung |
|---------|:------:|-----------|
| LDS 正式定義 v3 | ✅ Fertig | `docs/lds_formal_definition.md` |
| OSF 预注册 | ✅ Fertig | `docs/osf_preregistration.md` |
| 论文撰写 | 🔶 ~80% | 主要章节完整，需语言统一 (DE为主) |
| 人类实验 N=8→30 | 🔶 **Critical Path** | 调查前端 ✅, 招募 ❌ |
| ΔLDS 分析 | 🔶 部分 (`scripts/analyze_human_lds.py`) | 等待 N≥30 数据 |
| 黄金数据集 20→50 | ❌ 未开始 | E4 里程碑 |

### Stufe 2: 论文提交准备 (Aug–Sep)

```text
Paper DE 语言统一
图表嵌入 → PDF 生成
Poster / Präsentation 准备
```

### Stufe 3: Finale Einreichung (Deadline 21. September)

```text
Paper finalisieren
Poster / Präsentation vorbereiten
Einreichung auf bw-ki.de
```

---

## 📊 Ressourcenverteilung (Empfohlen Jul)

```text
40%  Paper schreiben + DE Übersetzung
30%  Probanden-Rekrutierung
15%  Ergebnisse analysieren + Charts
10%  Visualisierung / UI polieren
 5%  Gold Dataset erweitern
```

---

## 🔮 Nach BWKI

- **Model Merging & Fine-Tuning** — Qwen2.5-1.5B + LoRA + TIES + GGUF
- Multi-Agent Orchestrierung
- Knowledge Base (RAG) Integration

---

## ⛔ Was wir NICHT tun (jetzt)

- ❌ Model trainieren / fusionieren
- ❌ Neue Metriken erfinden (LDS ist frozen)
- ❌ Pipeline umbauen
- ❌ Concept Mapping erweitern
- ❌ Neue Corpora sammeln (语料扩展已停止)

---

## 📋 Nächste konkrete Schritte

```
Sofort:
1. 🔴 论文 DE 语言统一 (04_discussion, 05_conclusion → DE)
2. 🔴 删除过时文件 (03_results_text.md ✅)
3. 🔶 编写招募材料 (ZH/EN/DE)
4. 🔶 部署调查问卷到 GitHub Pages
5. 🔶 通过学校/微信渠道启动招募

Nach Rekrutierung:
6. ΔLDS 计算 + 分析
7. Paper 图表嵌入
8. PDF/LaTeX 论文生成
```
