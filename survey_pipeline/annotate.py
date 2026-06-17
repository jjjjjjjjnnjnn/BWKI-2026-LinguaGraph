"""
Survey Pipeline — LLM Annotation
==================================
Extract concepts and relations from survey responses using LLM.

Usage:
    python annotate.py                    # Annotate all unprocessed responses
    python annotate.py --student S001     # Annotate one student
    python annotate.py --mock             # Use mock extraction (no LLM)
"""

import json
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from db_utils import get_connection, query, query_one, insert

from config import (
    LLM_BASE_URL, LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS,
    USE_MOCK_EXTRACTION, ANNOTATION_BATCH_SIZE
)


def call_llm(system: str, user: str, temperature: float = LLM_TEMPERATURE) -> Optional[str]:
    """Call LLM via OpenAI-compatible API."""
    try:
        from openai import OpenAI
        client = OpenAI(base_url=LLM_BASE_URL, api_key="not-needed")
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=LLM_MAX_TOKENS,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"    [WARN] LLM call failed: {e}")
        return None


def build_extraction_prompt(text: str, language: str) -> tuple:
    """Build system and user prompts for concept extraction."""
    system = """You are a cognitive linguistics concept extractor.

Extract cognitive concepts and their relationships from the given text.

Output JSON ONLY. No explanations, no markdown.
Format:
{
  "concepts": ["concept1", "concept2", ...],
  "relations": [
    {"source": "concept1", "target": "concept2", "type": "relation_type"}
  ]
}

Relation types: requires, is_a, part_of, enables, causes, equivalent, contradicts, co_occurs

Rules:
1. Extract 3-8 key concepts (nouns, noun phrases)
2. Extract 2-5 explicit relationships
3. Use the SAME language as the input text for concept names
4. Keep concept names concise (1-3 words)
5. Focus on the MAIN ideas, not every detail"""

    user = f"Language: {language}\n\nText:\n{text}"

    return system, user


def parse_llm_response(raw: str) -> dict:
    """Parse LLM JSON response, handling common issues."""
    if not raw:
        return {"concepts": [], "relations": []}

    cleaned = raw.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
        if "concepts" not in data:
            data["concepts"] = []
        if "relations" not in data:
            data["relations"] = []
        return data
    except json.JSONDecodeError:
        import re
        match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
                if "concepts" not in data:
                    data["concepts"] = []
                if "relations" not in data:
                    data["relations"] = []
                return data
            except json.JSONDecodeError:
                pass
        return {"concepts": [], "relations": []}


def annotate_response(response_id: str, text: str, language: str, use_mock: bool = False) -> dict:
    """Annotate a single response with concepts and relations."""
    if use_mock or USE_MOCK_EXTRACTION:
        return mock_annotate(text, language)

    system, user = build_extraction_prompt(text, language)
    raw = call_llm(system, user)
    result = parse_llm_response(raw)

    return {
        "concepts": result.get("concepts", []),
        "relations": result.get("relations", []),
        "raw_response": raw or "",
    }


def mock_annotate(text: str, language: str) -> dict:
    """Mock annotation using keyword matching (no LLM needed)."""
    import re

    # Simple keyword extraction
    keywords_zh = {
        "成功": ["成功", "成就", "目标"],
        "努力": ["努力", "奋斗", "坚持"],
        "家庭": ["家庭", "家人", "父母"],
        "责任": ["责任", "义务", "担当"],
        "自由": ["自由", "自主", "选择"],
        "社会": ["社会", "集体", "公共"],
        "法律": ["法律", "法治", "规则"],
        "道德": ["道德", "良心", "伦理"],
    }

    keywords_en = {
        "success": ["success", "achievement", "goal"],
        "effort": ["effort", "hard work", "perseverance"],
        "family": ["family", "parents", "home"],
        "responsibility": ["responsibility", "duty", "obligation"],
        "freedom": ["freedom", "liberty", "choice"],
        "society": ["society", "community", "public"],
        "law": ["law", "legal", "justice"],
        "morality": ["morality", "ethics", "conscience"],
    }

    keywords_de = {
        "Erfolg": ["Erfolg", "Leistung", "Ziel"],
        "Anstrengung": ["Anstrengung", "Mühe", "Aufwand"],
        "Familie": ["Familie", "Eltern", "Zuhause"],
        "Verantwortung": ["Verantwortung", "Pflicht", "Obliegenheit"],
        "Freiheit": ["Freiheit", "Wahl", "Selbstbestimmung"],
        "Gesellschaft": ["Gesellschaft", "Gemeinschaft", "Öffentlichkeit"],
        "Gesetz": ["Gesetz", "Recht", "Justiz"],
        "Moral": ["Moral", "Ethik", "Gewissen"],
    }

    kw_map = {"zh": keywords_zh, "en": keywords_en, "de": keywords_de}
    keywords = kw_map.get(language, keywords_en)

    found = []
    for concept, words in keywords.items():
        for w in words:
            if w.lower() in text.lower():
                found.append(concept)
                break

    # Generate simple relations
    relations = []
    for i, c1 in enumerate(found):
        for c2 in found[i+1:]:
            relations.append({
                "source": c1,
                "target": c2,
                "type": "co_occurs"
            })

    return {
        "concepts": found[:8],
        "relations": relations[:5],
        "raw_response": json.dumps({"concepts": found, "relations": relations}, ensure_ascii=False),
    }


def annotate_student(conn, student_id: str, use_mock: bool = False) -> dict:
    """Annotate all responses for a student."""
    responses = query(conn, """
        SELECT response_id, answer_text, language, question_id
        FROM responses
        WHERE student_id = ? AND source = 'survey'
        ORDER BY language, question_id
    """, (student_id,))

    if not responses:
        return {"error": "no responses found"}

    results = {
        "student_id": student_id,
        "annotated": 0,
        "skipped": 0,
        "errors": 0,
        "extractions": [],
    }

    for r in responses:
        # Skip if already annotated
        existing = query_one(conn, """
            SELECT extraction_id FROM extractions
            WHERE response_id = ?
        """, (r["response_id"],))
        if existing:
            results["skipped"] += 1
            continue

        text = r["answer_text"]
        if not text or len(text) < 10:
            results["skipped"] += 1
            continue

        try:
            extraction = annotate_response(
                r["response_id"], text, r["language"], use_mock=use_mock
            )

            extraction_id = f"E_{student_id}_{r['response_id']}"

            insert(conn, "extractions", {
                "extraction_id": extraction_id,
                "response_id": r["response_id"],
                "student_id": student_id,
                "concepts": json.dumps(extraction["concepts"], ensure_ascii=False),
                "relations": json.dumps(extraction["relations"], ensure_ascii=False),
                "raw_response": extraction.get("raw_response", ""),
                "model": "mock" if use_mock else LLM_MODEL,
                "extraction_type": "survey",
            })

            results["annotated"] += 1
            results["extractions"].append({
                "response_id": r["response_id"],
                "concepts": extraction["concepts"],
                "relation_count": len(extraction["relations"]),
            })

            if not use_mock:
                time.sleep(0.5)  # Rate limiting

        except Exception as e:
            results["errors"] += 1
            print(f"    [ERROR] {r['response_id']}: {e}")

    conn.commit()
    return results


def annotate_all(use_mock: bool = False):
    """Annotate all unprocessed survey responses."""
    print(f"\n{'='*60}")
    print(f"  LLM Concept Annotation")
    print(f"{'='*60}\n")

    conn = get_connection()

    # Get all students with survey responses
    students = query(conn, """
        SELECT DISTINCT student_id FROM responses
        WHERE source = 'survey'
        ORDER BY student_id
    """)

    print(f"  Students to annotate: {len(students)}")

    total_annotated = 0
    total_errors = 0

    for s in students:
        sid = s["student_id"]
        print(f"\n  Annotating {sid}...")

        result = annotate_student(conn, sid, use_mock=use_mock)
        print(f"    Annotated: {result['annotated']}, Skipped: {result['skipped']}, Errors: {result['errors']}")

        total_annotated += result["annotated"]
        total_errors += result["errors"]

    conn.close()

    print(f"\n{'='*60}")
    print(f"  Annotation complete: {total_annotated} annotated, {total_errors} errors")
    print(f"{'='*60}\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Annotate survey responses")
    parser.add_argument("--student", help="Annotate specific student")
    parser.add_argument("--mock", action="store_true", help="Use mock extraction")
    args = parser.parse_args()

    if args.student:
        conn = get_connection()
        result = annotate_student(conn, args.student, use_mock=args.mock)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        conn.close()
    else:
        annotate_all(use_mock=args.mock)


if __name__ == "__main__":
    main()
