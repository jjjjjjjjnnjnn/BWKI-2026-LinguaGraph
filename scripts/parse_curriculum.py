"""
parse_curriculum.py — 解析 NRW Kernlehrplan Mathematik PDF → 结构化概念图谱

策略：基于 PDF 文本提取 + 规则解析（不依赖 LLM）
输出：config/expert_graphs/curriculum_nrw_math.json（与 math_full.json 格式统一）
"""

import json
import re
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("ERROR: pdfplumber not installed. Run: pip install pdfplumber")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "curricula"
OUTPUT_DIR = PROJECT_ROOT / "config" / "expert_graphs"

# ── Stage definitions ──────────────────────────────────────────────────────
# NRW Gymnasium: 5 years Sek I + 3 years Sek II
STAGES = {
    "seki_erprobung": {"grades": "5-6", "level": "middle", "label_de": "Erprobungsstufe (5-6)"},
    "seki_stufe1":     {"grades": "7-8", "level": "middle", "label_de": "Erste Stufe (7-8)"},
    "seki_stufe2":     {"grades": "9-10", "level": "high",  "label_de": "Zweite Stufe (9-10)"},
    "sekii_einfuehrung": {"grades": "11", "level": "high",    "label_de": "Einführungsphase (11)"},
    "sekii_grundkurs":   {"grades": "12-13", "level": "college", "label_de": "Grundkurs (12-13)"},
    "sekii_leistungskurs": {"grades": "12-13", "level": "college", "label_de": "Leistungskurs (12-13)"},
}

# ── Inhaltsfelder (content areas) ──────────────────────────────────────────
# Sek I uses simple names, Sek II uses expanded names with letter codes
INHALTSFELDER = {
    "Ari": {"de": "Arithmetik/Algebra", "en": "Arithmetic/Algebra", "zh": "算术/代数"},
    "Fkt": {"de": "Funktionen", "en": "Functions", "zh": "函数"},
    "Geo": {"de": "Geometrie", "en": "Geometry", "zh": "几何"},
    "Sto": {"de": "Stochastik", "en": "Stochastics", "zh": "概率统计"},
    # Sek II expanded names
    "Ana": {"de": "Funktionen und Analysis", "en": "Functions and Analysis", "zh": "函数与分析"},
    "Lin": {"de": "Lineare Algebra", "en": "Linear Algebra", "zh": "线性代数"},
    "Num": {"de": "Numerik", "en": "Numerics", "zh": "数值计算"},
}

# Map Sek II field names to our keys
SEKII_FIELD_MAP = {
    "Funktionen und Analysis": "Ana",
    "Arithmetik/Algebra": "Ari",
    "Lineare Algebra": "Lin",
    "Geometrie": "Geo",
    "Stochastik": "Sto",
    "Numerik": "Num",
}

# ── Competency areas (process-oriented) ────────────────────────────────────
KOMPETENZBEREICHE = {
    "Ope": {"de": "Operieren", "en": "Operating", "zh": "运算"},
    "Mod": {"de": "Modellieren", "en": "Modeling", "zh": "建模"},
    "Pro": {"de": "Problemlösen", "en": "Problem Solving", "zh": "问题解决"},
    "Arg": {"de": "Argumentieren", "en": "Arguing", "zh": "论证"},
    "Kom": {"de": "Kommunizieren", "en": "Communicating", "zh": "交流"},
}


def extract_text(pdf_path: Path) -> str:
    """Extract all text from a PDF."""
    texts = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                texts.append(t)
    return "\n".join(texts)


def parse_seki(text: str) -> dict:
    """
    Parse Sek I Kernlehrplan text.
    Returns: {stage_key: {inhaltsfeld: [topics]}}
    """
    result = {}
    
    # Find the Erprobungsstufe section (grades 5-6)
    # Pattern: "Inhaltliche Schwerpunkte:" followed by bullet points
    # Then "Die Schülerinnen und Schüler" followed by numbered items
    
    # Split by stage markers
    sections = re.split(r'(?:2\.3\s+Kompetenzerwartungen|2\.4\.1\s+Erste Stufe|2\.4\.2\s+Zweite Stufe)', text)
    
    # ── Erprobungsstufe (5-6) ──
    if len(sections) > 1:
        sec = sections[1]
        result["seki_erprobung"] = _parse_inhaltsfelder(sec)
    
    # ── Erste Stufe (7-8) ──
    if len(sections) > 2:
        sec = sections[2]
        result["seki_stufe1"] = _parse_inhaltsfelder(sec)
    
    # ── Zweite Stufe (9-10) ──
    if len(sections) > 3:
        sec = sections[3]
        result["seki_stufe2"] = _parse_inhaltsfelder(sec)
    
    return result


def parse_sekii(text: str) -> dict:
    """
    Parse Sek II Kernlehrplan text.
    Returns: {stage_key: {inhaltsfeld_key: [topics]}}
    """
    result = {}
    
    # Find section boundaries by content markers
    # Einführungsphase: after "2.3 Kompetenzerwartungen" and "Einführungsphase"
    # Grundkurs: after "2.4.1 Grundkurs"
    # Leistungskurs: after "2.4.2 Leistungskurs"
    
    # Split on section markers
    parts = re.split(r'(?:2\.3\s+Kompetenzerwartungen|2\.4\.1\s+Grundkurs|2\.4\.2\s+Leistungskurs)', text)
    
    # ── Einführungsphase (11) ──
    if len(parts) > 1:
        result["sekii_einfuehrung"] = _parse_sekii_inhaltsfelder(parts[1])
    
    # ── Grundkurs (12-13) ──
    if len(parts) > 2:
        result["sekii_grundkurs"] = _parse_sekii_inhaltsfelder(parts[2])
    
    # ── Leistungskurs (12-13) ──
    if len(parts) > 3:
        result["sekii_leistungskurs"] = _parse_sekii_inhaltsfelder(parts[3])
    
    return result


def _parse_sekii_inhaltsfelder(section_text: str) -> dict:
    """
    Parse Inhaltsfelder from a Sek II section.
    Sek II uses different field names (e.g., "Funktionen und Analysis (A)")
    and bullet points with • instead of –.
    
    Strategy: Find each "Inhaltliche Schwerpunkte:" marker, look backwards
    to find the field name, then extract bullet points.
    """
    result = {}
    
    # Find all "Inhaltliche Schwerpunkte:" positions
    markers = list(re.finditer(r'Inhaltliche Schwerpunkte:', section_text))
    
    for i, marker in enumerate(markers):
        # Look backwards from marker to find the field name
        before = section_text[max(0, marker.start()-500):marker.start()]
        
        field_key = None
        for name, key in SEKII_FIELD_MAP.items():
            if name in before:
                field_key = key
                break
        
        if not field_key:
            continue
        
        # Extract text after marker until next marker or end
        start = marker.end()
        end = markers[i+1].start() if i+1 < len(markers) else len(section_text)
        chunk = section_text[start:end]
        
        # Extract bullet points (• or – or -)
        topics = []
        for line in chunk.split('\n'):
            line = line.strip()
            if line.startswith('•') or line.startswith('–') or line.startswith('-'):
                topic = line.lstrip('•–-').strip()
                if topic and len(topic) > 3:
                    topics.append(topic)
            elif line.startswith('Die Schülerinnen') or line.startswith('Die Schüler'):
                break
        
        if topics:
            if field_key in result:
                result[field_key].extend(topics)
            else:
                result[field_key] = topics
    
    return result


def _parse_inhaltsfelder(section_text: str) -> dict:
    """
    Parse Inhaltsfelder from a curriculum section.
    Returns: {inhaltsfeld_key: [topic_strings]}
    """
    result = {}
    
    # Find Inhaltsfeld sections by their German names
    # Pattern: "Arithmetik/Algebra" or "Funktionen" or "Geometrie" or "Stochastik"
    # followed by "Inhaltliche Schwerpunkte:" and bullet points
    
    # Split by Inhaltsfeld headers
    parts = re.split(
        r'(?:^|\n)\s*(?:Arithmetik/Algebra|Funktionen|Geometrie|Stochastik)\s*\n',
        section_text
    )
    
    # Map parts to keys based on order
    field_keys = ["Ari", "Fkt", "Geo", "Sto"]
    
    for i, part in enumerate(parts[1:], 0):  # Skip first part (before any field)
        if i >= len(field_keys):
            break
        
        key = field_keys[i]
        topics = _extract_schwerpunkte(part)
        if topics:
            result[key] = topics
    
    return result


def _extract_schwerpunkte(text: str) -> list:
    """
    Extract Inhaltliche Schwerpunkte (topic bullet points) from a section.
    Returns list of topic strings.
    """
    topics = []
    
    # Find "Inhaltliche Schwerpunkte:" marker
    match = re.search(r'Inhaltliche Schwerpunkte:\s*\n', text)
    if not match:
        return topics
    
    after_marker = text[match.end():]
    
    # Extract bullet points (lines starting with – or -)
    for line in after_marker.split('\n'):
        line = line.strip()
        if line.startswith('–') or line.startswith('-'):
            topic = line.lstrip('–-').strip()
            if topic and len(topic) > 3:
                topics.append(topic)
        elif line.startswith('Die Schülerinnen') or line.startswith('Die Schüler'):
            break  # End of Schwerpunkte, start of Competency expectations
    
    return topics


def build_concepts(seki_data: dict, sekii_data: dict) -> list:
    """
    Build concept list from parsed curriculum data.
    Each concept = one Schwerpunkt topic within an Inhaltsfeld at a specific stage.
    """
    concepts = []
    
    for stage_key, stage_info in STAGES.items():
        # Get data for this stage
        stage_data = seki_data.get(stage_key) or sekii_data.get(stage_key)
        if not stage_data:
            continue
        
        for field_key, topics in stage_data.items():
            field_info = INHALTSFELDER[field_key]
            
            for topic in topics:
                # Create concept name from topic
                # Clean up the topic string
                clean_topic = topic.strip()
                if not clean_topic:
                    continue
                
                # Generate a stable concept name
                concept_name = _topic_to_name(field_key, stage_key, clean_topic)
                
                concepts.append({
                    "name": concept_name,
                    "display_name": clean_topic,
                    "category": "concept",
                    "level": stage_info["level"],
                    "labels": {
                        "de": clean_topic,
                        "en": field_info["en"],
                        "zh": field_info["zh"],
                    },
                    "source": f"Kernlehrplan Mathematik NRW {'2019' if 'seki' in stage_key else '2023'}",
                    "stage": stage_key,
                    "stage_label": stage_info["label_de"],
                    "inhaltsfeld": field_key,
                    "inhaltsfeld_de": field_info["de"],
                })
    
    return concepts


def _topic_to_name(field_key: str, stage_key: str, topic: str) -> str:
    """Generate a stable concept name from topic text."""
    # Take first ~40 chars, sanitize for use as identifier
    short = topic[:50].strip()
    # Remove special chars, keep alphanumeric and underscores
    sanitized = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s]', '', short)
    sanitized = re.sub(r'\s+', '_', sanitized).strip('_')
    return f"curriculum_nrw_{field_key}_{stage_key}_{sanitized}"


def build_relations(concepts: list) -> list:
    """
    Build prerequisite relations between concepts.
    Simple rule: concepts in earlier stages are prerequisites for later stages
    within the same Inhaltsfeld.
    """
    relations = []
    
    # Group by stage + field
    grouped = {}
    for c in concepts:
        key = (c["stage"], c["inhaltsfeld"])
        grouped.setdefault(key, []).append(c)
    
    # Sort stages chronologically
    stage_order = list(STAGES.keys())
    
    for field_key in INHALTSFELDER.keys():
        prev_concepts = []
        for stage_key in stage_order:
            current = grouped.get((stage_key, field_key), [])
            # Each concept in previous stage is prerequisite for each in current
            for prev_c in prev_concepts:
                for curr_c in current:
                    relations.append({
                        "source": prev_c["name"],
                        "target": curr_c["name"],
                        "type": "prerequisite",
                        "relation": "prerequisite",
                    })
            prev_concepts.extend(current)
    
    return relations


def main():
    print("=" * 60)
    print("LinguaGraph — NRW Kernlehrplan Parser")
    print("=" * 60)
    
    # ── Step 1: Extract text ──
    print("\n[1/4] Extracting PDF text...")
    seki_path = DATA_DIR / "nrw_seki_mathematik_2019.pdf"
    sekii_path = DATA_DIR / "nrw_sekii_mathematik_2023.pdf"
    
    if not seki_path.exists():
        print(f"ERROR: {seki_path} not found. Download first.")
        sys.exit(1)
    if not sekii_path.exists():
        print(f"ERROR: {sekii_path} not found. Download first.")
        sys.exit(1)
    
    seki_text = extract_text(seki_path)
    sekii_text = extract_text(sekii_path)
    print(f"  Sek I: {len(seki_text)} chars extracted")
    print(f"  Sek II: {len(sekii_text)} chars extracted")
    
    # ── Step 2: Parse structure ──
    print("\n[2/4] Parsing curriculum structure...")
    seki_data = parse_seki(seki_text)
    sekii_data = parse_sekii(sekii_text)
    
    for stage_key in STAGES:
        data = seki_data.get(stage_key) or sekii_data.get(stage_key)
        if data:
            total_topics = sum(len(v) for v in data.values())
            print(f"  {STAGES[stage_key]['label_de']}: {len(data)} fields, {total_topics} topics")
        else:
            print(f"  {STAGES[stage_key]['label_de']}: (no data parsed)")
    
    # ── Step 3: Build concepts ──
    print("\n[3/4] Building concept graph...")
    concepts = build_concepts(seki_data, sekii_data)
    relations = build_relations(concepts)
    print(f"  Concepts: {len(concepts)}")
    print(f"  Relations: {len(relations)}")
    
    # ── Step 4: Export ──
    print("\n[4/4] Exporting JSON...")
    output = {
        "version": "2.0",
        "domain": "curriculum_nrw_math",
        "description": "NRW Kernlehrplan Mathematik — 课程标准概念图谱（Sek I + Sek II）",
        "languages": ["de", "en", "zh"],
        "created": "2026-06-22",
        "pipeline": "scripts/parse_curriculum.py",
        "source_documents": [
            "Kernlehrplan Mathematik NRW Sek I (2019)",
            "Kernlehrplan Mathematik NRW Sek II (2023)",
        ],
        "concepts": concepts,
        "relations": relations,
        "metadata": {
            "total_concepts": len(concepts),
            "total_relations": len(relations),
            "inhaltsfelder": list(INHALTSFELDER.keys()),
            "stages": list(STAGES.keys()),
        },
    }
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "curriculum_nrw_math.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"  Written: {out_path}")
    print(f"\n{'=' * 60}")
    print(f"DONE: {len(concepts)} concepts, {len(relations)} relations")
    print(f"{'=' * 60}")
    
    # ── Summary by field ──
    print("\nConcepts by Inhaltsfeld:")
    from collections import Counter
    field_counts = Counter(c["inhaltsfeld"] for c in concepts)
    for fk, cnt in field_counts.most_common():
        print(f"  {INHALTSFELDER[fk]['de']}: {cnt} concepts")
    
    print("\nConcepts by stage:")
    stage_counts = Counter(c["stage"] for c in concepts)
    for sk, cnt in stage_counts.most_common():
        print(f"  {STAGES[sk]['label_de']}: {cnt} concepts")


if __name__ == "__main__":
    main()
