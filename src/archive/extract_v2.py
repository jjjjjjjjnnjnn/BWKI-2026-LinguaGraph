"""LinguaGraph — 增强版概念提取模块
基于两阶段提取设计（Meta-Knowledge-Graph 方法论）：
Stage 1: 文本理解 → 识别关键概念
Stage 2: 概念关系提取 → 构建认知图
支持多语言输入，输出标准化概念-关系三元组。
"""
import json
import re
import os
import sys
from typing import Dict, List, Tuple, Optional

LM_URL = os.getenv("LM_URL", "http://127.0.0.1:1234/v1/chat/completions")
LM_MODEL = os.getenv("LM_MODEL", "qwen3.5-9b-uncensored-hauhaucs-aggressive")

CONCEPT_EXTRACTION_PROMPT_ZH = """你是一个认知科学研究员。从以下回答中提取核心概念和它们之间的关系。

规则：
1. 提取 5-15 个核心概念（名词或名词短语）
2. 识别概念之间的关系（如：因果、对比、包含、前提、等价）
3. 输出 JSON 格式

示例输入：
"自由是每个人最基本的权利，但自由也需要责任来平衡。真正的幸福来自于对真理的追求。"

示例输出：
{
  "concepts": ["自由", "责任", "权利", "幸福", "真理"],
  "relations": [
    {"from": "自由", "to": "责任", "type": "requires"},
    {"from": "自由", "to": "权利", "type": "is_a"},
    {"from": "幸福", "to": "真理", "type": "derived_from"}
  ]
}

现在请分析以下文本：
"""


CONCEPT_EXTRACTION_PROMPT_DE = """Du bist ein kognitiver Wissenschaftler. Extrahiere die Kernkonzepte und ihre Beziehungen aus der folgenden Antwort.

Regeln:
1. Extrahiere 5-15 Kernkonzepte (Substantive oder Substantivphrasen)
2. Identifiziere Beziehungen zwischen Konzepten (z.B. Ursache-Wirkung, Kontrast, Enthaltensein, Voraussetzung, Gleichwertigkeit)
3. Gib das Ergebnis im JSON-Format aus

Beispieltext:
"Freiheit ist das grundlegendste Recht eines jeden Menschen, aber Freiheit braucht auch Verantwortung als Gegenpol."

Beispielausgabe:
{
  "concepts": ["Freiheit", "Verantwortung", "Recht", "Gleichgewicht"],
  "relations": [
    {"from": "Freiheit", "to": "Verantwortung", "type": "requires"},
    {"from": "Freiheit", "to": "Recht", "type": "is_a"}
  ]
}

Analysiere nun folgenden Text:
"""


CONCEPT_EXTRACTION_PROMPT_EN = """You are a cognitive scientist. Extract core concepts and their relationships from the following response.

Rules:
1. Extract 5-15 core concepts (nouns or noun phrases)
2. Identify relationships between concepts (e.g., causal, contrast, contains, prerequisite, equivalent)
3. Output in JSON format

Example input:
"Freedom is every person's most fundamental right, but freedom also requires responsibility as a counterbalance."

Example output:
{
  "concepts": ["freedom", "responsibility", "right", "balance"],
  "relations": [
    {"from": "freedom", "to": "responsibility", "type": "requires"},
    {"from": "freedom", "to": "right", "type": "is_a"}
  ]
}

Now analyze the following text:
"""

PROMPTS = {
    "zh": CONCEPT_EXTRACTION_PROMPT_ZH,
    "de": CONCEPT_EXTRACTION_PROMPT_DE,
    "en": CONCEPT_EXTRACTION_PROMPT_EN,
}


def call_llm(messages, max_tokens=2048):
    """调用本地 LM Studio 或 OpenAI API。"""
    import requests
    try:
        payload = {
            "model": LM_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.2,
        }
        resp = requests.post(LM_URL, json=payload, timeout=120)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        return content
    except Exception as e:
        print(f"[WARN] LLM call failed: {e}")
        return None


def extract_concepts_llm(text: str, lang: str = "en") -> Dict:
    """Stage 1: 使用 LLM 提取概念和关系。"""
    prompt = PROMPTS.get(lang, PROMPTS["en"]) + text
    messages = [
        {"role": "system", "content": "You are a cognitive scientist. Output only valid JSON."},
        {"role": "user", "content": prompt},
    ]

    response = call_llm(messages)
    if not response:
        return fallback_extract(text, lang)

    try:
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            data = json.loads(json_match.group())
            concepts = data.get("concepts", [])
            relations = data.get("relations", [])
            if concepts:
                return {"concepts": concepts, "relations": relations, "method": "llm"}
    except json.JSONDecodeError:
        pass

    return fallback_extract(text, lang)


def fallback_extract(text: str, lang: str = "en") -> Dict:
    """后备方案：基于关键词匹配的简单提取。"""
    keyword_maps = {
        "zh": {
            "自由": ["自由", "权利"], "正义": ["正义", "公平", "公正"],
            "幸福": ["幸福", "快乐", "满足"], "真理": ["真理", "真相", "事实"],
            "知识": ["知识", "学问", "认知"], "权力": ["权力", "力量", "权"],
            "时间": ["时间", "时刻", "时代"], "变化": ["变化", "改变", "变迁"],
            "思维": ["思维", "思考", "思想"], "语言": ["语言", "话语", "表达"],
            "文化": ["文化", "文明"], "社会": ["社会", "社群"],
            "自然": ["自然", "生态"], "自我": ["自我", "自己", "自身"],
            "爱": ["爱", "爱情", "热爱"], "死亡": ["死亡", "逝去", "终结"],
            "生命": ["生命", "生活", "生"], "家庭": ["家庭", "家"],
        },
        "de": {
            "Freiheit": ["Freiheit", "frei"], "Gerechtigkeit": ["Gerechtigkeit", "gerecht"],
            "Glück": ["Glück", "glücklich"], "Wahrheit": ["Wahrheit", "wahr"],
            "Wissen": ["Wissen", "Kenntnis"], "Macht": ["Macht", "Kraft"],
            "Zeit": ["Zeit", "Zeiten"], "Veränderung": ["Veränderung", "ändern"],
            "Gedanke": ["Gedanke", "Denken"], "Sprache": ["Sprache", "Sprachen"],
            "Kultur": ["Kultur"], "Gesellschaft": ["Gesellschaft"],
            "Natur": ["Natur"], "Selbst": ["Selbst", "sich"],
            "Liebe": ["Liebe", "lieben"], "Tod": ["Tod", "sterben"],
            "Leben": ["Leben", "leben"], "Familie": ["Familie"],
        },
        "en": {
            "freedom": ["freedom", "free", "liberty"], "justice": ["justice", "fair"],
            "happiness": ["happiness", "happy", "joy"], "truth": ["truth", "true"],
            "knowledge": ["knowledge", "know"], "power": ["power", "strength"],
            "time": ["time", "temporal"], "change": ["change", "transform"],
            "thought": ["thought", "think", "thinking"], "language": ["language", "linguistic"],
            "culture": ["culture", "cultural"], "society": ["society", "social"],
            "nature": ["nature", "natural"], "self": ["self", "identity"],
            "love": ["love", "loving"], "death": ["death", "die"],
            "life": ["life", "live", "living"], "family": ["family"],
        },
    }

    keywords = keyword_maps.get(lang, keyword_maps["en"])
    text_lower = text.lower()
    concepts = []
    relations = []

    for concept, words in keywords.items():
        for w in words:
            if w.lower() in text_lower:
                concepts.append(concept)
                break

    for i, c1 in enumerate(concepts):
        for c2 in concepts[i+1:]:
            relations.append({"from": c1, "to": c2, "type": "co_occurs"})

    return {"concepts": concepts, "relations": relations, "method": "fallback"}


def extract_from_student_response(response: str, lang: str = "en", use_llm: bool = True) -> Dict:
    """从学生回答中提取认知图。
    
    Args:
        response: 学生的回答文本
        lang: 语言代码 (zh/de/en)
        use_llm: 是否使用 LLM（False 时用 fallback）
    
    Returns:
        包含 concepts, relations, method 的字典
    """
    if use_llm:
        return extract_concepts_llm(response, lang)
    else:
        return fallback_extract(response, lang)


def extract_batch(responses: List[Dict], use_llm: bool = True) -> List[Dict]:
    """批量提取概念。
    
    Args:
        responses: [{"text": "...", "lang": "zh", "id": "S001"}, ...]
    
    Returns:
        提取结果列表
    """
    results = []
    for i, item in enumerate(responses):
        print(f"  [{i+1}/{len(responses)}] Extracting {item.get('lang', 'en')}...")
        result = extract_from_student_response(
            item["text"], item.get("lang", "en"), use_llm=use_llm
        )
        result["id"] = item.get("id", f"item_{i}")
        result["lang"] = item.get("lang", "en")
        result["source_text"] = item["text"][:200]
        results.append(result)
    return results


if __name__ == "__main__":
    test_responses = [
        {"text": "自由是每个人最基本的权利，但自由也需要责任来平衡。真正的幸福来自于对真理的追求。", "lang": "zh", "id": "zh_001"},
        {"text": "Freiheit ist das grundlegendste Recht eines jeden Menschen, aber Freiheit braucht auch Verantwortung.", "lang": "de", "id": "de_001"},
        {"text": "Freedom is every person's most fundamental right, but freedom also requires responsibility.", "lang": "en", "id": "en_001"},
    ]

    print("=== 测试 Fallback 提取 ===")
    for item in test_responses:
        result = extract_from_student_response(item["text"], item["lang"], use_llm=False)
        print(f"  {item['id']}: {result['concepts']} ({len(result['relations'])} relations)")
