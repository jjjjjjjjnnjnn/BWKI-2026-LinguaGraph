"""
LinguaGraph — Structured Cognitive Simulation Dataset Generator
=================================================================
Generates 300 simulated responses (5 concepts × 3 languages × 20 samples)
as a controlled computational cognitive simulation baseline.

Design:
  - NOT free-text generation
  - Persona-based cognitive simulation
  - Structured JSON output
  - Batched generation (60 per batch)
  - Fully reproducible (seed-controlled)
  - Clear synthetic data labeling

Usage:
    python scripts/simulate_baseline.py --generate     # Generate all 300 responses
    python scripts/simulate_baseline.py --batch 1      # Batch 1: success + freedom
    python scripts/imitate_baseline.py --batch 2       # Batch 2: responsibility + justice
    python scripts/simulate_baseline.py --status       # Show generation status
    python scripts/simulate_baseline.py --pipeline     # Run full pipeline on simulated data

Data Isolation:
    All simulated data uses source='simulation' and student_id='SIMULATION'
    in the database, clearly separated from human data.
"""

import json
import os
import sys
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR / 'src'))
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / 'scripts'))  # for db_utils

from db_utils import get_connection, insert, query, query_one


# ===== PERSONA DEFINITIONS =====
PERSONAS = {
    "zh": {
        "name": "Chinese native speaker",
        "background": "Born and raised in mainland China. Attended school in Chinese. Daily life and thinking are in Chinese. Never lived abroad for extended periods.",
        "culture_note": "Collectivist cultural background. Family and social harmony are important reference points.",
        "style": "Naturally expresses concepts through relationships and social context.",
    },
    "de": {
        "name": "German native speaker",
        "background": "Born and raised in Germany. Attended school in German. Daily life and thinking are in German. Never lived abroad for extended periods.",
        "culture_note": "Individualist cultural background with strong philosophical tradition. Precision and system-building are natural.",
        "style": "Naturally expresses concepts through principles, systems, and categorical distinctions.",
    },
    "en": {
        "name": "English native speaker (American)",
        "background": "Born and raised in the United States. Attended school in English. Daily life and thinking are in English. Never lived abroad for extended periods.",
        "culture_note": "Individualist cultural background emphasizing personal choice and opportunity.",
        "style": "Naturally expresses concepts through individual agency, rights, and practical outcomes.",
    },
}

# ===== CONCEPT QUESTIONS =====
QUESTIONS = {
    "freedom": {"zh": "什么是自由？", "de": "Was ist Freiheit?", "en": "What is freedom?"},
    "justice": {"zh": "什么是公平？", "de": "Was ist Gerechtigkeit?", "en": "What is justice or fairness?"},
    "success": {"zh": "什么算是好的人生？", "de": "Was macht ein gelungenes Leben aus?", "en": "What makes a good life?"},
    "responsibility": {"zh": "责任是什么？", "de": "Was bedeutet Verantwortung?", "en": "What does responsibility mean?"},
    "home": {"zh": "家对你意味着什么？", "de": "Was bedeutet Heimat?", "en": "What does home mean to you?"},
}

CONCEPTS = ["freedom", "justice", "success", "responsibility", "home"]
LANGUAGES = ["zh", "de", "en"]
BATCH_SIZE = 60  # 2 concepts × 3 languages × 10 samples per batch
SAMPLES_PER_CELL = 20  # 20 responses per (concept × language) cell
TOTAL_RESPONSES = len(CONCEPTS) * len(LANGUAGES) * SAMPLES_PER_CELL  # = 300

OUTPUT_DIR = PROJECT_DIR / "data" / "corpus" / "simulation"


def get_seed(concept: str, lang: str, sample_idx: int) -> int:
    """Deterministic seed for reproducibility."""
    seed_str = f"linguaGraph_simulation_{concept}_{lang}_{sample_idx}_v1"
    return int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)


def build_system_prompt() -> str:
    """Build the system prompt for the simulation generator."""
    return """You are a cognitive linguistics simulation engine.
Your task is to generate realistic human-like responses for a cross-language study.

RULES:
1. Output JSON ONLY. No explanations, no markdown.
2. Each response must be exactly 1-3 sentences, natural and spontaneous.
3. Do NOT use philosophical or academic language. Respond like an ordinary person.
4. Each response must reflect the persona's cultural background naturally.
5. Vary the responses across samples — do NOT repeat patterns.
6. Do NOT mention "as a [nationality] person" — just answer naturally.

The response should sound like someone quickly answering a survey question,
not like an essay or a dictionary definition."""


def build_user_prompt(concept: str, lang: str, persona_key: str, n: int, existing: List[str]) -> str:
    """Build the batch generation prompt for one (concept × language × n) cell."""
    persona = PERSONAS[persona_key]
    question = QUESTIONS[concept][lang]

    # Show existing responses to avoid repetition
    diversity_instruction = ""
    if existing:
        sample_existing = existing[:3]
        diversity_instruction = f"\n\nALREADY GENERATED (avoid repeating these patterns):\n"
        for s in sample_existing:
            diversity_instruction += f"- {s[:80]}...\n"

    return f"""Generate {n} independent responses from ONE specific persona.

PERSONA: {persona['name']}
BACKGROUND: {persona['background']}
CULTURAL NOTE: {persona['culture_note']}
STYLE: {persona['style']}

QUESTION ({lang}): {question}

Respond in the same language as the question.{diversity_instruction}

Output as JSON array:
[
  {{"id": 1, "response": "..."}},
  {{"id": 2, "response": "..."}},
  ...
]"""


def call_llm(system: str, user: str, temperature: float = 0.9) -> Optional[str]:
    """Call the LLM (via project provider or direct API)."""
    try:
        # Use project's router/provider layer
        sys.path.insert(0, str(PROJECT_DIR / 'src'))
        from providers import create_router
        from src.models import TaskRequest, TaskType

        router = create_router()
        request = TaskRequest(
            task=TaskType.ANNOTATION_ASSIST,
            text=user_prompt,
            system_prompt=system_prompt,
            max_tokens=256,
            temperature=0.7,
        )
        response = router.route(request)
        if response.success:
            return response.raw_text
        else:
            raise RuntimeError(response.error)

        client = OpenAI(base_url=base_url, api_key='not-needed')
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"    [WARN] LLM call failed: {e}")
        return None


def parse_response(raw: str) -> List[Dict]:
    """Parse LLM response into structured list. Handles common JSON issues."""
    if not raw:
        return []

    # Strip markdown code fences
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
        if isinstance(data, list):
            return data
        return []
    except json.JSONDecodeError:
        # Try to extract JSON array from text
        import re
        match = re.search(r'\[.*?\]', cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                return []
        return []


def generate_batch(
    concept: str,
    lang: str,
    n: int = SAMPLES_PER_CELL,
    existing: Optional[List[str]] = None,
    temperature: float = 0.9,
) -> List[Dict]:
    """Generate n responses for one (concept × language) cell."""
    if existing is None:
        existing = []

    persona_key = lang
    system = build_system_prompt()
    user = build_user_prompt(concept, lang, persona_key, n, existing)

    print(f"    Generating {n} responses...", end=" ", flush=True)
    raw = call_llm(system, user, temperature=temperature)
    responses = parse_response(raw)
    print(f"got {len(responses)} valid responses")
    return responses


def save_cell(concept: str, lang: str, responses: List[Dict]):
    """Save one (concept × language) cell to JSON file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / f"{concept}_{lang}.json"

    # Tag each response with metadata
    tagged = []
    for i, r in enumerate(responses):
        tagged.append({
            "id": r.get("id", i + 1),
            "concept": concept,
            "language": lang,
            "persona": PERSONAS[lang]["name"],
            "response": r.get("response", ""),
            "seed": get_seed(concept, lang, i),
            "source": "simulation",
            "generated_at": datetime.now().isoformat(),
        })

    # Load existing if any, merge
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            existing = json.load(f)
        existing.extend(tagged)
        tagged = existing

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(tagged, f, ensure_ascii=False, indent=2)

    print(f"    Saved {len(tagged)} total to {filepath.name}")
    return filepath


def import_to_db(concept: str, lang: str, responses: List[Dict]):
    """Import simulated responses into the database with clear markers."""
    conn = get_connection()

    # Ensure SIMULATION student exists
    try:
        insert(conn, "students", {
            "student_id": "SIMULATION",
            "native_lang": "N/A",
            "school_lang": "N/A",
            "consent": 1,
            "notes": "Simulation baseline - synthetic data",
        })
    except Exception:
        pass

    topic_map = {"freedom": "q1", "justice": "q2", "success": "q3", "responsibility": "q4", "home": "q5"}
    qid = topic_map[concept]

    count = 0
    for r in responses:
        answer = r.get("response", "").strip()
        if not answer:
            continue

        sid = f"SIM_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{count:03d}"
        word_count = len(answer.split()) if lang != "zh" else len([c for c in answer if '一' <= c <= '鿿'])

        try:
            insert(conn, "responses", {
                "response_id": f"RSIM_{concept}_{lang}_{count:04d}",
                "student_id": "SIMULATION",
                "questionnaire_id": f"simulation_{lang}",
                "language": lang,
                "question_id": qid,
                "answer_text": answer,
                "word_count": word_count,
                "source": "simulation",
                "quality_flag": "ok" if word_count >= 5 else "short",
            })
            count += 1
        except Exception as e:
            print(f"    [WARN] DB import: {e}")

    conn.commit()
    conn.close()
    return count


def generate_all(temperature: float = 0.9):
    """Generate all 300 responses across all concepts and languages."""
    print(f"\n{'='*60}")
    print(f"  LinguaGraph Simulation Generator")
    print(f"  Target: {TOTAL_RESPONSES} responses ({len(CONCEPTS)} concepts × {len(LANGUAGES)} languages × {SAMPLES_PER_CELL} samples)")
    print(f"{'='*60}\n")

    total = 0
    batches_done = set()

    for concept in CONCEPTS:
        for lang in LANGUAGES:
            cell_key = f"{concept}_{lang}"
            if cell_key in batches_done:
                continue

            print(f"\n  Cell: {concept} × {lang} ({PERSONAS[lang]['name']})")

            # Load existing responses for diversity
            cell_file = OUTPUT_DIR / f"{concept}_{lang}.json"
            existing_responses = []
            existing_texts = []
            if cell_file.exists():
                with open(cell_file, "r", encoding="utf-8") as f:
                    existing_responses = json.load(f)
                existing_texts = [r.get("response", "") for r in existing_responses]
                have = len(existing_responses)
                if have >= SAMPLES_PER_CELL:
                    print(f"    Already have {have}/{SAMPLES_PER_CELL} — skipping")
                    batches_done.add(cell_key)
                    total += have
                    continue
                need = SAMPLES_PER_CELL - have
                print(f"    Have {have}, need {need} more")
            else:
                need = SAMPLES_PER_CELL

            if need <= 0:
                batches_done.add(cell_key)
                total += SAMPLES_PER_CELL
                continue

            # Generate in sub-batches to avoid token limits
            sub_batch_size = min(need, 10)
            generated = []
            for sub_start in range(0, need, sub_batch_size):
                sub_n = min(sub_batch_size, need - sub_start)
                results = generate_batch(concept, lang, n=sub_n, existing=existing_texts, temperature=temperature)
                for r in results:
                    txt = r.get("response", "")
                    if txt and txt not in existing_texts:
                        generated.append(r)
                        existing_texts.append(txt)
                time.sleep(0.3)

            if generated:
                save_cell(concept, lang, generated)
                n_db = import_to_db(concept, lang, generated)
                print(f"    Imported {n_db} to database")
                total += len(generated)

            batches_done.add(cell_key)

    print(f"\n{'='*60}")
    print(f"  Generation complete: {total}/{TOTAL_RESPONSES} responses")
    if total < TOTAL_RESPONSES:
        print(f"  Missing: {TOTAL_RESPONSES - total} — run again to fill")
    print(f"{'='*60}")


def generate_batch_n(batch_num: int, temperature: float = 0.9):
    """Generate specific batch (1, 2, or 3)."""
    batches = {
        1: {"concepts": ["success", "freedom"], "langs": ["zh", "de", "en"]},
        2: {"concepts": ["responsibility", "justice"], "langs": ["zh", "de", "en"]},
        3: {"concepts": ["home"], "langs": ["zh", "de", "en"]},
    }

    if batch_num not in batches:
        print(f"[ERROR] Batch {batch_num} not found. Use 1, 2, or 3.")
        return

    config = batches[batch_num]
    n_per_cell = SAMPLES_PER_CELL
    expected = len(config["concepts"]) * len(config["langs"]) * n_per_cell
    print(f"\n  Batch {batch_num}: {config['concepts']} × {config['langs']} = {expected} responses")

    total = 0
    for concept in config["concepts"]:
        for lang in config["langs"]:
            cell_key = f"{concept}_{lang}"
            existing_texts = []
            cell_file = OUTPUT_DIR / f"{concept}_{lang}.json"
            if cell_file.exists():
                with open(cell_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                existing_texts = [r.get("response", "") for r in existing]
                if len(existing) >= n_per_cell:
                    print(f"  [SKIP] {cell_key}: already {len(existing)} responses")
                    total += len(existing)
                    continue

            print(f"\n  {cell_key}...")
            generated = generate_batch(concept, lang, n=n_per_cell, existing=existing_texts, temperature=temperature)
            if generated:
                save_cell(concept, lang, generated)
                n_db = import_to_db(concept, lang, generated)
                print(f"    DB: {n_db} imported")
                total += len(generated)
            time.sleep(0.5)

    print(f"\n  Batch {batch_num} complete: {total} responses")


def run_pipeline_on_simulation():
    """Run the full analysis pipeline on simulation data."""
    print(f"\n{'='*60}")
    print(f"  Running Pipeline on Simulation Data")
    print(f"{'='*60}")

    # Use the existing analyze_student pipeline
    sys.path.insert(0, str(PROJECT_DIR))
    from analyze_student import analyze_student_responses

    conn = get_connection()

    # Check if simulation data exists
    sim_count = query_one(conn, "SELECT COUNT(*) as c FROM responses WHERE source='simulation'")
    count = sim_count["c"] if sim_count else 0
    if count == 0:
        print("  [ERROR] No simulation data in DB. Run --generate first.")
        conn.close()
        return

    print(f"  Found {count} simulation responses in DB")

    # Run analysis
    result = analyze_student_responses(conn, "SIMULATION", use_mock=True, verbose=True)

    if result and "error" not in result:
        print(f"\n  LDS Results:")
        for comp in result.get("comparisons", []):
            print(f"    {comp['lang_pair']}: LCD={comp['lcd'].get('lcd_score', 'N/A')}")
    else:
        print(f"\n  [WARN] Analysis returned: {result}")

    conn.close()


def print_status():
    """Show current simulation generation status."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Simulation Generation Status")
    print(f"{'='*60}")

    total = 0
    target = TOTAL_RESPONSES

    # Check files
    for concept in CONCEPTS:
        for lang in LANGUAGES:
            cell_file = OUTPUT_DIR / f"{concept}_{lang}.json"
            file_count = 0
            if cell_file.exists():
                with open(cell_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                file_count = len(data)
            total += file_count
            status = "OK" if file_count >= SAMPLES_PER_CELL else "PARTIAL" if file_count > 0 else "EMPTY"
            print(f"  [{status:<7s}] {concept:<15s} {lang:<4s} {file_count:>3d}/{SAMPLES_PER_CELL}")

    print(f"\n  Total: {total}/{target} ({total/target*100:.0f}%)")
    if total >= target:
        print("  [OK] All cells complete! Ready for pipeline.")
    else:
        need = target - total
        print(f"  [WARN]  Need {need} more responses.")

    # DB check
    try:
        conn = get_connection()
        db_count = query_one(conn, "SELECT COUNT(*) as c FROM responses WHERE source='simulation'")
        db_n = db_count["c"] if db_count else 0
        print(f"  DB records (source='simulation'): {db_n}")
        conn.close()
    except Exception:
        pass

    print()


def generate_template():
    """Generate the empty template JSON structure for review before generation."""
    template = []
    idx = 0
    for concept in CONCEPTS:
        for lang in LANGUAGES:
            for i in range(SAMPLES_PER_CELL):
                idx += 1
                template.append({
                    "id": idx,
                    "concept": concept,
                    "language": lang,
                    "persona": PERSONAS[lang]["name"],
                    "response": "[TO_BE_GENERATED]",
                    "seed": get_seed(concept, lang, i),
                    "source": "simulation",
                })

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    template_path = OUTPUT_DIR / "simulation_template.json"
    with open(template_path, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    print(f"\n  Template saved: {template_path}")
    print(f"  Structure: {len(template)} responses")
    print(f"  Fill with '--generate' to replace '[TO_BE_GENERATED]' with LLM output")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph Structured Simulation Generator")
    parser.add_argument("--generate", action="store_true", help="Generate all 300 responses")
    parser.add_argument("--batch", type=int, choices=[1, 2, 3], help="Generate specific batch")
    parser.add_argument("--template", action="store_true", help="Generate empty template only")
    parser.add_argument("--status", action="store_true", help="Show generation status")
    parser.add_argument("--pipeline", action="store_true", help="Run pipeline on simulation data")
    parser.add_argument("--temperature", type=float, default=0.9, help="Generation temperature")
    args = parser.parse_args()

    if args.template:
        generate_template()
    elif args.status:
        print_status()
    elif args.batch:
        generate_batch_n(args.batch, temperature=args.temperature)
    elif args.generate or not any([args.status, args.pipeline, args.template, args.batch]):
        generate_all(temperature=args.temperature)
    elif args.pipeline:
        run_pipeline_on_simulation()


if __name__ == "__main__":
    main()
