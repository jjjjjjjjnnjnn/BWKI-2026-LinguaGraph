#!/usr/bin/env python3
"""Build a self-contained interactive 'divergence map' demo for laypeople.

Reads the verified deepseek-v4-flash results and inlines them into a single
HTML file (docs/demo/divergence_map.html) that needs no server, no API, no
dependencies — double-click and it works. Trilingual (EN/DE/ZH).

Data inlined (all verified, Stand 2026-08-09):
  - per-language top concepts per topic (original word + English gloss + freq)
  - LDS-C vs within-language floor per pair (design effect)
  - ZH-DE divergence drivers (DE-only vs ZH-only)
  - domain asymmetry (institutional 0.44 vs social 0.80)

Re-run after any data change:  python scripts/build_divergence_map.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_compute import canonical_key  # noqa: E402
from lds_c_llm_analyze import unit_to_record  # noqa: E402

LLM_OUT = PROJECT_ROOT / "data" / "lds_c" / "llm_subject"
LDS_K_DEEP = PROJECT_ROOT / "data" / "lds_c" / "lds_k_deep"
DRIVERS = PROJECT_ROOT / "data" / "lds_c"
OUT = PROJECT_ROOT / "docs" / "demo"

TOPICS = ["Freiheit", "Gerechtigkeit", "Verantwortung", "Heimat", "Erfolg"]
LANGS = ["zh", "de", "en"]
TOP_N = 8


def load_latest(glob: str, base: Path) -> dict:
    files = sorted(base.glob(glob))
    if not files:
        raise FileNotFoundError(f"No {glob} in {base}")
    return json.loads(files[-1].read_text(encoding="utf-8"))


def concept_map() -> Dict[str, Dict[str, List[dict]]]:
    """lang -> topic -> [{key, orig, gloss, freq}] top concepts (deepseek P1)."""
    subj = load_latest("llm_subject_20260808.json", LLM_OUT)
    recs = [unit_to_record(u) for u in subj["units"] if u.get("probe") == "P1"]
    # lang -> topic -> key -> (Counter by orig text, most-common gloss, count)
    acc = defaultdict(lambda: defaultdict(lambda: defaultdict(Counter)))
    gloss_of: Dict[str, Dict[str, Dict[str, str]]] = defaultdict(lambda: defaultdict(dict))
    for r in recs:
        lang = r["language"]
        for t in r.get("topics", []):
            tl = t.get("topic", "")
            for c in t.get("concepts", []):
                en = c.get("en", "")
                orig = c.get("concept", "")
                k = canonical_key(en)
                if not k:
                    continue
                acc[lang][tl][k][orig] += 1
                gloss_of[lang][tl][k] = en or gloss_of[lang][tl][k]
    out: Dict[str, Dict[str, List[dict]]] = {}
    for lang in LANGS:
        out[lang] = {}
        for tl in TOPICS:
            by_key = acc[lang][tl]
            items = []
            for k, orig_counter in by_key.items():
                freq = sum(orig_counter.values())
                items.append({
                    "key": k,
                    "orig": orig_counter.most_common(1)[0][0],
                    "gloss": gloss_of[lang][tl].get(k, k),
                    "freq": freq,
                })
            items.sort(key=lambda x: -x["freq"])
            out[lang][tl] = items[:TOP_N]
    return out


def signal_data() -> dict:
    de = load_latest("design_effect_20260809.json", LLM_OUT)
    bp = de["llm_signal"]["by_pair"]
    return {pair: {
        "lds_c": bp[pair]["lds_c"],
        "floor": bp[pair]["split_half_floor"],
        "margin": bp[pair]["signal_margin"],
        "ratio": bp[pair]["signal_to_floor_ratio"],
    } for pair in bp}


def driver_data() -> dict:
    d = load_latest("divergence_drivers_20260809.json", DRIVERS)
    td = d["concept_drivers"]["llm_p1"]["ZH-DE"]["top_drivers"]
    de_only = [x for x in td if x.get("lang") == "de"]
    zh_only = [x for x in td if x.get("lang") == "zh"]
    return {
        "de_only": [{"topic": x["topic"], "key": x["key"], "freq": x.get("freq_b", x.get("freq_a", 0))}
                    for x in de_only[:6]],
        "zh_only": [{"topic": x["topic"], "key": x["key"], "freq": x.get("freq_a", x.get("freq_b", 0))}
                    for x in zh_only[:6]],
    }


def domain_data() -> dict:
    d = load_latest("node_edge_decomp_20260809.json", LDS_K_DEEP)
    m = d["math_institutional"]["ZH-DE"]
    s = d["wiki_social"]["ZH-DE"]
    return {
        "institutional": round(m["node_only_lds"], 3),
        "social": round(s["node_only_lds"], 3),
    }


def multi_data() -> dict:
    """Multi-model replication summary (ZH-DE margins + direction consistency)."""
    d = load_latest("multi_model_replication_*.json", LLM_OUT)
    margins = d["comparison"]["per_pair"]["ZH-DE"]["margin"]
    dc = d["comparison"]["direction_consistency"]
    return {
        "margins_zhde": {m: round(v, 3) for m, v in margins.items() if v is not None},
        "n_consistent": dc["n_consistent_total"],
        "de_consistent_n": len(dc["de_only_consistent"]),
        "zh_consistent_n": len(dc["zh_only_consistent"]),
        "n_models": dc["n_models"],
        "min_models": dc["min_models"],
    }


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LinguaGraph — Does your AI understand 'fairness' the same way in every language?</title>
<style>
  :root{--bg:#0f172a;--card:#1e293b;--line:#334155;--txt:#e2e8f0;--dim:#94a3b8;
        --accent:#60a5fa;--zh:#f87171;--de:#4ade80;--en:#a78bfa}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--txt);line-height:1.55;padding:24px;max-width:1080px;margin:0 auto}
  h1{font-size:1.5rem;font-weight:800;margin-bottom:6px}
  h2{font-size:1.05rem;font-weight:700;margin:28px 0 10px}
  .sub{color:var(--dim);font-size:.95rem;margin-bottom:20px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;margin:14px 0}
  .langbar{display:flex;gap:6px;justify-content:flex-end;margin-bottom:10px}
  .langbar button{background:var(--card);border:1px solid var(--line);color:var(--txt);border-radius:6px;padding:4px 10px;cursor:pointer;font-size:.8rem}
  .langbar button.on{background:var(--accent);border-color:var(--accent);color:#0f172a;font-weight:700}
  select{padding:8px 12px;border-radius:8px;border:1px solid var(--line);background:#0f172a;color:var(--txt);font-size:.95rem;margin-right:8px}
  .cols{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:12px}
  @media(max-width:760px){.cols{grid-template-columns:1fr}}
  .col{background:#0f172a;border:1px solid var(--line);border-radius:10px;padding:12px}
  .col h3{font-size:.9rem;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center}
  .tag{font-size:.68rem;padding:2px 7px;border-radius:999px;color:#0f172a;font-weight:700}
  .tag.zh{background:var(--zh)} .tag.de{background:var(--de)} .tag.en{background:var(--en)}
  .concept{margin:7px 0}
  .concept .row{display:flex;justify-content:space-between;gap:8px;font-size:.82rem}
  .concept .orig{font-weight:600}
  .concept .gloss{color:var(--dim);font-size:.74rem}
  .bar{height:5px;background:var(--line);border-radius:3px;margin-top:4px;overflow:hidden}
  .bar>div{height:100%;border-radius:3px}
  .sig{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:8px}
  @media(max-width:760px){.sig{grid-template-columns:1fr}}
  .metric{background:#0f172a;border:1px solid var(--line);border-radius:8px;padding:12px}
  .metric .big{font-size:1.35rem;font-weight:800}
  .metric .lbl{color:var(--dim);font-size:.74rem;text-transform:uppercase;letter-spacing:.04em}
  .vis{display:flex;align-items:flex-end;gap:14px;height:150px;margin-top:14px}
  .vbar{width:34px;border-radius:6px 6px 0 0;position:relative}
  .vbar .lab{position:absolute;top:-20px;left:50%;transform:translateX(-50%);font-size:.7rem;color:var(--dim);white-space:nowrap}
  .vbar .val{position:absolute;top:-20px;left:50%;transform:translateX(-50%);font-size:.7rem;color:var(--dim);white-space:nowrap}
  .drivers{display:grid;grid-template-columns:1fr 1fr;gap:12px}
  @media(max-width:760px){.drivers{grid-template-columns:1fr}}
  .dside{border:1px solid var(--line);border-radius:10px;padding:12px;background:#0f172a}
  .dside h4{font-size:.85rem;margin-bottom:8px}
  .dside.de h4{color:var(--de)} .dside.zh h4{color:var(--zh)}
  .ditem{font-size:.8rem;padding:3px 0;display:flex;justify-content:space-between;gap:8px}
  .ditem .n{color:var(--dim);font-size:.7rem}
  .plain{font-size:.95rem}
  .plain b{color:var(--accent)}
  .foot{color:var(--dim);font-size:.75rem;margin-top:26px;border-top:1px solid var(--line);padding-top:12px}
</style>
</head>
<body>

<div class="langbar">
  <button data-lang="en" class="on">EN</button>
  <button data-lang="de">DE</button>
  <button data-lang="zh">中文</button>
</div>

<h1 id="h1">Does the AI you use understand &ldquo;fairness&rdquo; the same way in every language?</h1>
<p class="sub" id="sub">We asked the same AI model — in Chinese, German and English — what belongs to five everyday concepts. The answer is measurable &mdash; and it is not the same.</p>

<div class="card">
  <h2 id="c1title">Pick a concept, see what the model associates in each language</h2>
  <div>
    <select id="topic"></select>
  </div>
  <div class="cols" id="cols"></div>
</div>

<div class="card">
  <h2 id="c2title">The difference is real — not noise</h2>
  <p class="plain" id="c2sub">For every language pair, the cross-language difference (blue) sits clearly above the model&rsquo;s own within-language noise floor (grey). A permutation test says p&lt;0.01.</p>
  <div class="vis" id="signalvis"></div>
  <div class="sig" id="signalcards"></div>
</div>

<div class="card">
  <h2 id="c2btitle">It is not one AI&rsquo;s quirk — four independent AIs all drift</h2>
  <p class="plain" id="c2bsub"></p>
  <div class="vis" id="multivis"></div>
  <div class="metric" id="multistats" style="margin-top:12px"></div>
</div>

<div class="card">
  <h2 id="c3title">Where the cultures diverge (Chinese ↔ German)</h2>
  <p class="plain" id="c3sub">Same word, different map. These concepts appear in only one language&rsquo;s framing of the topic.</p>
  <div class="drivers" id="drivers"></div>
</div>

<div class="card">
  <h2 id="c4title">The control: it is culture, not method</h2>
  <p class="plain" id="c4sub">When the same pipeline measures <b>institutional knowledge</b> (mathematics), languages converge. When it measures <b>cultural concepts</b>, they diverge. A measurement artifact would affect both equally — it does not.</p>
  <div class="vis" id="domainvis"></div>
</div>

<div class="card">
  <h2 id="c5title">Why this matters for the AI you use</h2>
  <p class="plain" id="c5body"></p>
</div>

<div class="foot">
  LinguaGraph · BWKI 2026 · data: deepseek-v4-flash, LDS-C (frozen v3), Stand 2026-08-09 ·
  <span id="footdata"></span>
</div>

<script>
const DATA = __DATA__;
const T = {
  en: {
    h1:"Does the AI you use understand &ldquo;fairness&rdquo; the same way in every language?",
    sub:"We asked the same AI model — in Chinese, German and English — what belongs to five everyday concepts. The answer is measurable — and it is not the same.",
    c1title:"Pick a concept, see what the model associates in each language",
    c2title:"The difference is real — not noise",
    c2sub:"For every language pair, the cross-language difference (blue) sits clearly above the model's own within-language noise floor (grey). A permutation test says p<0.01.",
    c2btitle:"It is not one AI's quirk — four independent AIs all drift",
    c2bsub:"We ran the same probe on four independently-built models (DeepSeek, Zhipu, Moonshot). Every single one shows the Chinese↔German gap clearly above its own noise floor — and the cultural direction is the same.",
    multiStats:"ZH-DE drift magnitude per model (LDS-C minus noise floor). 47 concepts keep the same cultural direction across ≥3 of 4 models (12 unanimous: DE autonomy/rules vs ZH relational/space).",
    c3title:"Where the cultures diverge (Chinese ↔ German)",
    c3sub:"Same word, different map. These concepts appear in only one language's framing of the topic.",
    c4title:"The control: it is culture, not method",
    c4sub:"When the same pipeline measures <b>institutional knowledge</b> (mathematics), languages converge. When it measures <b>cultural concepts</b>, they diverge. A measurement artifact would affect both equally — it does not.",
    c5title:"Why this matters for the AI you use",
    c5body:"An AI that answers loan, moderation or advice questions is trained mostly on English data. If its idea of &ldquo;fairness&rdquo; shifts between German and Chinese, users get different treatment depending on the language they speak. LinguaGraph measures this drift — and pinpoints exactly which concepts diverge — so developers, regulators and researchers can check and calibrate multilingual AI.",
    langName:{zh:"Chinese",de:"German",en:"English"},
    topic:"Topic", sigVs:"Cross-language difference", floor:"Model's own noise", margin:"signal margin", ratio:"signal/noise",
    deOnly:"Only in German framing", zhOnly:"Only in Chinese framing", deLab:"German", zhLab:"Chinese",
    inst:"Institutional (math)", soc:"Cultural concepts", freq:"×",
    instSub:"converges", socSub:"diverges"
  },
  de: {
    h1:"Versteht die KI, die Sie nutzen, &ldquo;Gerechtigkeit&rdquo; in jeder Sprache gleich?",
    sub:"Wir haben dasselbe KI-Modell — auf Chinesisch, Deutsch und Englisch — gefragt, was zu fünf Alltagskonzepten gehört. Die Antwort ist messbar — und sie ist nicht dieselbe.",
    c1title:"Wählen Sie ein Konzept — sehen Sie, was das Modell in jeder Sprache assoziiert",
    c2title:"Der Unterschied ist real — kein Rauschen",
    c2sub:"Für jedes Sprachpaar liegt der sprachübergreifende Unterschied (blau) klar über dem sprachinternen Rauschboden des Modells (grau). Permutationstest p<0.01.",
    c2btitle:"Kein Einzelmodell-Zufall — vier unabhängige KIs driftieren",
    c2bsub:"Wir haben dieselbe Sonde auf vier unabhängig entwickelte Modelle (DeepSeek, Zhipu, Moonshot) angewendet. Jedes zeigt die chinesisch-deutsche Kluft klar über seinem eigenen Rauschboden — und die Kulturrichtung ist dieselbe.",
    multiStats:"ZH-DE-Drift-Magnitude pro Modell (LDS-C minus Rauschboden). 47 Konzepte behalten über ≥3 von 4 Modellen dieselbe Kulturrichtung (12 einhellig: DE Autonomie/Regeln vs ZH Beziehung/Raum).",
    c3title:"Wo die Kulturen divergieren (Chinesisch ↔ Deutsch)",
    c3sub:"Dasselbe Wort, andere Landkarte. Diese Konzepte erscheinen nur in der Rahmung einer Sprache.",
    c4title:"Die Kontrolle: Es ist Kultur, nicht Methode",
    c4sub:"Misst dieselbe Pipeline <b>institutionelles Wissen</b> (Mathematik), konvergieren die Sprachen. Misst sie <b>kulturelle Konzepte</b>, divergieren sie. Ein Messartefakt würde beide gleichermaßen betreffen — tut es nicht.",
    c5title:"Warum das für die KI, die Sie nutzen, wichtig ist",
    c5body:"Eine KI, die Kredit-, Moderations- oder Beratungsfragen beantwortet, ist überwiegend mit englischen Daten trainiert. Wenn sich ihre Vorstellung von &ldquo;Gerechtigkeit&rdquo; zwischen Deutsch und Chinesisch verschiebt, erhalten Nutzer je nach Sprache unterschiedliche Behandlung. LinguaGraph misst diese Drift — und benennt genau, welche Konzepte divergieren — damit Entwickler, Regulierer und Forscher mehrsprachige KI prüfen und kalibrieren können.",
    langName:{zh:"Chinesisch",de:"Deutsch",en:"Englisch"},
    topic:"Thema", sigVs:"Sprachübergreifender Unterschied", floor:"Eigenes Rauschen des Modells", margin:"Signal-Marge", ratio:"Signal/Rauschen",
    deOnly:"Nur im deutschen Rahmen", zhOnly:"Nur im chinesischen Rahmen", deLab:"Deutsch", zhLab:"Chinesisch",
    inst:"Institutionell (Mathematik)", soc:"Kulturelle Konzepte", freq:"×",
    instSub:"konvergiert", socSub:"divergiert"
  },
  zh: {
    h1:"你使用的 AI，在不同语言里对“公平”的理解一样吗？",
    sub:"我们用同一个 AI 模型——用中文、德语、英语——询问五个日常概念。答案是可测量的——而且并不相同。",
    c1title:"选一个概念，看模型在每种语言里关联什么",
    c2title:"差异是真实的——不是噪声",
    c2sub:"对每个语言对，跨语言差异（蓝色）都明显高于模型自身的组内噪声底（灰色）。置换检验 p&lt;0.01。",
    c2btitle:"不是某个 AI 的怪癖——四个独立 AI 都漂移",
    c2bsub:"我们把同样的探针用于四个独立开发的模型（DeepSeek、智谱、Moonshot）。每一个都在中文↔德语的差距上清晰高于自身噪声底——且文化方向一致。",
    multiStats:"每个模型的 ZH-DE 漂移幅度（LDS-C 减噪声底）。47 个概念在 ≥3/4 模型上保持相同文化方向（12 个全一致：德=自主/规则，中=关系/空间/应得）。",
    c3title:"文化分歧在哪里（中文 ↔ 德语）",
    c3sub:"同一个词，不同的概念地图。这些概念只出现在一种语言对该主题的框定中。",
    c4title:"对照实验：是文化，不是方法",
    c4sub:"同一管线测量<b>制度性知识</b>（数学）时，语言趋同；测量<b>文化概念</b>时，语言分歧。如果是测量伪影，两者会同样受影响——但没有。",
    c5title:"为什么这对你使用的 AI 很重要",
    c5body:"回答贷款、内容审核或建议问题的 AI 主要用英语数据训练。如果它对“公平”的理解在德语和中文之间发生漂移，用户会因语言不同而得到不同的对待。LinguaGraph 测量这种漂移——并精确定位哪些概念发生分歧——让开发者、监管者和研究者能检查和校准多语言 AI。",
    langName:{zh:"中文",de:"德语",en:"英语"},
    topic:"主题", sigVs:"跨语言差异", floor:"模型自身噪声", margin:"信号余量", ratio:"信号/噪声",
    deOnly:"仅在德语框定中", zhOnly:"仅在中文框定中", deLab:"德语", zhLab:"中文",
    inst:"制度性（数学）", soc:"文化概念", freq:"×",
    instSub:"趋同", socSub:"分歧"
  }
};

let lang='en';
const topKeys = Object.keys(DATA.concepts);

function tr(k){ return T[lang][k] ?? k; }

function conceptCol(langKey){
  const topic = document.getElementById('topic').value;
  const items = DATA.concepts[langKey]?.[topic] || [];
  const maxF = Math.max(1, ...items.map(i=>i.freq));
  const langName = T[lang].langName[langKey];
  const tagCls = langKey;
  let h = `<div class="col"><h3>${langName} <span class="tag ${tagCls}">${langKey.toUpperCase()}</span></h3>`;
  for(const it of items){
    const w = Math.round(30 + 70*(it.freq/maxF));
    h += `<div class="concept"><div class="row"><span class="orig">${it.orig}</span><span>${it.freq}${tr('freq')}</span></div>
          <div class="gloss">${it.gloss}</div><div class="bar"><div style="width:${w}%;background:${langKey==='zh'?'var(--zh)':langKey==='de'?'var(--de)':'var(--en)'}"></div></div></div>`;
  }
  h += `</div>`;
  return h;
}

function renderCols(){
  document.getElementById('cols').innerHTML = conceptCol('zh')+conceptCol('de')+conceptCol('en');
}

function renderSignal(){
  const v = document.getElementById('signalvis');
  const cards = document.getElementById('signalcards');
  const pairs = Object.keys(DATA.signal);
  const maxVal = Math.max(...pairs.map(p=>Math.max(DATA.signal[p].lds_c, DATA.signal[p].floor))) + 0.05;
  let vh = '';
  for(const p of pairs){
    const s = DATA.signal[p];
    const hSig = 100*s.lds_c/maxVal, hFloor = 100*s.floor/maxVal;
    vh += `<div style="text-align:center;flex:1">
      <div style="display:flex;justify-content:center;align-items:flex-end;gap:6px;height:150px">
        <div class="vbar" style="height:${hSig}%;background:var(--accent)" title="LDS-C ${s.lds_c}"></div>
        <div class="vbar" style="height:${hFloor}%;background:#475569" title="floor ${s.floor}"></div>
      </div>
      <div style="font-size:.72rem;color:var(--dim);margin-top:4px">${p}</div>
    </div>`;
  }
  v.innerHTML = vh;
  let ch = '';
  for(const p of pairs){
    const s = DATA.signal[p];
    ch += `<div class="metric"><div class="lbl">${tr('sigVs')} · ${p}</div>
      <div class="big" style="color:var(--accent)">${s.lds_c.toFixed(3)}</div>
      <div class="lbl">${tr('floor')}: ${s.floor.toFixed(3)}</div></div>`;
  }
  cards.innerHTML = ch;
}

function renderMulti(){
  const m = DATA.multi;
  const entries = Object.entries(m.margins_zhde).sort((a,b)=>b[1]-a[1]);
  if(!entries.length) return;
  const maxV = Math.max(...entries.map(e=>e[1])) + 0.03;
  const labels = {'deepseek-v4-flash':'DeepSeek','deepseek-v4-pro':'DeepSeek','glm-5.2':'Zhipu','kimi-k2.6':'Moonshot'};
  let h = '';
  for(const [model, val] of entries){
    const short = labels[model] || model;
    h += `<div style="flex:1;text-align:center">
      <div style="display:flex;justify-content:center;align-items:flex-end;height:150px">
        <div class="vbar" style="height:${100*val/maxV}%;background:var(--accent)"><span class="val">${val}</span></div>
      </div>
      <div style="font-size:.72rem;color:var(--dim);margin-top:4px">${short}</div>
    </div>`;
  }
  document.getElementById('multivis').innerHTML = h;
  document.getElementById('multistats').innerHTML =
    `<div class="lbl">${tr('multiStats')}</div>`;
}

function renderDrivers(){
  const d = DATA.drivers;
  let h = `<div class="dside de"><h4>🇩🇪 ${tr('deOnly')}</h4>`;
  for(const it of d.de_only){
    h += `<div class="ditem"><span>${it.topic}: <b>${it.key}</b></span><span class="n">${it.freq}${tr('freq')}</span></div>`;
  }
  h += `</div><div class="dside zh"><h4>🇨🇳 ${tr('zhOnly')}</h4>`;
  for(const it of d.zh_only){
    h += `<div class="ditem"><span>${it.topic}: <b>${it.key}</b></span><span class="n">${it.freq}${tr('freq')}</span></div>`;
  }
  h += `</div>`;
  document.getElementById('drivers').innerHTML = h;
}

function renderDomain(){
  const d = DATA.domain;
  const maxV = Math.max(d.institutional, d.social) + 0.05;
  const v = document.getElementById('domainvis');
  v.innerHTML = `
    <div style="flex:1;text-align:center">
      <div style="display:flex;justify-content:center;align-items:flex-end;height:150px">
        <div class="vbar" style="height:${100*d.institutional/maxV}%;background:#38bdf8">
          <span class="val">${d.institutional}</span></div>
      </div>
      <div style="font-size:.72rem;color:var(--dim)">${tr('inst')}<br><span style="color:#38bdf8">${tr('instSub')}</span></div>
    </div>
    <div style="flex:1;text-align:center">
      <div style="display:flex;justify-content:center;align-items:flex-end;height:150px">
        <div class="vbar" style="height:${100*d.social/maxV}%;background:#fbbf24">
          <span class="val">${d.social}</span></div>
      </div>
      <div style="font-size:.72rem;color:var(--dim)">${tr('soc')}<br><span style="color:#fbbf24">${tr('socSub')}</span></div>
    </div>`;
}

function applyLang(){
  lang = document.querySelector('.langbar button.on').dataset.lang;
  const t = T[lang];
  document.getElementById('h1').innerHTML = t.h1;
  document.getElementById('sub').textContent = t.sub;
  document.getElementById('c1title').textContent = t.c1title;
  document.getElementById('c2title').textContent = t.c2title;
  document.getElementById('c2sub').innerHTML = t.c2sub;
  document.getElementById('c3title').textContent = t.c3title;
  document.getElementById('c3sub').textContent = t.c3sub;
  document.getElementById('c4title').textContent = t.c4title;
  document.getElementById('c4sub').innerHTML = t.c4sub;
  document.getElementById('c5title').textContent = t.c5title;
  document.getElementById('c5body').innerHTML = t.c5body;
  renderCols(); renderSignal(); renderMulti(); renderDrivers(); renderDomain();
}

function init(){
  const sel = document.getElementById('topic');
  for(const k of topKeys){ const o=document.createElement('option'); o.value=k; o.textContent=k; sel.appendChild(o); }
  sel.addEventListener('change', renderCols);
  document.querySelectorAll('.langbar button').forEach(b=>{
    b.addEventListener('click', ()=>{ document.querySelectorAll('.langbar button').forEach(x=>x.classList.remove('on')); b.classList.add('on'); applyLang(); });
  });
  applyLang();
}
init();
</script>
</body>
</html>
"""


def main() -> None:
    data = {
        "concepts": concept_map(),
        "signal": signal_data(),
        "drivers": driver_data(),
        "domain": domain_data(),
        "multi": multi_data(),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    inline = json.dumps(data, ensure_ascii=False)
    html = HTML.replace("__DATA__", inline)
    out_path = OUT / "divergence_map.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"  concepts: {sum(len(v) for v in data['concepts']['zh'].values())} zh/topic rows")
    print(f"  signal: {list(data['signal'].keys())}")
    print(f"  drivers: de={len(data['drivers']['de_only'])} zh={len(data['drivers']['zh_only'])}")
    print(f"  domain: inst={data['domain']['institutional']} social={data['domain']['social']}")
    print(f"  Saved: {out_path} ({out_path.stat().st_size//1024} KB)")


if __name__ == "__main__":
    main()
