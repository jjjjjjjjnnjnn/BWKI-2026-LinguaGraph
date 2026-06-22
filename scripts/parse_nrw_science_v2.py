"""
parse_nrw_science_v2.py — 解析 NRW 物理/化学 Kernlehrplan (v2: 动态章节匹配)
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
    # Sek II
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
    # Sek II
    "IF11": {"de": "Organische Stoffklassen", "en": "Organic Substance Classes", "zh": "有机物类别"},
    "IF12": {"de": "Reaktionsgeschwindigkeit und chemisches Gleichgewicht", "en": "Reaction Rate and Equilibrium", "zh": "反应速率与化学平衡"},
    "IF13": {"de": "Säuren, Basen und analytische Verfahren", "en": "Acids, Bases and Analytical Methods", "zh": "酸碱与分析方法"},
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


def find_stage_sections(text):
    """
    Dynamically find stage sections.
    Returns dict of stage_key → section_text.
    """
    result = {}
    
    # Find all stage markers ( Sek I + Sek II )
    markers = []
    for pattern, key in [
        (r'(?:Ende\s+der\s+)?Erprobungsstufe', "seki_erprobung"),
        (r'(?:Ende\s+der\s+)?Erste\s+Stufe', "seki_stufe1"),
        (r'(?:Ende\s+der\s+)?Zweite\s+Stufe', "seki_stufe2"),
        (r'(?:Ende\s+der\s+)?Einführungsphase', "sekii_einfuehrung"),
        (r'(?:bis\s+zum\s+Ende\s+der\s+)?Qualifikationsphase', "sekii_grundkurs"),
        (r'Leistungskurs', "sekii_leistungskurs"),
    ]:
        for m in re.finditer(pattern, text):
            markers.append((m.start(), key))
    
    markers.sort()
    
    # Extract sections between markers
    for i, (pos, key) in enumerate(markers):
        end = markers[i+1][0] if i+1 < len(markers) else len(text)
        if key not in result:  # Don't overwrite earlier match
            result[key] = text[pos:end]
    
    return result


def parse_inhaltsfelder(section_text, inhaltsfelder):
    """Parse Inhaltsfelder and their Schwerpunkte/Kompetenzerwartungen from a section."""
    result = {}
    
    field_names = [v["de"] for v in inhaltsfelder.values()]
    field_key_map = {v["de"]: k for k, v in inhaltsfelder.items()}
    
    # Build pattern to match "Inhaltsfeld N: Name" or just "Name" at line start
    escaped = '|'.join(re.escape(name) for name in field_names)
    # Match Inhaltsfelder: "Inhaltsfeld N: Name" followed by newline OR content
    parts = re.split(rf'(?:Inhaltsfeld\s+\d+:\s*)?({escaped})\s*[\n]', section_text)
    
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        content = parts[i+1] if i+1 < len(parts) else ""
        
        field_key = field_key_map.get(header)
        if not field_key:
            continue
        
        # Extract Schwerpunkte (bullet points after "Inhaltliche Schwerpunkte:")
        topics = []
        sp_match = re.search(r'Inhaltliche Schwerpunkte:\s*\n', content)
        if sp_match:
            sp_text = content[sp_match.end():]
            for line in sp_text.split('\n'):
                line = line.strip()
                if line.startswith('–') or line.startswith('•') or line.startswith('-'):
                    topic = line.lstrip('–•-').strip()
                    if topic and len(topic) > 3:
                        topics.append(topic)
                elif line.startswith('Die Schülerinnen') or line.startswith('Die Schüler'):
                    break
                elif re.match(r'^(?:Umgang|Erkenntnis|Kommunikation|Bewertung|Beiträge)', line):
                    break
        
        # Extract Kompetenzerwartungen (numbered items)
        competencies = []
        comp_patterns = [
            r'Die Schüler(?:innen und Schüler)?\s*können\s*\n',
            r'Die Schüler(?:innen und Schüler)?\s*können',
        ]
        for cp in comp_patterns:
            cm = re.search(cp, content)
            if cm:
                comp_text = content[cm.end():]
                for line in comp_text.split('\n'):
                    line = line.strip()
                    # Match numbered items or bullet items with (cid:...) 
                    num_match = re.match(r'[\(（]?\d+[\)）]?\s*(.+)', line)
                    if num_match:
                        competencies.append(num_match.group(1).strip())
                    elif line.startswith('•') or line.startswith('\uf0a7') or line.startswith('(cid:'):
                        cleaned = line.replace('\uf0a7', '').lstrip('•(cid:').strip()
                        if cleaned and len(cleaned) > 5:
                            competencies.append(cleaned)
                break
        
        if topics or competencies:
            result[field_key] = {"topics": topics, "competencies": competencies}
    
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
    print("NRW Science Kernlehrplan Parser (v2)")
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
            else:
                print(f"  MISSING: {filename}")
        
        if not all_text:
            print(f"  No data for {subject_name}")
            continue
        
        # Find stage sections dynamically
        stage_sections = find_stage_sections(all_text)
        print(f"  Found stages: {list(stage_sections.keys())}")
        
        # Parse Inhaltsfelder for each stage
        parsed = {}
        for stage_key, section_text in stage_sections.items():
            fields = parse_inhaltsfelder(section_text, inhaltsfelder)
            if fields:
                parsed[stage_key] = fields
                total = sum(len(v.get("topics", [])) + len(v.get("competencies", [])) for v in fields.values())
                print(f"  {stage_key}: {len(fields)} fields, {total} items")
        
        total_items = sum(sum(len(v.get("topics", [])) + len(v.get("competencies", [])) for v in d.values()) for d in parsed.values())
        print(f"  Total: {total_items} items across {len(parsed)} stages")
        
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
