"""
LinguaGraph — BWKI Corpus Reorganizer
======================================

Reorganizes existing BWKI scraped data into the social media corpus
directory with proper metadata and topic classification.

Reads from: BWKI/01_cognitive_science, 06_cross_lingual_kg, 07_cultural_psychology
Writes to: BWKI/13_social_media_corpus/

Usage:
    python experiments/reorganize_corpus.py
"""

import json
import os
import re
import hashlib
from datetime import datetime, timezone

BWKI_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "本地知识库", "知识库内容", "BWKI"
)
OUTPUT_DIR = os.path.join(BWKI_DIR, "13_social_media_corpus")

SOURCE_DIRS = [
    "01_cognitive_science",
    "06_cross_lingual_kg",
    "07_cultural_psychology",
    "02_linguistics",
    "03_education",
]

TOPIC_KEYWORDS = {
    "freedom": ["freedom", "liberty", "free", "autonomy", "self-determination",
                "自由", "Freiheit", "recht", "autonomie"],
    "language_thought": ["language", "thought", "cognition", "thinking", "whorf",
                         "sapir", "linguistic relativity", "语言", "思维", "认知",
                         "Sprache", "Gedanke", "Kognition"],
    "bilingualism": ["bilingual", "multilingual", "bilingualism", "multilingualism",
                     "双语", "多语", "bilingual", "mehrsprachig"],
    "knowledge": ["knowledge", "power", "education", "learning", "cognition",
                  "知识", "权力", "教育", "Wissen", "Macht", "Bildung"],
    "emotion_culture": ["emotion", "feeling", "culture", "cultural", "emotion expression",
                        "情感", "情绪", "文化", "Emotion", "Kultur"],
    "identity": ["identity", "self", "self-construal", "personal identity",
                 "身份", "自我", "Identität", "Selbst"],
    "moral_reasoning": ["moral", "ethics", "ethical", "reasoning", "judgment",
                        "道德", "伦理", "Moral", "Ethik"],
}


def detect_language(text):
    sample = text[:500]
    zh_chars = len(re.findall(r"[\u4e00-\u9fff]", sample))
    de_chars = len(re.findall(r"[äöüßÄÖÜ]", sample))
    total_alpha = len(re.findall(r"\w", sample))
    if total_alpha == 0:
        return "en"
    if zh_chars / max(total_alpha, 1) > 0.3:
        return "zh"
    if de_chars > 2:
        return "de"
    return "en"


def classify_topic(text):
    text_lower = text.lower()
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        scores[topic] = score
    if max(scores.values()) == 0:
        return None
    return max(scores, key=scores.get)


def read_kb_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2].strip()
    return "", content.strip()


def create_corpus_entry(source_dir, filename, frontmatter, content, topic, lang):
    now = datetime.now(timezone.utc).isoformat()
    content_hash = hashlib.md5(content[:500].encode()).hexdigest()[:12]

    entry = f"""---
type: social_media
topic: {topic}
language: {lang}
platform: academic_paper
source_domain: {source_dir}
source_file: {filename}
crawled_at: "{now}"
content_hash: "{content_hash}"
quality: B
status: unverified
tags:
  - {topic}
  - {lang}
  - academic
  - crawled
---

# {filename.replace('.md', '')}

**Source:** {source_dir}/{filename}
**Language:** {lang}
**Topic:** {topic}
**Crawled:** {now}

## Content

{content[:3000]}
"""
    return entry


def reorganize():
    print("=" * 60)
    print("LinguaGraph BWKI Corpus Reorganizer")
    print("=" * 60)

    stats = {"total": 0, "classified": 0, "saved": 0, "by_topic": {}, "by_lang": {}}

    for source_dir in SOURCE_DIRS:
        source_path = os.path.join(BWKI_DIR, source_dir)
        if not os.path.isdir(source_path):
            continue

        print(f"\n--- Scanning: {source_dir} ---")
        dir_count = 0

        for filename in os.listdir(source_path):
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(source_path, filename)
            try:
                frontmatter, content = read_kb_file(filepath)
                if len(content) < 100:
                    continue

                lang = detect_language(content)
                topic = classify_topic(content)

                stats["total"] += 1
                dir_count += 1

                if topic:
                    stats["classified"] += 1
                    stats["by_topic"][topic] = stats["by_topic"].get(topic, 0) + 1
                    stats["by_lang"][lang] = stats["by_lang"].get(lang, 0) + 1

                    entry = create_corpus_entry(source_dir, filename, frontmatter, content, topic, lang)

                    subdir = os.path.join(OUTPUT_DIR, topic)
                    os.makedirs(subdir, exist_ok=True)

                    safe_name = re.sub(r'[\\/:*?"<>|]', "-", filename)[:100]
                    out_path = os.path.join(subdir, safe_name)

                    if not os.path.exists(out_path):
                        with open(out_path, "w", encoding="utf-8") as f:
                            f.write(entry)
                        stats["saved"] += 1

            except Exception as e:
                continue

        print(f"  Scanned: {dir_count} files")

    print(f"\n{'='*60}")
    print(f"Reorganization complete!")
    print(f"  Total scanned: {stats['total']}")
    print(f"  Classified: {stats['classified']}")
    print(f"  Saved to corpus: {stats['saved']}")
    print(f"\n  By topic:")
    for topic, count in sorted(stats["by_topic"].items(), key=lambda x: -x[1]):
        print(f"    {topic:25s}: {count}")
    print(f"\n  By language:")
    for lang, count in sorted(stats["by_lang"].items(), key=lambda x: -x[1]):
        print(f"    {lang:25s}: {count}")
    print(f"{'='*60}")

    return stats


if __name__ == "__main__":
    reorganize()
