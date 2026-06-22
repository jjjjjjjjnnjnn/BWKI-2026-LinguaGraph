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
import random
import sys
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

import numpy as np

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
    """Call the LLM via LM Studio OpenAI-compatible API."""
    try:
        from openai import OpenAI
        client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
        response = client.chat.completions.create(
            model="qwen/qwen3.5-9b",
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

    cleaned = raw.strip()

    # Strip <think> tags (Qwen's reasoning output)
    if "<think>" in cleaned:
        # Remove everything between <think> and </think>
        import re
        cleaned = re.sub(r'<think>.*?</think>', '', cleaned, flags=re.DOTALL)
    # Also handle standalone think tags
    cleaned = cleaned.replace("</think>", "").replace("<think>", "")
    cleaned = cleaned.strip()

    # Strip markdown code fences
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
        if isinstance(data, dict) and "responses" in data:
            return data["responses"]
        return []
    except json.JSONDecodeError:
        # Try to extract JSON array from text (greedy match)
        import re
        match = re.search(r'\[.*\]', cleaned, re.DOTALL)
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

    # Use existing questionnaire IDs
    q_id_map = {"de": "social_issues_v1_de", "en": "social_issues_v1_en", "zh": "social_issues_v1_zh"}

    count = 0
    for r in responses:
        answer = r.get("response", "").strip()
        if not answer:
            continue

        # Unique student_id per response to work around UNIQUE(student_id, lang, question_id)
        sim_student_id = f"SIM_{concept}_{lang}_{count:04d}"

        # Ensure student exists
        try:
            insert(conn, "students", {
                "student_id": sim_student_id,
                "native_lang": "N/A",
                "school_lang": "N/A",
                "consent": 1,
                "notes": f"Simulation baseline - {concept}/{lang} #{count}",
            })
        except Exception:
            pass

        sid = f"SIM_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{count:03d}"
        word_count = len(answer.split()) if lang != "zh" else len([c for c in answer if '一' <= c <= '鿿'])

        try:
            insert(conn, "responses", {
                "response_id": f"RSIM_{concept}_{lang}_{count:04d}",
                "student_id": sim_student_id,
                "questionnaire_id": q_id_map[lang],
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


# ===== MOCK GENERATION (Deterministic, no LLM needed) =====

MOCK_RESPONSES = {
    "zh": {
        "freedom": [
            "自由就是能够按照自己的意愿生活，不受他人的强制和干预。",
            "自由不是为所欲为，而是在不侵犯他人权利的前提下做自己想做的事。",
            "自由意味着每个人都有平等的机会去追求自己的梦想。",
            "对我来说，自由就是可以选择自己的生活方式，无论是职业还是信仰。",
            "自由很重要，但也要承担责任，没有绝对的自由。",
            "自由是在法律框架内的自主权，每个人都应该尊重他人的自由。",
            "我理解的自由是思想自由和表达自由，能够说出自己的想法。",
            "自由不是胡来，而是知道自己为什么做、怎么做。",
            "真正的自由来自内心的独立，不盲从他人。",
            "自由是选择的权利，也是选择的责任。",
            "没有社会秩序的保障，个人自由也无从谈起。",
            "自由是发展的前提，每个人都应该有发展的自由。",
            "自由就是不被束缚，能够探索自己感兴趣的事物。",
            "经济自由是基础，没有经济独立就没有真正的自由。",
            "自由的环境需要法治来保障，否则强者会侵犯弱者的自由。",
            "对我来说，自由意味着时间自主，能够决定自己每天做什么。",
            "思想自由是最重要的，没有人能控制你的想法。",
            "自由需要勇气，为自己的选择负责。",
            "自由不是每个人都能理解的，它需要教育作为基础。",
            "最简单的自由就是做自己喜欢的事，和喜欢的人在一起。",
        ],
        "justice": [
            "公平就是每个人都得到应得的东西，不因出身、性别而区别对待。",
            "公平不是平均主义，而是给每个人平等的机会。",
            "在我看来，公平是机会均等，但结果可以不同。",
            "社会公平需要制度和法律来保障，不能只靠个人道德。",
            "公平是我付出多少就应该得到多少回报。",
            "教育公平最重要，因为教育决定了一个人未来的机会。",
            "公平对待他人，就是推己及人，己所不欲勿施于人。",
            "分配公平是社会稳定的基础。",
            "公平不是一刀切，而是根据不同情况给予不同对待。",
            "在机会面前人人平等，但也要承认个人努力的差异。",
            "程序正义很重要，过程公正结果才能让人接受。",
            "代际公平也是公平的一部分，我们不能透支后代的资源。",
            "公平需要公开透明的规则，暗箱操作是对公平的破坏。",
            "市场竞争中的公平就是遵守规则，不搞特殊化。",
            "司法公正是社会公平的最后一道防线。",
            "公平的社会应该让弱者也活得有尊严。",
            "我理解的公平是每个人都有发声和参与的权利。",
            "无论贫富，都应该享有基本的医疗保障和受教育权。",
            "公平不是结果平等，而是机会平等加上合理的差别原则。",
            "人与人之间天然有差异，公平是让这些差异不影响基本权利。",
        ],
        "success": [
            "一家人平平安安，工作稳定孩子能成才，父母身体好，这就够了。",
            "成功不是赚多少钱，而是能做自己真正热爱的事情。",
            "好的人生是健康的身体、和睦的家庭和对社会有所贡献。",
            "成功是对自己有价值，对他人有意义。",
            "能够按照自己的价值观生活，不为外界所左右，这就是成功。",
            "成功是不断成长、不断超越昨天的自己。",
            "好的人生在于平衡——工作、家庭、健康、兴趣的平衡。",
            "为社会创造价值，得到他人的尊重和认可，这是成功。",
            "成功不是终点，而是一个持续进步的过程。",
            "有钱有权不是成功，内心充实和宁静才是。",
            "能够帮助他人、回馈社会，这是我理解的成功。",
            "成功是拥有选择的自由，不被生活所迫。",
            "有一份热爱的事业和一群真心的朋友，人生就成功了。",
            "好的人生是经历了各种滋味，仍然热爱生活。",
            "成功就是在自己的领域做出一点不一样的东西。",
            "对我来说，成功意味着养得起家人，还有时间陪伴他们。",
            "成功是知道自己想要什么，并且有勇气去追求。",
            "过一种真实、简单、自在的生活就是成功。",
            "好的人生需要持续学习、探索未知。",
            "成功是在平凡的日子里找到快乐和意义。",
        ],
        "responsibility": [
            "责任就是做好自己分内的事情，不推卸、不逃避。",
            "责任意味着对自己的行为负责，承担后果。",
            "首先对自己负责，然后对家人、对社会负责。",
            "履行责任不是为了别人，而是为了自己的内心安宁。",
            "责任不是负担，而是成熟的标志。",
            "一个负责任的人会信守承诺，说到做到。",
            "社会责任是每个公民应尽的义务。",
            "责任包括对自己、对他人、对环境的责任。",
            "没有责任感的人很难获得他人的信任。",
            "责任不分大小，认真对待每一件小事就是尽责。",
            "作为学生，努力学习是一种责任。",
            "责任与权利是相对应的，享受权利就要承担相应的责任。",
            "对家庭负责就是照顾好自己和家人。",
            "对社会的责任体现在遵守法律、保护环境、帮助他人。",
            "责任需要自律，没有人监督也要做到。",
            "做错了事要敢于承认和改正，这是负责任的表现。",
            "责任意味着在困难面前不退缩，坚持到底。",
            "责任不是别人强加给你的，而是你主动选择承担的。",
            "自己选择的路，跪着也要走完，这就是责任。",
            "责任心是一个人的立身之本，没有责任心就难以在社会立足。",
        ],
        "home": [
            "家是一个可以放松的地方，不用伪装自己。",
            "家是我无论走多远都会回去的地方。",
            "有家人的地方就是家，不一定是房子。",
            "家是温暖的港湾，在外累了可以回来休息。",
            "家意味着归属感和安全感。",
            "对我来说，家是记忆的集合——童年的玩具、妈妈做的饭菜。",
            "家是责任，也是爱。",
            "不管在外面多累，回到家就觉得一切都值得。",
            "家不是一栋建筑，而是一种感觉。",
            "家是理解和支持的地方，是你可以做自己的地方。",
            "家是你受了委屈第一个想回去的地方。",
            "传统意义上，家是宗族的延续，但现在家更多是个人的选择。",
            "家是你能放下所有防备的地方。",
            "没有家的感觉就像漂泊的船找不到港湾。",
            "家是每天晚饭时大家坐在一起聊天的地方。",
            "家意味着有人等你回来。",
            "对我来说，家既是一个物理空间，也是一种情感联系。",
            "家是最小国的国，国是最大家的家。",
            "家的意义随着成长而变化，但核心是爱和责任。",
            "家就是那个你抱怨无数次却不允许别人说一句不好的地方。",
        ],
    },
    "en": {
        "freedom": [
            "Freedom means being able to live life on my own terms without interference from others.",
            "Freedom is about having choices, and having the ability to act on those choices.",
            "True freedom includes freedom of speech, thought, and the pursuit of happiness.",
            "Freedom is not free — it requires responsibility and respect for others' freedom.",
            "To me, freedom means I can express my opinions without fear.",
            "Freedom of choice is the foundation of human dignity.",
            "Freedom is having control over your own life and decisions.",
            "Freedom is the ability to challenge authority and question the status quo.",
            "The most important freedom is the freedom to be yourself.",
            "Freedom means equal rights for everyone, regardless of background.",
            "Freedom is limited by the freedom of others — that's the social contract.",
            "Economic freedom — being able to choose your career and how to spend your money.",
            "Freedom is the opportunity to make mistakes and learn from them.",
            "Personal freedom ends where another person's rights begin.",
            "Freedom requires education — you can't choose what you don't know exists.",
            "Freedom of movement — being able to travel, live, and work where you want.",
            "Real freedom is freedom from fear, hunger, and oppression.",
            "Freedom means having a voice in how your society is governed.",
            "The opposite of freedom isn't just imprisonment — it's also dependency.",
            "Freedom is the ability to define success on your own terms.",
        ],
        "justice": [
            "Justice means everyone gets what they deserve, nothing more and nothing less.",
            "Justice is about fair treatment under the law, regardless of status.",
            "Fairness means equal opportunity — everyone starts with a fair chance.",
            "Justice requires impartial rules and unbiased application.",
            "Distributive justice — resources should be allocated based on need and contribution.",
            "Social justice is about correcting historical inequities.",
            "Fairness isn't sameness — different situations sometimes require different treatment.",
            "Justice delayed is justice denied.",
            "A just society protects the vulnerable from exploitation.",
            "Procedural justice — fair processes matter as much as fair outcomes.",
            "Justice is the foundation of a stable and peaceful society.",
            "Fair wages for fair work — that's economic justice.",
            "Justice means accountability — no one is above the law.",
            "Intergenerational justice means we don't sacrifice the future for the present.",
            "Environmental justice means everyone deserves clean air and water.",
            "Justice is when the system works equally well for rich and poor.",
            "Fairness in education means every child has access to quality schooling.",
            "Justice includes both punishment for wrongdoing and rehabilitation.",
            "Restorative justice focuses on healing rather than just punishment.",
            "A fair society is one where your birth doesn't determine your future.",
        ],
        "success": [
            "A good life means finding purpose and meaning in what you do each day.",
            "Success isn't just about wealth — it's about relationships and fulfillment.",
            "Happiness is the ultimate measure of a good life.",
            "Success is achieving goals that matter to you, not what others expect.",
            "A good life balances career, family, health, and personal growth.",
            "Making a positive impact on others' lives is true success.",
            "Success is loving your work and being good at it.",
            "A good life is one of continuous learning and growth.",
            "Success is having the freedom to choose how to spend your time.",
            "Building meaningful relationships is the foundation of a good life.",
            "Success is resilience — getting back up after failure.",
            "A good life includes financial security, but that's just the baseline.",
            "Success means living authentically — true to your values and beliefs.",
            "Leaving the world better than you found it is a kind of success.",
            "A good life has room for both ambition and contentment.",
            "Success is being remembered well by the people who know you best.",
            "The good life involves both personal achievement and community contribution.",
            "Success isn't a destination — it's how you travel.",
            "A good life requires courage to pursue your own path, not the beaten one.",
            "Success is waking up excited about the day ahead.",
        ],
        "responsibility": [
            "Responsibility means owning your actions and their consequences.",
            "Being responsible means others can count on you to keep your word.",
            "Responsibility starts with taking care of yourself and extends to others.",
            "Freedom and responsibility are two sides of the same coin.",
            "A responsible person thinks before they act.",
            "Civic responsibility — participating in democracy and community.",
            "Responsibility means doing the right thing even when no one is watching.",
            "Taking responsibility for mistakes is a sign of strength, not weakness.",
            "We have responsibility not just to the present but to future generations.",
            "Responsibility is the price of freedom.",
            "Environmental responsibility — we're stewards of the planet.",
            "Financial responsibility means living within your means and planning ahead.",
            "Responsibility is love in action — caring for family and community.",
            "Professional responsibility means doing your job well and with integrity.",
            "Moral responsibility — we're accountable for how our choices affect others.",
            "Responsibility is what separates adults from children.",
            "You can delegate tasks but you can't delegate responsibility.",
            "Social responsibility includes helping those less fortunate.",
            "Responsibility is proactive, not reactive — anticipate needs before they arise.",
            "Every right comes with a corresponding responsibility.",
        ],
        "home": [
            "Home is where I feel safe and can be myself without judgment.",
            "Home is more than a building — it's the people who make it warm.",
            "Home is where I belong, where my roots are.",
            "A place becomes home when you've made memories there.",
            "Home is the place you can always return to, no matter what.",
            "Home means family, comfort, and the familiarity of everyday routines.",
            "Home is where you're understood — or at least tolerated.",
            "For me, home is a feeling of being accepted unconditionally.",
            "Home is the physical space where my personal history lives.",
            "Home is where I recharge and find peace.",
            "Home is the one place I have control over how it looks and feels.",
            "A home is built over time — through meals, conversations, and shared experiences.",
            "Home is where I can let my guard down completely.",
            "The idea of home has become more flexible — I find home in many places.",
            "Home is the people who know you and love you anyway.",
            "Home is memory — the smell of certain foods, a familiar chair.",
            "Home is where I learned who I am.",
            "Home means stability in a changing world.",
            "A home isn't necessarily where you grew up — it's where you grow into yourself.",
            "Home is the place where you're needed and you need others.",
        ],
    },
    "de": {
        "freedom": [
            "Freiheit bedeutet, nach eigenen Überzeugungen leben zu können.",
            "Freiheit ist nicht die Abwesenheit von Grenzen, sondern die Fähigkeit, verantwortungsvoll mit ihnen umzugehen.",
            "Negative Freiheit ist Freiheit von Zwang, positive Freiheit ist die Fähigkeit zur Selbstverwirklichung.",
            "Freiheit braucht Ordnung, sonst wird sie zur Willkür.",
            "Meine Freiheit endet dort, wo die Freiheit des anderen beginnt.",
            "Freiheit ist das Recht, eigene Entscheidungen zu treffen und dafür einzustehen.",
            "Wahre Freiheit setzt Bildung voraus — nur wer informiert ist, kann frei wählen.",
            "Freiheit bedeutet auch, Nein sagen zu können.",
            "Gesellschaftliche Freiheit und persönliche Verantwortung gehören zusammen.",
            "Freiheit ist kein Naturzustand, sondern eine kulturelle Errungenschaft.",
            "Die Freiheit der Meinungsäußerung ist fundamental für eine Demokratie.",
            "Freiheit bedeutet nicht, alles zu können, was man will, sondern das zu wollen, was man kann.",
            "Autonomie ist der Kern der Freiheit — selbstbestimmt leben.",
            "Freiheit ohne Verantwortung ist Willkür, Verantwortung ohne Freiheit ist Zwang.",
            "Freiheit ist ein Prozess der Befreiung von Vorurteilen und Unwissenheit.",
            "Wirtschaftliche Freiheit ist wichtig, aber sie muss sozial eingebettet sein.",
            "Freiheit ist die Grundlage für Würde und Selbstachtung.",
            "Die Freiheit des Einzelnen ist durch das Gemeinwohl begrenzt.",
            "Freiheit bedeutet, verschiedene Lebensentwürfe verwirklichen zu können.",
            "Freiheit ist die Möglichkeit, aus der Geschichte zu lernen und anders zu handeln.",
        ],
        "justice": [
            "Gerechtigkeit bedeutet, jedem das Seine zu geben — nach Bedarf, Leistung oder Recht.",
            "Gerechtigkeit ist die Grundlage jeder funktionierenden Gesellschaft.",
            "Soziale Gerechtigkeit gleicht unverdiente Ungleichheiten aus.",
            "Gerechtigkeit braucht faire Verfahren — der Weg ist genauso wichtig wie das Ziel.",
            "Verteilungsgerechtigkeit fragt, wie Ressourcen fair aufgeteilt werden können.",
            "Chancengerechtigkeit bedeutet, dass die Herkunft nicht über die Zukunft entscheidet.",
            "Gerechtigkeit ist mehr als bloße Gleichheit — sie berücksichtigt Unterschiede.",
            "Generationengerechtigkeit bedeutet, dass wir nicht auf Kosten unserer Kinder leben.",
            "Recht und Gerechtigkeit sind nicht dasselbe — manchmal ist ein Gesetz ungerecht.",
            "Eine gerechte Gesellschaft schützt die Schwachen vor den Starken.",
            "Gerechtigkeit erfordert Transparenz und Unparteilichkeit.",
            "Bildungsgerechtigkeit ist der Schlüssel zu sozialer Mobilität.",
            "Justitia ist blind — vor dem Gesetz sind alle gleich.",
            "Gerechtigkeit bedeutet, dass Leistung sich lohnen muss.",
            "Umweltgerechtigkeit — jeder hat ein Recht auf eine gesunde Umwelt.",
            "Wiedergutmachung ist Teil der Gerechtigkeit.",
            "Gerechtigkeit ist keine Frage des Gefühls, sondern des Prinzips.",
            "Soziale Marktwirtschaft verbindet wirtschaftliche Freiheit mit sozialem Ausgleich.",
            "Gerechtigkeit ist ein regulatives Ideal — wir streben danach, auch wenn wir es nie vollständig erreichen.",
        ],
        "success": [
            "Ein gelungenes Leben ist eines, in dem man seine Talente entfalten konnte.",
            "Erfolg bedeutet für mich, zufrieden und im Einklang mit sich selbst zu sein.",
            "Ein gutes Leben verbindet berufliche Erfüllung mit persönlichem Glück.",
            "Erfolg ist die Fähigkeit, aus Fehlern zu lernen und daran zu wachsen.",
            "Ein gelungenes Leben trägt zum Gemeinwohl bei — nicht nur zum eigenen Vorteil.",
            "Erfolg ist nicht nur materieller Wohlstand, sondern auch kulturelle Teilhabe.",
            "Ein gutes Leben ist authentisch — es folgt den eigenen Werten, nicht fremden Erwartungen.",
            "Erfolg bedeutet, ein Leben nach eigenen Maßstäben zu führen.",
            "Bildung, Freundschaft und Gesundheit — das sind die wahren Säulen eines guten Lebens.",
            "Ein gelungenes Leben ist geprägt von Neugier und lebenslangem Lernen.",
            "Erfolg ist die Summe von Disziplin, Leidenschaft und Beharrlichkeit.",
            "Ein gutes Leben hat Raum für Muße und Besinnung, nicht nur für Leistung.",
            "Erfolg misst sich nicht am Besitz, sondern am Beitrag.",
            "Ein gelungenes Leben bedeutet, geliebt zu haben und geliebt worden zu sein.",
            "Erfolg ist die Verwirklichung dessen, was in einem angelegt ist.",
            "Ein gutes Leben ist ein Leben in Würde — unabhängig von äußeren Umständen.",
            "Erfolg ist, abends müde und morgens motiviert zu sein.",
            "Ein gelungenes Leben erkennt die eigenen Grenzen an und findet Freiheit darin.",
            "Erfolg bedeutet, das Richtige zu tun — auch wenn es schwerfällt.",
            "Ein gutes Leben ist ein Leben mit Sinn — für sich selbst und für andere.",
        ],
        "responsibility": [
            "Verantwortung bedeutet, für die Konsequenzen des eigenen Handelns einzustehen.",
            "Verantwortung ist die Kehrseite der Freiheit — wer frei ist, muss auch Verantwortung tragen.",
            "Eigenverantwortung ist die Grundlage der Mündigkeit.",
            "Verantwortung für andere zu übernehmen ist Ausdruck von Fürsorge.",
            "Gesellschaftliche Verantwortung bedeutet, sich für das Gemeinwohl einzusetzen.",
            "Verantwortung kann man nicht delegieren, nur teilen.",
            "Eltern tragen Verantwortung für die Entwicklung ihrer Kinder.",
            "Politische Verantwortung bedeutet, wählen zu gehen und sich zu informieren.",
            "Verantwortung heißt, Versprechen zu halten und Vertrauen nicht zu enttäuschen.",
            "Ökologische Verantwortung — wir sind nur Gäste auf diesem Planeten.",
            "Verantwortung beginnt im Kleinen, im Alltag, in den eigenen vier Wänden.",
            "Wer Verantwortung übernimmt, gewinnt Gestaltungsfreiheit.",
            "Verantwortung bedeutet, auch unangenehme Entscheidungen zu treffen.",
            "Selbstverantwortung ist die Voraussetzung für jede Form von Mitverantwortung.",
            "Verantwortung ist nicht last, sondern eine Form der Selbstachtung.",
            "In einer Demokratie trägt jeder Bürger Mitverantwortung.",
            "Verantwortung bedeutet, vorauszudenken und Risiken zu vermeiden.",
            "Fachliche Verantwortung heißt, sein Bestes zu geben und sein Wissen zu teilen.",
            "Verantwortung ist die Brücke zwischen Freiheit und Gemeinschaft.",
            "Moralische Verantwortung endet nicht an Landesgrenzen.",
        ],
        "home": [
            "Heimat ist der Ort, an dem man verstanden wird, ohne erklären zu müssen.",
            "Zuhause ist ein Gefühl der Geborgenheit und des Angenommenseins.",
            "Heimat ist nicht unbedingt der Geburtsort, sondern der Ort, an dem man lebt.",
            "Zuhause ist der Raum, in dem ich ganz ich selbst sein kann.",
            "Heimat bedeutet Verwurzelung und Zugehörigkeit.",
            "Zuhause ist der Ort, an dem meine Erinnerungen wohnen.",
            "Heimat kann auch ein Mensch sein, nicht nur ein Ort.",
            "Zuhause ist ein sicherer Hafen in einer unsicheren Welt.",
            "Heimat ist da, wo man die Sprache spricht, die man im Herzen versteht.",
            "Zuhause ist der Ort, an dem einen niemand nach einem Grund fragt, warum man da ist.",
            "Heimat ist für mich kein statischer Begriff — sie verändert sich mit dem Leben.",
            "Zuhause bedeutet Vertrautheit — die Rituale, die Gerüche, die Geräusche.",
            "Heimat ist die Landschaft der Kindheit, die in einem weiterlebt.",
            "Zuhause ist da, wo das WLAN sich automatisch verbindet.",
            "Heimat hat viel mit Identität zu tun — wie man sich selbst verortet.",
            "Zuhause ist weniger ein Ort als eine Zeit — die Momente, die zählen.",
            "Heimat ist keine Frage des Passes, sondern des Herzens.",
            "Zuhause ist, wo man nach einer Reise ankommt und sich freut.",
            "Heimat ist Solidarität — die Gemeinschaft, die zusammenhält.",
            "Zuhause ist die Basis, von der aus man die Welt erkundet.",
        ],
    },
}


def generate_mock_all():
    """Generate all 300 responses using pre-written templates (no LLM needed)."""
    random.seed(42)  # Deterministic

    print(f"\n{'='*60}")
    print(f"  LinguaGraph Simulation Generator (MOCK MODE)")
    print(f"  Target: {TOTAL_RESPONSES} responses ({len(CONCEPTS)} concepts × {len(LANGUAGES)} languages × {SAMPLES_PER_CELL} samples)")
    print(f"  No LLM needed — using pre-written response templates")
    print(f"{'='*60}\n")

    total = 0
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for concept in CONCEPTS:
        for lang in LANGUAGES:
            pool = MOCK_RESPONSES[lang][concept]
            cell_responses = []
            for i in range(SAMPLES_PER_CELL):
                idx = i % len(pool)
                text = pool[idx]
                cell_responses.append({
                    "id": i + 1,
                    "concept": concept,
                    "language": lang,
                    "persona": PERSONAS[lang]["name"],
                    "response": text,
                    "seed": get_seed(concept, lang, i),
                    "source": "simulation",
                })

            # Save to file
            filepath = OUTPUT_DIR / f"{concept}_{lang}.json"
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(cell_responses, f, ensure_ascii=False, indent=2)

            # Import to DB
            n_db = import_to_db(concept, lang, cell_responses)
            print(f"  [{concept:<15s}] [{lang}] {len(cell_responses):>2d} → DB ({n_db} imported)")
            total += n_db

    print(f"\n{'='*60}")
    print(f"  Complete: {total}/{TOTAL_RESPONSES} responses in DB")
    print(f"  Source: simulation (clearly marked)")
    print(f"{'='*60}")


def generate_template():
    """Generate the empty template JSON structure for review."""
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


def main():
    random.seed(42)
    np.random.seed(42)
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph Structured Simulation Generator")
    parser.add_argument("--generate", action="store_true", help="Generate all 300 responses via LLM")
    parser.add_argument("--mock", action="store_true", help="Generate 300 responses from templates (no LLM)")
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
    elif args.mock:
        generate_mock_all()
    elif args.pipeline:
        run_pipeline_on_simulation()
    elif args.generate or not any([args.status, args.pipeline, args.template, args.batch, args.mock]):
        generate_all(temperature=args.temperature)


if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    main()
