"""
CognitiveSpace Pipeline v1.0

完整流程：
Student Answer → LLM → JSON → Schema校验 → 专家图谱对比 → Missing Links

这是第一个可运行的原型。
"""

import json
import os
import sys
import io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# === 配置 ===
LM_STUDIO_URL = "http://localhost:1234/v1"
MODEL_NAME = "qwen3.5-9b-uncensored-hauhaucs-aggressive"

# === Prompt v1.0 (冻结) ===
PROMPT_V1 = """你是一名认知科学研究员。

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

# === 专家图谱 v1.0 (5-8个节点) ===
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


def extract_concepts(text):
    """从学生回答中提取概念和关系"""
    try:
        from openai import OpenAI
        client = OpenAI(base_url=LM_STUDIO_URL, api_key="not-needed")

        prompt = PROMPT_V1.replace("{text}", text)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500,
            timeout=60
        )

        result = response.choices[0].message.content

        # 尝试解析JSON
        # 处理可能的Markdown代码块
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0]
        elif "```" in result:
            result = result.split("```")[1].split("```")[0]

        return json.loads(result.strip())

    except Exception as e:
        print(f"  [ERROR] 提取失败: {e}")
        return None


def validate_schema(output):
    """校验输出是否符合Schema"""
    errors = []

    if "concepts" not in output:
        errors.append("缺少concepts字段")
    elif not isinstance(output["concepts"], list):
        errors.append("concepts必须是数组")

    if "relations" not in output:
        errors.append("缺少relations字段")
    elif not isinstance(output["relations"], list):
        errors.append("relations必须是数组")

    if "missing_hints" not in output:
        errors.append("缺少missing_hints字段")
    elif not isinstance(output["missing_hints"], list):
        errors.append("missing_hints必须是数组")

    # 校验relations类型
    valid_types = ["prerequisite", "part_of", "cause_effect", "represents", "inverse_of"]
    for i, rel in enumerate(output.get("relations", [])):
        if "type" in rel and rel["type"] not in valid_types:
            errors.append(f"relations[{i}].type无效: {rel['type']}")

    return len(errors) == 0, errors


def compare_with_expert(student_output, expert_graph):
    """对比学生图谱与专家图谱，找出Missing Links"""
    missing = []

    # 提取学生概念
    student_concepts = set(student_output.get("concepts", []))

    # 提取专家概念
    expert_concepts = {c["name"] for c in expert_graph["concepts"]}

    # 找缺失概念
    missing_concepts = expert_concepts - student_concepts

    # 找缺失关系
    for rel in expert_graph["relations"]:
        # 检查关系两端是否都在学生概念中
        if rel["from"] in student_concepts and rel["to"] in student_concepts:
            # 检查学生是否有这个关系
            student_relations = student_output.get("relations", [])
            has_relation = False
            for sr in student_relations:
                if sr.get("from") == rel["from"] and sr.get("to") == rel["to"]:
                    has_relation = True
                    break

            if not has_relation:
                missing.append({
                    "from": rel["from"],
                    "to": rel["to"],
                    "type": rel["type"],
                    "reason": f"专家图谱中有此关系，但学生未表达"
                })

    return {
        "missing_concepts": list(missing_concepts),
        "missing_relations": missing,
        "coverage": len(student_concepts) / max(len(expert_concepts), 1)
    }


def run_pipeline(student_answer, language="zh"):
    """运行完整Pipeline"""
    print(f"\n{'='*60}")
    print(f"Pipeline开始")
    print(f"{'='*60}")

    print(f"\n1. 学生回答: {student_answer[:50]}...")

    # Step 1: LLM提取
    print(f"\n2. LLM提取中...")
    student_output = extract_concepts(student_answer)

    if student_output is None:
        print("  [FAIL] 提取失败")
        return None

    print(f"  概念数: {len(student_output.get('concepts', []))}")
    print(f"  关系数: {len(student_output.get('relations', []))}")
    print(f"  提示数: {len(student_output.get('missing_hints', []))}")

    # Step 2: Schema校验
    print(f"\n3. Schema校验...")
    is_valid, errors = validate_schema(student_output)

    if is_valid:
        print("  [PASS] 校验通过")
    else:
        print(f"  [FAIL] 校验失败: {errors}")

    # Step 3: 对比专家图谱
    print(f"\n4. 对比专家图谱...")
    comparison = compare_with_expert(student_output, EXPERT_GRAPH)

    print(f"  缺失概念: {comparison['missing_concepts']}")
    print(f"  缺失关系: {len(comparison['missing_relations'])}条")
    print(f"  覆盖率: {comparison['coverage']:.1%}")

    # Step 4: 生成报告
    print(f"\n5. 生成报告...")
    report = {
        "student_answer": student_answer,
        "language": language,
        "student_output": student_output,
        "schema_valid": is_valid,
        "schema_errors": errors,
        "comparison": comparison,
        "timestamp": datetime.now().isoformat()
    }

    print(f"\n{'='*60}")
    print(f"Pipeline完成")
    print(f"{'='*60}")

    return report


def save_report(report, filename):
    """保存报告"""
    output_dir = r"output"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n报告已保存: {filepath}")
    return filepath


# === 主程序 ===
if __name__ == "__main__":
    # 测试用例
    test_cases = [
        {
            "text": "我知道导数表示变化率，但不知道为什么需要极限。",
            "language": "zh"
        },
        {
            "text": "积分是导数的逆运算，可以用来求面积。",
            "language": "zh"
        }
    ]

    # 运行Pipeline
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'#'*60}")
        print(f"测试用例 {i}")
        print(f"{'#'*60}")

        report = run_pipeline(case["text"], case["language"])

        if report:
            # 保存报告
            filename = f"report_{i}.json"
            save_report(report, filename)

            # 显示关键结果
            print(f"\n关键结果:")
            print(f"  概念: {report['student_output']['concepts']}")
            print(f"  关系数: {len(report['student_output']['relations'])}")
            print(f"  缺失概念: {report['comparison']['missing_concepts']}")
            print(f"  缺失关系: {len(report['comparison']['missing_relations'])}条")
