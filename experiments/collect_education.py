"""
Education Materials Corpus Collector
====================================

Searches for educational materials on specific topics in zh/en/de.
Uses DuckDuckGo + Jina Reader.

Usage:
    python experiments/collect_education.py

Output:
    data/pilot_dataset/education/{topic}/{lang}_{topic}_{id}.json
"""

import json
import os
import re
import time
import hashlib
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "pilot_dataset", "education")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

TOPICS = {
    "freedom": {
        "en": ["freedom philosophy education", "what is freedom essay", "freedom political science textbook",
               "liberty and rights education", "freedom concept explained"],
        "zh": ["自由 哲学 教育", "什么是自由 论文", "自由 政治学 教材",
               "自由与权利 教育", "自由概念 解释"],
        "de": ["Freiheit Philosophie Bildung", "was ist Freiheit Aufsatz", "Freiheit Politik Lehrbuch",
               "Freiheit Recht Bildung", "Freiheit Konzept Erklärung"],
    },
    "justice": {
        "en": ["justice philosophy education", "what is justice essay", "justice political theory",
               "fairness and justice explained", "justice concept education"],
        "zh": ["正义 哲学 教育", "什么是正义 论文", "正义 政治哲学 教材",
               "公平与正义 教育", "正义概念 解释"],
        "de": ["Gerechtigkeit Philosophie Bildung", "was ist Gerechtigkeit Aufsatz", "Gerechtigkeit Politik Theorie",
               "Fairness Gerechtigkeit Erklärung", "Gerechtigkeit Konzept Bildung"],
    },
    "responsibility": {
        "en": ["responsibility ethics education", "personal responsibility essay", "social responsibility explained",
               "responsibility philosophy", "moral responsibility education"],
        "zh": ["责任 伦理 教育", "个人责任 论文", "社会责任 解释",
               "责任 哲学 教育", "道德责任 教育"],
        "de": ["Verantwortung Ethik Bildung", "persönliche Verantwortung Aufsatz", "soziale Verantwortung Erklärung",
               "Verantwortung Philosophie", "moralische Verantwortung Bildung"],
    },
    "democracy": {
        "en": ["democracy education explained", "what is democracy essay", "democratic theory education",
               "democracy and participation", "democratic values education"],
        "zh": ["民主 教育 解释", "什么是民主 论文", "民主理论 教育",
               "民主与参与 教育", "民主价值观 教育"],
        "de": ["Demokratie Bildung Erklärung", "was ist Demokratie Aufsatz", "Demokratietheorie Bildung",
               "Demokratie Teilhabe", "demokratische Werte Bildung"],
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
                if len(snippet) > 50:
                    results.append({"title": title_el.get_text(strip=True), "url": href, "snippet": snippet})
        return results
    except Exception:
        return []


def read_via_jina(url, max_chars=4000):
    try:
        resp = requests.get(f"https://r.jina.ai/{url}", headers={"User-Agent": UA}, timeout=30)
        return resp.text[:max_chars]
    except Exception:
        return None


def collect_topic(topic, lang_queries):
    results = []
    for lang, queries in lang_queries.items():
        print(f"  [{lang}] Searching {len(queries)} queries...")
        seen_urls = set()

        for query in queries:
            search_results = search_ddg(query, num=5)
            time.sleep(2)

            for sr in search_results:
                if sr["url"] in seen_urls:
                    continue
                seen_urls.add(sr["url"])

                content = read_via_jina(sr["url"])
                time.sleep(1)

                if not content or len(content) < 200:
                    content = sr["snippet"]

                entry = {
                    "id": f"edu_{lang}_{topic}_{hashlib_md5(sr['url'])}",
                    "dataset": "education",
                    "topic": topic,
                    "language": lang,
                    "platform": "educational_web",
                    "source_url": sr["url"],
                    "title": sr["title"],
                    "content": content[:4000],
                    "word_count": len(content.split()),
                    "crawled_at": datetime.now(timezone.utc).isoformat(),
                    "content_hash": hashlib_md5(content[:500]),
                }
                results.append(entry)

            print(f"    [{lang}] Query done, total so far: {len([r for r in results if r['language'] == lang])}")

    return results


def hashlib_md5(text):
    return hashlib.md5(text.encode()).hexdigest()[:12]


def save_results(topic, results):
    topic_dir = os.path.join(OUTPUT_DIR, topic)
    os.makedirs(topic_dir, exist_ok=True)
    for i, entry in enumerate(results):
        filename = f"{entry['language']}_{topic}_{i:03d}.json"
        filepath = os.path.join(topic_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)


def main():
    print("=" * 60)
    print("Education Materials Corpus Collector")
    print("=" * 60)

    total = 0
    for topic, lang_queries in TOPICS.items():
        print(f"\n--- Topic: {topic} ---")
        results = collect_topic(topic, lang_queries)
        save_results(topic, results)
        total += len(results)
        print(f"  Saved: {len(results)} texts")

    print(f"\n{'='*60}")
    print(f"Total: {total} education texts collected")
    print(f"Output: {OUTPUT_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
