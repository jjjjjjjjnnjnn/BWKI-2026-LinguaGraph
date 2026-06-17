"""
Social Discussion Corpus Collector
===================================

Searches for social media discussions on specific topics in zh/en/de.
Uses DuckDuckGo + Jina Reader.

Usage:
    python experiments/collect_social.py

Output:
    data/pilot_dataset/social/{topic}/{lang}_{platform}_{id}.json
"""

import json
import os
import re
import time
import hashlib
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "pilot_dataset", "social")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

TOPICS = {
    "freedom": {
        "en": ["reddit what is freedom discussion", "reddit freedom meaning philosophy",
               "reddit freedom vs security", "reddit individual freedom society"],
        "zh": ["知乎 什么是自由 讨论", "知乎 自由与责任", "知乎 自由的定义", "知乎 自由 权利"],
        "de": ["Reddit Freiheit Bedeutung Diskussion", "Freiheit Verantwortung Forum",
               "was ist Freiheit Meinung", "Freiheit Gesellschaft Debatte"],
    },
    "justice": {
        "en": ["reddit what is justice discussion", "reddit justice fairness society",
               "reddit criminal justice philosophy", "reddit social justice debate"],
        "zh": ["知乎 什么是正义 讨论", "知乎 正义与公平", "知乎 社会正义", "知乎 正义 讨论"],
        "de": ["Reddit Gerechtigkeit Bedeutung Diskussion", "Gerechtigkeit Fairness Forum",
               "was ist Gerechtigkeit Debatte", "soziale Gerechtigkeit Discussion"],
    },
    "responsibility": {
        "en": ["reddit personal responsibility debate", "reddit responsibility freedom",
               "reddit social responsibility ethics", "reddit moral responsibility"],
        "zh": ["知乎 个人责任 讨论", "知乎 社会责任", "知乎 责任与自由", "知乎 道德责任"],
        "de": ["Reddit Verantwortung Bedeutung Diskussion", "persönliche Verantwortung Forum",
               "soziale Verantwortung Debatte", "moralische Verantwortung Discussion"],
    },
    "democracy": {
        "en": ["reddit what is democracy discussion", "reddit democracy meaning",
               "reddit democratic values debate", "reddit participation democracy"],
        "zh": ["知乎 什么是民主 讨论", "知乎 民主制度", "知乎 民主与参与", "知乎 民主价值观"],
        "de": ["Reddit Demokratie Bedeutung Diskussion", "Demokratie Teilhabe Forum",
               "was ist Demokratie Debatte", "demokratische Werte Discussion"],
    },
}


def search_ddg(query, num=8):
    try:
        resp = requests.post("https://html.duckduckgo.com/html/",
                           data={"q": query}, headers={"User-Agent": UA}, timeout=30)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for item in soup.select(".result")[:num]:
            title_el = item.select_one(".result__a")
            snippet_el = item.select_one(".result__snippet")
            if title_el and snippet_el:
                href = title_el.get("href", "")
                snippet = snippet_el.get_text(strip=True)
                if len(snippet) > 30:
                    results.append({"title": title_el.get_text(strip=True), "url": href, "snippet": snippet})
        return results
    except Exception:
        return []


def read_via_jina(url, max_chars=3000):
    try:
        resp = requests.get(f"https://r.jina.ai/{url}", headers={"User-Agent": UA}, timeout=30)
        return resp.text[:max_chars]
    except Exception:
        return None


def detect_platform(url):
    url_lower = url.lower()
    if "reddit.com" in url_lower:
        return "reddit"
    elif "zhihu.com" in url_lower:
        return "zhihu"
    elif "v2ex.com" in url_lower:
        return "v2ex"
    elif "stackoverflow.com" in url_lower:
        return "stackoverflow"
    elif "quora.com" in url_lower:
        return "quora"
    else:
        return "forum"


def collect_topic(topic, lang_queries):
    results = []
    for lang, queries in lang_queries.items():
        print(f"  [{lang}] Searching {len(queries)} queries...")
        seen_urls = set()

        for query in queries:
            search_results = search_ddg(query, num=6)
            time.sleep(2)

            for sr in search_results:
                if sr["url"] in seen_urls:
                    continue
                seen_urls.add(sr["url"])

                platform = detect_platform(sr["url"])
                content = read_via_jina(sr["url"])
                time.sleep(1)

                if not content or len(content) < 100:
                    content = sr["snippet"]

                entry = {
                    "id": f"social_{lang}_{platform}_{hashlib_md5(sr['url'])}",
                    "dataset": "social",
                    "topic": topic,
                    "language": lang,
                    "platform": platform,
                    "source_url": sr["url"],
                    "title": sr["title"],
                    "content": content[:3000],
                    "word_count": len(content.split()),
                    "crawled_at": datetime.now(timezone.utc).isoformat(),
                    "content_hash": hashlib_md5(content[:500]),
                }
                results.append(entry)

            lang_count = len([r for r in results if r["language"] == lang])
            print(f"    [{lang}] Done, total: {lang_count}")

    return results


def hashlib_md5(text):
    return hashlib.md5(text.encode()).hexdigest()[:12]


def save_results(topic, results):
    topic_dir = os.path.join(OUTPUT_DIR, topic)
    os.makedirs(topic_dir, exist_ok=True)
    for i, entry in enumerate(results):
        filename = f"{entry['language']}_{entry['platform']}_{i:03d}.json"
        filepath = os.path.join(topic_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)


def main():
    print("=" * 60)
    print("Social Discussion Corpus Collector")
    print("=" * 60)

    total = 0
    for topic, lang_queries in TOPICS.items():
        print(f"\n--- Topic: {topic} ---")
        results = collect_topic(topic, lang_queries)
        save_results(topic, results)
        total += len(results)
        print(f"  Saved: {len(results)} discussions")

    print(f"\n{'='*60}")
    print(f"Total: {total} social discussions collected")
    print(f"Output: {OUTPUT_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
