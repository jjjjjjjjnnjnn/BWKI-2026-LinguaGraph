#!/usr/bin/env python3
"""Bailian (DashScope OpenAI-compatible) independent re-extraction of textbook files.

Reads BAILIAN_API_KEY/BAILIAN_BASE from env. NEVER writes key to disk.
Usage: python scripts/tools/bailian_reextract.py <basename> [--model ID] [--timeout S]
Output: research/bailian_audit/<basename>.bailian.json
"""
import json, os, re, sys, urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.environ.get("BAILIAN_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
KEY = os.environ.get("BAILIAN_API_KEY", "")
try:
    MAX_TOKENS = int(os.environ.get("BAILIAN_MAX_TOKENS", "8000"))
except Exception:
    MAX_TOKENS = 8000
OUTDIR = os.path.join(BASE_DIR, "research", "bailian_audit")

PROMPT = """TASK: Extract knowledge-graph JSON from the textbook text at the end. Do NOT ask questions. Do NOT converse. Do NOT explain. Output ONLY the JSON object, nothing else before or after it.

Schema:
{"extracted_concepts": [{"name": "<source-language name>", "aliases": ["english", "chinese"], "definition_snippet": "<short>", "category": "concept|operation|theorem|property"}],
 "extracted_relations": [{"source": "<name from concepts>", "target": "<name from concepts>", "type": "requires|representation|generalization|inverse_of|part_of", "importance": 0.0-1.0, "evidence": "<short>"}]}
Keys MUST be exactly "extracted_concepts" and "extracted_relations" (never "nodes"/"edges"/"concepts"/"relations"). Aim 15-40 concepts, 10-30 relations. Every source/target must be a listed concept name. No placeholders. Empty lists are FORBIDDEN.

TEXTBOOK (%s / %s):
%s
BEGIN JSON NOW:"""

LANGS = {"de": "German", "en": "English", "zh": "Chinese"}


def call(model, prompt, timeout):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "temperature": 0, "max_tokens": MAX_TOKENS}).encode()
    req = urllib.request.Request(BASE + "/chat/completions", data=body,
                                 headers={"Authorization": "Bearer " + KEY,
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.load(r)
    msg = d["choices"][0]["message"]
    content = msg.get("content") or ""
    if not (isinstance(content, str) and content.strip()):
        # deepseek compat fallback: empty content -> reasoning_content
        rc = msg.get("reasoning_content") or ""
        if isinstance(rc, str) and rc.strip():
            content = rc
    return content


def parse(raw):
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return None
    try:
        d = json.loads(m.group())
    except Exception:
        return None
    if not isinstance(d, dict) or "extracted_concepts" not in d or "extracted_relations" not in d:
        return None
    cs = d["extracted_concepts"]
    if not isinstance(cs, list) or len(cs) == 0:
        return None
    names = {c.get("name", "") for c in cs if isinstance(c, dict)}
    if any(v in ("...", "..", "") for v in names):
        return None
    return d


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: bailian_reextract.py <basename> [--model ID] [--timeout S] [--help]")
        print("  Extracts knowledge-graph JSON from data/textbook/<basename>.txt via DashScope")
        print("  compatible-mode (temperature=0, max_tokens from $BAILIAN_MAX_TOKENS, default 8000).")
        print("  Output: research/bailian_audit/<basename>.bailian.json. Key ONLY from env.")
        return
    if not KEY:
        print("ERROR: BAILIAN_API_KEY unset", file=sys.stderr)
        sys.exit(1)
    base = sys.argv[1]
    model = "qwen-flash"
    timeout = 300
    for i, a in enumerate(sys.argv[2:]):
        if a == "--model":
            model = sys.argv[3 + i]
        if a == "--timeout":
            timeout = int(sys.argv[3 + i])
    txt_p = os.path.join(BASE_DIR, "data", "textbook", base + ".txt")
    if not os.path.exists(txt_p):
        print(json.dumps({"base": base, "model": model, "parsed": None,
                          "note": "source_txt_missing"}))
        os.makedirs(OUTDIR, exist_ok=True)
        json.dump({"base": base, "model": model, "parsed": None,
                   "note": "source_txt_missing", "raw": ""},
                  open(os.path.join(OUTDIR, base + ".bailian.json"), "w", encoding="utf-8"),
                  ensure_ascii=False)
        sys.exit(2)
    text = open(txt_p, encoding="utf-8", errors="ignore").read()
    lang = LANGS.get(base.split("_")[0], "German")
    try:
        raw = call(model, PROMPT % (lang, base, text), timeout)
    except Exception as e:
        print("CALL_ERROR: %s: %s" % (type(e).__name__, str(e)[:200]), file=sys.stderr)
        sys.exit(3)
    parsed = parse(raw)
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump({"base": base, "model": model, "parsed": parsed, "raw": raw},
              open(os.path.join(OUTDIR, base + ".bailian.json"), "w", encoding="utf-8"),
              ensure_ascii=False)
    if parsed:
        print("OK c=%d r=%d" % (len(parsed["extracted_concepts"]),
                                len(parsed["extracted_relations"])))
    else:
        head = raw[:200].encode("ascii", "replace").decode("ascii")
        print("PARSE_FAIL raw_len=%d head=%s" % (len(raw), head))
        sys.exit(4)


if __name__ == "__main__":
    main()
