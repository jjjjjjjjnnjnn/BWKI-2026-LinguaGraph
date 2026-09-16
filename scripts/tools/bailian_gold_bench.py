#!/usr/bin/env python3
"""Bailian gold benchmark (QWEN_MODELS override, temperature=0).
- Models: from env QWEN_MODELS (default 'qwen3.8-flash,qwen3.8-max')
- Reads ONLY: linguaGraph.db (gold_labels + responses), research/wiki_gloss_audit_30_qwen_cross_20260914.json (control)
- Writes ONLY: research/bailian_gold_20260914.json + research/bailian_gold_20260914.md
- Key: ONLY from env BAILIAN_API_KEY, never written to disk.
"""
import json, os, re, sqlite3, sys

if "--help" in sys.argv or "-h" in sys.argv:
    print("Usage: bailian_gold_bench.py [--help]  (no other options; models via $QWEN_MODELS)")
    print("  Runs temp=0 gold extraction bench (n=92 zh/de/en) against linguaGraph.db,")
    print("  writes research/bailian_gold_20260914.json/.md. Key ONLY from env. Needs: pip install openai.")
    sys.exit(0)

from collections import defaultdict
from datetime import date
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: pip install openai")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from evaluate_gold import compute_f1

PROJECT = Path(__file__).resolve().parent.parent.parent
API_URL = os.environ.get("BAILIAN_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
API_KEY = os.environ.get("BAILIAN_API_KEY", "")
if not API_KEY:
    print("ERROR: Set BAILIAN_API_KEY environment variable")
    sys.exit(1)
MODELS = [m.strip() for m in os.environ.get("QWEN_MODELS", "qwen3.8-flash,qwen3.8-max").split(",") if m.strip()]
if not MODELS:
    print("ERROR: QWEN_MODELS empty")
    sys.exit(1)

DATE = "20260914"

if "--help" in sys.argv or "-h" in sys.argv:
    print("Usage: bailian_gold_bench.py [--help]  (no other options; models via $QWEN_MODELS)")
    print("  Runs temp=0 gold extraction bench (n=92 zh/de/en) against linguaGraph.db,")
    print("  writes research/bailian_gold_20260914.json/.md. Key ONLY from env. Needs: pip install openai.")
    sys.exit(0)

def b(x):
    return x.decode("utf-8", "ignore") if isinstance(x, bytes) else (x or "")

conn = sqlite3.connect(str(PROJECT / "linguaGraph.db"))
conn.text_factory = bytes
gold_items = conn.execute("""
    SELECT gl.response_id, gl.concepts, r.answer_text, r.language
    FROM gold_labels gl JOIN responses r ON gl.response_id = r.response_id
    ORDER BY r.language, gl.response_id
""").fetchall()
conn.close()

# control: known qwen-max gloss cross
cross_path = PROJECT / "research" / "wiki_gloss_audit_30_qwen_cross_20260914.json"
cross = json.loads(cross_path.read_text(encoding="utf-8")) if cross_path.exists() else {"records": []}
max_gloss = {}  # word -> max gloss
for r in cross.get("records", []):
    q = r.get("qwen_cross", {})
    m = q.get("qwen3.8-max", "") or q.get("qwen-max", "")
    if r.get("zh"):
        max_gloss[r["zh"]] = m
# control sentences: gold items whose gold concepts hit cross words (case-insensitive)
cross_words_lower = set(w.lower() for w in max_gloss)

EXAMPLES = {
    "zh": '{"concepts": ["\u81ea\u7531", "\u8d23\u4efb"]}',
    "en": '{"concepts": ["freedom", "responsibility"]}',
    "de": '{"concepts": ["Freiheit", "Verantwortung"]}',
}

all_results = {}
per_model_items = {}
for model in MODELS:
    print(f"\n=== {model} ===", flush=True)
    client = OpenAI(base_url=API_URL, api_key=API_KEY)
    per_item = []
    n_exc = 0
    n_parsefail = 0
    n_fallback = 0
    for item in gold_items:
        resp_id = b(item[0])
        try:
            gold_c = json.loads(b(item[1]))
        except Exception:
            gold_c = []
        text = b(item[2])
        lang = b(item[3])
        example = EXAMPLES.get(lang, EXAMPLES["en"])
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "\u4f60\u662f\u6982\u5ff5\u63d0\u53d6\u52a9\u624b\u3002\u53ea\u8f93\u51faJSON\u3002"},
                    {"role": "user", "content": f"{example}\n\nText: {text}\n\n\u63d0\u53d6\u6982\u5ff5\u4e3aJSON\u683c\u5f0f\u3002"},
                ],
                temperature=0,
                max_tokens=256,
                timeout=30,
            )
            raw = (resp.choices[0].message.content or "").strip()
            # deepseek compat fallback: content empty -> reasoning_content
            _fb = False
            if not raw:
                _rc = getattr(resp.choices[0].message, "reasoning_content", "") or ""
                _rc = _rc.strip() if isinstance(_rc, str) else ""
                if _rc:
                    raw = _rc
                    _fb = True
                    n_fallback += 1
        except Exception as e:
            n_exc += 1
            per_item.append({"lang": lang, "f1": 0.0, "resp_id": resp_id,
                             "pred": [], "gold": gold_c, "fail": "exception", "note": str(e)[:120]})
            continue
        cleaned = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
        match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        try:
            pred_c = json.loads(match.group()).get("concepts", []) if match else []
            if match is None:
                n_parsefail += 1
        except Exception:
            pred_c = []
            n_parsefail += 1
        gold_set = set(c.strip().lower() for c in gold_c if isinstance(c, str) and c.strip())
        pred_set = set(c.strip().lower() for c in pred_c if isinstance(c, str) and c.strip())
        metrics = compute_f1(gold_set, pred_set)
        fail = "parse_fail" if not match or not pred_c else ""
        per_item.append({"lang": lang, "f1": metrics["f1"], "precision": metrics["precision"],
                         "recall": metrics["recall"], "resp_id": resp_id,
                         "pred": pred_c, "gold": gold_c, "fail": fail, "fallback": _fb})
    by_lang = defaultdict(list)
    for r in per_item:
        by_lang[r["lang"]].append(r)
    scores = {}
    for lang in ["zh", "de", "en"]:
        items = by_lang.get(lang, [])
        f1v = [i["f1"] for i in items]
        scores[lang] = round(sum(f1v) / len(f1v), 4) if f1v else 0.0
        scores[lang + "_n"] = len(items)
        scores[lang + "_fail"] = sum(1 for i in items if i.get("fail"))
    scores["overall"] = round(sum(i["f1"] for i in per_item) / len(per_item), 4) if per_item else 0.0
    scores["n"] = len(per_item)
    scores["exc_fail"] = n_exc
    scores["parse_fail"] = n_parsefail
    scores["fallback_hits"] = n_fallback
    scores["fail_rate"] = round((n_exc + n_parsefail) / len(per_item), 4) if per_item else 0.0
    all_results[model] = scores
    per_model_items[model] = per_item
    print(f"  ZH={scores['zh']:.4f}(n={scores['zh_n']}) DE={scores['de']:.4f}(n={scores['de_n']}) EN={scores['en']:.4f}(n={scores['en_n']}) Overall={scores['overall']:.4f} fail={scores['fail_rate']:.2%} fallback_hits={n_fallback}")

# control sentences: gold items overlapping cross words
control_hits = []
seen = set()
for it in per_model_items.get(MODELS[0], []):
    golds = [g for g in it.get("gold", []) if isinstance(g, str)]
    hits = [g for g in golds if g.lower() in cross_words_lower]
    if hits and it["resp_id"] not in seen:
        seen.add(it["resp_id"])
        maxmap = {g: max_gloss.get(next((w for w in max_gloss if w.lower() == g.lower()), g), "") for g in hits}
        control_hits.append({"resp_id": it["resp_id"], "lang": it["lang"],
                             "gold": golds, "hit_concepts": hits, "qwen_max_gloss": maxmap})

out_json = {
    "date": DATE,
    "models": MODELS,
    "temperature": 0,
    "source": "linguaGraph.db gold_labels+responses",
    "scores": all_results,
    "control": {
        "cross_file": "research/wiki_gloss_audit_30_qwen_cross_20260914.json",
        "cross_agree": "28/30=93.3% (G012,G017 disagree)",
        "match_source_flash": "27/30=90.0%",
        "match_source_max": "26/30=86.7%",
        "divergent": [{"audit_id": "G012", "zh": "\u623f\u4ea7", "flash": "property", "max": "real estate"},
                      {"audit_id": "G017", "zh": "negative Freiheit", "flash": "negative liberty", "max": "negative freedom"}],
        "gold_overlap_hits": len(control_hits),
        "hits": control_hits[:20],
    },
    "items": per_model_items,
}
jp = PROJECT / "research" / f"bailian_gold_{DATE}.json"
jp.write_text(json.dumps(out_json, ensure_ascii=False, indent=1), encoding="utf-8")

# markdown
L = []
L.append(f"# Bailian Gold Bench {DATE}")
L.append("")
L.append(f"- models: {', '.join(MODELS)} | temperature=0 | n={len(gold_items)} (zh={all_results[MODELS[0]].get('zh_n',0)}, de={all_results[MODELS[0]].get('de_n',0)}, en={all_results[MODELS[0]].get('en_n',0)})")
L.append(f"- source: linguaGraph.db gold_labels+responses (read-only, no DB write)")
L.append("")
L.append("## 1. 分语言F1")
L.append("")
L.append("| model | zh F1 | de F1 | en F1 | overall | fail_rate (exc+parse) |")
L.append("|---|---|---|---|---|---|")
for m in MODELS:
    s = all_results[m]
    L.append(f"| {m} | {s['zh']:.4f} | {s['de']:.4f} | {s['en']:.4f} | {s['overall']:.4f} | {s['fail_rate']:.2%} (exc={s['exc_fail']},parse={s['parse_fail']}) |")
L.append("")
L.append("## 2. 失败率口径")
L.append("")
L.append("- exception: API调用异常 (timeout/4xx/5xx); parse_fail: 无`{...}`匹配或concepts空/JSON解析失败。fail_rate=(exc+parse)/总数。")
L.append("")
L.append("## 3. 与已知qwen-max gloss交叉的对照")
L.append("")
L.append("- 已知交叉 (research/wiki_gloss_audit_30_qwen_cross_20260914.json): 双模型一致 28/30=93.3%, 分歧 G012(房产:property vs real estate)、G017(negative Freiheit:liberty vs freedom); flash匹配源27/30, max匹配源26/30。")
L.append(f"- 金标重叠对照句: {len(control_hits)} 条 (gold概念命中cross 30词, 不区分大小写)。前20条见JSON `control.hits`, 下表示例(最多10条):")
L.append("")
L.append("| resp_id | lang | hit_concepts | qwen-max gloss |")
L.append("|---|---|---|---|")
for h in control_hits[:10]:
    gm = "; ".join(f"{k}=>{v}" for k, v in h["qwen_max_gloss"].items())
    L.append(f"| {h['resp_id']} | {h['lang']} | {'; '.join(h['hit_concepts'])} | {gm} |")
if not control_hits:
    L.append("| (无重叠) | | | |")
L.append("")
mp = PROJECT / "research" / f"bailian_gold_{DATE}.md"
mp.write_text("\n".join(L) + "\n", encoding="utf-8")
print(f"\nSaved {jp}\nSaved {mp}")

print("\n" + "=" * 70)
print(f"{'Model':<22s} {'ZH F1':>8s} {'DE F1':>8s} {'EN F1':>8s} {'Overall':>8s} {'Fail':>8s}")
for m in MODELS:
    s = all_results[m]
    print(f"{m:<22s} {s['zh']:>8.4f} {s['de']:>8.4f} {s['en']:>8.4f} {s['overall']:>8.4f} {s['fail_rate']:>7.2%}")
