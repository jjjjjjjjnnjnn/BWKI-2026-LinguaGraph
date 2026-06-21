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
    """Call local Qwen2.5-0.5B via llama-cli for concept extraction."""
    prompt = EXTRACT_PROMPT.format(text=text, language=language)

    llama_path = PROJECT_DIR / "llama" / "llama-cli.exe"
    model_path = PROJECT_DIR / "models" / "qwen2.5-0.5b-q4_k_m.gguf"

    if not llama_path.exists():
        print("WARN: llama-cli not found, using rule-based fallback")
        return rule_based_extraction(text, language)

    try:
        result = subprocess.run(
            [str(llama_path), "-m", str(model_path), "-p", prompt,
             "-n", "512", "--temp", "0.1", "--repeat-penalty", "1.1"],
            capture_output=True, text=True, timeout=60, encoding="utf-8"
        )
        output = result.stdout
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        print(f"LLM call failed: {e}")

    return rule_based_extraction(text, language)


def rule_based_extraction(text, language="zh"):
    """Simple keyword-based extraction as fallback when LLM unavailable."""
    # Common math concepts by language
    MATH_CONCEPTS = {
        "zh": ["函数","导数","极限","积分","微分","方程","矩阵","向量","概率","统计",
               "集合","数列","三角函数","指数","对数","不等式","几何","代数","复数","级数"],
        "en": ["function","derivative","limit","integral","differential","equation",
               "matrix","vector","probability","statistics"],
        "de": ["Funktion","Ableitung","Grenzwert","Integral","Differential","Gleichung",
               "Matrix","Vektor","Wahrscheinlichkeit","Statistik"],
    }
    concepts = []
    relations = []
    seen = set()
    for word in MATH_CONCEPTS.get(language, MATH_CONCEPTS["zh"]):
        if word in text and word not in seen:
            seen.add(word)
            # Assign level heuristically
            level = "college"
            if word in ["集合","数列","几何","代数"]:
                level = "middle"
            elif word in ["函数","三角函数","概率","统计"]:
                level = "high"
            concepts.append({
                "id": f"concept_{len(concepts)+1}",
                "name": word,
                "level": level
            })
    # Create simple relations between consecutive concepts
    for i in range(len(concepts) - 1):
        relations.append({
            "source": concepts[i]["id"],
            "target": concepts[i+1]["id"],
            "type": "related_to",
            "evidence": f"{concepts[i]['name']} 与 {concepts[i+1]['name']} 相关"
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
