#!/usr/bin/env python3
"""Task 1: Batch Wikipedia Concept Extraction — 5 topics × 3 languages"""
import json, re, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT / "data" / "wikipedia_extractions"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TOPICS = [
    ("freedom", "自由", "Freiheit",
     "https://zh.wikipedia.org/wiki/自由",
     "https://en.wikipedia.org/wiki/Freedom",
     "https://de.wikipedia.org/wiki/Freiheit"),
    ("justice", "正义", "Gerechtigkeit",
     "https://zh.wikipedia.org/wiki/正义",
     "https://en.wikipedia.org/wiki/Justice",
     "https://de.wikipedia.org/wiki/Gerechtigkeit"),
    ("responsibility", "责任", "Verantwortung",
     "https://zh.wikipedia.org/wiki/责任",
     "https://en.wikipedia.org/wiki/Responsibility",
     "https://de.wikipedia.org/wiki/Verantwortung"),
    ("home", "家", "Heimat",
     "https://zh.wikipedia.org/wiki/家",
     "https://en.wikipedia.org/wiki/Home",
     "https://de.wikipedia.org/wiki/Heimat"),
    ("success", "成功", "Erfolg",
     "https://zh.wikipedia.org/wiki/成功",
     "https://en.wikipedia.org/wiki/Success",
     "https://de.wikipedia.org/wiki/Erfolg"),
]

LANG_MAP = {"zh": 1, "en": 2, "de": 3}  # index in TOPICS tuple

def fetch_wiki_text(url, lang):
    """Fetch Wikipedia plain text via API."""
    title = url.rstrip("/").split("/")[-1]
    api = f"https://{lang}.wikipedia.org/w/api.php"
    params = (
        f"?action=query&titles={urllib.request.quote(title)}"
        f"&prop=extracts&explaintext=true&format=json"
        f"&exsectionformat=plain"
    )
    full_url = api + params
    try:
        req = urllib.request.Request(full_url, headers={"User-Agent": "LinguaGraph/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid == "-1":
                return None
            return page.get("extract", "")
    except Exception as e:
        print(f"  [WARN] fetch failed for {url}: {e}")
        return None

def extract_concepts_from_text(text, topic, lang, url):
    """Rule-based concept extraction from Wikipedia text."""
    sentences = re.split(r'[。！？\.\!\?\n]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]

    # Extract key noun phrases (simplified)
    concepts = []
    seen = set()

    # Language-specific patterns
    if lang == "zh":
        patterns = [
            r'([\u4e00-\u9fff]{2,8})(?:是|为|指|表示|意味着|包括|包含|属于)',
            r'([\u4e00-\u9fff]{2,6})(?:和|与|及|同|跟)([\u4e00-\u9fff]{2,6})',
        ]
    elif lang == "en":
        patterns = [
            r'([A-Z][a-z]+(?:\s+[a-z]+){0,3})\s+(?:is|are|refers?\s+to|means?)',
            r'(?:the\s+)?([a-z]+(?:\s+[a-z]+){0,2})\s+(?:of|and|or|in|for)\s+',
        ]
    else:  # de
        patterns = [
            r'([A-ZÄÖÜ][a-zäöüß]+(?:\s+[a-zäöüß]+){0,3})\s+(?:ist|sind|bedeutet|heißt)',
            r'(?:die\s+|der\s+|das\s+)([A-ZÄÖÜ][a-zäöüß]+(?:\s+[a-zäöüß]+){0,2})',
        ]

    for pat in patterns:
        for m in re.finditer(pat, text):
            name = m.group(1).strip()
            if len(name) >= 2 and name not in seen and name.lower() not in {topic.lower(), "wikipedia", "citation"}:
                seen.add(name)
                concepts.append(name)

    # Fallback: extract important words from first few sentences
    if len(concepts) < 5:
        for s in sentences[:15]:
            words = re.findall(r'[\w\u4e00-\u9fff]{3,}', s)
            for w in words:
                if w not in seen and len(w) >= 3:
                    seen.add(w)
                    concepts.append(w)
                    if len(concepts) >= 15:
                        break
            if len(concepts) >= 15:
                break

    concepts = concepts[:20]

    # Build relations
    relations = []
    for i, c1 in enumerate(concepts):
        for c2 in concepts[i+1:i+4]:
            if c1 != c2:
                relations.append({"source": c1, "target": c2, "type": "relates_to"})

    # Categorize
    categorized = []
    for i, c in enumerate(concepts):
        cat = "核心概念" if i < 5 else ("相关概念" if i < 12 else "具体事例")
        related = [concepts[j] for j in range(len(concepts)) if j != i and abs(j - i) <= 3][:3]
        categorized.append({
            "name": c,
            "category": cat,
            "related_concepts": related,
            "definition_snippet": next((s for s in sentences if c in s), "")[:100]
        })

    return {
        "topic": topic,
        "language": lang,
        "source_url": url,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "concepts": categorized,
        "relations": relations[:30]
    }


def run_extraction(topic_en, lang):
    idx = LANG_MAP[lang]
    topic_zh = TOPICS[[t[0] for t in TOPICS].index(topic_en)][1]
    topic_de = TOPICS[[t[0] for t in TOPICS].index(topic_en)][2]
    url = TOPICS[[t[0] for t in TOPICS].index(topic_en)][3 + list(LANG_MAP.keys()).index(lang)]

    print(f"  [{lang.upper()}] Fetching {topic_en}...")
    text = fetch_wiki_text(url, lang)
    if not text:
        print(f"  [SKIP] No text for {topic_en}/{lang}")
        return None

    print(f"  [{lang.upper()}] Extracting concepts from {len(text)} chars...")
    result = extract_concepts_from_text(text, topic_en, lang, url)

    out_file = OUT_DIR / f"{topic_en}_{lang}.json"
    out_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  [OK] {out_file.name}: {len(result['concepts'])} concepts, {len(result['relations'])} relations")
    return result


def main():
    print("=" * 60)
    print("Task 1: Wikipedia Concept Extraction")
    print("=" * 60)
    total = 0
    for topic_en, _, _, _, _, _ in TOPICS:
        for lang in ["zh", "en", "de"]:
            r = run_extraction(topic_en, lang)
            if r:
                total += 1
    print(f"\nDone: {total}/15 extractions saved to {OUT_DIR}")


if __name__ == "__main__":
    main()
