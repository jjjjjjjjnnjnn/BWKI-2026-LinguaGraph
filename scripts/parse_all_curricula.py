"""
parse_all_curricula.py — 统一课标解析器

支持：NRW (已完成)、UK、China、US
输出格式：config/expert_graphs/curriculum_{country}_math.json
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

try:
    import pdfplumber
except ImportError:
    print("ERROR: pdfplumber not installed. Run: pip install pdfplumber")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "curricula"
OUTPUT_DIR = PROJECT_ROOT / "config" / "expert_graphs"


def extract_text(pdf_path):
    texts = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                texts.append(t)
    return "\n".join(texts)


# ══════════════════════════════════════════════════════════════════════════════
# UK National Curriculum Parser
# ══════════════════════════════════════════════════════════════════════════════

UK_STAGES = {
    "uk_ks1_y1":    {"grades": "Y1", "level": "elementary", "label": "Key Stage 1 - Year 1 (ages 5-6)"},
    "uk_ks1_y2":    {"grades": "Y2", "level": "elementary", "label": "Key Stage 1 - Year 2 (ages 6-7)"},
    "uk_ks2_y3":    {"grades": "Y3", "level": "elementary", "label": "Lower KS2 - Year 3 (ages 7-8)"},
    "uk_ks2_y4":    {"grades": "Y4", "level": "elementary", "label": "Lower KS2 - Year 4 (ages 8-9)"},
    "uk_ks2_y5":    {"grades": "Y5", "level": "middle",     "label": "Upper KS2 - Year 5 (ages 9-10)"},
    "uk_ks2_y6":    {"grades": "Y6", "level": "middle",     "label": "Upper KS2 - Year 6 (ages 10-11)"},
    "uk_ks3":       {"grades": "Y7-9", "level": "middle",   "label": "Key Stage 3 (ages 11-14)"},
    "uk_ks4":       {"grades": "Y10-11", "level": "high",   "label": "Key Stage 4 / GCSE (ages 14-16)"},
}

UK_DOMAINS = {
    "Num": {"en": "Number", "de": "Zahlen", "zh": "数与运算"},
    "Alg": {"en": "Algebra", "de": "Algebra", "zh": "代数"},
    "Geo": {"en": "Geometry", "de": "Geometrie", "zh": "几何"},
    "Mea": {"en": "Measurement", "de": "Messung", "zh": "度量"},
    "Sta": {"en": "Statistics", "de": "Stochastik", "zh": "统计"},
    "Rat": {"en": "Ratio and Proportion", "de": "Verhältnis", "zh": "比与比例"},
}


def parse_uk_ks12(text):
    """Parse UK KS1-2 curriculum text → {stage: {domain: [topics]}}"""
    result = {}
    
    # Find year sections (skip first 6 ToC entries)
    year_pattern = r'Year (\d) programme of study'
    year_matches = list(re.finditer(year_pattern, text))
    
    # Only process actual content (skip ToC)
    content_years = [m for m in year_matches if m.start() > 5000]
    
    for i, m in enumerate(content_years):
        year_num = int(m.group(1))
        stage_key = f"uk_ks1_y{year_num}" if year_num <= 2 else f"uk_ks2_y{year_num}"
        
        start = m.end()
        end = content_years[i+1].start() if i+1 < len(content_years) else len(text)
        section = text[start:end]
        
        domains = _extract_uk_domains(section)
        if domains:
            result[stage_key] = domains
    
    return result


def parse_uk_combined(text):
    """Parse combined UK curriculum text (all key stages)."""
    result = {}
    
    # Find all year/ks sections
    year_matches = list(re.finditer(r'Year (\d) programme of study', text))
    
    # Find KS3 and KS4 CONTENT sections (not just mentions)
    # KS3 content: "Mathematics – key stage 3\nKey stage 3\n"
    # KS4 content: "Mathematics – key stage 4\nKey stage 4\n"
    ks3_content = re.search(r'Mathematics\s*[-–—]\s*key stage 3\s*\nKey stage 3\s*\n', text)
    ks4_content = re.search(r'Mathematics\s*[-–—]\s*key stage 4\s*\nKey stage 4\s*\n', text)
    
    # Process Years 1-6 (content only, skip ToC)
    content_years = [m for m in year_matches if m.start() > 5000]
    
    # Determine end of KS2 section
    ks2_end = ks3_content.start() if ks3_content else len(text)
    
    for i, m in enumerate(content_years):
        year_num = int(m.group(1))
        if year_num > 6:
            break
        stage_key = f"uk_ks1_y{year_num}" if year_num <= 2 else f"uk_ks2_y{year_num}"
        
        start = m.end()
        end = content_years[i+1].start() if i+1 < len(content_years) and content_years[i+1].start() < ks2_end else ks2_end
        section = text[start:end]
        
        domains = _extract_uk_domains(section)
        if domains:
            result[stage_key] = domains
    
    # Process KS3
    if ks3_content:
        start = ks3_content.end()
        end = ks4_content.start() if ks4_content else len(text)
        section = text[start:end]
        domains = _extract_uk_domains(section)
        if domains:
            result["uk_ks3"] = domains
    
    # Process KS4
    if ks4_content:
        section = text[ks4_content.end():]
        domains = _extract_uk_domains(section)
        if domains:
            result["uk_ks4"] = domains
    
    return result


def _extract_uk_domains(section_text):
    """
    Extract domain topics from a UK curriculum section.
    Handles: en-dash (–), U+F0A7 bullet, plain text items.
    KS3/KS4 use different header formats.
    """
    result = {}
    
    # Split by domain headers (KS1-2: "Number – ...", KS3/4: "Number\n" or "Number\n")
    # Use a flexible pattern that handles both formats
    domain_pattern = r'(?:^|\n)\s*((?:Number|Algebra|Geometry|Measurement|Statistics|Ratio)[^\n]*)\s*\n'
    
    parts = re.split(domain_pattern, section_text)
    
    # Map domain names to keys
    domain_map = {
        "Number": "Num",
        "Algebra": "Alg",
        "Geometry": "Geo",
        "Measurement": "Mea",
        "Statistics": "Sta",
        "Ratio": "Rat",
    }
    
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        content = parts[i+1] if i+1 < len(parts) else ""
        
        domain_key = None
        for name, key in domain_map.items():
            if header.startswith(name):
                domain_key = key
                break
        
        if not domain_key:
            continue
        
        # Skip "Purpose of study", "Aims", "Notes" sections
        if any(skip in header.lower() for skip in ['purpose', 'aim', 'note', 'glossary']):
            continue
        
        # Extract items: bullet (U+F0A7), en-dash, or just text lines
        topics = []
        current = None
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Match bullet items
            if '\uf0a7' in line or line.startswith('•') or line.startswith('-'):
                if current:
                    topics.append(current)
                # Remove bullet characters
                cleaned = line.replace('\uf0a7', '').lstrip('•-').strip()
                if cleaned and len(cleaned) > 5:
                    current = cleaned
                else:
                    current = None
            # Continuation line
            elif current and not re.match(r'^(?:Number|Algebra|Geometry|Measurement|Statistics|Ratio|Notes|Purpose|Aims|Working|Solve|Subject)', line):
                current += ' ' + line
            else:
                if current:
                    topics.append(current)
                    current = None
                # Stop at next domain or section
                if re.match(r'^(?:Number|Algebra|Geometry|Measurement|Statistics|Ratio)\s*[-–—\n]', line):
                    break
        
        if current:
            topics.append(current)
        
        if topics:
            if domain_key in result:
                result[domain_key].extend(topics)
            else:
                result[domain_key] = topics
    
    return result


def parse_uk_ks3(text):
    """Parse UK KS3 curriculum text."""
    # KS3 is shorter, extract topics directly
    result = {}
    domains = _extract_uk_domains(text)
    if domains:
        result["uk_ks3"] = domains
    return result


def parse_uk_ks4(text):
    """Parse UK KS4 (GCSE) curriculum text."""
    result = {}
    domains = _extract_uk_domains(text)
    if domains:
        result["uk_ks4"] = domains
    return result


# ══════════════════════════════════════════════════════════════════════════════
# China Curriculum Parser (placeholder — will be filled when files arrive)
# ══════════════════════════════════════════════════════════════════════════════

CHINA_STAGES = {
    "cn_compulsory":   {"grades": "1-9",  "level": "middle",   "label": "义务教育阶段 (1-9年级)"},
    "cn_senior_high":  {"grades": "10-12", "level": "high",    "label": "普通高中阶段 (10-12年级)"},
}

CHINA_DOMAINS = {
    "Num": {"zh": "数与代数", "en": "Number and Algebra", "de": "Zahlen und Algebra"},
    "Geo": {"zh": "图形与几何", "en": "Shapes and Geometry", "de": "Formen und Geometrie"},
    "Sta": {"zh": "统计与概率", "en": "Statistics and Probability", "de": "Statistik und Wahrscheinlichkeit"},
    "Mea": {"zh": "综合与实践", "en": "Comprehensive Practice", "de": "Umsetzung und Anwendung"},
}


def parse_china_curriculum(text):
    """Parse China curriculum text → {stage: {domain: [topics]}}"""
    result = {}
    
    # China curriculum has sections like "第一学段 (1-2年级)" etc.
    # Or "内容要求" sections with topic lists
    
    # Try to find stage sections
    stage_patterns = [
        (r'第一学段.*?(?=第二学段|$)', "cn_compulsory"),
        (r'第二学段.*?(?=第三学段|$)', "cn_compulsory"),
        (r'第三学段.*?(?=第四学段|$)', "cn_compulsory"),
        (r'第四学段.*?(?=普通高中|$)', "cn_compulsory"),
        (r'普通高中.*?(?=$)', "cn_senior_high"),
    ]
    
    # For now, try to extract topics from the full text
    # China curriculum uses "内容要求" sections
    topics_by_domain = defaultdict(list)
    
    # Extract numbered items or bullet points
    for line in text.split('\n'):
        line = line.strip()
        # Chinese curriculum items often start with numbers or specific markers
        if re.match(r'^[\d一二三四五六七八九十]+[、．.]', line):
            topic = re.sub(r'^[\d一二三四五六七八九十]+[、．.]\s*', '', line)
            if len(topic) > 3:
                # Try to classify by keyword
                if any(k in topic for k in ['数', '运算', '方程', '函数', '不等式']):
                    topics_by_domain["Num"].append(topic)
                elif any(k in topic for k in ['形', '几何', '图形', '三角', '圆', '坐标']):
                    topics_by_domain["Geo"].append(topic)
                elif any(k in topic for k in ['统计', '概率', '数据']):
                    topics_by_domain["Sta"].append(topic)
                else:
                    topics_by_domain["Mea"].append(topic)
    
    if topics_by_domain:
        for stage in CHINA_STAGES:
            result[stage] = dict(topics_by_domain)
    
    return result


# ══════════════════════════════════════════════════════════════════════════════
# US Common Core Parser (placeholder — will be filled when files arrive)
# ══════════════════════════════════════════════════════════════════════════════

US_STAGES = {
    "us_k5":    {"grades": "K-5",   "level": "elementary", "label": "Elementary (K-5)"},
    "us_68":    {"grades": "6-8",   "level": "middle",     "label": "Middle School (6-8)"},
    "us_912":   {"grades": "9-12",  "level": "high",       "label": "High School (9-12)"},
}

US_DOMAINS = {
    "Num": {"en": "Number and Quantity", "de": "Zahlen", "zh": "数与量"},
    "Alg": {"en": "Algebra", "de": "Algebra", "zh": "代数"},
    "Fct": {"en": "Functions", "de": "Funktionen", "zh": "函数"},
    "Geo": {"en": "Geometry", "de": "Geometrie", "zh": "几何"},
    "Sta": {"en": "Statistics and Probability", "de": "Stochastik", "zh": "统计与概率"},
    "MP":  {"en": "Mathematical Practices", "de": "Mathematische Praxis", "zh": "数学实践"},
}


def parse_us_common_core(text):
    """Parse US Common Core text → {stage: {domain: [topics]}}"""
    result = {}
    
    # US CCSS structure: grade-level sections with domain headers
    # E.g., "Grade 3" → "Number and Operations in Base Ten" → standards
    
    # Find grade sections
    grade_pattern = r'(?:Kindergarten|Grade\s+(\d+)|High School)'
    grade_matches = list(re.finditer(grade_pattern, text, re.IGNORECASE))
    
    # Group by stage
    stage_grades = {
        "us_k5": list(range(0, 6)),  # K-5
        "us_68": list(range(6, 9)),  # 6-8
        "us_912": ["hs"],            # High School
    }
    
    # Extract all domain-standard pairs
    # Pattern: "Domain Name X.Y.Z" followed by standard text
    # E.g., "Operations and Algebraic Thinking 3.OA"
    
    # Find domain headers in high school sections
    hs_domains = {
        "Number and Quantity": "Num",
        "Algebra": "Alg",
        "Functions": "Fct",
        "Geometry": "Geo",
        "Statistics and Probability": "Sta",
    }
    
    # Find grade-level domain headers
    grade_domains = {
        "Counting and Cardinality": "Num",
        "Operations and Algebraic Thinking": "Alg",
        "Number and Operations in Base Ten": "Num",
        "Number and Operations\u2014Fractions": "Num",
        "Number and Operations\u2014Fractions": "Num",
        "Fractions": "Num",
        "Measurement and Data": "Mea",
        "Geometry": "Geo",
        "Statistics and Probability": "Sta",
        "Ratios and Proportional Relationships": "Rat",
        "The Number System": "Num",
        "Expressions and Equations": "Alg",
        "Functions": "Fct",
        "Number and Quantity": "Num",
        "Modeling": "Alg",
    }
    
    # Extract numbered standards from the text
    # Pattern: "1. " or "1." at start of line, followed by standard text
    standards_by_domain = defaultdict(list)
    
    # Find all standards (numbered items like "1. Understand that ..." or "CCSS.MATH.CONTENT...")
    for line in text.split('\n'):
        line = line.strip()
        
        # Match standard numbers: "1. " or "1." at line start
        std_match = re.match(r'^(\d+)\.\s+(.{10,200})', line)
        if std_match:
            std_num = int(std_match.group(1))
            std_text = std_match.group(2)
            
            # Try to classify by keywords
            lower = std_text.lower()
            if any(k in lower for k in ['count', 'number', 'place value', 'operation', 'add', 'subtract',
                                          'multiply', 'divide', 'fraction', 'decimal', 'integer', 'rational',
                                          'whole number', 'base ten', 'numerator', 'denominator']):
                standards_by_domain["Num"].append(std_text)
            elif any(k in lower for k in ['expression', 'equation', 'inequality', 'variable', 'symbol',
                                            'solve', 'linear', 'quadratic', 'pattern', 'ratio', 'proportion',
                                            'analyze', 'compare', 'rewrite']):
                standards_by_domain["Alg"].append(std_text)
            elif any(k in lower for k in ['function', 'domain', 'range', 'linear function',
                                            'intercept', 'slope', 'rate of change']):
                standards_by_domain["Fct"].append(std_text)
            elif any(k in lower for k in ['angle', 'triangle', 'circle', 'congruent', 'similar',
                                            'pythagorean', 'coordinate', 'transformation', 'area',
                                            'perimeter', 'volume', 'surface']):
                standards_by_domain["Geo"].append(std_text)
            elif any(k in lower for k in ['data', 'statistics', 'probability', 'random', 'survey',
                                            'mean', 'median', 'mode', 'histogram', 'scatter']):
                standards_by_domain["Sta"].append(std_text)
            else:
                standards_by_domain["Num"].append(std_text)  # Default to Number
    
    # Assign to stages
    if standards_by_domain:
        for stage_key in US_STAGES:
            result[stage_key] = dict(standards_by_domain)
    
    return result


# ══════════════════════════════════════════════════════════════════════════════
# Unified Builder
# ══════════════════════════════════════════════════════════════════════════════

def build_curriculum_graph(country, stages_def, domains_def, parsed_data, source_docs):
    """Build a curriculum concept graph from parsed data."""
    concepts = []
    
    for stage_key, stage_info in stages_def.items():
        stage_data = parsed_data.get(stage_key, {})
        
        for field_key, topics in stage_data.items():
            if not topics:
                continue
            domain_info = domains_def.get(field_key, {})
            
            for topic in topics:
                clean = topic.strip()
                if not clean or len(clean) < 3:
                    continue
                
                name = re.sub(r'[^a-zA-Z0-9\s]', '', clean)[:50]
                name = re.sub(r'\s+', '_', name).strip('_')
                concept_name = f"curriculum_{country}_{field_key}_{stage_key}_{name}"
                
                concepts.append({
                    "name": concept_name,
                    "display_name": clean,
                    "category": "concept",
                    "level": stage_info["level"],
                    "labels": {
                        "en": domain_info.get("en", field_key),
                        "de": domain_info.get("de", field_key),
                        "zh": domain_info.get("zh", field_key),
                    },
                    "source": source_docs,
                    "stage": stage_key,
                    "stage_label": stage_info["label"],
                    "domain": field_key,
                    "domain_en": domain_info.get("en", field_key),
                })
    
    # Build relations: earlier stages → later stages within same domain
    relations = []
    grouped = defaultdict(list)
    for c in concepts:
        grouped[(c["stage"], c["domain"])].append(c)
    
    stage_order = list(stages_def.keys())
    for domain_key in domains_def:
        prev = []
        for sk in stage_order:
            curr = grouped.get((sk, domain_key), [])
            for pc in prev:
                for cc in curr:
                    relations.append({
                        "source": pc["name"],
                        "target": cc["name"],
                        "type": "prerequisite",
                        "relation": "prerequisite",
                    })
            prev.extend(curr)
    
    return {
        "version": "2.0",
        "domain": f"curriculum_{country}_math",
        "description": f"{country.upper()} Math Curriculum Standards",
        "languages": ["en", "de", "zh"],
        "concepts": concepts,
        "relations": relations,
        "metadata": {
            "total_concepts": len(concepts),
            "total_relations": len(relations),
            "source_documents": source_docs,
        },
    }


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("LinguaGraph — Multi-Curriculum Parser")
    print("=" * 60)
    
    # ── UK ──
    print("\n[UK] Parsing National Curriculum...")
    uk_text = ""
    for f in ["uk_ks12_maths.pdf", "uk_ks3_maths.pdf", "uk_ks4_maths.pdf"]:
        fp = DATA_DIR / f
        if fp.exists():
            uk_text += extract_text(fp) + "\n"
    
    uk_data = parse_uk_combined(uk_text)
    total_uk = sum(sum(len(topics) for topics in domains.values()) for domains in uk_data.values())
    print(f"  Stages: {len(uk_data)}, Total topics: {total_uk}")
    
    uk_graph = build_curriculum_graph(
        "uk", UK_STAGES, UK_DOMAINS, uk_data,
        "National Curriculum England Mathematics (2013/2021)"
    )
    
    out_path = OUTPUT_DIR / "curriculum_uk_math.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(uk_graph, f, ensure_ascii=False, indent=2)
    print(f"  Written: {out_path} ({uk_graph['metadata']['total_concepts']} concepts)")
    
    # ── China (use pre-built graph, skip corrupted PDFs) ──
    cn_json = PROJECT_ROOT / "config" / "expert_graphs" / "curriculum_cn_math.json"
    if cn_json.exists():
        print("\n[China] Using pre-built curriculum graph...")
        cn_data = json.load(open(cn_json, 'r', encoding='utf-8'))
        print(f"  Concepts: {cn_data['metadata']['total_concepts']}")
        print(f"  Relations: {cn_data['metadata']['total_relations']}")
        print(f"  Source: {cn_data['metadata']['source_documents']}")
    else:
        print("\n[China] No curriculum graph found. Run build_china_curriculum.py first.")
    
    # ── US (if files exist) ──
    us_files = list(DATA_DIR.glob("us_*"))
    if us_files:
        print("\n[US] Parsing Common Core...")
        us_text = ""
        for f in us_files:
            if f.suffix == '.pdf':
                us_text += extract_text(f) + "\n"
            elif f.suffix in ('.txt', '.html'):
                us_text += f.read_text(encoding='utf-8') + "\n"
        
        us_data = parse_us_common_core(us_text)
        total_us = sum(sum(len(topics) for topics in domains.values()) for domains in us_data.values())
        print(f"  Stages: {len(us_data)}, Total topics: {total_us}")
        
        us_graph = build_curriculum_graph(
            "us", US_STAGES, US_DOMAINS, us_data,
            "US Common Core State Standards for Mathematics"
        )
        
        out_path = OUTPUT_DIR / "curriculum_us_math.json"
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(us_graph, f, ensure_ascii=False, indent=2)
        print(f"  Written: {out_path} ({us_graph['metadata']['total_concepts']} concepts)")
    else:
        print("\n[US] No curriculum files found yet.")
    
    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)


if __name__ == "__main__":
    main()
