"""
parse_nrw_science_v3.py — NRW 物理/化学 Kernlehrplan (v3: 全局 Inhaltsfelder 提取)
"""

import json
import re
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("ERROR: pdfplumber not installed")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "curricula"
OUTPUT_DIR = PROJECT_ROOT / "config" / "expert_graphs"

STAGES = {
    "seki_erprobung": {"grades": "5-6", "level": "middle", "label": "Erprobungsstufe (5-6)"},
    "seki_stufe1":     {"grades": "7-8", "level": "middle", "label": "Erste Stufe (7-8)"},
    "seki_stufe2":     {"grades": "9-10", "level": "high",  "label": "Zweite Stufe (9-10)"},
    "sekii_einfuehrung": {"grades": "11", "level": "high",    "label": "Einführungsphase (11)"},
    "sekii_grundkurs":   {"grades": "12-13", "level": "college", "label": "Grundkurs (12-13)"},
    "sekii_leistungskurs": {"grades": "12-13", "level": "college", "label": "Leistungskurs (12-13)"},
}

PHYSICS_INHALTSFELDER = {
    "IF1":  {"de": "Temperatur und Wärme", "en": "Temperature and Heat", "zh": "温度与热"},
    "IF2":  {"de": "Elektrischer Strom und Magnetismus", "en": "Electric Current and Magnetism", "zh": "电流与磁"},
    "IF3":  {"de": "Schall", "en": "Sound", "zh": "声"},
    "IF4":  {"de": "Licht", "en": "Light", "zh": "光"},
    "IF5":  {"de": "Optische Instrumente", "en": "Optical Instruments", "zh": "光学仪器"},
    "IF6":  {"de": "Sterne und Weltall", "en": "Stars and Universe", "zh": "恒星与宇宙"},
    "IF7":  {"de": "Bewegung, Kraft und Energie", "en": "Motion, Force and Energy", "zh": "运动、力与能量"},
    "IF8":  {"de": "Druck und Auftrieb", "en": "Pressure and Buoyancy", "zh": "压强与浮力"},
    "IF9":  {"de": "Elektrizität", "en": "Electricity", "zh": "电学"},
    "IF10": {"de": "Ionisierende Strahlung und Kernenergie", "en": "Ionizing Radiation", "zh": "电离辐射"},
    "IF11": {"de": "Energieversorgung", "en": "Energy Supply", "zh": "能源供应"},
    "IF12": {"de": "Grundlagen der Mechanik", "en": "Mechanics Foundations", "zh": "力学基础"},
    "IF13": {"de": "Kreisbewegung, Gravitation und physikalische Weltbilder", "en": "Circular Motion and Gravity", "zh": "圆周运动与引力"},
    "IF14": {"de": "Klassische Wellen und geladene Teilchen in Feldern", "en": "Classical Waves and Charged Particles", "zh": "经典波与带电粒子"},
    "IF15": {"de": "Quantenobjekte", "en": "Quantum Objects", "zh": "量子客体"},
    "IF16": {"de": "Elektrodynamik und Energieübertragung", "en": "Electrodynamics and Energy Transfer", "zh": "电动力学与能量传输"},
    "IF17": {"de": "Strahlung und Materie", "en": "Radiation and Matter", "zh": "辐射与物质"},
    "IF18": {"de": "Ladungen, Felder und Induktion", "en": "Charges, Fields and Induction", "zh": "电荷、场与感应"},
    "IF19": {"de": "Schwingende Systeme und Wellen", "en": "Oscillating Systems and Waves", "zh": "振动系统与波"},
    "IF20": {"de": "Quantenphysik", "en": "Quantum Physics", "zh": "量子物理"},
    "IF21": {"de": "Atom- und Kernphysik", "en": "Atomic and Nuclear Physics", "zh": "原子与核物理"},
}

CHEMISTRY_INHALTSFELDER = {
    "IF1":  {"de": "Stoffe und Stoffeigenschaften", "en": "Substances and Properties", "zh": "物质与性质"},
    "IF2":  {"de": "Chemische Reaktion", "en": "Chemical Reactions", "zh": "化学反应"},
    "IF3":  {"de": "Verbrennung", "en": "Combustion", "zh": "燃烧"},
    "IF4":  {"de": "Metalle und Metallgewinnung", "en": "Metals and Metal Extraction", "zh": "金属与冶金"},
    "IF5":  {"de": "Elemente und ihre Ordnung", "en": "Elements and Their Order", "zh": "元素规律"},
    "IF6":  {"de": "Salze und Ionen", "en": "Salts and Ions", "zh": "盐与离子"},
    "IF7":  {"de": "Metalle und Anwendungen", "en": "Metals and Applications", "zh": "金属应用"},
    "IF8":  {"de": "Molekülverbindungen", "en": "Molecular Compounds", "zh": "分子化合物"},
    "IF9":  {"de": "Saure und alkalische Lösungen", "en": "Acid and Alkaline Solutions", "zh": "酸碱溶液"},
    "IF10": {"de": "Organische Chemie", "en": "Organic Chemistry", "zh": "有机化学"},
    "IF11": {"de": "Organische Stoffklassen", "en": "Organic Substance Classes", "zh": "有机物类别"},
    "IF12": {"de": "Reaktionsgeschwindigkeit und chemisches Gleichgewicht", "en": "Reaction Rate and Equilibrium", "zh": "反应速率与平衡"},
    "IF13": {"de": "Säuren, Basen und analytische Verfahren", "en": "Acids, Bases and Analytical Methods", "zh": "酸碱与分析"},
    "IF14": {"de": "Elektrochemische Prozesse und Energetik", "en": "Electrochemical Processes", "zh": "电化学过程"},
    "IF15": {"de": "Reaktionswege in der organischen Chemie", "en": "Organic Reaction Pathways", "zh": "有机反应路径"},
    "IF16": {"de": "Moderne Werkstoffe", "en": "Modern Materials", "zh": "现代材料"},
}


def extract_text(pdf_path):
    texts = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                texts.append(t)
    return "\n".join(texts)


def find_stage_content(text):
    """
    Find ACTUAL stage content sections (skip ToC).
    Look for "Am Ende der..." or "Kompetenzerwartungen und inhaltliche Schwerpunkte bis zum"
    """
    result = {}
    
    # Find actual content sections by their heading patterns
    patterns = [
        (r'Am Ende der Erprobungsstufe', "seki_erprobung"),
        (r'Am Ende der Ersten Stufe', "seki_stufe1"),
        (r'Am Ende der Zweiten Stufe', "seki_stufe2"),
        (r'Am Ende der Einführungsphase', "sekii_einfuehrung"),
        (r'Am Ende der Qualifikationsphase.*?Grundkurs', "sekii_grundkurs"),
        (r'Am Ende der Qualifikationsphase.*?Leistungskurs', "sekii_leistungskurs"),
    ]
    
    markers = []
    for pat, key in patterns:
        for m in re.finditer(pat, text):
            markers.append((m.start(), key))
    
    markers.sort()
    
    for i, (pos, key) in enumerate(markers):
        end = markers[i+1][0] if i+1 < len(markers) else len(text)
        if key not in result:
            result[key] = text[pos:end]
    
    return result


def parse_inhaltsfelder_global(text, inhaltsfelder):
    """
    Parse Inhaltsfelder from the ENTIRE text.
    Find "Inhaltliche Schwerpunkte:" markers and associate with nearest Inhaltsfeld name.
    """
    result = {}
    
    field_names = {v["de"]: k for k, v in inhaltsfelder.items()}
    
    # Find all "Inhaltliche Schwerpunkte:" markers
    markers = list(re.finditer(r'Inhaltliche Schwerpunkte:', text))
    
    for i, marker in enumerate(markers):
        # Look backwards to find the Inhaltsfeld name
        before = text[max(0, marker.start()-1000):marker.start()]
        
        field_key = None
        for name, key in field_names.items():
            if name in before[-500:]:  # Check last 500 chars before marker
                field_key = key
                break
        
        if not field_key:
            # Try looking for "Inhaltsfeld N:" pattern
            if_match = re.search(r'Inhaltsfeld\s+(\d+)', before[-500:])
            if if_match:
                if_num = int(if_match.group(1))
                for key, info in inhaltsfelder.items():
                    if key.endswith(str(if_num)) or key == f"IF{if_num}":
                        field_key = key
                        break
        
        if not field_key:
            continue
        
        # Extract topics from after marker
        start = marker.end()
        end = markers[i+1].start() if i+1 < len(markers) else len(text)
        chunk = text[start:end]
        
        topics = []
        current = None
        for line in chunk.split('\n'):
            line = line.strip()
            if line.startswith('–') or line.startswith('•') or line.startswith('-'):
                if current:
                    topics.append(current)
                current = line.lstrip('–•-').strip()
            elif current and line and not re.match(r'^(?:Umgang|Erkenntnis|Kommunikation|Bewertung|Beiträge|Die Schüler)', line):
                if len(line) > 3:
                    current += ' ' + line
            elif re.match(r'^(?:Umgang|Erkenntnis|Kommunikation|Bewertung|Beiträge|Die Schüler)', line):
                if current:
                    topics.append(current)
                    current = None
                break
        if current:
            topics.append(current)
        
        # Extract competencies (numbered items)
        competencies = []
        comp_match = re.search(r'Die Schüler(?:innen und Schüler)?\s*können', chunk)
        if comp_match:
            comp_text = chunk[comp_match.end():]
            for line in comp_text.split('\n'):
                line = line.strip()
                num_match = re.match(r'[\(（]?\d+[\)）]?\s*(.+)', line)
                if num_match:
                    competencies.append(num_match.group(1).strip())
                elif line.startswith('•') or line.startswith('\uf0a7'):
                    cleaned = line.replace('\uf0a7', '').lstrip('•').strip()
                    if cleaned and len(cleaned) > 5:
                        competencies.append(cleaned)
        
        if field_key in result:
            result[field_key]["topics"].extend(topics)
            result[field_key]["competencies"].extend(competencies)
        else:
            result[field_key] = {"topics": topics, "competencies": competencies}
    
    return result


def assign_to_stages(global_data, stage_sections, inhaltsfelder):
    """Assign Inhaltsfelder data to stages based on position in text."""
    # For simplicity, assign all Inhaltsfelder to all stages that exist
    # (the Erprobungsstufe covers all Sek I Inhaltsfelder)
    result = {}
    
    for stage_key in stage_sections:
        result[stage_key] = dict(global_data)
    
    return result


def build_graph(stages_def, parsed_data, inhaltsfelder, subject, source_doc):
    concepts = []
    
    for stage_key, stage_info in stages_def.items():
        stage_data = parsed_data.get(stage_key, {})
        
        for field_key, field_data in stage_data.items():
            info = inhaltsfelder.get(field_key, {})
            topics = field_data.get("topics", [])
            competencies = field_data.get("competencies", [])
            
            for topic in topics:
                clean = topic.strip()
                if not clean:
                    continue
                name_part = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s]', '', clean)[:40]
                name_part = re.sub(r'\s+', '_', name_part).strip('_')
                concepts.append({
                    "name": f"curriculum_nrw_{subject}_{field_key}_{stage_key}_{name_part}",
                    "display_name": clean,
                    "category": "concept",
                    "concept_type": "schwerpunkt",
                    "level": stage_info["level"],
                    "labels": {"de": clean, "en": info.get("en", ""), "zh": info.get("zh", "")},
                    "source": source_doc,
                    "stage": stage_key,
                    "stage_label": stage_info["label"],
                    "inhaltsfeld": field_key,
                    "inhaltsfeld_de": info.get("de", ""),
                })
            
            for comp in competencies:
                clean = comp.strip()
                if not clean:
                    continue
                name_part = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s]', '', clean)[:40]
                name_part = re.sub(r'\s+', '_', name_part).strip('_')
                concepts.append({
                    "name": f"curriculum_nrw_{subject}_{field_key}_{stage_key}_{name_part}",
                    "display_name": clean,
                    "category": "competency",
                    "concept_type": "kompetenzerwartung",
                    "level": stage_info["level"],
                    "labels": {"de": clean, "en": info.get("en", ""), "zh": info.get("zh", "")},
                    "source": source_doc,
                    "stage": stage_key,
                    "stage_label": stage_info["label"],
                    "inhaltsfeld": field_key,
                    "inhaltsfeld_de": info.get("de", ""),
                })
    
    relations = []
    grouped = {}
    for c in concepts:
        grouped.setdefault((c["stage"], c["inhaltsfeld"]), []).append(c)
    
    stage_order = list(stages_def.keys())
    for field_key in inhaltsfelder:
        prev = []
        for sk in stage_order:
            curr = grouped.get((sk, field_key), [])
            for pc in prev:
                for cc in curr:
                    relations.append({"source": pc["name"], "target": cc["name"], "type": "prerequisite", "relation": "prerequisite"})
            prev.extend(curr)
    
    return {
        "version": "2.0",
        "domain": f"curriculum_nrw_{subject}",
        "description": f"NRW Kernlehrplan {subject.title()} — 课程标准概念图谱",
        "languages": ["de", "en", "zh"],
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
    print("NRW Science Kernlehrplan Parser (v3)")
    print("=" * 60)
    
    subjects = [
        ("physik", "Physik", PHYSICS_INHALTSFELDER,
         [("nrw_seki_physik_2019.pdf", "Kernlehrplan Physik NRW Sek I (2019)"),
          ("nrw_sekii_physik_2022.pdf", "Kernlehrplan Physik NRW Sek II (2022)")]),
        ("chemie", "Chemie", CHEMISTRY_INHALTSFELDER,
         [("nrw_seki_chemie_2019.pdf", "Kernlehrplan Chemie NRW Sek I (2019)"),
          ("nrw_sekii_chemie_2022.pdf", "Kernlehrplan Chemie NRW Sek II (2022)")]),
    ]
    
    for subject_key, subject_name, inhaltsfelder, files in subjects:
        print(f"\n[{subject_name}]")
        
        all_text = ""
        source_docs = []
        for filename, doc_name in files:
            fp = DATA_DIR / filename
            if fp.exists():
                all_text += extract_text(fp) + "\n"
                source_docs.append(doc_name)
                print(f"  Loaded: {filename}")
        
        if not all_text:
            print(f"  No data for {subject_name}")
            continue
        
        # Parse Inhaltsfelder globally
        global_data = parse_inhaltsfelder_global(all_text, inhaltsfelder)
        total = sum(len(v.get("topics", [])) + len(v.get("competencies", [])) for v in global_data.values())
        print(f"  Global Inhaltsfelder: {len(global_data)} fields, {total} items")
        
        # Find stage sections
        stage_sections = find_stage_content(all_text)
        print(f"  Stage sections: {list(stage_sections.keys())}")
        
        # Assign to stages
        parsed = assign_to_stages(global_data, stage_sections, inhaltsfelder)
        
        graph = build_graph(STAGES, parsed, inhaltsfelder, subject_key, " + ".join(source_docs))
        
        out_path = OUTPUT_DIR / f"curriculum_nrw_{subject_key}.json"
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(graph, f, ensure_ascii=False, indent=2)
        
        print(f"  Written: {out_path} ({graph['metadata']['total_concepts']} concepts)")
    
    print(f"\n{'='*60}")
    print("DONE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
