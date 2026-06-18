"""
Participant Management Module
==============================
CRUD operations for participant lifecycle in LinguaGraph human validation study.

Manages:
    - Participant registration (add, update, list)
    - Consent tracking (GDPR Art. 6, 7)
    - Anonymization pipeline (PII removal)
    - Status reporting (recruitment progress)

Usage:
    from participant_manager import ParticipantManager

    pm = ParticipantManager()
    pm.add_participant("S001", native_lang="zh", age_group="16-18", consent=True)
    pm.list_participants()
    pm.export_anonymized("pilot_001")

CLI:
    python participant_manager.py status
    python participant_manager.py add --id S001 --lang zh --consent
    python participant_manager.py list
    python participant_manager.py export-anonymized --batch pilot_001
"""

import csv
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from db_utils import get_connection, query, query_one, insert, upsert


# === Constants ===

REQUIRED_LANGUAGES = {"zh", "de", "en"}
TARGET_PER_LANGUAGE = 10
TARGET_TOTAL = 30

CONSENT_STATUS = {
    0: "pending",
    1: "granted",
    2: "withdrawn",
}


class ParticipantManager:
    """Manages participant lifecycle for the LinguaGraph human validation study."""

    def __init__(self, db_path: Optional[Path] = None):
        self.conn = get_connection()

    def close(self):
        self.conn.close()

    # ===== CRUD =====

    def add_participant(
        self,
        student_id: str,
        native_lang: str,
        age_group: str = "",
        school_lang: str = "",
        other_langs: str = "",
        years_in_germany: float = 0,
        consent: bool = False,
        notes: str = "",
    ) -> str:
        """
        Register a new participant or update existing.

        Args:
            student_id: e.g. "S001"
            native_lang: "zh", "de", or "en"
            age_group: e.g. "16-18"
            school_lang: language of schooling
            other_langs: comma-separated other languages
            years_in_germany: years living in Germany
            consent: whether consent has been granted
            notes: free-text notes

        Returns:
            student_id
        """
        if native_lang not in REQUIRED_LANGUAGES:
            raise ValueError(f"native_lang must be one of {REQUIRED_LANGUAGES}, got '{native_lang}'")

        student = {
            "student_id": student_id,
            "age_group": age_group,
            "native_lang": native_lang,
            "school_lang": school_lang or native_lang,
            "other_langs": other_langs,
            "years_in_germany": years_in_germany,
            "consent": 1 if consent else 0,
            "notes": notes,
        }

        upsert(self.conn, "students", student, "student_id")
        return student_id

    def update_consent(self, student_id: str, consent: bool) -> bool:
        """Update consent status for a participant."""
        row = query_one(self.conn, "SELECT student_id FROM students WHERE student_id = ?", (student_id,))
        if not row:
            return False

        self.conn.execute(
            "UPDATE students SET consent = ? WHERE student_id = ?",
            (1 if consent else 0, student_id),
        )
        self.conn.commit()
        return True

    def get_participant(self, student_id: str) -> Optional[Dict]:
        """Get a single participant by ID."""
        return query_one(self.conn, "SELECT * FROM students WHERE student_id = ?", (student_id,))

    def list_participants(self, native_lang: Optional[str] = None) -> List[Dict]:
        """List all participants, optionally filtered by language."""
        if native_lang:
            return query(
                self.conn,
                "SELECT * FROM students WHERE native_lang = ? ORDER BY student_id",
                (native_lang,),
            )
        return query(self.conn, "SELECT * FROM students ORDER BY student_id")

    def delete_participant(self, student_id: str) -> bool:
        """
        Remove a participant and all associated data.
        Use with caution — for GDPR right to erasure (Art. 17).
        """
        row = query_one(self.conn, "SELECT student_id FROM students WHERE student_id = ?", (student_id,))
        if not row:
            return False

        # Delete in order (foreign keys)
        self.conn.execute("DELETE FROM extractions WHERE response_id IN (SELECT response_id FROM responses WHERE student_id = ?)", (student_id,))
        self.conn.execute("DELETE FROM cross_language_analysis WHERE student_id = ?", (student_id,))
        self.conn.execute("DELETE FROM responses WHERE student_id = ?", (student_id,))
        self.conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        self.conn.commit()
        return True

    # ===== Status & Progress =====

    def get_recruitment_status(self) -> Dict:
        """
        Get recruitment progress toward target (30 participants).

        Returns dict with counts per language and overall progress.
        """
        students = self.list_participants()

        by_lang = {}
        for lang in REQUIRED_LANGUAGES:
            lang_students = [s for s in students if s["native_lang"] == lang]
            consented = [s for s in lang_students if s["consent"] == 1]
            by_lang[lang] = {
                "registered": len(lang_students),
                "consented": len(consented),
                "target": TARGET_PER_LANGUAGE,
            }

        total_registered = len(students)
        total_consented = sum(1 for s in students if s["consent"] == 1)

        return {
            "total_registered": total_registered,
            "total_consented": total_consented,
            "target_total": TARGET_TOTAL,
            "progress_pct": round(total_registered / TARGET_TOTAL * 100, 1),
            "consent_pct": round(total_consented / TARGET_TOTAL * 100, 1) if TARGET_TOTAL > 0 else 0,
            "by_language": by_lang,
            "ready_for_study": total_consented >= TARGET_TOTAL,
        }

    def get_response_status(self) -> Dict:
        """
        Get response collection progress per participant.

        Returns per-participant response counts and completion status.
        """
        students = self.list_participants()
        results = []

        for s in students:
            sid = s["student_id"]
            resp_count = query_one(
                self.conn,
                "SELECT COUNT(*) as cnt FROM responses WHERE student_id = ?",
                (sid,),
            )
            extraction_count = query_one(
                self.conn,
                "SELECT COUNT(*) as cnt FROM extractions e JOIN responses r ON e.response_id = r.response_id WHERE r.student_id = ?",
                (sid,),
            )

            n_resp = resp_count["cnt"] if resp_count else 0
            n_ext = extraction_count["cnt"] if extraction_count else 0

            # 5 topics x 3 languages = 15 expected responses
            results.append({
                "student_id": sid,
                "native_lang": s["native_lang"],
                "consent": CONSENT_STATUS.get(s["consent"], "unknown"),
                "responses": n_resp,
                "extractions": n_ext,
                "completion_pct": round(n_resp / 15 * 100, 1) if n_resp > 0 else 0,
            })

        return {
            "participants": results,
            "total_responses": sum(r["responses"] for r in results),
            "total_extractions": sum(r["extractions"] for r in results),
            "expected_total": TARGET_TOTAL * 15,
        }

    # ===== Anonymization =====

    def anonymize_response(self, response: Dict) -> Dict:
        """
        Remove PII from a response record.

        Removes: student_id (replaced with anonymous hash), timestamps.
        Keeps: language, question_id, answer text (needed for analysis).
        """
        anon = dict(response)

        # Hash student_id for anonymity
        if "student_id" in anon:
            raw_id = anon["student_id"]
            anon["anonymous_id"] = hashlib.sha256(raw_id.encode()).hexdigest()[:12]
            del anon["student_id"]

        # Remove timestamps
        for key in ["timestamp", "created_at", "updated_at"]:
            if key in anon:
                del anon[key]

        return anon

    def export_anonymized(self, batch_id: str = "default") -> Path:
        """
        Export all responses in anonymized format.

        Args:
            batch_id: Identifier for this export batch (e.g. "pilot_001")

        Returns:
            Path to the output JSONL file
        """
        responses = query(self.conn, """
            SELECT r.*, s.native_lang, s.age_group
            FROM responses r
            JOIN students s ON r.student_id = s.student_id
            ORDER BY r.student_id, r.language, r.question_id
        """)

        output_dir = Path(__file__).parent / "anonymized"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{batch_id}.jsonl"

        with open(output_path, "w", encoding="utf-8") as f:
            for resp in responses:
                anon = self.anonymize_response(dict(resp))
                f.write(json.dumps(anon, ensure_ascii=False) + "\n")

        print(f"  [OK] Exported {len(responses)} anonymized responses to {output_path}")
        return output_path

    # ===== Import from CSV =====

    def import_from_csv(self, csv_path: str, batch_id: str = "default") -> Dict:
        """
        Import participants from a Google Forms CSV export.

        Creates participant records and links responses.
        Uses the survey_pipeline.import_csv logic for parsing.

        Args:
            csv_path: Path to CSV file
            batch_id: Batch identifier

        Returns:
            Import statistics
        """
        csv_path = Path(csv_path)
        if not csv_path.exists():
            return {"error": f"File not found: {csv_path}"}

        # Delegate to survey_pipeline import
        sys.path.insert(0, str(Path(__file__).parent.parent / "survey_pipeline"))
        try:
            from import_csv import import_csv
            result = import_csv(str(csv_path))
            return result
        except ImportError:
            return {"error": "survey_pipeline.import_csv not available"}

    # ===== Reporting =====

    def print_status(self):
        """Print a formatted status report to stdout."""
        status = self.get_recruitment_status()
        resp_status = self.get_response_status()

        print(f"\n{'='*60}")
        print(f"  LinguaGraph — Participant Status")
        print(f"{'='*60}")
        print(f"  Registered: {status['total_registered']}/{status['target_total']} ({status['progress_pct']}%)")
        print(f"  Consented:  {status['total_consented']}/{status['target_total']} ({status['consent_pct']}%)")
        print(f"\n  By Language:")
        for lang, data in status["by_language"].items():
            bar = "#" * data["registered"] + "." * (TARGET_PER_LANGUAGE - data["registered"])
            print(f"    {lang}: [{bar}] {data['registered']}/{data['target']} (consented: {data['consented']})")
        print(f"\n  Responses: {resp_status['total_responses']}/{resp_status['expected_total']}")
        print(f"  Extractions: {resp_status['total_extractions']}")
        print(f"\n  Ready for study: {'YES' if status['ready_for_study'] else 'NO'}")
        print(f"{'='*60}\n")


# ===== CLI =====

def main():
    import argparse

    parser = argparse.ArgumentParser(description="LinguaGraph Participant Manager")
    sub = parser.add_subparsers(dest="command")

    # status
    sub.add_parser("status", help="Show recruitment status")

    # add
    add_p = sub.add_parser("add", help="Add a participant")
    add_p.add_argument("--id", required=True, help="Participant ID (e.g. S001)")
    add_p.add_argument("--lang", required=True, choices=["zh", "de", "en"], help="Native language")
    add_p.add_argument("--age", default="", help="Age group")
    add_p.add_argument("--school-lang", default="", help="Language of schooling")
    add_p.add_argument("--other-langs", default="", help="Other languages")
    add_p.add_argument("--years", type=float, default=0, help="Years in Germany")
    add_p.add_argument("--consent", action="store_true", help="Consent granted")
    add_p.add_argument("--notes", default="", help="Notes")

    # list
    list_p = sub.add_parser("list", help="List participants")
    list_p.add_argument("--lang", choices=["zh", "de", "en"], help="Filter by language")

    # export-anonymized
    exp_p = sub.add_parser("export-anonymized", help="Export anonymized responses")
    exp_p.add_argument("--batch", default="default", help="Batch ID")

    # delete
    del_p = sub.add_parser("delete", help="Delete a participant (GDPR Art. 17)")
    del_p.add_argument("--id", required=True, help="Participant ID")

    args = parser.parse_args()
    pm = ParticipantManager()

    try:
        if args.command == "status":
            pm.print_status()

        elif args.command == "add":
            pm.add_participant(
                student_id=args.id,
                native_lang=args.lang,
                age_group=args.age,
                school_lang=args.school_lang,
                other_langs=args.other_langs,
                years_in_germany=args.years,
                consent=args.consent,
                notes=args.notes,
            )
            print(f"  [OK] Participant {args.id} added ({args.lang})")

        elif args.command == "list":
            participants = pm.list_participants(native_lang=args.lang)
            if not participants:
                print("  No participants found.")
            else:
                print(f"\n  {'ID':<8} {'Lang':<5} {'Age':<8} {'Consent':<10} {'Notes'}")
                print(f"  {'-'*60}")
                for p in participants:
                    consent_str = CONSENT_STATUS.get(p["consent"], "?")
                    age_str = str(p.get('age_group') or '')
                    notes_str = str(p.get('notes') or '')
                    print(f"  {p['student_id']:<8} {p['native_lang']:<5} {age_str:<8} {consent_str:<10} {notes_str}")

        elif args.command == "export-anonymized":
            pm.export_anonymized(batch_id=args.batch)

        elif args.command == "delete":
            confirm = input(f"  Delete participant {args.id} and all associated data? [y/N]: ")
            if confirm.lower() == "y":
                if pm.delete_participant(args.id):
                    print(f"  [OK] Participant {args.id} deleted (GDPR Art. 17)")
                else:
                    print(f"  [ERROR] Participant {args.id} not found")
            else:
                print("  Cancelled.")

        else:
            parser.print_help()

    finally:
        pm.close()


if __name__ == "__main__":
    main()
