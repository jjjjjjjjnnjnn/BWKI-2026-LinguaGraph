#!/usr/bin/env python3
"""G2 gold blind-audit tool (social subset, n=72).

- --generate: deterministic shuffle (seed default 20260914) of the 72
  auto_accepted social gold items, STRIPPING gold concepts, writing a
  review template to research/gold_review_v2/review_72.json.
  concepts are NEVER prefilled and no AI pre-labeling is run.
- --import <filled.json>: score a filled review file:
  (1) Jaccard agreement vs current gold concepts (overall + by language);
  (2) qwen-plus social F1 recomputed with v2 as gold, using
      data/model_comparison/qwen-plus_results.json predicted_concepts
      (rejects count as F1 = 0.0);
  (3) verdict: pass (may mature) iff F1>=0.85 AND agreement>=0.8 overall
      AND >=0.7 in every language.
- --workbench: build offline single-file review UI (workbench.html)
  with a blindness gate (fails loud if any seed leaks into the template).

Template record fields:
  audit_id / sample_id / language / question / text /
  concepts_blank[] (always []) / reviewer / decision (accept|edit|reject) /
  edited_concepts (reviewer-filled list; required unless reject).
"""

import argparse
import json
import random
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
GOLD_PATH = PROJECT / "data" / "gold" / "gold_dataset.json"
QWEN_PLUS_PATH = PROJECT / "data" / "model_comparison" / "qwen-plus_results.json"
OUT_DIR = PROJECT / "research" / "gold_review_v2"
DEFAULT_SEED = 20260914
PASS_F1 = 0.85
PASS_AGR = 0.80
PASS_AGR_LANG = 0.70  # per-language floor: no subgroup may be averaged out


def load_social_gold():
    items = json.loads(GOLD_PATH.read_text(encoding="utf-8"))
    if isinstance(items, dict):
        items = items.get("items", items.get("results", items.get("data", [])))
    social = [x for x in items if x.get("annotator") == "auto_accepted"]
    if len(social) != 72:
        print(f"[warn] expected 72 social items, found {len(social)}", file=sys.stderr)
    return social


def generate(seed: int, out_name: str = "review_72.json") -> Path:
    social = load_social_gold()
    rng = random.Random(seed)
    order = list(social)
    rng.shuffle(order)
    records = []
    for i, it in enumerate(order, 1):
        records.append({
            "audit_id": f"A{i:03d}",
            "sample_id": it.get("sample_id"),
            "language": it.get("language"),
            "question": it.get("question", ""),
            "text": it.get("text", ""),
            "concepts_blank": [],
            "reviewer": "",
            "decision": "",
            "edited_concepts": [],
        })
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / out_name
    payload = {
        "meta": {
            "seed": seed,
            "n": len(records),
            "source": "data/gold/gold_dataset.json (annotator=auto_accepted)",
            "blinding": "gold concepts stripped; concepts_blank always []; no AI pre-label",
            "decision_values": ["accept", "edit", "reject"],
        },
        "records": records,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[generate] seed={seed} n={len(records)} -> {out}")
    return out


def jaccard(a, b) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def prf(gold, pred):
    g, p = set(gold), set(pred)
    if not g or not p:
        return 0.0, 0.0, 0.0
    tp = len(g & p)
    prec = tp / len(p)
    rec = tp / len(g)
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    return prec, rec, f1


def import_scores(path: Path):
    filled = json.loads(Path(path).read_text(encoding="utf-8"))
    records = filled.get("records", filled) if isinstance(filled, dict) else filled
    gold = {x["sample_id"]: x for x in load_social_gold()}
    qpred = {}
    qd = json.loads(QWEN_PLUS_PATH.read_text(encoding="utf-8"))
    for r in qd.get("results", []):
        qpred[r["sample_id"]] = r.get("predicted_concepts", [])

    agr_all, agr_by_lang = [], {}
    f1s = []
    n_reject = 0
    for rec in records:
        sid = rec.get("sample_id")
        dec = (rec.get("decision") or "").strip().lower()
        edited = rec.get("edited_concepts", []) or []
        cur = gold.get(sid, {}).get("human_labels", {}).get("concepts", [])
        lang = rec.get("language", gold.get(sid, {}).get("language", "?"))
        if dec == "reject":
            n_reject += 1
            agr = 0.0
        elif dec in ("accept", "edit"):
            agr = jaccard(cur, edited)
        else:
            print(f"[warn] {sid}: bad decision {dec!r}, skipped", file=sys.stderr)
            continue
        agr_all.append(agr)
        agr_by_lang.setdefault(lang, []).append(agr)
        # Rejects count as F1 = 0.0 (dropping hard items must not inflate F1).
        if dec == "reject":
            f1s.append(0.0)
        elif edited:
            _, _, f1 = prf(edited, qpred.get(sid, []))
            f1s.append(f1)

    agr_mean = sum(agr_all) / len(agr_all) if agr_all else 0.0
    by_lang = {k: round(sum(v) / len(v), 4) for k, v in sorted(agr_by_lang.items())}
    f1_mean = sum(f1s) / len(f1s) if f1s else 0.0
    lang_floor_ok = all(v >= PASS_AGR_LANG for v in by_lang.values()) if by_lang else False
    verdict = ("pass (may mature)"
               if (f1_mean >= PASS_F1 and agr_mean >= PASS_AGR and lang_floor_ok)
               else "maintain (stay Developing, C9b)")
    report = {
        "n_reviewed": len(agr_all),
        "n_reject": n_reject,
        "agreement_overall": round(agr_mean, 4),
        "agreement_by_language": by_lang,
        "per_language_floor": PASS_AGR_LANG,
        "per_language_floor_ok": lang_floor_ok,
        "qwen_plus_social_f1_v2gold": round(f1_mean, 4),
        "n_f1_valid": len(f1s),
        "thresholds": {"f1": PASS_F1, "agreement": PASS_AGR, "agreement_per_lang": PASS_AGR_LANG},
        "verdict": verdict,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def build_workbench(src_name: str = "review_72.json") -> Path:
    """Build an offline single-file review workbench (blinded).

    Embeds the template records into workbench.html. The reviewer opens it
    in a browser, judges all 72 items, clicks Export, and the downloaded
    JSON feeds --import. localStorage autosaves progress per audit_id.
    """
    src = OUT_DIR / src_name
    payload = json.loads(src.read_text(encoding="utf-8"))
    records = payload.get("records", payload)
    # Blindness gate: template must carry no gold/model concepts.
    forbidden = ("human_labels", "auto_concepts", "predicted_concepts", "gold_concepts")
    for r in records:
        assert r.get("concepts_blank", []) == [], r.get("audit_id")
        assert not any(k in r for k in forbidden), r.get("audit_id")
        assert not r.get("edited_concepts"), r.get("audit_id")
    data_js = json.dumps(records, ensure_ascii=False).replace("</", "<\\/")
    html = WORKBENCH_HTML.replace("__DATA__", data_js)
    out = OUT_DIR / "workbench.html"
    out.write_text(html, encoding="utf-8")
    print(f"[workbench] n={len(records)} blindness-gate OK -> {out}")
    return out


WORKBENCH_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Gold Blind Audit — 72 social labels</title>
<style>
body{font-family:system-ui,sans-serif;max-width:760px;margin:24px auto;padding:0 16px;color:#111}
#bar{height:8px;background:#eee;border-radius:4px;margin:8px 0}
#fill{height:8px;background:#1e7e4d;border-radius:4px;width:0%}
.card{border:1px solid #ddd;border-radius:8px;padding:16px;margin:16px 0}
.badge{display:inline-block;background:#eee;border-radius:4px;padding:2px 8px;font-size:.8rem}
textarea{width:100%;height:110px;font-size:.95rem}
.q{color:#555;font-size:.85rem}.t{font-size:1.05rem;margin:8px 0}
.row{margin:10px 0}.btn{padding:8px 16px;margin-right:8px;cursor:pointer}
.dec{padding:8px 14px;margin-right:8px;cursor:pointer;border:2px solid #ccc;background:#fff;border-radius:6px}
.dec.on{border-color:#1e7e4d;background:#e8f5ee}
#nav{position:sticky;bottom:0;background:#fff;padding:10px 0;border-top:1px solid #ddd}
</style>
</head>
<body>
<h2>Gold Blind Audit <span class="badge" id="prog">0 / 72</span></h2>
<div id="bar"><div id="fill"></div></div>
<div class="row">Reviewer: <input id="who" placeholder="name (recorded in export)"></div>
<div class="card">
<div><span class="badge" id="aid"></span> <span class="badge" id="lng"></span></div>
<div class="q" id="q"></div>
<div class="t" id="txt"></div>
<div class="row">Your concepts (one per line, your own words — no AI help):</div>
<textarea id="con"></textarea>
<div class="row" id="decs">
<button class="dec" data-d="accept">accept — my list stands as gold</button>
<button class="dec" data-d="edit">edit — gold needs my corrected list</button>
<button class="dec" data-d="reject">reject — item unusable</button>
</div>
</div>
<div id="nav">
<button class="btn" id="prev">← Prev</button>
<button class="btn" id="next">Next → (Ctrl+Enter)</button>
<button class="btn" id="exp">Export filled JSON</button>
<span id="msg"></span>
</div>
<script>
var R = __DATA__;
var i = 0, S = {};
try { S = JSON.parse(localStorage.getItem('g2audit') || '{}'); } catch(e) { S = {}; }
if (S._who) document.getElementById('who').value = S._who;
function save() {
  var a = R[i];
  S[a.audit_id] = {d: cur, c: document.getElementById('con').value};
  S._who = document.getElementById('who').value;
  try { localStorage.setItem('g2audit', JSON.stringify(S)); } catch(e) {}
  paint();
}
var cur = '';
function paint() {
  var done = R.filter(function(a){ var s=S[a.audit_id]; return s && s.d; }).length;
  document.getElementById('prog').textContent = done + ' / ' + R.length;
  document.getElementById('fill').style.width = (100*done/R.length) + '%';
}
function show() {
  var a = R[i], s = S[a.audit_id] || {};
  document.getElementById('aid').textContent = a.audit_id + ' · ' + a.sample_id;
  document.getElementById('lng').textContent = a.language;
  document.getElementById('q').textContent = 'Q: ' + a.question;
  document.getElementById('txt').textContent = a.text;
  document.getElementById('con').value = s.c || '';
  cur = s.d || '';
  document.querySelectorAll('.dec').forEach(function(b){ b.classList.toggle('on', b.dataset.d === cur); });
  paint();
}
document.querySelectorAll('.dec').forEach(function(b){
  b.addEventListener('click', function(){ cur = b.dataset.d; save(); });
});
document.getElementById('con').addEventListener('input', save);
document.getElementById('who').addEventListener('input', save);
document.getElementById('prev').addEventListener('click', function(){ if (i>0){ i--; show(); } });
document.getElementById('next').addEventListener('click', function(){ if (i<R.length-1){ i++; show(); } });
document.addEventListener('keydown', function(e){
  if (e.ctrlKey && e.key === 'Enter'){ if (i<R.length-1){ i++; show(); } }
});
document.getElementById('exp').addEventListener('click', function(){
  var who = document.getElementById('who').value || 'UNNAMED';
  var recs = R.map(function(a){
    var s = S[a.audit_id] || {};
    var cl = (s.c || '').split('\\n').map(function(x){ return x.trim(); }).filter(Boolean);
    return {audit_id: a.audit_id, sample_id: a.sample_id, language: a.language,
      question: a.question, text: a.text, concepts_blank: [],
      reviewer: who, decision: s.d || '', edited_concepts: cl};
  });
  var missing = recs.filter(function(r){ return !r.decision; }).length;
  document.getElementById('msg').textContent = missing ? ('⚠ ' + missing + ' undecided — exported anyway') : '✓ all decided';
  var blob = new Blob([JSON.stringify({meta: {exporter: who, n: recs.length}, records: recs}, null, 2)],
    {type: 'application/json'});
  var u = URL.createObjectURL(blob), l = document.createElement('a');
  l.href = u; l.download = 'review_72_filled.json'; l.click();
  setTimeout(function(){ URL.revokeObjectURL(u); }, 5000);
});
show();
</script>
</body>
</html>"""


def main():
    ap = argparse.ArgumentParser(description="G2 gold blind audit (social n=72)")
    ap.add_argument("--generate", action="store_true")
    ap.add_argument("--import", dest="import_path", default=None)
    ap.add_argument("--workbench", action="store_true",
                    help="build offline review workbench (workbench.html)")
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--out", default="review_72.json")
    args = ap.parse_args()
    if args.generate:
        generate(args.seed, args.out)
    elif args.import_path:
        import_scores(Path(args.import_path))
    elif args.workbench:
        build_workbench()
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
