"""
Computational Cognitive Baseline Generator
==========================================

Generates 300 simulated survey responses using LLM-style patterns.
NOT real human data — this is a computational baseline for comparison.

Usage:
    python experiments/generate_baseline.py

Output:
    data/baseline/computational_baseline.json (300 responses)
"""

import json
import os
import random
from datetime import datetime, timezone

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "baseline")

LANGUAGES = ["zh", "en", "de"]
TOPICS = ["success", "responsibility", "freedom", "home", "justice"]

# Concept pools per language per topic (simulating LLM extraction patterns)
CONCEPT_POOLS = {
    "success": {
        "zh": ["努力", "成就", "家庭", "责任", "学习", "目标", "幸福", "事业", "财富", "地位"],
        "en": ["achievement", "opportunity", "choice", "career", "wealth", "recognition", "freedom", "passion", "goal", "competition"],
        "de": ["Leistung", "Karriere", "Selbstständigkeit", "Kompetenz", "Bildung", "Erfolg", "Ziel", "Fähigkeit", "Qualifikation", "Unabhängigkeit"],
    },
    "responsibility": {
        "zh": ["责任", "社会", "义务", "家庭", "集体", "法律", "道德", "良心", "承诺", "担当"],
        "en": ["duty", "accountability", "freedom", "ethics", "obligation", "moral", "conscience", "commitment", "society", "choice"],
        "de": ["Pflicht", "Freiheit", "Ethik", "Gesellschaft", "Recht", "Moral", "Verpflichtung", "Gewissen", "Solidarität", "Bürgerpflicht"],
    },
    "freedom": {
        "zh": ["自由", "责任", "权利", "社会", "个人", "法律", "选择", "平等", "民主", "约束"],
        "en": ["rights", "choice", "liberty", "responsibility", "democracy", "individual", "equality", "autonomy", "power", "constraint"],
        "de": ["Selbstbestimmung", "Recht", "Verantwortung", "Demokratie", "Würde", "Gleichheit", "Autonomie", "Menschenrecht", "Gesetz", "Pflicht"],
    },
    "home": {
        "zh": ["家", "归属", "温暖", "家人", "记忆", "安全感", "故乡", "童年", "爱", "港湾"],
        "en": ["belonging", "family", "safety", "comfort", "memories", "warmth", "shelter", "roots", "love", "identity"],
        "de": ["Heimat", "Familie", "Zugehörigkeit", "Sicherheit", "Erinnerung", "Geborgenheit", "Wurzeln", "Identität", "Liebe", "Ruhe"],
    },
    "justice": {
        "zh": ["正义", "公平", "法律", "权利", "平等", "道德", "秩序", "惩罚", "自由", "社会"],
        "en": ["fairness", "equality", "rights", "law", "moral", "order", "punishment", "freedom", "society", "balance"],
        "de": ["Fairness", "Gleichheit", "Recht", "Gesetz", "Moral", "Ordnung", "Strafe", "Freiheit", "Gerechtigkeit", "Ausgleich"],
    },
}

RELATIONS = ["requires", "is_a", "part_of", "enables", "causes", "equivalent", "based_on", "through"]


def generate_response(lang, topic, respondent_id):
    """Generate a simulated survey response."""
    concepts = CONCEPT_POOLS[topic][lang]
    selected = random.sample(concepts, min(5, len(concepts)))

    # Generate open definition
    definitions = {
        "zh": {
            "success": "成功对我意味着{c1}和{c2}的结合。我认为{c3}也很重要。真正的成功不只是{c4}，而是{c5}。",
            "responsibility": "责任是{c1}的基础。我认为{c2}和{c3}是责任的核心。没有{c4}就没有{c5}。",
            "freedom": "自由的边界在于{c1}。自由需要{c2}来平衡。我认为{c3}是自由的前提。{c4}和{c5}定义了自由的范围。",
            "home": "家不只是{c1}，更是{c2}的来源。{c3}让我感到安全。家是{c4}和{c5}的结合。",
            "justice": "正义意味着{c1}和{c2}。我认为{c3}是正义的核心。没有{c4}就没有{c5}。",
        },
        "en": {
            "success": "Success means combining {c1} and {c2}. I believe {c3} is essential. True success is not just {c4} but also {c5}.",
            "responsibility": "Responsibility is the foundation of {c1}. I think {c2} and {c3} are core to responsibility. Without {c4}, there is no {c5}.",
            "freedom": "The boundary of freedom lies in {c1}. Freedom needs {c2} for balance. I believe {c3} is a prerequisite for freedom. {c4} and {c5} define its scope.",
            "home": "Home is not just {c1}, but the source of {c2}. {c3} makes me feel safe. Home is a combination of {c4} and {c5}.",
            "justice": "Justice means {c1} and {c2}. I believe {c3} is the core of justice. Without {c4}, there is no {c5}.",
        },
        "de": {
            "success": "Erfolg bedeutet für mich die Kombination aus {c1} und {c2}. Ich glaube, {c3} ist wesentlich. Wahre Erfolg ist nicht nur {c4}, sondern auch {c5}.",
            "responsibility": "Verantwortung ist die Grundlage von {c1}. Ich denke, {c2} und {c3} sind der Kern der Verantwortung. Ohne {c4} gibt es kein {c5}.",
            "freedom": "Die Grenze der Freiheit liegt bei {c1}. Freiheit braucht {c2} als Gegenpol. Ich glaube, {c3} ist eine Voraussetzung für Freiheit. {c4} und {c5} definieren ihren Rahmen.",
            "home": "Zuhause ist nicht nur {c1}, sondern die Quelle von {c2}. {c3} gibt mir Sicherheit. Zuhause ist eine Kombination aus {c4} und {c5}.",
            "justice": "Gerechtigkeit bedeutet {c1} und {c2}. Ich glaube, {c3} ist der Kern der Gerechtigkeit. Ohne {c4} gibt es kein {c5}.",
        },
    }

    template = definitions[lang][topic]
    definition = template.format(
        c1=selected[0], c2=selected[1], c3=selected[2],
        c4=selected[3], c5=selected[4]
    )

    return {
        "id": f"sim_{lang}_{topic}_{respondent_id:03d}",
        "type": "computational_baseline",
        "language": lang,
        "topic": topic,
        "respondent_id": respondent_id,
        "definition": definition,
        "concepts": selected,
        "relations": random.sample(RELATIONS, min(3, len(RELATIONS))),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_baseline(responses_per_combo=20):
    """Generate 300 simulated responses."""
    print("=" * 60)
    print("Computational Cognitive Baseline Generator")
    print("=" * 60)

    all_responses = []
    for topic in TOPICS:
        for lang in LANGUAGES:
            for i in range(responses_per_combo):
                resp = generate_response(lang, topic, i + 1)
                all_responses.append(resp)

    print(f"Generated {len(all_responses)} responses")
    print(f"  Topics: {len(TOPICS)}")
    print(f"  Languages: {len(LANGUAGES)}")
    print(f"  Per combo: {responses_per_combo}")
    print(f"  Total: {len(TOPICS)} x {len(LANGUAGES)} x {responses_per_combo} = {len(TOPICS) * len(LANGUAGES) * responses_per_combo}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "computational_baseline.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_responses, f, ensure_ascii=False, indent=2)

    print(f"\nSaved: {out_path}")

    # Summary by topic
    print("\nConcept distribution by topic:")
    for topic in TOPICS:
        topic_responses = [r for r in all_responses if r["topic"] == topic]
        all_concepts = []
        for r in topic_responses:
            all_concepts.extend(r["concepts"])
        from collections import Counter
        top5 = Counter(all_concepts).most_common(5)
        print(f"  {topic}: {', '.join(c for c,_ in top5)}")

    return all_responses


if __name__ == "__main__":
    generate_baseline()
