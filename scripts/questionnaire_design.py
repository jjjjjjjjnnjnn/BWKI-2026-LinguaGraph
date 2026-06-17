"""
LinguaGraph 问卷设计

用于收集学生对社会议题的跨语言回答
"""

# 中文问卷
QUESTIONNAIRE_ZH = {
    "title": "语言与思维调查（中文版）",
    "description": "请用中文回答以下问题，表达你真实的想法",
    "questions": [
        {
            "id": "q1",
            "topic": "自由",
            "text": "什么是自由？请用自己的话解释。",
            "type": "open"
        },
        {
            "id": "q2",
            "topic": "公平",
            "text": "什么是公平？它和什么有关？",
            "type": "open"
        },
        {
            "id": "q3",
            "topic": "成功",
            "text": "什么是成功？你怎么定义成功？",
            "type": "open"
        },
        {
            "id": "q4",
            "topic": "家庭",
            "text": "家庭对你来说意味着什么？",
            "type": "open"
        }
    ],
    "metadata": {
        "language": "zh",
        "version": "1.0",
        "created": "2026-06-16"
    }
}

# 德语问卷
QUESTIONNAIRE_DE = {
    "title": "Sprache und Denken (Deutsch)",
    "description": "Bitte beantworten Sie die folgenden Fragen auf Deutsch",
    "questions": [
        {
            "id": "q1",
            "topic": "Freiheit",
            "text": "Was ist Freiheit? Erklären Sie mit eigenen Worten.",
            "type": "open"
        },
        {
            "id": "q2",
            "topic": "Gerechtigkeit",
            "text": "Was ist Gerechtigkeit? Womit hängt sie zusammen?",
            "type": "open"
        },
        {
            "id": "q3",
            "topic": "Erfolg",
            "text": "Was ist Erfolg? Wie definieren Sie Erfolg?",
            "type": "open"
        },
        {
            "id": "q4",
            "topic": "Familie",
            "text": "Was bedeutet Familie für Sie?",
            "type": "open"
        }
    ],
    "metadata": {
        "language": "de",
        "version": "1.0",
        "created": "2026-06-16"
    }
}

# 英语问卷
QUESTIONNAIRE_EN = {
    "title": "Language and Thinking (English)",
    "description": "Please answer the following questions in English",
    "questions": [
        {
            "id": "q1",
            "topic": "freedom",
            "text": "What is freedom? Explain in your own words.",
            "type": "open"
        },
        {
            "id": "q2",
            "topic": "justice",
            "text": "What is justice? What is it related to?",
            "type": "open"
        },
        {
            "id": "q3",
            "topic": "success",
            "text": "What is success? How do you define success?",
            "type": "open"
        },
        {
            "id": "q4",
            "topic": "family",
            "text": "What does family mean to you?",
            "type": "open"
        }
    ],
    "metadata": {
        "language": "en",
        "version": "1.0",
        "created": "2026-06-16"
    }
}

# 预期的认知差异
EXPECTED_DIFFERENCES = {
    "freedom": {
        "zh": ["集体", "责任", "社会", "义务"],
        "de": ["Individualität", "Selbstbestimmung", "Recht", "Wahl"],
        "en": ["Liberty", "Choice", "Opportunity", "Independence"],
        "hypothesis": "中文强调集体和责任，德语强调个体和权利，英语强调选择和机会"
    },
    "justice": {
        "zh": ["平等", "公正", "社会", "分配"],
        "de": ["Gleichheit", "Fairness", "Gesetz", "Recht"],
        "en": ["Equality", "Fairness", "Rights", "Law"],
        "hypothesis": "中文强调社会和分配，德语强调法律和权利，英语强调平等和公平"
    },
    "success": {
        "zh": ["努力", "目标", "成就", "家庭"],
        "de": ["Leistung", "Ziel", "Anerkennung", "Karriere"],
        "en": ["Achievement", "Goal", "Recognition", "Wealth"],
        "hypothesis": "中文强调努力和家庭，德语强调成就和认可，英语强调成就和财富"
    },
    "family": {
        "zh": ["孝", "责任", "归属", "传统"],
        "de": ["Heimat", "Unterstützung", "Gemeinschaft", "Bindung"],
        "en": ["Support", "Love", "Belonging", "Connection"],
        "hypothesis": "中文强调孝和传统，德语强调归属和支持，英语强调爱和联系"
    }
}


def save_questionnaires(output_dir):
    """保存问卷"""
    import json
    import os

    os.makedirs(output_dir, exist_ok=True)

    # 保存中文问卷
    filepath = os.path.join(output_dir, "questionnaire_zh.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(QUESTIONNAIRE_ZH, f, ensure_ascii=False, indent=2)
    print(f"中文问卷已保存: {filepath}")

    # 保存德语问卷
    filepath = os.path.join(output_dir, "questionnaire_de.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(QUESTIONNAIRE_DE, f, ensure_ascii=False, indent=2)
    print(f"德语问卷已保存: {filepath}")

    # 保存英语问卷
    filepath = os.path.join(output_dir, "questionnaire_en.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(QUESTIONNAIRE_EN, f, ensure_ascii=False, indent=2)
    print(f"英语问卷已保存: {filepath}")

    # 保存预期差异
    filepath = os.path.join(output_dir, "expected_differences.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(EXPECTED_DIFFERENCES, f, ensure_ascii=False, indent=2)
    print(f"预期差异已保存: {filepath}")


if __name__ == "__main__":
    print("=" * 60)
    print("LinguaGraph 问卷设计")
    print("=" * 60)

    output_dir = r"\data\questionnaires"
    save_questionnaires(output_dir)

    print("\n问卷内容:")
    print("-" * 60)

    for lang, q in [("中文", QUESTIONNAIRE_ZH), ("德语", QUESTIONNAIRE_DE), ("英语", QUESTIONNAIRE_EN)]:
        print(f"\n{lang}问卷 ({q['title']}):")
        for question in q["questions"]:
            try:
                print(f"  {question['id']}: {question['text']}")
            except UnicodeEncodeError:
                print(f"  {question['id']}: [question saved]")

    print("\n" + "=" * 60)
    print("预期认知差异:")
    print("-" * 60)

    for topic, diff in EXPECTED_DIFFERENCES.items():
        print(f"\n{topic}:")
        try:
            print(f"  中文: {diff['zh']}")
            print(f"  德语: {diff['de']}")
            print(f"  英语: {diff['en']}")
            print(f"  假设: {diff['hypothesis']}")
        except UnicodeEncodeError:
            print(f"  [differences saved]")
