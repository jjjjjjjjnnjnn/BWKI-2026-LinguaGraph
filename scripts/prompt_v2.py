"""
Phase 0 - 升级版Prompt测试

目标：打磨Prompt，稳定输出高质量JSON
"""

# 升级版Prompt - 角色定义 + 输出Schema固定

PROMPT_V2 = """你是一名认知科学研究员。

你的任务不是总结文本，而是估计学生脑中的知识结构。

对于下面的学生回答：

1. 提取出现的核心概念（concepts）
2. 提取学生明确表达的概念关系（relations）
3. 如果学生暴露出某个概念连接缺失，请放入 missing_hints
4. 不要推测没有依据的关系
5. confidence 为 0~1
6. 只输出合法 JSON，不输出 Markdown，不输出解释

relation.type 只能使用：
- prerequisite
- part_of
- cause_effect
- represents
- inverse_of

输出格式（严格遵守）：
{
  "concepts": ["概念1", "概念2", "概念3"],
  "relations": [
    {
      "from": "概念1",
      "to": "概念2",
      "type": "represents",
      "confidence": 0.95,
      "evidence": "学生原话"
    }
  ],
  "missing_hints": [
    {
      "from": "概念A",
      "to": "概念B",
      "reason": "学生明确表示不知道..."
    }
  ]
}

学生回答：
{text}"""

# 测试用例
TEST_CASES = [
    {
        "text": "我知道导数表示变化率，但不知道为什么需要极限。",
        "expected_concepts": ["导数", "变化率", "极限"],
        "expected_relations": 1,
        "expected_hints": 1
    },
    {
        "text": "积分是导数的逆运算，可以用来求面积。",
        "expected_concepts": ["积分", "导数", "面积"],
        "expected_relations": 2,
        "expected_hints": 0
    },
    {
        "text": "Die Ableitung beschreibt die Änderungsrate, aber ich verstehe nicht, warum man den Grenzwert braucht.",
        "expected_concepts": ["Ableitung", "Änderungsrate", "Grenzwert"],
        "expected_relations": 1,
        "expected_hints": 1
    }
]

print("=" * 60)
print("Phase 0 - 升级版Prompt")
print("=" * 60)

print("\nPrompt模板：")
print("-" * 60)
print(PROMPT_V2[:500] + "...")
print("-" * 60)

print("\n测试用例：")
for i, case in enumerate(TEST_CASES, 1):
    print(f"\n用例{i}: {case['text']}")
    print(f"  预期概念: {case['expected_concepts']}")
    print(f"  预期关系数: {case['expected_relations']}")
    print(f"  预期提示数: {case['expected_hints']}")

print("\n" + "=" * 60)
print("下一步：")
print("1. 把Prompt复制到ChatGPT网页测试")
print("2. 检查输出是否符合Schema")
print("3. 调整Prompt直到稳定")
print("=" * 60)
