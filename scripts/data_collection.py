"""
CognitiveSpace 数据采集流程

收集学生回答，标注来源，符合比赛要求
"""

import json
import os
import sys
import io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class DataCollector:
    """数据采集器"""

    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_consent_form(self):
        """创建知情同意书模板"""
        consent = """# 知情同意书

## 项目信息
- 项目名称：CognitiveSpace - 跨语言认知断裂研究
- 研究目的：探索语言切换如何影响知识结构
- 参与者：在德国学习微积分的国际学生

## 数据用途
- 仅用于学术研究
- 数据匿名化处理
- 不会公开个人信息

## 参与者权利
- 随时退出
- 要求删除数据
- 了解研究结果

## 签名
- 参与者签名：________________
- 日期：________________
"""
        filepath = os.path.join(self.output_dir, "consent_form.md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(consent)
        print(f"知情同意书已创建: {filepath}")

    def create_questionnaire_zh(self):
        """创建中文问卷"""
        questionnaire = {
            "title": "微积分学习情况调查（中文版）",
            "description": "请根据你的理解回答以下问题",
            "questions": [
                {
                    "id": "q1",
                    "text": "什么是导数？用自己的话解释。",
                    "type": "open"
                },
                {
                    "id": "q2",
                    "text": "什么是积分？它和导数有什么关系？",
                    "type": "open"
                },
                {
                    "id": "q3",
                    "text": "什么是极限？为什么重要？",
                    "type": "open"
                },
                {
                    "id": "q4",
                    "text": "什么是连续性？它和极限有什么关系？",
                    "type": "open"
                },
                {
                    "id": "q5",
                    "text": "你在微积分学习中遇到的最大困难是什么？",
                    "type": "open"
                }
            ],
            "metadata": {
                "language": "zh",
                "version": "1.0",
                "created": datetime.now().isoformat()
            }
        }

        filepath = os.path.join(self.output_dir, "questionnaire_zh.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(questionnaire, f, ensure_ascii=False, indent=2)
        print(f"中文问卷已创建: {filepath}")

    def create_questionnaire_de(self):
        """创建德语问卷"""
        questionnaire = {
            "title": "Umfrage zum Analysis-Lernen (Deutsch)",
            "description": "Bitte beantworten Sie die folgenden Fragen basierend auf Ihrem Verständnis",
            "questions": [
                {
                    "id": "q1",
                    "text": "Was ist eine Ableitung? Erklären Sie mit eigenen Worten.",
                    "type": "open"
                },
                {
                    "id": "q2",
                    "text": "Was ist ein Integral? Wie hängt es mit der Ableitung zusammen?",
                    "type": "open"
                },
                {
                    "id": "q3",
                    "text": "Was ist ein Grenzwert? Warum ist er wichtig?",
                    "type": "open"
                },
                {
                    "id": "q4",
                    "text": "Was ist Stetigkeit? Wie hängt sie mit dem Grenzwert zusammen?",
                    "type": "open"
                },
                {
                    "id": "q5",
                    "text": "Was ist Ihre größte Schwierigkeit beim Lernen von Analysis?",
                    "type": "open"
                }
            ],
            "metadata": {
                "language": "de",
                "version": "1.0",
                "created": datetime.now().isoformat()
            }
        }

        filepath = os.path.join(self.output_dir, "questionnaire_de.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(questionnaire, f, ensure_ascii=False, indent=2)
        print(f"德语问卷已创建: {filepath}")

    def create_questionnaire_en(self):
        """创建英语问卷"""
        questionnaire = {
            "title": "Calculus Learning Survey (English)",
            "description": "Please answer the following questions based on your understanding",
            "questions": [
                {
                    "id": "q1",
                    "text": "What is a derivative? Explain in your own words.",
                    "type": "open"
                },
                {
                    "id": "q2",
                    "text": "What is an integral? How does it relate to derivatives?",
                    "type": "open"
                },
                {
                    "id": "q3",
                    "text": "What is a limit? Why is it important?",
                    "type": "open"
                },
                {
                    "id": "q4",
                    "text": "What is continuity? How does it relate to limits?",
                    "type": "open"
                },
                {
                    "id": "q5",
                    "text": "What is your biggest difficulty in learning calculus?",
                    "type": "open"
                }
            ],
            "metadata": {
                "language": "en",
                "version": "1.0",
                "created": datetime.now().isoformat()
            }
        }

        filepath = os.path.join(self.output_dir, "questionnaire_en.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(questionnaire, f, ensure_ascii=False, indent=2)
        print(f"英语问卷已创建: {filepath}")

    def save_student_response(self, student_id, language, responses, source):
        """
        保存学生回答

        参数：
        - student_id: 学生ID（匿名）
        - language: 语言
        - responses: 回答内容
        - source: 数据来源
        """
        response = {
            "student_id": student_id,
            "language": language,
            "responses": responses,
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "consent": True
        }

        filepath = os.path.join(self.output_dir, f"{student_id}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=2)

        print(f"学生回答已保存: {filepath}")
        return filepath

    def create_data_manifest(self):
        """创建数据清单"""
        manifest = {
            "project": "CognitiveSpace",
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "data_sources": [
                {
                    "name": "自采数据",
                    "description": "通过问卷收集的学生回答",
                    "language": ["zh", "de", "en"],
                    "target_count": 60
                }
            ],
            "ethical_approval": {
                "status": "pending",
                "note": "需要学校审批"
            },
            "files": []
        }

        # 扫描已有的数据文件
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.json') and filename.startswith('student_'):
                manifest["files"].append(filename)

        filepath = os.path.join(self.output_dir, "data_manifest.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        print(f"数据清单已创建: {filepath}")


# === 主程序 ===
if __name__ == "__main__":
    print("=" * 60)
    print("CognitiveSpace 数据采集流程")
    print("=" * 60)

    # 创建数据采集器
    output_dir = r"\data"
    collector = DataCollector(output_dir)

    # 创建知情同意书
    print("\n1. 创建知情同意书...")
    collector.create_consent_form()

    # 创建问卷
    print("\n2. 创建问卷...")
    collector.create_questionnaire_zh()
    collector.create_questionnaire_de()
    collector.create_questionnaire_en()

    # 示例：保存学生回答
    print("\n3. 示例：保存学生回答...")
    sample_responses = {
        "q1": "导数表示函数的变化率。",
        "q2": "积分是导数的逆运算。",
        "q3": "极限是函数趋近的值。",
        "q4": "连续函数是图像不断开的函数。",
        "q5": "最大的困难是不理解为什么需要极限。"
    }
    collector.save_student_response(
        student_id="student_001",
        language="zh",
        responses=sample_responses,
        source="问卷调查"
    )

    # 创建数据清单
    print("\n4. 创建数据清单...")
    collector.create_data_manifest()

    print("\n" + "=" * 60)
    print("数据采集流程已准备就绪")
    print("=" * 60)
