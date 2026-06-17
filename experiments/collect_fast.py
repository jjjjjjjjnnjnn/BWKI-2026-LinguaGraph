"""
Fast Corpus Collector — DDG Snippets Only (No Jina)
=====================================================

Uses DuckDuckGo search snippets directly — much faster.
No page fetching, just search results.

Usage:
    python experiments/collect_fast.py
"""

import json
import os
import re
import time
import hashlib
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "pilot_dataset")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

TOPICS = {
    "freedom": {
        "en": ["what is freedom philosophy", "freedom meaning society", "freedom rights responsibility",
               "concept of freedom political", "freedom individual society", "liberty freedom difference"],
        "zh": ["什么是自由 哲学", "自由的含义 社会", "自由 权利 责任",
               "自由的概念 政治", "自由 个人 社会", "自由与区别"],
        "de": ["was ist Freiheit Philosophie", "Freiheit Bedeutung Gesellschaft", "Freiheit Recht Verantwortung",
               "Freiheit Konzept Politik", "Freiheit Individuum Gesellschaft", "Freiheit Liberty Unterschied"],
    },
    "justice": {
        "en": ["what is justice philosophy", "justice fairness society", "justice concept political",
               "social justice meaning", "justice ethics morality", "justice law society"],
        "zh": ["什么是正义 哲学", "正义 公平 社会", "正义的概念 政治",
               "社会正义 含义", "正义 伦理 道德", "正义 法律 社会"],
        "de": ["was ist Gerechtigkeit Philosophie", "Gerechtigkeit Fairness Gesellschaft", "Gerechtigkeit Konzept Politik",
               "soziale Gerechtigkeit Bedeutung", "Gerechtigkeit Ethik Moral", "Gerechtigkeit Recht Gesellschaft"],
    },
    "responsibility": {
        "en": ["what is responsibility ethics", "personal responsibility meaning", "social responsibility concept",
               "responsibility freedom ethics", "moral responsibility philosophy", "responsibility society duty"],
        "zh": ["什么是责任 伦理", "个人责任 含义", "社会责任 概念",
               "责任 自由 伦理", "道德责任 哲学", "责任 社会 义务"],
        "de": ["was ist Verantwortung Ethik", "persoenliche Verantwortung Bedeutung", "soziale Verantwortung Konzept",
               "Verantwortung Freiheit Ethik", "moralische Verantwortung Philosophie", "Verantwortung Gesellschaft Pflicht"],
    },
    "success": {
        "en": ["what is success meaning", "success definition philosophy", "success happiness society",
               "measure of success life", "success failure learning", "success values education"],
        "zh": ["什么是成功 含义", "成功的定义 哲学", "成功 幸福 社会",
               "成功的标准 人生", "成功 失败 学习", "成功 价值观 教育"],
        "de": ["was ist Erfolg Bedeutung", "Erfolg Definition Philosophie", "Erfolg Glueck Gesellschaft",
               "Erfolg messen Leben", "Erfolg Misserfolg Lernen", "Erfolg Werte Bildung"],
    },
    "home": {
        "en": ["what is home meaning", "home concept philosophy", "home belonging identity",
               "home vs house difference", "home culture society", "heimat home comparison"],
        "zh": ["什么是家 含义", "家的概念 哲学", "家 归属 身份",
               "家与房子 区别", "家 文化 社会", "家 乡愁 概念"],
        "de": ["was ist Heimat Bedeutung", "Heimat Konzept Philosophie", "Heimat Zugehoerigkeit Identitaet",
               "Heimat vs Zuhause Unterschied", "Heimat Kultur Gesellschaft", "Heimat Bedeutung modern"],
    },
}


def search_ddg(query, num=10):
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
                    results.append({
                        "title": title_el.get_text(strip=True),
                        "url": href,
                        "snippet": snippet,
                    })
        return results
    except Exception:
        return []


def hashlib_md5(text):
    return hashlib.md5(text.encode()).hexdigest()[:12]


def collect_all():
    print("=" * 60)
    print("Fast Corpus Collector (DDG Snippets)")
    print("=" * 60)

    total = 0
    for topic, lang_queries in TOPICS.items():
        print(f"\n--- Topic: {topic} ---")
        topic_dir = os.path.join(OUTPUT_DIR, "education", topic)
        os.makedirs(topic_dir, exist_ok=True)
        saved = 0

        for lang, queries in lang_queries.items():
            seen = set()
            for query in queries:
                results = search_ddg(query, num=8)
                time.sleep(2)

                for r in results:
                    url_hash = hashlib.md5(r["url"].encode()).hexdigest()[:12]
                    if url_hash in seen:
                        continue
                    seen.add(url_hash)

                    entry = {
                        "id": f"edu_{lang}_{topic}_{url_hash}",
                        "dataset": "education",
                        "topic": topic,
                        "language": lang,
                        "platform": "web",
                        "source_url": r["url"],
                        "title": r["title"],
                        "content": r["snippet"],
                        "word_count": len(r["snippet"].split()),
                        "crawled_at": datetime.now(timezone.utc).isoformat(),
                        "content_hash": url_hash,
                    }

                    filename = f"{lang}_{topic}_{url_hash}.json"
                    filepath = os.path.join(topic_dir, filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(entry, f, ensure_ascii=False, indent=2)
                    saved += 1

            lang_count = len([f for f in os.listdir(topic_dir) if f.startswith(f"{lang}_")])
            print(f"  [{lang}] {lang_count} entries")

        total += saved
        print(f"  Topic total: {saved}")

    print(f"\n{'='*60}")
    print(f"Total: {total} entries collected")
    print(f"Output: {OUTPUT_DIR}/education/")
    print(f"{'='*60}")


if __name__ == "__main__":
    collect_all()
