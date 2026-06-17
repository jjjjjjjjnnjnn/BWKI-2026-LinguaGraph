"""
Schema校验器 - 验证LLM输出是否符合标准
"""

import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 加载Schema
schema_path = r"\schema_v1.json"
with open(schema_path, 'r', encoding='utf-8') as f:
    schema = json.load(f)

def validate_output(output):
    """校验LLM输出是否符合Schema"""
    errors = []

    # 检查必需字段
    required = ["concepts", "relations", "missing_hints"]
    for field in required:
        if field not in output:
            errors.append(f"缺少必需字段: {field}")

    if errors:
        return False, errors

    # 检查concepts
    if not isinstance(output["concepts"], list):
        errors.append("concepts必须是数组")
    elif len(output["concepts"]) == 0:
        errors.append("concepts不能为空")
    else:
        for i, concept in enumerate(output["concepts"]):
            if not isinstance(concept, str):
                errors.append(f"concepts[{i}]必须是字符串")

    # 检查relations
    if not isinstance(output["relations"], list):
        errors.append("relations必须是数组")
    else:
        valid_types = ["prerequisite", "part_of", "cause_effect", "represents", "inverse_of"]
        for i, rel in enumerate(output["relations"]):
            if not isinstance(rel, dict):
                errors.append(f"relations[{i}]必须是对象")
                continue

            required_fields = ["from", "to", "type", "confidence", "evidence"]
            for field in required_fields:
                if field not in rel:
                    errors.append(f"relations[{i}]缺少字段: {field}")

            if "type" in rel and rel["type"] not in valid_types:
                errors.append(f"relations[{i}].type必须是{valid_types}之一")

            if "confidence" in rel:
                if not isinstance(rel["confidence"], (int, float)):
                    errors.append(f"relations[{i}].confidence必须是数字")
                elif not (0 <= rel["confidence"] <= 1):
                    errors.append(f"relations[{i}].confidence必须在0-1之间")

    # 检查missing_hints
    if not isinstance(output["missing_hints"], list):
        errors.append("missing_hints必须是数组")
    else:
        for i, hint in enumerate(output["missing_hints"]):
            if not isinstance(hint, dict):
                errors.append(f"missing_hints[{i}]必须是对象")
                continue

            required_fields = ["from", "to", "reason"]
            for field in required_fields:
                if field not in hint:
                    errors.append(f"missing_hints[{i}]缺少字段: {field}")

    return len(errors) == 0, errors


# 测试用例
test_outputs = [
    # 有效输出
    {
        "concepts": ["导数", "变化率", "极限"],
        "relations": [
            {
                "from": "导数",
                "to": "变化率",
                "type": "represents",
                "confidence": 0.95,
                "evidence": "导数表示变化率"
            }
        ],
        "missing_hints": [
            {
                "from": "极限",
                "to": "导数",
                "reason": "学生明确表示不知道为什么需要极限"
            }
        ]
    },
    # 无效输出 - 缺少字段
    {
        "concepts": ["导数", "变化率"]
    },
    # 无效输出 - 错误类型
    {
        "concepts": ["导数"],
        "relations": [
            {
                "from": "导数",
                "to": "变化率",
                "type": "错误类型",
                "confidence": 0.95,
                "evidence": "导数表示变化率"
            }
        ],
        "missing_hints": []
    }
]

print("=" * 60)
print("Schema校验器测试")
print("=" * 60)

for i, output in enumerate(test_outputs, 1):
    print(f"\n测试用例 {i}:")
    print(f"  输入: {json.dumps(output, ensure_ascii=False)[:100]}...")

    is_valid, errors = validate_output(output)

    if is_valid:
        print(f"  结果: ✓ 有效")
    else:
        print(f"  结果: ✗ 无效")
        for error in errors:
            print(f"    - {error}")

print("\n" + "=" * 60)
print("Schema校验器已准备就绪")
print("=" * 60)
