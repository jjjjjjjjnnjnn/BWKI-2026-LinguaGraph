"""
build_china_curriculum.py — 基于已知结构构建中国数学课标概念图谱

数据源：
- 义务教育数学课程标准（2022年版）：第一~四学段
- 普通高中数学课程标准（2017年版2020年修订）

课标结构（已知）：
义务教育 (1-9年级):
  第一学段 (1-2): 数与代数、图形与几何、统计与概率
  第二学段 (3-4): 数与代数、图形与几何、统计与概率
  第三学段 (5-6): 数与代数、图形与几何、统计与概率、综合与实践
  第四学段 (7-9): 数与代数、图形与几何、统计与概率、综合与实践

高中 (10-12):
  必修: 函数、几何与代数、统计与概率、数学建模与数学探究
  选择性必修: 函数进阶、几何进阶、计数原理与概率统计
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "config" / "expert_graphs"

# ── 义务教育阶段 (1-9年级) ────────────────────────────────────────────────

COMPULSORY_STAGES = {
    "cn_grade_1_2": {"grades": "1-2", "level": "elementary", "label": "第一学段 (1-2年级)"},
    "cn_grade_3_4": {"grades": "3-4", "level": "elementary", "label": "第二学段 (3-4年级)"},
    "cn_grade_5_6": {"grades": "5-6", "level": "middle",     "label": "第三学段 (5-6年级)"},
    "cn_grade_7_9": {"grades": "7-9", "level": "middle",     "label": "第四学段 (7-9年级)"},
}

# 第一学段 (1-2年级)
COMPULSORY_TOPICS = {
    "cn_grade_1_2": {
        "Num": [
            "认识万以内的数", "整数四则混合运算", "万以内加减法",
            "表内乘法", "简单的除法", "长度单位（厘米、米）",
            "质量单位（克、千克）", "时间单位（时、分、秒）",
            "简单的数据收集和整理", "人民币的认识和简单计算",
        ],
        "Geo": [
            "认识平面图形（长方形、正方形、三角形、圆）",
            "认识立体图形（长方体、正方体、圆柱、球）",
            "图形的拼组", "位置与方向（上下、前后、左右）",
            "简单的测量（长度、周长）",
        ],
        "Sta": [
            "简单的分类和整理", "认识象形统计图和条形统计图",
            "简单的数据分析",
        ],
    },
    "cn_grade_3_4": {
        "Num": [
            "万以内数的认识", "三位数乘一位数", "两位数除以一位数",
            "简单的分数（几分之一、几分之几）", "小数的初步认识",
            "面积单位（平方厘米、平方分米、平方米）",
            "时间计算（时分秒的换算）",
            "估算", "混合运算",
        ],
        "Geo": [
            "角的认识（锐角、直角、钝角）", "平行与垂直",
            "长方形和正方形的特征", "周长和面积的计算",
            "对称图形", "平移和旋转",
        ],
        "Sta": [
            "数据的收集和整理", "条形统计图",
            "简单的平均数", "可能性（确定事件、不确定事件）",
        ],
    },
    "cn_grade_5_6": {
        "Num": [
            "大数的认识（亿以内）", "小数的意义和性质",
            "小数的四则运算", "分数的意义和性质",
            "分数的加减法", "分数的乘除法",
            "百分数的认识", "比和比例",
            "负数的认识", "方程（用字母表示数、简单方程）",
            "因数与倍数", "质数与合数",
        ],
        "Geo": [
            "图形的运动（轴对称、平移、旋转）",
            "平行四边形和梯形的面积", "三角形的面积",
            "圆的周长和面积", "圆柱和圆锥的体积",
            "观察物体（从不同方向观察）", "图形的放大与缩小",
            "比例尺",
        ],
        "Sta": [
            "折线统计图", "扇形统计图",
            "平均数和中位数", "众数",
            "可能性的大小", "概率的初步认识",
        ],
    },
    "cn_grade_7_9": {
        "Num": [
            "有理数及其运算", "整式的加减",
            "一元一次方程", "二元一次方程组",
            "一元一次不等式", "实数",
            "二次根式", "一元二次方程",
            "分式", "因式分解",
        ],
        "Geo": [
            "线段、射线、直线", "角的度量",
            "相交线与平行线", "三角形（全等、相似）",
            "四边形（平行四边形、矩形、菱形、正方形）",
            "圆（弧、弦、圆心角、圆周角）",
            "图形的旋转与对称", "勾股定理",
            "锐角三角函数", "投影与视图",
        ],
        "Sta": [
            "数据的收集、整理与描述",
            "数据的分析（平均数、中位数、众数、方差）",
            "概率（等可能事件的概率）",
            "频率与概率",
        ],
    },
}

# ── 高中阶段 (10-12年级) ─────────────────────────────────────────────────

SENIOR_HIGH_STAGES = {
    "cn_grade_10_12": {"grades": "10-12", "level": "high", "label": "普通高中 (10-12年级)"},
}

SENIOR_HIGH_TOPICS = {
    "cn_grade_10_12": {
        "Num": [
            "集合与常用逻辑用语", "不等式",
            "函数的概念与性质", "指数函数", "对数函数",
            "幂函数", "三角函数（正弦、余弦、正切）",
            "三角恒等变换", "数列（等差数列、等比数列）",
            "向量（平面向量、空间向量）",
            "复数", "排列组合与二项式定理",
        ],
        "Alg": [
            "直线与方程", "圆与方程",
            "圆锥曲线（椭圆、双曲线、抛物线）",
            "导数及其应用", "定积分",
            "推理与证明", "数学归纳法",
        ],
        "Geo": [
            "空间几何体（棱柱、棱锥、球）",
            "点、线、面之间的位置关系",
            "空间向量与立体几何",
            "平面解析几何（坐标系、直线、圆、圆锥曲线）",
        ],
        "Sta": [
            "随机抽样", "用样本估计总体",
            "变量间的相关关系", "回归分析",
            "古典概型", "几何概型",
            "条件概率与独立事件", "离散型随机变量",
            "二项分布", "正态分布",
        ],
    },
}


def build_graph(stages_def, topics_def, country, source_doc):
    """Build concept graph from stages and topics."""
    concepts = []
    
    domains = {
        "Num": {"zh": "数与代数", "en": "Number and Algebra", "de": "Zahlen und Algebra"},
        "Alg": {"zh": "代数与几何", "en": "Algebra and Geometry", "de": "Algebra und Geometrie"},
        "Geo": {"zh": "图形与几何", "en": "Shapes and Geometry", "de": "Formen und Geometrie"},
        "Sta": {"zh": "统计与概率", "en": "Statistics and Probability", "de": "Statistik und Wahrscheinlichkeit"},
    }
    
    for stage_key, stage_info in stages_def.items():
        stage_topics = topics_def.get(stage_key, {})
        
        for field_key, topics in stage_topics.items():
            domain_info = domains.get(field_key, {})
            
            for topic in topics:
                clean = topic.strip()
                if not clean:
                    continue
                
                # Generate stable name
                import re
                name_part = re.sub(r'[^\u4e00-\u9fff\w]', '', clean)[:30]
                concept_name = f"curriculum_{country}_{field_key}_{stage_key}_{name_part}"
                
                concepts.append({
                    "name": concept_name,
                    "display_name": clean,
                    "category": "concept",
                    "level": stage_info["level"],
                    "labels": {
                        "zh": clean,
                        "en": domain_info.get("en", field_key),
                        "de": domain_info.get("de", field_key),
                    },
                    "source": source_doc,
                    "stage": stage_key,
                    "stage_label": stage_info["label"],
                    "domain": field_key,
                    "domain_zh": domain_info.get("zh", field_key),
                })
    
    # Relations: earlier stages → later stages
    relations = []
    grouped = {}
    for c in concepts:
        key = (c["stage"], c["domain"])
        grouped.setdefault(key, []).append(c)
    
    stage_order = list(stages_def.keys())
    for field_key in domains:
        prev = []
        for sk in stage_order:
            curr = grouped.get((sk, field_key), [])
            for pc in prev:
                for cc in curr:
                    relations.append({
                        "source": pc["name"],
                        "target": cc["name"],
                        "type": "prerequisite",
                        "relation": "prerequisite",
                    })
            prev.extend(curr)
    
    return {
        "version": "2.0",
        "domain": f"curriculum_{country}_math",
        "description": f"中国数学课程标准 — {'义务教育 (2022)' if country == 'cn' else '高中 (2017)'}",
        "languages": ["zh", "en", "de"],
        "concepts": concepts,
        "relations": relations,
        "metadata": {
            "total_concepts": len(concepts),
            "total_relations": len(relations),
            "source_documents": [source_doc],
        },
    }


def main():
    print("=" * 60)
    print("Building China Curriculum Graphs")
    print("=" * 60)
    
    # 义务教育
    print("\n[1/2] 义务教育数学课程标准 (2022)...")
    cn_compulsory = build_graph(
        COMPULSORY_STAGES, COMPULSORY_TOPICS, "cn",
        "义务教育数学课程标准（2022年版）"
    )
    out1 = OUTPUT_DIR / "curriculum_cn_compulsory_math.json"
    with open(out1, 'w', encoding='utf-8') as f:
        json.dump(cn_compulsory, f, ensure_ascii=False, indent=2)
    print(f"  Concepts: {cn_compulsory['metadata']['total_concepts']}")
    print(f"  Relations: {cn_compulsory['metadata']['total_relations']}")
    print(f"  Written: {out1}")
    
    # 高中
    print("\n[2/2] 普通高中数学课程标准 (2017)...")
    cn_senior = build_graph(
        SENIOR_HIGH_STAGES, SENIOR_HIGH_TOPICS, "cn",
        "普通高中数学课程标准（2017年版2020年修订）"
    )
    out2 = OUTPUT_DIR / "curriculum_cn_senior_math.json"
    with open(out2, 'w', encoding='utf-8') as f:
        json.dump(cn_senior, f, ensure_ascii=False, indent=2)
    print(f"  Concepts: {cn_senior['metadata']['total_concepts']}")
    print(f"  Relations: {cn_senior['metadata']['total_relations']}")
    print(f"  Written: {out2}")
    
    # 合并为统一中国课标图谱
    print("\n[Merging] Combining into curriculum_cn_math.json...")
    all_concepts = cn_compulsory["concepts"] + cn_senior["concepts"]
    all_relations = cn_compulsory["relations"] + cn_senior["relations"]
    
    cn_combined = {
        "version": "2.0",
        "domain": "curriculum_cn_math",
        "description": "中国数学课程标准 — 义务教育 (2022) + 高中 (2017)",
        "languages": ["zh", "en", "de"],
        "concepts": all_concepts,
        "relations": all_relations,
        "metadata": {
            "total_concepts": len(all_concepts),
            "total_relations": len(all_relations),
            "source_documents": [
                "义务教育数学课程标准（2022年版）",
                "普通高中数学课程标准（2017年版2020年修订）",
            ],
        },
    }
    
    out3 = OUTPUT_DIR / "curriculum_cn_math.json"
    with open(out3, 'w', encoding='utf-8') as f:
        json.dump(cn_combined, f, ensure_ascii=False, indent=2)
    print(f"  Total: {cn_combined['metadata']['total_concepts']} concepts, {cn_combined['metadata']['total_relations']} relations")
    print(f"  Written: {out3}")
    
    print(f"\n{'='*60}")
    print("DONE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
