"""
Pipeline v1.0 - Mock测试版（不需要LLM）

验证完整流程：提取 → 校验 → 对比 → 缺失检测
"""

import json
import os
import sys
import io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# === 专家图谱 v1.0 ===
EXPERT_GRAPH = {
    "domain": "calculus",
    "version": "1.0",
    "concepts": [
        {"name": "极限", "name_de": "Grenzwert", "name_en": "limit"},
        {"name": "导数定义", "name_de": "Ableitungsdefinition", "name_en": "derivative definition"},
        {"name": "导数", "name_de": "Ableitung", "name_en": "derivative"},
        {"name": "变化率", "name_de": "Änderungsrate", "name_en": "rate of change"},
        {"name": "切线斜率", "name_de": "Tangentenneigung", "name_en": "tangent slope"},
        {"name": "积分", "name_de": "Integral", "name_en": "integral"},
        {"name": "面积", "name_de": "Fläche", "name_en": "area"}
    ],
    "relations": [
        {"from": "极限", "to": "导数定义", "type": "prerequisite"},
        {"from": "导数定义", "to": "导数", "type": "part_of"},
        {"from": "导数", "to": "变化率", "type": "represents"},
        {"from": "导数", "to": "切线斜率", "type": "represents"},
        {"from": "积分", "to": "导数", "type": "inverse_of"},
        {"from": "积分", "to": "面积", "type": "represents"}
    ]
}


def mock_extract(text):
    """Mock提取 - 模拟LLM输出"""
    # 简单的关键词匹配
    concepts = []
    relations = []
    missing_hints = []

    # 检测概念
    concept_map = {
        "导数": ["导数", "Ableitung", "derivative"],
        "变化率": ["变化率", "Änderungsrate", "rate of change"],
        "极限": ["极限", "Grenzwert", "limit"],
        "积分": ["积分", "Integral", "integration"],
        "面积": ["面积", "Fläche", "area"],
        "链式法则": ["链式法则", "Kettenregel", "chain rule"],
        "连续": ["连续", "stetig", "continuous"]
    }

    for concept, keywords in concept_map.items():
        for kw in keywords:
            if kw in text:
                concepts.append(concept)
                break

    # 添加关系
    if "导数" in concepts and "变化率" in concepts:
        relations.append({
            "from": "导数",
            "to": "变化率",
            "type": "represents",
            "confidence": 0.9,
            "evidence": "导数表示变化率"
        })

    if "积分" in concepts and "导数" in concepts:
        relations.append({
            "from": "积分",
            "to": "导数",
            "type": "inverse_of",
            "confidence": 0.85,
            "evidence": "积分是导数的逆运算"
        })

    # 检测缺失提示
    if "不知道" in text or "不理解" in text or "nicht" in text or "don't" in text:
        if "极限" in text or "Grenzwert" in text or "limit" in text:
            missing_hints.append({
                "from": "极限",
                "to": "导数",
                "reason": "学生明确表示不知道为什么需要极限"
            })

    return {
        "concepts": concepts,
        "relations": relations,
        "missing_hints": missing_hints
    }


def validate_schema(output):
    """校验Schema"""
    errors = []

    if "concepts" not in output or not isinstance(output["concepts"], list):
        errors.append("concepts无效")
    if "relations" not in output or not isinstance(output["relations"], list):
        errors.append("relations无效")
    if "missing_hints" not in output or not isinstance(output["missing_hints"], list):
        errors.append("missing_hints无效")

    valid_types = ["prerequisite", "part_of", "cause_effect", "represents", "inverse_of"]
    for i, rel in enumerate(output.get("relations", [])):
        if "type" in rel and rel["type"] not in valid_types:
            errors.append(f"relations[{i}].type无效")

    return len(errors) == 0, errors


def compare_with_expert(student_output, expert_graph):
    """对比学生图谱与专家图谱"""
    missing = []

    student_concepts = set(student_output.get("concepts", []))
    expert_concepts = {c["name"] for c in expert_graph["concepts"]}

    missing_concepts = expert_concepts - student_concepts

    for rel in expert_graph["relations"]:
        if rel["from"] in student_concepts and rel["to"] in student_concepts:
            student_relations = student_output.get("relations", [])
            has_relation = any(
                sr.get("from") == rel["from"] and sr.get("to") == rel["to"]
                for sr in student_relations
            )
            if not has_relation:
                missing.append({
                    "from": rel["from"],
                    "to": rel["to"],
                    "type": rel["type"],
                    "reason": "专家图谱中有此关系，但学生未表达"
                })

    return {
        "missing_concepts": list(missing_concepts),
        "missing_relations": missing,
        "coverage": len(student_concepts) / max(len(expert_concepts), 1)
    }


def run_pipeline(student_answer, language="zh"):
    """运行Pipeline"""
    print(f"\n{'='*60}")
    print(f"Pipeline开始")
    print(f"{'='*60}")

    print(f"\n1. 学生回答: {student_answer}")

    # Step 1: 提取
    print(f"\n2. 提取概念...")
    student_output = mock_extract(student_answer)

    print(f"  概念: {student_output['concepts']}")
    print(f"  关系: {len(student_output['relations'])}条")
    print(f"  提示: {len(student_output['missing_hints'])}条")

    # Step 2: 校验
    print(f"\n3. Schema校验...")
    is_valid, errors = validate_schema(student_output)
    print(f"  {'✓ 通过' if is_valid else '✗ 失败'}")

    # Step 3: 对比
    print(f"\n4. 对比专家图谱...")
    comparison = compare_with_expert(student_output, EXPERT_GRAPH)

    print(f"  缺失概念: {comparison['missing_concepts']}")
    print(f"  缺失关系: {len(comparison['missing_relations'])}条")
    for rel in comparison['missing_relations']:
        print(f"    - {rel['from']} → {rel['to']} ({rel['type']})")
    print(f"  覆盖率: {comparison['coverage']:.1%}")

    print(f"\n{'='*60}")
    print(f"Pipeline完成")
    print(f"{'='*60}")

    return {
        "student_answer": student_answer,
        "language": language,
        "student_output": student_output,
        "schema_valid": is_valid,
        "comparison": comparison
    }


# === 主程序 ===
if __name__ == "__main__":
    print("=" * 60)
    print("CognitiveSpace Pipeline v1.0 - Mock测试")
    print("=" * 60)

    # 测试用例
    test_cases = [
        {"text": "我知道导数表示变化率，但不知道为什么需要极限。", "lang": "zh"},
        {"text": "积分是导数的逆运算，可以用来求面积。", "lang": "zh"},
        {"text": "Die Ableitung beschreibt die Änderungsrate.", "lang": "de"},
        {"text": "I understand derivatives represent rate of change.", "lang": "en"},
    ]

    # 运行测试
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'#'*60}")
        print(f"测试用例 {i} ({case['lang']})")
        print(f"{'#'*60}")

        report = run_pipeline(case["text"], case["lang"])

    # 保存专家图谱
    output_dir = r"output"
    os.makedirs(output_dir, exist_ok=True)

    expert_path = os.path.join(output_dir, "expert_graph_v1.json")
    with open(expert_path, 'w', encoding='utf-8') as f:
        json.dump(EXPERT_GRAPH, f, ensure_ascii=False, indent=2)

    print(f"\n专家图谱已保存: {expert_path}")
