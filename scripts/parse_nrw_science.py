"""
parse_nrw_science.py — 解析 NRW 物理/化学 Kernlehrplan

策略：与 parse_curriculum.py 相同，但 Inhaltsfelder 名称不同
输出：config/expert_graphs/curriculum_nrw_{physik|chemie}_math.json
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

# ── Subject-specific Inhaltsfelder ─────────────────────────────────────────

PHYSICS_INHALTSFELDER = {
    "IF1":  {"de": "Temperatur und Wärme", "en": "Temperature and Heat", "zh": "温度与热"},
    "IF2":  {"de": "Elektrizität und Magnetismus", "en": "Electricity and Magnetism", "zh": "电与磁"},
    "IF3":  {"de": "Schall", "en": "Sound", "zh": "声"},
    "IF4":  {"de": "Licht", "en": "Light", "zh": "光"},
    "IF5":  {"de": "Optische Instrumente", "en": "Optical Instruments", "zh": "光学仪器"},
    "IF6":  {"de": "Sterne und Weltall", "en": "Stars and Universe", "zh": "恒星与宇宙"},
    "IF7":  {"de": "Bewegung, Kraft und Energie", "en": "Motion, Force and Energy", "zh": "运动、力与能量"},
    "IF8":  {"de": "Druck und Auftrieb", "en": "Pressure and Buoyancy", "zh": "压强与浮力"},
    "IF9":  {"de": "Elektrizität", "en": "Electricity", "zh": "电学"},
    "IF10": {"de": "Ionisierende Strahlung und Kernenergie", "en": "Ionizing Radiation and Nuclear Energy", "zh": "电离辐射与核能"},
    "IF11": {"de": "Energieversorgung", "en": "Energy Supply", "zh": "能源供应"},
}

CHEMISTRY_INHALTSFELDER = {
    "IF1":  {"de": "Stoffe und Stoffeigenschaften", "en": "Substances and Properties", "zh": "物质与性质"},
    "IF2":  {"de": "Chemische Reaktion", "en": "Chemical Reactions", "zh": "化学反应"},
    "IF3":  {"de": "Verbrennung", "en": "Combustion", "zh": "燃烧"},
    "IF4":  {"de": "Metalle und Metallgewinnung", "en": "Metals and Metal Extraction", "zh": "金属与冶金"},
    "IF5":  {"de": "Elemente und ihre Ordnung", "en": "Elements and Their Order", "zh": "元素及其规律"},
    "IF6":  {"de": "Salze und Ionen", "en": "Salts and Ions", "zh": "盐与离子"},
    "IF7":  {"de": "Metalle und Anwendungen", "en": "Metals and Applications", "zh": "金属与应用"},
    "IF8":  {"de": "Molekülverbindungen", "en": "Molecular Compounds", "zh": "分子化合物"},
    "IF9":  {"de": "Saure und alkalische Lösungen", "en": "Acidic and Alkaline Solutions", "zh": "酸碱溶液"},
    "IF10": {"de": "Organische Chemie", "en": "Organic Chemistry", "zh": "有机化学"},
}


def extract_text(pdf_path):
    texts = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                texts.append(t)
    return "\n".join(texts)


def parse_nrw_seki(text, inhaltsfelder):
    """Parse Sek I text → {stage: {field_key: {"topics": [...], "competencies": [...]}}}"""
    result = {}
    
    # Find section markers
    parts = re.split(
        r'(?:2\.3\s+Kompetenzerwartungen|2\.4\.1\s+Erste Stufe|2\.4\.2\s+Zweite Stufe)',
        text
    )
    
    if len(parts) > 1:
        result["seki_erprobung"] = _parse_fields(parts[1], inhaltsfelder)
    if len(parts) > 2:
        result["seki_stufe1"] = _parse_fields(parts[2], inhaltsfelder)
    if len(parts) > 3:
        result["seki_stufe2"] = _parse_fields(parts[3], inhaltsfelder)
    
    return result


def parse_nrw_sekii(text, inhaltsfelder):
    """Parse Sek II text → {stage: {field_key: {"topics": [...], "competencies": [...]}}}"""
    result = {}
    
    pattern = (
        r'(?:2\.3\s+Kompetenzerwartungen und inhaltliche Schwerpunkte'
        r'|2\.4\.1\s+Grundkurs\n'
        r'|2\.4\.2\s+Leistungskurs\n)'
    )
    parts = re.split(pattern, text)
    
    if len(parts) > 2:
        result["sekii_einfuehrung"] = _parse_sekii_fields(parts[2], inhaltsfelder)
    if len(parts) > 3:
        result["sekii_grundkurs"] = _parse_sekii_fields(parts[3], inhaltsfelder)
    if len(parts) > 4:
        result["sekii_leistungskurs"] = _parse_sekii_fields(parts[4], inhaltsfelder)
    
    return result


def _parse_fields(section_text, inhaltsfelder):
    """Parse Inhaltsfelder from a section (Sek I format)."""
    result = {}
    
    # Build pattern: "Inhaltsfeld N: Name" or just "Name" at line start
    field_names = [v["de"] for v in inhaltsfelder.values()]
    field_key_map = {v["de"]: k for k, v in inhaltsfelder.items()}
    
    # Split by "Inhaltsfeld N: Name" pattern
    escaped_names = '|'.join(re.escape(name) for name in field_names)
    parts = re.split(
        rf'(?:^|\n)\s*(?:Inhaltsfeld\s+\d+:\s*)?({escaped_names})\s*\n',
        section_text
    )
    
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        content = parts[i+1] if i+1 < len(parts) else ""
        
        field_key = field_key_map.get(header)
        if not field_key:
            continue
        
        topics = _extract_schwerpunkte(content)
        competencies = _extract_kompetenzerwartungen(content)
        
        if topics or competencies:
            result[field_key] = {"topics": topics, "competencies": competencies}
    
    return result


def _parse_sekii_fields(section_text, inhaltsfelder):
    """Parse Inhaltsfelder from a Sek II section."""
    result = {}
    
    markers = list(re.finditer(r'Inhaltliche Schwerpunkte:', section_text))
    
    for i, marker in enumerate(markers):
        before = section_text[max(0, marker.start()-500):marker.start()]
        
        field_key = None
        for key, info in inhaltsfelder.items():
            if info["de"] in before:
                field_key = key
                break
        
        if not field_key:
            continue
        
        start = marker.end()
        end = markers[i+1].start() if i+1 < len(markers) else len(section_text)
        chunk = section_text[start:end]
        
        topics = []
        for line in chunk.split('\n'):
            line = line.strip()
            if line.startswith('•') or line.startswith('–') or line.startswith('-'):
                topic = line.lstrip('•–-').strip()
                if topic and len(topic) > 3:
                    topics.append(topic)
            elif line.startswith('Die Schülerinnen') or line.startswith('Die Schüler'):
                break
        
        competencies = _extract_kompetenzerwartungen(chunk)
        
        if topics or competencies:
            if field_key in result:
                result[field_key]["topics"].extend(topics)
                result[field_key]["competencies"].extend(competencies)
            else:
                result[field_key] = {"topics": topics, "competencies": competencies}
    
    return result


def _extract_schwerpunkte(text):
    topics = []
    match = re.search(r'Inhaltliche Schwerpunkte:\s*\n', text)
    if not match:
        return topics
    
    after = text[match.end():]
    current = None
    for line in after.split('\n'):
        line = line.strip()
        if line.startswith('–') or line.startswith('•') or line.startswith('-'):
            if current:
                topics.append(current)
            current = line.lstrip('–•-').strip()
        elif current and line and not line.startswith('Die Schülerinnen') and not line.startswith('Die Schüler'):
            if not re.match(r'^[A-Z][a-z]+\s+[A-Z]', line) and len(line) > 5:
                current += ' ' + line
        elif line.startswith('Die Schülerinnen') or line.startswith('Die Schüler'):
            if current:
                topics.append(current)
            break
    if current:
        topics.append(current)
    return topics


def _extract_kompetenzerwartungen(text):
    competencies = []
    match = re.search(r'Die Schüler(?:innen und Schüler)?\s*\n', text)
    if not match:
        return competencies
    
    after = text[match.end():]
    current = None
    for line in after.split('\n'):
        line = line.strip()
        num_match = re.match(r'\((\d+)\)\s+(.+)', line)
        if num_match:
            if current:
                competencies.append(current)
            current = num_match.group(2)
        elif current and line and not re.match(r'\(\d+\)', line):
            if re.match(r'^(?:Inhaltsfeld|Arithmetik|Funktionen|Geometrie|Stochastik|Temperatur|Elektrizität|Schall|Licht|Sterne|Bewegung|Druck|Ionisierende|Energieversorgung|Stoffe|Chemische|Verbrennung|Metalle|Elemente|Salze|Molekül|Saure|Organische)', line):
                competencies.append(current)
                break
            if line.startswith('Die Schülerinnen') or line.startswith('Die Schüler'):
                competencies.append(current)
                break
            current += ' ' + line
    if current:
        competencies.append(current)
    return competencies


def build_graph(stages_def, parsed_data, inhaltsfelder, subject, source_doc):
    """Build concept graph from parsed data."""
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
    
    # Relations
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
    print("NRW Science Kernlehrplan Parser")
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
        print(f"\n[{subject_name}] Parsing...")
        
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
        
        parsed = {}
        parsed.update(parse_nrw_seki(all_text, inhaltsfelder))
        parsed.update(parse_nrw_sekii(all_text, inhaltsfelder))
        
        total = sum(sum(len(v) for v in d.values()) for d in parsed.values())
        print(f"  Stages: {len(parsed)}, Total: {total}")
        
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
