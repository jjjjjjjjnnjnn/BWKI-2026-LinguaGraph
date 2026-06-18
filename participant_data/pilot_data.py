#!/usr/bin/env python3
"""
Pilot Data Query Module
=======================
Easy programmatic access to pilot data for analysis and comparison.

Usage:
    from pilot_data import PilotData

    pd = PilotData()

    # Get all pilot participants
    pd.participants()

    # Get P001's responses
    pd.responses("P001")

    # Compare answers to q9 across all participants
    pd.compare("q9_xiao_explain")

    # Get word association data (q8)
    pd.word_associations()

    # Export as DataFrame
    df = pd.to_dataframe()
"""

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from db_utils import get_connection, query


PILOT_IDS = ["P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008"]

QUESTION_LABELS = {
    "q8_time_assoc": "时间联想 (Time Association)",
    "q9_xiao_explain": "孝 (Filial Piety)",
    "q10_emotion_reaction": "情感反应 (Emotional Reaction)",
    "q11_picture_vase": "图画描述-花瓶 (Picture: Vase)",
    "q12_translate_mike": "翻译-路径 (Translation: Motion)",
    "q13_picture_spatial": "空间描述 (Spatial Description)",
    "q14_translate_test": "翻译-时间 (Translation: Time)",
    "q15_picture_exchange": "图画描述-交换 (Picture: Exchange)",
    "q16_translate_umbrella": "翻译-复杂句 (Translation: Complex)",
    "q17_robot_description": "专业描述 (Robot Description)",
}

QUESTION_TYPES = {
    "q8_time_assoc": "自由联想",
    "q9_xiao_explain": "文化概念",
    "q10_emotion_reaction": "情感反应",
    "q11_picture_vase": "图画描述",
    "q12_translate_mike": "翻译",
    "q13_picture_spatial": "空间描述",
    "q14_translate_test": "翻译",
    "q15_picture_exchange": "图画描述",
    "q16_translate_umbrella": "翻译",
    "q17_robot_description": "专业描述",
}


class PilotData:
    """Query and analyze pilot study data."""

    def __init__(self):
        self.conn = get_connection()

    def close(self):
        self.conn.close()

    # ===== Participant Info =====

    def participants(self, pilot_only: bool = True) -> List[Dict]:
        """Get all participants, optionally filter to pilot only."""
        if pilot_only:
            return query(self.conn,
                "SELECT * FROM students WHERE student_id LIKE 'P%' ORDER BY student_id")
        return query(self.conn,
            "SELECT * FROM students ORDER BY student_id")

    def participant(self, pid: str) -> Optional[Dict]:
        """Get a single participant."""
        rows = query(self.conn,
            "SELECT * FROM students WHERE student_id = ?", (pid,))
        return rows[0] if rows else None

    # ===== Response Queries =====

    def responses(self, pid: str, language: str = "zh") -> List[Dict]:
        """Get all responses for a participant in a language."""
        return query(self.conn, """
            SELECT question_id, answer_text, word_count
            FROM responses
            WHERE student_id = ? AND language = ?
            ORDER BY question_id
        """, (pid, language))

    def question(self, qid: str, language: str = "zh") -> List[Dict]:
        """Get all participants' answers to a specific question."""
        return query(self.conn, """
            SELECT r.student_id, r.answer_text, s.age_group, s.other_langs
            FROM responses r
            JOIN students s ON r.student_id = s.student_id
            WHERE r.question_id = ? AND r.language = ?
            ORDER BY r.student_id
        """, (qid, language))

    def compare(self, qid: str, language: str = "zh") -> str:
        """Print a side-by-side comparison of answers to a question."""
        answers = self.question(qid, language)
        if not answers:
            return f"[No data for {qid}]"

        label = QUESTION_LABELS.get(qid, qid)
        lines = [f"\n=== {label} ==="]
        for a in answers:
            lines.append(f"\n{a['student_id']} (age {a.get('age_group','?')}):")
            lines.append(f"  {a['answer_text']}")
        return "\n".join(lines)

    # ===== Specialized Queries =====

    def word_associations(self, language: str = "zh") -> Dict[str, List[str]]:
        """Get time word associations (q8) parsed into word lists."""
        answers = self.question("q8_time_assoc", language)
        result = {}
        for a in answers:
            text = a["answer_text"]
            # Split on common delimiters
            words = [w.strip() for w in text.replace("、", " ").replace("，", " ").replace("  ", " ").split()]
            result[a["student_id"]] = words
        return result

    def word_association_freq(self, language: str = "zh") -> Dict[str, int]:
        """Get word frequency across all q8 answers."""
        freq = defaultdict(int)
        associations = self.word_associations(language)
        for words in associations.values():
            for w in words:
                if w and w != "（" and w != "）":
                    # Clean punctuation
                    w = w.replace("（", "").replace("）", "").replace("？", "")
                    if w:
                        freq[w] += 1
        return dict(sorted(freq.items(), key=lambda x: -x[1]))

    def translation_errors(self) -> List[Dict]:
        """Find potential translation errors in q12, q14, q16."""
        trans_questions = ["q12_translate_mike", "q14_translate_test", "q16_translate_umbrella"]
        issues = []

        for qid in trans_questions:
            answers = self.question(qid, "zh")
            for a in answers:
                text = a["answer_text"]
                # Check for common issues
                warnings = []
                if len(text) < 10:
                    warnings.append("too_short")
                if "?" in text or "？" in text:
                    warnings.append("contains_question_mark")

                if warnings:
                    issues.append({
                        "student_id": a["student_id"],
                        "question_id": qid,
                        "question_label": QUESTION_LABELS.get(qid, qid),
                        "answer": text,
                        "warnings": warnings,
                    })
        return issues

    def language_mixing(self) -> List[Dict]:
        """Find responses that mix Chinese and English characters."""
        import re
        mixed = []
        answers = query(self.conn, """
            SELECT student_id, question_id, answer_text
            FROM responses
            WHERE source = 'pilot' AND language = 'zh'
            ORDER BY student_id, question_id
        """)
        for a in answers:
            has_chinese = bool(re.search(r'[一-鿿]', a["answer_text"]))
            has_english = bool(re.search(r'[a-zA-Z]{2,}', a["answer_text"]))
            if has_chinese and has_english:
                mixed.append(a)
        return mixed

    # ===== Aggregations =====

    def summary(self, language: str = "zh") -> Dict:
        """Get summary statistics for pilot data."""
        students = self.participants()
        total_responses = query(self.conn,
            "SELECT COUNT(*) as c FROM responses WHERE source='pilot'")[0]["c"]
        avg_words = query(self.conn, """
            SELECT AVG(word_count) as avg_w
            FROM responses WHERE source='pilot' AND language=?
        """, (language,))

        return {
            "total_participants": len(students),
            "total_responses": total_responses,
            "avg_word_count": round(avg_words[0]["avg_w"], 1) if avg_words else 0,
            "age_range": f"{min(int(p.get('age_group','0')[:2]) for p in students if p.get('age_group'))}-{max(int(p.get('age_group','0')[-2:]) for p in students if p.get('age_group'))}",
            "languages_available": list(set(r["language"] for r in
                query(self.conn, "SELECT DISTINCT language FROM responses WHERE source='pilot'"))),
        }

    def to_dataframe(self):
        """Export pilot data as a DataFrame-compatible dict."""
        try:
            import pandas as pd
        except ImportError:
            print("[WARN] pandas not installed. Run: pip install pandas")
            return None

        rows = query(self.conn, """
            SELECT r.student_id, s.age_group, s.native_lang,
                   r.language, r.question_id, r.answer_text, r.word_count
            FROM responses r
            JOIN students s ON r.student_id = s.student_id
            WHERE r.source = 'pilot'
            ORDER BY r.student_id, r.language, r.question_id
        """)
        return pd.DataFrame(rows)

    # ===== Print Report =====

    def print_report(self):
        """Print a formatted summary report."""
        s = self.summary()
        print(f"\n{'='*60}")
        print(f"  LinguaGraph — Pilot Data Summary")
        print(f"{'='*60}")
        print(f"  Participants: {s['total_participants']}")
        print(f"  Responses:    {s['total_responses']}")
        print(f"  Avg words:    {s['avg_word_count']}")
        print(f"  Age range:    {s['age_range']}")
        print(f"  Languages:    {', '.join(s['languages_available'])}")
        print(f"\n  Questions:")
        for qid, label in QUESTION_LABELS.items():
            n = len(self.question(qid))
            print(f"    {qid}: {label} ({n} answers)")
        print(f"{'='*60}\n")


# ===== CLI =====

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", type=str, help="Compare answers to a question (e.g., q9_xiao_explain)")
    parser.add_argument("--freq", action="store_true", help="Show word association frequency (q8)")
    parser.add_argument("--mix", action="store_true", help="Show language mixing instances")
    parser.add_argument("--errors", action="store_true", help="Show potential translation errors")
    parser.add_argument("--summary", action="store_true", help="Show summary report")
    parser.add_argument("--export", type=str, help="Export to JSON file")
    args = parser.parse_args()

    pd = PilotData()

    try:
        if args.compare:
            print(pd.compare(args.compare))

        elif args.freq:
            freq = pd.word_association_freq()
            print("\n=== Word Association Frequency (q8) ===")
            for word, count in sorted(freq.items(), key=lambda x: -x[1])[:20]:
                print(f"  {word}: {count}")

        elif args.mix:
            mixed = pd.language_mixing()
            print(f"\n=== Language Mixing Instances ({len(mixed)} cases) ===")
            for m in mixed:
                print(f"  {m['student_id']} {m['question_id']}: {m['answer_text'][:60]}")

        elif args.errors:
            errors = pd.translation_errors()
            print(f"\n=== Translation Issues ({len(errors)} cases) ===")
            for e in errors:
                print(f"  {e['student_id']} {e['question_label']}: {e['warnings']}")
                print(f"    {e['answer'][:80]}")

        elif args.export:
            data = {
                "participants": pd.participants(),
                "responses": pd.responses("P001"),  # single example
                "summary": pd.summary(),
            }
            Path(args.export).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  [OK] Exported to {args.export}")

        else:
            pd.print_report()

    finally:
        pd.close()


if __name__ == "__main__":
    main()
