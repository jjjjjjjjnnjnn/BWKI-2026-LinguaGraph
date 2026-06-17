"""
LinguaGraph 社会议题专家图谱 v1.0

用于研究语言对思维的影响
"""

# 社会议题核心概念（中德英对照）
SOCIAL_ISSUES_CONCEPTS = [
    # 自由
    {"id": "S001", "zh": "自由", "de": "Freiheit", "en": "Freedom", "category": "concept"},
    {"id": "S002", "zh": "个体", "de": "Individuum", "en": "Individual", "category": "entity"},
    {"id": "S003", "zh": "权利", "de": "Recht", "en": "Right", "category": "concept"},
    {"id": "S004", "zh": "选择", "de": "Entscheidung", "en": "Choice", "category": "action"},
    {"id": "S005", "zh": "责任", "de": "Verantwortung", "en": "Responsibility", "category": "concept"},

    # 公平
    {"id": "S006", "zh": "公平", "de": "Gerechtigkeit", "en": "Justice", "category": "concept"},
    {"id": "S007", "zh": "平等", "de": "Gleichheit", "en": "Equality", "category": "concept"},
    {"id": "S008", "zh": "机会", "de": "Chance", "en": "Opportunity", "category": "concept"},
    {"id": "S009", "zh": "分配", "de": "Verteilung", "en": "Distribution", "category": "action"},

    # 成功
    {"id": "S010", "zh": "成功", "de": "Erfolg", "en": "Success", "category": "concept"},
    {"id": "S011", "zh": "目标", "de": "Ziel", "en": "Goal", "category": "entity"},
    {"id": "S012", "zh": "努力", "de": "Anstrengung", "en": "Effort", "category": "action"},
    {"id": "S013", "zh": "成就", "de": "Leistung", "en": "Achievement", "category": "concept"},

    # 家庭
    {"id": "S014", "zh": "家庭", "de": "Familie", "en": "Family", "category": "entity"},
    {"id": "S015", "zh": "孝", "de": " Pietät", "en": "Filial Piety", "category": "concept"},
    {"id": "S016", "zh": "Heimat", "de": "Heimat", "en": "Home", "category": "concept"},
    {"id": "S017", "zh": "归属", "de": "Zugehörigkeit", "en": "Belonging", "category": "concept"},
]

# 社会议题核心关系
SOCIAL_ISSUES_RELATIONS = [
    # 自由关系
    {"from": "S001", "to": "S002", "type": "part_of", "importance": 0.9, "description": "自由属于个体"},
    {"from": "S001", "to": "S003", "type": "part_of", "importance": 0.85, "description": "自由是权利"},
    {"from": "S001", "to": "S004", "type": "part_of", "importance": 0.8, "description": "自由是选择"},
    {"from": "S001", "to": "S005", "type": "cause_effect", "importance": 0.85, "description": "自由带来责任"},

    # 公平关系
    {"from": "S006", "to": "S007", "type": "part_of", "importance": 0.9, "description": "公平包含平等"},
    {"from": "S006", "to": "S008", "type": "cause_effect", "importance": 0.85, "description": "公平带来机会"},
    {"from": "S006", "to": "S009", "type": "part_of", "importance": 0.8, "description": "公平涉及分配"},

    # 成功关系
    {"from": "S010", "to": "S011", "type": "cause_effect", "importance": 0.9, "description": "成功需要目标"},
    {"from": "S010", "to": "S012", "type": "cause_effect", "importance": 0.85, "description": "成功需要努力"},
    {"from": "S010", "to": "S013", "type": "part_of", "importance": 0.8, "description": "成功包含成就"},

    # 家庭关系
    {"from": "S014", "to": "S015", "type": "part_of", "importance": 0.9, "description": "家庭包含孝"},
    {"from": "S014", "to": "S016", "type": "part_of", "importance": 0.85, "description": "家庭是Heimat"},
    {"from": "S014", "to": "S017", "type": "cause_effect", "importance": 0.8, "description": "家庭带来归属"},

    # 跨主题关系
    {"from": "S001", "to": "S005", "type": "cause_effect", "importance": 0.85, "description": "自由与责任相关"},
    {"from": "S006", "to": "S001", "type": "applies_to", "importance": 0.8, "description": "公平应用于自由"},
    {"from": "S010", "to": "S008", "type": "cause_effect", "importance": 0.85, "description": "成功需要机会"},
]


def create_social_issues_graph():
    """创建社会议题专家图谱"""
    graph = {
        "version": "1.0",
        "domain": "social_issues",
        "description": "社会议题认知图谱，用于研究语言对思维的影响",
        "concepts": SOCIAL_ISSUES_CONCEPTS,
        "relations": SOCIAL_ISSUES_RELATIONS,
        "metadata": {
            "total_concepts": len(SOCIAL_ISSUES_CONCEPTS),
            "total_relations": len(SOCIAL_ISSUES_RELATIONS),
            "languages": ["zh", "de", "en"],
            "created": "2026-06-16"
        }
    }
    return graph


# 专家图谱
SOCIAL_ISSUES_GRAPH = create_social_issues_graph()


if __name__ == "__main__":
    import json
    import os

    print("=" * 60)
    print("LinguaGraph 社会议题专家图谱 v1.0")
    print("=" * 60)

    # 保存图谱
    output_dir = r"\expert_graph"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, "social_issues_graph.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(SOCIAL_ISSUES_GRAPH, f, ensure_ascii=False, indent=2)

    print(f"\n专家图谱已保存: {filepath}")

    # 显示统计
    print(f"\n统计:")
    print(f"  概念数: {len(SOCIAL_ISSUES_CONCEPTS)}")
    print(f"  关系数: {len(SOCIAL_ISSUES_RELATIONS)}")
    print(f"  语言: 中文、德语、英语")

    # 显示概念
    print(f"\n概念列表:")
    for c in SOCIAL_ISSUES_CONCEPTS:
        try:
            print(f"  {c['id']}: {c['zh']} / {c['de']} / {c['en']}")
        except UnicodeEncodeError:
            print(f"  {c['id']}: [concept saved]")

    # 显示关系
    print(f"\n关系列表:")
    for r in SOCIAL_ISSUES_RELATIONS:
        try:
            print(f"  {r['from']} -> {r['to']} ({r['type']}): {r['description']}")
        except UnicodeEncodeError:
            print(f"  {r['from']} -> {r['to']} ({r['type']})")
