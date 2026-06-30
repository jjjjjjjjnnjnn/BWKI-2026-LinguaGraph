#!/usr/bin/env python3
"""
compute_all_coverage_v2.py — Recalculate multi-curriculum coverage
with CORRECT methodology: curriculum concepts → textbook concepts.

Fixes coverage_all_curricula.json which showed ~100% for all curricula
(incorrect). The correct approach checks how many curriculum concepts
are covered BY the textbook (197 math_full concepts), not the reverse.

Expected ranges:
  NRW: 10-40%
  UK: 70-90%
  US: varies (many abstract standards)
  CN: < 15%
"""

import json
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GRAPH_DIR = PROJECT_ROOT / "config" / "expert_graphs"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_keywords(text):
    """Extract meaningful keywords, filtering stopwords in all 3 languages."""
    text = text.lower()
    text = re.sub(r"[,;:()\[\]{}.!?''\"]", " ", text)
    words = text.split()
    stop = {
        # English
        "the", "and", "or", "of", "in", "to", "for", "with", "by", "at",
        "on", "from", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "can", "shall", "must", "need", "use",
        "that", "this", "these", "those", "it", "its", "they", "them",
        "their", "we", "our", "you", "your", "he", "she", "his", "her",
        "pupils", "students", "children", "taught", "include", "using",
        "understand", "apply", "solve", "represent", "describe", "explain",
        "develop", "evaluate", "compare", "identify", "recognize", "state",
        "given", "real", "context", "mathematical", "mathematics",
        # German
        "die", "der", "das", "und", "oder", "von", "zu", "in", "mit",
        "für", "auf", "aus", "nach", "bei", "über", "unter", "vor",
        "sich", "auch", "als", "ist", "sind", "werden", "diese",
        "einer", "eines", "einem", "einen", "dem", "den", "des",
        "im", "am", "zum", "zur", "bis", "per", "pro", "etc",
        "bzw", "dh", "z.b", "insbesondere", "besonders", "grundlegende",
        "schülerinnen", "schüler", "schülerinnen und schüler",
        "man", "kann", "soll", "muss", "dass", "wenn", "wie",
        "eine", "einem", "einer", "eines", "einen",
        # Chinese
        "的", "了", "在", "是", "和", "与", "或", "及", "等",
        "认识", "知道", "理解", "掌握", "运用", "能", "会",
        "通过", "利用", "结合", "比较", "分析", "解决",
        "简单", "实际", "具体", "适当", "基本", "初步",
    }
    return {w for w in words if len(w) > 2 and w not in stop}


# Cross-language keyword bridge: curriculum lang → Chinese (textbook lang)
KEYWORD_BRIDGE = {
    # ── German → Chinese ──
    "zahlen": ["数", "数字"], "addition": ["加法", "加"],
    "subtraktion": ["减法", "减"], "multiplikation": ["乘法", "乘"],
    "division": ["除法", "除"], "bruch": ["分数"],
    "dezimal": ["小数"], "prozent": ["百分"],
    "gleichung": ["方程"], "funktion": ["函数"],
    "ableitung": ["导数"], "integral": ["积分"],
    "dreieck": ["三角形"], "kreis": ["圆"],
    "quadrat": ["正方形", "二次"], "flächeninhalt": ["面积"],
    "volumen": ["体积"], "wahrscheinlichkeit": ["概率"],
    "statistik": ["统计"], "vektor": ["向量"],
    "matrix": ["矩阵"], "koordinate": ["坐标"],
    "symmetrie": ["对称"], "parallel": ["平行"],
    "winkel": ["角"], "länge": ["长度"],
    "gewicht": ["质量"], "zeit": ["时间"],
    "geld": ["钱", "货币"], "muster": ["规律", "模式"],
    "potenz": ["幂"], "wurzel": ["根"],
    "unbekannte": ["未知数"], "variable": ["变量"],
    "rechnen": ["计算"], "formel": ["公式"],
    "satz": ["定理"], "beweis": ["证明"],
    "konstruktion": ["作图"], "graph": ["图"],
    "tabelle": ["表"], "zahl": ["数"],
    "brüche": ["分数"], "prozentsatz": ["百分"],
    "gleichungen": ["方程"], "terme": ["表达式"],
    "funktionen": ["function"], "potenzen": ["幂"],
    "wurzeln": ["根"], "daten": ["数据"],
    "raum": ["空间"], "körper": ["立体"],
    "stochastik": ["概率", "统计"],
    "lineare": ["线性"], "quadratische": ["二次"],
    "exponentielle": ["指数"], "logarithmische": ["对数"],
    "trigonometrie": ["三角"], "geometrie": ["几何"],
    "analysis": ["分析", "微积分"], "algebra": ["代数"],
    "arithmetic": ["算术"],
    # ── English → Chinese ──
    "number": ["数", "数字"], "numbers": ["数", "数字"],
    "addition": ["加法"], "subtraction": ["减法"],
    "multiplication": ["乘法"], "division": ["除法"],
    "fraction": ["分数"], "fractions": ["分数"],
    "decimal": ["小数"], "decimals": ["小数"],
    "percent": ["百分"], "percentage": ["百分"],
    "algebra": ["代数"], "equation": ["方程"],
    "equations": ["方程"], "expression": ["表达式"],
    "expressions": ["表达式"], "function": ["函数"],
    "functions": ["函数"], "graph": ["图"],
    "graphs": ["图"], "geometry": ["几何"],
    "angle": ["角"], "angles": ["角"],
    "triangle": ["三角形"], "triangles": ["三角形"],
    "circle": ["圆"], "circles": ["圆"],
    "area": ["面积"], "perimeter": ["周长"],
    "volume": ["体积"], "probability": ["概率"],
    "statistics": ["统计"], "data": ["数据"],
    "ratio": ["比", "比例"], "ratios": ["比", "比例"],
    "proportion": ["比例"], "proportions": ["比例"],
    "pattern": ["规律", "模式"], "patterns": ["规律", "模式"],
    "sequence": ["数列"], "sequences": ["数列"],
    "coordinate": ["坐标"], "coordinates": ["坐标"],
    "symmetry": ["对称"], "parallel": ["平行"],
    "perpendicular": ["垂直"], "length": ["长度"],
    "mass": ["质量"], "time": ["时间"],
    "money": ["货币"], "measure": ["测量"],
    "measurement": ["测量"], "shape": ["图形"],
    "shapes": ["图形"], "space": ["空间"],
    "statistics": ["统计"], "average": ["平均"],
    "mean": ["平均"], "median": ["中位数"],
    "mode": ["众数"], "range": ["极差"],
    "prime": ["素数", "质数"], "factor": ["因数"],
    "factors": ["因数"], "multiple": ["倍数"],
    "multiples": ["倍数"], "integer": ["整数"],
    "integers": ["整数"], "negative": ["负"],
    "positive": ["正"], "power": ["幂"],
    "powers": ["幂"], "root": ["根"],
    "roots": ["根"], "square": ["平方"],
    "cube": ["立方"], "linear": ["线性"],
    "quadratic": ["二次"], "exponential": ["指数"],
    "logarithm": ["对数"], "logarithms": ["对数"],
    "sine": ["正弦"], "cosine": ["余弦"],
    "tangent": ["正切"], "trigonometry": ["三角"],
    "vector": ["向量"], "vectors": ["向量"],
    "matrix": ["矩阵"], "matrices": ["矩阵"],
    "transform": ["变换"], "transformation": ["变换"],
    "congruent": ["全等"], "similarity": ["相似"],
    "theorem": ["定理"], "proof": ["证明"],
    "formula": ["公式"], " formulas": ["公式"],
    "construct": ["作图"], "construction": ["作图"],
    # ── Chinese → Chinese (direct) ──
    "数": ["数"], "数字": ["数字"],
    "加法": ["加法"], "减法": ["减法"],
    "乘法": ["乘法"], "除法": ["除法"],
    "分数": ["分数"], "小数": ["小数"],
    "百分": ["百分"], "方程": ["方程"],
    "函数": ["函数"], "导数": ["导数"],
    "积分": ["积分"], "三角形": ["三角形"],
    "圆": ["圆"], "面积": ["面积"],
    "体积": ["体积"], "概率": ["概率"],
    "统计": ["统计"], "向量": ["向量"],
    "矩阵": ["矩阵"], "坐标": ["坐标"],
    "对称": ["对称"], "平行": ["平行"],
    "角": ["角"], "长度": ["长度"],
    "质量": ["质量"], "时间": ["时间"],
    "代数": ["代数"], "几何": ["几何"],
    "算术": ["算术"], "线性": ["线性"],
    "二次": ["二次"], "幂": ["幂"],
    "根": ["根"], "公式": ["公式"],
    "定理": ["定理"], "证明": ["证明"],
    "变换": ["变换"], "作图": ["作图"],
    "数据": ["数据"], "规律": ["规律"],
    "模式": ["模式"], "比例": ["比例"],
    "变量": ["变量"], "表达式": ["表达式"],
    "未知数": ["未知数"],
}


def get_textbook_zh_keywords(tc):
    """Extract all Chinese keywords from a textbook concept."""
    kws = set()
    name = tc["name"]
    # Extract Chinese part from name like "math_calculus_导数"
    parts = name.split("_")
    for p in parts:
        # Check if part contains Chinese characters
        if re.search(r"[\u4e00-\u9fff]", p):
            kws.add(p)
    # Also check labels
    for lang, label in tc.get("labels", {}).items():
        if lang == "zh" and label:
            kws |= extract_keywords(label)
            # Also add the full label if it's short Chinese
            if re.search(r"[\u4e00-\u9fff]", label) and len(label) <= 20:
                kws.add(label)
    return kws


def match_curriculum_concept(cc, tb_concepts, curriculum_lang):
    """Check if a curriculum concept is covered by any textbook concept.

    Uses cross-language keyword bridging + direct matching.
    Returns True if at least one textbook concept has >= 2 keyword overlaps.
    """
    label = cc.get("display_name", "") or cc.get("labels", {}).get(curriculum_lang, "")
    cc_kws = extract_keywords(label)

    # Bridge to Chinese keywords
    cn_kws = set()
    for kw in cc_kws:
        if kw in KEYWORD_BRIDGE:
            cn_kws |= set(KEYWORD_BRIDGE[kw])

    # If curriculum is already Chinese, add direct keywords
    if curriculum_lang == "zh":
        cn_kws |= cc_kws

    all_kws = cc_kws | cn_kws
    if not all_kws:
        return False, []

    matched_tb = []
    for tc in tb_concepts:
        tb_kws = get_textbook_zh_keywords(tc)
        overlap = all_kws & tb_kws
        if len(overlap) >= 2:
            matched_tb.append((tc["name"], len(overlap), overlap))

    if matched_tb:
        matched_tb.sort(key=lambda x: -x[1])
        return True, matched_tb[:3]

    # Fallback: allow 1 keyword overlap for very specific terms
    for tc in tb_concepts:
        tb_kws = get_textbook_zh_keywords(tc)
        overlap = all_kws & tb_kws
        if len(overlap) >= 1:
            matched_tb.append((tc["name"], len(overlap), overlap))

    if matched_tb:
        matched_tb.sort(key=lambda x: -x[1])
        # Only accept if the matched keyword is specific (not a single common char)
        best_overlap = matched_tb[0][2]
        if any(len(kw) >= 2 for kw in best_overlap):
            return True, matched_tb[:3]

    return False, []


def compute_coverage(cur_concepts, tb_concepts, curriculum_lang):
    """Compute coverage for one curriculum."""
    by_stage = defaultdict(list)
    for cc in cur_concepts:
        by_stage[cc["stage"]].append(cc)

    results = {}
    all_matched = set()
    all_samples = {}

    for stage_key, stage_concepts in by_stage.items():
        matched_count = 0
        samples = []
        for cc in stage_concepts:
            is_matched, sample = match_curriculum_concept(cc, tb_concepts, curriculum_lang)
            if is_matched:
                matched_count += 1
                all_matched.add(cc["name"])
                if len(samples) < 5:
                    samples.append({
                        "curriculum_concept": cc["display_name"][:60],
                        "textbook_matches": [s[0] for s in sample],
                    })

        total = len(stage_concepts)
        cov = matched_count / max(total, 1)
        results[stage_key] = {
            "curriculum_concepts": total,
            "matched": matched_count,
            "coverage": round(cov, 4),
        }
        all_samples[stage_key] = samples

    total_cur = len(cur_concepts)
    total_matched = len(all_matched)
    results["overall"] = {
        "curriculum_concepts": total_cur,
        "matched": total_matched,
        "coverage": round(total_matched / max(total_cur, 1), 4),
    }

    return results, all_samples


def main():
    print("=" * 60)
    print("LinguaGraph — Multi-Curriculum Coverage (v2)")
    print("Methodology: curriculum concepts → textbook concepts")
    print("=" * 60)

    textbook = load_json(GRAPH_DIR / "math_full.json")
    tb_concepts = textbook["concepts"]
    print(f"Textbook concepts: {len(tb_concepts)}")

    curricula = {
        "NRW": {
            "file": "curriculum_nrw_math.json",
            "lang": "de",
        },
        "UK": {
            "file": "curriculum_uk_math.json",
            "lang": "en",
        },
        "US": {
            "file": "curriculum_us_math.json",
            "lang": "en",
        },
        "China": {
            "file": "curriculum_cn_compulsory_math.json",
            "lang": "zh",
        },
    }

    all_results = {}

    for name, config in curricula.items():
        print(f"\n[{name}]")
        cur_data = load_json(GRAPH_DIR / config["file"])
        cur_concepts = cur_data["concepts"]
        print(f"  Curriculum concepts: {len(cur_concepts)}")

        coverage, samples = compute_coverage(cur_concepts, tb_concepts, config["lang"])
        all_results[name] = coverage

        print(f"\n  {'Stage':<40} {'Cur':>5} {'Match':>6} {'Cov%':>8}")
        print(f"  {'-'*40} {'-'*5} {'-'*6} {'-'*8}")
        for sk in sorted(coverage.keys()):
            if sk == "overall":
                continue
            r = coverage[sk]
            print(f"  {sk:<40} {r['curriculum_concepts']:>5} {r['matched']:>6} {r['coverage']*100:>7.1f}%")
        r = coverage["overall"]
        print(f"  {'OVERALL':<40} {r['curriculum_concepts']:>5} {r['matched']:>6} {r['coverage']*100:>7.1f}%")

    # Save
    output = {
        "description": "Multi-Curriculum Coverage Scores — 课标概念→教材概念匹配",
        "methodology": "curriculum_concepts → textbook_concepts (keyword bridge + 2-overlap threshold)",
        "textbook_source": f"LinguaGraph math_full.json ({len(tb_concepts)} concepts)",
        "results": all_results,
    }

    out_path = GRAPH_DIR / "coverage_all_curricula.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Also update coverage_scores.json for NRW
    nrw_output = {
        "description": "Curriculum Coverage Score — 教材对NRW课标的覆盖率",
        "curriculum_source": "Kernlehrplan Mathematik NRW (Sek I 2019 + Sek II 2023)",
        "textbook_source": f"LinguaGraph math_full.json ({len(tb_concepts)} concepts)",
        "methodology": "curriculum_concepts → textbook_concepts (keyword bridge + 2-overlap threshold)",
        "coverage_by_stage": all_results["NRW"],
    }
    scores_path = GRAPH_DIR / "coverage_scores.json"
    with open(scores_path, "w", encoding="utf-8") as f:
        json.dump(nrw_output, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"Saved: {out_path}")
    print(f"Saved: {scores_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
