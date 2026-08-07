"""
QC Checks — Individual validation functions for LinguaGraph survey data.

Three-tier outcome system:
    PASS   = No issues detected
    FLAG   = Ambiguous — needs manual review (short answer, fast duration, refusal phrase, potential duplicate)
    FAILED = Definite exclusion (gibberish/spam, no consent, missing response_id, corrupted data)

Each check implements:
    check(response: dict) -> CheckResult

CheckResult = {
    "check": str,       # Check name
    "passed": bool,     # True = PASS or FLAG; False = FAILED
    "reason": str,      # "passed" | "flag" | "failed"
    "detail": str,      # Human-readable explanation
}
"""

import re
from typing import Any, TypedDict


class CheckResult(TypedDict):
    check: str
    passed: bool
    reason: str  # "passed" | "flag" | "failed"
    detail: str


# ── Thresholds ──────────────────────────────────────────────
MIN_CHARS_PER_QUESTION = 50       # Minimum for paragraph answers (FLAG if below)
MIN_CHARS_5WORDS = 8              # Minimum for 5-word-list questions (FLAG if below)
MIN_DURATION_SECONDS = 60         # < 60s for 5 paragraphs = FLAG
MAX_DURATION_SECONDS = 7200       # > 2 hours = abandoned session (FLAG)
GIBBERISH_PATTERNS = [
    r'^(.)\1{5,}$',               # qqqqq, aaaaaaa, 啊啊啊啊啊啊
    r'^(qwer|asdf|zxcv|test|x{3,})$',  # Keyboard mash
    r'^\d{10,}$',                 # Pure digits
]
# Phrases indicating genuine refusal / non-response (FLAG, not FAILED —
# "I don't know" may express conceptual uncertainty, which is valid data
# in linguist research).
PHRASE_REFUSAL_FLAG = [
    "i don't know", "i dont know", "idk",
    "我不知道", "不会", "不清楚",
    "ich weiss nicht", "ich weiß nicht", "keine ahnung",
    "unsure", "not sure",
]
# Phrases indicating intentional refusal / non-participation (FAILED)
PHRASE_REFUSAL_FAIL = [
    "不想回答", "skip", "pass",
    "next", "none",
    "无", "没有",
]


# ── Helpers ─────────────────────────────────────────────────

def _get_responses(data: dict) -> list[dict[str, Any]]:
    """Extract the individual question responses from a survey submission."""
    raw = data.get("responses", data.get("answers", []))
    if isinstance(raw, list):
        return raw
    return []


def _get_full_text(data: dict) -> str:
    """Concatenate all response texts into one string."""
    parts = []
    for r in _get_responses(data):
        t = r.get("text", r.get("content", ""))
        if isinstance(t, str):
            parts.append(t)
    return "\n".join(parts)


def _check_gibberish(text: str) -> bool:
    """Return True if text looks like gibberish / spam (FAILED)."""
    if not isinstance(text, str) or not text.strip():
        return False
    for pat in GIBBERISH_PATTERNS:
        if re.search(pat, text.strip(), re.IGNORECASE):
            return True
    # Check for random keyboard patterns (e.g. "jjjjjjnnnnn")
    stripped = re.sub(r'\s+', '', text.strip())
    if len(stripped) >= 6 and len(set(stripped)) <= 2:
        return True
    return False


def _check_flag_phrase(text: str, phrases: list[str]) -> bool:
    """Return True if text matches a phrase from the given list."""
    if not isinstance(text, str):
        return False
    low = text.strip().lower()
    for phrase in phrases:
        if low == phrase or low.startswith(phrase + " ") or low.startswith(phrase + "."):
            return True
    return False


# ── 7 QC Checks ─────────────────────────────────────────────

def check_duplicate(data: dict, seen_ids: set | None = None) -> CheckResult:
    """C1: Potential duplicate detection.

    FLAG (not FAILED): A duplicate may be accidental re-submission or
    genuine identical response. Must be manually reviewed.
    """
    rid = data.get("response_id", "")
    issues = []
    if seen_ids is not None and rid in seen_ids:
        issues.append(f"Duplicate response_id: {rid}")

    passed = len(issues) == 0
    return {
        "check": "duplicate",
        "passed": passed,
        "reason": "passed" if passed else "flag",
        "detail": "; ".join(issues) if issues else "Unique response",
    }


def check_language(data: dict) -> CheckResult:
    """C2: Language field present and valid.

    FAILED: Missing or unsupported language = cannot assign to group.
    """
    lang = data.get("language", "").strip().lower()
    valid = {"zh", "de", "en", "chinese", "german", "english"}
    if not lang:
        return {"check": "language", "passed": False, "reason": "failed",
                "detail": "Missing language field"}
    lang_map = {"chinese": "zh", "german": "de", "english": "en"}
    normalized = lang_map.get(lang, lang)
    if normalized not in {"zh", "de", "en"}:
        return {"check": "language", "passed": False, "reason": "failed",
                "detail": f"Unsupported language: {lang}"}
    return {"check": "language", "passed": True, "reason": "passed",
            "detail": f"Language: {normalized}"}


def check_completeness(data: dict) -> CheckResult:
    """C3: How many of 5 topics answered.

    FAILED: 0-2 answered = likely abandoned.
    FLAG: 3-4 answered = partial completion, judge manually.
    PASS: All 5 answered.
    """
    responses = _get_responses(data)
    answered = sum(1 for r in responses if isinstance(r.get("text"), str) and r["text"].strip())
    total = len(responses) if responses else 5

    if answered == 0:
        return {"check": "completeness", "passed": False, "reason": "failed",
                "detail": "No questions answered"}
    if answered < total:
        ratio = answered / max(total, 1)
        if ratio < 0.6:  # 0-2 out of 5
            return {"check": "completeness", "passed": False, "reason": "failed",
                    "detail": f"Only {answered}/{total} questions answered"}
        else:  # 3-4 out of 5
            return {"check": "completeness", "passed": False, "reason": "flag",
                    "detail": f"Partial completion: {answered}/{total}"}
    return {"check": "completeness", "passed": True, "reason": "passed",
            "detail": f"All {total} questions answered"}


def check_min_length(data: dict) -> CheckResult:
    """C4: Per-question minimum length.

    FLAG (not FAILED): Short answers may reflect genuine conceptual
    minimalism, not low effort. Cannot automatically exclude.

    Two-tier threshold:
    - Word-list (5+ lines or comma-separated tokens): 8 chars
    - Paragraph: 50 chars
    - At least 3/5 should be paragraph-length (otherwise FLAG).
    """
    issues = []
    paragraph_count = 0
    for i, r in enumerate(_get_responses(data)):
        text = r.get("text", "").strip() if isinstance(r.get("text"), str) else ""
        topic = r.get("topic", f"Q{i+1}")

        if not text:
            issues.append(f"'{topic}' is empty")
            continue

        # Detect word-list: 3+ lines or comma-separated short tokens
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        is_word_list = len(lines) >= 3
        if not is_word_list:
            tokens = [t.strip() for t in text.replace("、", ",").split(",") if t.strip()]
            if len(tokens) >= 4 and all(len(t) < 15 for t in tokens):
                is_word_list = True

        threshold = MIN_CHARS_5WORDS if is_word_list else MIN_CHARS_PER_QUESTION
        if len(text) < threshold:
            issues.append(f"'{topic}' too short ({len(text)} < {threshold} chars)")
        elif len(text) >= MIN_CHARS_PER_QUESTION:
            paragraph_count += 1

    if paragraph_count < 3:
        issues.append(f"Only {paragraph_count}/5 meet paragraph length ({MIN_CHARS_PER_QUESTION} chars)")

    if issues:
        return {"check": "min_length", "passed": False, "reason": "flag",
                "detail": "; ".join(issues)}
    return {"check": "min_length", "passed": True, "reason": "passed",
            "detail": "All answers meet minimum length"}


def check_refusal(data: dict) -> CheckResult:
    """C5: Detect refusals and gibberish.

    FAILED: Gibberish/spam (qqqqq, asdf, etc.) = non-response.
    FLAG: "I don't know" phrases = may express conceptual uncertainty,
          a valid linguistic datum. Manual review required.

    This separation avoids systematically excluding participants who
    honestly report uncertainty — which is itself a meaningful response
    pattern in cross-linguistic research.
    """
    has_gibberish = False
    has_flag = False
    details = []

    for i, r in enumerate(_get_responses(data)):
        text = r.get("text", "").strip() if isinstance(r.get("text"), str) else ""
        topic = r.get("topic", f"Q{i+1}")
        if not text:
            continue
        if _check_gibberish(text):
            has_gibberish = True
            details.append(f"'{topic}' gibberish: '{text[:40]}'")
        elif _check_flag_phrase(text, PHRASE_REFUSAL_FAIL):
            has_gibberish = True
            details.append(f"'{topic}' refusal (fail): '{text[:40]}'")
        elif _check_flag_phrase(text, PHRASE_REFUSAL_FLAG):
            has_flag = True
            details.append(f"'{topic}' potential uncertainty: '{text[:40]}'")

    # Overall gibberish check
    full = _get_full_text(data)
    if full and _check_gibberish(full):
        has_gibberish = True
        details.append("Overall response appears to be spam/gibberish")

    if has_gibberish:
        return {"check": "refusal", "passed": False, "reason": "failed",
                "detail": "; ".join(details)}
    if has_flag:
        return {"check": "refusal", "passed": False, "reason": "flag",
                "detail": "; ".join(details)}
    return {"check": "refusal", "passed": True, "reason": "passed",
            "detail": "No refusals or gibberish detected"}


def check_duration(data: dict) -> CheckResult:
    """C6: Completion duration.

    FLAG (not FAILED): Fast completion may indicate premeditated
    responses rather than low effort. Slow completion may indicate
    an abandoned session. Both require context for judgment.
    """
    dur = data.get("duration_seconds", data.get("duration", 0))
    if not isinstance(dur, (int, float)) or dur <= 0:
        return {"check": "duration", "passed": True, "reason": "passed",
                "detail": "No duration data"}
    if dur < MIN_DURATION_SECONDS:
        return {"check": "duration", "passed": False, "reason": "flag",
                "detail": f"Fast completion: {dur}s (threshold: {MIN_DURATION_SECONDS}s)"}
    if dur > MAX_DURATION_SECONDS:
        return {"check": "duration", "passed": False, "reason": "flag",
                "detail": f"Very slow: {dur}s — may be abandoned session"}
    return {"check": "duration", "passed": True, "reason": "passed",
            "detail": f"Duration: {dur}s"}


def check_metadata(data: dict) -> CheckResult:
    """C7: Basic metadata integrity.

    FAILED: No consent or missing response_id = cannot include
    under any circumstances. These are hard exclusion criteria.
    """
    issues = []
    if not data.get("consent"):
        issues.append("No consent recorded")
    if not data.get("response_id"):
        issues.append("Missing response_id")
    if issues:
        return {"check": "metadata", "passed": False, "reason": "failed",
                "detail": "; ".join(issues)}
    return {"check": "metadata", "passed": True, "reason": "passed",
            "detail": "Metadata OK"}


# ── Composite ───────────────────────────────────────────────

ALL_CHECKS = [
    check_duplicate,
    check_language,
    check_completeness,
    check_min_length,
    check_refusal,
    check_duration,
    check_metadata,
]


def run_all_checks(data: dict, seen_ids: set | None = None,
                   seen_texts: dict[str, str] | None = None) -> list[CheckResult]:
    """Run all 7 QC checks against a single survey submission.

    seen_ids: set of previously seen response_ids (for duplicate detection).
    seen_texts: dict of {response_id: full_text} for text-level duplicate flags.
    """
    results = []
    for check_fn in ALL_CHECKS:
        if check_fn is check_duplicate:
            result = check_duplicate(data, seen_ids)
            # Text duplication check — FLAG level
            if result["reason"] == "passed" and seen_texts is not None:
                full = _get_full_text(data)
                for prev_id, prev_text in seen_texts.items():
                    if full and prev_text and len(full) > 50 and _text_similar(full, prev_text) > 0.95:
                        result = {
                            "check": "duplicate",
                            "passed": False,
                            "reason": "flag",
                            "detail": f"Text very similar to {prev_id} ({_text_similar(full, prev_text):.0%})"
                        }
                        break
        else:
            result = check_fn(data)
        results.append(result)
    return results


def _text_similar(a: str, b: str) -> float:
    """Simple text similarity (character overlap)."""
    if not a or not b:
        return 0.0
    set_a, set_b = set(a.strip()), set(b.strip())
    if not set_a and not set_b:
        return 1.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def classify(results: list[CheckResult]) -> tuple[str, list[str], list[str]]:
    """Classify a submission based on all check results.

    Returns:
        (status, failed_reasons, flag_reasons)
    where status is one of:
        "eligible"            — all checks PASSED
        "eligible_with_flags" — no FAILED, some FLAGs (manual review needed)
        "excluded"            — at least one FAILED
    """
    failed = [r for r in results if r["reason"] == "failed"]
    flags = [r for r in results if r["reason"] == "flag"]

    if failed:
        reasons = [f"{r['check']}: {r['detail']}" for r in failed]
        return "excluded", reasons, [f"{r['check']}: {r['detail']}" for r in flags]

    if flags:
        reasons = [f"{r['check']}: {r['detail']}" for r in flags]
        return "eligible_with_flags", [], reasons

    return "eligible", [], []


def needs_manual_review(results: list[CheckResult]) -> bool:
    """Check if this submission needs manual review (any FLAGs)."""
    return any(r["reason"] == "flag" for r in results)
