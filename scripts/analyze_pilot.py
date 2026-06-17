"""
LinguaGraph Pilot Analysis Template
======================================
Run this when pilot data (9 participants) arrives.

Usage:
    python scripts/analyze_pilot.py --data data/pilot_responses.json
    python scripts/analyze_pilot.py --data data/pilot_responses.json --report

Output:
    research/findings/pilot_report.md
    research/findings/pilot_issues.json
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Add project paths
PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR / 'src'))
sys.path.insert(0, str(PROJECT_DIR))

from db_utils import get_connection, insert, query
from graph import build_graph, graph_stats
from scoring import calculate_lcd_score


# ===== CONFIG =====
MIN_WORDS = 20
LANGUAGE_NAMES = {"zh": "Chinese", "de": "German", "en": "English"}
TOPICS = {"q1": "Freedom", "q2": "Justice", "q3": "Success", "q4": "Responsibility", "q5": "Home"}
CONTROL_TOPICS = {"q6": "Food", "q7": "Weather"}


def load_pilot_data(filepath):
    """Load pilot responses from JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]


def check_quality(responses):
    """Check response quality per question."""
    issues = []
    for r in responses:
        for lang in ["zh", "de", "en"]:
            answer = r.get(lang, {}).get("answer", "")
            qid = r.get(lang, {}).get("question_id", "unknown")
            wc = len(answer.split()) if lang != "zh" else len([c for c in answer if '一' <= c <= '鿿'])

            if not answer.strip():
                issues.append({"participant": r["id"], "question": qid, "lang": lang, "issue": "blank"})
            elif wc < MIN_WORDS:
                issues.append({"participant": r["id"], "question": qid, "lang": lang, "issue": f"too_short ({wc} words)"})

    return issues


def compute_basic_stats(responses):
    """Compute per-question, per-language statistics."""
    stats = {}
    for r in responses:
        for lang in ["zh", "de", "en"]:
            answer = r.get(lang, {}).get("answer", "")
            qid = r.get(lang, {}).get("question_id", "unknown")
            key = f"{qid}_{lang}"
            if key not in stats:
                stats[key] = {"word_counts": [], "count": 0}
            wc = len(answer.split()) if lang != "zh" else len(answer)
            stats[key]["word_counts"].append(wc)
            stats[key]["count"] += 1

    return stats


def detect_misunderstandings(responses):
    """Flag potential misunderstandings based on keyword analysis."""
    # Check for ZH participants answering in DE/EN when they should use ZH (and vice versa)
    issues = []
    for r in responses:
        native = r.get("native_lang", "zh")
        for target_lang in ["zh", "de", "en"]:
            answer = r.get(target_lang, {}).get("answer", "")
            qid = r.get(target_lang, {}).get("question_id", "unknown")

            # Check if participant used wrong language
            if target_lang == "zh" and native != "zh":
                # Check for German/English characters
                de_chars = sum(1 for c in answer if ord(c) > 0x7F and not ('一' <= c <= '鿿'))
                if de_chars > len(answer) * 0.3:
                    issues.append({"participant": r["id"], "question": qid, "lang": target_lang, "issue": "language_mismatch"})

    return issues


def generate_pilot_report(responses, quality_issues, stats, misunderstandings):
    """Generate a pilot report markdown file."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    md = []
    md.append(f"# LinguaGraph Pilot Report\n")
    md.append(f"Generated: {now} | Participants: {len(responses)}\n")
    md.append("---\n")

    # Participant overview
    md.append("## 1. Participant Overview\n")
    md.append("| ID | Native Language | Languages Tested | Status |\n")
    md.append("|----|----------------|-----------------|--------|\n")
    for r in responses:
        langs_completed = sum(1 for l in ["zh", "de", "en"] if r.get(l, {}).get("answer", "").strip())
        status = "✅ Complete" if langs_completed >= 3 else "⚠️ Partial"
        md.append(f"| {r['id']} | {r.get('native_lang', '?')} | {langs_completed}/3 | {status} |\n")

    # Quality check results
    md.append("\n## 2. Response Quality\n")
    if quality_issues:
        md.append(f"| Participant | Question | Language | Issue |\n")
        md.append(f"|-------------|----------|----------|-------|\n")
        for issue in quality_issues[:20]:
            md.append(f"| {issue['participant']} | {issue['question']} | {issue['lang']} | {issue['issue']} |\n")
        md.append(f"\n*{len(quality_issues)} total issues found*\n")
    else:
        md.append("*No quality issues found*\n")

    # Misunderstandings
    md.append("\n## 3. Potential Misunderstandings\n")
    if misunderstandings:
        md.append("| Participant | Question | Language | Issue |\n")
        md.append("|------------|----------|----------|-------|\n")
        for m in misunderstandings:
            md.append(f"| {m['participant']} | {m['question']} | {m['lang']} | {m['issue']} |\n")
    else:
        md.append("*None detected*\n")

    # Per-question statistics
    md.append("\n## 4. Per-Question Statistics\n")
    for qid in ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]:
        topic_name = TOPICS.get(qid, CONTROL_TOPICS.get(qid, "Unknown"))
        md.append(f"\n### {topic_name} ({qid})\n")
        md.append("| Language | Responses | Avg Words | Min | Max |\n")
        md.append("|----------|-----------|-----------|-----|-----|\n")
        for lang in ["zh", "de", "en"]:
            key = f"{qid}_{lang}"
            if key in stats:
                wcs = stats[key]["word_counts"]
                avg = sum(wcs) / len(wcs) if wcs else 0
                md.append(f"| {LANGUAGE_NAMES[lang]} | {stats[key]['count']} | {avg:.0f} | {min(wcs)} | {max(wcs)} |\n")
            else:
                md.append(f"| {LANGUAGE_NAMES[lang]} | 0 | - | - | - |\n")

    # LDS computation (placeholder - requires pipeline run)
    md.append("\n## 5. LDS Results (Preliminary)\n")
    md.append("*Results will appear after running full pipeline on pilot data*\n")
    md.append("```\npython scripts/analyze_pilot.py --pipeline\n```\n")

    # Issues to fix
    if quality_issues or misunderstandings:
        md.append("\n## 6. Recommended Changes Before Full Study\n")
        for issue in quality_issues:
            if issue["issue"] == "blank":
                md.append(f"- ⚠️ Q{issue['question']} ({LANGUAGE_NAMES[issue['lang']]}): Participant skipped — reword or add instruction\n")
        for m in misunderstandings:
            if m["issue"] == "language_mismatch":
                md.append(f"- ⚠️ Q{m['question']} ({LANGUAGE_NAMES[m['lang']]}): Language mismatch — check translation clarity\n")

    # Save
    outdir = PROJECT_DIR / "research" / "findings"
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / "pilot_report.md"
    outpath.write_text("\n".join(md), encoding="utf-8")
    print(f"[OK] Pilot report saved to {outpath}")

    # Also save issues as JSON for machine processing
    issues_out = outdir / "pilot_issues.json"
    with open(issues_out, "w", encoding="utf-8") as f:
        json.dump({"quality_issues": quality_issues, "misunderstandings": misunderstandings}, f, ensure_ascii=False, indent=2)
    print(f"[OK] Issues exported to {issues_out}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph Pilot Analysis")
    parser.add_argument("--data", type=str, required=True, help="Path to pilot responses JSON")
    parser.add_argument("--report", action="store_true", help="Generate report only (no pipeline)")
    parser.add_argument("--pipeline", action="store_true", help="Run full pipeline on pilot data")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  LinguaGraph Pilot Analysis")
    print(f"{'='*50}")

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"[ERROR] File not found: {data_path}")
        return

    responses = load_pilot_data(data_path)
    print(f"\n[OK] Loaded {len(responses)} participants")

    # Quality checks
    print("\n--- Quality Check ---")
    quality_issues = check_quality(responses)
    misunderstandings = detect_misunderstandings(responses)
    print(f"  Quality issues: {len(quality_issues)}")
    print(f"  Misunderstandings: {len(misunderstandings)}")

    # Stats
    stats = compute_basic_stats(responses)

    # Report
    if args.report or True:
        generate_pilot_report(responses, quality_issues, stats, misunderstandings)

    # Full pipeline
    if args.pipeline:
        print("\n--- Running Full Pipeline ---")
        from src.extract import extract_concepts
        for r in responses:
            pid = r["id"]
            for lang in ["zh", "de", "en"]:
                answer = r.get(lang, {}).get("answer", "")
                if not answer.strip():
                    continue
                try:
                    result = extract_concepts(answer, language=lang, use_mock=False)
                    print(f"  {pid}/{lang}: {len(result.get('concepts', []))} concepts extracted")
                except Exception as e:
                    print(f"  {pid}/{lang}: [ERROR] {e}")

    print(f"\n[DONE] Analysis complete.\n")


if __name__ == "__main__":
    main()
