"""
LinguaGraph Social Media Corpus Scraper
=======================================

Automatically scrapes social media discussions on specific topics
across multiple languages and platforms.

Stores raw text + full metadata in BWKI knowledge base.

Usage:
    python experiments/social_media_scraper.py

Targets:
    - Reddit (English discussions)
    - 知乎 discussions (via DuckDuckGo)
    - German forums (via DuckDuckGo)
    - YouTube comments (via Jina)

Topics: freedom, knowledge, success, responsibility, home/heimat
"""

import json
import os
import re
import sys
import time
import hashlib
from datetime import datetime, timezone
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "本地知识库", "知识库内容",
    "BWKI", "13_social_media_corpus"
)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

TOPICS = {
    "freedom": {
        "en": ["what is freedom", "freedom vs responsibility", "meaning of freedom society"],
        "zh": ["什么是自由", "自由与责任的关系", "自由的定义"],
        "de": ["was ist Freiheit", "Freiheit und Verantwortung", "Bedeutung von Freiheit"],
    },
    "knowledge": {
        "en": ["knowledge vs wisdom", "knowledge is power", "importance of education"],
        "zh": ["知识就是力量", "知识与智慧的区别", "教育的重要性"],
        "de": ["Wissen ist Macht", "Wissen und Weisung", "Bildung Bedeutung"],
    },
    "success": {
        "en": ["what is success", "success and happiness", "measure of success"],
        "zh": ["什么是成功", "成功的定义", "成功的标准"],
        "de": ["was ist Erfolg", "Erfolg und Glück", "Erfolg messen"],
    },
    "responsibility": {
        "en": ["personal responsibility", "responsibility vs freedom", "social responsibility"],
        "zh": ["个人责任", "社会责任", "责任与自由"],
        "de": ["persönliche Verantwortung", "soziale Verantwortung", "Verantwortung Freiheit"],
    },
    "home_heimat": {
        "en": ["what is home", "concept of home", "home vs house"],
        "zh": ["什么是家", "家的概念", "家与房子的区别"],
        "de": ["was ist Heimat", "Heimat Bedeutung", "Heimat und Zuhause"],
    },
}


def search_duckduckgo(query, num_results=10):
    """Search DuckDuckGo and return text snippets."""
    try:
        resp = requests.post(
            "https://html.duckduckgo.com/html/",
            data={"q": query},
            headers={"User-Agent": UA},
            timeout=30,
        )
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for item in soup.select(".result")[:num_results]:
            title_el = item.select_one(".result__a")
            snippet_el = item.select_one(".result__snippet")
            url_el = item.select_one(".result__url")
            if title_el:
                href = title_el.get("href", "")
                if href.startswith("//"):
                    href = "https:" + href
                title_text = title_el.get_text(strip=True)
                snippet_text = snippet_el.get_text(strip=True) if snippet_el else ""
                if len(snippet_text) > 30:
                    results.append({
                        "title": title_text,
                        "url": href,
                        "snippet": snippet_text,
                        "display_url": url_el.get_text(strip=True) if url_el else "",
                    })
        return results
    except Exception as e:
        print(f"  [WARN] DDG search failed: {e}")
        return []


def fetch_page_content(url, max_chars=3000):
    """Fetch page content via Jina Reader."""
    try:
        resp = requests.get(
            "https://r.jina.ai/" + url,
            headers={"User-Agent": UA},
            timeout=30,
        )
        resp.encoding = "utf-8"
        return resp.text[:max_chars]
    except Exception as e:
        return f"[FETCH_ERROR: {e}]"


def create_entry(topic, lang, platform, title, url, content, query):
    """Create a KB entry with full metadata."""
    now = datetime.now(timezone.utc).isoformat()
    content_hash = hashlib.md5(content[:500].encode()).hexdigest()[:12]
    safe_title = re.sub(r'[\\/:*?"<>|]', "-", title)[:80]

    filename = f"{topic}_{lang}_{platform}_{content_hash}.md"

    entry = f"""---
type: social_media
topic: {topic}
language: {lang}
platform: {platform}
source_url: "{url}"
query_used: "{query}"
crawled_at: "{now}"
content_hash: "{content_hash}"
quality: B
status: unverified
tags:
  - {topic}
  - {lang}
  - {platform}
  - social_media
  - crawled
---

# {title}

**Platform:** {platform}
**Language:** {lang}
**Topic:** {topic}
**URL:** {url}
**Query:** {query}
**Crawled:** {now}

## Content

{content}
"""
    return filename, entry


def scrape_topic(topic, lang, queries, platform_name, max_per_query=5):
    """Scrape all queries for a topic in a language."""
    entries = []
    for query in queries:
        try:
            print(f"  [{lang}] Query: {query.encode('ascii', 'replace').decode()}")
        except Exception:
            print(f"  [{lang}] Query: [encoded]")
        results = search_duckduckgo(query, num_results=max_per_query)

        for r in results:
            content = r["snippet"]
            if len(content) < 50:
                continue

            filename, entry = create_entry(
                topic=topic,
                lang=lang,
                platform=platform_name,
                title=r["title"],
                url=r["url"],
                content=content,
                query=query,
            )
            entries.append((filename, entry))

        time.sleep(2)

    return entries


def save_entries(entries, subdir):
    """Save entries to the KB directory."""
    dir_path = os.path.join(OUTPUT_DIR, subdir)
    os.makedirs(dir_path, exist_ok=True)

    saved = 0
    for filename, content in entries:
        filepath = os.path.join(dir_path, filename)
        if os.path.exists(filepath):
            continue
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            saved += 1
        except Exception as e:
            print(f"  [ERROR] Save failed: {filename}: {e}")

    return saved


def run_scraper():
    print("=" * 60)
    print("LinguaGraph Social Media Corpus Scraper")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    stats = {"total": 0, "saved": 0}

    for topic, lang_queries in TOPICS.items():
        print(f"\n--- Topic: {topic} ---")

        for lang, queries in lang_queries.items():
            platform = "duckduckgo_web"
            entries = scrape_topic(topic, lang, queries, platform, max_per_query=8)
            saved = save_entries(entries, "news_comments")
            stats["total"] += len(entries)
            stats["saved"] += saved
            print(f"  [{lang}] Found: {len(entries)}, Saved: {saved}")

    print(f"\n{'='*60}")
    print(f"Scraping complete!")
    print(f"  Total found: {stats['total']}")
    print(f"  Saved to KB: {stats['saved']}")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"{'='*60}")

    return stats


if __name__ == "__main__":
    run_scraper()
