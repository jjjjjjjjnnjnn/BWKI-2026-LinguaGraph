#!/usr/bin/env python3
"""
Improved corpus analysis for LinguaGraph BWKI 2026.
Analyzes 12 Wikipedia corpus files (4 topics x 3 languages).
"""
import re, json
from collections import Counter
from pathlib import Path

BASE = Path(r"C:\Users\rongj\Desktop\学校\BWKI-2026-备战\data\corpus")

FILES = {
    "freedom": {"de": "freedom/de_freiheit_wikipedia.txt",    "en": "freedom/en_freedom_wikipedia.txt",    "zh": "freedom/zh_自由_wikipedia.txt"},
    "justice": {"de": "justice/de_gerechtigkeit_wikipedia.txt","en": "justice/en_justice_wikipedia.txt",    "zh": "justice/zh_公平正义_wikipedia.txt"},
    "responsibility": {"de": "responsibility/de_verantwortung_wikipedia.txt","en": "responsibility/en_responsibility_wikipedia.txt","zh": "responsibility/zh_责任_wikipedia.txt"},
    "success": {"de": "success/de_erfolg_wikipedia.txt",      "en": "success/en_success_wikipedia.txt",     "zh": "success/zh_成功_wikipedia.txt"},
}

DE_STOP = set("der die das den dem des ein eine einer eines einem einen und oder aber denn doch jedoch auch sowie als wie beim durch fuer gegen ohne mit nach auf von zur zum bis aus bei in an um ueber unter vor zwischen ist sind war wurde werden wird sein habe hat sich sie er es wir ihr ich man nicht kein keine keinen keinem keines nur sehr ganz schon noch mal dass weil wenn da also dann dort hier dieser diese dieses diesen diesem welcher welche welches welchen welchem alle beide bitte etwas gross gut immer mehr vielleicht viel wirklich wer was welche welcher wie worden zum zwischen schon sondern".split())

EN_STOP = set("the a an of in to is and that for it as be with on at by from or are this have has not but they he she we its about because if which all their each would could should may might must can do does did will been being having some no nor only so than very just also well there into over such what when where who how whether though although".split())

# Common Chinese function characters to exclude from keyword lists
ZH_FUNC = set('的了在和有也这不那我一她他它个就对都与为被把从到要会可让让而是很又没将向您来说些之吗吧啊哦嗯呢呀嘛么什么如何')

def is_cjk(c):
    return '一' <= c <= '鿿' or '㐀' <= c <= '䶿'

def clean_line(line):
    return not (line.startswith('Source:') or line.startswith('License:') or line.startswith('Retrieved:'))

def load_text(topic, lang):
    path = BASE / FILES[topic][lang]
    with open(path, 'r', encoding='utf-8') as f:
        return ''.join(l for l in f.read().split('\n') if clean_line(l))

# ---- ZH analysis ----
def analyze_zh(text):
    chars = [c for c in text if is_cjk(c)]
    total = len(chars)
    unique = len(set(chars))

    # Character frequency
    char_freq = Counter(chars)

    # Generate bigrams (sliding window of 2 chars, like words)
    bigrams = [chars[i] + chars[i+1] for i in range(len(chars)-1)]
    trigrams = [chars[i] + chars[i+1] + chars[i+2] for i in range(len(chars)-2)]

    bigram_freq = Counter(bigrams)
    trigram_freq = Counter(trigrams)

    # Top characters (filtering function chars)
    top_chars_raw = [(c, f) for c, f in char_freq.most_common(30) if c not in ZH_FUNC]

    # Top bigrams (filter out those containing only function chars)
    top_bigrams_raw = [(w, f) for w, f in bigram_freq.most_common(30)
                       if len(w) == 2 and not all(c in ZH_FUNC for c in w)]

    # Top trigrams
    top_trigrams_raw = [(w, f) for w, f in trigram_freq.most_common(30)
                        if len(w) == 3 and not all(c in ZH_FUNC for c in w)]

    diversity = round(unique / total * 100, 2) if total else 0

    return {
        "total_words": total,
        "unique_tokens": unique,
        "type_token_ratio": round(unique / total, 4) if total else 0,
        "vocabulary_diversity_index": diversity,
        "top_chars": [{"char": c, "freq": f} for c, f in top_chars_raw[:10]],
        "top_bigrams": [{"word": w, "freq": f} for w, f in top_bigrams_raw[:10]],
        "top_trigrams": [{"word": w, "freq": f} for w, f in top_trigrams_raw[:10]],
    }

# ---- DE analysis ----
def analyze_de(text):
    tokens = re.findall(r'[a-zA-ZäöüÄÖÜß]+', text.lower())
    total = len(tokens)
    unique = len(set(tokens))
    content = [t for t in tokens if t not in DE_STOP and len(t) > 1]
    freq = Counter(content)
    diversity = round(len(set(content)) / total * 100, 2) if total else 0
    return {
        "total_words": total,
        "unique_tokens": unique,
        "type_token_ratio": round(unique / total, 4) if total else 0,
        "vocabulary_diversity_index": diversity,
        "top_keywords": [{"word": w, "freq": f} for w, f in freq.most_common(10)],
    }

# ---- EN analysis ----
def analyze_en(text):
    tokens = re.findall(r'[a-zA-Z]+', text.lower())
    total = len(tokens)
    unique = len(set(tokens))
    content = [t for t in tokens if t not in EN_STOP and len(t) > 1]
    freq = Counter(content)
    diversity = round(len(set(content)) / total * 100, 2) if total else 0
    return {
        "total_words": total,
        "unique_tokens": unique,
        "type_token_ratio": round(unique / total, 4) if total else 0,
        "vocabulary_diversity_index": diversity,
        "top_keywords": [{"word": w, "freq": f} for w, f in freq.most_common(10)],
    }

# ---- RUN ----
results = {}
for topic in ["freedom", "justice", "responsibility", "success"]:
    lang_data = {}
    for lang in ["zh", "de", "en"]:
        text = load_text(topic, lang)
        if lang == "zh":
            lang_data[lang] = analyze_zh(text)
        elif lang == "de":
            lang_data[lang] = analyze_de(text)
        else:
            lang_data[lang] = analyze_en(text)
    results[topic] = {"topic": topic, "languages": lang_data}

# Cross-language comparison
comparison = {}
for topic in results:
    langs = results[topic]["languages"]
    sizes = {l: langs[l]["total_words"] for l in langs}
    diversi = {l: langs[l]["vocabulary_diversity_index"] for l in langs}

    # Analyze unique conceptual framing per language
    zh_top = set(c["char"] for c in langs["zh"].get("top_chars", []))
    en_top = set(w["word"] for w in langs["en"].get("top_keywords", []))
    de_top = set(w["word"] for w in langs["de"].get("top_keywords", []))

    comparison[topic] = {
        "corpus_size_by_language": sizes,
        "total_words_all_languages": sum(sizes.values()),
        "largest_corpus": max(sizes, key=sizes.get),
        "vocabulary_diversity_by_language": diversi,
        "most_diverse_language": max(diversi, key=diversi.get),
        "least_diverse_language": min(diversi, key=diversi.get),
    }

output = {"analysis_timestamp": "2026-06-17", "per_topic_per_language": results, "cross_language_comparison": comparison}

outpath = BASE / "corpus_analysis.json"
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f"Written to {outpath}")
