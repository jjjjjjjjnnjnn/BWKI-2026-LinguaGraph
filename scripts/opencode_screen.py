#!/usr/bin/env python3
"""Screen OpenCode GO models: stage1=5 items, stage2=full 92."""
import json, os, re, sys, time, urllib.request
from pathlib import Path

API_KEY = os.environ.get("OPENCODE_KEY", "")
if not API_KEY: print("ERROR: set OPENCODE_KEY"); sys.exit(1)

API_URL = "https://opencode.ai/zen/go/v1/chat/completions"
PROJECT = Path(__file__).resolve().parent.parent
GOLD = json.load(open(PROJECT / "data/gold/gold_dataset.json", encoding="utf-8"))
all_items = GOLD if isinstance(GOLD, list) else GOLD.get("items", GOLD.get("results", GOLD.get("data", [])))
OUT = PROJECT / "data/model_comparison"
OUT.mkdir(parents=True, exist_ok=True)

PROMPT = """从以下文本中提取关键概念。输出严格JSON格式:
{{"concepts": [{{"name": "概念名称"}}]}}
概念名称用原始语言UTF-8。文本: {text}"""

ALREADY = {"deepseek-v4-pro","deepseek-v4-flash","deepseek-chat","qwen-plus","qwen-max"}

def get_models():
    req = urllib.request.Request("https://opencode.ai/zen/go/v1/models",
        headers={"Authorization": f"Bearer {API_KEY}",
                 "User-Agent": "curl/8.0",
                 "Accept": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=15).read())
    return [m["id"] for m in r.get("data",[]) if m["id"] not in ALREADY]

def evaluate(model, items, label=""):
    total_f1 = 0; n_valid = 0; failed = 0
    for item in items:
        text = item.get("text",""); gold = set(item.get("human_labels",{}).get("concepts",[]))
        if not text or not gold: continue
        p = json.dumps({"model": model, "messages": [
            {"role":"system","content":"概念提取专家。输出严格JSON，UTF-8。"},
            {"role":"user","content":PROMPT.format(text=text[:2000])}
        ], "temperature":0.1,"max_tokens":1024}).encode()
        try:
            req = urllib.request.Request(API_URL, data=p,
                headers={"Content-Type":"application/json",
                         "Authorization":f"Bearer {API_KEY}",
                         "User-Agent":"curl/8.0"})
            resp = json.loads(urllib.request.urlopen(req, timeout=60).read())
            content = resp["choices"][0]["message"]["content"]
            m = re.search(r"\{.*\}", content, re.DOTALL)
            if not m: failed+=1; continue
            pred = {c["name"] for c in json.loads(m.group()).get("concepts",[]) if c.get("name")}
            if not pred: failed+=1; continue
            tp = len(gold & pred); prec = tp/max(len(pred),1); rec = tp/max(len(gold),1)
            total_f1 += 2*prec*rec/max(prec+rec,0.001); n_valid += 1
        except: failed+=1
        time.sleep(0.3)
    return {"model":model,"valid":n_valid,"failed":failed,
            "f1":round(total_f1/max(n_valid,1),4)}

# Stage 1: Screen all on 5 items
print("=== Stage 1: Screen 5 items ===")
models = get_models()
print(f"Models to test: {len(models)}")
results = []
for i, m in enumerate(models):
    print(f"  [{i+1}/{len(models)}] {m}...", end=" ", flush=True)
    r = evaluate(m, all_items[:5])
    results.append(r)
    print(f"F1={r['f1']:.4f}")

results.sort(key=lambda x: -x["f1"])
print("\n=== Rankings ===")
for r in results:
    tag = " >>> FULL" if r["f1"] >= 0.5 else ""
    print(f"  {r['model']:25s} F1={r['f1']:.4f} v={r['valid']}{tag}")

# Stage 2: Full eval on F1>=0.5
print("\n=== Stage 2: Full N=92 ===")
for r in results:
    if r["f1"] < 0.5: continue
    print(f"  {r['model']}...", end=" ", flush=True)
    full = evaluate(r["model"], all_items)
    print(f"F1={full['f1']:.4f} v={full['valid']}/{len(all_items)} failed={full['failed']}")
    safe = r["model"].replace("/","_").replace(":","_")
    json.dump({"model":r["model"],"total_items":len(all_items),"valid":full["valid"],
        "failed":full["failed"],"summary":{"mean_f1":full["f1"],"mean_precision":0,"mean_recall":0}},
        open(OUT/f"oc_{safe}_results.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
