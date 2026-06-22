#!/usr/bin/env python3
"""
LinguaGraph — Batch Response Processing Pipeline
=================================================
Batch-submits unextracted survey responses to LM Studio for concept extraction.
Supports: progress tracking, resume, retry, timing.

Usage:
    python scripts/batch_process_responses.py                          # Process all unextracted
    python scripts/batch_process_responses.py --dry-run                # Show what would be processed
    python scripts/batch_process_responses.py --gold-only              # Only gold label responses
    python scripts/batch_process_responses.py --max 50                # Process max 50 and stop
    python scripts/batch_process_responses.py --resume                # Skip already-extracted (default)

Authors: BWKI 2026 — LinguaGraph Team
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Ensure project root is on path
PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / "scripts"))

from db_utils import get_connection, insert, query, query_one


# ===== CONFIGURATION =====

LM_STUDIO_URL = "http://localhost:1234/v1"
MODEL_NAME = "qwen/qwen3-8b"
API_KEY = ""  # Set via --api-key or OPENROUTER_API_KEY env
BATCH_SIZE = 10  # Responses between DB reads
REQUEST_TIMEOUT = 120  # Seconds per LLM call
MAX_RETRIES = 3

EXTRACTION_PROMPT_TEMPLATE = """{example}

学生回答：
{text}

提取该回答中的核心概念，输出JSON格式。"""

EXTRACTION_PROMPT_EN = """{example}

Student response:
{text}

Extract the core concepts from this response. Output JSON format."""

EXTRACTION_PROMPT_DE = """{example}

Schülerantwort:
{text}

Extrahiere die Kernkonzepte aus dieser Antwort. Ausgabe im JSON-Format."""

EXAMPLES = {
    "zh": '{"concepts": ["自由", "责任", "权利"]}',
    "en": '{"concepts": ["freedom", "responsibility", "choice"]}',
    "de": '{"concepts": ["Freiheit", "Verantwortung", "Selbstbestimmung"]}',
}


# ===== LLM INTERFACE =====

def call_llm(prompt: str, language: str = "zh", temperature: float = 0.3) -> Optional[Dict]:
    """Call LLM (OpenRouter or LM Studio) for concept extraction. Returns parsed JSON dict or None."""
    from openai import OpenAI

    # Choose prompt + example by language
    example = EXAMPLES.get(language, EXAMPLES["en"])

    if language == "de":
        system = "Du bist ein präziser Kognitionsextraktor. Antworte NUR mit JSON, ohne Erklärung."
        user = EXTRACTION_PROMPT_DE.format(example=example, text=prompt)
    elif language == "en":
        system = "You are a precise concept extractor. Respond ONLY with JSON, no explanation."
        user = EXTRACTION_PROMPT_EN.format(example=example, text=prompt)
    else:
        system = "你是一名精准的概念提取器。只输出 JSON，不输出解释。"
        user = EXTRACTION_PROMPT_TEMPLATE.format(example=example, text=prompt)

    for attempt in range(MAX_RETRIES):
        try:
            client = OpenAI(base_url=LM_STUDIO_URL, api_key=API_KEY if API_KEY else "not-needed")
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=temperature,
                max_tokens=1024,
                timeout=REQUEST_TIMEOUT,
            )
            raw = response.choices[0].message.content.strip()
            return _parse_json_response(raw)
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                wait = 2 ** attempt
                print(f"    [RETRY {attempt+1}/{MAX_RETRIES}] {e} — waiting {wait}s")
                time.sleep(wait)
            else:
                print(f"    [FAIL] All {MAX_RETRIES} retries exhausted: {e}")
                return None


def _parse_json_response(raw: str) -> Optional[Dict]:
    """Parse JSON from LLM response, handling think tags, markdown fences, and stray text."""
    # Strip <think> tags (Qwen's reasoning output)
    import re
    cleaned = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL)
    cleaned = cleaned.replace("</think>", "").replace("<think>", "")
    cleaned = cleaned.strip()

    # Strip markdown code fences
    if "```json" in cleaned:
        cleaned = cleaned.split("```json")[1].split("```")[0].strip()
    elif "```" in cleaned:
        cleaned = cleaned.split("```")[1].split("```")[0].strip()

    # Try parsing
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to find {...} as fallback
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        return None


# ===== DATABASE OPERATIONS =====

def get_unextracted_responses(conn, gold_only: bool = False, max_count: Optional[int] = None) -> List[Dict]:
    """Get responses that don't have extractions yet."""
    conditions = ["e.extraction_id IS NULL"]
    if gold_only:
        conditions.append("r.student_id = 'GOLD_LABEL'")

    where_clause = " AND ".join(conditions)

    sql = f"""
        SELECT r.response_id, r.student_id, r.language, r.question_id, r.answer_text, r.word_count
        FROM responses r
        LEFT JOIN extractions e ON r.response_id = e.response_id
        WHERE {where_clause}
        ORDER BY r.created_at
    """

    if max_count:
        sql += f" LIMIT {max_count}"

    rows = query(conn, sql)
    return rows


def save_extraction(conn, response_id: str, model_used: str,
                    concepts: List[str], raw_response: str,
                    extraction_time_ms: int) -> str:
    """Save extraction result to database."""
    ext_id = f"E_{datetime.now().strftime('%Y%m%d')}_{response_id[:20]}"

    data = {
        "extraction_id": ext_id,
        "response_id": response_id,
        "model_used": model_used,
        "concepts": json.dumps(concepts, ensure_ascii=False),
        "relations": "[]",
        "missing_hints": json.dumps([]),
        "raw_response": raw_response[:1000] if raw_response else "",
        "extraction_time_ms": extraction_time_ms,
        "confidence": 1.0,
    }

    insert(conn, "extractions", data)
    return ext_id


def get_processing_status(conn) -> Dict:
    """Get processing status summary."""
    total = query_one(conn, "SELECT COUNT(*) as c FROM responses")["c"]
    extracted = query_one(conn, "SELECT COUNT(*) as c FROM extractions")["c"]
    gold_total = query_one(conn, "SELECT COUNT(*) as c FROM responses WHERE student_id='GOLD_LABEL'")["c"]
    gold_extracted = query_one(conn, """
        SELECT COUNT(*) as c FROM responses r
        JOIN extractions e ON r.response_id = e.response_id
        WHERE r.student_id='GOLD_LABEL'
    """)["c"]

    return {
        "total_responses": total,
        "extracted": extracted,
        "remaining": total - extracted,
        "gold_total": gold_total,
        "gold_extracted": gold_extracted,
        "gold_remaining": gold_total - gold_extracted,
    }


# ===== MAIN PROCESSING LOOP =====

def process_batch(conn, responses: List[Dict], batch_label: str = "") -> Tuple[int, int]:
    """Process a batch of responses. Returns (success_count, fail_count)."""
    total = len(responses)
    success = 0
    fail = 0
    start_time = time.time()

    for idx, row in enumerate(responses):
        response_id = row["response_id"]
        language = row["language"] or "zh"
        answer_text = row.get("answer_text", "")

        if not answer_text or not answer_text.strip():
            print(f"  [{idx+1}/{total}] [SKIP] {response_id} — empty response")
            fail += 1
            continue

        print(f"  [{idx+1}/{total}] {response_id} ({language}, {len(answer_text)} chars)...", end=" ", flush=True)
        t0 = time.time()

        result = call_llm(answer_text, language=language)

        elapsed_ms = int((time.time() - t0) * 1000)

        if result and "concepts" in result:
            concepts = result["concepts"]
            concepts = [c.strip() for c in concepts if c and c.strip()]
            ext_id = save_extraction(conn, response_id, f"{MODEL_NAME} (batch)",
                                     concepts, json.dumps(result, ensure_ascii=False), elapsed_ms)
            print(f"  OK {len(concepts)} concepts ({elapsed_ms}ms)")
            success += 1
        else:
            # Save failed attempt with empty concepts so we don't retry indefinitely
            save_extraction(conn, response_id, f"{MODEL_NAME} (batch)",
                           [], json.dumps(result or {}), elapsed_ms)
            print(f"  FAIL parse ({elapsed_ms}ms)")
            fail += 1

        # Small delay between calls
        time.sleep(0.2)

    elapsed = time.time() - start_time
    print(f"  Batch done: {success} success, {fail} failed in {elapsed:.0f}s ({elapsed/max(total,1):.1f}s/response)")
    return success, fail


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Batch process responses through LLM extraction")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed without processing")
    parser.add_argument("--gold-only", action="store_true", help="Only process gold label responses")
    parser.add_argument("--max", type=int, default=None, help="Max responses to process (default: all)")
    parser.add_argument("--status", action="store_true", help="Show processing status only")
    parser.add_argument("--source", type=str, default=None, help="Filter by source (e.g., 'simulation', 'survey')")
    parser.add_argument("--model", type=str, default=None, help="Model name (e.g., 'qwen/qwen3-8b', 'qwen2.5-0.5b-instruct')")
    parser.add_argument("--api-url", type=str, default=None, help="OpenAI-compatible API URL (default: LM Studio localhost:1234)")
    parser.add_argument("--api-key", type=str, default=None, help="API key (or set OPENROUTER_API_KEY env var)")
    args = parser.parse_args()

    # Override model if specified
    global MODEL_NAME, LM_STUDIO_URL, API_KEY
    if args.model:
        MODEL_NAME = args.model
        print(f"  [MODEL] Override: {MODEL_NAME}")
    if args.api_url:
        LM_STUDIO_URL = args.api_url
        print(f"  [API] Override: {LM_STUDIO_URL}")
    if args.api_key:
        API_KEY = args.api_key
    elif os.environ.get("OPENROUTER_API_KEY"):
        API_KEY = os.environ["OPENROUTER_API_KEY"]

    conn = get_connection()
    status = get_processing_status(conn)

    print(f"\n{'='*60}")
    print(f"  LinguaGraph — Batch Response Processor")
    print(f"{'='*60}")
    print(f"\n  Current Status:")
    print(f"    Total responses:    {status['total_responses']}")
    print(f"    Already extracted:  {status['extracted']}")
    print(f"    Remaining:          {status['remaining']}")
    print(f"    Gold total:         {status['gold_total']}")
    print(f"    Gold remaining:     {status['gold_remaining']}")

    if args.status:
        conn.close()
        return

    # Get unextracted responses
    responses = get_unextracted_responses(conn, gold_only=args.gold_only, max_count=args.max)

    if args.source:
        responses = [r for r in responses if r.get("source") == args.source]

    if not responses:
        print(f"\n  ✅ All responses processed! Nothing to do.")
        conn.close()
        return

    print(f"\n  Processing: {len(responses)} unextracted responses")
    if args.dry_run:
        print(f"\n  Sample responses to process:")
        for r in responses[:5]:
            text_preview = (r.get("answer_text") or "")[:60]
            print(f"    {r['response_id']} ({r['language']}): {text_preview}...")
        if len(responses) > 5:
            print(f"    ... and {len(responses) - 5} more")
        conn.close()
        return

    # Confirm
    print(f"\n  Starting extraction with model: {MODEL_NAME}")
    print(f"  LM Studio endpoint: {LM_STUDIO_URL}")
    print(f"\n  {'='*60}")
    print(f"  Processing {len(responses)} responses...")
    print(f"  {'='*60}\n")

    t0 = time.time()
    success, fail = process_batch(conn, responses)
    elapsed = time.time() - t0

    print(f"\n  {'='*60}")
    print(f"  Complete: {success} success, {fail} failed")
    print(f"  Total time: {elapsed:.0f}s ({elapsed/60:.1f}m)")
    print(f"  Avg: {elapsed/max(success+fail,1):.1f}s/response")
    print(f"  {'='*60}")

    conn.close()


if __name__ == "__main__":
    main()
