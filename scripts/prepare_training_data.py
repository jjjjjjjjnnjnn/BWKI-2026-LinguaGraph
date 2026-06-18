#!/usr/bin/env python3
"""
Prepare Training Data for LinguaGraph Local Model

Converts gold labels, Wikipedia corpus, and education texts
into Alpaca-format training data for LoRA fine-tuning.

Usage:
    # Convert gold labels to training format
    python prepare_training_data.py \
        --gold data/gold/gold_dataset.json \
        --output data/training/train.json

    # Generate synthetic training data
    python prepare_training_data.py \
        --generate-synthetic 500 \
        --output data/training/synthetic.json

    # Pipeline: combine and split
    python prepare_training_data.py \
        --combine data/training/*.json \
        --output data/training/combined.json \
        --split train,val,test
"""

import json
import random
import sys
from pathlib import Path
from typing import Dict, List, Optional


# === Constants ===

TOPICS = {
    "zh": {
        "freedom": "从这段关于自由的回答中提取概念和关系。",
        "justice": "从这段关于公平的回答中提取概念和关系。",
        "responsibility": "从这段关于责任的回答中提取概念和关系。",
        "success": "从这段关于成功的回答中提取概念和关系。",
        "family": "从这段关于家庭的回答中提取概念和关系。",
    },
    "de": {
        "freedom": "Extrahiere Konzepte und Beziehungen aus dieser Antwort zum Thema Freiheit.",
        "justice": "Extrahiere Konzepte und Beziehungen aus dieser Antwort zum Thema Gerechtigkeit.",
        "responsibility": "Extrahiere Konzepte und Beziehungen aus dieser Antwort zum Thema Verantwortung.",
        "success": "Extrahiere Konzepte und Beziehungen aus dieser Antwort zum Thema Erfolg.",
        "family": "Extrahiere Konzepte und Beziehungen aus dieser Antwort zum Thema Familie.",
    },
    "en": {
        "freedom": "Extract concepts and relations from this answer about freedom.",
        "justice": "Extract concepts and relations from this answer about justice.",
        "responsibility": "Extract concepts and relations from this answer about responsibility.",
        "success": "Extract concepts and relations from this answer about success.",
        "family": "Extract concepts and relations from this answer about family.",
    },
}

# === Conversion Functions ===


def gold_to_alpaca(gold_entry: dict) -> Optional[dict]:
    """Convert a gold label entry to Alpaca-format training example."""
    language = gold_entry.get("language", "zh")
    topic = _infer_topic(gold_entry.get("question", ""), language)

    if language not in TOPICS or topic not in TOPICS[language]:
        return None

    instruction = TOPICS[language][topic]
    input_text = gold_entry.get("text", "")
    labels = gold_entry.get("human_labels", {})

    output = json.dumps({
        "concepts": labels.get("concepts", []),
        "relations": [
            {"source": r.get("from", ""), "target": r.get("to", ""), "type": r.get("type", "relates_to")}
            for r in labels.get("relations", [])
        ],
    }, ensure_ascii=False)

    return {
        "instruction": instruction,
        "input": input_text,
        "output": output,
        "language": language,
        "topic": topic,
        "source": "gold",
        "difficulty": gold_entry.get("difficulty", "medium"),
    }


def _infer_topic(question: str, language: str) -> str:
    """Infer topic from question text."""
    q = question.lower()
    keywords = {
        "freedom": ["freiheit", "freedom", "自由", "liberty"],
        "justice": ["gerechtigkeit", "justice", "公平", "公正"],
        "responsibility": ["verantwortung", "responsibility", "责任", "义务"],
        "success": ["erfolg", "success", "成功", "成就"],
        "family": ["familie", "family", "家庭", "家"],
    }
    for topic, kws in keywords.items():
        for kw in kws:
            if kw.lower() in q:
                return topic
    return "freedom"  # default


def generate_synthetic(
    count: int = 500,
    languages: List[str] = None,
    topics: List[str] = None,
    seed: int = 42,
) -> List[dict]:
    """
    Generate synthetic training data using template-based augmentation.
    This creates structurally varied examples that teach the model
    the expected output format.
    """
    if languages is None:
        languages = ["zh", "de", "en"]
    if topics is None:
        topics = ["freedom", "justice", "responsibility", "success", "family"]

    rng = random.Random(seed)
    samples = []

    concept_pools = {
        "zh": {
            "freedom": ["自由", "权利", "选择", "个体", "社会", "责任", "平等", "法律"],
            "justice": ["公平", "正义", "平等", "法律", "权利", "社会", "秩序", "道德"],
            "responsibility": ["责任", "义务", "社会", "个体", "家庭", "工作", "道德", "承诺"],
            "success": ["成功", "努力", "目标", "成就", "坚持", "学习", "进步", "机会"],
            "family": ["家庭", "爱", "父母", "孩子", "温暖", "支持", "教育", "传统"],
        },
        "de": {
            "freedom": ["Freiheit", "Recht", "Wahl", "Individuum", "Gesellschaft", "Verantwortung", "Gleichheit", "Gesetz"],
            "justice": ["Gerechtigkeit", "Recht", "Gleichheit", "Gesetz", "Moral", "Ordnung", "Würde", "Fairness"],
            "responsibility": ["Verantwortung", "Pflicht", "Gesellschaft", "Arbeit", "Familie", "Gewissen", "Sorgfalt"],
            "success": ["Erfolg", "Leistung", "Ziel", "Arbeit", "Ausdauer", "Bildung", "Fortschritt", "Chance"],
            "family": ["Familie", "Liebe", "Eltern", "Kind", "Zuhause", "Geborgenheit", "Erziehung", "Tradition"],
        },
        "en": {
            "freedom": ["freedom", "rights", "choice", "individual", "society", "responsibility", "equality", "law"],
            "justice": ["justice", "fairness", "equality", "law", "rights", "society", "order", "morality"],
            "responsibility": ["responsibility", "duty", "society", "individual", "family", "work", "ethics", "commitment"],
            "success": ["success", "effort", "goal", "achievement", "persistence", "learning", "progress", "opportunity"],
            "family": ["family", "love", "parents", "children", "home", "support", "education", "tradition"],
        },
    }

    relation_templates = [
        ("represents", "{0} represents {1}"),
        ("opposite_of", "{0} is opposite to {1}"),
        ("part_of", "{0} is part of {1}"),
        ("cause_effect", "{0} leads to {1}"),
        ("implies", "{0} implies {1}"),
        ("relates_to", "{0} relates to {1}"),
        ("requires", "{0} requires {1}"),
    ]

    for i in range(count):
        lang = rng.choice(languages)
        topic = rng.choice(topics)
        concepts = concept_pools[lang][topic]

        # Pick 2-5 concepts
        n_concepts = rng.randint(2, 5)
        selected = rng.sample(concepts, min(n_concepts, len(concepts)))

        # Pick 1-3 relations
        n_relations = rng.randint(0, min(3, len(selected) - 1))
        relations = []
        used_pairs = set()
        for _ in range(n_relations):
            src = rng.choice(selected)
            tgt = rng.choice([c for c in selected if c != src])
            pair = (src, tgt)
            if pair not in used_pairs:
                used_pairs.add(pair)
                rel_type, _ = rng.choice(relation_templates)
                relations.append({"source": src, "target": tgt, "type": rel_type})

        instruction = TOPICS[lang][topic]

        # Generate synthetic answer text
        if relations:
            sample_rel = rng.choice(relations)
            sample_text = rng.choice([
                f"{sample_rel['source']} {sample_rel['type'].replace('_', ' ')} {sample_rel['target']}.",
                f"I think {sample_rel['source']} is related to {sample_rel['target']}.",
                f"{sample_rel['source']} and {sample_rel['target']} are connected.",
            ])
        else:
            sample_text = f"{selected[0]} is an important concept in {topic}."

        output = json.dumps({"concepts": selected, "relations": relations}, ensure_ascii=False)

        samples.append({
            "instruction": instruction,
            "input": sample_text,
            "output": output,
            "language": lang,
            "topic": topic,
            "source": "synthetic",
            "difficulty": "medium",
        })

    return samples


def combine_and_split(
    input_files: List[str],
    output_prefix: str,
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    seed: int = 42,
):
    """Combine multiple JSON files and split into train/val/test."""
    all_data = []
    for f in input_files:
        with open(f, encoding="utf-8") as fh:
            all_data.extend(json.load(fh))

    rng = random.Random(seed)
    rng.shuffle(all_data)

    n = len(all_data)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)

    splits = {
        "train": all_data[:n_train],
        "val": all_data[n_train:n_train + n_val],
        "test": all_data[n_train + n_val:],
    }

    for name, data in splits.items():
        path = f"{output_prefix}_{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  {name}: {len(data)} examples → {path}")

    print(f"\n  Total: {n} examples")
    return splits


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Prepare LinguaGraph training data")
    parser.add_argument("--gold", type=str, help="Gold labels JSON file")
    parser.add_argument("--generate-synthetic", type=int, default=0, help="Generate N synthetic examples")
    parser.add_argument("--combine", type=str, nargs="+", help="Combine multiple JSON files")
    parser.add_argument("--output", type=str, required=True, help="Output path")
    parser.add_argument("--split", type=str, default=None, help="Comma-separated: train,val,test")
    parser.add_argument("--languages", type=str, default="zh,de,en", help="Comma-separated languages")
    parser.add_argument("--topics", type=str, default="freedom,justice,responsibility,success,family")
    args = parser.parse_args()

    all_data = []

    # Convert gold labels
    if args.gold:
        print(f"Converting gold labels: {args.gold}")
        with open(args.gold, encoding="utf-8") as f:
            gold_data = json.load(f)
        for entry in gold_data:
            example = gold_to_alpaca(entry)
            if example:
                all_data.append(example)
        print(f"  → {len(all_data)} gold examples converted")

    # Generate synthetic data
    if args.generate_synthetic > 0:
        languages = args.languages.split(",")
        topics = args.topics.split(",")
        print(f"Generating {args.generate_synthetic} synthetic examples...")
        synthetic = generate_synthetic(
            count=args.generate_synthetic,
            languages=languages,
            topics=topics,
        )
        all_data.extend(synthetic)
        print(f"  → {len(synthetic)} synthetic examples generated")

    # Combine files
    if args.combine:
        for f in args.combine:
            path = Path(f)
            if path.exists():
                print(f"Combining: {f}")
                with open(path, encoding="utf-8") as fh:
                    all_data.extend(json.load(fh))

    if not all_data:
        print("[ERROR] No data generated. Provide --gold, --generate-synthetic, or --combine")
        sys.exit(1)

    # Split or save
    if args.split:
        parts = args.split.split(",")
        splits = combine_and_split(
            input_files=[],
            output_prefix=args.output.replace(".json", ""),
            train_ratio=0.8 if "train" in parts else 0.0,
            val_ratio=0.1 if "val" in parts else 0.0,
        )

        # Actually need to split the data we have
        rng = random.Random(42)
        rng.shuffle(all_data)
        n = len(all_data)
        n_train = int(n * 0.8)
        n_val = int(n * 0.1)

        output_base = args.output.replace(".json", "")
        splits_data = {
            "train": all_data[:n_train],
            "val": all_data[n_train:n_train + n_val],
            "test": all_data[n_train + n_val:],
        }
        for name in parts:
            path = f"{output_base}_{name}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(splits_data[name], f, ensure_ascii=False, indent=2)
            print(f"  {name}: {len(splits_data[name])} examples → {path}")
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"\n  Saved: {len(all_data)} examples → {args.output}")

    # Print statistics
    from collections import Counter
    lang_counts = Counter(d.get("language", "unknown") for d in all_data)
    source_counts = Counter(d.get("source", "unknown") for d in all_data)
    print(f"\n  Language distribution: {dict(lang_counts)}")
    print(f"  Source distribution: {dict(source_counts)}")


if __name__ == "__main__":
    main()
