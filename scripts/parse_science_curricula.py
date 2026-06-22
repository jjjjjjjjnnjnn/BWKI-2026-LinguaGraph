"""
parse_science_curricula.py — 解析 UK/US 科学课标
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


def extract_text(pdf_path):
    texts = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                texts.append(t)
    return "\n".join(texts)


# ── UK Science ──────────────────────────────────────────────────────────────

UK_SCIENCE_STAGES = {
    "uk_sci_ks1":    {"grades": "Y1-2", "level": "elementary", "label": "KS1 Science (ages 5-7)"},
    "uk_sci_ks2_lower": {"grades": "Y3-4", "level": "elementary", "label": "Lower KS2 Science (ages 7-9)"},
    "uk_sci_ks2_upper": {"grades": "Y5-6", "level": "middle", "label": "Upper KS2 Science (ages 9-11)"},
    "uk_sci_ks3":    {"grades": "Y7-9", "level": "middle", "label": "KS3 Science (ages 11-14)"},
    "uk_sci_ks4":    {"grades": "Y10-11", "level": "high", "label": "KS4/GCSE Science (ages 14-16)"},
}

UK_SCIENCE_DOMAINS = {
    "Bio": {"en": "Biology", "de": "Biologie", "zh": "生物学"},
    "Che": {"en": "Chemistry", "de": "Chemie", "zh": "化学"},
    "Phy": {"en": "Physics", "de": "Physik", "zh": "物理学"},
    "EaS": {"en": "Earth and Space", "de": "Erde und Weltraum", "zh": "地球与太空"},
}


def parse_uk_science():
    """Parse UK Science curricula."""
    result = {}
    
    # KS1-2
    fp = DATA_DIR / "uk_science_ks1_ks2.pdf"
    if fp.exists():
        text = extract_text(fp)
        # Find year sections
        for year in range(1, 7):
            pattern = rf'Year {year}\s*(?:programme of study|–)'
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                start = m.end()
                # Find next year or end
                next_m = re.search(rf'Year {year+1}\s*(?:programme of study|–)', text[start:], re.IGNORECASE)
                end = start + next_m.start() if next_m else len(text)
                section = text[start:end]
                
                stage_key = f"uk_sci_ks1" if year <= 2 else f"uk_sci_ks2_lower" if year <= 4 else "uk_sci_ks2_upper"
                
                # Extract topics by domain
                domains = {}
                for line in section.split('\n'):
                    line = line.strip()
                    if line.startswith('-') or line.startswith('•'):
                        topic = line.lstrip('-•').strip()
                        if topic and len(topic) > 5:
                            # Classify by keyword
                            lower = topic.lower()
                            if any(k in lower for k in ['plant', 'animal', 'living', 'growth', 'habitat', 'micro']):
                                domains.setdefault("Bio", []).append(topic)
                            elif any(k in lower for k in ['material', 'change', 'mix', 'dissolv', 'heat', 'temperature']):
                                domains.setdefault("Che", []).append(topic)
                            elif any(k in lower for k in ['force', 'movement', 'light', 'sound', 'magnet', 'electric']):
                                domains.setdefault("Phy", []).append(topic)
                            else:
                                domains.setdefault("EaS", []).append(topic)
                
                if domains:
                    result[stage_key] = domains
    
    # KS3
    fp = DATA_DIR / "uk_science_ks3.pdf"
    if fp.exists():
        text = extract_text(fp)
        domains = {}
        for line in text.split('\n'):
            line = line.strip()
            if line.startswith('-') or line.startswith('•'):
                topic = line.lstrip('-•').strip()
                if topic and len(topic) > 5:
                    lower = topic.lower()
                    if any(k in lower for k in ['cell', 'organ', 'ecosystem', 'evolution', 'genetic', 'bio']):
                        domains.setdefault("Bio", []).append(topic)
                    elif any(k in lower for k in ['atom', 'element', 'compound', 'reaction', 'bond', 'acid', 'chem']):
                        domains.setdefault("Che", []).append(topic)
                    elif any(k in lower for k in ['energy', 'force', 'wave', 'electric', 'magnet', 'light', 'space']):
                        domains.setdefault("Phy", []).append(topic)
                    else:
                        domains.setdefault("EaS", []).append(topic)
        
        if domains:
            result["uk_sci_ks3"] = domains
    
    # KS4
    fp = DATA_DIR / "uk_science_ks4.pdf"
    if fp.exists():
        text = extract_text(fp)
        domains = {}
        for line in text.split('\n'):
            line = line.strip()
            if line.startswith('-') or line.startswith('•'):
                topic = line.lstrip('-•').strip()
                if topic and len(topic) > 5:
                    lower = topic.lower()
                    if any(k in lower for k in ['cell', 'organ', 'ecosystem', 'evolution', 'genetic', 'bio', 'homeost']):
                        domains.setdefault("Bio", []).append(topic)
                    elif any(k in lower for k in ['atom', 'element', 'compound', 'reaction', 'bond', 'acid', 'chem', 'rate']):
                        domains.setdefault("Che", []).append(topic)
                    elif any(k in lower for k in ['energy', 'force', 'wave', 'electric', 'magnet', 'light', 'space', 'motion']):
                        domains.setdefault("Phy", []).append(topic)
                    else:
                        domains.setdefault("EaS", []).append(topic)
        
        if domains:
            result["uk_sci_ks4"] = domains
    
    return result


# ── US NGSS ────────────────────────────────────────────────────────────────

US_SCIENCE_STAGES = {
    "us_sci_k5":    {"grades": "K-5", "level": "elementary", "label": "Elementary Science (K-5)"},
    "us_sci_68":    {"grades": "6-8", "level": "middle", "label": "Middle School Science (6-8)"},
    "us_sci_912":   {"grades": "9-12", "level": "high", "label": "High School Science (9-12)"},
}

US_SCIENCE_DOMAINS = {
    "LS": {"en": "Life Science", "de": "Lebenswissenschaft", "zh": "生命科学"},
    "PS": {"en": "Physical Science", "de": "Physikalische Wissenschaft", "zh": "物质科学"},
    "ES": {"en": "Earth and Space Science", "de": "Erd- und Raumwissenschaft", "zh": "地球与空间科学"},
    "EP": {"en": "Engineering Practices", "de": "Ingenieurpraxis", "zh": "工程实践"},
}


def parse_us_ngss():
    """Parse US NGSS."""
    result = {}
    
    fp = DATA_DIR / "us_ngss_science.pdf"
    if not fp.exists():
        return result
    
    text = extract_text(fp)
    
    # NGSS is organized by Disciplinary Core Ideas (DCIs)
    # Life Science: LS1-LS4
    # Physical Science: PS1-PS4
    # Earth and Space Science: ESS1-ESS3
    # Engineering: ETS1
    
    domains = {"LS": [], "PS": [], "ES": [], "EP": []}
    
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('-') or line.startswith('•'):
            topic = line.lstrip('-•').strip()
            if topic and len(topic) > 5:
                lower = topic.lower()
                if any(k in lower for k in ['cell', 'organ', 'ecosystem', 'evolution', 'genetic', 'body', 'heredity']):
                    domains["LS"].append(topic)
                elif any(k in lower for k in ['atom', 'molecule', 'force', 'energy', 'wave', 'chemical', 'structure']):
                    domains["PS"].append(topic)
                elif any(k in lower for k in ['earth', 'space', 'weather', 'climate', 'plate', 'history', 'solar']):
                    domains["ES"].append(topic)
                elif any(k in lower for k in ['engineer', 'design', 'model', 'optimize', 'solution']):
                    domains["EP"].append(topic)
    
    # Assign to stages
    for stage in US_SCIENCE_STAGES:
        result[stage] = {k: list(v) for k, v in domains.items() if v}
    
    return result


# ── Builder ─────────────────────────────────────────────────────────────────

def build_graph(stages_def, domains_def, parsed_data, country, source_doc):
    concepts = []
    
    for stage_key, stage_info in stages_def.items():
        stage_domains = parsed_data.get(stage_key, {})
        
        for field_key, topics in stage_domains.items():
            domain_info = domains_def.get(field_key, {})
            
            for topic in topics:
                clean = topic.strip()
                if not clean:
                    continue
                name_part = re.sub(r'[^a-zA-Z0-9\s]', '', clean)[:40]
                name_part = re.sub(r'\s+', '_', name_part).strip('_')
                concepts.append({
                    "name": f"curriculum_{country}_{field_key}_{stage_key}_{name_part}",
                    "display_name": clean,
                    "category": "concept",
                    "level": stage_info["level"],
                    "labels": {"en": domain_info.get("en", ""), "de": domain_info.get("de", ""), "zh": domain_info.get("zh", "")},
                    "source": source_doc,
                    "stage": stage_key,
                    "stage_label": stage_info["label"],
                    "domain": field_key,
                    "domain_en": domain_info.get("en", ""),
                })
    
    relations = []
    grouped = {}
    for c in concepts:
        grouped.setdefault((c["stage"], c["domain"]), []).append(c)
    
    stage_order = list(stages_def.keys())
    for dk in domains_def:
        prev = []
        for sk in stage_order:
            curr = grouped.get((sk, dk), [])
            for pc in prev:
                for cc in curr:
                    relations.append({"source": pc["name"], "target": cc["name"], "type": "prerequisite", "relation": "prerequisite"})
            prev.extend(curr)
    
    return {
        "version": "2.0",
        "domain": f"curriculum_{country}_science",
        "description": f"{country.upper()} Science Curriculum Standards",
        "languages": ["en", "de", "zh"],
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
    print("Science Curriculum Parser (UK + US)")
    print("=" * 60)
    
    # UK
    print("\n[UK] Parsing Science...")
    uk_data = parse_uk_science()
    total_uk = sum(sum(len(v) for v in d.values()) for d in uk_data.values())
    print(f"  Stages: {len(uk_data)}, Total: {total_uk}")
    
    uk_graph = build_graph(UK_SCIENCE_STAGES, UK_SCIENCE_DOMAINS, uk_data, "uk",
                           "National Curriculum England Science (2013/2021)")
    out_uk = OUTPUT_DIR / "curriculum_uk_science.json"
    with open(out_uk, 'w', encoding='utf-8') as f:
        json.dump(uk_graph, f, ensure_ascii=False, indent=2)
    print(f"  Written: {out_uk} ({uk_graph['metadata']['total_concepts']} concepts)")
    
    # US
    print("\n[US] Parsing NGSS...")
    us_data = parse_us_ngss()
    total_us = sum(sum(len(v) for v in d.values()) for d in us_data.values())
    print(f"  Stages: {len(us_data)}, Total: {total_us}")
    
    us_graph = build_graph(US_SCIENCE_STAGES, US_SCIENCE_DOMAINS, us_data, "us",
                           "Next Generation Science Standards (NGSS)")
    out_us = OUTPUT_DIR / "curriculum_us_science.json"
    with open(out_us, 'w', encoding='utf-8') as f:
        json.dump(us_graph, f, ensure_ascii=False, indent=2)
    print(f"  Written: {out_us} ({us_graph['metadata']['total_concepts']} concepts)")
    
    print(f"\n{'='*60}")
    print("DONE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
