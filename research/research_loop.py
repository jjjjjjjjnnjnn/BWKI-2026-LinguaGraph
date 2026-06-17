"""
LinguaGraph Research Loop Orchestrator
======================================

Structured research loop that iterates through:
Phase A: Data Discovery (parallel text collection)
Phase B: Data Audit (quality check)
Phase C: Pipeline Validation (extract + compare)
Phase D: Error Mining (find failure cases)
Phase E: Report (output findings)

Usage:
    python research/research_loop.py --topic freedom --target 50
    python research/research_loop.py --all --target 50
"""

import json
import os
import sys
import re
import hashlib
import argparse
from datetime import datetime, timezone
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.compare import build_graph, compare_graphs, compare_three_languages
from src.cross_language import build_concept_translations, compute_conceptual_stability
from src.extract_v2 import fallback_extract

RESEARCH_DIR = os.path.dirname(__file__)
DATASET_DIR = os.path.join(RESEARCH_DIR, "..", "data", "pilot_dataset")
FINDINGS_DIR = os.path.join(RESEARCH_DIR, "findings")
FAILURE_DIR = os.path.join(RESEARCH_DIR, "failure_cases")
NOTABLE_DIR = os.path.join(RESEARCH_DIR, "notable_cases")

TOPICS = {
    "freedom": {"zh": "自由", "en": "Freedom", "de": "Freiheit"},
    "justice": {"zh": "正义", "en": "Justice", "de": "Gerechtigkeit"},
    "responsibility": {"zh": "责任", "en": "Responsibility", "de": "Verantwortung"},
    "success": {"zh": "成功", "en": "Success", "de": "Erfolg"},
    "home": {"zh": "家", "en": "Home", "de": "Heimat"},
}


def load_texts(topic, lang, source="education"):
    """Load texts for a topic and language from the dataset."""
    topic_dir = os.path.join(DATASET_DIR, source, topic)
    if not os.path.isdir(topic_dir):
        return []

    texts = []
    for filename in os.listdir(topic_dir):
        if not filename.endswith(".json"):
            continue
        if not filename.startswith(f"{lang}_"):
            continue
        filepath = os.path.join(topic_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                entry = json.load(f)
            if entry.get("content") and len(entry["content"]) > 50:
                texts.append(entry)
        except Exception:
            continue
    return texts


def phase_a_discovery(topic, target_per_lang=50):
    """Phase A: Check what data we have and what we need."""
    print(f"\n{'='*60}")
    print(f"Phase A: Data Discovery — {topic}")
    print(f"{'='*60}")

    status = {}
    for lang in ["zh", "en", "de"]:
        texts = load_texts(topic, lang)
        status[lang] = {
            "count": len(texts),
            "target": target_per_lang,
            "gap": max(0, target_per_lang - len(texts)),
            "sources": list(set(t.get("platform", "unknown") for t in texts)),
        }
        emoji = "OK" if len(texts) >= target_per_lang else "WARN"
        print(f"  {emoji} {lang}: {len(texts)}/{target_per_lang} texts")

    total = sum(s["count"] for s in status.values())
    total_gap = sum(s["gap"] for s in status.values())
    print(f"\n  Total: {total} texts, Gap: {total_gap}")

    return status


def phase_b_audit(topic):
    """Phase B: Audit data quality."""
    print(f"\n{'='*60}")
    print(f"Phase B: Data Audit — {topic}")
    print(f"{'='*60}")

    audit = {"total": 0, "high_quality": 0, "low_quality": 0, "issues": []}

    for lang in ["zh", "en", "de"]:
        texts = load_texts(topic, lang)
        for t in texts:
            audit["total"] += 1
            content = t.get("content", "")

            issues = []
            if len(content) < 100:
                issues.append("too_short")
            if len(content) > 5000:
                issues.append("too_long")
            if content.count("\n") < 2:
                issues.append("no_structure")
            if not any(c.isalpha() for c in content):
                issues.append("no_text")

            if issues:
                audit["low_quality"] += 1
                audit["issues"].extend(issues)
            else:
                audit["high_quality"] += 1

    print(f"  Total: {audit['total']}")
    print(f"  High quality: {audit['high_quality']}")
    print(f"  Low quality: {audit['low_quality']}")
    if audit["issues"]:
        issue_counts = Counter(audit["issues"])
        print(f"  Issues: {dict(issue_counts)}")

    return audit


def phase_c_pipeline(topic):
    """Phase C: Run extraction and comparison pipeline."""
    print(f"\n{'='*60}")
    print(f"Phase C: Pipeline Validation — {topic}")
    print(f"{'='*60}")

    graphs = {}
    extractions = {}

    for lang in ["zh", "en", "de"]:
        texts = load_texts(topic, lang)
        if len(texts) < 3:
            print(f"  [{lang}] SKIP — only {len(texts)} texts")
            continue

        combined = "\n".join(t["content"][:500] for t in texts[:20])
        extraction = fallback_extract(combined, lang)
        concepts = extraction["concepts"]

        if not concepts:
            print(f"  [{lang}] SKIP — no concepts extracted")
            continue

        relations = [(r["from"], r["type"], r["to"]) for r in extraction.get("relations", [])]
        G = build_graph(concepts, relations)
        graphs[lang] = G
        extractions[lang] = extraction

        print(f"  [{lang}] {len(texts)} texts → {len(concepts)} concepts: {concepts[:6]}")

    if len(graphs) < 2:
        print("  Not enough languages for comparison")
        return None

    result = compare_three_languages(graphs)

    print(f"\n  LDS Results:")
    for key, val in result["pairwise"].items():
        print(f"    {key}: LDS={val['language_drift_score']}")
    print(f"  Average LDS: {result['average_lds']}")

    return {"graphs": {k: list(G.nodes()) for k, G in graphs.items()},
            "extractions": extractions,
            "comparison": result}


def phase_d_error_mining(topic, pipeline_result):
    """Phase D: Find failure cases and notable cases."""
    print(f"\n{'='*60}")
    print(f"Phase D: Error Mining — {topic}")
    print(f"{'='*60}")

    if not pipeline_result:
        print("  No pipeline results to mine")
        return []

    cases = []

    comparison = pipeline_result["comparison"]
    for key, val in comparison["pairwise"].items():
        lds = val["language_drift_score"]
        overlap = val["concept_overlap"]

        if lds > 0.8:
            case = {
                "type": "high_drift",
                "topic": topic,
                "pair": key,
                "lds": lds,
                "shared_concepts": overlap["shared"],
                "unique_to_g1": overlap["only_in_g1"][:5],
                "unique_to_g2": overlap["only_in_g2"][:5],
                "description": f"High LDS ({lds:.3f}) between {key} — very different concept structures",
            }
            cases.append(case)
            print(f"  [!] HIGH DRIFT: {key} LDS={lds:.3f}")
            print(f"     Shared: {overlap['shared'][:5]}")
            print(f"     Unique to lang1: {overlap['only_in_g1'][:5]}")
            print(f"     Unique to lang2: {overlap['only_in_g2'][:5]}")

        if overlap["shared_count"] == 0 and lds > 0.5:
            case = {
                "type": "no_overlap",
                "topic": topic,
                "pair": key,
                "lds": lds,
                "description": f"No shared concepts between {key}",
            }
            cases.append(case)
            print(f"  [~] NO OVERLAP: {key}")

    for lang, extraction in pipeline_result["extractions"].items():
        concepts = extraction["concepts"]
        if len(concepts) < 3:
            case = {
                "type": "sparse_extraction",
                "topic": topic,
                "language": lang,
                "concept_count": len(concepts),
                "description": f"Only {len(concepts)} concepts extracted from {lang}",
            }
            cases.append(case)
            print(f"  [~] SPARSE: {lang} only {len(concepts)} concepts")

    return cases


def phase_e_report(topic, discovery, audit, pipeline_result, cases):
    """Phase E: Generate research report."""
    print(f"\n{'='*60}")
    print(f"Phase E: Report — {topic}")
    print(f"{'='*60}")

    os.makedirs(FINDINGS_DIR, exist_ok=True)

    report = f"""# Research Finding: {topic}

**Date:** {datetime.now().isoformat()}
**Topic:** {topic} ({TOPICS[topic]['zh']}/{TOPICS[topic]['en']}/{TOPICS[topic]['de']})

## Data Status

| Language | Count | Target | Status |
|----------|-------|--------|--------|
"""
    for lang in ["zh", "en", "de"]:
        count = discovery[lang]["count"]
        target = discovery[lang]["target"]
        status = "[OK]" if count >= target else "[WARN]"
        report += f"| {lang} | {count} | {target} | {status} |\n"

    total = sum(d["count"] for d in discovery.values())
    report += f"\n**Total:** {total} texts\n"

    if audit:
        report += f"\n## Data Quality\n"
        report += f"- High quality: {audit['high_quality']}\n"
        report += f"- Low quality: {audit['low_quality']}\n"

    if pipeline_result:
        comparison = pipeline_result["comparison"]
        report += f"\n## LDS Results\n"
        report += f"- Average LDS: {comparison['average_lds']}\n"
        for key, val in comparison["pairwise"].items():
            report += f"- {key}: LDS={val['language_drift_score']}\n"

    if cases:
        report += f"\n## Notable Cases ({len(cases)})\n"
        for case in cases:
            report += f"- **{case['type']}**: {case['description']}\n"

    report_path = os.path.join(FINDINGS_DIR, f"topic_{topic}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  Report saved: {report_path}")

    return report


def run_loop(topic, target_per_lang=50):
    """Execute one full research loop iteration for a topic."""
    print(f"\n{'#'*60}")
    print(f"# RESEARCH LOOP: {topic}")
    print(f"# Target: {target_per_lang} texts per language")
    print(f"{'#'*60}")

    discovery = phase_a_discovery(topic, target_per_lang)
    audit = phase_b_audit(topic)
    pipeline_result = phase_c_pipeline(topic)
    cases = phase_d_error_mining(topic, pipeline_result)
    report = phase_e_report(topic, discovery, audit, pipeline_result, cases)

    return {
        "topic": topic,
        "discovery": discovery,
        "audit": audit,
        "cases": cases,
        "has_pipeline": pipeline_result is not None,
    }


def main():
    parser = argparse.ArgumentParser(description="LinguaGraph Research Loop")
    parser.add_argument("--topic", type=str, help="Specific topic to analyze")
    parser.add_argument("--all", action="store_true", help="Analyze all topics")
    parser.add_argument("--target", type=int, default=50, help="Target texts per language")
    args = parser.parse_args()

    topics = [args.topic] if args.topic else list(TOPICS.keys()) if args.all else ["freedom"]

    all_results = {}
    for topic in topics:
        result = run_loop(topic, args.target)
        all_results[topic] = result

    print(f"\n{'#'*60}")
    print(f"# LOOP SUMMARY")
    print(f"{'#'*60}")
    for topic, result in all_results.items():
        total = sum(d["count"] for d in result["discovery"].values())
        cases = len(result["cases"])
        pipeline = "[OK]" if result["has_pipeline"] else "❌"
        print(f"  {topic:15s}: {total:3d} texts, {cases:2d} cases, pipeline={pipeline}")

    summary_path = os.path.join(RESEARCH_DIR, "loop_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nSummary saved: {summary_path}")


if __name__ == "__main__":
    main()
