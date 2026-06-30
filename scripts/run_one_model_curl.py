#!/usr/bin/env python3
"""Run benchmark for ONE model using curl subprocess (more reliable)."""
import json, os, re, subprocess, sys, time

API_KEY = os.environ.get("OPENCODE_KEY", "")
if not API_KEY: print("ERROR: OPENCODE_KEY not set"); sys.exit(1)
model = sys.argv[1] if len(sys.argv) > 1 else "qwen3.7-plus"

d = json.load(open("data/gold/gold_dataset.json", encoding="utf-8"))
items = d if isinstance(d, list) else d.get("items", d.get("results", d.get("data", [])))
safe = model.replace("/", "_").replace(":", "_")
outpath = f"data/model_comparison/oc_{safe}_results.json"

print(f"START {model} ({len(items)} items)", flush=True)
total_f1, n_valid, failed = 0.0, 0, 0

for idx, item in enumerate(items):
    text = item.get("text", "")
    gold = set(item.get("human_labels", {}).get("concepts", []))
    if not text or not gold: continue

    prompt = f'从文本中提取关键概念。JSON格式: {{"concepts":[{{"name":"概念名称"}}]}}\n概念名称用原始语言UTF-8。\n文本:{text[:2000]}'
    payload = json.dumps({"model": model, "messages": [
        {"role": "system", "content": "概念提取专家。输出严格JSON，UTF-8。"},
        {"role": "user", "content": prompt}
    ], "temperature": 0.1, "max_tokens": 1024})

    try:
        proc = subprocess.run([
            "curl", "-s", "-X", "POST",
            "https://opencode.ai/zen/go/v1/chat/completions",
            "-H", f"Authorization: Bearer {API_KEY}",
            "-H", "Content-Type: application/json",
            "-d", payload,
            "--max-time", "120"
        ], capture_output=True, timeout=130)
        # Decode stdout as UTF-8 (curl returns raw bytes)
        stdout = proc.stdout.decode("utf-8", errors="replace")
        resp = json.loads(stdout)
        content = resp["choices"][0]["message"]["content"]
        m = re.search(r"\{.*\}", content, re.DOTALL)
        if not m: failed += 1; continue
        pred = {c["name"] for c in json.loads(m.group()).get("concepts", []) if c.get("name")}
        if not pred: failed += 1; continue
        tp = len(gold & pred)
        prec = tp / max(len(pred), 1)
        rec = tp / max(len(gold), 1)
        total_f1 += 2 * prec * rec / max(prec + rec, 0.001)
        n_valid += 1
    except Exception as e:
        failed += 1
        if failed <= 3: print(f"  [{idx}] FAIL: {str(e)[:60]}", flush=True)

    if (idx + 1) % 10 == 0:
        cur = total_f1 / max(n_valid, 1)
        print(f"  [{idx+1}/{len(items)}] F1={cur:.4f} v={n_valid} f={failed}", flush=True)
    time.sleep(0.3)

f1 = round(total_f1 / max(n_valid, 1), 4)
json.dump({"model": model, "total_items": len(items), "valid": n_valid,
    "failed": failed, "summary": {"mean_f1": f1, "mean_precision": 0, "mean_recall": 0}},
    open(outpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"DONE {model}: F1={f1} v={n_valid}/{len(items)} f={failed}", flush=True)
print(f"SAVED {outpath}", flush=True)
