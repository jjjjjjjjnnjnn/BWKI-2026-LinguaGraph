"""
compute_all_coverage.py — 为所有课标计算覆盖率

为每个课标图谱计算 Coverage Score（教材覆盖率）
"""

import json
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GRAPH_DIR = PROJECT_ROOT / "config" / "expert_graphs"


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_keywords(text):
    text = text.lower()
    text = re.sub(r'[,;:()\[\]{}]', ' ', text)
    words = text.split()
    stop = {'the', 'and', 'or', 'of', 'in', 'to', 'for', 'with', 'by', 'at',
            'on', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'shall', 'must', 'need', 'use',
            'that', 'this', 'these', 'those', 'it', 'its', 'they', 'them',
            'their', 'we', 'our', 'you', 'your', 'he', 'she', 'his', 'her',
            'pupils', 'students', 'children', 'should', 'taught', 'include',
            'die', 'der', 'das', 'und', 'oder', 'von', 'zu', 'in', 'mit',
            'für', 'auf', 'aus', 'nach', 'bei', 'über', 'unter', 'vor',
            'sich', 'auch', 'als', 'ist', 'sind', 'werden', 'diese',
            '的', '了', '在', '是', '和', '与', '或', '及', '等',
            '认识', '知道', '理解', '掌握', '运用'}
    return {w for w in words if len(w) > 2 and w not in stop}


# ── Cross-language keyword bridge ──────────────────────────────────────────
KEYWORD_BRIDGE = {
    # German → Chinese
    'zahlen': ['数', '数字'], 'addition': ['加法', '加'], 'subtraktion': ['减法', '减'],
    'multiplikation': ['乘法', '乘'], 'division': ['除法', '除'],
    'bruch': ['分数'], 'dezimal': ['小数'], 'prozent': ['百分'],
    'gleichung': ['方程'], 'funktion': ['函数'], 'ableitung': ['导数'],
    'integral': ['积分'], 'dreieck': ['三角形'], 'kreis': ['圆'],
    'quadrat': ['正方形', '二次'], 'flächeninhalt': ['面积'], 'volumen': ['体积'],
    'wahrscheinlichkeit': ['概率'], 'statistik': ['统计'],
    'vektor': ['向量'], 'matrix': ['矩阵'], 'koordinate': ['坐标'],
    'symmetrie': ['对称'], 'parallel': ['平行'], 'winkel': ['角'],
    'länge': ['长度'], 'gewicht': ['质量'], 'zeit': ['时间'],
    'geld': ['钱', '货币'], 'muster': ['规律', '模式'],
    'potenz': ['幂'], 'wurzel': ['根'], 'gleichung': ['方程'],
    'unbekannte': ['未知数'], 'variable': ['变量'],
    # English → Chinese
    'number': ['数', '数字'], 'addition': ['加法'], 'subtraction': ['减法'],
    'multiplication': ['乘法'], 'division': ['除法'],
    'fraction': ['分数'], 'decimal': ['小数'], 'percent': ['百分'],
    'algebra': ['代数'], 'equation': ['方程'], 'expression': ['表达式'],
    'function': ['函数'], 'graph': ['图'], 'geometry': ['几何'],
    'angle': ['角'], 'triangle': ['三角形'], 'circle': ['圆'],
    'area': ['面积'], 'perimeter': ['周长'], 'volume': ['体积'],
    'probability': ['概率'], 'statistics': ['统计'], 'data': ['数据'],
    'ratio': ['比', '比例'], 'proportion': ['比例'],
    'pattern': ['规律', '模式'], 'sequence': ['数列'],
    'coordinate': ['坐标'], 'symmetry': ['对称'],
    'parallel': ['平行'], 'perpendicular': ['垂直'],
    'length': ['长度'], 'mass': ['质量'], 'time': ['时间'],
    'money': ['货币'], 'measure': ['测量'],
}


def match_curriculum_to_textbook(cur_concepts, tb_concepts, curriculum_lang='de'):
    """Match curriculum concepts to textbook concepts."""
    matches = {}
    
    # Build textbook keyword index
    tb_kw = {}
    for tc in tb_concepts:
        name = tc["name"]
        labels = tc.get("labels", {})
        kws = set()
        for label in labels.values():
            kws |= extract_keywords(label)
        name_parts = name.replace("math_", "").replace("_", " ").split()
        kws |= {p.lower() for p in name_parts if len(p) > 2}
        tb_kw[name] = kws
    
    for cc in cur_concepts:
        cc_name = cc["name"]
        label = cc.get("labels", {}).get(curriculum_lang, "")
        cc_kws = extract_keywords(label)
        
        # Bridge to Chinese keywords
        cn_kws = set()
        for kw in cc_kws:
            if kw in KEYWORD_BRIDGE:
                cn_kws |= set(KEYWORD_BRIDGE[kw])
        
        all_kws = cc_kws | cn_kws
        
        matched = []
        for tc in tb_concepts:
            tb_name = tc["name"]
            tb_kws = tb_kw.get(tb_name, set())
            overlap = all_kws & tb_kws
            if len(overlap) >= 1:
                matched.append((tb_name, len(overlap)))
        
        matched.sort(key=lambda x: -x[1])
        matches[cc_name] = [m[0] for m in matched[:5]]
    
    return matches


def compute_coverage_by_stage(cur_concepts, matches, stage_key_map):
    """Compute coverage grouped by stage."""
    by_stage = defaultdict(list)
    for cc in cur_concepts:
        by_stage[cc["stage"]].append(cc)
    
    results = {}
    all_matched = set()
    
    for stage_key, stage_concepts in by_stage.items():
        matched = sum(1 for cc in stage_concepts if matches.get(cc["name"], []))
        total = len(stage_concepts)
        cov = matched / max(total, 1)
        
        level = stage_key_map.get(stage_key, "unknown")
        results[stage_key] = {
            "curriculum_concepts": total,
            "matched": matched,
            "coverage": round(cov, 4),
        }
        
        for cc in stage_concepts:
            if matches.get(cc["name"], []):
                all_matched.add(cc["name"])
    
    total_cur = len(cur_concepts)
    total_matched = len(all_matched)
    results["overall"] = {
        "curriculum_concepts": total_cur,
        "matched": total_matched,
        "coverage": round(total_matched / max(total_cur, 1), 4),
    }
    
    return results


def main():
    print("=" * 60)
    print("LinguaGraph — Multi-Curriculum Coverage Scores")
    print("=" * 60)
    
    textbook = load_json(GRAPH_DIR / "math_full.json")
    tb_concepts = textbook["concepts"]
    
    curricula = {
        "NRW (Germany)": {
            "file": "curriculum_nrw_math.json",
            "lang": "de",
            "stage_map": {
                "seki_erprobung": "elementary", "seki_stufe1": "middle",
                "seki_stufe2": "high", "sekii_einfuehrung": "high",
                "sekii_grundkurs": "college", "sekii_leistungskurs": "college",
            },
        },
        "UK": {
            "file": "curriculum_uk_math.json",
            "lang": "en",
            "stage_map": {
                "uk_ks1_y1": "elementary", "uk_ks1_y2": "elementary",
                "uk_ks2_y3": "elementary", "uk_ks2_y4": "elementary",
                "uk_ks2_y5": "middle", "uk_ks2_y6": "middle",
                "uk_ks3": "middle", "uk_ks4": "high",
            },
        },
        "China": {
            "file": "curriculum_cn_math.json",
            "lang": "zh",
            "stage_map": {
                "cn_grade_1_2": "elementary", "cn_grade_3_4": "elementary",
                "cn_grade_5_6": "middle", "cn_grade_7_9": "middle",
                "cn_grade_10_12": "high",
            },
        },
        "US": {
            "file": "curriculum_us_math.json",
            "lang": "en",
            "stage_map": {
                "us_k5": "elementary", "us_68": "middle", "us_912": "high",
            },
        },
    }
    
    all_results = {}
    
    for name, config in curricula.items():
        print(f"\n[{name}]")
        cur_data = load_json(GRAPH_DIR / config["file"])
        cur_concepts = cur_data["concepts"]
        print(f"  Concepts: {len(cur_concepts)}")
        
        matches = match_curriculum_to_textbook(cur_concepts, tb_concepts, config["lang"])
        matched_count = sum(1 for v in matches.values() if v)
        print(f"  Matched to textbook: {matched_count}/{len(cur_concepts)}")
        
        coverage = compute_coverage_by_stage(cur_concepts, matches, config["stage_map"])
        all_results[name] = coverage
        
        print(f"\n  Coverage by stage:")
        print(f"  {'Stage':<35} {'Cur':>5} {'Match':>6} {'Cov%':>8}")
        print(f"  {'-'*35} {'-'*5} {'-'*6} {'-'*8}")
        for sk in sorted(coverage.keys()):
            if sk == "overall":
                continue
            r = coverage[sk]
            print(f"  {sk:<35} {r['curriculum_concepts']:>5} {r['matched']:>6} {r['coverage']*100:>7.1f}%")
        r = coverage["overall"]
        print(f"  {'OVERALL':<35} {r['curriculum_concepts']:>5} {r['matched']:>6} {r['coverage']*100:>7.1f}%")
    
    # Save all results
    output = {
        "description": "Multi-Curriculum Coverage Scores — 教材对各国课标的覆盖率",
        "textbook_source": "LinguaGraph math_full.json (197 concepts)",
        "results": all_results,
    }
    
    out_path = GRAPH_DIR / "coverage_all_curricula.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"All results saved: {out_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
