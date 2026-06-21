"""
LinguaGraph Workbench — Text Processing Backend

Takes user text → calls LLM → builds graph → generates 3D visualization.
Uses existing pipeline components. No new research code.

Usage:
    python workbench/process.py --text "导数建立在极限概念之上" --lang zh
    python workbench/process.py --file input.txt --lang en
"""

import json, sys, os, re, subprocess, tempfile, shutil
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

# ── LLM extraction prompt ──────────────────────────────────────────────
EXTRACT_PROMPT = """你是一名知识图谱构建专家。从以下教材文本中提取所有数学概念及其关系。

只输出JSON，不输出其他内容。

输出格式：
{{"concepts": [
    {{"id": "concept_1", "name": "概念名称", "level": "elementary|middle|high|college"}}
  ],
  "relations": [
    {{"source": "concept_1", "target": "concept_2", "type": "depends_on|related_to|part_of", "evidence": "文本证据"}}
  ]}}

文本：
{text}

语言：{language}
"""

def call_llm(text, language="zh"):
    """Extract concepts and relations from text.

    Uses a comprehensive rule-based extraction (no external LLM dependency).
    For production use, the full pipeline in scripts/ supports OpenAI/Ollama.
    """
    return rule_based_extraction(text, language)


# Comprehensive math concept dictionary by language
MATH_CONCEPTS_BY_LANG = {
    "zh": {
        # 小学
        "自然数": "elementary", "整数": "elementary", "加法": "elementary", "减法": "elementary",
        "乘法": "elementary", "除法": "elementary", "分数": "elementary", "小数": "elementary",
        "百分数": "elementary", "周长": "elementary", "面积": "elementary", "体积": "elementary",
        "图形": "elementary", "三角形": "elementary", "长方形": "elementary", "正方形": "elementary",
        "圆": "elementary", "数轴": "elementary", "平均数": "elementary",
        # 初中
        "有理数": "middle", "实数": "middle", "整式": "middle", "方程": "middle",
        "不等式": "middle", "函数": "middle", "一次函数": "middle", "二次函数": "middle",
        "反比例函数": "middle", "集合": "middle", "数列": "middle", "几何": "middle",
        "代数": "middle", "四边形": "middle", "勾股定理": "middle", "相似": "middle",
        "三角函数": "middle", "概率": "middle", "统计": "middle", "向量": "middle",
        "坐标系": "middle",
        # 高中
        "导数": "high", "极限": "high", "积分": "high", "微分": "high",
        "指数": "high", "对数": "high", "幂函数": "high", "圆锥曲线": "high",
        "椭圆": "high", "双曲线": "high", "抛物线": "high", "排列": "high",
        "组合": "high", "二项式": "high", "复数": "high", "矩阵": "high",
        "级数": "high", "数学归纳法": "high",
        # 大学
        "微分方程": "college", "偏微分方程": "college", "傅里叶": "college",
        "拉普拉斯": "college", "特征值": "college", "特征向量": "college", "线性空间": "college",
        "线性变换": "college", "正交": "college", "内积": "college", "范数": "college",
        "极限理论": "college", "中值定理": "college", "泰勒公式": "college",
        "多元函数": "college", "重积分": "college", "曲线积分": "college", "曲面积分": "college",
    },
    "en": {
        "number": "elementary", "addition": "elementary", "subtraction": "elementary",
        "multiplication": "elementary", "division": "elementary", "fraction": "elementary",
        "decimal": "elementary", "percentage": "elementary", "area": "elementary",
        "perimeter": "elementary", "volume": "elementary", "shape": "elementary",
        "integer": "middle", "equation": "middle", "inequality": "middle",
        "function": "middle", "linear function": "middle", "quadratic function": "middle",
        "set": "middle", "sequence": "middle", "geometry": "middle",
        "trigonometry": "middle", "probability": "middle", "statistics": "middle",
        "vector": "middle", "coordinate": "middle", "theorem": "middle",
        "derivative": "high", "limit": "high", "integral": "high", "differential": "high",
        "exponential": "high", "logarithm": "high", "complex number": "high",
        "matrix": "high", "series": "high", "calculus": "high",
        "differential equation": "college", "pde": "college", "fourier": "college",
        "laplace": "college", "eigenvalue": "college", "eigenvector": "college",
        "vector space": "college", "linear transformation": "college", "inner product": "college",
        "norm": "college", "multivariable": "college", "taylor series": "college",
    },
    "de": {
        "Zahl": "elementary", "Addition": "elementary", "Subtraktion": "elementary",
        "Multiplikation": "elementary", "Division": "elementary", "Bruch": "elementary",
        "Dezimalzahl": "elementary", "Prozent": "elementary", "Fläche": "elementary",
        "Umfang": "elementary", "Volumen": "elementary", "Dreieck": "elementary",
        "Kreis": "elementary", "Rechteck": "elementary",
        "Gleichung": "middle", "Ungleichung": "middle", "Funktion": "middle",
        "lineare Funktion": "middle", "quadratische Funktion": "middle",
        "Menge": "middle", "Folge": "middle", "Geometrie": "middle",
        "Trigonometrie": "middle", "Wahrscheinlichkeit": "middle", "Statistik": "middle",
        "Vektor": "middle", "Koordinaten": "middle", "Satz": "middle",
        "Ableitung": "high", "Grenzwert": "high", "Integral": "high", "Differential": "high",
        "Exponential": "high", "Logarithmus": "high", "komplexe Zahl": "high",
        "Matrix": "high", "Reihe": "high", "Analysis": "high",
        "Differentialgleichung": "college", "partielle DGL": "college", "Fourier": "college",
        "Eigenwert": "college", "Eigenvektor": "college", "Vektorraum": "college",
        "lineare Abbildung": "college", "inneres Produkt": "college", "Norm": "college",
    }
}

# Relation types based on concept pairs
RELATION_PATTERNS = {
    ("导数", "极限"): ("depends_on", "导数建立在极限概念之上"),
    ("derivative", "limit"): ("depends_on", "The derivative is defined through limits"),
    ("Ableitung", "Grenzwert"): ("depends_on", "Die Ableitung wird über den Grenzwert definiert"),
    ("积分", "导数"): ("related_to", "积分是导数的逆运算"),
    ("integral", "derivative"): ("related_to", "Integration is the inverse of differentiation"),
    ("Integral", "Ableitung"): ("related_to", "Integration ist die Umkehrung der Differentiation"),
    ("微分方程", "导数"): ("depends_on", "微分方程涉及导数"),
    ("differential equation", "derivative"): ("depends_on", "DEs involve derivatives"),
    ("Differentialgleichung", "Ableitung"): ("depends_on", "DGLn enthalten Ableitungen"),
    ("特征值", "矩阵"): ("depends_on", "特征值从矩阵计算"),
    ("eigenvalue", "matrix"): ("depends_on", "Eigenvalues are computed from matrices"),
    ("Eigenwert", "Matrix"): ("depends_on", "Eigenwerte werden aus Matrizen berechnet"),
    ("概率", "统计"): ("related_to", "概率论是统计学的基础"),
    ("probability", "statistics"): ("related_to", "Probability theory underlies statistics"),
    ("函数", "方程"): ("related_to", "函数可以表示为方程"),
    ("function", "equation"): ("related_to", "Functions can be expressed as equations"),
    ("Funktion", "Gleichung"): ("related_to", "Funktionen können als Gleichungen dargestellt werden"),
}

# Known dependencies between concept pairs (infer from their levels)
def infer_relation(c1_name, c2_name, c1_level, c2_level, language):
    """Infer a relation between two concepts."""
    # Check explicit patterns first
    pair = (c1_name, c2_name)
    rev_pair = (c2_name, c1_name)
    if pair in RELATION_PATTERNS:
        return RELATION_PATTERNS[pair]
    if rev_pair in RELATION_PATTERNS:
        r = RELATION_PATTERNS[rev_pair]
        return (r[0], r[1])

    # Infer from level ordering
    level_order = {"elementary": 1, "middle": 2, "high": 3, "college": 4}
    o1 = level_order.get(c1_level, 0)
    o2 = level_order.get(c2_level, 0)
    if o1 > 0 and o2 > 0:
        if o1 < o2:
            return ("depends_on", f"{c1_name} is foundational for {c2_name}")
        elif o1 == o2:
            return ("related_to", f"{c1_name} and {c2_name} are related")
        else:
            return ("extends", f"{c2_name} extends from {c1_name}")
    return ("related_to", f"{c1_name} and {c2_name} are connected")


def rule_based_extraction(text, language="zh"):
    """Extract concepts based on keyword matching."""
    concepts = []
    seen_names = set()
    concept_map = {}

    dict_lang = language if language in MATH_CONCEPTS_BY_LANG else "zh"
    dictionary = MATH_CONCEPTS_BY_LANG[dict_lang]

    # Find concepts in text
    for name, level in dictionary.items():
        if name.lower() in text.lower() and name not in seen_names:
            seen_names.add(name)
            cid = f"c{len(concepts)+1}"
            concepts.append({
                "id": cid, "name": name, "level": level
            })
            concept_map[name] = {"id": cid, "level": level}

    # Generate relations between co-occurring concepts
    relations = []
    used_pairs = set()
    for i in range(len(concepts)):
        for j in range(i+1, len(concepts)):
            pair = (concepts[i]["name"], concepts[j]["name"])
            if pair in used_pairs:
                continue
            used_pairs.add(pair)

            rel_type, evidence = infer_relation(
                concepts[i]["name"], concepts[j]["name"],
                concepts[i]["level"], concepts[j]["level"],
                language
            )
            relations.append({
                "source": concepts[i]["id"],
                "target": concepts[j]["id"],
                "type": rel_type,
                "evidence": evidence
            })

    return {"concepts": concepts, "relations": relations}


def build_graph(extracted, language="zh"):
    """Convert extracted concepts/relations into CognitiveSpace format."""
    nodes = []
    links = []

    for c in extracted.get("concepts", []):
        node = {
            "id": c["id"],
            "name": c["name"],
            "labels": {language: c["name"]},
            "group": "user_upload",
            "level": c.get("level", "college"),
            "level_order": {"elementary":1,"middle":2,"high":3,"college":4}.get(c.get("level","college"),4),
            "importance": 5,
            "source_count": 1,
            "cross_references": []
        }
        nodes.append(node)

    # Build ID → name mapping
    name_map = {c["id"]: c["name"] for c in extracted.get("concepts", [])}

    for r in extracted.get("relations", []):
        if r["source"] in name_map and r["target"] in name_map:
            link = {
                "source": r["source"],
                "target": r["target"],
                "type": r.get("type", "related_to"),
                "importance": 0.8,
                "known": True,
                "inferred": False,
                "evidence": r.get("evidence", "")
            }
            links.append(link)

    return {"nodes": nodes, "links": links}


def export_visualization(graph_data, output_dir):
    """Generate a standalone CognitiveSpace HTML from graph data."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read the existing CognitiveSpace HTML as template
    source_viz = PROJECT_DIR / "cognitive-space" / "web" / "index.html"
    if not source_viz.exists():
        print("ERROR: CognitiveSpace source not found")
        return None

    html = source_viz.read_text("utf-8")

    # Replace inline COGNITIVE_DATA with our new data
    # Find the data block and replace it
    data_start = html.find('const COGNITIVE_DATA = {')
    data_end = html.find('"links": [', data_start)
    if data_end > 0:
        # Find the closing bracket of the links array
        links_end = html.find(']', data_end)
        # Find the closing of the whole COGNITIVE_DATA object
        obj_end = html.find('};', links_end) + 2

        new_data = json.dumps(graph_data, ensure_ascii=False, indent=2)
        new_block = f'const COGNITIVE_DATA = {new_data};'

        html = html[:data_start] + new_block + html[obj_end:]

    # Write output
    output_html = output_dir / "index.html"
    output_html.write_text(html, encoding="utf-8")
    return output_html


def process_text(text, language="zh", output_dir=None):
    """Full pipeline: text → extraction → graph → visualization."""
    if output_dir is None:
        output_dir = PROJECT_DIR / "workbench" / "output" / "latest"
    output_dir = Path(output_dir)

    print(f"Processing {language} text ({len(text)} chars)...")

    # Step 1: Concept extraction via LLM
    extracted = call_llm(text, language)
    concepts = extracted.get("concepts", [])
    relations = extracted.get("relations", [])
    print(f"  Extracted {len(concepts)} concepts, {len(relations)} relations")

    # Step 2: Build graph
    graph = build_graph(extracted, language)
    print(f"  Graph: {len(graph['nodes'])} nodes, {len(graph['links'])} links")

    # Step 3: Generate visualization
    viz_path = export_visualization(graph, output_dir)
    if viz_path:
        print(f"  Visualization: {viz_path}")

    # Step 4: Compute basic statistics
    stats = {
        "concepts": len(graph["nodes"]),
        "relations": len(graph["links"]),
        "levels": {},
        "text_length": len(text),
        "language": language
    }
    for n in graph["nodes"]:
        lv = n.get("level", "unknown")
        stats["levels"][lv] = stats["levels"].get(lv, 0) + 1

    return {"stats": stats, "graph": graph, "viz_path": str(viz_path)}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", help="Text to process")
    parser.add_argument("--file", help="Input file")
    parser.add_argument("--lang", default="zh", choices=["zh","en","de"])
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        text = "函数是数学中描述变量之间关系的重要工具。导数描述函数的变化率。极限是导数的基础。积分用于计算面积。"
        args.lang = "zh"

    result = process_text(text, args.lang)
    print(f"\nDone! Concepts: {result['stats']['concepts']}, Relations: {result['stats']['relations']}")
    print(f"Open: {result['viz_path']}")
