"""
compute_coverage.py — 计算教材对课标的覆盖率 (Coverage Score)

Coverage(L) = |教材概念_L ∩ 课标概念_L| / |课标概念_L|

改进策略：
1. 用 concept_mapping.json 的 de↔zh 映射做核心桥接
2. 用概念名称中的德语关键词做补充匹配
3. 按学段分组计算
"""

import json
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_keywords(text):
    """Extract meaningful keywords from text."""
    text = text.lower()
    text = re.sub(r'[,;:()\[\]{}]', ' ', text)
    words = text.split()
    stop = {'die', 'der', 'das', 'und', 'oder', 'von', 'zu', 'in', 'mit',
            'für', 'auf', 'aus', 'nach', 'bei', 'über', 'unter', 'vor',
            'sich', 'auch', 'als', 'ist', 'sind', 'werden', 'diese',
            'einer', 'eines', 'einem', 'einen', 'dem', 'den', 'des',
            'im', 'am', 'zum', 'zur', 'bis', 'per', 'pro', 'etc',
            'bzw', 'dh', 'z.b', 'insbesondere', 'besonders', 'grundlegende',
            'schülerinnen', 'schüler', 'schülerinnen und schüler'}
    return {w for w in words if len(w) > 2 and w not in stop}


def main():
    print("=" * 60)
    print("LinguaGraph — Coverage Score (v2: mapping-based)")
    print("=" * 60)
    
    curriculum = load_json(PROJECT_ROOT / "config" / "expert_graphs" / "curriculum_nrw_math.json")
    textbook = load_json(PROJECT_ROOT / "config" / "expert_graphs" / "math_full.json")
    mapping = load_json(PROJECT_ROOT / "config" / "concept_mapping.json")
    
    cur_concepts = curriculum["concepts"]
    tb_concepts = textbook["concepts"]
    
    # ── Build mapping index ──
    de_to_zh = dict(mapping.get("de_to_zh", {}))
    zh_to_de = dict(mapping.get("de_to_zh", {}))  # reverse
    # Actually de_to_zh is already {de: zh}
    # Build zh -> de reverse
    zh_to_de = {v: k for k, v in de_to_zh.items()}
    
    print(f"Curriculum: {len(cur_concepts)} concepts")
    print(f"Textbook: {len(tb_concepts)} concepts")
    print(f"De↔Zh mappings: {len(de_to_zh)}")
    
    # ── Build textbook keyword index ──
    # Each textbook concept has a name like "math_calculus_导数" and labels
    # We need to match curriculum German terms to textbook Chinese terms via mapping
    
    # Build a set of all Chinese terms in textbook
    tb_zh_terms = set()
    for tc in tb_concepts:
        name = tc["name"]
        # Extract Chinese from name (after last underscore group)
        zh_part = name.split("_")[-1] if "_" in name else name
        tb_zh_terms.add(zh_part)
        # Also add labels
        for lang, label in tc.get("labels", {}).items():
            if lang == "zh":
                tb_zh_terms.add(label)
    
    # ── Match curriculum concepts to textbook ──
    matches = {}
    
    for cc in cur_concepts:
        cc_name = cc["name"]
        label_de = cc.get("labels", {}).get("de", "")
        
        # Strategy 1: Direct de→zh mapping
        matched_tb = set()
        
        # Extract German keywords from curriculum concept
        de_kws = extract_keywords(label_de)
        
        for de_term in de_kws:
            if de_term in de_to_zh:
                zh_term = de_to_zh[de_term]
                # Find textbook concepts containing this zh term
                for tc in tb_concepts:
                    tc_name = tc["name"]
                    tc_labels = tc.get("labels", {})
                    if zh_term in tc_name or zh_term in tc_labels.get("zh", ""):
                        matched_tb.add(tc_name)
        
        # Strategy 2: Direct German term match in textbook name
        # Some textbook names contain German-like patterns
        for tc in tb_concepts:
            tc_name = tc["name"].lower()
            for de_term in de_kws:
                if de_term in tc_name:
                    matched_tb.add(tc["name"])
        
        # Strategy 3: Match by concept category keywords
        # Common math terms that appear in both
        category_keywords = {
            "ableitung": ["导数", "微分", "derivative"],
            "integral": ["积分", "integral"],
            "gleichung": ["方程", "equation"],
            "funktion": ["函数", "function"],
            "dreieck": ["三角形", "triangle"],
            "kreis": ["圆", "circle"],
            "wahrscheinlichkeit": ["概率", "probability"],
            "statistik": ["统计", "statistics"],
            "vektor": ["向量", "vector"],
            "matrix": ["矩阵", "matrix"],
            "potenz": ["幂", "power"],
            "wurzel": ["根", "root"],
            "bruch": ["分数", "fraction"],
            "prozent": ["百分", "percent"],
            "gleichung": ["方程", "equation"],
            "unbekannte": ["未知数", "unknown"],
            "koordinate": ["坐标", "coordinate"],
            "symmetrie": ["对称", "symmetry"],
            "konstruktion": ["作图", "construction"],
            "graph": ["图", "graph"],
            "tabelle": ["表", "table"],
            "zahl": ["数", "number"],
            "rechnen": ["计算", "calculation"],
            "formel": ["公式", "formula"],
            "satz": ["定理", "theorem"],
            "beweis": ["证明", "proof"],
            "_definition": ["定义", "definition"],
            "beispiel": ["例", "example"],
            "aufgabe": ["题", "problem"],
        }
        
        for de_term, zh_list in category_keywords.items():
            if de_term in de_kws:
                for zh in zh_list:
                    for tc in tb_concepts:
                        tc_name = tc["name"]
                        tc_labels = tc.get("labels", {})
                        if zh in tc_name or zh in tc_labels.get("zh", ""):
                            matched_tb.add(tc["name"])
        
        matches[cc_name] = list(matched_tb)
    
    # ── Compute coverage by stage ──
    stage_order = ["seki_erprobung", "seki_stufe1", "seki_stufe2",
                    "sekii_einfuehrung", "sekii_grundkurs", "sekii_leistungskurs"]
    
    stage_labels = {
        "seki_erprobung": "Erprobungsstufe (5-6)",
        "seki_stufe1": "Erste Stufe (7-8)",
        "seki_stufe2": "Zweite Stufe (9-10)",
        "sekii_einfuehrung": "Einführungsphase (11)",
        "sekii_grundkurs": "Grundkurs (12-13)",
        "sekii_leistungskurs": "Leistungskurs (12-13)",
    }
    
    # Group by stage
    cur_by_stage = defaultdict(list)
    for cc in cur_concepts:
        cur_by_stage[cc["stage"]].append(cc)
    
    results = {}
    all_matched = set()
    
    print("\n  Coverage by stage:")
    print(f"  {'Stage':<35} {'Cur':>5} {'Match':>6} {'Cov%':>8}")
    print(f"  {'-'*35} {'-'*5} {'-'*6} {'-'*8}")
    
    for stage_key in stage_order:
        stage_concepts = cur_by_stage.get(stage_key, [])
        matched = sum(1 for cc in stage_concepts if matches.get(cc["name"], []))
        total = len(stage_concepts)
        cov = matched / max(total, 1)
        
        results[stage_key] = {
            "stage": stage_key,
            "stage_label": stage_labels[stage_key],
            "curriculum_concepts": total,
            "matched_textbook_concepts": matched,
            "coverage_score": round(cov, 4),
        }
        
        label = stage_labels[stage_key]
        print(f"  {label:<35} {total:>5} {matched:>6} {cov*100:>7.1f}%")
        
        for cc in stage_concepts:
            if matches.get(cc["name"], []):
                all_matched.add(cc["name"])
    
    # Overall
    total_cur = len(cur_concepts)
    total_matched = len(all_matched)
    overall_cov = total_matched / max(total_cur, 1)
    
    results["overall"] = {
        "stage": "overall",
        "stage_label": "Overall",
        "curriculum_concepts": total_cur,
        "matched_textbook_concepts": total_matched,
        "coverage_score": round(overall_cov, 4),
    }
    
    print(f"  {'OVERALL':<35} {total_cur:>5} {total_matched:>6} {overall_cov*100:>7.1f}%")
    
    # ── Save ──
    output = {
        "description": "Curriculum Coverage Score — 教材对NRW课标的覆盖率",
        "curriculum_source": "Kernlehrplan Mathematik NRW (Sek I 2019 + Sek II 2023)",
        "textbook_source": "LinguaGraph math_full.json (197 concepts)",
        "methodology": "Keyword + mapping-based concept matching (de→zh bridge)",
        "coverage_by_stage": results,
        "concept_matches_sample": {},
    }
    
    # Add sample matches for each stage
    for stage_key in stage_order:
        stage_concepts = cur_by_stage.get(stage_key, [])
        matched_concepts = [(cc["name"], cc["display_name"][:60], matches[cc["name"]][:3])
                           for cc in stage_concepts if matches.get(cc["name"])]
        output["concept_matches_sample"][stage_key] = matched_concepts[:5]
    
    out_path = PROJECT_ROOT / "config" / "expert_graphs" / "coverage_scores.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n  Written: {out_path}")
    print(f"\n{'='*60}")
    print(f"OVERALL COVERAGE: {overall_cov*100:.1f}%")
    print(f"  ({total_matched}/{total_cur} curriculum concepts matched)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
