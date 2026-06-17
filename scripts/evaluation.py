"""
CognitiveSpace 评价框架

用于评估AI提取的准确性和MCL检测的有效性
"""

import json
import os
import sys
import io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class EvaluationFramework:
    """评价框架"""

    def __init__(self):
        self.results = []

    def evaluate_single(self, student_id, ai_output, human_labels):
        """
        评估单个样本

        参数：
        - student_id: 学生ID
        - ai_output: AI提取结果
        - human_labels: 人工标注结果

        返回：
        - 评估指标字典
        """
        # Concept Precision
        ai_concepts = set(ai_output.get("concepts", []))
        human_concepts = set(human_labels.get("concepts", []))

        if len(ai_concepts) == 0:
            concept_precision = 0
        else:
            correct_concepts = ai_concepts.intersection(human_concepts)
            concept_precision = len(correct_concepts) / len(ai_concepts)

        # Concept Recall
        if len(human_concepts) == 0:
            concept_recall = 0
        else:
            concept_recall = len(correct_concepts) / len(human_concepts)

        # Relation Precision
        ai_relations = set()
        for rel in ai_output.get("relations", []):
            ai_relations.add((rel["from"], rel["to"], rel["type"]))

        human_relations = set()
        for rel in human_labels.get("relations", []):
            human_relations.add((rel["from"], rel["to"], rel["type"]))

        if len(ai_relations) == 0:
            relation_precision = 0
        else:
            correct_relations = ai_relations.intersection(human_relations)
            relation_precision = len(correct_relations) / len(ai_relations)

        # MCL Detection
        ai_missing = set()
        for hint in ai_output.get("missing_hints", []):
            ai_missing.add((hint["from"], hint["to"]))

        human_missing = set()
        for hint in human_labels.get("missing_hints", []):
            human_missing.add((hint["from"], hint["to"]))

        correct_missing = ai_missing.intersection(human_missing)

        if len(ai_missing) == 0:
            mcl_precision = 0
        else:
            mcl_precision = len(correct_missing) / len(ai_missing)

        if len(human_missing) == 0:
            mcl_recall = 0
        else:
            mcl_recall = len(correct_missing) / len(human_missing)

        # Coverage
        coverage = len(ai_concepts) / max(len(human_concepts), 1)

        result = {
            "student_id": student_id,
            "concept_precision": concept_precision,
            "concept_recall": concept_recall,
            "relation_precision": relation_precision,
            "mcl_precision": mcl_precision,
            "mcl_recall": mcl_recall,
            "coverage": coverage,
            "timestamp": datetime.now().isoformat()
        }

        self.results.append(result)
        return result

    def calculate_metrics(self):
        """计算整体指标"""
        if not self.results:
            return {}

        metrics = {
            "total_samples": len(self.results),
            "avg_concept_precision": sum(r["concept_precision"] for r in self.results) / len(self.results),
            "avg_concept_recall": sum(r["concept_recall"] for r in self.results) / len(self.results),
            "avg_relation_precision": sum(r["relation_precision"] for r in self.results) / len(self.results),
            "avg_mcl_precision": sum(r["mcl_precision"] for r in self.results) / len(self.results),
            "avg_mcl_recall": sum(r["mcl_recall"] for r in self.results) / len(self.results),
            "avg_coverage": sum(r["coverage"] for r in self.results) / len(self.results)
        }

        # F1 scores
        if metrics["avg_concept_precision"] + metrics["avg_concept_recall"] > 0:
            metrics["concept_f1"] = 2 * metrics["avg_concept_precision"] * metrics["avg_concept_recall"] / (
                metrics["avg_concept_precision"] + metrics["avg_concept_recall"]
            )
        else:
            metrics["concept_f1"] = 0

        if metrics["avg_mcl_precision"] + metrics["avg_mcl_recall"] > 0:
            metrics["mcl_f1"] = 2 * metrics["avg_mcl_precision"] * metrics["avg_mcl_recall"] / (
                metrics["avg_mcl_precision"] + metrics["avg_mcl_recall"]
            )
        else:
            metrics["mcl_f1"] = 0

        return metrics

    def save_results(self, filepath):
        """保存结果"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        data = {
            "results": self.results,
            "metrics": self.calculate_metrics(),
            "timestamp": datetime.now().isoformat()
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"结果已保存: {filepath}")


# === 测试评价框架 ===
if __name__ == "__main__":
    print("=" * 60)
    print("CognitiveSpace 评价框架测试")
    print("=" * 60)

    # 创建评价框架
    framework = EvaluationFramework()

    # 测试用例1
    ai_output_1 = {
        "concepts": ["导数", "变化率", "极限"],
        "relations": [
            {"from": "导数", "to": "变化率", "type": "represents", "confidence": 0.9, "evidence": "导数表示变化率"}
        ],
        "missing_hints": [
            {"from": "极限", "to": "导数", "reason": "学生不知道为什么需要极限"}
        ]
    }

    human_labels_1 = {
        "concepts": ["导数", "变化率", "极限"],
        "relations": [
            {"from": "导数", "to": "变化率", "type": "represents"}
        ],
        "missing_hints": [
            {"from": "极限", "to": "导数", "reason": "学生不知道为什么需要极限"}
        ]
    }

    result_1 = framework.evaluate_single("zh_001", ai_output_1, human_labels_1)
    print(f"\n测试用例1:")
    print(f"  Concept Precision: {result_1['concept_precision']:.1%}")
    print(f"  Concept Recall: {result_1['concept_recall']:.1%}")
    print(f"  Relation Precision: {result_1['relation_precision']:.1%}")
    print(f"  MCL Precision: {result_1['mcl_precision']:.1%}")
    print(f"  MCL Recall: {result_1['mcl_recall']:.1%}")
    print(f"  Coverage: {result_1['coverage']:.1%}")

    # 测试用例2
    ai_output_2 = {
        "concepts": ["导数", "积分", "面积"],
        "relations": [
            {"from": "积分", "to": "导数", "type": "inverse_of", "confidence": 0.85, "evidence": "积分是导数的逆运算"},
            {"from": "积分", "to": "面积", "type": "represents", "confidence": 0.9, "evidence": "积分可以用来求面积"}
        ],
        "missing_hints": []
    }

    human_labels_2 = {
        "concepts": ["导数", "积分", "面积", "变化率"],
        "relations": [
            {"from": "积分", "to": "导数", "type": "inverse_of"},
            {"from": "积分", "to": "面积", "type": "represents"},
            {"from": "导数", "to": "变化率", "type": "represents"}
        ],
        "missing_hints": [
            {"from": "导数", "to": "变化率", "reason": "学生未表达"}
        ]
    }

    result_2 = framework.evaluate_single("zh_002", ai_output_2, human_labels_2)
    print(f"\n测试用例2:")
    print(f"  Concept Precision: {result_2['concept_precision']:.1%}")
    print(f"  Concept Recall: {result_2['concept_recall']:.1%}")
    print(f"  Relation Precision: {result_2['relation_precision']:.1%}")
    print(f"  MCL Precision: {result_2['mcl_precision']:.1%}")
    print(f"  MCL Recall: {result_2['mcl_recall']:.1%}")
    print(f"  Coverage: {result_2['coverage']:.1%}")

    # 计算整体指标
    metrics = framework.calculate_metrics()
    print(f"\n{'='*60}")
    print("整体指标")
    print(f"{'='*60}")
    print(f"  样本数: {metrics['total_samples']}")
    print(f"  平均Concept Precision: {metrics['avg_concept_precision']:.1%}")
    print(f"  平均Concept Recall: {metrics['avg_concept_recall']:.1%}")
    print(f"  平均Relation Precision: {metrics['avg_relation_precision']:.1%}")
    print(f"  平均MCL Precision: {metrics['avg_mcl_precision']:.1%}")
    print(f"  平均MCL Recall: {metrics['avg_mcl_recall']:.1%}")
    print(f"  平均Coverage: {metrics['avg_coverage']:.1%}")
    print(f"  Concept F1: {metrics['concept_f1']:.1%}")
    print(f"  MCL F1: {metrics['mcl_f1']:.1%}")

    # 保存结果
    output_dir = r"output"
    os.makedirs(output_dir, exist_ok=True)
    framework.save_results(os.path.join(output_dir, "evaluation_results.json"))
