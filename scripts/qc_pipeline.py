#!/usr/bin/env python3
"""
LinguaGraph QC Pipeline — Quality Control + Dataset Freeze

Usage:
    # From CSV (Google Sheets export):
    python scripts/qc_pipeline.py --input data/raw/survey_export.csv --format csv

    # From JSON lines:
    python scripts/qc_pipeline.py --input data/raw/survey_data.jsonl --format jsonl

    # Dry run (no files written):
    python scripts/qc_pipeline.py --input data/raw/survey_export.csv --dry-run

    # Create freeze from validated data:
    python scripts/qc_pipeline.py --input data/raw/survey_export.csv --freeze

    # Full pipeline (validate + freeze + readiness check):
    python scripts/qc_pipeline.py --input data/raw/survey_export.csv --freeze --readiness

Output:
    freeze/freeze_<tag>/
        eligible.csv         — Passed all QC checks
        excluded.csv         — Failed at least one check (with reason)
        qc_report.json       — Full QC report (per-check stats)
        manifest.json        — Dataset metadata (provenance)
        checksum.txt         — SHA256 of all dataset files
        readiness.json       — Analysis Readiness Review (if --readiness)
"""

import argparse
import csv
import hashlib
import io
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# Add parent dir for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from qc_checks import run_all_checks, classify, needs_manual_review, ALL_CHECKS, _get_full_text


# ── Paths ───────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FREEZE_DIR = PROJECT_ROOT / "freeze"
RAW_DIR = PROJECT_ROOT / "data" / "raw"


# ── Data Loading ────────────────────────────────────────────

def load_csv(path: Path | str) -> list[dict]:
    """Load survey data from CSV (Google Sheets export).
    Expected columns: Timestamp, Response ID, Language, Duration (s), Q1-Q5, Raw JSON.
    """
    path = Path(path)
    records = []
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Try to parse Raw JSON column for full payload
            raw_json = row.get("Raw JSON", row.get("raw_json", ""))
            if raw_json and raw_json.strip():
                try:
                    parsed = json.loads(raw_json)
                    records.append(parsed)
                    continue
                except (json.JSONDecodeError, TypeError):
                    pass

            # Fallback: reconstruct from CSV columns
            lang = row.get("Language", row.get("language", "")).strip().lower()
            lang_map = {"chinese": "zh", "german": "de", "english": "en"}
            lang = lang_map.get(lang, lang)

            duration_str = row.get("Duration (s)", row.get("duration_seconds", "0"))
            try:
                duration = int(float(duration_str))
            except (ValueError, TypeError):
                duration = 0

            rid = row.get("Response ID", row.get("response_id", ""))
            ts = row.get("Timestamp", row.get("timestamp", ""))

            # Collect question texts (columns Q1-Q5 or custom names)
            q_texts = []
            for i in range(1, 6):
                for col_key in [f"Q{i}", f"q{i}", f"Q{i}:", f"Question {i}"]:
                    val = row.get(col_key)
                    if val:
                        q_texts.append(val.strip())
                        break
                else:
                    q_texts.append("")

            # Build structured record
            record = {
                "response_id": rid,
                "language": lang,
                "timestamp": ts,
                "duration_seconds": duration,
                "responses": [
                    {"topicIdx": i, "text": t, "topic": f"Topic {i}"}
                    for i, t in enumerate(q_texts)
                ],
                "consent": True,
                "metadata": {"survey_version": "unknown", "platform": "csv_import"},
            }
            records.append(record)

    return records


def load_jsonl(path: Path | str) -> list[dict]:
    """Load survey data from JSON lines file (one JSON object per line)."""
    path = Path(path)
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  [WARN] Skipping invalid JSON line: {e}")
    return records


def load_input(path: Path | str, fmt: str) -> list[dict]:
    """Load data from any supported format."""
    if fmt == "csv":
        return load_csv(path)
    elif fmt == "jsonl":
        return load_jsonl(path)
    else:
        raise ValueError(f"Unsupported format: {fmt}")


# ── QC Pipeline ─────────────────────────────────────────────

def run_qc(records: list[dict]) -> dict:
    """Run full QC pipeline on all records.
    Returns a dict with per-record results and aggregate stats.
    """
    seen_ids: set[str] = set()
    seen_texts: dict[str, str] = {}

    all_entries = []
    eligible = []          # PASS only
    eligible_with_flags = []  # PASS + FLAG (manual review needed)
    excluded = []          # at least one FAILED

    for record in records:
        rid = record.get("response_id", "unknown")
        chk_results = run_all_checks(record, seen_ids, seen_texts)

        # Track seen for downstream duplicate detection
        if rid:
            seen_ids.add(rid)
        full_text = _get_full_text(record)
        if full_text:
            seen_texts[rid] = full_text

        # Three-tier classification
        status, fail_reasons, flag_reasons = classify(chk_results)

        entry = {
            "response_id": rid,
            "language": record.get("language", ""),
            "timestamp": record.get("timestamp", record.get("start_time", "")),
            "duration_seconds": record.get("duration_seconds", record.get("duration", 0)),
            "checks": {c["check"]: c["reason"] for c in chk_results},
            "status": status,
            "failed_reasons": fail_reasons,
            "flag_reasons": flag_reasons,
            "record": record,
        }
        all_entries.append(entry)

        if status == "excluded":
            excluded.append(entry)
        elif status == "eligible_with_flags":
            eligible_with_flags.append(entry)
            eligible.append(entry)  # Included but flagged
        else:
            eligible.append(entry)

    total = len(records)
    n_eligible = len(eligible)
    n_eligible_clean = sum(1 for e in all_entries if e["status"] == "eligible")
    n_eligible_flags = len(eligible_with_flags)
    n_excluded = len(excluded)
    n_flags = sum(1 for e in all_entries if e["flag_reasons"])

    # Per-check stats (PASS / FLAG / FAILED)
    check_stats = {}
    for check_fn in ALL_CHECKS:
        name = check_fn.__name__.replace("check_", "")
        passed = sum(1 for e in all_entries if e["checks"].get(name) == "passed")
        flags = sum(1 for e in all_entries if e["checks"].get(name) == "flag")
        failed = sum(1 for e in all_entries if e["checks"].get(name) == "failed")
        check_stats[name] = {
            "passed": passed,
            "flag": flags,
            "failed": failed,
            "pass_rate": round(passed / total * 100, 1) if total > 0 else 0,
            "flag_rate": round(flags / total * 100, 1) if total > 0 else 0,
        }

    # Language distribution (eligible = clean + flagged)
    lang_dist: dict[str, int] = {}
    for e in eligible:
        lang = e.get("language", "unknown")
        lang_dist[lang] = lang_dist.get(lang, 0) + 1

    # Duration stats
    durations = [e["duration_seconds"] for e in eligible
                 if isinstance(e["duration_seconds"], (int, float)) and e["duration_seconds"] > 0]
    dur_stats = {}
    if durations:
        dur_stats = {
            "min": min(durations),
            "max": max(durations),
            "median": sorted(durations)[len(durations) // 2],
            "mean": round(sum(durations) / len(durations), 1),
        }

    report = {
        "qc_timestamp": datetime.now().isoformat(),
        "total_submitted": total,
        "eligible": n_eligible,
        "eligible_clean": n_eligible_clean,
        "eligible_with_flags": n_eligible_flags,
        "excluded_n": n_excluded,
        "needs_manual_review": n_flags > 0,
        "flagged_count": n_flags,
        "eligible_pct": round(n_eligible / total * 100, 1) if total > 0 else 0,
        "check_stats": check_stats,
        "language_distribution": lang_dist,
        "duration_stats": dur_stats,
        "flags": [],  # populated below
        "excluded": [  # list of excluded records with reasons
            {
                "response_id": e["response_id"],
                "language": e["language"],
                "reason": "; ".join(e.get("failed_reasons", [])),
                "checks": e["checks"],
            }
            for e in excluded
        ],
        "eligible_ids": [e["response_id"] for e in eligible],
    }

    # Rebuild flags list from structured data
    flag_entries = []
    for e in all_entries:
        for r_str in e.get("flag_reasons", []):
            check_name = r_str.split(":")[0] if ":" in r_str else "unknown"
            flag_entries.append({
                "response_id": e["response_id"],
                "language": e["language"],
                "check": check_name,
                "detail": r_str,
            })
    report["flags"] = flag_entries

    return report


# ── Freeze ──────────────────────────────────────────────────

def create_freeze(report: dict, records: list[dict], tag: str | None = None,
                  note: str = "") -> Path:
    """Create a frozen dataset snapshot."""
    if tag is None:
        tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    freeze_path = FREEZE_DIR / f"freeze_{tag}"
    freeze_path.mkdir(parents=True, exist_ok=True)

    # Filter records by eligibility
    eligible_ids = set(report["eligible_ids"])
    eligible_records = [r for r in records
                        if r.get("response_id", "") in eligible_ids]
    excluded_ids = set(e["response_id"] for e in report["excluded"])

    # Write eligible.csv
    csv_path = freeze_path / "eligible.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        # Flatten records to CSV rows
        writer = csv.writer(f)
        writer.writerow(["response_id", "language", "timestamp", "duration_seconds",
                         "q1", "q2", "q3", "q4", "q5", "exclude_reason"])
        for rec in eligible_records:
            responses = rec.get("responses", [])
            q_texts = [r.get("text", "") for r in responses[:5]]
            q_texts += [""] * (5 - len(q_texts))
            writer.writerow([
                rec.get("response_id", ""), rec.get("language", ""),
                rec.get("timestamp", ""), rec.get("duration_seconds", 0),
                *q_texts, "",
            ])

    # Write excluded.csv
    excl_path = freeze_path / "excluded.csv"
    with open(excl_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["response_id", "language", "timestamp", "duration_seconds",
                         "q1", "q2", "q3", "q4", "q5", "exclude_reason"])
        for rec in records:
            rid = rec.get("response_id", "")
            if rid in excluded_ids:
                ex = next((e for e in report["excluded"] if e["response_id"] == rid), {})
                responses = rec.get("responses", [])
                q_texts = [r.get("text", "") for r in responses[:5]]
                q_texts += [""] * (5 - len(q_texts))
                writer.writerow([
                    rid, rec.get("language", ""),
                    rec.get("timestamp", ""), rec.get("duration_seconds", 0),
                    *q_texts, ex.get("reason", ""),
                ])

    # Write qc_report.json
    report_path = freeze_path / "qc_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # Write manifest.json
    manifest = {
        "dataset": f"LinguaGraph LDS-C Freeze {tag}",
        "freeze_date": datetime.now().isoformat(),
        "freeze_tag": tag,
        "total_submitted": report["total_submitted"],
        "eligible_n": report["eligible"],
        "excluded_n": report["excluded"],
        "language_distribution": report["language_distribution"],
        "duration_stats": report.get("duration_stats", {}),
        "pipeline_version": "1.0",
        "qc_timestamp": report["qc_timestamp"],
        "note": note,
        "files": {
            "eligible": "eligible.csv",
            "excluded": "excluded.csv",
            "qc_report": "qc_report.json",
            "manifest": "manifest.json",
        },
    }
    manifest_path = freeze_path / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # Write checksums
    checksums = {}
    for fname in ["eligible.csv", "excluded.csv", "qc_report.json", "manifest.json"]:
        fpath = freeze_path / fname
        if fpath.exists():
            checksums[fname] = sha256_file(fpath)
    checksum_path = freeze_path / "checksum.txt"
    with open(checksum_path, "w") as f:
        for fname, chk in sorted(checksums.items()):
            f.write(f"{chk}  {fname}\n")

    # Write freeze_report.md (human-readable, Methods-section-ready)
    report_md = _generate_freeze_md(report, tag, note)
    md_path = freeze_path / "freeze_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(report_md)

    return freeze_path


def _generate_freeze_md(report: dict, tag: str, note: str) -> str:
    """Generate a human-readable freeze report (Methods-section-ready)."""
    lang_dist = report.get("language_distribution", {})
    dur = report.get("duration_stats", {})
    check_stats = report.get("check_stats", {})

    lines = []
    lines.append(f"# Dataset Freeze: {tag}")
    lines.append(f"")
    lines.append(f"**Freeze date**: {report.get('qc_timestamp', 'unknown')[:10]}")
    lines.append(f"**Pipeline version**: 1.0")
    lines.append(f"")
    if note:
        lines.append(f"**Note**: {note}")
        lines.append(f"")
    lines.append(f"## Summary")
    lines.append(f"")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total submitted | {report.get('total_submitted', 0)} |")
    lines.append(f"| Eligible (final) | {report.get('eligible', 0)} |")
    lines.append(f"|   Clean pass | {report.get('eligible_clean', 0)} |")
    lines.append(f"|   With flags (manual review) | {report.get('eligible_with_flags', 0)} |")
    lines.append(f"| Excluded | {report.get('excluded_n', 0)} |")
    lines.append(f"")
    lines.append(f"### Language distribution")
    lines.append(f"")
    lines.append(f"| Language | N |")
    lines.append(f"|----------|---|")
    for lang in sorted(lang_dist.keys()):
        lines.append(f"| {lang} | {lang_dist[lang]} |")
    lines.append(f"")
    if dur:
        lines.append(f"### Duration statistics (eligible, seconds)")
        lines.append(f"")
        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Median | {dur.get('median', 'N/A')} |")
        lines.append(f"| Mean | {dur.get('mean', 'N/A')} |")
        lines.append(f"| Range | {dur.get('min', 'N/A')} -- {dur.get('max', 'N/A')} |")
        lines.append(f"")
    lines.append(f"## QC Check Pass Rates")
    lines.append(f"")
    lines.append(f"| Check | Pass | Flag (review) | Failed | Pass rate |")
    lines.append(f"|-------|:----:|:-------------:|:------:|:---------:|")
    for name, stats in sorted(check_stats.items()):
        lines.append(f"| {name} | {stats['passed']} | {stats['flag']} | {stats['failed']} | {stats['pass_rate']}% |")
    lines.append(f"")
    lines.append(f"## Exclusion Reasons")
    lines.append(f"")
    for ex in report.get("excluded", []):
        lines.append(f"- [{ex['language']}] {ex['response_id']}: {ex['reason'][:120]}")
    lines.append(f"")
    if report.get("flags"):
        lines.append(f"## Items Flagged for Manual Review")
        lines.append(f"")
        for fl in report.get("flags", []):
            lines.append(f"- [{fl['language']}] {fl['response_id']} ({fl['check']}): {fl['detail'][:120]}")
        lines.append(f"")
    return "\n".join(lines)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ── Analysis Readiness Review ───────────────────────────────

def readiness_check(report: dict, freeze_path: Path) -> dict:
    """Check whether the frozen dataset is ready for formal analysis.

    Returns a dict of all checks with PASS/FAIL/WARN status.
    """
    checks = {}

    # RC1: Minimum sample size (eligible = clean + flagged)
    checks["minimum_n"] = {
        "status": "PASS" if report["eligible"] >= 20 else "FAIL",
        "detail": f"N={report['eligible']} (threshold: 20)",
    }

    # RC2: Language balance
    lang_dist = report.get("language_distribution", {})
    min_lang = min(lang_dist.values()) if lang_dist else 0
    checks["language_balance"] = {
        "status": "PASS" if min_lang >= 5 else "WARN",
        "detail": f"Min per language: {min_lang} (threshold: 5)",
    }

    # RC3: Exclusion rate
    excl_n = report.get("excluded_n", len(report.get("excluded", [])))
    excl_pct = excl_n / max(report["total_submitted"], 1) * 100
    checks["exclusion_rate"] = {
        "status": "PASS" if excl_pct < 25 else "WARN",
        "detail": f"{excl_pct:.1f}% excluded (threshold: <25%)",
    }

    # RC4: Manual review complete (all flags resolved)
    n_flags = len(report.get("flags", report.get("eligible_with_flags", 0)))
    checks["manual_review"] = {
        "status": "PASS" if n_flags == 0 else "WARN",
        "detail": f"{n_flags} items flagged for manual review",
    }

    # RC5: QC complete
    checks["qc_complete"] = {
        "status": "PASS" if report["eligible"] > 0 else "FAIL",
        "detail": f"{report['eligible']} eligible responses",
    }

    # RC6: Freeze integrity (checksums present)
    freeze_files = list(freeze_path.glob("*")) if freeze_path.exists() else []
    has_checksum = any(f.name == "checksum.txt" for f in freeze_files)
    checks["freeze_integrity"] = {
        "status": "PASS" if has_checksum else "FAIL",
        "detail": f"Freeze at {freeze_path.name}" if freeze_path.exists() else "No freeze directory",
    }

    # Overall
    statuses = [c["status"] for c in checks.values()]
    overall = "PASS" if all(s == "PASS" for s in statuses) else \
              "PASS_WITH_WARNINGS" if "WARN" in statuses and "FAIL" not in statuses else "FAIL"

    return {
        "timestamp": datetime.now().isoformat(),
        "overall": overall,
        "checks": checks,
        "freeze_path": str(freeze_path),
    }


# ── CLI ─────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="LinguaGraph QC Pipeline — Quality Control + Dataset Freeze")
    ap.add_argument("--input", "-i", type=str, required=True, help="Input data file")
    ap.add_argument("--format", "-f", choices=["csv", "jsonl"], default="csv",
                    help="Input format (default: csv)")
    ap.add_argument("--freeze", action="store_true", help="Create frozen dataset snapshot")
    ap.add_argument("--tag", type=str, default=None,
                    help="Freeze tag (default: auto-generated timestamp)")
    ap.add_argument("--dry-run", action="store_true", help="Run QC but don't write files")
    ap.add_argument("--readiness", action="store_true",
                    help="Run Analysis Readiness Review after freeze")
    ap.add_argument("--note", type=str, default="", help="Freeze description note")
    ap.add_argument("--output", "-o", type=str, default=None,
                    help="Output path for QC report JSON (default: stdout)")
    args = ap.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_path}")
        sys.exit(1)

    print("=" * 60)
    print("  LinguaGraph QC Pipeline")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Step 1: Load data
    print(f"\n[1/4] Loading data from {input_path} ({args.format})...")
    records = load_input(input_path, args.format)
    print(f"  Loaded {len(records)} records")

    if not records:
        print("  [WARN] No records found. Nothing to do.")
        sys.exit(0)

    # Step 2: Run QC
    print("\n[2/4] Running QC checks...")
    report = run_qc(records)

    print(f"\n  Total submitted:      {report['total_submitted']}")
    print(f"  Eligible (final):     {report['eligible']} ({report['eligible_pct']}%)")
    print(f"    Clean pass:         {report['eligible_clean']}")
    print(f"    With flags (review): {report['eligible_with_flags']}")
    print(f"  Excluded:             {report['excluded_n']}")

    print(f"\n  Per-check results [PASS/FLAG/FAIL]:")
    for name, stats in report["check_stats"].items():
        pass_bar = "#" * max(int(stats["pass_rate"] / 5), 0)
        flag_bar = "~" * max(int(stats["flag_rate"] / 5), 0)
        print(f"    {name:<15s} PASS={stats['passed']:3d}  FLAG={stats['flag']:3d}  FAIL={stats['failed']:3d}")

    print(f"\n  Language distribution (eligible):")
    for lang, count in sorted(report["language_distribution"].items()):
        print(f"    {lang}: {count}")

    print(f"\n  Excluded ({report['excluded_n']}):")
    for ex in report.get("excluded", [])[:10]:
        print(f"    [FAIL] [{ex['language']}] {ex['response_id']}: {ex['reason'][:80]}")
        if len(report.get("excluded", [])) > 10:
            print(f"    ... and {len(report.get('excluded', [])) - 10} more")

    if report.get("flags"):
        print(f"\n  Flagged for manual review ({len(report['flags'])}):")
        for fl in report["flags"][:8]:
            print(f"    [FLAG] [{fl['language']}] {fl['response_id']} ({fl['check']}): {fl['detail'][:60]}")
        if len(report["flags"]) > 8:
            print(f"    ... and {len(report['flags']) - 8} more")

    # Step 3: Freeze
    if args.freeze and not args.dry_run:
        print(f"\n[3/4] Creating freeze...")
        freeze_path = create_freeze(report, records, args.tag, args.note)
        print(f"  Freeze created at: {freeze_path}")
        print(f"  Files:")
        for f in sorted(freeze_path.iterdir()):
            size = f.stat().st_size
            print(f"    {f.name:20s} {size:>8,} bytes")

    elif args.dry_run:
        print(f"\n[3/4] DRY RUN — no files written")
        if args.freeze:
            print(f"  Would create freeze with tag: {args.tag or '<auto>'}")

    # Step 4: Readiness Review
    if args.readiness and args.freeze and not args.dry_run:
        print(f"\n[4/4] Analysis Readiness Review...")
        ready = readiness_check(report, freeze_path)
        status_icon = {"PASS": "[PASS]", "PASS_WITH_WARNINGS": "[WARN]", "FAIL": "[FAIL]"}
        print(f"  Overall: {status_icon.get(ready['overall'], '?')} {ready['overall']}")
        for name, check in ready["checks"].items():
            icon = {"PASS": "[OK]", "WARN": "[!]", "FAIL": "[X]"}
            print(f"    {icon.get(check['status'], '?')} {name:<25s} {check['detail']}")

        ready_path = freeze_path / "readiness.json"
        with open(ready_path, "w", encoding="utf-8") as f:
            json.dump(ready, f, ensure_ascii=False, indent=2)
        print(f"  Readiness report saved to {ready_path}")

    # Output
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n  QC report saved to {out_path}")

    print(f"\n{'='*60}")
    print("  QC Pipeline complete.")
    print(f"  {report['eligible']} eligible ({report['eligible_clean']} clean + {report['eligible_with_flags']} with flags).")
    if report.get("needs_manual_review"):
        tag_display = args.tag or datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"  [ACTION REQUIRED] {report['flagged_count']} items flagged for manual review.")
        if args.freeze:
            print(f"  Review freeze/freeze_{tag_display}/freeze_report.md then re-run readiness.")
    if report["eligible"] > 0:
        print(f"  {report['eligible']} responses ready for analysis.")
    else:
        print("  No eligible responses found.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
