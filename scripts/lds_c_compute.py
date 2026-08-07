#!/usr/bin/env python3
"""
LinguaGraph — LDS-C Computation (concept-level, aligned via English gloss)

Computes LDS-C for the human eligible set (freeze SSOT) using LLM-extracted
concepts (lds_c_extract.py output), with:
  1. Cross-language alignment via normalized English gloss
  2. Per-topic and pooled LDS-C per language pair
  3. LDS-K concept-level (recomputed from aligned_data.json nodes) so
     ΔLDS = LDS-C − LDS-K uses the SAME metric (apples-to-apples)
  4. Bootstrap 95% CI (resample participants)
  5. Null models: within-language split-half (noise floor) + label permutation
  6. ΔLDS with Cohen's d / effect size

Usage:
    python scripts/lds_c_compute.py                          # latest extractions
    python scripts/lds_c_compute.py --input data/lds_c/extractions_20260807.json
    python scripts/lds_c_compute.py --iterations 1000

Output: outputs/lds_c_results_<date>.json
"""

import argparse
import json
import random
import re
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

RANDOM_SEED = 42
USE_FUZZY = False  # set True via --fuzzy (slower, marginal gain)
CANON_MAP: Dict[str, str] = {}  # gloss -> canonical_term, loaded via --canonical
TOPICS = ["Freiheit", "Gerechtigkeit", "Verantwortung", "Heimat", "Erfolg"]
PAIRS = [("ZH-EN", "zh", "en"), ("DE-EN", "de", "en"), ("ZH-DE", "zh", "de")]

DEFAULT_ALIGNED = PROJECT_ROOT / "data" / "math_extractions" / "merged" / "aligned_data.json"
DEFAULT_EXTRACTION = None  # resolved to latest in data/lds_c


def normalize(s: str) -> str:
    """Normalize an English gloss for matching."""
    if not s:
        return ""
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9 ]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# ── Improved alignment (v2): synonym map + stemmer + token dedup ──
# Word-level synonym canonicalization for the social-topic domain.
# Applied BEFORE stemming so "duties" -> "responsibility" directly.
SYNONYMS = {
    # responsibility cluster
    "duty": "responsibility", "duties": "responsibility", "obligation": "responsibility",
    "obligations": "responsibility", "accountability": "responsibility",
    # freedom cluster
    "liberty": "freedom", "free": "freedom",
    # home cluster
    "homeland": "home", "hometown": "home", "dwelling": "home", "domicile": "home",
    "house": "home", "residence": "home", "birthplace": "home",
    # safety cluster
    "security": "safety", "safe": "safety",
    # justice cluster
    "fairness": "justice", "fair": "justice",
    # success cluster
    "achievement": "success", "accomplishment": "success", "achieving": "success",
    # goal cluster
    "objective": "goal",
    # rights cluster
    "entitlement": "rights",
}

# Simple suffix-strip stemmer (no external deps). Applied AFTER synonym map.
_STEM_RULES = [("ies", "y"), ("sses", "ss"), ("xes", "x"), ("es", ""), ("s", "")]


def _stem(w: str) -> str:
    if len(w) <= 3:
        return w
    for suf, repl in _STEM_RULES:
        if w.endswith(suf) and len(w) > len(suf) + 2:
            return w[: -len(suf)] + repl
    for suf in ("ing", "ed", "ly"):
        if w.endswith(suf) and len(w) > len(suf) + 3:
            return w[: -len(suf)]
    return w


def canonical_key(s: str) -> str:
    """Canonical matching key for a gloss: synonym-map -> stem -> dedup -> sort.
    Handles slash-hedged glosses ('duty/obligation') via token dedup."""
    s = s.lower().strip()
    s = s.replace("/", " ")
    tokens = re.findall(r"[a-z0-9]+", s)
    canon = set()
    for t in tokens:
        t = SYNONYMS.get(t, t)
        canon.add(_stem(t))
    return " ".join(sorted(canon)) if canon else ""


def aligns_with(a_key: str, b_key: str, threshold: float = 0.88) -> bool:
    """Fuzzy fallback for near-identical canonical keys (e.g. typo variants).
    Uses difflib SequenceMatcher ratio."""
    if not a_key or not b_key:
        return False
    if a_key == b_key:
        return True
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a_key, b_key).ratio() >= threshold


def latest_extraction_path() -> Path:
    out_dir = PROJECT_ROOT / "data" / "lds_c"
    files = sorted(out_dir.glob("extractions_*.json"))
    if not files:
        raise FileNotFoundError(f"No extraction files in {out_dir}")
    return files[-1]


def load_extractions(path: Path) -> List[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("responses", [])


# ── Alignment & aggregation ────────────────────────────────

def response_concept_groups(record: dict) -> Dict[str, Set[str]]:
    """Map topic -> set of normalized English glosses for one response.
    Also includes a pooled set under 'ALL'."""
    per_topic: Dict[str, Set[str]] = {t: set() for t in TOPICS}
    for t in record.get("topics", []):
        topic_label = t.get("topic", "")
        if topic_label not in per_topic:
            # tolerate topic label mismatches
            topic_label = next((x for x in TOPICS if x.lower() in topic_label.lower()), None)
            if topic_label is None:
                continue
        for c in t.get("concepts", []):
            en = c.get("en", "")
            key = canonical_key(CANON_MAP.get(en, en))
            if key:
                per_topic[topic_label].add(key)
    pooled: Set[str] = set()
    for s in per_topic.values():
        pooled |= s
    per_topic["ALL"] = pooled
    return per_topic


def aggregate_languages(records: List[dict]) -> Dict[str, Dict[str, Set[str]]]:
    """lang -> (topic -> set of glosses), pooled across participants."""
    agg: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: defaultdict(set))
    for r in records:
        lang = r.get("language", "")
        groups = response_concept_groups(r)
        for topic, glosses in groups.items():
            agg[lang][topic] |= glosses
    return dict(agg)


def jaccard(a: Set[str], b: Set[str], use_fuzzy: bool = False) -> float:
    """Jaccard over canonical keys. Optional fuzzy fallback for near-misses."""
    a, b = set(a), set(b)
    inter = len(a & b)
    if use_fuzzy or USE_FUZZY:
        a_only = sorted(a - b)
        b_only = sorted(b - a)
        extra = 0
        used: Set[str] = set()
        for x in a_only:
            for y in b_only:
                if y in used:
                    continue
                if aligns_with(x, y):
                    extra += 1
                    used.add(y)
                    break
        inter += extra
    union = len(a | b)
    return inter / union if union else 0.0


def lds_concept(set_a: Set[str], set_b: Set[str]) -> float:
    return round(1.0 - jaccard(set_a, set_b), 4)


def compute_pairwise(agg: Dict[str, Dict[str, Set[str]]]) -> Dict[str, Dict[str, float]]:
    """pair -> (topic -> LDS-C)."""
    out = {}
    for pair, la, lb in PAIRS:
        if la not in agg or lb not in agg:
            continue
        out[pair] = {}
        topics = set(agg[la]) | set(agg[lb])
        for topic in topics:
            out[pair][topic] = lds_concept(agg[la].get(topic, set()), agg[lb].get(topic, set()))
    return out


# ── LDS-K concept-level (same metric as LDS-C) ─────────────

def load_lds_k_nodes(path: Path) -> Dict[str, Set[str]]:
    """Load language node sets from aligned_data.json (for LDS-K concept-level)."""
    aligned = json.loads(path.read_text(encoding="utf-8"))
    lang_nodes: Dict[str, Set[str]] = {"zh": set(), "en": set(), "de": set()}
    for g in aligned.get("aligned_groups", []):
        labels = g.get("labels", {})
        for lang in ["zh", "en", "de"]:
            label = labels.get(lang)
            if label:
                lang_nodes[lang].add(canonical_key(label))
    return lang_nodes


def compute_lds_k_concept(lang_nodes: Dict[str, Set[str]]) -> Dict[str, float]:
    out = {}
    for pair, la, lb in PAIRS:
        if la in lang_nodes and lb in lang_nodes:
            out[pair] = lds_concept(lang_nodes[la], lang_nodes[lb])
    return out


# ── Bootstrap CI (resample participants) ───────────────────

def bootstrap_ci(records: List[dict], n_iter: int = 1000) -> Dict[str, dict]:
    """Bootstrap pooled LDS-C CI by resampling participants with replacement."""
    random.seed(RANDOM_SEED)
    by_lang: Dict[str, List[dict]] = defaultdict(list)
    for r in records:
        by_lang[r.get("language", "")].append(r)

    pair_vals: Dict[str, List[float]] = defaultdict(list)
    for _ in range(n_iter):
        sample: List[dict] = []
        for lang, reps in by_lang.items():
            if not reps:
                continue
            for _ in range(len(reps)):
                sample.append(random.choice(reps))
        agg = aggregate_languages(sample)
        pairwise = compute_pairwise(agg)
        for pair, vals in pairwise.items():
            pair_vals[pair].append(vals.get("ALL", float("nan")))

    ci = {}
    for pair, vals in pair_vals.items():
        vals = [v for v in vals if v == v]  # drop NaN
        if len(vals) < 2:
            continue
        vals.sort()
        lo = vals[int(0.025 * len(vals))]
        hi = vals[int(0.975 * len(vals))]
        ci[pair] = {
            "lds_c_mean": round(statistics.mean(vals), 4),
            "ci_lower": round(lo, 4),
            "ci_upper": round(hi, 4),
            "std": round(statistics.stdev(vals), 4),
            "n_boot": len(vals),
        }
    return ci


# ── Null models ────────────────────────────────────────────

def within_language_split_half(records: List[dict], n_iter: int = 100) -> Dict[str, float]:
    """Noise floor from participant variability: for each language, randomly split
    participants into two halves, aggregate each half's concepts, compute LDS
    between the two aggregates. Average over iterations. This measures how much
    within-language participant variability inflates LDS (NOT a concept-set
    partition, which always yields LDS=1.0)."""
    random.seed(RANDOM_SEED)
    by_lang: Dict[str, List[dict]] = defaultdict(list)
    for r in records:
        by_lang[r.get("language", "")].append(r)

    pair_floors: Dict[str, List[float]] = defaultdict(list)
    for _ in range(n_iter):
        for pair, la, lb in PAIRS:
            if la not in by_lang or lb not in by_lang:
                continue
            vals = []
            for lang in [la, lb]:
                reps = by_lang[lang]
                if len(reps) < 2:
                    continue
                random.shuffle(reps)
                half = len(reps) // 2
                agg_a = aggregate_languages(reps[:half])
                agg_b = aggregate_languages(reps[half:])
                vals.append(lds_concept(agg_a.get(lang, {}).get("ALL", set()),
                                        agg_b.get(lang, {}).get("ALL", set())))
            if vals:
                pair_floors[pair].append(statistics.mean(vals))

    floors = {}
    for pair, vals in pair_floors.items():
        floors[pair] = round(statistics.mean(vals), 4)
    return floors


def label_permutation_null(records: List[dict], n_iter: int = 200) -> Dict[str, dict]:
    """Permute language labels across responses; if observed LDS differs from
    permuted distribution, labels carry signal."""
    random.seed(RANDOM_SEED)
    langs = [r.get("language", "") for r in records]
    if not langs:
        return {}
    pair_perm: Dict[str, List[float]] = defaultdict(list)
    for _ in range(n_iter):
        shuffled = langs[:]
        random.shuffle(shuffled)
        perm_records = [{**r, "language": l} for r, l in zip(records, shuffled)]
        agg = aggregate_languages(perm_records)
        pairwise = compute_pairwise(agg)
        for pair, vals in pairwise.items():
            pair_perm[pair].append(vals.get("ALL", float("nan")))
    out = {}
    for pair, vals in pair_perm.items():
        vals = [v for v in vals if v == v]
        if not vals:
            continue
        out[pair] = {
            "perm_mean": round(statistics.mean(vals), 4),
            "perm_std": round(statistics.stdev(vals), 4) if len(vals) > 1 else 0.0,
        }
    return out


def cohens_d_for_delta(delta_mean: float, delta_std: float, n_pairs: int) -> dict:
    d = abs(delta_mean) / max(delta_std, 0.001)
    return {"cohens_d": round(d, 4), "n_pairs": n_pairs}


# ── Report ─────────────────────────────────────────────────

def build_report(records: List[dict], extractions_path: Path, aligned_path: Path,
                 iterations: int) -> dict:
    agg = aggregate_languages(records)
    pairwise = compute_pairwise(agg)

    # LDS-K concept-level (same metric)
    lds_k_nodes = load_lds_k_nodes(aligned_path)
    lds_k_concept = compute_lds_k_concept(lds_k_nodes)

    # Bootstrap CI for pooled LDS-C
    ci = bootstrap_ci(records, iterations)

    # Null models
    split_half = within_language_split_half(records, max(100, iterations // 10))
    perm_null = label_permutation_null(records, max(200, iterations // 5))

    # ΔLDS (pooled LDS-C − LDS-K concept)
    delta = {}
    for pair in lds_k_concept:
        lc = ci.get(pair, {}).get("lds_c_mean")
        lk = lds_k_concept[pair]
        if lc is not None:
            delta[pair] = {"lds_c": lc, "lds_k": lk, "delta": round(lc - lk, 4)}

    # Language sizes
    sizes = defaultdict(int)
    for r in records:
        sizes[r.get("language", "")] += 1

    return {
        "generated_at": datetime.now().isoformat(),
        "model": "deepseek-v4-flash@opencode",
        "extraction_source": str(extractions_path),
        "n_responses": len(records),
        "language_sizes": dict(sizes),
        "lds_k_aligned_source": str(aligned_path),
        "per_topic_lds_c": pairwise,
        "pooled_lds_c": {p: v.get("ALL") for p, v in pairwise.items()},
        "lds_k_concept_level": lds_k_concept,
        "bootstrap_ci": ci,
        "delta_lds": delta,
        "null_models": {"within_language_split_half": split_half, "label_permutation": perm_null},
        "n_iterations": iterations,
    }


def format_table(report: dict) -> str:
    lines = []
    lines.append(f"{'Pair':8s} | {'LDS-C':7s} | {'95% CI':17s} | {'LDS-K':7s} | {'ΔLDS':7s} | {'d':6s} | {'split-half':10s}")
    lines.append("-" * 78)
    ci = report["bootstrap_ci"]
    delta = report["delta_lds"]
    split = report["null_models"]["within_language_split_half"]
    for pair in ["ZH-EN", "DE-EN", "ZH-DE"]:
        c = ci.get(pair, {})
        d = delta.get(pair, {})
        lc = c.get("lds_c_mean", "-")
        lc = f"{lc:.4f}" if isinstance(lc, float) else "-"
        cistr = f"[{c.get('ci_lower','-'):.4f}, {c.get('ci_upper','-'):.4f}]" if "ci_lower" in c else "-"
        lk = d.get("lds_k", "-")
        lk = f"{lk:.4f}" if isinstance(lk, float) else "-"
        dl = d.get("delta", "-")
        dl = f"{dl:+.4f}" if isinstance(dl, float) else "-"
        dd = abs(dl) if isinstance(dl, float) else "-"
        sh = split.get(pair)
        sh = f"{sh:.4f}" if isinstance(sh, float) else "-"
        lines.append(f"{pair:8s} | {lc:7s} | {cistr:17s} | {lk:7s} | {dl:7s} | {dd:6s} | {sh:10s}")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="LDS-C computation")
    ap.add_argument("--input", type=str, default=None)
    ap.add_argument("--aligned", type=str, default=None)
    ap.add_argument("--canonical", type=str, default=None,
                    help="LLM gloss->canonical mapping JSON (from lds_c_canonicalize.py)")
    ap.add_argument("--iterations", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=RANDOM_SEED)
    ap.add_argument("--fuzzy", action="store_true", help="Enable fuzzy matching (slower)")
    args = ap.parse_args()
    global USE_FUZZY, CANON_MAP
    USE_FUZZY = args.fuzzy
    if args.canonical:
        CANON_MAP = json.loads(Path(args.canonical).read_text(encoding="utf-8"))
        print(f"  Canonical map: {len(CANON_MAP)} glosses loaded")
    random.seed(RANDOM_SEED)

    path = Path(args.input) if args.input else latest_extraction_path()
    aligned_path = Path(args.aligned) if args.aligned else DEFAULT_ALIGNED
    print(f"  Extractions: {path}")
    print(f"  Aligned (LDS-K source): {aligned_path}")
    print(f"  Bootstrap iterations: {args.iterations}")

    records = load_extractions(path)
    print(f"  Loaded {len(records)} responses")

    report = build_report(records, path, aligned_path, args.iterations)
    print("\n" + format_table(report))

    out_dir = PROJECT_ROOT / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"lds_c_results_{datetime.now().strftime('%Y%m%d')}.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  [OK] Saved to {out_path}")


if __name__ == "__main__":
    main()
