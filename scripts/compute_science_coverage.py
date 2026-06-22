"""
compute_science_coverage.py — 物理/化学课标覆盖率计算
"""

import json
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GRAPH_DIR = PROJECT_ROOT / "config" / "expert_graphs"

# Cross-language keyword bridge for science
SCIENCE_BRIDGE = {
    'kraft': ['力', 'force'], 'bewegung': ['运动', 'motion'], 'energie': ['能量', 'energy'],
    'geschwindigkeit': ['速度', 'velocity'], 'beschleunigung': ['加速度', 'acceleration'],
    'masse': ['质量', 'mass'], 'temperatur': ['温度', 'temperature'],
    'wärme': ['热', 'heat'], 'schall': ['声', 'sound'], 'licht': ['光', 'light'],
    'elektrizität': ['电', 'electricity'], 'magnetismus': ['磁', 'magnetism'],
    'stern': ['恒星', 'star'], 'weltall': ['宇宙', 'universe'],
    'druck': ['压强', 'pressure'], 'auftrieb': ['浮力', 'buoyancy'],
    'strahlung': ['辐射', 'radiation'], 'kern': ['核', 'nuclear'],
    'energieversorgung': ['能源', 'energy supply'],
    'mechanik': ['力学', 'mechanics'], 'gravitation': ['引力', 'gravity'],
    'welle': ['波', 'wave'], 'quanten': ['量子', 'quantum'],
    'elektrodynamik': ['电动力学', 'electrodynamics'],
    'induktion': ['感应', 'induction'],
    'stoff': ['物质', 'substance'], 'eigenschaft': ['性质', 'property'],
    'reaktion': ['反应', 'reaction'], 'verbrennung': ['燃烧', 'combustion'],
    'metall': ['金属', 'metal'], 'element': ['元素', 'element'],
    'salz': ['盐', 'salt'], 'ion': ['离子', 'ion'],
    'molekül': ['分子', 'molecule'], 'säure': ['酸', 'acid'],
    'base': ['碱', 'base'], 'organisch': ['有机', 'organic'],
    'sauerstoff': ['氧', 'oxygen'], 'wasserstoff': ['氢', 'hydrogen'],
    'kohlenstoff': ['碳', 'carbon'], 'stickstoff': ['氮', 'nitrogen'],
    'energie': ['能量', 'energy'], 'kraft': ['力', 'force'],
    'bewegung': ['运动', 'motion'], 'welle': ['波', 'wave'],
    'elektrizität': ['电', 'electricity'], 'magnetismus': ['磁', 'magnetism'],
    'optik': ['光学', 'optics'], 'thermodynamik': ['热力学', 'thermodynamics'],
    'cell': ['细胞', 'cell'], 'organ': ['器官', 'organ'],
    'ecosystem': ['生态系统', 'ecosystem'], 'evolution': ['进化', 'evolution'],
    'genetic': ['遗传', 'genetic'], 'atom': ['原子', 'atom'],
    'molecule': ['分子', 'molecule'], 'compound': ['化合物', 'compound'],
    'reaction': ['反应', 'reaction'], 'bond': ['键', 'bond'],
    'energy': ['能量', 'energy'], 'force': ['力', 'force'],
    'wave': ['波', 'wave'], 'electric': ['电', 'electric'],
    'magnet': ['磁', 'magnet'], 'light': ['光', 'light'],
    'earth': ['地球', 'earth'], 'space': ['空间', 'space'],
}


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_keywords(text):
    text = text.lower()
    text = re.sub(r'[,;:()\[\]{}]', ' ', text)
    return {w for w in text.split() if len(w) > 2}


def match_to_textbook(cur_concepts, tb_concepts, lang='de'):
    matches = {}
    
    tb_kw = {}
    for tc in tb_concepts:
        kws = set()
        for label in tc.get("labels", {}).values():
            kws |= extract_keywords(label)
        name_parts = tc["name"].replace("_", " ").split()
        kws |= {p.lower() for p in name_parts if len(p) > 2}
        tb_kw[tc["name"]] = kws
    
    for cc in cur_concepts:
        label = cc.get("labels", {}).get(lang, "")
        cc_kws = extract_keywords(label)
        
        cn_kws = set()
        for kw in cc_kws:
            if kw in SCIENCE_BRIDGE:
                cn_kws |= set(SCIENCE_BRIDGE[kw])
        
        all_kws = cc_kws | cn_kws
        matched = []
        for tc in tb_concepts:
            overlap = all_kws & tb_kw.get(tc["name"], set())
            if overlap:
                matched.append(tc["name"])
        
        matches[cc["name"]] = matched[:5]
    
    return matches


def compute_coverage(cur_concepts, matches):
    matched = sum(1 for cc in cur_concepts if matches.get(cc["name"]))
    total = len(cur_concepts)
    return matched, total, matched / max(total, 1)


def main():
    print("=" * 60)
    print("Science Coverage Scores")
    print("=" * 60)
    
    # Load textbook graphs
    physics_tb = load_json(GRAPH_DIR / "physics_full.json")["concepts"]
    chemistry_tb = load_json(GRAPH_DIR / "chemistry_full.json")["concepts"]
    
    print(f"Textbook: Physics {len(physics_tb)} concepts, Chemistry {len(chemistry_tb)} concepts")
    
    curricula = {
        "NRW Physik": ("curriculum_nrw_physik.json", "de", physics_tb),
        "NRW Chemie": ("curriculum_nrw_chemie.json", "de", chemistry_tb),
        "UK Science": ("curriculum_uk_science.json", "en", physics_tb + chemistry_tb),
        "US NGSS": ("curriculum_us_science.json", "en", physics_tb + chemistry_tb),
    }
    
    for name, (file, lang, tb) in curricula.items():
        print(f"\n[{name}]")
        data = load_json(GRAPH_DIR / file)
        concepts = data["concepts"]
        print(f"  Concepts: {len(concepts)}")
        
        matches = match_to_textbook(concepts, tb, lang)
        matched, total, cov = compute_coverage(concepts, matches)
        print(f"  Matched: {matched}/{total} = {cov*100:.1f}%")
    
    print(f"\n{'='*60}")
    print("DONE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
