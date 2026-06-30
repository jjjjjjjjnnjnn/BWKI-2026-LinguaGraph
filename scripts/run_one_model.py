#!/usr/bin/env python3
"""Run full N=92 benchmark for ONE model through OpenCode GO API."""
import json, os, re, sys, time, urllib.request

API_KEY = os.environ.get("OPENCODE_KEY", "")
if not API_KEY: print("ERROR: OPENCODE_KEY not set"); sys.exit(1)

API_URL = "https://opencode.ai/zen/go/v1/chat/completions"
model = sys.argv[1] if len(sys.argv) > 1 else "qwen3.7-plus"

d = json.load(open("data/gold/gold_dataset.json", encoding="utf-8"))
items = d if isinstance(d, list) else d.get("items", d.get("results", d.get("data", [])))

safe = model.replace("/", "_").replace(":", "_")
outpath = f"data/model_comparison/oc_{safe}_results.json"
logpath = f"data/model_comparison/oc_{safe}_log.txt"

print(f"Starting: {model} ({len(items)} items)")
log = open(logpath, "w", encoding="utf-8")
total_f1, total_p, total_r = 0.0, 0.0, 0.0
n_valid, failed = 0, 0

for idx, item in enumerate(items):
    text = item.get("text", "")
    gold = set(item.get("human_labels", {}).get("concepts", []))
    if not text or not gold:
        continue

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "概念提取专家。输出严格JSON，UTF-8。"},
            {"role": "user", "content": f'从文本中提取关键概念。JSON格式: {{"concepts":[{{"name":"概念名称"}}]}}\n概念名称用原始语言UTF-8。\n文本:{text[:2000]}'}
        ],
        "temperature": 0.1, "max_tokens": 1024
    }).encode()

    try:
        req = urllib.request.Request(API_URL, data=payload, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
            "User-Agent": "curl/8.0"
        })
        resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
        content = resp["choices"][0]["message"]["content"]
        m = re.search(r"\{.*\}", content, re.DOTALL)
        if not m: failed += 1; log.write(f"[{idx}] {text[:50]}... NO_JSON\n"); continue
        pred = {c["name"] for c in json.loads(m.group()).get("concepts", []) if c.get("name")}
        if not pred: failed += 1; log.write(f"[{idx}] {text[:50]}... EMPTY_PRED\n"); continue

        tp = len(gold & pred)
        prec = tp / max(len(pred), 1)
        rec = tp / max(len(gold), 1)
        f1 = 2 * prec * rec / max(prec + rec, 0.001)
        total_f1 += f1; total_p += prec; total_r += rec; n_valid += 1
    except Exception as e:
        failed += 1
        log.write(f"[{idx}] ERROR: {str(e)[:80]}\n")

    if (idx + 1) % 10 == 0:
        cur = total_f1 / max(n_valid, 1)
        msg = f"[{idx+1}/{len(items)}] cur_F1={cur:.4f} valid={n_valid} failed={failed}"
        print(msg); log.write(msg + "\n")
    time.sleep(0.3)

f1 = round(total_f1 / max(n_valid, 1), 4)
prec = round(total_p / max(n_valid, 1), 4)
rec = round(total_r / max(n_valid, 1), 4)

result = {"model": model, "total_items": len(items), "valid": n_valid,
          "failed": failed, "summary": {"mean_f1": f1, "mean_precision": prec, "mean_recall": rec}}
json.dump(result, open(outpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
msg = f"DONE: {model} F1={f1} P={prec} R={rec} v={n_valid}/{len(items)} f={failed}"
print(msg); log.write(msg + "\n"); log.close()
print(f"Saved: {outpath}")
