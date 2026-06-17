"""
Wikipedia Parallel Corpus Collector
====================================

Downloads Wikipedia articles on specific topics in zh/en/de.
Uses the Wikipedia REST API (no authentication needed).

Usage:
    python experiments/collect_wikipedia.py

Output:
    data/pilot_dataset/wikipedia/{topic}/{lang}_{topic}.json
"""

import json
import os
import re
import time
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "pilot_dataset", "wikipedia")

TOPICS = {
    "freedom": {"zh": "自由", "en": "Freedom", "de": "Freiheit"},
    "justice": {"zh": "正义", "en": "Justice", "de": "Gerechtigkeit"},
    "responsibility": {"zh": "责任", "en": "Responsibility", "de": "Verantwortung"},
    "democracy": {"zh": "民主", "en": "Democracy", "de": "Demokratie"},
}

LANGUAGES = ["zh", "en", "de"]


def get_wikipedia_summary(lang, title):
    """Get Wikipedia article summary via REST API."""
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"
    try:
        resp = requests.get(url, headers={"User-Agent": "LinguaGraph/1.0"}, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return {
            "title": data.get("title", title),
            "extract": data.get("extract", ""),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
            "description": data.get("description", ""),
        }
    except Exception as e:
        print(f"  [WARN] Summary failed for {lang}/{title}: {e}")
        return None


def get_wikipedia_full_text(lang, title):
    """Get full Wikipedia article text via HTML endpoint."""
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/html/{title}"
    try:
        resp = requests.get(url, headers={"User-Agent": "LinguaGraph/1.0"}, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup.find_all(["script", "style", "nav", "footer", "sup"]):
            tag.decompose()

        paragraphs = []
        for p in soup.find_all(["p", "h2", "h3"]):
            text = p.get_text(strip=True)
            if len(text) > 20:
                paragraphs.append(text)

        return "\n\n".join(paragraphs)
    except Exception as e:
        print(f"  [WARN] Full text failed for {lang}/{title}: {e}")
        return None


def collect_topic(topic, lang_titles):
    """Collect Wikipedia articles for one topic across languages."""
    results = []
    for lang in LANGUAGES:
        title = lang_titles.get(lang)
        if not title:
            continue

        print(f"  [{lang}] Fetching: {title}")

        summary = get_wikipedia_summary(lang, title)
        time.sleep(1)

        full_text = get_wikipedia_full_text(lang, title)
        time.sleep(1)

        if not summary and not full_text:
            print(f"  [{lang}] SKIP — no data")
            continue

        content = full_text or summary.get("extract", "")
        word_count = len(content.split())

        entry = {
            "id": f"wiki_{lang}_{topic}_{datetime.now().strftime('%Y%m%d')}",
            "dataset": "wikipedia",
            "topic": topic,
            "language": lang,
            "platform": "wikipedia",
            "source_url": summary.get("url", "") if summary else "",
            "title": summary.get("title", title) if summary else title,
            "content": content[:5000],
            "word_count": word_count,
            "crawled_at": datetime.now(timezone.utc).isoformat(),
            "content_hash": hashlib_md5(content[:500]),
        }
        results.append(entry)
        print(f"  [{lang}] OK — {word_count} words")

    return results


def hashlib_md5(text):
    import hashlib
    return hashlib.md5(text.encode()).hexdigest()[:12]


def save_results(topic, results):
    """Save results to JSON."""
    topic_dir = os.path.join(OUTPUT_DIR, topic)
    os.makedirs(topic_dir, exist_ok=True)

    for entry in results:
        filename = f"{entry['language']}_{topic}.json"
        filepath = os.path.join(topic_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)


def main():
    print("=" * 60)
    print("Wikipedia Parallel Corpus Collector")
    print("=" * 60)

    total = 0
    for topic, lang_titles in TOPICS.items():
        print(f"\n--- Topic: {topic} ---")
        results = collect_topic(topic, lang_titles)
        save_results(topic, results)
        total += len(results)
        print(f"  Saved: {len(results)} articles")

    print(f"\n{'='*60}")
    print(f"Total: {total} articles collected")
    print(f"Output: {OUTPUT_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
