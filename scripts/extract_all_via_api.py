#!/usr/bin/env python3
"""Run full extraction on all survey responses using qwen-plus via BaiLian API."""

import json, os, re, sqlite3, sys, time
from collections import defaultdict
from datetime import datetime
from openai import OpenAI
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / "scripts"))
from db_utils import insert

API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
API_KEY = os.environ.get("BAILIAN_API_KEY", "")
if not API_KEY:
    print("ERROR: Set BAILIAN_API_KEY environment variable")
    sys.exit(1)
MODEL = "qwen-plus"
BATCH_SIZE = 20

EXAMPLES = {
    "zh": '{"concepts": ["自由", "责任", "权利"]}',
    "en": '{"concepts": ["freedom", "responsibility", "choice"]}',
    "de": '{"concepts": ["Freiheit", "Verantwortung", "Selbstbestimmung"]}',
}

def call_api(text, lang):
    client = OpenAI(base_url=API_URL, api_key=API_KEY)
    example = EXAMPLES.get(lang, EXAMPLES["en"])
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是概念提取助手。只输出JSON。"},
                {"role": "user", "content": f"{example}\n\nText: {text}\n\n提取概念为JSON格式。"},
            ],
            temperature=0.3, max_tokens=256, timeout=30,
        )
        raw = resp.choices[0].message.content.strip()
        cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        data = json.loads(match.group()) if match else {}
        return data.get("concepts", []), raw
    except Exception as e:
        return [], f"ERROR: {e}"

def main():
    conn = sqlite3.connect(str(PROJECT_DIR / "linguaGraph.db"))
    conn.text_factory = bytes

    # Get all responses WITHOUT extractions
    responses = conn.execute("""
        SELECT r.response_id, r.answer_text, r.language
        FROM responses r
        LEFT JOIN extractions e ON r.response_id = e.response_id
        WHERE e.extraction_id IS NULL
        AND r.source = 'survey'
        ORDER BY r.response_id
    """).fetchall()
    conn.close()

    if not responses:
        print("All responses already extracted.")
        return

    total = len(responses)
    success = 0
    t0 = time.time()

    conn = sqlite3.connect(str(PROJECT_DIR / "linguaGraph.db"))

    for idx, item in enumerate(responses):
        resp_id = item[0].decode()
        text = item[1].decode() if item[1] else ""
        lang = item[2].decode()

        if not text.strip():
            print(f"  [{idx+1}/{total}] {resp_id} empty, skipping")
            continue

        print(f"  [{idx+1}/{total}] {resp_id} ({lang})...", end=" ", flush=True)
        call_t0 = time.time()
        concepts, raw = call_api(text, lang)
        elapsed = int((time.time() - call_t0) * 1000)

        if concepts:
            ext_id = f"E_qwenplus_{resp_id[:20]}"
            insert(conn, "extractions", {
                "extraction_id": ext_id,
                "response_id": resp_id,
                "model_used": "qwen-plus (batch)",
                "concepts": json.dumps(concepts, ensure_ascii=False),
                "relations": "[]",
                "missing_hints": "[]",
                "raw_response": raw[:500],
                "extraction_time_ms": elapsed,
                "confidence": 1.0,
            })
            print(f"OK {len(concepts)} conc ({elapsed}ms)")
            success += 1
        else:
            print(f"FAIL ({elapsed}ms)")
        time.sleep(0.1)

    conn.commit()
    conn.close()
    elapsed = time.time() - t0
    print(f"\nDone: {success}/{total} success in {elapsed:.0f}s ({elapsed/60:.1f}m)")

if __name__ == "__main__":
    main()
