#!/usr/bin/env python3
"""qwen cross-gloss for wiki_gloss_audit_30 (30 words), via DashScope compatible-mode.
Reads BAILIAN_API_KEY/BAILIAN_BASE from env. NEVER writes key to disk.
Output: research/wiki_gloss_audit_30_qwen_cross_20260914.json
"""
import json, os, sys, pathlib, urllib.request

if "--help" in sys.argv or "-h" in sys.argv:
    print("Usage: qwen_cross_gloss_30.py [--help]  (no other options; models via $QWEN_MODELS)")
    print("  Fetches English glosses for wiki_gloss_audit_30 (30 words) and writes")
    print("  research/wiki_gloss_audit_30_qwen_cross_20260914.json. Key ONLY from env.")
    sys.exit(0)

BASE = os.environ.get("BAILIAN_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
KEY = os.environ.get("BAILIAN_API_KEY", "")
if not KEY:
    print("ERROR: BAILIAN_API_KEY unset", file=sys.stderr); sys.exit(1)
MODELS = [m for m in os.environ.get("QWEN_MODELS", "qwen3.8-flash,qwen3.8-max").split(",") if m]
PROJECT = str(pathlib.Path(__file__).resolve().parent.parent.parent) if "__file__" in globals() else os.getcwd()

def chat(model, words):
    prompt = ("Give the English gloss for each word below. Return ONLY compact JSON:\n"
              '{"glosses":[{"word":"<original>","en":"<english gloss>"}]}\n\nWords:\n' + "\n".join(words))
    body = json.dumps({"model": model, "messages": [
        {"role": "system", "content": "You are a multilingual lexicographer. Respond ONLY with valid JSON."},
        {"role": "user", "content": prompt}], "temperature": 0.0, "max_tokens": 2048}).encode()
    req = urllib.request.Request(BASE + "/chat/completions", data=body,
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    raw = urllib.request.urlopen(req, timeout=120).read().decode("utf-8", "ignore")
    try:
        content = json.loads(raw)["choices"][0]["message"]["content"]
        # strip code fences
        if "```json" in content: content = content.split("```json")[1].split("```")[0]
        elif "```" in content: content = content.split("```")[1].split("```")[0]
        gl = json.loads(content).get("glosses", [])
        return {g.get("word", "").strip(): g.get("en", "").strip() for g in gl if g.get("word")}
    except Exception as e:
        print(f"[warn] {model} parse fail: {e} raw_head={raw[:200]!r}", file=sys.stderr)
        return {}

def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: qwen_cross_gloss_30.py [--help]  (no other options; models via $QWEN_MODELS)")
        print("  Fetches English glosses for wiki_gloss_audit_30 (30 words) and writes")
        print("  research/wiki_gloss_audit_30_qwen_cross_20260914.json. Key ONLY from env.")
        return
    import pathlib
    root = pathlib.Path(PROJECT)
    audit = json.loads((root / "research" / "wiki_gloss_audit_30.json").read_text(encoding="utf-8"))
    words = [r["zh"] for r in audit["records"]]
    out = {"meta": {"models": MODELS, "n": len(words)}, "records": []}
    maps = {}
    for m in MODELS:
        maps[m] = chat(m, words)
        print(f"[{m}] got {len(maps[m])}/{len(words)}")
    for r in audit["records"]:
        w = r["zh"]
        rec = {"audit_id": r["audit_id"], "zh": w, "gloss_en": r.get("gloss_en", ""),
               "qwen_cross": {m: maps[m].get(w, "") for m in MODELS}}
        # agreement: flash vs max (case-insensitive exact match)
        vals = [v.lower() for v in rec["qwen_cross"].values() if v]
        rec["cross_agree"] = len(set(vals)) == 1 if vals else False
        rec["match_source"] = (vals and vals[0] == r.get("gloss_en", "").lower())
        out["records"].append(rec)
    agree = sum(1 for r in out["records"] if r["cross_agree"])
    print(f"cross_agree={agree}/{len(words)}")
    (root / "research" / "wiki_gloss_audit_30_qwen_cross_20260914.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved research/wiki_gloss_audit_30_qwen_cross_20260914.json")

if __name__ == "__main__":
    main()
